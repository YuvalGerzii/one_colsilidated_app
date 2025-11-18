/**
 * Sensitivity Analysis Dashboard
 *
 * Main component that provides comprehensive sensitivity analysis
 * with tabbed interface for different analysis types.
 *
 * Usage:
 * <SensitivityAnalysisDashboard
 *   baseInputs={{ annual_noi: 100000, total_cash_invested: 500000 }}
 *   propertyType="multifamily"
 *   metricType="cash_on_cash"
 *   metricName="Cash on Cash Return"
 * />
 */

import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Activity, Loader2, Settings2 } from 'lucide-react';

import { TornadoChart } from './TornadoChart';
import { SensitivityHeatMap } from './SensitivityHeatMap';
import { MonteCarloResults } from './MonteCarloResults';
import { ScenarioComparison } from './ScenarioComparison';
import { BreakEvenTable } from './BreakEvenTable';

import {
  sensitivityAnalysisApi,
  type Variable,
  type OneWaySensitivityResponse,
  type TwoWaySensitivityResponse,
  type MonteCarloResponse,
  type ScenarioAnalysisResponse,
  type BreakEvenResponse,
} from '@/services/sensitivityAnalysisApi';

interface SensitivityAnalysisDashboardProps {
  baseInputs: Record<string, number>;
  propertyType?: 'multifamily' | 'single_family' | 'commercial' | 'fix_and_flip';
  metricType?: 'cash_on_cash' | 'cap_rate' | 'dscr' | 'irr';
  metricName?: string;
  initialVariables?: Variable[];
}

