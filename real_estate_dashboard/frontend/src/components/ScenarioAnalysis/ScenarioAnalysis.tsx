import React, { useState, useMemo } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Stack,
  Card,
  CardContent,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress,
  Divider,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ShowChart as ShowChartIcon,
  Assessment as AssessmentIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  Cell,
  ComposedChart,
  Area,
} from 'recharts';

export interface Variable {
  name: string;
  label: string;
  baseValue: number;
  min: number;
  max: number;
  step: number;
  unit?: string;
}

interface ScenarioAnalysisProps {
  // Base calculation function that takes variables and returns the output metric
  calculateMetric: (variables: Record<string, number>) => number;
  // Variables to analyze
  variables: Variable[];
  // Metric name (e.g., "NPV", "IRR", "Equity Value")
  metricName: string;
  metricUnit?: string;
  // Break-even target (e.g., for NPV break-even target is 0)
  breakEvenTarget?: number;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const ScenarioAnalysis: React.FC<ScenarioAnalysisProps> = ({
  calculateMetric,
  variables,
  metricName,
  metricUnit = '',
  breakEvenTarget = 0,
}) => {
  const [tabValue, setTabValue] = useState(0);
  const [monteCarloIterations, setMonteCarloIterations] = useState(10000);
  const [monteCarloRunning, setMonteCarloRunning] = useState(false);
  const [monteCarloResults, setMonteCarloResults] = useState<number[]>([]);

  // Scenario configurations
  const [scenarios, setScenarios] = useState<Record<string, Record<string, number>>>({
    base: variables.reduce((acc, v) => ({ ...acc, [v.name]: v.baseValue }), {}),
    optimistic: variables.reduce((acc, v) => ({ ...acc, [v.name]: v.baseValue * 1.2 }), {}),
    pessimistic: variables.reduce((acc, v) => ({ ...acc, [v.name]: v.baseValue * 0.8 }), {}),
  });

  // Calculate base case
  const baseCase = useMemo(() => {
    const vars = variables.reduce((acc, v) => ({ ...acc, [v.name]: v.baseValue }), {});
    return calculateMetric(vars);
  }, [variables, calculateMetric]);

  // Monte Carlo Simulation
  const runMonteCarloSimulation = () => {
    setMonteCarloRunning(true);

    setTimeout(() => {
      const results: number[] = [];

      for (let i = 0; i < monteCarloIterations; i++) {
        const randomVars: Record<string, number> = {};

        variables.forEach(v => {
          // Assume normal distribution around base value
          const range = (v.max - v.min) / 4; // Using 4 standard deviations
          const randomValue = v.baseValue + (Math.random() - 0.5) * 2 * range;
          randomVars[v.name] = Math.max(v.min, Math.min(v.max, randomValue));
        });

        const result = calculateMetric(randomVars);
        results.push(result);
      }

      setMonteCarloResults(results.sort((a, b) => a - b));
      setMonteCarloRunning(false);
    }, 100);
  };

  // Calculate Monte Carlo statistics
  const monteCarloStats = useMemo(() => {
    if (monteCarloResults.length === 0) return null;

    const mean = monteCarloResults.reduce((sum, val) => sum + val, 0) / monteCarloResults.length;
    const variance = monteCarloResults.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / monteCarloResults.length;
    const stdDev = Math.sqrt(variance);

    const p5 = monteCarloResults[Math.floor(monteCarloResults.length * 0.05)];
    const p25 = monteCarloResults[Math.floor(monteCarloResults.length * 0.25)];
    const p50 = monteCarloResults[Math.floor(monteCarloResults.length * 0.50)];
    const p75 = monteCarloResults[Math.floor(monteCarloResults.length * 0.75)];
    const p95 = monteCarloResults[Math.floor(monteCarloResults.length * 0.95)];

    const probPositive = monteCarloResults.filter(r => r > breakEvenTarget).length / monteCarloResults.length;

    return { mean, stdDev, p5, p25, p50, p75, p95, probPositive };
  }, [monteCarloResults, breakEvenTarget]);

  // Create distribution chart data
  const distributionData = useMemo(() => {
    if (monteCarloResults.length === 0) return [];

    const numBins = 50;
    const min = Math.min(...monteCarloResults);
    const max = Math.max(...monteCarloResults);
    const binWidth = (max - min) / numBins;

    const bins: { value: number; count: number }[] = [];
    for (let i = 0; i < numBins; i++) {
      bins.push({ value: min + i * binWidth + binWidth / 2, count: 0 });
    }

    monteCarloResults.forEach(result => {
      const binIndex = Math.min(Math.floor((result - min) / binWidth), numBins - 1);
      bins[binIndex].count++;
    });

    return bins;
  }, [monteCarloResults]);

  // Sensitivity Analysis - Tornado Chart
  const tornadoData = useMemo(() => {
    const data: { variable: string; low: number; high: number; range: number }[] = [];

    variables.forEach(v => {
      const varsLow = variables.reduce((acc, variable) => ({
        ...acc,
        [variable.name]: variable.name === v.name ? v.min : variable.baseValue
      }), {});

      const varsHigh = variables.reduce((acc, variable) => ({
        ...acc,
        [variable.name]: variable.name === v.name ? v.max : variable.baseValue
      }), {});

      const low = calculateMetric(varsLow);
      const high = calculateMetric(varsHigh);

      data.push({
        variable: v.label,
        low: low - baseCase,
        high: high - baseCase,
        range: Math.abs(high - low),
      });
    });

    return data.sort((a, b) => b.range - a.range);
  }, [variables, calculateMetric, baseCase]);

  // 2D Sensitivity Table
  const [sensitivityVar1, setSensitivityVar1] = useState(variables[0]?.name || '');
  const [sensitivityVar2, setSensitivityVar2] = useState(variables[1]?.name || '');

  const sensitivityTable = useMemo(() => {
    if (!sensitivityVar1 || !sensitivityVar2) return null;

    const var1 = variables.find(v => v.name === sensitivityVar1);
    const var2 = variables.find(v => v.name === sensitivityVar2);

    if (!var1 || !var2) return null;

    const steps1 = 7;
    const steps2 = 7;
    const step1 = (var1.max - var1.min) / (steps1 - 1);
    const step2 = (var2.max - var2.min) / (steps2 - 1);

    const table: number[][] = [];

    for (let i = 0; i < steps2; i++) {
      const row: number[] = [];
      const val2 = var2.min + i * step2;

      for (let j = 0; j < steps1; j++) {
        const val1 = var1.min + j * step1;

        const vars = variables.reduce((acc, v) => ({
          ...acc,
          [v.name]: v.name === var1.name ? val1 : v.name === var2.name ? val2 : v.baseValue
        }), {});

        row.push(calculateMetric(vars));
      }

      table.push(row);
    }

    return { table, var1, var2, step1, step2 };
  }, [sensitivityVar1, sensitivityVar2, variables, calculateMetric]);

  // Break-even Analysis
  const breakEvenData = useMemo(() => {
    return variables.map(v => {
      // Binary search for break-even point
      let low = v.min;
      let high = v.max;
      let breakEvenValue = null;

      for (let i = 0; i < 50; i++) {
        const mid = (low + high) / 2;
        const vars = variables.reduce((acc, variable) => ({
          ...acc,
          [variable.name]: variable.name === v.name ? mid : variable.baseValue
        }), {});

        const result = calculateMetric(vars);

        if (Math.abs(result - breakEvenTarget) < 0.01) {
          breakEvenValue = mid;
          break;
        }

        if (result < breakEvenTarget) {
          low = mid;
        } else {
          high = mid;
        }
      }

      const percentChange = breakEvenValue !== null
        ? ((breakEvenValue - v.baseValue) / v.baseValue) * 100
        : null;

      return {
        variable: v.label,
        baseValue: v.baseValue,
        breakEvenValue,
        percentChange,
        unit: v.unit || '',
      };
    }).filter(d => d.breakEvenValue !== null);
  }, [variables, calculateMetric, breakEvenTarget]);

  // Scenario Comparison
  const scenarioResults = useMemo(() => {
    return Object.entries(scenarios).map(([name, vars]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value: calculateMetric(vars),
    }));
  }, [scenarios, calculateMetric]);

