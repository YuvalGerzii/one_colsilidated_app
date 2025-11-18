// Base interfaces shared across all calculators

export interface BaseInputs {
  projectName: string;
  location: string;
  analyst: string;
  propertyType: string;
  squareFootage: number;
  bedrooms: number;
  bathrooms: number;
  yearBuilt: number;
}

export interface BaseSavedReport {
  id: string;
  modelType: string;
  projectName: string;
  location: string;
  date: string;
  inputs: any;
  results: any;
}

// Single Family Rental Types
export interface SingleFamilyRentalInputs extends BaseInputs {
  // Acquisition & Rehab
  purchasePrice: number;
  closingCosts: number;
  renovationCosts: number;
  arv: number;
  holdingCostsMonthly: number;
  holdingPeriodMonths: number;

  // Income & Growth
  monthlyRent: number;
  otherIncomeMonthly: number;
  rentGrowthRate: number;
  vacancyRate: number;
  appreciationRate: number;

  // Operating Expenses
  managementPct: number;
  maintenancePct: number;
  propertyTaxAnnual: number;
  insuranceAnnual: number;
  utilitiesMonthly: number;
  hoaMonthly: number;
  otherExpensesMonthly: number;
  capexReserveMonthly: number;
  expenseGrowthRate: number;

  // Financing & Disposition
  downPaymentPct: number;
  interestRate: number;
  loanTermYears: number;
  refinanceLtv: number;
  refinanceRate: number;
  refinanceTermYears: number;
  refinanceYear: number;
  refinanceCostPct: number;
  sellingCostPct: number;

  // Holding Strategy
  holdPeriodYears: number;
}

export interface YearProjection {
  year: number;
  grossRent: number;
  vacancy: number;
  otherIncome: number;
  effectiveGrossIncome: number;
  operatingExpenses: number;
  noi: number;
  debtService: number;
  cashFlow: number;
  loanBalance: number;
  propertyValue: number;
  equity: number;
  cumulativeCashFlow: number;
}

export interface SingleFamilyRentalResults {
  // Acquisition Metrics
  loanAmount: number;
  downPayment: number;
  equityInvested: number;
  totalProjectCost: number;
  annualDebtService: number;

  // Year 1 Metrics
  year1GrossRent: number;
  year1Vacancy: number;
  year1EffectiveIncome: number;
  year1OperatingExpenses: number;
  year1Noi: number;
  year1CashFlow: number;
  capRate: number;
  cashOnCash: number;
  dscr: number;
  onePercentRule: number;

  // Hold Strategy
  exitValue: number;
  netSaleProceeds: number;
  loanBalanceExit: number;
  irr: number;
  equityMultiple: number;
  cashOutRefi: number;

  // Exit Comparison
  flipGrossProfit: number;
  flipRoi: number;
  flipProfitMargin: number;
  brrrCashOut: number;
  brrrYear2CashFlow: number;
  holdYear10CashFlow: number;
  holdMonthlyCashFlow: number;

  // Projections
  projections: YearProjection[];
  cashFlows: number[];
  cumulativeCashFlows: number[];
}

// Small Multifamily Types
export interface SmallMultifamilyInputs extends BaseInputs {
  purchasePrice: number;
  closingCosts: number;
  renovationCosts: number;
  units: number;
  currentRentPerUnit: number;
  targetRentPerUnit: number;
  vacancyRate: number;
  otherIncomePerUnit: number;
  managementPct: number;
  repairMaintenancePerUnit: number;
  utilitiesPerUnit: number;
  insurancePerUnit: number;
  propertyTaxPerUnit: number;
  otherExpensesPerUnit: number;
  capexReservePerUnit: number;
  rentGrowthRate: number;
  expenseGrowthRate: number;
  appreciationRate: number;
  stabilizationMonths: number;
  holdPeriodYears: number;
  exitCapRate: number;
  loanLtv: number;
  interestRate: number;
  amortizationYears: number;
  locationScore: number;
  conditionScore: number;
  financialScore: number;
  rentUpsideScore: number;
  dealStructureScore: number;
}

