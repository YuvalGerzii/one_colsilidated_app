import { useState } from 'react';
import { Home, Building, Building2, Hotel, Blocks, FileText, Wrench, TrendingUp, Zap } from 'lucide-react';
import { Card } from './ui/card';
import { FixFlipCalculator } from './calculators/FixFlipCalculator';
import { SingleFamilyCalculator } from './calculators/SingleFamilyCalculator';
import { SmallMultifamilyCalculator } from './calculators/SmallMultifamilyCalculator';
import { HighRiseCalculator } from './calculators/HighRiseCalculator';
import { HotelCalculator } from './calculators/HotelCalculator';
import { MixedUseCalculator } from './calculators/MixedUseCalculator';
import { LeaseAnalyzer } from './calculators/LeaseAnalyzer';
import { RenovationBudget } from './calculators/RenovationBudget';
import { useTheme } from '../contexts/ThemeContext';

const models = [
  {
    id: 'fix-flip',
    name: 'Fix & Flip',
    description: 'Short-term renovation projects with MAO calculation, 70% rule analysis, and exit strategy modeling',
    icon: Home,
    gradient: 'from-blue-500 via-blue-600 to-blue-700',
    glowColor: 'blue',
    component: FixFlipCalculator,
    metrics: ['ROI', 'MAO', 'Profit Margin'],
  },
  {
    id: 'single-family',
    name: 'Single Family Rental',
    description: 'Long-term rental cash flow analysis with debt service coverage and appreciation projections',
    icon: Home,
    gradient: 'from-green-500 via-green-600 to-green-700',
    glowColor: 'green',
    component: SingleFamilyCalculator,
    metrics: ['Cash Flow', 'Cap Rate', 'CoC Return'],
  },
  {
    id: 'small-multifamily',
    name: 'Small Multifamily',
    description: '2-4 unit property analysis with per-unit economics and DSCR calculations',
    icon: Building,
    gradient: 'from-purple-500 via-purple-600 to-purple-700',
    glowColor: 'purple',
    component: SmallMultifamilyCalculator,
    metrics: ['DSCR', 'NOI', 'Unit Economics'],
  },
  {
    id: 'high-rise',
    name: 'High-Rise Multifamily',
    description: 'Institutional-grade modeling for large apartment complexes with income stratification',
    icon: Building2,
    gradient: 'from-indigo-500 via-indigo-600 to-indigo-700',
    glowColor: 'indigo',
    component: HighRiseCalculator,
    metrics: ['Cap Rate', 'GPI', 'Operating Ratio'],
  },
  {
    id: 'hotel',
    name: 'Hotel & Hospitality',
    description: 'Hospitality financial modeling with RevPAR, ADR, and seasonal variance analysis',
    icon: Hotel,
    gradient: 'from-orange-500 via-orange-600 to-orange-700',
    glowColor: 'orange',
    component: HotelCalculator,
    metrics: ['RevPAR', 'ADR', 'Occupancy'],
  },
  {
    id: 'mixed-use',
    name: 'Mixed-Use Development',
    description: 'Complex developments blending residential, retail, and office with blended metrics',
    icon: Blocks,
    gradient: 'from-teal-500 via-teal-600 to-teal-700',
    glowColor: 'teal',
    component: MixedUseCalculator,
    metrics: ['Blended Cap', 'Income Mix', 'NOI'],
  },
  {
    id: 'lease-analyzer',
    name: 'Lease Analyzer',
    description: 'Side-by-side lease comparison with escalation clauses and total cost analysis',
    icon: FileText,
    gradient: 'from-pink-500 via-pink-600 to-pink-700',
    glowColor: 'pink',
    component: LeaseAnalyzer,
    metrics: ['Total Cost', 'Escalations', 'NPV'],
  },
  {
    id: 'renovation-budget',
    name: 'Renovation Budget',
    description: 'Construction cost estimation with line-item budgeting and contingency planning',
    icon: Wrench,
    gradient: 'from-amber-500 via-amber-600 to-amber-700',
    glowColor: 'amber',
    component: RenovationBudget,
    metrics: ['Total Budget', 'Cost/SF', 'Timeline'],
  },
];

