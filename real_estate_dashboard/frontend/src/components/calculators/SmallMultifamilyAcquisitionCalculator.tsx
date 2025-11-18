import React, { useState, useMemo } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  TextField,
  MenuItem,
  Tabs,
  Tab,
  Stack,
  Chip,
  alpha,
  useTheme,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  FormControl,
  InputLabel,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Divider,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Home as HomeIcon,
  AttachMoney as MoneyIcon,
  Build as BuildIcon,
  Transform as TransformIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  ShowChart,
} from '@mui/icons-material';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import { useAppTheme } from '../../contexts/ThemeContext';
import {
  SmallMultifamilyAcquisitionInputs,
  SmallMultifamilyAcquisitionResults,
  UnitDetail,
  UnitRenovationCosts,
  FinancingScenario,
  ConversionCosts,
  ExitStrategy,
  MonthlyProjection,
} from '../../types/calculatorTypes';

// Default inputs for a 4-unit property in Miami, FL
const DEFAULT_INPUTS: SmallMultifamilyAcquisitionInputs = {
  // Project Information
  projectName: 'Miami Quadplex Acquisition',
  location: 'Miami, FL',
  analyst: '',

  // Property Details
  address: '123 Ocean Drive, Miami, FL 33139',
  propertyType: 'quadplex',
  numberOfUnits: 4,
  totalBuildingSF: 4800,
  lotSizeAcres: 0.25,
  yearBuilt: 1985,
  zoning: 'R-4 Multi-Family',
  conversionAllowed: true,

  // Individual Unit Details
  units: [
    {
      unitNumber: 1,
      bedrooms: 2,
      bathrooms: 1,
      squareFootage: 1200,
      currentRent: 1500,
      marketRent: 1800,
      condition: 'fair',
      occupancyStatus: 'occupied',
      leaseEndDate: '2025-12-31',
      notes: 'Needs kitchen and bathroom updates',
    },
    {
      unitNumber: 2,
      bedrooms: 2,
      bathrooms: 1,
      squareFootage: 1200,
      currentRent: 0,
      marketRent: 1800,
      condition: 'poor',
      occupancyStatus: 'vacant',
      leaseEndDate: undefined,
      notes: 'Complete renovation needed',
    },
    {
      unitNumber: 3,
      bedrooms: 2,
      bathrooms: 1.5,
      squareFootage: 1200,
      currentRent: 1600,
      marketRent: 1850,
      condition: 'good',
      occupancyStatus: 'occupied',
      leaseEndDate: '2025-06-30',
      notes: 'Minor cosmetic updates',
    },
    {
      unitNumber: 4,
      bedrooms: 2,
      bathrooms: 1,
      squareFootage: 1200,
      currentRent: 0,
      marketRent: 1800,
      condition: 'fair',
      occupancyStatus: 'vacant',
      leaseEndDate: undefined,
      notes: 'Flooring and paint needed',
    },
  ],

  // Acquisition
  purchasePrice: 650000,
  closingCostsPct: 3,
  inspectionDueDiligence: 5000,

  // Financing Scenarios
  financingScenarios: [
    {
      name: '3% Conv 30yr',
      downPaymentPct: 25,
      interestRate: 7.5,
      loanTermYears: 30,
      loanType: 'conventional',
      cashRequired: 0,
      loanAmount: 0,
      monthlyPayment: 0,
      isSelected: true,
    },
    {
      name: '3.5% FHA',
      downPaymentPct: 3.5,
      interestRate: 6.5,
      loanTermYears: 30,
      loanType: 'fha',
      cashRequired: 0,
      loanAmount: 0,
      monthlyPayment: 0,
      isSelected: false,
    },
    {
      name: '20% Conv 15yr',
      downPaymentPct: 20,
      interestRate: 7.0,
      loanTermYears: 15,
      loanType: 'conventional',
      cashRequired: 0,
      loanAmount: 0,
      monthlyPayment: 0,
      isSelected: false,
    },
    {
      name: 'Hard Money',
      downPaymentPct: 30,
      interestRate: 12.0,
      loanTermYears: 2,
      loanType: 'hard-money',
      cashRequired: 0,
      loanAmount: 0,
      monthlyPayment: 0,
      isSelected: false,
    },
  ],
  selectedFinancingIndex: 0,

  // Renovation Budget (13 categories per unit)
  unitRenovations: [
    {
      unitNumber: 1,
      kitchen: 15000,
      bathroom: 8000,
      flooring: 4000,
      interiorPaint: 2000,
      exteriorPaint: 0,
      appliances: 3000,
      plumbing: 2000,
      electrical: 1500,
      hvac: 0,
      windowsDoors: 2000,
      landscaping: 0,
      roof: 0,
      other: 1000,
      subtotal: 0,
      contingency: 0,
      total: 0,
    },
    {
      unitNumber: 2,
      kitchen: 20000,
      bathroom: 12000,
      flooring: 5000,
      interiorPaint: 2500,
      exteriorPaint: 0,
      appliances: 4000,
      plumbing: 3000,
      electrical: 2500,
      hvac: 4000,
      windowsDoors: 3000,
      landscaping: 0,
      roof: 0,
      other: 2000,
      subtotal: 0,
      contingency: 0,
      total: 0,
    },
    {
      unitNumber: 3,
      kitchen: 5000,
      bathroom: 3000,
      flooring: 3000,
      interiorPaint: 1500,
      exteriorPaint: 0,
      appliances: 2000,
      plumbing: 500,
      electrical: 500,
      hvac: 0,
      windowsDoors: 1000,
      landscaping: 0,
      roof: 0,
      other: 500,
      subtotal: 0,
      contingency: 0,
      total: 0,
    },
    {
      unitNumber: 4,
      kitchen: 10000,
      bathroom: 6000,
      flooring: 4500,
      interiorPaint: 2000,
      exteriorPaint: 0,
      appliances: 3000,
      plumbing: 1500,
      electrical: 1000,
      hvac: 0,
      windowsDoors: 1500,
      landscaping: 0,
      roof: 0,
      other: 1000,
      subtotal: 0,
      contingency: 0,
      total: 0,
    },
  ],
  globalContingencyPct: 10,

  // Conversion Costs
  conversionCosts: {
    type: 'condo',
    surveyEngineering: 8000,
    legalFees: 15000,
    hoaCoopFormation: 5000,
    titleWorkPerUnit: 1500,
    countyPermits: 3000,
    utilitySeparation: 12000,
    environmentalInspections: 2500,
    architecturalPlans: 6000,
    insuranceDuringConversion: 4000,
    other: 3000,
    total: 0,
    costPerUnit: 0,
    timelineMonths: 6,
  },

  // Exit Strategy Parameters
  conversionPremiumPct: 25,
  asIsSaleCapRate: 6.5,
  refinanceLTV: 75,
  seasoningMonths: 12,
  stabilizedVacancyPct: 5,
  propertyManagementPct: 8,
  maintenancePct: 10,
  insuranceAnnual: 4800,
  taxesAnnual: 9000,
  hybridUnitsToSell: 2,
  wholesaleAssignmentFee: 25000,

  // Timeline
  renovationMonths: 6,
  conversionMonths: 6,
  salesMonthsPerUnit: 2,

  // Holding Costs
  holdingCostsMonthly: 3500,
};

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const SmallMultifamilyAcquisitionCalculator: React.FC = () => {
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [inputs, setInputs] = useState<SmallMultifamilyAcquisitionInputs>(DEFAULT_INPUTS);
  const [activeTab, setActiveTab] = useState(0);

  // Update input handler
  const handleInputChange = (field: keyof SmallMultifamilyAcquisitionInputs, value: any) => {
    setInputs((prev) => ({ ...prev, [field]: value }));
  };

  // Unit detail update handler
  const handleUnitChange = (unitIndex: number, field: keyof UnitDetail, value: any) => {
    const updatedUnits = [...inputs.units];
    updatedUnits[unitIndex] = { ...updatedUnits[unitIndex], [field]: value };
    setInputs((prev) => ({ ...prev, units: updatedUnits }));
  };

  // Renovation costs update handler
  const handleRenovationChange = (unitIndex: number, field: keyof UnitRenovationCosts, value: number) => {
    const updatedRenovations = [...inputs.unitRenovations];
    updatedRenovations[unitIndex] = { ...updatedRenovations[unitIndex], [field]: value };
    setInputs((prev) => ({ ...prev, unitRenovations: updatedRenovations }));
  };

  // Financing scenario update handler
  const handleFinancingChange = (scenarioIndex: number, field: keyof FinancingScenario, value: any) => {
    const updatedScenarios = [...inputs.financingScenarios];
    updatedScenarios[scenarioIndex] = { ...updatedScenarios[scenarioIndex], [field]: value };
    setInputs((prev) => ({ ...prev, financingScenarios: updatedScenarios }));
  };

  // Conversion costs update handler
  const handleConversionCostChange = (field: keyof ConversionCosts, value: any) => {
    setInputs((prev) => ({
      ...prev,
      conversionCosts: { ...prev.conversionCosts, [field]: value },
    }));
  };

  // Calculation logic
  const results = useMemo((): SmallMultifamilyAcquisitionResults => {
    // Calculate acquisition costs
    const closingCosts = inputs.purchasePrice * (inputs.closingCostsPct / 100);
    const totalAcquisitionCost = inputs.purchasePrice + closingCosts + inputs.inspectionDueDiligence;

    // Calculate financing for each scenario
    const financingScenariosWithCalcs = inputs.financingScenarios.map((scenario) => {
      const loanAmount = inputs.purchasePrice * (1 - scenario.downPaymentPct / 100);
      const downPayment = inputs.purchasePrice - loanAmount;
      const monthlyRate = scenario.interestRate / 100 / 12;
      const numPayments = scenario.loanTermYears * 12;
      const monthlyPayment =
        loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) /
        (Math.pow(1 + monthlyRate, numPayments) - 1);
      const cashRequired = downPayment + closingCosts + inputs.inspectionDueDiligence;

      return {
        ...scenario,
        loanAmount,
        monthlyPayment,
        cashRequired,
      };
    });

    const selectedFinancing = financingScenariosWithCalcs[inputs.selectedFinancingIndex];

    // Calculate renovation costs per unit
    const unitRenovationsWithTotals = inputs.unitRenovations.map((renovation) => {
      const subtotal =
        renovation.kitchen +
        renovation.bathroom +
        renovation.flooring +
        renovation.interiorPaint +
        renovation.exteriorPaint +
        renovation.appliances +
        renovation.plumbing +
        renovation.electrical +
        renovation.hvac +
        renovation.windowsDoors +
        renovation.landscaping +
        renovation.roof +
        renovation.other;
      const contingency = subtotal * (inputs.globalContingencyPct / 100);
      const total = subtotal + contingency;

      return {
        ...renovation,
        subtotal,
        contingency,
        total,
      };
    });

    const totalRenovationCost = unitRenovationsWithTotals.reduce((sum, unit) => sum + unit.total, 0);
    const avgCostPerUnit = totalRenovationCost / inputs.numberOfUnits;
    const renovationContingency = totalRenovationCost * (inputs.globalContingencyPct / 100);

    // Calculate conversion costs
    const conversionCostsTotal =
      inputs.conversionCosts.surveyEngineering +
      inputs.conversionCosts.legalFees +
      inputs.conversionCosts.hoaCoopFormation +
      inputs.conversionCosts.titleWorkPerUnit * inputs.numberOfUnits +
      inputs.conversionCosts.countyPermits +
      inputs.conversionCosts.utilitySeparation +
      inputs.conversionCosts.environmentalInspections +
      inputs.conversionCosts.architecturalPlans +
      inputs.conversionCosts.insuranceDuringConversion +
      inputs.conversionCosts.other;

    const conversionCostsWithCalcs: ConversionCosts = {
      ...inputs.conversionCosts,
      total: conversionCostsTotal,
      costPerUnit: conversionCostsTotal / inputs.numberOfUnits,
    };

    // Calculate total project cost
    const totalProjectCost = totalAcquisitionCost + totalRenovationCost + conversionCostsTotal;
    const cashRequired = selectedFinancing.cashRequired + totalRenovationCost + conversionCostsTotal;

    // Calculate current and market values
    const currentAnnualRent = inputs.units.reduce((sum, unit) => sum + unit.currentRent * 12, 0);
    const marketAnnualRent = inputs.units.reduce((sum, unit) => sum + unit.marketRent * 12, 0);
    const asIsValue = currentAnnualRent / (inputs.asIsSaleCapRate / 100);

    // Calculate exit strategies
    const exitStrategies: ExitStrategy[] = [];

    // 1. Subdivide & Convert Strategy
    const conversionPremium = inputs.conversionPremiumPct / 100;
    const individualUnitPrices = inputs.units.map((unit) => {
      const unitValue = (unit.marketRent * 12) / (inputs.asIsSaleCapRate / 100);
      return unitValue * (1 + conversionPremium);
    });
    const grossProceeds = individualUnitPrices.reduce((sum, price) => sum + price, 0);
    const sellingCosts = grossProceeds * 0.08; // 8% selling costs
    const netProceeds = grossProceeds - sellingCosts;
    const subdivideNetProfit = netProceeds - totalProjectCost;
    const subdivideROI = (subdivideNetProfit / cashRequired) * 100;
    const subdivideTimeline =
      inputs.renovationMonths + inputs.conversionMonths + inputs.numberOfUnits * inputs.salesMonthsPerUnit;

    exitStrategies.push({
      strategyType: 'subdivide-convert',
      name: 'Subdivide & Convert',
      description: 'Convert to condos and sell individually',
      individualUnitPrices,
      grossProceeds,
      sellingCosts,
      netProceeds,
      netProfit: subdivideNetProfit,
      roi: subdivideROI,
      timelineMonths: subdivideTimeline,
      totalValueCreated: grossProceeds - inputs.purchasePrice,
    });

    // 2. Sell As-Is Strategy
    const asIsSalePrice = asIsValue;
    const asIsSellingCosts = asIsSalePrice * 0.06; // 6% selling costs
    const asIsNetProceeds = asIsSalePrice - asIsSellingCosts;
    const asIsNetProfit = asIsNetProceeds - totalAcquisitionCost;
    const asIsROI = (asIsNetProfit / selectedFinancing.cashRequired) * 100;

    exitStrategies.push({
      strategyType: 'sell-as-is',
      name: 'Sell As-Is',
      description: 'Quick sale without major renovations',
      asIsPrice: asIsSalePrice,
      sellingCosts: asIsSellingCosts,
      netProceeds: asIsNetProceeds,
      netProfit: asIsNetProfit,
      roi: asIsROI,
      timelineMonths: 3,
    });

    // 3. BRRRR Strategy
    const stabilizedVacancy = 1 - inputs.stabilizedVacancyPct / 100;
    const effectiveGrossIncome = marketAnnualRent * stabilizedVacancy;
    const propertyManagement = effectiveGrossIncome * (inputs.propertyManagementPct / 100);
    const maintenance = effectiveGrossIncome * (inputs.maintenancePct / 100);
    const totalOperatingExpenses = propertyManagement + maintenance + inputs.insuranceAnnual + inputs.taxesAnnual;
    const noi = effectiveGrossIncome - totalOperatingExpenses;
    const stabilizedValue = noi / (inputs.asIsSaleCapRate / 100);
    const refinanceAmount = stabilizedValue * (inputs.refinanceLTV / 100);
    const cashLeftInDeal = cashRequired - refinanceAmount;
    const annualDebtService = selectedFinancing.monthlyPayment * 12;
    const annualCashFlow = noi - annualDebtService;
    const cashOnCashReturn = (annualCashFlow / cashLeftInDeal) * 100;

    exitStrategies.push({
      strategyType: 'brrrr',
      name: 'BRRRR',
      description: 'Buy, Renovate, Rent, Refinance, Repeat',
      stabilizedValue,
      refinanceAmount,
      refinanceLtv: inputs.refinanceLTV,
      annualRentalIncome: marketAnnualRent,
      annualExpenses: totalOperatingExpenses,
      annualDebtService,
      annualCashFlow,
      cashOnCashReturn,
      cashLeftInDeal,
      netProfit: annualCashFlow, // Annual profit
      roi: cashOnCashReturn,
      timelineMonths: inputs.renovationMonths + inputs.seasoningMonths,
    });

    // 4. Hybrid Strategy
    const unitsToSell = inputs.hybridUnitsToSell;
    const unitsToHold = inputs.numberOfUnits - unitsToSell;
    const soldUnitPrices = individualUnitPrices.slice(0, unitsToSell);
    const heldUnitValues = individualUnitPrices.slice(unitsToSell);
    const soldUnitsRevenue = soldUnitPrices.reduce((sum, price) => sum + price, 0);
    const soldUnitsSellingCosts = soldUnitsRevenue * 0.08;
    const soldUnitsNet = soldUnitsRevenue - soldUnitsSellingCosts;
    const heldUnitRentalIncome = inputs.units.slice(unitsToSell).reduce((sum, unit) => sum + unit.marketRent * 12, 0);
    const heldUnitExpenses = heldUnitRentalIncome * 0.35; // 35% expense ratio
    const heldUnitNOI = heldUnitRentalIncome - heldUnitExpenses;
    const hybridCashRecovered = soldUnitsNet;
    const hybridCashLeftInDeal = totalProjectCost - hybridCashRecovered;
    const hybridCashOnCash = (heldUnitNOI / hybridCashLeftInDeal) * 100;
    const hybridEquity = heldUnitValues.reduce((sum, val) => sum + val, 0);
    const hybridTotalValue = soldUnitsNet + hybridEquity;
    const hybridNetProfit = hybridTotalValue - totalProjectCost;
    const hybridROI = (hybridNetProfit / cashRequired) * 100;

    exitStrategies.push({
      strategyType: 'hybrid',
      name: 'Hybrid',
      description: `Sell ${unitsToSell} units, hold ${unitsToHold}`,
      unitsToSell,
      unitsToHold,
      soldUnitPrices,
      heldUnitValues,
      grossProceeds: soldUnitsRevenue,
      sellingCosts: soldUnitsSellingCosts,
      netProceeds: soldUnitsNet,
      heldUnitRentalIncome,
      cashOnCashReturn: hybridCashOnCash,
      cashLeftInDeal: hybridCashLeftInDeal,
      netProfit: hybridNetProfit,
      roi: hybridROI,
      timelineMonths: inputs.renovationMonths + inputs.conversionMonths + unitsToSell * inputs.salesMonthsPerUnit,
      totalValueCreated: hybridTotalValue - inputs.purchasePrice,
    });

    // 5. Wholesale Strategy
    const wholesaleRevenue = inputs.wholesaleAssignmentFee;
    const wholesaleCosts = inputs.inspectionDueDiligence + 2000; // Due diligence + marketing
    const wholesaleNetProfit = wholesaleRevenue - wholesaleCosts;
    const wholesaleROI = (wholesaleNetProfit / wholesaleCosts) * 100;

    exitStrategies.push({
      strategyType: 'wholesale',
      name: 'Wholesale',
      description: 'Assign contract for quick profit',
      assignmentFee: inputs.wholesaleAssignmentFee,
      dueDiligenceCosts: wholesaleCosts,
      netProfit: wholesaleNetProfit,
      roi: wholesaleROI,
      timelineMonths: 2,
    });

    // Rank strategies by ROI
    const strategyRankings = exitStrategies
      .map((strategy, index) => ({
        strategy: strategy.name,
        rank: 0,
        score: strategy.roi,
      }))
      .sort((a, b) => b.score - a.score)
      .map((item, index) => ({ ...item, rank: index + 1 }));

    // Determine recommended strategy (highest ROI with reasonable timeline)
    const viableStrategies = exitStrategies.filter((s) => s.timelineMonths <= 24);
    const recommendedStrategy = viableStrategies.reduce((best, current) =>
      current.roi > best.roi ? current : best
    );

    // Calculate monthly projections for subdivide strategy
    const monthlyProjections: MonthlyProjection[] = [];
    let cumulativeCashFlow = 0;
    let loanBalance = selectedFinancing.loanAmount;

    for (let month = 1; month <= subdivideTimeline; month++) {
      let phase: 'acquisition' | 'renovation' | 'conversion' | 'sales' | 'stabilized';
      let cashInflows = 0;
      let cashOutflows = 0;

      if (month === 1) {
        phase = 'acquisition';
        cashOutflows = selectedFinancing.cashRequired;
      } else if (month <= inputs.renovationMonths) {
        phase = 'renovation';
        cashOutflows = totalRenovationCost / inputs.renovationMonths + inputs.holdingCostsMonthly;
      } else if (month <= inputs.renovationMonths + inputs.conversionMonths) {
        phase = 'conversion';
        cashOutflows = conversionCostsTotal / inputs.conversionMonths + inputs.holdingCostsMonthly;
      } else {
        phase = 'sales';
        const salesStartMonth = inputs.renovationMonths + inputs.conversionMonths + 1;
        const monthsIntoSales = month - salesStartMonth + 1;
        const unitsSoldSoFar = Math.min(
          Math.floor(monthsIntoSales / inputs.salesMonthsPerUnit),
          inputs.numberOfUnits
        );

        if (monthsIntoSales % inputs.salesMonthsPerUnit === 1 && unitsSoldSoFar < inputs.numberOfUnits) {
          const unitPrice = individualUnitPrices[unitsSoldSoFar];
          cashInflows = unitPrice * 0.92; // Net of 8% selling costs
        }

        cashOutflows = inputs.holdingCostsMonthly;
      }

      const netCashFlow = cashInflows - cashOutflows;
      cumulativeCashFlow += netCashFlow;

      // Update loan balance
      if (loanBalance > 0) {
        const monthlyRate = selectedFinancing.interestRate / 100 / 12;
        const interest = loanBalance * monthlyRate;
        loanBalance = loanBalance + interest - (selectedFinancing.monthlyPayment - interest);
      }

      monthlyProjections.push({
        month,
        phase,
        cashInflows,
        cashOutflows,
        netCashFlow,
        cumulativeCashFlow,
        loanBalance: Math.max(0, loanBalance),
        unitsRenovated: Math.min(month, inputs.renovationMonths),
        unitsSold: Math.max(0, Math.min(Math.floor((month - inputs.renovationMonths - inputs.conversionMonths) / inputs.salesMonthsPerUnit), inputs.numberOfUnits)),
        unitsHeld: 0,
        description: `${phase.charAt(0).toUpperCase() + phase.slice(1)} phase`,
      });
    }

    // Risk assessment
    const conversionRisk: 'low' | 'medium' | 'high' =
      inputs.conversionCosts.total < 30000 ? 'low' : inputs.conversionCosts.total < 60000 ? 'medium' : 'high';
    const marketRisk: 'low' | 'medium' | 'high' =
      inputs.conversionPremiumPct < 20 ? 'low' : inputs.conversionPremiumPct < 35 ? 'medium' : 'high';
    const capitalRisk: 'low' | 'medium' | 'high' =
      cashRequired < 150000 ? 'low' : cashRequired < 300000 ? 'medium' : 'high';

    let overallRisk: 'low' | 'medium' | 'high';
    const riskScore = [conversionRisk, marketRisk, capitalRisk].filter((r) => r === 'high').length;
    if (riskScore >= 2) overallRisk = 'high';
    else if (riskScore === 1) overallRisk = 'medium';
    else overallRisk = 'low';

    return {
      totalProjectCost,
      cashRequired,
      peakCapitalRequirement: Math.max(...monthlyProjections.map((p) => Math.abs(p.cumulativeCashFlow))),
      purchasePrice: inputs.purchasePrice,
      closingCosts,
      totalAcquisitionCost,
      selectedFinancing,
      loanAmount: selectedFinancing.loanAmount,
      downPayment: inputs.purchasePrice - selectedFinancing.loanAmount,
      monthlyMortgagePayment: selectedFinancing.monthlyPayment,
      totalRenovationCost,
      avgCostPerUnit,
      renovationContingency,
      totalConversionCost: conversionCostsTotal,
      conversionCostPerUnit: conversionCostsWithCalcs.costPerUnit,
      conversionTimeline: inputs.conversionCosts.timelineMonths,
      conversionPremium: inputs.conversionPremiumPct,
      exitStrategies,
      recommendedStrategy,
      strategyRankings,
      monthlyProjections,
      totalMonthsToCompletion: subdivideTimeline,
      totalHoldingCosts: inputs.holdingCostsMonthly * subdivideTimeline,
      maxCashOutflow: Math.min(...monthlyProjections.map((p) => p.cumulativeCashFlow)),
      asIsValue,
      individualUnitsTotal: grossProceeds,
      maxProfitPotential: Math.max(...exitStrategies.map((s) => s.netProfit)),
      safestStrategy: exitStrategies.find((s) => s.strategyType === 'sell-as-is')?.name || 'Sell As-Is',
      fastestStrategy: exitStrategies.reduce((fastest, current) =>
        current.timelineMonths < fastest.timelineMonths ? current : fastest
      ).name,
      highestROI: Math.max(...exitStrategies.map((s) => s.roi)),
      conversionRisk,
      marketRisk,
      capitalRisk,
      overallRisk,
    };
  }, [inputs]);

  // Format currency
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  // Format percentage
  const formatPercent = (value: number): string => {
    return `${value.toFixed(2)}%`;
  };

  // Chart colors
  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

  return (
    <Box sx={{ p: 4 }}>
      {/* Header */}
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
            Small Multifamily Acquisition
          </Typography>
          <Typography variant="body2" color="text.secondary">
            2-10 unit property acquisition with multiple exit strategies
          </Typography>
        </Box>
        <Stack direction="row" spacing={2} alignItems="center">
          <Chip
            label={`${inputs.numberOfUnits} Units`}
            color="primary"
            sx={{ fontWeight: 600 }}
          />
          <Chip
            label={results.recommendedStrategy.name}
            sx={{
              bgcolor: alpha('#10b981', 0.1),
              color: '#10b981',
              fontWeight: 600,
            }}
          />
        </Stack>
      </Stack>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
          <Tab label="Calculator" icon={<AssessmentIcon />} iconPosition="start" />
          <Tab label="Analytics" icon={<TrendingUpIcon />} iconPosition="start" />
          <Tab label="Projections" icon={<ShowChart />} iconPosition="start" />
          <Tab label="Documentation" icon={<InfoIcon />} iconPosition="start" />
        </Tabs>
      </Box>

      {/* Tab Panels */}
      <TabPanel value={activeTab} index={0}>
        <Grid container spacing={3}>
          {/* Left Column - Inputs */}
          <Grid item xs={12} lg={6}>
            {/* Project Information */}
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Stack direction="row" spacing={2} alignItems="center">
                  <HomeIcon color="primary" />
                  <Typography variant="h6">Project Information</Typography>
                </Stack>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Project Name"
                      value={inputs.projectName}
                      onChange={(e) => handleInputChange('projectName', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Location"
                      value={inputs.location}
                      onChange={(e) => handleInputChange('location', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Analyst"
                      value={inputs.analyst}
                      onChange={(e) => handleInputChange('analyst', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Property Address"
                      value={inputs.address}
                      onChange={(e) => handleInputChange('address', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth>
                      <InputLabel>Property Type</InputLabel>
                      <Select
                        value={inputs.propertyType}
                        label="Property Type"
                        onChange={(e) => handleInputChange('propertyType', e.target.value)}
                      >
                        <MenuItem value="duplex">Duplex (2 units)</MenuItem>
                        <MenuItem value="triplex">Triplex (3 units)</MenuItem>
                        <MenuItem value="quadplex">Quadplex (4 units)</MenuItem>
                        <MenuItem value="5-unit">5-Unit Building</MenuItem>
                        <MenuItem value="6-unit">6-Unit Building</MenuItem>
                        <MenuItem value="7-10-unit">7-10 Unit Building</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Number of Units"
                      value={inputs.numberOfUnits}
                      onChange={(e) => handleInputChange('numberOfUnits', parseInt(e.target.value))}
                      InputProps={{ inputProps: { min: 2, max: 10 } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Total Building SF"
                      value={inputs.totalBuildingSF}
                      onChange={(e) => handleInputChange('totalBuildingSF', parseFloat(e.target.value))}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Lot Size (acres)"
                      value={inputs.lotSizeAcres}
                      onChange={(e) => handleInputChange('lotSizeAcres', parseFloat(e.target.value))}
                      InputProps={{ inputProps: { step: 0.01 } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Year Built"
                      value={inputs.yearBuilt}
                      onChange={(e) => handleInputChange('yearBuilt', parseInt(e.target.value))}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Zoning"
                      value={inputs.zoning}
                      onChange={(e) => handleInputChange('zoning', e.target.value)}
                    />
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>

            {/* Acquisition Details */}
            <Accordion defaultExpanded sx={{ mt: 2 }}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Stack direction="row" spacing={2} alignItems="center">
                  <MoneyIcon color="primary" />
                  <Typography variant="h6">Acquisition Details</Typography>
                </Stack>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Purchase Price"
                      value={inputs.purchasePrice}
                      onChange={(e) => handleInputChange('purchasePrice', parseFloat(e.target.value))}
                      InputProps={{
                        startAdornment: '$',
                        inputProps: { step: 10000 },
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Closing Costs %"
                      value={inputs.closingCostsPct}
                      onChange={(e) => handleInputChange('closingCostsPct', parseFloat(e.target.value))}
                      InputProps={{
                        endAdornment: '%',
                        inputProps: { step: 0.1 },
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Inspection & Due Diligence"
                      value={inputs.inspectionDueDiligence}
                      onChange={(e) => handleInputChange('inspectionDueDiligence', parseFloat(e.target.value))}
                      InputProps={{
                        startAdornment: '$',
                        inputProps: { step: 500 },
                      }}
                    />
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>

            {/* Financing Scenarios */}
            <Accordion sx={{ mt: 2 }}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Stack direction="row" spacing={2} alignItems="center">
                  <MoneyIcon color="primary" />
                  <Typography variant="h6">Financing Scenarios</Typography>
                </Stack>
              </AccordionSummary>
              <AccordionDetails>
                <Stack spacing={2}>
                  {inputs.financingScenarios.map((scenario, index) => (
                    <Card
                      key={index}
                      sx={{
                        border: scenario.isSelected ? `2px solid #3b82f6` : `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                        background: scenario.isSelected ? alpha('#3b82f6', 0.05) : 'transparent',
                      }}
                    >
                      <CardContent>
                        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                          <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                            {scenario.name}
                          </Typography>
                          <Button
                            size="small"
                            variant={scenario.isSelected ? 'contained' : 'outlined'}
                            onClick={() => handleInputChange('selectedFinancingIndex', index)}
                          >
                            {scenario.isSelected ? 'Selected' : 'Select'}
                          </Button>
                        </Stack>
                        <Grid container spacing={2}>
                          <Grid item xs={6}>
                            <TextField
                              fullWidth
                              size="small"
                              type="number"
                              label="Down Payment %"
                              value={scenario.downPaymentPct}
                              onChange={(e) => handleFinancingChange(index, 'downPaymentPct', parseFloat(e.target.value))}
                              InputProps={{ endAdornment: '%' }}
                            />
                          </Grid>
                          <Grid item xs={6}>
                            <TextField
                              fullWidth
                              size="small"
                              type="number"
                              label="Interest Rate %"
                              value={scenario.interestRate}
                              onChange={(e) => handleFinancingChange(index, 'interestRate', parseFloat(e.target.value))}
                              InputProps={{ endAdornment: '%', inputProps: { step: 0.1 } }}
                            />
                          </Grid>
                          <Grid item xs={6}>
                            <TextField
                              fullWidth
                              size="small"
                              type="number"
                              label="Loan Term (years)"
                              value={scenario.loanTermYears}
                              onChange={(e) => handleFinancingChange(index, 'loanTermYears', parseInt(e.target.value))}
                            />
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="body2" color="text.secondary">
                              Monthly Payment: {formatCurrency(results.selectedFinancing.monthlyPayment || 0)}
                            </Typography>
                          </Grid>
                        </Grid>
                      </CardContent>
                    </Card>
                  ))}
                </Stack>
              </AccordionDetails>
            </Accordion>

            {/* Exit Strategy Parameters */}
            <Accordion sx={{ mt: 2 }}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Stack direction="row" spacing={2} alignItems="center">
                  <TrendingUpIcon color="primary" />
                  <Typography variant="h6">Exit Strategy Parameters</Typography>
                </Stack>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Conversion Premium %"
                      value={inputs.conversionPremiumPct}
                      onChange={(e) => handleInputChange('conversionPremiumPct', parseFloat(e.target.value))}
                      InputProps={{ endAdornment: '%', inputProps: { step: 1 } }}
                      helperText="Premium for converted/subdivided units"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="As-Is Sale Cap Rate %"
                      value={inputs.asIsSaleCapRate}
                      onChange={(e) => handleInputChange('asIsSaleCapRate', parseFloat(e.target.value))}
                      InputProps={{ endAdornment: '%', inputProps: { step: 0.1 } }}
                      helperText="Cap rate for as-is valuation"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Refinance LTV %"
                      value={inputs.refinanceLTV}
                      onChange={(e) => handleInputChange('refinanceLTV', parseFloat(e.target.value))}
                      InputProps={{ endAdornment: '%', inputProps: { step: 1 } }}
                      helperText="Loan-to-value for BRRRR refinance"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Seasoning Months"
                      value={inputs.seasoningMonths}
                      onChange={(e) => handleInputChange('seasoningMonths', parseInt(e.target.value))}
                      helperText="Months before refinance allowed"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Vacancy %"
                      value={inputs.stabilizedVacancyPct}
                      onChange={(e) => handleInputChange('stabilizedVacancyPct', parseFloat(e.target.value))}
                      InputProps={{ endAdornment: '%', inputProps: { step: 1 } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Property Management %"
                      value={inputs.propertyManagementPct}
                      onChange={(e) => handleInputChange('propertyManagementPct', parseFloat(e.target.value))}
                      InputProps={{ endAdornment: '%', inputProps: { step: 1 } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Annual Insurance"
                      value={inputs.insuranceAnnual}
                      onChange={(e) => handleInputChange('insuranceAnnual', parseFloat(e.target.value))}
                      InputProps={{ startAdornment: '$', inputProps: { step: 100 } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Annual Taxes"
                      value={inputs.taxesAnnual}
                      onChange={(e) => handleInputChange('taxesAnnual', parseFloat(e.target.value))}
                      InputProps={{ startAdornment: '$', inputProps: { step: 100 } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Hybrid: Units to Sell"
                      value={inputs.hybridUnitsToSell}
                      onChange={(e) => handleInputChange('hybridUnitsToSell', parseInt(e.target.value))}
                      InputProps={{ inputProps: { min: 1, max: inputs.numberOfUnits - 1 } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Wholesale Assignment Fee"
                      value={inputs.wholesaleAssignmentFee}
                      onChange={(e) => handleInputChange('wholesaleAssignmentFee', parseFloat(e.target.value))}
                      InputProps={{ startAdornment: '$', inputProps: { step: 1000 } }}
                    />
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>

            {/* Timeline & Holding Costs */}
            <Accordion sx={{ mt: 2 }}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Stack direction="row" spacing={2} alignItems="center">
                  <BuildIcon color="primary" />
                  <Typography variant="h6">Timeline & Holding Costs</Typography>
                </Stack>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Renovation Months"
                      value={inputs.renovationMonths}
                      onChange={(e) => handleInputChange('renovationMonths', parseInt(e.target.value))}
                      helperText="Time to complete all renovations"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Conversion Months"
                      value={inputs.conversionMonths}
                      onChange={(e) => handleInputChange('conversionMonths', parseInt(e.target.value))}
                      helperText="Time for legal conversion process"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Sales Months Per Unit"
                      value={inputs.salesMonthsPerUnit}
                      onChange={(e) => handleInputChange('salesMonthsPerUnit', parseInt(e.target.value))}
                      helperText="Average time to sell each unit"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Monthly Holding Costs"
                      value={inputs.holdingCostsMonthly}
                      onChange={(e) => handleInputChange('holdingCostsMonthly', parseFloat(e.target.value))}
                      InputProps={{ startAdornment: '$', inputProps: { step: 100 } }}
                      helperText="Utilities, insurance, etc."
                    />
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          </Grid>

          {/* Right Column - Summary Cards */}
          <Grid item xs={12} lg={6}>
            <Stack spacing={3}>
              {/* Key Metrics Card */}
              <Card sx={{ background: isDark ? alpha('#3b82f6', 0.05) : alpha('#3b82f6', 0.02) }}>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Key Metrics
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Total Project Cost
                      </Typography>
                      <Typography variant="h6">{formatCurrency(results.totalProjectCost)}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Cash Required
                      </Typography>
                      <Typography variant="h6">{formatCurrency(results.cashRequired)}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Recommended Strategy
                      </Typography>
                      <Typography variant="h6">{results.recommendedStrategy.name}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Expected ROI
                      </Typography>
                      <Typography variant="h6" color="success.main">
                        {formatPercent(results.recommendedStrategy.roi)}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              {/* Exit Strategies Comparison */}
              <Card>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Exit Strategies Comparison
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={results.exitStrategies}>
                      <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
                      <XAxis dataKey="name" tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
                      <YAxis tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: isDark ? '#1f2937' : '#ffffff',
                          border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                        }}
                      />
                      <Legend />
                      <Bar dataKey="roi" fill="#3b82f6" name="ROI %" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Risk Assessment */}
              <Card>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Risk Assessment
                  </Typography>
                  <Grid container spacing={2}>
                    {[
                      { label: 'Conversion Risk', value: results.conversionRisk },
                      { label: 'Market Risk', value: results.marketRisk },
                      { label: 'Capital Risk', value: results.capitalRisk },
                      { label: 'Overall Risk', value: results.overallRisk },
                    ].map((risk, index) => (
                      <Grid item xs={6} key={index}>
                        <Stack direction="row" spacing={1} alignItems="center">
                          {risk.value === 'low' ? (
                            <CheckCircleIcon sx={{ color: '#10b981', fontSize: 20 }} />
                          ) : risk.value === 'medium' ? (
                            <WarningIcon sx={{ color: '#f59e0b', fontSize: 20 }} />
                          ) : (
                            <ErrorIcon sx={{ color: '#ef4444', fontSize: 20 }} />
                          )}
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {risk.label}
                            </Typography>
                            <Typography
                              variant="body1"
                              sx={{
                                fontWeight: 600,
                                color:
                                  risk.value === 'low' ? '#10b981' : risk.value === 'medium' ? '#f59e0b' : '#ef4444',
                                textTransform: 'capitalize',
                              }}
                            >
                              {risk.value}
                            </Typography>
                          </Box>
                        </Stack>
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            </Stack>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Analytics Tab */}
      <TabPanel value={activeTab} index={1}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Analytics visualizations will be added here
        </Typography>
      </TabPanel>

      {/* Projections Tab */}
      <TabPanel value={activeTab} index={2}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Monthly projections will be added here
        </Typography>
      </TabPanel>

      {/* Documentation Tab */}
      <TabPanel value={activeTab} index={3}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Comprehensive documentation will be added here
        </Typography>
      </TabPanel>
    </Box>
  );
};
