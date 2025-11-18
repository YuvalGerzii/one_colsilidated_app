import { Button } from './ui/button';
import { Card } from './ui/card';
import { Building2, Calculator, BarChart3, TrendingUp, ArrowRight, DollarSign, Activity, Zap, Shield } from 'lucide-react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip } from 'recharts';
import { useTheme } from '../contexts/ThemeContext';

interface DashboardProps {
  onNavigate: (view: 'home' | 'property' | 'models') => void;
}

const performanceData = [
  { month: 'Jan', value: 85, portfolio: 92 },
  { month: 'Feb', value: 88, portfolio: 94 },
  { month: 'Mar', value: 92, portfolio: 96 },
  { month: 'Apr', value: 87, portfolio: 93 },
  { month: 'May', value: 95, portfolio: 98 },
  { month: 'Jun', value: 98, portfolio: 100 },
];

const marketData = [
  { month: 'Jan', value: 320000 },
  { month: 'Feb', value: 335000 },
  { month: 'Mar', value: 342000 },
  { month: 'Apr', value: 355000 },
  { month: 'May', value: 368000 },
  { month: 'Jun', value: 380000 },
];

export function Dashboard({ onNavigate }: DashboardProps) {
  const { theme, colors } = useTheme();
  
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className={`sticky top-0 z-20 ${theme === 'dark' ? 'bg-[#0f1419]/80' : 'bg-gradient-to-r from-slate-50 via-blue-50/80 to-cyan-50/60'} backdrop-blur-xl border-b ${theme === 'dark' ? colors.border.primary : 'border-blue-200/80'}`}>
        <div className="px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <h1 className={`text-3xl ${theme === 'dark' ? colors.text.primary : 'text-slate-800'}`}>Dashboard</h1>
                <div className={`px-3 py-1.5 ${theme === 'dark' ? 'bg-green-500/10 border-green-500/20' : 'bg-green-50 border-green-200'} border rounded-lg`}>
                  <span className={`text-xs ${theme === 'dark' ? 'text-green-400' : 'text-green-700'}`}>Live</span>
                </div>
              </div>
              <p className={`text-sm ${theme === 'dark' ? colors.text.secondary : 'text-slate-600'}`}>Real-time analytics & portfolio insights</p>
            </div>
            <div className="flex items-center gap-3">
              <select className={`text-sm ${theme === 'dark' ? 'bg-slate-800/50 border-slate-700/50 text-white' : 'bg-white border-blue-300 text-slate-700'} border rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500/50 backdrop-blur-sm shadow-sm`}>
                <option>All Companies</option>
                <option>ABC Properties LLC</option>
                <option>XYZ Real Estate</option>
              </select>
              <div className={`text-sm ${theme === 'dark' ? colors.text.secondary : 'text-slate-600'} px-4 py-2.5 ${theme === 'dark' ? 'bg-slate-800/30 border-slate-700/50' : 'bg-white border-blue-300'} rounded-lg border shadow-sm`}>
                {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className={`p-8 ${theme === 'light' ? 'bg-slate-50/30' : ''}`}>
        {/* Hero Stats */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md hover:shadow-lg' : 'backdrop-blur-sm'} relative overflow-hidden group hover:border-blue-500/50 transition-all`}>
            <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-br from-blue-600/10 to-transparent' : 'bg-gradient-to-br from-blue-50 to-transparent'} opacity-0 group-hover:opacity-100 transition-opacity`} />
            <div className={`absolute top-0 right-0 w-32 h-32 ${theme === 'dark' ? 'bg-blue-500/5' : 'bg-blue-100/50'} rounded-full -mr-16 -mt-16`} />
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-11 h-11 ${theme === 'dark' ? 'bg-gradient-to-br from-blue-500/20 to-blue-600/20 border-blue-500/20' : 'bg-gradient-to-br from-blue-100 to-blue-200 border-blue-300'} rounded-xl flex items-center justify-center border`}>
                  <Building2 className={`w-5 h-5 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
                </div>
                <div className={`flex items-center gap-1 text-xs px-2 py-1 ${theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'} rounded-md border`}>
                  <TrendingUp className="w-3 h-3" />
                  <span>+12%</span>
                </div>
              </div>
              <div className={`text-sm ${colors.text.secondary} mb-2`}>Total Portfolio Value</div>
              <div className={`text-3xl ${colors.text.primary} mb-1`}>$18.5M</div>
              <div className={`text-xs ${colors.text.tertiary}`}>Across 12 properties</div>
            </div>
          </Card>

          <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md hover:shadow-lg' : 'backdrop-blur-sm'} relative overflow-hidden group hover:border-green-500/50 transition-all`}>
            <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-br from-green-600/10 to-transparent' : 'bg-gradient-to-br from-green-50 to-transparent'} opacity-0 group-hover:opacity-100 transition-opacity`} />
            <div className={`absolute top-0 right-0 w-32 h-32 ${theme === 'dark' ? 'bg-green-500/5' : 'bg-green-100/50'} rounded-full -mr-16 -mt-16`} />
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-11 h-11 ${theme === 'dark' ? 'bg-gradient-to-br from-green-500/20 to-green-600/20 border-green-500/20' : 'bg-gradient-to-br from-green-100 to-green-200 border-green-300'} rounded-xl flex items-center justify-center border`}>
                  <DollarSign className={`w-5 h-5 ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`} />
                </div>
                <div className={`flex items-center gap-1 text-xs px-2 py-1 ${theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'} rounded-md border`}>
                  <TrendingUp className="w-3 h-3" />
                  <span>+8.2%</span>
                </div>
              </div>
              <div className={`text-sm ${colors.text.secondary} mb-2`}>Annual NOI</div>
              <div className={`text-3xl ${colors.text.primary} mb-1`}>$1.02M</div>
              <div className={`text-xs ${colors.text.tertiary}`}>Monthly: $85.2K</div>
            </div>
          </Card>

          <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md hover:shadow-lg' : 'backdrop-blur-sm'} relative overflow-hidden group hover:border-purple-500/50 transition-all`}>
            <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-br from-purple-600/10 to-transparent' : 'bg-gradient-to-br from-purple-50 to-transparent'} opacity-0 group-hover:opacity-100 transition-opacity`} />
            <div className={`absolute top-0 right-0 w-32 h-32 ${theme === 'dark' ? 'bg-purple-500/5' : 'bg-purple-100/50'} rounded-full -mr-16 -mt-16`} />
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-11 h-11 ${theme === 'dark' ? 'bg-gradient-to-br from-purple-500/20 to-purple-600/20 border-purple-500/20' : 'bg-gradient-to-br from-purple-100 to-purple-200 border-purple-300'} rounded-xl flex items-center justify-center border`}>
                  <Activity className={`w-5 h-5 ${theme === 'dark' ? 'text-purple-400' : 'text-purple-600'}`} />
                </div>
                <div className={`flex items-center gap-1 text-xs px-2 py-1 ${theme === 'dark' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-green-100 text-green-700 border-green-300'} rounded-md border`}>
                  <TrendingUp className="w-3 h-3" />
                  <span>+2.3%</span>
                </div>
              </div>
              <div className={`text-sm ${colors.text.secondary} mb-2`}>Occupancy Rate</div>
              <div className={`text-3xl ${colors.text.primary} mb-1`}>94.6%</div>
              <div className={`text-xs ${colors.text.tertiary}`}>140 of 148 units</div>
            </div>
          </Card>

          <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md hover:shadow-lg' : 'backdrop-blur-sm'} relative overflow-hidden group hover:border-amber-500/50 transition-all`}>
            <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-br from-amber-600/10 to-transparent' : 'bg-gradient-to-br from-amber-50 to-transparent'} opacity-0 group-hover:opacity-100 transition-opacity`} />
            <div className={`absolute top-0 right-0 w-32 h-32 ${theme === 'dark' ? 'bg-amber-500/5' : 'bg-amber-100/50'} rounded-full -mr-16 -mt-16`} />
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-11 h-11 ${theme === 'dark' ? 'bg-gradient-to-br from-amber-500/20 to-amber-600/20 border-amber-500/20' : 'bg-gradient-to-br from-amber-100 to-amber-200 border-amber-300'} rounded-xl flex items-center justify-center border`}>
                  <BarChart3 className={`w-5 h-5 ${theme === 'dark' ? 'text-amber-400' : 'text-amber-600'}`} />
                </div>
                <div className={`text-xs px-2 py-1 ${theme === 'dark' ? 'bg-slate-700/50 text-slate-400 border-slate-600/50' : 'bg-slate-100 text-slate-500 border-slate-300'} rounded-md border`}>
                  <span>6.8%</span>
                </div>
              </div>
              <div className={`text-sm ${colors.text.secondary} mb-2`}>Portfolio Cap Rate</div>
              <div className={`text-3xl ${colors.text.primary} mb-1`}>6.8%</div>
              <div className={`text-xs ${colors.text.tertiary}`}>Above market average</div>
            </div>
          </Card>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-3 gap-6 mb-8">
          <Card className={`col-span-2 p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className={`text-lg ${colors.text.primary} mb-1`}>Portfolio Performance</h3>
                <p className={`text-sm ${colors.text.secondary}`}>6-month trend analysis</p>
              </div>
              <div className="flex items-center gap-2">
                <button className={`px-3 py-1.5 text-xs ${theme === 'dark' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 'bg-blue-100 text-blue-700 border-blue-300'} rounded-lg border`}>
                  6M
                </button>
                <button className={`px-3 py-1.5 text-xs ${colors.text.secondary} hover:${colors.text.primary} rounded-lg`}>
                  1Y
                </button>
                <button className={`px-3 py-1.5 text-xs ${colors.text.secondary} hover:${colors.text.primary} rounded-lg`}>
                  All
                </button>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart data={performanceData}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorPortfolio" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#cbd5e1'} opacity={0.3} />
                <XAxis dataKey="month" stroke={theme === 'dark' ? '#64748b' : '#475569'} fontSize={12} />
                <YAxis stroke={theme === 'dark' ? '#64748b' : '#475569'} fontSize={12} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff', 
                    border: theme === 'dark' ? '1px solid #334155' : '1px solid #cbd5e1',
                    borderRadius: '12px',
                    color: theme === 'dark' ? '#fff' : '#0f172a'
                  }}
                />
                <Area type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorValue)" />
                <Area type="monotone" dataKey="portfolio" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#colorPortfolio)" />
              </AreaChart>
            </ResponsiveContainer>
          </Card>

          <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
            <h3 className={`text-lg ${colors.text.primary} mb-6`}>Quick Actions</h3>
            <div className="space-y-3">
              <button
                onClick={() => onNavigate('property')}
                className={`w-full p-4 ${theme === 'dark' ? 'bg-gradient-to-r from-blue-600/10 to-blue-500/10 hover:from-blue-600/20 hover:to-blue-500/20 border-blue-500/20 hover:border-blue-500/40' : 'bg-blue-50 hover:bg-blue-100 border-blue-200 hover:border-blue-300'} rounded-xl border transition-all text-left group`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 ${theme === 'dark' ? 'bg-blue-500/20' : 'bg-blue-200'} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform`}>
                    <Building2 className={`w-5 h-5 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
                  </div>
                  <div className="flex-1">
                    <div className={`${colors.text.primary} text-sm mb-0.5`}>Portfolio Manager</div>
                    <div className={`text-xs ${colors.text.tertiary}`}>View all properties</div>
                  </div>
                  <ArrowRight className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-500 group-hover:text-blue-400' : 'text-slate-400 group-hover:text-blue-600'} transition-colors`} />
                </div>
              </button>

              <button
                onClick={() => onNavigate('models')}
                className={`w-full p-4 ${theme === 'dark' ? 'bg-gradient-to-r from-green-600/10 to-green-500/10 hover:from-green-600/20 hover:to-green-500/20 border-green-500/20 hover:border-green-500/40' : 'bg-green-50 hover:bg-green-100 border-green-200 hover:border-green-300'} rounded-xl border transition-all text-left group`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 ${theme === 'dark' ? 'bg-green-500/20' : 'bg-green-200'} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform`}>
                    <Calculator className={`w-5 h-5 ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`} />
                  </div>
                  <div className="flex-1">
                    <div className={`${colors.text.primary} text-sm mb-0.5`}>Financial Models</div>
                    <div className={`text-xs ${colors.text.tertiary}`}>Run analysis</div>
                  </div>
                  <ArrowRight className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-500 group-hover:text-green-400' : 'text-slate-400 group-hover:text-green-600'} transition-colors`} />
                </div>
              </button>

              <button className={`w-full p-4 ${theme === 'dark' ? 'bg-gradient-to-r from-purple-600/10 to-purple-500/10 hover:from-purple-600/20 hover:to-purple-500/20 border-purple-500/20 hover:border-purple-500/40' : 'bg-purple-50 hover:bg-purple-100 border-purple-200 hover:border-purple-300'} rounded-xl border transition-all text-left group`}>
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 ${theme === 'dark' ? 'bg-purple-500/20' : 'bg-purple-200'} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform`}>
                    <BarChart3 className={`w-5 h-5 ${theme === 'dark' ? 'text-purple-400' : 'text-purple-600'}`} />
                  </div>
                  <div className="flex-1">
                    <div className={`${colors.text.primary} text-sm mb-0.5`}>Market Analysis</div>
                    <div className={`text-xs ${colors.text.tertiary}`}>View trends</div>
                  </div>
                  <ArrowRight className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-500 group-hover:text-purple-400' : 'text-slate-400 group-hover:text-purple-600'} transition-colors`} />
                </div>
              </button>
            </div>
          </Card>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-4 gap-6">
          {[
            {
              icon: Shield,
              title: 'Risk Analysis',
              description: 'Advanced risk modeling and scenario planning',
              color: 'red',
            },
            {
              icon: Zap,
              title: 'Real-Time Pricing',
              description: 'Live market data and property valuations',
              color: 'yellow',
            },
            {
              icon: Activity,
              title: 'Performance Tracking',
              description: 'Monitor KPIs and investment returns',
              color: 'cyan',
            },
            {
              icon: TrendingUp,
              title: 'Market Insights',
              description: 'Data-driven investment recommendations',
              color: 'emerald',
            },
          ].map((feature, index) => (
            <Card key={index} className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md hover:shadow-lg' : ''} transition-all group cursor-pointer`}>
              <div className={`w-12 h-12 ${theme === 'dark' ? `bg-gradient-to-br from-${feature.color}-500/20 to-${feature.color}-600/20 border-${feature.color}-500/20` : `bg-gradient-to-br from-${feature.color}-100 to-${feature.color}-200 border-${feature.color}-300`} rounded-xl flex items-center justify-center border mb-4 group-hover:scale-110 transition-transform`}>
                <feature.icon className={`w-6 h-6 ${theme === 'dark' ? `text-${feature.color}-400` : `text-${feature.color}-600`}`} />
              </div>
              <h3 className={`${colors.text.primary} mb-2`}>{feature.title}</h3>
              <p className={`text-sm ${colors.text.secondary} leading-relaxed`}>{feature.description}</p>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}