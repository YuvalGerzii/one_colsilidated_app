/**
 * Break-Even Table Component
 *
 * Displays break-even analysis showing what value each variable
 * needs to reach the target metric.
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Target, AlertCircle, CheckCircle2, XCircle } from 'lucide-react';
import type { BreakEvenResult } from '@/services/sensitivityAnalysisApi';

interface BreakEvenTableProps {
  data: {
    target_metric: number;
    base_metric: number;
    variables: BreakEvenResult[];
  };
  metricName: string;
  loading?: boolean;
}

export const BreakEvenTable: React.FC<BreakEvenTableProps> = ({
  data,
  metricName,
  loading = false,
}) => {
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Break-Even Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-96 flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!data || !data.variables || data.variables.length === 0) {
    return (
      <Alert>
        <Target className="h-4 w-4" />
        <AlertDescription>
          No break-even data available. Set a target metric and run analysis.
        </AlertDescription>
      </Alert>
    );
  }

  const { target_metric, base_metric, variables } = data;

  // Get difficulty color
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'text-green-600 bg-green-50';
      case 'moderate':
        return 'text-yellow-600 bg-yellow-50';
      case 'challenging':
        return 'text-orange-600 bg-orange-50';
      case 'difficult':
        return 'text-red-600 bg-red-50';
      case 'impossible':
        return 'text-gray-600 bg-gray-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  // Get difficulty icon
  const getDifficultyIcon = (difficulty: string, achievable: boolean) => {
    if (!achievable) return <XCircle className="h-4 w-4" />;
    if (difficulty.toLowerCase() === 'easy') return <CheckCircle2 className="h-4 w-4" />;
    return <AlertCircle className="h-4 w-4" />;
  };

  // Sort variables by ease of achievement (easiest first)
  const sortedVariables = [...variables].sort((a, b) => {
    if (!a.achievable && b.achievable) return 1;
    if (a.achievable && !b.achievable) return -1;
    return Math.abs(a.change_required_pct) - Math.abs(b.change_required_pct);
  });

  // Find easiest achievable variable
  const easiestVariable = sortedVariables.find((v) => v.achievable);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Target className="h-5 w-5" />
          Break-Even Analysis
        </CardTitle>
        <p className="text-sm text-muted-foreground mt-2">
          Shows what value each variable needs to reach target {metricName} of {target_metric.toFixed(2)}
        </p>
      </CardHeader>
      <CardContent>
        {/* Current vs Target */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="p-4 bg-muted/50 rounded-lg">
            <p className="text-xs text-muted-foreground mb-1">Current {metricName}</p>
            <p className="text-2xl font-bold">{base_metric.toFixed(2)}</p>
          </div>
          <div className="p-4 bg-primary/10 rounded-lg border-2 border-primary">
            <p className="text-xs text-muted-foreground mb-1">Target {metricName}</p>
            <p className="text-2xl font-bold text-primary">{target_metric.toFixed(2)}</p>
          </div>
        </div>

        {/* Recommendation */}
        {easiestVariable && (
          <Alert className="mb-6 border-green-200 bg-green-50">
            <CheckCircle2 className="h-4 w-4 text-green-600" />
            <AlertDescription>
              <p className="font-semibold text-green-900">Easiest Path to Target:</p>
              <p className="text-sm text-green-700 mt-1">
                Adjust <span className="font-semibold">{easiestVariable.variable_label}</span>{' '}
                from {easiestVariable.base_value.toFixed(2)} to {easiestVariable.break_even_value.toFixed(2)}{' '}
                ({easiestVariable.change_required_pct >= 0 ? '+' : ''}{easiestVariable.change_required_pct.toFixed(1)}% change)
              </p>
            </AlertDescription>
          </Alert>
        )}

        {/* Break-Even Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-4 py-2 text-left">Variable</th>
                <th className="px-4 py-2 text-right">Current Value</th>
                <th className="px-4 py-2 text-right">Break-Even Value</th>
                <th className="px-4 py-2 text-right">Change Required</th>
                <th className="px-4 py-2 text-center">Difficulty</th>
              </tr>
            </thead>
            <tbody>
              {sortedVariables.map((variable) => (
                <tr
                  key={variable.variable_name}
                  className={`border-b hover:bg-muted/30 ${
                    !variable.achievable ? 'opacity-50' : ''
                  }`}
                >
                  <td className="px-4 py-2 font-semibold">
                    {variable.variable_label}
                    {!variable.achievable && (
                      <span className="ml-2 text-xs text-muted-foreground">(unachievable)</span>
                    )}
                  </td>
                  <td className="px-4 py-2 text-right font-mono">{variable.base_value.toFixed(2)}</td>
                  <td className="px-4 py-2 text-right font-mono font-semibold">
                    {variable.achievable ? variable.break_even_value.toFixed(2) : '—'}
                  </td>
                  <td className="px-4 py-2 text-right">
                    {variable.achievable ? (
                      <div>
                        <div className="font-mono">
                          {variable.change_required >= 0 ? '+' : ''}{variable.change_required.toFixed(2)}
                        </div>
                        <div className={`text-xs ${
                          Math.abs(variable.change_required_pct) <= 10 ? 'text-green-600' :
                          Math.abs(variable.change_required_pct) <= 25 ? 'text-yellow-600' :
                          'text-red-600'
                        }`}>
                          ({variable.change_required_pct >= 0 ? '+' : ''}{variable.change_required_pct.toFixed(1)}%)
                        </div>
                      </div>
                    ) : (
                      '—'
                    )}
                  </td>
                  <td className="px-4 py-2">
                    <div className="flex items-center justify-center gap-2">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold flex items-center gap-1 ${getDifficultyColor(variable.difficulty)}`}>
                        {getDifficultyIcon(variable.difficulty, variable.achievable)}
                        {variable.difficulty}
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Difficulty Legend */}
        <div className="mt-6 p-4 bg-muted/30 rounded-lg">
          <h4 className="text-sm font-semibold mb-3">Difficulty Levels</h4>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span><strong>Easy:</strong> &lt;10% change</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <span><strong>Moderate:</strong> 10-25% change</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-orange-500"></div>
              <span><strong>Challenging:</strong> 25-50% change</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <span><strong>Difficult:</strong> &gt;50% change</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-gray-500"></div>
              <span><strong>Impossible:</strong> Not achievable</span>
            </div>
          </div>
        </div>

        {/* Interpretation */}
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <h4 className="text-sm font-semibold mb-1 flex items-center gap-2">
            <AlertCircle className="h-4 w-4" />
            How to Use This Analysis:
          </h4>
          <ul className="text-xs space-y-1 text-muted-foreground ml-4">
            <li>• Focus on "Easy" or "Moderate" variables for quickest path to target</li>
            <li>• "Challenging" variables require significant changes - consider feasibility</li>
            <li>• "Difficult" or "Impossible" variables may not be realistic levers</li>
            <li>• Combine multiple small changes for better results than one large change</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
};
