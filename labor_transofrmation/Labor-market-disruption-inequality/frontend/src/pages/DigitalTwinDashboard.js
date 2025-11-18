import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  LinearProgress,
  Chip,
  Alert
} from '@mui/material';
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
  ResponsiveContainer
} from 'recharts';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function DigitalTwinDashboard() {
  const [macroRisk, setMacroRisk] = useState(null);
  const [simulation, setSimulation] = useState(null);
  const [occupation, setOccupation] = useState('');
  const [displacementPred, setDisplacementPred] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadMacroRisk();
  }, []);

  const loadMacroRisk = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/digital-twin/macro-risk-index`);
      setMacroRisk(response.data);
    } catch (error) {
      console.error('Error loading macro risk:', error);
    }
  };

  const runSimulation = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/digital-twin/simulate`, {
        time_horizon_months: 12,
        automation_adoption_rate: 0.05
      });
      setSimulation(response.data);
    } catch (error) {
      console.error('Error running simulation:', error);
    } finally {
      setLoading(false);
    }
  };

  const predictDisplacement = async () => {
    if (!occupation) return;

    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/digital-twin/displacement-prediction`, {
        occupation,
        time_horizon_months: 18
      });
      setDisplacementPred(response.data);
    } catch (error) {
      console.error('Error predicting displacement:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    const colors = {
      'Low': 'success',
      'Moderate': 'warning',
      'High': 'error',
      'Critical': 'error'
    };
    return colors[level] || 'default';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Workforce Digital Twin™
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Real-time AI simulation of the entire labor market
      </Typography>

      {/* Macro Risk Index */}
      {macroRisk && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Macro AI Job-Risk Index
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h2" color={`${getRiskColor(macroRisk.level)}.main`}>
                  {macroRisk.index}
                </Typography>
                <Chip
                  label={macroRisk.level}
                  color={getRiskColor(macroRisk.level)}
                  sx={{ mt: 1 }}
                />
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  Trend: {macroRisk.trend}
                </Typography>
              </Box>
            </Grid>

            <Grid item xs={12} md={8}>
              <Typography variant="h6" gutterBottom>
                Risk Factors
              </Typography>
              <Grid container spacing={2}>
                {Object.entries(macroRisk.factors).map(([key, value]) => (
                  <Grid item xs={12} sm={6} key={key}>
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        {key.replace(/_/g, ' ').toUpperCase()}
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={value}
                        sx={{ mt: 1 }}
                        color={value > 70 ? 'error' : value > 50 ? 'warning' : 'success'}
                      />
                      <Typography variant="body2">{value}%</Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>

              <Alert severity="info" sx={{ mt: 2 }}>
                <strong>Recommendation:</strong> {macroRisk.recommendation}
              </Alert>
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* Market Simulation */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Labor Market Simulation
        </Typography>

        <Button
          variant="contained"
          onClick={runSimulation}
          disabled={loading}
          sx={{ mb: 2 }}
        >
          {loading ? 'Simulating...' : 'Run 12-Month Simulation'}
        </Button>

        {simulation && (
          <Box>
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Projected Job Loss
                    </Typography>
                    <Typography variant="h5" color="error">
                      {simulation.insights.projected_job_loss.toLocaleString()}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Unemployment Rate Change
                    </Typography>
                    <Typography variant="h5">
                      +{simulation.insights.unemployment_delta.toFixed(2)}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={simulation.simulations}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" label={{ value: 'Month', position: 'insideBottom', offset: -5 }} />
                <YAxis yAxisId="left" label={{ value: 'Jobs (millions)', angle: -90, position: 'insideLeft' }} />
                <YAxis yAxisId="right" orientation="right" label={{ value: 'Unemployment %', angle: 90, position: 'insideRight' }} />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="total_jobs" stroke="#8884d8" name="Total Jobs" />
                <Line yAxisId="right" type="monotone" dataKey="unemployment_rate" stroke="#f44336" name="Unemployment %" />
              </LineChart>
            </ResponsiveContainer>
          </Box>
        )}
      </Paper>

      {/* Occupation Displacement Prediction */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Occupation Displacement Predictor
        </Typography>

        <Grid container spacing={2} alignItems="center" sx={{ mb: 3 }}>
          <Grid item xs={12} md={8}>
            <TextField
              fullWidth
              label="Occupation"
              value={occupation}
              onChange={(e) => setOccupation(e.target.value)}
              placeholder="e.g., Data Entry Specialist, Cashier, Accountant"
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <Button
              fullWidth
              variant="contained"
              onClick={predictDisplacement}
              disabled={loading || !occupation}
              sx={{ height: '56px' }}
            >
              Predict Risk
            </Button>
          </Grid>
        </Grid>

        {displacementPred && (
          <Box>
            <Alert
              severity={
                displacementPred.current_risk > 70 ? 'error' :
                displacementPred.current_risk > 50 ? 'warning' : 'info'
              }
              sx={{ mb: 3 }}
            >
              <Typography variant="h6">
                {displacementPred.occupation}: {displacementPred.current_risk}% Displacement Risk
              </Typography>
              <Typography variant="body2">
                {displacementPred.recommended_action}
              </Typography>
            </Alert>

            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={displacementPred.displacement_curve}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" label={{ value: 'Months Ahead', position: 'insideBottom', offset: -5 }} />
                <YAxis label={{ value: 'Displacement Probability %', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="displacement_probability" stroke="#f44336" name="Displacement Risk %" />
                <Line type="monotone" dataKey="jobs_at_risk_pct" stroke="#ff9800" name="Jobs at Risk %" />
              </LineChart>
            </ResponsiveContainer>
          </Box>
        )}
      </Paper>
    </Box>
  );
}

export default DigitalTwinDashboard;
