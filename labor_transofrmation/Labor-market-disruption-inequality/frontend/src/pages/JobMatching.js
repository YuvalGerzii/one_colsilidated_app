import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  Alert
} from '@mui/material';
import { matchJobsForWorker } from '../services/api';

function JobMatching() {
  const [workerId, setWorkerId] = useState('');
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!workerId) {
      setError('Please enter a worker ID');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await matchJobsForWorker(parseInt(workerId), 10);
      setMatches(response.data.top_matches || []);

    } catch (err) {
      setError('Error finding job matches. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getMatchColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 65) return 'primary';
    if (score >= 50) return 'warning';
    return 'default';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Job Matching
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Find the best job opportunities matched to worker skills and preferences
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={8}>
            <TextField
              fullWidth
              label="Worker ID"
              type="number"
              value={workerId}
              onChange={(e) => setWorkerId(e.target.value)}
              helperText="Enter worker ID to find matching jobs"
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handleSearch}
              disabled={loading}
            >
              {loading ? 'Searching...' : 'Find Matches'}
            </Button>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {matches.length > 0 && (
        <Box>
          <Typography variant="h6" gutterBottom>
            Top Job Matches
          </Typography>

          <Grid container spacing={2}>
            {matches.map((match, index) => (
              <Grid item xs={12} key={index}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                      <Box>
                        <Typography variant="h6">
                          {match.job_title}
                        </Typography>
                        <Typography color="text.secondary">
                          {match.company}
                        </Typography>
                      </Box>
                      <Chip
                        label={`${match.match_score}% Match`}
                        color={getMatchColor(match.match_score)}
                        size="large"
                      />
                    </Box>

                    <Typography variant="body2" paragraph>
                      {match.recommendation}
                    </Typography>

                    <Box sx={{ mt: 2 }}>
                      <Chip
                        size="small"
                        label={`Match Level: ${match.match_level}`}
                        sx={{ mr: 1 }}
                      />
                    </Box>

                    {match.details && (
                      <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                        <Grid container spacing={1}>
                          <Grid item xs={6} md={3}>
                            <Typography variant="caption" color="text.secondary">
                              Skill Match
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {match.details.skill_analysis?.overall_match || 0}%
                            </Typography>
                          </Grid>
                          <Grid item xs={6} md={3}>
                            <Typography variant="caption" color="text.secondary">
                              Location
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {match.details.location_score || 0}%
                            </Typography>
                          </Grid>
                          <Grid item xs={6} md={3}>
                            <Typography variant="caption" color="text.secondary">
                              Salary
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {match.details.salary_score || 0}%
                            </Typography>
                          </Grid>
                          <Grid item xs={6} md={3}>
                            <Typography variant="caption" color="text.secondary">
                              Experience
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {match.details.experience_score || 0}%
                            </Typography>
                          </Grid>
                        </Grid>
                      </Box>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Box>
  );
}

export default JobMatching;
