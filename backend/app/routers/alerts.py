"""
Alerts & Events API Router.

Provides endpoints to query alerts, events, statistics, and camera status.
"""

from typing import Optional

from fastapi import APIRouter, Query, HTTPException

from app.alert_manager import alert_manager
from app.camera_manager import camera_manager
from app.models.schemas import StatsResponse

router = APIRouter()


@router.get("/detections")
async def get_recent_detections():
    """Get the most recent detection results (from last processed frame)."""
    # Return recent alerts as proxy for detections
    alerts = alert_manager.get_alerts(limit=10)
    return {
        "detections": [
            {
                "label": a.alert_type.value,
                "confidence": a.confidence,
                "camera_id": a.camera_id,
                "timestamp": a.timestamp.isoformat(),
            }
            for a in alerts
        ]
    }


@router.get("/alerts")
async def get_alerts(
    limit: int = Query(50, ge=1, le=200, description="Number of alerts to return"),
    alert_type: Optional[str] = Query(None, description="Filter by alert type: fire, smoke, fall"),
):
    """Get recent alerts, optionally filtered by type."""
    alerts = alert_manager.get_alerts(limit=limit, alert_type=alert_type)
    return {"alerts": [a.model_dump() for a in alerts], "total": len(alerts)}


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    """Acknowledge an alert by its ID."""
    success = alert_manager.acknowledge_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "acknowledged", "alert_id": alert_id}


@router.get("/events")
async def get_events(
    limit: int = Query(100, ge=1, le=500, description="Number of events to return"),
):
    """Get recent events (system logs and alert events)."""
    events = alert_manager.get_events(limit=limit)
    return {"events": [e.model_dump() for e in events], "total": len(events)}


@router.get("/stats")
async def get_stats():
    """Get surveillance system statistics."""
    stats = alert_manager.get_stats()
    stats["cameras_online"] = camera_manager.get_online_count()
    stats["cameras_total"] = len(camera_manager.cameras) or 1
    return StatsResponse(**stats)


@router.get("/cameras")
async def get_cameras():
    """Get status of all configured cameras."""
    statuses = camera_manager.get_all_cameras_status()
    if not statuses:
        # Return default camera status if none configured
        return {
            "cameras": [
                {
                    "camera_id": "cam-01",
                    "name": "Main Camera",
                    "status": "offline",
                    "resolution": "N/A",
                    "fps": 0,
                    "last_frame": None,
                }
            ]
        }
    return {"cameras": statuses}