export interface SmallMultifamilyResults {
  loanAmount: number;
  downPayment: number;
  equityInvested: number;
  totalProjectCost: number;
  stabilizedNoi: number;
  stabilizedCashFlow: number;
  year1CapRate: number;
  year1CashOnCash: number;
  year1Dscr: number;
  exitValue: number;
  netSaleProceeds: number;
  irr: number;
  equityMultiple: number;
  totalScore: number;
  projections: YearProjection[];
}

// Extended Multifamily Types
export interface ExtendedMultifamilyInputs {
  // Property Profile
  projectName: string;
  location: string;
  analyst: string;
  totalUnits: number;
  analysisYears: number;
  totalFloors: number;

  // Unit Mix Percentages
  unitMixStudioPct: number;
  unitMixOneBedPct: number;
  unitMixTwoBedPct: number;
  unitMixThreeBedPct: number;
  unitMixPenthousePct: number;

  // Unit Square Footage
  studioAvgSf: number;
  oneBedAvgSf: number;
  twoBedAvgSf: number;
  threeBedAvgSf: number;
  penthouseAvgSf: number;

  // Unit Rents
  studioRent: number;
  oneBedRent: number;
  twoBedRent: number;
  threeBedRent: number;
  penthouseRent: number;

  // Revenue Assumptions
  physicalOccupancy: number;
  economicOccupancy: number;
  rentGrowth: number;
  concessionRate: number;
  badDebtRate: number;
  otherIncomePerUnit: number;
  otherIncomeGrowth: number;

  // Operating Expenses (per unit monthly unless specified)
  propertyManagementPerUnit: number;
  staffPerUnit: number;
  repairsPerUnit: number;
  utilitiesPerUnit: number;
  marketingPerUnit: number;
  insurancePerUnit: number; // annual
  taxesPerUnit: number; // annual
  reservesPerUnit: number; // annual
  expenseGrowth: number;

  // Development Costs
  landCost: number;
  hardCostPerSf: number;
  softCostPct: number;
  ffePerUnit: number;
  developerFeePct: number;
  contingencyPct: number;
  closingCostPct: number;

  // Financing
  ltc: number; // Loan-to-Cost
  interestRate: number;
  loanTermYears: number;
  interestOnlyYears: number;
  loanFeesPct: number;

  // Exit Strategy
  exitYear: number;
  exitCapRate: number;
  sellingCostPct: number;
  condoSalePct: number;
  condoPremiumPct: number;
  condoConversionCost: number;
}

export interface ExtendedMultifamilyProjection {
  year: number;
  grossPotentialRent: number;
  vacancyLoss: number;
  concessionLoss: number;
  badDebtLoss: number;
  otherIncome: number;
  effectiveGrossIncome: number;
  operatingExpenses: number;
  noi: number;
  noiMargin: number;
  debtService: number;
  cashFlow: number;
  cumulativeCashFlow: number;
}

export interface ExtendedMultifamilyResults {
  // Unit Mix Results
  unitMixCounts: {
    studio: number;
    oneBed: number;
    twoBed: number;
    threeBed: number;
    penthouse: number;
  };
  averageUnitRent: number;
  averageUnitSf: number;
  rentableSf: number;

  // Development Costs
  hardCosts: number;
  softCosts: number;
  ffeTotal: number;
  developerFee: number;
  contingency: number;
  closingCosts: number;
  totalDevelopmentCost: number;
  loanAmount: number;
  loanFees: number;
  totalProjectCost: number;
  equityRequirement: number;

  // Operating Metrics
  grossPotentialRentYear1: number;
  otherIncomeYear1: number;
  operatingExpenseYear1: number;

  // Exit Metrics
  exitNoi: number;
  exitValue: number;
  sellingCosts: number;
  loanBalanceExit: number;
  netSaleProceeds: number;
  condoSaleValue: number;
  condoConversionCosts: number;
  condoNetValue: number;

