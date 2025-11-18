import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Alert,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  Tab
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import BusinessIcon from '@mui/icons-material/Business';
import PeopleIcon from '@mui/icons-material/People';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import WarningIcon from '@mui/icons-material/Warning';
import BalanceIcon from '@mui/icons-material/Balance';
import PolicyIcon from '@mui/icons-material/Policy';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function CorporateTransformation() {
  const [companyId] = useState(1);
  const [dashboard, setDashboard] = useState(null);
  const [predictiveHiring, setPredictiveHiring] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDashboard();
    loadPredictiveHiring();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/corporate/transformation-dashboard/${companyId}`);
      setDashboard(response.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadPredictiveHiring = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/corporate/predictive-hiring/${companyId}`);
      setPredictiveHiring(response.data);
    } catch (error) {
      console.error('Error loading predictive hiring:', error);
    }
  };

  if (!dashboard) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4">Loading Corporate Transformation Dashboard...</Typography>
        <LinearProgress sx={{ mt: 2 }} />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Corporate Workforce Transformation OS
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Internal tools to reduce layoffs, increase productivity, and manage automation transitions
      </Typography>

      {/* Key Metrics */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#e3f2fd' }}>
            <CardContent>
              <PeopleIcon sx={{ fontSize: 40, color: '#1976d2' }} />
              <Typography variant="h4">{dashboard.overview.total_employees}</Typography>
              <Typography variant="body2" color="text.secondary">
                Total Employees
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#fff3e0' }}>
            <CardContent>
              <WarningIcon sx={{ fontSize: 40, color: '#f57c00' }} />
              <Typography variant="h4">{dashboard.overview.at_risk_employees}</Typography>
              <Typography variant="body2" color="text.secondary">
                At-Risk Employees
              </Typography>
              <Typography variant="caption">
                {((dashboard.overview.at_risk_employees / dashboard.overview.total_employees) * 100).toFixed(1)}% of workforce
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#e8f5e9' }}>
            <CardContent>
              <AutorenewIcon sx={{ fontSize: 40, color: '#388e3c' }} />
              <Typography variant="h4">{dashboard.overview.automation_opportunities}</Typography>
              <Typography variant="body2" color="text.secondary">
                Automation Opportunities
              </Typography>
              <Typography variant="caption">
                ${(dashboard.overview.estimated_annual_savings / 1000000).toFixed(1)}M annual savings
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#f3e5f5' }}>
            <CardContent>
              <TrendingUpIcon sx={{ fontSize: 40, color: '#7b1fa2' }} />
              <Typography variant="h4">{dashboard.workforce_health.automation_readiness}%</Typography>
              <Typography variant="body2" color="text.secondary">
                Automation Readiness
              </Typography>
              <LinearProgress
                variant="determinate"
                value={dashboard.workforce_health.automation_readiness}
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Financial Impact Overview */}
      <Paper sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <Typography variant="h5" gutterBottom>Financial Impact</Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={3}>
            <Typography variant="h4">${(dashboard.financial_impact.ytd_savings / 1000).toFixed(0)}K</Typography>
            <Typography variant="body2">YTD Savings</Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="h4">{dashboard.financial_impact.roi_on_automation}%</Typography>
            <Typography variant="body2">ROI on Automation</Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="h4">${(dashboard.financial_impact.cost_per_automated_process / 1000).toFixed(0)}K</Typography>
            <Typography variant="body2">Cost per Process</Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="h4">{dashboard.financial_impact.average_payback_months}mo</Typography>
            <Typography variant="body2">Avg Payback Period</Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Workforce Health" />
          <Tab label="Predictive Hiring" />
          <Tab label="Automation Status" />
          <Tab label="Recent Activities" />
        </Tabs>
      </Box>

      {/* Tab Content */}
      {activeTab === 0 && (
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>Workforce Health Metrics</Typography>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography>Employee Satisfaction</Typography>
                  <Typography fontWeight="bold">{dashboard.workforce_health.employee_satisfaction}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={dashboard.workforce_health.employee_satisfaction}
                  color="success"
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography>Automation Readiness</Typography>
                  <Typography fontWeight="bold">{dashboard.workforce_health.automation_readiness}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={dashboard.workforce_health.automation_readiness}
                  color="primary"
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography>Skill Gap Index</Typography>
                  <Typography fontWeight="bold">{dashboard.workforce_health.skill_gap_index}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={dashboard.workforce_health.skill_gap_index}
                  color="warning"
                />
              </Box>

              <Alert severity="info" sx={{ mt: 2 }}>
                Turnover Rate: {dashboard.workforce_health.turnover_rate}% (Industry avg: 15%)
              </Alert>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>Recommendations</Typography>
              <List>
                {dashboard.recommendations.map((rec, i) => (
                  <ListItem key={i}>
                    <ListItemText
                      primary={`${i + 1}. ${rec}`}
                      primaryTypographyProps={{ fontSize: '0.95rem' }}
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && predictiveHiring && (
        <Box>
          <Typography variant="h6" gutterBottom>Predictive Hiring Insights</Typography>

          <TableContainer component={Paper} sx={{ mb: 3 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Role</TableCell>
                  <TableCell>Trend</TableCell>
                  <TableCell>Growth Rate</TableCell>
                  <TableCell>Demand Score</TableCell>
                  <TableCell>Automation Impact</TableCell>
                  <TableCell>Recommendation</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {predictiveHiring.role_insights.map((role, i) => (
                  <TableRow key={i}>
                    <TableCell>{role.role}</TableCell>
                    <TableCell>
                      <Chip
                        label={role.trend}
                        color={
                          role.trend === 'growing' ? 'success' :
                          role.trend === 'emerging' ? 'primary' :
                          role.trend === 'shrinking' ? 'error' : 'default'
                        }
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {role.growth_rate > 0 ? '+' : ''}{role.growth_rate}%
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Box sx={{ width: '100%', mr: 1 }}>
                          <LinearProgress variant="determinate" value={role.future_demand_score} />
                        </Box>
                        <Box sx={{ minWidth: 35 }}>
                          <Typography variant="body2" color="text.secondary">
                            {role.future_demand_score}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={role.automation_impact}
                        size="small"
                        variant="outlined"
                        color={
                          role.automation_impact.includes('very_low') ? 'success' :
                          role.automation_impact.includes('low') ? 'primary' :
                          role.automation_impact.includes('high') ? 'error' : 'warning'
                        }
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{role.recommendation}</Typography>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>Emerging Roles</Typography>
                <List>
                  {predictiveHiring.emerging_roles.map((role, i) => (
                    <ListItem key={i}>
                      <ListItemText
                        primary={role.role}
                        secondary={
                          <>
                            <Typography component="span" variant="body2" color="text.primary">
                              {role.demand_trajectory}
                            </Typography>
                            {" — "}{role.suggested_action}
                          </>
                        }
                      />
                      <Chip
                        label={role.market_availability}
                        size="small"
                        color={role.market_availability === 'scarce' ? 'error' : 'warning'}
                      />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>Hiring Timeline</Typography>
                <List dense>
                  {Object.entries(predictiveHiring.hiring_timeline_recommendations).map(([quarter, plan], i) => (
                    <ListItem key={i}>
                      <ListItemText
                        primary={quarter.toUpperCase()}
                        secondary={plan}
                      />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>
          </Grid>
        </Box>
      )}

      {activeTab === 2 && (
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>Automation Progress</Typography>
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography>Current Automation Rate</Typography>
                  <Typography fontWeight="bold">{dashboard.automation_status.current_automation_rate}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={dashboard.automation_status.current_automation_rate}
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography>Target Automation Rate</Typography>
                  <Typography fontWeight="bold">{dashboard.automation_status.target_automation_rate}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={dashboard.automation_status.target_automation_rate}
                />
              </Box>

              <Divider sx={{ my: 2 }} />

              <Typography variant="body2" gutterBottom>
                Projects In Progress: <strong>{dashboard.automation_status.projects_in_progress}</strong>
              </Typography>
              <Typography variant="body2">
                Projects Completed: <strong>{dashboard.automation_status.projects_completed}</strong>
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>Investment Analysis</Typography>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">Retraining Investment Needed</Typography>
                <Typography variant="h5" color="primary">
                  ${(dashboard.overview.retraining_investment_needed / 1000000).toFixed(2)}M
                </Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">Annual Savings Potential</Typography>
                <Typography variant="h5" color="success.main">
                  ${(dashboard.overview.estimated_annual_savings / 1000000).toFixed(2)}M
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box>
                <Typography variant="body2" color="text.secondary">Net ROI</Typography>
                <Typography variant="h5" color="success.main">
                  {((dashboard.overview.estimated_annual_savings - dashboard.overview.retraining_investment_needed) / dashboard.overview.retraining_investment_needed * 100).toFixed(0)}%
                </Typography>
              </Box>

              <Alert severity="success" sx={{ mt: 2 }}>
                Payback period: {(dashboard.overview.retraining_investment_needed / dashboard.overview.estimated_annual_savings * 12).toFixed(1)} months
              </Alert>
            </Paper>
          </Grid>
        </Grid>
      )}

      {activeTab === 3 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Recent Activities</Typography>
          <List>
            {dashboard.recent_activities.map((activity, i) => (
              <React.Fragment key={i}>
                <ListItem>
                  <ListItemText
                    primary={activity.activity}
                    secondary={
                      <>
                        <Typography component="span" variant="body2" color="text.primary">
                          {activity.date}
                        </Typography>
                        {" — "}{activity.impact}
                      </>
                    }
                  />
                </ListItem>
                {i < dashboard.recent_activities.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      )}

      {/* Quick Actions */}
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>Quick Actions</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <Button variant="contained" fullWidth startIcon={<PeopleIcon />}>
              Run Internal Job Matching
            </Button>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Button variant="contained" color="secondary" fullWidth startIcon={<AutorenewIcon />}>
              Scan for Automations
            </Button>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Button variant="contained" color="warning" fullWidth startIcon={<WarningIcon />}>
              Calculate Employee Risks
            </Button>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Button variant="contained" color="success" fullWidth startIcon={<BalanceIcon />}>
              Simulate Union Negotiation
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
}

export default CorporateTransformation;
