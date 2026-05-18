"""
AI CCTV Surveillance System - FastAPI Backend

Real-time video surveillance with YOLOv8-based fire/smoke and fall detection.
Provides MJPEG video streaming, alerts, events, and camera management APIs.
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import video, alerts
from app.camera_manager import camera_manager
from app.alert_manager import alert_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Video source from environment (0=webcam, or RTSP/file path)
VIDEO_SOURCE = os.environ.get("VIDEO_SOURCE", "0")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    logger.info("Starting AI CCTV Surveillance System...")
    logger.info(f"Video source: {VIDEO_SOURCE}")

    camera_manager.add_camera(
        camera_id="cam-01",
        source=VIDEO_SOURCE,
        name="Main Camera",
    )
    alert_manager.log_system_event("Surveillance system started")

    yield

    logger.info("Shutting down surveillance system...")
    camera_manager.release_all()
    alert_manager.log_system_event("Surveillance system stopped")


app = FastAPI(
    title="AI CCTV Surveillance System",
    description="Real-time video surveillance with fire/smoke and fall detection",
    version="1.0.0",
    lifespan=lifespan,
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(video.router, tags=["Video"])
app.include_router(alerts.router, tags=["Alerts & Events"])


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "name": "AI CCTV Surveillance System",
        "version": "1.0.0",
        "endpoints": {
            "video_stream": "/video-stream",
            "detections": "/detections",
            "alerts": "/alerts",
            "events": "/events",
            "stats": "/stats",
            "cameras": "/cameras",
            "docs": "/docs",
        },
    }
