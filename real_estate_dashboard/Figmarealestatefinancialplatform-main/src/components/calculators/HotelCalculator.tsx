import { useState, useEffect } from 'react';
import { Hotel, DollarSign, Users, Percent } from 'lucide-react';
import { CalculatorLayout } from './CalculatorLayout';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { useTheme } from '../../contexts/ThemeContext';

export function HotelCalculator({ onBack }: { onBack: () => void }) {
  const { theme, colors } = useTheme();
  const [inputs, setInputs] = useState({
    purchasePrice: 3000000,
    rooms: 80,
    adr: 150,
    occupancyRate: 70,
    operatingExpenseRatio: 65,
  });

  const [results, setResults] = useState({
    revpar: 0,
    annualRevenue: 0,
    operatingExpenses: 0,
    noi: 0,
    pricePerRoom: 0,
  });

  useEffect(() => {
    const revpar = inputs.adr * (inputs.occupancyRate / 100);
    const annualRevenue = inputs.rooms * inputs.adr * (inputs.occupancyRate / 100) * 365;
    const operatingExpenses = annualRevenue * (inputs.operatingExpenseRatio / 100);
    const noi = annualRevenue - operatingExpenses;
    const pricePerRoom = inputs.purchasePrice / inputs.rooms;

    setResults({
      revpar,
      annualRevenue,
      operatingExpenses,
      noi,
      pricePerRoom,
    });
  }, [inputs]);

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);

  return (
    <CalculatorLayout
      title="Hotel & Hospitality"
      description="Comprehensive hospitality financial modeling with RevPAR calculations, ADR analysis, occupancy projections, and seasonal variance. Includes operating expense ratios specific to hotel operations and ancillary revenue streams."
      icon={Hotel}
      gradient="from-orange-600 to-orange-700"
      badge={`RevPAR: ${formatCurrency(results.revpar)}`}
      badgeColor="bg-orange-600"
      onBack={onBack}
    >
      {{
        calculator: (
          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-7 space-y-6">
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-orange-500/10 rounded-xl flex items-center justify-center border border-orange-500/20">
                    <Hotel className="w-5 h-5 text-orange-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Hotel Metrics</h3>
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
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Number of Rooms</Label>
                    <Input
                      type="number"
                      value={inputs.rooms}
                      onChange={(e) => setInputs(prev => ({ ...prev, rooms: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Average Daily Rate (ADR)</Label>
                    <Input
                      type="number"
                      value={inputs.adr}
                      onChange={(e) => setInputs(prev => ({ ...prev, adr: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Occupancy Rate %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={inputs.occupancyRate}
                      onChange={(e) => setInputs(prev => ({ ...prev, occupancyRate: Number(e.target.value) }))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div className="col-span-2">
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
              <Card className="p-8 bg-gradient-to-br from-orange-600 via-orange-700 to-orange-800 border-0 shadow-2xl shadow-orange-500/20 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
                <div className="relative z-10">
                  <h3 className="text-sm uppercase tracking-wider text-orange-200 mb-3">RevPAR</h3>
                  <div className="text-5xl text-white mb-3">{formatCurrency(results.revpar)}</div>
                  <p className="text-sm text-orange-100">Revenue Per Available Room</p>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Financial Summary</h3>
                <div className="space-y-4">
                  {[
                    { label: 'Annual Revenue', value: formatCurrency(results.annualRevenue) },
                    { label: 'Operating Expenses', value: formatCurrency(results.operatingExpenses) },
                    { label: 'Net Operating Income', value: formatCurrency(results.noi) },
                    { label: 'Price Per Room', value: formatCurrency(results.pricePerRoom) },
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
            <h2 className={`text-3xl ${colors.text.primary} mb-6`}>Hotel & Hospitality Documentation</h2>
            <div className={`${colors.text.secondary} space-y-4 leading-relaxed`}>
              <p>Hotel investments require unique metrics like RevPAR (Revenue Per Available Room) and ADR (Average Daily Rate) for accurate performance analysis.</p>
            </div>
          </Card>
        ),
      }}
    </CalculatorLayout>
  );
}
