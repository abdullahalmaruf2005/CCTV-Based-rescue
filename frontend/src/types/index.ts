export interface Alert {
  id: string;
  alert_type: "fire" | "smoke" | "fall";
  severity: "low" | "medium" | "high" | "critical";
  message: string;
  confidence: number;
  camera_id: string;
  timestamp: string;
  acknowledged: boolean;
}

export interface Event {
  id: string;
  event_type: string;
  description: string;
  camera_id: string;
  timestamp: string;
  metadata: Record<string, unknown>;
}

export interface CameraStatus {
  camera_id: string;
  name: string;
  status: "online" | "offline" | "error";
  resolution: string;
  fps: number;
  last_frame: string | null;
}

export interface Stats {
  total_alerts: number;
  fire_count: number;
  fall_count: number;
  smoke_count: number;
  cameras_online: number;
  cameras_total: number;
  uptime_hours: number;
}

export interface Detection {
  label: string;
  confidence: number;
  camera_id: string;
  timestamp: string;
}
