import React, { useMemo, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Stack,
  Typography,
  Grid,
  Chip,
} from '@mui/material';
import {
  OpenInNew as OpenInNewIcon,
  Refresh as RefreshIcon,
  HomeWork as HomeWorkIcon,
  Home as HomeIcon,
  Apartment as ApartmentIcon,
  Hotel as HotelIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';

import { API_BASE_URL } from '@/services/api';
import { PageHeader } from '../../components/common/PageHeader';

const buildToolsUrl = (path: string): string => {
  const normalizedBase = API_BASE_URL.replace(/\/$/, '');
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${normalizedBase}${normalizedPath}`;
};

const TOOLS_LANDING_PATH = '/real-estate/tools';

const MODEL_TYPES = [
  {
    title: 'Fix & Flip',
    description: 'Short-term value-add residential projects',
    icon: <HomeIcon fontSize="large" />,
    color: '#1976d2',
  },
  {
    title: 'Single Family Rental',
    description: 'Long-term buy-and-hold analysis',
    icon: <HomeWorkIcon fontSize="large" />,
    color: '#2e7d32',
  },
  {
    title: 'Multifamily',
    description: '2-6 units and 7+ units extended analysis',
    icon: <ApartmentIcon fontSize="large" />,
    color: '#9c27b0',
  },
  {
    title: 'Hotel',
    description: 'Hospitality investment modeling',
    icon: <HotelIcon fontSize="large" />,
    color: '#ed6c00',
  },
  {
    title: 'Mixed-Use',
    description: 'Combined commercial and residential',
    icon: <BusinessIcon fontSize="large" />,
    color: '#1565c0',
  },
];

export const RealEstateTools: React.FC = () => {
  const [isIframeLoaded, setIframeLoaded] = useState(false);
  const [iframeKey, setIframeKey] = useState(0);

  const landingUrl = useMemo(() => buildToolsUrl(TOOLS_LANDING_PATH), []);

  return (
    <Stack spacing={4}>
      <PageHeader
        title="Real Estate Models Workbench"
        description="Launch institutional-grade fix & flip, rental, multifamily, and hotel models directly inside the dashboard."
        icon={HomeWorkIcon}
        secondaryActions={[
          {
            label: 'Open in New Tab',
            onClick: () => window.open(landingUrl, '_blank'),
            icon: OpenInNewIcon,
          },
          {
            label: 'Refresh',
            onClick: () => {
              setIframeLoaded(false);
              setIframeKey((prev) => prev + 1);
            },
            icon: RefreshIcon,
          },
        ]}
      />

      {/* Model Types Grid */}
      <Grid container spacing={3}>
        {MODEL_TYPES.map((model, index) => (
          <Grid item xs={12} sm={6} md={4} lg={2.4} key={index}>
            <Card
              sx={{
                height: '100%',
                textAlign: 'center',
                transition: 'all 0.3s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 6,
                },
              }}
            >
              <CardContent>
                <Box
                  sx={{
                    width: 64,
                    height: 64,
                    borderRadius: 2,
                    bgcolor: `${model.color}15`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    mx: 'auto',
                    mb: 2,
                  }}
                >
                  {React.cloneElement(model.icon, { sx: { color: model.color } })}
                </Box>
                <Typography variant="h6" gutterBottom>
                  {model.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {model.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Embedded Tools */}
      <Card sx={{ overflow: 'hidden', minHeight: { xs: 500, md: 720 } }}>
        <CardContent sx={{ p: 0 }}>
          <Box sx={{ position: 'relative', height: { xs: 500, md: 720 } }}>
            {!isIframeLoaded && (
              <Stack
                spacing={2}
                alignItems="center"
                justifyContent="center"
                sx={{
                  position: 'absolute',
                  inset: 0,
                  bgcolor: 'background.default',
                  zIndex: 1,
                }}
              >
                <CircularProgress size={60} />
                <Typography variant="h6" color="text.secondary">
                  Loading real estate tools…
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Preparing models and calculators
                </Typography>
              </Stack>
            )}
            <Box
              component="iframe"
              key={iframeKey}
              src={landingUrl}
              title="Real Estate Tools"
              sx={{
                border: 0,
                width: '100%',
                height: '100%',
                display: isIframeLoaded ? 'block' : 'none',
              }}
              onLoad={() => setIframeLoaded(true)}
            />
          </Box>
        </CardContent>
      </Card>

      {/* Help Section */}
      <Alert severity="info" icon={<HotelIcon />}>
        <Typography variant="subtitle2" gutterBottom>
          Need help getting started?
        </Typography>
        <Typography variant="body2">
          Use the tabs within each model to view outputs exactly as the Excel workbooks, download reports, and capture screenshots for investment memos.
          All models support multi-scenario analysis and sensitivity tables.
        </Typography>
      </Alert>
    </Stack>
  );
};
