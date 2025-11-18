import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Search,
  Network,
  Brain,
  Zap,
  Building2,
  Briefcase,
  Users,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle,
  ChevronRight,
  Activity,
  Database,
  Globe,
  BarChart3,
  GitBranch,
  Workflow,
  History
} from 'lucide-react';

interface QueryResult {
  platform: string;
  agent: string;
  response: string;
  confidence: number;
  latency: number;
}

interface ActiveAgent {
  id: string;
  name: string;
  platform: string;
  status: 'active' | 'processing' | 'idle';
  lastQuery: string;
}

export default function CrossPlatformIntelligence() {
  const location = useLocation();
  const [query, setQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState<QueryResult[]>([]);
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['all']);
  const [queryHistory, setQueryHistory] = useState<{query: string; timestamp: string; results: number}[]>([
    { query: 'Find investors interested in multifamily', timestamp: '2 hours ago', results: 12 },
    { query: 'Analyze market impact on portfolio', timestamp: '5 hours ago', results: 8 },
    { query: 'Match skills to opportunities', timestamp: '1 day ago', results: 15 },
  ]);

  const featureNavigation = [
    { path: '/unified-platform/intelligence', name: 'Query', icon: Search, description: 'Cross-platform queries' },
    { path: '/unified-platform/intelligence/entities', name: 'Entities', icon: Network, description: 'Knowledge graph' },
    { path: '/unified-platform/intelligence/analytics', name: 'Analytics', icon: BarChart3, description: 'Platform metrics' },
    { path: '/unified-platform/intelligence/workflows', name: 'Workflows', icon: Workflow, description: 'Automation' },
  ];

  const platforms = [
    { id: 'all', name: 'All Platforms', icon: Globe, color: 'bg-purple-500' },
    { id: 'finance', name: 'Finance', icon: TrendingUp, color: 'bg-green-500' },
    { id: 'real_estate', name: 'Real Estate', icon: Building2, color: 'bg-blue-500' },
    { id: 'bond_ai', name: 'Bond.AI', icon: Users, color: 'bg-orange-500' },
    { id: 'labor', name: 'Labor', icon: Briefcase, color: 'bg-indigo-500' },
  ];

  const activeAgents: ActiveAgent[] = [
    { id: '1', name: 'Extreme Events Detector', platform: 'Finance', status: 'active', lastQuery: '2m ago' },
    { id: '2', name: 'Arbitrage Scanner', platform: 'Finance', status: 'processing', lastQuery: 'now' },
    { id: '3', name: 'Property Analyzer', platform: 'Real Estate', status: 'active', lastQuery: '5m ago' },
    { id: '4', name: 'Network Analyzer', platform: 'Bond.AI', status: 'idle', lastQuery: '10m ago' },
    { id: '5', name: 'Skill Matcher', platform: 'Labor', status: 'active', lastQuery: '3m ago' },
  ];

  const sampleQueries = [
    "Find investors in my network interested in multifamily real estate",
    "Analyze market regime impact on my property portfolio",
    "Match my skills to high-growth job opportunities",
    "Detect arbitrage opportunities with low correlation to my holdings",
    "Who in my network works at companies with open engineering roles?"
  ];

  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsProcessing(true);

    // Simulate cross-platform query
    setTimeout(() => {
      setResults([
        {
          platform: 'Finance',
          agent: 'Portfolio Optimizer',
          response: 'Found 3 investment opportunities matching your risk profile with 15% expected return.',
          confidence: 0.92,
          latency: 234
        },
        {
          platform: 'Real Estate',
          agent: 'Property Analyzer',
          response: 'Identified 5 properties in target markets with 7%+ cap rates.',
          confidence: 0.88,
          latency: 456
        },
        {
          platform: 'Bond.AI',
          agent: 'Network Intelligence',
          response: 'Found 12 connections with relevant expertise. 3 are active investors.',
          confidence: 0.85,
          latency: 312
        },
        {
          platform: 'Labor',
          agent: 'Opportunity Matcher',
          response: 'Your skills match 8 high-growth positions with 25% salary premium.',
          confidence: 0.90,
          latency: 289
        }
      ]);
      setIsProcessing(false);
    }, 2000);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'processing': return 'bg-yellow-500 animate-pulse';
      case 'idle': return 'bg-gray-400';
      default: return 'bg-gray-400';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
            <Brain className="w-6 h-6 text-purple-600 dark:text-purple-400" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Cross-Platform Intelligence
          </h1>
        </div>
        <p className="text-gray-600 dark:text-gray-400">
          Query 104+ AI agents across Finance, Real Estate, Bond.AI, and Labor platforms
        </p>
      </div>

      {/* Feature Navigation */}
      <div className="mb-6">
        <div className="flex flex-wrap gap-2">
          {featureNavigation.map((feature) => (
            <Link
              key={feature.path}
              to={feature.path}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-lg transition-all ${
                location.pathname === feature.path
                  ? 'bg-purple-600 text-white shadow-lg'
                  : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-purple-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700'
              }`}
            >
              <feature.icon className="w-4 h-4" />
              <div className="text-left">
                <p className="text-sm font-medium">{feature.name}</p>
                <p className={`text-xs ${location.pathname === feature.path ? 'text-purple-200' : 'text-gray-400'}`}>
                  {feature.description}
                </p>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <Network className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">104+</p>
              <p className="text-sm text-gray-500">Active Agents</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
              <Database className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">5</p>
              <p className="text-sm text-gray-500">Platforms</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <Zap className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">~300ms</p>
              <p className="text-sm text-gray-500">Avg Response</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 dark:bg-orange-900 rounded-lg">
              <Activity className="w-5 h-5 text-orange-600 dark:text-orange-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">1.2K</p>
              <p className="text-sm text-gray-500">Queries Today</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Query Panel */}
        <div className="lg:col-span-2 space-y-6">
          {/* Search Box */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Cross-Platform Query
            </h2>

            {/* Platform Selection */}
            <div className="flex flex-wrap gap-2 mb-4">
              {platforms.map((platform) => (
                <button
                  key={platform.id}
                  onClick={() => setSelectedPlatforms([platform.id])}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                    selectedPlatforms.includes(platform.id)
                      ? `${platform.color} text-white`
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  <platform.icon className="w-4 h-4" />
                  {platform.name}
                </button>
              ))}
            </div>

            {/* Query Input */}
            <div className="relative">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask anything across all platforms..."
                className="w-full h-32 p-4 pr-12 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
              />
              <button
                onClick={handleSearch}
                disabled={isProcessing || !query.trim()}
                className="absolute bottom-4 right-4 p-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 rounded-lg text-white transition-colors"
              >
                {isProcessing ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <Search className="w-5 h-5" />
                )}
              </button>
            </div>

            {/* Sample Queries */}
            <div className="mt-4">
              <p className="text-sm text-gray-500 mb-2">Try these queries:</p>
              <div className="flex flex-wrap gap-2">
                {sampleQueries.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => setQuery(q)}
                    className="text-xs px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-full hover:bg-purple-100 dark:hover:bg-purple-900 hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
                  >
                    {q.length > 50 ? q.substring(0, 50) + '...' : q}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Results */}
          {results.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Results from {results.length} Platforms
              </h2>
              <div className="space-y-4">
                {results.map((result, i) => (
                  <div
                    key={i}
                    className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-400 text-xs font-medium rounded">
                          {result.platform}
                        </span>
                        <span className="text-sm text-gray-500">{result.agent}</span>
                      </div>
                      <div className="flex items-center gap-3 text-xs text-gray-500">
                        <span className="flex items-center gap-1">
                          <CheckCircle className="w-3 h-3 text-green-500" />
                          {(result.confidence * 100).toFixed(0)}%
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {result.latency}ms
                        </span>
                      </div>
                    </div>
                    <p className="text-gray-700 dark:text-gray-300">{result.response}</p>
                    <button className="mt-2 text-sm text-purple-600 dark:text-purple-400 hover:underline flex items-center gap-1">
                      View Details <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Active Agents Sidebar */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Active Agents
            </h2>
            <div className="space-y-3">
              {activeAgents.map((agent) => (
                <div
                  key={agent.id}
                  className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${getStatusColor(agent.status)}`} />
                    <div>
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {agent.name}
                      </p>
                      <p className="text-xs text-gray-500">{agent.platform}</p>
                    </div>
                  </div>
                  <span className="text-xs text-gray-400">{agent.lastQuery}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Knowledge Graph Preview */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Knowledge Graph
            </h2>
            <div className="aspect-square bg-gray-50 dark:bg-gray-900 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <Network className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-2" />
                <p className="text-sm text-gray-500">Entity Graph Visualization</p>
                <Link
                  to="/unified-platform/intelligence/entities"
                  className="mt-2 text-sm text-purple-600 dark:text-purple-400 hover:underline flex items-center justify-center gap-1"
                >
                  Open Full View <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
              <div className="p-2 bg-gray-50 dark:bg-gray-900 rounded">
                <p className="font-medium text-gray-900 dark:text-white">2,456</p>
                <p className="text-xs text-gray-500">Entities</p>
              </div>
              <div className="p-2 bg-gray-50 dark:bg-gray-900 rounded">
                <p className="font-medium text-gray-900 dark:text-white">8,923</p>
                <p className="text-xs text-gray-500">Relationships</p>
              </div>
            </div>
          </div>

          {/* Query History */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Query History
              </h2>
              <History className="w-5 h-5 text-gray-400" />
            </div>
            <div className="space-y-3">
              {queryHistory.map((item, i) => (
                <button
                  key={i}
                  onClick={() => setQuery(item.query)}
                  className="w-full text-left p-3 bg-gray-50 dark:bg-gray-900 rounded-lg hover:bg-purple-50 dark:hover:bg-gray-700 transition-colors"
                >
                  <p className="text-sm text-gray-900 dark:text-white line-clamp-1">
                    {item.query}
                  </p>
                  <div className="flex items-center justify-between mt-1">
                    <span className="text-xs text-gray-400">{item.timestamp}</span>
                    <span className="text-xs text-purple-600 dark:text-purple-400">
                      {item.results} results
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
