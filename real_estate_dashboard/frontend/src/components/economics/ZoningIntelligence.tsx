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
  Landscape as LandscapeIcon,
  AccountBalance as GovernmentIcon,
  Block as BarrierIcon,
  DirectionsTransit as TransitIcon,
  Assessment as MetricsIcon,
  LocationCity as CityIcon,
  TrendingUp as TrendingUpIcon,
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

interface ZoningCategory {
  id: string;
  label: string;
  icon: any;
  endpoint: string;
  color: string;
  description: string;
}

const ZONING_CATEGORIES: ZoningCategory[] = [
  {
    id: 'entitled-land',
    label: 'Entitled Land Inventory',
    icon: LandscapeIcon,
    endpoint: '/market-intelligence/data/zoning/entitled-land',
    color: '#10b981',
    description: 'Parcels with development rights and entitlements'
  },
  {
    id: 'future-initiatives',
    label: 'Future Zoning Initiatives',
    icon: GovernmentIcon,
    endpoint: '/market-intelligence/data/zoning/future-initiatives',
    color: '#3b82f6',
    description: 'Upcoming zoning changes and policy initiatives'
  },
  {
    id: 'regulatory-barriers',
    label: 'Regulatory Barriers',
    icon: BarrierIcon,
    endpoint: '/market-intelligence/data/zoning/regulatory-barriers',
    color: '#ef4444',
    description: 'Constraints and obstacles to development'
  },
  {
    id: 'tod',
    label: 'Transit-Oriented Development',
    icon: TransitIcon,
    endpoint: '/market-intelligence/data/zoning/tod',
    color: '#8b5cf6',
    description: 'Development near public transit hubs'
  },
  {
    id: 'master-metrics',
    label: 'Zoning Master Metrics',
    icon: MetricsIcon,
    endpoint: '/market-intelligence/data/zoning/master-metrics',
    color: '#f59e0b',
    description: 'Comprehensive zoning analytics and KPIs'
  },
];

const ZoningIntelligence: React.FC = () => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [selectedCategory, setSelectedCategory] = useState<string>('entitled-land');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [zoningData, setZoningData] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetchZoningData();
  }, [selectedCategory]);

  const fetchZoningData = async () => {
    try {
      setLoading(true);
      setError(null);

      const category = ZONING_CATEGORIES.find(c => c.id === selectedCategory);
      if (!category) return;

      const response = await api.get(category.endpoint, {
        params: { limit: 100 }
      });

      setZoningData(response.data.data || []);

      // Calculate basic statistics
      if (response.data.data && response.data.data.length > 0) {
        calculateStats(response.data.data);
      }
    } catch (error: any) {
      console.error('Error fetching zoning data:', error);
      setError('Failed to load zoning data');
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (data: any[]) => {
    const totalRecords = data.length;

    // Get unique cities/locations
    const cities = new Set(data.map(d => d.city || d.location || d.jurisdiction).filter(Boolean));

    // Calculate category-specific stats
    let additionalStats: any = {};

    if (selectedCategory === 'entitled-land') {
      const statuses = data.map(d => d.development_status).filter(Boolean);
      additionalStats.developmentStatuses = new Set(statuses).size;
    } else if (selectedCategory === 'tod') {
      const avgDistance = data.reduce((sum, d) => sum + (parseFloat(d.distance_to_transit_km) || 0), 0) / data.length;
      additionalStats.avgTransitDistance = avgDistance.toFixed(2);
    }

    setStats({
      totalRecords,
      uniqueLocations: cities.size,
      dataPoints: data.length,
      ...additionalStats,
    });
  };

  const renderCategoryContent = () => {
    if (loading) {
      return (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <CircularProgress size={48} />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Loading zoning data...
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

    if (!zoningData || zoningData.length === 0) {
      return (
        <Alert severity="info" sx={{ mb: 3 }}>
          No data available for this category. The data may still be importing or there may be no records for this category.
        </Alert>
      );
    }

    // Render data table for all categories
    const columns = Object.keys(zoningData[0]).filter(key => key !== 'id').slice(0, 8);

    return (
      <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {columns.map((key) => (
                <TableCell key={key} sx={{ fontWeight: 700, textTransform: 'capitalize', bgcolor: isDark ? '#1f2937' : '#f9fafb' }}>
                  {key.replace(/_/g, ' ')}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {zoningData.slice(0, 50).map((row, idx) => (
              <TableRow key={idx} hover>
                {columns.map((key, cellIdx) => (
                  <TableCell key={cellIdx}>
                    {typeof row[key] === 'number'
                      ? row[key].toLocaleString()
                      : row[key] !== null && row[key] !== undefined
                        ? String(row[key])
                        : 'N/A'}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {zoningData.length > 50 && (
          <Box sx={{ p: 2, textAlign: 'center', bgcolor: isDark ? 'rgba(59, 130, 246, 0.05)' : 'rgba(59, 130, 246, 0.02)' }}>
            <Typography variant="body2" color="text.secondary">
              Showing first 50 of {zoningData.length} records
            </Typography>
          </Box>
        )}
      </TableContainer>
    );
  };

  const currentCategory = ZONING_CATEGORIES.find(c => c.id === selectedCategory);
  const CategoryIcon = currentCategory?.icon || LandscapeIcon;

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
                  {currentCategory?.description}
                </Typography>
              </Box>
            </Stack>

            <Divider />

            {/* Category Selector */}
            <TextField
              fullWidth
              select
              label="Select Zoning Intelligence Category"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              size="medium"
            >
              {ZONING_CATEGORIES.map((category) => (
                <MenuItem key={category.id} value={category.id}>
                  <Stack direction="row" alignItems="center" spacing={1}>
                    <category.icon sx={{ fontSize: 20, color: category.color }} />
                    <Box>
                      <Typography>{category.label}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {category.description}
                      </Typography>
                    </Box>
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
                  Unique Locations
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: '#10b981' }}>
                  {stats.uniqueLocations}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {selectedCategory === 'tod' && stats.avgTransitDistance
                    ? 'Avg Transit Distance (km)'
                    : 'Data Points'}
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: '#3b82f6' }}>
                  {selectedCategory === 'tod' && stats.avgTransitDistance
                    ? stats.avgTransitDistance
                    : stats.dataPoints}
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
      <Alert severity="info" icon={<CityIcon />}>
        <Typography variant="body2" sx={{ fontWeight: 600 }}>
          Zoning Intelligence Data Sources:
        </Typography>
        <Typography variant="caption" component="div">
          • Comprehensive zoning data across 5 categories covering land entitlements, regulations, and development
        </Typography>
        <Typography variant="caption" component="div">
          • Includes entitled land inventory, future initiatives, regulatory barriers, TOD opportunities, and master metrics
        </Typography>
        <Typography variant="caption" component="div" sx={{ mt: 1 }}>
          Data is cached for optimal performance
        </Typography>
      </Alert>
    </Stack>
  );
};

export default ZoningIntelligence;
