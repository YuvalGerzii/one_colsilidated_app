import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import {
  Users,
  User,
  ArrowLeft,
  Calendar,
  CheckCircle,
  MessageSquare,
  Sparkles,
  Award,
  Handshake,
  PauseCircle,
  TrendingUp,
  ArrowUpRight,
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { connectionApi } from '../lib/api';
import { formatDate } from '../lib/utils';

export default function ConnectionsPage() {
  const { user } = useAuthStore();

  const { data: connections = [], isLoading } = useQuery({
    queryKey: ['connections', user?.id],
    queryFn: () => connectionApi.getConnections(user!.id),
    enabled: !!user,
  });

  const activeConnections = connections.filter((c) => c.status === 'active');
  const pausedConnections = connections.filter((c) => c.status === 'paused');

  const stats = [
    {
      icon: Award,
      label: 'Total Partnerships',
      value: connections.length,
      bgGradient: 'from-violet-50 to-purple-50',
      iconBg: 'bg-violet-100',
      textColor: 'text-violet-600',
      valueColor: 'text-violet-700',
    },
    {
      icon: Handshake,
      label: 'Active',
      value: activeConnections.length,
      bgGradient: 'from-emerald-50 to-teal-50',
      iconBg: 'bg-emerald-100',
      textColor: 'text-emerald-600',
      valueColor: 'text-emerald-700',
    },
    {
      icon: PauseCircle,
      label: 'Paused',
      value: pausedConnections.length,
      bgGradient: 'from-amber-50 to-orange-50',
      iconBg: 'bg-amber-100',
      textColor: 'text-amber-600',
      valueColor: 'text-amber-700',
    },
  ];

  const getStatusStyles = (status: string) => {
    switch (status) {
      case 'active':
        return {
          bg: 'bg-emerald-50',
          text: 'text-emerald-700',
          border: 'border-emerald-200',
          dot: 'bg-emerald-500',
        };
      case 'paused':
        return {
          bg: 'bg-amber-50',
          text: 'text-amber-700',
          border: 'border-amber-200',
          dot: 'bg-amber-500',
        };
      default:
        return {
          bg: 'bg-slate-50',
          text: 'text-slate-600',
          border: 'border-slate-200',
          dot: 'bg-slate-400',
        };
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200/60 sticky top-0 z-50">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            <Link
              to="/dashboard"
              className="flex items-center space-x-2 text-slate-600 hover:text-slate-900 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span className="font-medium">Back to Dashboard</span>
            </Link>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-violet-500/30">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
                Bond.AI
              </span>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container-custom py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center space-x-3 mb-2">
            <h1 className="text-2xl md:text-3xl font-bold text-slate-900">Your Partnerships</h1>
            <div className="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200">
              <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />
              <span className="text-xs font-semibold text-emerald-700">Growing</span>
            </div>
          </div>
          <p className="text-slate-500">
            Active collaborations and partnerships you've established
          </p>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`p-5 rounded-2xl bg-gradient-to-br ${stat.bgGradient} border border-white/60`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className={`text-3xl font-bold ${stat.valueColor} mb-1`}>{stat.value}</p>
                  <p className="text-sm text-slate-600">{stat.label}</p>
                </div>
                <div className={`w-12 h-12 rounded-xl ${stat.iconBg} flex items-center justify-center`}>
                  <stat.icon className={`w-6 h-6 ${stat.textColor}`} />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Connections List */}
        {isLoading ? (
          <div className="text-center py-16">
            <div className="animate-spin w-12 h-12 border-4 border-violet-600 border-t-transparent rounded-full mx-auto" />
            <p className="text-slate-500 mt-4">Loading partnerships...</p>
          </div>
        ) : connections.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-2xl border border-slate-200/60 shadow-sm p-12 text-center"
          >
            <div className="w-20 h-20 rounded-2xl bg-slate-100 flex items-center justify-center mx-auto mb-6">
              <Users className="w-10 h-10 text-slate-400" />
            </div>
            <h3 className="text-xl font-semibold text-slate-900 mb-2">No partnerships yet</h3>
            <p className="text-slate-500 mb-6 max-w-md mx-auto">
              Accept matches to start building your professional network and create valuable partnerships
            </p>
            <Link
              to="/matches"
              className="inline-flex items-center px-5 py-2.5 bg-gradient-to-r from-violet-600 to-indigo-600 text-white font-medium rounded-xl hover:shadow-lg hover:shadow-violet-500/30 transition-all"
            >
              View Matches
              <ArrowUpRight className="w-4 h-4 ml-2" />
            </Link>
          </motion.div>
        ) : (
          <div className="space-y-4">
            {connections.map((connection, index) => {
              const statusStyles = getStatusStyles(connection.status);
              return (
                <motion.div
                  key={connection.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="bg-white rounded-2xl border border-slate-200/60 shadow-sm hover:shadow-lg hover:shadow-slate-200/50 transition-all p-6"
                >
                  <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                    <div className="flex items-start space-x-4 flex-1">
                      <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center flex-shrink-0 shadow-lg shadow-violet-500/20">
                        <User className="w-7 h-7 text-white" />
                      </div>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center flex-wrap gap-2 mb-2">
                          <h3 className="text-lg font-semibold text-slate-900">
                            {connection.connectedUser.name || connection.connectedUser.email}
                          </h3>
                          <span
                            className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium border ${statusStyles.bg} ${statusStyles.text} ${statusStyles.border}`}
                          >
                            <span className={`w-1.5 h-1.5 rounded-full ${statusStyles.dot} mr-1.5`} />
                            {connection.status}
                          </span>
                        </div>

                        {connection.relationship && (
                          <p className="text-sm text-slate-600 mb-3">{connection.relationship}</p>
                        )}

                        <div className="flex items-center text-sm text-slate-500">
                          <Calendar className="w-4 h-4 mr-1.5" />
                          <span>Partnership started {formatDate(connection.createdAt)}</span>
                        </div>

                        {connection.agreedTerms && (
                          <div className="mt-4 p-4 bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl border border-emerald-100">
                            <div className="flex items-center space-x-2 mb-3">
                              <div className="w-6 h-6 rounded-md bg-emerald-100 flex items-center justify-center">
                                <CheckCircle className="w-4 h-4 text-emerald-600" />
                              </div>
                              <span className="text-sm font-semibold text-emerald-900">
                                Partnership Agreement
                              </span>
                            </div>
                            <div className="grid md:grid-cols-2 gap-4 text-sm">
                              <div>
                                <p className="font-medium text-slate-700 mb-2">What you receive</p>
                                <ul className="space-y-1.5">
                                  {connection.agreedTerms.terms.party1Gets?.map((item, i) => (
                                    <li key={i} className="flex items-start text-slate-600">
                                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 mr-2 flex-shrink-0" />
                                      {item}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                              <div>
                                <p className="font-medium text-slate-700 mb-2">What you provide</p>
                                <ul className="space-y-1.5">
                                  {connection.agreedTerms.terms.party1Gives?.map((item, i) => (
                                    <li key={i} className="flex items-start text-slate-600">
                                      <span className="w-1.5 h-1.5 rounded-full bg-violet-500 mt-1.5 mr-2 flex-shrink-0" />
                                      {item}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex lg:flex-col gap-2 lg:min-w-[140px]">
                      <button className="flex-1 lg:flex-none inline-flex items-center justify-center px-4 py-2.5 bg-gradient-to-r from-violet-600 to-indigo-600 text-white font-medium rounded-xl hover:shadow-lg hover:shadow-violet-500/30 transition-all text-sm">
                        <MessageSquare className="w-4 h-4 mr-2" />
                        Message
                      </button>
                      <Link
                        to={`/connections/${connection.id}`}
                        className="flex-1 lg:flex-none inline-flex items-center justify-center px-4 py-2.5 bg-white text-slate-700 font-medium rounded-xl border border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all text-sm"
                      >
                        View Details
                      </Link>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
