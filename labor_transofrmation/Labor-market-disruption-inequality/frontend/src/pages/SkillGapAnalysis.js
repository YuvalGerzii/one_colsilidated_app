import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Alert,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider
} from '@mui/material';
import { analyzeSkillGap, recommendLearningPath } from '../services/api';

function SkillGapAnalysis() {
  const [workerId, setWorkerId] = useState('');
  const [targetJobId, setTargetJobId] = useState('');
  const [gapAnalysis, setGapAnalysis] = useState(null);
  const [learningPath, setLearningPath] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!workerId || !targetJobId) {
      setError('Please enter both Worker ID and Target Job ID');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const gapResponse = await analyzeSkillGap(
        parseInt(workerId),
        parseInt(targetJobId)
      );
      setGapAnalysis(gapResponse.data);

      const pathResponse = await recommendLearningPath(
        parseInt(workerId),
        parseInt(targetJobId)
      );
      setLearningPath(pathResponse.data);

    } catch (err) {
      setError('Error analyzing skill gap. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getReadinessColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 50) return 'warning';
    return 'error';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Skill Gap Analysis
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Analyze skill gaps and get personalized reskilling recommendations
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={5}>
            <TextField
              fullWidth
              label="Worker ID"
              type="number"
              value={workerId}
              onChange={(e) => setWorkerId(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              fullWidth
              label="Target Job ID"
              type="number"
              value={targetJobId}
              onChange={(e) => setTargetJobId(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handleAnalyze}
              disabled={loading}
              sx={{ height: '56px' }}
            >
              Analyze
            </Button>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {loading && <LinearProgress sx={{ mb: 2 }} />}

      {gapAnalysis && (
        <Box>
          {/* Readiness Score */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Job Readiness Score
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Typography variant="h3" color={`${getReadinessColor(gapAnalysis.readiness_score)}.main`}>
                {gapAnalysis.readiness_score}%
              </Typography>
              <Box sx={{ flexGrow: 1 }}>
                <LinearProgress
                  variant="determinate"
                  value={gapAnalysis.readiness_score}
                  color={getReadinessColor(gapAnalysis.readiness_score)}
                  sx={{ height: 10, borderRadius: 5 }}
                />
                <Typography variant="caption" color="text.secondary">
                  Estimated learning time: {gapAnalysis.total_estimated_weeks} weeks
                </Typography>
              </Box>
            </Box>
          </Paper>

          <Grid container spacing={3}>
            {/* Missing Skills */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Missing Skills ({gapAnalysis.missing_skills.length})
                </Typography>
                <List>
                  {gapAnalysis.missing_skills.map((skill, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={skill.skill_name}
                        secondary={
                          <>
                            Category: {skill.category}
                            <br />
                            Learning time: {skill.estimated_learning_time_weeks} weeks
                            {skill.required && (
                              <Chip
                                size="small"
                                label="Required"
                                color="error"
                                sx={{ ml: 1 }}
                              />
                            )}
                          </>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            {/* Skills to Upgrade */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Skills to Upgrade ({gapAnalysis.skills_to_upgrade.length})
                </Typography>
                <List>
                  {gapAnalysis.skills_to_upgrade.map((skill, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={skill.skill_name}
                        secondary={
                          <>
                            Current: Level {skill.current_proficiency} → Target: Level {skill.target_proficiency}
                            <br />
                            Learning time: {skill.estimated_learning_time_weeks} weeks
                          </>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>
          </Grid>

          {/* Learning Path */}
          {learningPath && (
            <Paper sx={{ p: 3, mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                Recommended Learning Path
              </Typography>

              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={12} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Total Duration
                  </Typography>
                  <Typography variant="h6">
                    {learningPath.total_duration_weeks} weeks
                  </Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Total Cost
                  </Typography>
                  <Typography variant="h6">
                    ${learningPath.total_cost.toLocaleString()}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Budget Fit
                  </Typography>
                  <Chip
                    label={learningPath.budget_fit ? 'Yes' : 'No'}
                    color={learningPath.budget_fit ? 'success' : 'warning'}
                  />
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Completion Date
                  </Typography>
                  <Typography variant="body2">
                    {learningPath.estimated_completion_date}
                  </Typography>
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />

              <Typography variant="subtitle1" gutterBottom>
                Training Programs
              </Typography>
              <List>
                {learningPath.recommended_programs.map((program, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={program.title}
                      secondary={
                        <>
                          Provider: {program.provider}
                          <br />
                          Duration: {program.duration_weeks} weeks | Cost: ${program.cost}
                          <br />
                          Success Rate: {(program.success_rate * 100).toFixed(0)}%
                        </>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          )}
        </Box>
      )}
    </Box>
  );
}

export default SkillGapAnalysis;
