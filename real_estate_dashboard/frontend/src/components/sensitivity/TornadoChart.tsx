/**
 * Tornado Chart Component
 *
 * Visualizes one-way sensitivity analysis results.
 * Shows which variables have the biggest impact on the output metric.
 */

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';
import type { SensitivityVariableResult } from '@/services/sensitivityAnalysisApi';

interface TornadoChartProps {
  data: SensitivityVariableResult[];
  baseMetric: number;
  metricName: string;
  loading?: boolean;
}

export const TornadoChart: React.FC<TornadoChartProps> = ({
  data,
  baseMetric,
  metricName,
  loading = false,
}) => {
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>One-Way Sensitivity Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-96 flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!data || data.length === 0) {
    return (
      <Alert>
        <Activity className="h-4 w-4" />
        <AlertDescription>
          No sensitivity data available. Configure variables and run analysis.
        </AlertDescription>
      </Alert>
    );
  }

  // Transform data for tornado chart
  // Sort by impact (already sorted from backend, but double-check)
  const sortedData = [...data].sort((a, b) => b.impact_percentage - a.impact_percentage);

  // Create chart data with min and max values relative to base
  const chartData = sortedData.map((item) => ({
    name: item.variable_label,
    lowValue: item.metric_at_min - baseMetric,
    highValue: item.metric_at_max - baseMetric,
    impact: item.impact_percentage,
    baseValue: item.base_value,
    minValue: item.min_value,
    maxValue: item.max_value,
  }));

  // Find most impactful variable
  const mostImpactful = sortedData[0];

  // Custom tooltip
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-4 border rounded-lg shadow-lg">
          <p className="font-semibold text-sm mb-2">{data.name}</p>
          <div className="space-y-1 text-xs">
            <p>
              <span className="text-muted-foreground">Base Value:</span>{' '}
              <span className="font-medium">{data.baseValue.toFixed(2)}</span>
            </p>
            <p>
              <span className="text-muted-foreground">Range:</span>{' '}
              <span className="font-medium">
                {data.minValue.toFixed(2)} - {data.maxValue.toFixed(2)}
              </span>
            </p>
            <p className="pt-1 border-t">
              <span className="text-muted-foreground">Impact on {metricName}:</span>{' '}
              <span className="font-semibold text-primary">{data.impact.toFixed(1)}%</span>
            </p>
            <div className="flex items-center gap-2 pt-1">
              <TrendingDown className="h-3 w-3 text-red-500" />
              <span className="text-xs">Low: {(baseMetric + data.lowValue).toFixed(2)}</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-3 w-3 text-green-500" />
              <span className="text-xs">High: {(baseMetric + data.highValue).toFixed(2)}</span>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Activity className="h-5 w-5" />
          One-Way Sensitivity Analysis (Tornado Chart)
        </CardTitle>
        <p className="text-sm text-muted-foreground mt-2">
          Shows how each variable individually affects {metricName}. Longer bars = higher sensitivity.
        </p>
      </CardHeader>
      <CardContent>
        {/* Insights */}
        <Alert className="mb-6">
          <TrendingUp className="h-4 w-4" />
          <AlertDescription>
            <span className="font-semibold">{mostImpactful.variable_label}</span> is the most
            sensitive variable, with a <span className="font-semibold">{mostImpactful.impact_percentage.toFixed(1)}%</span>{' '}
            impact on {metricName}. Focus on getting this variable right.
          </AlertDescription>
        </Alert>

        {/* Base metric reference */}
        <div className="mb-4 p-3 bg-muted/50 rounded-lg">
          <p className="text-sm font-medium">
            Base Case {metricName}: <span className="text-lg font-bold text-primary">{baseMetric.toFixed(2)}</span>
          </p>
        </div>

        {/* Tornado Chart */}
        <ResponsiveContainer width="100%" height={Math.max(400, chartData.length * 50)}>
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 20, right: 30, left: 120, bottom: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
            <XAxis
              type="number"
              label={{ value: `Change in ${metricName}`, position: 'bottom', offset: 0 }}
            />
            <YAxis type="category" dataKey="name" width={110} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <ReferenceLine x={0} stroke="#666" strokeWidth={2} />

            {/* Low values (negative change) */}
            <Bar
              dataKey="lowValue"
              name="Low Impact"
              fill="#ef4444"
              stackId="stack"
            />

            {/* High values (positive change) */}
            <Bar
              dataKey="highValue"
              name="High Impact"
              fill="#10b981"
              stackId="stack"
            />
          </BarChart>
        </ResponsiveContainer>

        {/* Variable Ranking Table */}
        <div className="mt-8">
          <h3 className="text-sm font-semibold mb-3">Variable Impact Rankings</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-4 py-2 text-left">Rank</th>
                  <th className="px-4 py-2 text-left">Variable</th>
                  <th className="px-4 py-2 text-right">Base Value</th>
                  <th className="px-4 py-2 text-right">Range Tested</th>
                  <th className="px-4 py-2 text-right">Impact %</th>
                </tr>
              </thead>
              <tbody>
                {sortedData.map((item, index) => (
                  <tr key={item.variable_name} className="border-b hover:bg-muted/30">
                    <td className="px-4 py-2 font-semibold">{index + 1}</td>
                    <td className="px-4 py-2">{item.variable_label}</td>
                    <td className="px-4 py-2 text-right font-mono">{item.base_value.toFixed(2)}</td>
                    <td className="px-4 py-2 text-right font-mono text-xs">
                      {item.min_value.toFixed(2)} - {item.max_value.toFixed(2)}
                    </td>
                    <td className="px-4 py-2 text-right">
                      <span className={`font-semibold ${
                        item.impact_percentage > 15 ? 'text-red-600' :
                        item.impact_percentage > 10 ? 'text-orange-600' :
                        item.impact_percentage > 5 ? 'text-yellow-600' :
                        'text-green-600'
                      }`}>
                        {item.impact_percentage.toFixed(1)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Interpretation Guide */}
        <div className="mt-6 p-4 bg-muted/30 rounded-lg">
          <h4 className="text-sm font-semibold mb-2">How to Read This Chart:</h4>
          <ul className="text-xs space-y-1 text-muted-foreground">
            <li>• Longer bars = Variable has more impact on {metricName}</li>
            <li>• Red side = Impact when variable is at minimum value</li>
            <li>• Green side = Impact when variable is at maximum value</li>
            <li>• Focus your efforts on the top-ranked variables for maximum effect</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
};
