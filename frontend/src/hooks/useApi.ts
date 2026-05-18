import { useState, useEffect, useCallback } from "react";
import type { Alert, Event, CameraStatus, Stats } from "../types";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function fetchJson<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${API_URL}${endpoint}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export function useAlerts(pollInterval = 3000) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchAlerts = useCallback(async () => {
    try {
      const data = await fetchJson<{ alerts: Alert[] }>("/alerts?limit=50");
      setAlerts(data.alerts);
    } catch (err) {
      console.error("Failed to fetch alerts:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, pollInterval);
    return () => clearInterval(interval);
  }, [fetchAlerts, pollInterval]);

  const acknowledgeAlert = useCallback(async (alertId: string) => {
    try {
      await fetch(`${API_URL}/alerts/${alertId}/acknowledge`, { method: "POST" });
      setAlerts((prev) =>
        prev.map((a) => (a.id === alertId ? { ...a, acknowledged: true } : a))
      );
    } catch (err) {
      console.error("Failed to acknowledge alert:", err);
    }
  }, []);

  return { alerts, loading, acknowledgeAlert, refetch: fetchAlerts };
}

export function useEvents(pollInterval = 5000) {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchEvents = useCallback(async () => {
    try {
      const data = await fetchJson<{ events: Event[] }>("/events?limit=100");
      setEvents(data.events);
    } catch (err) {
      console.error("Failed to fetch events:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, pollInterval);
    return () => clearInterval(interval);
  }, [fetchEvents, pollInterval]);

  return { events, loading, refetch: fetchEvents };
}

export function useCameras(pollInterval = 5000) {
  const [cameras, setCameras] = useState<CameraStatus[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchCameras = useCallback(async () => {
    try {
      const data = await fetchJson<{ cameras: CameraStatus[] }>("/cameras");
      setCameras(data.cameras);
    } catch (err) {
      console.error("Failed to fetch cameras:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCameras();
    const interval = setInterval(fetchCameras, pollInterval);
    return () => clearInterval(interval);
  }, [fetchCameras, pollInterval]);

  return { cameras, loading, refetch: fetchCameras };
}

export function useStats(pollInterval = 3000) {
  const [stats, setStats] = useState<Stats>({
    total_alerts: 0,
    fire_count: 0,
    fall_count: 0,
    smoke_count: 0,
    cameras_online: 0,
    cameras_total: 1,
    uptime_hours: 0,
  });
  const [loading, setLoading] = useState(true);

  const fetchStats = useCallback(async () => {
    try {
      const data = await fetchJson<Stats>("/stats");
      setStats(data);
    } catch (err) {
      console.error("Failed to fetch stats:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, pollInterval);
    return () => clearInterval(interval);
  }, [fetchStats, pollInterval]);

  return { stats, loading, refetch: fetchStats };
}

export function getVideoStreamUrl(cameraId = "cam-01", fire = true, fall = true) {
  return `${API_URL}/video-stream?camera_id=${cameraId}&fire=${fire}&fall=${fall}`;
}