  // Returns
  irr: number;
  equityMultiple: number;
  cashOnCash: number;
  stabilizedCapRate: number;
  noiMarginYear1: number;
  exitYear: number;

  // Projections
  projections: ExtendedMultifamilyProjection[];
  cashFlows: number[];
  cumulativeCashFlows: number[];
}

// Hotel Types
export interface HotelInputs {
  // Property Overview (5 fields)
  projectName: string;
  hotelType: string; // Luxury, Upper Upscale, Upscale, Midscale, Economy
  location: string;
  brandAffiliation: string;
  analyst: string;

  // Room & Demand (7 fields)
  rooms: number;
  adr: number; // Average Daily Rate
  year1Occupancy: number; // percentage (0-1)
  stabilizedOccupancy: number; // percentage (0-1)
  adrGrowthRate: number; // percentage (0-1)
  fnbGrowthRate: number; // percentage (0-1)
  otherIncomeGrowthRate: number; // percentage (0-1)

  // Ancillary Revenue (7 fields)
  fnbOutletPerRoomDay: number; // F&B outlet revenue per room-night
  banquetRevPerGroupRoom: number;
  groupRoomPct: number; // percentage (0-1)
  meetingRevPerRoom: number; // annual
  parkingRevPerRoom: number; // annual
  spaRevPerRoom: number; // annual
  otherOperatedRevPerRoom: number; // annual

  // Operating Expenses (9 fields)
  roomsDeptPct: number; // Rooms department expense as % of rooms revenue (0-1)
  fnbDeptPct: number; // F&B department expense as % of F&B revenue (0-1)
  otherDeptPct: number; // Other department expense as % of other revenue (0-1)
  adminPerRoom: number; // annual
  maintenancePerRoom: number; // annual
  utilitiesPerRoom: number; // annual
  insurancePct: number; // as % of revenue (0-1)
  propertyTaxPct: number; // as % of revenue (0-1)
  expenseGrowthRate: number; // percentage (0-1)

  // Financing & Exit (6 fields)
  totalProjectCost: number;
  loanToCost: number; // percentage (0-1)
  interestRate: number; // percentage (0-1)
  amortYears: number;
  holdPeriodYears: number;
  exitCapRate: number; // percentage (0-1)
}

export interface HotelProjection {
  year: number;
  occupancy: number;
  adr: number;
  revpar: number;
  roomsRevenue: number;
  fnbRevenue: number;
  otherRevenue: number;
  totalRevenue: number;
  departmentalExpenses: number;
  undistributed: number;
  insurance: number;
  propertyTax: number;
  totalExpenses: number;
  gop: number; // Gross Operating Profit
  gopMargin: number;
  noi: number;
  noiMargin: number;
  cashFlow: number;
  cumulativeCashFlow: number;
}

export interface HotelResults {
  // Financial Metrics
  loanAmount: number;
  equity: number;
  annualDebtService: number;

  // Revenue Mix (Year 1)
  year1RoomsRevenue: number;
  year1FnbRevenue: number;
  year1OtherRevenue: number;
  year1TotalRevenue: number;

  // Performance Metrics (Year 1)
  year1Occupancy: number;
  year1Adr: number;
  year1Revpar: number;
  year1Noi: number;
  year1NoiMargin: number;
  year1GopMargin: number;
  year1CashFlow: number;

  // Investment Returns
  dscr: number; // Debt Service Coverage Ratio
  irr: number;
  equityMultiple: number;

  // Exit Metrics
  exitNoi: number;
  exitValue: number;
  loanBalanceExit: number;
  netSaleProceeds: number;

  // Projections
  projections: HotelProjection[];
  cashFlows: number[];
  cumulativeCashFlows: number[];
}

// Mixed Use Types
export interface MixedUseInputs {
  // Property Overview (4 fields)
  projectName: string;
  location: string;
  totalBuildingSf: number;
  analysisYears: number;

