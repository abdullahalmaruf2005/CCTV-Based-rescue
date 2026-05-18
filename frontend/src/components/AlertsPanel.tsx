import { Flame, PersonStanding, Wind, CheckCircle, XCircle } from "lucide-react";
import type { Alert } from "../types";

interface AlertsPanelProps {
  alerts: Alert[];
  onAcknowledge: (id: string) => void;
}

function getAlertIcon(type: string) {
  switch (type) {
    case "fire":
      return <Flame className="w-5 h-5 text-orange-400" />;
    case "fall":
      return <PersonStanding className="w-5 h-5 text-yellow-400" />;
    case "smoke":
      return <Wind className="w-5 h-5 text-blue-400" />;
    default:
      return <XCircle className="w-5 h-5 text-red-400" />;
  }
}

function getSeverityBadge(severity: string) {
  const styles: Record<string, string> = {
    critical: "bg-red-500/20 text-red-400 border-red-500/30",
    high: "bg-orange-500/20 text-orange-400 border-orange-500/30",
    medium: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
    low: "bg-green-500/20 text-green-400 border-green-500/30",
  };
  return styles[severity] || styles.medium;
}

function formatTimestamp(ts: string) {
  const date = new Date(ts);
  return date.toLocaleString();
}

export default function AlertsPanel({ alerts, onAcknowledge }: AlertsPanelProps) {
  if (alerts.length === 0) {
    return (
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-12 text-center">
        <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-white mb-2">All Clear</h3>
        <p className="text-gray-400">No alerts detected. System is monitoring normally.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">Alert Dashboard</h2>
        <span className="text-sm text-gray-400">{alerts.length} total alerts</span>
      </div>

      {alerts.map((alert) => (
        <div
          key={alert.id}
          className={`bg-gray-900 border rounded-xl p-4 transition-all ${
            alert.acknowledged
              ? "border-gray-800 opacity-60"
              : alert.severity === "critical"
              ? "border-red-500/40 glow-red"
              : "border-orange-500/30 glow-orange"
          }`}
        >
          <div className="flex items-start gap-3">
            <div className="mt-0.5">{getAlertIcon(alert.alert_type)}</div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-semibold text-white uppercase">
                  {alert.alert_type} Detected
                </span>
                <span
                  className={`text-xs px-2 py-0.5 rounded-full border ${getSeverityBadge(
                    alert.severity
                  )}`}
                >
                  {alert.severity}
                </span>
                {!alert.acknowledged && (
                  <span className="text-xs px-2 py-0.5 rounded-full bg-red-600 text-white animate-pulse-alert">
                    NEW
                  </span>
                )}
              </div>

              <p className="text-sm text-gray-300 mb-2">{alert.message}</p>

              <div className="flex items-center gap-4 text-xs text-gray-500">
                <span>Confidence: {(alert.confidence * 100).toFixed(0)}%</span>
                <span>Camera: {alert.camera_id}</span>
                <span>{formatTimestamp(alert.timestamp)}</span>
              </div>
            </div>

            {!alert.acknowledged && (
              <button
                onClick={() => onAcknowledge(alert.id)}
                className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs rounded-lg transition-colors border border-gray-700"
              >
                Acknowledge
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
