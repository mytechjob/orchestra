import { useAuthStore } from '../store/authStore';
import { 
  BarChart3, 
  Users, 
  MessageSquare, 
  Activity,
  ArrowUpRight,
  Sparkles
} from 'lucide-react';
import { motion } from 'framer-motion';

const StatCard = ({ title, value, icon: Icon, trend, color }: any) => (
  <motion.div 
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-slate-900/50 border border-slate-800 p-6 rounded-3xl hover:border-slate-700 transition-all group"
  >
    <div className="flex justify-between items-start mb-4">
      <div className={cn("p-3 rounded-2xl bg-opacity-10", color)}>
        <Icon className={cn("w-6 h-6", color.replace('bg-', 'text-'))} />
      </div>
      <span className="flex items-center text-xs font-bold text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded-full uppercase tracking-wider">
        <ArrowUpRight className="w-3 h-3 mr-1" />
        {trend}
      </span>
    </div>
    <p className="text-slate-500 text-sm font-semibold mb-1 uppercase tracking-tight">{title}</p>
    <h3 className="text-3xl font-bold text-white tracking-tight">{value}</h3>
  </motion.div>
);

import { cn } from '../lib/utils';

const Dashboard = () => {
  const { user } = useAuthStore();

  return (
    <div className="space-y-10 max-w-7xl mx-auto">
      <header className="flex justify-between items-end">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 mb-2 font-bold tracking-widest text-xs uppercase">
            <Sparkles className="w-4 h-4" />
            <span>Welcome Back</span>
          </div>
          <h1 className="text-4xl font-extrabold text-white tracking-tight capitalize">
            {user?.username}'s Dashboard
          </h1>
          <p className="text-slate-400 mt-2 font-medium">Monitor your agent's performance and customer interactions.</p>
        </div>
        
        <div className="flex gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl px-6 py-3 text-sm font-bold flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            System Live
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Total Customers" 
          value="1,284" 
          icon={Users} 
          trend="12%" 
          color="bg-indigo-500" 
        />
        <StatCard 
          title="Active Chats" 
          value="42" 
          icon={MessageSquare} 
          trend="8%" 
          color="bg-purple-500" 
        />
        <StatCard 
          title="API Latency" 
          value="124ms" 
          icon={Activity} 
          trend="5%" 
          color="bg-blue-500" 
        />
        <StatCard 
          title="Agent Success" 
          value="94.2%" 
          icon={BarChart3} 
          trend="2%" 
          color="bg-pink-500" 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-slate-900/50 border border-slate-800 rounded-3xl p-8 min-h-[400px]">
          <h3 className="text-xl font-bold text-white mb-6">Conversation Trends</h3>
          <div className="h-64 flex items-end justify-between gap-2 px-4">
            {[40, 70, 45, 90, 65, 80, 55, 95, 75, 40, 85, 60].map((h, i) => (
              <motion.div 
                key={i}
                initial={{ height: 0 }}
                animate={{ height: `${h}%` }}
                transition={{ delay: i * 0.05, duration: 1 }}
                className="flex-1 bg-gradient-to-t from-indigo-600 to-indigo-400 rounded-lg group relative"
              >
                <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                  {h} messages
                </div>
              </motion.div>
            ))}
          </div>
          <div className="flex justify-between mt-6 text-slate-500 text-xs font-bold uppercase tracking-widest px-4">
            <span>Jan</span>
            <span>Mar</span>
            <span>May</span>
            <span>Jul</span>
            <span>Sep</span>
            <span>Nov</span>
          </div>
        </div>

        <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-8">
          <h3 className="text-xl font-bold text-white mb-6">Recent Activity</h3>
          <div className="space-y-6">
            {[
              { text: 'New customer "Sarah" extracted', time: '2 mins ago', icon: Sparkles },
              { text: 'User "Admin" added to system', time: '1 hour ago', icon: Users },
              { text: 'Agent resolved conversation #124', time: '3 hours ago', icon: MessageSquare },
              { text: 'System backup completed', time: 'Yesterday', icon: Activity },
            ].map((item, i) => (
              <div key={i} className="flex gap-4">
                <div className="w-8 h-8 rounded-xl bg-slate-800 flex items-center justify-center shrink-0">
                  <item.icon className="w-4 h-4 text-slate-400" />
                </div>
                <div>
                  <p className="text-sm text-slate-300 font-medium">{item.text}</p>
                  <p className="text-xs text-slate-500 mt-1 font-bold uppercase tracking-tighter">{item.time}</p>
                </div>
              </div>
            ))}
          </div>
          <button className="w-full mt-8 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded-2xl transition-colors text-sm uppercase tracking-widest">
            View All Activity
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
