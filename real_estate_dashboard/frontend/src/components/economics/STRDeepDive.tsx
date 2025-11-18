import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Stack,
  TextField,
  MenuItem,
  Alert,
  CircularProgress,
  Paper,
  Chip,
  Divider,
  alpha,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Business as BusinessIcon,
  Gavel as GavelIcon,
  People as PeopleIcon,
  AttachMoney as MoneyIcon,
  Home as HomeIcon,
  Assessment as AssessmentIcon,
  DataUsage as DataUsageIcon,
  LocalOffer as PriceIcon,
  ShowChart as ChartIcon,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { useAppTheme } from '../../contexts/ThemeContext';
import { api } from '../../services/apiClient';

interface STRCategory {
  id: string;
  label: string;
  icon: any;
  endpoint: string;
  color: string;
}

const STR_CATEGORIES: STRCategory[] = [
  { id: 'competitive', label: 'Competitive Analysis', icon: BusinessIcon, endpoint: '/market-intelligence/data/str-analytics/competitive-analysis', color: '#3b82f6' },
  { id: 'compliance', label: 'Compliance Enforcement', icon: GavelIcon, endpoint: '/market-intelligence/data/str-analytics/compliance-enforcement', color: '#ef4444' },
  { id: 'demographics', label: 'Guest Demographics', icon: PeopleIcon, endpoint: '/market-intelligence/data/str-analytics/guest-demographics', color: '#10b981' },
  { id: 'economics', label: 'Host Economics', icon: MoneyIcon, endpoint: '/market-intelligence/data/str-analytics/host-economics', color: '#f59e0b' },
  { id: 'impact', label: 'Housing Market Impact', icon: HomeIcon, endpoint: '/market-intelligence/data/str-analytics/housing-market-impact', color: '#8b5cf6' },
  { id: 'investment', label: 'Investment Analysis', icon: AssessmentIcon, endpoint: '/market-intelligence/data/str-analytics/investment-analysis', color: '#06b6d4' },
  { id: 'platform', label: 'Platform Performance', icon: DataUsageIcon, endpoint: '/market-intelligence/data/str-analytics/platform-performance', color: '#ec4899' },
  { id: 'pricing', label: 'Pricing Patterns', icon: PriceIcon, endpoint: '/market-intelligence/data/str-analytics/pricing-patterns', color: '#14b8a6' },
  { id: 'supply-demand', label: 'Supply-Demand Dynamics', icon: ChartIcon, endpoint: '/market-intelligence/data/str-analytics/supply-demand', color: '#f43f5e' },
];

