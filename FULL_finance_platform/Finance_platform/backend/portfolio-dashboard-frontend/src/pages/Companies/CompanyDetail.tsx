// src/pages/Companies/CompanyDetail.tsx
import React, { useEffect, useMemo, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Chip,
  Stack,
  Tabs,
  Tab,
  Divider,
  Table,
  TableBody,
  TableRow,
  TableCell,
  IconButton,
  Tooltip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
} from '@mui/material';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip as ChartTooltip,
  Legend,
} from 'recharts';
import {
  EditOutlined as EditIcon,
  Timeline as TimelineIcon,
  DeleteOutline as DeleteIcon,
  ArrowBack as ArrowBackIcon,
  Description as DocumentIcon,
  TrendingUp as TrendingUpIcon,
  Event as EventIcon,
  Business as BusinessIcon,
  Share as ShareIcon,
} from '@mui/icons-material';
import { useCompany } from '../../hooks/useCompanies';
import { formatCurrency, formatPercent, formatMultiple } from '../../utils/formatters';
import { PageSkeleton } from '../../components/common/LoadingSkeleton';
import { ErrorState } from '../../components/common/ErrorState';
import { EmptyState } from '../../components/common/EmptyState';

const SECTION_CONFIG = [
  { id: 'overview', label: 'Overview' },
  { id: 'metrics', label: 'Key Metrics' },
  { id: 'performance', label: 'Performance' },
  { id: 'financials', label: 'Financials' },
  { id: 'activity', label: 'Activity' },
];

