# 📡 StreamCast Pro - RTSP Overlay App

**Professional RTSP livestreaming with dynamic overlays and modern web interface.**

## ✨ Features

- 🎥 Live RTSP stream playback via HLS in browser
- 🎨 Interactive overlay editor with drag & drop
- 💾 Persistent overlay presets with MongoDB
- 🎛️ Professional streaming controls
- 📱 Responsive modern UI design
- ⚡ Real-time stream management

---

## 🏗️ File Structure

```
rtsp-overlay-app/
├─ server/
│  ├─ app.py              # Flask backend
│  ├─ ffmpeg_manager.py   # FFmpeg stream handling
│  ├─ models.py           # MongoDB models
│  ├─ requirements.txt    # Python dependencies
│  ├─ .env               # Environment variables
│  └─ hls/               # HLS output (auto-created)
├─ client/               # React frontend
│  ├─ package.json
│  ├─ public/
│  │  └─ index.html
│  └─ src/
│     ├─ App.js          # Main application
│     ├─ App.css         # Modern styling
│     ├─ api.js          # API client
│     └─ components/
│        ├─ VideoPlayer.js    # HLS video player
│        └─ OverlayEditor.js  # Drag & drop overlays
├─ docker-compose.yml    # MongoDB setup
└─ setup_mongodb.py      # Setup helper script
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **FFmpeg** (must be in system PATH)
- **MongoDB** (see setup options below)

### 1. MongoDB Setup (Required)

Choose one of these options:

#### Option A: Docker (Recommended)

```bash
# Run the setup helper
python setup_mongodb.py

# Or manually with Docker
docker-compose up -d mongodb
```

#### Option B: MongoDB Atlas (Cloud)

1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Update `server/.env` with your connection string

#### Option C: Local Installation

1. Install [MongoDB Community](https://www.mongodb.com/try/download/community)
2. Start MongoDB service
3. Use default connection in `server/.env`

### 2. Backend Setup

```bash
cd server
pip install -r requirements.txt
python app.py
```

### 3. Frontend Setup

```bash
cd client
npm install
npm start
```

### 4. Access the App

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:5000](http://localhost:5000)
- **MongoDB UI** (if using Docker): [http://localhost:8081](http://localhost:8081)

---

## Usage

- Open your browser at [http://localhost:3000](http://localhost:3000)
- Enter an RTSP URL or stream key.
- View live stream, add overlays (logo/text), and manage them via overlay editor.
- Overlay settings are persistent via the server API.

---

## Notes

- HLS output folders are auto-created in `server/hls/` and served by the backend.
- Overlays are managed with CRUD operations via API calls between the client and server.
- FFmpeg is required for stream conversion.

---

This app lets you quickly publish, view, and personalize RTSP livestreams with overlays—all from a modern web interface.

---

## 🎯 Usage

1. **Start Streaming**

   - Enter your RTSP URL (e.g., `rtsp://example.com:554/stream`)
   - Set a stream key (default: "demo")
   - Click "Start Stream"

2. **Add Overlays**

   - Click "+ Add Text" to create text overlays
   - Drag and resize overlays on the video
   - Customize text, colors, and positioning

3. **Save Presets**

   - Name your overlay configuration
   - Click "Save Preset" to store in MongoDB
   - Apply saved presets anytime

4. **Manage Stream**
   - Use "Stop Stream" to end streaming
   - Monitor live status indicator
   - View real-time stream feedback

---

## 🔧 Configuration

### Environment Variables (server/.env)

```bash
# MongoDB connection
MONGO_URI=mongodb://localhost:27017/rtsp_overlay_app

# For MongoDB Atlas:
# MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/rtsp_overlay_app
```

### FFmpeg Requirements

- Ensure FFmpeg is installed and in your system PATH
- Test with: `ffmpeg -version`
- Download from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

---

## 🐛 Troubleshooting

### MongoDB Connection Issues

```bash
# Check if MongoDB is running
python setup_mongodb.py

# Test connection
python -c "from server.models import overlays; print('✅ MongoDB connected')"
```

### FFmpeg Issues

