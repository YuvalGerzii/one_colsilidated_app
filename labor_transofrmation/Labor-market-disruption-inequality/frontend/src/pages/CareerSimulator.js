import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Card,
  CardContent,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function CareerSimulator() {
  const [workerId] = useState(1);
  const [selectedCareer, setSelectedCareer] = useState('');
  const [simulation, setSimulation] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);

  const careerOptions = [
    'data_technician',
    'software_engineer',
    'data_scientist',
    'project_manager',
    'devops_engineer',
    'ux_designer'
  ];

  const runSimulation = async () => {
    if (!selectedCareer) return;

    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/autopilot/simulate-career`, {
        career_path: selectedCareer,
        worker_id: workerId,
        time_horizon_years: 10
      });
      setSimulation(response.data);
    } catch (error) {
      console.error('Error running simulation:', error);
    } finally {
      setLoading(false);
    }
  };

  const compareAll = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/autopilot/compare-careers`, {
        worker_id: workerId,
        career_options: careerOptions,
        time_horizon_years: 10
      });
      setComparison(response.data);
    } catch (error) {
      console.error('Error comparing careers:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCareerName = (career) => {
    return career.split('_').map(word =>
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Career Simulator
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Simulate different career paths: income, burnout, growth, and market value projections
      </Typography>

      {/* Career Selection */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Select Career Path</InputLabel>
              <Select
                value={selectedCareer}
                onChange={(e) => setSelectedCareer(e.target.value)}
                label="Select Career Path"
              >
                {careerOptions.map((career) => (
                  <MenuItem key={career} value={career}>
                    {formatCareerName(career)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={3}>
            <Button
              fullWidth
              variant="contained"
              onClick={runSimulation}
              disabled={loading || !selectedCareer}
              sx={{ height: '56px' }}
            >
              Simulate
            </Button>
          </Grid>
          <Grid item xs={12} md={3}>
            <Button
              fullWidth
              variant="outlined"
              onClick={compareAll}
              disabled={loading}
              sx={{ height: '56px' }}
            >
              Compare All
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Simulation Results */}
      {simulation && (
        <Box>
          {/* Summary Cards */}
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Peak Income
                  </Typography>
                  <Typography variant="h5">
                    ${simulation.summary.peak_income.toLocaleString()}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Avg Burnout
                  </Typography>
                  <Typography variant="h5" color={
                    simulation.summary.avg_burnout > 70 ? 'error' :
                    simulation.summary.avg_burnout > 50 ? 'warning' : 'success'
                  }>
                    {simulation.summary.avg_burnout.toFixed(0)}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Life Satisfaction
                  </Typography>
                  <Typography variant="h5">
                    {simulation.summary.avg_life_satisfaction.toFixed(0)}/100
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Market Value
                  </Typography>
                  <Typography variant="h5">
                    {simulation.summary.final_market_value.toFixed(0)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Recommendation */}
          <Alert
            severity={
              simulation.summary.overall_recommendation.includes('HIGHLY') ? 'success' :
              simulation.summary.overall_recommendation.includes('RECOMMENDED') ? 'info' :
              simulation.summary.overall_recommendation.includes('CAUTION') ? 'warning' : 'error'
            }
            sx={{ mb: 3 }}
          >
            <Typography variant="h6">
              {simulation.summary.overall_recommendation}
            </Typography>
          </Alert>

          {/* Income Projection Chart */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Income Projection (10 Years)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={simulation.income_projection}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" label={{ value: 'Year', position: 'insideBottom', offset: -5 }} />
                <YAxis label={{ value: 'Salary ($)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="salary" stroke="#4caf50" fill="#4caf50" fillOpacity={0.6} name="Nominal Salary" />
                <Area type="monotone" dataKey="real_salary" stroke="#2196f3" fill="#2196f3" fillOpacity={0.4} name="Real Salary (Inflation Adjusted)" />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>

          {/* Burnout & Satisfaction */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Burnout & Life Satisfaction
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={simulation.life_satisfaction.map((item, idx) => ({
                ...item,
                burnout: simulation.burnout_curve[idx].burnout_level
              }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="satisfaction_score" stroke="#4caf50" name="Life Satisfaction" />
                <Line type="monotone" dataKey="burnout" stroke="#f44336" name="Burnout Level" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>

          {/* Market Value & Growth */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Market Value & Career Growth
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={simulation.market_value_projection.map((item, idx) => ({
                ...item,
                growth: simulation.growth_trajectory[idx].growth_score
              }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="market_value_index" stroke="#2196f3" name="Market Value" />
                <Line type="monotone" dataKey="growth" stroke="#ff9800" name="Growth Potential" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>

          {/* Risk Factors */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Risk Factors & Career Longevity
            </Typography>
            <List>
              {simulation.summary.risk_factors.map((risk, index) => (
                <ListItem key={index}>
                  <Chip label={risk} color="warning" sx={{ mr: 2 }} />
                </ListItem>
              ))}
            </List>
            <Alert severity="info" sx={{ mt: 2 }}>
              <Typography variant="body2">
                Estimated Career Longevity: <strong>{simulation.summary.career_longevity} years</strong>
              </Typography>
            </Alert>
          </Paper>
        </Box>
      )}

      {/* Career Comparison */}
      {comparison && (
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="h5" gutterBottom>
            Career Comparison Matrix
          </Typography>

          <Alert severity="success" sx={{ mb: 3 }}>
            <Typography variant="h6">
              Best Overall: {formatCareerName(comparison.overall_best.recommended_career)}
            </Typography>
            <Typography variant="body2">
              Score: {comparison.overall_best.overall_score} - {comparison.overall_best.rationale}
            </Typography>
          </Alert>

          <Grid container spacing={2}>
            {comparison.comparison_matrix.map((career, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="h6">
                      {formatCareerName(career.career)}
                    </Typography>

                    <Grid container spacing={1} sx={{ mt: 1 }}>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Avg Income
                        </Typography>
                        <Typography variant="body1">
                          ${(career.avg_income / 1000).toFixed(0)}K
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Peak Income
                        </Typography>
                        <Typography variant="body1">
                          ${(career.peak_income / 1000).toFixed(0)}K
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Burnout
                        </Typography>
                        <Typography variant="body1">
                          {career.avg_burnout.toFixed(0)}%
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Satisfaction
                        </Typography>
                        <Typography variant="body1">
                          {career.avg_satisfaction.toFixed(0)}/100
                        </Typography>
                      </Grid>
                    </Grid>

                    <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                      {career.recommendation}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}
    </Box>
  );
}

export default CareerSimulator;
