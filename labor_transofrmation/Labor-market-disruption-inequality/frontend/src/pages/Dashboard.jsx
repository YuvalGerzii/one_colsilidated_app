/**
 * Main Dashboard Page
 * Overview of all platform metrics and quick access to features
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  Button,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  IconButton,
  Tab,
  Tabs,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  School,
  WorkOutline,
  AttachMoney,
  Assessment,
  Notifications,
  ArrowForward,
  Psychology,
  EmojiEvents,
  LocalFireDepartment,
} from '@mui/icons-material';
import MetricCard from '../components/Dashboard/MetricCard';
import { progressAPI, studyBuddyAPI, digitalTwinAPI, gigAPI } from '../services/api';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const userId = 1; // Get from auth context

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [progress, studyBuddy, digitalTwin] = await Promise.all([
        progressAPI.getDashboard(userId),
        studyBuddyAPI.getLearningDashboard(userId),
        digitalTwinAPI.getMacroRiskIndex(),
      ]);

      setDashboardData({
        progress,
        studyBuddy,
        digitalTwin,
      });
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 4 }}>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Welcome back, Sarah! 👋
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here's what's happening with your career transition journey
        </Typography>
      </Box>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Automation Risk"
            value="42"
            unit="%"
            trend="down"
            trendValue={-8}
            icon={Assessment}
            color="success"
            subtitle="Lower is better - Great progress!"
            sparklineData={[45, 48, 46, 44, 43, 42]}
          />
        </Grid>

        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Skills Mastered"
            value="12"
            trend="up"
            trendValue={15}
            icon={School}
            color="primary"
            subtitle="Python, SQL, Machine Learning, +"
            sparklineData={[8, 9, 10, 11, 11, 12]}
          />
        </Grid>

        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Learning Streak"
            value="23"
            unit="days"
            trend="up"
            trendValue={12}
            icon={LocalFireDepartment}
            color="warning"
            subtitle="Keep it up! 7 more for milestone"
          />
        </Grid>

        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Credits Earned"
            value="$1,250"
            trend="up"
            trendValue={28}
            icon={AttachMoney}
            color="success"
            subtitle="From Study Buddy contributions"
            sparklineData={[850, 920, 1050, 1120, 1180, 1250]}
          />
        </Grid>
      </Grid>

      {/* Main Content Grid */}
      <Grid container spacing={3}>
        {/* Left Column */}
        <Grid item xs={12} lg={8}>
          {/* Active Learning Paths */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h6" fontWeight={600}>
                Active Learning Paths
              </Typography>
              <Button endIcon={<ArrowForward />}>View All</Button>
            </Box>

            <Grid container spacing={2}>
              {[
                {
                  title: 'Python to Data Scientist',
                  progress: 68,
                  color: 'primary',
                  hoursLeft: 45,
                  icon: '🐍',
                },
                {
                  title: 'Machine Learning Fundamentals',
                  progress: 42,
                  color: 'secondary',
                  hoursLeft: 78,
                  icon: '🤖',
                },
                {
                  title: 'Cloud Architecture Basics',
                  progress: 15,
                  color: 'info',
                  hoursLeft: 120,
                  icon: '☁️',
                },
              ].map((path, index) => (
                <Grid item xs={12} md={4} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Avatar sx={{ bgcolor: `${path.color}.50`, color: `${path.color}.main`, mr: 2 }}>
                          {path.icon}
                        </Avatar>
                        <Typography variant="subtitle2" fontWeight={600}>
                          {path.title}
                        </Typography>
                      </Box>

                      <Box sx={{ mb: 1 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                          <Typography variant="caption" color="text.secondary">
                            Progress
                          </Typography>
                          <Typography variant="caption" fontWeight={600}>
                            {path.progress}%
                          </Typography>
                        </Box>
                        <LinearProgress
                          variant="determinate"
                          value={path.progress}
                          sx={{
                            height: 6,
                            borderRadius: 3,
                            bgcolor: `${path.color}.50`,
                            '& .MuiLinearProgress-bar': {
                              bgcolor: `${path.color}.main`,
                            },
                          }}
                        />
                      </Box>

                      <Typography variant="caption" color="text.secondary">
                        ~{path.hoursLeft} hours remaining
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>

          {/* AI Agents Insights */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              AI Agent Insights
            </Typography>

            <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)} sx={{ mb: 2 }}>
              <Tab label="Recommendations" />
              <Tab label="Opportunities" />
              <Tab label="Progress" />
            </Tabs>

            {tabValue === 0 && (
              <List>
                {[
                  {
                    icon: <Psychology color="primary" />,
                    primary: 'Learning Strategist suggests',
                    secondary: 'Focus on SQL optimization next - high market demand in your target role',
                    action: 'Start Learning',
                  },
                  {
                    icon: <TrendingUp color="success" />,
                    primary: 'Career Navigator recommends',
                    secondary: 'Apply for Data Analyst roles now - you meet 85% of requirements',
                    action: 'View Jobs',
                  },
                  {
                    icon: <School color="secondary" />,
                    primary: 'Teaching Coach says',
                    secondary: 'Great progress on ML! Ready for advanced topics in neural networks',
                    action: 'Continue',
                  },
                ].map((item, index) => (
                  <ListItem
                    key={index}
                    secondaryAction={
                      <Button size="small" variant="outlined">
                        {item.action}
                      </Button>
                    }
                    sx={{ mb: 1, bgcolor: 'background.default', borderRadius: 2 }}
                  >
                    <ListItemAvatar>
                      <Avatar>{item.icon}</Avatar>
                    </ListItemAvatar>
                    <ListItemText primary={item.primary} secondary={item.secondary} />
                  </ListItem>
                ))}
              </List>
            )}

            {tabValue === 1 && (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <WorkOutline sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  12 New Opportunities Found
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Including 5 hidden market positions
                </Typography>
                <Button variant="contained">Explore Opportunities</Button>
              </Box>
            )}

            {tabValue === 2 && (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <TrendingUp sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  You're on Track!
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  87% probability of landing target role in 8-12 weeks
                </Typography>
                <Button variant="contained">View Detailed Analysis</Button>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Right Column */}
        <Grid item xs={12} lg={4}>
          {/* Achievements */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" fontWeight={600}>
                Recent Achievements
              </Typography>
              <IconButton size="small">
                <EmojiEvents />
              </IconButton>
            </Box>

            <List>
              {[
                { badge: '🔥', title: '30-Day Streak', desc: 'Unlocked yesterday', color: 'warning' },
                { badge: '⭐', title: 'Python Expert', desc: '95% proficiency', color: 'primary' },
                { badge: '💰', title: 'First $1K Earned', desc: 'Study Buddy milestone', color: 'success' },
              ].map((achievement, index) => (
                <ListItem key={index} sx={{ px: 0 }}>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: `${achievement.color}.50` }}>{achievement.badge}</Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={achievement.title}
                    secondary={achievement.desc}
                    primaryTypographyProps={{ fontWeight: 600 }}
                  />
                </ListItem>
              ))}
            </List>

            <Button fullWidth variant="outlined" sx={{ mt: 2 }}>
              View All Achievements
            </Button>
          </Paper>

          {/* Study Groups */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              Your Study Groups
            </Typography>

            <List sx={{ mt: 2 }}>
              {[
                { name: 'ML Enthusiasts', members: 8, next: 'Tomorrow 7PM' },
                { name: 'Python Mastery', members: 12, next: 'Friday 6PM' },
              ].map((group, index) => (
                <ListItem key={index} sx={{ px: 0, py: 1.5 }}>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: 'primary.main' }}>{group.members}</Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={group.name}
                    secondary={`Next session: ${group.next}`}
                    primaryTypographyProps={{ fontWeight: 600, fontSize: '0.9rem' }}
                    secondaryTypographyProps={{ fontSize: '0.8rem' }}
                  />
                </ListItem>
              ))}
            </List>

            <Button fullWidth variant="text" sx={{ mt: 1 }}>
              Find More Groups
            </Button>
          </Paper>

          {/* Quick Actions */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              Quick Actions
            </Typography>

            <Grid container spacing={1.5} sx={{ mt: 2 }}>
              {[
                { label: 'Chat with AI', icon: <Psychology />, color: 'primary' },
                { label: 'Browse Library', icon: <School />, color: 'secondary' },
                { label: 'Track Progress', icon: <TrendingUp />, color: 'success' },
                { label: 'Find Jobs', icon: <WorkOutline />, color: 'info' },
              ].map((action, index) => (
                <Grid item xs={6} key={index}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={action.icon}
                    sx={{
                      py: 1.5,
                      flexDirection: 'column',
                      '& .MuiButton-startIcon': { m: 0, mb: 0.5 },
                    }}
                  >
                    {action.label}
                  </Button>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
