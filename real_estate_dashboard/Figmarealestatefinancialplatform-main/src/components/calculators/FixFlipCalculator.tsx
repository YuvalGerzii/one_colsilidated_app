import { useState, useEffect } from 'react';
import { Home, TrendingUp, DollarSign, AlertTriangle, CheckCircle, XCircle, Target, Clock, Percent } from 'lucide-react';
import { CalculatorLayout } from './CalculatorLayout';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip, Cell, PieChart, Pie, Legend } from 'recharts';
import { useTheme } from '../../contexts/ThemeContext';

interface Inputs {
  purchasePrice: number;
  rehabCosts: number;
  afterRepairValue: number;
  holdingMonths: number;
  closingCostsBuy: number;
  closingCostsSell: number;
  financingType: 'cash' | 'loan';
  downPayment: number;
  loanInterestRate: number;
  monthlyUtilities: number;
  propertyTax: number;
  insurance: number;
}

interface Results {
  totalInvestment: number;
  totalHoldingCosts: number;
  sellingCosts: number;
  netProfit: number;
  roi: number;
  maxAllowableOffer: number;
  monthlyHoldingCost: number;
}

export function FixFlipCalculator({ onBack }: { onBack: () => void }) {
  const { theme, colors } = useTheme();
  const [inputs, setInputs] = useState<Inputs>({
    purchasePrice: 200000,
    rehabCosts: 50000,
    afterRepairValue: 300000,
    holdingMonths: 6,
    closingCostsBuy: 3,
    closingCostsSell: 6,
    financingType: 'loan',
    downPayment: 20,
    loanInterestRate: 8,
    monthlyUtilities: 200,
    propertyTax: 3000,
    insurance: 1200,
  });

  const [results, setResults] = useState<Results>({
    totalInvestment: 0,
    totalHoldingCosts: 0,
    sellingCosts: 0,
    netProfit: 0,
    roi: 0,
    maxAllowableOffer: 0,
    monthlyHoldingCost: 0,
  });

  const updateInput = (key: keyof Inputs, value: number | string) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  useEffect(() => {
    const closingCostsBuyAmount = inputs.purchasePrice * (inputs.closingCostsBuy / 100);
    
    let downPaymentAmount = 0;
    let loanAmount = 0;
    let totalInterest = 0;
    
    if (inputs.financingType === 'loan') {
      downPaymentAmount = inputs.purchasePrice * (inputs.downPayment / 100);
      loanAmount = inputs.purchasePrice - downPaymentAmount;
      const monthlyRate = inputs.loanInterestRate / 100 / 12;
      totalInterest = loanAmount * monthlyRate * inputs.holdingMonths;
    } else {
      downPaymentAmount = inputs.purchasePrice;
    }

    const monthlyPropertyTax = inputs.propertyTax / 12;
    const monthlyInsurance = inputs.insurance / 12;
    const monthlyHoldingCost = inputs.monthlyUtilities + monthlyPropertyTax + monthlyInsurance;
    const totalHoldingCosts = monthlyHoldingCost * inputs.holdingMonths + totalInterest;
    const sellingCosts = inputs.afterRepairValue * (inputs.closingCostsSell / 100);
    const totalInvestment = downPaymentAmount + closingCostsBuyAmount + inputs.rehabCosts + totalHoldingCosts;
    const netProfit = inputs.afterRepairValue - inputs.purchasePrice - closingCostsBuyAmount - inputs.rehabCosts - totalHoldingCosts - sellingCosts;
    const roi = (netProfit / totalInvestment) * 100;
    const maxAllowableOffer = inputs.afterRepairValue * 0.7 - inputs.rehabCosts;

    setResults({
      totalInvestment,
      totalHoldingCosts,
      sellingCosts,
      netProfit,
      roi,
      maxAllowableOffer,
      monthlyHoldingCost,
    });
  }, [inputs]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${value.toFixed(2)}%`;
  };

  const costBreakdownData = [
    { name: 'Purchase', value: inputs.purchasePrice, color: '#3b82f6' },
    { name: 'Rehab', value: inputs.rehabCosts, color: '#8b5cf6' },
    { name: 'Holding', value: results.totalHoldingCosts, color: '#f59e0b' },
    { name: 'Selling', value: results.sellingCosts, color: '#ef4444' },
  ];

  const profitData = [
    { name: 'Total Costs', value: results.totalInvestment, color: '#ef4444' },
    { name: 'ARV', value: inputs.afterRepairValue, color: '#10b981' },
  ];

  return (
    <CalculatorLayout
      title="Fix & Flip"
      description="Analyze short-term renovation projects with comprehensive financial modeling including MAO calculation (70% rule), renovation costs, holding expenses, financing scenarios, and exit strategies. Optimized for investors seeking 15-20% ROI targets."
      icon={Home}
      gradient="from-blue-600 to-blue-700"
      badge={results.roi > 15 ? "Excellent Deal" : results.roi > 0 ? "Profitable" : "Review Required"}
      badgeColor={results.roi > 15 ? "bg-green-600" : results.roi > 0 ? "bg-blue-600" : "bg-orange-600"}
      onBack={onBack}
    >
      {{
        calculator: (
          <div className="grid grid-cols-12 gap-6">
            {/* Left Column - Inputs (7 columns) */}
            <div className="col-span-7 space-y-6">
              {/* Purchase Details */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-blue-500/10 rounded-xl flex items-center justify-center border border-blue-500/20">
                    <DollarSign className="w-5 h-5 text-blue-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Purchase Details</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="purchasePrice" className={`${colors.text.secondary} mb-2 text-sm`}>Purchase Price</Label>
                    <Input
                      id="purchasePrice"
                      type="number"
                      value={inputs.purchasePrice}
                      onChange={(e) => updateInput('purchasePrice', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                  <div>
                    <Label htmlFor="closingCostsBuy" className={`${colors.text.secondary} mb-2 text-sm`}>Closing Costs (Buy) %</Label>
                    <Input
                      id="closingCostsBuy"
                      type="number"
                      value={inputs.closingCostsBuy}
                      onChange={(e) => updateInput('closingCostsBuy', Number(e.target.value))}
                      step="0.1"
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-blue-500/50 focus:ring-blue-500/20`}
                    />
                  </div>
                </div>
              </Card>

              {/* Renovation & ARV */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-purple-500/10 rounded-xl flex items-center justify-center border border-purple-500/20">
                    <Home className="w-5 h-5 text-purple-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Renovation & ARV</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="rehabCosts" className={`${colors.text.secondary} mb-2 text-sm`}>Rehab/Renovation Costs</Label>
                    <Input
                      id="rehabCosts"
                      type="number"
                      value={inputs.rehabCosts}
                      onChange={(e) => updateInput('rehabCosts', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-purple-500/50 focus:ring-purple-500/20`}
                    />
                  </div>
                  <div>
                    <Label htmlFor="afterRepairValue" className={`${colors.text.secondary} mb-2 text-sm`}>After Repair Value (ARV)</Label>
                    <Input
                      id="afterRepairValue"
                      type="number"
                      value={inputs.afterRepairValue}
                      onChange={(e) => updateInput('afterRepairValue', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-purple-500/50 focus:ring-purple-500/20`}
                    />
                  </div>
                  <div className="col-span-2">
                    <Label htmlFor="closingCostsSell" className={`${colors.text.secondary} mb-2 text-sm`}>Closing Costs (Sell) %</Label>
                    <Input
                      id="closingCostsSell"
                      type="number"
                      value={inputs.closingCostsSell}
                      onChange={(e) => updateInput('closingCostsSell', Number(e.target.value))}
                      step="0.1"
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-purple-500/50 focus:ring-purple-500/20`}
                    />
                  </div>
                </div>
              </Card>

              {/* Financing */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-green-500/10 rounded-xl flex items-center justify-center border border-green-500/20">
                    <Percent className="w-5 h-5 text-green-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Financing Structure</h3>
                </div>
                <div className="space-y-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-3 text-sm`}>Financing Type</Label>
                    <div className="grid grid-cols-2 gap-3 mt-2">
                      <button
                        onClick={() => updateInput('financingType', 'cash')}
                        className={`h-11 rounded-xl border-2 text-sm transition-all relative overflow-hidden ${
                          inputs.financingType === 'cash'
                            ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white border-blue-600 shadow-lg shadow-blue-500/20'
                            : `${theme === 'dark' ? 'bg-slate-900/50 text-slate-400 border-slate-700/50' : 'bg-white text-slate-600 border-blue-200'} hover:border-blue-500/50`
                        }`}
                      >
                        Cash Purchase
                      </button>
                      <button
                        onClick={() => updateInput('financingType', 'loan')}
                        className={`h-11 rounded-xl border-2 text-sm transition-all relative overflow-hidden ${
                          inputs.financingType === 'loan'
                            ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white border-blue-600 shadow-lg shadow-blue-500/20'
                            : `${theme === 'dark' ? 'bg-slate-900/50 text-slate-400 border-slate-700/50' : 'bg-white text-slate-600 border-blue-200'} hover:border-blue-500/50`
                        }`}
                      >
                        Financed
                      </button>
                    </div>
                  </div>
                  {inputs.financingType === 'loan' && (
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="downPayment" className={`${colors.text.secondary} mb-2 text-sm`}>Down Payment %</Label>
                        <Input
                          id="downPayment"
                          type="number"
                          value={inputs.downPayment}
                          onChange={(e) => updateInput('downPayment', Number(e.target.value))}
                          step="1"
                          className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                        />
                      </div>
                      <div>
                        <Label htmlFor="loanInterestRate" className={`${colors.text.secondary} mb-2 text-sm`}>Interest Rate %</Label>
                        <Input
                          id="loanInterestRate"
                          type="number"
                          value={inputs.loanInterestRate}
                          onChange={(e) => updateInput('loanInterestRate', Number(e.target.value))}
                          step="0.1"
                          className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-green-500/50 focus:ring-green-500/20`}
                        />
                      </div>
                    </div>
                  )}
                </div>
              </Card>

              {/* Holding Costs */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-orange-500/10 rounded-xl flex items-center justify-center border border-orange-500/20">
                    <Clock className="w-5 h-5 text-orange-400" />
                  </div>
                  <h3 className={`text-lg ${colors.text.primary}`}>Holding Costs & Timeline</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="holdingMonths" className={`${colors.text.secondary} mb-2 text-sm`}>Holding Period (Months)</Label>
                    <Input
                      id="holdingMonths"
                      type="number"
                      value={inputs.holdingMonths}
                      onChange={(e) => updateInput('holdingMonths', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-orange-500/50 focus:ring-orange-500/20`}
                    />
                  </div>
                  <div>
                    <Label htmlFor="monthlyUtilities" className={`${colors.text.secondary} mb-2 text-sm`}>Monthly Utilities</Label>
                    <Input
                      id="monthlyUtilities"
                      type="number"
                      value={inputs.monthlyUtilities}
                      onChange={(e) => updateInput('monthlyUtilities', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-orange-500/50 focus:ring-orange-500/20`}
                    />
                  </div>
                  <div>
                    <Label htmlFor="propertyTax" className={`${colors.text.secondary} mb-2 text-sm`}>Annual Property Tax</Label>
                    <Input
                      id="propertyTax"
                      type="number"
                      value={inputs.propertyTax}
                      onChange={(e) => updateInput('propertyTax', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-orange-500/50 focus:ring-orange-500/20`}
                    />
                  </div>
                  <div>
                    <Label htmlFor="insurance" className={`${colors.text.secondary} mb-2 text-sm`}>Annual Insurance</Label>
                    <Input
                      id="insurance"
                      type="number"
                      value={inputs.insurance}
                      onChange={(e) => updateInput('insurance', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary} focus:border-orange-500/50 focus:ring-orange-500/20`}
                    />
                  </div>
                </div>
              </Card>
            </div>

            {/* Right Column - Results (5 columns) */}
            <div className="col-span-5 space-y-6">
              {/* MAO Card */}
              <Card className="p-8 bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 border-0 shadow-2xl shadow-blue-500/20 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
                <div className="absolute top-0 right-0 w-48 h-48 bg-white/5 rounded-full blur-3xl -mr-24 -mt-24" />
                <div className="relative z-10">
                  <div className="flex items-center gap-2 mb-3">
                    <Target className="w-5 h-5 text-blue-200" />
                    <h3 className="text-sm uppercase tracking-wider text-blue-200">Maximum Allowable Offer</h3>
                  </div>
                  <div className="text-5xl text-white mb-3">{formatCurrency(results.maxAllowableOffer)}</div>
                  <p className="text-sm text-blue-100 leading-relaxed mb-4">
                    Based on the 70% rule: 70% of ARV minus rehab costs
                  </p>
                  {inputs.purchasePrice > results.maxAllowableOffer && (
                    <div className="mt-4 p-4 bg-orange-500/20 backdrop-blur-sm rounded-xl border border-orange-400/30 text-sm flex items-start gap-3">
                      <AlertTriangle className="w-5 h-5 text-orange-300 flex-shrink-0 mt-0.5" />
                      <div>
                        <div className="text-white mb-1">Purchase price exceeds MAO</div>
                        <div className="text-orange-100">Overpayment: {formatCurrency(inputs.purchasePrice - results.maxAllowableOffer)}</div>
                      </div>
                    </div>
                  )}
                </div>
              </Card>

              {/* Profitability */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Profitability Metrics</h3>
                <div className="space-y-6">
                  <div>
                    <div className="flex justify-between items-end mb-3">
                      <span className="text-sm text-slate-400">Net Profit</span>
                      <span className={`text-3xl ${results.netProfit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {formatCurrency(results.netProfit)}
                      </span>
                    </div>
                    <div className="w-full bg-slate-700/30 rounded-full h-2 overflow-hidden">
                      <div
                        className={`h-2 rounded-full transition-all ${results.netProfit >= 0 ? 'bg-gradient-to-r from-green-500 to-green-600' : 'bg-gradient-to-r from-red-500 to-red-600'}`}
                        style={{ width: `${Math.min(Math.abs((results.netProfit / inputs.afterRepairValue) * 100), 100)}%` }}
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between items-end mb-3">
                      <span className="text-sm text-slate-400">Return on Investment (ROI)</span>
                      <span className={`text-3xl ${results.roi >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {formatPercent(results.roi)}
                      </span>
                    </div>
                    <div className="w-full bg-slate-700/30 rounded-full h-2 overflow-hidden">
                      <div
                        className={`h-2 rounded-full transition-all ${results.roi >= 0 ? 'bg-gradient-to-r from-green-500 to-green-600' : 'bg-gradient-to-r from-red-500 to-red-600'}`}
                        style={{ width: `${Math.min(Math.abs(results.roi), 100)}%` }}
                      />
                    </div>
                    <div className="flex justify-between mt-2 text-xs text-slate-500">
                      <span>0%</span>
                      <span>Target: 15%</span>
                      <span>50%</span>
                    </div>
                  </div>
                </div>
              </Card>

              {/* Investment Summary */}
              <Card className="p-6 bg-gradient-to-br from-slate-800/40 to-slate-900/40 border-slate-700/50 backdrop-blur-sm">
                <h3 className="text-lg text-white mb-6">Investment Summary</h3>
                <div className="space-y-4">
                  {[
                    { label: 'Total Investment', value: results.totalInvestment, icon: DollarSign, color: 'text-blue-400' },
                    { label: 'Holding Costs', value: results.totalHoldingCosts, icon: Clock, color: 'text-purple-400' },
                    { label: 'Selling Costs', value: results.sellingCosts, icon: TrendingUp, color: 'text-orange-400' },
                    { label: 'Monthly Holding', value: results.monthlyHoldingCost, icon: DollarSign, color: 'text-green-400' },
                  ].map((item) => (
                    <div key={item.label} className="flex items-center justify-between pb-4 border-b border-slate-700/50 last:border-0">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-slate-700/30 rounded-lg flex items-center justify-center">
                          <item.icon className={`w-4 h-4 ${item.color}`} />
                        </div>
                        <span className="text-sm text-slate-400">{item.label}</span>
                      </div>
                      <span className="text-white">{formatCurrency(item.value)}</span>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Deal Analysis */}
              <Card className={`p-6 border-2 shadow-xl backdrop-blur-sm ${
                results.roi > 15 
                  ? 'bg-gradient-to-br from-green-900/20 to-green-800/20 border-green-700/30' 
                  : results.roi > 0 
                  ? 'bg-gradient-to-br from-blue-900/20 to-blue-800/20 border-blue-700/30'
                  : 'bg-gradient-to-br from-orange-900/20 to-orange-800/20 border-orange-700/30'
              }`}>
                <div className="flex items-start gap-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                    results.roi > 15 ? 'bg-green-500/20 border border-green-500/30' :
                    results.roi > 0 ? 'bg-blue-500/20 border border-blue-500/30' :
                    'bg-orange-500/20 border border-orange-500/30'
                  }`}>
                    {results.roi > 15 ? (
                      <CheckCircle className="w-6 h-6 text-green-400" />
                    ) : results.roi > 0 ? (
                      <CheckCircle className="w-6 h-6 text-blue-400" />
                    ) : (
                      <XCircle className="w-6 h-6 text-orange-400" />
                    )}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg text-white mb-3">Deal Analysis</h3>
                    <div className="space-y-2 text-sm leading-relaxed">
                      {results.roi > 15 ? (
                        <p className="text-green-300">
                          ✓ <strong>Excellent opportunity</strong> with {formatPercent(results.roi)} ROI. This significantly exceeds typical fix & flip targets of 15-20%.
                        </p>
                      ) : results.roi > 0 ? (
                        <p className="text-blue-300">
                          ✓ <strong>Profitable deal</strong> with {formatPercent(results.roi)} ROI. Consider if this meets your investment criteria and risk tolerance.
                        </p>
                      ) : (
                        <p className="text-orange-300">
                          ⚠ <strong>Negative returns projected.</strong> Consider negotiating a lower purchase price, reducing renovation scope, or passing on this opportunity.
                        </p>
                      )}
                      <p className="text-slate-400">
                        Your maximum allowable offer is <strong className="text-white">{formatCurrency(results.maxAllowableOffer)}</strong> based on the industry-standard 70% rule.
                      </p>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        ),
        charts: (
          <div className="grid grid-cols-2 gap-8">
            <Card className="p-8 bg-gradient-to-br from-slate-800/40 to-slate-900/40 border-slate-700/50 backdrop-blur-sm">
              <h3 className="text-xl text-white mb-6">Cost Breakdown</h3>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={costBreakdownData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.2} vertical={false} />
                  <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                  <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '12px',
                    }}
                    formatter={(value: number) => formatCurrency(value)}
                  />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                    {costBreakdownData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </Card>

            <Card className="p-8 bg-gradient-to-br from-slate-800/40 to-slate-900/40 border-slate-700/50 backdrop-blur-sm">
              <h3 className="text-xl text-white mb-6">Profit vs Investment</h3>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={profitData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.2} vertical={false} />
                  <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#94a3b8' }} />
                  <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '12px',
                    }}
                    formatter={(value: number) => formatCurrency(value)}
                  />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                    {profitData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </div>
        ),
        documentation: (
          <Card className="p-8 bg-gradient-to-br from-slate-800/40 to-slate-900/40 border-slate-700/50 backdrop-blur-sm max-w-5xl">
            <h2 className="text-3xl text-white mb-6">Fix & Flip Model Documentation</h2>
            <div className="prose prose-invert max-w-none">
              <div className="text-slate-300 space-y-6 leading-relaxed">
                <div>
                  <h3 className="text-2xl text-white mt-8 mb-4">Overview</h3>
                  <p>
                    The Fix & Flip financial model is designed for real estate investors analyzing short-term renovation projects. 
                    This model incorporates industry-standard metrics and best practices to evaluate acquisition, renovation, 
                    holding, and exit strategies.
                  </p>
                </div>
                
                <div>
                  <h3 className="text-2xl text-white mt-8 mb-4">The 70% Rule</h3>
                  <p>
                    The Maximum Allowable Offer (MAO) is calculated using the widely-adopted 70% rule in real estate investing:
                  </p>
                  <div className="p-5 bg-blue-900/20 rounded-xl border border-blue-700/30 my-4">
                    <p className="text-blue-200 text-lg mb-2">
                      <strong>MAO Formula:</strong> (ARV × 0.70) - Rehab Costs
                    </p>
                    <p className="text-sm text-blue-300">
                      This ensures adequate profit margin while accounting for holding costs, selling expenses, and market fluctuations.
                    </p>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-2xl text-white mt-8 mb-4">Key Financial Metrics</h3>
                  <div className="space-y-4">
                    <div className="p-4 bg-slate-700/30 rounded-xl">
                      <strong className="text-white">Return on Investment (ROI)</strong>
                      <p className="mt-2 text-slate-400">
                        Measures profitability as a percentage of total capital invested. Calculated as (Net Profit / Total Investment) × 100. 
                        Target ROI for fix & flip projects typically ranges from 15-20% minimum.
                      </p>
                    </div>
                    <div className="p-4 bg-slate-700/30 rounded-xl">
                      <strong className="text-white">Net Profit</strong>
                      <p className="mt-2 text-slate-400">
                        Total profit after all costs including purchase price, renovation, holding costs, financing charges, and selling expenses.
                      </p>
                    </div>
                    <div className="p-4 bg-slate-700/30 rounded-xl">
                      <strong className="text-white">After Repair Value (ARV)</strong>
                      <p className="mt-2 text-slate-400">
                        Estimated market value of the property after all renovations are complete. Should be based on comparable sales data.
                      </p>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-2xl text-white mt-8 mb-4">Best Practices</h3>
                  <ul className="space-y-3 text-slate-300">
                    <li className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                      <span>Maintain a contingency budget of 10-20% for unexpected renovation costs and timeline extensions</span>
                    </li>
                    <li className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                      <span>Target a minimum ROI of 15-20% to justify the risk and effort of fix & flip projects</span>
                    </li>
                    <li className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                      <span>Never exceed the Maximum Allowable Offer unless you have a specific value-add strategy</span>
                    </li>
                    <li className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                      <span>Account for seasonal market fluctuations when estimating your holding period and sale timeline</span>
                    </li>
                    <li className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                      <span>Obtain multiple contractor bids and professional property inspections before finalizing rehab estimates</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </Card>
        ),
      }}
    </CalculatorLayout>
  );
}