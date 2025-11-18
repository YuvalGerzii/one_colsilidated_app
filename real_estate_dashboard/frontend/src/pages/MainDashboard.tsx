/**
 * Main Executive Dashboard - Comprehensive Summary
 *
 * @version 2.1.0
 * @created 2025-11-15
 * @updated 2025-11-15
 * @description Executive dashboard with sidebar layout showing key data from all modules
 */
import { useState, useMemo, useEffect } from 'react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { StatsCard } from '../components/ui/StatsCard';
import { GradientCard } from '../components/ui/GradientCard';
import {
  Building2, DollarSign, TrendingUp, Users, PieChart,
  AlertCircle, CheckCircle2, Clock, Target, BarChart3,
  Home, Briefcase, Calculator, Landmark, ArrowUpRight, ArrowDownRight,
  Activity, Bell, Plus, FileText, ListTodo, Calendar
} from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { useCompany } from '../context/CompanyContext';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip, Legend, Cell, PieChart as RechartsPieChart, Pie } from 'recharts';
import { ProjectTrackingWidget } from '../components/ProjectTracking/ProjectTrackingWidget';
import { apiClient } from '../services/apiClient';

type TimeFrame = 'week' | 'month' | 'quarter' | 'year';

interface RecentActivity {
  id: string;
  type: 'property' | 'deal' | 'task' | 'financial' | 'alert';
  title: string;
  description: string;
  time: string;
  icon: any;
  color: string;
}

interface DashboardData {
  // Property Management data
  portfolioSummary: {
    total_properties: number;
    total_units: number;
    occupied_units: number;
    vacant_units: number;
    physical_occupancy_rate: number;
    portfolio_value: number;
    monthly_gpr: number;
    monthly_noi: number;
    portfolio_cap_rate: number;
  } | null;
  // Project Tracking data
  projectSummary: {
    total_tasks: number;
    pending_tasks: number;
    in_progress_tasks: number;
    completed_tasks: number;
  } | null;
  // CRM data
  deals: {
    total: number;
  } | null;
  // Portfolio Analytics data
  performanceMetrics: {
    irr: number | null;
    average_occupancy: number | null;
    total_noi: number | null;
  } | null;
}

