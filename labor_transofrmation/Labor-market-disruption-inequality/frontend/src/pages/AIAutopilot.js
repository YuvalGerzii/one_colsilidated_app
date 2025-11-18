import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Card,
  CardContent,
  Stepper,
  Step,
  StepLabel,
  LinearProgress,
  Chip,
  Alert,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function AIAutopilot() {
  const [workerId] = useState(1);
  const [prp, setPrp] = useState(null);
  const [todaysLesson, setTodaysLesson] = useState(null);
  const [loading, setLoading] = useState(false);

  const generatePRP = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/autopilot/personal-reskilling-plan`, {
        worker_id: workerId,
        target_role_id: 1,
        hours_per_week: 10,
        max_budget: 5000
      });
      setPrp(response.data);
    } catch (error) {
      console.error('Error generating PRP:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTodaysLesson = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/autopilot/todays-lesson/${workerId}`);
      setTodaysLesson(response.data);
    } catch (error) {
      console.error('Error loading lesson:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        AI Reskilling Autopilot
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Your personalized, adaptive learning journey - updated weekly
      </Typography>

      {/* Generate PRP */}
      {!prp && (
        <Paper sx={{ p: 3, mb: 3, textAlign: 'center' }}>
          <Typography variant="h6" gutterBottom>
            Ready to transform your career?
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Generate your Personal Reskilling Plan (PRP) in seconds
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={generatePRP}
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate My Learning Plan'}
          </Button>
        </Paper>
      )}

      {/* PRP Overview */}
      {prp && (
        <Box>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              Your Personal Reskilling Plan
            </Typography>

            <Grid container spacing={3}>
              <Grid item xs={12} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Target Role
                    </Typography>
                    <Typography variant="h6">
                      {prp.target_role}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Current Readiness
                    </Typography>
                    <Typography variant="h4">
                      {prp.current_readiness}%
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={prp.current_readiness}
                      sx={{ mt: 1 }}
                    />
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Target Readiness
                    </Typography>
                    <Typography variant="h4" color="success.main">
                      {prp.target_readiness}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Time to Complete
                    </Typography>
                    <Typography variant="h4">
                      {prp.estimated_completion_weeks}
                    </Typography>
                    <Typography variant="caption">weeks</Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Alert severity="success" sx={{ mt: 3 }}>
              <strong>Plan adapts weekly</strong> based on your progress and market trends!
            </Alert>
          </Paper>

          {/* Learning Modules */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              Learning Modules ({prp.learning_modules.length})
            </Typography>

            <Grid container spacing={2}>
              {prp.learning_modules.map((module, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">
                        Module {index + 1}: {module.skill_target}
                      </Typography>

                      <Box sx={{ mt: 2 }}>
                        <Typography variant="body2">
                          Current: {module.current_proficiency}% → Target: {module.target_proficiency}%
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={module.current_proficiency}
                          sx={{ mt: 1, mb: 2 }}
                        />
                      </Box>

                      <Grid container spacing={1}>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">
                            Micro-lessons
                          </Typography>
                          <Typography variant="body1">
                            {module.total_micro_lessons}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">
                            Practice Projects
                          </Typography>
                          <Typography variant="body1">
                            {module.practice_projects.length}
                          </Typography>
                        </Grid>
                      </Grid>

                      <Chip
                        label={module.ai_tutor_available ? 'AI Tutor Available' : 'Self-paced'}
                        color="primary"
                        size="small"
                        sx={{ mt: 2 }}
                      />

                      <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
                        {module.estimated_hours}hrs total
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>

          {/* Weekly Schedule */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              Weekly Schedule
            </Typography>

            <Stepper orientation="vertical">
              {prp.weekly_schedule.slice(0, 4).map((week, index) => (
                <Step key={index} active={index === 0}>
                  <StepLabel>
                    <Typography variant="h6">
                      Week {week.week} - {week.total_hours} hours
                    </Typography>
                  </StepLabel>
                  <Box sx={{ ml: 4, mt: 1, mb: 2 }}>
                    <List dense>
                      {week.modules.map((module, idx) => (
                        <ListItem key={idx}>
                          <ListItemText
                            primary={module.skill_target}
                            secondary={module.activities.join(' • ')}
                          />
                        </ListItem>
                      ))}
                    </List>
                    <Chip label={week.checkpoint} size="small" color="primary" />
                  </Box>
                </Step>
              ))}
            </Stepper>

            {prp.weekly_schedule.length > 4 && (
              <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                + {prp.weekly_schedule.length - 4} more weeks
              </Typography>
            )}
          </Paper>

          {/* Today's Micro-Lessons */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Today's 5-Minute Lessons
            </Typography>

            <Button
              variant="contained"
              onClick={loadTodaysLesson}
              sx={{ mb: 3 }}
            >
              Get Today's Lessons
            </Button>

            {todaysLesson && (
              <Box>
                <Alert severity="info" sx={{ mb: 2 }}>
                  <Typography variant="body2">
                    {todaysLesson.date} - Week {todaysLesson.week}
                  </Typography>
                  <Typography variant="caption">
                    Total time: {todaysLesson.total_time_minutes} minutes
                  </Typography>
                </Alert>

                {todaysLesson.lessons && todaysLesson.lessons.map((lesson, index) => (
                  <Card key={index} sx={{ mb: 2 }}>
                    <CardContent>
                      <Typography variant="h6">
                        Lesson {index + 1}: {lesson.title}
                      </Typography>
                      <Chip label={`${lesson.duration_minutes} min`} size="small" sx={{ mr: 1 }} />
                      <Chip label={lesson.difficulty} size="small" />
                      <Typography variant="body2" sx={{ mt: 2 }}>
                        Topics: {lesson.topics.join(', ')}
                      </Typography>
                      <Button variant="outlined" size="small" sx={{ mt: 2 }}>
                        Start Lesson
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </Box>
            )}
          </Paper>

          {/* Next Steps */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Next Steps
            </Typography>
            <List>
              {prp.next_steps.map((step, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`${index + 1}. ${step}`} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Box>
      )}
    </Box>
  );
}

export default AIAutopilot;
