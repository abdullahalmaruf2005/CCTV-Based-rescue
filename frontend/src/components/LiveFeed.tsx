import { useState } from "react";
import {
  Camera,
  Maximize2,
  Minimize2,
  Flame,
  PersonStanding,
  RefreshCw,
} from "lucide-react";
import { getVideoStreamUrl } from "../hooks/useApi";
import type { Stats } from "../types";

interface LiveFeedProps {
  stats: Stats;
}

export default function LiveFeed({ stats }: LiveFeedProps) {
  const [fireEnabled, setFireEnabled] = useState(true);
  const [fallEnabled, setFallEnabled] = useState(true);
  const [fullscreen, setFullscreen] = useState(false);
  const [streamKey, setStreamKey] = useState(0);

  const streamUrl = getVideoStreamUrl("cam-01", fireEnabled, fallEnabled);

  const handleRefresh = () => {
    setStreamKey((prev) => prev + 1);
  };

  return (
    <div className="space-y-4">
      {/* Controls bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Camera className="w-5 h-5 text-red-400" />
          <h2 className="text-lg font-semibold text-white">Live CCTV Feed</h2>
          <span className="flex items-center gap-1.5 ml-2">
            <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
            <span className="text-xs text-red-400 font-medium">LIVE</span>
          </span>
        </div>

        <div className="flex items-center gap-3">
          {/* Detection toggles */}
          <button
            onClick={() => {
              setFireEnabled(!fireEnabled);
              handleRefresh();
            }}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              fireEnabled
                ? "bg-orange-500/20 text-orange-400 border border-orange-500/30"
                : "bg-gray-800 text-gray-500 border border-gray-700"
            }`}
          >
            <Flame className="w-3.5 h-3.5" />
            Fire
          </button>

          <button
            onClick={() => {
              setFallEnabled(!fallEnabled);
              handleRefresh();
            }}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              fallEnabled
                ? "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30"
                : "bg-gray-800 text-gray-500 border border-gray-700"
            }`}
          >
            <PersonStanding className="w-3.5 h-3.5" />
            Fall
          </button>

          <button
            onClick={handleRefresh}
            className="p-1.5 rounded-lg bg-gray-800 text-gray-400 hover:text-white transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          <button
            onClick={() => setFullscreen(!fullscreen)}
            className="p-1.5 rounded-lg bg-gray-800 text-gray-400 hover:text-white transition-colors"
          >
            {fullscreen ? (
              <Minimize2 className="w-4 h-4" />
            ) : (
              <Maximize2 className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>

      {/* Video feed */}
      <div
        className={`relative bg-gray-900 border border-gray-800 rounded-xl overflow-hidden ${
          fullscreen ? "fixed inset-4 z-50" : ""
        }`}
      >
        <img
          key={streamKey}
          src={`${streamUrl}&t=${streamKey}`}
          alt="Live CCTV Feed"
          className="w-full h-auto object-contain"
          style={{ minHeight: fullscreen ? "calc(100vh - 2rem)" : "400px", maxHeight: fullscreen ? "calc(100vh - 2rem)" : "600px" }}
        />

        {/* Overlay info */}
        <div className="absolute top-3 left-3 flex gap-2">
          <span className="bg-black/70 text-white text-xs px-2 py-1 rounded">
            CAM-01 | Main Camera
          </span>
          {stats.total_alerts > 0 && (
            <span className="bg-red-600/90 text-white text-xs px-2 py-1 rounded animate-pulse-alert">
              {stats.total_alerts} Active Alerts
            </span>
          )}
        </div>

        {/* Fullscreen close button */}
        {fullscreen && (
          <button
            onClick={() => setFullscreen(false)}
            className="absolute top-3 right-3 bg-black/70 text-white p-2 rounded-lg hover:bg-black/90"
          >
            <Minimize2 className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Quick stats below feed */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-3 text-center">
          <p className="text-xs text-gray-400">Fire Detections</p>
          <p className="text-xl font-bold text-orange-400">{stats.fire_count}</p>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-3 text-center">
          <p className="text-xs text-gray-400">Fall Detections</p>
          <p className="text-xl font-bold text-yellow-400">{stats.fall_count}</p>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-3 text-center">
          <p className="text-xs text-gray-400">Smoke Detections</p>
          <p className="text-xl font-bold text-blue-400">{stats.smoke_count}</p>
        </div>
      </div>
    </div>
  );
}
