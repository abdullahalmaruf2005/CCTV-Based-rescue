import {
  Camera,
  Shield,
  AlertTriangle,
  Activity,
  List,
  BarChart3,
} from "lucide-react";

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  alertCount: number;
}

const navItems = [
  { id: "live", label: "Live Feed", icon: Camera },
  { id: "alerts", label: "Alerts", icon: AlertTriangle },
  { id: "events", label: "Event Logs", icon: List },
  { id: "cameras", label: "Cameras", icon: Activity },
  { id: "stats", label: "Statistics", icon: BarChart3 },
];

export default function Sidebar({ activeTab, onTabChange, alertCount }: SidebarProps) {
  return (
    <aside className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col min-h-screen">
      {/* Logo */}
      <div className="p-4 border-b border-gray-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">AI CCTV</h1>
            <p className="text-xs text-gray-400">Surveillance System</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? "bg-red-600/20 text-red-400 border border-red-600/30"
                  : "text-gray-400 hover:bg-gray-800 hover:text-gray-200"
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
              {item.id === "alerts" && alertCount > 0 && (
                <span className="ml-auto bg-red-600 text-white text-xs font-bold px-2 py-0.5 rounded-full animate-pulse-alert">
                  {alertCount}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* System Status */}
      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-xs text-gray-400">System Active</span>
        </div>
      </div>
    </aside>
  );
}
