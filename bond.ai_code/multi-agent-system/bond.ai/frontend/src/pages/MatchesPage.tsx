import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import {
  Users,
  Filter,
  Search,
  Sparkles,
  User,
  CheckCircle,
  X,
  MessageSquare,
  TrendingUp,
  ArrowLeft,
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { matchingApi } from '../lib/api';
import { calculateMatchScore, getStatusColor, formatRelativeTime } from '../lib/utils';

export default function MatchesPage() {
  const { user } = useAuthStore();
  const queryClient = useQueryClient();
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const { data: matches = [], isLoading } = useQuery({
    queryKey: ['matches', user?.id, filterStatus],
    queryFn: () =>
      matchingApi.getMatches(user!.id, filterStatus === 'all' ? undefined : filterStatus),
    enabled: !!user,
  });

  const acceptMutation = useMutation({
    mutationFn: (matchId: string) => matchingApi.acceptMatch(matchId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['matches'] });
      toast.success('Match accepted! Starting negotiation...');
    },
    onError: () => {
      toast.error('Failed to accept match');
    },
  });

  const rejectMutation = useMutation({
    mutationFn: (matchId: string) => matchingApi.rejectMatch(matchId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['matches'] });
      toast.success('Match rejected');
    },
    onError: () => {
      toast.error('Failed to reject match');
    },
  });

  const filteredMatches = matches.filter((match) => {
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      const name = match.matchedUser.name?.toLowerCase() || '';
      const email = match.matchedUser.email.toLowerCase();
      return name.includes(query) || email.includes(query);
    }
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <ArrowLeft className="w-5 h-5 text-gray-600" />
              <span className="text-gray-900 font-medium">Back to Dashboard</span>
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container-custom py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Matches</h1>
          <p className="text-gray-600">
            AI-curated partnerships based on your needs and offerings
          </p>
        </div>

        {/* Filters */}
        <div className="card mb-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search matches..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input pl-11 w-full"
              />
            </div>

            <div className="flex items-center space-x-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="input"
              >
                <option value="all">All Matches</option>
                <option value="pending">Pending</option>
                <option value="negotiating">Negotiating</option>
                <option value="accepted">Accepted</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          {[
            { label: 'Total Matches', value: matches.length, color: 'blue' },
            {
              label: 'Pending',
              value: matches.filter((m) => m.status === 'pending').length,
              color: 'yellow',
            },
            {
              label: 'Negotiating',
              value: matches.filter((m) => m.status === 'negotiating').length,
              color: 'purple',
            },
            {
              label: 'Accepted',
              value: matches.filter((m) => m.status === 'accepted').length,
              color: 'green',
            },
          ].map((stat, index) => (
            <div key={index} className="card text-center">
              <div className={`text-3xl font-bold text-${stat.color}-600`}>{stat.value}</div>
              <div className="text-sm text-gray-600 mt-1">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Matches List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full mx-auto" />
            <p className="text-gray-600 mt-4">Loading matches...</p>
          </div>
        ) : filteredMatches.length === 0 ? (
          <div className="card text-center py-12">
            <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No matches found</h3>
            <p className="text-gray-600">
              {searchQuery
                ? 'Try adjusting your search'
                : 'Your AI agents are searching for perfect partnerships'}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredMatches.map((match, index) => {
              const { percentage, label, color } = calculateMatchScore(match.score);
              return (
                <motion.div
                  key={match.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="card hover:shadow-lg transition-shadow"
                >
                  <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                    <div className="flex items-start space-x-4 flex-1">
                      <div className="w-16 h-16 rounded-full bg-gradient-secondary flex items-center justify-center flex-shrink-0">
                        <User className="w-8 h-8 text-white" />
                      </div>

                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {match.matchedUser.name || match.matchedUser.email}
                          </h3>
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
                              match.status
                            )}`}
                          >
                            {match.status}
                          </span>
                        </div>

                        <div className="flex items-center space-x-4 mb-3">
                          <div className="flex items-center space-x-2">
                            <TrendingUp className={`w-4 h-4 ${color}`} />
                            <span className={`font-semibold ${color}`}>
                              {percentage}% Match
                            </span>
                          </div>
                          <span className="text-sm text-gray-500">
                            {formatRelativeTime(match.createdAt)}
                          </span>
                        </div>

                        {match.matchReasons && match.matchReasons.length > 0 && (
                          <div className="space-y-1">
                            <p className="text-sm font-medium text-gray-700">Match Reasons:</p>
                            <ul className="space-y-1">
                              {match.matchReasons.slice(0, 3).map((reason, i) => (
                                <li key={i} className="text-sm text-gray-600 flex items-start">
                                  <CheckCircle className="w-4 h-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                                  {reason}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex lg:flex-col gap-2 lg:min-w-[140px]">
                      {match.status === 'pending' && (
                        <>
                          <button
                            onClick={() => acceptMutation.mutate(match.id)}
                            disabled={acceptMutation.isPending}
                            className="btn-primary flex-1 lg:flex-none"
                          >
                            <CheckCircle className="w-4 h-4 mr-2" />
                            Accept
                          </button>
                          <button
                            onClick={() => rejectMutation.mutate(match.id)}
                            disabled={rejectMutation.isPending}
                            className="btn-outline flex-1 lg:flex-none"
                          >
                            <X className="w-4 h-4 mr-2" />
                            Reject
                          </button>
                        </>
                      )}

                      {match.status === 'negotiating' && (
                        <Link
                          to={`/negotiations/${match.id}`}
                          className="btn-primary flex-1 lg:flex-none"
                        >
                          <MessageSquare className="w-4 h-4 mr-2" />
                          View Chat
                        </Link>
                      )}

                      {match.status === 'accepted' && (
                        <Link
                          to={`/connections/${match.id}`}
                          className="btn-primary flex-1 lg:flex-none"
                        >
                          View Connection
                        </Link>
                      )}
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
