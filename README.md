# AI CCTV Surveillance System

Real-time AI-powered CCTV surveillance web application with fire/smoke detection and human fall detection using YOLOv8.

## Features

- **Fire & Smoke Detection** - Custom YOLOv8 model (train locally on your PC)
- **Human Fall Detection** - YOLOv8 person detection + aspect ratio logic with time-based confirmation
- **Live Video Streaming** - Real-time MJPEG stream with detection overlays
- **Web Dashboard** - Dark modern security-style UI built with React + Tailwind CSS
- **Alert System** - Real-time alerts with severity levels and acknowledgment
- **Event Logging** - Timestamped event logs for all detections
- **Statistics** - Charts and analytics for detection data
- **Camera Management** - Monitor camera status and configuration
- **Telegram Alerts** - Optional notification integration (placeholder included)

## Folder Structure

```
ai-cctv-surveillance/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py             # FastAPI application entry point
│   │   ├── camera_manager.py   # Video capture management
│   │   ├── alert_manager.py    # Alert & event storage
│   │   ├── notifications.py    # Telegram alert placeholder
│   │   ├── detectors/
│   │   │   ├── fire_detector.py    # YOLOv8 fire/smoke detection
│   │   │   └── fall_detector.py    # YOLOv8 fall detection
│   │   ├── models/
│   │   │   └── schemas.py      # Pydantic data models
│   │   └── routers/
│   │       ├── video.py        # Video streaming endpoints
│   │       └── alerts.py       # Alerts/events/stats API
│   ├── models/                 # Place trained model files here
│   │   └── .gitkeep
│   ├── training/
│   │   ├── train_fire_model.py # Fire model training script
│   │   └── README_TRAINING.md  # Step-by-step training guide
│   ├── .env                    # Backend configuration
│   └── pyproject.toml          # Python dependencies
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.tsx             # Main application
│   │   ├── components/
│   │   │   ├── Sidebar.tsx     # Navigation sidebar
│   │   │   ├── LiveFeed.tsx    # Live video feed page
│   │   │   ├── AlertsPanel.tsx # Alerts dashboard
│   │   │   ├── EventLogs.tsx   # Event log viewer
│   │   │   ├── CameraPanel.tsx # Camera status panel
│   │   │   ├── StatsCards.tsx  # Statistics cards
│   │   │   └── StatsPage.tsx   # Statistics charts page
│   │   ├── hooks/
│   │   │   └── useApi.ts       # API hooks with auto-polling
│   │   ├── types/
│   │   │   └── index.ts        # TypeScript type definitions
│   │   └── index.css           # Global styles (dark theme)
│   ├── .env                    # Frontend configuration
│   └── package.json            # Node.js dependencies
└── README.md                   # This file
```

## Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **pip** and **npm**
- **Webcam** or IP camera (optional - shows "No Signal" placeholder without camera)

For fire model training (optional):
- **GPU with CUDA** recommended (CPU works but is slower)
- **ultralytics** package (included in backend dependencies)

## Setup Instructions

### 1. Clone & Setup Backend

```bash
cd ai-cctv-surveillance/backend

# Install Python dependencies
pip install poetry
poetry install

# Start the backend server
poetry run fastapi dev app/main.py
```

The backend runs at `http://localhost:8000`.

**API Documentation:** Visit `http://localhost:8000/docs` for interactive Swagger UI.

### 2. Setup Frontend

```bash
cd ai-cctv-surveillance/frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The frontend runs at `http://localhost:5173`.

### 3. Open the Dashboard

Open `http://localhost:5173` in your browser to see the surveillance dashboard.

## Configuration

### Backend (.env)

```env
# Video source
VIDEO_SOURCE=0                    # 0 = webcam, or RTSP URL, or video file path

# Fire detection (after training)
FIRE_MODEL_PATH=models/fire_best.pt
FIRE_CONFIDENCE_THRESHOLD=0.6

# Fall detection
FALL_DURATION_THRESHOLD=1.5       # Seconds before confirming fall
FALL_ASPECT_RATIO=1.2             # Width/height ratio threshold
MIN_PERSON_AREA=5000              # Minimum bounding box area

# Telegram notifications (optional)
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

### Video Sources

| Source | Example |
|--------|---------|
| Webcam | `VIDEO_SOURCE=0` |
| Second webcam | `VIDEO_SOURCE=1` |
| IP Camera (RTSP) | `VIDEO_SOURCE=rtsp://192.168.1.100:554/stream` |
| IP Camera (HTTP) | `VIDEO_SOURCE=http://192.168.1.100:8080/video` |
| Video file | `VIDEO_SOURCE=test_video.mp4` |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/video-stream` | GET | MJPEG live video stream with detections |
| `/detections` | GET | Recent detection results |
| `/alerts` | GET | Alert history (filterable by type) |
| `/alerts/{id}/acknowledge` | POST | Acknowledge an alert |
| `/events` | GET | Event log entries |
| `/stats` | GET | System statistics |
| `/cameras` | GET | Camera status information |
| `/healthz` | GET | Health check |
| `/docs` | GET | Swagger API documentation |

## Training Fire Detection Model

See [training/README_TRAINING.md](backend/training/README_TRAINING.md) for the complete guide.

### Quick Start

```bash
# 1. Download a fire detection dataset from Roboflow in YOLOv8 format
# 2. Create data.yaml (or use the script)
python backend/training/train_fire_model.py --create-yaml /path/to/dataset

# 3. Train the model
python backend/training/train_fire_model.py --data /path/to/data.yaml --epochs 50

# 4. Copy the trained model
cp runs/fire_detection/train/weights/best.pt backend/models/fire_best.pt

# 5. Restart the backend - fire detection is now active!
```

## How It Works

### Fire & Smoke Detection
1. Custom YOLOv8 model trained on fire/smoke images
2. Runs inference on each video frame
3. Draws bounding boxes with confidence scores
4. Triggers FIRE ALERT when confidence > 0.6 (configurable)

### Human Fall Detection
1. YOLOv8 pretrained model detects persons (COCO class 0)
2. Calculates bounding box aspect ratio (width/height)
3. If ratio > 1.2 (person is horizontal), starts monitoring
4. After 1.5 seconds of sustained horizontal posture → FALL ALERT
5. Time-based confirmation reduces false positives

### Real-time Streaming
1. Backend captures frames from webcam/IP camera via OpenCV
2. Each frame is processed through enabled detectors
3. Annotated frames are streamed as MJPEG to the frontend
4. Frontend displays the stream with auto-refreshing stats

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, FastAPI, OpenCV, Ultralytics YOLOv8 |
| Frontend | React, TypeScript, Tailwind CSS, Recharts |
| Detection | YOLOv8 (fire: custom trained, fall: pretrained) |
| Streaming | MJPEG over HTTP |
| UI Style | Dark security-system theme |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No video feed | Check VIDEO_SOURCE in .env, ensure camera is connected |
| Fire detection not working | Train the model first (see training guide) |
| Fall detection not working | YOLOv8 model downloads automatically on first run |
| Frontend can't connect | Ensure backend is running on port 8000 |
| High CPU usage | Reduce frame rate in video.py (increase sleep time) |
| CORS errors | Don't modify CORS settings in main.py |

## License

MIT
