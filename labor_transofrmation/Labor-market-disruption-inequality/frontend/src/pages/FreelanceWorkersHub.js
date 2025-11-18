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
  CircularProgress,
  Rating,
  Avatar,
  Badge,
  IconButton,
  Tooltip,
  CardActions,
  CardHeader
} from '@mui/material';
import {
  Work,
  Star,
  TrendingUp,
  AttachMoney,
  Assignment,
  CheckCircle,
  Assessment,
  School,
  Message,
  Send,
  Edit,
  Visibility,
  ThumbUp,
  EmojiEvents,
  VerifiedUser,
  Speed,
  Timer,
  People,
  PersonAdd,
  Search,
  Add,
  FilterList
} from '@mui/icons-material';
import axios from 'axios';

function FreelanceWorkersHub() {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [freelancerId, setFreelancerId] = useState(1); // Default freelancer ID

  // Dashboard States
  const [dashboard, setDashboard] = useState(null);

  // Profile States
  const [profile, setProfile] = useState(null);
  const [profileOptimization, setProfileOptimization] = useState(null);

  // Job Search States
  const [jobs, setJobs] = useState([]);
  const [jobRecommendations, setJobRecommendations] = useState(null);
  const [searchCategory, setSearchCategory] = useState('');
  const [searchBudgetMin, setSearchBudgetMin] = useState('');
  const [searchBudgetMax, setSearchBudgetMax] = useState('');

  // Proposals States
  const [proposals, setProposals] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [proposalDialog, setProposalDialog] = useState(false);
  const [proposalTemplate, setProposalTemplate] = useState(null);

  // Contracts States
  const [contracts, setContracts] = useState([]);

  // Reviews States
  const [reviews, setReviews] = useState([]);

  // Portfolio States
  const [portfolio, setPortfolio] = useState([]);

  // AI Advisory States
  const [pricingAnalysis, setPricingAnalysis] = useState(null);
  const [competitionAnalysis, setCompetitionAnalysis] = useState(null);
  const [growthStrategy, setGrowthStrategy] = useState(null);

  // Analytics States
  const [marketAnalytics, setMarketAnalytics] = useState(null);

  useEffect(() => {
    loadDashboard();
    loadMarketAnalytics();
  }, []);

  // ==================== API CALLS ====================

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/api/v1/freelance/dashboard/freelancer/${freelancerId}`);
      setDashboard(response.data);
      setProfile(response.data.profile);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadProfile = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/freelance/profile/${freelancerId}`);
      setProfile(response.data);
    } catch (error) {
      console.error('Error loading profile:', error);
    }
  };

  const optimizeProfile = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`http://localhost:8000/api/v1/freelance/profile/${freelancerId}/optimize`);
      setProfileOptimization(response.data.optimization);
    } catch (error) {
      console.error('Error optimizing profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchJobs = async () => {
    try {
      setLoading(true);
      const params = {
        category: searchCategory || undefined,
        budget_min: searchBudgetMin || undefined,
        budget_max: searchBudgetMax || undefined,
        limit: 20
      };
      const response = await axios.get('http://localhost:8000/api/v1/freelance/jobs/search', { params });
      setJobs(response.data.jobs);
    } catch (error) {
      console.error('Error searching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const getJobRecommendations = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`http://localhost:8000/api/v1/freelance/advisor/job-recommendations/${freelancerId}?limit=10`);
      setJobRecommendations(response.data);
    } catch (error) {
      console.error('Error getting recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadProposals = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/freelance/proposals/freelancer/${freelancerId}`);
      setProposals(response.data.proposals);
    } catch (error) {
      console.error('Error loading proposals:', error);
    }
  };

  const generateProposalTemplate = async (jobId) => {
    try {
      setLoading(true);
      const response = await axios.post(`http://localhost:8000/api/v1/freelance/proposals/1/generate-template?freelancer_id=${freelancerId}&job_id=${jobId}`);
      setProposalTemplate(response.data.template);
      setProposalDialog(true);
    } catch (error) {
      console.error('Error generating proposal:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadContracts = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/freelance/contracts/freelancer/${freelancerId}`);
      setContracts(response.data.contracts);
    } catch (error) {
      console.error('Error loading contracts:', error);
    }
  };

  const loadReviews = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/freelance/reviews/freelancer/${freelancerId}`);
      setReviews(response.data.reviews);
    } catch (error) {
      console.error('Error loading reviews:', error);
    }
  };

  const loadPortfolio = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/freelance/portfolio/freelancer/${freelancerId}`);
      setPortfolio(response.data.portfolio);
    } catch (error) {
      console.error('Error loading portfolio:', error);
    }
  };

  const getPricingOptimization = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`http://localhost:8000/api/v1/freelance/advisor/pricing-optimization/${freelancerId}`);
      setPricingAnalysis(response.data.pricing_analysis);
    } catch (error) {
      console.error('Error getting pricing analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  const getGrowthStrategy = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`http://localhost:8000/api/v1/freelance/advisor/growth-strategy/${freelancerId}?annual_income_goal=100000`);
      setGrowthStrategy(response.data.growth_plan);
    } catch (error) {
      console.error('Error getting growth strategy:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadMarketAnalytics = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/freelance/analytics/marketplace');
      setMarketAnalytics(response.data);
    } catch (error) {
      console.error('Error loading market analytics:', error);
    }
  };

  // ==================== RENDER FUNCTIONS ====================

  const renderDashboard = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h4" gutterBottom>
        <Work sx={{ mr: 1, verticalAlign: 'middle' }} />
        Freelance Dashboard
      </Typography>

      {loading && <CircularProgress />}

      {dashboard && (
        <>
          {/* Profile Summary Card */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Grid container spacing={3} alignItems="center">
                <Grid item xs={12} md={3} textAlign="center">
                  <Avatar
                    sx={{ width: 100, height: 100, margin: '0 auto', bgcolor: 'primary.main' }}
                  >
                    {dashboard.profile?.name?.charAt(0) || 'F'}
                  </Avatar>
                  <Typography variant="h6" sx={{ mt: 2 }}>
                    {dashboard.profile?.name || 'Freelancer'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {dashboard.profile?.title || 'Professional'}
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    {dashboard.profile?.badges?.map((badge, idx) => (
                      <Chip
                        key={idx}
                        label={badge.replace('_', ' ')}
                        size="small"
                        color="primary"
                        sx={{ m: 0.5 }}
                        icon={<VerifiedUser />}
                      />
                    ))}
                  </Box>
                </Grid>

                <Grid item xs={12} md={9}>
                  <Grid container spacing={2}>
                    <Grid item xs={6} md={3}>
                      <Box textAlign="center">
                        <Star sx={{ color: 'gold', fontSize: 40 }} />
                        <Typography variant="h5">
                          {dashboard.profile?.rating_average || 0}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Rating
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <Box textAlign="center">
                        <CheckCircle sx={{ color: 'green', fontSize: 40 }} />
                        <Typography variant="h5">
                          {dashboard.profile?.total_jobs_completed || 0}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Jobs Completed
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <Box textAlign="center">
                        <AttachMoney sx={{ color: 'primary.main', fontSize: 40 }} />
                        <Typography variant="h5">
                          ${dashboard.profile?.total_earnings?.toLocaleString() || 0}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Total Earned
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <Box textAlign="center">
                        <TrendingUp sx={{ color: 'success.main', fontSize: 40 }} />
                        <Typography variant="h5">
                          {dashboard.profile?.success_rate || 0}%
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Success Rate
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          {/* Activity Cards */}
          <Grid container spacing={3}>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Active Contracts
                  </Typography>
                  <Typography variant="h4">{dashboard.active_contracts || 0}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Pending Proposals
                  </Typography>
                  <Typography variant="h4">{dashboard.pending_proposals || 0}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    This Month Earnings
                  </Typography>
                  <Typography variant="h4">
                    ${dashboard.this_month_earnings?.toLocaleString() || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Avg Monthly Earnings
                  </Typography>
                  <Typography variant="h4">
                    ${dashboard.average_monthly_earnings?.toLocaleString() || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Notifications */}
          {dashboard.notifications && dashboard.notifications.length > 0 && (
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent Notifications
                </Typography>
                <List>
                  {dashboard.notifications.map((notif, idx) => (
                    <ListItem key={idx}>
                      <ListItemIcon>
                        {notif.type === 'proposal_viewed' ? <Visibility /> : <Work />}
                      </ListItemIcon>
                      <ListItemText
                        primary={notif.message}
                        secondary={notif.time}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </Box>
  );

  const renderProfile = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        <Edit sx={{ mr: 1, verticalAlign: 'middle' }} />
        Profile Management
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Your Profile
              </Typography>
              {profile && (
                <>
                  <TextField
                    fullWidth
                    label="Professional Title"
                    value={profile.title || ''}
                    margin="normal"
                  />
                  <TextField
                    fullWidth
                    label="Bio"
                    value={profile.bio || ''}
                    multiline
                    rows={4}
                    margin="normal"
                  />
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <TextField
                        fullWidth
                        label="Hourly Rate"
                        type="number"
                        value={profile.hourly_rate || ''}
                        margin="normal"
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                    <Grid item xs={6}>
                      <TextField
                        fullWidth
                        label="Hours Available/Week"
                        type="number"
                        value={profile.availability_hours_weekly || ''}
                        margin="normal"
                      />
                    </Grid>
                  </Grid>
                  <Button variant="contained" sx={{ mt: 2 }}>
                    Save Changes
                  </Button>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                AI Profile Optimization
              </Typography>
              <Button
                variant="outlined"
                fullWidth
                onClick={optimizeProfile}
                disabled={loading}
                startIcon={<Assessment />}
              >
                Analyze Profile
              </Button>

              {profileOptimization && (
                <Box sx={{ mt: 2 }}>
                  <Alert severity="info" sx={{ mb: 2 }}>
                    Profile Strength: {profileOptimization.profile_strength_score}%
                  </Alert>
                  <LinearProgress
                    variant="determinate"
                    value={profileOptimization.profile_strength_score}
                    sx={{ mb: 2 }}
                  />
                  <Typography variant="subtitle2" gutterBottom>
                    Priority Actions:
                  </Typography>
                  <List dense>
                    {profileOptimization.priority_actions?.map((action, idx) => (
                      <ListItem key={idx}>
                        <ListItemIcon>
                          <CheckCircle fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={action} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );

  const renderJobSearch = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        <Search sx={{ mr: 1, verticalAlign: 'middle' }} />
        Find Jobs
      </Typography>

      {/* Search Filters */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select
                value={searchCategory}
                onChange={(e) => setSearchCategory(e.target.value)}
                label="Category"
              >
                <MenuItem value="">All Categories</MenuItem>
                <MenuItem value="web_development">Web Development</MenuItem>
                <MenuItem value="mobile_development">Mobile Development</MenuItem>
                <MenuItem value="graphic_design">Graphic Design</MenuItem>
                <MenuItem value="writing">Content Writing</MenuItem>
                <MenuItem value="data_analysis">Data Analysis</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Min Budget"
              type="number"
              value={searchBudgetMin}
              onChange={(e) => setSearchBudgetMin(e.target.value)}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Max Budget"
              type="number"
              value={searchBudgetMax}
              onChange={(e) => setSearchBudgetMax(e.target.value)}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button
              fullWidth
              variant="contained"
              onClick={searchJobs}
              startIcon={<Search />}
            >
              Search Jobs
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* AI Recommendations */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            AI-Powered Recommendations
          </Typography>
          <Button
            variant="outlined"
            onClick={getJobRecommendations}
            disabled={loading}
            startIcon={<Assessment />}
          >
            Get Personalized Recommendations
          </Button>

          {jobRecommendations && (
            <Box sx={{ mt: 3 }}>
              <Alert severity="success" sx={{ mb: 2 }}>
                Found {jobRecommendations.total_opportunities} matching opportunities!
              </Alert>

              {jobRecommendations.strategic_insights?.high_value_opportunities?.length > 0 && (
                <>
                  <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                    🎯 High-Value Opportunities
                  </Typography>
                  <Grid container spacing={2}>
                    {jobRecommendations.strategic_insights.high_value_opportunities.map((job, idx) => (
                      <Grid item xs={12} key={idx}>
                        <Card variant="outlined">
                          <CardContent>
                            <Grid container spacing={2} alignItems="center">
                              <Grid item xs={12} md={8}>
                                <Typography variant="h6">{job.job_title}</Typography>
                                <Typography variant="body2" color="text.secondary">
                                  Estimated Earnings: ${job.estimated_earnings}
                                </Typography>
                                <Chip
                                  label={`${job.recommendation_score}% Match`}
                                  color="success"
                                  size="small"
                                  sx={{ mt: 1 }}
                                />
                                <Chip
                                  label={`${job.competition} Competition`}
                                  size="small"
                                  sx={{ mt: 1, ml: 1 }}
                                />
                              </Grid>
                              <Grid item xs={12} md={4} textAlign="right">
                                <Button
                                  variant="contained"
                                  onClick={() => {
                                    setSelectedJob(job);
                                    generateProposalTemplate(job.job_id);
                                  }}
                                  startIcon={<Send />}
                                >
                                  Submit Proposal
                                </Button>
                              </Grid>
                            </Grid>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                </>
              )}
            </Box>
          )}
        </Box>
      </Card>

      {/* Job Listings */}
      {jobs.length > 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Available Jobs ({jobs.length})
            </Typography>
            {jobs.map((job, idx) => (
              <Card key={idx} variant="outlined" sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6">{job.title}</Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {job.description}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                    <Chip label={`Budget: $${job.budget_max}`} size="small" />
                    <Chip label={`${job.proposals_count} proposals`} size="small" />
                  </Box>
                  <Button variant="outlined" size="small" startIcon={<Send />}>
                    Apply Now
                  </Button>
                </CardContent>
              </Card>
            ))}
          </CardContent>
        </Card>
      )}
    </Box>
  );

  const renderContracts = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        <Assignment sx={{ mr: 1, verticalAlign: 'middle' }} />
        My Contracts
      </Typography>

      <Button variant="contained" onClick={loadContracts} sx={{ mb: 2 }}>
        Load Contracts
      </Button>

      {contracts.length > 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Project</TableCell>
                <TableCell>Client</TableCell>
                <TableCell>Amount</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Progress</TableCell>
                <TableCell>Deadline</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {contracts.map((contract) => (
                <TableRow key={contract.id}>
                  <TableCell>{contract.job_title}</TableCell>
                  <TableCell>{contract.client_name}</TableCell>
                  <TableCell>${contract.total_amount}</TableCell>
                  <TableCell>
                    <Chip
                      label={contract.status}
                      color={contract.status === 'active' ? 'primary' : 'default'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <LinearProgress
                        variant="determinate"
                        value={contract.progress_percentage}
                        sx={{ flexGrow: 1, mr: 1 }}
                      />
                      <Typography variant="body2">
                        {contract.progress_percentage}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{new Date(contract.deadline).toLocaleDateString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );

  const renderAIAdvisor = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        <Assessment sx={{ mr: 1, verticalAlign: 'middle' }} />
        AI Freelance Advisor
      </Typography>

      <Grid container spacing={3}>
        {/* Pricing Optimization */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                💰 Pricing Optimization
              </Typography>
              <Button
                variant="contained"
                fullWidth
                onClick={getPricingOptimization}
                disabled={loading}
              >
                Analyze My Pricing
              </Button>

              {pricingAnalysis && (
                <Box sx={{ mt: 3 }}>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Current Rate
                      </Typography>
                      <Typography variant="h6">
                        ${pricingAnalysis.current_hourly_rate}/hr
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Recommended Rate
                      </Typography>
                      <Typography variant="h6" color="primary">
                        ${pricingAnalysis.recommended_rate}/hr
                      </Typography>
                    </Grid>
                  </Grid>

                  <Alert severity="info" sx={{ mt: 2 }}>
                    {pricingAnalysis.message}
                  </Alert>

                  <Typography variant="subtitle2" sx={{ mt: 2 }}>
                    Potential Monthly Increase: ${pricingAnalysis.potential_monthly_increase}
                  </Typography>

                  <Divider sx={{ my: 2 }} />

                  <Typography variant="subtitle2" gutterBottom>
                    Recommendations:
                  </Typography>
                  <List dense>
                    {pricingAnalysis.recommendations?.map((rec, idx) => (
                      <ListItem key={idx}>
                        <ListItemIcon>
                          <TrendingUp fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={rec} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Growth Strategy */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📈 Growth Strategy
              </Typography>
              <Button
                variant="contained"
                fullWidth
                onClick={getGrowthStrategy}
                disabled={loading}
              >
                Get Growth Plan
              </Button>

              {growthStrategy && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Roadmap Phases
                  </Typography>
                  {growthStrategy.phases?.map((phase, idx) => (
                    <Card key={idx} variant="outlined" sx={{ mb: 2 }}>
                      <CardContent>
                        <Typography variant="subtitle2" color="primary">
                          {phase.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {phase.focus}
                        </Typography>
                        <List dense>
                          {phase.goals?.map((goal, gidx) => (
                            <ListItem key={gidx} sx={{ py: 0 }}>
                              <ListItemIcon sx={{ minWidth: 30 }}>
                                <CheckCircle fontSize="small" color="success" />
                              </ListItemIcon>
                              <ListItemText
                                primary={goal}
                                primaryTypographyProps={{ variant: 'body2' }}
                              />
                            </ListItem>
                          ))}
                        </List>
                      </CardContent>
                    </Card>
                  ))}

                  <Alert severity="success" sx={{ mt: 2 }}>
                    Next Step: {growthStrategy.immediate_actions?.[0]}
                  </Alert>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );

  const renderAnalytics = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        <Assessment sx={{ mr: 1, verticalAlign: 'middle' }} />
        Marketplace Analytics
      </Typography>

      {marketAnalytics && (
        <>
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Total Freelancers
                  </Typography>
                  <Typography variant="h4">
                    {marketAnalytics.total_freelancers?.toLocaleString()}
                  </Typography>
                  <Typography variant="body2" color="success.main">
                    {marketAnalytics.active_freelancers} active
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Open Jobs
                  </Typography>
                  <Typography variant="h4">{marketAnalytics.open_jobs}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Avg Hourly Rate
                  </Typography>
                  <Typography variant="h4">${marketAnalytics.avg_hourly_rate}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Platform Earnings
                  </Typography>
                  <Typography variant="h4">
                    ${(marketAnalytics.total_earnings_platform / 1000000).toFixed(1)}M
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Top Categories
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Category</TableCell>
                          <TableCell align="right">Jobs</TableCell>
                          <TableCell align="right">Avg Rate</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {marketAnalytics.top_categories?.map((cat, idx) => (
                          <TableRow key={idx}>
                            <TableCell>{cat.name}</TableCell>
                            <TableCell align="right">{cat.job_count}</TableCell>
                            <TableCell align="right">${cat.avg_rate}/hr</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Trending Skills
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {marketAnalytics.trending_skills?.map((skill, idx) => (
                      <Chip
                        key={idx}
                        label={skill}
                        color="primary"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </>
      )}
    </Box>
  );

  // ==================== MAIN RENDER ====================

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" gutterBottom>
        <EmojiEvents sx={{ fontSize: 40, mr: 2, verticalAlign: 'middle', color: 'gold' }} />
        Freelance Workers Hub
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        Your complete platform for freelance success - Find jobs, manage contracts, and grow your career
      </Typography>

      <Paper sx={{ mt: 3 }}>
        <Tabs
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab label="Dashboard" icon={<Work />} />
          <Tab label="Profile" icon={<Edit />} />
          <Tab label="Find Jobs" icon={<Search />} />
          <Tab label="Contracts" icon={<Assignment />} />
          <Tab label="AI Advisor" icon={<Assessment />} />
          <Tab label="Analytics" icon={<TrendingUp />} />
        </Tabs>

        {activeTab === 0 && renderDashboard()}
        {activeTab === 1 && renderProfile()}
        {activeTab === 2 && renderJobSearch()}
        {activeTab === 3 && renderContracts()}
        {activeTab === 4 && renderAIAdvisor()}
        {activeTab === 5 && renderAnalytics()}
      </Paper>

      {/* Proposal Dialog */}
      <Dialog
        open={proposalDialog}
        onClose={() => setProposalDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Generate Proposal</DialogTitle>
        <DialogContent>
          {proposalTemplate && (
            <>
              <Alert severity="info" sx={{ mb: 2 }}>
                Estimated: {proposalTemplate.estimated_hours} hours at $
                {proposalTemplate.estimated_cost}
              </Alert>
              <TextField
                fullWidth
                multiline
                rows={12}
                value={proposalTemplate.template}
                label="Proposal Text"
                variant="outlined"
              />
              <Typography variant="subtitle2" sx={{ mt: 2 }}>
                Enhancement Tips:
              </Typography>
              <List dense>
                {proposalTemplate.sections && Object.entries(proposalTemplate.sections).map(([key, value], idx) => (
                  <ListItem key={idx}>
                    <ListItemText
                      primary={key.charAt(0).toUpperCase() + key.slice(1)}
                      secondary={value}
                    />
                  </ListItem>
                ))}
              </List>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setProposalDialog(false)}>Cancel</Button>
          <Button variant="contained" startIcon={<Send />}>
            Submit Proposal
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default FreelanceWorkersHub;
