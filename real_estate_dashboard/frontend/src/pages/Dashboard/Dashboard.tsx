import React from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Stack,
  Button,
  Paper,
  Avatar,
  Chip,
  useTheme,
  alpha,
} from '@mui/material';
import {
  HomeWork as HomeWorkIcon,
  Assessment as AssessmentIcon,
  Speed as SpeedIcon,
  Analytics as AnalyticsIcon,
  ArrowForward as ArrowForwardIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  const features = [
    {
      icon: HomeWorkIcon,
      title: 'Property Management',
      description: 'Manage your entire portfolio with comprehensive tracking of properties, units, leases, and maintenance.',
      color: theme.palette.primary.main,
      path: '/property-management',
    },
    {
      icon: AssessmentIcon,
      title: 'Financial Models',
      description: 'Run institutional-grade real estate models including fix & flip, rentals, multifamily, and mixed-use.',
      color: theme.palette.secondary.main,
      path: '/real-estate-tools',
    },
    {
      icon: AnalyticsIcon,
      title: 'ROI Analytics',
      description: 'Calculate IRR, cash-on-cash returns, cap rates, and other key performance indicators.',
      color: theme.palette.info.main,
      path: '/property-management',
    },
    {
      icon: SpeedIcon,
      title: 'Real-time Updates',
      description: 'All metrics and dashboards update automatically with the latest data.',
      color: theme.palette.warning.main,
      path: '/property-management',
    },
  ];

  const benefits = [
    'Track unlimited properties and units',
    'Institutional-grade financial models',
    'Real-time portfolio analytics',
    'Professional reports and exports',
    'Maintenance tracking system',
    'Lease management and alerts',
  ];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Hero Section */}
      <Box
        sx={{
          background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
          color: 'white',
          pt: 8,
          pb: 12,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={7}>
              <Stack spacing={3}>
                <Chip
                  label="Professional Real Estate Platform"
                  sx={{
                    bgcolor: alpha(theme.palette.common.white, 0.2),
                    color: 'white',
                    fontWeight: 600,
                    width: 'fit-content',
                  }}
                />
                <Typography variant="h2" fontWeight="bold" sx={{ fontSize: { xs: '2rem', md: '3rem' } }}>
                  Real Estate Dashboard
                </Typography>
                <Typography variant="h5" sx={{ opacity: 0.9, fontWeight: 400 }}>
                  Comprehensive property management and institutional-grade financial modeling in one powerful platform
                </Typography>
                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} sx={{ mt: 2 }}>
                  <Button
                    variant="contained"
                    size="large"
                    endIcon={<ArrowForwardIcon />}
                    onClick={() => navigate('/property-management')}
                    sx={{
                      bgcolor: 'white',
                      color: 'primary.main',
                      '&:hover': {
                        bgcolor: alpha(theme.palette.common.white, 0.9),
                      },
                    }}
                  >
                    Property Management
                  </Button>
                  <Button
                    variant="outlined"
                    size="large"
                    endIcon={<ArrowForwardIcon />}
                    onClick={() => navigate('/real-estate-tools')}
                    sx={{
                      borderColor: 'white',
                      color: 'white',
                      '&:hover': {
                        borderColor: 'white',
                        bgcolor: alpha(theme.palette.common.white, 0.1),
                      },
                    }}
                  >
                    Financial Models
                  </Button>
                </Stack>
              </Stack>
            </Grid>
            <Grid item xs={12} md={5} sx={{ display: { xs: 'none', md: 'block' } }}>
              <Box
                sx={{
                  position: 'relative',
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                }}
              >
                <Box
                  sx={{
                    width: 300,
                    height: 300,
                    borderRadius: '50%',
                    bgcolor: alpha(theme.palette.common.white, 0.1),
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    animation: 'pulse 2s ease-in-out infinite',
                    '@keyframes pulse': {
                      '0%, 100%': { transform: 'scale(1)' },
                      '50%': { transform: 'scale(1.05)' },
                    },
                  }}
                >
                  <HomeWorkIcon sx={{ fontSize: 150, opacity: 0.8 }} />
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ mt: -6, mb: 8 }}>
        <Grid container spacing={3}>
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Card
                  sx={{
                    height: '100%',
                    cursor: 'pointer',
                    transition: 'all 0.3s',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: 6,
                    },
                  }}
                  onClick={() => navigate(feature.path)}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Stack spacing={2}>
                      <Avatar
                        sx={{
                          bgcolor: alpha(feature.color, 0.1),
                          width: 56,
                          height: 56,
                        }}
                      >
                        <Icon sx={{ fontSize: 32, color: feature.color }} />
                      </Avatar>
                      <Typography variant="h6" fontWeight="bold">
                        {feature.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {feature.description}
                      </Typography>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      </Container>

      {/* Benefits Section */}
      <Container maxWidth="lg" sx={{ mb: 8 }}>
        <Paper
          elevation={0}
          sx={{
            p: 6,
            background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
            borderRadius: 3,
          }}
        >
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h4" fontWeight="bold" gutterBottom>
                Everything you need to manage and analyze real estate
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Our platform combines powerful property management tools with institutional-grade financial modeling capabilities.
              </Typography>
              <Stack spacing={2} sx={{ mt: 3 }}>
                {benefits.map((benefit, index) => (
                  <Stack key={index} direction="row" spacing={2} alignItems="center">
                    <CheckCircleIcon sx={{ color: 'success.main' }} />
                    <Typography variant="body1">{benefit}</Typography>
                  </Stack>
                ))}
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  bgcolor: 'white',
                  p: 4,
                  borderRadius: 2,
                  boxShadow: 3,
                }}
              >
                <Stack spacing={3}>
                  <Box>
                    <Typography variant="h3" fontWeight="bold" color="primary.main">
                      12+
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Properties Tracked
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="h3" fontWeight="bold" color="secondary.main">
                      148+
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Units Managed
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="h3" fontWeight="bold" color="info.main">
                      6
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Financial Models
                    </Typography>
                  </Box>
                </Stack>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      </Container>

      {/* CTA Section */}
      <Container maxWidth="md" sx={{ mb: 8, textAlign: 'center' }}>
        <Paper
          elevation={0}
          sx={{
            p: 6,
            background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
            color: 'white',
            borderRadius: 3,
          }}
        >
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Ready to get started?
          </Typography>
          <Typography variant="h6" sx={{ mb: 4, opacity: 0.9 }}>
            Explore the platform and see how it can transform your real estate operations
          </Typography>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} justifyContent="center">
            <Button
              variant="contained"
              size="large"
              endIcon={<ArrowForwardIcon />}
              onClick={() => navigate('/property-management')}
              sx={{
                bgcolor: 'white',
                color: 'primary.main',
                '&:hover': {
                  bgcolor: alpha(theme.palette.common.white, 0.9),
                },
              }}
            >
              Start Managing Properties
            </Button>
            <Button
              variant="outlined"
              size="large"
              endIcon={<ArrowForwardIcon />}
              onClick={() => navigate('/real-estate-tools')}
              sx={{
                borderColor: 'white',
                color: 'white',
                '&:hover': {
                  borderColor: 'white',
                  bgcolor: alpha(theme.palette.common.white, 0.1),
                },
              }}
            >
              Explore Financial Models
            </Button>
          </Stack>
        </Paper>
      </Container>
    </Box>
  );
};
