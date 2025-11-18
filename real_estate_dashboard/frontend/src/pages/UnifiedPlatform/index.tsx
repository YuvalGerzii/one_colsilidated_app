import React from 'react';
import { Link } from 'react-router-dom';
import {
  Brain,
  Bot,
  Database,
  Building,
  ArrowRight,
  Zap,
  Shield,
  Globe,
  TrendingUp,
  Users,
  DollarSign
} from 'lucide-react';

interface FeatureCard {
  title: string;
  description: string;
  icon: React.ElementType;
  color: string;
  link: string;
  stats: { label: string; value: string }[];
}

export default function UnifiedPlatform() {
  const features: FeatureCard[] = [
    {
      title: 'Cross-Platform Intelligence',
      description: 'Query 104+ AI agents across Finance, Real Estate, Bond.AI, and Labor platforms with unified entity resolution.',
      icon: Brain,
      color: 'purple',
      link: '/unified-platform/intelligence',
      stats: [
        { label: 'Agents', value: '104+' },
        { label: 'Platforms', value: '5' },
        { label: 'Avg Response', value: '~300ms' }
      ]
    },
    {
      title: 'Autonomous Agents',
      description: 'Monitor and control AI agents that execute real-world actions with safety controls and human-in-the-loop approvals.',
      icon: Bot,
      color: 'blue',
      link: '/unified-platform/agents',
      stats: [
        { label: 'Active Agents', value: '4' },
        { label: 'Actions Today', value: '226' },
        { label: 'Success Rate', value: '93%' }
      ]
    },
    {
      title: 'Data Products',
      description: 'Manage API keys, monitor usage, and access premium data feeds for Finance, Real Estate, and Labor markets.',
      icon: Database,
      color: 'green',
      link: '/unified-platform/data-products',
      stats: [
        { label: 'Products', value: '12' },
        { label: 'API Keys', value: '2' },
        { label: 'Revenue', value: '$291K' }
      ]
    },
    {
      title: 'White-Label Platform',
      description: 'Manage tenants, custom domains, branding, and partner billing for your white-label deployments.',
      icon: Building,
      color: 'indigo',
      link: '/unified-platform/white-label',
      stats: [
        { label: 'Tenants', value: '3' },
        { label: 'Users', value: '76' },
        { label: 'MRR', value: '$6.5K' }
      ]
    }
  ];

  const getColorClasses = (color: string) => {
    const colors: Record<string, { bg: string; icon: string; border: string }> = {
      purple: {
        bg: 'bg-purple-100 dark:bg-purple-900/30',
        icon: 'text-purple-600 dark:text-purple-400',
        border: 'hover:border-purple-500'
      },
      blue: {
        bg: 'bg-blue-100 dark:bg-blue-900/30',
        icon: 'text-blue-600 dark:text-blue-400',
        border: 'hover:border-blue-500'
      },
      green: {
        bg: 'bg-green-100 dark:bg-green-900/30',
        icon: 'text-green-600 dark:text-green-400',
        border: 'hover:border-green-500'
      },
      indigo: {
        bg: 'bg-indigo-100 dark:bg-indigo-900/30',
        icon: 'text-indigo-600 dark:text-indigo-400',
        border: 'hover:border-indigo-500'
      }
    };
    return colors[color];
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl">
            <Zap className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Unified Platform Core
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Enterprise-grade AI infrastructure for cross-platform intelligence
            </p>
          </div>
        </div>

        {/* Platform Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 text-gray-500 mb-1">
              <TrendingUp className="w-4 h-4" />
              <span className="text-sm">Revenue Potential</span>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">$290M+</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 text-gray-500 mb-1">
              <Bot className="w-4 h-4" />
              <span className="text-sm">Total Agents</span>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">104+</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 text-gray-500 mb-1">
              <Globe className="w-4 h-4" />
              <span className="text-sm">Platforms</span>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">5</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2 text-gray-500 mb-1">
              <Shield className="w-4 h-4" />
              <span className="text-sm">Uptime</span>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">99.9%</p>
          </div>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {features.map((feature) => {
          const colorClasses = getColorClasses(feature.color);
          return (
            <Link
              key={feature.title}
              to={feature.link}
              className={`block bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 ${colorClasses.border} transition-all hover:shadow-lg group`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`p-3 ${colorClasses.bg} rounded-xl`}>
                  <feature.icon className={`w-6 h-6 ${colorClasses.icon}`} />
                </div>
                <ArrowRight className="w-5 h-5 text-gray-300 dark:text-gray-600 group-hover:text-gray-500 dark:group-hover:text-gray-400 transition-colors" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4 text-sm">
                {feature.description}
              </p>
              <div className="grid grid-cols-3 gap-2">
                {feature.stats.map((stat) => (
                  <div key={stat.label} className="text-center p-2 bg-gray-50 dark:bg-gray-900 rounded-lg">
                    <p className="text-lg font-bold text-gray-900 dark:text-white">{stat.value}</p>
                    <p className="text-xs text-gray-500">{stat.label}</p>
                  </div>
                ))}
              </div>
            </Link>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div className="mt-8 bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="flex items-center gap-2 p-3 bg-purple-50 dark:bg-purple-900/20 hover:bg-purple-100 dark:hover:bg-purple-900/40 text-purple-700 dark:text-purple-400 rounded-lg text-sm font-medium transition-colors">
            <Brain className="w-4 h-4" />
            New Query
          </button>
          <button className="flex items-center gap-2 p-3 bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/40 text-blue-700 dark:text-blue-400 rounded-lg text-sm font-medium transition-colors">
            <Bot className="w-4 h-4" />
            Launch Agent
          </button>
          <button className="flex items-center gap-2 p-3 bg-green-50 dark:bg-green-900/20 hover:bg-green-100 dark:hover:bg-green-900/40 text-green-700 dark:text-green-400 rounded-lg text-sm font-medium transition-colors">
            <Database className="w-4 h-4" />
            Create API Key
          </button>
          <button className="flex items-center gap-2 p-3 bg-indigo-50 dark:bg-indigo-900/20 hover:bg-indigo-100 dark:hover:bg-indigo-900/40 text-indigo-700 dark:text-indigo-400 rounded-lg text-sm font-medium transition-colors">
            <Building className="w-4 h-4" />
            Add Tenant
          </button>
        </div>
      </div>
    </div>
  );
}
