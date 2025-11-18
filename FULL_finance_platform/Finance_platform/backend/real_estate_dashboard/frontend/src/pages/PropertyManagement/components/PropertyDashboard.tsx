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

const COLORS = ['#1976d2', '#42a5f5', '#2e7d32', '#ff9800', '#9c27b0'];

// Sample data - in real app would come from API
const monthlyNOI = [
  { month: 'Jan', noi: 82000, cashFlow: 65000 },
  { month: 'Feb', noi: 84000, cashFlow: 67000 },
  { month: 'Mar', noi: 83500, cashFlow: 66500 },
  { month: 'Apr', noi: 85000, cashFlow: 68000 },
  { month: 'May', noi: 86500, cashFlow: 69500 },
  { month: 'Jun', noi: 85200, cashFlow: 68200 },
];

const occupancyByProperty = [
  { name: 'Maple Apartments', value: 96 },
  { name: 'Oak Plaza', value: 92 },
  { name: 'Pine Tower', value: 98 },
  { name: 'Cedar Heights', value: 89 },
  { name: 'Birch Estates', value: 95 },
];

const propertyTypeDistribution = [
  { name: 'Multifamily', value: 45 },
  { name: 'Single Family', value: 25 },
  { name: 'Commercial', value: 20 },
  { name: 'Mixed-Use', value: 10 },
];

const PropertyDashboard: React.FC = () => {
  return (
    <Grid container spacing={3}>
      {/* Key Performance Indicators */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom fontWeight="bold">
          Portfolio Overview
        </Typography>
      </Grid>

      {/* Financial Performance */}
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
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip
                  formatter={(value: number) => `$${value.toLocaleString()}`}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="noi"
                  stroke="#1976d2"
                  fillOpacity={1}
                  fill="url(#colorNOI)"
                  name="Net Operating Income"
                />
                <Area
                  type="monotone"
                  dataKey="cashFlow"
                  stroke="#2e7d32"
                  fillOpacity={1}
                  fill="url(#colorCF)"
                  name="Cash Flow"
                />
              </AreaChart>
            </ResponsiveContainer>
          </Box>
        </Paper>
      </Grid>

      {/* Property Type Distribution */}
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
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Box>
        </Paper>
      </Grid>

      {/* Occupancy Rates by Property */}
      <Grid item xs={12} lg={6}>
        <Paper sx={{ p: 3, height: '100%' }}>
          <Typography variant="h6" gutterBottom>
            Occupancy Rates by Property
          </Typography>
          <Box sx={{ height: 300, mt: 2 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={occupancyByProperty} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 100]} />
                <YAxis dataKey="name" type="category" width={120} />
                <Tooltip formatter={(value: number) => `${value}%`} />
                <Bar dataKey="value" fill="#1976d2" name="Occupancy %" />
              </BarChart>
            </ResponsiveContainer>
          </Box>
        </Paper>
      </Grid>

      {/* Critical Alerts & Actions */}
      <Grid item xs={12} lg={6}>
        <Paper sx={{ p: 3, height: '100%' }}>
          <Typography variant="h6" gutterBottom>
            Critical Alerts & Actions
          </Typography>
          <List>
            <ListItem>
              <ListItemIcon>
                <Avatar sx={{ bgcolor: 'error.main' }}>
                  <WarningIcon />
                </Avatar>
              </ListItemIcon>
              <ListItemText
                primary="3 Leases Expiring in 30 Days"
                secondary="Contact tenants: Unit 2A (Maple), Unit 5B (Oak), Unit 12C (Pine)"
              />
            </ListItem>
            <Divider />
            <ListItem>
              <ListItemIcon>
                <Avatar sx={{ bgcolor: 'warning.main' }}>
                  <ErrorIcon />
                </Avatar>
              </ListItemIcon>
              <ListItemText
                primary="8 Vacant Units"
                secondary="Average vacancy: 15 days. Market units actively."
              />
            </ListItem>
            <Divider />
            <ListItem>
              <ListItemIcon>
                <Avatar sx={{ bgcolor: 'info.main' }}>
                  <CheckCircleIcon />
                </Avatar>
              </ListItemIcon>
              <ListItemText
                primary="5 Maintenance Requests Open"
                secondary="2 emergency, 3 routine. All assigned to vendors."
              />
            </ListItem>
            <Divider />
            <ListItem>
              <ListItemIcon>
                <Avatar sx={{ bgcolor: 'success.main' }}>
                  <TrendingUpIcon />
                </Avatar>
              </ListItemIcon>
              <ListItemText
                primary="Portfolio NOI Up 3.2%"
                secondary="Month-over-month growth driven by rent increases"
              />
            </ListItem>
          </List>
        </Paper>
      </Grid>

      {/* Key Metrics Cards */}
      <Grid item xs={12} md={6} lg={3}>
        <Card elevation={2}>
          <CardContent>
            <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
              <Box>
                <Typography color="text.secondary" gutterBottom variant="caption">
                  Portfolio Value
                </Typography>
                <Typography variant="h5" fontWeight="bold">
                  $18.5M
                </Typography>
                <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1 }}>
                  <TrendingUpIcon fontSize="small" color="success" />
                  <Typography variant="caption" color="success.main">
                    +5.2% YoY
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
                  $4.6M
                </Typography>
                <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1 }}>
                  <Typography variant="caption" color="text.secondary">
                    25% LTV Ratio
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
                  6.8%
                </Typography>
                <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1 }}>
                  <Typography variant="caption" color="text.secondary">
                    Above market avg
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
                  9.4%
                </Typography>
                <Stack direction="row" alignItems="center" spacing={0.5} sx={{ mt: 1 }}>
                  <TrendingUpIcon fontSize="small" color="success" />
                  <Typography variant="caption" color="success.main">
                    Strong returns
                  </Typography>
                </Stack>
              </Box>
              <TrendingUpIcon color="warning" />
            </Stack>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default PropertyDashboard;
