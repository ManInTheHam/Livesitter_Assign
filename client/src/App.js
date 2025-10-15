import { useEffect, useState } from "react";
import { API } from "./api";
import VideoPlayer from "./components/VideoPlayer";
import OverlayEditor from "./components/OverlayEditor";
import "./App.css";

export default function App() {
  const [rtspUrl, setRtspUrl] = useState("");
  const [streamKey, setStreamKey] = useState("demo");
  const [hlsUrl, setHlsUrl] = useState("");
  const [name, setName] = useState("My Overlay");
  const [items, setItems] = useState([
    { type: "text", content: "LIVE", x: 0.02, y: 0.02, w: 0.12, h: 0.08, fontSize: 28, color: "#ff4444", z: 9 },
  ]);
  const [saved, setSaved] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState("");

  const start = async () => {
    if (!rtspUrl.trim()) {
      setError("Please enter a valid RTSP URL");
      return;
    }
    
    setIsLoading(true);
    setError("");
    try {
      const { data } = await API.post("/api/streams/start", { rtspUrl, streamKey });
      const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:5000";
      setHlsUrl(`${apiUrl}${data.hlsPath}`);
      setIsStreaming(true);
    } catch (err) {
      setError("Failed to start stream. Please check your RTSP URL.");
    } finally {
      setIsLoading(false);
    }
  };

  const stop = async () => {
    setIsLoading(true);
    try {
      await API.post("/api/streams/stop", { streamKey });
      setHlsUrl("");
      setIsStreaming(false);
    } catch (err) {
      setError("Failed to stop stream");
    } finally {
      setIsLoading(false);
    }
  };

  const load = async () => {
    try {
      const { data } = await API.get("/api/overlays", { params: { userId: "demo" } });
      setSaved(data);
    } catch (err) {
      console.error("Failed to load overlays:", err);
    }
  };

  const save = async () => {
    if (!name.trim()) {
      setError("Please enter a preset name");
      return;
    }
    
    try {
      await API.post("/api/overlays", { userId: "demo", name, items });
      await load();
      setName("My Overlay");
      setError("");
    } catch (err) {
      setError("Failed to save overlay preset");
    }
  };

  const apply = (ov) => {
    setItems(ov.items);
    setError("");
  };

  const deletePreset = async (id) => {
    try {
      await API.delete(`/api/overlays/${id}`);
      await load();
    } catch (err) {
      setError("Failed to delete preset");
    }
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <h1 className="title">
              <span className="title-icon">📡</span>
              RTSP Livestream
            </h1>
            <p className="subtitle">Professional RTSP Livestreaming with Dynamic Overlays</p>
          </div>
        </header>

        {/* Error Display */}
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            {error}
            <button className="error-close" onClick={() => setError("")}>×</button>
          </div>
        )}

        {/* Stream Controls */}
        <div className="control-panel">
          <h2 className="section-title">Stream Configuration</h2>
          <div className="stream-controls">
            <div className="input-group">
              <label className="input-label">RTSP URL</label>
              <input 
                className="input-field rtsp-input"
                placeholder="rtsp://example.com:554/stream" 
                value={rtspUrl} 
                onChange={(e) => setRtspUrl(e.target.value)}
                disabled={isStreaming}
              />
            </div>
            <div className="input-group">
              <label className="input-label">Stream Key</label>
              <input 
                className="input-field"
                placeholder="demo" 
                value={streamKey} 
                onChange={(e) => setStreamKey(e.target.value)}
                disabled={isStreaming}
              />
            </div>
            <div className="button-group">
              <button 
                className={`btn btn-primary ${isLoading ? 'loading' : ''}`}
                onClick={start}
                disabled={isLoading || isStreaming}
              >
                {isLoading ? '⏳' : '▶️'} Start Stream
              </button>
              <button 
                className={`btn btn-secondary ${isLoading ? 'loading' : ''}`}
                onClick={stop}
                disabled={isLoading || !isStreaming}
              >
                {isLoading ? '⏳' : '⏹️'} Stop Stream
              </button>
            </div>
          </div>
        </div>

        {/* Video Player */}
        <div className="video-section">
          <div className="video-container">
            {hlsUrl ? (
              <>
                <VideoPlayer src={hlsUrl} />
                <OverlayEditor items={items} setItems={setItems} />
                <div className="stream-status">
                  <span className="live-indicator">🔴 LIVE</span>
                </div>
              </>
            ) : (
              <div className="video-placeholder">
                <div className="placeholder-content">
                  <div className="placeholder-icon">📹</div>
                  <h3>Ready to Stream</h3>
                  <p>Enter your RTSP URL above and click <strong>Start Stream</strong> to begin</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Overlay Presets */}
        <div className="overlay-section">
          <h2 className="section-title">Overlay Presets</h2>
          
          <div className="preset-controls">
            <div className="input-group">
              <input 
                className="input-field"
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                placeholder="Enter preset name" 
              />
            </div>
            <button className="btn btn-accent" onClick={save}>
              💾 Save Preset
            </button>
          </div>

          <div className="presets-grid">
            {saved.length === 0 ? (
              <div className="empty-state">
                <p>No saved presets yet. Create your first overlay preset!</p>
              </div>
            ) : (
              saved.map((ov) => (
                <div key={ov._id} className="preset-card">
                  <div className="preset-info">
                    <h4 className="preset-name">{ov.name}</h4>
                    <p className="preset-details">{ov.items?.length || 0} overlay(s)</p>
                  </div>
                  <div className="preset-actions">
                    <button 
                      className="btn btn-sm btn-primary" 
                      onClick={() => apply(ov)}
                    >
                      Apply
                    </button>
                    <button 
                      className="btn btn-sm btn-danger" 
                      onClick={() => deletePreset(ov._id)}
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              ))
            )}
 