  // Space Allocation (5 fields) - percentages (0-1)
  multifamilyAllocation: number;
  officeAllocation: number;
  retailAllocation: number;
  hotelAllocation: number;
  restaurantAllocation: number;

  // Multifamily Assumptions (6 fields)
  mfAvgUnitSf: number;
  mfAvgRent: number; // monthly rent per unit
  mfOccupancy: number; // percentage (0-1)
  mfRentGrowth: number; // percentage (0-1)
  mfOtherIncomePerUnit: number; // monthly per unit
  mfOperatingExpensePerUnit: number; // monthly per unit

  // Office Assumptions (7 fields)
  officeLoadFactor: number; // rentable vs gross (e.g., 1.2)
  officeRentPerSf: number; // annual rent per RSF
  officeOccupancy: number; // percentage (0-1)
  officeRentGrowth: number; // percentage (0-1)
  officeExpensePerSf: number; // annual expense per RSF
  officeExpenseRecovery: number; // percentage (0-1)

  // Retail Assumptions (7 fields)
  retailRentPerSf: number; // annual base rent per SF
  retailOccupancy: number; // percentage (0-1)
  retailRentGrowth: number; // percentage (0-1)
  retailPercentageRentPct: number; // percentage rent (0-1)
  retailSalesPerSf: number; // annual sales per SF
  retailCamPerSf: number; // annual CAM charges per SF
  retailExpensePerSf: number; // annual operating expense per SF

  // Hotel Assumptions (8 fields)
  hotelAvgRoomSf: number; // average SF per hotel room
  hotelAdr: number; // Average Daily Rate
  hotelOccupancy: number; // percentage (0-1)
  hotelRevparGrowth: number; // RevPAR growth rate (0-1)
  hotelFnbPerRoom: number; // daily F&B revenue per room
  hotelOtherPerRoom: number; // daily other revenue per room
  hotelOperatingExpensePct: number; // as % of revenue (0-1)
  hotelManagementFeePct: number; // as % of revenue (0-1)

  // Restaurant Assumptions (6 fields)
  restaurantRentPerSf: number; // annual base rent per SF
  restaurantPercentageRentPct: number; // percentage rent (0-1)
  restaurantSalesPerSf: number; // annual sales per SF
  restaurantOccupancy: number; // percentage (0-1)
  restaurantRentGrowth: number; // percentage (0-1)
  restaurantExpensePerSf: number; // annual operating expense per SF

  // Development Costs (9 fields)
  landCost: number;
  hardCostPerSf: number;
  softCostPct: number; // as % of hard costs (0-1)
  mfFfePerUnit: number; // FF&E cost per MF unit
  hotelFfePerRoom: number; // FF&E cost per hotel room
  restaurantFfePerSf: number; // FF&E cost per restaurant SF
  developerFeePct: number; // as % of subtotal (0-1)
  contingencyPct: number; // as % of hard+soft (0-1)

  // Financing (6 fields)
  ltc: number; // Loan-to-Cost (0-1)
  interestRate: number; // annual rate (0-1)
  loanTermYears: number;
  interestOnlyYears: number;
  loanFeesPct: number; // as % of loan amount (0-1)
  holdPeriodYears: number;

  // Exit Assumptions (6 fields)
  mfExitCap: number; // exit cap rate for multifamily (0-1)
  officeExitCap: number; // exit cap rate for office (0-1)
  retailExitCap: number; // exit cap rate for retail (0-1)
  hotelExitCap: number; // exit cap rate for hotel (0-1)
  restaurantExitCap: number; // exit cap rate for restaurant (0-1)
  sellingCostPct: number; // selling costs as % of value (0-1)
}

export interface MixedUseProjection {
  year: number;
  totalIncome: number;
  totalNoi: number;
  debtService: number;
  cashFlow: number;
  cumulativeCashFlow: number;
  componentNois: {
    Multifamily: number;
    Office: number;
    Retail: number;
    Hotel: number;
    Restaurant: number;
  };
}

