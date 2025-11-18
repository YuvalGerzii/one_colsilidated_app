import { useState, useEffect } from 'react';
import { FileText, DollarSign } from 'lucide-react';
import { CalculatorLayout } from './CalculatorLayout';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { useTheme } from '../../contexts/ThemeContext';

export function LeaseAnalyzer({ onBack }: { onBack: () => void }) {
  const { theme, colors } = useTheme();
  const [leaseA, setLeaseA] = useState({
    monthlyRent: 2000,
    annualIncrease: 3,
    leaseTerm: 36,
    securityDeposit: 2000,
  });

  const [leaseB, setLeaseB] = useState({
    monthlyRent: 1900,
    annualIncrease: 4,
    leaseTerm: 36,
    securityDeposit: 1900,
  });

  const [results, setResults] = useState({
    leaseATotalCost: 0,
    leaseBTotalCost: 0,
    difference: 0,
    recommendation: '',
  });

  useEffect(() => {
    const calculateTotalCost = (lease: typeof leaseA) => {
      let total = 0;
      let currentRent = lease.monthlyRent;
      
      for (let month = 1; month <= lease.leaseTerm; month++) {
        total += currentRent;
        if (month % 12 === 0) {
          currentRent = currentRent * (1 + lease.annualIncrease / 100);
        }
      }
      
      return total;
    };

    const leaseATotalCost = calculateTotalCost(leaseA);
    const leaseBTotalCost = calculateTotalCost(leaseB);
    const difference = Math.abs(leaseATotalCost - leaseBTotalCost);
    const recommendation = leaseATotalCost < leaseBTotalCost ? 'Lease A' : 'Lease B';

    setResults({
      leaseATotalCost,
      leaseBTotalCost,
      difference,
      recommendation,
    });
  }, [leaseA, leaseB]);

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);

  return (
    <CalculatorLayout
      title="Lease Analyzer"
      description="Side-by-side lease comparison tool with escalation clause analysis, total cost calculations, NPV adjustments, and time-value considerations. Perfect for tenants evaluating multiple lease options or landlords structuring competitive offers."
      icon={FileText}
      gradient="from-pink-600 to-pink-700"
      badge={`Best: ${results.recommendation}`}
      badgeColor="bg-pink-600"
      onBack={onBack}
    >
      {{
        calculator: (
          <div className="grid grid-cols-2 gap-8">
            <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
              <h3 className={`text-xl ${colors.text.primary} mb-6`}>Lease Option A</h3>
              <div className="space-y-4">
                <div>
                  <Label className={`${colors.text.secondary} mb-2 text-sm`}>Monthly Rent</Label>
                  <Input
                    type="number"
                    value={leaseA.monthlyRent}
                    onChange={(e) => setLeaseA(prev => ({ ...prev, monthlyRent: Number(e.target.value) }))}
                    className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                  />
                </div>
                <div>
                  <Label className={`${colors.text.secondary} mb-2 text-sm`}>Annual Increase %</Label>
                  <Input
                    type="number"
                    step="0.1"
                    value={leaseA.annualIncrease}
                    onChange={(e) => setLeaseA(prev => ({ ...prev, annualIncrease: Number(e.target.value) }))}
                    className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                  />
                </div>
                <div>
                  <Label className={`${colors.text.secondary} mb-2 text-sm`}>Lease Term (Months)</Label>
                  <Input
                    type="number"
                    value={leaseA.leaseTerm}
                    onChange={(e) => setLeaseA(prev => ({ ...prev, leaseTerm: Number(e.target.value) }))}
                    className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                  />
                </div>
                <div>
                  <Label className={`${colors.text.secondary} mb-2 text-sm`}>Security Deposit</Label>
                  <Input
                    type="number"
                    value={leaseA.securityDeposit}
                    onChange={(e) => setLeaseA(prev => ({ ...prev, securityDeposit: Number(e.target.value) }))}
                    className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                  />
                </div>
              </div>

              <div className={`mt-8 p-6 ${theme === 'dark' ? 'bg-slate-800/40' : 'bg-blue-50'} rounded-xl`}>
                <div className={`text-sm ${colors.text.secondary} mb-2`}>Total Cost Over Term</div>
                <div className="text-3xl text-pink-500 mb-2">{formatCurrency(results.leaseATotalCost)}</div>
                {results.recommendation === 'Lease A' && (
                  <div className="text-sm text-green-400 flex items-center gap-2">
                    ✓ Lower total cost
                  </div>
                )}
              </div>
            </Card>

            <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
              <h3 className={`text-xl ${colors.text.primary} mb-6`}>Lease Option B</h3>
              <div className="space-y-4">
                <div>
                  <Label className={`${colors.text.secondary} mb-2 text-sm`}>Monthly Rent</Label>
                  <Input
                    type="number"
                    value={leaseB.monthlyRent}
                    onChange={(e) => setLeaseB(prev => ({ ...prev, monthlyRent: Number(e.target.value) }))}
                    className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                  />
                </div>
                <div>
                  <Label className={`${colors.text.secondary} mb-2 text-sm`}>Annual Increase %</Label>
                  <Input
                    type="number"
                    step="0.1"
                    value={leaseB.annualIncrease}
                    onChange={(e) => setLeaseB(prev => ({ ...prev, annualIncrease: Number(e.target.value) }))}
                    className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                  />
                </div>
                <div>
                  <Label className={`${colors.text.secondary} mb-2 text-sm`}>Lease Term (Months)</Label>
                  <Input
                    type="number"
                    value={leaseB.leaseTerm}
                    onChange={(e) => setLeaseB(prev => ({ ...prev, leaseTerm: Number(e.target.value) }))}
                    className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                  />
                </div>
                <div>
                  <Label className={`${colors.text.secondary} mb-2 text-sm`}>Security Deposit</Label>
                  <Input
                    type="number"
                    value={leaseB.securityDeposit}
                    onChange={(e) => setLeaseB(prev => ({ ...prev, securityDeposit: Number(e.target.value) }))}
                    className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                  />
                </div>
              </div>

              <div className={`mt-8 p-6 ${theme === 'dark' ? 'bg-slate-800/40' : 'bg-blue-50'} rounded-xl`}>
                <div className={`text-sm ${colors.text.secondary} mb-2`}>Total Cost Over Term</div>
                <div className="text-3xl text-pink-500 mb-2">{formatCurrency(results.leaseBTotalCost)}</div>
                {results.recommendation === 'Lease B' && (
                  <div className="text-sm text-green-400 flex items-center gap-2">
                    ✓ Lower total cost
                  </div>
                )}
              </div>
            </Card>

            <Card className={`col-span-2 p-8 ${theme === 'dark' ? 'bg-gradient-to-br from-pink-900/20 to-pink-800/20 border-pink-700/30' : 'bg-pink-50 border-pink-200'}`}>
              <h3 className={`text-xl ${colors.text.primary} mb-4`}>Comparison Summary</h3>
              <div className="grid grid-cols-3 gap-6">
                <div>
                  <div className={`text-sm ${colors.text.secondary} mb-2`}>Recommended Option</div>
                  <div className="text-2xl text-pink-500">{results.recommendation}</div>
                </div>
                <div>
                  <div className={`text-sm ${colors.text.secondary} mb-2`}>Cost Difference</div>
                  <div className="text-2xl text-green-400">{formatCurrency(results.difference)}</div>
                </div>
                <div>
                  <div className={`text-sm ${colors.text.secondary} mb-2`}>Savings</div>
                  <div className={`text-2xl ${colors.text.primary}`}>
                    {((results.difference / Math.max(results.leaseATotalCost, results.leaseBTotalCost)) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
            </Card>
          </div>
        ),
        documentation: (
          <Card className={`p-8 ${colors.card} border ${colors.border.secondary} max-w-5xl`}>
            <h2 className={`text-3xl ${colors.text.primary} mb-6`}>Lease Analyzer Documentation</h2>
            <div className={`${colors.text.secondary} space-y-4 leading-relaxed`}>
              <p>Compare multiple lease options side-by-side, accounting for escalation clauses and total cost over the lease term.</p>
            </div>
          </Card>
        ),
      }}
    </CalculatorLayout>
  );
}
