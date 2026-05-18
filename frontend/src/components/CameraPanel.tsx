import { Camera, Wifi, WifiOff, AlertCircle } from "lucide-react";
import type { CameraStatus } from "../types";

interface CameraPanelProps {
  cameras: CameraStatus[];
}

function getStatusIcon(status: string) {
  switch (status) {
    case "online":
      return <Wifi className="w-4 h-4 text-green-400" />;
    case "offline":
      return <WifiOff className="w-4 h-4 text-gray-500" />;
    case "error":
      return <AlertCircle className="w-4 h-4 text-red-400" />;
    default:
      return <WifiOff className="w-4 h-4 text-gray-500" />;
  }
}

function getStatusBadge(status: string) {
  switch (status) {
    case "online":
      return "bg-green-500/20 text-green-400 border-green-500/30";
    case "offline":
      return "bg-gray-500/20 text-gray-400 border-gray-500/30";
    case "error":
      return "bg-red-500/20 text-red-400 border-red-500/30";
    default:
      return "bg-gray-500/20 text-gray-400 border-gray-500/30";
  }
}

export default function CameraPanel({ cameras }: CameraPanelProps) {
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">Camera Status</h2>
        <span className="text-sm text-gray-400">{cameras.length} cameras configured</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {cameras.map((cam) => (
          <div
            key={cam.camera_id}
            className={`bg-gray-900 border rounded-xl p-5 transition-all hover:border-gray-700 ${
              cam.status === "online"
                ? "border-green-500/20"
                : cam.status === "error"
                ? "border-red-500/20"
                : "border-gray-800"
            }`}
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div
                  className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    cam.status === "online"
                      ? "bg-green-500/10"
                      : "bg-gray-800"
                  }`}
                >
                  <Camera
                    className={`w-5 h-5 ${
                      cam.status === "online" ? "text-green-400" : "text-gray-500"
                    }`}
                  />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">{cam.name}</p>
                  <p className="text-xs text-gray-500">{cam.camera_id}</p>
                </div>
              </div>
              {getStatusIcon(cam.status)}
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-gray-500">Status</span>
                <span
                  className={`px-2 py-0.5 rounded-full border text-xs ${getStatusBadge(
                    cam.status
                  )}`}
                >
                  {cam.status.toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-gray-500">Resolution</span>
                <span className="text-gray-300">{cam.resolution}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-gray-500">FPS</span>
                <span className="text-gray-300">{cam.fps.toFixed(1)}</span>
              </div>
              {cam.last_frame && (
                <div className="flex justify-between text-xs">
                  <span className="text-gray-500">Last Frame</span>
                  <span className="text-gray-300">
                    {new Date(cam.last_frame).toLocaleTimeString()}
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
