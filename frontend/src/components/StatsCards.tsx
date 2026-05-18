import { Flame, PersonStanding, Wind, AlertTriangle, Camera, Clock } from "lucide-react";
import type { Stats } from "../types";

interface StatsCardsProps {
  stats: Stats;
}

export default function StatsCards({ stats }: StatsCardsProps) {
  const cards = [
    {
      label: "Total Alerts",
      value: stats.total_alerts,
      icon: AlertTriangle,
      color: "text-red-400",
      bg: "bg-red-500/10",
      border: "border-red-500/20",
    },
    {
      label: "Fire Alerts",
      value: stats.fire_count,
      icon: Flame,
      color: "text-orange-400",
      bg: "bg-orange-500/10",
      border: "border-orange-500/20",
    },
    {
      label: "Fall Alerts",
      value: stats.fall_count,
      icon: PersonStanding,
      color: "text-yellow-400",
      bg: "bg-yellow-500/10",
      border: "border-yellow-500/20",
    },
    {
      label: "Smoke Alerts",
      value: stats.smoke_count,
      icon: Wind,
      color: "text-blue-400",
      bg: "bg-blue-500/10",
      border: "border-blue-500/20",
    },
    {
      label: "Cameras Online",
      value: `${stats.cameras_online}/${stats.cameras_total}`,
      icon: Camera,
      color: "text-green-400",
      bg: "bg-green-500/10",
      border: "border-green-500/20",
    },
    {
      label: "Uptime",
      value: `${stats.uptime_hours}h`,
      icon: Clock,
      color: "text-purple-400",
      bg: "bg-purple-500/10",
      border: "border-purple-500/20",
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <div
            key={card.label}
            className={`${card.bg} ${card.border} border rounded-xl p-4 transition-all hover:scale-105`}
          >
            <div className="flex items-center justify-between mb-2">
              <Icon className={`w-5 h-5 ${card.color}`} />
            </div>
            <p className="text-2xl font-bold text-white">{card.value}</p>
            <p className="text-xs text-gray-400 mt-1">{card.label}</p>
          </div>
        );
      })}
    </div>
  );
}