export const CompanyDetail: React.FC = () => {
  const { companyId } = useParams<{ companyId: string }>();
  const navigate = useNavigate();
  const { company, loading, error, refetch } = useCompany(companyId!);
  const [activeSection, setActiveSection] = useState('overview');

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.find((entry) => entry.isIntersecting);
        if (visible?.target?.id) {
          setActiveSection(visible.target.id);
        }
      },
      { rootMargin: '-120px 0px -60%', threshold: 0.3 }
    );

    SECTION_CONFIG.forEach((section) => {
      const element = document.getElementById(section.id);
      if (element) {
        observer.observe(element);
      }
    });

    return () => observer.disconnect();
  }, [company]);

  const handleScrollTo = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setActiveSection(sectionId);
    }
  };

  const handleDelete = () => {
    // Placeholder for future delete integration
    console.info('Delete action triggered for company', companyId);
  };

  const performanceData = useMemo(() => {
    if (!company) {
      return [];
    }

    const baseRevenue = company.entry_revenue || 0;
    const baseEbitda = company.entry_ebitda || 0;

    if (!baseRevenue && !baseEbitda) {
      return [
        { year: '2019', revenue: 0, ebitda: 0 },
        { year: '2020', revenue: 0, ebitda: 0 },
        { year: '2021', revenue: 0, ebitda: 0 },
        { year: '2022', revenue: 0, ebitda: 0 },
        { year: '2023', revenue: 0, ebitda: 0 },
      ];
    }

    return Array.from({ length: 5 }).map((_, index) => {
      const year = new Date(company.investment_date).getFullYear() + index;
      const growthFactor = 1 + 0.08 * index;
      return {
        year: year.toString(),
        revenue: Math.round(baseRevenue * growthFactor),
        ebitda: Math.round(baseEbitda * (1 + 0.06 * index)),
      };
    });
  }, [company]);

  // Show loading skeleton
  if (loading && !company) {
    return <PageSkeleton type="detail" />;
  }

  // Show error state
  if (error && !company) {
    return (
      <ErrorState
        title="Failed to load company"
        message="We couldn't load this company's details. Please try again."
        onRetry={refetch}
      />
    );
  }

  // Show not found state
  if (!loading && !company) {
    return (
      <EmptyState
        icon={BusinessIcon}
        title="Company not found"
        description="This company may have been deleted or you may not have permission to view it."
        actionLabel="Back to Companies"
        onAction={() => navigate('/companies')}
      />
    );
  }

  const statusColor = company.company_status === 'Active' ? 'success' : company.company_status === 'Exited' ? 'info' : 'warning';

  return (
    <Stack spacing={4}>
      {/* Back Button */}
      <Box>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/companies')}
          sx={{ mb: 2 }}
        >
          Back to Companies
        </Button>
      </Box>

      {/* Company Header */}
      <Box
        id="overview"
        sx={{
          position: 'relative',
          color: 'common.white',
          background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
          borderRadius: 4,
          p: { xs: 3, md: 5 },
          overflow: 'hidden',
        }}
      >
        <Box sx={{ position: 'absolute', inset: 0, opacity: 0.08, backgroundImage: 'radial-gradient(circle at top right, #fff, transparent 60%)' }} />
        <Stack spacing={2} position="relative" zIndex={1}>
          <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
            <Chip
              label={company.company_status}
              color={statusColor}
              variant="outlined"
              sx={{ alignSelf: 'flex-start', borderColor: 'common.white', color: 'common.white' }}
            />
            <Tooltip title="Share company">
              <IconButton sx={{ color: 'common.white' }}>
                <ShareIcon />
              </IconButton>
            </Tooltip>
          </Stack>
          <Typography variant="h3" sx={{ fontWeight: 700 }}>
            {company.company_name}
          </Typography>
          <Typography variant="body1" sx={{ opacity: 0.95 }}>
            {company.sector} • {company.headquarters_city || 'City TBD'}, {company.headquarters_country || 'Country TBD'}
          </Typography>
          <Typography variant="body2" sx={{ maxWidth: 640, opacity: 0.9 }}>
            {company.business_description || 'Business description coming soon.'}
          </Typography>

          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} pt={2}>
            <Button
              variant="contained"
              startIcon={<EditIcon />}
              sx={{
                bgcolor: 'common.white',
                color: 'primary.main',
                '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' },
              }}
            >
              Edit Company
            </Button>
            <Button
              variant="contained"
              color="secondary"
              startIcon={<TimelineIcon />}
              onClick={() => navigate(`/companies/${companyId}/models`)}
            >
              Generate Models
            </Button>
            <Button
              variant="outlined"
              startIcon={<DeleteIcon />}
              onClick={handleDelete}
              sx={{
                borderColor: 'common.white',
                color: 'common.white',
                '&:hover': {
                  borderColor: 'common.white',
                  bgcolor: 'rgba(255,255,255,0.12)',
                },
              }}
            >
              Delete
            </Button>
          </Stack>
        </Stack>
      </Box>

      <Box sx={{ position: 'sticky', top: 72, zIndex: 2, backgroundColor: 'background.default', borderBottom: '1px solid', borderColor: 'divider' }}>
        <Tabs
          value={activeSection}
          onChange={(_, value) => handleScrollTo(value)}
          variant="scrollable"
          scrollButtons="auto"
        >
          {SECTION_CONFIG.map((section) => (
            <Tab key={section.id} value={section.id} label={section.label} />
          ))}
        </Tabs>
      </Box>

      <Grid container spacing={3} id="metrics">
        {[{
          label: 'Revenue (Entry)',
          value: formatCurrency(company.entry_revenue),
          helper: 'Last reported'
        }, {
          label: 'EBITDA (Entry)',
          value: formatCurrency(company.entry_ebitda),
          helper: `${formatPercent((company.entry_ebitda && company.entry_revenue) ? (company.entry_ebitda / company.entry_revenue) * 100 : 0)} margin`
        }, {
          label: 'Entry Multiple',
          value: formatMultiple(company.entry_multiple),
          helper: company.deal_type
        }, {
          label: 'Equity Invested',
          value: formatCurrency(company.equity_invested),
          helper: `Ownership ${company.ownership_percentage ? formatPercent(company.ownership_percentage * 100) : 'N/A'}`
        }, {
          label: 'Purchase Price',
          value: formatCurrency(company.purchase_price),
          helper: company.investment_date ? `Closed ${new Date(company.investment_date).toLocaleDateString()}` : 'Date TBD'
        }, {
          label: 'Realized IRR',
          value: company.realized_irr ? formatPercent(company.realized_irr * 100) : 'In progress',
          helper: company.exit_date ? `Exited ${new Date(company.exit_date).toLocaleDateString()}` : 'Active investment'
        }].map((metric) => (
          <Grid item xs={12} md={4} key={metric.label}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="body2" color="text.secondary">
                  {metric.label}
                </Typography>
                <Typography variant="h5" sx={{ mt: 1, mb: 1 }}>
                  {metric.value}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {metric.helper}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} id="performance">
        <Grid item xs={12}>
          <Card sx={{ height: 420 }}>
            <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <Typography variant="h6" gutterBottom>
                Revenue & EBITDA Over Time
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Modeled using entry values with conservative growth assumptions.
              </Typography>
              <Box sx={{ flexGrow: 1 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={performanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis tickFormatter={(value) => `${Math.round((value as number) / 1_000_000)}M`} />
                    <Tooltip formatter={(value: number) => formatCurrency(value)} />
                    <Legend />
                    <Line type="monotone" dataKey="revenue" stroke="#1976d2" strokeWidth={2} dot />
                    <Line type="monotone" dataKey="ebitda" stroke="#2e7d32" strokeWidth={2} dot />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3} id="financials">
        <Grid item xs={12} md={7}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Financial Snapshot
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Table size="small">
                <TableBody>
                  <TableRow>
                    <TableCell variant="head">Investment Date</TableCell>
                    <TableCell>{company.investment_date ? new Date(company.investment_date).toLocaleDateString() : 'TBD'}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell variant="head">Deal Type</TableCell>
                    <TableCell>{company.deal_type}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell variant="head">Equity Invested</TableCell>
                    <TableCell>{formatCurrency(company.equity_invested)}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell variant="head">Debt Raised</TableCell>
                    <TableCell>{formatCurrency(company.debt_raised)}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell variant="head">Ownership %</TableCell>
                    <TableCell>{company.ownership_percentage ? formatPercent(company.ownership_percentage * 100) : 'N/A'}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell variant="head">Purchase Price</TableCell>
                    <TableCell>{formatCurrency(company.purchase_price)}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell variant="head">Exit Metrics</TableCell>
                    <TableCell>
                      {company.exit_date
                        ? `Exited ${new Date(company.exit_date).toLocaleDateString()} • MOIC ${company.realized_moic?.toFixed(2) || 'N/A'}`
                        : 'Exit pending'}
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={5}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Strategic Notes
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Stack spacing={2}>
                <Box>
                  <Typography variant="subtitle2">Value Creation Plan</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Diversify revenue streams, optimize pricing, and accelerate digital transformation initiatives.
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2">Key Risks</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Monitor supply chain volatility and currency exposure in international markets.
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2">Next Review</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Quarterly portfolio review scheduled for {new Date().getFullYear()}-Q{Math.ceil((new Date().getMonth() + 1) / 3)}.
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Activity Timeline */}
      <Grid container spacing={3} id="activity">
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Activity Timeline
              </Typography>
              <Divider sx={{ mb: 3 }} />
              <List>
                {[
                  {
                    icon: <EventIcon />,
                    title: 'Investment Closed',
                    description: `Acquired ${company.ownership_percentage ? formatPercent(company.ownership_percentage * 100) : 'N/A'} ownership for ${formatCurrency(company.equity_invested)}`,
                    date: company.investment_date ? new Date(company.investment_date).toLocaleDateString() : 'TBD',
                    color: '#1976d2',
                  },
                  {
                    icon: <TrendingUpIcon />,
                    title: 'Q4 2023 Performance',
                    description: 'Revenue growth of 12% YoY, EBITDA margin improved to 18%',
                    date: '3 months ago',
                    color: '#2e7d32',
                  },
                  {
                    icon: <DocumentIcon />,
                    title: 'Board Meeting',
                    description: 'Reviewed strategic initiatives and approved budget for digital transformation',
                    date: '1 month ago',
                    color: '#9c27b0',
                  },
                  {
                    icon: <BusinessIcon />,
                    title: 'Management Update',
                    description: 'New CFO appointed to drive operational excellence',
                    date: '2 weeks ago',
                    color: '#ed6c00',
                  },
                ].map((item, index) => (
                  <ListItem
                    key={index}
                    sx={{
                      borderLeft: '3px solid',
                      borderColor: item.color,
                      mb: 2,
                      bgcolor: 'action.hover',
                      borderRadius: 1,
                    }}
                  >
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: item.color }}>
                        {item.icon}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={item.title}
                      secondary={
                        <Stack spacing={0.5}>
                          <Typography variant="body2" color="text.secondary">
                            {item.description}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {item.date}
                          </Typography>
                        </Stack>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Stack>
  );
};
