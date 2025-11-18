import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Tabs,
  Tab,
  Box,
  TextField,
  Chip,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress
} from '@mui/material';
import {
  TrendingUp,
  AccountBalance,
  ShowChart,
  Work,
  Assessment,
  AttachMoney,
  Schedule,
  Security,
  CompareArrows,
  CheckCircle,
  Warning,
  Info
} from '@mui/icons-material';
import axios from 'axios';

function GigEconomyHub() {
  const [activeTab, setActiveTab] = useState(0);
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  // Skill Matching States
  const [skills, setSkills] = useState('');
  const [hoursAvailable, setHoursAvailable] = useState(20);
  const [incomeTarget, setIncomeTarget] = useState(3000);
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [gigMatches, setGigMatches] = useState(null);

  // Benefits Calculator States
  const [annualIncome, setAnnualIncome] = useState(60000);
  const [age, setAge] = useState(30);
  const [dependents, setDependents] = useState(0);
  const [state, setState] = useState('CA');
  const [retirementPct, setRetirementPct] = useState(10);
  const [benefitsResults, setBenefitsResults] = useState(null);

  // Income Stabilization States
  const [monthlyExpenses, setMonthlyExpenses] = useState(3500);
  const [stabilizationResults, setStabilizationResults] = useState(null);

  // Comparison Dialog
  const [comparisonOpen, setComparisonOpen] = useState(false);
  const [w2Salary, setW2Salary] = useState(70000);
  const [comparisonResults, setComparisonResults] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:8000/api/v1/gig/dashboard/1');
      setDashboard(response.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const matchSkillsToGigs = async () => {
    try {
      setLoading(true);
      const skillsList = skills.split(',').map(s => s.trim().toLowerCase().replace(/ /g, '_'));
      const response = await axios.post('http://localhost:8000/api/v1/gig/match-skills-to-gigs', {
        worker_skills: skillsList,
        availability_hours_weekly: hoursAvailable,
        income_target_monthly: incomeTarget,
        preferences: { remote_only: remoteOnly }
      });
      setGigMatches(response.data);
    } catch (error) {
      console.error('Error matching skills:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateBenefits = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:8000/api/v1/gig/benefits-calculator', {
        annual_gig_income: annualIncome,
        state: state,
        age: age,
        dependents: dependents,
        retirement_contribution_pct: retirementPct
      });
      setBenefitsResults(response.data);
    } catch (error) {
      console.error('Error calculating benefits:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateIncomeStabilization = async () => {
    try {
      setLoading(true);
      const incomeSourcesExample = [
        { name: "Upwork", monthly_avg: 1500, volatility: "medium" },
        { name: "Fiverr", monthly_avg: 950, volatility: "high" },
        { name: "Part-time", monthly_avg: 800, volatility: "low" }
      ];

      const response = await axios.post('http://localhost:8000/api/v1/gig/income-stabilization-plan', {
        current_income_sources: incomeSourcesExample,
        monthly_expenses: monthlyExpenses,
        emergency_fund_months: 6,
        risk_tolerance: "moderate"
      });
      setStabilizationResults(response.data);
    } catch (error) {
      console.error('Error calculating stabilization:', error);
    } finally {
      setLoading(false);
    }
  };

  const compareGigVsW2 = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        `http://localhost:8000/api/v1/gig/compare-gig-vs-w2?gig_annual_income=${annualIncome}&w2_annual_salary=${w2Salary}&age=${age}&state=${state}`
      );
      setComparisonResults(response.data);
      setComparisonOpen(true);
    } catch (error) {
      console.error('Error comparing:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const getStabilityColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'error';
  };

  const getRiskColor = (risk) => {
    if (risk === 'low') return 'success';
    if (risk === 'moderate') return 'warning';
    return 'error';
  };

  if (loading && !dashboard) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>Loading Gig Economy Hub...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" gutterBottom>
        Gig Economy & Hybrid Labor Hub
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Match skills to gigs, stabilize income, optimize benefits, and manage hybrid work
      </Typography>

      {/* Key Metrics */}
      {dashboard && (
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <Typography variant="h4">{dashboard.gig_summary.active_platforms}</Typography>
                    <Typography variant="body2">Active Platforms</Typography>
                  </div>
                  <Work sx={{ fontSize: 40, opacity: 0.8 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <Typography variant="h4">${dashboard.gig_summary.monthly_income.toLocaleString()}</Typography>
                    <Typography variant="body2">Monthly Income</Typography>
                  </div>
                  <AttachMoney sx={{ fontSize: 40, opacity: 0.8 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <Typography variant="h4">${dashboard.gig_summary.average_hourly_rate}</Typography>
                    <Typography variant="body2">Avg Hourly Rate</Typography>
                  </div>
                  <TrendingUp sx={{ fontSize: 40, opacity: 0.8 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', color: 'white' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <Typography variant="h4">{dashboard.stability_metrics.income_stability_score}</Typography>
                    <Typography variant="body2">Stability Score</Typography>
                  </div>
                  <ShowChart sx={{ fontSize: 40, opacity: 0.8 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Main Content Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={activeTab} onChange={handleTabChange} variant="scrollable" scrollButtons="auto">
          <Tab label="Gig Matching" icon={<Work />} />
          <Tab label="Income Stability" icon={<ShowChart />} />
          <Tab label="Benefits Calculator" icon={<Security />} />
          <Tab label="Dashboard" icon={<Assessment />} />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {/* Tab 1: Gig Matching */}
          {activeTab === 0 && (
            <Box>
              <Typography variant="h5" gutterBottom>Match Your Skills to Gig Opportunities</Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
                Find the best gig platforms and opportunities based on your skills and availability
              </Typography>

              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Your Skills (comma-separated)"
                    placeholder="e.g., python, web development, graphic design"
                    value={skills}
                    onChange={(e) => setSkills(e.target.value)}
                    helperText="Enter skills like: python, javascript, writing, design, etc."
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    type="number"
                    label="Hours Available Per Week"
                    value={hoursAvailable}
                    onChange={(e) => setHoursAvailable(parseInt(e.target.value))}
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    type="number"
                    label="Monthly Income Target ($)"
                    value={incomeTarget}
                    onChange={(e) => setIncomeTarget(parseFloat(e.target.value))}
                    sx={{ mb: 2 }}
                  />
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Work Preference</InputLabel>
                    <Select
                      value={remoteOnly ? 'remote' : 'any'}
                      onChange={(e) => setRemoteOnly(e.target.value === 'remote')}
                    >
                      <MenuItem value="any">Any (Remote + Local)</MenuItem>
                      <MenuItem value="remote">Remote Only</MenuItem>
                    </Select>
                  </FormControl>
                  <Button
                    variant="contained"
                    size="large"
                    fullWidth
                    onClick={matchSkillsToGigs}
                    disabled={!skills}
                    sx={{ mb: 2 }}
                  >
                    Find Gig Opportunities
                  </Button>
                </Grid>

                <Grid item xs={12} md={6}>
                  {gigMatches && (
                    <Box>
                      <Alert severity="info" sx={{ mb: 2 }}>
                        Found {gigMatches.total_opportunities} opportunities across{' '}
                        {gigMatches.platforms_to_join.length} platforms
                      </Alert>

                      <Typography variant="h6" gutterBottom>Top Platforms to Join:</Typography>
                      <Box sx={{ mb: 2 }}>
                        {gigMatches.platforms_to_join.map((platform, idx) => (
                          <Chip key={idx} label={platform} sx={{ m: 0.5 }} color="primary" />
                        ))}
                      </Box>

                      <Typography variant="h6" gutterBottom>Income Strategy:</Typography>
                      <Paper sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}>
                        <Typography variant="body2">
                          <strong>Target:</strong> ${gigMatches.income_optimization_strategy.income_target.toLocaleString()}/month
                        </Typography>
                        <Typography variant="body2">
                          <strong>Projected:</strong> ${gigMatches.income_optimization_strategy.total_monthly_income.toLocaleString()}/month
                        </Typography>
                        <Typography variant="body2">
                          <strong>Hours:</strong> {gigMatches.income_optimization_strategy.total_monthly_hours} hours/month
                        </Typography>
                        <Typography variant="body2">
                          <strong>Avg Rate:</strong> ${gigMatches.income_optimization_strategy.average_hourly_rate}/hour
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={gigMatches.income_optimization_strategy.target_achievement_pct}
                          sx={{ mt: 1, height: 8, borderRadius: 4 }}
                        />
                        <Typography variant="caption">
                          {gigMatches.income_optimization_strategy.target_achievement_pct}% of target ({gigMatches.income_optimization_strategy.feasibility})
                        </Typography>
                      </Paper>

                      <Typography variant="h6" gutterBottom>Recommendations:</Typography>
                      <List dense>
                        {gigMatches.recommendations.map((rec, idx) => (
                          <ListItem key={idx}>
                            <ListItemIcon>
                              <CheckCircle color="primary" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText primary={rec} />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}
                </Grid>
              </Grid>

              {gigMatches && gigMatches.top_opportunities && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" gutterBottom>Top Opportunities:</Typography>
                  <TableContainer component={Paper}>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Skill</TableCell>
                          <TableCell>Platform</TableCell>
                          <TableCell>Task</TableCell>
                          <TableCell align="right">Hourly Rate</TableCell>
                          <TableCell align="right">Monthly Potential</TableCell>
                          <TableCell align="right">Match Score</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {gigMatches.top_opportunities.slice(0, 10).map((opp, idx) => (
                          <TableRow key={idx}>
                            <TableCell>{opp.skill}</TableCell>
                            <TableCell>
                              <Chip label={opp.platform} size="small" />
                            </TableCell>
                            <TableCell>{opp.task}</TableCell>
                            <TableCell align="right">${opp.hourly_rate}</TableCell>
                            <TableCell align="right">${opp.monthly_income_potential.toLocaleString()}</TableCell>
                            <TableCell align="right">
                              <Chip label={opp.match_score} color={opp.match_score >= 70 ? 'success' : 'default'} size="small" />
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Box>
              )}
            </Box>
          )}

          {/* Tab 2: Income Stability */}
          {activeTab === 1 && (
            <Box>
              <Typography variant="h5" gutterBottom>Income Stabilization Analysis</Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
                Analyze your income streams for diversification and stability
              </Typography>

              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Monthly Expenses ($)"
                    value={monthlyExpenses}
                    onChange={(e) => setMonthlyExpenses(parseFloat(e.target.value))}
                    sx={{ mb: 2 }}
                  />
                  <Button
                    variant="contained"
                    size="large"
                    fullWidth
                    onClick={calculateIncomeStabilization}
                  >
                    Analyze Income Stability
                  </Button>
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                    Using example income sources: Upwork ($1500), Fiverr ($950), Part-time ($800)
                  </Typography>
                </Grid>

                {stabilizationResults && (
                  <Grid item xs={12} md={8}>
                    <Paper sx={{ p: 2, mb: 2 }}>
                      <Typography variant="h6" gutterBottom>Current Situation</Typography>
                      <Grid container spacing={2}>
                        <Grid item xs={6}>
                          <Typography variant="body2">Monthly Income</Typography>
                          <Typography variant="h5">${stabilizationResults.current_situation.total_monthly_income.toLocaleString()}</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body2">Income Sources</Typography>
                          <Typography variant="h5">{stabilizationResults.current_situation.income_sources_count}</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body2">Surplus/Deficit</Typography>
                          <Typography variant="h5" color={stabilizationResults.current_situation.surplus_deficit >= 0 ? 'success.main' : 'error.main'}>
                            ${stabilizationResults.current_situation.surplus_deficit.toLocaleString()}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body2">Diversification</Typography>
                          <Chip
                            label={stabilizationResults.current_situation.diversification_status.replace('_', ' ')}
                            color={
                              stabilizationResults.current_situation.diversification_status === 'well_diversified' ? 'success' :
                              stabilizationResults.current_situation.diversification_status === 'moderately_concentrated' ? 'warning' : 'error'
                            }
                          />
                        </Grid>
                      </Grid>
                    </Paper>

                    <Paper sx={{ p: 2, mb: 2 }}>
                      <Typography variant="h6" gutterBottom>Stability Score</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Box sx={{ flex: 1, mr: 2 }}>
                          <LinearProgress
                            variant="determinate"
                            value={stabilizationResults.stability_score.score}
                            color={getStabilityColor(stabilizationResults.stability_score.score)}
                            sx={{ height: 10, borderRadius: 5 }}
                          />
                        </Box>
                        <Typography variant="h5">{stabilizationResults.stability_score.score}/100</Typography>
                      </Box>
                      <Chip label={stabilizationResults.stability_score.rating} color={getStabilityColor(stabilizationResults.stability_score.score)} />
                      <Typography variant="body2" sx={{ mt: 1 }}>{stabilizationResults.stability_score.interpretation}</Typography>
                    </Paper>

                    <Paper sx={{ p: 2, mb: 2 }}>
                      <Typography variant="h6" gutterBottom>Risk Assessment</Typography>
                      <Grid container spacing={2}>
                        <Grid item xs={4}>
                          <Typography variant="body2">Income Volatility</Typography>
                          <Chip label={stabilizationResults.risk_assessment.income_volatility} color={getRiskColor(stabilizationResults.risk_assessment.income_volatility)} size="small" />
                        </Grid>
                        <Grid item xs={4}>
                          <Typography variant="body2">Concentration Risk</Typography>
                          <Chip label={stabilizationResults.risk_assessment.concentration_risk} color={getRiskColor(stabilizationResults.risk_assessment.concentration_risk)} size="small" />
                        </Grid>
                        <Grid item xs={4}>
                          <Typography variant="body2">Adequacy Risk</Typography>
                          <Chip label={stabilizationResults.risk_assessment.adequacy_risk} color={getRiskColor(stabilizationResults.risk_assessment.adequacy_risk)} size="small" />
                        </Grid>
                      </Grid>
                    </Paper>

                    <Alert severity="info" sx={{ mb: 2 }}>
                      <Typography variant="subtitle2">Recommended Monthly Income</Typography>
                      <Typography variant="h6">${stabilizationResults.recommendations.recommended_monthly_income.toLocaleString()}</Typography>
                      <Typography variant="body2">
                        Emergency Fund Target: ${stabilizationResults.recommendations.emergency_fund_target.toLocaleString()}
                      </Typography>
                    </Alert>

                    <Typography variant="h6" gutterBottom>Action Items:</Typography>
                    <List dense>
                      {stabilizationResults.recommendations.diversification_actions.map((action, idx) => (
                        <ListItem key={idx}>
                          <ListItemIcon>
                            <Warning color="warning" fontSize="small" />
                          </ListItemIcon>
                          <ListItemText primary={action} />
                        </ListItem>
                      ))}
                    </List>
                  </Grid>
                )}
              </Grid>
            </Box>
          )}

          {/* Tab 3: Benefits Calculator */}
          {activeTab === 2 && (
            <Box>
              <Typography variant="h5" gutterBottom>Gig Worker Benefits Calculator</Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
                Calculate total cost of benefits as a gig worker (health, retirement, taxes)
              </Typography>

              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Annual Gig Income ($)"
                    value={annualIncome}
                    onChange={(e) => setAnnualIncome(parseFloat(e.target.value))}
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    type="number"
                    label="Your Age"
                    value={age}
                    onChange={(e) => setAge(parseInt(e.target.value))}
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    type="number"
                    label="Number of Dependents"
                    value={dependents}
                    onChange={(e) => setDependents(parseInt(e.target.value))}
                    sx={{ mb: 2 }}
                  />
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>State</InputLabel>
                    <Select value={state} onChange={(e) => setState(e.target.value)}>
                      <MenuItem value="CA">California</MenuItem>
                      <MenuItem value="NY">New York</MenuItem>
                      <MenuItem value="TX">Texas</MenuItem>
                      <MenuItem value="FL">Florida</MenuItem>
                      <MenuItem value="WA">Washington</MenuItem>
                    </Select>
                  </FormControl>
                  <TextField
                    fullWidth
                    type="number"
                    label="Retirement Contribution %"
                    value={retirementPct}
                    onChange={(e) => setRetirementPct(parseFloat(e.target.value))}
                    sx={{ mb: 2 }}
                  />
                  <Button
                    variant="contained"
                    size="large"
                    fullWidth
                    onClick={calculateBenefits}
                    sx={{ mb: 1 }}
                  >
                    Calculate Benefits Cost
                  </Button>
                  <Button
                    variant="outlined"
                    size="large"
                    fullWidth
                    onClick={compareGigVsW2}
                    startIcon={<CompareArrows />}
                  >
                    Compare with W2
                  </Button>
                </Grid>

                {benefitsResults && (
                  <Grid item xs={12} md={8}>
                    <Alert severity="success" sx={{ mb: 2 }}>
                      <Typography variant="subtitle2">Net Annual Income</Typography>
                      <Typography variant="h4">${benefitsResults.summary.net_annual_income.toLocaleString()}</Typography>
                      <Typography variant="body2">
                        ${benefitsResults.summary.net_monthly_income.toLocaleString()}/month
                        &nbsp;•&nbsp;
                        ${benefitsResults.summary.effective_hourly_rate}/hour (after taxes & benefits)
                      </Typography>
                    </Alert>

                    <Grid container spacing={2} sx={{ mb: 2 }}>
                      <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="h6" gutterBottom color="primary">Health Insurance</Typography>
                          <Typography variant="body2">Monthly Premium: ${benefitsResults.health_insurance.monthly_premium}</Typography>
                          <Typography variant="body2">Annual Premium: ${benefitsResults.health_insurance.annual_premium.toLocaleString()}</Typography>
                          <Typography variant="body2">Deductible: ${benefitsResults.health_insurance.deductible.toLocaleString()}</Typography>
                          <Typography variant="body2">Est. Out-of-Pocket: ${benefitsResults.health_insurance.estimated_out_of_pocket.toLocaleString()}</Typography>
                          <Divider sx={{ my: 1 }} />
                          <Typography variant="body1" fontWeight="bold">
                            Total Annual: ${benefitsResults.health_insurance.total_annual_cost.toLocaleString()}
                          </Typography>
                          {benefitsResults.health_insurance.subsidy_eligible && (
                            <Chip label="ACA Subsidy Eligible" color="success" size="small" sx={{ mt: 1 }} />
                          )}
                        </Paper>
                      </Grid>

                      <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="h6" gutterBottom color="primary">Retirement</Typography>
                          <Typography variant="body2">Contribution: {benefitsResults.retirement.contribution_pct}%</Typography>
                          <Typography variant="body2">Monthly: ${benefitsResults.retirement.monthly_contribution.toLocaleString()}</Typography>
                          <Typography variant="body2">Annual: ${benefitsResults.retirement.annual_contribution.toLocaleString()}</Typography>
                          <Typography variant="body2">Account: {benefitsResults.retirement.account_type}</Typography>
                          <Divider sx={{ my: 1 }} />
                          <Typography variant="body1" fontWeight="bold" color="success.main">
                            Tax Benefit: ${benefitsResults.retirement.tax_benefit.toLocaleString()}
                          </Typography>
                        </Paper>
                      </Grid>

                      <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="h6" gutterBottom color="primary">Taxes</Typography>
                          <Typography variant="body2">Federal: ${benefitsResults.taxes.federal_income_tax.toLocaleString()}</Typography>
                          <Typography variant="body2">State: ${benefitsResults.taxes.state_income_tax.toLocaleString()}</Typography>
                          <Typography variant="body2">Self-Employment: ${benefitsResults.taxes.self_employment_tax.toLocaleString()}</Typography>
                          <Divider sx={{ my: 1 }} />
                          <Typography variant="body1" fontWeight="bold">
                            Total Taxes: ${benefitsResults.taxes.total_tax.toLocaleString()}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Effective Rate: {benefitsResults.taxes.effective_tax_rate_pct}%
                          </Typography>
                          <Alert severity="warning" sx={{ mt: 1 }}>
                            Quarterly Payment: ${benefitsResults.taxes.quarterly_payment_estimate.toLocaleString()}
                          </Alert>
                        </Paper>
                      </Grid>

                      <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="h6" gutterBottom color="primary">Other Insurance</Typography>
                          <Typography variant="body2">
                            Disability: ${benefitsResults.insurance.disability_insurance_monthly}/month
                          </Typography>
                          <Typography variant="body2">
                            Life: ${benefitsResults.insurance.life_insurance_monthly}/month
                          </Typography>
                          <Divider sx={{ my: 1 }} />
                          <Typography variant="body1" fontWeight="bold">
                            Total Annual: ${(benefitsResults.insurance.disability_insurance_annual + benefitsResults.insurance.life_insurance_annual).toLocaleString()}
                          </Typography>
                        </Paper>
                      </Grid>
                    </Grid>

                    <Paper sx={{ p: 2, bgcolor: 'info.light' }}>
                      <Typography variant="h6" gutterBottom>W2 Equivalent</Typography>
                      <Typography variant="body2">{benefitsResults.w2_comparison.explanation}</Typography>
                    </Paper>

                    <Box sx={{ mt: 2 }}>
                      <Typography variant="h6" gutterBottom>Recommendations:</Typography>
                      <List dense>
                        {benefitsResults.recommendations.map((rec, idx) => (
                          <ListItem key={idx}>
                            <ListItemIcon>
                              <Info color="primary" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText primary={rec} />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  </Grid>
                )}
              </Grid>
            </Box>
          )}

          {/* Tab 4: Dashboard */}
          {activeTab === 3 && dashboard && (
            <Box>
              <Typography variant="h5" gutterBottom>Your Gig Economy Dashboard</Typography>

              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant="h6" gutterBottom>Income Streams</Typography>
                    <TableContainer>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Source</TableCell>
                            <TableCell align="right">Monthly</TableCell>
                            <TableCell>Volatility</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {dashboard.income_streams.map((stream, idx) => (
                            <TableRow key={idx}>
                              <TableCell>{stream.source}</TableCell>
                              <TableCell align="right">${stream.monthly.toLocaleString()}</TableCell>
                              <TableCell>
                                <Chip
                                  label={stream.volatility}
                                  size="small"
                                  color={stream.volatility === 'low' ? 'success' : stream.volatility === 'medium' ? 'warning' : 'error'}
                                />
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </Paper>

                  <Paper sx={{ p: 2 }}>
                    <Typography variant="h6" gutterBottom>Stability Metrics</Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2">Diversification Score</Typography>
                      <LinearProgress
                        variant="determinate"
                        value={dashboard.stability_metrics.diversification_score}
                        sx={{ height: 8, borderRadius: 4, mb: 1 }}
                      />
                      <Typography variant="caption">{dashboard.stability_metrics.diversification_score}/100</Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2">Income Stability Score</Typography>
                      <LinearProgress
                        variant="determinate"
                        value={dashboard.stability_metrics.income_stability_score}
                        color="success"
                        sx={{ height: 8, borderRadius: 4, mb: 1 }}
                      />
                      <Typography variant="caption">{dashboard.stability_metrics.income_stability_score}/100</Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2">Burnout Risk</Typography>
                      <Chip label={dashboard.stability_metrics.burnout_risk} color={getRiskColor(dashboard.stability_metrics.burnout_risk)} />
                    </Box>
                  </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant="h6" gutterBottom>Quick Actions</Typography>
                    <List>
                      {dashboard.quick_actions.map((action, idx) => (
                        <ListItem key={idx}>
                          <ListItemIcon>
                            <CheckCircle color="primary" />
                          </ListItemIcon>
                          <ListItemText primary={action} />
                        </ListItem>
                      ))}
                    </List>
                  </Paper>

                  <Paper sx={{ p: 2 }}>
                    <Typography variant="h6" gutterBottom>Next Steps</Typography>
                    <List>
                      {dashboard.next_steps.map((step, idx) => (
                        <ListItem key={idx}>
                          <ListItemIcon>
                            <TrendingUp color="success" />
                          </ListItemIcon>
                          <ListItemText primary={step} />
                        </ListItem>
                      ))}
                    </List>
                  </Paper>
                </Grid>
              </Grid>
            </Box>
          )}
        </Box>
      </Paper>

      {/* Gig vs W2 Comparison Dialog */}
      <Dialog open={comparisonOpen} onClose={() => setComparisonOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Gig Work vs W2 Employment Comparison</DialogTitle>
        <DialogContent>
          {comparisonResults && (
            <Box>
              <Grid container spacing={2} sx={{ mb: 2 }}>
                <Grid item xs={6}>
                  <Paper sx={{ p: 2, bgcolor: 'primary.light' }}>
                    <Typography variant="h6" gutterBottom>Gig Work</Typography>
                    <Typography variant="body2">Gross: ${comparisonResults.gig_work.gross_income.toLocaleString()}</Typography>
                    <Typography variant="body2">Taxes: ${comparisonResults.gig_work.total_taxes.toLocaleString()}</Typography>
                    <Typography variant="body2">Benefits: ${comparisonResults.gig_work.benefits_cost.toLocaleString()}</Typography>
                    <Divider sx={{ my: 1 }} />
                    <Typography variant="h5">Net: ${comparisonResults.gig_work.net_income.toLocaleString()}</Typography>
                    <Typography variant="body2">${comparisonResults.gig_work.effective_hourly_rate}/hr</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6}>
                  <Paper sx={{ p: 2, bgcolor: 'success.light' }}>
                    <Typography variant="h6" gutterBottom>W2 Employment</Typography>
                    <Typography variant="body2">Salary: ${comparisonResults.w2_employment.salary.toLocaleString()}</Typography>
                    <Typography variant="body2">Employer Benefits: ${comparisonResults.w2_employment.employer_benefits_value.toLocaleString()}</Typography>
                    <Typography variant="body2">Taxes: ${comparisonResults.w2_employment.total_taxes.toLocaleString()}</Typography>
                    <Divider sx={{ my: 1 }} />
                    <Typography variant="h5">Net: ${comparisonResults.w2_employment.net_income.toLocaleString()}</Typography>
                    <Typography variant="body2">${comparisonResults.w2_employment.effective_hourly_rate}/hr</Typography>
                  </Paper>
                </Grid>
              </Grid>

              <Alert severity={comparisonResults.comparison.net_income_difference > 0 ? 'success' : 'info'} sx={{ mb: 2 }}>
                <Typography variant="subtitle2">{comparisonResults.comparison.recommendation}</Typography>
                <Typography variant="body2">
                  Net Income Difference: ${Math.abs(comparisonResults.comparison.net_income_difference).toLocaleString()}
                  &nbsp;({comparisonResults.comparison.gig_premium_required_pct > 0 ? '+' : ''}{comparisonResults.comparison.gig_premium_required_pct}%)
                </Typography>
              </Alert>

              <Typography variant="body2">{comparisonResults.comparison.analysis}</Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <TextField
            type="number"
            label="W2 Salary for Comparison"
            value={w2Salary}
            onChange={(e) => setW2Salary(parseFloat(e.target.value))}
            size="small"
            sx={{ mr: 2 }}
          />
          <Button onClick={compareGigVsW2}>Recalculate</Button>
          <Button onClick={() => setComparisonOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default GigEconomyHub;
