import {
  Home as HomeIcon,
  HomeWork as HomeWorkIcon,
  Apartment as ApartmentIcon,
  Hotel as HotelIcon,
  Business as BusinessIcon,
  Domain as DomainIcon,
  Description as DescriptionIcon,
  Build as BuildIcon,
  Construction as ConstructionIcon,
} from '@mui/icons-material';
import { SvgIconComponent } from '@mui/icons-material';

export interface ModelConfig {
  id: string;
  label: string;
  icon: SvgIconComponent;
  path: string;
  color: string;
  description: string;
  category: 'residential' | 'commercial' | 'mixed' | 'tools';
  quickStartGuide?: string;
  keyMetrics?: Array<{
    name: string;
    target: string;
    formula?: string;
  }>;
  docFiles?: Array<{
    name: string;
    path: string;
  }>;
}

export const MODEL_CONFIGS: Record<string, ModelConfig> = {
  fix_and_flip: {
    id: 'fix_and_flip',
    label: 'Fix & Flip',
    icon: HomeIcon,
    path: '/real-estate-models/fix-and-flip',
    color: '#1976d2',
    category: 'residential',
    description: 'Analyze short-term renovation projects with comprehensive financial modeling including MAO calculation, renovation costs, holding expenses, and exit strategies using the 70% rule.',
    quickStartGuide: `
## Quick Start (5 Steps)

1. **Open** the Calculator tab
2. **Enter** your property details and purchase price
3. **Input** renovation costs and ARV (After Repair Value)
4. **Review** the 70% Rule calculation
5. **Analyze** profitability metrics and recommendations

## The 70% Rule (Core Formula)

\`\`\`
Maximum Allowable Offer (MAO) = (ARV × 70%) - Repair Costs
\`\`\`

**Example:**
- ARV: $300,000
- Repairs: $50,000
- **MAO = $160,000** ← Don't pay more than this!
    `,
    keyMetrics: [
      { name: 'ROI', target: '20%+', formula: 'Gross Profit / Cash Invested' },
      { name: 'Profit Margin', target: '15%+', formula: 'Gross Profit / ARV' },
      { name: 'Gross Profit', target: '$35k+', formula: 'ARV - Selling Costs - All-In Cost' },
    ],
  },
  single_family_rental: {
    id: 'single_family_rental',
    label: 'Single Family Rental',
    icon: HomeWorkIcon,
    path: '/real-estate-models/single-family-rental',
    color: '#2e7d32',
    category: 'residential',
    description: 'Model long-term buy-and-hold strategies including BRRRR (Buy, Rehab, Rent, Refinance, Repeat), with 30-year cash flow projections and multiple exit scenarios.',
    quickStartGuide: `
## Quick Start

1. **Enter** property details and purchase price
2. **Input** monthly rent and operating expenses
3. **Set** financing terms (LTV, interest rate, term)
4. **Configure** growth assumptions (rent, appreciation, vacancy)
5. **Review** cash flow projections and exit strategies

## Key Metrics Targets

| Metric | Target | Excellent |
|--------|--------|-----------|
| **1% Rule** | ≥1.0% | ≥1.5% |
| **Cap Rate** | ≥7.0% | ≥9.0% |
| **Cash-on-Cash** | ≥10% | ≥15% |
| **DSCR** | ≥1.25x | ≥1.35x |
| **10-Year IRR** | ≥15% | ≥20% |
    `,
    keyMetrics: [
      { name: '1% Rule', target: '≥1.0%', formula: 'Monthly Rent / Purchase Price' },
      { name: 'Cap Rate', target: '≥7.0%', formula: 'NOI / All-In Cost' },
      { name: 'Cash-on-Cash', target: '≥10%', formula: 'Annual CF / Initial Investment' },
      { name: 'DSCR', target: '≥1.25x', formula: 'NOI / Annual Debt Service' },
    ],
  },
  small_multifamily: {
    id: 'small_multifamily',
    label: 'Small Multifamily',
    icon: ApartmentIcon,
    path: '/real-estate-models/small-multifamily',
    color: '#9c27b0',
    category: 'residential',
    description: 'Evaluate small multifamily properties (2-6 units) with unit-by-unit analysis, value-add strategies, and comprehensive disposition planning.',
    quickStartGuide: `
## Quick Start

1. **Set** number of units (2-6)
2. **Enter** rent per unit and unit details
3. **Input** purchase price and renovation costs
4. **Configure** operating expenses and financing
5. **Review** NOI, DSCR, and IRR projections

## Best For

- Duplexes, triplexes, quad-plexes
- Small apartment buildings (up to 6 units)
- Value-add renovation opportunities
- First-time multifamily investors
    `,
    keyMetrics: [
      { name: 'Cap Rate', target: '6-8%', formula: 'NOI / Purchase Price' },
      { name: 'DSCR', target: '≥1.25x', formula: 'NOI / Annual Debt Service' },
      { name: 'IRR', target: '≥15%', formula: 'Internal Rate of Return' },
    ],
  },
  extended_multifamily: {
    id: 'extended_multifamily',
    label: 'High-Rise Multifamily',
    icon: DomainIcon,
    path: '/real-estate-models/extended-multifamily',
    color: '#7b1fa2',
    category: 'residential',
    description: 'Extended multifamily analysis for high-rise developments (7+ units) with institutional-grade reporting, detailed unit mix, and lease-up schedules.',
    quickStartGuide: `
## Quick Start

1. **Enter** total units and unit mix breakdown
2. **Input** T12 operating expenses and revenue
3. **Set** value-add business plan assumptions
4. **Configure** institutional financing structure
5. **Review** 10-year cash flow and exit analysis
    `,
    keyMetrics: [
      { name: 'IRR', target: '15-22%', formula: 'Internal Rate of Return' },
      { name: 'Equity Multiple', target: '2.0-3.0x', formula: 'Total Return / Equity' },
      { name: 'Cash-on-Cash', target: '8-12%', formula: 'Annual CF / Equity' },
    ],
  },
  hotel: {
    id: 'hotel',
    label: 'Hotel Model',
    icon: HotelIcon,
    path: '/real-estate-models/hotel',
    color: '#ed6c00',
    category: 'commercial',
    description: 'Comprehensive hotel financial modeling covering rooms revenue, F&B operations, meeting/event spaces, and ancillary outlets with stabilized P&L projections.',
    quickStartGuide: `
## Quick Start (10 Minutes)

1. **Property Basics**: Name, type (Luxury/Upscale/Midscale/Economy), location
2. **Rooms**: Number of rooms, ADR (Average Daily Rate), occupancy %
3. **Revenue**: F&B outlets, banquet revenue, group business %
4. **Expenses**: Operating expense ratios, franchise fees
5. **Development**: Construction costs, FF&E, financing
6. **Exit**: Hold period, exit cap rate

## 2024 Industry Benchmarks

| Segment | ADR | Occupancy | RevPAR |
|---------|-----|-----------|--------|
| **Luxury** | $380 | 68-75% | $200-375 |
| **Upper Upscale** | $227 | 68-72% | $135-215 |
| **Upscale** | $186 | 68-72% | $80-145 |
| **Midscale** | $95 | 58-65% | $40-75 |
    `,
    keyMetrics: [
      { name: 'RevPAR', target: 'Varies by segment', formula: 'ADR × Occupancy%' },
      { name: 'GOP Margin', target: '25-45%', formula: 'GOP / Total Revenue' },
      { name: 'IRR', target: '15-25%', formula: 'Internal Rate of Return' },
      { name: 'Equity Multiple', target: '2.0-3.0x', formula: 'Total Return / Equity' },
    ],
  },
  mixed_use: {
    id: 'mixed_use',
    label: 'Mixed-Use',
    icon: BusinessIcon,
    path: '/real-estate-models/mixed-use',
    color: '#1565c0',
    category: 'mixed',
    description: 'Complex mixed-use development modeling combining residential, retail, office, and hotel components with integrated cash flow analysis.',
    quickStartGuide: `
## Quick Start

1. **Define** component mix (Residential %, Retail %, Office %, Hotel %)
2. **Enter** square footage and revenue assumptions per component
3. **Input** development costs and phasing schedule
4. **Configure** financing structure per component
5. **Analyze** weighted returns and exit strategies

## Best For

- Urban mixed-use towers
- Multi-component developments
- Complex financing structures
- Transit-oriented developments
    `,
    keyMetrics: [
      { name: 'Blended IRR', target: '15-20%', formula: 'Weighted avg of all components' },
      { name: 'Weighted Cap Rate', target: '5-7%', formula: 'Blended NOI / Total Cost' },
      { name: 'Project IRR', target: '18-25%', formula: 'Total project IRR' },
    ],
  },
  lease_analyzer: {
    id: 'lease_analyzer',
    label: 'Lease Analyzer',
    icon: DescriptionIcon,
    path: '/real-estate-models/lease-analyzer',
    color: '#0288d1',
    category: 'tools',
    description: 'AI-powered lease document processing and rent roll analytics for commercial real estate portfolio management. Extract key terms, calculate WALT, and analyze rollover risk.',
    quickStartGuide: `
## Quick Start

1. **Upload** lease PDF or rent roll document
2. **Extract** key lease terms automatically (30 seconds)
3. **Review** abstracted data (tenant, rent, dates, options)
4. **Analyze** rent roll metrics (WALT, loss-to-lease, rollover risk)
5. **Generate** comprehensive Excel reports

## Key Features

- ✅ Lease abstraction from PDFs
- ✅ Rent roll processing
- ✅ Mark-to-market analysis
- ✅ WALT calculation
- ✅ Rollover risk analysis
- ✅ Automated Excel reports
    `,
    keyMetrics: [
      { name: 'WALT', target: '5-7 years', formula: 'Weighted Average Lease Term' },
      { name: 'Occupancy', target: '90%+', formula: 'Occupied SF / Total SF' },
      { name: 'Loss to Lease', target: '<10%', formula: '(Market Rent - In-Place Rent) / Market Rent' },
    ],
  },
  renovation_budget: {
    id: 'renovation_budget',
    label: 'Renovation Budget',
    icon: BuildIcon,
    path: '/real-estate-models/renovation-budget',
    color: '#f57c00',
    category: 'tools',
    description: 'Value-add renovation budget builder for multifamily properties. Track costs, schedule, and ROI for unit turns, common area upgrades, and capital improvements.',
    quickStartGuide: `
## Quick Start

1. **Property** details and total units
2. **Scope** of renovation (interior, exterior, common areas)
3. **Budget** per unit and timeline
4. **Schedule** renovation phases
5. **Analyze** value creation and ROI

## Renovation Scopes

- **Interior**: Kitchens, bathrooms, flooring, paint
- **Exterior**: Facade, landscaping, signage
- **Common Areas**: Lobby, gym, pool, amenities
- **Systems**: HVAC, plumbing, electrical
- **Capital**: Roof, windows, parking
    `,
    keyMetrics: [
      { name: 'Renovation ROI', target: '15-25%', formula: 'Rent Increase / Renovation Cost' },
      { name: 'Payback Period', target: '<3 years', formula: 'Renovation Cost / Annual Rent Increase' },
      { name: 'Value Created', target: '2-3x', formula: 'NOI Increase / Renovation Cost at Cap Rate' },
    ],
  },
  small_multifamily_acquisition: {
    id: 'small_multifamily_acquisition',
    label: 'Small Multifamily Acquisition',
    icon: ApartmentIcon,
    path: '/real-estate-models/small-multifamily-acquisition',
    color: '#673ab7',
    category: 'residential',
    description: 'Detailed acquisition analysis for small multifamily properties (2-20 units) including unit-by-unit renovation strategies and comprehensive exit analysis.',
    quickStartGuide: `
## Quick Start

1. **Property** details (type, units, SF, year built)
2. **Acquisition** costs (purchase, closing, renovation)
3. **Financing** terms (LTV, interest rate, term)
4. **Holding** costs (insurance, utilities, taxes)
5. **Exit** assumptions (cap rate, selling costs)

## Best For

- Duplex, triplex, quadplex acquisitions
- Small multifamily (2-20 units)
- Value-add opportunities
- Hold-period analysis (3-7 years)
    `,
    keyMetrics: [
      { name: 'Cash-on-Cash', target: '10-15%', formula: 'Annual CF / Equity Required' },
      { name: 'IRR', target: '15-20%', formula: 'Internal Rate of Return' },
      { name: 'Cap Rate', target: '6-8%', formula: 'NOI / Total Project Cost' },
      { name: 'DSCR', target: '≥1.25x', formula: 'NOI / Annual Debt Service' },
    ],
  },
  subdivision: {
    id: 'subdivision',
    label: 'Subdivision / Condo Conversion',
    icon: ConstructionIcon,
    path: '/real-estate-models/subdivision',
    color: '#5e35b1',
    category: 'residential',
    description: 'Analyze multi-unit subdivision and condo conversion opportunities with comprehensive exit strategy comparison including subdivide & sell, sell as-is, BRRRR, and hybrid approaches.',
    quickStartGuide: `
## Quick Start

1. **Property** details (units, SF, beds/baths)
2. **Purchase** price and financing
3. **Renovation** costs per unit
4. **Conversion** costs (legal, survey, HOA formation)
5. **Exit** strategies (Subdivide, As-Is, BRRRR, Hybrid)

## Exit Strategies

- **Subdivide & Sell**: Maximum profit (15-40% premium)
- **Sell As-Is**: Quick exit to investors
- **BRRRR**: Refinance and hold for cash flow
- **Hybrid**: Sell some units, keep some
    `,
    keyMetrics: [
      { name: 'Subdivide ROI', target: '25-40%', formula: 'Total Return / Investment' },
      { name: 'As-Is ROI', target: '15-25%', formula: 'Sale Price / All-In Cost' },
      { name: 'BRRRR Cash-on-Cash', target: '10-15%', formula: 'Annual CF / Cash Left In' },
    ],
  },
  tax_strategy: {
    id: 'tax_strategy',
    label: 'Tax Strategy Integration',
    icon: DescriptionIcon,
    path: '/real-estate-models/tax-strategy',
    color: '#00695c',
    category: 'tools',
    description: 'Comprehensive tax planning and optimization toolkit including 1031 Exchange modeling, Cost Segregation analysis, Opportunity Zone benefits, Entity Structure comparison, and Depreciation Recapture.',
    quickStartGuide: `
## Quick Start

1. **Property** value and purchase details
2. **Tax** situation (rates, entity type, holding period)
3. **Strategies** to analyze (1031, Cost Seg, OZ, etc.)
4. **Exit** planning (date, sale price, replacement property)
5. **Compare** tax savings across strategies

## Tax Strategies

- **1031 Exchange**: Tax-deferred exchange
- **Cost Segregation**: Accelerated depreciation
- **Opportunity Zones**: Tax elimination potential
- **Entity Structure**: LLC vs S-Corp vs Partnership
- **Depreciation Recapture**: Exit tax calculation
    `,
    keyMetrics: [
      { name: '1031 Tax Deferral', target: 'Varies', formula: 'Capital Gains Tax Deferred' },
      { name: 'Cost Seg Savings', target: '15-30%', formula: 'NPV of Accelerated Depreciation' },
      { name: 'OZ Tax Elimination', target: '100%', formula: 'Capital Gains Eliminated after 10 years' },
    ],
  },
  portfolio_dashboard: {
    id: 'portfolio_dashboard',
    label: 'Multi-Property Portfolio Dashboard',
    icon: DomainIcon,
    path: '/real-estate-models/portfolio-dashboard',
    color: '#004d40',
    category: 'tools',
    description: 'Comprehensive portfolio analytics dashboard featuring consolidated performance metrics, property comparison matrix, diversification analysis, rebalancing recommendations, and automated alerts.',
    quickStartGuide: `
## Quick Start

1. **Add** properties to portfolio (name, type, value, NOI)
2. **Configure** portfolio settings (reserves, thresholds)
3. **Review** consolidated metrics (total value, cash flow, IRR)
4. **Analyze** diversification (by type, geography, concentration)
5. **Monitor** alerts (lease expirations, rate resets)

## Key Features

- ✅ Consolidated performance metrics
- ✅ Property comparison matrix
- ✅ Correlation analysis & HHI
- ✅ Rebalancing recommendations
- ✅ Automated alerts
    `,
    keyMetrics: [
      { name: 'Portfolio IRR', target: '15-20%', formula: 'Weighted Average IRR' },
      { name: 'Diversification Score', target: '70-100', formula: 'Based on HHI and correlation' },
      { name: 'Weighted Cap Rate', target: '6-8%', formula: 'Total NOI / Total Portfolio Value' },
    ],
  },
};

export const getModelConfig = (modelId: string): ModelConfig | undefined => {
  return MODEL_CONFIGS[modelId];
};

export const getAllModels = (): ModelConfig[] => {
  return Object.values(MODEL_CONFIGS);
};

export const getModelsByCategory = (category: string): ModelConfig[] => {
  return Object.values(MODEL_CONFIGS).filter((model) => model.category === category);
};
