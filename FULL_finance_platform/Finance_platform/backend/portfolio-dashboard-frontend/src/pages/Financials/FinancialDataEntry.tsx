import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  MenuItem,
  Stack,
  Switch,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
  Typography,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { useCompanies } from '../../hooks/useCompanies';

const METRIC_FIELDS = [
  { key: 'revenue', label: 'Revenue' },
  { key: 'ebitda', label: 'EBITDA' },
  { key: 'cashFlow', label: 'Operating Cash Flow' },
  { key: 'grossMargin', label: 'Gross Margin %' },
  { key: 'operatingIncome', label: 'Operating Income' },
  { key: 'netIncome', label: 'Net Income' },
  { key: 'arr', label: 'ARR' },
  { key: 'churn', label: 'Customer Churn %' },
  { key: 'capex', label: 'CapEx' },
  { key: 'workingCapital', label: 'Working Capital' },
  { key: 'debt', label: 'Total Debt' },
  { key: 'equity', label: 'Equity Invested' },
  { key: 'headcount', label: 'Headcount' },
  { key: 'cashBalance', label: 'Ending Cash Balance' },
  { key: 'lenderCovenant', label: 'Lender Covenant Ratio' },
] as const;

type MetricKey = (typeof METRIC_FIELDS)[number]['key'];

type FinancialFormValues = {
  companyId: string;
  period: 'Q1' | 'Q2' | 'Q3' | 'Q4' | 'Annual';
  metrics: Partial<Record<MetricKey, number | ''>>;
};

const defaultMetrics = METRIC_FIELDS.reduce<Partial<Record<MetricKey, number | ''>>>(
  (acc, field) => ({ ...acc, [field.key]: '' }),
  {}
);

export const FinancialDataEntry: React.FC = () => {
  const { companies, loading } = useCompanies();
  const [autoSave, setAutoSave] = useState(true);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const initialRender = useRef(true);

  const {
    control,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<FinancialFormValues>({
    defaultValues: {
      companyId: '',
      period: 'Q1',
      metrics: defaultMetrics,
    },
  });

  const selectedCompany = watch('companyId');
  const selectedPeriod = watch('period');
  const metricValues = watch('metrics');

  useEffect(() => {
    if (companies.length && !selectedCompany) {
      setValue('companyId', companies[0].company_id);
    }
  }, [companies, selectedCompany, setValue]);

  const companyName = useMemo(
    () => companies.find((company) => company.company_id === selectedCompany)?.company_name,
    [companies, selectedCompany]
  );

  useEffect(() => {
    if (initialRender.current) {
      initialRender.current = false;
      return;
    }

    if (!autoSave || !selectedCompany) {
      return;
    }

    setSaving(true);
    const timeout = setTimeout(() => {
      setSaving(false);
      setSaveMessage(`Auto-saved ${selectedPeriod} financials for ${companyName || 'selected company'}.`);
    }, 900);

    return () => clearTimeout(timeout);
  }, [metricValues, autoSave, selectedCompany, selectedPeriod, companyName]);

  const onSubmit = handleSubmit((values) => {
    setSaving(true);
    setTimeout(() => {
      setSaving(false);
      setSaveMessage(
        `Saved ${values.period} metrics for ${
          companies.find((company) => company.company_id === values.companyId)?.company_name || 'selected company'
        }.`
      );
    }, 900);
  });

  return (
    <Box component="form" onSubmit={onSubmit}>
      <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" mb={4} spacing={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Financial Data Entry
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Capture quarter-over-quarter metrics, enforce numeric validation, and keep models in sync.
          </Typography>
        </Box>
        <Stack direction="row" spacing={3}>
          <Stack alignItems="center" direction="row" spacing={1}>
            <Typography variant="body2" color="text.secondary">
              Auto-save
            </Typography>
            <Switch checked={autoSave} onChange={() => setAutoSave((prev) => !prev)} />
          </Stack>
        </Stack>
      </Stack>

      <Card>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Controller
                name="companyId"
                control={control}
                rules={{ required: 'Select a company' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Company"
                    fullWidth
                    disabled={loading}
                    error={Boolean(errors.companyId)}
                    helperText={errors.companyId?.message}
                  >
                    {companies.map((company) => (
                      <MenuItem key={company.company_id} value={company.company_id}>
                        {company.company_name}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Controller
                name="period"
                control={control}
                render={({ field: { value, onChange } }) => (
                  <ToggleButtonGroup
                    value={value}
                    exclusive
                    onChange={(_, newValue) => newValue && onChange(newValue)}
                    fullWidth
                    color="primary"
                  >
                    <ToggleButton value="Q1">Q1</ToggleButton>
                    <ToggleButton value="Q2">Q2</ToggleButton>
                    <ToggleButton value="Q3">Q3</ToggleButton>
                    <ToggleButton value="Q4">Q4</ToggleButton>
                    <ToggleButton value="Annual">Annual</ToggleButton>
                  </ToggleButtonGroup>
                )}
              />
            </Grid>
            {METRIC_FIELDS.map((field) => (
              <Grid item xs={12} md={6} key={field.key}>
                <Controller
                  name={`metrics.${field.key}` as const}
                  control={control}
                  rules={{
                    required: 'Required',
                    pattern: {
                      value: /^-?\d*(\.\d+)?$/,
                      message: 'Numbers only',
                    },
                  }}
                  render={({ field: controllerField, fieldState }) => (
                    <TextField
                      {...controllerField}
                      label={field.label}
                      fullWidth
                      placeholder="Enter value"
                      inputMode="decimal"
                      error={Boolean(fieldState.error)}
                      helperText={fieldState.error?.message || ' '}
                    />
                  )}
                />
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="flex-end" spacing={2} mt={4}>
        <Button variant="outlined" onClick={() => setValue('metrics', { ...defaultMetrics })}>
          Reset values
        </Button>
        <Button type="submit" variant="contained" size="large" disabled={saving}>
          {saving ? 'Saving…' : 'Save'}
        </Button>
      </Stack>

      {saveMessage && (
        <Alert severity={autoSave ? 'info' : 'success'} sx={{ mt: 3 }} onClose={() => setSaveMessage(null)}>
          {saveMessage}
        </Alert>
      )}
    </Box>
  );
};
