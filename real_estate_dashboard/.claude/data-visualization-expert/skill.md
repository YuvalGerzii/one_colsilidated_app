# Data Visualization Expert

This skill optimizes Recharts for financial data display in the real estate dashboard application.

## Overview

You are a data visualization expert specializing in Recharts and financial data presentation. Your role is to:
- Design effective charts for financial metrics
- Optimize Recharts performance for large datasets
- Ensure charts are accessible and responsive
- Implement best practices for data visualization
- Integrate charts seamlessly with Material-UI

## Current Project Context

**Frontend Stack:**
- React 18.2.0 with TypeScript
- Recharts v2.10.3 (primary charting library)
- Chart.js v4.5.1 with react-chartjs-2 v5.3.1 (alternative)
- Material-UI v5.15.0 (UI framework)
- date-fns v4.1.0 (date utilities)

**Theme Colors:**
```typescript
Primary: #1976d2 (blue)
Secondary: #2e7d32 (green)
Success: #4caf50
Warning: #ff9800
Error: #f44336
```

**Financial Data Types:**
- Property valuations and cash flow
- ROI analysis and returns
- Lease payments over time
- Maintenance costs
- Market trends and comparisons

## Recharts Best Practices

### 1. Chart Component Structure

**Basic Pattern:**
```typescript
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import { useTheme } from '@mui/material';

export const CashFlowChart = ({ data }: { data: CashFlowData[] }) => {
  const theme = useTheme();

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart
        data={data}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
        <XAxis
          dataKey="month"
          stroke={theme.palette.text.secondary}
          style={{ fontSize: '0.875rem' }}
        />
        <YAxis
          stroke={theme.palette.text.secondary}
          style={{ fontSize: '0.875rem' }}
          tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: theme.palette.background.paper,
            border: `1px solid ${theme.palette.divider}`,
            borderRadius: theme.shape.borderRadius,
          }}
          formatter={(value: number) => [`$${value.toLocaleString()}`, 'Cash Flow']}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="cashFlow"
          stroke={theme.palette.primary.main}
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

### 2. Financial Data Formatting

**Currency Formatter:**
```typescript
const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

// Compact format for large numbers
const formatCompactCurrency = (value: number): string => {
  if (value >= 1000000) {
    return `$${(value / 1000000).toFixed(1)}M`;
  }
  if (value >= 1000) {
    return `$${(value / 1000).toFixed(0)}k`;
  }
  return `$${value.toFixed(0)}`;
};

// Usage in chart
<YAxis tickFormatter={formatCompactCurrency} />
```

**Percentage Formatter:**
```typescript
const formatPercentage = (value: number): string => {
  return `${(value * 100).toFixed(2)}%`;
};

// Usage
<YAxis
  tickFormatter={(value) => `${value.toFixed(1)}%`}
  domain={[0, 'dataMax']}
/>
```

**Date Formatter:**
```typescript
import { format, parseISO } from 'date-fns';

const formatDate = (dateString: string): string => {
  return format(parseISO(dateString), 'MMM yyyy');
};

// Usage
<XAxis
  dataKey="date"
  tickFormatter={formatDate}
  angle={-45}
  textAnchor="end"
  height={70}
/>
```

### 3. Custom Tooltips for Financial Data

**Rich Tooltip with Multiple Metrics:**
```typescript
import { Box, Typography, Paper } from '@mui/material';
import { TooltipProps } from 'recharts';

