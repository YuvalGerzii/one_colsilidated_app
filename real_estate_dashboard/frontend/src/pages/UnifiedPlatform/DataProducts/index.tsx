import React, { useState } from 'react';
import {
  Database,
  Key,
  BarChart3,
  DollarSign,
  Clock,
  Users,
  Zap,
  Copy,
  Eye,
  EyeOff,
  Plus,
  Trash2,
  Settings,
  TrendingUp,
  Building2,
  Briefcase,
  AlertCircle,
  CheckCircle,
  ArrowUpRight
} from 'lucide-react';

interface APIKey {
  id: string;
  name: string;
  key: string;
  tier: string;
  products: string[];
  requestsToday: number;
  requestsLimit: number;
  created: string;
  lastUsed: string;
  status: 'active' | 'expired' | 'revoked';
}

interface DataProduct {
  id: string;
  name: string;
  category: string;
  description: string;
  pricing: string;
  requestsToday: number;
  revenue: number;
  icon: React.ElementType;
}

export default function DataProducts() {
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({});
  const [selectedProduct, setSelectedProduct] = useState<string | null>(null);

  const apiKeys: APIKey[] = [
    {
      id: 'key_1',
      name: 'Production API',
      key: 'pk_live_abc123xyz789def456ghi012jkl345mno678',
      tier: 'Enterprise',
      products: ['Finance', 'Real Estate', 'Labor'],
      requestsToday: 15234,
      requestsLimit: 200000,
      created: '2024-01-15',
      lastUsed: '2m ago',
      status: 'active'
    },
    {
      id: 'key_2',
      name: 'Development API',
      key: 'pk_test_test123test456test789test012test345',
      tier: 'Professional',
      products: ['Finance'],
      requestsToday: 456,
      requestsLimit: 50000,
      created: '2024-02-20',
      lastUsed: '1h ago',
      status: 'active'
    }
  ];

  const dataProducts: DataProduct[] = [
    {
      id: 'extreme_events',
      name: 'Extreme Events Alerts',
      category: 'Finance',
      description: 'Real-time alerts for black swan events, market crashes, and tail risks',
      pricing: '$100K+/year',
      requestsToday: 2345,
      revenue: 125000,
      icon: AlertCircle
    },
    {
      id: 'arbitrage_signals',
      name: 'Arbitrage Signals Feed',
      category: 'Finance',
      description: 'Cross-exchange, triangular, and statistical arbitrage opportunities',
      pricing: '$50K/year',
      requestsToday: 8901,
      revenue: 89000,
      icon: TrendingUp
    },
    {
      id: 'property_valuations',
      name: 'Property Valuation API',
      category: 'Real Estate',
      description: 'AI-powered property valuations with comparable analysis',
      pricing: '$299-$1,499/mo',
      requestsToday: 3456,
      revenue: 45000,
      icon: Building2
    },
    {
      id: 'skill_forecasts',
      name: 'Skill Demand Forecasts',
      category: 'Labor',
      description: 'Predict in-demand skills with salary premiums',
      pricing: '$99-$2,499/mo',
      requestsToday: 1234,
      revenue: 32000,
      icon: Briefcase
    }
  ];

  const tiers = [
    { name: 'Free', requests: '500/day', price: '$0', features: ['Basic endpoints', 'Email support'] },
    { name: 'Starter', requests: '10K/day', price: '$49/mo', features: ['All endpoints', 'Priority support'] },
    { name: 'Professional', requests: '50K/day', price: '$299/mo', features: ['Higher limits', 'Webhook support'] },
    { name: 'Enterprise', requests: '200K/day', price: 'Custom', features: ['Unlimited', 'Dedicated support', 'SLA'] }
  ];

  const totalRevenue = dataProducts.reduce((sum, p) => sum + p.revenue, 0);
  const totalRequests = apiKeys.reduce((sum, k) => sum + k.requestsToday, 0);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // Would show toast notification
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
            <Database className="w-6 h-6 text-green-600 dark:text-green-400" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Data Products
          </h1>
        </div>
        <p className="text-gray-600 dark:text-gray-400">
          Manage API keys, monitor usage, and access premium data feeds
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
              <DollarSign className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                ${(totalRevenue / 1000).toFixed(0)}K
              </p>
              <p className="text-sm text-gray-500">Monthly Revenue</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <Zap className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {(totalRequests / 1000).toFixed(1)}K
              </p>
              <p className="text-sm text-gray-500">Requests Today</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <Key className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{apiKeys.length}</p>
              <p className="text-sm text-gray-500">Active Keys</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 dark:bg-orange-900 rounded-lg">
              <Database className="w-5 h-5 text-orange-600 dark:text-orange-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{dataProducts.length}</p>
              <p className="text-sm text-gray-500">Products</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* API Keys */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                API Keys
              </h2>
              <button className="flex items-center gap-2 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors">
                <Plus className="w-4 h-4" />
                Create Key
              </button>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {apiKeys.map((apiKey) => (
                <div key={apiKey.id} className="p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-gray-900 dark:text-white">{apiKey.name}</p>
                        <span className={`px-2 py-0.5 text-xs rounded ${
                          apiKey.tier === 'Enterprise'
                            ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-400'
                            : 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-400'
                        }`}>
                          {apiKey.tier}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <code className="text-sm text-gray-500 font-mono">
                          {showKeys[apiKey.id]
                            ? apiKey.key
                            : apiKey.key.substring(0, 12) + '••••••••••••••••'}
                        </code>
                        <button
                          onClick={() => setShowKeys({ ...showKeys, [apiKey.id]: !showKeys[apiKey.id] })}
                          className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                        >
                          {showKeys[apiKey.id] ? (
                            <EyeOff className="w-4 h-4 text-gray-400" />
                          ) : (
                            <Eye className="w-4 h-4 text-gray-400" />
                          )}
                        </button>
                        <button
                          onClick={() => copyToClipboard(apiKey.key)}
                          className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                        >
                          <Copy className="w-4 h-4 text-gray-400" />
                        </button>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                        <Settings className="w-4 h-4 text-gray-400" />
                      </button>
                      <button className="p-2 hover:bg-red-100 dark:hover:bg-red-900/20 rounded">
                        <Trash2 className="w-4 h-4 text-red-400" />
                      </button>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-sm">
                    <div className="flex items-center gap-1 text-gray-500">
                      <Zap className="w-4 h-4" />
                      {apiKey.requestsToday.toLocaleString()} / {apiKey.requestsLimit.toLocaleString()}
                    </div>
                    <div className="flex items-center gap-1 text-gray-500">
                      <Clock className="w-4 h-4" />
                      Last used {apiKey.lastUsed}
                    </div>
                  </div>

                  <div className="mt-3 flex flex-wrap gap-1">
                    {apiKey.products.map((product) => (
                      <span
                        key={product}
                        className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded"
                      >
                        {product}
                      </span>
                    ))}
                  </div>

                  {/* Usage bar */}
                  <div className="mt-3">
                    <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                      <span>Usage</span>
                      <span>{((apiKey.requestsToday / apiKey.requestsLimit) * 100).toFixed(1)}%</span>
                    </div>
                    <div className="h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-green-500 rounded-full"
                        style={{ width: `${(apiKey.requestsToday / apiKey.requestsLimit) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Data Products Catalog */}
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Product Catalog
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
              {dataProducts.map((product) => (
                <div
                  key={product.id}
                  className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-green-500 transition-colors cursor-pointer"
                  onClick={() => setSelectedProduct(product.id)}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="p-2 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                      <product.icon className="w-5 h-5 text-green-600 dark:text-green-400" />
                    </div>
                    <span className="text-xs text-gray-500">{product.category}</span>
                  </div>
                  <h3 className="font-medium text-gray-900 dark:text-white mb-1">
                    {product.name}
                  </h3>
                  <p className="text-sm text-gray-500 mb-3">{product.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-green-600 dark:text-green-400">
                      {product.pricing}
                    </span>
                    <button className="flex items-center gap-1 text-sm text-blue-600 dark:text-blue-400 hover:underline">
                      View Docs <ArrowUpRight className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Pricing Tiers */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Pricing Tiers
              </h2>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {tiers.map((tier) => (
                <div key={tier.name} className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-medium text-gray-900 dark:text-white">{tier.name}</p>
                    <p className="text-sm font-semibold text-green-600 dark:text-green-400">
                      {tier.price}
                    </p>
                  </div>
                  <p className="text-sm text-gray-500 mb-2">{tier.requests} requests</p>
                  <ul className="space-y-1">
                    {tier.features.map((feature, i) => (
                      <li key={i} className="flex items-center gap-2 text-xs text-gray-500">
                        <CheckCircle className="w-3 h-3 text-green-500" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          {/* Usage Stats */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
            <h3 className="font-medium text-gray-900 dark:text-white mb-4">
              Usage This Month
            </h3>
            <div className="space-y-3">
              <div>
                <div className="flex items-center justify-between text-sm mb-1">
                  <span className="text-gray-500">API Requests</span>
                  <span className="font-medium text-gray-900 dark:text-white">456K / 500K</span>
                </div>
                <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full" style={{ width: '91%' }} />
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between text-sm mb-1">
                  <span className="text-gray-500">Data Transfer</span>
                  <span className="font-medium text-gray-900 dark:text-white">85 GB / 100 GB</span>
                </div>
                <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div className="h-full bg-purple-500 rounded-full" style={{ width: '85%' }} />
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between text-sm mb-1">
                  <span className="text-gray-500">Webhooks</span>
                  <span className="font-medium text-gray-900 dark:text-white">12K / 20K</span>
                </div>
                <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div className="h-full bg-green-500 rounded-full" style={{ width: '60%' }} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
