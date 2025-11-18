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
import {
  OpenInNew as OpenInNewIcon,
  Refresh as RefreshIcon,
  SvgIconComponent,
} from '@mui/icons-material';

import { API_BASE_URL } from '@/services/apiClient';
import { PageHeader } from '../../components/common/PageHeader';

interface ModelPageProps {
  modelSlug: string;
  title: string;
  description: string;
  icon: SvgIconComponent;
}

const buildModelUrl = (modelSlug: string): string => {
  const normalizedBase = API_BASE_URL.replace(/\/$/, '');
  // Convert dashes to underscores for backend compatibility
  const backendSlug = modelSlug.replace(/-/g, '_');
  return `${normalizedBase}/real-estate/tools/${backendSlug}`;
};

export const ModelPage: React.FC<ModelPageProps> = ({
  modelSlug,
  title,
  description,
  icon: Icon,
}) => {
  const [isIframeLoaded, setIframeLoaded] = useState(false);
  const [iframeKey, setIframeKey] = useState(0);

  const modelUrl = useMemo(() => buildModelUrl(modelSlug), [modelSlug]);

  const handleRefresh = () => {
    setIframeLoaded(false);
    setIframeKey((prev) => prev + 1);
  };

  const handleOpenInNewTab = () => {
    window.open(modelUrl, '_blank');
  };

  return (
    <Stack spacing={4}>
      <PageHeader
        title={title}
        description={description}
        icon={Icon}
        secondaryActions={[
          {
            label: 'Open in New Tab',
            onClick: handleOpenInNewTab,
            icon: OpenInNewIcon,
          },
          {
            label: 'Refresh',
            onClick: handleRefresh,
            icon: RefreshIcon,
          },
        ]}
      />

      {/* Embedded Model */}
      <Card sx={{ overflow: 'hidden', minHeight: { xs: 600, md: 800 } }}>
        <CardContent sx={{ p: 0 }}>
          <Box sx={{ position: 'relative', height: { xs: 600, md: 800 } }}>
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
                  Loading {title}…
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Preparing model interface
                </Typography>
              </Stack>
            )}
            <Box
              component="iframe"
              key={iframeKey}
              src={modelUrl}
              title={title}
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
      <Alert severity="info" icon={<Icon />}>
        <Typography variant="subtitle2" gutterBottom>
          How to use this model
        </Typography>
        <Typography variant="body2">
          Adjust the input parameters in the form on the left, then click "Run analysis" to generate
          detailed financial projections, tables, and charts. All calculations mirror the Excel workbook
          methodology. You can download results or open in a new tab for full-screen analysis.
        </Typography>
      </Alert>
    </Stack>
  );
};