export interface MixedUseResults {
  // Space Allocation
  componentSf: {
    Multifamily: number;
    Office: number;
    Retail: number;
    Hotel: number;
    Restaurant: number;
  };
  mfUnits: number;
  hotelRooms: number;
  officeRsf: number; // Rentable Square Feet

  // Development Costs
  hardCosts: number;
  softCosts: number;
  mfFfe: number;
  hotelFfe: number;
  restaurantFfe: number;
  developerFee: number;
  contingency: number;
  totalDevelopmentCost: number;
  loanAmount: number;
  loanFees: number;
  totalProjectCost: number;
  equity: number;

  // Component Performance (Year 1)
  componentNoiYear1: {
    Multifamily: number;
    Office: number;
    Retail: number;
    Hotel: number;
    Restaurant: number;
  };

  // Exit Metrics
  componentNoiExit: {
    Multifamily: number;
    Office: number;
    Retail: number;
    Hotel: number;
    Restaurant: number;
  };
  exitValues: {
    Multifamily: number;
    Office: number;
    Retail: number;
    Hotel: number;
    Restaurant: number;
  };
  totalExitValue: number;
  weightedExitCap: number;
  sellingCosts: number;
  loanBalanceExit: number;
  netSale: number;

  // Returns
  irr: number;
  equityMultiple: number;
  cashOnCash: number;
  exitYear: number;

  // Projections
  projections: MixedUseProjection[];
  cashFlows: number[];
  cumulativeCashFlows: number[];
}

// Subdivision Development Calculator Types
export interface SubdivisionInputs {
  // Project Information
  projectName: string;
  location: string;
  analyst: string;

  // Land Acquisition
  totalAcres: number;
  landCostPerAcre: number;
  closingCosts: number;
  dueDiligenceCosts: number;

  // Subdivision Details
  totalLots: number;
  averageLotSizeAcres: number;
  lotTypes: {
    standard: { count: number; size: number; salePrice: number };
    premium: { count: number; size: number; salePrice: number };
    estate: { count: number; size: number; salePrice: number };
  };

  // Development Costs
  siteworkPerAcre: number; // Grading, clearing
  streetsPerFoot: number; // Road construction cost per linear foot
  totalStreetFeet: number; // Total linear feet of streets
  waterSewerPerLot: number; // Utilities per lot
  stormwaterPerAcre: number; // Drainage systems
  landscapingPerAcre: number; // Common areas
  amenitiesCost: number; // Clubhouse, pool, etc.
  contingencyPct: number; // Construction contingency

  // Soft Costs
  engineeringPct: number; // % of hard costs
  architecturePct: number;
  legalPermitsPct: number;
  marketingSalesPct: number; // % of gross sales
  developerFeePct: number;

  // Sales Assumptions
  absorptionMonths: number; // Total sellout period
  salesStartMonth: number; // When sales begin after acquisition
  priceEscalationPct: number; // Annual price appreciation

  // Financing
  ltc: number; // Loan to cost
  interestRate: number; // Annual rate
  loanTermYears: number;
  loanFeesPct: number;

  // Costs During Development
  propertyTaxRate: number; // Annual % of land value
  insuranceAnnual: number;
  maintenanceMonthly: number;
}

export interface SubdivisionResults {
  // Land & Acquisition
  totalLandCost: number;
  totalAcquisitionCost: number;
  costPerLot: number;
  costPerAcre: number;

  // Development Costs
  siteworkCost: number;
  streetsCost: number;
  utilitiesCost: number;
  stormwaterCost: number;
  landscapingCost: number;
  amenitiesCost: number;
  totalHardCosts: number;
  hardCostPerLot: number;

  // Soft Costs
  engineeringCost: number;
  architectureCost: number;
  legalPermitsCost: number;
  marketingSalesCost: number;
  developerFee: number;
  totalSoftCosts: number;

  // Total Project Cost
  totalDevelopmentCost: number;
  allInCostPerLot: number;
  contingencyCost: number;

