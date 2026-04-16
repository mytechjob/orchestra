import { Outlet, Link, useLocation } from 'react-router';
import {
  LayoutDashboard,
  Users as UsersIcon,
  MessageSquare,
  UserCircle,
  LogOut,
  Database
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { cn } from '../lib/utils';

const Layout = () => {
  const { user, logout } = useAuthStore();
  const location = useLocation();

  const menuItems = [
    { name: 'Dashboard', icon: LayoutDashboard, path: '/' },
    { name: 'Customers', icon: Database, path: '/customers' },
    { name: 'Agent Chat', icon: MessageSquare, path: '/chat' },
  ];

  if (user?.role === 'admin') {
    menuItems.push({ name: 'System Users', icon: UsersIcon, path: '/users' });
  }

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="w-72 bg-slate-900 border-r border-slate-800 flex flex-col">
        <div className="p-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <MessageSquare className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
              Agent Bot
            </h1>
          </div>
        </div>

        <nav className="flex-1 px-4 space-y-1">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
            return (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group relative",
                  isActive
                    ? "bg-indigo-600/10 text-indigo-400"
                    : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
                )}
              >
                <item.icon className={cn("w-5 h-5", isActive ? "text-indigo-400" : "group-hover:text-slate-200")} />
                <span className="font-medium">{item.name}</span>
                {isActive && <div className="absolute left-0 w-1 h-6 bg-indigo-500 rounded-r-full" />}
              </Link>
            );
          })}
        </nav>

        <div className="p-4 mt-auto border-t border-slate-800 bg-slate-900/50">
          <div className="flex items-center gap-3 px-4 py-3 mb-4">
            <div className="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center ring-2 ring-slate-700">
              <UserCircle className="w-6 h-6 text-slate-400" />
            </div>
            <div className="flex-1 overflow-hidden">
              <p className="text-sm font-semibold truncate capitalize">{user?.username}</p>
              <p className="text-xs text-slate-500 truncate lowercase">{user?.role}</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-3 w-full px-4 py-3 text-slate-400 hover:text-red-400 hover:bg-red-400/5 rounded-xl transition-colors font-medium"
          >
            <LogOut className="w-5 h-5" />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-slate-950 relative overflow-x-hidden">
        {/* Subtle decorative elements */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-500/5 blur-[120px] rounded-full -mr-64 -mt-64" />
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-purple-500/5 blur-[120px] rounded-full -ml-64 -mb-64" />

        <div className="p-8 relative z-10">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Layout;
