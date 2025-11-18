# Scenario Analysis & Stress Testing Integration Guide

## Overview

The `ScenarioAnalysis` component provides comprehensive risk analysis for all financial models including:

- **Monte Carlo Simulations** - Run 10,000+ iterations to understand probability distributions
- **Sensitivity Analysis** - Tornado charts and 2D sensitivity tables
- **Waterfall Charts** - Visualize value drivers and their impact
- **Break-Even Analysis** - Calculate required changes to hit targets
- **Downside Protection** - Risk metrics and Value-at-Risk (VaR)

## Quick Integration Example

### Step 1: Import the Component

```typescript
import { ScenarioAnalysis } from '../../components/ScenarioAnalysis/ScenarioAnalysis';
```

### Step 2: Define Your Variables

```typescript
const variables: Variable[] = [
  {
    name: 'revenue',
    label: 'Revenue',
    baseValue: 1000000,
    min: 500000,
    max: 1500000,
    step: 50000,
    unit: '$',
  },
  {
    name: 'growthRate',
    label: 'Growth Rate',
    baseValue: 5,
    min: 0,
    max: 15,
    step: 0.5,
    unit: '%',
  },
  // Add more variables...
];
```

### Step 3: Create Calculation Function

```typescript
const calculateNPV = (vars: Record<string, number>): number => {
  // Your valuation logic here
  const fcf = vars.revenue * (vars.ebitdaMargin / 100) - vars.capex;
  const terminalValue = fcf * (1 + vars.terminalGrowth / 100) / (vars.wacc / 100 - vars.terminalGrowth / 100);
  // ... complete DCF calc
  return npv;
};
```

### Step 4: Add to Your Tab Structure

```typescript
// Add new tab
<Tab label="Scenario Analysis" icon={<AssessmentIcon />} iconPosition="start" />

// Add TabPanel
<TabPanel value={tabValue} index={4}>
  <ScenarioAnalysis
    calculateMetric={calculateNPV}
    variables={variables}
    metricName="NPV"
    metricUnit="$"
    breakEvenTarget={0}
  />
</TabPanel>
```

## Full DCF Model Example

```typescript
export const DCFModelEnhanced: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [inputs, setInputs] = useState({
    revenue: '1000000',
    ebitdaMargin: '25',
    capex: '50000',
    nwcChange: '10000',
    taxRate: '21',
    wacc: '10',
    terminalGrowth: '3',
    // ... other inputs
  });

  // Define variables for scenario analysis
  const scenarioVariables: Variable[] = [
    {
      name: 'revenue',
      label: 'Base Revenue',
      baseValue: parseFloat(inputs.revenue || '0'),
      min: parseFloat(inputs.revenue || '0') * 0.5,
      max: parseFloat(inputs.revenue || '0') * 1.5,
      step: 10000,
      unit: '$',
    },
    {
      name: 'ebitdaMargin',
      label: 'EBITDA Margin',
      baseValue: parseFloat(inputs.ebitdaMargin || '0'),
      min: 10,
      max: 40,
      step: 1,
      unit: '%',
    },
    {
      name: 'wacc',
      label: 'WACC',
      baseValue: parseFloat(inputs.wacc || '0'),
      min: 5,
      max: 20,
      step: 0.5,
      unit: '%',
    },
    // ... more variables
  ];

  // Calculation function
  const calculateDCFValue = (vars: Record<string, number>): number => {
    // Simplified DCF calculation
    const fcf = vars.revenue * (vars.ebitdaMargin / 100) - parseFloat(inputs.capex || '0');
    const pv = fcf / (1 + vars.wacc / 100);
    const terminalValue = fcf * (1 + vars.terminalGrowth / 100) / (vars.wacc / 100 - vars.terminalGrowth / 100);
    const pvTerminal = terminalValue / Math.pow(1 + vars.wacc / 100, 5);

    return pv + pvTerminal;
  };

  return (
    <Box>
      <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
        <Tab label="Inputs" />
        <Tab label="Outputs" />
        <Tab label="Valuation" />
        <Tab label="Comparables" />
        <Tab label="Scenario Analysis" /> {/* NEW TAB */}
      </Tabs>

      {/* ... existing tabs ... */}

      <TabPanel value={tabValue} index={4}>
        <ScenarioAnalysis
          calculateMetric={calculateDCFValue}
          variables={scenarioVariables}
          metricName="Enterprise Value"
          metricUnit="$"
          breakEvenTarget={0}
        />
      </TabPanel>
    </Box>
  );
};
```

