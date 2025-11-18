import React, { useMemo, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  FormControl,
  InputLabel,
  LinearProgress,
  MenuItem,
  Select,
  SelectChangeEvent,
  Snackbar,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { PictureAsPdf as PictureAsPdfIcon, TableView as TableViewIcon } from '@mui/icons-material';
import { useCompanies } from '../../hooks/useCompanies';

const REPORT_TYPES = [
  'Quarterly LP Report',
  'Capital Account Statement',
  'Valuation Bridge',
  'Capital Calls & Distributions',
];

export const Reports: React.FC = () => {
  const { companies } = useCompanies();
  const [reportType, setReportType] = useState<string>('Quarterly LP Report');
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [selectedCompanies, setSelectedCompanies] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [downloadsReady, setDownloadsReady] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  const companyOptions = useMemo(
    () =>
      companies.map((company) => ({
        label: company.company_name,
        value: company.company_id,
      })),
    [companies]
  );

  const handleCompanyChange = (event: SelectChangeEvent<string[]>) => {
    const {
      target: { value },
    } = event;
    setSelectedCompanies(typeof value === 'string' ? value.split(',') : value);
  };

  const generateReport = () => {
    if (!startDate || !endDate || selectedCompanies.length === 0) {
      setSnackbarOpen(true);
      return;
    }

    setLoading(true);
    setDownloadsReady(false);
    setTimeout(() => {
      setLoading(false);
      setDownloadsReady(true);
      setSnackbarOpen(true);
    }, 1500);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        LP Reporting
      </Typography>
      <Typography variant="body1" color="text.secondary" mb={4}>
        Package quarterly updates with multi-company selections, async generation, and downloadable outputs.
      </Typography>

      <Card>
        <CardContent>
          <Stack spacing={3}>
            <FormControl fullWidth>
              <InputLabel id="report-type-label">Report type</InputLabel>
              <Select
                labelId="report-type-label"
                value={reportType}
                label="Report type"
                onChange={(event) => setReportType(event.target.value)}
              >
                {REPORT_TYPES.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <TextField
                type="date"
                label="Start date"
                InputLabelProps={{ shrink: true }}
                value={startDate}
                onChange={(event) => setStartDate(event.target.value)}
                fullWidth
              />
              <TextField
                type="date"
                label="End date"
                InputLabelProps={{ shrink: true }}
                value={endDate}
                onChange={(event) => setEndDate(event.target.value)}
                fullWidth
              />
            </Stack>

            <FormControl fullWidth>
              <InputLabel id="company-multi-label">Companies</InputLabel>
              <Select
                labelId="company-multi-label"
                multiple
                value={selectedCompanies}
                label="Companies"
                onChange={handleCompanyChange}
                renderValue={(selected) => (
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    {selected.map((value) => {
                      const company = companyOptions.find((option) => option.value === value);
                      return <Chip key={value} label={company?.label || value} sx={{ mr: 0.5, mb: 0.5 }} />;
                    })}
                  </Stack>
                )}
              >
                {companyOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {loading && <LinearProgress />}

            {downloadsReady && (
              <Alert severity="success">
                Reports generated. Download the formatted packages below.
              </Alert>
            )}

            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <Button
                variant="contained"
                size="large"
                onClick={generateReport}
                disabled={loading}
              >
                {loading ? 'Generating…' : 'Generate Report'}
              </Button>
              {downloadsReady && (
                <Stack direction="row" spacing={2}>
                  <Button variant="outlined" startIcon={<PictureAsPdfIcon />}>
                    Download PDF
                  </Button>
                  <Button variant="outlined" startIcon={<TableViewIcon />}>
                    Download Excel
                  </Button>
                </Stack>
              )}
            </Stack>
          </Stack>
        </CardContent>
      </Card>

      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        message={
          !startDate || !endDate || selectedCompanies.length === 0
            ? 'Select a date range and at least one company.'
            : downloadsReady
            ? 'Reports ready for download.'
            : 'Generating reports…'
        }
      />
    </Box>
  );
};
