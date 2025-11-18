import { useState, useEffect } from 'react';
import { Blocks, DollarSign } from 'lucide-react';
import { CalculatorLayout } from './CalculatorLayout';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { useTheme } from '../../contexts/ThemeContext';

export function MixedUseCalculator({ onBack }: { onBack: () => void }) {
  const { theme, colors } = useTheme();
  const [inputs, setInputs] = useState({
    purchasePrice: 4000000,
    residentialUnits: 20,
    residentialRent: 1800,
    retailSqFt: 5000,
    retailRentPsf: 25,
    officeSqFt: 10000,
    officeRentPsf: 30,
    vacancyRate: 6,
    operatingExpenseRatio: 42,
  });

  const [results, setResults] = useState({
    residentialIncome: 0,
    retailIncome: 0,
    officeIncome: 0,
    totalIncome: 0,
    effectiveIncome: 0,
    noi: 0,
    blendedCapRate: 0,
  });

  useEffect(() => {
    const residentialIncome = inputs.residentialUnits * inputs.residentialRent * 12;
    const retailIncome = inputs.retailSqFt * inputs.retailRentPsf * 12;
    const officeIncome = inputs.officeSqFt * inputs.officeRentPsf * 12;
    const totalIncome = residentialIncome + retailIncome + officeIncome;
    const effectiveIncome = totalIncome * (1 - inputs.vacancyRate / 100);
    const operatingExpenses = effectiveIncome * (inputs.operatingExpenseRatio / 100);
    const noi = effectiveIncome - operatingExpenses;
    const blendedCapRate = (noi / inputs.purchasePrice) * 100;

    setResults({
      residentialIncome,
      retailIncome,
      officeIncome,
      totalIncome,
      effectiveIncome,
      noi,
      blendedCapRate,
    });
  }, [inputs]);

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);

  return (
    <CalculatorLayout
      title="Mixed-Use Development"
      description="Complex development analysis blending residential, retail, and office components with income stratification, blended cap rates, and mixed-use operating metrics. Ideal for urban developments with multiple revenue streams."
      icon={Blocks}
      gradient="from-teal-600 to-teal-700"
      badge={`Blended Cap: ${results.blendedCapRate.toFixed(2)}%`}
      badgeColor="bg-teal-600"
      onBack={onBack}
    >
      {{
        calculator: (
          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-7 space-y-6">
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-teal-500/10 rounded-xl flex items-center justify-center border border-teal-500/20">
                    <Blocks className="w-5 h-5 text-teal-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Property Details</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="col-span-2">
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Purchase Price</Label>
                    <Input
                      type="number"
                      value={inputs.purchasePrice}
                      onChange={(e) => setInputs(prev => ({ ...prev, purchasePrice: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Residential Component</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Units</Label>
                    <Input
                      type="number"
                      value={inputs.residentialUnits}
                      onChange={(e) => setInputs(prev => ({ ...prev, residentialUnits: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Avg Rent/Unit</Label>
                    <Input
                      type="number"
                      value={inputs.residentialRent}
                      onChange={(e) => setInputs(prev => ({ ...prev, residentialRent: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Retail Component</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Square Feet</Label>
                    <Input
                      type="number"
                      value={inputs.retailSqFt}
                      onChange={(e) => setInputs(prev => ({ ...prev, retailSqFt: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Rent PSF/Month</Label>
                    <Input
                      type="number"
                      value={inputs.retailRentPsf}
                      onChange={(e) => setInputs(prev => ({ ...prev, retailRentPsf: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Office Component</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Square Feet</Label>
                    <Input
                      type="number"
                      value={inputs.officeSqFt}
                      onChange={(e) => setInputs(prev => ({ ...prev, officeSqFt: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Rent PSF/Month</Label>
                    <Input
                      type="number"
                      value={inputs.officeRentPsf}
                      onChange={(e) => setInputs(prev => ({ ...prev, officeRentPsf: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Operating Assumptions</h3>
                <div className="grid grid-cols-2 gap-4">
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
                </div>
              </Card>
            </div>

            <div className="col-span-5 space-y-6">
              <Card className="p-8 bg-gradient-to-br from-teal-600 via-teal-700 to-teal-800 border-0 shadow-2xl shadow-teal-500/20 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
                <div className="relative z-10">
                  <h3 className="text-sm uppercase tracking-wider text-teal-200 mb-3">Blended Cap Rate</h3>
                  <div className="text-5xl text-white mb-3">{results.blendedCapRate.toFixed(2)}%</div>
                  <p className="text-sm text-teal-100">Mixed-Use Performance</p>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Income Breakdown</h3>
                <div className="space-y-4">
                  {[
                    { label: 'Residential Income', value: formatCurrency(results.residentialIncome), percent: (results.residentialIncome / results.totalIncome * 100).toFixed(1) },
                    { label: 'Retail Income', value: formatCurrency(results.retailIncome), percent: (results.retailIncome / results.totalIncome * 100).toFixed(1) },
                    { label: 'Office Income', value: formatCurrency(results.officeIncome), percent: (results.officeIncome / results.totalIncome * 100).toFixed(1) },
                  ].map((item) => (
                    <div key={item.label} className={`pb-3 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'} last:border-0`}>
                      <div className="flex justify-between mb-2">
                        <span className={`text-sm ${colors.text.secondary}`}>{item.label}</span>
                        <span className={colors.text.primary}>{item.value}</span>
                      </div>
                      <div className="w-full bg-slate-700/20 rounded-full h-2">
                        <div
                          className="h-2 bg-gradient-to-r from-teal-500 to-teal-600 rounded-full"
                          style={{ width: `${item.percent}%` }}
                        />
                      </div>
                      <div className="text-xs text-teal-400 mt-1">{item.percent}% of total</div>
                    </div>
                  ))}
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Financial Summary</h3>
                <div className="space-y-3">
                  <div className={`flex justify-between pb-2 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'}`}>
                    <span className={`text-sm ${colors.text.secondary}`}>Total Income</span>
                    <span className="text-green-400">{formatCurrency(results.totalIncome)}</span>
                  </div>
                  <div className={`flex justify-between pb-2 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'}`}>
                    <span className={`text-sm ${colors.text.secondary}`}>Effective Income</span>
                    <span className={colors.text.primary}>{formatCurrency(results.effectiveIncome)}</span>
                  </div>
                  <div className={`pt-3 border-t-2 ${theme === 'dark' ? 'border-slate-600' : 'border-blue-200'} flex justify-between`}>
                    <span className={colors.text.primary}>NOI</span>
                    <span className="text-lg text-green-400">{formatCurrency(results.noi)}</span>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        ),
        documentation: (
          <Card className={`p-8 ${colors.card} border ${colors.border.secondary} max-w-5xl`}>
            <h2 className={`text-3xl ${colors.text.primary} mb-6`}>Mixed-Use Development Documentation</h2>
            <div className={`${colors.text.secondary} space-y-4 leading-relaxed`}>
              <p>Mixed-use properties combine residential, retail, and office spaces, requiring analysis of blended income streams and diversified risk profiles.</p>
            </div>
          </Card>
        ),
      }}
    </CalculatorLayout>
  );
}
