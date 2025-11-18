import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Chip,
  Alert
} from '@mui/material';
import {
  ComposableMap,
  Geographies,
  Geography
} from 'react-simple-maps';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const geoUrl = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

function GovernmentDashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/digital-twin/government-dashboard`);
      setDashboardData(response.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Typography>Loading...</Typography>;
  if (!dashboardData) return <Typography>No data available</Typography>;

  const getRiskColor = (risk) => {
    if (risk < 30) return '#4caf50';
    if (risk < 60) return '#ff9800';
    return '#f44336';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Government Policy Dashboard
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Nationwide labor market insights and policy recommendations
      </Typography>

      {/* Macro Risk */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          National Risk Overview
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Macro Risk Index
                </Typography>
                <Typography variant="h3" color={dashboardData.macro_risk_index.level === 'High' ? 'error' : 'warning'}>
                  {dashboardData.macro_risk_index.index}
                </Typography>
                <Chip
                  label={dashboardData.macro_risk_index.level}
                  color={dashboardData.macro_risk_index.level === 'High' ? 'error' : 'warning'}
                  sx={{ mt: 1 }}
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Workers at Risk
                </Typography>
                <Typography variant="h4" color="error">
                  {(dashboardData.total_workers_at_risk / 1000000).toFixed(1)}M
                </Typography>
                <Typography variant="caption">
                  Across all regions
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  National Avg Risk
                </Typography>
                <Typography variant="h4">
                  {dashboardData.region_heatmap.global_avg_risk}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>

      {/* Region Heatmap */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Regional Risk Heatmap
        </Typography>

        <Grid container spacing={2}>
          {dashboardData.region_heatmap.regions.map((region, index) => (
            <Grid item xs={12} md={6} lg={4} key={index}>
              <Card sx={{ borderLeft: `4px solid ${getRiskColor(region.risk_score)}` }}>
                <CardContent>
                  <Typography variant="h6">
                    {region.name}
                  </Typography>
                  <Typography variant="h4" sx={{ color: getRiskColor(region.risk_score), mt: 1 }}>
                    {region.risk_score}%
                  </Typography>
                  <Chip
                    label={region.risk_level}
                    size="small"
                    sx={{ mt: 1, mb: 1 }}
                    style={{ backgroundColor: getRiskColor(region.risk_score), color: 'white' }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    Workers at risk: {(region.workers_at_risk / 1000).toFixed(0)}K
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Unemployment: {region.unemployment_rate}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* High Risk Occupations */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Top Threatened Occupations
        </Typography>

        <List>
          {dashboardData.high_risk_occupations.map((occ, index) => (
            <ListItem key={index}>
              <ListItemText
                primary={
                  <Typography variant="h6">
                    {occ.occupation}
                  </Typography>
                }
                secondary={
                  <>
                    <Typography variant="body2">
                      Workers: {(occ.workers / 1000000).toFixed(1)}M
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      <Chip
                        label={`${occ.displacement_risk}% Displacement Risk`}
                        color="error"
                        size="small"
                      />
                    </Box>
                  </>
                }
              />
            </ListItem>
          ))}
        </List>
      </Paper>

      {/* Policy Recommendations */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Policy Recommendations
        </Typography>

        {dashboardData.policy_recommendations.map((rec, index) => (
          <Alert key={index} severity="info" sx={{ mb: 2 }}>
            {rec}
          </Alert>
        ))}
      </Paper>
    </Box>
  );
}

export default GovernmentDashboard;