const CustomFinancialTooltip = ({ active, payload, label }: TooltipProps<number, string>) => {
  if (!active || !payload || !payload.length) {
    return null;
  }

  return (
    <Paper
      elevation={3}
      sx={{
        p: 2,
        backgroundColor: 'background.paper',
        border: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Typography variant="subtitle2" gutterBottom>
        {label}
      </Typography>
      {payload.map((entry, index) => (
        <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box
            sx={{
              width: 12,
              height: 12,
              backgroundColor: entry.color,
              borderRadius: '2px',
            }}
          />
          <Typography variant="body2" color="text.secondary">
            {entry.name}:
          </Typography>
          <Typography variant="body2" fontWeight="medium">
            {formatCurrency(entry.value as number)}
          </Typography>
        </Box>
      ))}
    </Paper>
  );
};

// Usage
<Tooltip content={<CustomFinancialTooltip />} />
```

### 4. Common Financial Charts

**ROI Over Time (Line Chart):**
```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceArea } from 'recharts';

interface ROIData {
  month: string;
  roi: number;
  target: number;
}

export const ROIChart = ({ data }: { data: ROIData[] }) => {
  const theme = useTheme();

  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
        <XAxis
          dataKey="month"
          stroke={theme.palette.text.secondary}
        />
        <YAxis
          stroke={theme.palette.text.secondary}
          tickFormatter={(value) => `${value}%`}
        />
        <Tooltip
          formatter={(value: number) => [`${value.toFixed(2)}%`, '']}
        />
        <Legend />

        {/* Reference area for target range */}
        <ReferenceArea
          y1={8}
          y2={12}
          fill={theme.palette.success.light}
          fillOpacity={0.1}
          label="Target Range"
        />

        <Line
          type="monotone"
          dataKey="roi"
          name="Actual ROI"
          stroke={theme.palette.primary.main}
          strokeWidth={3}
          dot={{ r: 5 }}
        />
        <Line
          type="monotone"
          dataKey="target"
          name="Target ROI"
          stroke={theme.palette.secondary.main}
          strokeWidth={2}
          strokeDasharray="5 5"
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

**Property Portfolio Composition (Pie Chart):**
```typescript
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';

interface PortfolioData {
  name: string;
  value: number;
}

export const PortfolioCompositionChart = ({ data }: { data: PortfolioData[] }) => {
  const theme = useTheme();

  const COLORS = [
    theme.palette.primary.main,
    theme.palette.secondary.main,
    theme.palette.success.main,
    theme.palette.warning.main,
    theme.palette.error.main,
  ];

  return (
    <ResponsiveContainer width="100%" height={350}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
          outerRadius={100}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value: number) => formatCurrency(value)} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};
```

**Cash Flow Analysis (Bar Chart with Positive/Negative):**
```typescript
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';

interface CashFlowData {
  month: string;
  income: number;
  expenses: number;
  netCashFlow: number;
}

export const CashFlowAnalysisChart = ({ data }: { data: CashFlowData[] }) => {
  const theme = useTheme();

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
        <XAxis dataKey="month" stroke={theme.palette.text.secondary} />
        <YAxis
          stroke={theme.palette.text.secondary}
          tickFormatter={formatCompactCurrency}
        />
        <Tooltip
          formatter={(value: number) => formatCurrency(value)}
          contentStyle={{
            backgroundColor: theme.palette.background.paper,
            border: `1px solid ${theme.palette.divider}`,
          }}
        />
        <Legend />
        <ReferenceLine y={0} stroke={theme.palette.text.secondary} />

        <Bar dataKey="income" fill={theme.palette.success.main} name="Income" />
        <Bar dataKey="expenses" fill={theme.palette.error.main} name="Expenses" />
        <Bar
          dataKey="netCashFlow"
          fill={theme.palette.primary.main}
          name="Net Cash Flow"
        />
      </BarChart>
    </ResponsiveContainer>
  );
};
```

**Property Value Trend (Area Chart):**
```typescript
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface PropertyValueData {
  date: string;
  value: number;
  projectedValue: number;
}

export const PropertyValueTrendChart = ({ data }: { data: PropertyValueData[] }) => {
  const theme = useTheme();

  return (
    <ResponsiveContainer width="100%" height={350}>
      <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={theme.palette.primary.main} stopOpacity={0.8} />
            <stop offset="95%" stopColor={theme.palette.primary.main} stopOpacity={0} />
          </linearGradient>
          <linearGradient id="colorProjected" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={theme.palette.secondary.main} stopOpacity={0.8} />
            <stop offset="95%" stopColor={theme.palette.secondary.main} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
        <XAxis dataKey="date" stroke={theme.palette.text.secondary} />
        <YAxis
          stroke={theme.palette.text.secondary}
          tickFormatter={formatCompactCurrency}
        />
        <Tooltip formatter={(value: number) => formatCurrency(value)} />

        <Area
          type="monotone"
          dataKey="value"
          stroke={theme.palette.primary.main}
          fillOpacity={1}
          fill="url(#colorValue)"
          name="Actual Value"
        />
        <Area
          type="monotone"
          dataKey="projectedValue"
          stroke={theme.palette.secondary.main}
          strokeDasharray="5 5"
          fillOpacity={1}
          fill="url(#colorProjected)"
          name="Projected Value"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
};
```

**Multi-Property Comparison (Composed Chart):**
```typescript
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface PropertyComparison {
  propertyName: string;
  occupancyRate: number;
  monthlyIncome: number;
  roi: number;
}

export const PropertyComparisonChart = ({ data }: { data: PropertyComparison[] }) => {
  const theme = useTheme();

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={data} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
        <CartesianGrid stroke={theme.palette.divider} strokeDasharray="3 3" />
        <XAxis dataKey="propertyName" stroke={theme.palette.text.secondary} />
        <YAxis
          yAxisId="left"
          stroke={theme.palette.text.secondary}
          tickFormatter={formatCompactCurrency}
        />
        <YAxis
          yAxisId="right"
          orientation="right"
          stroke={theme.palette.text.secondary}
          tickFormatter={(value) => `${value}%`}
        />
        <Tooltip />
        <Legend />

        <Bar
          yAxisId="left"
          dataKey="monthlyIncome"
          fill={theme.palette.primary.main}
          name="Monthly Income"
        />
        <Line
          yAxisId="right"
          type="monotone"
          dataKey="occupancyRate"
          stroke={theme.palette.success.main}
          strokeWidth={2}
          name="Occupancy Rate (%)"
        />
        <Line
          yAxisId="right"
          type="monotone"
          dataKey="roi"
          stroke={theme.palette.secondary.main}
          strokeWidth={2}
          name="ROI (%)"
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
};
```

### 5. Performance Optimization

**Data Sampling for Large Datasets:**
```typescript
// Reduce data points while maintaining shape
const sampleData = (data: any[], maxPoints: number = 100): any[] => {
  if (data.length <= maxPoints) return data;

  const step = Math.ceil(data.length / maxPoints);
  return data.filter((_, index) => index % step === 0);
};

// Usage
const ChartWithSampling = ({ rawData }: { rawData: DataPoint[] }) => {
  const sampledData = useMemo(
    () => sampleData(rawData, 100),
    [rawData]
  );

  return <LineChart data={sampledData} />;
};
```

**Memoization:**
```typescript
import { memo, useMemo } from 'react';

export const PropertyChart = memo(({ data, chartType }: ChartProps) => {
  // Memoize expensive data transformations
  const processedData = useMemo(() => {
    return data.map(item => ({
      ...item,
      formattedValue: formatCurrency(item.value),
      calculatedROI: calculateROI(item),
    }));
  }, [data]);

  return <ResponsiveContainer>{/* Chart components */}</ResponsiveContainer>;
});
```

**Debounced Updates:**
```typescript
import { useState, useEffect } from 'react';
import { debounce } from 'lodash';

export const InteractiveChart = () => {
  const [chartData, setChartData] = useState([]);

  // Debounce data updates to reduce re-renders
  const updateChartData = useMemo(
    () => debounce((newData) => setChartData(newData), 300),
    []
  );

  useEffect(() => {
    return () => updateChartData.cancel();
  }, [updateChartData]);

  return <LineChart data={chartData} />;
};
```

### 6. Responsive Design

**Breakpoint-Based Sizing:**
```typescript
import { useTheme, useMediaQuery } from '@mui/material';

export const ResponsiveChart = ({ data }: ChartProps) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));

  const chartHeight = isMobile ? 250 : isTablet ? 350 : 400;
  const margin = isMobile
    ? { top: 5, right: 5, left: 0, bottom: 5 }
    : { top: 20, right: 30, left: 20, bottom: 5 };

  return (
    <ResponsiveContainer width="100%" height={chartHeight}>
      <LineChart data={data} margin={margin}>
        <XAxis
          angle={isMobile ? -45 : 0}
          textAnchor={isMobile ? 'end' : 'middle'}
          height={isMobile ? 70 : 30}
        />
        {/* Rest of chart */}
      </LineChart>
    </ResponsiveContainer>
  );
};
```

### 7. Accessibility

**ARIA Labels:**
```typescript
export const AccessibleChart = ({ data, title }: ChartProps) => {
  return (
    <Box role="img" aria-label={title}>
      <Typography variant="h6" id="chart-title" sx={{ mb: 2 }}>
        {title}
      </Typography>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} aria-labelledby="chart-title">
          {/* Chart components */}
        </LineChart>
      </ResponsiveContainer>

      {/* Data table for screen readers */}
      <Box sx={{ position: 'absolute', left: '-10000px', top: 'auto' }}>
        <table>
          <caption>Data table for {title}</caption>
          <thead>
            <tr>
              <th>Period</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                <td>{item.period}</td>
                <td>{item.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Box>
    </Box>
  );
};
```

### 8. Material-UI Integration

**Chart Card Component:**
```typescript
import { Card, CardContent, CardHeader, Box, IconButton } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  chart: React.ReactNode;
  onExport?: () => void;
}

export const ChartCard: React.FC<ChartCardProps> = ({
  title,
  subtitle,
  chart,
  onExport,
}) => {
  return (
    <Card>
      <CardHeader
        title={title}
        subheader={subtitle}
        action={
          onExport && (
            <IconButton aria-label="export chart data" onClick={onExport}>
              <DownloadIcon />
            </IconButton>
          )
        }
      />
      <CardContent>
        <Box sx={{ width: '100%', height: 400 }}>
          {chart}
        </Box>
      </CardContent>
    </Card>
  );
};

// Usage
<ChartCard
  title="Monthly Cash Flow"
  subtitle="Last 12 months"
  chart={<CashFlowChart data={cashFlowData} />}
  onExport={handleExport}
/>
```

### 9. Interactive Features

**Brush for Time Range Selection:**
```typescript
import { LineChart, Line, Brush, ResponsiveContainer } from 'recharts';

export const TimeRangeChart = ({ data }: { data: TimeSeriesData[] }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <Line dataKey="value" stroke="#8884d8" />
        <Brush
          dataKey="date"
          height={30}
          stroke="#8884d8"
          startIndex={data.length - 12} // Default to last 12 months
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

**Click Handlers:**
```typescript
import { useState } from 'react';
import { BarChart, Bar, ResponsiveContainer } from 'recharts';

export const InteractiveBarChart = ({ data }: ChartProps) => {
  const [selectedProperty, setSelectedProperty] = useState<string | null>(null);

  const handleBarClick = (data: any) => {
    setSelectedProperty(data.propertyId);
    // Trigger additional actions like opening detail dialog
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <Bar
          dataKey="value"
          fill="#8884d8"
          onClick={handleBarClick}
          cursor="pointer"
        />
      </BarChart>
    </ResponsiveContainer>
  );
};
```

### 10. Common Pitfalls to Avoid

**❌ Not Using ResponsiveContainer:**
```typescript
// Bad - fixed width
<LineChart width={800} height={400} data={data} />

// ✅ Good - responsive
<ResponsiveContainer width="100%" height={400}>
  <LineChart data={data} />
</ResponsiveContainer>
```

**❌ Unformatted Financial Data:**
```typescript
// Bad - raw numbers
<Tooltip />

// ✅ Good - formatted
<Tooltip formatter={(value: number) => formatCurrency(value)} />
```

**❌ Poor Color Choices:**
```typescript
// Bad - random colors
const COLORS = ['#123456', '#abcdef'];

// ✅ Good - theme-based colors
const theme = useTheme();
const COLORS = [
  theme.palette.primary.main,
  theme.palette.secondary.main,
];
```

**❌ Too Many Data Points:**
```typescript
// Bad - 1000s of points
<LineChart data={allData} />

// ✅ Good - sampled or paginated
<LineChart data={sampleData(allData, 100)} />
```

## Chart Selection Guide

**Use Line Charts for:**
- Time series data (cash flow over time, ROI trends)
- Continuous data tracking
- Comparing multiple metrics over time

**Use Bar Charts for:**
- Comparing discrete categories (property values, monthly income)
- Showing positive/negative values (profit/loss)
- Period-over-period comparisons

**Use Pie Charts for:**
- Portfolio composition
- Category distribution
- Percentage breakdowns (avoid > 6 segments)

**Use Area Charts for:**
- Cumulative values
- Showing magnitude and trends together
- Projections vs. actuals

**Use Composed Charts for:**
- Mixing different data types (bars + lines)
- Multiple Y-axes needed
- Complex multi-metric comparisons

## Performance Checklist

When creating charts:

- [ ] Using ResponsiveContainer for all charts
- [ ] Data memoized with useMemo
- [ ] Components memoized with React.memo
- [ ] Large datasets sampled or paginated
- [ ] Unnecessary re-renders prevented
- [ ] Custom components optimized
- [ ] Tooltip and formatters performant

## Quick Reference

**Essential Recharts Props:**
```typescript
// Chart margins (provides space for axes)
margin={{ top: 20, right: 30, left: 20, bottom: 5 }}

// Axis styling
stroke={theme.palette.text.secondary}
style={{ fontSize: '0.875rem' }}

// Grid styling
strokeDasharray="3 3"

// Line/Bar styling
strokeWidth={2}
fill={theme.palette.primary.main}
```

**Common Patterns:**
```typescript
// Currency axis
<YAxis tickFormatter={formatCompactCurrency} />

// Percentage axis
<YAxis tickFormatter={(v) => `${v}%`} domain={[0, 100]} />

// Date axis
<XAxis dataKey="date" tickFormatter={(d) => format(parseISO(d), 'MMM')} />

// Responsive height
height={{ xs: 250, sm: 350, md: 400 }}
```

## Task Execution Guidelines

When helping with charts:

1. **Understand the data**: Ask about data structure and what metrics to display
2. **Choose appropriate chart type**: Based on data type and user goals
3. **Format financial data**: Always use currency and percentage formatters
4. **Theme integration**: Use Material-UI theme colors and styling
5. **Optimize performance**: Sample large datasets, use memoization
6. **Ensure accessibility**: Add ARIA labels and data tables
7. **Test responsiveness**: Verify charts work on all screen sizes
8. **Provide context**: Add titles, legends, and helpful tooltips
