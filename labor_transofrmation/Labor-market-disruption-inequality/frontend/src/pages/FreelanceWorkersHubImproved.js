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
  Alert,
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
  IconButton,
  Tooltip,
  CardActions,
  Skeleton,
  Fade,
  Zoom,
  Slide,
  Collapse,
  Stack,
  Divider,
  alpha,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Work,
  Star,
  TrendingUp,
  AttachMoney,
  Assignment,
  CheckCircle,
  Assessment,
  Message,
  Send,
  Edit,
  Visibility,
  EmojiEvents,
  VerifiedUser,
  Search,
  Add,
  FilterList,
  Close,
  MoreVert,
  Share,
  Bookmark,
  TrendingDown,
  Schedule,
  LocationOn,
  Business,
  Person,
  Notifications,
  Settings,
  Dashboard as DashboardIcon,
  Description,
  AutoAwesome,
  RocketLaunch,
} from '@mui/icons-material';
import axios from 'axios';

// Custom styled components for modern UI
const GradientCard = ({ children, gradient, ...props }) => {
  const theme = useTheme();

  return (
    <Card
      {...props}
      sx={{
        background: gradient || `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
        color: 'white',
        borderRadius: 3,
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 12px 48px rgba(0,0,0,0.15)',
        },
        ...props.sx,
      }}
    >
      {children}
    </Card>
  );
};

const ModernCard = ({ children, ...props }) => {
  return (
    <Card
      {...props}
      sx={{
        borderRadius: 3,
        boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        border: '1px solid rgba(0,0,0,0.06)',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: '0 8px 32px rgba(0,0,0,0.12)',
        },
        ...props.sx,
      }}
    >
      {children}
    </Card>
  );
};

const StatCard = ({ icon: Icon, title, value, trend, trendUp, gradient, loading }) => {
  return (
    <ModernCard>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box
            sx={{
              width: 48,
              height: 48,
              borderRadius: 2,
              background: gradient || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
            }}
          >
            {Icon && <Icon />}
          </Box>
          {trend && (
            <Chip
              icon={trendUp ? <TrendingUp fontSize="small" /> : <TrendingDown fontSize="small" />}
              label={trend}
              size="small"
              color={trendUp ? 'success' : 'error'}
              sx={{ fontWeight: 600 }}
            />
          )}
        </Box>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {title}
        </Typography>
        {loading ? (
          <Skeleton width="60%" height={40} />
        ) : (
          <Typography variant="h4" fontWeight="bold">
            {value}
          </Typography>
        )}
      </CardContent>
    </ModernCard>
  );
};

const JobCard = ({ job, onApply, loading }) => {
  const [expanded, setExpanded] = useState(false);
  const [bookmarked, setBookmarked] = useState(false);

  return (
    <Zoom in timeout={300}>
      <ModernCard sx={{ mb: 2 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
            <Box flex={1}>
              <Typography variant="h6" fontWeight="600" gutterBottom>
                {job.title}
              </Typography>
              <Stack direction="row" spacing={1} mb={1} flexWrap="wrap">
                <Chip
                  icon={<AttachMoney fontSize="small" />}
                  label={`$${job.budget_min}-$${job.budget_max}`}
                  size="small"
                  color="success"
                  variant="outlined"
                />
                <Chip
                  icon={<Person fontSize="small" />}
                  label={`${job.proposals_count} proposals`}
                  size="small"
                  variant="outlined"
                />
                <Chip
                  icon={<Schedule fontSize="small" />}
                  label={job.duration_estimate || 'Flexible'}
                  size="small"
                  variant="outlined"
                />
              </Stack>
            </Box>
            <Box>
              <IconButton size="small" onClick={() => setBookmarked(!bookmarked)}>
                <Bookmark color={bookmarked ? 'primary' : 'inherit'} />
              </IconButton>
              <IconButton size="small">
                <Share fontSize="small" />
              </IconButton>
            </Box>
          </Box>

          <Collapse in={expanded} timeout={300}>
            <Typography variant="body2" color="text.secondary" paragraph>
              {job.description}
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Box mb={2}>
              <Typography variant="subtitle2" gutterBottom>
                Required Skills:
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap">
                {job.required_skills?.map((skill, idx) => (
                  <Chip key={idx} label={skill} size="small" sx={{ mb: 1 }} />
                ))}
              </Stack>
            </Box>
          </Collapse>

          <Box display="flex" gap={1} justifyContent="space-between" alignItems="center">
            <Button
              size="small"
              onClick={() => setExpanded(!expanded)}
              startIcon={expanded ? <Close /> : <Visibility />}
            >
              {expanded ? 'Show Less' : 'View Details'}
            </Button>
            <Button
              variant="contained"
              size="small"
              startIcon={<Send />}
              onClick={() => onApply(job)}
              disabled={loading}
              sx={{
                borderRadius: 2,
                textTransform: 'none',
                fontWeight: 600,
              }}
            >
              Apply Now
            </Button>
          </Box>
        </CardContent>
      </ModernCard>
    </Zoom>
  );
};

const LoadingSkeleton = () => (
  <Box>
    <Skeleton variant="rectangular" height={200} sx={{ borderRadius: 3, mb: 2 }} />
    <Grid container spacing={2}>
      {[1, 2, 3, 4].map((i) => (
        <Grid item xs={12} sm={6} md={3} key={i}>
          <Skeleton variant="rectangular" height={120} sx={{ borderRadius: 3 }} />
        </Grid>
      ))}
    </Grid>
  </Box>
);

const EmptyState = ({ icon: Icon, title, description, action }) => (
  <Box
    sx={{
      textAlign: 'center',
      py: 8,
      px: 3,
    }}
  >
    <Box
      sx={{
        width: 80,
        height: 80,
        borderRadius: '50%',
        background: (theme) => alpha(theme.palette.primary.main, 0.1),
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        margin: '0 auto 16px',
      }}
    >
      {Icon && <Icon sx={{ fontSize: 40, color: 'primary.main' }} />}
    </Box>
    <Typography variant="h6" gutterBottom fontWeight="600">
      {title}
    </Typography>
    <Typography variant="body2" color="text.secondary" paragraph>
      {description}
    </Typography>
    {action}
  </Box>
);

function FreelanceWorkersHubImproved() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [freelancerId, setFreelancerId] = useState(1);

  // Dashboard States
  const [dashboard, setDashboard] = useState(null);
  const [profile, setProfile] = useState(null);

  // Job Search States
  const [jobs, setJobs] = useState([]);
  const [searchFilters, setSearchFilters] = useState({
    category: '',
    budgetMin: '',
    budgetMax: '',
    experienceLevel: '',
  });

  // Dialog States
  const [proposalDialog, setProposalDialog] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);

  useEffect(() => {
    loadDashboard();
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

  const searchJobs = async () => {
    try {
      setLoading(true);
      const params = {
        category: searchFilters.category || undefined,
        budget_min: searchFilters.budgetMin || undefined,
        budget_max: searchFilters.budgetMax || undefined,
        experience_level: searchFilters.experienceLevel || undefined,
        page: 1,
        page_size: 20,
      };
      const response = await axios.get('http://localhost:8000/api/v1/freelance/jobs/search', { params });
      setJobs(response.data.jobs || response.data.items || []);
    } catch (error) {
      console.error('Error searching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyJob = (job) => {
    setSelectedJob(job);
    setProposalDialog(true);
  };

  // ==================== RENDER FUNCTIONS ====================

  const renderDashboard = () => (
    <Fade in timeout={500}>
      <Box>
        {/* Hero Profile Card */}
        <GradientCard
          gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
          sx={{ mb: 3 }}
        >
          <CardContent sx={{ p: 4 }}>
            <Grid container spacing={3} alignItems="center">
              <Grid item xs={12} md={4}>
                <Box display="flex" flexDirection={isMobile ? 'row' : 'column'} alignItems={isMobile ? 'center' : 'flex-start'} gap={2}>
                  <Avatar
                    sx={{
                      width: isMobile ? 64 : 100,
                      height: isMobile ? 64 : 100,
                      bgcolor: 'rgba(255,255,255,0.2)',
                      border: '4px solid rgba(255,255,255,0.3)',
                    }}
                  >
                    {profile?.name?.charAt(0) || 'F'}
                  </Avatar>
                  <Box>
                    <Typography variant="h5" fontWeight="700" gutterBottom>
                      {profile?.name || 'Freelancer'}
                    </Typography>
                    <Typography variant="body1" sx={{ opacity: 0.9, mb: 1 }}>
                      {profile?.title || 'Professional'}
                    </Typography>
                    <Stack direction="row" spacing={1} flexWrap="wrap">
                      {profile?.badges?.map((badge, idx) => (
                        <Chip
                          key={idx}
                          label={badge.replace('_', ' ')}
                          size="small"
                          icon={<VerifiedUser fontSize="small" />}
                          sx={{
                            bgcolor: 'rgba(255,255,255,0.2)',
                            color: 'white',
                            backdropFilter: 'blur(10px)',
                            border: '1px solid rgba(255,255,255,0.3)',
                          }}
                        />
                      ))}
                    </Stack>
                  </Box>
                </Box>
              </Grid>

              <Grid item xs={12} md={8}>
                <Grid container spacing={3}>
                  <Grid item xs={6} sm={3}>
                    <Box textAlign="center">
                      <Typography variant="h4" fontWeight="700">
                        {profile?.rating_average?.toFixed(1) || '0.0'}
                      </Typography>
                      <Box display="flex" justifyContent="center" my={0.5}>
                        <Rating value={profile?.rating_average || 0} readOnly size="small" />
                      </Box>
                      <Typography variant="caption" sx={{ opacity: 0.8 }}>
                        Rating
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Box textAlign="center">
                      <Typography variant="h4" fontWeight="700">
                        {profile?.total_jobs_completed || 0}
                      </Typography>
                      <Typography variant="caption" sx={{ opacity: 0.8 }}>
                        Jobs Done
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Box textAlign="center">
                      <Typography variant="h4" fontWeight="700">
                        ${(profile?.total_earnings || 0).toLocaleString()}
                      </Typography>
                      <Typography variant="caption" sx={{ opacity: 0.8 }}>
                        Earned
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Box textAlign="center">
                      <Typography variant="h4" fontWeight="700">
                        {profile?.success_rate || 0}%
                      </Typography>
                      <Typography variant="caption" sx={{ opacity: 0.8 }}>
                        Success
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </CardContent>
        </GradientCard>

        {/* Stats Grid */}
        {loading ? (
          <LoadingSkeleton />
        ) : (
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                icon={Work}
                title="Active Contracts"
                value={dashboard?.active_contracts || 0}
                trend="+2 this week"
                trendUp={true}
                gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                loading={loading}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                icon={Assignment}
                title="Pending Proposals"
                value={dashboard?.pending_proposals || 0}
                trend="3 viewed"
                trendUp={true}
                gradient="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
                loading={loading}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                icon={AttachMoney}
                title="This Month"
                value={`$${(dashboard?.this_month_earnings || 0).toLocaleString()}`}
                trend="+12%"
                trendUp={true}
                gradient="linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
                loading={loading}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                icon={TrendingUp}
                title="Avg Monthly"
                value={`$${(dashboard?.average_monthly_earnings || 0).toLocaleString()}`}
                gradient="linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
                loading={loading}
              />
            </Grid>
          </Grid>
        )}

        {/* Quick Actions */}
        <ModernCard sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" fontWeight="600" gutterBottom>
              Quick Actions
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6} sm={3}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Search />}
                  onClick={() => setActiveTab(1)}
                  sx={{ py: 1.5, borderRadius: 2 }}
                >
                  Find Jobs
                </Button>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Edit />}
                  onClick={() => setActiveTab(2)}
                  sx={{ py: 1.5, borderRadius: 2 }}
                >
                  Edit Profile
                </Button>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Assessment />}
                  onClick={() => setActiveTab(5)}
                  sx={{ py: 1.5, borderRadius: 2 }}
                >
                  Analytics
                </Button>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<Message />}
                  sx={{ py: 1.5, borderRadius: 2 }}
                >
                  Messages
                </Button>
              </Grid>
            </Grid>
          </CardContent>
        </ModernCard>

        {/* Recent Notifications */}
        {dashboard?.notifications && dashboard.notifications.length > 0 && (
          <Slide in direction="up" timeout={500}>
            <ModernCard>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="h6" fontWeight="600">
                    Recent Activity
                  </Typography>
                  <IconButton size="small">
                    <MoreVert />
                  </IconButton>
                </Box>
                <List>
                  {dashboard.notifications.map((notif, idx) => (
                    <ListItem
                      key={idx}
                      sx={{
                        borderRadius: 2,
                        mb: 1,
                        bgcolor: alpha(theme.palette.primary.main, 0.04),
                        '&:hover': {
                          bgcolor: alpha(theme.palette.primary.main, 0.08),
                        },
                      }}
                    >
                      <ListItemIcon>
                        <Box
                          sx={{
                            width: 40,
                            height: 40,
                            borderRadius: '50%',
                            bgcolor: 'primary.main',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'white',
                          }}
                        >
                          {notif.type === 'proposal_viewed' ? <Visibility fontSize="small" /> : <Work fontSize="small" />}
                        </Box>
                      </ListItemIcon>
                      <ListItemText
                        primary={notif.message}
                        secondary={notif.time}
                        primaryTypographyProps={{ fontWeight: 500 }}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </ModernCard>
          </Slide>
        )}
      </Box>
    </Fade>
  );

  const renderJobSearch = () => (
    <Fade in timeout={500}>
      <Box>
        {/* Search Header */}
        <Box mb={4}>
          <Typography variant="h4" fontWeight="700" gutterBottom>
            Find Your Next Opportunity
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Browse thousands of freelance jobs or get AI-powered recommendations
          </Typography>
        </Box>

        {/* Search Filters */}
        <ModernCard sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel>Category</InputLabel>
                  <Select
                    value={searchFilters.category}
                    onChange={(e) => setSearchFilters({ ...searchFilters, category: e.target.value })}
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
              <Grid item xs={12} sm={6} md={2}>
                <TextField
                  fullWidth
                  size="small"
                  label="Min Budget"
                  type="number"
                  value={searchFilters.budgetMin}
                  onChange={(e) => setSearchFilters({ ...searchFilters, budgetMin: e.target.value })}
                  InputProps={{ startAdornment: '$' }}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={2}>
                <TextField
                  fullWidth
                  size="small"
                  label="Max Budget"
                  type="number"
                  value={searchFilters.budgetMax}
                  onChange={(e) => setSearchFilters({ ...searchFilters, budgetMax: e.target.value })}
                  InputProps={{ startAdornment: '$' }}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel>Experience Level</InputLabel>
                  <Select
                    value={searchFilters.experienceLevel}
                    onChange={(e) => setSearchFilters({ ...searchFilters, experienceLevel: e.target.value })}
                    label="Experience Level"
                  >
                    <MenuItem value="">All Levels</MenuItem>
                    <MenuItem value="beginner">Beginner</MenuItem>
                    <MenuItem value="intermediate">Intermediate</MenuItem>
                    <MenuItem value="expert">Expert</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={2}>
                <Button
                  fullWidth
                  variant="contained"
                  onClick={searchJobs}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <Search />}
                  sx={{ borderRadius: 2, py: 1 }}
                >
                  Search
                </Button>
              </Grid>
            </Grid>
          </CardContent>
        </ModernCard>

        {/* AI Recommendations Banner */}
        <GradientCard
          gradient="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
          sx={{ mb: 3 }}
        >
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={8}>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <AutoAwesome />
                  <Typography variant="h6" fontWeight="600">
                    AI-Powered Job Matching
                  </Typography>
                </Box>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  Get personalized job recommendations based on your skills, experience, and preferences
                </Typography>
              </Grid>
              <Grid item xs={12} md={4} textAlign={isMobile ? 'left' : 'right'}>
                <Button
                  variant="contained"
                  startIcon={<RocketLaunch />}
                  sx={{
                    bgcolor: 'white',
                    color: 'primary.main',
                    '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' },
                    borderRadius: 2,
                    px: 3,
                  }}
                >
                  Get Recommendations
                </Button>
              </Grid>
            </Grid>
          </CardContent>
        </GradientCard>

        {/* Job Listings */}
        {loading ? (
          <Box>
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} variant="rectangular" height={150} sx={{ borderRadius: 3, mb: 2 }} />
            ))}
          </Box>
        ) : jobs.length > 0 ? (
          <Box>
            <Typography variant="h6" fontWeight="600" gutterBottom>
              {jobs.length} Jobs Found
            </Typography>
            {jobs.map((job, idx) => (
              <JobCard key={idx} job={job} onApply={handleApplyJob} loading={loading} />
            ))}
          </Box>
        ) : (
          <EmptyState
            icon={Search}
            title="No jobs found"
            description="Try adjusting your search filters or browse all available jobs"
            action={
              <Button
                variant="contained"
                onClick={() => {
                  setSearchFilters({ category: '', budgetMin: '', budgetMax: '', experienceLevel: '' });
                  searchJobs();
                }}
                sx={{ mt: 2, borderRadius: 2 }}
              >
                Browse All Jobs
              </Button>
            }
          />
        )}
      </Box>
    </Fade>
  );

  // ==================== MAIN RENDER ====================

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(180deg, ${alpha(theme.palette.primary.main, 0.02)} 0%, ${alpha(theme.palette.background.default, 1)} 100%)`,
        pb: 4,
      }}
    >
      <Container maxWidth="xl">
        {/* Header */}
        <Box py={3} display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography variant="h4" fontWeight="700" gutterBottom>
              Freelance Hub
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage your freelance career in one place
            </Typography>
          </Box>
          <Box display="flex" gap={1}>
            <IconButton>
              <Notifications />
            </IconButton>
            <IconButton>
              <Settings />
            </IconButton>
          </Box>
        </Box>

        {/* Navigation Tabs */}
        <Paper
          sx={{
            borderRadius: 3,
            mb: 3,
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          }}
        >
          <Tabs
            value={activeTab}
            onChange={(e, newValue) => setActiveTab(newValue)}
            variant={isMobile ? 'scrollable' : 'fullWidth'}
            scrollButtons={isMobile ? 'auto' : false}
            sx={{
              '& .MuiTab-root': {
                textTransform: 'none',
                fontWeight: 600,
                fontSize: '0.95rem',
                py: 2,
              },
            }}
          >
            <Tab icon={<DashboardIcon />} label="Dashboard" iconPosition="start" />
            <Tab icon={<Search />} label="Find Jobs" iconPosition="start" />
            <Tab icon={<Person />} label="Profile" iconPosition="start" />
            <Tab icon={<Assignment />} label="Proposals" iconPosition="start" />
            <Tab icon={<Description />} label="Contracts" iconPosition="start" />
            <Tab icon={<Assessment />} label="Analytics" iconPosition="start" />
          </Tabs>
        </Paper>

        {/* Tab Content */}
        <Box>
          {activeTab === 0 && renderDashboard()}
          {activeTab === 1 && renderJobSearch()}
          {activeTab === 2 && (
            <EmptyState
              icon={Person}
              title="Profile Management"
              description="Edit your profile, add skills, and showcase your portfolio"
            />
          )}
          {activeTab === 3 && (
            <EmptyState
              icon={Assignment}
              title="Proposals"
              description="View and manage your submitted proposals"
            />
          )}
          {activeTab === 4 && (
            <EmptyState
              icon={Description}
              title="Contracts"
              description="Track your active and completed contracts"
            />
          )}
          {activeTab === 5 && (
            <EmptyState
              icon={Assessment}
              title="Analytics"
              description="View detailed insights about your freelance career"
            />
          )}
        </Box>

        {/* Proposal Dialog */}
        <Dialog
          open={proposalDialog}
          onClose={() => setProposalDialog(false)}
          maxWidth="md"
          fullWidth
          PaperProps={{
            sx: { borderRadius: 3 },
          }}
        >
          <DialogTitle>
            <Typography variant="h6" fontWeight="600">
              Submit Proposal
            </Typography>
          </DialogTitle>
          <DialogContent dividers>
            {selectedJob && (
              <Box>
                <Typography variant="subtitle1" fontWeight="600" gutterBottom>
                  {selectedJob.title}
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  label="Cover Letter"
                  placeholder="Explain why you're the perfect fit for this project..."
                  sx={{ mt: 2 }}
                />
                <Grid container spacing={2} sx={{ mt: 1 }}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Your Rate"
                      type="number"
                      InputProps={{ startAdornment: '$' }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Delivery Time"
                      placeholder="e.g., 5 days"
                    />
                  </Grid>
                </Grid>
              </Box>
            )}
          </DialogContent>
          <DialogActions sx={{ p: 2.5 }}>
            <Button onClick={() => setProposalDialog(false)} sx={{ borderRadius: 2 }}>
              Cancel
            </Button>
            <Button variant="contained" startIcon={<Send />} sx={{ borderRadius: 2, px: 3 }}>
              Submit Proposal
            </Button>
          </DialogActions>
        </Dialog>
      </Container>
    </Box>
  );
}

export default FreelanceWorkersHubImproved;
