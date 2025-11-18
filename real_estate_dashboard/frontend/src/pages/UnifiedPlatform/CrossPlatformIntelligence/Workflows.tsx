import React, { useState } from 'react';
import {
  GitBranch,
  Plus,
  Play,
  Pause,
  Settings,
  ChevronRight,
  Clock,
  CheckCircle,
  AlertCircle,
  Zap,
  ArrowRight,
  Layers,
  Copy,
  Trash2,
  Edit,
  Calendar,
  RefreshCw
} from 'lucide-react';

interface WorkflowStep {
  id: string;
  type: 'query' | 'action' | 'condition' | 'notification';
  name: string;
  platform?: string;
  config: Record<string, any>;
}

interface Workflow {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'paused' | 'draft';
  steps: WorkflowStep[];
  trigger: string;
  lastRun: string;
  runs: number;
  successRate: number;
}

export default function Workflows() {
  const [selectedWorkflow, setSelectedWorkflow] = useState<Workflow | null>(null);

  const workflows: Workflow[] = [
    {
      id: 'wf_1',
      name: 'Arbitrage Alert Pipeline',
      description: 'Detect arbitrage opportunities and notify when thresholds are met',
      status: 'active',
      trigger: 'Every 5 minutes',
      lastRun: '2m ago',
      runs: 1256,
      successRate: 98.5,
      steps: [
        { id: 's1', type: 'query', name: 'Scan Arbitrage Opportunities', platform: 'Finance', config: { minSpread: 0.5 } },
        { id: 's2', type: 'condition', name: 'Check Profit Threshold', config: { minProfit: 1000 } },
        { id: 's3', type: 'action', name: 'Execute Trade', platform: 'Finance', config: { autoApprove: false } },
        { id: 's4', type: 'notification', name: 'Send Alert', config: { channels: ['email', 'slack'] } }
      ]
    },
    {
      id: 'wf_2',
      name: 'Investor Match Workflow',
      description: 'Match new deals with investors from network based on criteria',
      status: 'active',
      trigger: 'On new deal',
      lastRun: '15m ago',
      runs: 89,
      successRate: 94.2,
      steps: [
        { id: 's1', type: 'query', name: 'Get Deal Details', platform: 'Real Estate', config: {} },
        { id: 's2', type: 'query', name: 'Find Matching Investors', platform: 'Bond.AI', config: { minMatch: 0.7 } },
        { id: 's3', type: 'action', name: 'Generate Intro Messages', platform: 'Bond.AI', config: {} },
        { id: 's4', type: 'notification', name: 'Notify Deal Owner', config: { channels: ['email'] } }
      ]
    },
    {
      id: 'wf_3',
      name: 'Market Regime Monitor',
      description: 'Monitor market conditions and adjust portfolio recommendations',
      status: 'paused',
      trigger: 'Daily at 9:00 AM',
      lastRun: '1d ago',
      runs: 45,
      successRate: 91.1,
      steps: [
        { id: 's1', type: 'query', name: 'Analyze Market Regime', platform: 'Finance', config: {} },
        { id: 's2', type: 'query', name: 'Get Portfolio Holdings', platform: 'Finance', config: {} },
        { id: 's3', type: 'condition', name: 'Check Risk Levels', config: { maxRisk: 0.3 } },
        { id: 's4', type: 'action', name: 'Generate Recommendations', config: {} }
      ]
    },
    {
      id: 'wf_4',
      name: 'Skill Gap Analysis',
      description: 'Track skill trends and update learning recommendations',
      status: 'draft',
      trigger: 'Weekly',
      lastRun: 'Never',
      runs: 0,
      successRate: 0,
      steps: [
        { id: 's1', type: 'query', name: 'Get Skill Forecasts', platform: 'Labor', config: {} },
        { id: 's2', type: 'query', name: 'Analyze User Skills', platform: 'Labor', config: {} },
        { id: 's3', type: 'action', name: 'Update Learning Paths', config: {} }
      ]
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-400';
      case 'paused': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-400';
      case 'draft': return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-400';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getStepTypeColor = (type: string) => {
    switch (type) {
      case 'query': return 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400';
      case 'action': return 'bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-400';
      case 'condition': return 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400';
      case 'notification': return 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400';
      default: return 'bg-gray-100 text-gray-600';
    }
  };

  const getStepIcon = (type: string) => {
    switch (type) {
      case 'query': return Layers;
      case 'action': return Zap;
      case 'condition': return GitBranch;
      case 'notification': return CheckCircle;
      default: return Layers;
    }
  };

  const activeWorkflows = workflows.filter(w => w.status === 'active').length;
  const totalRuns = workflows.reduce((sum, w) => sum + w.runs, 0);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
                <GitBranch className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Workflow Automation
              </h1>
            </div>
            <p className="text-gray-600 dark:text-gray-400">
              Create automated workflows across all platforms
            </p>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg">
            <Plus className="w-4 h-4" />
            Create Workflow
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <GitBranch className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{workflows.length}</p>
              <p className="text-sm text-gray-500">Total Workflows</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
              <Play className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{activeWorkflows}</p>
              <p className="text-sm text-gray-500">Active</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <RefreshCw className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalRuns}</p>
              <p className="text-sm text-gray-500">Total Runs</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 dark:bg-orange-900 rounded-lg">
              <CheckCircle className="w-5 h-5 text-orange-600 dark:text-orange-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">96.2%</p>
              <p className="text-sm text-gray-500">Avg Success</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Workflow List */}
        <div className="lg:col-span-2">
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Workflows
              </h2>
            </div>
            <div className="divide-y divide-gray-200 dark:divide-gray-700">
              {workflows.map((workflow) => (
                <div
                  key={workflow.id}
                  onClick={() => setSelectedWorkflow(workflow)}
                  className={`p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer transition-colors ${
                    selectedWorkflow?.id === workflow.id ? 'bg-purple-50 dark:bg-purple-900/20' : ''
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-gray-900 dark:text-white">{workflow.name}</p>
                        <span className={`px-2 py-0.5 text-xs rounded ${getStatusColor(workflow.status)}`}>
                          {workflow.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500 mt-1">{workflow.description}</p>
                    </div>
                    <div className="flex gap-1">
                      {workflow.status === 'active' ? (
                        <button className="p-1.5 hover:bg-yellow-100 dark:hover:bg-yellow-900/20 rounded">
                          <Pause className="w-4 h-4 text-yellow-600" />
                        </button>
                      ) : (
                        <button className="p-1.5 hover:bg-green-100 dark:hover:bg-green-900/20 rounded">
                          <Play className="w-4 h-4 text-green-600" />
                        </button>
                      )}
                      <button className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                        <Settings className="w-4 h-4 text-gray-400" />
                      </button>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {workflow.trigger}
                    </span>
                    <span>•</span>
                    <span>Last run: {workflow.lastRun}</span>
                    <span>•</span>
                    <span>{workflow.runs} runs</span>
                    {workflow.successRate > 0 && (
                      <>
                        <span>•</span>
                        <span>{workflow.successRate}% success</span>
                      </>
                    )}
                  </div>

                  <div className="flex items-center gap-2 mt-3">
                    {workflow.steps.map((step, i) => {
                      const Icon = getStepIcon(step.type);
                      return (
                        <React.Fragment key={step.id}>
                          <div className={`p-1.5 rounded ${getStepTypeColor(step.type)}`}>
                            <Icon className="w-3 h-3" />
                          </div>
                          {i < workflow.steps.length - 1 && (
                            <ArrowRight className="w-3 h-3 text-gray-300" />
                          )}
                        </React.Fragment>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Workflow Details */}
        <div>
          {selectedWorkflow ? (
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
              <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-gray-900 dark:text-white">Workflow Steps</h3>
                  <div className="flex gap-1">
                    <button className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                      <Edit className="w-4 h-4 text-gray-400" />
                    </button>
                    <button className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                      <Copy className="w-4 h-4 text-gray-400" />
                    </button>
                    <button className="p-1.5 hover:bg-red-100 dark:hover:bg-red-900/20 rounded">
                      <Trash2 className="w-4 h-4 text-red-400" />
                    </button>
                  </div>
                </div>
              </div>

              <div className="p-4 space-y-3">
                {selectedWorkflow.steps.map((step, i) => {
                  const Icon = getStepIcon(step.type);
                  return (
                    <div key={step.id} className="relative">
                      <div className="p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className={`p-2 rounded ${getStepTypeColor(step.type)}`}>
                            <Icon className="w-4 h-4" />
                          </div>
                          <div className="flex-1">
                            <p className="text-sm font-medium text-gray-900 dark:text-white">
                              {step.name}
                            </p>
                            <div className="flex items-center gap-2 text-xs text-gray-500">
                              <span className="capitalize">{step.type}</span>
                              {step.platform && (
                                <>
                                  <span>•</span>
                                  <span>{step.platform}</span>
                                </>
                              )}
                            </div>
                          </div>
                          <span className="text-xs text-gray-400">#{i + 1}</span>
                        </div>
                      </div>
                      {i < selectedWorkflow.steps.length - 1 && (
                        <div className="absolute left-6 top-full w-0.5 h-3 bg-gray-200 dark:bg-gray-700" />
                      )}
                    </div>
                  );
                })}
              </div>

              <div className="p-4 border-t border-gray-200 dark:border-gray-700">
                <button className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg">
                  <Play className="w-4 h-4" />
                  Run Now
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-8 text-center">
              <GitBranch className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
              <p className="text-gray-500">Select a workflow to view steps</p>
            </div>
          )}

          {/* Quick Templates */}
          <div className="mt-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
            <h3 className="font-medium text-gray-900 dark:text-white mb-3">Quick Templates</h3>
            <div className="space-y-2">
              {[
                'Deal-to-Investor Matching',
                'Portfolio Risk Monitor',
                'Skill Trend Alerts',
                'Property Valuation Pipeline'
              ].map((template) => (
                <button
                  key={template}
                  className="w-full flex items-center justify-between p-2 text-sm text-left text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg"
                >
                  {template}
                  <ChevronRight className="w-4 h-4" />
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
