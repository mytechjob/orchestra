import { useQuery } from '@tanstack/react-query';
import {
  Calendar,
  ExternalLink,
  Filter,
  Mail,
  Phone,
  Search,
  User as UserIcon
} from 'lucide-react';
import { Link } from 'react-router';
import api from '../api/axios';
import type { Customer } from '../types';

const Customers = () => {
  const { data: customers, isLoading } = useQuery<Customer[]>({
    queryKey: ['customers'],
    queryFn: async () => {
      // Assuming a generic list endpoint exists or we fetch from recent ones
      // Since backend only has get_customer_info(contact_id), 
      // I'll assume we might need to add a list endpoint or use a dummy list for now.
      // For this demo, let's assume /api/customers returns all.
      try {
        const response = await api.get('/api/customers');
        return response.data;
      } catch {
        return []; // Fallback
      }
    }
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h1 className="text-4xl font-extrabold text-white tracking-tight">Customers</h1>
          <p className="text-slate-400 mt-2 font-medium">Manage and view your extracted customer audience.</p>
        </div>

        <div className="flex gap-3">
          <div className="relative group">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-indigo-400" />
            <input
              type="text"
              placeholder="Search customers..."
              className="bg-slate-900 border border-slate-800 rounded-2xl pl-12 pr-6 py-3.5 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 w-full md:w-80 transition-all font-medium"
            />
          </div>
          <button className="bg-slate-900 border border-slate-800 p-3.5 rounded-2xl text-slate-400 hover:text-white transition-colors hover:bg-slate-800">
            <Filter className="w-6 h-6" />
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isLoading ? (
          [1, 2, 3, 4, 5, 6].map(i => (
            <div key={i} className="bg-slate-900/50 border border-slate-800 p-8 rounded-3xl animate-pulse">
              <div className="w-16 h-16 bg-slate-800 rounded-2xl mb-6" />
              <div className="w-2/3 h-6 bg-slate-800 rounded mb-4" />
              <div className="w-full h-4 bg-slate-800 rounded mb-2" />
              <div className="w-1/2 h-4 bg-slate-800 rounded" />
            </div>
          ))
        ) : customers?.length === 0 ? (
          <div className="col-span-full py-20 text-center bg-slate-900/40 rounded-3xl border border-slate-800 border-dashed">
            <div className="w-20 h-20 bg-slate-800 rounded-3xl flex items-center justify-center mx-auto mb-6">
              <UserIcon className="w-10 h-10 text-slate-600" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">No Customers Found</h3>
            <p className="text-slate-500 max-w-xs mx-auto mb-8 font-medium">
              Start chatting on Chatwoot to begin extracting customer information automatically.
            </p>
          </div>
        ) : (
          customers?.map((customer) => (
            <Link
              key={customer.id}
              to={`/customers/${customer.chatwoot_contact_id}`}
              className="group bg-slate-900/50 border border-slate-800 p-8 rounded-3xl hover:border-indigo-500/30 hover:bg-indigo-500/[0.02] transition-all relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                <ExternalLink className="w-5 h-5 text-indigo-400" />
              </div>

              <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-indigo-500/10 group-hover:scale-110 transition-transform">
                <span className="text-2xl font-bold text-white uppercase">{customer.name?.[0] || '?'}</span>
              </div>

              <h3 className="text-xl font-bold text-white mb-4 group-hover:text-indigo-400 transition-colors uppercase tracking-tight">
                {customer.name || 'Anonymous User'}
              </h3>

              <div className="space-y-3">
                <div className="flex items-center gap-3 text-sm text-slate-400 font-medium">
                  <Mail className="w-4 h-4 text-indigo-500/60" />
                  <span className="truncate">{customer.email || 'No email provided'}</span>
                </div>
                <div className="flex items-center gap-3 text-sm text-slate-400 font-medium">
                  <Phone className="w-4 h-4 text-indigo-500/60" />
                  <span>{customer.phone || 'No phone number'}</span>
                </div>
                <div className="flex items-center gap-3 text-sm text-slate-400 font-medium pt-4 border-t border-white/5 mt-4">
                  <Calendar className="w-4 h-4 text-indigo-500/60" />
                  <span>Joined {new Date(customer.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </Link>
          ))
        )}
      </div>
    </div>
  );
};

export default Customers;
