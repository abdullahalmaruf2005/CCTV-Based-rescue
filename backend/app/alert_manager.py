"""
Alert & Event Management System.

Stores alerts and events in memory. In production, replace with a database.
Provides methods to create, query, and manage alerts and events.
"""

import uuid
import logging
from datetime import datetime
from collections import deque
from typing import Optional

from app.models.schemas import Alert, AlertType, AlertSeverity, Event

logger = logging.getLogger(__name__)

# Maximum number of alerts/events to keep in memory
MAX_ALERTS = 500
MAX_EVENTS = 1000

# Cooldown in seconds between duplicate alerts for same camera/type
ALERT_COOLDOWN = 10.0


class AlertManager:
    """Manages alerts and events for the surveillance system."""

    def __init__(self):
        self.alerts: deque[Alert] = deque(maxlen=MAX_ALERTS)
        self.events: deque[Event] = deque(maxlen=MAX_EVENTS)
        self._last_alert_time: dict[str, float] = {}
        self._start_time = datetime.utcnow()

        # Counters
        self.fire_count = 0
        self.smoke_count = 0
        self.fall_count = 0

        logger.info("Alert manager initialized")

    def _should_alert(self, alert_type: str, camera_id: str) -> bool:
        """Check if enough time has passed since last alert of this type."""
        key = f"{alert_type}_{camera_id}"
        now = datetime.utcnow().timestamp()
        last_time = self._last_alert_time.get(key, 0)

        if now - last_time >= ALERT_COOLDOWN:
            self._last_alert_time[key] = now
            return True
        return False

    def create_fire_alert(
        self, confidence: float, camera_id: str = "cam-01"
    ) -> Optional[Alert]:
        """Create a fire detection alert."""
        if not self._should_alert("fire", camera_id):
            return None

        self.fire_count += 1
        alert = Alert(
            id=str(uuid.uuid4()),
            alert_type=AlertType.FIRE,
            severity=AlertSeverity.CRITICAL,
            message=f"Fire detected on {camera_id} with {confidence:.0%} confidence",
            confidence=confidence,
            camera_id=camera_id,
        )
        self.alerts.appendleft(alert)
        self._log_event("fire_alert", f"Fire detected ({confidence:.0%})", camera_id)
        logger.warning(f"FIRE ALERT: {alert.message}")
        return alert

    def create_smoke_alert(
        self, confidence: float, camera_id: str = "cam-01"
    ) -> Optional[Alert]:
        """Create a smoke detection alert."""
        if not self._should_alert("smoke", camera_id):
            return None

        self.smoke_count += 1
        alert = Alert(
            id=str(uuid.uuid4()),
            alert_type=AlertType.SMOKE,
            severity=AlertSeverity.HIGH,
            message=f"Smoke detected on {camera_id} with {confidence:.0%} confidence",
            confidence=confidence,
            camera_id=camera_id,
        )
        self.alerts.appendleft(alert)
        self._log_event("smoke_alert", f"Smoke detected ({confidence:.0%})", camera_id)
        logger.warning(f"SMOKE ALERT: {alert.message}")
        return alert

    def create_fall_alert(
        self, confidence: float, camera_id: str = "cam-01"
    ) -> Optional[Alert]:
        """Create a fall detection alert."""
        if not self._should_alert("fall", camera_id):
            return None

        self.fall_count += 1
        alert = Alert(
            id=str(uuid.uuid4()),
            alert_type=AlertType.FALL,
            severity=AlertSeverity.HIGH,
            message=f"Person fall detected on {camera_id} with {confidence:.0%} confidence",
            confidence=confidence,
            camera_id=camera_id,
        )
        self.alerts.appendleft(alert)
        self._log_event("fall_alert", f"Fall detected ({confidence:.0%})", camera_id)
        logger.warning(f"FALL ALERT: {alert.message}")
        return alert

    def _log_event(
        self, event_type: str, description: str, camera_id: str = "cam-01"
    ):
        """Log an event."""
        event = Event(
            id=str(uuid.uuid4()),
            event_type=event_type,
            description=description,
            camera_id=camera_id,
        )
        self.events.appendleft(event)

    def log_system_event(self, description: str):
        """Log a system-level event."""
        self._log_event("system", description, "system")

    def get_alerts(self, limit: int = 50, alert_type: Optional[str] = None) -> list[Alert]:
        """Get recent alerts, optionally filtered by type."""
        alerts = list(self.alerts)
        if alert_type:
            alerts = [a for a in alerts if a.alert_type.value == alert_type]
        return alerts[:limit]

    def get_events(self, limit: int = 100) -> list[Event]:
        """Get recent events."""
        return list(self.events)[:limit]

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert by ID."""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                return True
        return False

    def get_stats(self) -> dict:
        """Get summary statistics."""
        uptime = (datetime.utcnow() - self._start_time).total_seconds() / 3600
        return {
            "total_alerts": len(self.alerts),
            "fire_count": self.fire_count,
            "smoke_count": self.smoke_count,
            "fall_count": self.fall_count,
            "uptime_hours": round(uptime, 2),
        }


# Global singleton instance
alert_manager = AlertManager()
