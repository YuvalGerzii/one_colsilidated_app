import { useState, useEffect } from 'react';
import { Building2, DollarSign, TrendingUp, BarChart } from 'lucide-react';
import { CalculatorLayout } from './CalculatorLayout';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { useTheme } from '../../contexts/ThemeContext';

export function HighRiseCalculator({ onBack }: { onBack: () => void }) {
  const { theme, colors } = useTheme();
  const [inputs, setInputs] = useState({
    purchasePrice: 5000000,
    units: 50,
    avgRentPerUnit: 2000,
    vacancyRate: 5,
    operatingExpenseRatio: 40,
    capRate: 6,
  });

  const [results, setResults] = useState({
    grossPotentialIncome: 0,
    effectiveGrossIncome: 0,
    operatingExpenses: 0,
    noi: 0,
    value: 0,
    pricePerUnit: 0,
  });

  useEffect(() => {
    const grossPotentialIncome = inputs.units * inputs.avgRentPerUnit * 12;
    const effectiveGrossIncome = grossPotentialIncome * (1 - inputs.vacancyRate / 100);
    const operatingExpenses = effectiveGrossIncome * (inputs.operatingExpenseRatio / 100);
    const noi = effectiveGrossIncome - operatingExpenses;
    const value = noi / (inputs.capRate / 100);
    const pricePerUnit = inputs.purchasePrice / inputs.units;

    setResults({
      grossPotentialIncome,
      effectiveGrossIncome,
      operatingExpenses,
      noi,
      value,
      pricePerUnit,
    });
  }, [inputs]);

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);

  return (
    <CalculatorLayout
      title="High-Rise Multifamily"
      description="Institutional-grade modeling for large apartment complexes with 50+ units, including gross potential income calculations, operating expense ratios, cap rate analysis, and per-unit valuations for sophisticated commercial real estate investments."
      icon={Building2}
      gradient="from-indigo-600 to-indigo-700"
      badge="Commercial Grade"
      badgeColor="bg-indigo-600"
      onBack={onBack}
    >
      {{
        calculator: (
          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-7 space-y-6">
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-indigo-500/10 rounded-xl flex items-center justify-center border border-indigo-500/20">
                    <Building2 className="w-5 h-5 text-indigo-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Property Information</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Purchase Price</Label>
                    <Input
                      type="number"
                      value={inputs.purchasePrice}
                      onChange={(e) => setInputs(prev => ({ ...prev, purchasePrice: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Total Units</Label>
                    <Input
                      type="number"
                      value={inputs.units}
                      onChange={(e) => setInputs(prev => ({ ...prev, units: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Avg Rent Per Unit</Label>
                    <Input
                      type="number"
                      value={inputs.avgRentPerUnit}
                      onChange={(e) => setInputs(prev => ({ ...prev, avgRentPerUnit: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Vacancy Rate %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.vacancyRate}
                      onChange={(e) => setInputs(prev => ({ ...prev, vacancyRate: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Operating Expense Ratio %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.operatingExpenseRatio}
                      onChange={(e) => setInputs(prev => ({ ...prev, operatingExpenseRatio: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Market Cap Rate %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.capRate}
                      onChange={(e) => setInputs(prev => ({ ...prev, capRate: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>
            </div>

            <div className="col-span-5 space-y-6">
              <Card className="p-8 bg-gradient-to-br from-indigo-600 via-indigo-700 to-indigo-800 border-0 shadow-2xl shadow-indigo-500/20 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
                <div className="relative z-10">
                  <h3 className="text-sm uppercase tracking-wider text-indigo-200 mb-3">Net Operating Income</h3>
                  <div className="text-5xl text-white mb-3">{formatCurrency(results.noi)}</div>
                  <p className="text-sm text-indigo-100">Annual NOI</p>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Valuation Metrics</h3>
                <div className="space-y-4">
                  {[
                    { label: 'Estimated Value', value: formatCurrency(results.value) },
                    { label: 'Price Per Unit', value: formatCurrency(results.pricePerUnit) },
                    { label: 'Gross Potential Income', value: formatCurrency(results.grossPotentialIncome) },
                    { label: 'Effective Gross Income', value: formatCurrency(results.effectiveGrossIncome) },
                  ].map((item) => (
                    <div key={item.label} className={`flex justify-between pb-3 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'} last:border-0`}>
                      <span className={`text-sm ${colors.text.secondary}`}>{item.label}</span>
                      <span className={colors.text.primary}>{item.value}</span>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </div>
        ),
        documentation: (
          <Card className={`p-8 ${colors.card} border ${colors.border.secondary} max-w-5xl`}>
            <h2 className={`text-3xl ${colors.text.primary} mb-6`}>High-Rise Multifamily Documentation</h2>
            <div className={`${colors.text.secondary} space-y-4 leading-relaxed`}>
              <p>High-rise multifamily properties require sophisticated institutional-grade analysis with focus on NOI, cap rates, and per-unit economics.</p>
            </div>
          </Card>
        ),
      }}
    </CalculatorLayout>
  );
}
