import { useState } from "react";
import Sidebar from "./components/Sidebar";
import StatsCards from "./components/StatsCards";
import LiveFeed from "./components/LiveFeed";
import AlertsPanel from "./components/AlertsPanel";
import EventLogs from "./components/EventLogs";
import CameraPanel from "./components/CameraPanel";
import StatsPage from "./components/StatsPage";
import { useAlerts, useEvents, useCameras, useStats } from "./hooks/useApi";

function App() {
  const [activeTab, setActiveTab] = useState("live");
  const { alerts, acknowledgeAlert } = useAlerts(3000);
  const { events } = useEvents(5000);
  const { cameras } = useCameras(5000);
  const { stats } = useStats(3000);

  const unacknowledgedCount = alerts.filter((a) => !a.acknowledged).length;

  return (
    <div className="flex min-h-screen bg-gray-950">
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        alertCount={unacknowledgedCount}
      />

      <main className="flex-1 p-6 overflow-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-white">
              {activeTab === "live" && "Live Surveillance"}
              {activeTab === "alerts" && "Alert Dashboard"}
              {activeTab === "events" && "Event Logs"}
              {activeTab === "cameras" && "Camera Management"}
              {activeTab === "stats" && "Statistics"}
            </h1>
            <p className="text-sm text-gray-400 mt-1">
              Real-time AI-powered CCTV monitoring system
            </p>
          </div>

          {unacknowledgedCount > 0 && (
            <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 rounded-lg px-4 py-2 animate-pulse-alert">
              <span className="w-2 h-2 bg-red-500 rounded-full" />
              <span className="text-sm text-red-400 font-medium">
                {unacknowledgedCount} Active Alert{unacknowledgedCount !== 1 ? "s" : ""}
              </span>
            </div>
          )}
        </div>

        {/* Stats cards - always visible */}
        <div className="mb-6">
          <StatsCards stats={stats} />
        </div>

        {/* Page content */}
        <div>
          {activeTab === "live" && <LiveFeed stats={stats} />}
          {activeTab === "alerts" && (
            <AlertsPanel alerts={alerts} onAcknowledge={acknowledgeAlert} />
          )}
          {activeTab === "events" && <EventLogs events={events} />}
          {activeTab === "cameras" && <CameraPanel cameras={cameras} />}
          {activeTab === "stats" && <StatsPage stats={stats} />}
        </div>
      </main>
    </div>
  );
}

export default App;
