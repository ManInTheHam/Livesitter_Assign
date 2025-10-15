import { useEffect, useRef, useState } from "react";
import Hls from "hls.js";

export default function VideoPlayer({ src }) {
  const ref = useRef(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const video = ref.current;
    if (!video || !src) return;

    setIsLoading(true);
    setError(null);
    let hls;

    const handleLoadStart = () => setIsLoading(true);
    const handleCanPlay = () => setIsLoading(false);
    const handleError = () => {
      setError("Failed to load video stream");
      setIsLoading(false);
    };

    video.addEventListener('loadstart', handleLoadStart);
    video.addEventListener('canplay', handleCanPlay);
    video.addEventListener('error', handleError);

    if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = src;
    } else if (Hls.isSupported()) {
      hls = new Hls({ 
        lowLatencyMode: true,
        backBufferLength: 90
      });
      
      hls.on(Hls.Events.ERROR, (event, data) => {
        if (data.fatal) {
          setError("Stream connection failed");
          setIsLoading(false);
        }
      });
      
      hls.loadSource(src);
      hls.attachMedia(video);
    }

    // Cleanup function to prevent memory leaks
    return () => {
      video.removeEventListener('loadstart', handleLoadStart);
      video.removeEventListener('canplay', handleCanPlay);
      video.removeEventListener('error', handleError);
      
      if (hls) {
        hls.destroy();
      }
    };
  }, [src]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      {isLoading && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          zIndex: 10,
          fontSize: '1.1rem'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', marginBottom: '10px' }}>⏳</div>
            Loading stream...
          </div>
        </div>
      )}
      
      {error && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(220, 38, 38, 0.9)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          zIndex: 10,
          fontSize: '1.1rem'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', marginBottom: '10px' }}>⚠️</div>
            {error}
          </div>
        </div>
      )}
      
      <video
        ref={ref}
        controls
        autoPlay
        muted
        style={{ 
          width: "100%", 
          height: "100%", 
          background: "#000",
          objectFit: "contain"
        }}
      />
    </div>
  );
}
