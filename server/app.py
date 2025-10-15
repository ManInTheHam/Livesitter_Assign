import os
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
try:
    from bson.objectid import ObjectId
except ImportError:
    # Fallback for file database
    ObjectId = str
from dotenv import load_dotenv
from models import overlays
from ffmpeg_manager import FFmpegManager

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder=None)
CORS(app)  # enable CORS for all routes

# ---------- Base Directories ----------
BASE_DIR = Path(__file__).resolve().parent
HLS_DIR = BASE_DIR / "hls"
HLS_DIR.mkdir(exist_ok=True)

# ---------- FFmpeg Manager ----------
ff = FFmpegManager(base_dir=str(HLS_DIR))


@app.route("/")
def root():
    return {"message": "Flask RTSP → HLS backend running"}


# ---------- Streaming Endpoints ----------

@app.route("/api/streams/start", methods=["POST"])
def start_stream():
    data = request.get_json(force=True)
    rtsp_url = data.get("rtspUrl")
    stream_key = data.get("streamKey", "default")

    if not rtsp_url:
        return jsonify({"error": "rtspUrl is required"}), 400

    print(f"[Flask] Starting FFmpeg for '{stream_key}' with RTSP: {rtsp_url}")
    try:
        hls_rel = ff.start(rtsp_url, stream_key)
        print(f"[Flask] HLS will be written to: {HLS_DIR / stream_key}")
        return jsonify({
            "hlsPath": hls_rel,
            "status": ff.status(stream_key)
        })
    except Exception as e:
        print(f"[Flask] Error starting FFmpeg: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/streams/stop", methods=["POST"])
def stop_stream():
    data = request.get_json(force=True)
    stream_key = data.get("streamKey", "default")
    ff.stop(stream_key)
    return jsonify({"status": ff.status(stream_key)})


@app.route("/api/streams/status", methods=["GET"])
def stream_status():
    stream_key = request.args.get("streamKey", "default")
    return jsonify({"status": ff.status(stream_key)})


# ---------- HLS File Serving ----------

@app.route("/hls/<stream_key>/<path:filename>")
def serve_hls(stream_key, filename):
    """
    Serve HLS playlist (.m3u8) and segment (.ts) files
    from hls/<stream_key>/
    """
    stream_dir = HLS_DIR / stream_key
    file_path = stream_dir / filename

    if not file_path.exists():
        print(f"[Flask] HLS file not found: {file_path}")
        return jsonify({"error": f"Not found: {stream_key}/{filename}"}), 404

    # Explicit MIME handling
    if filename.endswith(".m3u8"):
        return send_from_directory(stream_dir, filename, mimetype="application/vnd.apple.mpegurl")
    elif filename.endswith(".ts"):
        return send_from_directory(stream_dir, filename, mimetype="video/mp2t")

    return send_from_directory(stream_dir, filename)


# ---------- Overlay CRUD ----------

def serialize(doc):
    if isinstance(doc.get("_id"), str):
        return doc  # Already serialized (file database)
    doc["_id"] = str(doc["_id"])
    return doc


@app.route("/api/overlays", methods=["POST"])
def create_overlay():
    data = request.get_json(force=True)
    result = overlays.insert_one(data)
    return jsonify({"_id": str(result.inserted_id), **data}), 201


@app.route("/api/overlays", methods=["GET"])
def list_overlays():
    user_id = request.args.get("userId")  # optional
    q = {"userId": user_id} if user_id else {}
    docs = [serialize(d) for d in overlays.find(q).sort("_id", -1)]
    return jsonify(docs)


@app.route("/api/overlays/<id>", methods=["PUT"])
def update_overlay(id):
    data = request.get_json(force=True)
    # Handle both MongoDB ObjectId and file database string IDs
    query_id = ObjectId(id) if ObjectId != str else id
    overlays.update_one({"_id": query_id}, {"$set": data})
    doc = overlays.find_one({"_id": query_id})
    return jsonify(serialize(doc))


@app.route("/api/overlays/<id>", methods=["DELETE"])
def delete_overl