  // Waterfall Chart Data
  const waterfallData = useMemo(() => {
    const data: { name: string; value: number; color: string }[] = [
      { name: 'Base Case', value: baseCase, color: '#2196f3' }
    ];

    let cumulative = baseCase;

    variables.forEach((v, index) => {
      const varsHigh = variables.reduce((acc, variable) => ({
        ...acc,
        [variable.name]: variable.name === v.name ? v.max : variable.baseValue
      }), {});

      const high = calculateMetric(varsHigh);
      const impact = high - cumulative;

      data.push({
        name: v.label,
        value: impact,
        color: impact >= 0 ? '#4caf50' : '#f44336',
      });

      cumulative += impact;
    });

    return data;
  }, [variables, calculateMetric, baseCase]);

  // Downside Protection Metrics
  const downsideMetrics = useMemo(() => {
    if (monteCarloResults.length === 0) return null;

    const negativeOutcomes = monteCarloResults.filter(r => r < breakEvenTarget);
    const avgNegative = negativeOutcomes.length > 0
      ? negativeOutcomes.reduce((sum, val) => sum + val, 0) / negativeOutcomes.length
      : 0;

    const worstCase = Math.min(...monteCarloResults);
    const downside5th = monteCarloStats?.p5 || 0;

    return {
      probNegative: (negativeOutcomes.length / monteCarloResults.length) * 100,
      avgNegative,
      worstCase,
      downside5th,
      downsideDeviation: Math.abs(downside5th - baseCase),
    };
  }, [monteCarloResults, monteCarloStats, baseCase, breakEvenTarget]);

