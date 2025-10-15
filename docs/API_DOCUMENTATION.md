# API Documentation

## Overview

StreamCast Pro provides a RESTful API for managing RTSP streams and overlay configurations. The API is built with Flask and supports real-time streaming with dynamic overlay management.

**Base URL**: `http://localhost:5000`

---

## 🎥 Stream Management Endpoints

### Start Stream

**POST** `/api/streams/start`

Starts an RTSP stream conversion to HLS format.

#### Request Body

```json
{
  "rtspUrl": "rtsp://example.com:554/stream",
  "streamKey": "demo"
}
```

#### Parameters

- `rtspUrl` (string, required): The RTSP stream URL to convert
- `streamKey` (string, optional): Unique identifier for the stream (default: "default")

#### Response

```json
{
  "hlsPath": "/hls/demo/playlist.m3u8",
  "status": "running"
}
```

#### Status Codes

- `200 OK`: Stream started successfully
- `400 Bad Request`: Missing rtspUrl parameter
- `500 Internal Server Error`: FFmpeg error or stream unavailable

#### Example

```bash
curl -X POST http://localhost:5000/api/streams/start \
  -H "Content-Type: application/json" \
  -d '{
    "rtspUrl": "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4",
    "streamKey": "demo"
  }'
```

---

### Stop Stream

**POST** `/api/streams/stop`

Stops an active RTSP stream.

#### Request Body

```json
{
  "streamKey": "demo"
}
```

#### Parameters

- `streamKey` (string, optional): Stream identifier to stop (default: "default")

#### Response

```json
{
  "status": "stopped"
}
```

#### Example

```bash
curl -X POST http://localhost:5000/api/streams/stop \
  -H "Content-Type: application/json" \
  -d '{"streamKey": "demo"}'
```

---

### Stream Status

**GET** `/api/streams/status`

Gets the current status of a stream.

#### Query Parameters

- `streamKey` (string, optional): Stream identifier (default: "default")

#### Response

```json
{
  "status": "running" | "stopped" | "error"
}
```

#### Example

```bash
curl "http://localhost:5000/api/streams/status?streamKey=demo"
```

---

## 🎨 Overlay Management Endpoints

### Create Overlay Preset

**POST** `/api/overlays`

Creates a new overlay preset with multiple overlay items.

#### Request Body

```json
{
  "userId": "demo",
  "name": "Live Stream Overlay",
  "items": [
    {
      "type": "text",
      "content": "LIVE",
      "x": 0.02,
      "y": 0.02,
      "w": 0.12,
      "h": 0.08,
      "fontSize": 28,
      "color": "#ff4444",
      "opacity": 1,
      "z": 9
    },
    {
      "type": "image",
      "content": "https://example.com/logo.png",
      "x": 0.8,
      "y": 0.85,
      "w": 0.15,
      "h": 0.1,
      "opacity": 0.8,
      "z": 5
    }
  ]
}
```

#### Parameters

- `userId` (string, required): User identifier for organizing presets
- `name` (string, required): Display name for the overlay preset
- `items` (array, required): Array of overlay items

#### Overlay Item Properties

- `type` (string): "text" or "image"
- `content` (string): Text content or image URL
- `x` (number): Horizontal position (0-1, percentage of video width)
- `y` (number): Vertical position (0-1, percentage of video height)
- `w` (number): Width (0-1, percentage of video width)
- `h` (number): Height (0-1, percentage of video height)
- `fontSize` (number, text only): Font size in pixels
- `color` (string, text only): CSS color value
- `opacity` (number, optional): Transparency (0-1, default: 1)
- `z` (number, optional): Z-index for layering (default: 1)

#### Response

```json
{
  "_id": "507f1f77bcf86cd799439011",
  "userId": "demo",
  "name": "Live Stream Overlay",
  "items": [...],
  "createdAt": "2025-10-15T09:30:00Z"
}
```

#### Status Codes

- `201 Created`: Overlay preset created successfully
- `400 Bad Request`: Invalid request body or missing required fields
- `500 Internal Server Error`: Database error

#### Example

```bash
curl -X POST http://localhost:5000/api/overlays \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "demo",
    "name": "Gaming Stream",
    "items": [
      {
        "type": "text",
        "content": "🔴 LIVE",
        "x": 0.02,
        "y": 0.02,
        "w": 0.15,
        "h": 0.08,
        "fontSize": 32,
        "color": "#ff0000",
        "z": 10
      }
    ]
  }'
```

---

### List Overlay Presets

**GET** `/api/overlays`

Retrieves all overlay presets, optionally filtered by user.

#### Query Parameters

- `userId` (string, optional): Filter presets by user ID

#### Response

```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "userId": "demo",
    "name": "Live Stream Overlay",
    "items": [...],
    "createdAt": "2025-10-15T09:30:00Z"
  },
  {
    "_id": "507f1f77bcf86cd799439012",
    "userId": "demo",
    "name": "Gaming Overlay",
    "items": [...],
    "createdAt": "2025-10-15T09:25:00Z"
  }
]
```

#### Example

