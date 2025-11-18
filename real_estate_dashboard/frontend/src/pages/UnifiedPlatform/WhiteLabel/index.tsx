import React, { useState } from 'react';
import {
  Building,
  Palette,
  Globe,
  DollarSign,
  Users,
  Settings,
  Plus,
  Edit,
  Trash2,
  CheckCircle,
  AlertCircle,
  ExternalLink,
  Lock,
  Unlock,
  ToggleLeft,
  ToggleRight,
  Copy,
  Search
} from 'lucide-react';

interface Tenant {
  id: string;
  name: string;
  domain: string;
  plan: string;
  users: number;
  maxUsers: number;
  status: 'active' | 'trial' | 'suspended';
  revenue: number;
  branding: {
    primaryColor: string;
    logo: string;
  };
  created: string;
}

interface Domain {
  id: string;
  domain: string;
  tenant: string;
  status: 'active' | 'pending' | 'failed';
  ssl: 'active' | 'pending' | 'expired';
  primary: boolean;
}

export default function WhiteLabel() {
  const [activeTab, setActiveTab] = useState<'tenants' | 'domains' | 'branding' | 'billing'>('tenants');
  const [searchQuery, setSearchQuery] = useState('');

  const tenants: Tenant[] = [
    {
      id: 'tenant_1',
      name: 'Acme Real Estate',
      domain: 'acme-realestate.com',
      plan: 'Enterprise',
      users: 45,
      maxUsers: 100,
      status: 'active',
      revenue: 4999,
      branding: {
        primaryColor: '#3B82F6',
        logo: 'acme-logo.png'
      },
      created: '2024-01-15'
    },
    {
      id: 'tenant_2',
      name: 'Summit Financial',
      domain: 'summit-financial.io',
      plan: 'Growth',
      users: 23,
      maxUsers: 50,
      status: 'active',
      revenue: 1499,
      branding: {
        primaryColor: '#10B981',
        logo: 'summit-logo.png'
      },
      created: '2024-02-20'
    },
    {
      id: 'tenant_3',
      name: 'Harbor Consulting',
      domain: 'harbor-consulting.com',
      plan: 'Starter',
      users: 8,
      maxUsers: 20,
      status: 'trial',
      revenue: 0,
      branding: {
        primaryColor: '#8B5CF6',
        logo: 'harbor-logo.png'
      },
      created: '2024-03-01'
    }
  ];

  const domains: Domain[] = [
    { id: 'dom_1', domain: 'acme-realestate.com', tenant: 'Acme Real Estate', status: 'active', ssl: 'active', primary: true },
    { id: 'dom_2', domain: 'app.acme-realestate.com', tenant: 'Acme Real Estate', status: 'active', ssl: 'active', primary: false },
    { id: 'dom_3', domain: 'summit-financial.io', tenant: 'Summit Financial', status: 'active', ssl: 'active', primary: true },
    { id: 'dom_4', domain: 'harbor-consulting.com', tenant: 'Harbor Consulting', status: 'pending', ssl: 'pending', primary: true }
  ];

  const featureFlags = [
    { id: 'ai_chatbot', name: 'AI Chatbot', enabled: true, rollout: 100 },
    { id: 'predictive_analytics', name: 'Predictive Analytics', enabled: true, rollout: 50 },
    { id: 'advanced_reports', name: 'Advanced Reports', enabled: false, rollout: 0 },
    { id: 'white_label_branding', name: 'Custom Branding', enabled: true, rollout: 100 }
  ];

  const totalRevenue = tenants.reduce((sum, t) => sum + t.revenue, 0);
  const totalUsers = tenants.reduce((sum, t) => sum + t.users, 0);
  const activeTenants = tenants.filter(t => t.status === 'active').length;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-400';
      case 'trial': return 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-400';
      case 'pending': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-400';
      case 'suspended':
      case 'failed': return 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-400';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
            <Building className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            White-Label Platform
          </h1>
        </div>
        <p className="text-gray-600 dark:text-gray-400">
          Manage tenants, domains, branding, and partner billing
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
              <Building className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{activeTenants}</p>
              <p className="text-sm text-gray-500">Active Tenants</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
              <DollarSign className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                ${(totalRevenue / 1000).toFixed(1)}K
              </p>
              <p className="text-sm text-gray-500">Monthly Revenue</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <Users className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalUsers}</p>
              <p className="text-sm text-gray-500">Total Users</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <Globe className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{domains.length}</p>
              <p className="text-sm text-gray-500">Custom Domains</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
        <div className="border-b border-gray-200 dark:border-gray-700">
          <div className="flex">
            {[
              { id: 'tenants', label: 'Tenants', icon: Building },
              { id: 'domains', label: 'Domains', icon: Globe },
              { id: 'branding', label: 'Feature Flags', icon: Settings },
              { id: 'billing', label: 'Billing', icon: DollarSign }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tenants Tab */}
        {activeTab === 'tenants' && (
          <div>
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search tenants..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <button className="flex items-center gap-2 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors">
                <Plus className="w-4 h-4" />
                Add Tenant
              </button>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {tenants.map((tenant) => (
                <div key={tenant.id} className="p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div
                        className="w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold"
                        style={{ backgroundColor: tenant.branding.primaryColor }}
                      >
                        {tenant.name.charAt(0)}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="font-medium text-gray-900 dark:text-white">{tenant.name}</p>
                          <span className={`px-2 py-0.5 text-xs rounded ${getStatusColor(tenant.status)}`}>
                            {tenant.status}
                          </span>
                          <span className="px-2 py-0.5 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">
                            {tenant.plan}
                          </span>
                        </div>
                        <div className="flex items-center gap-3 mt-1 text-sm text-gray-500">
                          <span className="flex items-center gap-1">
                            <Globe className="w-3 h-3" />
                            {tenant.domain}
                          </span>
                          <span>•</span>
                          <span>{tenant.users} / {tenant.maxUsers} users</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <p className="font-medium text-gray-900 dark:text-white">
                          ${tenant.revenue.toLocaleString()}/mo
                        </p>
                        <p className="text-xs text-gray-500">Since {tenant.created}</p>
                      </div>
                      <div className="flex items-center gap-1">
                        <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                          <Edit className="w-4 h-4 text-gray-400" />
                        </button>
                        <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                          <ExternalLink className="w-4 h-4 text-gray-400" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Domains Tab */}
        {activeTab === 'domains' && (
          <div>
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <p className="text-sm text-gray-500">{domains.length} domains configured</p>
              <button className="flex items-center gap-2 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors">
                <Plus className="w-4 h-4" />
                Add Domain
              </button>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {domains.map((domain) => (
                <div key={domain.id} className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-gray-900 dark:text-white">{domain.domain}</p>
                        {domain.primary && (
                          <span className="px-2 py-0.5 text-xs bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-400 rounded">
                            Primary
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-500 mt-1">{domain.tenant}</p>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <span className={`flex items-center gap-1 px-2 py-1 text-xs rounded ${getStatusColor(domain.status)}`}>
                          {domain.status === 'active' ? (
                            <CheckCircle className="w-3 h-3" />
                          ) : (
                            <AlertCircle className="w-3 h-3" />
                          )}
                          DNS {domain.status}
                        </span>
                        <span className={`flex items-center gap-1 px-2 py-1 text-xs rounded ${getStatusColor(domain.ssl)}`}>
                          {domain.ssl === 'active' ? (
                            <Lock className="w-3 h-3" />
                          ) : (
                            <Unlock className="w-3 h-3" />
                          )}
                          SSL {domain.ssl}
                        </span>
                      </div>
                      <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                        <Settings className="w-4 h-4 text-gray-400" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Feature Flags Tab */}
        {activeTab === 'branding' && (
          <div>
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <p className="text-sm text-gray-500">Control feature availability across all tenants</p>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {featureFlags.map((flag) => (
                <div key={flag.id} className="p-4 flex items-center justify-between">
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">{flag.name}</p>
                    <p className="text-sm text-gray-500">
                      {flag.enabled ? `${flag.rollout}% rollout` : 'Disabled'}
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    {flag.enabled && (
                      <div className="flex items-center gap-2">
                        <input
                          type="range"
                          min="0"
                          max="100"
                          value={flag.rollout}
                          className="w-24 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                          readOnly
                        />
                        <span className="text-sm text-gray-600 dark:text-gray-400 w-8">
                          {flag.rollout}%
                        </span>
                      </div>
                    )}
                    <button className="p-2 rounded-lg">
                      {flag.enabled ? (
                        <ToggleRight className="w-6 h-6 text-green-500" />
                      ) : (
                        <ToggleLeft className="w-6 h-6 text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Billing Tab */}
        {activeTab === 'billing' && (
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">Revenue Share</h3>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400">75%</p>
                <p className="text-sm text-gray-500 mt-1">Partner keeps</p>
              </div>
              <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">Next Payout</h3>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">$4,872</p>
                <p className="text-sm text-gray-500 mt-1">Due in 7 days</p>
              </div>
              <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">Total Paid</h3>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">$28,450</p>
                <p className="text-sm text-gray-500 mt-1">All time</p>
              </div>
            </div>

            <div className="mt-6">
              <h3 className="font-medium text-gray-900 dark:text-white mb-4">Recent Invoices</h3>
              <div className="space-y-2">
                {[
                  { id: 'INV-001', date: '2024-03-01', amount: 6498, status: 'paid' },
                  { id: 'INV-002', date: '2024-02-01', amount: 5999, status: 'paid' },
                  { id: 'INV-003', date: '2024-01-01', amount: 4999, status: 'paid' }
                ].map((invoice) => (
                  <div key={invoice.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
                    <div className="flex items-center gap-3">
                      <span className="font-mono text-sm text-gray-600 dark:text-gray-400">
                        {invoice.id}
                      </span>
                      <span className="text-sm text-gray-500">{invoice.date}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="font-medium text-gray-900 dark:text-white">
                        ${invoice.amount.toLocaleString()}
                      </span>
                      <span className="px-2 py-0.5 text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400 rounded">
                        {invoice.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