  return (
    <Box>
      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
          <Tab label="Monte Carlo" icon={<ShowChartIcon />} iconPosition="start" />
          <Tab label="Sensitivity Analysis" icon={<AssessmentIcon />} iconPosition="start" />
          <Tab label="Scenario Comparison" icon={<TrendingUpIcon />} iconPosition="start" />
          <Tab label="Break-Even" icon={<WarningIcon />} iconPosition="start" />
          <Tab label="Downside Protection" icon={<TrendingDownIcon />} iconPosition="start" />
        </Tabs>
      </Paper>

      {/* Monte Carlo Simulation Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Monte Carlo Simulation</Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Run thousands of simulations with randomized inputs to understand the probability distribution of outcomes
                </Typography>

                <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 3 }}>
                  <TextField
                    label="Number of Iterations"
                    type="number"
                    value={monteCarloIterations}
                    onChange={(e) => setMonteCarloIterations(parseInt(e.target.value))}
                    disabled={monteCarloRunning}
                    sx={{ width: 200 }}
                  />
                  <Button
                    variant="contained"
                    onClick={runMonteCarloSimulation}
                    disabled={monteCarloRunning}
                  >
                    {monteCarloRunning ? 'Running...' : 'Run Simulation'}
                  </Button>
                </Stack>

                {monteCarloRunning && <LinearProgress sx={{ mb: 2 }} />}
              </CardContent>
            </Card>
          </Grid>

          {monteCarloStats && (
            <>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>Distribution</Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={distributionData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="value" tickFormatter={(val) => val.toFixed(0)} />
                        <YAxis />
                        <Tooltip formatter={(val) => val.toLocaleString()} />
                        <Bar dataKey="count" fill="#2196f3" />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>Statistics</Typography>
                    <TableContainer>
                      <Table size="small">
                        <TableBody>
                          <TableRow>
                            <TableCell>Mean</TableCell>
                            <TableCell align="right"><strong>{monteCarloStats.mean.toFixed(2)} {metricUnit}</strong></TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Std Dev</TableCell>
                            <TableCell align="right">{monteCarloStats.stdDev.toFixed(2)} {metricUnit}</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>5th Percentile</TableCell>
                            <TableCell align="right">{monteCarloStats.p5.toFixed(2)} {metricUnit}</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>25th Percentile</TableCell>
                            <TableCell align="right">{monteCarloStats.p25.toFixed(2)} {metricUnit}</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Median (50th)</TableCell>
                            <TableCell align="right"><strong>{monteCarloStats.p50.toFixed(2)} {metricUnit}</strong></TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>75th Percentile</TableCell>
                            <TableCell align="right">{monteCarloStats.p75.toFixed(2)} {metricUnit}</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>95th Percentile</TableCell>
                            <TableCell align="right">{monteCarloStats.p95.toFixed(2)} {metricUnit}</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell><strong>Probability {'>'} {breakEvenTarget}</strong></TableCell>
                            <TableCell align="right">
                              <Chip
                                label={`${(monteCarloStats.probPositive * 100).toFixed(1)}%`}
                                color={monteCarloStats.probPositive > 0.5 ? 'success' : 'error'}
                                size="small"
                              />
                            </TableCell>
                          </TableRow>
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </CardContent>
                </Card>
              </Grid>
            </>
          )}
        </Grid>
      </TabPanel>

      {/* Sensitivity Analysis Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Tornado Chart - Impact on {metricName}</Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Shows the sensitivity of {metricName} to changes in each variable (sorted by impact)
                </Typography>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart
                    data={tornadoData}
                    layout="vertical"
                    margin={{ left: 150 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="variable" type="category" />
                    <Tooltip formatter={(val: any) => val.toFixed(2)} />
                    <Legend />
                    <Bar dataKey="low" fill="#f44336" name="Downside" stackId="a" />
                    <Bar dataKey="high" fill="#4caf50" name="Upside" stackId="a" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>2D Sensitivity Table</Typography>
                <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
                  <FormControl sx={{ minWidth: 200 }}>
                    <InputLabel>Variable 1 (Rows)</InputLabel>
                    <Select
                      value={sensitivityVar1}
                      onChange={(e) => setSensitivityVar1(e.target.value)}
                      label="Variable 1 (Rows)"
                    >
                      {variables.map(v => (
                        <MenuItem key={v.name} value={v.name}>{v.label}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <FormControl sx={{ minWidth: 200 }}>
                    <InputLabel>Variable 2 (Columns)</InputLabel>
                    <Select
                      value={sensitivityVar2}
                      onChange={(e) => setSensitivityVar2(e.target.value)}
                      label="Variable 2 (Columns)"
                    >
                      {variables.map(v => (
                        <MenuItem key={v.name} value={v.name}>{v.label}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Stack>

                {sensitivityTable && (
                  <TableContainer sx={{ maxHeight: 500 }}>
                    <Table size="small" stickyHeader>
                      <TableHead>
                        <TableRow>
                          <TableCell>{sensitivityTable.var1.label} \ {sensitivityTable.var2.label}</TableCell>
                          {Array.from({ length: 7 }).map((_, i) => (
                            <TableCell key={i} align="right">
                              {(sensitivityTable.var2.min + i * sensitivityTable.step2).toFixed(2)}
                            </TableCell>
                          ))}
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {sensitivityTable.table.map((row, i) => (
                          <TableRow key={i}>
                            <TableCell component="th" scope="row">
                              {(sensitivityTable.var1.min + i * sensitivityTable.step1).toFixed(2)}
                            </TableCell>
                            {row.map((val, j) => {
                              const color = val > baseCase ? '#e8f5e9' : val < baseCase ? '#ffebee' : 'inherit';
                              return (
                                <TableCell key={j} align="right" sx={{ bgcolor: color }}>
                                  {val.toFixed(2)}
                                </TableCell>
                              );
                            })}
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Scenario Comparison Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Scenario Results</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={scenarioResults}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip formatter={(val) => `${val} ${metricUnit}`} />
                    <Bar dataKey="value">
                      {scenarioResults.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={index === 0 ? '#2196f3' : index === 1 ? '#4caf50' : '#f44336'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Waterfall Chart - Value Drivers</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <ComposedChart data={waterfallData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value">
                      {waterfallData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </ComposedChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Break-Even Analysis Tab */}
      <TabPanel value={tabValue} index={3}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>Break-Even Analysis</Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Shows the value each variable must reach to achieve {metricName} = {breakEvenTarget}
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Variable</TableCell>
                    <TableCell align="right">Base Value</TableCell>
                    <TableCell align="right">Break-Even Value</TableCell>
                    <TableCell align="right">Change Required</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {breakEvenData.map((row) => (
                    <TableRow key={row.variable}>
                      <TableCell>{row.variable}</TableCell>
                      <TableCell align="right">{row.baseValue.toFixed(2)} {row.unit}</TableCell>
                      <TableCell align="right">{row.breakEvenValue?.toFixed(2)} {row.unit}</TableCell>
                      <TableCell align="right">
                        <Chip
                          label={`${row.percentChange! > 0 ? '+' : ''}${row.percentChange?.toFixed(1)}%`}
                          color={Math.abs(row.percentChange!) < 20 ? 'success' : 'warning'}
                          size="small"
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Downside Protection Tab */}
      <TabPanel value={tabValue} index={4}>
        {downsideMetrics ? (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Downside Risk Metrics</Typography>
                  <TableContainer>
                    <Table>
                      <TableBody>
                        <TableRow>
                          <TableCell>Probability of Loss</TableCell>
                          <TableCell align="right">
                            <Chip
                              label={`${downsideMetrics.probNegative.toFixed(1)}%`}
                              color={downsideMetrics.probNegative < 25 ? 'success' : downsideMetrics.probNegative < 50 ? 'warning' : 'error'}
                            />
                          </TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Average Negative Outcome</TableCell>
                          <TableCell align="right">{downsideMetrics.avgNegative.toFixed(2)} {metricUnit}</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Worst Case</TableCell>
                          <TableCell align="right">{downsideMetrics.worstCase.toFixed(2)} {metricUnit}</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>5th Percentile (95% VaR)</TableCell>
                          <TableCell align="right">{downsideMetrics.downside5th.toFixed(2)} {metricUnit}</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Downside Deviation</TableCell>
                          <TableCell align="right">{downsideMetrics.downsideDeviation.toFixed(2)} {metricUnit}</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Risk Assessment</Typography>
                  <Alert severity={downsideMetrics.probNegative < 25 ? 'success' : downsideMetrics.probNegative < 50 ? 'warning' : 'error'} sx={{ mb: 2 }}>
                    <Typography variant="body2">
                      <strong>Risk Level: {downsideMetrics.probNegative < 25 ? 'Low' : downsideMetrics.probNegative < 50 ? 'Medium' : 'High'}</strong>
                    </Typography>
                    <Typography variant="body2">
                      There is a {downsideMetrics.probNegative.toFixed(1)}% chance of not achieving the target.
                    </Typography>
                  </Alert>

                  <Typography variant="body2" paragraph>
                    <strong>Recommendations:</strong>
                  </Typography>
                  {downsideMetrics.probNegative > 50 && (
                    <Alert severity="error" sx={{ mb: 1 }}>
                      High risk - Consider hedging strategies or restructuring the deal
                    </Alert>
                  )}
                  {downsideMetrics.probNegative > 25 && downsideMetrics.probNegative <= 50 && (
                    <Alert severity="warning" sx={{ mb: 1 }}>
                      Moderate risk - Monitor key variables closely and have contingency plans
                    </Alert>
                  )}
                  {downsideMetrics.probNegative <= 25 && (
                    <Alert severity="success" sx={{ mb: 1 }}>
                      Low risk - Proceed with confidence, maintain monitoring
                    </Alert>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        ) : (
          <Alert severity="info">
            Run Monte Carlo simulation first to see downside protection analysis
          </Alert>
        )}
      </TabPanel>
    </Box>
  );
};