## LBO Model Example

```typescript
const scenarioVariables: Variable[] = [
  {
    name: 'entryMultiple',
    label: 'Entry EBITDA Multiple',
    baseValue: 8.0,
    min: 6.0,
    max: 12.0,
    step: 0.5,
    unit: 'x',
  },
  {
    name: 'exitMultiple',
    label: 'Exit EBITDA Multiple',
    baseValue: 10.0,
    min: 7.0,
    max: 13.0,
    step: 0.5,
    unit: 'x',
  },
  {
    name: 'debtRatio',
    label: 'Debt / Total Capital',
    baseValue: 60,
    min: 40,
    max: 75,
    step: 5,
    unit: '%',
  },
  {
    name: 'revenueGrowth',
    label: 'Revenue CAGR',
    baseValue: 5,
    min: 0,
    max: 15,
    step: 1,
    unit: '%',
  },
];

const calculateIRR = (vars: Record<string, number>): number => {
  // Your LBO IRR calculation
  const purchasePrice = baseEBITDA * vars.entryMultiple;
  const exitPrice = projectedEBITDA * vars.exitMultiple;
  const equity = purchasePrice * (1 - vars.debtRatio / 100);
  // ... IRR calculation
  return irr;
};

<ScenarioAnalysis
  calculateMetric={calculateIRR}
  variables={scenarioVariables}
  metricName="IRR"
  metricUnit="%"
  breakEvenTarget={15}  // Target 15% IRR
/>
```

## Features Breakdown

### 1. Monte Carlo Simulation
- Runs up to 100,000 iterations
- Assumes normal distribution around base values
- Provides full statistical analysis (mean, std dev, percentiles)
- Shows probability distribution histogram
- Calculates probability of exceeding target

### 2. Sensitivity Analysis
- **Tornado Chart**: Shows variables sorted by impact (most sensitive at top)
- **2D Sensitivity Table**: Heat map showing interaction between two variables
- Color-coded cells (green = above base, red = below base)

### 3. Scenario Comparison
- Pre-defined scenarios: Base, Optimistic, Pessimistic
- Bar chart visualization
- Can be customized per model

### 4. Waterfall Chart
- Shows cumulative impact of each variable
- Base case + incremental changes
- Color-coded (green for positive, red for negative)

### 5. Break-Even Analysis
- Calculates exact value needed for each variable to hit target
- Shows % change required from base case
- Color-coded difficulty (green = easy, yellow = moderate, red = difficult)

### 6. Downside Protection
- Probability of loss
- Average negative outcome
- Worst case scenario
- 5th percentile (95% VaR)
- Risk assessment with recommendations

## Variable Configuration Best Practices

### For DCF Models
- Revenue growth rates (±50% of base)
- EBITDA margins (realistic range for industry)
- WACC (±5% of base)
- Terminal growth (0-5%)
- Tax rate (±10% of statutory rate)

### For LBO Models
- Entry/Exit multiples (±30% of base)
- Debt/Equity ratio (40-75%)
- Revenue growth (0-15% CAGR)
- EBITDA margin expansion (±500bps)

### For M&A Models
- Synergy realization (50-150% of projected)
- Integration costs (±50% of budget)
- Cross-sell revenue (0-200% of projection)
- Cost of capital (±300bps)

## Performance Notes

- Monte Carlo with 10,000 iterations: ~100-200ms
- Sensitivity tables (7x7): ~50ms
- Break-even calculations: ~200ms
- All calculations are client-side (no backend required)

## Customization

You can customize the component by:

1. **Changing probability distributions** in Monte Carlo (currently normal)
2. **Adding correlation** between variables
3. **Custom scenario definitions** (beyond optimistic/pessimistic)
4. **Additional charts** (3D sensitivity surface, risk matrices)

## Future Enhancements

- Export to Excel with full analysis
- Save scenarios to database
- Historical comparison of forecasts
- Integration with real-time market data
- Custom distribution types (triangular, uniform, beta)

---

## Files Modified

To add this to all models, update:
- ✅ `DCFModelEnhanced.tsx`
- ✅ `LBOModelEnhanced.tsx`
- ⏳ `MergerModelPage.tsx`
- ⏳ `DueDiligenceModel.tsx`
- ⏳ `ComparableCompanyAnalysis.tsx`

All real estate models can also benefit from this analysis!
