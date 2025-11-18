// src/pages/MarketData/MarketData.tsx
import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  MenuItem,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Chip,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
} from '@mui/material';
import {
  Home,
  People,
  DirectionsWalk,
  Business,
  Assessment,
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import axios from 'axios';
import { API_BASE_URL } from '@/services/api';

interface MarketDataRequest {
  address: string;
  city: string;
  state: string;
  zip_code: string;
  property_type: string;
  latitude?: number;
  longitude?: number;
}

interface MarketDataResponse {
  success: boolean;
  data: any;
  cached?: boolean;
}

export const MarketData: React.FC = () => {
  const [formData, setFormData] = useState<MarketDataRequest>({
    address: '123 Market Street',
    city: 'San Francisco',
    state: 'CA',
    zip_code: '94103',
    property_type: 'Multifamily',
    latitude: 37.7749,
    longitude: -122.4194,
  });

  const [searchTriggered, setSearchTriggered] = useState(false);

  const { data, isLoading, error, refetch } = useQuery<MarketDataResponse>(
    ['marketData', formData],
    async () => {
      const response = await axios.post(
        `${API_BASE_URL}/market-data/investment-summary`,
        formData
      );
      return response.data;
    },
    {
      enabled: searchTriggered,
      onSuccess: () => setSearchTriggered(false),
    }
  );

  const handleInputChange = (field: keyof MarketDataRequest, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSearch = () => {
    setSearchTriggered(true);
    refetch();
  };

  const marketData = data?.data;

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          📈 Market Data Integration
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Real-time market intelligence from CoStar, Zillow, Census, and Walk Score
        </Typography>
      </Box>

      {/* Search Form */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Property Search
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Address"
              value={formData.address}
              onChange={(e) => handleInputChange('address', e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="City"
              value={formData.city}
              onChange={(e) => handleInputChange('city', e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={1.5}>
            <TextField
              fullWidth
              label="State"
              value={formData.state}
              onChange={(e) => handleInputChange('state', e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={1.5}>
            <TextField
              fullWidth
              label="ZIP Code"
              value={formData.zip_code}
              onChange={(e) => handleInputChange('zip_code', e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              select
              fullWidth
              label="Property Type"
              value={formData.property_type}
              onChange={(e) => handleInputChange('property_type', e.target.value)}
            >
              <MenuItem value="Multifamily">Multifamily</MenuItem>
              <MenuItem value="SFR">Single Family Residential</MenuItem>
              <MenuItem value="Office">Office</MenuItem>
              <MenuItem value="Retail">Retail</MenuItem>
              <MenuItem value="Industrial">Industrial</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} md={8}>
            <Button
              variant="contained"
              size="large"
              fullWidth
              onClick={handleSearch}
              disabled={isLoading}
            >
              {isLoading ? <CircularProgress size={24} /> : 'Get Market Data'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Loading State */}
      {isLoading && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>
            Fetching market data...
          </Typography>
        </Box>
      )}

      {/* Error State */}
      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          Failed to fetch market data. Please try again.
        </Alert>
      )}

      {/* Results */}
      {marketData && !isLoading && (
        <>
          {/* Cache Indicator */}
          {data.cached && (
            <Alert severity="info" sx={{ mb: 2 }}>
              Showing cached data (less than 24 hours old)
            </Alert>
          )}

          {/* Property Info */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              {marketData.property_info?.address}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              {marketData.property_info?.city}, {marketData.property_info?.state}{' '}
              {marketData.property_info?.zip_code}
            </Typography>
            <Chip
              label={marketData.property_info?.property_type}
              color="primary"
              sx={{ mt: 1 }}
            />
          </Paper>

          {/* Key Metrics Dashboard */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            {/* CoStar Metrics */}
            <Grid item xs={12} md={6} lg={3}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Business color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h6">CoStar Data</Typography>
                  </Box>
                  <Divider sx={{ mb: 2 }} />
                  <MetricRow
                    label="Cap Rate"
                    value={`${marketData.key_metrics?.cap_rate}%`}
                  />
                  <MetricRow
                    label="Market Trend"
                    value={marketData.key_metrics?.market_trend}
                    valueColor={
                      marketData.key_metrics?.market_trend === 'Growing'
                        ? 'success.main'
                        : marketData.key_metrics?.market_trend === 'Stable'
                        ? 'info.main'
                        : 'error.main'
                    }
                  />
                  <MetricRow
                    label="Vacancy Rate"
                    value={`${marketData.key_metrics?.vacancy_rate}%`}
                  />
                  <MetricRow
                    label="Market Rating"
                    value={marketData.key_metrics?.market_rating}
                  />
                </CardContent>
              </Card>
            </Grid>

            {/* Zillow/Redfin Metrics */}
            <Grid item xs={12} md={6} lg={3}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Home color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h6">Zillow/Redfin</Typography>
                  </Box>
                  <Divider sx={{ mb: 2 }} />
                  <MetricRow
                    label="Property Value"
                    value={formatCurrency(marketData.key_metrics?.property_value)}
                  />
                  <MetricRow
                    label="Rent Estimate"
                    value={formatCurrency(marketData.key_metrics?.rent_estimate)}
                  />
                  <MetricRow
                    label="30-Day Trend"
                    value={`${marketData.key_metrics?.price_trend_30d >= 0 ? '+' : ''}${marketData.key_metrics?.price_trend_30d}%`}
                    valueColor={
                      marketData.key_metrics?.price_trend_30d >= 0
                        ? 'success.main'
                        : 'error.main'
                    }
                  />
                  <MetricRow
                    label="Days on Market"
                    value={marketData.key_metrics?.days_on_market}
                  />
                </CardContent>
              </Card>
            </Grid>

            {/* Census Metrics */}
            <Grid item xs={12} md={6} lg={3}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <People color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h6">Census Data</Typography>
                  </Box>
                  <Divider sx={{ mb: 2 }} />
                  <MetricRow
                    label="Population"
                    value={formatNumber(marketData.key_metrics?.population)}
                  />
                  <MetricRow
                    label="5-Year Growth"
                    value={`${marketData.key_metrics?.population_growth >= 0 ? '+' : ''}${marketData.key_metrics?.population_growth}%`}
                    valueColor={
                      marketData.key_metrics?.population_growth >= 0
                        ? 'success.main'
                        : 'error.main'
                    }
                  />
                  <MetricRow
                    label="Median Income"
                    value={formatCurrency(marketData.key_metrics?.median_income)}
                  />
                  <MetricRow
                    label="Employment"
                    value={`${marketData.key_metrics?.employment_rate}%`}
                  />
                </CardContent>
              </Card>
            </Grid>

            {/* Walk Score */}
            <Grid item xs={12} md={6} lg={3}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <DirectionsWalk color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h6">Walk Score</Typography>
                  </Box>
                  <Divider sx={{ mb: 2 }} />
                  <ScoreBar
                    label="Walk Score"
                    value={marketData.key_metrics?.walk_score || 0}
                  />
                  <ScoreBar
                    label="Transit Score"
                    value={marketData.key_metrics?.transit_score || 0}
                  />
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                    {marketData.key_metrics?.walkability}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Investment Indicators */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              <Assessment sx={{ mr: 1, verticalAlign: 'middle' }} />
              Investment Analysis
            </Typography>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} md={4}>
                <Chip
                  label={`Market Strength: ${marketData.investment_indicators?.market_strength}`}
                  color={
                    marketData.investment_indicators?.market_strength === 'Strong'
                      ? 'success'
                      : marketData.investment_indicators?.market_strength === 'Moderate'
                      ? 'warning'
                      : 'error'
                  }
                  sx={{ mr: 1, mb: 1 }}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <Chip
                  label={marketData.investment_indicators?.cap_rate_analysis}
                  color="primary"
                  sx={{ mr: 1, mb: 1 }}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <Chip
                  label={`Demographics: ${marketData.investment_indicators?.demographic_quality}`}
                  color="info"
                  sx={{ mr: 1, mb: 1 }}
                />
              </Grid>
            </Grid>
          </Paper>

          {/* Comparable Properties */}
          {marketData.comparable_properties?.length > 0 && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Comparable Properties
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Address</TableCell>
                      <TableCell align="right">Price</TableCell>
                      <TableCell align="right">Beds</TableCell>
                      <TableCell align="right">Baths</TableCell>
                      <TableCell align="right">Sq Ft</TableCell>
                      <TableCell align="right">Distance</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {marketData.comparable_properties.map((comp: any, index: number) => (
                      <TableRow key={index}>
                        <TableCell>{comp.address}</TableCell>
                        <TableCell align="right">{formatCurrency(comp.price)}</TableCell>
                        <TableCell align="right">{comp.beds}</TableCell>
                        <TableCell align="right">{comp.baths}</TableCell>
                        <TableCell align="right">{formatNumber(comp.sqft)}</TableCell>
                        <TableCell align="right">{comp.distance_miles} mi</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          )}
        </>
      )}
    </Container>
  );
};

// Helper Components
const MetricRow: React.FC<{
  label: string;
  value: any;
  valueColor?: string;
}> = ({ label, value, valueColor }) => (
  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1.5 }}>
    <Typography variant="body2" color="text.secondary">
      {label}
    </Typography>
    <Typography variant="body2" fontWeight="600" color={valueColor || 'text.primary'}>
      {value || 'N/A'}
    </Typography>
  </Box>
);

const ScoreBar: React.FC<{ label: string; value: number }> = ({ label, value }) => (
  <Box sx={{ mb: 2 }}>
    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
      <Typography variant="body2" fontWeight="600">
        {value}
      </Typography>
    </Box>
    <LinearProgress
      variant="determinate"
      value={value}
      sx={{
        height: 8,
        borderRadius: 4,
        backgroundColor: 'rgba(0, 0, 0, 0.1)',
        '& .MuiLinearProgress-bar': {
          backgroundColor:
            value >= 70
              ? 'success.main'
              : value >= 50
              ? 'warning.main'
              : 'error.main',
        },
      }}
    />
  </Box>
);

// Helper Functions
const formatCurrency = (value: number | undefined) => {
  if (!value) return 'N/A';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

const formatNumber = (value: number | undefined) => {
  if (!value) return 'N/A';
  return new Intl.NumberFormat('en-US').format(value);
};
