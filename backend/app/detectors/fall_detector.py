"""
Human Fall Detection Module using YOLOv8.

Uses YOLOv8 pretrained person detection + bounding box aspect ratio analysis.
A fall is detected when a person's bounding box becomes horizontal
(width > height) for a sustained period (1-2 seconds) to reduce false positives.
"""

import time
import logging
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)

# How long (seconds) a person must appear "fallen" before triggering alert
FALL_DURATION_THRESHOLD = float(
    __import__("os").environ.get("FALL_DURATION_THRESHOLD", "1.5")
)

# Minimum aspect ratio (width/height) to consider a person as fallen
FALL_ASPECT_RATIO = float(
    __import__("os").environ.get("FALL_ASPECT_RATIO", "1.2")
)

# Minimum bounding box area to filter out noise
MIN_PERSON_AREA = int(
    __import__("os").environ.get("MIN_PERSON_AREA", "5000")
)


class FallDetector:
    """Detects human falls using YOLOv8 person detection + aspect ratio logic."""

    def __init__(self):
        self.model = None
        self.fall_duration_threshold = FALL_DURATION_THRESHOLD
        self.fall_aspect_ratio = FALL_ASPECT_RATIO
        self.min_person_area = MIN_PERSON_AREA
        # Track when each person-region started appearing "fallen"
        # Key: approximate center position, Value: timestamp when fall posture started
        self._fall_start_times: dict[str, float] = {}
        self._confirmed_falls: dict[str, float] = {}
        self._load_model()

    def _load_model(self):
        """Load YOLOv8 pretrained model for person detection."""
        try:
            from ultralytics import YOLO

            self.model = YOLO("yolov8n.pt")
            logger.info("YOLOv8 person detection model loaded for fall detection")
        except Exception as e:
            logger.error(f"Failed to load YOLOv8 model for fall detection: {e}")
            self.model = None

    def _get_region_key(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """Generate a rough spatial key for tracking fall state per person."""
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        # Quantize to 50px grid for approximate tracking
        return f"{cx // 50}_{cy // 50}"

    def detect(self, frame: np.ndarray) -> list[dict]:
        """
        Run fall detection on a single frame.

        Args:
            frame: BGR image as numpy array

        Returns:
            List of detection dicts with keys:
                label, confidence, x1, y1, x2, y2, is_alert, fall_duration
        """
        if self.model is None:
            return []

        detections = []
        current_time = time.time()
        active_regions: set[str] = set()

        try:
            # Run YOLOv8 - only detect persons (class 0 in COCO)
            results = self.model(frame, verbose=False, classes=[0], conf=0.4)

            for result in results:
                boxes = result.boxes
                if boxes is None:
                    continue

                for box in boxes:
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                    width = x2 - x1
                    height = y2 - y1
                    area = width * height

                    # Skip tiny detections (noise)
                    if area < self.min_person_area:
                        continue

                    aspect_ratio = width / max(height, 1)
                    region_key = self._get_region_key(x1, y1, x2, y2)
                    active_regions.add(region_key)

                    is_horizontal = aspect_ratio > self.fall_aspect_ratio
                    is_alert = False
                    fall_duration = 0.0

                    if is_horizontal:
                        # Person appears to be in a fallen position
                        if region_key not in self._fall_start_times:
                            self._fall_start_times[region_key] = current_time

                        fall_duration = current_time - self._fall_start_times[region_key]

                        # Confirm fall after sustained duration
                        if fall_duration >= self.fall_duration_threshold:
                            is_alert = True
                            self._confirmed_falls[region_key] = current_time
                            label = "fall"
                        else:
                            label = "person (monitoring)"
                    else:
                        # Person is upright - clear fall tracking for this region
                        self._fall_start_times.pop(region_key, None)
                        self._confirmed_falls.pop(region_key, None)
                        label = "person"

                    detections.append(
                        {
                            "label": label,
                            "confidence": round(conf, 3),
                            "x1": x1,
                            "y1": y1,
                            "x2": x2,
                            "y2": y2,
                            "is_alert": is_alert,
                            "fall_duration": round(fall_duration, 1),
                        }
                    )

        except Exception as e:
            logger.error(f"Fall detection error: {e}")

        # Clean up stale tracking entries (regions no longer visible)
        stale_keys = [
            k for k in self._fall_start_times if k not in active_regions
        ]
        for k in stale_keys:
            self._fall_start_times.pop(k, None)
            self._confirmed_falls.pop(k, None)

        return detections

    def draw_detections(self, frame: np.ndarray, detections: list[dict]) -> np.ndarray:
        """Draw bounding boxes and labels on the frame."""
        annotated = frame.copy()

        for det in detections:
            x1, y1, x2, y2 = det["x1"], det["y1"], det["x2"], det["y2"]
            label = det["label"]
            conf = det["confidence"]
            is_alert = det.get("is_alert", False)
            fall_dur = det.get("fall_duration", 0)

            if is_alert:
                color = (0, 0, 255)  # Red for confirmed fall
                thickness = 3
            elif "monitoring" in label:
                color = (0, 165, 255)  # Orange for potential fall
                thickness = 2
            else:
                color = (0, 255, 0)  # Green for normal person
                thickness = 2

            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)

            if is_alert:
                text = f"FALL {conf:.0%} ({fall_dur:.1f}s)"
            elif "monitoring" in label:
                text = f"Monitoring {fall_dur:.1f}s"
            else:
                text = f"Person {conf:.0%}"

            font_scale = 0.6
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
            cv2.rectangle(annotated, (x1, y1 - th - 10), (x1 + tw, y1), color, -1)
            cv2.putText(
                annotated, text, (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2,
            )

            if is_alert:
                warning = "ALERT: FALL DETECTED!"
                cv2.putText(
                    annotated, warning, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3,
                )

        return annotated

    @property
    def is_available(self) -> bool:
        return self.model is not None
