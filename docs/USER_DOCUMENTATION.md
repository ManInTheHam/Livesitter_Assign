# 📡 StreamCast Pro - User Documentation

## Table of Contents

1. [Getting Started](#getting-started)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Using the Application](#using-the-application)
5. [RTSP Stream Setup](#rtsp-stream-setup)
6. [Overlay Management](#overlay-management)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)
9. [FAQ](#faq)

---

## 🚀 Getting Started

StreamCast Pro is a professional RTSP livestreaming application that allows you to:

- Convert RTSP streams to web-compatible HLS format
- Add dynamic text and image overlays to your streams
- Manage overlay presets for different streaming scenarios
- Monitor stream status in real-time

### Quick Start Checklist

- [ ] Install Python 3.8+ and Node.js 16+
- [ ] Install FFmpeg
- [ ] Set up MongoDB (Atlas, local, or Docker)
- [ ] Clone and configure the application
- [ ] Start backend and frontend servers
- [ ] Access the web interface at `http://localhost:3000`

---

## 💻 System Requirements

### Minimum Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux Ubuntu 18.04+
- **CPU**: Intel i3 or AMD equivalent (2+ cores)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Stable internet connection for RTSP streams

### Software Dependencies

- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **FFmpeg**: Latest stable version
- **MongoDB**: Atlas (cloud) or local installation
- **Docker**: Optional, for easy MongoDB setup

---

## 🛠️ Installation Guide

### Step 1: Install System Dependencies

#### Windows

1. **Python**: Download from [python.org](https://www.python.org/downloads/)
2. **Node.js**: Download from [nodejs.org](https://nodejs.org/)
3. **FFmpeg**:
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to your PATH environment variable
4. **Git**: Download from [git-scm.com](https://git-scm.com/)

#### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python node ffmpeg git
```

#### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install dependencies
sudo apt install python3 python3-pip nodejs npm ffmpeg git

# Install latest Node.js (optional)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/rtsp-overlay-app.git
cd rtsp-overlay-app
```

### Step 3: Set Up MongoDB

Choose one of the following options:

#### Option A: MongoDB Atlas (Recommended for beginners)

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free account
3. Create a new cluster (free tier available)
4. Create a database user with read/write permissions
5. Get your connection string
6. Update `server/.env` with your connection string

#### Option B: Docker (Easiest for local development)

```bash
# Install Docker Desktop from docker.com
# Then run:
docker-compose up -d mongodb

# MongoDB will be available at mongodb://localhost:27017
```

#### Option C: Local MongoDB Installation

1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Install and start the MongoDB service
3. MongoDB will be available at `mongodb://localhost:27017`

### Step 4: Configure Environment Variables

```bash
# Navigate to server directory
cd server

# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# For MongoDB Atlas:
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/rtsp_overlay_app

# For local MongoDB:
MONGO_URI=mongodb://localhost:27017/rtsp_overlay_app

# Use file database for testing (no MongoDB required):
USE_FILE_DB=true
```

### Step 5: Install Backend Dependencies

```bash
# In the server directory
cd server
pip install -r requirements.txt
```

### Step 6: Install Frontend Dependencies

```bash
# In the client directory
cd ../client
npm install
```

### Step 7: Start the Application

```bash
# Terminal 1: Start backend (from server directory)
cd server
python app.py

# Terminal 2: Start frontend (from client directory)
cd client
npm start
```

### Step 8: Access the Application

Open your web browser and navigate to:

- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:5000`

---

## 🎯 Using the Application

### Main Interface Overview

The StreamCast Pro interface consists of several key sections:

1. **Header**: Application branding and title
2. **Stream Configuration**: RTSP URL input and stream controls
3. **Video Player**: Live stream display with overlay preview
4. **Overlay Controls**: Tools for adding and managing overlays
5. **Preset Management**: Save and load overlay configurations

### Basic Workflow

1. **Configure Stream**: Enter your RTSP URL and stream key
2. **Start Streaming**: Click "Start Stream" to begin conversion
3. **Add Overlays**: Use overlay tools to add text or images
4. **Save Presets**: Save your overlay configuration for reuse
5. **Monitor Stream**: Watch live stream with real-time overlays

---

## 📺 RTSP Stream Setup

### Understanding RTSP URLs

RTSP (Real-Time Streaming Protocol) URLs typically follow this format:

```
rtsp://[username:password@]hostname[:port]/path
```

### Common RTSP URL Examples

#### IP Cameras

```
rtsp://192.168.1.100:554/stream1
rtsp://admin:password@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0
rtsp://192.168.1.100/axis-media/media.amp
```

#### Streaming Servers

```
rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4
rtsp://streaming.server.com:1935/live/stream_key
rtsp://rtsp.stream.com/live/channel1
```

#### OBS Studio RTSP Output

1. In OBS, go to **Settings > Stream**
2. Set **Service** to "Custom"
3. Set **Server** to your RTSP server URL
4. Use the complete RTSP URL in StreamCast Pro

### Testing RTSP Streams

Before using in StreamCast Pro, test your RTSP stream:

#### Using FFmpeg (Command Line)

```bash
# Test stream connectivity
ffmpeg -i rtsp://your-stream-url -t 10 -f null -

# Save a test video
ffmpeg -i rtsp://your-stream-url -t 30 -c copy test_output.mp4
```

#### Using VLC Media Player

1. Open VLC
2. Go to **Media > Open Network Stream**
3. Enter your RTSP URL
4. Click **Play**

### Stream Configuration in StreamCast Pro

1. **RTSP URL Field**: Enter your complete RTSP URL

   ```
   rtsp://192.168.1.100:554/stream1
   ```

2. **Stream Key Field**: Enter a unique identifier for your stream

   ```
   demo
   living_room_camera
   main_stream
   ```

3. **Click Start Stream**: The application will:
   - Validate the RTSP URL
   - Start FFmpeg conversion process
   - Generate HLS output
   - Display the live stream in the player

### Common RTSP Issues and Solutions

#### Connection Refused

- **Problem**: Cannot connect to RTSP server
- **Solutions**:
  - Check if the camera/server is online
  - Verify IP address and port
  - Check firewall settings
  - Ensure RTSP is enabled on the device

#### Authentication Failed

- **Problem**: Username/password incorrect
- **Solutions**:
  - Verify credentials
  - Check if special characters need URL encoding
  - Try accessing via web interface first

#### Stream Format Not Supported

- **Problem**: FFmpeg cannot process the stream
- **Solutions**:
  - Check camera codec settings
  - Try different resolution/bitrate
  - Update FFmpeg to latest version

---

## 🎨 Overlay Management

### Adding Text Overlays

1. **Click "+ Add Text"** in the overlay controls
2. **Position the Overlay**: Drag to desired location
3. **Resize**: Drag the corner handle to adjust size
4. **Customize Properties**:
   - Edit text content by modifying the overlay item
   - Change colors, fonts, and opacity
   - Adjust positioning with precision

### Text Overlay Properties

#### Content

- **Text**: Any UTF-8 text including emojis
- **Examples**: "🔴 LIVE", "Breaking News", "Stream Starting Soon"

#### Positioning (0.0 to 1.0 scale)

- **X**: Horizontal position (0 = left edge, 1 = right edge)
- **Y**: Vertical position (0 = top edge, 1 = bottom edge)
- **Width**: Overlay width as percentage of video width
- **Height**: Overlay height as percentage of video height

#### Styling

- **Font Size**: Size in pixels (12-72 recommended)
- **Color**: CSS color values (#ffffff, rgb(255,0,0), red)
- **Opacity**: Transparency (0.0 = invisible, 1.0 = opaque)
- **Z-Index**: Layer order (higher numbers appear on top)

### Adding Image Overlays

1. **Prepare Your Image**:

   - Supported formats: PNG, JPG, GIF, SVG
   - Recommended: PNG with transparency
   - Optimal size: 200x200 pixels or smaller

2. **Upload to Web Server** or use direct URL:

   ```
   https://your-server.com/logo.png
   https://i.imgur.com/your-image.png
   ```

3. **Add Image Overlay**:
   - Use the same positioning system as text
   - Images automatically scale to fit overlay bounds
   - Maintain aspect ratio with object-fit: contain

### Overlay Best Practices

#### Positioning Guidelines

- **Top-left corner**: Logo, live indicator
- **Top-right corner**: Time, viewer count
- **Bottom-left**: Channel name, social media
- **Bottom-right**: Sponsor logos
- **Center**: Temporary messages, alerts

#### Design Tips

- **High Contrast**: Ensure text is readable against video background
- **Text Shadow**: Use shadows for better visibility
- **Consistent Branding**: Use brand colors and fonts
- **Size Appropriately**: Don't cover important video content
- **Test on Different Content**: Verify overlays work with various backgrounds

### Managing Overlay Presets

#### Saving Presets

1. **Configure Overlays**: Set up all desired overlays
2. **Enter Preset Name**: Choose a descriptive name
   ```
   Gaming Stream Setup
   News Broadcast
   Product Demo
   ```
3. **Click "Save Preset"**: Stores configuration to database

#### Loading Presets

1. **Browse Saved Presets**: View all saved configurations
2. **Click "Apply"**: Instantly load overlay setup
3. **Modify as Needed**: Adjust loaded overlays if required

#### Preset Management

- **Edit**: Load preset, modify, and save with same name
- **Delete**: Remove unwanted presets
- **Duplicate**: Load preset, modify, save with new name
- **Share**: Export preset data for team collaboration

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'flask'`

```bash
# Solution: Install Python dependencies
cd server
pip install -r requirements.txt
```

**Error**: `MongoDB connection failed`

```bash
# Solution 1: Use file database for testing
# Edit server/.env:
USE_FILE_DB=true

# Solution 2: Start MongoDB with Docker
docker-compose up -d mongodb

# Solution 3: Check MongoDB Atlas credentials
# Verify MONGO_URI in server/.env
```

#### Frontend Won't Start

**Error**: `npm: command not found`

```bash
# Solution: Install Node.js
# Download from nodejs.org or use package manager
```

**Error**: `Module not found: Can't resolve 'react'`

```bash
# Solution: Install frontend dependencies
cd client
npm install
```

#### Stream Won't Load

**Error**: "Failed to load video stream"

```bash
# Check RTSP URL accessibility
ffmpeg -i your-rtsp-url -t 5 -f null -

# Verify FFmpeg installation
ffmpeg -version

# Check network connectivity
ping camera-ip-address
```

**Error**: "Stream connection failed"

- Verify RTSP URL format
- Check camera/server status
- Confirm network access
- Test with VLC player first

#### Overlay Issues

**Problem**: Overlays not saving

- Check MongoDB connection
- Verify database permissions
- Check browser console for errors

**Problem**: Overlays not positioning correctly

- Ensure video player is fully loaded
- Check overlay coordinates (0.0-1.0 range)
- Verify container dimensions

### Performance Optimization

#### Server Performance

```bash
# Monitor FFmpeg processes
ps aux | grep ffmpeg

# Check system resources
top
htop

# Monitor disk space (HLS files)
du -sh server/hls/
```

#### Client Performance

- **Close unused browser tabs**
- **Disable browser extensions**
- **Use Chrome or Firefox for best HLS support**
- **Check network bandwidth**

### Log Analysis

#### Backend Logs

```bash
# Run with verbose logging
cd server
python app.py

# Check for errors in output:
# - MongoDB connection issues
# - FFmpeg errors
# - API request failures
```

#### Frontend Logs

1. **Open Browser Developer Tools** (F12)
2. **Check Console Tab** for JavaScript errors
3. **Check Network Tab** for API request failures
4. **Monitor Performance Tab** for rendering issues

---

## ⚙️ Advanced Configuration

### Environment Variables

#### Server Configuration (server/.env)

```bash
# Database settings
USE_FILE_DB=false
MONGO_URI=mongodb://localhost:27017/rtsp_overlay_app

# FFmpeg settings (optional)
FFMPEG_PATH=/usr/local/bin/ffmpeg
HLS_SEGMENT_DURATION=2
HLS_PLAYLIST_SIZE=5

# Server settings
FLASK_ENV=development
FLASK_DEBUG=true
SERVER_PORT=5000
```

### FFmpeg Optimization

#### Low Latency Settings

```bash
# Edit ffmpeg_manager.py for custom FFmpeg parameters
ffmpeg_cmd = [
    'ffmpeg',
    '-i', rtsp_url,
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-g', '30',
    '-sc_threshold', '0',
    '-f', 'hls',
    '-hls_time', '1',
    '-hls_list_size', '3',
    '-hls_flags', 'delete_segments',
    output_path
]
```

#### Quality Settings

```bash
# High quality (higher CPU usage)
'-preset', 'slow'
'-crf', '18'

# Balanced (recommended)
'-preset', 'medium'
'-crf', '23'

# Low latency (lower quality)
'-preset', 'ultrafast'
'-crf', '28'
```

### Database Configuration

#### MongoDB Optimization

```javascript
// Create indexes for better performance
db.overlays.createIndex({ userId: 1 });
db.overlays.createIndex({ createdAt: -1 });
```

#### File Database Optimization

```python
# For high-frequency updates, consider SQLite
# Edit models.py to use SQLite instead of JSON
import sqlite3
```

### Security Considerations

#### Production Deployment

```bash
# Use environment variables for sensitive data
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/db"
export SECRET_KEY="your-secret-key"

# Enable HTTPS
# Use reverse proxy (nginx, Apache)
# Implement authentication
# Add rate limiting
```

#### CORS Configuration

```python
# Edit app.py for production CORS settings
CORS(app, origins=['https://yourdomain.com'])
```

---

## ❓ FAQ

### General Questions

**Q: Can I use StreamCast Pro for commercial purposes?**
A: Check the license file for usage terms. Generally, open-source projects allow commercial use with proper attribution.

**Q: What video formats are supported?**
A: Any format supported by FFmpeg, including H.264, H.265, VP8, VP9. Output is always HLS (H.264).

**Q: Can I stream to multiple platforms simultaneously?**
A: Currently, StreamCast Pro converts RTSP to HLS for web viewing. For multi-platform streaming, consider using OBS Studio with RTMP outputs.

### Technical Questions

**Q: Why use HLS instead of direct RTSP in browsers?**
A: Browsers don't natively support RTSP. HLS provides wide browser compatibility and adaptive bitrate streaming.

**Q: Can I add custom overlay types?**
A: Yes, modify the OverlayEditor component to support additional overlay types like shapes, animations, or widgets.

**Q: How do I reduce stream latency?**
A: Adjust FFmpeg parameters in ffmpeg_manager.py:

- Reduce HLS segment duration
- Use faster encoding presets
- Minimize buffer sizes

**Q: Can I run multiple streams simultaneously?**
A: Yes, use different stream keys for each stream. Monitor system resources as each stream requires CPU for encoding.

### Troubleshooting Questions

**Q: Stream works in VLC but not in StreamCast Pro**
A: Check FFmpeg compatibility with your stream format. Some proprietary codecs may not be supported.

**Q: Overlays disappear when I refresh the page**
A: Ensure MongoDB is connected and overlay presets are saved. Check browser console for API errors.

**Q: High CPU usage during streaming**
A: Adjust FFmpeg encoding settings for lower CPU usage:

- Use hardware acceleration if available
- Reduce video resolution/bitrate
- Use faster encoding presets

### Setup Questions

**Q: Do I need a powerful server for streaming?**
A: Requirements depend on:

- Number of concurrent streams
- Video resolution and bitrate
- Encoding settings
- A modern dual-core CPU can handle 1-2 HD streams

**Q: Can I use this with IP cameras?**
A: Yes, most IP cameras support RTSP output. Check your camera's documentation for the correct RTSP URL format.

**Q: How do I backup my overlay presets?**
A:

- **MongoDB**: Use mongodump/mongorestore
- **File Database**: Copy the overlays.json file
- **Manual**: Export presets via API and save JSON

---

## 📞 Support and Resources

### Getting Help

- **Documentation**: Check API and User documentation
- **Issues**: Create GitHub issues for bugs
- **Discussions**: Use GitHub discussions for questions
- **Community**: Join project Discord/Slack if available

### Useful Resources

- **FFmpeg Documentation**: [ffmpeg.org/documentation.html](https://ffmpeg.org/documentation.html)
- **MongoDB Docs**: [docs.mongodb.com](https://docs.mongodb.com/)
- **React Documentation**: [reactjs.org/docs](https://reactjs.org/docs/)
- **HLS Specification**: [tools.ietf.org/html/rfc8216](https://tools.ietf.org/html/rfc8216)

### Contributing

- **Bug Reports**: Include system info, logs, and reproduction steps
- **Feature Requests**: Describe use case and expected behavior
- **Code Contributions**: Follow project coding standards
- **Documentation**: Help improve guides and examples

---

**Last Updated**: October 15, 2025  
**Version**: 1.0.0  
**Compatibility**: Windows 10+, macOS 10.15+, Linux Ubuntu 18.04+