export function MainDashboard() {
  const { theme, colors } = useTheme();
  const { selectedCompany } = useCompany();
  const [timeFrame, setTimeFrame] = useState<TimeFrame>('month');
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState<DashboardData>({
    portfolioSummary: null,
    projectSummary: null,
    deals: null,
    performanceMetrics: null,
  });

  // Fetch all dashboard data from APIs
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        console.log('[MainDashboard] Fetching data for company:', selectedCompany?.name);

        // Fetch data from all endpoints in parallel (only use endpoints that exist)
        const [portfolioRes, projectRes, dealsRes] = await Promise.allSettled([
          apiClient.get('/property-management/dashboard/summary').catch(err => {
            console.warn('[MainDashboard] Portfolio API error:', err);
            return null;
          }),
          apiClient.get('/project-tracking/dashboard/summary').catch(err => {
            console.warn('[MainDashboard] Project tracking API error:', err);
            return null;
          }),
          apiClient.get('/crm/api/deals').catch(err => {
            console.warn('[MainDashboard] CRM API error:', err);
            return null;
          }),
        ]);

        const portfolioData = portfolioRes.status === 'fulfilled' ? portfolioRes.value : null;
        const projectData = projectRes.status === 'fulfilled' ? projectRes.value : null;
        const dealsData = dealsRes.status === 'fulfilled' ? dealsRes.value : null;

        console.log('[MainDashboard] API Results:', {
          portfolio: portfolioData,
          project: projectData,
          deals: dealsData,
        });

        setDashboardData({
          portfolioSummary: portfolioData,
          projectSummary: projectData,
          deals: dealsData,
          performanceMetrics: null, // TODO: Add when portfolio analytics endpoint is available
        });
      } catch (error) {
        console.error('[MainDashboard] Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [selectedCompany]);

  // Check if this is a new company with no data
  const isNewCompany = useMemo(() => {
    // Company is "new" if it has no properties
    const hasNoProperties = (dashboardData.portfolioSummary?.total_properties || 0) === 0;
    console.log('[MainDashboard] isNewCompany:', hasNoProperties, 'properties:', dashboardData.portfolioSummary?.total_properties);
    return hasNoProperties;
  }, [dashboardData.portfolioSummary]);

  // Extract real data from API responses with fallbacks
  const portfolioValue = (dashboardData.portfolioSummary?.portfolio_value || 0) / 1000000; // Convert to millions
  const propertyCount = dashboardData.portfolioSummary?.total_properties || 0;
  const revenue = ((dashboardData.portfolioSummary?.monthly_gpr || 0) * 12) / 1000000; // Annual revenue in millions
  const occupancy = dashboardData.portfolioSummary?.physical_occupancy_rate || 0;
  const occupiedUnits = dashboardData.portfolioSummary?.occupied_units || 0;
  const totalUnits = dashboardData.portfolioSummary?.total_units || 0;
  const activeDeals = dashboardData.deals?.total || 0;
  const pipelineValue = 0; // TODO: Add pipeline value calculation
  const fundNav = 0; // TODO: Fetch from fund management API
  const portfolioIRR = dashboardData.performanceMetrics?.irr || 0;

  console.log('[MainDashboard] Calculated values:', {
    portfolioValue,
    propertyCount,
    revenue,
    occupancy,
    occupiedUnits,
    totalUnits,
    activeDeals,
    portfolioIRR,
    isNewCompany,
    loading
  });

  // Sparkline data for metrics
  const portfolioValueSparkline = isNewCompany ? [] : [
    { value: 42.5 }, { value: 43.8 }, { value: 44.2 }, { value: 45.6 }, { value: 46.3 }, { value: 47.2 }
  ];
  const revenueSparkline = isNewCompany ? [] : [
    { value: 5.1 }, { value: 5.3 }, { value: 5.4 }, { value: 5.5 }, { value: 5.6 }, { value: 5.8 }
  ];
  const irrSparkline = isNewCompany ? [] : [
    { value: 12.8 }, { value: 13.1 }, { value: 13.5 }, { value: 13.8 }, { value: 14.0 }, { value: 14.2 }
  ];
  const occupancySparkline = isNewCompany ? [] : [
    { value: 94.2 }, { value: 95.1 }, { value: 95.8 }, { value: 96.2 }, { value: 96.5 }, { value: 96.8 }
  ];
  const dealsSparkline = isNewCompany ? [] : [
    { value: 8 }, { value: 9 }, { value: 10 }, { value: 11 }, { value: 11 }, { value: 12 }
  ];
  const navSparkline = isNewCompany ? [] : [
    { value: 110 }, { value: 112 }, { value: 115 }, { value: 117 }, { value: 119 }, { value: 120 }
  ];

  // Comprehensive metrics across all sections
  const overallMetrics = [
    {
      label: 'Total Portfolio Value',
      value: portfolioValue,
      prefix: '$',
      suffix: 'M',
      decimals: 1,
      change: isNewCompany ? '—' : '+8.2%',
      trend: 'up' as const,
      icon: Building2,
      gradient: 'blue' as const,
      subtitle: isNewCompany ? 'No properties yet' : `${propertyCount} properties`,
      sparkline: portfolioValueSparkline
    },
    {
      label: 'Annual Revenue',
      value: revenue,
      prefix: '$',
      suffix: 'M',
      decimals: 1,
      change: isNewCompany ? '—' : '+12.4%',
      trend: 'up' as const,
      icon: DollarSign,
      gradient: 'green' as const,
      subtitle: isNewCompany ? 'No revenue yet' : 'Last 12 months',
      sparkline: revenueSparkline
    },
    {
      label: 'Avg Portfolio IRR',
      value: portfolioIRR,
      prefix: '',
      suffix: '%',
      decimals: 1,
      change: isNewCompany ? '—' : '+1.8%',
      trend: 'up' as const,
      icon: TrendingUp,
      gradient: 'purple' as const,
      subtitle: 'Target: 12%',
      sparkline: irrSparkline
    },
    {
      label: 'Occupancy Rate',
      value: occupancy,
      prefix: '',
      suffix: '%',
      decimals: 1,
      change: isNewCompany ? '—' : '+2.1%',
      trend: 'up' as const,
      icon: Home,
      gradient: 'cyan' as const,
      subtitle: isNewCompany ? 'No units yet' : `${occupiedUnits}/${totalUnits} units`,
      sparkline: occupancySparkline
    },
    {
      label: 'Active Deals',
      value: activeDeals,
      prefix: '',
      suffix: '',
      decimals: 0,
      change: isNewCompany ? '—' : '+3',
      trend: 'up' as const,
      icon: Briefcase,
      gradient: 'amber' as const,
      subtitle: isNewCompany ? 'No deals yet' : `$${pipelineValue}M pipeline`,
      sparkline: dealsSparkline
    },
    {
      label: 'Fund NAV',
      value: fundNav,
      prefix: '$',
      suffix: 'M',
      decimals: 0,
      change: isNewCompany ? '—' : '+5.3%',
      trend: 'up' as const,
      icon: PieChart,
      gradient: 'orange' as const,
      subtitle: isNewCompany ? 'No funds yet' : 'Fund I & II',
      sparkline: navSparkline
    },
  ];

  const sectionSummaries = [
    {
      section: 'Operations',
      icon: Building2,
      color: 'blue',
      metrics: [
        { label: 'Properties', value: isNewCompany ? '0' : '23', status: 'good' },
        { label: 'Occupancy', value: isNewCompany ? '—' : '96.8%', status: 'good' },
        { label: 'Maintenance Tickets', value: isNewCompany ? '0' : '8', status: 'warning' },
        { label: 'Lease Renewals', value: isNewCompany ? '0' : '14', status: 'info' },
      ],
      alerts: isNewCompany ? 0 : 3,
      trend: 'up'
    },
    {
      section: 'Investment',
      icon: TrendingUp,
      color: 'emerald',
      metrics: [
        { label: 'Active Deals', value: isNewCompany ? '0' : '12', status: 'good' },
        { label: 'Pipeline Value', value: isNewCompany ? '$0' : '$68M', status: 'good' },
        { label: 'Due Diligence', value: isNewCompany ? '0' : '5', status: 'info' },
        { label: 'Under LOI', value: isNewCompany ? '0' : '3', status: 'info' },
      ],
      alerts: isNewCompany ? 0 : 2,
      trend: 'up'
    },
    {
      section: 'Capital',
      icon: DollarSign,
      color: 'purple',
      metrics: [
        { label: 'Total Funds', value: isNewCompany ? '$0' : '$120M', status: 'good' },
        { label: 'Deployed', value: isNewCompany ? '—' : '68%', status: 'good' },
        { label: 'Total Debt', value: isNewCompany ? '$0' : '$28M', status: 'good' },
        { label: 'Avg DSCR', value: isNewCompany ? '—' : '1.48x', status: 'good' },
      ],
      alerts: isNewCompany ? 0 : 1,
      trend: 'stable'
    },
    {
      section: 'Analytics',
      icon: BarChart3,
      color: 'cyan',
      metrics: [
        { label: 'Portfolio ROI', value: isNewCompany ? '—' : '14.2%', status: 'good' },
        { label: 'Cash Yield', value: isNewCompany ? '—' : '6.8%', status: 'good' },
        { label: 'Reports Generated', value: isNewCompany ? '0' : '24', status: 'info' },
        { label: 'Models Run', value: isNewCompany ? '0' : '47', status: 'info' },
      ],
      alerts: 0,
      trend: 'up'
    },
  ];

  const revenueData = isNewCompany ? [] : [
    { month: 'Jan', revenue: 420, expenses: 280, profit: 140 },
    { month: 'Feb', revenue: 445, expenses: 290, profit: 155 },
    { month: 'Mar', revenue: 470, expenses: 295, profit: 175 },
    { month: 'Apr', revenue: 485, expenses: 300, profit: 185 },
    { month: 'May', revenue: 510, expenses: 310, profit: 200 },
    { month: 'Jun', revenue: 528, expenses: 315, profit: 213 },
  ];

  const portfolioPerformance = isNewCompany ? [] : [
    { name: 'Multifamily', value: 18500000, count: 12, yield: 7.2 },
    { name: 'Office', value: 12200000, count: 5, yield: 6.8 },
    { name: 'Retail', value: 8900000, count: 4, yield: 6.5 },
    { name: 'Industrial', value: 7600000, count: 2, yield: 7.8 },
  ];

  // Recent activity feed (company-specific)
  const recentActivities: RecentActivity[] = isNewCompany ? [
    {
      id: '1',
      type: 'alert',
      title: 'Welcome to Your Dashboard',
      description: 'Start by adding your first property or investment deal',
      time: 'Just now',
      icon: Bell,
      color: 'blue'
    }
  ] : [
    {
      id: '1',
      type: 'property',
      title: 'New Lease Signed',
      description: 'Unit 204 at Maple Heights - $2,400/mo',
      time: '2 hours ago',
      icon: Home,
      color: 'green'
    },
    {
      id: '2',
      type: 'deal',
      title: 'Deal Progressed',
      description: 'Oak Street Retail moved to Due Diligence',
      time: '5 hours ago',
      icon: Briefcase,
      color: 'blue'
    },
    {
      id: '3',
      type: 'task',
      title: 'Task Completed',
      description: 'Q4 Financial Report submitted',
      time: '1 day ago',
      icon: CheckCircle2,
      color: 'purple'
    },
    {
      id: '4',
      type: 'financial',
      title: 'Payment Received',
      description: '$45,200 rent collection processed',
      time: '2 days ago',
      icon: DollarSign,
      color: 'emerald'
    },
    {
      id: '5',
      type: 'alert',
      title: 'Maintenance Alert',
      description: 'HVAC inspection due at Pine Valley',
      time: '3 days ago',
      icon: AlertCircle,
      color: 'amber'
    },
  ];

  // Quick actions
  const quickActions = [
    { label: 'Add Property', icon: Building2, color: 'blue', path: '/property-management' },
    { label: 'New Deal', icon: Briefcase, color: 'emerald', path: '/crm/deals' },
    { label: 'Create Task', icon: ListTodo, color: 'purple', path: '/project-tracking' },
    { label: 'Run Report', icon: FileText, color: 'cyan', path: '/reports' },
  ];

  const getColorClasses = (color: string) => {
    const colorMap: Record<string, { bg: string; text: string; border: string; gradient: string }> = {
      blue: {
        bg: theme === 'dark' ? 'bg-blue-500/10' : 'bg-blue-50',
        text: theme === 'dark' ? 'text-blue-400' : 'text-blue-600',
        border: theme === 'dark' ? 'border-blue-500/20' : 'border-blue-200',
        gradient: 'from-blue-600 to-blue-700'
      },
      green: {
        bg: theme === 'dark' ? 'bg-green-500/10' : 'bg-green-50',
        text: theme === 'dark' ? 'text-green-400' : 'text-green-600',
        border: theme === 'dark' ? 'border-green-500/20' : 'border-green-200',
        gradient: 'from-green-600 to-green-700'
      },
      emerald: {
        bg: theme === 'dark' ? 'bg-emerald-500/10' : 'bg-emerald-50',
        text: theme === 'dark' ? 'text-emerald-400' : 'text-emerald-600',
        border: theme === 'dark' ? 'border-emerald-500/20' : 'border-emerald-200',
        gradient: 'from-emerald-600 to-emerald-700'
      },
      cyan: {
        bg: theme === 'dark' ? 'bg-cyan-500/10' : 'bg-cyan-50',
        text: theme === 'dark' ? 'text-cyan-400' : 'text-cyan-600',
        border: theme === 'dark' ? 'border-cyan-500/20' : 'border-cyan-200',
        gradient: 'from-cyan-600 to-cyan-700'
      },
      purple: {
        bg: theme === 'dark' ? 'bg-purple-500/10' : 'bg-purple-50',
        text: theme === 'dark' ? 'text-purple-400' : 'text-purple-600',
        border: theme === 'dark' ? 'border-purple-500/20' : 'border-purple-200',
        gradient: 'from-purple-600 to-purple-700'
      },
      orange: {
        bg: theme === 'dark' ? 'bg-orange-500/10' : 'bg-orange-50',
        text: theme === 'dark' ? 'text-orange-400' : 'text-orange-600',
        border: theme === 'dark' ? 'border-orange-500/20' : 'border-orange-200',
        gradient: 'from-orange-600 to-orange-700'
      },
      amber: {
        bg: theme === 'dark' ? 'bg-amber-500/10' : 'bg-amber-50',
        text: theme === 'dark' ? 'text-amber-400' : 'text-amber-600',
        border: theme === 'dark' ? 'border-amber-500/20' : 'border-amber-200',
        gradient: 'from-amber-600 to-amber-700'
      },
    };
    return colorMap[color] || colorMap.blue;
  };

  const getActivityIcon = (type: string) => {
    const iconMap: Record<string, any> = {
      property: Home,
      deal: Briefcase,
      task: CheckCircle2,
      financial: DollarSign,
      alert: AlertCircle,
    };
    return iconMap[type] || Activity;
  };

  const timeFrameLabels: Record<TimeFrame, string> = {
    week: 'This Week',
    month: '30 Days',
    quarter: 'Quarter',
    year: 'Year'
  };

  return (
    <div className={`${colors.bg.primary} min-h-screen`}>
      {/* Header */}
      <div className={`${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50' : 'bg-white/60 border-slate-200/80'} border-b px-8 py-5 backdrop-blur-sm sticky top-0 z-10`}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className={`text-2xl font-bold mb-1 ${colors.text.primary}`}>
              Executive Dashboard
            </h1>
            <p className={`text-sm ${colors.text.secondary}`}>
              {selectedCompany?.name || 'All Companies'} · {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}
            </p>
          </div>
          <div className="flex items-center gap-2">
            {(Object.keys(timeFrameLabels) as TimeFrame[]).map((tf) => (
              <Button
                key={tf}
                variant={timeFrame === tf ? "default" : "outline"}
                size="sm"
                onClick={() => setTimeFrame(tf)}
                className={`h-8 text-xs ${
                  timeFrame === tf
                    ? theme === 'dark'
                      ? 'border-blue-500 text-white bg-blue-600 hover:bg-blue-700'
                      : 'border-blue-600 text-white bg-blue-600 hover:bg-blue-700'
                    : theme === 'dark'
                      ? 'border-slate-700 text-slate-300 bg-slate-800/50 hover:bg-slate-800 hover:text-white'
                      : 'border-slate-300 text-slate-700 bg-white hover:bg-slate-50'
                }`}
              >
                {timeFrameLabels[tf]}
              </Button>
            ))}
          </div>
        </div>

        {/* Top-Level Metrics - Enhanced with animations and sparklines */}
        <div className="grid grid-cols-6 gap-4">
          {overallMetrics.map((metric, index) => (
            <StatsCard
              key={index}
              label={metric.label}
              value={metric.value}
              icon={metric.icon}
              gradient={metric.gradient}
              trend={metric.trend}
              trendValue={metric.change}
              subtitle={metric.subtitle}
              sparklineData={metric.sparkline}
              animated={true}
              prefix={metric.prefix}
              suffix={metric.suffix}
              decimals={metric.decimals}
            />
          ))}
        </div>
      </div>

      {/* Main Content with Sidebar Layout */}
      <div className="flex gap-6 p-8">
        {/* Left Sidebar - 30% width */}
        <div className="w-[30%] space-y-6">
          {/* Project Tracking Summary */}
          <GradientCard gradient="blue" className="p-5">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <ListTodo className="w-5 h-5" />
                <h3 className={`text-base font-semibold ${colors.text.primary}`}>Project Tracking</h3>
              </div>
              <Button
                size="sm"
                variant="outline"
                onClick={() => window.location.href = '/project-tracking'}
                className={`h-7 text-xs ${
                  theme === 'dark'
                    ? 'border-blue-500/50 text-blue-400 bg-blue-500/10 hover:bg-blue-500/20 hover:border-blue-400'
                    : 'border-blue-400 text-blue-600 bg-blue-50 hover:bg-blue-100'
                }`}
              >
                View All →
              </Button>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className={`text-sm ${colors.text.secondary}`}>In Progress</span>
                <span className={`text-lg font-bold ${colors.text.primary}`}>
                  {isNewCompany ? '0' : '5'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className={`text-sm ${colors.text.secondary}`}>To Do</span>
                <span className={`text-lg font-bold ${colors.text.primary}`}>
                  {isNewCompany ? '0' : '8'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className={`text-sm ${colors.text.secondary}`}>Completed Today</span>
                <span className={`text-lg font-bold text-green-500`}>
                  {isNewCompany ? '0' : '3'}
                </span>
              </div>
            </div>
          </GradientCard>

          {/* Quick Actions */}
          <GradientCard gradient="purple" className="p-5">
            <h3 className={`text-base font-semibold mb-4 ${colors.text.primary}`}>Quick Actions</h3>
            <div className="grid grid-cols-2 gap-3">
              {quickActions.map((action, index) => {
                const Icon = action.icon;
                const colorClasses = getColorClasses(action.color);
                return (
                  <button
                    key={index}
                    className={`${colorClasses.bg} ${colorClasses.border} border rounded-lg p-3 flex flex-col items-center gap-2 hover:scale-105 transition-transform`}
                  >
                    <Icon className={`w-5 h-5 ${colorClasses.text}`} />
                    <span className={`text-xs font-medium ${colorClasses.text}`}>{action.label}</span>
                  </button>
                );
              })}
            </div>
          </GradientCard>

          {/* Recent Activity */}
          <GradientCard gradient="cyan" className="p-5">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Activity className="w-5 h-5" />
                <h3 className={`text-base font-semibold ${colors.text.primary}`}>Recent Activity</h3>
              </div>
            </div>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {recentActivities.map((activity) => {
                const Icon = activity.icon;
                const colorClasses = getColorClasses(activity.color);
                return (
                  <div key={activity.id} className={`${colorClasses.bg} ${colorClasses.border} border rounded-lg p-3`}>
                    <div className="flex items-start gap-3">
                      <div className={`${colorClasses.bg} p-2 rounded-lg`}>
                        <Icon className={`w-4 h-4 ${colorClasses.text}`} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className={`text-sm font-medium ${colors.text.primary} truncate`}>
                          {activity.title}
                        </p>
                        <p className={`text-xs ${colors.text.secondary} mt-1`}>
                          {activity.description}
                        </p>
                        <p className={`text-xs ${colors.text.tertiary} mt-1`}>
                          {activity.time}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </GradientCard>
        </div>

        {/* Main Content Area - 70% width */}
        <div className="flex-1 space-y-6">
          {/* Empty State for New Companies */}
          {isNewCompany && (
            <GradientCard gradient="blue" className="p-6 mb-6">
              <div className="text-center py-8">
                <Building2 className={`w-16 h-16 ${colors.text.tertiary} mx-auto mb-4`} />
                <h2 className={`text-xl font-bold ${colors.text.primary} mb-2`}>
                  Welcome to {selectedCompany?.name}!
                </h2>
                <p className={`${colors.text.secondary} mb-6`}>
                  Get started by adding your first property, investment deal, or setting up your portfolio.
                </p>
                <div className="flex gap-3 justify-center">
                  <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                    <Plus className="w-4 h-4 mr-2" />
                    Add Property
                  </Button>
                  <Button variant="outline">
                    <Briefcase className="w-4 h-4 mr-2" />
                    New Deal
                  </Button>
                </div>
              </div>
            </GradientCard>
          )}

          {/* Section Summaries */}
          <div className="grid grid-cols-2 gap-6">
            {sectionSummaries.map((section, index) => {
              const Icon = section.icon;
              const colorClasses = getColorClasses(section.color);
              return (
                <GradientCard key={index} gradient={section.color as any} className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className={`w-12 h-12 bg-gradient-to-br ${colorClasses.gradient} rounded-lg flex items-center justify-center`}>
                        <Icon className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <h3 className={`text-lg font-semibold ${colors.text.primary}`}>{section.section}</h3>
                        <div className="flex items-center gap-2 mt-1">
                          {section.alerts > 0 && (
                            <div className={`flex items-center gap-1 text-xs ${theme === 'dark' ? 'text-amber-400' : 'text-amber-600'}`}>
                              <AlertCircle className="w-3 h-3" />
                              {section.alerts} alerts
                            </div>
                          )}
                          {section.alerts === 0 && (
                            <div className={`flex items-center gap-1 text-xs ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`}>
                              <CheckCircle2 className="w-3 h-3" />
                              All clear
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className={`p-1.5 rounded-lg ${
                      section.trend === 'up'
                        ? theme === 'dark' ? 'bg-green-500/10' : 'bg-green-100'
                        : theme === 'dark' ? 'bg-slate-700/50' : 'bg-slate-100'
                    }`}>
                      <TrendingUp className={`w-4 h-4 ${
                        section.trend === 'up'
                          ? theme === 'dark' ? 'text-green-400' : 'text-green-600'
                          : colors.text.tertiary
                      }`} />
                    </div>
                  </div>
                  <div className="space-y-3">
                    {section.metrics.map((metric, mIndex) => (
                      <div key={mIndex} className="flex items-center justify-between">
                        <span className={`text-sm ${colors.text.secondary}`}>{metric.label}</span>
                        <span className={`text-sm font-semibold ${colors.text.primary}`}>{metric.value}</span>
                      </div>
                    ))}
                  </div>
                </GradientCard>
              );
            })}
          </div>

          {/* Charts Row - Only show if not new company */}
          {!isNewCompany && (
            <div className="grid grid-cols-2 gap-6">
              {/* Revenue Trend */}
              <GradientCard gradient="blue" className="p-6">
                <h3 className={`text-lg font-semibold mb-4 ${colors.text.primary}`}>Revenue & Expenses</h3>
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={revenueData}>
                    <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#e2e8f0'} />
                    <XAxis dataKey="month" stroke={theme === 'dark' ? '#94a3b8' : '#64748b'} />
                    <YAxis stroke={theme === 'dark' ? '#94a3b8' : '#64748b'} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff',
                        border: `1px solid ${theme === 'dark' ? '#334155' : '#e2e8f0'}`,
                        borderRadius: '8px'
                      }}
                    />
                    <Legend />
                    <Bar dataKey="revenue" name="Revenue ($K)" fill="#3b82f6" />
                    <Bar dataKey="expenses" name="Expenses ($K)" fill="#ef4444" />
                    <Bar dataKey="profit" name="Profit ($K)" fill="#10b981" />
                  </BarChart>
                </ResponsiveContainer>
              </GradientCard>

              {/* Portfolio by Asset Type */}
              <GradientCard gradient="purple" className="p-6">
                <h3 className={`text-lg font-semibold mb-4 ${colors.text.primary}`}>Portfolio by Asset Type</h3>
                <div className="space-y-4">
                  {portfolioPerformance.map((asset, index) => (
                    <div key={index}>
                      <div className="flex items-center justify-between mb-2">
                        <span className={`text-sm font-medium ${colors.text.primary}`}>{asset.name}</span>
                        <div className="flex items-center gap-4">
                          <span className={`text-xs ${colors.text.secondary}`}>{asset.count} properties</span>
                          <span className={`text-sm font-semibold ${colors.text.primary}`}>
                            ${(asset.value / 1000000).toFixed(1)}M
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="flex-1 h-2 bg-slate-700/20 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full"
                            style={{ width: `${(asset.value / 47200000) * 100}%` }}
                          />
                        </div>
                        <span className={`text-xs font-medium ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`}>
                          {asset.yield}% yield
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </GradientCard>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
