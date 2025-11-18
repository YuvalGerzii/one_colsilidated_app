import { useState, useEffect } from 'react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { 
  Building2, Calculator, TrendingUp, Database, Shield, Zap, 
  Activity, BarChart3, Users, FileText, DollarSign, Globe,
  GitBranch, Server, Layers, Code, CheckCircle2, Clock,
  ArrowRight, ChevronRight, Sparkles, Target, Briefcase,
  PieChart, Home, Wrench, Scale, Landmark, Brain, Package,
  Play, ExternalLink, Circle, Check, AlertCircle
} from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { LineChart, Line, AreaChart, Area, ResponsiveContainer, Tooltip } from 'recharts';

interface PlatformOverviewProps {
  onNavigate: (view: 'home' | 'property' | 'models') => void;
}

// Animated counter component
function AnimatedCounter({ end, duration = 2000, suffix = '' }: { end: number; duration?: number; suffix?: string }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime: number;
    let animationFrame: number;

    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / duration, 1);
      
      setCount(Math.floor(progress * end));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [end, duration]);

  return <span>{count}{suffix}</span>;
}

// Mini sparkline data
const trendData = Array.from({ length: 12 }, (_, i) => ({
  value: Math.floor(Math.random() * 40) + 60 + i * 2
}));

