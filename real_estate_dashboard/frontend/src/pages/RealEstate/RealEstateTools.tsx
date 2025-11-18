import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Stack,
  Chip,
  alpha,
  useTheme,
} from '@mui/material';
import {
  Home as HomeIcon,
  HomeWork as HomeWorkIcon,
  Apartment as ApartmentIcon,
  Hotel as HotelIcon,
  Business as BusinessIcon,
  Domain as DomainIcon,
  Description as DescriptionIcon,
  Build as BuildIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  ShowChart as ShowChartIcon,
  Landscape as LandscapeIcon,
  AccountBalance as TaxIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';

const MODELS = [
  {
    id: 'fix-flip',
    title: 'Fix & Flip',
    description: 'Short-term renovation projects with MAO calculation, 70% rule analysis, and exit strategy modeling',
    icon: HomeIcon,
    gradient: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    glowColor: '#3b82f6',
    path: '/real-estate-models/fix-and-flip',
    metrics: ['ROI', 'MAO', 'Profit Margin'],
  },
  {
    id: 'single-family',
    title: 'Single Family Rental',
    description: 'Long-term rental cash flow analysis with debt service coverage and appreciation projections',
    icon: HomeWorkIcon,
    gradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    glowColor: '#10b981',
    path: '/real-estate-models/single-family-rental',
    metrics: ['Cash Flow', 'Cap Rate', 'CoC Return'],
  },
  {
    id: 'small-multifamily',
    title: 'Small Multifamily',
    description: '2-6 unit property analysis with per-unit economics and DSCR calculations',
    icon: ApartmentIcon,
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
    glowColor: '#8b5cf6',
    path: '/real-estate-models/small-multifamily',
    metrics: ['DSCR', 'NOI', 'Unit Economics'],
  },
  {
    id: 'high-rise',
    title: 'High-Rise Multifamily',
    description: '7+ units institutional-grade modeling for large apartment complexes with income stratification',
    icon: DomainIcon,
    gradient: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
    glowColor: '#6366f1',
    path: '/real-estate-models/extended-multifamily',
    metrics: ['Cap Rate', 'GPI', 'Operating Ratio'],
  },
  {
    id: 'hotel',
    title: 'Hotel & Hospitality',
    description: 'Hospitality financial modeling with RevPAR, ADR, and seasonal variance analysis',
    icon: HotelIcon,
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    glowColor: '#f59e0b',
    path: '/real-estate-models/hotel',
    metrics: ['RevPAR', 'ADR', 'Occupancy'],
  },
  {
    id: 'mixed-use',
    title: 'Mixed-Use Development',
    description: 'Complex developments blending residential, retail, and office with blended metrics',
    icon: BusinessIcon,
    gradient: 'linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)',
    glowColor: '#14b8a6',
    path: '/real-estate-models/mixed-use',
    metrics: ['Blended Cap', 'Income Mix', 'NOI'],
  },
  {
    id: 'subdivision',
    title: 'Subdivision Development',
    description: 'Land subdivision financial modeling with phased lot sales, absorption analysis, and development cost tracking',
    icon: LandscapeIcon,
    gradient: 'linear-gradient(135deg, #84cc16 0%, #65a30d 100%)',
    glowColor: '#84cc16',
    path: '/real-estate-models/subdivision',
    metrics: ['IRR', 'Absorption', 'Cost/Lot'],
  },
  {
    id: 'small-multifamily-acquisition',
    title: 'Small Multifamily Acquisition',
    description: '2-10 unit property acquisition with multiple exit strategies: subdivide/convert, sell as-is, BRRRR, hybrid, wholesale',
    icon: ApartmentIcon,
    gradient: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
    glowColor: '#06b6d4',
    path: '/real-estate-models/small-multifamily-acquisition',
    metrics: ['ROI', 'Exit Strategies', 'IRR'],
  },
  {
    id: 'lease-analyzer',
    title: 'Lease Analyzer',
    description: 'Side-by-side lease comparison with escalation clauses and total cost analysis',
    icon: DescriptionIcon,
    gradient: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
    glowColor: '#ec4899',
    path: '/real-estate-models/lease-analyzer',
    metrics: ['Total Cost', 'Escalations', 'NPV'],
  },
  {
    id: 'renovation-budget',
    title: 'Renovation Budget',
    description: 'Construction cost estimation with line-item budgeting and contingency planning',
    icon: BuildIcon,
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)',
    glowColor: '#f59e0b',
    path: '/real-estate-models/renovation-budget',
    metrics: ['Total Budget', 'Cost/SF', 'Timeline'],
  },
  {
    id: 'tax-strategy',
    title: 'Tax Strategy Integration',
    description: 'Comprehensive tax planning with 1031 Exchange, Cost Segregation, Opportunity Zones, and Entity Optimization',
    icon: TaxIcon,
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    glowColor: '#667eea',
    path: '/real-estate-models/tax-strategy',
    metrics: ['Tax Savings', 'ROI Optimization', 'Entity Comparison'],
  },
  {
    id: 'market-intelligence',
    title: 'Market Intelligence Dashboard',
    description: 'Real-time market data with macro indicators, local metrics, competitive landscape tracking, and filtered news aggregator',
    icon: TrendingUpIcon,
    gradient: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
    glowColor: '#06b6d4',
    path: '/real-estate-models/market-intelligence',
    metrics: ['Live Data', 'Market Trends', 'Competitive Intel'],
  },
];

