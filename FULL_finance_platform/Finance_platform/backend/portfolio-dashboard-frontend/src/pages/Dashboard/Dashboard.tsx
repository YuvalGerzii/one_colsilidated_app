// src/pages/Dashboard/Dashboard.tsx
import React, { useMemo } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Stack,
  Chip,
  Divider,
  Button,
  IconButton,
  Tooltip,
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbarQuickFilter } from '@mui/x-data-grid';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip as ChartTooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import {
  Description as DescriptionIcon,
  HomeWork as HomeWorkIcon,
  Timeline as TimelineIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ShowChart as ShowChartIcon,
  PieChart as PieChartIcon,
  Refresh as RefreshIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useCompanies } from '../../hooks/useCompanies';
import { formatCurrency, formatPercent } from '../../utils/formatters';
import { DashboardSkeleton } from '../../components/common/LoadingSkeleton';
import { EmptyState } from '../../components/common/EmptyState';
import { ErrorState } from '../../components/common/ErrorState';

const COLORS = ['#1976d2', '#42a5f5', '#2e7d32', '#1565c0', '#9c27b0', '#ef6c00'];

const QuickSearchToolbar = () => (
  <Box sx={{ p: 1 }}>
    <GridToolbarQuickFilter quickFilterParser={(value) => value.split(/\s+/).filter(Boolean)} />
  </Box>
);

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { companies, loading, error, refetch } = useCompanies();

  // All hooks must be called before any conditional returns
  const kpis = useMemo(() => {
    const totalRevenue = companies.reduce((sum, company) => sum + (company.entry_revenue || 0), 0);
    const totalEbitda = companies.reduce((sum, company) => sum + (company.entry_ebitda || 0), 0);
    const totalCashFlow = companies.reduce(
      (sum, company) => sum + ((company.entry_ebitda || 0) * 0.6),
      0
    );
    const roiValues = companies
      .map((company) => {
        if (company.realized_moic) {
          return company.realized_moic - 1;
        }
        if (company.entry_multiple) {
          return company.entry_multiple - 1;
        }
        return null;
      })
      .filter((value): value is number => value !== null && !Number.isNaN(value));
    const avgRoi = roiValues.length
      ? roiValues.reduce((sum, value) => sum + value, 0) / roiValues.length
      : 0;

    return {
      revenue: totalRevenue,
      ebitda: totalEbitda,
      cashFlow: totalCashFlow,
      roi: avgRoi,
    };
  }, [companies]);

  const revenueTrend = useMemo(() => {
    const yearly = new Map<string, { revenue: number; ebitda: number }>();
    companies.forEach((company) => {
      const year = new Date(company.investment_date).getFullYear().toString();
      const bucket = yearly.get(year) || { revenue: 0, ebitda: 0 };
      bucket.revenue += company.entry_revenue || 0;
      bucket.ebitda += company.entry_ebitda || 0;
      yearly.set(year, bucket);
    });

    const trend = Array.from(yearly.entries())
      .sort((a, b) => Number(a[0]) - Number(b[0]))
      .map(([year, values]) => ({ year, revenue: values.revenue, ebitda: values.ebitda }));

    if (trend.length === 0) {
      return [
        { year: '2019', revenue: 0, ebitda: 0 },
        { year: '2020', revenue: 0, ebitda: 0 },
        { year: '2021', revenue: 0, ebitda: 0 },
        { year: '2022', revenue: 0, ebitda: 0 },
        { year: '2023', revenue: 0, ebitda: 0 },
      ];
    }

    return trend;
  }, [companies]);

  const sectorAllocation = useMemo(() => {
    const map = new Map<string, number>();
    companies.forEach((company) => {
      const equity = company.equity_invested || 0;
      const key = company.sector || 'Other';
      map.set(key, (map.get(key) || 0) + equity);
    });
    return Array.from(map.entries()).map(([name, value]) => ({ name, value }));
  }, [companies]);

  const activityFeed = useMemo(() => {
    return [...companies]
      .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      .slice(0, 6)
      .map((company) => ({
        id: company.company_id,
        title: company.company_name,
        timestamp: new Date(company.updated_at).toLocaleDateString(),
        description: `${company.company_status} • ${company.sector || 'Sector TBD'}`,
      }));
  }, [companies]);

  const tableRows = useMemo(() => {
    return companies.map((company) => ({
      id: company.company_id,
      company: company.company_name,
      sector: company.sector,
      revenue: company.entry_revenue || 0,
      ebitda: company.entry_ebitda || 0,
      status: company.company_status,
    }));
  }, [companies]);

  const columns = useMemo<GridColDef[]>(
    () => [
      { field: 'company', headerName: 'Company', flex: 1, minWidth: 180 },
      { field: 'sector', headerName: 'Sector', flex: 0.8, minWidth: 140 },
      {
        field: 'revenue',
        headerName: 'Revenue',
        flex: 0.8,
        valueFormatter: (params) => formatCurrency(params.value as number),
      },
      {
        field: 'ebitda',
        headerName: 'EBITDA',
        flex: 0.8,
        valueFormatter: (params) => formatCurrency(params.value as number),
      },
      {
        field: 'status',
        headerName: 'Status',
        flex: 0.6,
        renderCell: (params) => (
          <Chip
            size="small"
            label={params.value as string}
            color={params.value === 'Active' ? 'success' : params.value === 'Exited' ? 'primary' : 'default'}
            variant="outlined"
          />
        ),
      },
    ],
    []
  );

  // Conditional returns AFTER all hooks
  // Show loading skeleton
  if (loading && companies.length === 0) {
    return <DashboardSkeleton />;
  }

  // Show error state
  if (error && companies.length === 0) {
    return (
      <ErrorState
        title="Failed to load dashboard"
        message="We couldn't load your portfolio data. Please try again."
        onRetry={() => refetch()}
      />
    );
  }

  // Show empty state
  if (!loading && companies.length === 0) {
    return (
      <EmptyState
        icon={AddIcon}
        title="No portfolio companies yet"
        description="Get started by adding your first portfolio company to track performance and generate insights."
        actionLabel="Add Company"
        onAction={() => navigate('/companies/new')}
        secondaryActionLabel="Learn More"
        onSecondaryAction={() => window.open('https://example.com/docs', '_blank')}
      />
    );
  }

  return (
    <Stack spacing={3}>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
            Portfolio Overview
          </Typography>
          <Typography color="text.secondary">
            Monitor performance, allocations, and portfolio activity at a glance.
          </Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          <Tooltip title="Refresh data">
            <IconButton onClick={() => refetch()} color="primary">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/companies/new')}
          >
            Add Company
          </Button>
        </Stack>
      </Stack>

      <Grid container spacing={3}>
        {[
          {
            label: 'Total Revenue',
            value: formatCurrency(kpis.revenue),
            change: 8.4,
            icon: ShowChartIcon,
            color: '#1976d2',
          },
          {
            label: 'Total EBITDA',
            value: formatCurrency(kpis.ebitda),
            change: 5.1,
            icon: TrendingUpIcon,
            color: '#2e7d32',
          },
          {
            label: 'Operating Cash Flow',
            value: formatCurrency(kpis.cashFlow),
            change: 3.2,
            icon: TrendingUpIcon,
            color: '#1565c0',
          },
          {
            label: 'Portfolio ROI',
            value: formatPercent((kpis.roi || 0) * 100),
            change: kpis.roi * 100,
            icon: PieChartIcon,
            color: '#9c27b0',
          },
        ].map((item) => {
          const Icon = item.icon;
          const isPositive = item.change >= 0;
          return (
            <Grid item xs={12} sm={6} md={3} key={item.label}>
              <Card
                sx={{
                  height: '100%',
                  position: 'relative',
                  overflow: 'visible',
                  '&:hover': {
                    boxShadow: 6,
                    transform: 'translateY(-4px)',
                    transition: 'all 0.3s ease-in-out',
                  },
                }}
              >
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                    <Box>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        {item.label}
                      </Typography>
                      <Typography variant="h4" sx={{ mt: 1, mb: 0.5, fontWeight: 700 }}>
                        {item.value}
                      </Typography>
                      <Stack direction="row" alignItems="center" spacing={0.5}>
                        {isPositive ? (
                          <TrendingUpIcon fontSize="small" sx={{ color: 'success.main' }} />
                        ) : (
                          <TrendingDownIcon fontSize="small" sx={{ color: 'error.main' }} />
                        )}
                        <Typography
                          variant="caption"
                          sx={{
                            color: isPositive ? 'success.main' : 'error.main',
                            fontWeight: 600,
                          }}
                        >
                          {isPositive ? '+' : ''}{item.change.toFixed(1)}% vs LY
                        </Typography>
                      </Stack>
                    </Box>
                    <Box
                      sx={{
                        width: 48,
                        height: 48,
                        borderRadius: 2,
                        bgcolor: `${item.color}15`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      <Icon sx={{ fontSize: 24, color: item.color }} />
                    </Box>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Stack
                direction={{ xs: 'column', md: 'row' }}
                spacing={3}
                alignItems={{ md: 'center' }}
                justifyContent="space-between"
              >
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Launch advanced modeling tools
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Access downloadable Excel generators or run the embedded real estate underwriting suite without leaving the dashboard.
                  </Typography>
                </Box>
                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1.5}>
                  <Button
                    variant="contained"
                    startIcon={<HomeWorkIcon />}
                    onClick={() => navigate('/real-estate')}
                  >
                    Real Estate Models
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<TimelineIcon />}
                    onClick={() => navigate('/finance-models')}
                  >
                    Corporate Finance Models
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<DescriptionIcon />}
                    onClick={() => navigate('/models')}
                  >
                    Excel Model Generator
                  </Button>
                </Stack>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ height: 360 }}>
              <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                <Box>
                  <Typography variant="h6">Revenue & EBITDA Trend</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Aggregated by investment year
                  </Typography>
                </Box>
              </Stack>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={revenueTrend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis tickFormatter={(value) => `${Math.round((value as number) / 1_000_000)}M`} />
                  <ChartTooltip formatter={(value: number) => formatCurrency(value)} labelFormatter={(label) => `Year ${label}`} />
                  <Legend />
                  <Line type="monotone" dataKey="revenue" name="Revenue" stroke="#1976d2" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                  <Line type="monotone" dataKey="ebitda" name="EBITDA" stroke="#2e7d32" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ height: 360 }}>
              <Typography variant="h6" gutterBottom>
                Sector Allocation
              </Typography>
              <ResponsiveContainer width="100%" height="90%">
                <PieChart>
                  <Pie
                    data={sectorAllocation}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={4}
                  >
                    {sectorAllocation.map((entry, index) => (
                      <Cell key={`cell-${entry.name}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <ChartTooltip formatter={(value: number) => formatCurrency(value)} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
              {sectorAllocation.length === 0 && (
                <Typography variant="body2" color="text.secondary" textAlign="center">
                  No allocation data yet
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card sx={{ height: 460 }}>
            <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <Typography variant="h6" gutterBottom>
                Portfolio Companies
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box sx={{ flexGrow: 1 }}>
                <DataGrid
                  density="comfortable"
                  rows={tableRows}
                  columns={columns}
                  loading={loading}
                  slots={{ toolbar: QuickSearchToolbar }}
                  initialState={{
                    pagination: { paginationModel: { pageSize: 10 } },
                  }}
                  pageSizeOptions={[10, 25, 50]}
                  onRowClick={(params) => navigate(`/companies/${params.id}`)}
                  sx={{
                    '& .MuiDataGrid-row': {
                      cursor: 'pointer',
                      '&:hover': {
                        bgcolor: 'action.hover',
                      },
                    },
                  }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: 460 }}>
            <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <Typography variant="h6" gutterBottom>
                Activity Feed
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box sx={{ flexGrow: 1, overflowY: 'auto', position: 'relative', pl: 3 }}>
                <Box
                  sx={{
                    position: 'absolute',
                    left: 14,
                    top: 0,
                    bottom: 0,
                    width: 2,
                    bgcolor: 'divider',
                  }}
                />
                <Stack spacing={3}>
                  {activityFeed.length === 0 && !loading && (
                    <Typography variant="body2" color="text.secondary">
                      No recent activity.
                    </Typography>
                  )}
                  {activityFeed.map((item, index) => (
                    <Box key={item.id} sx={{ position: 'relative', pl: 2 }}>
                      <Box
                        sx={{
                          position: 'absolute',
                          left: -16,
                          top: 4,
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          bgcolor: COLORS[index % COLORS.length],
                        }}
                      />
                      <Typography variant="subtitle2">{item.title}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {item.timestamp}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {item.description}
                      </Typography>
                    </Box>
                  ))}
                </Stack>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Stack>
  );
};