export function PlatformOverview({ onNavigate }: PlatformOverviewProps) {
  const { theme, colors } = useTheme();
  const [activeModuleTab, setActiveModuleTab] = useState<'core' | 'financial' | 'capital' | 'data' | 'management'>('core');
  const [expandedJourney, setExpandedJourney] = useState<string | null>(null);

  const stats = [
    { label: 'API Endpoints', value: 412, icon: Server, color: 'blue', trend: '+12%' },
    { label: 'Database Models', value: 50, icon: Database, color: 'purple', trend: '+8%' },
    { label: 'Frontend Pages', value: 30, icon: Layers, color: 'cyan', trend: '+15%' },
    { label: 'Real Estate Models', value: 12, icon: Building2, color: 'emerald', trend: '+3%' },
    { label: 'Financial Models', value: 5, icon: Calculator, color: 'amber', trend: 'Stable' },
    { label: 'Platform Modules', value: 18, icon: Package, color: 'pink', trend: '+2%' },
    { label: 'Data Integrations', value: 6, icon: Globe, color: 'teal', trend: 'Active' },
    { label: 'Service Modules', value: 19, icon: Briefcase, color: 'orange', trend: '+5%' },
  ];

  const modules = {
    core: [
      {
        title: 'Property Management',
        description: 'Complete property lifecycle management with leases, units, and maintenance tracking',
        icon: Building2,
        color: 'blue',
        endpoints: 50,
        features: ['Full CRUD', 'Lease Management', 'Maintenance Tracking', 'Financial Reporting']
      },
      {
        title: 'Accounting System',
        description: 'Chart of accounts, transactions, and comprehensive financial statements',
        icon: DollarSign,
        color: 'green',
        endpoints: 45,
        features: ['GL Management', 'Transactions', 'Financial Statements', 'Reconciliation']
      },
      {
        title: 'CRM & Deals',
        description: '6-stage pipeline with broker management and comparable properties',
        icon: Users,
        color: 'purple',
        endpoints: 50,
        features: ['Deal Pipeline', 'Broker CRM', 'Comps Database', 'Activity Logging']
      },
    ],
    financial: [
      {
        title: 'Real Estate Models',
        description: '12+ property-level financial models from fix & flip to hotel developments',
        icon: Home,
        color: 'emerald',
        endpoints: 40,
        features: ['Fix & Flip', 'Multifamily', 'Hotel', 'Mixed-Use', 'Subdivision']
      },
      {
        title: 'Institutional Models',
        description: 'DCF, LBO, Merger analysis with institutional-grade methodologies',
        icon: Briefcase,
        color: 'indigo',
        endpoints: 40,
        features: ['DCF Valuation', 'LBO Analysis', 'M&A Models', 'Due Diligence']
      },
      {
        title: 'Portfolio Analytics',
        description: 'Multi-property aggregation with risk metrics and performance attribution',
        icon: PieChart,
        color: 'cyan',
        endpoints: 30,
        features: ['Portfolio View', 'Risk Metrics', 'Performance', 'Scenarios']
      },
    ],
    capital: [
      {
        title: 'Fund Management',
        description: 'LP tracking, capital calls, distributions, and waterfall calculations',
        icon: Landmark,
        color: 'amber',
        endpoints: 40,
        features: ['LP Management', 'Capital Calls', 'Distributions', 'Waterfalls']
      },
      {
        title: 'Debt Management',
        description: 'Loan tracking, amortization, DSCR monitoring, and refinancing analysis',
        icon: FileText,
        color: 'red',
        endpoints: 30,
        features: ['Loan Tracking', 'Amortization', 'DSCR', 'Refinancing']
      },
      {
        title: 'Legal Services',
        description: 'Contract management, compliance tracking, and audit workflows',
        icon: Scale,
        color: 'purple',
        endpoints: 25,
        features: ['Contracts', 'Compliance', 'Audit Trails', '1031/OZ']
      },
    ],
    data: [
      {
        title: 'Market Intelligence',
        description: '6 official data sources: BLS, HUD, FHFA, BOI, Data.gov, Census',
        icon: Brain,
        color: 'teal',
        endpoints: 30,
        features: ['BLS Data', 'HUD FMR', 'FHFA HPI', 'Market Trends']
      },
      {
        title: 'Tax Strategy',
        description: '10+ optimization tools for entity selection and depreciation planning',
        icon: Calculator,
        color: 'orange',
        endpoints: 50,
        features: ['Entity Selection', 'Depreciation', '1031', 'Cost Seg']
      },
      {
        title: 'PDF Extraction',
        description: 'Document parsing and automated data extraction from contracts',
        icon: FileText,
        color: 'blue',
        endpoints: 20,
        features: ['OCR', 'Contract Parse', 'Data Extract', 'Validation']
      },
    ],
    management: [
      {
        title: 'Project Tracking',
        description: 'Tasks, milestones, Gantt charts, and budget management',
        icon: Target,
        color: 'green',
        endpoints: 20,
        features: ['Task Management', 'Gantt Charts', 'Milestones', 'Budgets']
      },
      {
        title: 'Reports Engine',
        description: 'Investment memos, quarterly/annual reports, custom templates',
        icon: FileText,
        color: 'purple',
        endpoints: 20,
        features: ['Investment Memos', 'Quarterly Reports', 'Templates', 'Export']
      },
      {
        title: 'Custom Dashboards',
        description: 'Interactive widgets and KPI visualizations',
        icon: BarChart3,
        color: 'cyan',
        endpoints: 15,
        features: ['Custom KPIs', 'Widgets', 'Drill-down', 'Real-time']
      },
    ],
  };

  const integrations = [
    { name: 'BLS', status: 'active', type: 'Economic', metrics: 'Employment, CPI, Wages', lastSync: '2 min ago' },
    { name: 'HUD', status: 'active', type: 'Housing', metrics: 'Fair Market Rent, Units', lastSync: '5 min ago' },
    { name: 'FHFA', status: 'active', type: 'Real Estate', metrics: 'House Price Index', lastSync: '1 min ago' },
    { name: 'Bank of Israel', status: 'active', type: 'International', metrics: 'Housing, CPI', lastSync: '8 min ago' },
    { name: 'Data.gov', status: 'active', type: 'Federal/State', metrics: '300K+ Datasets', lastSync: '3 min ago' },
    { name: 'Census', status: 'warning', type: 'Demographics', metrics: 'Population, Income', lastSync: 'Config needed' },
  ];

  const journeys = [
    {
      id: 'property',
      title: 'Manage Properties',
      description: 'Add properties, track leases, monitor maintenance, and view performance',
      icon: Building2,
      color: 'blue',
      time: '5 min',
      steps: ['Add Property', 'Configure Units', 'Set Up Leases', 'Track Financials'],
      action: () => onNavigate('property')
    },
    {
      id: 'deal',
      title: 'Analyze Real Estate Deal',
      description: 'Run financial models, calculate returns, and generate reports',
      icon: Calculator,
      color: 'emerald',
      time: '10 min',
      steps: ['Select Model', 'Input Assumptions', 'Review Metrics', 'Export Report'],
      action: () => onNavigate('models')
    },
    {
      id: 'fund',
      title: 'Manage a Fund',
      description: 'Track LPs, record capital calls, calculate distributions',
      icon: Landmark,
      color: 'amber',
      time: '15 min',
      steps: ['Create Fund', 'Add LPs', 'Capital Calls', 'Distributions'],
      action: () => {}
    },
    {
      id: 'portfolio',
      title: 'Portfolio Analytics',
      description: 'View aggregate metrics, analyze risk, run scenarios',
      icon: PieChart,
      color: 'purple',
      time: '8 min',
      steps: ['View Dashboard', 'Geographic Analysis', 'Risk Metrics', 'Scenarios'],
      action: () => {}
    },
  ];

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-[#0A0E27]' : 'bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/30'}`}>
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0">
          <div className={`absolute top-0 right-0 w-[600px] h-[600px] ${theme === 'dark' ? 'bg-blue-600/10' : 'bg-blue-200/20'} rounded-full blur-3xl`} />
          <div className={`absolute bottom-0 left-0 w-[500px] h-[500px] ${theme === 'dark' ? 'bg-purple-600/10' : 'bg-purple-200/20'} rounded-full blur-3xl`} />
          <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] ${theme === 'dark' ? 'bg-cyan-600/5' : 'bg-cyan-200/20'} rounded-full blur-3xl`} />
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-8 py-16">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="flex items-center justify-center gap-3 mb-4">
              <div className={`px-4 py-1.5 ${theme === 'dark' ? 'bg-blue-500/10 border-blue-500/20 text-blue-400' : 'bg-blue-100 border-blue-300 text-blue-700'} border rounded-full text-sm`}>
                Version 2.4.1
              </div>
              <div className={`px-4 py-1.5 ${theme === 'dark' ? 'bg-green-500/10 border-green-500/20' : 'bg-green-100 border-green-300'} border rounded-full text-sm flex items-center gap-2`}>
                <div className={`w-2 h-2 ${theme === 'dark' ? 'bg-green-400' : 'bg-green-600'} rounded-full animate-pulse`} />
                <span className={theme === 'dark' ? 'text-green-400' : 'text-green-700'}>Development Complete</span>
              </div>
            </div>
            <h1 className={`text-5xl mb-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'} flex items-center justify-center gap-3`}>
              <Sparkles className={`w-10 h-10 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
              Platform Overview
            </h1>
            <p className={`text-xl ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
              Comprehensive real estate financial platform with institutional-grade analytics
            </p>
          </div>

          {/* Hero Stats */}
          <div className="grid grid-cols-4 gap-6 mb-16">
            {[
              { label: 'API Endpoints', value: 412, icon: Server },
              { label: 'Database Models', value: 50, icon: Database },
              { label: 'Platform Modules', value: 18, icon: Package },
              { label: 'Data Sources', value: 6, icon: Globe },
            ].map((stat, index) => (
              <Card key={index} className={`p-8 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50 backdrop-blur-xl' : 'bg-white/60 border-slate-200 backdrop-blur-sm shadow-lg'} text-center relative overflow-hidden group`}>
                <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-br from-blue-600/10 to-transparent' : 'bg-gradient-to-br from-blue-100/50 to-transparent'} opacity-0 group-hover:opacity-100 transition-opacity`} />
                <div className="relative">
                  <stat.icon className={`w-8 h-8 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'} mx-auto mb-4`} />
                  <div className={`text-5xl mb-2 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>
                    <AnimatedCounter end={stat.value} suffix="+" />
                  </div>
                  <div className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{stat.label}</div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-8 pb-16">
        {/* Platform Stats Grid */}
        <div className="mb-16">
          <div className="flex items-center gap-3 mb-6">
            <Activity className={`w-6 h-6 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
            <h2 className={`text-2xl ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Platform Statistics</h2>
          </div>
          <div className="grid grid-cols-4 gap-4">
            {stats.map((stat, index) => (
              <Card key={index} className={`p-6 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50 backdrop-blur-sm' : 'bg-white/60 border-slate-200 shadow-md'} group hover:border-${stat.color}-500/50 transition-all`}>
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-10 h-10 ${theme === 'dark' ? `bg-${stat.color}-500/10 border-${stat.color}-500/20` : `bg-${stat.color}-100 border-${stat.color}-300`} rounded-lg flex items-center justify-center border group-hover:scale-110 transition-transform`}>
                    <stat.icon className={`w-5 h-5 ${theme === 'dark' ? `text-${stat.color}-400` : `text-${stat.color}-600`}`} />
                  </div>
                  <div className={`text-xs px-2 py-1 ${theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'} rounded border`}>
                    {stat.trend}
                  </div>
                </div>
                <div className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'} mb-2`}>{stat.label}</div>
                <div className={`text-3xl mb-3 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>
                  <AnimatedCounter end={stat.value} suffix="+" duration={1500} />
                </div>
                <ResponsiveContainer width="100%" height={30}>
                  <AreaChart data={trendData}>
                    <defs>
                      <linearGradient id={`gradient-${index}`} x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor={`var(--${stat.color}-500)`} stopOpacity={0.3}/>
                        <stop offset="95%" stopColor={`var(--${stat.color}-500)`} stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <Area type="monotone" dataKey="value" stroke={`var(--${stat.color}-500)`} strokeWidth={2} fill={`url(#gradient-${index})`} />
                  </AreaChart>
                </ResponsiveContainer>
              </Card>
            ))}
          </div>
        </div>

        {/* Module Explorer */}
        <div className="mb-16">
          <div className="flex items-center gap-3 mb-6">
            <Layers className={`w-6 h-6 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
            <h2 className={`text-2xl ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Platform Modules</h2>
          </div>

          {/* Tabs */}
          <div className={`flex gap-2 mb-6 p-2 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50' : 'bg-white/60 border-slate-200'} rounded-xl border`}>
            {[
              { id: 'core', label: 'Core Operations', count: 3 },
              { id: 'financial', label: 'Financial Analysis', count: 3 },
              { id: 'capital', label: 'Capital & Legal', count: 3 },
              { id: 'data', label: 'Data & Intelligence', count: 3 },
              { id: 'management', label: 'Management', count: 3 },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveModuleTab(tab.id as any)}
                className={`flex-1 px-4 py-3 rounded-lg transition-all text-sm ${
                  activeModuleTab === tab.id
                    ? theme === 'dark'
                      ? 'bg-blue-500/20 text-blue-400 border-blue-500/30 border'
                      : 'bg-blue-100 text-blue-700 border-blue-300 border shadow-sm'
                    : theme === 'dark'
                    ? 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                {tab.label}
                <span className={`ml-2 px-2 py-0.5 rounded text-xs ${activeModuleTab === tab.id ? (theme === 'dark' ? 'bg-blue-500/20' : 'bg-blue-200') : (theme === 'dark' ? 'bg-slate-700/50' : 'bg-slate-200')}`}>
                  {tab.count}
                </span>
              </button>
            ))}
          </div>

          {/* Module Cards */}
          <div className="grid grid-cols-3 gap-6">
            {modules[activeModuleTab].map((module, index) => (
              <Card key={index} className={`p-6 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50 backdrop-blur-sm hover:border-slate-600/50' : 'bg-white/60 border-slate-200 hover:border-slate-300 shadow-md hover:shadow-lg'} transition-all group cursor-pointer`}>
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-12 h-12 ${theme === 'dark' ? `bg-${module.color}-500/10 border-${module.color}-500/20` : `bg-${module.color}-100 border-${module.color}-300`} rounded-xl flex items-center justify-center border group-hover:scale-110 transition-transform`}>
                    <module.icon className={`w-6 h-6 ${theme === 'dark' ? `text-${module.color}-400` : `text-${module.color}-600`}`} />
                  </div>
                  <div className={`text-xs px-2.5 py-1 ${theme === 'dark' ? 'bg-slate-700/50 text-slate-400 border-slate-600/50' : 'bg-slate-100 text-slate-600 border-slate-300'} rounded border`}>
                    {module.endpoints} endpoints
                  </div>
                </div>
                <h3 className={`text-lg mb-2 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{module.title}</h3>
                <p className={`text-sm mb-4 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'} leading-relaxed`}>
                  {module.description}
                </p>
                <div className="space-y-2 mb-4">
                  {module.features.slice(0, 3).map((feature, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                      <CheckCircle2 className={`w-4 h-4 ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`} />
                      <span className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>{feature}</span>
                    </div>
                  ))}
                </div>
                <Button size="sm" variant="outline" className={`w-full ${theme === 'dark' ? 'border-slate-700 hover:bg-slate-800 text-white' : 'border-slate-300 hover:bg-slate-50 text-slate-700'} group`}>
                  Explore Module
                  <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Card>
            ))}
          </div>
        </div>

        {/* Integration Status */}
        <div className="mb-16">
          <div className="flex items-center gap-3 mb-6">
            <Globe className={`w-6 h-6 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
            <h2 className={`text-2xl ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Data Integrations</h2>
          </div>
          <div className="grid grid-cols-3 gap-4">
            {integrations.map((integration, index) => (
              <Card key={index} className={`p-5 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50 backdrop-blur-sm' : 'bg-white/60 border-slate-200 shadow-md'}`}>
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className={`text-lg mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{integration.name}</div>
                    <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>{integration.type}</div>
                  </div>
                  <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full border ${
                    integration.status === 'active' 
                      ? theme === 'dark' ? 'bg-green-500/10 border-green-500/20' : 'bg-green-100 border-green-300'
                      : theme === 'dark' ? 'bg-amber-500/10 border-amber-500/20' : 'bg-amber-100 border-amber-300'
                  }`}>
                    <Circle className={`w-2 h-2 ${integration.status === 'active' ? (theme === 'dark' ? 'text-green-400 fill-green-400' : 'text-green-600 fill-green-600') : (theme === 'dark' ? 'text-amber-400 fill-amber-400' : 'text-amber-600 fill-amber-600')}`} />
                    <span className={`text-xs ${integration.status === 'active' ? (theme === 'dark' ? 'text-green-400' : 'text-green-700') : (theme === 'dark' ? 'text-amber-400' : 'text-amber-700')}`}>
                      {integration.status === 'active' ? 'Active' : 'Config'}
                    </span>
                  </div>
                </div>
                <div className={`text-sm mb-3 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
                  {integration.metrics}
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5">
                    <Clock className={`w-3.5 h-3.5 ${theme === 'dark' ? 'text-slate-500' : 'text-slate-400'}`} />
                    <span className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>{integration.lastSync}</span>
                  </div>
                  {integration.status === 'active' && (
                    <Button size="sm" variant="ghost" className={`h-7 text-xs ${theme === 'dark' ? 'text-blue-400 hover:text-blue-300 hover:bg-blue-500/10' : 'text-blue-600 hover:text-blue-700 hover:bg-blue-50'}`}>
                      Test
                    </Button>
                  )}
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Quick Start Journeys */}
        <div className="mb-16">
          <div className="flex items-center gap-3 mb-6">
            <Target className={`w-6 h-6 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
            <h2 className={`text-2xl ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Quick Start Journeys</h2>
          </div>
          <div className="grid grid-cols-2 gap-6">
            {journeys.map((journey) => (
              <Card key={journey.id} className={`p-6 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50 backdrop-blur-sm hover:border-slate-600/50' : 'bg-white/60 border-slate-200 hover:border-slate-300 shadow-md hover:shadow-lg'} transition-all`}>
                <div className="flex items-start gap-4 mb-4">
                  <div className={`w-14 h-14 ${theme === 'dark' ? `bg-${journey.color}-500/10 border-${journey.color}-500/20` : `bg-${journey.color}-100 border-${journey.color}-300`} rounded-xl flex items-center justify-center border flex-shrink-0`}>
                    <journey.icon className={`w-7 h-7 ${theme === 'dark' ? `text-${journey.color}-400` : `text-${journey.color}-600`}`} />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{journey.title}</h3>
                      <div className={`text-xs px-2 py-0.5 ${theme === 'dark' ? 'bg-slate-700/50 text-slate-400 border-slate-600/50' : 'bg-slate-100 text-slate-600 border-slate-300'} rounded border flex items-center gap-1`}>
                        <Clock className="w-3 h-3" />
                        {journey.time}
                      </div>
                    </div>
                    <p className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'} mb-4`}>
                      {journey.description}
                    </p>
                  </div>
                </div>

                {/* Steps */}
                {expandedJourney === journey.id ? (
                  <div className="mb-4 space-y-2">
                    {journey.steps.map((step, idx) => (
                      <div key={idx} className={`flex items-center gap-3 p-3 ${theme === 'dark' ? 'bg-slate-800/30 border-slate-700/30' : 'bg-slate-50 border-slate-200'} rounded-lg border`}>
                        <div className={`w-6 h-6 ${theme === 'dark' ? 'bg-blue-500/20 text-blue-400 border-blue-500/30' : 'bg-blue-100 text-blue-700 border-blue-300'} rounded-full flex items-center justify-center text-xs border`}>
                          {idx + 1}
                        </div>
                        <span className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>{step}</span>
                      </div>
                    ))}
                  </div>
                ) : null}

                <div className="flex gap-2">
                  <Button
                    onClick={journey.action}
                    className={`flex-1 ${theme === 'dark' ? 'bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600' : 'bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600'} text-white`}
                  >
                    <Play className="w-4 h-4 mr-2" />
                    Start Journey
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => setExpandedJourney(expandedJourney === journey.id ? null : journey.id)}
                    className={theme === 'dark' ? 'border-slate-700 hover:bg-slate-800 text-white' : 'border-slate-300 hover:bg-slate-50 text-slate-700'}
                  >
                    {expandedJourney === journey.id ? 'Hide' : 'Steps'}
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Architecture Overview */}
        <div>
          <div className="flex items-center gap-3 mb-6">
            <GitBranch className={`w-6 h-6 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
            <h2 className={`text-2xl ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Technology Stack</h2>
          </div>
          <div className="grid grid-cols-4 gap-4">
            {[
              { title: 'Frontend', items: ['React 18', 'TypeScript', 'Material-UI v5', 'Vite'], color: 'cyan' },
              { title: 'Backend', items: ['FastAPI', 'SQLAlchemy', 'Pydantic', 'JWT Auth'], color: 'green' },
              { title: 'Database', items: ['PostgreSQL', '50+ Tables', 'Redis Cache', 'Migrations'], color: 'blue' },
              { title: 'DevOps', items: ['OpenAPI', 'Swagger', 'Error Handling', 'Logging'], color: 'purple' },
            ].map((stack, index) => (
              <Card key={index} className={`p-5 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50 backdrop-blur-sm' : 'bg-white/60 border-slate-200 shadow-md'}`}>
                <div className={`text-lg mb-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'} flex items-center gap-2`}>
                  <Code className={`w-5 h-5 ${theme === 'dark' ? `text-${stack.color}-400` : `text-${stack.color}-600`}`} />
                  {stack.title}
                </div>
                <div className="space-y-2">
                  {stack.items.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                      <Check className={`w-4 h-4 ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`} />
                      <span className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{item}</span>
                    </div>
                  ))}
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