```bash
# Test FFmpeg installation
ffmpeg -version

# Check if FFmpeg can access your RTSP stream
ffmpeg -i rtsp://your-stream-url -t 10 -f null -
```

### Stream Not Loading

- Verify RTSP URL is accessible
- Check firewall settings
- Ensure stream format is supported
- Monitor browser console for errors

---

## 🎨 Features Showcase

- **Modern UI**: Gradient backgrounds, smooth animations, professional design
- **Real-time Overlays**: Drag & drop interface with live preview
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Error Handling**: Graceful error messages and loading states
- **Persistent Storage**: MongoDB integration for overlay presets
- **Professional Controls**: Stream management with visual feedback

---

This professional streaming solution transforms RTSP feeds into interactive web experiences with dynamic overlays and modern interface design.

---

## 📚 Documentation

### For Users

- **[User Documentation](docs/USER_DOCUMENTATION.md)** - Complete setup and usage guide
- **[Installation Guide](docs/USER_DOCUMENTATION.md#installation-guide)** - Step-by-step setup instructions
- **[RTSP Stream Setup](docs/USER_DOCUMENTATION.md#rtsp-stream-setup)** - How to configure your streams
- **[Overlay Management](docs/USER_DOCUMENTATION.md#overlay-management)** - Creating and managing overlays
- **[Troubleshooting](docs/USER_DOCUMENTATION.md#troubleshooting)** - Common issues and solutions

### For Developers

- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete REST API reference
- **[Stream Endpoints](docs/API_DOCUMENTATION.md#stream-management-endpoints)** - Start/stop/status operations
- **[Overlay CRUD](docs/API_DOCUMENTATION.md#overlay-management-endpoints)** - Create, read, update, delete overlays
- **[Error Handling](docs/API_DOCUMENTATION.md#error-handling)** - Error codes and responses

---

## 🎯 Quick Examples

### Start a Stream via API

```bash
curl -X POST http://localhost:5000/api/streams/start \
  -H "Content-Type: application/json" \
  -d '{
    "rtspUrl": "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4",
    "streamKey": "demo"
  }'
```

### Create an Overlay Preset

```bash
curl -X POST http://localhost:5000/api/overlays \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "demo",
    "name": "Live Stream Overlay",
    "items": [{
      "type": "text",
      "content": "🔴 LIVE",
      "x": 0.02, "y": 0.02, "w": 0.15, "h": 0.08,
      "fontSize": 32, "color": "#ff0000"
    }]
  }'
```

### Test RTSP Stream

```bash
# Test with FFmpeg
ffmpeg -i rtsp://your-stream-url -t 10 -f null -

# Test with VLC
vlc rtsp://your-stream-url
```

---

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   RTSP Source   │───▶│   StreamCast Pro │───▶│   Web Browser   │
│  (IP Camera,    │    │                  │    │                 │
│   OBS, etc.)    │    │  ┌─────────────┐ │    │  ┌─────────────┐│
└─────────────────┘    │  │   FFmpeg    │ │    │  │ HLS Player  ││
                       │  │ Converter   │ │    │  │ + Overlays  ││
┌─────────────────┐    │  └─────────────┘ │    │  └─────────────┘│
│    MongoDB      │◀───│                  │    └─────────────────┘
│  (Overlays DB)  │    │  ┌─────────────┐ │
└─────────────────┘    │  │   Flask     │ │
                       │  │   API       │ │
                       │  └─────────────┘ │
                       │                  │
                       │  ┌─────────────┐ │
                       │  │   React     │ │
                       │  │   Frontend  │ │
                       │  └─────────────┘ │
                       └──────────────────┘
```

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/rtsp-overlay-app.git

# Install dependencies
cd server && pip install -r requirements.txt
cd ../client && npm install

# Start development servers
npm run dev  # Starts both backend and frontend
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FFmpeg** - Powerful multimedia framework
- **React** - Frontend framework
- **Flask** - Python web framework
- **MongoDB** - Database solution
- **HLS.js** - JavaScript HLS player
- **React-RnD** - Drag and drop components

---

**Built with ❤️ for the streaming community**
