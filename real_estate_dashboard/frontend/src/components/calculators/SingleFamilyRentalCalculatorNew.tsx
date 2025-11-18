import { useState, useEffect } from 'react';
import { Home, TrendingUp, DollarSign, Wrench, Percent, Calendar, Building, CheckCircle } from 'lucide-react';
import { CalculatorLayout } from './CalculatorLayout';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Area,
  AreaChart,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import { SingleFamilyRentalInputs, SingleFamilyRentalResults, YearProjection } from '../../types/calculatorTypes';
import {
  formatCurrency,
  formatPercent,
  annuityPayment,
  remainingBalance,
  calculateIRR,
  saveToLocalStorage,
} from '../../utils/calculatorUtils';

const DEFAULT_INPUTS: SingleFamilyRentalInputs = {
  // Property Profile
  projectName: 'Maple Street Rental',
  location: 'Charlotte, NC',
  analyst: '',
  propertyType: 'Single-Family Residence',
  squareFootage: 1600,
  bedrooms: 3,
  bathrooms: 2,
  yearBuilt: 1990,

  // Acquisition & Rehab
  purchasePrice: 280000,
  closingCosts: 5000,
  renovationCosts: 30000,
  arv: 340000,
  holdingCostsMonthly: 600,
  holdingPeriodMonths: 6,

  // Income & Growth
  monthlyRent: 2200,
  otherIncomeMonthly: 0,
  rentGrowthRate: 3,
  vacancyRate: 5,
  appreciationRate: 3,

  // Operating Expenses
  managementPct: 8,
  maintenancePct: 8,
  propertyTaxAnnual: 3500,
  insuranceAnnual: 1500,
  utilitiesMonthly: 150,
  hoaMonthly: 0,
  otherExpensesMonthly: 50,
  capexReserveMonthly: 150,
  expenseGrowthRate: 2.5,

  // Financing & Disposition
  downPaymentPct: 25,
  interestRate: 6.5,
  loanTermYears: 30,
  refinanceLtv: 75,
  refinanceRate: 6,
  refinanceTermYears: 30,
  refinanceYear: 0,
  refinanceCostPct: 3,
  sellingCostPct: 7,

  // Holding Strategy
  holdPeriodYears: 10,
};

