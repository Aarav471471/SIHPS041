import React from "react";
import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/api/client";
import { Users, FileCheck, AlertTriangle, TrendingUp } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Legend } from "recharts";

const fetchKpis = async () => (await apiClient.get("/admin/kpis")).data;
const fetchCompliance = async () => (await apiClient.get("/admin/compliance")).data;
const fetchTimeline = async () => (await apiClient.get("/admin/analytics/timeline")).data;

export default function Dashboard() {
  const { data: kpis, isLoading: kpisLoading } = useQuery({ queryKey: ["kpis"], queryFn: fetchKpis, refetchInterval: 30000 });
  const { data: matrix, isLoading: matrixLoading } = useQuery({ queryKey: ["compliance"], queryFn: fetchCompliance });
  const { data: timeline } = useQuery({ queryKey: ["timeline"], queryFn: fetchTimeline });

  if (kpisLoading || matrixLoading) {
    return <div className="flex h-64 items-center justify-center text-slate-500">Loading dashboard...</div>;
  }

  const moduleNames: Record<string, string> = {
    fire: "Fire & Exp",
    gas: "Gas & Space",
    machinery: "Machinery",
    electrical: "Electrical",
    ppe: "PPE & Height"
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Compliance Overview</h1>
        <button className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-md text-sm font-medium shadow-sm">
          Export Report
        </button>
      </div>
      
      {/* KPI Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg border border-slate-200">
          <div className="p-5 flex items-center">
            <div className="flex-shrink-0 bg-blue-100 rounded-md p-3">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dt className="text-sm font-medium text-slate-500 truncate">Total Workers</dt>
              <dd className="text-2xl font-bold text-slate-900">{kpis?.total_workers}</dd>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg border border-slate-200">
          <div className="p-5 flex items-center">
            <div className="flex-shrink-0 bg-green-100 rounded-md p-3">
              <FileCheck className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dt className="text-sm font-medium text-slate-500 truncate">Certified (Overall)</dt>
              <dd className="text-2xl font-bold text-slate-900">{kpis?.certified_pct}%</dd>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg border border-slate-200">
          <div className="p-5 flex items-center">
            <div className="flex-shrink-0 bg-orange-100 rounded-md p-3">
              <AlertTriangle className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dt className="text-sm font-medium text-slate-500 truncate">Expiring in 30d</dt>
              <dd className="text-2xl font-bold text-slate-900">{kpis?.expiring_30d}</dd>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg border border-slate-200">
          <div className="p-5 flex items-center">
            <div className="flex-shrink-0 bg-purple-100 rounded-md p-3">
              <TrendingUp className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dt className="text-sm font-medium text-slate-500 truncate">Pass Rate</dt>
              <dd className="text-2xl font-bold text-slate-900">{kpis?.pass_rate}%</dd>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Compliance Matrix */}
        <div className="bg-white shadow rounded-lg border border-slate-200 overflow-hidden flex flex-col">
          <div className="px-5 py-4 border-b border-slate-200">
            <h3 className="text-lg leading-6 font-medium text-slate-900">Site Compliance Heatmap</h3>
          </div>
          <div className="p-5 overflow-x-auto flex-1">
            <table className="min-w-full divide-y divide-slate-200 text-sm">
              <thead>
                <tr>
                  <th className="px-3 py-3 bg-slate-50 text-left font-semibold text-slate-900">Site</th>
                  {Object.keys(moduleNames).map(mod => (
                    <th key={mod} className="px-3 py-3 bg-slate-50 text-center font-semibold text-slate-900">{moduleNames[mod]}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 bg-white">
                {matrix?.map((row: any) => (
                  <tr key={row.site_id}>
                    <td className="px-3 py-4 whitespace-nowrap font-medium text-slate-900">{row.site_name}</td>
                    {Object.keys(moduleNames).map(mod => {
                      const pct = row.modules[mod] || 0;
                      let colorClass = "bg-red-100 text-red-800";
                      if (pct >= 80) colorClass = "bg-green-100 text-green-800";
                      else if (pct >= 50) colorClass = "bg-yellow-100 text-yellow-800";
                      
                      return (
                        <td key={mod} className="px-3 py-4 whitespace-nowrap text-center">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colorClass}`}>
                            {pct}%
                          </span>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Timeline Chart */}
        <div className="bg-white shadow rounded-lg border border-slate-200">
          <div className="px-5 py-4 border-b border-slate-200">
            <h3 className="text-lg leading-6 font-medium text-slate-900">Certifications Timeline</h3>
          </div>
          <div className="p-5 h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={timeline} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748B' }} />
                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748B' }} />
                <RechartsTooltip cursor={{ fill: '#F1F5F9' }} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Bar dataKey="attempts" fill="#EA580C" radius={[4, 4, 0, 0]} name="Attempts" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
