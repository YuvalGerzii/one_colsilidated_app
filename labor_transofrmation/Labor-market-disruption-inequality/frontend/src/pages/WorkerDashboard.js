import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Alert
} from '@mui/material';
import {
  getWorkerRiskAssessment,
  matchJobsForWorker,
  getWorkerProfile
} from '../services/api';

function WorkerDashboard() {
  const [workerId] = useState(1); // Demo: hardcoded worker ID
  const [riskData, setRiskData] = useState(null);
  const [jobMatches, setJobMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadWorkerData();
  }, []);

  const loadWorkerData = async () => {
    try {
      setLoading(true);

      // Load risk assessment
      const riskResponse = await getWorkerRiskAssessment(workerId);
      setRiskData(riskResponse.data);

      // Load job matches
      const matchResponse = await matchJobsForWorker(workerId, 5);
      setJobMatches(matchResponse.data.top_matches || []);

    } catch (error) {
      console.error('Error loading worker data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    const colors = {
      low: 'success',
      medium: 'warning',
      high: 'error'
    };
    return colors[level] || 'default';
  };

  if (loading) {
    return <LinearProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Worker Dashboard
      </Typography>

      {/* Risk Assessment */}
      {riskData && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Job Loss Risk Assessment
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h2" color={`${getRiskColor(riskData.risk_level)}.main`}>
                  {riskData.risk_score}%
                </Typography>
                <Chip
                  label={riskData.risk_level.toUpperCase()}
                  color={getRiskColor(riskData.risk_level)}
                  sx={{ mt: 1 }}
                />
              </Box>
            </Grid>

            <Grid item xs={12} md={8}>
              <Typography variant="h6" gutterBottom>
                Risk Factors
              </Typography>
              {riskData.factors.map((factor, index) => (
                <Alert
                  key={index}
                  severity={factor.impact === 'high' ? 'error' : 'warning'}
                  sx={{ mb: 1 }}
                >
                  <strong>{factor.factor}:</strong> {factor.description}
                </Alert>
              ))}
            </Grid>
          </Grid>

          <Box sx={{ mt: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Confidence: {(riskData.confidence * 100).toFixed(0)}%
            </Typography>
          </Box>
        </Paper>
      )}

      {/* Job Matches */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Recommended Job Opportunities
        </Typography>

        {jobMatches.length === 0 ? (
          <Alert severity="info">
            No job matches found. Complete your profile to get personalized recommendations.
          </Alert>
        ) : (
          <Grid container spacing={2}>
            {jobMatches.map((match, index) => (
              <Grid item xs={12} key={index}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
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
                        color={match.match_score >= 80 ? 'success' : match.match_score >= 60 ? 'primary' : 'default'}
                      />
                    </Box>

                    <Typography variant="body2" sx={{ mt: 2 }}>
                      {match.recommendation}
                    </Typography>

                    <Box sx={{ mt: 2 }}>
                      <Chip
                        size="small"
                        label={match.match_level}
                        sx={{ mr: 1 }}
                      />
                    </Box>

                    <Button
                      variant="outlined"
                      size="small"
                      sx={{ mt: 2 }}
                    >
                      View Details
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Paper>
    </Box>
  );
}

export default WorkerDashboard;
