import { useState } from 'react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { StatsCard } from '../components/ui/StatsCard';
import { GradientCard } from '../components/ui/GradientCard';
import {
  AlertCircle, Clock, TrendingUp, Building2, DollarSign,
  ArrowRight, Plus, Calendar, Users, FileText, Calculator,
  Briefcase, Home, Bell, ChevronRight, Target, Activity,
  TrendingDown, CheckCircle2, AlertTriangle, Landmark,
  BarChart3, Globe, Wrench, CreditCard, PieChart, Zap,
  MapPin, Shield, Rocket, Banknote, TrendingUpDown, Award,
  AlertOctagon, Map, CircleDollarSign, Layers, Eye
} from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { useCompany } from '../context/CompanyContext';
import { BarChart as RechartsBar, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Cell, LineChart, Line, AreaChart, Area, Tooltip, Legend, ComposedChart } from 'recharts';

interface CommandCenterProps {
  onNavigate: (workspace: string, module?: string) => void;
}

export function CommandCenter({ onNavigate }: CommandCenterProps) {
  const { theme, colors } = useTheme();
  const { selectedCompany } = useCompany();
  const [activeTab, setActiveTab] = useState<'overview' | 'performance' | 'risk' | 'growth' | 'cash'>('overview');
  const [timeFrame, setTimeFrame] = useState<'week' | 'month' | 'quarter'>('month');

  // Default brand color
  const brandColor = {
    primary: 'blue',
    gradient: 'from-blue-600 to-blue-700'
  };

  // Sparkline data for KPIs
  const portfolioValueSparkline = [
    { value: 18.5 }, { value: 18.8 }, { value: 19.2 }, { value: 19.5 }, { value: 19.8 }, { value: 20.1 }
  ];
  const occupancySparkline = [
    { value: 96 }, { value: 96.5 }, { value: 97 }, { value: 97.5 }, { value: 98 }, { value: 98.2 }
  ];
  const irrSparkline = [
    { value: 11.2 }, { value: 11.5 }, { value: 11.8 }, { value: 12.0 }, { value: 12.2 }, { value: 12.4 }
  ];
  const dealsSparkline = [
    { value: 5 }, { value: 6 }, { value: 6 }, { value: 7 }, { value: 7 }, { value: 8 }
  ];
  const dscrSparkline = [
    { value: 1.38 }, { value: 1.39 }, { value: 1.40 }, { value: 1.41 }, { value: 1.41 }, { value: 1.42 }
  ];

  const kpis = [
    {
      label: 'Portfolio Value',
      value: 20.1,
      prefix: '$',
      suffix: 'M',
      decimals: 1,
      change: '+5.2%',
      trend: 'up' as const,
      icon: Building2,
      gradient: 'blue' as const,
      sparkline: portfolioValueSparkline
    },
    {
      label: 'Occupancy Rate',
      value: 98.2,
      suffix: '%',
      decimals: 1,
      subtitle: '145/148 units',
      icon: Home,
      gradient: 'green' as const,
      sparkline: occupancySparkline
    },
    {
      label: 'Portfolio IRR',
      value: 12.4,
      suffix: '%',
      decimals: 1,
      change: '+0.8%',
      trend: 'up' as const,
      icon: TrendingUp,
      gradient: 'purple' as const,
      sparkline: irrSparkline
    },
    {
      label: 'Active Deals',
      value: 8,
      subtitle: '$42M pipeline',
      icon: Target,
      gradient: 'orange' as const,
      sparkline: dealsSparkline
    },
    {
      label: 'Avg DSCR',
      value: 1.42,
      suffix: 'x',
      decimals: 2,
      subtitle: 'All properties',
      icon: BarChart3,
      gradient: 'cyan' as const,
      sparkline: dscrSparkline
    },
  ];

  const alerts = [
    {
      title: 'Leases Expiring Soon',
      description: '3 leases expiring in next 60 days',
      count: 3,
      color: 'amber',
      icon: Calendar,
      action: () => onNavigate('operate', 'leases')
    },
    {
      title: 'DSCR Alert',
      description: 'Oak Plaza below 1.25x threshold',
      count: 1,
      color: 'red',
      icon: AlertTriangle,
      action: () => onNavigate('capital', 'debt')
    },
    {
      title: 'Maintenance Requests',
      description: '5 open requests, 2 urgent',
      count: 5,
      color: 'orange',
      icon: Wrench,
      action: () => onNavigate('operate', 'maintenance')
    },
    {
      title: 'Capital Call Due',
      description: 'Summit Fund III - Due in 10 days',
      count: 1,
      color: 'blue',
      icon: Landmark,
      action: () => onNavigate('capital', 'funds')
    },
  ];

  const recentWork = [
    {
      title: 'Maple Street Apartments',
      type: 'Multifamily Underwriting',
      status: 'In Progress',
      updated: '2 hours ago',
      icon: Calculator,
      progress: 65,
      action: () => onNavigate('invest', 'realestate-models')
    },
    {
      title: 'Downtown Office Tower',
      type: 'DCF Valuation',
      status: 'Complete',
      updated: '5 hours ago',
      icon: Briefcase,
      progress: 100,
      action: () => onNavigate('invest', 'institutional-models')
    },
    {
      title: 'Q4 2024 Portfolio Report',
      type: 'Quarterly Report',
      status: 'Draft',
      updated: '1 day ago',
      icon: FileText,
      progress: 80,
      action: () => onNavigate('analytics', 'reports')
    },
    {
      title: 'Coastal Fund II Waterfall',
      type: 'Fund Distribution',
      status: 'In Progress',
      updated: '2 days ago',
      icon: Landmark,
      progress: 45,
      action: () => onNavigate('capital', 'funds')
    },
  ];

  const quickActions = [
    {
      title: 'Add Property',
      description: 'New property to portfolio',
      icon: Building2,
      color: 'emerald',
      action: () => onNavigate('operate', 'properties')
    },
    {
      title: 'Underwrite Deal',
      description: 'Run financial model',
      icon: Calculator,
      color: brandColor.primary,
      action: () => onNavigate('invest', 'realestate-models')
    },
    {
      title: 'Create Fund',
      description: 'New fund structure',
      icon: Landmark,
      color: 'purple',
      action: () => onNavigate('capital', 'funds')
    },
    {
      title: 'Upload Documents',
      description: 'Extract data from PDF',
      icon: FileText,
      color: 'blue',
      action: () => onNavigate('invest', 'pdf-extraction')
    },
  ];

  const marketInsights = [
    {
      source: 'HUD',
      update: 'Fair Market Rent updated for Dallas-Fort Worth',
      date: '2 hours ago',
      action: () => onNavigate('invest', 'market-intelligence')
    },
    {
      source: 'FHFA',
      update: 'House Price Index +3.2% QoQ',
      date: '1 day ago',
      action: () => onNavigate('invest', 'market-intelligence')
    },
    {
      source: 'BLS',
      update: 'Employment data shows strong market',
      date: '2 days ago',
      action: () => onNavigate('invest', 'market-intelligence')
    },
  ];

  // Performance Tab Data
  const aumByFund = [
    { name: 'Summit Fund III', value: 145, color: '#3b82f6' },
    { name: 'Coastal Fund II', value: 98, color: '#8b5cf6' },
    { name: 'Metro Growth I', value: 72, color: '#10b981' },
    { name: 'Direct Holdings', value: 35, color: '#f59e0b' },
  ];

  const fundPerformance = [
    { fund: 'Summit Fund III', irr: '14.2%', moic: '1.8x', cashOnCash: '11.5%', status: 'Active' },
    { fund: 'Coastal Fund II', irr: '18.6%', moic: '2.3x', cashOnCash: '15.2%', status: 'Active' },
    { fund: 'Metro Growth I', irr: '12.1%', moic: '1.6x', cashOnCash: '9.8%', status: 'Harvesting' },
    { fund: 'Legacy Fund', irr: '22.4%', moic: '3.1x', cashOnCash: '18.7%', status: 'Closed' },
  ];

  const topAssets = [
    { name: 'Downtown Tower', location: 'Austin, TX', value: '$42M', irr: '16.2%', badge: 'Top' },
    { name: 'Maple Apartments', location: 'Dallas, TX', value: '$28M', irr: '14.8%', badge: 'Top' },
    { name: 'Cedar Heights', location: 'Houston, TX', value: '$22M', irr: '13.5%', badge: 'Top' },
    { name: 'Coastal Plaza', location: 'Miami, FL', value: '$18M', irr: '12.9%', badge: 'Top' },
    { name: 'Tech Park Office', location: 'San Jose, CA', value: '$15M', irr: '11.2%', badge: 'Top' },
  ];

  const bottomAssets = [
    { name: 'Elm Street Retail', location: 'Detroit, MI', value: '$8M', irr: '4.2%', badge: 'Bottom' },
    { name: 'Oak Plaza', location: 'Cleveland, OH', value: '$12M', irr: '5.1%', badge: 'Bottom' },
    { name: 'Pine Tower', location: 'Pittsburgh, PA', value: '$9M', irr: '5.8%', badge: 'Bottom' },
    { name: 'Birch Commons', location: 'Buffalo, NY', value: '$7M', irr: '6.3%', badge: 'Bottom' },
    { name: 'Willow Square', location: 'Syracuse, NY', value: '$6M', irr: '6.7%', badge: 'Bottom' },
  ];

  // Risk Tab Data
  const dscrData = [
    { property: 'Maple Apts', dscr: 1.68, ltv: 0.62, status: 'Healthy' },
    { property: 'Downtown Tower', dscr: 1.52, ltv: 0.58, status: 'Healthy' },
    { property: 'Cedar Heights', dscr: 1.41, ltv: 0.65, status: 'Watch' },
    { property: 'Oak Plaza', dscr: 1.18, ltv: 0.72, status: 'Alert' },
    { property: 'Pine Tower', dscr: 1.35, ltv: 0.68, status: 'Watch' },
  ];

  const exposureData = [
    { category: 'Austin, TX', percentage: 28, amount: '$56M' },
    { category: 'Dallas-Fort Worth', percentage: 22, amount: '$44M' },
    { category: 'Houston, TX', percentage: 18, amount: '$36M' },
    { category: 'Miami, FL', percentage: 15, amount: '$30M' },
    { category: 'Other Markets', percentage: 17, amount: '$34M' },
  ];

  const riskAlerts = [
    { type: 'Covenant', description: 'Oak Plaza DSCR approaching minimum threshold', severity: 'High', property: 'Oak Plaza' },
    { type: 'Occupancy', description: 'Willow Square below 85% occupancy target', severity: 'Medium', property: 'Willow Square' },
    { type: 'Delay', description: 'Tech Park renovation 45 days behind schedule', severity: 'Medium', property: 'Tech Park' },
    { type: 'Market', description: 'Detroit market cap rates compressing', severity: 'Low', property: 'Elm Street' },
  ];

  // Growth Tab Data
  const dealFunnel = [
    { stage: 'Sourcing', count: 24, equity: '$18M' },
    { stage: 'Initial Review', count: 12, equity: '$28M' },
    { stage: 'Underwriting', count: 8, equity: '$42M' },
    { stage: 'Due Diligence', count: 4, equity: '$22M' },
    { stage: 'Closing', count: 2, equity: '$15M' },
  ];

  const developmentPipeline = [
    { project: 'Riverfront Mixed-Use', cost: '$85M', completion: 'Q3 2025', status: 'On Track' },
    { project: 'Tech Campus Phase II', cost: '$62M', completion: 'Q1 2026', status: 'Delayed' },
    { project: 'Metro Apartments', cost: '$42M', completion: 'Q4 2025', status: 'On Track' },
  ];

  const capitalRaising = [
    { fund: 'Summit Fund IV', target: '$250M', committed: '$180M', status: 'Fundraising' },
    { fund: 'Opportunity Fund II', target: '$150M', committed: '$95M', status: 'First Close' },
    { fund: 'Value-Add Fund', target: '$200M', committed: '$45M', status: 'Launch' },
  ];

  const aumProjection = [
    { quarter: 'Q1 24', current: 200, projected: 200 },
    { quarter: 'Q2 24', current: 215, projected: 215 },
    { quarter: 'Q3 24', current: 228, projected: 230 },
    { quarter: 'Q4 24', current: 245, projected: 250 },
    { quarter: 'Q1 25', current: null, projected: 275 },
    { quarter: 'Q2 25', current: null, projected: 305 },
    { quarter: 'Q3 25', current: null, projected: 340 },
    { quarter: 'Q4 25', current: null, projected: 380 },
  ];

  // Cash Tab Data
  const upcomingEvents = [
    { type: 'Capital Call', entity: 'Summit Fund III - Series B', amount: '$8.5M', date: 'Dec 15, 2024', days: 10 },
    { type: 'Distribution', entity: 'Coastal Fund II', amount: '$12.2M', date: 'Dec 20, 2024', days: 15 },
    { type: 'Debt Maturity', entity: 'Maple Apartments Loan', amount: '$18.5M', date: 'Jan 5, 2025', days: 30 },
    { type: 'Capital Call', entity: 'Metro Growth I', amount: '$5.8M', date: 'Jan 10, 2025', days: 35 },
    { type: 'Distribution', entity: 'Summit Fund III', amount: '$6.4M', date: 'Feb 1, 2025', days: 57 },
  ];

  const cashByEntity = [
    { entity: 'Summit Fund III LP', cash: '$24.5M', reserved: '$8.5M', available: '$16.0M' },
    { entity: 'Coastal Fund II LP', cash: '$18.2M', reserved: '$3.2M', available: '$15.0M' },
    { entity: 'Metro Growth I LP', cash: '$12.8M', reserved: '$5.8M', available: '$7.0M' },
    { entity: 'ABC Properties LLC', cash: '$8.4M', reserved: '$2.1M', available: '$6.3M' },
  ];

  const cashflowProjection = [
    { quarter: 'Q4 2024', inflows: 28, outflows: 22, net: 6 },
    { quarter: 'Q1 2025', inflows: 32, outflows: 38, net: -6 },
    { quarter: 'Q2 2025', inflows: 42, outflows: 28, net: 14 },
    { quarter: 'Q3 2025', inflows: 38, outflows: 32, net: 6 },
  ];

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Eye },
    { id: 'performance', label: 'Performance', icon: Award },
    { id: 'risk', label: 'Risk & Exposure', icon: Shield },
    { id: 'growth', label: 'Growth & Pipeline', icon: Rocket },
    { id: 'cash', label: 'Cash & Liquidity', icon: Banknote },
  ];

  const renderOverview = () => (
    <div className="grid grid-cols-12 gap-6">
      {/* Left: What Needs Attention - Wider */}
      <div className="col-span-4">
        <div className="flex items-center gap-2 mb-4">
          <Bell className={`w-5 h-5 ${theme === 'dark' ? 'text-red-400' : 'text-red-600'}`} />
          <h2 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Needs Attention</h2>
          <div className={`ml-auto w-6 h-6 ${theme === 'dark' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-red-100 text-red-700 border-red-300'} rounded-full flex items-center justify-center text-xs border`}>
            {alerts.length}
          </div>
        </div>

        <div className="space-y-3">
          {alerts.map((alert, index) => (
            <GradientCard
              key={index}
              onClick={alert.action}
              gradient={alert.color as any}
              className="p-4 cursor-pointer group"
            >
              <div className="flex items-start gap-3">
                <div className={`w-10 h-10 bg-gradient-to-br ${theme === 'dark' ? `from-${alert.color}-500/10 to-${alert.color}-600/10 border-${alert.color}-500/20` : `from-${alert.color}-100 to-${alert.color}-200 border-${alert.color}-300`} rounded-lg flex items-center justify-center border flex-shrink-0`}>
                  <alert.icon className={`w-5 h-5 ${theme === 'dark' ? `text-${alert.color}-400` : `text-${alert.color}-600`}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between mb-1.5">
                    <h3 className={`text-sm ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{alert.title}</h3>
                    <div className={`px-2 py-0.5 ${theme === 'dark' ? `bg-${alert.color}-500/10 text-${alert.color}-400 border-${alert.color}-500/20` : `bg-${alert.color}-100 text-${alert.color}-700 border-${alert.color}-300`} rounded border text-xs flex-shrink-0 ml-2`}>
                      {alert.count}
                    </div>
                  </div>
                  <p className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'} mb-2 leading-relaxed`}>
                    {alert.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className={`text-xs ${theme === 'dark' ? `text-${alert.color}-400` : `text-${alert.color}-600`}`}>View Details</span>
                    <ChevronRight className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-600' : 'text-slate-400'} group-hover:translate-x-1 transition-transform`} />
                  </div>
                </div>
              </div>
            </GradientCard>
          ))}
        </div>

        {/* Platform Info Card - Compact */}
        <Card className={`mt-4 p-4 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50' : 'bg-gradient-to-br from-slate-100 to-slate-50 border-slate-200'}`}>
          <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'} mb-3`}>Platform Stats</div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <div className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>412+</div>
              <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Endpoints</div>
            </div>
            <div>
              <div className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>18+</div>
              <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Modules</div>
            </div>
            <div>
              <div className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>50+</div>
              <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>DB Models</div>
            </div>
            <div>
              <div className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>v2.4.1</div>
              <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Version</div>
            </div>
          </div>
        </Card>
      </div>

      {/* Middle: What I'm Working On */}
      <div className="col-span-5">
        <div className="flex items-center gap-2 mb-4">
          <Activity className={`w-5 h-5 ${theme === 'dark' ? `text-${brandColor.primary}-400` : `text-${brandColor.primary}-600`}`} />
          <h2 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Working On</h2>
        </div>

        <div className="space-y-3">
          {recentWork.map((work, index) => (
            <GradientCard
              key={index}
              onClick={work.action}
              gradient="blue"
              className="p-4 cursor-pointer group"
            >
              <div className="flex items-start gap-3 mb-3">
                <div className={`w-10 h-10 bg-gradient-to-br ${theme === 'dark' ? `from-${brandColor.primary}-500/10 to-${brandColor.primary}-600/10 border-${brandColor.primary}-500/20` : `from-${brandColor.primary}-100 to-${brandColor.primary}-200 border-${brandColor.primary}-300`} rounded-lg flex items-center justify-center border flex-shrink-0`}>
                  <work.icon className={`w-5 h-5 ${theme === 'dark' ? `text-${brandColor.primary}-400` : `text-${brandColor.primary}-600`}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className={`text-sm mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{work.title}</h3>
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{work.type}</span>
                    <span className={`text-xs ${theme === 'dark' ? 'text-slate-600' : 'text-slate-400'}`}>•</span>
                    <span className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>{work.updated}</span>
                  </div>
                  <div className={`px-2 py-0.5 rounded text-xs inline-flex ${
                    work.status === 'Complete' 
                      ? theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'
                      : work.status === 'In Progress'
                      ? theme === 'dark' ? `bg-${brandColor.primary}-500/10 text-${brandColor.primary}-400 border-${brandColor.primary}-500/20` : `bg-${brandColor.primary}-100 text-${brandColor.primary}-700 border-${brandColor.primary}-300`
                      : theme === 'dark' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' : 'bg-amber-100 text-amber-700 border-amber-300'
                  } border`}>
                    {work.status}
                  </div>
                </div>
              </div>
              
              {/* Progress Bar */}
              <div className="mb-2">
                <div className="flex items-center justify-between mb-1">
                  <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Progress</span>
                  <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{work.progress}%</span>
                </div>
                <div className={`h-1.5 ${theme === 'dark' ? 'bg-slate-800' : 'bg-slate-200'} rounded-full overflow-hidden`}>
                  <div 
                    className={`h-full bg-gradient-to-r ${brandColor.gradient} rounded-full transition-all`}
                    style={{ width: `${work.progress}%` }}
                  />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <span className={`text-xs ${theme === 'dark' ? `text-${brandColor.primary}-400` : `text-${brandColor.primary}-600`}`}>
                  {work.status === 'Complete' ? 'View' : 'Continue'}
                </span>
                <ChevronRight className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-600' : 'text-slate-400'} group-hover:translate-x-1 transition-transform`} />
              </div>
            </GradientCard>
          ))}
        </div>
      </div>

      {/* Right: Insights & Shortcuts */}
      <div className="col-span-3">
        <div className="flex items-center gap-2 mb-4">
          <Target className={`w-5 h-5 ${theme === 'dark' ? 'text-purple-400' : 'text-purple-600'}`} />
          <h2 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Quick Actions</h2>
        </div>

        <div className="grid grid-cols-1 gap-2.5 mb-5">
          {quickActions.map((action, index) => (
            <GradientCard
              key={index}
              onClick={action.action}
              gradient={action.color as any}
              className="p-3.5 cursor-pointer group"
            >
              <div className="flex items-center gap-3">
                <div className={`w-9 h-9 bg-gradient-to-br ${theme === 'dark' ? `from-${action.color}-500/10 to-${action.color}-600/10 border-${action.color}-500/20` : `from-${action.color}-100 to-${action.color}-200 border-${action.color}-300`} rounded-lg flex items-center justify-center border flex-shrink-0 group-hover:scale-110 transition-transform`}>
                  <action.icon className={`w-4 h-4 ${theme === 'dark' ? `text-${action.color}-400` : `text-${action.color}-600`}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className={`text-sm mb-0.5 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{action.title}</h3>
                  <p className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{action.description}</p>
                </div>
              </div>
            </GradientCard>
          ))}
        </div>

        <div className="mb-3">
          <div className="flex items-center gap-2 mb-3">
            <Globe className={`w-4 h-4 ${theme === 'dark' ? 'text-cyan-400' : 'text-cyan-600'}`} />
            <h3 className={`text-sm ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Market Intelligence</h3>
          </div>

          <div className="space-y-2">
            {marketInsights.map((insight, index) => (
              <GradientCard
                key={index}
                onClick={insight.action}
                gradient="cyan"
                className="p-3 cursor-pointer group"
              >
                <div className="flex items-start gap-2.5">
                  <div className={`px-2 py-0.5 ${theme === 'dark' ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20' : 'bg-cyan-100 text-cyan-700 border-cyan-300'} rounded border text-xs flex-shrink-0`}>
                    {insight.source}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className={`text-xs mb-1 leading-relaxed ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>{insight.update}</p>
                    <div className="flex items-center gap-1.5">
                      <Clock className={`w-3 h-3 ${theme === 'dark' ? 'text-slate-500' : 'text-slate-400'}`} />
                      <span className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>{insight.date}</span>
                    </div>
                  </div>
                </div>
              </GradientCard>
            ))}
          </div>
        </div>

        <Button 
          onClick={() => onNavigate('invest', 'market-intelligence')}
          variant="outline" 
          size="sm"
          className={`w-full ${theme === 'dark' ? 'border-slate-700 text-white hover:bg-slate-800/50 bg-slate-900/40' : 'border-slate-300 text-slate-700 hover:bg-slate-50 bg-white'}`}
        >
          View All Market Data
          <ArrowRight className="w-4 h-4 ml-2" />
        </Button>
      </div>
    </div>
  );

  const renderPerformance = () => (
    <div className="space-y-6">
      {/* AUM by Fund */}
      <div className="grid grid-cols-3 gap-6">
        <Card className={`col-span-2 p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
          <h3 className={`text-lg mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>AUM by Fund / Company</h3>
          <p className={`text-sm mb-6 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Total: $350M across 4 vehicles</p>
          <ResponsiveContainer width="100%" height={280}>
            <RechartsBar data={aumByFund} barSize={60}>
              <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#cbd5e1'} opacity={0.2} vertical={false} />
              <XAxis dataKey="name" tick={{ fontSize: 12, fill: theme === 'dark' ? '#94a3b8' : '#475569' }} />
              <YAxis tick={{ fontSize: 12, fill: theme === 'dark' ? '#94a3b8' : '#475569' }} label={{ value: '$M', angle: -90, position: 'insideLeft' }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff', 
                  border: theme === 'dark' ? '1px solid #334155' : '1px solid #cbd5e1',
                  borderRadius: '12px',
                  color: theme === 'dark' ? '#fff' : '#0f172a'
                }}
              />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {aumByFund.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </RechartsBar>
          </ResponsiveContainer>
        </Card>

        <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
          <h3 className={`text-lg mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Realized vs Unrealized</h3>
          <p className={`text-sm mb-6 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Gains breakdown</p>
          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Realized Gains</span>
                <span className={`text-lg ${theme === 'dark' ? 'text-green-400' : 'text-green-700'}`}>$48.2M</span>
              </div>
              <div className={`h-3 ${theme === 'dark' ? 'bg-slate-800' : 'bg-slate-200'} rounded-full overflow-hidden`}>
                <div className="h-full bg-green-500 rounded-full" style={{ width: '62%' }} />
              </div>
            </div>
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Unrealized Gains</span>
                <span className={`text-lg ${theme === 'dark' ? 'text-blue-400' : 'text-blue-700'}`}>$29.6M</span>
              </div>
              <div className={`h-3 ${theme === 'dark' ? 'bg-slate-800' : 'bg-slate-200'} rounded-full overflow-hidden`}>
                <div className="h-full bg-blue-500 rounded-full" style={{ width: '38%' }} />
              </div>
            </div>
            <div className={`pt-4 mt-4 border-t ${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'}`}>
              <div className="flex items-center justify-between">
                <span className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Total Gains</span>
                <span className={`text-xl ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>$77.8M</span>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Fund Performance Table */}
      <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
        <h3 className={`text-lg mb-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Fund Performance Metrics</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className={`border-b ${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'}`}>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Fund</th>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>IRR</th>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>MOIC</th>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Cash-on-Cash</th>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Status</th>
              </tr>
            </thead>
            <tbody>
              {fundPerformance.map((fund, index) => (
                <tr key={index} className={`border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-100'}`}>
                  <td className={`py-3 px-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{fund.fund}</td>
                  <td className={`py-3 px-4 ${theme === 'dark' ? 'text-green-400' : 'text-green-700'}`}>{fund.irr}</td>
                  <td className={`py-3 px-4 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-700'}`}>{fund.moic}</td>
                  <td className={`py-3 px-4 ${theme === 'dark' ? 'text-purple-400' : 'text-purple-700'}`}>{fund.cashOnCash}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs ${
                      fund.status === 'Active' 
                        ? theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'
                        : fund.status === 'Harvesting'
                        ? theme === 'dark' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' : 'bg-amber-100 text-amber-700 border-amber-300'
                        : theme === 'dark' ? 'bg-slate-700 text-slate-300 border-slate-600' : 'bg-slate-200 text-slate-700 border-slate-300'
                    } border`}>
                      {fund.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* League Tables */}
      <div className="grid grid-cols-2 gap-6">
        <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
          <div className="flex items-center gap-2 mb-4">
            <Award className={`w-5 h-5 ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`} />
            <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Top 5 Performing Assets</h3>
          </div>
          <div className="space-y-3">
            {topAssets.map((asset, index) => (
              <div key={index} className={`p-3 rounded-lg ${theme === 'dark' ? 'bg-slate-800/40' : 'bg-slate-50'}`}>
                <div className="flex items-start justify-between mb-1">
                  <div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{asset.name}</div>
                    <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{asset.location}</div>
                  </div>
                  <div className={`px-2 py-0.5 rounded text-xs ${theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'} border`}>
                    #{index + 1}
                  </div>
                </div>
                <div className="flex items-center justify-between mt-2">
                  <span className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>{asset.value}</span>
                  <span className={`text-sm ${theme === 'dark' ? 'text-green-400' : 'text-green-700'}`}>IRR: {asset.irr}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle className={`w-5 h-5 ${theme === 'dark' ? 'text-orange-400' : 'text-orange-600'}`} />
            <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Bottom 5 Assets (Watch List)</h3>
          </div>
          <div className="space-y-3">
            {bottomAssets.map((asset, index) => (
              <div key={index} className={`p-3 rounded-lg ${theme === 'dark' ? 'bg-slate-800/40' : 'bg-slate-50'}`}>
                <div className="flex items-start justify-between mb-1">
                  <div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{asset.name}</div>
                    <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{asset.location}</div>
                  </div>
                  <div className={`px-2 py-0.5 rounded text-xs ${theme === 'dark' ? 'bg-orange-500/10 text-orange-400 border-orange-500/20' : 'bg-orange-100 text-orange-700 border-orange-300'} border`}>
                    {index + 1}
                  </div>
                </div>
                <div className="flex items-center justify-between mt-2">
                  <span className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>{asset.value}</span>
                  <span className={`text-sm ${theme === 'dark' ? 'text-orange-400' : 'text-orange-700'}`}>IRR: {asset.irr}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );

  const renderRisk = () => (
    <div className="space-y-6">
      {/* DSCR & LTV Table */}
      <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
        <h3 className={`text-lg mb-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>DSCR & LTV by Property</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className={`border-b ${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'}`}>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Property</th>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>DSCR</th>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>LTV</th>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Status</th>
                <th className={`text-left py-3 px-4 text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Covenant Health</th>
              </tr>
            </thead>
            <tbody>
              {dscrData.map((row, index) => (
                <tr key={index} className={`border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-100'}`}>
                  <td className={`py-3 px-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{row.property}</td>
                  <td className={`py-3 px-4 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-700'}`}>{row.dscr.toFixed(2)}x</td>
                  <td className={`py-3 px-4 ${theme === 'dark' ? 'text-purple-400' : 'text-purple-700'}`}>{(row.ltv * 100).toFixed(0)}%</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs ${
                      row.status === 'Healthy' 
                        ? theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'
                        : row.status === 'Watch'
                        ? theme === 'dark' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' : 'bg-amber-100 text-amber-700 border-amber-300'
                        : theme === 'dark' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-red-100 text-red-700 border-red-300'
                    } border`}>
                      {row.status}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <div className={`h-2 w-24 ${theme === 'dark' ? 'bg-slate-800' : 'bg-slate-200'} rounded-full overflow-hidden`}>
                      <div 
                        className={`h-full ${row.status === 'Healthy' ? 'bg-green-500' : row.status === 'Watch' ? 'bg-amber-500' : 'bg-red-500'}`}
                        style={{ width: row.status === 'Healthy' ? '90%' : row.status === 'Watch' ? '65%' : '40%' }}
                      />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Exposure & Concentration */}
      <div className="grid grid-cols-2 gap-6">
        <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
          <div className="flex items-center gap-2 mb-4">
            <Map className={`w-5 h-5 ${theme === 'dark' ? 'text-cyan-400' : 'text-cyan-600'}`} />
            <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Geographic Exposure</h3>
          </div>
          <div className="space-y-3">
            {exposureData.map((item, index) => (
              <div key={index}>
                <div className="flex items-center justify-between mb-1">
                  <span className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>{item.category}</span>
                  <div className="flex items-center gap-2">
                    <span className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{item.amount}</span>
                    <span className={`text-sm ${theme === 'dark' ? 'text-blue-400' : 'text-blue-700'}`}>{item.percentage}%</span>
                  </div>
                </div>
                <div className={`h-2 ${theme === 'dark' ? 'bg-slate-800' : 'bg-slate-200'} rounded-full overflow-hidden`}>
                  <div 
                    className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                    style={{ width: `${item.percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
          <div className="flex items-center gap-2 mb-4">
            <Layers className={`w-5 h-5 ${theme === 'dark' ? 'text-purple-400' : 'text-purple-600'}`} />
            <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Concentration Risk</h3>
          </div>
          <div className="space-y-4">
            <div className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-slate-800/40 border border-slate-700' : 'bg-blue-50 border border-blue-200'}`}>
              <div className={`text-xs mb-1 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Top 10 Tenants</div>
              <div className={`text-2xl mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>42%</div>
              <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-600'}`}>of total rental revenue</div>
            </div>
            <div className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-slate-800/40 border border-slate-700' : 'bg-purple-50 border border-purple-200'}`}>
              <div className={`text-xs mb-1 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Top 3 Lenders</div>
              <div className={`text-2xl mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>68%</div>
              <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-600'}`}>of total debt outstanding</div>
            </div>
            <div className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-slate-800/40 border border-slate-700' : 'bg-green-50 border border-green-200'}`}>
              <div className={`text-xs mb-1 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Single Asset Exposure</div>
              <div className={`text-2xl mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>21%</div>
              <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-600'}`}>largest asset (Downtown Tower)</div>
            </div>
          </div>
        </Card>
      </div>

      {/* Risk Alerts */}
      <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
        <div className="flex items-center gap-2 mb-4">
          <AlertOctagon className={`w-5 h-5 ${theme === 'dark' ? 'text-red-400' : 'text-red-600'}`} />
          <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Risk Alerts</h3>
        </div>
        <div className="space-y-3">
          {riskAlerts.map((alert, index) => (
            <div key={index} className={`p-4 rounded-lg border ${
              alert.severity === 'High'
                ? theme === 'dark' ? 'bg-red-500/10 border-red-500/20' : 'bg-red-50 border-red-200'
                : alert.severity === 'Medium'
                ? theme === 'dark' ? 'bg-amber-500/10 border-amber-500/20' : 'bg-amber-50 border-amber-200'
                : theme === 'dark' ? 'bg-blue-500/10 border-blue-500/20' : 'bg-blue-50 border-blue-200'
            }`}>
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    alert.severity === 'High'
                      ? theme === 'dark' ? 'bg-red-500/20 text-red-400' : 'bg-red-200 text-red-800'
                      : alert.severity === 'Medium'
                      ? theme === 'dark' ? 'bg-amber-500/20 text-amber-400' : 'bg-amber-200 text-amber-800'
                      : theme === 'dark' ? 'bg-blue-500/20 text-blue-400' : 'bg-blue-200 text-blue-800'
                  }`}>
                    {alert.severity}
                  </span>
                  <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{alert.type}</span>
                </div>
                <span className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-600'}`}>{alert.property}</span>
              </div>
              <p className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>{alert.description}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );

  const renderGrowth = () => (
    <div className="space-y-6">
      {/* Deal Funnel */}
      <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
        <h3 className={`text-lg mb-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Deal Funnel</h3>
        <div className="space-y-3">
          {dealFunnel.map((stage, index) => (
            <div key={index}>
              <div className="flex items-center justify-between mb-2">
                <span className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>{stage.stage}</span>
                <div className="flex items-center gap-3">
                  <span className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{stage.count} deals</span>
                  <span className={`text-sm ${theme === 'dark' ? 'text-blue-400' : 'text-blue-700'}`}>{stage.equity} equity</span>
                </div>
              </div>
              <div className={`h-3 ${theme === 'dark' ? 'bg-slate-800' : 'bg-slate-200'} rounded-full overflow-hidden`}>
                <div 
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                  style={{ width: `${(stage.count / 24) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
        <div className={`mt-6 pt-6 border-t ${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'}`}>
          <div className="flex items-center justify-between">
            <span className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Total Pipeline</span>
            <span className={`text-xl ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>$125M expected equity</span>
          </div>
        </div>
      </Card>

      {/* Development Pipeline & Capital Raising */}
      <div className="grid grid-cols-2 gap-6">
        <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
          <div className="flex items-center gap-2 mb-4">
            <Wrench className={`w-5 h-5 ${theme === 'dark' ? 'text-orange-400' : 'text-orange-600'}`} />
            <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Development Pipeline</h3>
          </div>
          <div className="space-y-3">
            {developmentPipeline.map((project, index) => (
              <div key={index} className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-slate-800/40' : 'bg-slate-50'}`}>
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <div className={`text-sm mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{project.project}</div>
                    <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Total Cost: {project.cost}</div>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    project.status === 'On Track'
                      ? theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'
                      : theme === 'dark' ? 'bg-orange-500/10 text-orange-400 border-orange-500/20' : 'bg-orange-100 text-orange-700 border-orange-300'
                  } border`}>
                    {project.status}
                  </span>
                </div>
                <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>Expected: {project.completion}</div>
              </div>
            ))}
          </div>
        </Card>

        <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
          <div className="flex items-center gap-2 mb-4">
            <CircleDollarSign className={`w-5 h-5 ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`} />
            <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Capital Raising</h3>
          </div>
          <div className="space-y-4">
            {capitalRaising.map((fund, index) => (
              <div key={index} className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-slate-800/40' : 'bg-slate-50'}`}>
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className={`text-sm mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{fund.fund}</div>
                    <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Target: {fund.target}</div>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-xs ${theme === 'dark' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 'bg-blue-100 text-blue-700 border-blue-300'} border`}>
                    {fund.status}
                  </span>
                </div>
                <div className="mb-2">
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Committed</span>
                    <span className={`text-xs ${theme === 'dark' ? 'text-green-400' : 'text-green-700'}`}>{fund.committed}</span>
                  </div>
                  <div className={`h-2 ${theme === 'dark' ? 'bg-slate-700' : 'bg-slate-200'} rounded-full overflow-hidden`}>
                    <div 
                      className="h-full bg-green-500"
                      style={{ width: `${(parseInt(fund.committed.replace(/[$M]/g, '')) / parseInt(fund.target.replace(/[$M]/g, ''))) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* AUM Projection */}
      <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
        <h3 className={`text-lg mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Projected AUM Growth</h3>
        <p className={`text-sm mb-6 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>12-24 month forecast vs current</p>
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={aumProjection}>
            <defs>
              <linearGradient id="projectedGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#cbd5e1'} opacity={0.2} />
            <XAxis dataKey="quarter" stroke={theme === 'dark' ? '#94a3b8' : '#475569'} fontSize={12} />
            <YAxis stroke={theme === 'dark' ? '#94a3b8' : '#475569'} fontSize={12} label={{ value: '$M', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff', 
                border: theme === 'dark' ? '1px solid #334155' : '1px solid #cbd5e1',
                borderRadius: '12px',
                color: theme === 'dark' ? '#fff' : '#0f172a'
              }}
            />
            <Legend />
            <Area type="monotone" dataKey="projected" stroke="#3b82f6" strokeWidth={2} fill="url(#projectedGrad)" name="Projected AUM" />
            <Line type="monotone" dataKey="current" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} name="Current AUM" />
          </ComposedChart>
        </ResponsiveContainer>
      </Card>
    </div>
  );

  const renderCash = () => (
    <div className="space-y-6">
      {/* Upcoming Events */}
      <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
        <h3 className={`text-lg mb-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Upcoming Capital Events</h3>
        <div className="space-y-3">
          {upcomingEvents.map((event, index) => (
            <div key={index} className={`p-4 rounded-lg border ${theme === 'dark' ? 'bg-slate-800/40 border-slate-700' : 'bg-slate-50 border-slate-200'}`}>
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-3">
                  <div className={`px-2 py-1 rounded text-xs ${
                    event.type === 'Capital Call'
                      ? theme === 'dark' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-red-100 text-red-700 border-red-300'
                      : event.type === 'Distribution'
                      ? theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'
                      : theme === 'dark' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' : 'bg-amber-100 text-amber-700 border-amber-300'
                  } border`}>
                    {event.type}
                  </div>
                  <div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{event.entity}</div>
                    <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{event.date} ({event.days} days)</div>
                  </div>
                </div>
                <div className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{event.amount}</div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Cash Balance by Entity */}
      <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
        <h3 className={`text-lg mb-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Cash Balance by Entity</h3>
        <div className="space-y-4">
          {cashByEntity.map((entity, index) => (
            <div key={index} className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-slate-800/40' : 'bg-slate-50'}`}>
              <div className={`text-sm mb-3 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{entity.entity}</div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <div className={`text-xs mb-1 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Total Cash</div>
                  <div className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>{entity.cash}</div>
                </div>
                <div>
                  <div className={`text-xs mb-1 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Reserved</div>
                  <div className={`text-lg ${theme === 'dark' ? 'text-amber-400' : 'text-amber-700'}`}>{entity.reserved}</div>
                </div>
                <div>
                  <div className={`text-xs mb-1 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Available</div>
                  <div className={`text-lg ${theme === 'dark' ? 'text-green-400' : 'text-green-700'}`}>{entity.available}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className={`mt-6 pt-6 border-t ${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'}`}>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <div className={`text-xs mb-1 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Total Cash</div>
              <div className={`text-2xl ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>$63.9M</div>
            </div>
            <div>
              <div className={`text-xs mb-1 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Total Reserved</div>
              <div className={`text-2xl ${theme === 'dark' ? 'text-amber-400' : 'text-amber-700'}`}>$19.6M</div>
            </div>
            <div>
              <div className={`text-xs mb-1 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Total Available</div>
              <div className={`text-2xl ${theme === 'dark' ? 'text-green-400' : 'text-green-700'}`}>$44.3M</div>
            </div>
          </div>
        </div>
      </Card>

      {/* Cashflow Projection */}
      <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'}`}>
        <h3 className={`text-lg mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Quarterly Cashflow Projection</h3>
        <p className={`text-sm mb-6 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Expected inflows vs outflows (in $M)</p>
        <ResponsiveContainer width="100%" height={300}>
          <RechartsBar data={cashflowProjection} barSize={40}>
            <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#cbd5e1'} opacity={0.2} vertical={false} />
            <XAxis dataKey="quarter" stroke={theme === 'dark' ? '#94a3b8' : '#475569'} fontSize={12} />
            <YAxis stroke={theme === 'dark' ? '#94a3b8' : '#475569'} fontSize={12} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff', 
                border: theme === 'dark' ? '1px solid #334155' : '1px solid #cbd5e1',
                borderRadius: '12px',
                color: theme === 'dark' ? '#fff' : '#0f172a'
              }}
            />
            <Legend />
            <Bar dataKey="inflows" fill="#10b981" radius={[8, 8, 0, 0]} name="Inflows" />
            <Bar dataKey="outflows" fill="#ef4444" radius={[8, 8, 0, 0]} name="Outflows" />
            <Bar dataKey="net" fill="#3b82f6" radius={[8, 8, 0, 0]} name="Net" />
          </RechartsBar>
        </ResponsiveContainer>
      </Card>
    </div>
  );

  return (
    <div className={`h-full overflow-auto ${theme === 'light' ? 'bg-slate-50/50' : ''}`}>
      {/* Hero KPI Strip - More Compact */}
      <div className={`${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50' : 'bg-white/60 border-slate-200/80'} border-b px-8 py-5 backdrop-blur-sm`}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className={`text-xl mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>
              CEO View
            </h1>
            <p className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
              {selectedCompany?.name || 'No Company Selected'} · {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setTimeFrame('week')}
              className={`h-8 text-xs ${
                timeFrame === 'week'
                  ? theme === 'dark'
                    ? 'border-blue-500 text-white bg-blue-600 hover:bg-blue-700'
                    : 'border-blue-600 text-white bg-blue-600 hover:bg-blue-700'
                  : theme === 'dark'
                    ? 'border-slate-700 text-slate-300 bg-slate-800/50 hover:bg-slate-800 hover:text-white'
                    : 'border-slate-300 text-slate-700 bg-white hover:bg-slate-50'
              }`}
            >
              This Week
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setTimeFrame('month')}
              className={`h-8 text-xs ${
                timeFrame === 'month'
                  ? theme === 'dark'
                    ? 'border-blue-500 text-white bg-blue-600 hover:bg-blue-700'
                    : 'border-blue-600 text-white bg-blue-600 hover:bg-blue-700'
                  : theme === 'dark'
                    ? 'border-slate-700 text-slate-300 bg-slate-800/50 hover:bg-slate-800 hover:text-white'
                    : 'border-slate-300 text-slate-700 bg-white hover:bg-slate-50'
              }`}
            >
              30 Days
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setTimeFrame('quarter')}
              className={`h-8 text-xs ${
                timeFrame === 'quarter'
                  ? theme === 'dark'
                    ? 'border-blue-500 text-white bg-blue-600 hover:bg-blue-700'
                    : 'border-blue-600 text-white bg-blue-600 hover:bg-blue-700'
                  : theme === 'dark'
                    ? 'border-slate-700 text-slate-300 bg-slate-800/50 hover:bg-slate-800 hover:text-white'
                    : 'border-slate-300 text-slate-700 bg-white hover:bg-slate-50'
              }`}
            >
              Quarter
            </Button>
          </div>
        </div>

        {/* Key KPIs - Enhanced with animations and sparklines */}
        <div className="grid grid-cols-5 gap-4">
          {kpis.map((kpi, index) => (
            <StatsCard
              key={index}
              label={kpi.label}
              value={kpi.value}
              icon={kpi.icon}
              gradient={kpi.gradient}
              trend={kpi.trend}
              trendValue={kpi.change}
              subtitle={kpi.subtitle}
              sparklineData={kpi.sparkline}
              animated={true}
              prefix={kpi.prefix}
              suffix={kpi.suffix}
              decimals={kpi.decimals}
            />
          ))}
        </div>
      </div>

      {/* Tab Navigation */}
      <div className={`${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50' : 'bg-white border-slate-200'} border-b px-8`}>
        <div className="flex gap-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-3 border-b-2 transition-all ${
                activeTab === tab.id
                  ? `${theme === 'dark' ? 'border-blue-500 text-blue-400 bg-slate-800/40' : 'border-blue-600 text-blue-700 bg-blue-50/50'}`
                  : `border-transparent ${theme === 'dark' ? 'text-slate-400 hover:text-white hover:bg-slate-800/20' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'}`
              }`}
            >
              <tab.icon className="w-4 h-4" />
              <span className="text-sm">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'performance' && renderPerformance()}
        {activeTab === 'risk' && renderRisk()}
        {activeTab === 'growth' && renderGrowth()}
        {activeTab === 'cash' && renderCash()}
      </div>
    </div>
  );
}