const STRDeepDive: React.FC = () => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [selectedCategory, setSelectedCategory] = useState<string>('competitive');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [strData, setStrData] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetchSTRData();
  }, [selectedCategory]);

  const fetchSTRData = async () => {
    try {
      setLoading(true);
      setError(null);

      const category = STR_CATEGORIES.find(c => c.id === selectedCategory);
      if (!category) return;

      const response = await api.get(category.endpoint, {
        params: { limit: 100 }
      });

      setStrData(response.data.data || []);

      // Calculate basic statistics
      if (response.data.data && response.data.data.length > 0) {
        calculateStats(response.data.data);
      }
    } catch (error: any) {
      console.error('Error fetching STR data:', error);
      setError('Failed to load STR data');
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (data: any[]) => {
    // Calculate category-specific statistics
    const totalRecords = data.length;

    // Get unique cities/locations
    const cities = new Set(data.map(d => d.city || d.location).filter(Boolean));

    setStats({
      totalRecords,
      uniqueCities: cities.size,
      dataPoints: data.length,
    });
  };

  const renderCategoryContent = () => {
    if (loading) {
      return (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <CircularProgress size={48} />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Loading STR data...
          </Typography>
        </Box>
      );
    }

    if (error) {
      return (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      );
    }

    if (!strData || strData.length === 0) {
      return (
        <Alert severity="info" sx={{ mb: 3 }}>
          No data available for this category. The data may still be importing or there may be no records for this category.
        </Alert>
      );
    }

    // Render data table for all categories
    return (
      <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {Object.keys(strData[0]).filter(key => key !== 'id').slice(0, 8).map((key) => (
                <TableCell key={key} sx={{ fontWeight: 700, textTransform: 'capitalize' }}>
                  {key.replace(/_/g, ' ')}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {strData.slice(0, 50).map((row, idx) => (
              <TableRow key={idx} hover>
                {Object.entries(row).filter(([key]) => key !== 'id').slice(0, 8).map(([key, value], cellIdx) => (
                  <TableCell key={cellIdx}>
                    {typeof value === 'number'
                      ? value.toLocaleString()
                      : value !== null && value !== undefined
                        ? String(value)
                        : 'N/A'}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {strData.length > 50 && (
          <Box sx={{ p: 2, textAlign: 'center', bgcolor: isDark ? 'rgba(59, 130, 246, 0.05)' : 'rgba(59, 130, 246, 0.02)' }}>
            <Typography variant="body2" color="text.secondary">
              Showing first 50 of {strData.length} records
            </Typography>
          </Box>
        )}
      </TableContainer>
    );
  };

  const currentCategory = STR_CATEGORIES.find(c => c.id === selectedCategory);
  const CategoryIcon = currentCategory?.icon || BusinessIcon;

  return (
    <Stack spacing={4}>
      {/* Header */}
      <Card>
        <CardContent>
          <Stack spacing={3}>
            <Stack direction="row" alignItems="center" spacing={2}>
              <Box
                sx={{
                  width: 56,
                  height: 56,
                  borderRadius: 3,
                  background: `linear-gradient(135deg, ${currentCategory?.color || '#3b82f6'} 0%, ${alpha(currentCategory?.color || '#3b82f6', 0.7)} 100%)`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: `0 4px 16px ${alpha(currentCategory?.color || '#3b82f6', 0.3)}`,
                }}
              >
                <CategoryIcon sx={{ fontSize: 32, color: 'white' }} />
              </Box>
              <Box sx={{ flex: 1 }}>
                <Typography variant="h5" sx={{ fontWeight: 700 }}>
                  {currentCategory?.label}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Short-Term Rental (STR) analytics and market intelligence
                </Typography>
              </Box>
            </Stack>

            <Divider />

            {/* Category Selector */}
            <TextField
              fullWidth
              select
              label="Select STR Analytics Category"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              size="medium"
            >
              {STR_CATEGORIES.map((category) => (
                <MenuItem key={category.id} value={category.id}>
                  <Stack direction="row" alignItems="center" spacing={1}>
                    <category.icon sx={{ fontSize: 20, color: category.color }} />
                    <Typography>{category.label}</Typography>
                  </Stack>
                </MenuItem>
              ))}
            </TextField>
          </Stack>
        </CardContent>
      </Card>

      {/* Statistics Cards */}
      {stats && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card
              sx={{
                background: `linear-gradient(135deg, ${currentCategory?.color} 0%, ${alpha(currentCategory?.color || '#3b82f6', 0.7)} 100%)`,
                color: 'white',
              }}
            >
              <CardContent>
                <Typography variant="body2" sx={{ opacity: 0.9, mb: 1 }}>
                  Total Records
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700 }}>
                  {stats.totalRecords}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  Unique Cities/Locations
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: '#10b981' }}>
                  {stats.uniqueCities}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  Data Points
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: '#3b82f6' }}>
                  {stats.dataPoints}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Category Content */}
      <Card>
        <CardContent>
          {renderCategoryContent()}
        </CardContent>
      </Card>

      {/* Info Alert */}
      <Alert severity="info" icon={<AssessmentIcon />}>
        <Typography variant="body2" sx={{ fontWeight: 600 }}>
          STR Analytics Data Sources:
        </Typography>
        <Typography variant="caption" component="div">
          • All data is loaded from comprehensive CSV files covering 9 STR analytics categories
        </Typography>
        <Typography variant="caption" component="div">
          • Data includes competitive analysis, compliance, demographics, economics, market impact, and more
        </Typography>
        <Typography variant="caption" component="div" sx={{ mt: 1 }}>
          Data is cached for optimal performance
        </Typography>
      </Alert>
    </Stack>
  );
};

export default STRDeepDive;
