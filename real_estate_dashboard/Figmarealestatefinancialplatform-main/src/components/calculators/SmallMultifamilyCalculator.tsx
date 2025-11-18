import { useState, useEffect } from 'react';
import { Building, DollarSign, TrendingUp, Users, Percent } from 'lucide-react';
import { CalculatorLayout } from './CalculatorLayout';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip, Cell, PieChart, Pie } from 'recharts';
import { useTheme } from '../../contexts/ThemeContext';

export function SmallMultifamilyCalculator({ onBack }: { onBack: () => void }) {
  const { theme, colors } = useTheme();
  const [inputs, setInputs] = useState({
    purchasePrice: 500000,
    units: 4,
    avgRentPerUnit: 1200,
    downPayment: 25,
    interestRate: 7,
    loanTerm: 30,
    vacancyRate: 7,
    propertyTax: 7500,
    insurance: 2400,
    maintenance: 500,
    propertyManagement: 8,
  });

  const [results, setResults] = useState({
    totalMonthlyRent: 0,
    effectiveGrossIncome: 0,
    monthlyExpenses: 0,
    noi: 0,
    cashFlow: 0,
    capRate: 0,
    cashOnCashReturn: 0,
    dscr: 0,
    monthlyPayment: 0,
  });

  useEffect(() => {
    const totalMonthlyRent = inputs.units * inputs.avgRentPerUnit;
    const effectiveGrossIncome = totalMonthlyRent * (1 - inputs.vacancyRate / 100);
    
    const loanAmount = inputs.purchasePrice * (1 - inputs.downPayment / 100);
    const monthlyRate = inputs.interestRate / 100 / 12;
    const numPayments = inputs.loanTerm * 12;
    const monthlyPayment = (loanAmount * monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / 
                          (Math.pow(1 + monthlyRate, numPayments) - 1);

    const monthlyPropMgmt = effectiveGrossIncome * (inputs.propertyManagement / 100);
    const monthlyExpenses = (inputs.propertyTax + inputs.insurance) / 12 + inputs.maintenance + monthlyPropMgmt;
    const noi = (effectiveGrossIncome - monthlyExpenses) * 12;
    const cashFlow = effectiveGrossIncome - monthlyExpenses - monthlyPayment;
    const capRate = (noi / inputs.purchasePrice) * 100;
    const downPaymentAmount = inputs.purchasePrice * (inputs.downPayment / 100);
    const cashOnCashReturn = ((cashFlow * 12) / downPaymentAmount) * 100;
    const dscr = (effectiveGrossIncome - monthlyExpenses) / monthlyPayment;

    setResults({
      totalMonthlyRent,
      effectiveGrossIncome,
      monthlyExpenses,
      noi,
      cashFlow,
      capRate,
      cashOnCashReturn,
      dscr,
      monthlyPayment,
    });
  }, [inputs]);

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);

  const formatPercent = (value: number) => `${value.toFixed(2)}%`;

  const unitData = Array.from({ length: inputs.units }, (_, i) => ({
    unit: `Unit ${i + 1}`,
    rent: inputs.avgRentPerUnit,
    color: ['#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe'][i % 4],
  }));

  return (
    <CalculatorLayout
      title="Small Multifamily (2-4 Units)"
      description="Analyze small multifamily properties with comprehensive per-unit economics, debt service coverage ratio (DSCR), net operating income calculations, and cash flow projections. Ideal for investors scaling from single-family to small apartment buildings."
      icon={Building}
      gradient="from-purple-600 to-purple-700"
      badge={results.dscr > 1.25 ? "Strong DSCR" : results.dscr > 1 ? "Acceptable" : "Review"}
      badgeColor={results.dscr > 1.25 ? "bg-green-600" : results.dscr > 1 ? "bg-blue-600" : "bg-orange-600"}
      onBack={onBack}
    >
      {{
        calculator: (
          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-7 space-y-6">
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-purple-500/10 rounded-xl flex items-center justify-center border border-purple-500/20">
                    <Building className="w-5 h-5 text-purple-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Property Details</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Purchase Price</Label>
                    <Input
                      type="number"
                      value={inputs.purchasePrice}
                      onChange={(e) => setInputs(prev => ({ ...prev, purchasePrice: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-purple-500/50 focus:ring-purple-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Number of Units</Label>
                    <Input
                      type="number"
                      value={inputs.units}
                      onChange={(e) => setInputs(prev => ({ ...prev, units: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-purple-500/50 focus:ring-purple-500/20`}
                    />
                  </div>
                  <div className="col-span-2">
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Average Rent Per Unit</Label>
                    <Input
                      type="number"
                      value={inputs.avgRentPerUnit}
                      onChange={(e) => setInputs(prev => ({ ...prev, avgRentPerUnit: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-purple-500/50 focus:ring-purple-500/20`}
                    />
                  </div>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-blue-500/10 rounded-xl flex items-center justify-center border border-blue-500/20">
                    <Percent className="w-5 h-5 text-blue-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Financing</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Down Payment %</Label>
                    <Input
                      type="number"
                      value={inputs.downPayment}
                      onChange={(e) => setInputs(prev => ({ ...prev, downPayment: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Interest Rate %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.interestRate}
                      onChange={(e) => setInputs(prev => ({ ...prev, interestRate: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                  <div className="col-span-2">
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Loan Term (Years)</Label>
                    <Input
                      type="number"
                      value={inputs.loanTerm}
                      onChange={(e) => setInputs(prev => ({ ...prev, loanTerm: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-green-500/10 rounded-xl flex items-center justify-center border border-green-500/20">
                    <DollarSign className="w-5 h-5 text-green-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Operating Expenses</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Vacancy Rate %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.vacancyRate}
                      onChange={(e) => setInputs(prev => ({ ...prev, vacancyRate: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Annual Property Tax</Label>
                    <Input
                      type="number"
                      value={inputs.propertyTax}
                      onChange={(e) => setInputs(prev => ({ ...prev, propertyTax: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Annual Insurance</Label>
                    <Input
                      type="number"
                      value={inputs.insurance}
                      onChange={(e) => setInputs(prev => ({ ...prev, insurance: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Monthly Maintenance</Label>
                    <Input
                      type="number"
                      value={inputs.maintenance}
                      onChange={(e) => setInputs(prev => ({ ...prev, maintenance: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                    />
                  </div>
                  <div className="col-span-2">
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Property Management %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.propertyManagement}
                      onChange={(e) => setInputs(prev => ({ ...prev, propertyManagement: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                    />
                  </div>
                </div>
              </Card>
            </div>

            <div className="col-span-5 space-y-6">
              <Card className="p-8 bg-gradient-to-br from-purple-600 via-purple-700 to-purple-800 border-0 shadow-2xl shadow-purple-500/20 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
                <div className="absolute top-0 right-0 w-48 h-48 bg-white/5 rounded-full blur-3xl -mr-24 -mt-24" />
                <div className="relative z-10">
                  <div className="flex items-center gap-2 mb-3">
                    <Users className="w-5 h-5 text-purple-200" />
                    <h3 className="text-sm uppercase tracking-wider text-purple-200">DSCR (Debt Service Coverage)</h3>
                  </div>
                  <div className="text-5xl text-white mb-3">{results.dscr.toFixed(2)}x</div>
                  <p className="text-sm text-purple-100">
                    {results.dscr > 1.25 ? 'Excellent coverage ratio' : results.dscr > 1 ? 'Acceptable coverage' : 'Below lender requirements'}
                  </p>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Key Metrics</h3>
                <div className="space-y-4">
                  {[
                    { label: 'Monthly Cash Flow', value: formatCurrency(results.cashFlow), color: results.cashFlow >= 0 ? 'text-green-400' : 'text-red-400' },
                    { label: 'Cap Rate', value: formatPercent(results.capRate), color: 'text-blue-400' },
                    { label: 'Cash-on-Cash Return', value: formatPercent(results.cashOnCashReturn), color: 'text-purple-400' },
                    { label: 'Annual NOI', value: formatCurrency(results.noi), color: 'text-green-400' },
                  ].map((item) => (
                    <div key={item.label} className={`flex items-center justify-between pb-4 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'} last:border-0`}>
                      <span className={`text-sm ${colors.text.secondary}`}>{item.label}</span>
                      <span className={item.color}>{item.value}</span>
                    </div>
                  ))}
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Per-Unit Analysis</h3>
                <div className="space-y-3">
                  <div className={`flex justify-between text-sm pb-2 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'}`}>
                    <span className={colors.text.secondary}>Rent Per Unit</span>
                    <span className={colors.text.primary}>{formatCurrency(inputs.avgRentPerUnit)}</span>
                  </div>
                  <div className={`flex justify-between text-sm pb-2 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'}`}>
                    <span className={colors.text.secondary}>Total Units</span>
                    <span className={colors.text.primary}>{inputs.units}</span>
                  </div>
                  <div className={`flex justify-between text-sm pb-2 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'}`}>
                    <span className={colors.text.secondary}>Gross Monthly Income</span>
                    <span className="text-green-400">{formatCurrency(results.totalMonthlyRent)}</span>
                  </div>
                  <div className={`pt-3 border-t-2 ${theme === 'dark' ? 'border-slate-600' : 'border-blue-200'} flex justify-between`}>
                    <span className={colors.text.primary}>Cash Flow/Unit</span>
                    <span className="text-lg text-purple-400">{formatCurrency(results.cashFlow / inputs.units)}</span>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        ),
        charts: (
          <div className="grid grid-cols-2 gap-8">
            <Card className={`p-8 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
              <h3 className={`text-xl ${colors.text.primary} mb-6`}>Rent Distribution by Unit</h3>
              <ResponsiveContainer width="100%" height={350}>
                <BarChart data={unitData}>
                  <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#334155' : '#dbeafe'} opacity={0.2} vertical={false} />
                  <XAxis dataKey="unit" tick={{ fontSize: 12, fill: theme === 'dark' ? '#94a3b8' : '#64748b' }} />
                  <YAxis tick={{ fontSize: 12, fill: theme === 'dark' ? '#94a3b8' : '#64748b' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: theme === 'dark' ? '#1e293b' : '#fff',
                      border: `1px solid ${theme === 'dark' ? '#334155' : '#dbeafe'}`,
                      borderRadius: '12px',
                    }}
                    formatter={(value: number) => formatCurrency(value)}
                  />
                  <Bar dataKey="rent" radius={[8, 8, 0, 0]}>
                    {unitData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </Card>

            <Card className={`p-8 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
              <h3 className={`text-xl ${colors.text.primary} mb-6`}>Income vs Expenses</h3>
              <ResponsiveContainer width="100%" height={350}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'Income', value: results.effectiveGrossIncome, fill: '#10b981' },
                      { name: 'Operating Expenses', value: results.monthlyExpenses, fill: '#f59e0b' },
                      { name: 'Debt Service', value: results.monthlyPayment, fill: '#ef4444' },
                    ]}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    dataKey="value"
                    label={(entry) => `${entry.name}: ${formatCurrency(entry.value)}`}
                  />
                  <Tooltip formatter={(value: number) => formatCurrency(value)} />
                </PieChart>
              </ResponsiveContainer>
            </Card>
          </div>
        ),
        documentation: (
          <Card className={`p-8 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''} max-w-5xl`}>
            <h2 className={`text-3xl ${colors.text.primary} mb-6`}>Small Multifamily Documentation</h2>
            <div className={`${colors.text.secondary} space-y-6 leading-relaxed`}>
              <p>
                Small multifamily properties (2-4 units) represent an ideal entry point for investors scaling from single-family rentals to larger apartment complexes.
              </p>
              <div>
                <h3 className={`text-2xl ${colors.text.primary} mt-8 mb-4`}>Key Metrics</h3>
                <ul className="space-y-3">
                  <li><strong className={colors.text.primary}>DSCR:</strong> Debt Service Coverage Ratio should be 1.25x or higher for most lenders.</li>
                  <li><strong className={colors.text.primary}>Cap Rate:</strong> Typical range 5-8% depending on market and property quality.</li>
                  <li><strong className={colors.text.primary}>Cash-on-Cash Return:</strong> Target 8-12% for competitive markets.</li>
                </ul>
              </div>
            </div>
          </Card>
        ),
      }}
    </CalculatorLayout>
  );
}
