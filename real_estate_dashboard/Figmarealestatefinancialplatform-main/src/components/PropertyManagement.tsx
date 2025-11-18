import { useState } from 'react';
import { Building2, DoorOpen, TrendingUp, DollarSign, AlertTriangle, AlertCircle, RefreshCw, Plus, LayoutGrid, Wrench, FileText, BarChart, ChevronDown, Calendar, Users } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { BarChart as RechartsBar, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Cell, PieChart, Pie, Tooltip, LineChart, Line, Area, AreaChart } from 'recharts';
import { useTheme } from '../contexts/ThemeContext';

const occupancyData = [
  { name: 'Maple Apts', value: 88, target: 95, color: '#3b82f6' },
  { name: 'Oak Plaza', value: 92, target: 95, color: '#6366f1' },
  { name: 'Pine Tower', value: 95, target: 95, color: '#8b5cf6' },
  { name: 'Cedar Heights', value: 97, target: 95, color: '#a855f7' },
  { name: 'Birch Estates', value: 100, target: 95, color: '#10b981' },
];

const portfolioData = [
  { name: 'Residential', value: 65, color: '#3b82f6' },
  { name: 'Commercial', value: 25, color: '#10b981' },
  { name: 'Mixed-Use', value: 10, color: '#f59e0b' },
];

const revenueData = [
  { month: 'Jan', revenue: 78, expenses: 42 },
  { month: 'Feb', revenue: 82, expenses: 45 },
  { month: 'Mar', revenue: 79, expenses: 43 },
  { month: 'Apr', revenue: 85, expenses: 46 },
  { month: 'May', revenue: 88, expenses: 44 },
  { month: 'Jun', revenue: 92, expenses: 47 },
];

