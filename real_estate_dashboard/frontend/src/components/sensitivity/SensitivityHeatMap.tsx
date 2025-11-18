/**
 * Sensitivity Heat Map Component
 *
 * Visualizes two-way sensitivity analysis showing how two variables
 * interact to affect the output metric.
 */

import React, { useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Grid3X3, Info } from 'lucide-react';

interface HeatMapProps {
  xVariable: { name: string; label: string; values: number[] };
  yVariable: { name: string; label: string; values: number[] };
  results: number[][];
  statistics: { min: number; max: number; mean: number; range: number };
  metricName: string;
  loading?: boolean;
}

export const SensitivityHeatMap: React.FC<HeatMapProps> = ({
  xVariable,
  yVariable,
  results,
  statistics,
  metricName,
  loading = false,
}) => {
  // Calculate color for each cell based on value
  const getColor = (value: number) => {
    const normalized = (value - statistics.min) / statistics.range;

    // Use gradient from red (low) to yellow (medium) to green (high)
    if (normalized < 0.5) {
      // Red to Yellow
      const factor = normalized * 2;
      const r = 239; // ef
      const g = Math.round(68 + (234 - 68) * factor); // 44 to ea
      const b = Math.round(68 + (72 - 68) * factor); // 44 to 48
      return `rgb(${r}, ${g}, ${b})`;
    } else {
      // Yellow to Green
      const factor = (normalized - 0.5) * 2;
      const r = Math.round(234 - (234 - 34) * factor); // ea to 22
      const g = Math.round(234 - (234 - 197) * factor); // ea to c5
      const b = Math.round(72 - (72 - 94) * factor); // 48 to 5e
      return `rgb(${r}, ${g}, ${b})`;
    }
  };

  // Get text color based on background
  const getTextColor = (value: number) => {
    const normalized = (value - statistics.min) / statistics.range;
    return normalized > 0.5 ? 'white' : 'black';
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Two-Way Sensitivity Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-96 flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!results || results.length === 0) {
    return (
      <Alert>
        <Grid3X3 className="h-4 w-4" />
        <AlertDescription>
          No heat map data available. Select two variables and run analysis.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Grid3X3 className="h-5 w-5" />
          Two-Way Sensitivity Analysis (Heat Map)
        </CardTitle>
        <p className="text-sm text-muted-foreground mt-2">
          Shows how varying {xVariable.label} and {yVariable.label} simultaneously affects {metricName}.
        </p>
      </CardHeader>
      <CardContent>
        {/* Statistics Summary */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="p-3 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground">Minimum</p>
            <p className="text-lg font-bold text-red-600">{statistics.min.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground">Average</p>
            <p className="text-lg font-bold">{statistics.mean.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground">Maximum</p>
            <p className="text-lg font-bold text-green-600">{statistics.max.toFixed(2)}</p>
          </div>
          <div className="p-3 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground">Range</p>
            <p className="text-lg font-bold">{statistics.range.toFixed(2)}</p>
          </div>
        </div>

        {/* Heat Map */}
        <div className="overflow-x-auto">
          <div className="inline-block min-w-full">
            <table className="border-collapse">
              <thead>
                <tr>
                  <th className="p-2 text-xs font-semibold bg-muted/30 border sticky left-0 z-10">
                    {yVariable.label} →<br/>{xVariable.label} ↓
                  </th>
                  {xVariable.values.map((xVal, xIdx) => (
                    <th
                      key={xIdx}
                      className="p-2 text-xs font-semibold bg-muted/30 border min-w-[80px]"
                    >
                      {xVal.toFixed(1)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {yVariable.values.map((yVal, yIdx) => (
                  <tr key={yIdx}>
                    <td className="p-2 text-xs font-semibold bg-muted/30 border sticky left-0 z-10">
                      {yVal.toFixed(1)}
                    </td>
                    {xVariable.values.map((_, xIdx) => {
                      const value = results[yIdx][xIdx];
                      return (
                        <td
                          key={xIdx}
                          className="p-2 text-center border cursor-pointer hover:opacity-80 transition-opacity"
                          style={{
                            backgroundColor: getColor(value),
                            color: getTextColor(value),
                          }}
                          title={`${xVariable.label}: ${xVariable.values[xIdx].toFixed(2)}\n${yVariable.label}: ${yVal.toFixed(2)}\n${metricName}: ${value.toFixed(2)}`}
                        >
                          <span className="text-xs font-semibold">
                            {value.toFixed(1)}
                          </span>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Color Legend */}
        <div className="mt-6 flex items-center gap-4">
          <span className="text-xs font-semibold">Legend:</span>
          <div className="flex items-center gap-2 flex-1">
            <div className="flex-1 h-6 rounded" style={{
              background: `linear-gradient(to right, rgb(239, 68, 68), rgb(234, 234, 72), rgb(34, 197, 94))`
            }}></div>
          </div>
          <div className="flex gap-4 text-xs">
            <span>Low: {statistics.min.toFixed(1)}</span>
            <span>High: {statistics.max.toFixed(1)}</span>
          </div>
        </div>

        {/* Interpretation Guide */}
        <Alert className="mt-6">
          <Info className="h-4 w-4" />
          <AlertDescription className="text-xs">
            <p className="font-semibold mb-1">How to Read This Heat Map:</p>
            <ul className="space-y-0.5 ml-4">
              <li>• Red cells = Low {metricName} values</li>
              <li>• Green cells = High {metricName} values</li>
              <li>• Hover over cells to see exact values</li>
              <li>• Look for "sweet spots" (green zones) where both variables optimize the metric</li>
            </ul>
          </AlertDescription>
        </Alert>
      </CardContent>
    </Card>
  );
};
