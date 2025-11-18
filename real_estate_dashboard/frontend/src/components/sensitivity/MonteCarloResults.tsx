/**
 * Monte Carlo Results Component
 *
 * Displays results from Monte Carlo simulation including:
 * - Histogram distribution
 * - Statistical metrics
 * - Risk metrics
 */

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Dice5, TrendingUp, AlertTriangle } from 'lucide-react';

interface MonteCarloResultsProps {
  data: {
    statistics: {
      mean: number;
      median: number;
      std: number;
      percentile_5: number;
      percentile_25: number;
      percentile_50: number;
      percentile_75: number;
      percentile_95: number;
      coefficient_of_variation: number;
    };
    risk_metrics: {
      probability_of_loss: number;
      value_at_risk_95: number;
      expected_shortfall: number;
    };
    histogram: { bin_start: number; bin_end: number; count: number; bin_center: number }[];
    iterations: number;
    distribution: string;
  };
  metricName: string;
  loading?: boolean;
}

export const MonteCarloResults: React.FC<MonteCarloResultsProps> = ({
  data,
  metricName,
  loading = false,
}) => {
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Monte Carlo Simulation</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-96 flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!data) {
    return (
      <Alert>
        <Dice5 className="h-4 w-4" />
        <AlertDescription>
          No simulation data available. Configure variables and run Monte Carlo simulation.
        </AlertDescription>
      </Alert>
    );
  }

  const { statistics, risk_metrics, histogram, iterations, distribution } = data;

  // Prepare histogram data for chart
  const chartData = histogram.map((bin) => ({
    range: `${bin.bin_start.toFixed(1)}`,
    count: bin.count,
    binCenter: bin.bin_center,
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      const bin = histogram.find((b) => b.bin_center === data.binCenter);
      if (bin) {
        const percentage = ((bin.count / iterations) * 100).toFixed(1);
        return (
          <div className="bg-white p-3 border rounded-lg shadow-lg">
            <p className="font-semibold text-sm">
              {bin.bin_start.toFixed(2)} - {bin.bin_end.toFixed(2)}
            </p>
            <p className="text-xs">
              <span className="text-muted-foreground">Occurrences:</span>{' '}
              <span className="font-semibold">{bin.count}</span> ({percentage}%)
            </p>
          </div>
        );
      }
    }
    return null;
  };

  // Risk level assessment
  const getRiskLevel = () => {
    if (risk_metrics.probability_of_loss > 30) return { level: 'High', color: 'text-red-600' };
    if (risk_metrics.probability_of_loss > 15) return { level: 'Moderate', color: 'text-yellow-600' };
    return { level: 'Low', color: 'text-green-600' };
  };

  const riskLevel = getRiskLevel();

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Dice5 className="h-5 w-5" />
          Monte Carlo Simulation Results
        </CardTitle>
        <p className="text-sm text-muted-foreground mt-2">
          {iterations.toLocaleString()} iterations using {distribution} distribution
        </p>
      </CardHeader>
      <CardContent>
        {/* Risk Assessment Alert */}
        {risk_metrics.probability_of_loss > 0 && (
          <Alert className="mb-6">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              <span className="font-semibold">Risk Level: <span className={riskLevel.color}>{riskLevel.level}</span></span>
              {' '}• Probability of loss: {risk_metrics.probability_of_loss.toFixed(1)}%
            </AlertDescription>
          </Alert>
        )}

        {/* Statistics Grid */}
        <div className="grid grid-cols-3 md:grid-cols-5 gap-4 mb-6">
          <div className="p-3 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground">Mean</p>
            <p className="text-lg font-bold">{statistics.mean.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground">Median</p>
            <p className="text-lg font-bold">{statistics.median.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground">Std Dev</p>
            <p className="text-lg font-bold">{statistics.std.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground">5th %ile</p>
            <p className="text-lg font-bold text-red-600">{statistics.percentile_5.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground">95th %ile</p>
            <p className="text-lg font-bold text-green-600">{statistics.percentile_95.toFixed(2)}</p>
          </div>
        </div>

        {/* Histogram */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold mb-3">Distribution of {metricName}</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
              <XAxis
                dataKey="range"
                angle={-45}
                textAnchor="end"
                height={80}
                tick={{ fontSize: 11 }}
              />
              <YAxis label={{ value: 'Frequency', angle: -90, position: 'insideLeft' }} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine
                x={chartData.find((d) => Math.abs(d.binCenter - statistics.mean) < 0.1)?.range}
                stroke="#3b82f6"
                strokeDasharray="3 3"
                label={{ value: 'Mean', position: 'top', fill: '#3b82f6' }}
              />
              <Bar dataKey="count" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Percentiles Table */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold mb-3">Percentile Distribution</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-4 py-2 text-left">Percentile</th>
                  <th className="px-4 py-2 text-right">Value</th>
                  <th className="px-4 py-2 text-left">Interpretation</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b">
                  <td className="px-4 py-2 font-semibold">5th</td>
                  <td className="px-4 py-2 text-right font-mono text-red-600">{statistics.percentile_5.toFixed(2)}</td>
                  <td className="px-4 py-2 text-xs text-muted-foreground">Worst case (95% of outcomes better)</td>
                </tr>
                <tr className="border-b">
                  <td className="px-4 py-2 font-semibold">25th</td>
                  <td className="px-4 py-2 text-right font-mono">{statistics.percentile_25.toFixed(2)}</td>
                  <td className="px-4 py-2 text-xs text-muted-foreground">Below average</td>
                </tr>
                <tr className="border-b bg-blue-50">
                  <td className="px-4 py-2 font-semibold">50th (Median)</td>
                  <td className="px-4 py-2 text-right font-mono font-bold">{statistics.percentile_50.toFixed(2)}</td>
                  <td className="px-4 py-2 text-xs text-muted-foreground">Most likely outcome</td>
                </tr>
                <tr className="border-b">
                  <td className="px-4 py-2 font-semibold">75th</td>
                  <td className="px-4 py-2 text-right font-mono">{statistics.percentile_75.toFixed(2)}</td>
                  <td className="px-4 py-2 text-xs text-muted-foreground">Above average</td>
                </tr>
                <tr className="border-b">
                  <td className="px-4 py-2 font-semibold">95th</td>
                  <td className="px-4 py-2 text-right font-mono text-green-600">{statistics.percentile_95.toFixed(2)}</td>
                  <td className="px-4 py-2 text-xs text-muted-foreground">Best case (95% of outcomes worse)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Risk Metrics */}
        <div className="p-4 bg-muted/30 rounded-lg">
          <h3 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <AlertTriangle className="h-4 w-4" />
            Risk Metrics
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p className="text-xs text-muted-foreground mb-1">Probability of Loss</p>
              <p className="text-2xl font-bold">{risk_metrics.probability_of_loss.toFixed(1)}%</p>
              <p className="text-xs text-muted-foreground mt-1">
                Chance of negative returns
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Value at Risk (95%)</p>
              <p className="text-2xl font-bold">{risk_metrics.value_at_risk_95.toFixed(2)}</p>
              <p className="text-xs text-muted-foreground mt-1">
                5% chance of falling below this
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Expected Shortfall</p>
              <p className="text-2xl font-bold">{risk_metrics.expected_shortfall.toFixed(2)}</p>
              <p className="text-xs text-muted-foreground mt-1">
                Average loss in worst 5% scenarios
              </p>
            </div>
          </div>
        </div>

        {/* Coefficient of Variation */}
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm">
            <span className="font-semibold">Coefficient of Variation:</span>{' '}
            {statistics.coefficient_of_variation.toFixed(2)}%
            {' '}<span className="text-xs text-muted-foreground">
              (Lower = more predictable, Higher = more volatile)
            </span>
          </p>
        </div>
      </CardContent>
    </Card>
  );
};