```bash
# Get all overlays
curl "http://localhost:5000/api/overlays"

# Get overlays for specific user
curl "http://localhost:5000/api/overlays?userId=demo"
```

---

### Update Overlay Preset

**PUT** `/api/overlays/{id}`

Updates an existing overlay preset.

#### URL Parameters

- `id` (string, required): Overlay preset ID

#### Request Body

```json
{
  "name": "Updated Overlay Name",
  "items": [
    {
      "type": "text",
      "content": "UPDATED LIVE",
      "x": 0.02,
      "y": 0.02,
      "w": 0.12,
      "h": 0.08,
      "fontSize": 30,
      "color": "#00ff00",
      "z": 9
    }
  ]
}
```

#### Response

```json
{
  "_id": "507f1f77bcf86cd799439011",
  "userId": "demo",
  "name": "Updated Overlay Name",
  "items": [...],
  "updatedAt": "2025-10-15T09:35:00Z"
}
```

#### Status Codes

- `200 OK`: Overlay updated successfully
- `404 Not Found`: Overlay preset not found
- `400 Bad Request`: Invalid request body

#### Example

```bash
curl -X PUT http://localhost:5000/api/overlays/507f1f77bcf86cd799439011 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Gaming Overlay",
    "items": [
      {
        "type": "text",
        "content": "🎮 GAMING LIVE",
        "x": 0.02,
        "y": 0.02,
        "w": 0.2,
        "h": 0.08,
        "fontSize": 28,
        "color": "#00ff88"
      }
    ]
  }'
```

---

### Delete Overlay Preset

**DELETE** `/api/overlays/{id}`

Deletes an overlay preset.

#### URL Parameters

- `id` (string, required): Overlay preset ID

#### Response

```json
{
  "ok": true
}
```

#### Status Codes

- `200 OK`: Overlay deleted successfully
- `404 Not Found`: Overlay preset not found

#### Example

```bash
curl -X DELETE http://localhost:5000/api/overlays/507f1f77bcf86cd799439011
```

---

## 📁 HLS File Serving

### Serve HLS Files

**GET** `/hls/{streamKey}/{filename}`

Serves HLS playlist and segment files for video playback.

#### URL Parameters

- `streamKey` (string): Stream identifier
- `filename` (string): HLS file name (.m3u8 or .ts)

#### Response

- **Content-Type**: `application/vnd.apple.mpegurl` for .m3u8 files
- **Content-Type**: `video/mp2t` for .ts files

#### Example

```bash
# Get playlist
curl "http://localhost:5000/hls/demo/playlist.m3u8"

# Get segment
curl "http://localhost:5000/hls/demo/segment001.ts"
```

---

## 🔧 Error Handling

### Error Response Format

```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "details": "Additional error details"
}
```

### Common Error Codes

- `RTSP_CONNECTION_FAILED`: Cannot connect to RTSP stream
- `FFMPEG_ERROR`: FFmpeg process error
- `INVALID_STREAM_KEY`: Stream key format invalid
- `OVERLAY_NOT_FOUND`: Overlay preset not found
- `DATABASE_ERROR`: MongoDB connection or query error
- `VALIDATION_ERROR`: Request validation failed

---

## 📊 Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting based on:

- IP address
- User ID
- API endpoint

---

## 🔐 Authentication

The current API does not implement authentication. For production deployment, consider adding:

- JWT token authentication
- API key authentication
- OAuth 2.0 integration

---

## 📝 Response Headers

All API responses include:

```
Content-Type: application/json
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## 🧪 Testing the API

### Using curl

```bash
# Test server status
curl http://localhost:5000/

# Start a test stream
curl -X POST http://localhost:5000/api/streams/start \
  -H "Content-Type: application/json" \
  -d '{"rtspUrl": "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4", "streamKey": "test"}'

# Create test overlay
curl -X POST http://localhost:5000/api/overlays \
  -H "Content-Type: application/json" \
  -d '{"userId": "test", "name": "Test Overlay", "items": [{"type": "text", "content": "TEST", "x": 0.1, "y": 0.1, "w": 0.2, "h": 0.1, "fontSize": 24, "color": "#ffffff"}]}'
```

### Using JavaScript (Frontend)

```javascript
// Start stream
const response = await fetch("http://localhost:5000/api/streams/start", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    rtspUrl: "rtsp://example.com/stream",
    streamKey: "demo",
  }),
});

// Create overlay
const overlayResponse = await fetch("http://localhost:5000/api/overlays", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    userId: "demo",
    name: "My Overlay",
    items: [
      {
        type: "text",
        content: "LIVE",
        x: 0.02,
        y: 0.02,
        w: 0.12,
        h: 0.08,
        fontSize: 28,
        color: "#ff4444",
      },
    ],
  }),
});
```

---

## 📋 API Changelog

### Version 1.0.0 (Current)

- Initial API implementation
- Stream management endpoints
- Overlay CRUD operations
- HLS file serving
- Basic error handling

---

For more information or support, please refer to the [User Documentation](USER_DOCUMENTATION.md) or create an issue in the project repository.
