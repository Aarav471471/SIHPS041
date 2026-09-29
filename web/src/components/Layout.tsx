import React from "react";
import { Outlet, Navigate, Link, useLocation } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { Shield, LayoutDashboard, Users, FileCheck, BarChart2, LogOut } from "lucide-react";

export default function Layout() {
  const { user, logout } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Workers", href: "/workers", icon: Users },
    { name: "Certificates", href: "/certificates", icon: FileCheck },
    { name: "Analytics", href: "/analytics", icon: BarChart2 },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <div className="w-64 bg-slate-900 text-white flex flex-col">
        <div className="h-16 flex items-center px-4 bg-slate-950 border-b border-slate-800">
          <Shield className="h-8 w-8 text-orange-500 mr-2" />
          <span className="font-bold text-lg tracking-wide">Suraksha-AR</span>
        </div>
        
        <div className="flex-1 overflow-y-auto py-4">
          <nav className="px-2 space-y-1">
            {navigation.map((item) => {
              const active = location.pathname.startsWith(item.href);
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                    active ? "bg-slate-800 text-white" : "text-slate-300 hover:bg-slate-700 hover:text-white"
                  }`}
                >
                  <item.icon className={`mr-3 flex-shrink-0 h-5 w-5 ${active ? "text-orange-500" : "text-slate-400 group-hover:text-slate-300"}`} />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
        
        <div className="p-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-white">{user.name}</p>
            <p className="text-xs text-slate-400 capitalize">{user.role}</p>
          </div>
          <button onClick={logout} className="text-slate-400 hover:text-white p-2">
            <LogOut className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-y-auto p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
