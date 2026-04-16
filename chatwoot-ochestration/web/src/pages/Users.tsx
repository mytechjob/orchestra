import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  Mail,
  Plus,
  Shield,
  Trash2,
  UserCheck,
  UserPlus
} from 'lucide-react';
import React, { useState } from 'react';
import { toast } from 'react-hot-toast';
import { userService } from '../services/userService';
import type { User } from '../types';

const Users = () => {
  const [showAddModal, setShowAddModal] = useState(false);
  const [newUserData, setNewUserData] = useState({ username: '', email: '', password: '', role: 'user' });
  const queryClient = useQueryClient();

  const { data: users, isLoading } = useQuery<User[]>({
    queryKey: ['users'],
    queryFn: userService.getUsers
  });

  const createUserMutation = useMutation({
    mutationFn: userService.createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast.success('User created successfully');
      setShowAddModal(false);
      setNewUserData({ username: '', email: '', password: '', role: 'user' });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create user');
    }
  });

  const handleAddUser = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUserData.username || !newUserData.email || !newUserData.password) {
      toast.error('Please fill in all fields');
      return;
    }
    createUserMutation.mutate(newUserData);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500">
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h1 className="text-4xl font-extrabold text-white tracking-tight">System Users</h1>
          <p className="text-slate-400 mt-1 font-medium italic">Manage administrative and standard user access.</p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3.5 rounded-2xl font-bold flex items-center justify-center gap-2 shadow-xl shadow-indigo-600/20 active:scale-95 transition-all"
        >
          <UserPlus className="w-5 h-5" />
          Add New User
        </button>
      </header>

      {/* Users Table */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-900/40 border-b border-slate-800">
                <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">User Profile</th>
                <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">System Role</th>
                <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">Status</th>
                <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest text-right">Access Control</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {isLoading ? (
                [1, 2, 3].map(i => (
                  <tr key={i} className="animate-pulse">
                    <td colSpan={4} className="p-8 h-20 bg-slate-800/20" />
                  </tr>
                ))
              ) : users?.map((user) => (
                <tr key={user.id} className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-6">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-slate-800 border border-slate-700 rounded-xl flex items-center justify-center">
                        <UserCheck className="w-6 h-6 text-slate-500" />
                      </div>
                      <div>
                        <p className="text-white font-bold tracking-tight capitalize">{user.username}</p>
                        <p className="text-slate-500 text-xs font-medium lowercase flex items-center gap-1.5 mt-0.5">
                          <Mail className="w-3 h-3" />
                          {user.email}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td className="p-6">
                    <span className={cn(
                      "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border",
                      user.role === 'admin'
                        ? "bg-indigo-500/10 text-indigo-400 border-indigo-500/20"
                        : "bg-slate-800/50 text-slate-500 border-slate-800"
                    )}>
                      {user.role === 'admin' ? <Shield className="w-3 h-3" /> : null}
                      {user.role}
                    </span>
                  </td>
                  <td className="p-6">
                    <div className="flex items-center gap-2 text-sm text-slate-400 font-medium">
                      <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                      Active
                    </div>
                  </td>
                  <td className="p-6 text-right">
                    <button className="text-slate-600 hover:text-red-400 p-2 transition-colors">
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add User Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-300">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-10 w-full max-w-md shadow-2xl relative">
            <button
              onClick={() => setShowAddModal(false)}
              className="absolute top-6 right-6 text-slate-500 hover:text-white transition-colors"
            >
              <Plus className="w-6 h-6 rotate-45" />
            </button>
            <h2 className="text-2xl font-bold text-white mb-2 tracking-tight">Create System User</h2>
            <p className="text-slate-500 mb-8 font-medium">Grant new access privileges to the dashboard.</p>

            <form onSubmit={handleAddUser} className="space-y-5">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2 ml-1">Username</label>
                <input
                  type="text"
                  value={newUserData.username}
                  onChange={(e) => setNewUserData({ ...newUserData, username: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-2xl px-5 py-3.5 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all font-medium"
                  placeholder="Enter username"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2 ml-1">Email</label>
                <input
                  type="email"
                  value={newUserData.email}
                  onChange={(e) => setNewUserData({ ...newUserData, email: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-2xl px-5 py-3.5 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all font-medium"
                  placeholder="Email address"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2 ml-1">Initial Password</label>
                <input
                  type="password"
                  value={newUserData.password}
                  onChange={(e) => setNewUserData({ ...newUserData, password: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-2xl px-5 py-3.5 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all font-medium"
                  placeholder="••••••••"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2 ml-1">Assigned Role</label>
                <select
                  value={newUserData.role}
                  onChange={(e) => setNewUserData({ ...newUserData, role: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-2xl px-5 py-3.5 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all font-medium appearance-none"
                >
                  <option value="user">Standard User</option>
                  <option value="admin">Administrator</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={createUserMutation.isPending}
                className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-600/50 text-white font-bold py-4 rounded-2xl shadow-xl shadow-indigo-600/20 transition-all mt-4"
              >
                {createUserMutation.isPending ? 'Processing...' : 'Provision Account'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

import { cn } from '../lib/utils';
export default Users;
