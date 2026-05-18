"""Pydantic models for API request/response schemas."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AlertType(str, Enum):
    FIRE = "fire"
    SMOKE = "smoke"
    FALL = "fall"


class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Detection(BaseModel):
    label: str
    confidence: float
    x1: int
    y1: int
    x2: int
    y2: int


class DetectionFrame(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    camera_id: str = "cam-01"
    detections: list[Detection] = []


class Alert(BaseModel):
    id: str
    alert_type: AlertType
    severity: AlertSeverity
    message: str
    confidence: float
    camera_id: str = "cam-01"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    acknowledged: bool = False


class Event(BaseModel):
    id: str
    event_type: str
    description: str
    camera_id: str = "cam-01"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = {}


class CameraStatus(BaseModel):
    camera_id: str
    name: str
    status: str  # "online", "offline", "error"
    resolution: str = "640x480"
    fps: float = 0.0
    last_frame: Optional[datetime] = None


class StatsResponse(BaseModel):
    total_alerts: int = 0
    fire_count: int = 0
    fall_count: int = 0
    smoke_count: int = 0
    cameras_online: int = 0
    cameras_total: int = 1
    uptime_hours: float = 0.0