  // Financing
  loanAmount: number;
  loanFees: number;
  totalInterestCost: number;
  equityRequired: number;

  // Sales Revenue
  grossSalesRevenue: number;
  averageSalePricePerLot: number;
  netSalesRevenue: number;

  // Returns
  grossProfit: number;
  grossProfitMargin: number;
  netProfit: number;
  netProfitMargin: number;
  irr: number;
  equityMultiple: number;
  cashOnCash: number;
  roi: number;

  // Timeline
  totalMonths: number;
  developmentMonths: number;
  salesMonths: number;

  // Monthly Projections
  projections: SubdivisionProjection[];
}

export interface SubdivisionProjection {
  month: number;
  phase: 'acquisition' | 'development' | 'sales' | 'completed';
  lotsSold: number;
  cumulativeLotsSold: number;
  monthlyRevenue: number;
  cumulativeRevenue: number;
  monthlyCosts: number;
  cumulativeCosts: number;
  loanBalance: number;
  interestExpense: number;
  cashFlow: number;
  cumulativeCashFlow: number;
}

// Lease Analyzer Types
export interface LeaseAnalyzerInputs {
  // Property Profile
  projectName: string;
  location: string;
  analyst: string;
  propertyType: string;
  totalSquareFootage: number;
  numTenants: number;

  // Lease Economics
  weightedAvgRentPsf: number;
  totalAnnualRent: number;
  vacancyRate: number;
  operatingExpenseRatio: number;
  annualRentGrowth: number;
  weightedAvgLeaseTerm: number;

  // Leasing Costs
  tenantImprovementPsf: number;
  leasingCommissionPct: number;

  // Lease Rollover Schedule
  leaseExpiryYear1: number;
  leaseExpiryYear2: number;
  leaseExpiryYear3: number;
  leaseExpiryYear4: number;
  leaseExpiryYear5: number;

  // Market Assumptions
  renewalProbability: number;
  marketRentPsf: number;
  freeRentMonths: number;

  // Valuation
  capRate: number;
  projectionYears: number;

  // Metadata
  tags: string;
  purpose: string;
  references: string;
  notes: string;
}

export interface LeaseAnalyzerProjection {
  year: number;
  occupiedSf: number;
  rolloverSf: number;
  renewedSf: number;
  newTenantSf: number;
  rentPsf: number;
  grossRent: number;
  freeRentLoss: number;
  effectiveGrossIncome: number;
  operatingExpenses: number;
  noi: number;
  tiCost: number;
  commission: number;
  totalLeasingCosts: number;
  cashFlow: number;
  propertyValue: number;
}

export interface LeaseAnalyzerResults {
  totalSf: number;
  occupiedSf: number;
  walt: number;
  avgRentPsf: number;
  marketRentPsf: number;
  avgAnnualNoi: number;
  avgAnnualCashFlow: number;
  totalLeasingCosts: number;
  stabilizedValue: number;
  capRate: number;
  projections: LeaseAnalyzerProjection[];
}

// Renovation Budget Types
export interface RenovationBudgetInputs {
  // Property Profile
  projectName: string;
  location: string;
  analyst: string;
  propertyType: string;
  totalUnits: number;
  squareFootagePerUnit: number;
  totalSquareFootage: number;

  // Interior Renovation Costs
  kitchenRenovationPerUnit: number;
  bathroomRenovationPerUnit: number;
  flooringPerUnit: number;
  paintPerUnit: number;
  appliancesPerUnit: number;
  fixturesPerUnit: number;

  // Systems & Mechanical
  hvacPerUnit: number;
  electricalPerUnit: number;
  plumbingPerUnit: number;
  otherPerUnit: number;

  // Exterior & Common Areas
  commonAreaRenovation: number;
  exteriorImprovements: number;
  landscaping: number;
  parkingLotRepaving: number;

  // Major Capital Items
  roofReplacement: number;
  structuralRepairs: number;

