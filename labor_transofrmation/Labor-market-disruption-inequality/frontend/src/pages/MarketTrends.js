import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  LinearProgress,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { getMarketTrends, getWorkerStatistics } from '../services/api';

function MarketTrends() {
  const [trends, setTrends] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTrends();
  }, []);

  const loadTrends = async () => {
    try {
      setLoading(true);

      const trendsResponse = await getMarketTrends();
      setTrends(trendsResponse.data);

      const statsResponse = await getWorkerStatistics();
      setStatistics(statsResponse.data);

    } catch (error) {
      console.error('Error loading trends:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LinearProgress />;
  }

  if (!trends) {
    return <Typography>No data available</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Labor Market Trends
      </Typography>

      <Typography variant="body1" color="text.secondary" paragraph>
        Real-time insights into automation risk, skill demand, and workforce transitions
      </Typography>

      {/* Platform Statistics */}
      {statistics && (
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={3}>
            <Paper sx={{ p: 2 }}>
              <Typography color="text.secondary">
                Total Workers
              </Typography>
              <Typography variant="h4">
                {statistics.total_workers}
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={3}>
            <Paper sx={{ p: 2 }}>
              <Typography color="text.secondary">
                High Risk Workers
              </Typography>
              <Typography variant="h4" color="error">
                {statistics.high_risk_workers}
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={3}>
            <Paper sx={{ p: 2 }}>
              <Typography color="text.secondary">
                Avg Risk Score
              </Typography>
              <Typography variant="h4">
                {statistics.average_risk_score.toFixed(1)}%
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={3}>
            <Paper sx={{ p: 2 }}>
              <Typography color="text.secondary">
                Industries Tracked
              </Typography>
              <Typography variant="h4">
                {statistics.workers_by_industry.length}
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      )}

      <Grid container spacing={3}>
        {/* In-Demand Skills */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Top In-Demand Skills
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={trends.top_in_demand_skills.slice(0, 8)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="demand_score" fill="#4caf50" name="Demand Score" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* High Risk Skills */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Skills at Automation Risk
            </Typography>
            <List>
              {trends.high_automation_risk_skills.slice(0, 8).map((skill, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={skill.name}
                    secondary={
                      <LinearProgress
                        variant="determinate"
                        value={skill.automation_risk}
                        color="error"
                        sx={{ mt: 1 }}
                      />
                    }
                  />
                  <Typography variant="body2" color="error">
                    {skill.automation_risk.toFixed(0)}%
                  </Typography>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Industry Risk Scores */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Industry Automation Risk
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={trends.industry_risk_scores}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="industry" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="avg_risk_score" fill="#ff9800" name="Avg Risk Score" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default MarketTrends;
