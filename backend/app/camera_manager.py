"""
Camera Manager - handles video capture from webcam or IP cameras.

Supports:
- Local webcam (device index 0, 1, etc.)
- IP camera streams (RTSP/HTTP URLs)
- Video file playback for testing
"""

import os
import time
import logging
import threading
from datetime import datetime
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)

# Default video source: 0 = first webcam, or a URL/file path
DEFAULT_VIDEO_SOURCE = os.environ.get("VIDEO_SOURCE", "0")


class CameraManager:
    """Manages video capture from cameras."""

    def __init__(self):
        self.cameras: dict[str, dict] = {}
        self._locks: dict[str, threading.Lock] = {}
        self._running = False

    def add_camera(
        self,
        camera_id: str,
        source: str,
        name: str = "Camera",
    ) -> bool:
        """
        Add a camera source.

        Args:
            camera_id: Unique identifier for the camera
            source: Video source - device index (e.g., "0"), RTSP URL, or file path
            name: Human-readable camera name
        """
        try:
            # Convert numeric strings to integers for device indices
            src = int(source) if source.isdigit() else source
            cap = cv2.VideoCapture(src)

            if not cap.isOpened():
                logger.warning(f"Could not open camera source: {source}")
                self.cameras[camera_id] = {
                    "capture": None,
                    "source": source,
                    "name": name,
                    "status": "offline",
                    "fps": 0,
                    "resolution": "N/A",
                    "last_frame": None,
                    "last_frame_time": None,
                }
                self._locks[camera_id] = threading.Lock()
                return False

            # Get camera properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

            self.cameras[camera_id] = {
                "capture": cap,
                "source": source,
                "name": name,
                "status": "online",
                "fps": fps,
                "resolution": f"{width}x{height}",
                "last_frame": None,
                "last_frame_time": None,
            }
            self._locks[camera_id] = threading.Lock()
            logger.info(f"Camera {camera_id} ({name}) added: {width}x{height} @ {fps:.1f}fps")
            return True

        except Exception as e:
            logger.error(f"Error adding camera {camera_id}: {e}")
            return False

    def get_frame(self, camera_id: str) -> Optional[np.ndarray]:
        """Read a single frame from the camera."""
        cam = self.cameras.get(camera_id)
        if not cam or not cam["capture"]:
            return None

        lock = self._locks.get(camera_id)
        if not lock:
            return None

        with lock:
            try:
                ret, frame = cam["capture"].read()
                if ret and frame is not None:
                    cam["last_frame"] = frame
                    cam["last_frame_time"] = datetime.utcnow()
                    cam["status"] = "online"
                    return frame
                else:
                    # Try to reconnect
                    cam["status"] = "error"
                    src = cam["source"]
                    s = int(src) if src.isdigit() else src
                    cam["capture"].release()
                    cam["capture"] = cv2.VideoCapture(s)
                    return cam["last_frame"]
            except Exception as e:
                logger.error(f"Error reading frame from {camera_id}: {e}")
                cam["status"] = "error"
                return None

    def get_camera_status(self, camera_id: str) -> dict:
        """Get the status of a camera."""
        cam = self.cameras.get(camera_id)
        if not cam:
            return {
                "camera_id": camera_id,
                "name": "Unknown",
                "status": "offline",
                "resolution": "N/A",
                "fps": 0,
                "last_frame": None,
            }

        return {
            "camera_id": camera_id,
            "name": cam["name"],
            "status": cam["status"],
            "resolution": cam["resolution"],
            "fps": cam["fps"],
            "last_frame": cam["last_frame_time"],
        }

    def get_all_cameras_status(self) -> list[dict]:
        """Get status of all cameras."""
        return [self.get_camera_status(cid) for cid in self.cameras]

    def release_all(self):
        """Release all camera resources."""
        for camera_id, cam in self.cameras.items():
            if cam["capture"]:
                cam["capture"].release()
                logger.info(f"Camera {camera_id} released")

    def get_online_count(self) -> int:
        """Get count of online cameras."""
        return sum(1 for cam in self.cameras.values() if cam["status"] == "online")


# Global singleton
camera_manager = CameraManager()
