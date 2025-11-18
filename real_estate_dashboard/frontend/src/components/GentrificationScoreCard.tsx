import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  LinearProgress,
  Chip,
  Grid,
  Alert,
  CircularProgress,
  Tooltip,
  Paper
} from '@mui/material';
import {
  TrendingUp,
  Speed,
  Work,
  AccountBalance,
  Home,
  InfoOutlined
} from '@mui/icons-material';
import { api } from '../services/apiClient';

interface ComponentScore {
  score: number;
  weight: string;
  value: string;
  indicator: string;
}

interface GentrificationData {
  score: number;
  risk_level: string;
  risk_description: string;
  recommendation: string;
  confidence: string;
  component_scores: {
    price_growth: ComponentScore;
    market_velocity: ComponentScore;
    employment: ComponentScore;
    interest_rates: ComponentScore;
    affordability: ComponentScore;
  };
  market_indicators: {
    price_growth_yoy: number;
    months_supply: number;
    unemployment_rate: number;
    mortgage_rate_30y: number;
    median_price: number;
  };
  location: string;
  timestamp: string;
  data_quality: {
    sources_available: number;
    confidence_level: string;
    employment_source: string;
    housing_source: string;
    rates_source: string;
  };
}

interface GentrificationScoreCardProps {
  location?: string;
}

const GentrificationScoreCard: React.FC<GentrificationScoreCardProps> = ({ location }) => {
  const [data, setData] = useState<GentrificationData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchGentrificationScore();
  }, [location]);

  const fetchGentrificationScore = async () => {
    try {
      setLoading(true);
      setError(null);

      const params = location ? { location } : {};
      const response = await api.get('/market-intelligence/analysis/gentrification-score', { params });
      setData(response.data);
    } catch (err: any) {
      console.error('Error fetching gentrification score:', err);
      setError(err.message || 'Failed to load gentrification score');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskLevel: string): string => {
    switch (riskLevel) {
      case 'very_high':
        return '#d32f2f'; // Red
      case 'high':
        return '#f57c00'; // Orange
      case 'moderate':
        return '#fbc02d'; // Yellow
      case 'low':
        return '#388e3c'; // Green
      default:
        return '#757575'; // Gray
    }
  };

  const getConfidenceColor = (confidence: string): 'success' | 'warning' | 'error' => {
    switch (confidence) {
      case 'high':
        return 'success';
      case 'medium':
        return 'warning';
      default:
        return 'error';
    }
  };

  const getComponentIcon = (component: string) => {
    switch (component) {
      case 'price_growth':
        return <TrendingUp />;
      case 'market_velocity':
        return <Speed />;
      case 'employment':
        return <Work />;
      case 'interest_rates':
        return <AccountBalance />;
      case 'affordability':
        return <Home />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="300px">
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error">{error}</Alert>
        </CardContent>
      </Card>
    );
  }

  if (!data) {
    return null;
  }

  const riskColor = getRiskColor(data.risk_level);

  return (
    <Card>
      <CardContent>
        {/* Header */}
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h5" component="h2" gutterBottom>
            Gentrification Risk Score
          </Typography>
          <Tooltip title="Analyzes 5 key indicators to assess gentrification pressure">
            <InfoOutlined color="action" />
          </Tooltip>
        </Box>

        {/* Main Score Display */}
        <Box textAlign="center" mb={4}>
          <Typography variant="h1" component="div" style={{ color: riskColor, fontWeight: 'bold' }}>
            {data.score}
          </Typography>
          <Typography variant="h6" color="textSecondary" gutterBottom>
            out of 100
          </Typography>
          <Chip
            label={data.risk_description}
            style={{ backgroundColor: riskColor, color: 'white', fontWeight: 'bold', marginTop: '8px' }}
            size="medium"
          />
          <Box mt={1}>
            <Chip
              label={`${data.confidence.toUpperCase()} CONFIDENCE`}
              color={getConfidenceColor(data.confidence)}
              size="small"
              variant="outlined"
            />
          </Box>
        </Box>

        {/* Score Range Bar */}
        <Box mb={4}>
          <Box position="relative" height="40px">
            <LinearProgress
              variant="determinate"
              value={100}
              sx={{
                height: '40px',
                borderRadius: '20px',
                backgroundColor: '#e0e0e0',
                '& .MuiLinearProgress-bar': {
                  background: 'linear-gradient(to right, #388e3c 0%, #388e3c 25%, #fbc02d 25%, #fbc02d 50%, #f57c00 50%, #f57c00 75%, #d32f2f 75%, #d32f2f 100%)',
                }
              }}
            />
            <Box
              position="absolute"
              top="0"
              left={`${data.score}%`}
              sx={{
                transform: 'translateX(-50%)',
                width: '4px',
                height: '40px',
                backgroundColor: 'black',
                borderRadius: '2px'
              }}
            />
          </Box>
          <Box display="flex" justifyContent="space-between" mt={1}>
            <Typography variant="caption">Low (0-25)</Typography>
            <Typography variant="caption">Moderate (26-50)</Typography>
            <Typography variant="caption">High (51-75)</Typography>
            <Typography variant="caption">Very High (76-100)</Typography>
          </Box>
        </Box>

        {/* Recommendation */}
        <Alert severity="info" icon={<InfoOutlined />} sx={{ mb: 3 }}>
          <Typography variant="body2">
            <strong>Recommendation:</strong> {data.recommendation}
          </Typography>
        </Alert>

        {/* Component Scores */}
        <Typography variant="h6" gutterBottom sx={{ mt: 3, mb: 2 }}>
          Score Breakdown
        </Typography>
        <Grid container spacing={2}>
          {Object.entries(data.component_scores).map(([key, score]) => (
            <Grid item xs={12} key={key}>
              <Paper elevation={1} sx={{ p: 2 }}>
                <Box display="flex" alignItems="center" mb={1}>
                  <Box mr={1} display="flex" alignItems="center">
                    {getComponentIcon(key)}
                  </Box>
                  <Typography variant="subtitle2" style={{ flex: 1 }}>
                    {score.indicator}
                  </Typography>
                  <Chip
                    label={score.weight}
                    size="small"
                    variant="outlined"
                    sx={{ mr: 1 }}
                  />
                  <Chip
                    label={score.value}
                    size="small"
                    color="primary"
                    variant="filled"
                  />
                </Box>
                <Box display="flex" alignItems="center">
                  <Box flexGrow={1} mr={2}>
                    <LinearProgress
                      variant="determinate"
                      value={score.score}
                      sx={{
                        height: '8px',
                        borderRadius: '4px',
                        backgroundColor: '#e0e0e0',
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: score.score > 75 ? '#d32f2f' :
                                         score.score > 50 ? '#f57c00' :
                                         score.score > 25 ? '#fbc02d' : '#388e3c'
                        }
                      }}
                    />
                  </Box>
                  <Typography variant="body2" color="textSecondary" style={{ minWidth: '40px', textAlign: 'right' }}>
                    {score.score}/100
                  </Typography>
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>

        {/* Data Quality Info */}
        <Box mt={3} pt={2} borderTop="1px solid #e0e0e0">
          <Typography variant="caption" color="textSecondary">
            <strong>Data Quality:</strong> {data.data_quality.sources_available} of 3 live data sources active
            {' • '}
            <strong>Location:</strong> {data.location || 'National'}
            {' • '}
            <strong>Updated:</strong> {new Date(data.timestamp).toLocaleString()}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default GentrificationScoreCard;