export function PropertyManagement() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const { theme, colors } = useTheme();

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <header className={`sticky top-0 z-20 ${theme === 'dark' ? 'bg-[#0f1419]/80' : 'bg-gradient-to-r from-stone-50 via-stone-100/80 to-amber-50/60'} backdrop-blur-xl border-b ${theme === 'dark' ? colors.border.primary : 'border-stone-200/80'}`}>
        <div className="px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <h1 className={`text-3xl ${theme === 'dark' ? colors.text.primary : 'text-slate-800'}`}>Portfolio Management</h1>
                <div className={`px-3 py-1.5 ${theme === 'dark' ? 'bg-green-500/10 border-green-500/20' : 'bg-emerald-50 border-emerald-200'} border rounded-lg`}>
                  <span className={`text-xs ${theme === 'dark' ? 'text-green-400' : 'text-emerald-700'}`}>12 Active</span>
                </div>
              </div>
              <p className={`text-sm ${theme === 'dark' ? colors.text.secondary : 'text-slate-600'}`}>Real-time portfolio tracking & performance analytics</p>
            </div>
            <div className="flex items-center gap-3">
              <select className={`text-sm ${theme === 'dark' ? 'bg-slate-800/50 border-slate-700/50 text-white' : 'bg-white border-stone-300 text-slate-700'} border rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 ${theme === 'dark' ? 'focus:ring-emerald-500/50' : 'focus:ring-emerald-400/50'} backdrop-blur-sm shadow-sm`}>
                <option>All Companies</option>
                <option>ABC Properties LLC</option>
                <option>XYZ Real Estate</option>
              </select>
              <Button variant="outline" size="sm" className={`${theme === 'dark' ? 'border-slate-700/50 hover:bg-slate-800/50 text-white' : 'border-stone-300 hover:bg-stone-50 text-slate-700'} shadow-sm`}>
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </Button>
              <Button size="sm" className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 shadow-lg shadow-emerald-500/30 text-white">
                <Plus className="w-4 h-4 mr-2" />
                Add Property
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className={`flex-1 overflow-auto ${theme === 'dark' ? '' : 'bg-stone-50/30'} p-8`}>
        {/* Metrics Cards */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          <Card className={`p-6 ${theme === 'dark' ? colors.card + ' border-slate-700/50' : 'bg-white/80 border-stone-200'} border ${theme === 'light' ? 'shadow-sm hover:shadow-md' : ''} relative overflow-hidden group transition-all`}>
            <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-br from-blue-600/5 to-transparent' : 'bg-gradient-to-br from-teal-50/50 to-transparent'}`} />
            <div className={`absolute top-0 right-0 w-32 h-32 ${theme === 'dark' ? 'bg-blue-500/10' : 'bg-teal-100/30'} rounded-full blur-2xl`} />
            <div className="relative">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-12 h-12 ${theme === 'dark' ? 'bg-gradient-to-br from-blue-500/20 to-blue-600/20 border-blue-500/20' : 'bg-gradient-to-br from-teal-100 to-teal-200 border-teal-300'} rounded-xl flex items-center justify-center border shadow-sm`}>
                  <Building2 className={`w-6 h-6 ${theme === 'dark' ? 'text-blue-400' : 'text-teal-600'}`} />
                </div>
                <div className={`text-xs px-2.5 py-1 ${theme === 'dark' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 'bg-teal-50 text-teal-700 border-teal-200'} rounded-md border`}>
                  Portfolio
                </div>
              </div>
              <div className={`text-sm ${theme === 'dark' ? colors.text.secondary : 'text-slate-500'} mb-2`}>Total Properties</div>
              <div className={`text-4xl ${theme === 'dark' ? colors.text.primary : 'text-slate-800'} mb-2`}>12</div>
              <div className="flex items-center gap-2 text-xs">
                <span className={`${theme === 'dark' ? 'text-green-400' : 'text-emerald-600'} flex items-center gap-1`}>
                  <TrendingUp className="w-3 h-3" />
                  +2 YTD
                </span>
                <span className={theme === 'dark' ? colors.text.tertiary : 'text-slate-400'}>Active portfolios</span>
              </div>
            </div>
          </Card>

          <Card className={`p-6 ${theme === 'dark' ? colors.card + ' border-slate-700/50' : 'bg-white/80 border-stone-200'} border ${theme === 'light' ? 'shadow-sm hover:shadow-md' : ''} relative overflow-hidden group transition-all`}>
            <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-br from-green-600/5 to-transparent' : 'bg-gradient-to-br from-emerald-50/50 to-transparent'}`} />
            <div className={`absolute top-0 right-0 w-32 h-32 ${theme === 'dark' ? 'bg-green-500/10' : 'bg-emerald-100/30'} rounded-full blur-2xl`} />
            <div className="relative">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-12 h-12 ${theme === 'dark' ? 'bg-gradient-to-br from-green-500/20 to-green-600/20 border-green-500/20' : 'bg-gradient-to-br from-emerald-100 to-emerald-200 border-emerald-300'} rounded-xl flex items-center justify-center border shadow-sm`}>
                  <DoorOpen className={`w-6 h-6 ${theme === 'dark' ? 'text-green-400' : 'text-emerald-600'}`} />
                </div>
                <div className={`text-xs px-2.5 py-1 ${theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-emerald-50 text-emerald-700 border-emerald-200'} rounded-md border`}>
                  Units
                </div>
              </div>
              <div className={`text-sm ${theme === 'dark' ? colors.text.secondary : 'text-slate-500'} mb-2`}>Total Units</div>
              <div className={`text-4xl ${theme === 'dark' ? colors.text.primary : 'text-slate-800'} mb-2`}>148</div>
              <div className="flex items-center gap-2 text-xs">
                <span className={`${theme === 'dark' ? 'text-green-400' : 'text-emerald-600'} flex items-center gap-1`}>
                  <TrendingUp className="w-3 h-3" />
                  +12 this quarter
                </span>
              </div>
            </div>
          </Card>

          <Card className={`p-6 ${theme === 'dark' ? colors.card + ' border-slate-700/50' : 'bg-white/80 border-stone-200'} border ${theme === 'light' ? 'shadow-sm hover:shadow-md' : ''} relative overflow-hidden group transition-all`}>
            <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-br from-purple-600/5 to-transparent' : 'bg-gradient-to-br from-violet-50 to-transparent'}`} />
            <div className={`absolute top-0 right-0 w-32 h-32 ${theme === 'dark' ? 'bg-purple-500/10' : 'bg-violet-100/50'} rounded-full blur-2xl`} />
            <div className="relative">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-12 h-12 ${theme === 'dark' ? 'bg-gradient-to-br from-purple-500/20 to-purple-600/20 border-purple-500/20' : 'bg-gradient-to-br from-violet-100 to-violet-200 border-violet-300'} rounded-xl flex items-center justify-center border shadow-sm`}>
                  <TrendingUp className={`w-6 h-6 ${theme === 'dark' ? 'text-purple-400' : 'text-violet-600'}`} />
                </div>
                <div className={`text-xs px-2.5 py-1 ${theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-emerald-50 text-emerald-700 border-emerald-200'} rounded-md border`}>
                  +2.3%
                </div>
              </div>
              <div className={`text-sm ${theme === 'dark' ? colors.text.secondary : 'text-slate-500'} mb-2`}>Occupancy Rate</div>
              <div className={`text-4xl ${theme === 'dark' ? colors.text.primary : 'text-slate-800'} mb-2`}>94.6%</div>
              <div className="flex items-center gap-2 text-xs">
                <span className={theme === 'dark' ? colors.text.tertiary : 'text-slate-400'}>140 of 148 occupied</span>
              </div>
            </div>
          </Card>

          <Card className={`p-6 ${theme === 'dark' ? colors.card + ' border-slate-700/50' : 'bg-white/80 border-stone-200'} border ${theme === 'light' ? 'shadow-sm hover:shadow-md' : ''} relative overflow-hidden group transition-all`}>
            <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-br from-emerald-600/5 to-transparent' : 'bg-gradient-to-br from-lime-50 to-transparent'}`} />
            <div className={`absolute top-0 right-0 w-32 h-32 ${theme === 'dark' ? 'bg-emerald-500/10' : 'bg-lime-100/50'} rounded-full blur-2xl`} />
            <div className="relative">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-12 h-12 ${theme === 'dark' ? 'bg-gradient-to-br from-emerald-500/20 to-emerald-600/20 border-emerald-500/20' : 'bg-gradient-to-br from-lime-100 to-lime-200 border-lime-300'} rounded-xl flex items-center justify-center border shadow-sm`}>
                  <DollarSign className={`w-6 h-6 ${theme === 'dark' ? 'text-emerald-400' : 'text-lime-600'}`} />
                </div>
                <div className={`text-xs px-2.5 py-1 ${theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-emerald-50 text-emerald-700 border-emerald-200'} rounded-md border`}>
                  +3.2%
                </div>
              </div>
              <div className={`text-sm ${theme === 'dark' ? colors.text.secondary : 'text-slate-500'} mb-2`}>Monthly NOI</div>
              <div className={`text-4xl ${theme === 'dark' ? colors.text.primary : 'text-slate-800'} mb-2`}>$85.2K</div>
              <div className="flex items-center gap-2 text-xs">
                <span className={theme === 'dark' ? colors.text.tertiary : 'text-slate-400'}>Annual: $1.02M</span>
              </div>
            </div>
          </Card>
        </div>

        {/* Alert Banners */}
        <div className="grid grid-cols-2 gap-6 mb-8">
          <div className={`${theme === 'dark' ? 'bg-gradient-to-r from-orange-900/20 to-orange-800/20 border-orange-700/30' : 'bg-gradient-to-r from-orange-50 to-amber-50 border-orange-200'} border rounded-2xl p-6 flex items-start gap-4 ${theme === 'light' ? 'shadow-sm' : 'backdrop-blur-sm'}`}>
            <div className={`w-12 h-12 ${theme === 'dark' ? 'bg-orange-500/20 border-orange-500/30' : 'bg-orange-200/60 border-orange-300'} rounded-xl flex items-center justify-center flex-shrink-0 border`}>
              <AlertTriangle className={`w-6 h-6 ${theme === 'dark' ? 'text-orange-400' : 'text-orange-600'}`} />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <div className={`${theme === 'dark' ? 'text-white' : 'text-slate-800'}`}>Leases Expiring Soon</div>
                <div className={`px-2.5 py-0.5 ${theme === 'dark' ? 'bg-orange-500/20 text-orange-400 border-orange-500/30' : 'bg-orange-200 text-orange-800 border-orange-300'} text-xs rounded-md border`}>
                  3 Units
                </div>
              </div>
              <div className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'} mb-3`}>
                Contact tenants for renewal: Unit 2A (Maple), Unit 5B (Oak), Unit 12C (Pine)
              </div>
              <button className={`text-sm ${theme === 'dark' ? 'text-orange-400 hover:text-orange-300' : 'text-orange-700 hover:text-orange-600'} flex items-center gap-1`}>
                View Details
                <ChevronDown className="w-3 h-3" />
              </button>
            </div>
          </div>

          <div className={`${theme === 'dark' ? 'bg-gradient-to-r from-red-900/20 to-red-800/20 border-red-700/30' : 'bg-gradient-to-r from-rose-50 to-pink-50 border-rose-200'} border rounded-2xl p-6 flex items-start gap-4 ${theme === 'light' ? 'shadow-sm' : 'backdrop-blur-sm'}`}>
            <div className={`w-12 h-12 ${theme === 'dark' ? 'bg-red-500/20 border-red-500/30' : 'bg-rose-200/60 border-rose-300'} rounded-xl flex items-center justify-center flex-shrink-0 border`}>
              <AlertCircle className={`w-6 h-6 ${theme === 'dark' ? 'text-red-400' : 'text-rose-600'}`} />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <div className={`${theme === 'dark' ? 'text-white' : 'text-slate-800'}`}>Emergency Maintenance</div>
                <div className={`px-2.5 py-0.5 ${theme === 'dark' ? 'bg-red-500/20 text-red-400 border-red-500/30' : 'bg-rose-200 text-rose-800 border-rose-300'} text-xs rounded-md border`}>
                  Urgent
                </div>
              </div>
              <div className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'} mb-3`}>
                2 emergency requests require immediate attention. All assigned to vendors.
              </div>
              <button className={`text-sm ${theme === 'dark' ? 'text-red-400 hover:text-red-300' : 'text-rose-700 hover:text-rose-600'} flex items-center gap-1`}>
                Take Action
                <ChevronDown className="w-3 h-3" />
              </button>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className={`${theme === 'dark' ? 'bg-gradient-to-br from-slate-800/40 to-slate-900/40 border-slate-700/50 backdrop-blur-sm' : 'bg-white/80 border-stone-200 shadow-sm'} rounded-2xl border`}>
          <div className={`border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-stone-200'} px-6 py-4`}>
            <div className="flex gap-6">
              {[
                { id: 'dashboard', label: 'Dashboard', icon: LayoutGrid },
                { id: 'properties', label: 'Properties', icon: Building2 },
                { id: 'units', label: 'Units', icon: DoorOpen },
                { id: 'leases', label: 'Leases', icon: FileText },
                { id: 'maintenance', label: 'Maintenance', icon: Wrench },
                { id: 'roi', label: 'ROI Analysis', icon: BarChart },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2.5 border-b-2 transition-all relative ${
                    activeTab === tab.id
                      ? `${theme === 'dark' ? 'border-blue-500 text-blue-400' : 'border-teal-600 text-teal-700'}`
                      : `border-transparent ${theme === 'dark' ? 'text-slate-400 hover:text-white' : 'text-slate-500 hover:text-slate-700'}`
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  <span className="text-sm">{tab.label}</span>
                  {activeTab === tab.id && (
                    <div className={`absolute bottom-0 left-0 right-0 h-0.5 ${theme === 'dark' ? 'bg-gradient-to-r from-blue-500 to-blue-600' : 'bg-gradient-to-r from-teal-600 to-emerald-600'}`} />
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Dashboard Content */}
          <div className="p-6">
            <div className="grid grid-cols-3 gap-6">
              {/* Occupancy Chart */}
              <Card className={`col-span-2 p-6 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50' : 'bg-slate-50/50 border-stone-200 shadow-sm'}`}>
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-800'} mb-1`}>Occupancy by Property</h3>
                    <p className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>Current vs Target Occupancy</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className={`flex items-center gap-1.5 px-3 py-1.5 ${theme === 'dark' ? 'bg-blue-500/10 border-blue-500/20' : 'bg-blue-100 border-blue-300'} rounded-lg border`}>
                      <div className={`w-2 h-2 ${theme === 'dark' ? 'bg-blue-500' : 'bg-blue-600'} rounded-full`} />
                      <span className={`text-xs ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>Current</span>
                    </div>
                    <div className={`flex items-center gap-1.5 px-3 py-1.5 ${theme === 'dark' ? 'bg-slate-700/30 border-slate-600/30' : 'bg-slate-200 border-slate-300'} rounded-lg border`}>
                      <div className={`w-2 h-2 ${theme === 'dark' ? 'bg-slate-500' : 'bg-slate-600'} rounded-full`} />
                      <span className={`text-xs ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>Target</span>
                    </div>
                  </div>
                </div>
                <ResponsiveContainer width="100%" height={320}>
                  <RechartsBar data={occupancyData} barSize={50}>
                    <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#cbd5e1'} opacity={0.2} vertical={false} />
                    <XAxis dataKey="name" tick={{ fontSize: 12, fill: theme === 'dark' ? '#94a3b8' : '#475569' }} />
                    <YAxis domain={[0, 100]} tick={{ fontSize: 12, fill: theme === 'dark' ? '#94a3b8' : '#475569' }} />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff', 
                        border: theme === 'dark' ? '1px solid #334155' : '1px solid #cbd5e1',
                        borderRadius: '12px',
                        color: theme === 'dark' ? '#fff' : '#0f172a'
                      }}
                      labelStyle={{ color: theme === 'dark' ? '#fff' : '#0f172a' }}
                    />
                    <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                      {occupancyData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </RechartsBar>
                </ResponsiveContainer>
              </Card>

              {/* Revenue Chart */}
              <Card className={`p-6 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50' : 'bg-slate-50/50 border-stone-200 shadow-sm'}`}>
                <div className="mb-6">
                  <h3 className={`text-lg ${theme === 'dark' ? 'text-white' : 'text-slate-800'} mb-1`}>Revenue vs Expenses</h3>
                  <p className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>6-month trend (in $K)</p>
                </div>
                <ResponsiveContainer width="100%" height={320}>
                  <AreaChart data={revenueData}>
                    <defs>
                      <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={theme === 'dark' ? 0.3 : 0.2}/>
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorExpenses" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#ef4444" stopOpacity={theme === 'dark' ? 0.3 : 0.2}/>
                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#cbd5e1'} opacity={0.2} />
                    <XAxis dataKey="month" stroke={theme === 'dark' ? '#94a3b8' : '#475569'} fontSize={12} />
                    <YAxis stroke={theme === 'dark' ? '#94a3b8' : '#475569'} fontSize={12} />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff', 
                        border: theme === 'dark' ? '1px solid #334155' : '1px solid #cbd5e1',
                        borderRadius: '12px',
                        color: theme === 'dark' ? '#fff' : '#0f172a'
                      }}
                    />
                    <Area type="monotone" dataKey="revenue" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#colorRevenue)" />
                    <Area type="monotone" dataKey="expenses" stroke="#ef4444" strokeWidth={2} fillOpacity={1} fill="url(#colorExpenses)" />
                  </AreaChart>
                </ResponsiveContainer>
              </Card>

              {/* Portfolio Metrics */}
              {[
                { label: 'Portfolio Value', value: '$18.5M', change: '+5.2%', positive: true, icon: Building2, color: 'blue' },
                { label: 'Total Equity', value: '$4.6M', subtitle: '25% LTV Ratio', icon: DollarSign, color: 'green' },
                { label: 'Portfolio Cap Rate', value: '6.8%', subtitle: 'Above market avg', icon: TrendingUp, color: 'purple' },
                { label: 'Cash-on-Cash', value: '9.4%', change: '+0.3%', positive: true, icon: BarChart, color: 'emerald' },
                { label: 'Avg Rent/Unit', value: '$1,685', change: '+4.1%', positive: true, icon: Users, color: 'orange' },
                { label: 'YTD Collections', value: '98.2%', subtitle: 'On-time payments', icon: Calendar, color: 'cyan' },
              ].map((metric, index) => (
                <Card key={index} className={`p-5 ${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50 hover:border-slate-600/50' : 'bg-white/70 border-stone-200 hover:border-stone-300 shadow-sm hover:shadow'} transition-all group`}>
                  <div className="flex items-start justify-between mb-3">
                    <div className={`w-10 h-10 ${theme === 'dark' ? `bg-${metric.color}-500/10 border-${metric.color}-500/20` : metric.color === 'blue' ? 'bg-blue-100 border-blue-300' : metric.color === 'green' ? 'bg-green-100 border-green-300' : metric.color === 'purple' ? 'bg-purple-100 border-purple-300' : metric.color === 'emerald' ? 'bg-emerald-100 border-emerald-300' : metric.color === 'orange' ? 'bg-orange-100 border-orange-300' : 'bg-cyan-100 border-cyan-300'} rounded-xl flex items-center justify-center border group-hover:scale-110 transition-transform`}>
                      <metric.icon className={`w-5 h-5 ${theme === 'dark' ? `text-${metric.color}-400` : metric.color === 'blue' ? 'text-blue-600' : metric.color === 'green' ? 'text-green-600' : metric.color === 'purple' ? 'text-purple-600' : metric.color === 'emerald' ? 'text-emerald-600' : metric.color === 'orange' ? 'text-orange-600' : 'text-cyan-600'}`} />
                    </div>
                    {metric.change && (
                      <div className={`px-2 py-0.5 ${metric.positive ? (theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300') : (theme === 'dark' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-red-100 text-red-700 border-red-300')} text-xs rounded border flex items-center gap-1`}>
                        <TrendingUp className="w-3 h-3" />
                        {metric.change}
                      </div>
                    )}
                  </div>
                  <div className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} mb-2`}>{metric.label}</div>
                  <div className={`text-2xl ${theme === 'dark' ? 'text-white' : 'text-slate-800'} mb-1`}>{metric.value}</div>
                  {metric.subtitle && (
                    <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-400'}`}>{metric.subtitle}</div>
                  )}
                </Card>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}