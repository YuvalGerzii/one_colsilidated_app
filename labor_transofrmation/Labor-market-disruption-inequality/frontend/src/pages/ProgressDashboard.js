import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Card,
  CardContent,
  Alert,
  List,
  ListItem,
  ListItemText,
  Chip,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Badge,
  Avatar,
  IconButton,
  Tabs,
  Tab,
  Divider
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import SchoolIcon from '@mui/icons-material/School';
import WorkIcon from '@mui/icons-material/Work';
import CodeIcon from '@mui/icons-material/Code';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import LocalFireDepartmentIcon from '@mui/icons-material/LocalFireDepartment';
import AddIcon from '@mui/icons-material/Add';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RefreshIcon from '@mui/icons-material/Refresh';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function ProgressDashboard() {
  const [workerId] = useState(1);
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [applications, setApplications] = useState([]);
  const [achievements, setAchievements] = useState(null);
  const [portfolioRecommendations, setPortfolioRecommendations] = useState([]);

  // Dialog states
  const [activityDialog, setActivityDialog] = useState(false);
  const [applicationDialog, setApplicationDialog] = useState(false);
  const [projectDialog, setProjectDialog] = useState(false);

  // Form states
  const [activityForm, setActivityForm] = useState({
    skill: '',
    activity_type: 'course',
    difficulty: 'medium',
    time_spent_minutes: 60
  });
  const [applicationForm, setApplicationForm] = useState({
    company: '',
    position: '',
    location: '',
    remote: false,
    priority: 'medium',
    source: '',
    notes: ''
  });
  const [projectForm, setProjectForm] = useState({
    title: '',
    description: '',
    skills_demonstrated: [],
    github_url: '',
    difficulty: 'intermediate'
  });

  useEffect(() => {
    loadDashboard();
    loadAchievements();
    loadPortfolioRecommendations();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/progress/dashboard/${workerId}`);
      setDashboard(response.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAchievements = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/progress/achievements/${workerId}`);
      setAchievements(response.data);
    } catch (error) {
      console.error('Error loading achievements:', error);
    }
  };

  const loadApplications = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/progress/job-applications/${workerId}`);
      setApplications(response.data.applications);
    } catch (error) {
      console.error('Error loading applications:', error);
    }
  };

  const loadPortfolioRecommendations = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/progress/portfolio-recommendations/${workerId}`);
      setPortfolioRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Error loading recommendations:', error);
    }
  };

  const logActivity = async () => {
    try {
      await axios.post(`${API_BASE_URL}/progress/learning-activity/${workerId}`, activityForm);
      setActivityDialog(false);
      setActivityForm({ skill: '', activity_type: 'course', difficulty: 'medium', time_spent_minutes: 60 });
      loadDashboard();
      loadAchievements();
    } catch (error) {
      console.error('Error logging activity:', error);
    }
  };

  const createApplication = async () => {
    try {
      await axios.post(`${API_BASE_URL}/progress/job-application/${workerId}`, applicationForm);
      setApplicationDialog(false);
      setApplicationForm({ company: '', position: '', location: '', remote: false, priority: 'medium', source: '', notes: '' });
      loadDashboard();
      loadApplications();
    } catch (error) {
      console.error('Error creating application:', error);
    }
  };

  const createProject = async () => {
    try {
      await axios.post(`${API_BASE_URL}/progress/portfolio-project/${workerId}`, projectForm);
      setProjectDialog(false);
      setProjectForm({ title: '', description: '', skills_demonstrated: [], github_url: '', difficulty: 'intermediate' });
      loadDashboard();
    } catch (error) {
      console.error('Error creating project:', error);
    }
  };

  if (!dashboard) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4">Loading Dashboard...</Typography>
        <LinearProgress sx={{ mt: 2 }} />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Progress Dashboard
        </Typography>
        <IconButton onClick={loadDashboard} color="primary">
          <RefreshIcon />
        </IconButton>
      </Box>

      {/* Overall Progress Score */}
      <Paper sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={8}>
            <Typography variant="h3" gutterBottom>
              {dashboard.progress_score}/100
            </Typography>
            <Typography variant="h6">Overall Progress Score</Typography>
            <LinearProgress
              variant="determinate"
              value={dashboard.progress_score}
              sx={{ mt: 2, height: 10, borderRadius: 5, bgcolor: 'rgba(255,255,255,0.3)' }}
            />
            <Box sx={{ mt: 2 }}>
              {achievements && (
                <Chip
                  icon={<EmojiEventsIcon />}
                  label={`Level ${achievements.level} | ${achievements.total_points} XP`}
                  sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', fontWeight: 'bold' }}
                />
              )}
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <LocalFireDepartmentIcon sx={{ fontSize: 80, mr: 2 }} />
              <Box>
                <Typography variant="h2">{dashboard.learning_streak.current}</Typography>
                <Typography variant="body1">Day Streak</Typography>
                <Typography variant="caption">Best: {dashboard.learning_streak.longest}</Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* Quick Stats */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#f3e5f5' }}>
            <CardContent>
              <SchoolIcon sx={{ fontSize: 40, color: '#9c27b0' }} />
              <Typography variant="h4">{dashboard.this_week.activities_completed}</Typography>
              <Typography variant="body2" color="text.secondary">
                Activities This Week
              </Typography>
              <Typography variant="caption">
                {dashboard.this_week.time_spent_hours}h total
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#e3f2fd' }}>
            <CardContent>
              <WorkIcon sx={{ fontSize: 40, color: '#1976d2' }} />
              <Typography variant="h4">{dashboard.job_search.total_applications}</Typography>
              <Typography variant="body2" color="text.secondary">
                Applications Sent
              </Typography>
              <Typography variant="caption">
                {dashboard.this_week.applications_sent} this week
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#e8f5e9' }}>
            <CardContent>
              <CodeIcon sx={{ fontSize: 40, color: '#388e3c' }} />
              <Typography variant="h4">{dashboard.portfolio.total_projects}</Typography>
              <Typography variant="body2" color="text.secondary">
                Portfolio Projects
              </Typography>
              <Typography variant="caption">
                {dashboard.portfolio.completed} completed
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#fff3e0' }}>
            <CardContent>
              <EmojiEventsIcon sx={{ fontSize: 40, color: '#f57c00' }} />
              <Typography variant="h4">{dashboard.achievements.total}</Typography>
              <Typography variant="body2" color="text.secondary">
                Achievements
              </Typography>
              {achievements && (
                <Typography variant="caption">
                  {achievements.total_points} total XP
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recommendations */}
      {dashboard.recommendations && dashboard.recommendations.length > 0 && (
        <Alert severity="info" sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>Recommendations:</Typography>
          {dashboard.recommendations.map((rec, i) => (
            <Typography key={i} variant="body2">• {rec}</Typography>
          ))}
        </Alert>
      )}

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Recent Activity" />
          <Tab label="Job Applications" />
          <Tab label="Portfolio Projects" />
          <Tab label="Achievements" />
        </Tabs>
      </Box>

      {/* Tab Content */}
      {activeTab === 0 && (
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">Recent Learning Activities</Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setActivityDialog(true)}
            >
              Log Activity
            </Button>
          </Box>

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Skill</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Time</TableCell>
                  <TableCell>Score</TableCell>
                  <TableCell>Date</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {dashboard.recent_activities.map((activity) => (
                  <TableRow key={activity.id}>
                    <TableCell>{activity.skill}</TableCell>
                    <TableCell>
                      <Chip label={activity.activity_type} size="small" />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={activity.status}
                        size="small"
                        color={activity.status === 'completed' ? 'success' : 'default'}
                        icon={activity.status === 'completed' ? <CheckCircleIcon /> : null}
                      />
                    </TableCell>
                    <TableCell>{activity.time_spent_minutes} min</TableCell>
                    <TableCell>{activity.score || 'N/A'}</TableCell>
                    <TableCell>{new Date(activity.created_at).toLocaleDateString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}

      {activeTab === 1 && (
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">Job Applications</Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => {
                setApplicationDialog(true);
                loadApplications();
              }}
            >
              Add Application
            </Button>
          </Box>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {dashboard.job_search.by_status && Object.entries(dashboard.job_search.by_status).map(([status, count]) => (
              <Grid item key={status}>
                <Chip label={`${status}: ${count}`} />
              </Grid>
            ))}
          </Grid>

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Company</TableCell>
                  <TableCell>Position</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Priority</TableCell>
                  <TableCell>Applied Date</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {dashboard.job_search.recent_applications.map((app) => (
                  <TableRow key={app.id}>
                    <TableCell>{app.company}</TableCell>
                    <TableCell>{app.position}</TableCell>
                    <TableCell>
                      <Chip label={app.status} size="small" color="primary" />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={app.priority}
                        size="small"
                        color={app.priority === 'high' ? 'error' : app.priority === 'medium' ? 'warning' : 'default'}
                      />
                    </TableCell>
                    <TableCell>{new Date(app.applied_date).toLocaleDateString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}

      {activeTab === 2 && (
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">Portfolio Projects</Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setProjectDialog(true)}
            >
              Add Project
            </Button>
          </Box>

          <Grid container spacing={2}>
            {dashboard.portfolio.projects.map((project) => (
              <Grid item xs={12} md={6} key={project.id}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>{project.title}</Typography>
                    <Chip label={project.status} size="small" color={project.status === 'completed' ? 'success' : 'primary'} sx={{ mb: 1 }} />
                    <Box sx={{ mt: 1 }}>
                      {project.skills?.map((skill, i) => (
                        <Chip key={i} label={skill} size="small" variant="outlined" sx={{ m: 0.5 }} />
                      ))}
                    </Box>
                    {project.github_url && (
                      <Button size="small" href={project.github_url} target="_blank" sx={{ mt: 1 }}>
                        View on GitHub
                      </Button>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          {portfolioRecommendations.length > 0 && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>Recommended Projects</Typography>
              <Grid container spacing={2}>
                {portfolioRecommendations.map((rec, i) => (
                  <Grid item xs={12} md={6} key={i}>
                    <Card sx={{ border: '2px dashed #1976d2' }}>
                      <CardContent>
                        <Typography variant="h6">{rec.title}</Typography>
                        <Typography variant="body2" color="text.secondary" paragraph>
                          {rec.description}
                        </Typography>
                        <Box sx={{ mb: 1 }}>
                          <Chip label={rec.difficulty} size="small" sx={{ mr: 1 }} />
                          <Chip label={`${rec.estimated_hours}h`} size="small" />
                        </Box>
                        <Typography variant="caption" display="block" gutterBottom>
                          Skills: {rec.skills_required?.join(', ')}
                        </Typography>
                        <Typography variant="caption" display="block">
                          Impact Score: {rec.impact_score}/10
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}
        </Box>
      )}

      {activeTab === 3 && achievements && (
        <Box>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6" gutterBottom>Your Progress</Typography>
            <Typography variant="body1">Level {achievements.level}</Typography>
            <LinearProgress
              variant="determinate"
              value={(achievements.total_points % 1000) / 10}
              sx={{ mt: 1, height: 10, borderRadius: 5 }}
            />
            <Typography variant="caption">
              {achievements.total_points} / {achievements.next_level_points} XP to Level {achievements.level + 1}
            </Typography>
          </Paper>

          <Typography variant="h6" gutterBottom>Unlocked Achievements</Typography>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            {achievements.achievements.map((achievement, i) => (
              <Grid item xs={12} sm={6} md={4} key={i}>
                <Card sx={{ bgcolor: '#f5f5f5' }}>
                  <CardContent sx={{ display: 'flex', alignItems: 'center' }}>
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                      <EmojiEventsIcon />
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle1" fontWeight="bold">{achievement.title}</Typography>
                      <Typography variant="body2" color="text.secondary">{achievement.description}</Typography>
                      <Chip label={`+${achievement.points} XP`} size="small" color="primary" sx={{ mt: 1 }} />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Typography variant="h6" gutterBottom>Available Achievements</Typography>
          <Grid container spacing={2}>
            {achievements.available_achievements.map((achievement, i) => (
              <Grid item xs={12} sm={6} md={4} key={i}>
                <Card sx={{ opacity: 0.6, border: '1px dashed #ccc' }}>
                  <CardContent>
                    <Typography variant="subtitle1">{achievement.title}</Typography>
                    <Typography variant="body2" color="text.secondary">{achievement.description}</Typography>
                    <Chip label={`${achievement.points} XP`} size="small" variant="outlined" sx={{ mt: 1 }} />
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Log Activity Dialog */}
      <Dialog open={activityDialog} onClose={() => setActivityDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Log Learning Activity</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Skill"
            value={activityForm.skill}
            onChange={(e) => setActivityForm({ ...activityForm, skill: e.target.value })}
            sx={{ mt: 2, mb: 2 }}
          />
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Activity Type</InputLabel>
            <Select
              value={activityForm.activity_type}
              onChange={(e) => setActivityForm({ ...activityForm, activity_type: e.target.value })}
            >
              <MenuItem value="course">Course</MenuItem>
              <MenuItem value="practice">Practice</MenuItem>
              <MenuItem value="project">Project</MenuItem>
              <MenuItem value="reading">Reading</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Difficulty</InputLabel>
            <Select
              value={activityForm.difficulty}
              onChange={(e) => setActivityForm({ ...activityForm, difficulty: e.target.value })}
            >
              <MenuItem value="easy">Easy</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="hard">Hard</MenuItem>
            </Select>
          </FormControl>
          <TextField
            fullWidth
            type="number"
            label="Time Spent (minutes)"
            value={activityForm.time_spent_minutes}
            onChange={(e) => setActivityForm({ ...activityForm, time_spent_minutes: parseInt(e.target.value) })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setActivityDialog(false)}>Cancel</Button>
          <Button onClick={logActivity} variant="contained">Log Activity</Button>
        </DialogActions>
      </Dialog>

      {/* Add Application Dialog */}
      <Dialog open={applicationDialog} onClose={() => setApplicationDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Track Job Application</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Company"
            value={applicationForm.company}
            onChange={(e) => setApplicationForm({ ...applicationForm, company: e.target.value })}
            sx={{ mt: 2, mb: 2 }}
          />
          <TextField
            fullWidth
            label="Position"
            value={applicationForm.position}
            onChange={(e) => setApplicationForm({ ...applicationForm, position: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Location"
            value={applicationForm.location}
            onChange={(e) => setApplicationForm({ ...applicationForm, location: e.target.value })}
            sx={{ mb: 2 }}
          />
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Priority</InputLabel>
            <Select
              value={applicationForm.priority}
              onChange={(e) => setApplicationForm({ ...applicationForm, priority: e.target.value })}
            >
              <MenuItem value="low">Low</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="high">High</MenuItem>
            </Select>
          </FormControl>
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Notes"
            value={applicationForm.notes}
            onChange={(e) => setApplicationForm({ ...applicationForm, notes: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setApplicationDialog(false)}>Cancel</Button>
          <Button onClick={createApplication} variant="contained">Add Application</Button>
        </DialogActions>
      </Dialog>

      {/* Add Project Dialog */}
      <Dialog open={projectDialog} onClose={() => setProjectDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Portfolio Project</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Project Title"
            value={projectForm.title}
            onChange={(e) => setProjectForm({ ...projectForm, title: e.target.value })}
            sx={{ mt: 2, mb: 2 }}
          />
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Description"
            value={projectForm.description}
            onChange={(e) => setProjectForm({ ...projectForm, description: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Skills (comma separated)"
            placeholder="python, react, machine learning"
            onChange={(e) => setProjectForm({ ...projectForm, skills_demonstrated: e.target.value.split(',').map(s => s.trim()) })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="GitHub URL"
            value={projectForm.github_url}
            onChange={(e) => setProjectForm({ ...projectForm, github_url: e.target.value })}
            sx={{ mb: 2 }}
          />
          <FormControl fullWidth>
            <InputLabel>Difficulty</InputLabel>
            <Select
              value={projectForm.difficulty}
              onChange={(e) => setProjectForm({ ...projectForm, difficulty: e.target.value })}
            >
              <MenuItem value="beginner">Beginner</MenuItem>
              <MenuItem value="intermediate">Intermediate</MenuItem>
              <MenuItem value="advanced">Advanced</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setProjectDialog(false)}>Cancel</Button>
          <Button onClick={createProject} variant="contained">Add Project</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default ProgressDashboard;
