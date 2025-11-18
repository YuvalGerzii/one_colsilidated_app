// src/pages/PropertyManagement/components/PropertyDashboard.tsx
import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Stack,
  Chip,
  Divider,
  LinearProgress,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Avatar,
  useTheme,
  Alert,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  HomeWork as HomeWorkIcon,
  MeetingRoom as MeetingRoomIcon,
} from '@mui/icons-material';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { useAppTheme } from '../../../contexts/ThemeContext';
import { useCompany } from '../../../context/CompanyContext';

const COLORS = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899'];

// NOTE: Sample data removed - dashboard is now company-specific
// Each company will have its own isolated portfolio metrics

const PropertyDashboard: React.FC = () => {
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const { selectedCompany } = useCompany();
  const isDark = theme === 'dark';

  // Company-specific data (currently empty - will be loaded from backend API)
  const monthlyNOI = selectedCompany ? [] : [];
  const occupancyByProperty = selectedCompany ? [] : [];
  const propertyTypeDistribution = selectedCompany ? [] : [];
  const hasData = monthlyNOI.length > 0 && occupancyByProperty.length > 0;

  return (
    <Grid container spacing={3}>
      {/* Key Performance Indicators */}
      <Grid item xs={12}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Typography variant="h6" gutterBottom fontWeight="bold">
            Portfolio Overview {selectedCompany && `- ${selectedCompany.name}`}
          </Typography>
        </Stack>
      </Grid>

      {/* Company Selection & Empty State Alerts */}
      {!selectedCompany ? (
        <Grid item xs={12}>
          <Alert severity="info">
            Please select a company to view portfolio dashboard.
          </Alert>
        </Grid>
      ) : !hasData ? (
        <Grid item xs={12}>
          <Alert severity="info">
            No portfolio data found for {selectedCompany.name}. Add properties to see dashboard metrics and analytics.
          </Alert>
        </Grid>
      ) : null}

      {/* Financial Performance */}
      {selectedCompany && hasData && (
      <Grid item xs={12} lg={8}>
        <Paper sx={{ p: 3, height: '100%' }}>
          <Typography variant="h6" gutterBottom>
            Monthly NOI & Cash Flow Trend
          </Typography>
          <Box sx={{ height: 300, mt: 2 }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monthlyNOI}>
                <defs>
                  <linearGradient id="colorNOI" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#1976d2" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#1976d2" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorCF" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2e7d32" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#2e7d32" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke={isDark ? '#334155' : '#e2e8f0'}
                  opacity={0.2}
                />
                <XAxis
                  dataKey="month"
                  stroke={isDark ? '#94a3b8' : '#64748b'}
                  fontSize={12}
                />
                <YAxis
                  stroke={isDark ? '#94a3b8' : '#64748b'}
                  fontSize={12}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: isDark ? '#1e293b' : '#fff',
                    border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                    borderRadius: '12px',
                    color: isDark ? '#fff' : '#000',
                  }}
                  formatter={(value: number) => `$${value.toLocaleString()}`}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="noi"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorNOI)"
                  name="Net Operating Income"
                />
                <Area
                  type="monotone"
                  dataKey="cashFlow"
                  stroke="#10b981"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorCF)"
                  name="Cash Flow"
                />
              </AreaChart>
            </ResponsiveContainer>
          </Box>
        </Paper>
      </Grid>

      )}

      {/* Property Type Distribution */}
      {selectedCompany && hasData && (
      <Grid item xs={12} lg={4}>
        <Paper sx={{ p: 3, height: '100%' }}>
          <Typography variant="h6" gutterBottom>
            Portfolio Mix
          </Typography>
          <Box sx={{ height: 300, mt: 2 }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={propertyTypeDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {propertyTypeDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: isDark ? '#1e293b' : '#fff',
                    border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                    borderRadius: '12px',
                    color: isDark ? '#fff' : '#000',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </Box>
        </Paper>
      </Grid>

      )}

      {/* Occupancy Rates by Property */}
      {selectedCompany && hasData && (
      <Grid item xs={12} lg={6}>
        <Paper sx={{ p: 3, height: '100%' }}>
          <Typography variant="h6" gutterBottom>
            Occupancy Rates by Property
          </Typography>
          <Box sx={{ height: 300, mt: 2 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={occupancyByProperty} layout="horizontal">
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke={isDark ? '#334155' : '#e2e8f0'}
                  opacity={0.2}
                />
                <XAxis
                  type="number"
                  domain={[0, 100]}
                  stroke={isDark ? '#94a3b8' : '#64748b'}
                  fontSize={12}
                />
                <YAxis
                  dataKey="name"
                  type="category"
                  width={120}
                  stroke={isDark ? '#94a3b8' : '#64748b'}
                  fontSize={12}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: isDark ? '#1e293b' : '#fff',
                    border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                    borderRadius: '12px',
                    color: isDark ? '#fff' : '#000',
                  }}
                  formatter={(value: number) => `${value}%`}
                />
                <Bar dataKey="value" fill="#3b82f6" name="Occupancy %" />
              </BarChart>
            </ResponsiveContainer>
          </Box>
        </Paper>
      </Grid>

      )}

      {/* Critical Alerts & Actions */}
      {selectedCompany && hasData && (
      <Grid item xs={12} lg={6}>
        <Paper sx={{ p: 3, height: '100%' }}>
          <Typography variant="h6" gutterBottom>
            Critical Alerts & Actions
          </Typography>
          <Alert severity="info">
            No critical alerts at this time for {selectedCompany.name}.
          </Alert>
        </Paper>
      </Grid>
      )}

      {/* Key Metrics Cards */}
      {selectedCompany && hasData && (
        <>
          <Grid item xs={12} md={6} lg={3}>
            <Card elevation={2}>
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                  <Box>
                    <Typography color="text.secondary" gutterBottom variant="caption">
                      Portfolio Value
                    </Typography>
                    <Typography variant="h5" fontWeight="bold">
                      $0
                    </Typography>
                    <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        No data
                      </Typography>
                    </Stack>
                  </Box>
                  <HomeWorkIcon color="primary" />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6} lg={3}>
            <Card elevation={2}>
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                  <Box>
                    <Typography color="text.secondary" gutterBottom variant="caption">
                      Total Equity
                    </Typography>
                    <Typography variant="h5" fontWeight="bold">
                      $0
                    </Typography>
                    <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        No data
                      </Typography>
                    </Stack>
                  </Box>
                  <MeetingRoomIcon color="success" />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6} lg={3}>
            <Card elevation={2}>
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                  <Box>
                    <Typography color="text.secondary" gutterBottom variant="caption">
                      Portfolio Cap Rate
                    </Typography>
                    <Typography variant="h5" fontWeight="bold">
                      0%
                    </Typography>
                    <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        No data
                      </Typography>
                    </Stack>
                  </Box>
                  <TrendingUpIcon color="info" />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6} lg={3}>
            <Card elevation={2}>
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                  <Box>
                    <Typography color="text.secondary" gutterBottom variant="caption">
                      Cash-on-Cash Return
                    </Typography>
                    <Typography variant="h5" fontWeight="bold">
                      0%
                    </Typography>
                    <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        No data
                      </Typography>
                    </Stack>
                  </Box>
                  <TrendingUpIcon color="warning" />
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </>
      )}
    </Grid>
  );
};

export default PropertyDashboard;
