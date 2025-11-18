import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Alert,
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  IconButton,
  LinearProgress,
  MenuItem,
  Stack,
  TextField,
  Tooltip,
  Typography,
} from '@mui/material';
import {
  AccountBalance as AccountBalanceIcon,
  Timeline as TimelineIcon,
  Handshake as HandshakeIcon,
  Checklist as ChecklistIcon,
  Assessment as AssessmentIcon,
  InfoOutlined as InfoOutlinedIcon,
  Download as DownloadIcon,
  Description as DescriptionIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';

import { useModelGeneration } from '../../hooks/useModels';
import { useCompanies } from '../../hooks/useCompanies';
import { modelService } from '../../services/models';
import { PageHeader } from '../../components/common/PageHeader';
import { EmptyState } from '../../components/common/EmptyState';
import { PageSkeleton } from '../../components/common/LoadingSkeleton';

const MODEL_CARD_LAYOUT = [
  { key: 'dcf', title: 'Discounted Cash Flow', description: 'Intrinsic valuation with multi-scenario cash flow modeling.', sheets: '13 sheets / 600+ formulas', icon: <AccountBalanceIcon fontSize="large" /> },
  { key: 'lbo', title: 'Leveraged Buyout', description: 'Capital structure modeling with returns, debt tranches, and sensitivities.', sheets: '12 sheets / 500+ formulas', icon: <TimelineIcon fontSize="large" /> },
  { key: 'merger', title: 'Merger Model', description: 'Accretion / dilution, pro forma adjustments, and synergy tracking.', sheets: '9 sheets / 420+ formulas', icon: <HandshakeIcon fontSize="large" /> },
  { key: 'dd', title: 'Due Diligence Tracker', description: 'Comprehensive checklist tracker with owners, dates, and completion KPIs.', sheets: '8 trackers / 140 tasks', icon: <ChecklistIcon fontSize="large" /> },
  { key: 'qoe', title: 'Quality of Earnings', description: 'Bridge adjustments, working capital analysis, and variance commentary.', sheets: '6 sheets / 315+ formulas', icon: <AssessmentIcon fontSize="large" /> },
] as const;

type ModelKey = (typeof MODEL_CARD_LAYOUT)[number]['key'];
type GenerationStatus = 'idle' | 'loading' | 'success' | 'error';

const STATUS_LABELS: Record<GenerationStatus, string> = {
  idle: 'Idle',
  loading: 'Generating…',
  success: 'Ready',
  error: 'Retry needed',
};

const STATUS_COLOR: Record<GenerationStatus, 'default' | 'primary' | 'success' | 'error' | 'warning'> = {
  idle: 'default',
  loading: 'primary',
  success: 'success',
  error: 'error',
};

export const ModelGenerator: React.FC = () => {
  const params = useParams<{ companyId?: string }>();
  const { companies, loading: companiesLoading } = useCompanies();
  const { generate, loading, error, data, reset } = useModelGeneration();

  const [selectedCompany, setSelectedCompany] = useState<string>('');
  const [activeModel, setActiveModel] = useState<ModelKey | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogProgress, setDialogProgress] = useState(0);
  const [statuses, setStatuses] = useState<Record<ModelKey, GenerationStatus>>({
    dcf: 'idle',
    lbo: 'idle',
    merger: 'idle',
    dd: 'idle',
    qoe: 'idle',
  });
  const [downloads, setDownloads] = useState<Record<ModelKey, string | undefined>>({
    dcf: undefined,
    lbo: undefined,
    merger: undefined,
    dd: undefined,
    qoe: undefined,
  });
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(
    null
  );

  useEffect(() => {
    if (params.companyId) {
      setSelectedCompany(params.companyId);
    }
  }, [params.companyId]);

  useEffect(() => {
    if (!params.companyId && companies.length && !selectedCompany) {
      setSelectedCompany(companies[0].company_id);
    }
  }, [companies, params.companyId, selectedCompany]);

  useEffect(() => {
    let timer: ReturnType<typeof setInterval> | null = null;
    if (dialogOpen && loading) {
      setDialogProgress((prev) => (prev < 15 ? 15 : prev));
      timer = setInterval(() => {
        setDialogProgress((prev) => {
          if (prev >= 90) {
            return prev;
          }
          return prev + Math.floor(Math.random() * 10 + 5);
        });
      }, 450);
    }

    if (!loading && dialogOpen && activeModel) {
      setDialogProgress(100);
    }

    return () => {
      if (timer) {
        clearInterval(timer);
      }
    };
  }, [dialogOpen, loading, activeModel]);

  useEffect(() => {
    if (!loading && activeModel) {
      if (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unable to generate model.';
        setStatuses((prev) => ({ ...prev, [activeModel]: 'error' }));
        setFeedback({ type: 'error', message: errorMessage });
        setDialogOpen(false);
      } else if (data) {
        const filePath = data[activeModel as keyof typeof data];
        setStatuses((prev) => ({ ...prev, [activeModel]: 'success' }));
        setDownloads((prev) => ({ ...prev, [activeModel]: filePath }));
        setFeedback({
          type: 'success',
          message: `${MODEL_CARD_LAYOUT.find((card) => card.key === activeModel)?.title || 'Model'} generated successfully.`,
        });
        setDialogOpen(false);
      }
    }
  }, [loading, error, data, activeModel]);

  const handleGenerate = (model: ModelKey) => {
    if (!selectedCompany) {
      setFeedback({ type: 'error', message: 'Please select a company to generate models for.' });
      return;
    }

    setActiveModel(model);
    setDialogOpen(true);
    setDialogProgress(10);
    setStatuses((prev) => ({ ...prev, [model]: 'loading' }));
    setFeedback(null);
    reset();
    const requestedModel: Partial<Record<ModelKey, boolean>> = { [model]: true };
    generate({
      company_id: selectedCompany,
      models: requestedModel,
      scenario: 'base',
    });
  };

  const handleDialogClose = () => {
    if (!loading) {
      setDialogOpen(false);
    }
  };

  const handleFeedbackClose = () => setFeedback(null);

  const companyOptions = useMemo(
    () =>
      companies.map((company) => ({
        label: company.company_name,
        value: company.company_id,
      })),
    [companies]
  );

  // Show loading state
  if (companiesLoading && companies.length === 0) {
    return <PageSkeleton type="form" />;
  }

  // Show empty state when no companies exist
  if (!companiesLoading && companies.length === 0) {
    return (
      <EmptyState
        icon={DescriptionIcon}
        title="No companies available"
        description="You need to add a portfolio company before you can generate financial models."
        actionLabel="Add Company"
        onAction={() => window.location.href = '/companies/new'}
      />
    );
  }

  return (
    <Stack spacing={4}>
      <PageHeader
        title="Model Generator"
        description="Launch pre-built deal models with guided tooling and instant download links."
        icon={DescriptionIcon}
      >
        <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} alignItems={{ md: 'center' }} sx={{ mt: 3 }}>
          <TextField
            select
            fullWidth
            disabled={companiesLoading}
            label="Select Company"
            value={selectedCompany}
            onChange={(event) => setSelectedCompany(event.target.value)}
            sx={{ maxWidth: { md: 400 } }}
          >
            {companyOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={() => reset()}
          >
            Reset All
          </Button>
        </Stack>
      </PageHeader>

      <Grid container spacing={3}>
        {MODEL_CARD_LAYOUT.map((card) => (
          <Grid item xs={12} md={6} lg={4} key={card.key}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'all 0.3s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 6,
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start" mb={2}>
                  <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-start' }}>
                    <Box
                      sx={{
                        p: 1.5,
                        borderRadius: 2,
                        bgcolor: 'primary.lighter',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      {card.icon}
                    </Box>
                    <Box>
                      <Typography variant="h6" gutterBottom>
                        {card.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {card.description}
                      </Typography>
                    </Box>
                  </Box>
                  <Tooltip title="Learn what this model includes">
                    <IconButton size="small">
                      <InfoOutlinedIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </Stack>
                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 2 }}>
                  {card.sheets}
                </Typography>
                <Box>
                  <Chip
                    label={STATUS_LABELS[statuses[card.key]]}
                    color={STATUS_COLOR[statuses[card.key]]}
                    size="small"
                  />
                </Box>
                {downloads[card.key] && (
                  <Button
                    sx={{ mt: 2 }}
                    size="small"
                    fullWidth
                    variant="outlined"
                    startIcon={<DownloadIcon />}
                    href={modelService.downloadUrl(downloads[card.key] as string)}
                  >
                    Download Latest
                  </Button>
                )}
              </CardContent>
              <CardActions sx={{ px: 3, pb: 3 }}>
                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => handleGenerate(card.key)}
                  disabled={loading && activeModel === card.key || !selectedCompany}
                >
                  {loading && activeModel === card.key ? 'Generating…' : 'Generate Model'}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={dialogOpen} onClose={handleDialogClose} fullWidth maxWidth="sm">
        <DialogTitle>Generating model</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Preparing Excel workbook and downloading source data…
          </Typography>
          <LinearProgress variant="determinate" value={dialogProgress} sx={{ mt: 2 }} />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose} disabled={loading}>
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {feedback && (
        <Alert
          severity={feedback.type}
          onClose={handleFeedbackClose}
          sx={{ mt: 2 }}
        >
          {feedback.message}
        </Alert>
      )}
    </Stack>
  );
};
