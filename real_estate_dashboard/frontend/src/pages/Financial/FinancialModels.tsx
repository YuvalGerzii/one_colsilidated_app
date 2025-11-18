import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Stack,
  Chip,
  alpha,
  useTheme,
} from '@mui/material';
import {
  TrendingUp as DCFIcon,
  AccountBalance as LBOIcon,
  MergeType as MergerIcon,
  Assessment as AnalysisIcon,
  ArrowForward as ArrowIcon,
  Calculate as CalculateIcon,
  Assignment as DDIcon,
  CompareArrows as CompsIcon,
} from '@mui/icons-material';

interface ModelCard {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  path: string;
  status: 'active' | 'coming-soon';
  features: string[];
  complexity: 'Intermediate' | 'Advanced';
  timeToComplete: string;
}

const models: ModelCard[] = [
  {
    id: 'dcf',
    title: 'DCF Valuation Model',
    description: 'Discounted Cash Flow analysis for company valuation with comprehensive sensitivity analysis and terminal value calculations.',
    icon: <DCFIcon sx={{ fontSize: 40 }} />,
    path: '/financial-models/dcf',
    status: 'active',
    features: [
      '10 integrated worksheets',
      'Dual terminal value methods',
      'WACC calculator',
      'Sensitivity analysis (147 scenarios)',
      'Trading comps & precedent transactions',
      'Credit analysis & scenario modeling',
    ],
    complexity: 'Advanced',
    timeToComplete: '30-45 min',
  },
  {
    id: 'lbo',
    title: 'LBO Model',
    description: 'Leveraged Buyout analysis for private equity transactions with debt structure, cash sweeps, and return calculations.',
    icon: <LBOIcon sx={{ fontSize: 40 }} />,
    path: '/financial-models/lbo',
    status: 'active',
    features: [
      '8 integrated worksheets',
      'Intelligent cash sweep mechanics',
      '4-tranche debt structure',
      'IRR & MOIC calculations',
      'Distribution waterfall (4-tier)',
      'Sensitivity analysis',
    ],
    complexity: 'Advanced',
    timeToComplete: '45-60 min',
  },
  {
    id: 'merger',
    title: 'M&A Merger Model',
    description: 'Merger & acquisition analysis for evaluating deal accretion/dilution and synergies.',
    icon: <MergerIcon sx={{ fontSize: 40 }} />,
    path: '/financial-models/merger',
    status: 'active',
    features: [
      'Accretion/Dilution analysis',
      'Pro forma financials',
      'Synergy modeling',
      'Cash/Stock consideration split',
      'Ownership dilution analysis',
      'EPS impact calculations',
    ],
    complexity: 'Advanced',
    timeToComplete: '30-40 min',
  },
  {
    id: 'dd',
    title: 'Due Diligence Model',
    description: 'Comprehensive checklist and tracking system for M&A due diligence across all functional areas.',
    icon: <DDIcon sx={{ fontSize: 40 }} />,
    path: '/financial-models/dd',
    status: 'active',
    features: [
      '6 due diligence categories',
      '50+ checklist items',
      'Critical item flagging',
      'Progress tracking dashboard',
      'Document attachment support',
      'Exportable reports',
    ],
    complexity: 'Intermediate',
    timeToComplete: '15-20 min setup',
  },
  {
    id: 'comps',
    title: 'Comparable Company Analysis',
    description: 'Trading multiples analysis for public market valuation using comparable companies.',
    icon: <CompsIcon sx={{ fontSize: 40 }} />,
    path: '/financial-models/comps',
    status: 'active',
    features: [
      'Unlimited comparable companies',
      'EV/Revenue multiples',
      'EV/EBITDA multiples',
      'P/E ratio analysis',
      'Median & mean statistics',
      'Implied valuation ranges',
    ],
    complexity: 'Intermediate',
    timeToComplete: '20-30 min',
  },
];

