import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { BarChart3 } from "lucide-react";
import type { Stats } from "../types";

interface StatsPageProps {
  stats: Stats;
}

const COLORS = ["#f97316", "#eab308", "#3b82f6"];

export default function StatsPage({ stats }: StatsPageProps) {
  const barData = [
    { name: "Fire", count: stats.fire_count, fill: "#f97316" },
    { name: "Fall", count: stats.fall_count, fill: "#eab308" },
    { name: "Smoke", count: stats.smoke_count, fill: "#3b82f6" },
  ];

  const pieData = [
    { name: "Fire", value: stats.fire_count || 0 },
    { name: "Fall", value: stats.fall_count || 0 },
    { name: "Smoke", value: stats.smoke_count || 0 },
  ].filter((d) => d.value > 0);

  const hasData = stats.total_alerts > 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-4">
        <BarChart3 className="w-5 h-5 text-purple-400" />
        <h2 className="text-lg font-semibold text-white">Statistics Overview</h2>
      </div>

      {!hasData ? (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-12 text-center">
          <BarChart3 className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-white mb-2">No Data Yet</h3>
          <p className="text-gray-400">
            Statistics will populate as the system detects events.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Bar chart */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h3 className="text-sm font-medium text-gray-400 mb-4">
              Alert Distribution
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
                <YAxis stroke="#9ca3af" fontSize={12} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#1f2937",
                    border: "1px solid #374151",
                    borderRadius: "8px",
                    color: "#fff",
                  }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {barData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Pie chart */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h3 className="text-sm font-medium text-gray-400 mb-4">
              Alert Breakdown
            </h3>
            {pieData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                    label={({ name, percent }) =>
                      `${name} ${(percent * 100).toFixed(0)}%`
                    }
                  >
                    {pieData.map((_entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1f2937",
                      border: "1px solid #374151",
                      borderRadius: "8px",
                      color: "#fff",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-72 text-gray-500">
                No data to display
              </div>
            )}
          </div>

          {/* Summary table */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 lg:col-span-2">
            <h3 className="text-sm font-medium text-gray-400 mb-4">
              System Summary
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gray-800/50 rounded-lg p-4 text-center">
                <p className="text-3xl font-bold text-white">{stats.total_alerts}</p>
                <p className="text-xs text-gray-400 mt-1">Total Alerts</p>
              </div>
              <div className="bg-gray-800/50 rounded-lg p-4 text-center">
                <p className="text-3xl font-bold text-green-400">
                  {stats.cameras_online}/{stats.cameras_total}
                </p>
                <p className="text-xs text-gray-400 mt-1">Cameras Online</p>
              </div>
              <div className="bg-gray-800/50 rounded-lg p-4 text-center">
                <p className="text-3xl font-bold text-purple-400">
                  {stats.uptime_hours}h
                </p>
                <p className="text-xs text-gray-400 mt-1">System Uptime</p>
              </div>
              <div className="bg-gray-800/50 rounded-lg p-4 text-center">
                <p className="text-3xl font-bold text-blue-400">
                  {stats.total_alerts > 0
                    ? (stats.uptime_hours > 0
                        ? (stats.total_alerts / stats.uptime_hours).toFixed(1)
                        : stats.total_alerts)
                    : "0"}
                </p>
                <p className="text-xs text-gray-400 mt-1">Alerts/Hour</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