export const SensitivityAnalysisDashboard: React.FC<SensitivityAnalysisDashboardProps> = ({
  baseInputs,
  propertyType = 'multifamily',
  metricType = 'cash_on_cash',
  metricName = 'Cash on Cash Return',
  initialVariables,
}) => {
  // State
  const [variables, setVariables] = useState<Variable[]>(initialVariables || []);
  const [selectedXVariable, setSelectedXVariable] = useState<string>('');
  const [selectedYVariable, setSelectedYVariable] = useState<string>('');
  const [targetMetric, setTargetMetric] = useState<number>(15);
  const [monteCarloIterations, setMonteCarloIterations] = useState<number>(10000);
  const [distribution, setDistribution] = useState<'normal' | 'uniform' | 'triangular'>('normal');

  // Results state
  const [oneWayResults, setOneWayResults] = useState<OneWaySensitivityResponse | null>(null);
  const [twoWayResults, setTwoWayResults] = useState<TwoWaySensitivityResponse | null>(null);
  const [monteCarloResults, setMonteCarloResults] = useState<MonteCarloResponse | null>(null);
  const [scenarioResults, setScenarioResults] = useState<ScenarioAnalysisResponse | null>(null);
  const [breakEvenResults, setBreakEvenResults] = useState<BreakEvenResponse | null>(null);

  // Loading state
  const [loading, setLoading] = useState<Record<string, boolean>>({
    oneWay: false,
    twoWay: false,
    monteCarlo: false,
    scenarios: false,
    breakEven: false,
    template: false,
  });

  // Load template if no initial variables
  useEffect(() => {
    if (!initialVariables || initialVariables.length === 0) {
      loadTemplate();
    }
  }, [propertyType]);

  const loadTemplate = async () => {
    try {
      setLoading({ ...loading, template: true });
      const template = await sensitivityAnalysisApi.getTemplate(propertyType);
      if (template.template.variables) {
        setVariables(template.template.variables);
        // Auto-select first two variables for two-way analysis
        if (template.template.variables.length >= 2) {
          setSelectedXVariable(template.template.variables[0].name);
          setSelectedYVariable(template.template.variables[1].name);
        }
      }
    } catch (error) {
      console.error('Failed to load template:', error);
    } finally {
      setLoading({ ...loading, template: false });
    }
  };

  // Analysis functions
  const runOneWayAnalysis = async () => {
    try {
      setLoading({ ...loading, oneWay: true });
      const response = await sensitivityAnalysisApi.oneWaySensitivity({
        base_inputs: baseInputs,
        variables,
        metric_type: metricType,
        metric_name: metricName,
      });
      setOneWayResults(response);
    } catch (error) {
      console.error('One-way analysis failed:', error);
    } finally {
      setLoading({ ...loading, oneWay: false });
    }
  };

  const runTwoWayAnalysis = async () => {
    const xVar = variables.find((v) => v.name === selectedXVariable);
    const yVar = variables.find((v) => v.name === selectedYVariable);

    if (!xVar || !yVar) {
      alert('Please select both X and Y variables');
      return;
    }

    try {
      setLoading({ ...loading, twoWay: true });
      const response = await sensitivityAnalysisApi.twoWaySensitivity({
        base_inputs: baseInputs,
        metric_type: metricType,
        x_variable: xVar,
        y_variable: yVar,
        steps: 7,
      });
      setTwoWayResults(response);
    } catch (error) {
      console.error('Two-way analysis failed:', error);
    } finally {
      setLoading({ ...loading, twoWay: false });
    }
  };

  const runMonteCarloSimulation = async () => {
    try {
      setLoading({ ...loading, monteCarlo: true });
      const response = await sensitivityAnalysisApi.monteCarlo({
        base_inputs: baseInputs,
        variables,
        metric_type: metricType,
        iterations: monteCarloIterations,
        distribution,
      });
      setMonteCarloResults(response);
    } catch (error) {
      console.error('Monte Carlo simulation failed:', error);
    } finally {
      setLoading({ ...loading, monteCarlo: false });
    }
  };

  const runScenarioAnalysis = async () => {
    // Use default scenarios from template or create custom ones
    const scenarios = [
      {
        name: 'Optimistic',
        description: 'Strong market conditions',
        adjustments: {
          [variables[0]?.name]: { multiply_by: 1.15 },
        },
      },
      {
        name: 'Pessimistic',
        description: 'Market downturn',
        adjustments: {
          [variables[0]?.name]: { multiply_by: 0.85 },
        },
      },
    ];

    try {
      setLoading({ ...loading, scenarios: true });
      const response = await sensitivityAnalysisApi.scenarios({
        base_inputs: baseInputs,
        metric_type: metricType,
        scenarios,
      });
      setScenarioResults(response);
    } catch (error) {
      console.error('Scenario analysis failed:', error);
    } finally {
      setLoading({ ...loading, scenarios: false });
    }
  };

  const runBreakEvenAnalysis = async () => {
    try {
      setLoading({ ...loading, breakEven: true });
      const response = await sensitivityAnalysisApi.breakEven({
        base_inputs: baseInputs,
        variables,
        metric_type: metricType,
        target_metric: targetMetric,
      });
      setBreakEvenResults(response);
    } catch (error) {
      console.error('Break-even analysis failed:', error);
    } finally {
      setLoading({ ...loading, breakEven: false });
    }
  };

  if (loading.template) {
    return (
      <Card>
        <CardContent className="p-12">
          <div className="flex flex-col items-center justify-center gap-4">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <p className="text-muted-foreground">Loading sensitivity analysis template...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (variables.length === 0) {
    return (
      <Alert>
        <Settings2 className="h-4 w-4" />
        <AlertDescription>
          No variables configured for sensitivity analysis. Please provide initialVariables or select a property type.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Sensitivity Analysis Dashboard
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            Comprehensive risk and uncertainty analysis for {metricName}
          </p>
        </CardHeader>
      </Card>

      <Tabs defaultValue="one-way" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="one-way">Tornado</TabsTrigger>
          <TabsTrigger value="two-way">Heat Map</TabsTrigger>
          <TabsTrigger value="monte-carlo">Monte Carlo</TabsTrigger>
          <TabsTrigger value="scenarios">Scenarios</TabsTrigger>
          <TabsTrigger value="break-even">Break-Even</TabsTrigger>
        </TabsList>

        {/* One-Way Sensitivity */}
        <TabsContent value="one-way" className="space-y-4">
          <Card>
            <CardContent className="pt-6">
              <Button onClick={runOneWayAnalysis} disabled={loading.oneWay}>
                {loading.oneWay && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Run One-Way Analysis
              </Button>
            </CardContent>
          </Card>

          {oneWayResults && (
            <TornadoChart
              data={oneWayResults.data.variables}
              baseMetric={oneWayResults.data.base_metric}
              metricName={metricName}
              loading={loading.oneWay}
            />
          )}
        </TabsContent>

        {/* Two-Way Sensitivity */}
        <TabsContent value="two-way" className="space-y-4">
          <Card>
            <CardContent className="pt-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>X-Axis Variable</Label>
                  <Select value={selectedXVariable} onValueChange={setSelectedXVariable}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select X variable" />
                    </SelectTrigger>
                    <SelectContent>
                      {variables.map((v) => (
                        <SelectItem key={v.name} value={v.name}>
                          {v.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Y-Axis Variable</Label>
                  <Select value={selectedYVariable} onValueChange={setSelectedYVariable}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Y variable" />
                    </SelectTrigger>
                    <SelectContent>
                      {variables.map((v) => (
                        <SelectItem key={v.name} value={v.name}>
                          {v.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <Button onClick={runTwoWayAnalysis} disabled={loading.twoWay}>
                {loading.twoWay && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Run Two-Way Analysis
              </Button>
            </CardContent>
          </Card>

          {twoWayResults && (
            <SensitivityHeatMap
              xVariable={twoWayResults.data.x_variable}
              yVariable={twoWayResults.data.y_variable}
              results={twoWayResults.data.results}
              statistics={twoWayResults.data.statistics}
              metricName={metricName}
              loading={loading.twoWay}
            />
          )}
        </TabsContent>

        {/* Monte Carlo */}
        <TabsContent value="monte-carlo" className="space-y-4">
          <Card>
            <CardContent className="pt-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Iterations</Label>
                  <Input
                    type="number"
                    value={monteCarloIterations}
                    onChange={(e) => setMonteCarloIterations(Number(e.target.value))}
                    min={1000}
                    max={100000}
                    step={1000}
                  />
                </div>
                <div>
                  <Label>Distribution</Label>
                  <Select value={distribution} onValueChange={(v: any) => setDistribution(v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="normal">Normal</SelectItem>
                      <SelectItem value="uniform">Uniform</SelectItem>
                      <SelectItem value="triangular">Triangular</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <Button onClick={runMonteCarloSimulation} disabled={loading.monteCarlo}>
                {loading.monteCarlo && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Run Monte Carlo Simulation
              </Button>
            </CardContent>
          </Card>

          {monteCarloResults && (
            <MonteCarloResults
              data={monteCarloResults.data}
              metricName={metricName}
              loading={loading.monteCarlo}
            />
          )}
        </TabsContent>

        {/* Scenarios */}
        <TabsContent value="scenarios" className="space-y-4">
          <Card>
            <CardContent className="pt-6">
              <Button onClick={runScenarioAnalysis} disabled={loading.scenarios}>
                {loading.scenarios && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Run Scenario Analysis
              </Button>
            </CardContent>
          </Card>

          {scenarioResults && (
            <ScenarioComparison
              baseCase={scenarioResults.data.base_case}
              scenarios={scenarioResults.data.scenarios}
              metricName={metricName}
              loading={loading.scenarios}
            />
          )}
        </TabsContent>

        {/* Break-Even */}
        <TabsContent value="break-even" className="space-y-4">
          <Card>
            <CardContent className="pt-6 space-y-4">
              <div className="max-w-xs">
                <Label>Target {metricName}</Label>
                <Input
                  type="number"
                  value={targetMetric}
                  onChange={(e) => setTargetMetric(Number(e.target.value))}
                  step={0.1}
                />
              </div>
              <Button onClick={runBreakEvenAnalysis} disabled={loading.breakEven}>
                {loading.breakEven && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Run Break-Even Analysis
              </Button>
            </CardContent>
          </Card>

          {breakEvenResults && (
            <BreakEvenTable
              data={breakEvenResults.data}
              metricName={metricName}
              loading={loading.breakEven}
            />
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};