export const FinancialModels: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  const getStatusColor = (status: string) => {
    return status === 'active' ? '#10b981' : '#f59e0b';
  };

  const getComplexityColor = (complexity: string) => {
    return complexity === 'Advanced' ? '#ef4444' : '#3b82f6';
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
          <Box
            sx={{
              width: 56,
              height: 56,
              background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
              borderRadius: 3,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 20px rgba(59, 130, 246, 0.3)',
            }}
          >
            <CalculateIcon sx={{ fontSize: 32, color: 'white' }} />
          </Box>
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5 }}>
              Company Financial Analysis
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Institutional-grade financial models for valuation, M&A, and investment analysis
            </Typography>
          </Box>
        </Stack>

        {/* Quick Stats */}
        <Stack direction="row" spacing={2} sx={{ mt: 3 }}>
          <Chip
            label="5 Active Models"
            sx={{
              bgcolor: alpha('#10b981', 0.1),
              color: '#10b981',
              fontWeight: 600,
            }}
          />
          <Chip
            label="Professional-Grade Analysis"
            sx={{
              bgcolor: alpha('#3b82f6', 0.1),
              color: '#3b82f6',
              fontWeight: 600,
            }}
          />
          <Chip
            label="Investment Banking Quality"
            sx={{
              bgcolor: alpha('#8b5cf6', 0.1),
              color: '#8b5cf6',
              fontWeight: 600,
            }}
          />
        </Stack>
      </Box>

      {/* Model Cards Grid */}
      <Grid container spacing={3}>
        {models.map((model) => (
          <Grid item xs={12} md={6} lg={4} key={model.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative',
                overflow: 'visible',
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: '0 12px 40px rgba(0, 0, 0, 0.15)',
                },
              }}
            >
              {/* Status Badge */}
              <Box
                sx={{
                  position: 'absolute',
                  top: 16,
                  right: 16,
                  zIndex: 1,
                }}
              >
                <Chip
                  label={model.status === 'active' ? 'Active' : 'Coming Soon'}
                  size="small"
                  sx={{
                    bgcolor: getStatusColor(model.status),
                    color: 'white',
                    fontWeight: 600,
                    fontSize: '0.7rem',
                  }}
                />
              </Box>

              <CardContent sx={{ flexGrow: 1, pt: 3 }}>
                {/* Icon */}
                <Box
                  sx={{
                    width: 72,
                    height: 72,
                    background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.primary.main, 0.05)} 100%)`,
                    borderRadius: 3,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    mb: 2,
                    color: 'primary.main',
                  }}
                >
                  {model.icon}
                </Box>

                {/* Title & Description */}
                <Typography variant="h5" sx={{ fontWeight: 700, mb: 1.5 }}>
                  {model.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {model.description}
                </Typography>

                {/* Metadata */}
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip
                    label={model.complexity}
                    size="small"
                    sx={{
                      bgcolor: alpha(getComplexityColor(model.complexity), 0.1),
                      color: getComplexityColor(model.complexity),
                      fontSize: '0.7rem',
                      fontWeight: 600,
                    }}
                  />
                  <Chip
                    label={model.timeToComplete}
                    size="small"
                    variant="outlined"
                    sx={{ fontSize: '0.7rem' }}
                  />
                </Stack>

                {/* Features */}
                <Box>
                  <Typography variant="caption" sx={{ fontWeight: 600, color: 'text.secondary', mb: 1, display: 'block' }}>
                    Key Features:
                  </Typography>
                  <Stack spacing={0.5}>
                    {model.features.slice(0, 4).map((feature, idx) => (
                      <Stack key={idx} direction="row" spacing={1} alignItems="center">
                        <Box
                          sx={{
                            width: 4,
                            height: 4,
                            borderRadius: '50%',
                            bgcolor: 'primary.main',
                          }}
                        />
                        <Typography variant="caption" color="text.secondary">
                          {feature}
                        </Typography>
                      </Stack>
                    ))}
                    {model.features.length > 4 && (
                      <Typography variant="caption" sx={{ color: 'primary.main', fontWeight: 600, pl: 2 }}>
                        +{model.features.length - 4} more features
                      </Typography>
                    )}
                  </Stack>
                </Box>
              </CardContent>

              <CardActions sx={{ p: 2, pt: 0 }}>
                <Button
                  variant={model.status === 'active' ? 'contained' : 'outlined'}
                  fullWidth
                  endIcon={<ArrowIcon />}
                  onClick={() => model.status === 'active' && navigate(model.path)}
                  disabled={model.status !== 'active'}
                  sx={{
                    py: 1.25,
                    fontWeight: 600,
                    ...(model.status === 'active' && {
                      background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                    }),
                  }}
                >
                  {model.status === 'active' ? 'Open Model' : 'Coming Soon'}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Info Footer */}
      <Box
        sx={{
          mt: 6,
          p: 3,
          bgcolor: alpha('#3b82f6', 0.05),
          borderRadius: 2,
          border: `1px solid ${alpha('#3b82f6', 0.1)}`,
        }}
      >
        <Stack direction="row" spacing={2} alignItems="start">
          <AnalysisIcon sx={{ color: 'primary.main', mt: 0.5 }} />
          <Box>
            <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 0.5 }}>
              Professional-Grade Financial Models
            </Typography>
            <Typography variant="body2" color="text.secondary">
              All models include comprehensive worksheets, sensitivity analysis, and institutional-quality formulas
              validated for accuracy. Perfect for investment banking, private equity, corporate development, and
              financial analysis professionals.
            </Typography>
          </Box>
        </Stack>
      </Box>
    </Box>
  );
};
