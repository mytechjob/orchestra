import React from 'react';
import { useParams, Link } from 'react-router';
import { useQuery } from '@tanstack/react-query';
import {
  ArrowLeft,
  MessageSquare,
  User as UserIcon,
  Mail,
  Phone,
  Clock,
  BadgeCheck,
  ChevronRight,
  Database,
  History
} from 'lucide-react';
import { customerService } from '../services/customerService';
import { cn } from '../lib/utils';

const CustomerDetails = () => {
  const { contactId } = useParams();

  const { data: customer, isLoading: isLoadingInfo } = useQuery({
    queryKey: ['customer', contactId],
    queryFn: () => customerService.getCustomerInfo(contactId!),
    enabled: !!contactId
  });

  const { data: conversationsData, isLoading: isLoadingConvs } = useQuery({
    queryKey: ['customer-conversations', contactId],
    queryFn: () => customerService.getCustomerConversations(contactId!),
    enabled: !!contactId
  });

  const isLoading = isLoadingInfo || isLoadingConvs;

  if (isLoading) return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="w-12 h-12 border-4 border-indigo-600/20 border-t-indigo-600 rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <Link to="/customers" className="inline-flex items-center text-slate-500 hover:text-indigo-400 font-bold uppercase tracking-widest text-xs transition-colors group">
        <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
        Back to Customers
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Sidebar */}
        <div className="space-y-6">
          <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-8 sticky top-8">
            <div className="flex flex-col items-center text-center">
              <div className="w-24 h-24 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-3xl flex items-center justify-center mb-6 shadow-2xl shadow-indigo-600/20">
                <span className="text-4xl font-bold text-white uppercase">{customer?.name?.[0] || '?'}</span>
              </div>
              <h2 className="text-2xl font-bold text-white uppercase tracking-tight mb-2">{customer?.name || 'Anonymous'}</h2>
              <span className="bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest border border-emerald-500/20 mb-8">
                Active Contact
              </span>

              <div className="w-full space-y-4 text-left border-t border-white/5 pt-8">
                <div className="group">
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Email Address</p>
                  <div className="flex items-center gap-3 p-3.5 bg-slate-950/50 rounded-2xl border border-slate-800 group-hover:border-slate-700 transition-colors">
                    <Mail className="w-4 h-4 text-indigo-400" />
                    <span className="text-sm truncate text-slate-300 font-medium">{customer?.email || 'Not available'}</span>
                  </div>
                </div>

                <div className="group">
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Phone Number</p>
                  <div className="flex items-center gap-3 p-3.5 bg-slate-950/50 rounded-2xl border border-slate-800 group-hover:border-slate-700 transition-colors">
                    <Phone className="w-4 h-4 text-indigo-400" />
                    <span className="text-sm text-slate-300 font-medium">{customer?.phone || 'Not available'}</span>
                  </div>
                </div>

                <div className="group">
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Chatwoot ID</p>
                  <div className="flex items-center gap-3 p-3.5 bg-slate-950/50 rounded-2xl border border-slate-800 group-hover:border-slate-700 transition-colors">
                    <BadgeCheck className="w-4 h-4 text-indigo-400" />
                    <span className="text-sm text-slate-300 font-medium">#{customer?.chatwoot_contact_id}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Details & Conversations */}
        <div className="lg:col-span-2 space-y-8">
          {/* Extracted Data */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-3xl p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-5">
              <Database className="w-32 h-32 text-white" />
            </div>
            <div className="flex items-center gap-3 mb-8">
              <div className="w-10 h-10 bg-indigo-600/10 rounded-xl flex items-center justify-center">
                <BadgeCheck className="w-5 h-5 text-indigo-400" />
              </div>
              <h3 className="text-xl font-bold text-white uppercase tracking-tight">Intelligence Profile</h3>
            </div>

            {customer?.extracted_data && Object.keys(customer.extracted_data).length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {Object.entries(customer.extracted_data).map(([key, value]: any) => (
                  <div key={key} className="p-4 bg-slate-950/50 rounded-2xl border border-slate-800">
                    <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">{key.replace(/_/g, ' ')}</p>
                    <p className="text-slate-200 font-medium capitalize">{String(value)}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-12 text-center bg-slate-950/50 rounded-2xl border border-slate-800 border-dashed">
                <p className="text-slate-500 font-medium italic">No intelligence data has been extracted for this contact yet.</p>
              </div>
            )}
          </section>

          {/* Conversations History */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-3xl overflow-hidden">
            <div className="p-8 border-b border-slate-800 bg-slate-900/40">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-purple-600/10 rounded-xl flex items-center justify-center">
                  <History className="w-5 h-5 text-purple-400" />
                </div>
                <h3 className="text-xl font-bold text-white uppercase tracking-tight">Interaction History</h3>
              </div>
            </div>

            <div className="divide-y divide-slate-800">
              {conversationsData?.conversations.map((conv) => (
                <div key={conv.conversation_id} className="p-8 hover:bg-white/[0.02] transition-colors">
                  <div className="flex justify-between items-center mb-6">
                    <div className="flex items-center gap-4">
                      <span className="px-3 py-1 bg-slate-950 border border-slate-800 rounded-lg text-xs font-bold text-slate-400 uppercase tracking-tighter shadow-sm">
                        ID {conv.conversation_id}
                      </span>
                      <div className="flex items-center text-slate-500 text-xs font-medium">
                        <Clock className="w-3.5 h-3.5 mr-1.5" />
                        {new Date(conv.created_at).toLocaleString()}
                      </div>
                    </div>
                    <span className={cn(
                      "px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border",
                      conv.status === 'open' ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20' : 'bg-slate-800 text-slate-500 border-slate-700'
                    )}>
                      {conv.status}
                    </span>
                  </div>

                  <div className="space-y-6">
                    {conv.messages.map((msg, i) => (
                      <div key={i} className={cn(
                        "flex",
                        msg.sender === 'user' ? "justify-start" : "justify-end"
                      )}>
                        <div className={cn(
                          "max-w-[85%] p-4 rounded-2xl text-sm font-medium leading-relaxed shadow-sm",
                          msg.sender === 'user'
                            ? "bg-slate-800 text-slate-200 rounded-tl-none border-l-2 border-indigo-500/50"
                            : "bg-indigo-600 text-white rounded-tr-none shadow-indigo-600/10"
                        )}>
                          <p>{msg.content}</p>
                          <span className={cn(
                            "text-[10px] block mt-2 opacity-50 font-bold uppercase tracking-tight",
                            msg.sender === 'user' ? "text-slate-400" : "text-white"
                          )}>
                            {new Date(msg.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}

              {conversationsData?.conversations.length === 0 && (
                <div className="p-20 text-center">
                  <p className="text-slate-600 font-bold uppercase tracking-widest text-sm">No recorded conversations</p>
                </div>
              )}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default CustomerDetails;