export const RealEstateTools: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const stats = [
    { label: 'Models Available', value: '11', icon: AssessmentIcon },
    { label: 'Avg Analysis Time', value: '< 5 min', icon: TrendingUpIcon },
    { label: 'Data Points', value: '150+', icon: ShowChartIcon },
    { label: 'Export Formats', value: '3', icon: DescriptionIcon },
  ];

  return (
    <Box sx={{ px: 4, py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 6 }}>
        <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
          <Typography
            variant="h4"
            sx={{
              fontWeight: 700,
              background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Financial Models
          </Typography>
          <Chip
            label="11 Models"
            size="small"
            sx={{
              background: isDark
                ? 'rgba(59, 130, 246, 0.1)'
                : 'rgba(59, 130, 246, 0.15)',
              color: '#3b82f6',
              border: `1px solid ${alpha('#3b82f6', 0.2)}`,
              fontWeight: 600,
            }}
          />
        </Stack>
        <Typography
          variant="body1"
          color="text.secondary"
          sx={{ maxWidth: '800px' }}
        >
          Institutional-grade financial modeling & analysis tools for comprehensive real estate investment analysis
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 6 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                background: isDark
                  ? 'linear-gradient(135deg, rgba(15, 20, 25, 0.6) 0%, rgba(15, 20, 25, 0.8) 100%)'
                  : 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.95) 100%)',
                border: isDark
                  ? `1px solid ${alpha('#94a3b8', 0.1)}`
                  : `1px solid ${alpha('#0f172a', 0.1)}`,
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: isDark
                    ? '0 12px 32px rgba(0, 0, 0, 0.18)'
                    : '0 12px 32px rgba(0, 0, 0, 0.08)',
                },
              }}
            >
              <CardContent>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 3,
                    background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    mb: 2,
                    boxShadow: '0 4px 16px rgba(59, 130, 246, 0.3)',
                  }}
                >
                  <stat.icon sx={{ fontSize: 24, color: 'white' }} />
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                  {stat.label}
                </Typography>
                <Typography variant="h5" sx={{ fontWeight: 700 }}>
                  {stat.value}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Models Grid */}
      <Grid container spacing={4}>
        {MODELS.map((model) => {
          const Icon = model.icon;
          return (
            <Grid item xs={12} md={6} key={model.id}>
              <Card
                onClick={() => navigate(model.path)}
                sx={{
                  height: '100%',
                  cursor: 'pointer',
                  position: 'relative',
                  overflow: 'hidden',
                  background: isDark
                    ? 'linear-gradient(135deg, rgba(15, 20, 25, 0.6) 0%, rgba(15, 20, 25, 0.8) 100%)'
                    : 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.95) 100%)',
                  border: isDark
                    ? `1px solid ${alpha('#94a3b8', 0.1)}`
                    : `1px solid ${alpha('#0f172a', 0.1)}`,
                  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: isDark
                      ? '0 20px 40px rgba(0, 0, 0, 0.2)'
                      : '0 20px 40px rgba(0, 0, 0, 0.1)',
                    border: `1px solid ${alpha(model.glowColor, 0.3)}`,
                    '& .glow-effect': {
                      opacity: 1,
                    },
                  },
                }}
              >
                {/* Glow Effect */}
                <Box
                  className="glow-effect"
                  sx={{
                    position: 'absolute',
                    top: 0,
                    right: 0,
                    width: '300px',
                    height: '300px',
                    background: `radial-gradient(circle, ${alpha(model.glowColor, 0.15)} 0%, transparent 70%)`,
                    opacity: 0,
                    transition: 'opacity 0.5s ease',
                    pointerEvents: 'none',
                    transform: 'translate(40%, -40%)',
                  }}
                />

                <CardContent sx={{ p: 4, position: 'relative', zIndex: 1 }}>
                  <Stack direction="row" spacing={3} sx={{ mb: 3 }}>
                    {/* Icon */}
                    <Box
                      sx={{
                        width: 72,
                        height: 72,
                        borderRadius: 4,
                        background: model.gradient,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        position: 'relative',
                        boxShadow: `0 8px 24px ${alpha(model.glowColor, 0.4)}`,
                        '&::before': {
                          content: '""',
                          position: 'absolute',
                          inset: 0,
                          background: 'linear-gradient(to top, rgba(255,255,255,0.2), transparent)',
                          borderRadius: 4,
                        },
                      }}
                    >
                      <Icon sx={{ fontSize: 36, color: 'white', position: 'relative', zIndex: 1 }} />
                    </Box>

                    {/* Title & Description */}
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="h6" sx={{ fontWeight: 700, mb: 1 }}>
                        {model.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>
                        {model.description}
                      </Typography>
                    </Box>
                  </Stack>

                  {/* Metrics */}
                  <Stack direction="row" spacing={1} sx={{ mb: 3 }}>
                    {model.metrics.map((metric) => (
                      <Chip
                        key={metric}
                        label={metric}
                        size="small"
                        sx={{
                          background: isDark
                            ? alpha('#94a3b8', 0.1)
                            : alpha('#64748b', 0.1),
                          color: 'text.secondary',
                          border: isDark
                            ? `1px solid ${alpha('#94a3b8', 0.2)}`
                            : `1px solid ${alpha('#64748b', 0.2)}`,
                          fontWeight: 500,
                          fontSize: '0.75rem',
                        }}
                      />
                    ))}
                  </Stack>

                  {/* Footer */}
                  <Stack
                    direction="row"
                    justifyContent="space-between"
                    alignItems="center"
                    sx={{
                      pt: 3,
                      borderTop: isDark
                        ? `1px solid ${alpha('#94a3b8', 0.1)}`
                        : `1px solid ${alpha('#0f172a', 0.1)}`,
                    }}
                  >
                    <Typography variant="body2" color="text.secondary">
                      Click to open calculator
                    </Typography>
                    <Stack direction="row" alignItems="center" spacing={1} sx={{ color: model.glowColor }}>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>
                        Launch
                      </Typography>
                      <Box
                        component="svg"
                        sx={{ width: 16, height: 16 }}
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </Box>
                    </Stack>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      {/* Info Section */}
      <Card
        sx={{
          mt: 6,
          background: isDark
            ? 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)'
            : 'linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%)',
          border: `1px solid ${alpha('#3b82f6', 0.2)}`,
        }}
      >
        <CardContent sx={{ p: 4 }}>
          <Stack direction="row" spacing={3}>
            <Box
              sx={{
                width: 64,
                height: 64,
                borderRadius: 4,
                background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 4px 16px rgba(59, 130, 246, 0.3)',
              }}
            >
              <AssessmentIcon sx={{ fontSize: 32, color: 'white' }} />
            </Box>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
                Professional Real Estate Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3, lineHeight: 1.7 }}>
                Our financial models are built on institutional-grade frameworks used by commercial real estate firms,
                private equity funds, and REITs. Each calculator provides comprehensive analysis with industry-standard
                metrics and assumptions.
              </Typography>
              <Grid container spacing={2}>
                {['Real-time calculations', 'Multiple scenarios', 'Export capabilities'].map((feature) => (
                  <Grid item xs={12} sm={4} key={feature}>
                    <Stack direction="row" spacing={1} alignItems="center">
                      <Box
                        sx={{
                          width: 6,
                          height: 6,
                          borderRadius: '50%',
                          bgcolor: '#10b981',
                          boxShadow: '0 0 8px rgba(16, 185, 129, 0.5)',
                        }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        {feature}
                      </Typography>
                    </Stack>
                  </Grid>
                ))}
              </Grid>
            </Box>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
};
