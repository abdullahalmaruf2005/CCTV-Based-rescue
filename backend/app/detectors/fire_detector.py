"""
Fire & Smoke Detection Module using YOLOv8.

This module loads a custom-trained YOLOv8 model for detecting fire and smoke.
If no custom model is found, it uses a placeholder that returns no detections.
After training your own model, place the best.pt file in the models/ directory.
"""

import os
import logging
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)

# Path to the custom-trained fire detection model
FIRE_MODEL_PATH = os.environ.get(
    "FIRE_MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "..", "..", "models", "fire_best.pt"),
)

# Confidence threshold for triggering fire alerts
FIRE_CONFIDENCE_THRESHOLD = float(os.environ.get("FIRE_CONFIDENCE_THRESHOLD", "0.6"))


class FireDetector:
    """Detects fire and smoke using a custom-trained YOLOv8 model."""

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path or FIRE_MODEL_PATH
        self.confidence_threshold = FIRE_CONFIDENCE_THRESHOLD
        self.class_names = ["fire", "smoke"]
        self._load_model()

    def _load_model(self):
        """Load the YOLOv8 fire detection model."""
        try:
            if os.path.exists(self.model_path):
                from ultralytics import YOLO

                self.model = YOLO(self.model_path)
                logger.info(f"Fire detection model loaded from {self.model_path}")
            else:
                logger.warning(
                    f"Fire model not found at {self.model_path}. "
                    "Fire detection disabled. Train your model first! "
                    "See training/README_TRAINING.md for instructions."
                )
        except Exception as e:
            logger.error(f"Failed to load fire detection model: {e}")
            self.model = None

    def detect(self, frame: np.ndarray) -> list[dict]:
        """
        Run fire/smoke detection on a single frame.

        Args:
            frame: BGR image as numpy array (from OpenCV)

        Returns:
            List of detection dicts with keys:
                label, confidence, x1, y1, x2, y2, is_alert
        """
        if self.model is None:
            return []

        detections = []
        try:
            results = self.model(frame, verbose=False, conf=0.3)

            for result in results:
                boxes = result.boxes
                if boxes is None:
                    continue

                for box in boxes:
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                    # Map class ID to label
                    if cls_id < len(self.class_names):
                        label = self.class_names[cls_id]
                    else:
                        label = f"class_{cls_id}"

                    detections.append(
                        {
                            "label": label,
                            "confidence": round(conf, 3),
                            "x1": x1,
                            "y1": y1,
                            "x2": x2,
                            "y2": y2,
                            "is_alert": conf >= self.confidence_threshold,
                        }
                    )
        except Exception as e:
            logger.error(f"Fire detection error: {e}")

        return detections

    def draw_detections(self, frame: np.ndarray, detections: list[dict]) -> np.ndarray:
        """Draw bounding boxes and labels on the frame."""
        annotated = frame.copy()

        for det in detections:
            x1, y1, x2, y2 = det["x1"], det["y1"], det["x2"], det["y2"]
            label = det["label"]
            conf = det["confidence"]
            is_alert = det.get("is_alert", False)

            # Red for fire alerts, orange for smoke, green for low confidence
            if label == "fire":
                color = (0, 0, 255) if is_alert else (0, 165, 255)
            else:
                color = (0, 140, 255) if is_alert else (0, 200, 200)

            thickness = 3 if is_alert else 2
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)

            text = f"{label.upper()} {conf:.0%}"
            font_scale = 0.7
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
            cv2.rectangle(annotated, (x1, y1 - th - 10), (x1 + tw, y1), color, -1)
            cv2.putText(
                annotated, text, (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2,
            )

            # Flash warning text for high-confidence alerts
            if is_alert:
                warning = f"ALERT: {label.upper()} DETECTED!"
                cv2.putText(
                    annotated, warning, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3,
                )

        return annotated

    @property
    def is_available(self) -> bool:
        return self.model is not None
