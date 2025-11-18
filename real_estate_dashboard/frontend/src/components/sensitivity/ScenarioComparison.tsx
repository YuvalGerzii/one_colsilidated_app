/**
 * Scenario Comparison Component
 *
 * Visualizes comparison between multiple scenarios
 * (Base Case, Optimistic, Pessimistic, etc.)
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
  ReferenceLine,
  Cell,
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { GitCompare, TrendingUp, TrendingDown } from 'lucide-react';
import type { ScenarioResult } from '@/services/sensitivityAnalysisApi';

interface ScenarioComparisonProps {
  baseCase: { name: string; metric_value: number };
  scenarios: ScenarioResult[];
  metricName: string;
  loading?: boolean;
}

export const ScenarioComparison: React.FC<ScenarioComparisonProps> = ({
  baseCase,
  scenarios,
  metricName,
  loading = false,
}) => {
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Scenario Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-96 flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!scenarios || scenarios.length === 0) {
    return (
      <Alert>
        <GitCompare className="h-4 w-4" />
        <AlertDescription>
          No scenario data available. Configure scenarios and run analysis.
        </AlertDescription>
      </Alert>
    );
  }

  // Prepare chart data
  const chartData = [
    {
      name: baseCase.name,
      value: baseCase.metric_value,
      vs_base: 0,
      vs_base_pct: 0,
      isBase: true,
    },
    ...scenarios.map((s) => ({
      name: s.name,
      value: s.metric_value,
      vs_base: s.vs_base,
      vs_base_pct: s.vs_base_pct,
      isBase: false,
    })),
  ];

  // Get bar color based on performance vs base
  const getBarColor = (vs_base_pct: number, isBase: boolean) => {
    if (isBase) return '#3b82f6'; // Blue for base case
    if (vs_base_pct >= 10) return '#22c55e'; // Green for significantly better
    if (vs_base_pct >= 0) return '#84cc16'; // Light green for better
    if (vs_base_pct >= -10) return '#eab308'; // Yellow for slightly worse
    return '#ef4444'; // Red for significantly worse
  };

  // Find best and worst scenarios
  const sortedScenarios = [...scenarios].sort((a, b) => b.metric_value - a.metric_value);
  const bestScenario = sortedScenarios[0];
  const worstScenario = sortedScenarios[sortedScenarios.length - 1];

  // Custom tooltip
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border rounded-lg shadow-lg">
          <p className="font-semibold text-sm mb-1">{data.name}</p>
          <p className="text-xs mb-1">
            <span className="text-muted-foreground">{metricName}:</span>{' '}
            <span className="font-bold">{data.value.toFixed(2)}</span>
          </p>
          {!data.isBase && (
            <p className="text-xs">
              <span className="text-muted-foreground">vs Base:</span>{' '}
              <span className={`font-semibold ${data.vs_base >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {data.vs_base >= 0 ? '+' : ''}{data.vs_base.toFixed(2)} ({data.vs_base_pct >= 0 ? '+' : ''}{data.vs_base_pct.toFixed(1)}%)
              </span>
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <GitCompare className="h-5 w-5" />
          Scenario Analysis
        </CardTitle>
        <p className="text-sm text-muted-foreground mt-2">
          Compares different scenarios against the base case for {metricName}.
        </p>
      </CardHeader>
      <CardContent>
        {/* Key Insights */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <Alert className="border-green-200 bg-green-50">
            <TrendingUp className="h-4 w-4 text-green-600" />
            <AlertDescription>
              <p className="font-semibold text-green-900">Best Case: {bestScenario.name}</p>
              <p className="text-sm text-green-700 mt-1">
                {metricName}: {bestScenario.metric_value.toFixed(2)} (+{bestScenario.vs_base_pct.toFixed(1)}% vs base)
              </p>
            </AlertDescription>
          </Alert>
          <Alert className="border-red-200 bg-red-50">
            <TrendingDown className="h-4 w-4 text-red-600" />
            <AlertDescription>
              <p className="font-semibold text-red-900">Worst Case: {worstScenario.name}</p>
              <p className="text-sm text-red-700 mt-1">
                {metricName}: {worstScenario.metric_value.toFixed(2)} ({worstScenario.vs_base_pct.toFixed(1)}% vs base)
              </p>
            </AlertDescription>
          </Alert>
        </div>

        {/* Bar Chart */}
        <div className="mb-6">
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
              <XAxis dataKey="name" angle={-15} textAnchor="end" height={80} />
              <YAxis label={{ value: metricName, angle: -90, position: 'insideLeft' }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <ReferenceLine
                y={baseCase.metric_value}
                stroke="#666"
                strokeDasharray="3 3"
                label={{ value: 'Base Case', position: 'right' }}
              />
              <Bar dataKey="value" name={metricName}>
                {chartData.map((entry, index) => (
                  <Cell key={index} fill={getBarColor(entry.vs_base_pct, entry.isBase)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Detailed Comparison Table */}
        <div className="overflow-x-auto">
          <h3 className="text-sm font-semibold mb-3">Detailed Comparison</h3>
          <table className="w-full text-sm">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-4 py-2 text-left">Scenario</th>
                <th className="px-4 py-2 text-left">Description</th>
                <th className="px-4 py-2 text-right">{metricName}</th>
                <th className="px-4 py-2 text-right">vs Base</th>
                <th className="px-4 py-2 text-right">% Change</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b bg-blue-50 font-semibold">
                <td className="px-4 py-2">{baseCase.name}</td>
                <td className="px-4 py-2 text-muted-foreground">Baseline assumptions</td>
                <td className="px-4 py-2 text-right font-mono">{baseCase.metric_value.toFixed(2)}</td>
                <td className="px-4 py-2 text-right">—</td>
                <td className="px-4 py-2 text-right">—</td>
              </tr>
              {scenarios.map((scenario) => (
                <tr key={scenario.name} className="border-b hover:bg-muted/30">
                  <td className="px-4 py-2 font-semibold">{scenario.name}</td>
                  <td className="px-4 py-2 text-muted-foreground text-xs">{scenario.description}</td>
                  <td className="px-4 py-2 text-right font-mono">{scenario.metric_value.toFixed(2)}</td>
                  <td className={`px-4 py-2 text-right font-semibold ${
                    scenario.vs_base >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {scenario.vs_base >= 0 ? '+' : ''}{scenario.vs_base.toFixed(2)}
                  </td>
                  <td className={`px-4 py-2 text-right font-semibold ${
                    scenario.vs_base_pct >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {scenario.vs_base_pct >= 0 ? '+' : ''}{scenario.vs_base_pct.toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Range Summary */}
        <div className="mt-6 p-4 bg-muted/30 rounded-lg">
          <h4 className="text-sm font-semibold mb-2">Range Summary</h4>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <p className="text-xs text-muted-foreground">Best Case</p>
              <p className="text-lg font-bold text-green-600">{bestScenario.metric_value.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Base Case</p>
              <p className="text-lg font-bold text-blue-600">{baseCase.metric_value.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Worst Case</p>
              <p className="text-lg font-bold text-red-600">{worstScenario.metric_value.toFixed(2)}</p>
            </div>
          </div>
          <div className="mt-3 pt-3 border-t">
            <p className="text-xs">
              <span className="font-semibold">Total Range:</span>{' '}
              {(bestScenario.metric_value - worstScenario.metric_value).toFixed(2)}{' '}
              <span className="text-muted-foreground">
                ({((bestScenario.metric_value - worstScenario.metric_value) / baseCase.metric_value * 100).toFixed(1)}% of base)
              </span>
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
