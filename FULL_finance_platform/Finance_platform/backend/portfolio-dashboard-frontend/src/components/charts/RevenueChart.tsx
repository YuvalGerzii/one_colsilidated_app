// src/components/charts/RevenueChart.tsx
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Box, Typography } from '@mui/material';
import { FinancialMetric } from '../../types/financial';

interface RevenueChartProps {
  financials: FinancialMetric[];
  title?: string;
}

export const RevenueChart: React.FC<RevenueChartProps> = ({
  financials,
  title = 'Revenue & EBITDA Trend',
}) => {
  const data = financials.map((f) => ({
    period: f.period,
    revenue: f.revenue / 1000000, // Convert to millions
    ebitda: f.ebitda ? f.ebitda / 1000000 : 0,
  }));

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="period" />
          <YAxis tickFormatter={(value) => `$${value}M`} />
          <Tooltip
            formatter={(value: number) => [`$${value.toFixed(1)}M`, '']}
            labelFormatter={(label) => `Period: ${label}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="revenue"
            stroke="#1976d2"
            strokeWidth={2}
            name="Revenue"
          />
          <Line
            type="monotone"
            dataKey="ebitda"
            stroke="#2e7d32"
            strokeWidth={2}
            name="EBITDA"
          />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};