  // Budget Adjustments
  contingencyPct: number;
  softCostsPct: number;

  // Revenue Impact
  currentAvgRent: number;
  postRenoAvgRent: number;
  currentOccupancy: number;
  stabilizedOccupancy: number;

  // Timeline & Financing
  monthsToComplete: number;
  unitsRenovatedPerMonth: number;
  financingCostPct: number;
  holdingCostsMonthly: number;

  // Metadata
  tags: string;
  purpose: string;
  references: string;
  notes: string;
}

export interface RenovationBudgetResults {
  totalUnits: number;
  interiorPerUnit: number;
  totalInteriorCosts: number;
  exteriorCosts: number;
  majorCapital: number;
  hardCosts: number;
  contingency: number;
  softCosts: number;
  totalBudget: number;
  financingCosts: number;
  totalHoldingCosts: number;
  allInCost: number;
  costPerUnit: number;
  costPerSf: number;
  currentMonthlyRevenue: number;
  stabilizedMonthlyRevenue: number;
  monthlyRevenueIncrease: number;
  annualRevenueIncrease: number;
  renovationYield: number;
  paybackYears: number;
  breakdown: {
    kitchen: number;
    bathroom: number;
    flooring: number;
    paint: number;
    appliances: number;
    fixtures: number;
    hvac: number;
    electrical: number;
    plumbing: number;
    other: number;
    commonAreas: number;
    exterior: number;
    landscaping: number;
    parking: number;
    roof: number;
    structural: number;
  };
}

// Small Multifamily Acquisition Types (2-10 Units with Conversion Strategies)
export interface UnitDetail {
  unitNumber: number;
  bedrooms: number;
  bathrooms: number;
  squareFootage: number;
  currentRent: number;
  marketRent: number;
  condition: 'excellent' | 'good' | 'fair' | 'poor';
  occupancyStatus: 'occupied' | 'vacant';
  leaseEndDate?: string;
  notes: string;
}

export interface UnitRenovationCosts {
  unitNumber: number;
  kitchen: number;
  bathroom: number;
  flooring: number;
  interiorPaint: number;
  exteriorPaint: number;
  appliances: number;
  plumbing: number;
  electrical: number;
  hvac: number;
  windowsDoors: number;
  landscaping: number;
  roof: number;
  other: number;
  subtotal: number;
  contingency: number;
  total: number;
}

export interface FinancingScenario {
  name: string;
  downPaymentPct: number;
  interestRate: number;
  loanTermYears: number;
  loanType: 'conventional' | 'fha' | 'hard-money' | 'commercial';
  cashRequired: number;
  loanAmount: number;
  monthlyPayment: number;
  isSelected: boolean;
}

export interface ConversionCosts {
  type: 'condo' | 'townhome' | 'coop' | 'subdivision' | 'none';
  surveyEngineering: number;
  legalFees: number;
  hoaCoopFormation: number;
  titleWorkPerUnit: number;
  countyPermits: number;
  utilitySeparation: number;
  environmentalInspections: number;
  architecturalPlans: number;
  insuranceDuringConversion: number;
  other: number;
  total: number;
  costPerUnit: number;
  timelineMonths: number;
}

export interface ExitStrategy {
  strategyType: 'subdivide-convert' | 'sell-as-is' | 'brrrr' | 'hybrid' | 'wholesale';
  name: string;
  description: string;

  // Subdivide/Convert
  individualUnitPrices?: number[];
  grossProceeds?: number;
  sellingCosts?: number;
  netProceeds?: number;

  // Sell As-Is
  asIsPrice?: number;

  // BRRRR
  stabilizedValue?: number;
  refinanceAmount?: number;
  refinanceLtv?: number;
  annualRentalIncome?: number;
  annualExpenses?: number;
  annualDebtService?: number;
  annualCashFlow?: number;
  cashOnCashReturn?: number;
  cashLeftInDeal?: number;

