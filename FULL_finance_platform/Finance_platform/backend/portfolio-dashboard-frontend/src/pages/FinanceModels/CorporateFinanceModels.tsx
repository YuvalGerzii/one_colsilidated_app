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
} from '@mui/material';
import { Assessment as AssessmentIcon, OpenInNew as OpenInNewIcon, Refresh as RefreshIcon } from '@mui/icons-material';

import { API_BASE_URL } from '@/services/api';

const buildToolsUrl = (path: string): string => {
  const normalizedBase = API_BASE_URL.replace(/\/$/, '');
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${normalizedBase}${normalizedPath}`;
};

const TOOLS_LANDING_PATH = '/finance/models';

export const CorporateFinanceModels: React.FC = () => {
  const [isIframeLoaded, setIframeLoaded] = useState(false);
  const [iframeKey, setIframeKey] = useState(0);

  const landingUrl = useMemo(() => buildToolsUrl(TOOLS_LANDING_PATH), []);

  return (
    <Stack spacing={3}>
      <Box>
        <Typography variant="h4" gutterBottom>
          Corporate Finance Modeling Studio
        </Typography>
        <Typography color="text.secondary">
          Run discounted cash flow, leveraged buyout, and valuation comparison models directly in the browser with the same
          assumptions and layouts delivered in Excel.
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} justifyContent="space-between" alignItems={{ md: 'center' }}>
            <Box>
              <Typography variant="h6" gutterBottom>
                Launch DCF, LBO, and valuation comparison services
              </Typography>
              <Typography variant="body2" color="text.secondary">
                The embedded workspace mirrors our institutional templates and renders every table and chart used for IC
                materials.
              </Typography>
            </Box>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1.5}>
              <Button
                href={landingUrl}
                target="_blank"
                rel="noopener noreferrer"
                variant="contained"
                startIcon={<OpenInNewIcon />}
              >
                Open in New Tab
              </Button>
              <Button
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={() => {
                  setIframeLoaded(false);
                  setIframeKey((prev) => prev + 1);
                }}
              >
                Refresh Embed
              </Button>
            </Stack>
          </Stack>
        </CardContent>
      </Card>

      <Card sx={{ overflow: 'hidden', minHeight: { xs: 500, md: 720 } }}>
        <Box sx={{ position: 'relative', height: '100%' }}>
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
              <CircularProgress />
              <Typography variant="body2" color="text.secondary">
                Loading corporate finance tools…
              </Typography>
            </Stack>
          )}
          <Box
            component="iframe"
            key={iframeKey}
            src={landingUrl}
            title="Corporate Finance Models"
            sx={{
              border: 0,
              width: '100%',
              height: { xs: 500, md: 720 },
            }}
            onLoad={() => setIframeLoaded(true)}
          />
        </Box>
      </Card>

      <Alert icon={<AssessmentIcon fontSize="small" />} severity="info">
        Use the comparison model to benchmark DCF and LBO valuations against trading and transaction comps without leaving the
        dashboard.
      </Alert>
    </Stack>
  );
};

export default CorporateFinanceModels;
