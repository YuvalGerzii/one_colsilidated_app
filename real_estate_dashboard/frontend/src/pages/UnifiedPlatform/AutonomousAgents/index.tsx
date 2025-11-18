import React, { useState } from 'react';
import {
  Bot,
  Play,
  Pause,
  StopCircle,
  Settings,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  Activity,
  Shield,
  Eye,
  RotateCcw,
  ChevronDown,
  ChevronUp,
  Zap,
  TrendingUp,
  Building2,
  Mail,
  Briefcase
} from 'lucide-react';

interface Agent {
  id: string;
  name: string;
  type: string;
  status: 'running' | 'paused' | 'stopped' | 'error';
  actionsToday: number;
  successRate: number;
  spendToday: number;
  spendLimit: number;
  lastAction: string;
  pendingApprovals: number;
  icon: React.ElementType;
}

interface ApprovalRequest {
  id: string;
  agent: string;
  action: string;
  risk: 'low' | 'medium' | 'high';
  amount?: number;
  timestamp: string;
}

export default function AutonomousAgents() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [showApprovals, setShowApprovals] = useState(true);

  const agents: Agent[] = [
    {
      id: 'trading_1',
      name: 'Arbitrage Trading Agent',
      type: 'trading',
      status: 'running',
      actionsToday: 47,
      successRate: 94.2,
      spendToday: 234.50,
      spendLimit: 500,
      lastAction: '2m ago',
      pendingApprovals: 2,
      icon: TrendingUp
    },
    {
      id: 'outreach_1',
      name: 'Networking Outreach Agent',
      type: 'outreach',
      status: 'running',
      actionsToday: 156,
      successRate: 87.5,
      spendToday: 0,
      spendLimit: 100,
      lastAction: '5m ago',
      pendingApprovals: 0,
      icon: Mail
    },
    {
      id: 'property_1',
      name: 'Property Scout Agent',
      type: 'property',
      status: 'paused',
      actionsToday: 23,
      successRate: 91.3,
      spendToday: 12.30,
      spendLimit: 200,
      lastAction: '1h ago',
      pendingApprovals: 1,
      icon: Building2
    },
    {
      id: 'job_1',
      name: 'Job Application Agent',
      type: 'job',
      status: 'stopped',
      actionsToday: 0,
      successRate: 88.9,
      spendToday: 0,
      spendLimit: 50,
      lastAction: '1d ago',
      pendingApprovals: 0,
      icon: Briefcase
    }
  ];

  const approvalRequests: ApprovalRequest[] = [
    {
      id: 'apr_1',
      agent: 'Arbitrage Trading Agent',
      action: 'Execute triangular arbitrage: BTC → ETH → USDT',
      risk: 'high',
      amount: 5000,
      timestamp: '2m ago'
    },
    {
      id: 'apr_2',
      agent: 'Arbitrage Trading Agent',
      action: 'Open statistical arbitrage position',
      risk: 'medium',
      amount: 2500,
      timestamp: '5m ago'
    },
    {
      id: 'apr_3',
      agent: 'Property Scout Agent',
      action: 'Send investment memo to 3 stakeholders',
      risk: 'low',
      timestamp: '15m ago'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-green-500';
      case 'paused': return 'bg-yellow-500';
      case 'stopped': return 'bg-gray-400';
      case 'error': return 'bg-red-500';
      default: return 'bg-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <Play className="w-4 h-4" />;
      case 'paused': return <Pause className="w-4 h-4" />;
      case 'stopped': return <StopCircle className="w-4 h-4" />;
      case 'error': return <AlertTriangle className="w-4 h-4" />;
      default: return null;
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-400';
      case 'medium': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-400';
      case 'high': return 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-400';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const totalSpend = agents.reduce((sum, a) => sum + a.spendToday, 0);
  const totalActions = agents.reduce((sum, a) => sum + a.actionsToday, 0);
  const pendingApprovals = agents.reduce((sum, a) => sum + a.pendingApprovals, 0);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
            <Bot className="w-6 h-6 text-blue-600 dark:text-blue-400" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Autonomous Agents
          </h1>
        </div>
        <p className="text-gray-600 dark:text-gray-400">
          Monitor and control AI agents executing real-world actions
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
              <Activity className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalActions}</p>
              <p className="text-sm text-gray-500">Actions Today</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <DollarSign className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">${totalSpend.toFixed(2)}</p>
              <p className="text-sm text-gray-500">Spend Today</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <Bot className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{agents.filter(a => a.status === 'running').length}</p>
              <p className="text-sm text-gray-500">Active Agents</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg ${pendingApprovals > 0 ? 'bg-orange-100 dark:bg-orange-900' : 'bg-gray-100 dark:bg-gray-700'}`}>
              <Shield className={`w-5 h-5 ${pendingApprovals > 0 ? 'text-orange-600 dark:text-orange-400' : 'text-gray-600 dark:text-gray-400'}`} />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{pendingApprovals}</p>
              <p className="text-sm text-gray-500">Pending Approvals</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agents List */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Agent Fleet
              </h2>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {agents.map((agent) => (
                <div
                  key={agent.id}
                  className={`p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer transition-colors ${
                    selectedAgent === agent.id ? 'bg-blue-50 dark:bg-blue-900/20' : ''
                  }`}
                  onClick={() => setSelectedAgent(selectedAgent === agent.id ? null : agent.id)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className={`p-2 rounded-lg ${
                        agent.status === 'running' ? 'bg-blue-100 dark:bg-blue-900' : 'bg-gray-100 dark:bg-gray-700'
                      }`}>
                        <agent.icon className={`w-5 h-5 ${
                          agent.status === 'running' ? 'text-blue-600 dark:text-blue-400' : 'text-gray-500'
                        }`} />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="font-medium text-gray-900 dark:text-white">{agent.name}</p>
                          {agent.pendingApprovals > 0 && (
                            <span className="px-2 py-0.5 bg-orange-100 dark:bg-orange-900 text-orange-600 dark:text-orange-400 text-xs rounded-full">
                              {agent.pendingApprovals} pending
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-3 mt-1 text-sm text-gray-500">
                          <span className="flex items-center gap-1">
                            <div className={`w-2 h-2 rounded-full ${getStatusColor(agent.status)}`} />
                            {agent.status}
                          </span>
                          <span>•</span>
                          <span>{agent.actionsToday} actions</span>
                          <span>•</span>
                          <span>{agent.successRate}% success</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="text-right mr-4">
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          ${agent.spendToday.toFixed(2)}
                        </p>
                        <p className="text-xs text-gray-500">of ${agent.spendLimit}</p>
                      </div>
                      <button className="p-2 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg">
                        {agent.status === 'running' ? (
                          <Pause className="w-4 h-4 text-gray-500" />
                        ) : (
                          <Play className="w-4 h-4 text-gray-500" />
                        )}
                      </button>
                      <button className="p-2 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg">
                        <Settings className="w-4 h-4 text-gray-500" />
                      </button>
                    </div>
                  </div>

                  {/* Expanded Details */}
                  {selectedAgent === agent.id && (
                    <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="text-gray-500 mb-1">Spend Limit</p>
                          <div className="flex items-center gap-2">
                            <div className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-blue-500 rounded-full"
                                style={{ width: `${(agent.spendToday / agent.spendLimit) * 100}%` }}
                              />
                            </div>
                            <span className="text-gray-600 dark:text-gray-400">
                              {((agent.spendToday / agent.spendLimit) * 100).toFixed(0)}%
                            </span>
                          </div>
                        </div>
                        <div>
                          <p className="text-gray-500 mb-1">Last Action</p>
                          <p className="text-gray-900 dark:text-white">{agent.lastAction}</p>
                        </div>
                        <div>
                          <p className="text-gray-500 mb-1">Actions</p>
                          <div className="flex gap-2">
                            <button className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded text-xs">
                              View Logs
                            </button>
                            <button className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded text-xs">
                              Configure
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Approval Queue */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <button
              className="w-full p-4 flex items-center justify-between"
              onClick={() => setShowApprovals(!showApprovals)}
            >
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Approval Queue
              </h2>
              {showApprovals ? (
                <ChevronUp className="w-5 h-5 text-gray-500" />
              ) : (
                <ChevronDown className="w-5 h-5 text-gray-500" />
              )}
            </button>

            {showApprovals && (
              <div className="border-t border-gray-200 dark:border-gray-700">
                {approvalRequests.length === 0 ? (
                  <div className="p-8 text-center">
                    <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-2" />
                    <p className="text-gray-500">No pending approvals</p>
                  </div>
                ) : (
                  <div className="divide-y divide-gray-200 dark:divide-gray-700">
                    {approvalRequests.map((request) => (
                      <div key={request.id} className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className={`px-2 py-0.5 text-xs font-medium rounded ${getRiskColor(request.risk)}`}>
                            {request.risk.toUpperCase()}
                          </span>
                          <span className="text-xs text-gray-500">{request.timestamp}</span>
                        </div>
                        <p className="text-sm text-gray-500 mb-1">{request.agent}</p>
                        <p className="text-sm text-gray-900 dark:text-white mb-2">{request.action}</p>
                        {request.amount && (
                          <p className="text-sm font-medium text-gray-900 dark:text-white mb-3">
                            Amount: ${request.amount.toLocaleString()}
                          </p>
                        )}
                        <div className="flex gap-2">
                          <button className="flex-1 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors">
                            Approve
                          </button>
                          <button className="flex-1 px-3 py-1.5 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-lg transition-colors">
                            Deny
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
            <h3 className="font-medium text-gray-900 dark:text-white mb-3">Quick Actions</h3>
            <div className="space-y-2">
              <button className="w-full flex items-center gap-2 px-3 py-2 bg-red-50 dark:bg-red-900/20 hover:bg-red-100 dark:hover:bg-red-900/40 text-red-600 dark:text-red-400 rounded-lg text-sm transition-colors">
                <StopCircle className="w-4 h-4" />
                Emergency Stop All
              </button>
              <button className="w-full flex items-center gap-2 px-3 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg text-sm transition-colors">
                <Pause className="w-4 h-4" />
                Pause All Agents
              </button>
              <button className="w-full flex items-center gap-2 px-3 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg text-sm transition-colors">
                <RotateCcw className="w-4 h-4" />
                Reset Daily Limits
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
