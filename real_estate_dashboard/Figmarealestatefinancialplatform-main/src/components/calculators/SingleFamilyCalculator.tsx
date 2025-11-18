import { useState, useEffect } from 'react';
import { Home, TrendingUp, DollarSign, Percent, Users, Calendar } from 'lucide-react';
import { CalculatorLayout } from './CalculatorLayout';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip, BarChart, Bar } from 'recharts';
import { useTheme } from '../../contexts/ThemeContext';

interface Inputs {
  purchasePrice: number;
  downPayment: number;
  interestRate: number;
  loanTerm: number;
  monthlyRent: number;
  vacancyRate: number;
  propertyTax: number;
  insurance: number;
  hoa: number;
  maintenance: number;
  propertyManagement: number;
}

export function SingleFamilyCalculator({ onBack }: { onBack: () => void }) {
  const { theme, colors } = useTheme();
  const [inputs, setInputs] = useState<Inputs>({
    purchasePrice: 300000,
    downPayment: 20,
    interestRate: 6.5,
    loanTerm: 30,
    monthlyRent: 2500,
    vacancyRate: 5,
    propertyTax: 4500,
    insurance: 1200,
    hoa: 0,
    maintenance: 200,
    propertyManagement: 10,
  });

  const [results, setResults] = useState({
    loanAmount: 0,
    monthlyPayment: 0,
    grossMonthlyIncome: 0,
    monthlyExpenses: 0,
    monthlyCashFlow: 0,
    annualCashFlow: 0,
    cashOnCashReturn: 0,
    capRate: 0,
    totalCashNeeded: 0,
  });

  useEffect(() => {
    const loanAmount = inputs.purchasePrice * (1 - inputs.downPayment / 100);
    const monthlyRate = inputs.interestRate / 100 / 12;
    const numPayments = inputs.loanTerm * 12;
    const monthlyPayment = (loanAmount * monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / 
                          (Math.pow(1 + monthlyRate, numPayments) - 1);

    const grossMonthlyIncome = inputs.monthlyRent;
    const effectiveMonthlyIncome = grossMonthlyIncome * (1 - inputs.vacancyRate / 100);
    
    const monthlyPropertyTax = inputs.propertyTax / 12;
    const monthlyInsurance = inputs.insurance / 12;
    const monthlyPropMgmt = inputs.monthlyRent * (inputs.propertyManagement / 100);
    
    const monthlyExpenses = monthlyPayment + monthlyPropertyTax + monthlyInsurance + 
                           inputs.hoa + inputs.maintenance + monthlyPropMgmt;
    
    const monthlyCashFlow = effectiveMonthlyIncome - monthlyExpenses;
    const annualCashFlow = monthlyCashFlow * 12;
    
    const downPaymentAmount = inputs.purchasePrice * (inputs.downPayment / 100);
    const totalCashNeeded = downPaymentAmount;
    const cashOnCashReturn = (annualCashFlow / totalCashNeeded) * 100;
    
    const annualNOI = (grossMonthlyIncome * 12 * (1 - inputs.vacancyRate / 100)) - 
                     ((monthlyPropertyTax + monthlyInsurance + inputs.hoa + inputs.maintenance + monthlyPropMgmt) * 12);
    const capRate = (annualNOI / inputs.purchasePrice) * 100;

    setResults({
      loanAmount,
      monthlyPayment,
      grossMonthlyIncome,
      monthlyExpenses,
      monthlyCashFlow,
      annualCashFlow,
      cashOnCashReturn,
      capRate,
      totalCashNeeded,
    });
  }, [inputs]);

  const formatCurrency = (value: number) => 
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);

  const formatPercent = (value: number) => `${value.toFixed(2)}%`;

  const cashFlowData = Array.from({ length: 12 }, (_, i) => ({
    month: `M${i + 1}`,
    cashFlow: results.monthlyCashFlow,
    cumulative: results.monthlyCashFlow * (i + 1),
  }));

  return (
    <CalculatorLayout
      title="Single Family Rental"
      description="Comprehensive long-term rental analysis for single-family homes including cash flow projections, debt service coverage, cap rate analysis, and return metrics. Optimized for buy-and-hold investors building passive income portfolios."
      icon={Home}
      gradient="from-green-600 to-green-700"
      badge={results.cashOnCashReturn > 8 ? "Strong Returns" : results.cashOnCashReturn > 0 ? "Positive Cash Flow" : "Review Required"}
      badgeColor={results.cashOnCashReturn > 8 ? "bg-green-600" : results.cashOnCashReturn > 0 ? "bg-blue-600" : "bg-orange-600"}
      onBack={onBack}
    >
      {{
        calculator: (
          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-7 space-y-6">
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-green-500/10 rounded-xl flex items-center justify-center border border-green-500/20">
                    <Home className="w-5 h-5 text-green-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Purchase & Financing</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Purchase Price</Label>
                    <Input
                      type="number"
                      value={inputs.purchasePrice}
                      onChange={(e) => setInputs(prev => ({ ...prev, purchasePrice: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Down Payment %</Label>
                    <Input
                      type="number"
                      value={inputs.downPayment}
                      onChange={(e) => setInputs(prev => ({ ...prev, downPayment: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Interest Rate %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.interestRate}
                      onChange={(e) => setInputs(prev => ({ ...prev, interestRate: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Loan Term (Years)</Label>
                    <Input
                      type="number"
                      value={inputs.loanTerm}
                      onChange={(e) => setInputs(prev => ({ ...prev, loanTerm: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                    />
                  </div>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-blue-500/10 rounded-xl flex items-center justify-center border border-blue-500/20">
                    <DollarSign className="w-5 h-5 text-blue-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Income & Operating Expenses</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Monthly Rent</Label>
                    <Input
                      type="number"
                      value={inputs.monthlyRent}
                      onChange={(e) => setInputs(prev => ({ ...prev, monthlyRent: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Vacancy Rate %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.vacancyRate}
                      onChange={(e) => setInputs(prev => ({ ...prev, vacancyRate: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Annual Property Tax</Label>
                    <Input
                      type="number"
                      value={inputs.propertyTax}
                      onChange={(e) => setInputs(prev => ({ ...prev, propertyTax: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Annual Insurance</Label>
                    <Input
                      type="number"
                      value={inputs.insurance}
                      onChange={(e) => setInputs(prev => ({ ...prev, insurance: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Monthly HOA</Label>
                    <Input
                      type="number"
                      value={inputs.hoa}
                      onChange={(e) => setInputs(prev => ({ ...prev, hoa: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Monthly Maintenance</Label>
                    <Input
                      type="number"
                      value={inputs.maintenance}
                      onChange={(e) => setInputs(prev => ({ ...prev, maintenance: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                  <div className="col-span-2">
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Property Management %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.propertyManagement}
                      onChange={(e) => setInputs(prev => ({ ...prev, propertyManagement: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                </div>
              </Card>
            </div>

            <div className="col-span-5 space-y-6">
              <Card className="p-8 bg-gradient-to-br from-green-600 via-green-700 to-green-800 border-0 shadow-2xl shadow-green-500/20 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
                <div className="absolute top-0 right-0 w-48 h-48 bg-white/5 rounded-full blur-3xl -mr-24 -mt-24" />
                <div className="relative z-10">
                  <div className="flex items-center gap-2 mb-3">
                    <DollarSign className="w-5 h-5 text-green-200" />
                    <h3 className="text-sm uppercase tracking-wider text-green-200">Monthly Cash Flow</h3>
                  </div>
                  <div className="text-5xl text-white mb-3">{formatCurrency(results.monthlyCashFlow)}</div>
                  <p className="text-sm text-green-100">Annual: {formatCurrency(results.annualCashFlow)}</p>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Investment Metrics</h3>
                <div className="space-y-4">
                  {[
                    { label: 'Cash-on-Cash Return', value: formatPercent(results.cashOnCashReturn), icon: Percent, color: results.cashOnCashReturn > 8 ? 'text-green-400' : 'text-blue-400' },
                    { label: 'Cap Rate', value: formatPercent(results.capRate), icon: TrendingUp, color: 'text-purple-400' },
                    { label: 'Monthly Mortgage', value: formatCurrency(results.monthlyPayment), icon: Calendar, color: 'text-orange-400' },
                    { label: 'Cash Needed', value: formatCurrency(results.totalCashNeeded), icon: DollarSign, color: 'text-blue-400' },
                  ].map((item) => (
                    <div key={item.label} className={`flex items-center justify-between pb-4 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-200'} last:border-0`}>
                      <div className="flex items-center gap-3">
                        <div className={`w-8 h-8 ${theme === 'dark' ? 'bg-slate-700/30' : 'bg-slate-100'} rounded-lg flex items-center justify-center`}>
                          <item.icon className={`w-4 h-4 ${item.color}`} />
                        </div>
                        <span className={`text-sm ${colors.text.secondary}`}>{item.label}</span>
                      </div>
                      <span className={`${item.color}`}>{item.value}</span>
                    </div>
                  ))}
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Monthly Breakdown</h3>
                <div className="space-y-3">
                  <div className={`flex justify-between text-sm pb-2 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-200'}`}>
                    <span className={colors.text.secondary}>Gross Rent</span>
                    <span className="text-green-400">+{formatCurrency(results.grossMonthlyIncome)}</span>
                  </div>
                  <div className={`flex justify-between text-sm pb-2 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-200'}`}>
                    <span className={colors.text.secondary}>Total Expenses</span>
                    <span className="text-red-400">-{formatCurrency(results.monthlyExpenses)}</span>
                  </div>
                  <div className={`pt-3 border-t-2 ${theme === 'dark' ? 'border-slate-600' : 'border-slate-300'} flex justify-between`}>
                    <span className={colors.text.primary}>Net Cash Flow</span>
                    <span className={`text-lg ${results.monthlyCashFlow >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {formatCurrency(results.monthlyCashFlow)}
                    </span>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        ),
        charts: (
          <div className="grid grid-cols-2 gap-8">
            <Card className={`p-8 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
              <h3 className={`text-xl ${colors.text.primary} mb-6`}>12-Month Cash Flow Projection</h3>
              <ResponsiveContainer width="100%" height={350}>
                <AreaChart data={cashFlowData}>
                  <defs>
                    <linearGradient id="colorCashFlow" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#e2e8f0'} opacity={0.2} />
                  <XAxis dataKey="month" stroke={theme === 'dark' ? '#94a3b8' : '#64748b'} fontSize={12} />
                  <YAxis stroke={theme === 'dark' ? '#94a3b8' : '#64748b'} fontSize={12} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: theme === 'dark' ? '#1e293b' : '#fff', 
                      border: `1px solid ${theme === 'dark' ? '#334155' : '#e2e8f0'}`,
                      borderRadius: '12px',
                      color: theme === 'dark' ? '#fff' : '#000'
                    }}
                    formatter={(value: number) => formatCurrency(value)}
                  />
                  <Area type="monotone" dataKey="cashFlow" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#colorCashFlow)" />
                </AreaChart>
              </ResponsiveContainer>
            </Card>

            <Card className={`p-8 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
              <h3 className={`text-xl ${colors.text.primary} mb-6`}>Cumulative Cash Flow</h3>
              <ResponsiveContainer width="100%" height={350}>
                <LineChart data={cashFlowData}>
                  <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#e2e8f0'} opacity={0.2} />
                  <XAxis dataKey="month" stroke={theme === 'dark' ? '#94a3b8' : '#64748b'} fontSize={12} />
                  <YAxis stroke={theme === 'dark' ? '#94a3b8' : '#64748b'} fontSize={12} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: theme === 'dark' ? '#1e293b' : '#fff', 
                      border: `1px solid ${theme === 'dark' ? '#334155' : '#e2e8f0'}`,
                      borderRadius: '12px',
                      color: theme === 'dark' ? '#fff' : '#000'
                    }}
                    formatter={(value: number) => formatCurrency(value)}
                  />
                  <Line type="monotone" dataKey="cumulative" stroke="#3b82f6" strokeWidth={3} dot={{ fill: '#3b82f6', r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </div>
        ),
        documentation: (
          <Card className={`p-8 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm max-w-5xl`}>
            <h2 className={`text-3xl ${colors.text.primary} mb-6`}>Single Family Rental Documentation</h2>
            <div className={`${colors.text.secondary} space-y-6 leading-relaxed`}>
              <p>
                This model analyzes long-term single-family rental properties, focusing on sustainable cash flow, debt service coverage, and long-term return metrics.
              </p>
              <div>
                <h3 className={`text-2xl ${colors.text.primary} mt-8 mb-4`}>Key Metrics</h3>
                <ul className="space-y-3">
                  <li><strong className={colors.text.primary}>Cash-on-Cash Return:</strong> Annual cash flow divided by total cash invested. Target: 8-12% for stable markets.</li>
                  <li><strong className={colors.text.primary}>Cap Rate:</strong> Net operating income divided by purchase price. Useful for comparing properties.</li>
                  <li><strong className={colors.text.primary}>Cash Flow:</strong> Monthly income minus all expenses including mortgage, taxes, insurance, and management.</li>
                </ul>
              </div>
            </div>
          </Card>
        ),
      }}
    </CalculatorLayout>
  );
}