export function SingleFamilyRentalCalculatorNew() {
  const navigate = useNavigate();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [inputs, setInputs] = useState<SingleFamilyRentalInputs>(DEFAULT_INPUTS);
  const [results, setResults] = useState<SingleFamilyRentalResults>({
    loanAmount: 0,
    downPayment: 0,
    equityInvested: 0,
    totalProjectCost: 0,
    annualDebtService: 0,
    year1GrossRent: 0,
    year1Vacancy: 0,
    year1EffectiveIncome: 0,
    year1OperatingExpenses: 0,
    year1Noi: 0,
    year1CashFlow: 0,
    capRate: 0,
    cashOnCash: 0,
    dscr: 0,
    onePercentRule: 0,
    exitValue: 0,
    netSaleProceeds: 0,
    loanBalanceExit: 0,
    irr: 0,
    equityMultiple: 0,
    cashOutRefi: 0,
    flipGrossProfit: 0,
    flipRoi: 0,
    flipProfitMargin: 0,
    brrrCashOut: 0,
    brrrYear2CashFlow: 0,
    holdYear10CashFlow: 0,
    holdMonthlyCashFlow: 0,
    projections: [],
    cashFlows: [],
    cumulativeCashFlows: [],
  });

  const updateInput = <K extends keyof SingleFamilyRentalInputs>(
    key: K,
    value: SingleFamilyRentalInputs[K]
  ) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  // ALL THE COMPLEX CALCULATION LOGIC (UNCHANGED)
  useEffect(() => {
    // Calculate derived finance fields
    const downPayment = inputs.purchasePrice * (inputs.downPaymentPct / 100);
    const loanAmount = inputs.purchasePrice - downPayment;
    const equityInvested = downPayment + inputs.closingCosts + inputs.renovationCosts;
    const totalProjectCost = inputs.purchasePrice + inputs.closingCosts + inputs.renovationCosts;
    const monthlyPayment = annuityPayment(loanAmount, inputs.interestRate / 100, inputs.loanTermYears);
    const annualDebtService = monthlyPayment * 12;

    // Build 10-year projections
    const years = 10;
    const rentGrowth = inputs.rentGrowthRate / 100;
    const expenseGrowth = inputs.expenseGrowthRate / 100;
    const appreciation = inputs.appreciationRate / 100;
    const refinanceYear = inputs.refinanceYear;
    const performRefi = inputs.refinanceLtv > 0 && refinanceYear > 0;

    const projections: YearProjection[] = [];
    const cashFlows: number[] = [-equityInvested];
    let cashOutRefi = 0;

    let currentPrincipal = loanAmount;
    let currentRate = inputs.interestRate / 100;
    let currentTerm = inputs.loanTermYears;
    let paymentsMade = 0;
    let refiExecuted = false;

    const debtServices: number[] = [];
    const loanBalances: number[] = [];

    // Calculate debt service and loan balances for each year
    for (let year = 1; year <= years; year++) {
      const annualPayment = annuityPayment(currentPrincipal, currentRate, currentTerm) * 12;
      debtServices.push(annualPayment);
      paymentsMade += 12;
      let balanceEnd = remainingBalance(currentPrincipal, currentRate, currentTerm, paymentsMade);

      // Handle refinance
      if (performRefi && !refiExecuted && year === refinanceYear) {
        const propertyValue = inputs.arv * Math.pow(1 + appreciation, year);
        const newPrincipal = propertyValue * (inputs.refinanceLtv / 100);
        const refinanceCosts = newPrincipal * (inputs.refinanceCostPct / 100);
        cashOutRefi = newPrincipal - balanceEnd - refinanceCosts;
        currentPrincipal = newPrincipal;
        currentRate = inputs.refinanceRate / 100;
        currentTerm = inputs.refinanceTermYears;
        paymentsMade = 0;
        refiExecuted = true;
        balanceEnd = currentPrincipal;
      }

      loanBalances.push(balanceEnd);
    }

    let cumulativeCashFlow = 0;

    for (let year = 1; year <= years; year++) {
      const rentAnnual = inputs.monthlyRent * Math.pow(1 + rentGrowth, year - 1) * 12;
      const otherIncome = inputs.otherIncomeMonthly * Math.pow(1 + rentGrowth, year - 1) * 12;
      const vacancyLoss = rentAnnual * (inputs.vacancyRate / 100);
      const effectiveGrossIncome = rentAnnual - vacancyLoss + otherIncome;

      const mgmtExpense = rentAnnual * (inputs.managementPct / 100);
      const maintenanceExpense = rentAnnual * (inputs.maintenancePct / 100);
      const propertyTaxAnnual = inputs.propertyTaxAnnual * Math.pow(1 + expenseGrowth, year - 1);
      const insuranceAnnual = inputs.insuranceAnnual * Math.pow(1 + expenseGrowth, year - 1);
      const utilities = inputs.utilitiesMonthly * Math.pow(1 + expenseGrowth, year - 1) * 12;
      const hoa = inputs.hoaMonthly * Math.pow(1 + expenseGrowth, year - 1) * 12;
      const otherExpense = inputs.otherExpensesMonthly * Math.pow(1 + expenseGrowth, year - 1) * 12;
      const capex = inputs.capexReserveMonthly * Math.pow(1 + expenseGrowth, year - 1) * 12;

      const operatingExpenses =
        mgmtExpense +
        maintenanceExpense +
        propertyTaxAnnual +
        insuranceAnnual +
        utilities +
        hoa +
        otherExpense +
        capex;

      const noi = effectiveGrossIncome - operatingExpenses;
      const debtService = debtServices[year - 1];

      let annualCashFlow = noi - debtService;
      if (performRefi && year === refinanceYear) {
        annualCashFlow += cashOutRefi;
      }

      const propertyValue = inputs.arv * Math.pow(1 + appreciation, year);
      const loanBalance = loanBalances[year - 1];
      const equity = propertyValue - loanBalance;

      cumulativeCashFlow += annualCashFlow;

      projections.push({
        year,
        grossRent: rentAnnual,
        vacancy: vacancyLoss,
        otherIncome,
        effectiveGrossIncome,
        operatingExpenses,
        noi,
        debtService,
        cashFlow: annualCashFlow,
        loanBalance,
        propertyValue,
        equity,
        cumulativeCashFlow,
      });

      cashFlows.push(annualCashFlow);
    }

    // Exit calculations
    const holdYears = inputs.holdPeriodYears;
    const exitValue = inputs.arv * Math.pow(1 + appreciation, holdYears);
    const sellingCosts = exitValue * (inputs.sellingCostPct / 100);
    const loanBalanceExit = loanBalances[holdYears - 1];
    const netSaleProceeds = exitValue - sellingCosts - loanBalanceExit;

    // Add net sale proceeds to final cash flow for IRR calculation
    const cashFlowsWithExit = [...cashFlows];
    cashFlowsWithExit[holdYears] += netSaleProceeds;

    const irrValue = calculateIRR(cashFlowsWithExit);
    const equityMultiple = cashFlowsWithExit.slice(1).reduce((sum, cf) => sum + cf, 0) / equityInvested;

    // Year 1 metrics
    const year1 = projections[0];
    const capRate = year1.noi / totalProjectCost;
    const cashOnCash = year1.cashFlow / equityInvested;
    const dscr = year1.noi / annualDebtService;
    const onePercentRule = (inputs.monthlyRent / inputs.purchasePrice) * 100;

    // Exit strategy comparison
    const holdingCosts = inputs.holdingCostsMonthly * inputs.holdingPeriodMonths;
    const allInCost = inputs.purchasePrice + inputs.closingCosts + inputs.renovationCosts + holdingCosts;
    const sellingCostsFlip = inputs.arv * (inputs.sellingCostPct / 100);
    const flipGrossProfit = inputs.arv - sellingCostsFlip - allInCost;
    const flipRoi = (flipGrossProfit / equityInvested) * 100;
    const flipProfitMargin = (flipGrossProfit / inputs.arv) * 100;

    const brrrCashOut = cashOutRefi;
    const brrrYear2CashFlow = projections[Math.min(1, projections.length - 1)].cashFlow;

    const holdYear10CashFlow = projections[projections.length - 1].cashFlow;
    const holdMonthlyCashFlow = holdYear10CashFlow / 12;

    const cumulativeCashFlows = projections.map((p) => p.cumulativeCashFlow);

    setResults({
      loanAmount,
      downPayment,
      equityInvested,
      totalProjectCost,
      annualDebtService,
      year1GrossRent: year1.grossRent,
      year1Vacancy: year1.vacancy,
      year1EffectiveIncome: year1.effectiveGrossIncome,
      year1OperatingExpenses: year1.operatingExpenses,
      year1Noi: year1.noi,
      year1CashFlow: year1.cashFlow,
      capRate,
      cashOnCash,
      dscr,
      onePercentRule,
      exitValue,
      netSaleProceeds,
      loanBalanceExit,
      irr: irrValue * 100,
      equityMultiple,
      cashOutRefi,
      flipGrossProfit,
      flipRoi,
      flipProfitMargin,
      brrrCashOut,
      brrrYear2CashFlow,
      holdYear10CashFlow,
      holdMonthlyCashFlow,
      projections,
      cashFlows: cashFlowsWithExit,
      cumulativeCashFlows,
    });
  }, [inputs]);

  const handleSave = () => {
    saveToLocalStorage('single-family-rental', {
      projectName: inputs.projectName,
      location: inputs.location,
      inputs,
      results,
    });
  };

  const colors = {
    card: isDark ? 'bg-slate-900/60' : 'bg-white',
    border: {
      primary: isDark ? 'border-slate-700' : 'border-slate-200',
      secondary: isDark ? 'border-slate-700/50' : 'border-slate-200',
    },
    text: {
      primary: isDark ? 'text-white' : 'text-slate-900',
      secondary: isDark ? 'text-slate-400' : 'text-slate-600',
    },
    input: isDark ? 'bg-slate-800/50' : 'bg-white',
  };

  const cashFlowData = results.projections.map((p) => ({
    year: p.year,
    NOI: p.noi,
    'Debt Service': p.debtService,
    'Cash Flow': p.cashFlow,
  }));

  const equityData = results.projections.map((p) => ({
    year: p.year,
    'Property Value': p.propertyValue,
    Equity: p.equity,
    'Loan Balance': p.loanBalance,
  }));

  const exitComparisonData = [
    { strategy: 'Flip', value: results.flipGrossProfit },
    { strategy: 'BRRRR', value: results.brrrCashOut },
    { strategy: 'Hold', value: results.netSaleProceeds },
  ];

  return (
    <CalculatorLayout
      title={inputs.projectName}
      description="Comprehensive rental property analysis with 10-year cash flow projections, multiple exit strategies (Flip, BRRRR, Hold), and refinancing scenarios. Includes detailed operating expense tracking and institutional-grade metrics."
      icon={Home}
      gradient="from-green-600 to-green-700"
      badge={results.irr >= 20 ? "Excellent Returns" : results.irr >= 15 ? "Strong Returns" : results.irr >= 10 ? "Good Returns" : "Review Required"}
      badgeColor={results.irr >= 20 ? "bg-green-600" : results.irr >= 15 ? "bg-blue-600" : results.irr >= 10 ? "bg-orange-600" : "bg-red-600"}
      onBack={() => navigate('/real-estate-tools')}
    >
      {{
        calculator: (
          <div className="grid grid-cols-12 gap-6">
            {/* Left Column - Inputs */}
            <div className="col-span-7 space-y-6">
              {/* Property Profile */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-indigo-500/10 rounded-xl flex items-center justify-center border border-indigo-500/20">
                    <Home className="w-5 h-5 text-indigo-400" />
                  </div>
                  <div>
                    <h3 className={`text-lg ${colors.text.primary}`}>Property Profile</h3>
                    <p className={`text-xs ${colors.text.secondary}`}>Property details and characteristics</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Property Name</Label>
                    <Input
                      value={inputs.projectName}
                      onChange={(e) => updateInput('projectName', e.target.value)}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Location</Label>
                    <Input
                      value={inputs.location}
                      onChange={(e) => updateInput('location', e.target.value)}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Square Footage</Label>
                    <Input
                      type="number"
                      value={inputs.squareFootage}
                      onChange={(e) => updateInput('squareFootage', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Year Built</Label>
                    <Input
                      type="number"
                      value={inputs.yearBuilt}
                      onChange={(e) => updateInput('yearBuilt', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Bedrooms</Label>
                    <Input
                      type="number"
                      value={inputs.bedrooms}
                      onChange={(e) => updateInput('bedrooms', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Bathrooms</Label>
                    <Input
                      type="number"
                      step="0.5"
                      value={inputs.bathrooms}
                      onChange={(e) => updateInput('bathrooms', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>

              {/* Acquisition & Rehab */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-blue-500/10 rounded-xl flex items-center justify-center border border-blue-500/20">
                    <DollarSign className="w-5 h-5 text-blue-400" />
                  </div>
                  <div>
                    <h3 className={`text-lg ${colors.text.primary}`}>Acquisition & Rehab</h3>
                    <p className={`text-xs ${colors.text.secondary}`}>Purchase details and renovation costs</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Purchase Price</Label>
                    <Input
                      type="number"
                      value={inputs.purchasePrice}
                      onChange={(e) => updateInput('purchasePrice', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Closing Costs</Label>
                    <Input
                      type="number"
                      value={inputs.closingCosts}
                      onChange={(e) => updateInput('closingCosts', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Renovation Budget</Label>
                    <Input
                      type="number"
                      value={inputs.renovationCosts}
                      onChange={(e) => updateInput('renovationCosts', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>After Repair Value (ARV)</Label>
                    <Input
                      type="number"
                      value={inputs.arv}
                      onChange={(e) => updateInput('arv', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>

              {/* Income & Growth */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-green-500/10 rounded-xl flex items-center justify-center border border-green-500/20">
                    <TrendingUp className="w-5 h-5 text-green-400" />
                  </div>
                  <div>
                    <h3 className={`text-lg ${colors.text.primary}`}>Income & Growth</h3>
                    <p className={`text-xs ${colors.text.secondary}`}>Rental income and appreciation assumptions</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Monthly Rent</Label>
                    <Input
                      type="number"
                      value={inputs.monthlyRent}
                      onChange={(e) => updateInput('monthlyRent', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Other Monthly Income</Label>
                    <Input
                      type="number"
                      value={inputs.otherIncomeMonthly}
                      onChange={(e) => updateInput('otherIncomeMonthly', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Rent Growth %</Label>
                    <Input
                      type="number"
                      step="0.25"
                      value={inputs.rentGrowthRate}
                      onChange={(e) => updateInput('rentGrowthRate', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Vacancy Rate %</Label>
                    <Input
                      type="number"
                      step="0.25"
                      value={inputs.vacancyRate}
                      onChange={(e) => updateInput('vacancyRate', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div className="col-span-2">
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Appreciation %</Label>
                    <Input
                      type="number"
                      step="0.25"
                      value={inputs.appreciationRate}
                      onChange={(e) => updateInput('appreciationRate', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>

              {/* Operating Expenses */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-orange-500/10 rounded-xl flex items-center justify-center border border-orange-500/20">
                    <Wrench className="w-5 h-5 text-orange-400" />
                  </div>
                  <div>
                    <h3 className={`text-lg ${colors.text.primary}`}>Operating Expenses</h3>
                    <p className={`text-xs ${colors.text.secondary}`}>Monthly and annual operating costs</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Management Fee %</Label>
                    <Input
                      type="number"
                      step="0.25"
                      value={inputs.managementPct}
                      onChange={(e) => updateInput('managementPct', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Maintenance %</Label>
                    <Input
                      type="number"
                      step="0.25"
                      value={inputs.maintenancePct}
                      onChange={(e) => updateInput('maintenancePct', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Property Tax (Annual)</Label>
                    <Input
                      type="number"
                      value={inputs.propertyTaxAnnual}
                      onChange={(e) => updateInput('propertyTaxAnnual', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Insurance (Annual)</Label>
                    <Input
                      type="number"
                      value={inputs.insuranceAnnual}
                      onChange={(e) => updateInput('insuranceAnnual', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>CapEx Reserve (Monthly)</Label>
                    <Input
                      type="number"
                      value={inputs.capexReserveMonthly}
                      onChange={(e) => updateInput('capexReserveMonthly', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Expense Growth %</Label>
                    <Input
                      type="number"
                      step="0.25"
                      value={inputs.expenseGrowthRate}
                      onChange={(e) => updateInput('expenseGrowthRate', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>

              {/* Financing */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-purple-500/10 rounded-xl flex items-center justify-center border border-purple-500/20">
                    <Building className="w-5 h-5 text-purple-400" />
                  </div>
                  <div>
                    <h3 className={`text-lg ${colors.text.primary}`}>Financing & Disposition</h3>
                    <p className={`text-xs ${colors.text.secondary}`}>Loan terms and exit strategy</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Down Payment %</Label>
                    <Input
                      type="number"
                      value={inputs.downPaymentPct}
                      onChange={(e) => updateInput('downPaymentPct', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Interest Rate %</Label>
                    <Input
                      type="number"
                      step="0.25"
                      value={inputs.interestRate}
                      onChange={(e) => updateInput('interestRate', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Loan Term (Years)</Label>
                    <Input
                      type="number"
                      value={inputs.loanTermYears}
                      onChange={(e) => updateInput('loanTermYears', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Hold Period (Years)</Label>
                    <Input
                      type="number"
                      value={inputs.holdPeriodYears}
                      onChange={(e) => updateInput('holdPeriodYears', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Refinance Year (0 = none)</Label>
                    <Input
                      type="number"
                      value={inputs.refinanceYear}
                      onChange={(e) => updateInput('refinanceYear', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Refinance LTV %</Label>
                    <Input
                      type="number"
                      value={inputs.refinanceLtv}
                      onChange={(e) => updateInput('refinanceLtv', Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                  </div>
                </div>
              </Card>
            </div>

            {/* Right Column - Results */}
            <div className="col-span-5 space-y-6">
              {/* Hero Metric */}
              <Card className="p-8 bg-gradient-to-br from-green-600 via-green-700 to-green-800 border-0 shadow-2xl shadow-green-500/20 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
                <div className="absolute top-0 right-0 w-48 h-48 bg-white/5 rounded-full blur-3xl -mr-24 -mt-24" />
                <div className="relative z-10">
                  <div className="flex items-center gap-2 mb-3">
                    <DollarSign className="w-5 h-5 text-green-200" />
                    <h3 className="text-sm uppercase tracking-wider text-green-200">Year 1 Cash Flow</h3>
                  </div>
                  <div className="text-5xl text-white mb-3">{formatCurrency(results.year1CashFlow)}</div>
                  <p className="text-sm text-green-100">Monthly: {formatCurrency(results.year1CashFlow / 12)}</p>
                </div>
              </Card>

              {/* Key Metrics */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Year 1 Key Metrics</h3>
                <div className="space-y-4">
                  {[
                    { label: '1% Rule', value: formatPercent(results.onePercentRule, 2), icon: Percent, color: results.onePercentRule >= 1 ? 'text-green-400' : 'text-orange-400' },
                    { label: 'Cap Rate', value: formatPercent(results.capRate * 100, 2), icon: TrendingUp, color: results.capRate >= 0.07 ? 'text-green-400' : 'text-blue-400' },
                    { label: 'Cash-on-Cash', value: formatPercent(results.cashOnCash * 100, 2), icon: DollarSign, color: results.cashOnCash >= 0.10 ? 'text-green-400' : 'text-blue-400' },
                    { label: 'DSCR', value: `${results.dscr.toFixed(2)}x`, icon: Calendar, color: results.dscr >= 1.25 ? 'text-green-400' : 'text-orange-400' },
                  ].map((item) => (
                    <div key={item.label} className={`flex items-center justify-between pb-4 border-b ${isDark ? 'border-slate-700/50' : 'border-slate-200'} last:border-0`}>
                      <div className="flex items-center gap-3">
                        <div className={`w-8 h-8 ${isDark ? 'bg-slate-700/30' : 'bg-slate-100'} rounded-lg flex items-center justify-center`}>
                          <item.icon className={`w-4 h-4 ${item.color}`} />
                        </div>
                        <span className={`text-sm ${colors.text.secondary}`}>{item.label}</span>
                      </div>
                      <span className={`font-semibold ${item.color}`}>{item.value}</span>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Acquisition Summary */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Acquisition Summary</h3>
                <div className="space-y-3">
                  {[
                    { label: 'Purchase Price', value: inputs.purchasePrice },
                    { label: 'All-In Cost', value: results.totalProjectCost },
                    { label: 'Loan Amount', value: results.loanAmount },
                    { label: 'Equity Invested', value: results.equityInvested },
                  ].map((item) => (
                    <div key={item.label} className={`flex justify-between text-sm pb-2 border-b ${isDark ? 'border-slate-700/50' : 'border-slate-200'} last:border-0`}>
                      <span className={colors.text.secondary}>{item.label}</span>
                      <span className={`${colors.text.primary} font-semibold`}>{formatCurrency(item.value)}</span>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Exit Strategy Comparison */}
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Exit Strategy Comparison</h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className={`text-sm ${colors.text.secondary}`}>Flip</span>
                      <span className="text-sm text-blue-400">{formatCurrency(results.flipGrossProfit)}</span>
                    </div>
                    <div className="text-xs text-slate-500">ROI: {formatPercent(results.flipRoi, 1)}</div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className={`text-sm ${colors.text.secondary}`}>BRRRR</span>
                      <span className="text-sm text-green-400">{formatCurrency(results.brrrCashOut)}</span>
                    </div>
                    <div className="text-xs text-slate-500">Year 2 CF: {formatCurrency(results.brrrYear2CashFlow)}</div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className={`text-sm ${colors.text.secondary}`}>Hold {inputs.holdPeriodYears} Years</span>
                      <span className="text-sm text-purple-400">{formatCurrency(results.netSaleProceeds)}</span>
                    </div>
                    <div className="text-xs text-slate-500">IRR: {formatPercent(results.irr, 1)} | {results.equityMultiple.toFixed(2)}x</div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        ),
        charts: (
          <div className="grid grid-cols-1 gap-8">
            {/* Cash Flow Components */}
            <Card className={`p-8 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
              <h3 className={`text-xl ${colors.text.primary} mb-6`}>10-Year Cash Flow Components</h3>
              <div style={{ height: 400 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={cashFlowData}>
                    <defs>
                      <linearGradient id="colorNOI" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                      </linearGradient>
                      <linearGradient id="colorDebt" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                      </linearGradient>
                      <linearGradient id="colorCF" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} opacity={0.2} />
                    <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                    <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: isDark ? '#1e293b' : '#fff',
                        border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                        borderRadius: '12px',
                      }}
                      formatter={(value: number) => formatCurrency(value)}
                    />
                    <Legend />
                    <Area type="monotone" dataKey="NOI" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#colorNOI)" />
                    <Area type="monotone" dataKey="Debt Service" stroke="#ef4444" strokeWidth={2} fillOpacity={1} fill="url(#colorDebt)" />
                    <Area type="monotone" dataKey="Cash Flow" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorCF)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </Card>

            <div className="grid grid-cols-2 gap-8">
              {/* Equity Growth */}
              <Card className={`p-8 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <h3 className={`text-xl ${colors.text.primary} mb-6`}>Equity Growth</h3>
                <div style={{ height: 350 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={equityData}>
                      <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} opacity={0.2} />
                      <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                      <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: isDark ? '#1e293b' : '#fff',
                          border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                          borderRadius: '12px',
                        }}
                        formatter={(value: number) => formatCurrency(value)}
                      />
                      <Legend />
                      <Line type="monotone" dataKey="Property Value" stroke="#10b981" strokeWidth={2} />
                      <Line type="monotone" dataKey="Equity" stroke="#3b82f6" strokeWidth={2} />
                      <Line type="monotone" dataKey="Loan Balance" stroke="#ef4444" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </Card>

              {/* Exit Strategy Comparison */}
              <Card className={`p-8 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm`}>
                <h3 className={`text-xl ${colors.text.primary} mb-6`}>Exit Strategy Value Comparison</h3>
                <div style={{ height: 350 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={exitComparisonData}>
                      <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} opacity={0.2} />
                      <XAxis dataKey="strategy" stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                      <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: isDark ? '#1e293b' : '#fff',
                          border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                          borderRadius: '12px',
                        }}
                        formatter={(value: number) => formatCurrency(value)}
                      />
                      <Bar dataKey="value" fill="#10b981" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </Card>
            </div>
          </div>
        ),
        documentation: (
          <Card className={`p-8 ${colors.card} border ${colors.border.secondary} backdrop-blur-sm max-w-5xl mx-auto`}>
            <h2 className={`text-3xl ${colors.text.primary} mb-6`}>Single Family Rental Model Documentation</h2>
            <div className={`${colors.text.secondary} space-y-6 leading-relaxed`}>
              <p>
                This comprehensive rental property model analyzes long-term buy-and-hold strategies including
                BRRRR (Buy, Rehab, Rent, Refinance, Repeat). It projects 10 years of cash flows with growth
                assumptions and compares multiple exit strategies to help you make informed investment decisions.
              </p>
              <div>
                <h3 className={`text-2xl ${colors.text.primary} mt-8 mb-4`}>Key Metrics Targets</h3>
                <div className="grid grid-cols-2 gap-6">
                  {[
                    { metric: '1% Rule', target: '≥1.0%', excellent: '≥1.5%', formula: 'Monthly Rent / Purchase Price' },
                    { metric: 'Cap Rate', target: '≥7.0%', excellent: '≥9.0%', formula: 'NOI / All-In Cost' },
                    { metric: 'Cash-on-Cash', target: '≥10%', excellent: '≥15%', formula: 'Annual CF / Equity Invested' },
                    { metric: 'DSCR', target: '≥1.25x', excellent: '≥1.35x', formula: 'NOI / Annual Debt Service' },
                    { metric: '10-Year IRR', target: '≥15%', excellent: '≥20%', formula: 'Internal Rate of Return' },
                  ].map((row) => (
                    <div key={row.metric} className={`p-4 rounded-lg ${isDark ? 'bg-slate-800/30' : 'bg-slate-50'}`}>
                      <div className={`text-sm font-semibold ${colors.text.primary} mb-2`}>{row.metric}</div>
                      <div className={`text-xs ${colors.text.secondary}`}>Target: {row.target}</div>
                      <div className="text-xs text-green-400">Excellent: {row.excellent}</div>
                      <div className={`text-xs ${colors.text.secondary} mt-2`}>{row.formula}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h3 className={`text-2xl ${colors.text.primary} mt-8 mb-4`}>Exit Strategies</h3>
                <div className="space-y-4">
                  <div className={`p-4 rounded-lg ${isDark ? 'bg-blue-500/10' : 'bg-blue-50'} border ${isDark ? 'border-blue-500/20' : 'border-blue-200'}`}>
                    <div className={`text-lg font-semibold ${colors.text.primary} mb-2`}>Flip Strategy</div>
                    <p className={colors.text.secondary}>
                      Renovate and sell quickly for immediate profit. Best for markets with strong appreciation and high demand.
                    </p>
                  </div>
                  <div className={`p-4 rounded-lg ${isDark ? 'bg-green-500/10' : 'bg-green-50'} border ${isDark ? 'border-green-500/20' : 'border-green-200'}`}>
                    <div className={`text-lg font-semibold ${colors.text.primary} mb-2`}>BRRRR Strategy</div>
                    <p className={colors.text.secondary}>
                      Buy, Rehab, Rent, Refinance, Repeat. Pull out capital through refinancing to recycle into new deals while maintaining rental income.
                    </p>
                  </div>
                  <div className={`p-4 rounded-lg ${isDark ? 'bg-purple-500/10' : 'bg-purple-50'} border ${isDark ? 'border-purple-500/20' : 'border-purple-200'}`}>
                    <div className={`text-lg font-semibold ${colors.text.primary} mb-2`}>Hold Strategy</div>
                    <p className={colors.text.secondary}>
                      Long-term buy-and-hold for steady cash flow, appreciation, and tax benefits through depreciation.
                    </p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className={`text-2xl ${colors.text.primary} mt-8 mb-4`}>Best Practices</h3>
                <div className="space-y-3">
                  {[
                    'Use conservative rent growth assumptions (2-4%) to avoid over-optimistic projections',
                    'Budget at least 8-10% for management fees even if self-managing to value your time',
                    'Set aside 1-2% of property value annually for CapEx reserves',
                    'Factor in 5-8% vacancy rate even in strong markets',
                    'Verify comps and rent potential before finalizing purchase',
                    'Aim for DSCR above 1.25x to ensure stable debt coverage',
                    'Consider refinancing after forced appreciation through renovations',
                  ].map((practice, index) => (
                    <div key={index} className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                      <span className={colors.text.secondary}>{practice}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Card>
        ),
      }}
    </CalculatorLayout>
  );
}
