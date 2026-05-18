import { List, Flame, PersonStanding, Wind, Settings } from "lucide-react";
import type { Event } from "../types";

interface EventLogsProps {
  events: Event[];
}

function getEventIcon(type: string) {
  if (type.includes("fire")) return <Flame className="w-4 h-4 text-orange-400" />;
  if (type.includes("fall")) return <PersonStanding className="w-4 h-4 text-yellow-400" />;
  if (type.includes("smoke")) return <Wind className="w-4 h-4 text-blue-400" />;
  return <Settings className="w-4 h-4 text-gray-400" />;
}

function getEventColor(type: string) {
  if (type.includes("fire")) return "border-l-orange-500";
  if (type.includes("fall")) return "border-l-yellow-500";
  if (type.includes("smoke")) return "border-l-blue-500";
  return "border-l-gray-600";
}

function formatTimestamp(ts: string) {
  const date = new Date(ts);
  return date.toLocaleString();
}

export default function EventLogs({ events }: EventLogsProps) {
  if (events.length === 0) {
    return (
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-12 text-center">
        <List className="w-12 h-12 text-gray-600 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-white mb-2">No Events Yet</h3>
        <p className="text-gray-400">Events will appear here as the system detects activity.</p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">Event Logs</h2>
        <span className="text-sm text-gray-400">{events.length} events</span>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
        {/* Table header */}
        <div className="grid grid-cols-12 gap-4 px-4 py-3 border-b border-gray-800 text-xs font-medium text-gray-400 uppercase">
          <div className="col-span-1">Type</div>
          <div className="col-span-4">Description</div>
          <div className="col-span-2">Event Type</div>
          <div className="col-span-2">Camera</div>
          <div className="col-span-3">Timestamp</div>
        </div>

        {/* Event rows */}
        <div className="divide-y divide-gray-800/50 max-h-96 overflow-y-auto">
          {events.map((event) => (
            <div
              key={event.id}
              className={`grid grid-cols-12 gap-4 px-4 py-3 hover:bg-gray-800/50 transition-colors border-l-2 ${getEventColor(
                event.event_type
              )}`}
            >
              <div className="col-span-1 flex items-center">
                {getEventIcon(event.event_type)}
              </div>
              <div className="col-span-4 text-sm text-gray-300 truncate">
                {event.description}
              </div>
              <div className="col-span-2">
                <span className="text-xs px-2 py-0.5 rounded bg-gray-800 text-gray-400">
                  {event.event_type}
                </span>
              </div>
              <div className="col-span-2 text-sm text-gray-400">
                {event.camera_id}
              </div>
              <div className="col-span-3 text-xs text-gray-500">
                {formatTimestamp(event.timestamp)}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
