import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import {
  Users,
  MessageSquare,
  TrendingUp,
  Bell,
  Sparkles,
  LogOut,
  Menu,
  Search,
  Filter,
  ArrowRight,
  User,
  CheckCircle,
  Clock,
  AlertCircle,
  Zap,
  Target,
  Award,
  Activity,
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { matchingApi, notificationApi } from '../lib/api';
import { socketService } from '../lib/socket';
import { calculateMatchScore, formatRelativeTime, getStatusColor } from '../lib/utils';

export default function DashboardPage() {
  const { user, clearAuth } = useAuthStore();

  const { data: matches = [] } = useQuery({
    queryKey: ['matches', user?.id],
    queryFn: () => matchingApi.getMatches(user!.id),
    enabled: !!user,
  });

  const { data: notifications = [] } = useQuery({
    queryKey: ['notifications', user?.id],
    queryFn: () => notificationApi.getNotifications(user!.id, true),
    enabled: !!user,
  });

  useEffect(() => {
    if (user) {
      socketService.joinRoom(`user:${user.id}`);
    }

    return () => {
      if (user) {
        socketService.leaveRoom(`user:${user.id}`);
      }
    };
  }, [user]);

  const handleLogout = () => {
    socketService.disconnect();
    clearAuth();
  };

  const pendingMatches = matches.filter((m) => m.status === 'pending');
  const activeNegotiations = matches.filter((m) => m.status === 'negotiating');
  const acceptedMatches = matches.filter((m) => m.status === 'accepted');

  const stats = [
    {
      icon: Target,
      label: 'Pending Matches',
      value: pendingMatches.length,
      gradient: 'from-violet-500 to-purple-600',
      bgGradient: 'from-violet-50 to-purple-50',
      iconBg: 'bg-violet-100',
      textColor: 'text-violet-600',
      link: '/matches?filter=pending',
      trend: '+12%',
      trendUp: true,
    },
    {
      icon: MessageSquare,
      label: 'In Negotiation',
      value: activeNegotiations.length,
      gradient: 'from-amber-500 to-orange-600',
      bgGradient: 'from-amber-50 to-orange-50',
      iconBg: 'bg-amber-100',
      textColor: 'text-amber-600',
      link: '/matches?filter=negotiating',
      trend: '+5%',
      trendUp: true,
    },
    {
      icon: Award,
      label: 'Active Partnerships',
      value: acceptedMatches.length,
      gradient: 'from-emerald-500 to-teal-600',
      bgGradient: 'from-emerald-50 to-teal-50',
      iconBg: 'bg-emerald-100',
      textColor: 'text-emerald-600',
      link: '/connections',
      trend: '+8%',
      trendUp: true,
    },
    {
      icon: Bell,
      label: 'New Alerts',
      value: notifications.length,
      gradient: 'from-rose-500 to-pink-600',
      bgGradient: 'from-rose-50 to-pink-50',
      iconBg: 'bg-rose-100',
      textColor: 'text-rose-600',
      link: '#',
      trend: notifications.length > 0 ? 'New' : '',
      trendUp: notifications.length > 0,
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      {/* Top Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200/60 sticky top-0 z-50">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link to="/dashboard" className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-violet-500/30">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
                  Bond.AI
                </span>
              </Link>

              <div className="hidden md:flex items-center space-x-1">
                <Link to="/dashboard" className="px-4 py-2 rounded-lg bg-slate-100 text-slate-900 font-medium text-sm">
                  Dashboard
                </Link>
                <Link to="/matches" className="px-4 py-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-50 font-medium text-sm transition-colors">
                  Matches
                </Link>
                <Link to="/connections" className="px-4 py-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-50 font-medium text-sm transition-colors">
                  Connections
                </Link>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <button className="p-2.5 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg relative transition-colors">
                <Bell className="w-5 h-5" />
                {notifications.length > 0 && (
                  <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-rose-500 rounded-full ring-2 ring-white" />
                )}
              </button>

              <div className="flex items-center space-x-3 pl-3 border-l border-slate-200">
                <Link to="/profile" className="flex items-center space-x-2.5 hover:opacity-80 transition-opacity">
                  <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-slate-700 to-slate-900 flex items-center justify-center">
                    <User className="w-4 h-4 text-white" />
                  </div>
                  <span className="text-sm font-medium text-slate-700 hidden md:block">
                    {user?.name || user?.email}
                  </span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container-custom py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center space-x-2 mb-2">
            <h1 className="text-2xl md:text-3xl font-bold text-slate-900">
              Welcome back, {user?.name?.split(' ')[0] || 'there'}
            </h1>
            <span className="text-2xl">👋</span>
          </div>
          <p className="text-slate-500 text-sm md:text-base">
            Your AI agents are actively working to find your perfect partnerships
          </p>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Link
                to={stat.link}
                className={`block p-5 rounded-2xl bg-gradient-to-br ${stat.bgGradient} border border-white/60 hover:shadow-lg hover:shadow-slate-200/50 transition-all duration-300 group`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-11 h-11 rounded-xl ${stat.iconBg} flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
                    <stat.icon className={`w-5 h-5 ${stat.textColor}`} />
                  </div>
                  {stat.trend && (
                    <span className={`text-xs font-semibold px-2 py-1 rounded-full ${stat.trendUp ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-600'}`}>
                      {stat.trend}
                    </span>
                  )}
                </div>
                <div>
                  <p className="text-3xl font-bold text-slate-900 mb-1">{stat.value}</p>
                  <p className="text-sm text-slate-600">{stat.label}</p>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Recent Matches */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl border border-slate-200/60 shadow-sm p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900">Recent Matches</h2>
                  <p className="text-sm text-slate-500 mt-0.5">Your latest partnership opportunities</p>
                </div>
                <Link
                  to="/matches"
                  className="inline-flex items-center text-sm font-medium text-violet-600 hover:text-violet-700 transition-colors"
                >
                  View all
                  <ArrowRight className="w-4 h-4 ml-1" />
                </Link>
              </div>

              <div className="space-y-3">
                {matches.slice(0, 5).length === 0 ? (
                  <div className="text-center py-12 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50/50">
                    <div className="w-14 h-14 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-4">
                      <Users className="w-7 h-7 text-slate-400" />
                    </div>
                    <p className="text-slate-600 font-medium mb-1">No matches yet</p>
                    <p className="text-sm text-slate-400">
                      Your AI agents are searching for partnerships
                    </p>
                  </div>
                ) : (
                  matches.slice(0, 5).map((match, index) => {
                    const { percentage, label, color } = calculateMatchScore(match.score);
                    const statusColors = {
                      pending: 'bg-amber-50 text-amber-700 border-amber-200',
                      negotiating: 'bg-blue-50 text-blue-700 border-blue-200',
                      accepted: 'bg-emerald-50 text-emerald-700 border-emerald-200',
                      rejected: 'bg-slate-50 text-slate-600 border-slate-200',
                    };
                    return (
                      <motion.div
                        key={match.id}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                        className="flex items-center justify-between p-4 rounded-xl bg-slate-50/50 hover:bg-slate-100/80 border border-slate-100 hover:border-slate-200 transition-all group"
                      >
                        <div className="flex items-center space-x-4">
                          <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center shadow-md shadow-violet-500/20">
                            <User className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h3 className="font-medium text-slate-900 text-sm">
                              {match.matchedUser.name || match.matchedUser.email}
                            </h3>
                            <div className="flex items-center space-x-2 mt-1">
                              <div className="flex items-center space-x-1">
                                <div className={`w-1.5 h-1.5 rounded-full ${percentage >= 75 ? 'bg-emerald-500' : percentage >= 60 ? 'bg-blue-500' : 'bg-amber-500'}`} />
                                <span className={`text-xs font-semibold ${percentage >= 75 ? 'text-emerald-600' : percentage >= 60 ? 'text-blue-600' : 'text-amber-600'}`}>
                                  {percentage}% match
                                </span>
                              </div>
                              <span className="text-slate-300">•</span>
                              <span className={`text-xs px-2 py-0.5 rounded-md border font-medium capitalize ${statusColors[match.status as keyof typeof statusColors] || statusColors.pending}`}>
                                {match.status}
                              </span>
                            </div>
                          </div>
                        </div>
                        <Link
                          to={`/matches/${match.id}`}
                          className="px-3 py-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 bg-white border border-slate-200 hover:border-slate-300 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
                        >
                          View
                        </Link>
                      </motion.div>
                    );
                  })
                )}
              </div>
            </div>
          </div>

          {/* Activity Feed */}
          <div className="bg-white rounded-2xl border border-slate-200/60 shadow-sm p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-semibold text-slate-900">Activity</h2>
                <p className="text-sm text-slate-500 mt-0.5">Recent updates</p>
              </div>
              <Activity className="w-5 h-5 text-slate-400" />
            </div>

            <div className="space-y-4">
              {notifications.length === 0 ? (
                <div className="text-center py-8">
                  <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-3">
                    <Bell className="w-6 h-6 text-slate-400" />
                  </div>
                  <p className="text-slate-500 text-sm">No new updates</p>
                </div>
              ) : (
                notifications.slice(0, 8).map((notification, index) => (
                  <motion.div
                    key={notification.id}
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="flex items-start space-x-3 group"
                  >
                    <div
                      className={`w-2 h-2 rounded-full mt-2 ring-4 ${
                        notification.type === 'new_match'
                          ? 'bg-emerald-500 ring-emerald-100'
                          : notification.type === 'proposal_received'
                          ? 'bg-blue-500 ring-blue-100'
                          : 'bg-slate-400 ring-slate-100'
                      }`}
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-slate-700 leading-snug">{notification.message}</p>
                      <p className="text-xs text-slate-400 mt-1">
                        {formatRelativeTime(notification.createdAt)}
                      </p>
                    </div>
                  </motion.div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Agent Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-6 p-6 rounded-2xl bg-gradient-to-r from-violet-500 via-purple-500 to-indigo-500 shadow-xl shadow-violet-500/20"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-14 h-14 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center">
                <Zap className="w-7 h-7 text-white animate-pulse" />
              </div>
              <div>
                <h3 className="font-semibold text-white text-lg">AI Agents Active</h3>
                <p className="text-sm text-white/80 mt-0.5">
                  Analyzing {pendingMatches.length} potential partnerships for you
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse shadow-lg shadow-emerald-400/50" />
              <span className="text-sm font-medium text-white">Online</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
