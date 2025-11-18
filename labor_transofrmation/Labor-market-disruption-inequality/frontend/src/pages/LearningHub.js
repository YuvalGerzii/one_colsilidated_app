import React, { useState } from 'react';
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
  Divider,
  LinearProgress,
  Stepper,
  Step,
  StepLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import SchoolIcon from '@mui/icons-material/School';
import TimelineIcon from '@mui/icons-material/Timeline';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import AssignmentIcon from '@mui/icons-material/Assignment';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

function LearningHub() {
  const [workerId] = useState(1);
  const [learningPath, setLearningPath] = useState(null);
  const [progressReport, setProgressReport] = useState(null);
  const [careerPaths, setCareerPaths] = useState(null);
  const [teachingSession, setTeachingSession] = useState(null);
  const [practiceProblems, setPracticeProblems] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fullAnalysis, setFullAnalysis] = useState(null);

  const createLearningPath = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        `${API_BASE_URL}/agents/create-learning-path/${workerId}`
      );
      setLearningPath(response.data.learning_path);
    } catch (error) {
      console.error('Error creating learning path:', error);
    } finally {
      setLoading(false);
    }
  };

  const monitorProgress = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        `${API_BASE_URL}/agents/monitor-progress/${workerId}`
      );
      setProgressReport(response.data.progress_report);
    } catch (error) {
      console.error('Error monitoring progress:', error);
    } finally {
      setLoading(false);
    }
  };

  const exploreCareerPaths = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        `${API_BASE_URL}/agents/explore-career-paths/${workerId}?time_horizon_years=5`
      );
      setCareerPaths(response.data.career_paths);
    } catch (error) {
      console.error('Error exploring career paths:', error);
    } finally {
      setLoading(false);
    }
  };

  const startTeachingSession = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        `${API_BASE_URL}/agents/teaching-session/${workerId}?skill=machine_learning&difficulty=medium`
      );
      setTeachingSession(response.data.session);
    } catch (error) {
      console.error('Error starting teaching session:', error);
    } finally {
      setLoading(false);
    }
  };

  const generatePractice = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        `${API_BASE_URL}/agents/practice-problems?skill=python&difficulty=medium&count=5`
      );
      setPracticeProblems(response.data.problems);
    } catch (error) {
      console.error('Error generating practice:', error);
    } finally {
      setLoading(false);
    }
  };

  const runFullAnalysis = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        `${API_BASE_URL}/agents/full-agent-analysis/${workerId}`
      );
      setFullAnalysis(response.data);
    } catch (error) {
      console.error('Error running full analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Learning & Career Hub
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Complete learning system powered by 5 AI agents: personalized learning paths, adaptive teaching, career guidance, and progress tracking
      </Typography>

      {/* Quick Actions */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <SchoolIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6">Learning Path</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                AI-generated optimal learning strategy
              </Typography>
              <Button variant="contained" fullWidth onClick={createLearningPath}>
                Create My Path
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <TrendingUpIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
              <Typography variant="h6">Progress Tracking</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Monitor your learning progress
              </Typography>
              <Button variant="contained" color="success" fullWidth onClick={monitorProgress}>
                View Progress
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <TimelineIcon sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
              <Typography variant="h6">Career Paths</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Explore your career options
              </Typography>
              <Button variant="contained" color="warning" fullWidth onClick={exploreCareerPaths}>
                Explore Careers
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <Card>
            <CardContent>
              <EmojiEventsIcon sx={{ fontSize: 40, color: 'error.main', mb: 1 }} />
              <Typography variant="h6">Full Analysis</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Complete 5-agent analysis
              </Typography>
              <Button variant="contained" color="error" fullWidth onClick={runFullAnalysis}>
                Analyze Everything
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Loading */}
      {loading && <LinearProgress sx={{ mb: 3 }} />}

      {/* Full Analysis Results */}
      {fullAnalysis && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Complete 5-Agent Analysis
          </Typography>

          <Alert severity="info" sx={{ mb: 2 }}>
            All 5 AI agents have analyzed your profile. Here's your comprehensive career transition plan.
          </Alert>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">1. Gap Analysis</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {fullAnalysis.comprehensive_analysis.gap_analysis && (
                <Box>
                  <Alert severity={
                    fullAnalysis.comprehensive_analysis.gap_analysis.overall_readiness > 70 ? 'success' :
                    fullAnalysis.comprehensive_analysis.gap_analysis.overall_readiness > 50 ? 'warning' : 'error'
                  } sx={{ mb: 2 }}>
                    Overall Readiness: {fullAnalysis.comprehensive_analysis.gap_analysis.overall_readiness}%
                  </Alert>
                  <List dense>
                    {fullAnalysis.comprehensive_analysis.gap_analysis.recommendations.map((rec, i) => (
                      <ListItem key={i}>
                        <ListItemText primary={rec} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">2. Learning Path</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {fullAnalysis.comprehensive_analysis.learning_path && (
                <Box>
                  <Typography variant="subtitle1" gutterBottom>
                    {fullAnalysis.comprehensive_analysis.learning_path.timeline?.total_weeks} weeks total
                  </Typography>
                  <List dense>
                    {fullAnalysis.comprehensive_analysis.learning_path.recommendations.map((rec, i) => (
                      <ListItem key={i}>
                        <ListItemText primary={rec} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">3. Career Paths</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {fullAnalysis.comprehensive_analysis.career_paths && (
                <Box>
                  <List>
                    {fullAnalysis.comprehensive_analysis.career_paths.top_paths?.map((path, i) => (
                      <ListItem key={i}>
                        <ListItemText
                          primary={path.target_role}
                          secondary={`Score: ${path.overall_score} | Difficulty: ${path.transition_difficulty}`}
                        />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">4. Opportunities</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {fullAnalysis.comprehensive_analysis.opportunities && (
                <Box>
                  <Typography variant="body1" gutterBottom>
                    Found {fullAnalysis.comprehensive_analysis.opportunities.total_found} opportunities
                  </Typography>
                  <List dense>
                    {fullAnalysis.comprehensive_analysis.opportunities.recommendations.map((rec, i) => (
                      <ListItem key={i}>
                        <ListItemText primary={rec} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </AccordionDetails>
          </Accordion>

          <Divider sx={{ my: 3 }} />

          <Typography variant="h6" gutterBottom>
            Integrated Recommendations
          </Typography>

          <Grid container spacing={2}>
            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 2, bgcolor: 'error.light' }}>
                <Typography variant="subtitle2" gutterBottom>Immediate Actions</Typography>
                <List dense>
                  {fullAnalysis.integrated_recommendations?.immediate_actions.map((action, i) => (
                    <ListItem key={i}>
                      <ListItemText primary={action} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 2, bgcolor: 'warning.light' }}>
                <Typography variant="subtitle2" gutterBottom>This Week</Typography>
                <List dense>
                  {fullAnalysis.integrated_recommendations?.this_week.map((action, i) => (
                    <ListItem key={i}>
                      <ListItemText primary={action} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 2, bgcolor: 'info.light' }}>
                <Typography variant="subtitle2" gutterBottom>This Month</Typography>
                <List dense>
                  {fullAnalysis.integrated_recommendations?.this_month.map((action, i) => (
                    <ListItem key={i}>
                      <ListItemText primary={action} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 2, bgcolor: 'success.light' }}>
                <Typography variant="subtitle2" gutterBottom>This Quarter</Typography>
                <List dense>
                  {fullAnalysis.integrated_recommendations?.this_quarter.map((action, i) => (
                    <ListItem key={i}>
                      <ListItemText primary={action} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* Learning Path Results */}
      {learningPath && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Your Personalized Learning Path
          </Typography>

          <Alert severity="info" sx={{ mb: 2 }}>
            {learningPath.timeline?.total_weeks} weeks | {learningPath.total_estimated_hours} hours total
          </Alert>

          {learningPath.optimal_path && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                {learningPath.optimal_path.name}
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                {learningPath.optimal_path.description}
              </Typography>

              <Grid container spacing={1} sx={{ mb: 2 }}>
                <Grid item>
                  <Chip label={`Strategy: ${learningPath.optimal_path.recommended_style}`} color="primary" size="small" />
                </Grid>
                {learningPath.optimal_path.pros?.slice(0, 3).map((pro, i) => (
                  <Grid item key={i}>
                    <Chip label={`✓ ${pro}`} color="success" size="small" />
                  </Grid>
                ))}
              </Grid>

              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Skill</TableCell>
                      <TableCell>Level</TableCell>
                      <TableCell>Hours</TableCell>
                      <TableCell>Priority</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {learningPath.optimal_path.skills?.map((skill, i) => (
                      <TableRow key={i}>
                        <TableCell>{skill.name}</TableCell>
                        <TableCell>
                          <Chip label={skill.level} size="small" />
                        </TableCell>
                        <TableCell>{skill.estimated_hours}h</TableCell>
                        <TableCell>
                          <Chip
                            label={skill.priority}
                            color={skill.priority === 'critical' ? 'error' : 'default'}
                            size="small"
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}

          <Divider sx={{ my: 2 }} />

          <Typography variant="h6" gutterBottom>
            Milestones
          </Typography>
          <Stepper activeStep={0} alternativeLabel>
            {learningPath.milestones?.map((milestone, i) => (
              <Step key={i}>
                <StepLabel>
                  {milestone.name}
                  <Typography variant="caption" display="block">
                    {milestone.percentage}%
                  </Typography>
                </StepLabel>
              </Step>
            ))}
          </Stepper>

          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>Recommendations</Typography>
            <List>
              {learningPath.recommendations?.map((rec, i) => (
                <ListItem key={i}>
                  <ListItemText primary={`${i + 1}. ${rec}`} />
                </ListItem>
              ))}
            </List>
          </Box>
        </Paper>
      )}

      {/* Progress Report */}
      {progressReport && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Progress Report
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="h3" color="primary">
                  {progressReport.progress_score}
                </Typography>
                <Typography variant="subtitle1" color="text.secondary">
                  Progress Score
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={progressReport.progress_score}
                  sx={{ mt: 1, height: 10, borderRadius: 5 }}
                />
              </Box>

              <Typography variant="h6" gutterBottom>
                {progressReport.stage_message}
              </Typography>
              <Chip label={progressReport.stage} color="primary" sx={{ mb: 2 }} />

              <Typography variant="body1" sx={{ mb: 2 }}>
                {progressReport.motivational_message}
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>Metrics</Typography>
              <List dense>
                <ListItem>
                  <ListItemText
                    primary="Completed Activities"
                    secondary={`${progressReport.metrics?.completed_activities} / ${progressReport.metrics?.total_activities}`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Completion Rate"
                    secondary={`${progressReport.metrics?.completion_rate}%`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Learning Velocity"
                    secondary={`${progressReport.metrics?.learning_velocity} activities/day`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Current Streak"
                    secondary={`${progressReport.metrics?.streak_days} days`}
                  />
                </ListItem>
              </List>
            </Grid>
          </Grid>

          <Divider sx={{ my: 2 }} />

          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>Strengths</Typography>
              <Box>
                {progressReport.strengths?.map((strength, i) => (
                  <Chip key={i} label={strength} color="success" sx={{ m: 0.5 }} />
                ))}
              </Box>
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>Areas for Improvement</Typography>
              <Box>
                {progressReport.areas_for_improvement?.map((area, i) => (
                  <Chip key={i} label={area} color="warning" sx={{ m: 0.5 }} />
                ))}
              </Box>
            </Grid>
          </Grid>

          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>Recommendations</Typography>
            <List>
              {progressReport.recommendations?.map((rec, i) => (
                <ListItem key={i}>
                  <ListItemText primary={rec} />
                </ListItem>
              ))}
            </List>
          </Box>
        </Paper>
      )}

      {/* Career Paths */}
      {careerPaths && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Career Path Explorer
          </Typography>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {careerPaths.total_paths_identified} career paths identified for {careerPaths.time_horizon}
          </Typography>

          <Grid container spacing={2}>
            {careerPaths.career_paths?.map((path, i) => (
              <Grid item xs={12} md={6} key={i}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {path.target_role}
                    </Typography>

                    <Grid container spacing={1} sx={{ mb: 2 }}>
                      <Grid item>
                        <Chip label={path.path_type} size="small" />
                      </Grid>
                      <Grid item>
                        <Chip label={`Score: ${path.overall_score}`} color="primary" size="small" />
                      </Grid>
                      <Grid item>
                        <Chip label={`${path.estimated_time_years}y`} size="small" />
                      </Grid>
                    </Grid>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" gutterBottom>
                        Income: ${path.income_potential?.toLocaleString()}
                      </Typography>
                      <Typography variant="body2" gutterBottom>
                        Market Demand: {path.market_demand}/100
                      </Typography>
                      <Typography variant="body2">
                        Work-Life Balance: {path.work_life_balance}/100
                      </Typography>
                    </Box>

                    <Divider sx={{ my: 1 }} />

                    <Typography variant="subtitle2" gutterBottom>Pros:</Typography>
                    {path.pros?.slice(0, 3).map((pro, j) => (
                      <Typography key={j} variant="body2" color="success.main">
                        ✓ {pro}
                      </Typography>
                    ))}

                    <Typography variant="subtitle2" gutterBottom sx={{ mt: 1 }}>Cons:</Typography>
                    {path.cons?.slice(0, 2).map((con, j) => (
                      <Typography key={j} variant="body2" color="error.main">
                        ✗ {con}
                      </Typography>
                    ))}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>Recommendations</Typography>
            <List>
              {careerPaths.recommendations?.map((rec, i) => (
                <ListItem key={i}>
                  <ListItemText primary={rec} />
                </ListItem>
              ))}
            </List>
          </Box>
        </Paper>
      )}

      {/* Teaching & Practice Section */}
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <MenuBookIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Adaptive Teaching Session
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Get personalized 1-on-1 teaching from AI coach
              </Typography>
              <Button variant="contained" fullWidth onClick={startTeachingSession}>
                Start Learning Session
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <AssignmentIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Practice Problems
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Generate adaptive practice problems
              </Typography>
              <Button variant="contained" color="success" fullWidth onClick={generatePractice}>
                Generate Problems
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Teaching Session Results */}
      {teachingSession && (
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="h5" gutterBottom>
            Teaching Session: {teachingSession.skill}
          </Typography>

          <Alert severity="info" sx={{ mb: 2 }}>
            {teachingSession.adaptation_message}
          </Alert>

          <Grid container spacing={2}>
            {teachingSession.session_structure && Object.entries(teachingSession.session_structure).map(([key, value]) => (
              <Grid item xs={12} md={6} key={key}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </Typography>
                    {typeof value === 'object' ? (
                      <Typography variant="body2">
                        {value.description || JSON.stringify(value, null, 2)}
                      </Typography>
                    ) : (
                      <Typography variant="body2">{value}</Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}

      {/* Practice Problems */}
      {practiceProblems && (
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="h5" gutterBottom>
            Practice Problems: {practiceProblems.skill}
          </Typography>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {practiceProblems.total_problems} problems | Difficulty: {practiceProblems.difficulty}
          </Typography>

          {practiceProblems.problems?.map((problem, i) => (
            <Card key={i} sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Problem {problem.id}
                </Typography>
                <Typography variant="body1" paragraph>
                  {problem.problem}
                </Typography>
                <Typography variant="caption" display="block" gutterBottom>
                  Estimated time: {problem.estimated_time}
                </Typography>
                <Chip label={problem.difficulty} size="small" sx={{ mr: 1 }} />
                {problem.learning_objectives?.map((obj, j) => (
                  <Chip key={j} label={obj} size="small" variant="outlined" sx={{ mr: 1 }} />
                ))}
              </CardContent>
            </Card>
          ))}
        </Paper>
      )}
    </Box>
  );
}

export default LearningHub;
