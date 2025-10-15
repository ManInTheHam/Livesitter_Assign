import os
import shutil
import subprocess
import threading
import time
from pathlib import Path

class FFmpegManager:
    def __init__(self, base_dir: str = "hls"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.processes = {}  # streamKey -> Popen

    def hls_path(self, stream_key: str) -> Path:
        return self.base_dir / stream_key

    def _run_ffmpeg(self, cmd, stream_key):
        """Run FFmpeg command and track process."""
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True  # helps killing process group later
            )
        except FileNotFoundError:
            raise RuntimeError("FFmpeg not found on PATH. Please install ffmpeg.")
        self.processes[stream_key] = proc
        return proc

    def start(self, rtsp_url: str, stream_key: str, segment_time=2, with_audio=False):
        # Stop existing stream if any
        self.stop(stream_key)

        out_dir = self.hls_path(stream_key)
        try:
            if out_dir.exists():
                shutil.rmtree(out_dir)
        except Exception as e:
            print(f"Warning: Could not remove directory {out_dir}: {e}")
        out_dir.mkdir(parents=True, exist_ok=True)

        # Base FFmpeg command - try stream copy first
        cmd = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", rtsp_url,
            "-fflags", "nobuffer",
            "-flags", "low_delay",
            "-c:v", "copy",
            "-f", "hls",
            "-hls_time", str(segment_time),
            "-hls_list_size", "6",
            "-hls_flags", "delete_segments+append_list",
            "-hls_segment_filename", str(out_dir / "seg_%03d.ts"),
            str(out_dir / "index.m3u8"),
        ]

        if not with_audio:
            cmd.insert(-3, "-an")  # disable audio if requested

        proc = self._run_ffmpeg(cmd, stream_key)

        # Spawn a thread to monitor process and restart with re-encoding on quick failure
        def monitor():
            time.sleep(5)  # wait a bit to detect quick failure
            if proc.poll() is not None:
                # Process exited early; retry with re-encoding
                print(f"Stream copy failed for {stream_key}, retrying with re-encoding...")
                self.stop(stream_key)
                reencode_cmd = [
                    "ffmpeg",
                    "-rtsp_transport", "tcp",
                    "-i", rtsp_url,
                    "-fflags", "nobuffer",
                    "-flags", "low_delay",
                    "-c:v", "libx264",
                    "-preset", "veryfast",
                    "-f", "hls",
                    "-hls_time", str(segment_time),
                    "-hls_list_size", "6",
                    "-hls_flags", "delete_segments+append_list",
                    "-hls_segment_filename", str(out_dir / "seg_%03d.ts"),
                    str(out_dir / "index.m3u8"),
                ]
                if not with_audio:
                    reencode_cmd.insert(-3, "-an")
                self._run_ffmpeg(reencode_cmd, stream_key)

        threading.Thread(target=monitor, daemon=True).start()

        return f"/hls/{stream_key}/index.m3u8"

    def stop(self, stream_key: str):
        proc = self.processes.pop(stream_key, None)
        if proc and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                proc.kill()

    def status(self, stream_key: str) -> str:
        proc = self.processes.get(stream_key)
        if proc is None:
            return "stopped"
        return "running" if proc.poll() is None else "stopped"
