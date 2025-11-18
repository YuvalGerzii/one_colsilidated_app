import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Chip
} from '@mui/material';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { getWorkforceDashboard, getWorkforcePlanning } from '../services/api';

function EnterpriseDashboard() {
  const [enterpriseId] = useState(1); // Demo: hardcoded enterprise ID
  const [dashboardData, setDashboardData] = useState(null);
  const [planningData, setPlanningData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);

      const dashResponse = await getWorkforceDashboard(enterpriseId);
      setDashboardData(dashResponse.data);

      const planResponse = await getWorkforcePlanning(enterpriseId);
      setPlanningData(planResponse.data);

    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LinearProgress />;
  }

  if (!dashboardData) {
    return <Typography>No data available</Typography>;
  }

  const COLORS = ['#4caf50', '#ff9800', '#f44336'];

  const riskDistributionData = [
    { name: 'Low Risk', value: dashboardData.risk_distribution.low },
    { name: 'Medium Risk', value: dashboardData.risk_distribution.medium },
    { name: 'High Risk', value: dashboardData.risk_distribution.high }
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Enterprise HR Dashboard
      </Typography>

      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        {dashboardData.company_name} - {dashboardData.subscription_tier} Plan
      </Typography>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Employees
              </Typography>
              <Typography variant="h4">
                {dashboardData.total_employees}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                High Risk Workers
              </Typography>
              <Typography variant="h4" color="error">
                {dashboardData.high_risk_employees}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Avg Risk Score
              </Typography>
              <Typography variant="h4">
                {dashboardData.avg_risk_score}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Subscription Status
              </Typography>
              <Chip label="Active" color="success" />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Risk Distribution Chart */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Workforce Risk Distribution
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={riskDistributionData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value}`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {riskDistributionData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </Paper>

      <Grid container spacing={3}>
        {/* Skills Gap Summary */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Most Common Skill Gaps
            </Typography>
            <List>
              {dashboardData.skills_gap_summary.most_common_gaps.map((gap, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={gap.skill}
                    secondary={`${gap.workers_lacking} workers lacking this skill`}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Recommended Training */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recommended Training Programs
            </Typography>
            <List>
              {dashboardData.recommended_training.map((program, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={program.program}
                    secondary={
                      <>
                        <Typography variant="body2" component="span">
                          Target: {program.target_employees} employees
                        </Typography>
                        <br />
                        <Typography variant="body2" component="span">
                          Cost: ${program.estimated_cost.toLocaleString()}
                        </Typography>
                        <br />
                        <Chip
                          size="small"
                          label={`ROI: ${program.roi_score}/10`}
                          color="primary"
                          sx={{ mt: 0.5 }}
                        />
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Workforce Planning */}
        {planningData && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Workforce Planning Insights
              </Typography>

              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Automation Impact Forecast
                  </Typography>
                  <Typography variant="body2">
                    Next 12 months: {planningData.automation_impact_forecast.next_12_months.jobs_at_risk} jobs at risk
                    ({(planningData.automation_impact_forecast.next_12_months.automation_potential * 100).toFixed(0)}% automation potential)
                  </Typography>
                  <Typography variant="body2">
                    Next 24 months: {planningData.automation_impact_forecast.next_24_months.jobs_at_risk} jobs at risk
                    ({(planningData.automation_impact_forecast.next_24_months.automation_potential * 100).toFixed(0)}% automation potential)
                  </Typography>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Emerging Skill Needs
                  </Typography>
                  {planningData.emerging_skill_needs.map((skill, index) => (
                    <Chip
                      key={index}
                      label={`${skill.skill} (${skill.demand_growth})`}
                      sx={{ m: 0.5 }}
                      color="primary"
                      variant="outlined"
                    />
                  ))}
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
}

export default EnterpriseDashboard;
