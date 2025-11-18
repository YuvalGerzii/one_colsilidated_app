import React, { useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Activity,
  Zap,
  Clock,
  Target,
  ArrowUpRight,
  ArrowDownRight,
  Layers,
  Building2,
  Users,
  Briefcase,
  DollarSign,
  PieChart,
  LineChart,
  Calendar
} from 'lucide-react';

interface PlatformMetric {
  platform: string;
  queries: number;
  successRate: number;
  avgLatency: number;
  activeAgents: number;
  trend: number;
}

interface CorrelationData {
  platforms: [string, string];
  correlation: number;
  insights: string[];
}

interface TimeSeriesData {
  timestamp: string;
  finance: number;
  realEstate: number;
  bondAI: number;
  labor: number;
}

export default function Analytics() {
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d' | '90d'>('7d');
  const [selectedMetric, setSelectedMetric] = useState<'queries' | 'latency' | 'success'>('queries');

  const platformMetrics: PlatformMetric[] = [
    {
      platform: 'Finance',
      queries: 45230,
      successRate: 94.2,
      avgLatency: 245,
      activeAgents: 39,
      trend: 12.5
    },
    {
      platform: 'Real Estate',
      queries: 28450,
      successRate: 91.8,
      avgLatency: 312,
      activeAgents: 6,
      trend: 8.3
    },
    {
      platform: 'Bond.AI',
      queries: 67890,
      successRate: 89.5,
      avgLatency: 189,
      activeAgents: 35,
      trend: 23.1
    },
    {
      platform: 'Labor',
      queries: 19340,
      successRate: 93.4,
      avgLatency: 267,
      activeAgents: 15,
      trend: -2.4
    },
    {
      platform: 'Legacy',
      queries: 8920,
      successRate: 87.2,
      avgLatency: 445,
      activeAgents: 10,
      trend: 5.7
    }
  ];

  const correlations: CorrelationData[] = [
    {
      platforms: ['Finance', 'Real Estate'],
      correlation: 0.82,
      insights: [
        'Strong correlation between market volatility and property values',
        'Interest rate changes affect both platforms simultaneously',
        'Investment flows show 3-day lag pattern'
      ]
    },
    {
      platforms: ['Bond.AI', 'Labor'],
      correlation: 0.71,
      insights: [
        'Professional network activity correlates with job market trends',
        'Skill demand signals precede networking activity by 2 weeks',
        'Shared entity resolution improves both platform accuracy'
      ]
    },
    {
      platforms: ['Finance', 'Labor'],
      correlation: 0.65,
      insights: [
        'Economic indicators affect hiring patterns',
        'Salary trends follow market performance',
        'Sector rotation visible in both platforms'
      ]
    }
  ];

  const crossPlatformInsights = [
    {
      id: 1,
      type: 'opportunity',
      title: 'Arbitrage + Real Estate Synergy',
      description: 'Detected 15 REIT arbitrage opportunities correlating with property valuation discrepancies',
      impact: 'High',
      confidence: 0.89
    },
    {
      id: 2,
      type: 'trend',
      title: 'Skill-Investment Correlation',
      description: 'PropTech skills demand increasing 35% - aligns with $2.5B in recent RE tech investments',
      impact: 'Medium',
      confidence: 0.92
    },
    {
      id: 3,
      type: 'alert',
      title: 'Market Regime Shift Detected',
      description: 'Cross-platform signals indicate transition to risk-off environment',
      impact: 'High',
      confidence: 0.78
    },
    {
      id: 4,
      type: 'opportunity',
      title: 'Network-Deal Flow Connection',
      description: '23 qualified investors identified matching current multifamily deal criteria',
      impact: 'Medium',
      confidence: 0.85
    }
  ];

  const totalQueries = platformMetrics.reduce((sum, p) => sum + p.queries, 0);
  const avgSuccess = platformMetrics.reduce((sum, p) => sum + p.successRate, 0) / platformMetrics.length;
  const avgLatency = platformMetrics.reduce((sum, p) => sum + p.avgLatency, 0) / platformMetrics.length;
  const totalAgents = platformMetrics.reduce((sum, p) => sum + p.activeAgents, 0);

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'High': return 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-400';
      case 'Medium': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-400';
      case 'Low': return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-400';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                <BarChart3 className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Platform Analytics
              </h1>
            </div>
            <p className="text-gray-600 dark:text-gray-400">
              Cross-platform metrics, correlations, and insights
            </p>
          </div>
          <div className="flex gap-2">
            {(['24h', '7d', '30d', '90d'] as const).map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-colors ${
                  timeRange === range
                    ? 'bg-green-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                {range}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Queries</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {(totalQueries / 1000).toFixed(1)}K
              </p>
            </div>
            <div className="flex items-center text-green-600">
              <ArrowUpRight className="w-4 h-4" />
              <span className="text-sm font-medium">12.5%</span>
            </div>
          </div>
          <div className="mt-2 h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div className="h-full bg-green-500 rounded-full" style={{ width: '75%' }} />
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Avg Success Rate</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {avgSuccess.toFixed(1)}%
              </p>
            </div>
            <div className="flex items-center text-green-600">
              <ArrowUpRight className="w-4 h-4" />
              <span className="text-sm font-medium">2.3%</span>
            </div>
          </div>
          <div className="mt-2 h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div className="h-full bg-blue-500 rounded-full" style={{ width: `${avgSuccess}%` }} />
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Avg Latency</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {avgLatency.toFixed(0)}ms
              </p>
            </div>
            <div className="flex items-center text-green-600">
              <ArrowDownRight className="w-4 h-4" />
              <span className="text-sm font-medium">-8.2%</span>
            </div>
          </div>
          <div className="mt-2 h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div className="h-full bg-purple-500 rounded-full" style={{ width: '45%' }} />
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Active Agents</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalAgents}</p>
            </div>
            <div className="flex items-center text-green-600">
              <Activity className="w-4 h-4 mr-1" />
              <span className="text-sm font-medium">Online</span>
            </div>
          </div>
          <div className="mt-2 h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div className="h-full bg-orange-500 rounded-full" style={{ width: '100%' }} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Platform Performance */}
        <div className="lg:col-span-2">
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Platform Performance
              </h2>
            </div>
            <div className="p-4">
              <div className="space-y-4">
                {platformMetrics.map((platform) => (
                  <div key={platform.platform} className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                          {platform.platform === 'Finance' && <TrendingUp className="w-4 h-4 text-green-600" />}
                          {platform.platform === 'Real Estate' && <Building2 className="w-4 h-4 text-blue-600" />}
                          {platform.platform === 'Bond.AI' && <Users className="w-4 h-4 text-orange-600" />}
                          {platform.platform === 'Labor' && <Briefcase className="w-4 h-4 text-indigo-600" />}
                          {platform.platform === 'Legacy' && <Layers className="w-4 h-4 text-gray-600" />}
                        </div>
                        <div>
                          <p className="font-medium text-gray-900 dark:text-white">{platform.platform}</p>
                          <p className="text-xs text-gray-500">{platform.activeAgents} agents</p>
                        </div>
                      </div>
                      <div className={`flex items-center ${platform.trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {platform.trend >= 0 ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                        <span className="text-sm font-medium">{Math.abs(platform.trend)}%</span>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <p className="text-xs text-gray-500 mb-1">Queries</p>
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {(platform.queries / 1000).toFixed(1)}K
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 mb-1">Success</p>
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {platform.successRate}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 mb-1">Latency</p>
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {platform.avgLatency}ms
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Cross-Platform Insights */}
        <div className="space-y-6">
          {/* Correlations */}
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Platform Correlations
              </h2>
            </div>
            <div className="p-4 space-y-4">
              {correlations.map((corr, i) => (
                <div key={i} className="p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {corr.platforms[0]} ↔ {corr.platforms[1]}
                    </span>
                    <span className={`text-sm font-bold ${
                      corr.correlation > 0.7 ? 'text-green-600' : 'text-yellow-600'
                    }`}>
                      {(corr.correlation * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        corr.correlation > 0.7 ? 'bg-green-500' : 'bg-yellow-500'
                      }`}
                      style={{ width: `${corr.correlation * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Insights */}
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Cross-Platform Insights
              </h2>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-gray-700 max-h-[400px] overflow-y-auto">
              {crossPlatformInsights.map((insight) => (
                <div key={insight.id} className="p-4">
                  <div className="flex items-start justify-between mb-2">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {insight.title}
                    </p>
                    <span className={`px-2 py-0.5 text-xs rounded ${getImpactColor(insight.impact)}`}>
                      {insight.impact}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mb-2">{insight.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-400">
                      Confidence: {(insight.confidence * 100).toFixed(0)}%
                    </span>
                    <button className="text-xs text-green-600 dark:text-green-400 hover:underline">
                      Take Action →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
