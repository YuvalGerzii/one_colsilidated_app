/**
 * Property Comparison Heatmap Component
 * ======================================
 * Interactive visualization for comparing multiple real estate deals
 * Features: Heatmap, sorting, filtering, drill-down
 * Created: November 4, 2025
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box,
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Card,
  CardContent,
  Chip,
  Tooltip,
  IconButton,
} from '@mui/material';
import {
  Download as DownloadIcon,
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';

interface Deal {
  deal_id: string;
  property_name: string;
  property_type: string;
  city: string;
  state: string;
  overall_rank: number;
  overall_score: number;
  metrics: {
    levered_irr: number;
    equity_multiple: number;
    cash_on_cash_y1: number;
    dscr_year1: number;
    entry_cap_rate: number;
    noi_margin: number;
  };
}

interface ComparisonData {
  comparison_id: string;
  comparison_name: string;
  deals: Deal[];
}

const PropertyComparisonHeatmap: React.FC<{ comparisonId: string }> = ({ comparisonId }) => {
  const [comparisonData, setComparisonData] = useState<ComparisonData | null>(null);
  const [sortBy, setSortBy] = useState<string>('overall_score');
  const [filterType, setFilterType] = useState<string>('all');
  const [loading, setLoading] = useState<boolean>(true);
  const [hoveredDeal, setHoveredDeal] = useState<string | null>(null);

  // Fetch comparison data
  useEffect(() => {
    fetchComparisonData();
  }, [comparisonId]);

  const fetchComparisonData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/comparisons/${comparisonId}/deals`);
      setComparisonData(response.data);
    } catch (error) {
      console.error('Error fetching comparison data:', error);
    } finally {
      setLoading(false);
    }
  };

  const downloadICMemo = async () => {
    try {
      const response = await axios.get(`/api/comparisons/${comparisonId}/ic-memo`, {
        responseType: 'blob',
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `IC_Memo_${comparisonData?.comparison_name}.docx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading IC memo:', error);
    }
  };

  // Color coding for heatmap
  const getHeatmapColor = (value: number, metric: string): string => {
    // Normalize value to 0-1 scale based on metric
    let normalized = 0;
    
    if (metric === 'levered_irr') {
      // IRR: 0-30%
      normalized = Math.min(value * 100 / 30, 1);
    } else if (metric === 'equity_multiple') {
      // MOIC: 1-3x
      normalized = Math.min((value - 1) / 2, 1);
    } else if (metric === 'cash_on_cash_y1') {
      // CoC: 0-15%
      normalized = Math.min(value * 100 / 15, 1);
    } else if (metric === 'dscr_year1') {
      // DSCR: 1.0-2.0x
      normalized = Math.min((value - 1) / 1, 1);
    } else if (metric === 'entry_cap_rate') {
      // Cap Rate: 3-10%
      normalized = 1 - Math.min(value * 100 / 10, 1); // Inverse: lower cap = higher value
    } else if (metric === 'noi_margin') {
      // NOI Margin: 40-70%
      normalized = Math.min((value * 100 - 40) / 30, 1);
    }
    
    // Create gradient from red (0) to yellow (0.5) to green (1)
    if (normalized < 0.5) {
      const r = 255;
      const g = Math.round(255 * (normalized / 0.5));
      return `rgba(${r}, ${g}, 0, 0.6)`;
    } else {
      const r = Math.round(255 * (1 - (normalized - 0.5) / 0.5));
      const g = 255;
      return `rgba(${r}, ${g}, 0, 0.6)`;
    }
  };

  const formatMetric = (value: number | undefined, metric: string): string => {
    if (value === undefined || value === null) return 'N/A';
    
    switch (metric) {
      case 'levered_irr':
      case 'cash_on_cash_y1':
      case 'entry_cap_rate':
      case 'noi_margin':
        return `${(value * 100).toFixed(1)}%`;
      case 'equity_multiple':
      case 'dscr_year1':
        return `${value.toFixed(2)}x`;
      default:
        return value.toFixed(2);
    }
  };

  const getRankColor = (rank: number): string => {
    if (rank === 1) return '#FFD700'; // Gold
    if (rank === 2) return '#C0C0C0'; // Silver
    if (rank === 3) return '#CD7F32'; // Bronze
    return '#E0E0E0'; // Gray
  };

  const getScoreChip = (score: number): JSX.Element => {
    let color: 'success' | 'warning' | 'error' = 'error';
    let label = 'Low';
    
    if (score >= 80) {
      color = 'success';
      label = 'Excellent';
    } else if (score >= 60) {
      color = 'warning';
      label = 'Good';
    }
    
    return <Chip label={`${score.toFixed(0)} - ${label}`} color={color} size="small" />;
  };

  // Filter and sort deals
  const getFilteredDeals = (): Deal[] => {
    if (!comparisonData) return [];
    
    let filtered = [...comparisonData.deals];
    
    // Apply property type filter
    if (filterType !== 'all') {
      filtered = filtered.filter(deal => deal.property_type === filterType);
    }
    
    // Apply sort
    filtered.sort((a, b) => {
      if (sortBy === 'overall_score') {
        return b.overall_score - a.overall_score;
      } else if (sortBy === 'overall_rank') {
        return a.overall_rank - b.overall_rank;
      } else {
        const aValue = a.metrics[sortBy as keyof typeof a.metrics] || 0;
        const bValue = b.metrics[sortBy as keyof typeof b.metrics] || 0;
        return bValue - aValue;
      }
    });
    
    return filtered;
  };

  if (loading) {
    return <Typography>Loading comparison data...</Typography>;
  }

  if (!comparisonData) {
    return <Typography>No data available</Typography>;
  }

  const filteredDeals = getFilteredDeals();
  const metrics = ['levered_irr', 'equity_multiple', 'cash_on_cash_y1', 'dscr_year1', 'entry_cap_rate', 'noi_margin'];
  const metricLabels: { [key: string]: string } = {
    levered_irr: 'Levered IRR',
    equity_multiple: 'MOIC',
    cash_on_cash_y1: 'CoC Y1',
    dscr_year1: 'DSCR',
    entry_cap_rate: 'Entry Cap',
    noi_margin: 'NOI Margin',
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <Typography variant="h4" gutterBottom>
              {comparisonData.comparison_name}
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Comparing {comparisonData.deals.length} Properties
            </Typography>
          </Grid>
          <Grid item xs={12} md={6} sx={{ textAlign: 'right' }}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<DownloadIcon />}
              onClick={downloadICMemo}
              sx={{ mr: 2 }}
            >
              Export IC Memo
            </Button>
            <IconButton onClick={fetchComparisonData} color="primary">
              <RefreshIcon />
            </IconButton>
          </Grid>
        </Grid>
      </Paper>

      {/* Filters and Sort */}
      <Paper elevation={2} sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={4}>
            <FormControl fullWidth>
              <InputLabel>Sort By</InputLabel>
              <Select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                label="Sort By"
              >
                <MenuItem value="overall_score">Overall Score</MenuItem>
                <MenuItem value="overall_rank">Rank</MenuItem>
                <MenuItem value="levered_irr">Levered IRR</MenuItem>
                <MenuItem value="equity_multiple">Equity Multiple</MenuItem>
                <MenuItem value="cash_on_cash_y1">Cash-on-Cash</MenuItem>
                <MenuItem value="dscr_year1">DSCR</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <FormControl fullWidth>
              <InputLabel>Property Type</InputLabel>
              <Select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                label="Property Type"
              >
                <MenuItem value="all">All Types</MenuItem>
                <MenuItem value="Multifamily">Multifamily</MenuItem>
                <MenuItem value="Mixed-Use">Mixed-Use</MenuItem>
                <MenuItem value="Hotel">Hotel</MenuItem>
                <MenuItem value="SFR">Single Family</MenuItem>
                <MenuItem value="House Flipping">House Flipping</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* Top 3 Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {filteredDeals.slice(0, 3).map((deal, index) => (
          <Grid item xs={12} md={4} key={deal.deal_id}>
            <Card
              elevation={3}
              sx={{
                border: `3px solid ${getRankColor(index + 1)}`,
                position: 'relative',
              }}
            >
              <Box
                sx={{
                  position: 'absolute',
                  top: 10,
                  right: 10,
                  bgcolor: getRankColor(index + 1),
                  color: 'white',
                  borderRadius: '50%',
                  width: 40,
                  height: 40,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 'bold',
                }}
              >
                #{index + 1}
              </Box>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {deal.property_name}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {deal.property_type} | {deal.city}, {deal.state}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  {getScoreChip(deal.overall_score)}
                </Box>
                <Grid container spacing={1} sx={{ mt: 2 }}>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      Levered IRR
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {formatMetric(deal.metrics.levered_irr, 'levered_irr')}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      MOIC
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {formatMetric(deal.metrics.equity_multiple, 'equity_multiple')}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      DSCR
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {formatMetric(deal.metrics.dscr_year1, 'dscr_year1')}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      CoC Y1
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {formatMetric(deal.metrics.cash_on_cash_y1, 'cash_on_cash_y1')}
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Heatmap Table */}
      <Paper elevation={3}>
        <TableContainer>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell align="center" sx={{ fontWeight: 'bold', bgcolor: '#f5f5f5' }}>
                  Rank
                </TableCell>
                <TableCell sx={{ fontWeight: 'bold', bgcolor: '#f5f5f5' }}>
                  Property
                </TableCell>
                <TableCell sx={{ fontWeight: 'bold', bgcolor: '#f5f5f5' }}>
                  Type
                </TableCell>
                <TableCell sx={{ fontWeight: 'bold', bgcolor: '#f5f5f5' }}>
                  Location
                </TableCell>
                {metrics.map((metric) => (
                  <TableCell
                    key={metric}
                    align="center"
                    sx={{ fontWeight: 'bold', bgcolor: '#f5f5f5' }}
                  >
                    {metricLabels[metric]}
                  </TableCell>
                ))}
                <TableCell align="center" sx={{ fontWeight: 'bold', bgcolor: '#f5f5f5' }}>
                  Score
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredDeals.map((deal) => (
                <TableRow
                  key={deal.deal_id}
                  onMouseEnter={() => setHoveredDeal(deal.deal_id)}
                  onMouseLeave={() => setHoveredDeal(null)}
                  sx={{
                    '&:hover': { bgcolor: '#f9f9f9' },
                    cursor: 'pointer',
                  }}
                >
                  <TableCell align="center">
                    <Box
                      sx={{
                        bgcolor: getRankColor(deal.overall_rank),
                        color: deal.overall_rank <= 3 ? 'white' : 'black',
                        borderRadius: 1,
                        px: 1,
                        py: 0.5,
                        fontWeight: 'bold',
                      }}
                    >
                      #{deal.overall_rank}
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="medium">
                      {deal.property_name}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip label={deal.property_type} size="small" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {deal.city}, {deal.state}
                    </Typography>
                  </TableCell>
                  {metrics.map((metric) => {
                    const value = deal.metrics[metric as keyof typeof deal.metrics];
                    return (
                      <Tooltip
                        key={metric}
                        title={`${metricLabels[metric]}: ${formatMetric(value, metric)}`}
                      >
                        <TableCell
                          align="center"
                          sx={{
                            bgcolor: getHeatmapColor(value, metric),
                            fontWeight: 'medium',
                          }}
                        >
                          {formatMetric(value, metric)}
                        </TableCell>
                      </Tooltip>
                    );
                  })}
                  <TableCell align="center">{getScoreChip(deal.overall_score)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
};

export default PropertyComparisonHeatmap;