export function RealEstateModels() {
  const [selectedModel, setSelectedModel] = useState<string | null>(null);
  const { theme, colors } = useTheme();

  const activeModel = models.find(m => m.id === selectedModel);
  
  if (activeModel && activeModel.component) {
    const CalculatorComponent = activeModel.component;
    return <CalculatorComponent onBack={() => setSelectedModel(null)} />;
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <header className={`sticky top-0 z-20 ${theme === 'dark' ? 'bg-[#0f1419]/80' : 'bg-gradient-to-r from-indigo-50 to-purple-50/80'} backdrop-blur-xl border-b ${colors.border.primary}`}>
        <div className="px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-1">
                <h1 className={`text-2xl ${colors.text.primary}`}>Financial Models</h1>
                <div className={`px-2.5 py-1 ${theme === 'dark' ? 'bg-blue-500/10 border-blue-500/20' : 'bg-indigo-100 border-indigo-200'} border rounded-lg`}>
                  <span className={`text-xs ${theme === 'dark' ? 'text-blue-400' : 'text-indigo-700'}`}>8 Models</span>
                </div>
              </div>
              <p className={`text-sm ${colors.text.secondary}`}>Institutional-grade financial modeling & analysis tools</p>
            </div>
            <div className="flex items-center gap-3">
              <div className={`px-4 py-2 ${theme === 'dark' ? 'bg-slate-800/50 border-slate-700/50' : 'bg-white border-indigo-200'} border rounded-lg`}>
                <div className={`text-xs ${colors.text.tertiary} mb-0.5`}>Last Updated</div>
                <div className={`text-sm ${colors.text.primary}`}>Nov 7, 2025</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-auto p-8">
        <div className="max-w-[1600px] mx-auto">
          {/* Featured Stats */}
          <div className="grid grid-cols-4 gap-6 mb-8">
            {[
              { label: 'Models Available', value: '8', icon: Zap, color: 'blue' },
              { label: 'Avg Analysis Time', value: '< 5 min', icon: TrendingUp, color: 'green' },
              { label: 'Data Points', value: '150+', icon: Building2, color: 'purple' },
              { label: 'Export Formats', value: '3', icon: FileText, color: 'amber' },
            ].map((stat, index) => (
              <Card key={index} className={`p-5 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center justify-between mb-3">
                  <div className={`w-10 h-10 ${theme === 'dark' ? `bg-${stat.color}-500/10 border-${stat.color}-500/20` : `bg-${stat.color}-100 border-${stat.color}-300`} rounded-xl flex items-center justify-center border`}>
                    <stat.icon className={`w-5 h-5 ${theme === 'dark' ? `text-${stat.color}-400` : `text-${stat.color}-600`}`} />
                  </div>
                </div>
                <div className={`text-sm ${colors.text.secondary} mb-1`}>{stat.label}</div>
                <div className={`text-2xl ${colors.text.primary}`}>{stat.value}</div>
              </Card>
            ))}
          </div>

          {/* Models Grid */}
          <div className="grid grid-cols-2 gap-6">
            {models.map((model) => (
              <Card
                key={model.id}
                className={`p-8 cursor-pointer transition-all hover:scale-[1.02] ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md hover:shadow-xl' : 'hover:border-slate-600/50'} group relative overflow-hidden`}
                onClick={() => setSelectedModel(model.id)}
              >
                {/* Glow effect */}
                <div className={`absolute inset-0 ${theme === 'dark' ? `bg-gradient-to-br from-${model.glowColor}-600/0 to-${model.glowColor}-600/0 group-hover:from-${model.glowColor}-600/5 group-hover:to-transparent` : `bg-gradient-to-br from-${model.glowColor}-50/0 to-${model.glowColor}-50/0 group-hover:from-${model.glowColor}-50 group-hover:to-transparent`} transition-all duration-500`} />
                <div className={`absolute top-0 right-0 w-64 h-64 ${theme === 'dark' ? `bg-${model.glowColor}-500/0 group-hover:bg-${model.glowColor}-500/10` : `bg-${model.glowColor}-100/0 group-hover:bg-${model.glowColor}-100/50`} rounded-full blur-3xl transition-all duration-500 -mr-32 -mt-32`} />
                
                <div className="relative z-10">
                  <div className="flex items-start gap-6 mb-6">
                    <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${model.gradient} flex items-center justify-center shadow-2xl group-hover:scale-110 transition-transform relative`}>
                      <div className="absolute inset-0 bg-gradient-to-t from-white/20 to-transparent rounded-2xl" />
                      <model.icon className="w-8 h-8 text-white relative z-10" />
                    </div>
                    <div className="flex-1">
                      <h3 className={`text-xl ${colors.text.primary} mb-2 group-hover:text-${model.glowColor}-${theme === 'dark' ? '400' : '600'} transition-colors`}>{model.name}</h3>
                      <p className={`text-sm ${colors.text.secondary} leading-relaxed`}>{model.description}</p>
                    </div>
                  </div>

                  {/* Metrics */}
                  <div className="flex items-center gap-2 mb-4">
                    {model.metrics.map((metric) => (
                      <div key={metric} className={`px-3 py-1.5 ${theme === 'dark' ? 'bg-slate-800/50 border-slate-700/50 text-slate-300' : 'bg-slate-100 border-slate-200 text-slate-700'} border rounded-lg text-xs`}>
                        {metric}
                      </div>
                    ))}
                  </div>

                  <div className={`flex items-center justify-between pt-4 border-t ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-200'}`}>
                    <div className={`text-sm ${colors.text.tertiary}`}>Click to open calculator</div>
                    <div className={`${theme === 'dark' ? 'text-blue-400 group-hover:text-blue-300' : 'text-indigo-600 group-hover:text-indigo-500'} flex items-center gap-2 transition-all group-hover:gap-3`}>
                      <span className="text-sm">Launch</span>
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* Info Section */}
          <Card className={`mt-8 p-8 ${theme === 'dark' ? 'bg-gradient-to-br from-blue-900/20 to-blue-800/20 border-blue-700/30' : 'bg-gradient-to-br from-indigo-50 to-purple-50 border-indigo-200'} ${theme === 'light' ? 'shadow-md' : ''}`}>
            <div className="flex items-start gap-6">
              <div className={`w-14 h-14 ${theme === 'dark' ? 'bg-blue-500/20 border-blue-500/30' : 'bg-indigo-200 border-indigo-300'} rounded-2xl flex items-center justify-center border`}>
                <Building2 className={`w-7 h-7 ${theme === 'dark' ? 'text-blue-400' : 'text-indigo-600'}`} />
              </div>
              <div className="flex-1">
                <h3 className={`text-xl ${colors.text.primary} mb-2`}>Professional Real Estate Analysis</h3>
                <p className={`${colors.text.secondary} leading-relaxed mb-4`}>
                  Our financial models are built on institutional-grade frameworks used by commercial real estate firms, 
                  private equity funds, and REITs. Each calculator provides comprehensive analysis with industry-standard 
                  metrics and assumptions.
                </p>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div className={`flex items-center gap-2 ${colors.text.secondary}`}>
                    <div className={`w-1.5 h-1.5 ${theme === 'dark' ? 'bg-green-400' : 'bg-green-600'} rounded-full`} />
                    Real-time calculations
                  </div>
                  <div className={`flex items-center gap-2 ${colors.text.secondary}`}>
                    <div className={`w-1.5 h-1.5 ${theme === 'dark' ? 'bg-green-400' : 'bg-green-600'} rounded-full`} />
                    Multiple scenarios
                  </div>
                  <div className={`flex items-center gap-2 ${colors.text.secondary}`}>
                    <div className={`w-1.5 h-1.5 ${theme === 'dark' ? 'bg-green-400' : 'bg-green-600'} rounded-full`} />
                    Export capabilities
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}