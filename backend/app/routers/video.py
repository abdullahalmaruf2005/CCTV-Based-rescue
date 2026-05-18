"""
Video Streaming Router.

Provides MJPEG video stream with real-time detection overlays.
"""

import time
import logging
import asyncio
from datetime import datetime

import cv2
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.camera_manager import camera_manager
from app.alert_manager import alert_manager
from app.detectors.fire_detector import FireDetector
from app.detectors.fall_detector import FallDetector

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize detectors (lazy-loaded singletons)
fire_detector: FireDetector | None = None
fall_detector: FallDetector | None = None


def get_fire_detector() -> FireDetector:
    global fire_detector
    if fire_detector is None:
        fire_detector = FireDetector()
    return fire_detector


def get_fall_detector() -> FallDetector:
    global fall_detector
    if fall_detector is None:
        fall_detector = FallDetector()
    return fall_detector


def process_frame(frame, camera_id: str = "cam-01", enable_fire: bool = True, enable_fall: bool = True):
    """Run all enabled detectors on a frame and return annotated frame + detections."""
    all_detections = []

    # Fire/Smoke detection
    if enable_fire:
        fd = get_fire_detector()
        fire_dets = fd.detect(frame)
        if fire_dets:
            frame = fd.draw_detections(frame, fire_dets)
            all_detections.extend(fire_dets)

            # Create alerts for high-confidence fire/smoke detections
            for det in fire_dets:
                if det.get("is_alert"):
                    if det["label"] == "fire":
                        alert_manager.create_fire_alert(det["confidence"], camera_id)
                    elif det["label"] == "smoke":
                        alert_manager.create_smoke_alert(det["confidence"], camera_id)

    # Fall detection
    if enable_fall:
        fld = get_fall_detector()
        fall_dets = fld.detect(frame)
        if fall_dets:
            frame = fld.draw_detections(frame, fall_dets)
            all_detections.extend(fall_dets)

            # Create alerts for confirmed falls
            for det in fall_dets:
                if det.get("is_alert"):
                    alert_manager.create_fall_alert(det["confidence"], camera_id)

    return frame, all_detections


def generate_frames(
    camera_id: str = "cam-01",
    enable_fire: bool = True,
    enable_fall: bool = True,
):
    """Generator that yields MJPEG frames with detection overlays."""
    frame_count = 0
    fps_start = time.time()
    current_fps = 0.0

    while True:
        frame = camera_manager.get_frame(camera_id)

        if frame is None:
            # Generate a "No Signal" placeholder frame
            placeholder = _create_no_signal_frame()
            _, buffer = cv2.imencode(".jpg", placeholder, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )
            time.sleep(1.0)
            continue

        # Process frame with detectors
        annotated_frame, detections = process_frame(
            frame, camera_id, enable_fire, enable_fall
        )

        # Calculate FPS
        frame_count += 1
        elapsed = time.time() - fps_start
        if elapsed >= 1.0:
            current_fps = frame_count / elapsed
            frame_count = 0
            fps_start = time.time()

        # Draw FPS and timestamp overlay
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(
            annotated_frame,
            f"{timestamp} | FPS: {current_fps:.1f} | {camera_id}",
            (10, annotated_frame.shape[0] - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1,
        )

        # Encode frame as JPEG
        _, buffer = cv2.imencode(".jpg", annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
        )

        # Limit frame rate to ~20fps to reduce CPU load
        time.sleep(0.05)


def _create_no_signal_frame():
    """Create a placeholder frame when no camera is available."""
    frame = cv2.UMat(480, 640, cv2.CV_8UC3)
    frame = cv2.UMat.get(frame)
    frame[:] = (30, 30, 30)  # Dark gray background

    cv2.putText(
        frame, "NO SIGNAL", (180, 220),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 200), 3,
    )
    cv2.putText(
        frame, "Camera offline or not connected", (120, 270),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1,
    )
    cv2.putText(
        frame,
        f"Set VIDEO_SOURCE env var or connect a camera",
        (80, 310),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1,
    )
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(
        frame, timestamp, (220, 450),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1,
    )
    return frame


@router.get("/video-stream")
async def video_stream(
    camera_id: str = Query("cam-01", description="Camera ID to stream"),
    fire: bool = Query(True, description="Enable fire detection"),
    fall: bool = Query(True, description="Enable fall detection"),
):
    """Stream live video feed with detection overlays as MJPEG."""
    return StreamingResponse(
        generate_frames(camera_id, enable_fire=fire, enable_fall=fall),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