  // Hybrid
  unitsToSell?: number;
  unitsToHold?: number;
  soldUnitPrices?: number[];
  heldUnitValues?: number[];
  heldUnitRentalIncome?: number;

  // Wholesale
  assignmentFee?: number;
  dueDiligenceCosts?: number;

  // Common metrics
  netProfit: number;
  roi: number;
  timelineMonths: number;
  totalValueCreated?: number;
}

export interface MonthlyProjection {
  month: number;
  phase: 'acquisition' | 'renovation' | 'conversion' | 'sales' | 'stabilized';
  cashInflows: number;
  cashOutflows: number;
  netCashFlow: number;
  cumulativeCashFlow: number;
  loanBalance: number;
  unitsRenovated: number;
  unitsSold: number;
  unitsHeld: number;
  description: string;
}

export interface SmallMultifamilyAcquisitionInputs {
  // Project Information
  projectName: string;
  location: string;
  analyst: string;

  // Property Details
  address: string;
  propertyType: 'duplex' | 'triplex' | 'quadplex' | '5-unit' | '6-unit' | '7-10-unit';
  numberOfUnits: number;
  totalBuildingSF: number;
  lotSizeAcres: number;
  yearBuilt: number;
  zoning: string;
  conversionAllowed: boolean;

  // Individual Unit Details
  units: UnitDetail[];

  // Acquisition
  purchasePrice: number;
  closingCostsPct: number;
  inspectionDueDiligence: number;

  // Financing Scenarios (4 options)
  financingScenarios: FinancingScenario[];
  selectedFinancingIndex: number;

  // Renovation Budget
  unitRenovations: UnitRenovationCosts[];
  globalContingencyPct: number;

  // Conversion Costs
  conversionCosts: ConversionCosts;

  // Exit Strategy Parameters
  // For Subdivide/Convert
  conversionPremiumPct: number;

  // For As-Is Sale
  asIsSaleCapRate: number;

  // For BRRRR
  refinanceLTV: number;
  seasoningMonths: number;
  stabilizedVacancyPct: number;
  propertyManagementPct: number;
  maintenancePct: number;
  insuranceAnnual: number;
  taxesAnnual: number;

  // For Hybrid
  hybridUnitsToSell: number;

  // For Wholesale
  wholesaleAssignmentFee: number;

  // Timeline
  renovationMonths: number;
  conversionMonths: number;
  salesMonthsPerUnit: number;

  // Holding Costs
  holdingCostsMonthly: number;
}

export interface SmallMultifamilyAcquisitionResults {
  // Project Summary
  totalProjectCost: number;
  cashRequired: number;
  peakCapitalRequirement: number;

  // Acquisition Details
  purchasePrice: number;
  closingCosts: number;
  totalAcquisitionCost: number;

  // Selected Financing
  selectedFinancing: FinancingScenario;
  loanAmount: number;
  downPayment: number;
  monthlyMortgagePayment: number;

  // Renovation Summary
  totalRenovationCost: number;
  avgCostPerUnit: number;
  renovationContingency: number;

  // Conversion Summary
  totalConversionCost: number;
  conversionCostPerUnit: number;
  conversionTimeline: number;
  conversionPremium: number;

  // Exit Strategies Comparison
  exitStrategies: ExitStrategy[];
  recommendedStrategy: ExitStrategy;
  strategyRankings: { strategy: string; rank: number; score: number }[];

  // Cash Flow Analysis
  monthlyProjections: MonthlyProjection[];
  totalMonthsToCompletion: number;
  totalHoldingCosts: number;
  maxCashOutflow: number;

  // Key Metrics
  asIsValue: number;
  individualUnitsTotal: number;
  maxProfitPotential: number;
  safestStrategy: string;
  fastestStrategy: string;
  highestROI: number;

  // Risk Analysis
  conversionRisk: 'low' | 'medium' | 'high';
  marketRisk: 'low' | 'medium' | 'high';
  capitalRisk: 'low' | 'medium' | 'high';
  overallRisk: 'low' | 'medium' | 'high';
}
