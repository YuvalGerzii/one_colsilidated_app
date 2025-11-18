import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Stepper,
  Step,
  StepLabel,
  Button,
  TextField,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Card,
  CardContent,
  Stack,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Download as DownloadIcon,
  Preview as PreviewIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

interface AccountLine {
  id: string;
  accountNumber: string;
  accountName: string;
  currentBalance: string;
  priorBalance: string;
}

export const Big4ReportGenerator: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [reportType, setReportType] = useState('balance_sheet');
  const [reportData, setReportData] = useState({
    entityName: '',
    reportingDate: '',
    currency: 'USD',
    presentation: 'thousands',
    comparativePeriod: true,
  });
  const [accounts, setAccounts] = useState<AccountLine[]>([]);

  const steps = ['Report Type', 'Entity Information', 'Account Data', 'Review & Generate'];

  const reportTypes = [
    { value: 'balance_sheet', label: 'Balance Sheet (Statement of Financial Position)', standard: 'GAAP/IFRS' },
    { value: 'income_statement', label: 'Income Statement (P&L)', standard: 'GAAP Multi-Step' },
    { value: 'cash_flow', label: 'Statement of Cash Flows', standard: 'GAAP Indirect Method' },
    { value: 'equity', label: 'Statement of Changes in Equity', standard: 'GAAP' },
    { value: 'footnotes', label: 'Financial Statement Footnotes', standard: 'Big-4 Format' },
    { value: 'audit_workpaper', label: 'Audit Lead Schedule', standard: 'Big-4 Audit Standards' },
  ];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const addAccount = () => {
    const newAccount: AccountLine = {
      id: Date.now().toString(),
      accountNumber: '',
      accountName: '',
      currentBalance: '0.00',
      priorBalance: '0.00',
    };
    setAccounts([...accounts, newAccount]);
  };

  const removeAccount = (id: string) => {
    setAccounts(accounts.filter((acc) => acc.id !== id));
  };

  const updateAccount = (id: string, field: keyof AccountLine, value: string) => {
    setAccounts(
      accounts.map((acc) => (acc.id === id ? { ...acc, [field]: value } : acc))
    );
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Select Report Type
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Choose the financial report you want to generate according to Big-4 accounting firm standards.
            </Typography>

            <Grid container spacing={2} sx={{ mt: 2 }}>
              {reportTypes.map((type) => (
                <Grid item xs={12} md={6} key={type.value}>
                  <Card
                    sx={{
                      cursor: 'pointer',
                      border: reportType === type.value ? 2 : 1,
                      borderColor: reportType === type.value ? 'primary.main' : 'divider',
                      '&:hover': {
                        borderColor: 'primary.main',
                        boxShadow: 3,
                      },
                    }}
                    onClick={() => setReportType(type.value)}
                  >
                    <CardContent>
                      <Stack spacing={1}>
                        <Typography variant="subtitle1" fontWeight="bold">
                          {type.label}
                        </Typography>
                        <Chip label={type.standard} size="small" color="primary" sx={{ width: 'fit-content' }} />
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Entity Information
            </Typography>
            <Alert severity="info" sx={{ mb: 3 }}>
              <Typography variant="body2">
                Enter the reporting entity details. All fields are required for Big-4 compliant reporting.
              </Typography>
            </Alert>

            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Legal Entity Name"
                  value={reportData.entityName}
                  onChange={(e) => setReportData({ ...reportData, entityName: e.target.value })}
                  helperText="Full legal name as registered"
                  required
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  type="date"
                  label="Reporting Period End Date"
                  value={reportData.reportingDate}
                  onChange={(e) => setReportData({ ...reportData, reportingDate: e.target.value })}
                  InputLabelProps={{ shrink: true }}
                  helperText="As of date for Balance Sheet or end date for other statements"
                  required
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Currency</InputLabel>
                  <Select
                    value={reportData.currency}
                    label="Currency"
                    onChange={(e) => setReportData({ ...reportData, currency: e.target.value })}
                  >
                    <MenuItem value="USD">USD - US Dollars</MenuItem>
                    <MenuItem value="EUR">EUR - Euros</MenuItem>
                    <MenuItem value="GBP">GBP - British Pounds</MenuItem>
                    <MenuItem value="CAD">CAD - Canadian Dollars</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Presentation Format</InputLabel>
                  <Select
                    value={reportData.presentation}
                    label="Presentation Format"
                    onChange={(e) => setReportData({ ...reportData, presentation: e.target.value })}
                  >
                    <MenuItem value="actual">Actual Amounts</MenuItem>
                    <MenuItem value="thousands">Thousands (000's)</MenuItem>
                    <MenuItem value="millions">Millions (000,000's)</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Comparative Period</InputLabel>
                  <Select
                    value={reportData.comparativePeriod ? 'yes' : 'no'}
                    label="Comparative Period"
                    onChange={(e) =>
                      setReportData({ ...reportData, comparativePeriod: e.target.value === 'yes' })
                    }
                  >
                    <MenuItem value="yes">Include Prior Year Comparative</MenuItem>
                    <MenuItem value="no">Current Period Only</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Box>
        );

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Account Data Entry
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Enter account balances according to your chart of accounts. Use Big-4 account numbering conventions.
            </Typography>

            <Box sx={{ mb: 2 }}>
              <Button variant="contained" startIcon={<AddIcon />} onClick={addAccount}>
                Add Account Line
              </Button>
            </Box>

            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: 'primary.light' }}>
                    <TableCell sx={{ fontWeight: 'bold', color: 'white' }}>Account #</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', color: 'white' }}>Account Name</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', color: 'white' }} align="right">
                      Current Balance
                    </TableCell>
                    {reportData.comparativePeriod && (
                      <TableCell sx={{ fontWeight: 'bold', color: 'white' }} align="right">
                        Prior Balance
                      </TableCell>
                    )}
                    <TableCell sx={{ fontWeight: 'bold', color: 'white' }} align="center">
                      Actions
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {accounts.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={reportData.comparativePeriod ? 5 : 4} align="center">
                        <Typography variant="body2" color="text.secondary" sx={{ py: 3 }}>
                          No accounts added yet. Click "Add Account Line" to begin.
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    accounts.map((account) => (
                      <TableRow key={account.id}>
                        <TableCell>
                          <TextField
                            size="small"
                            value={account.accountNumber}
                            onChange={(e) => updateAccount(account.id, 'accountNumber', e.target.value)}
                            placeholder="1000"
                            sx={{ width: 100 }}
                          />
                        </TableCell>
                        <TableCell>
                          <TextField
                            size="small"
                            fullWidth
                            value={account.accountName}
                            onChange={(e) => updateAccount(account.id, 'accountName', e.target.value)}
                            placeholder="Cash and Cash Equivalents"
                          />
                        </TableCell>
                        <TableCell>
                          <TextField
                            size="small"
                            type="number"
                            value={account.currentBalance}
                            onChange={(e) => updateAccount(account.id, 'currentBalance', e.target.value)}
                            inputProps={{ style: { textAlign: 'right' } }}
                            sx={{ width: 150 }}
                          />
                        </TableCell>
                        {reportData.comparativePeriod && (
                          <TableCell>
                            <TextField
                              size="small"
                              type="number"
                              value={account.priorBalance}
                              onChange={(e) => updateAccount(account.id, 'priorBalance', e.target.value)}
                              inputProps={{ style: { textAlign: 'right' } }}
                              sx={{ width: 150 }}
                            />
                          </TableCell>
                        )}
                        <TableCell align="center">
                          <IconButton size="small" color="error" onClick={() => removeAccount(account.id)}>
                            <DeleteIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>

            <Alert severity="info" sx={{ mt: 2 }}>
              <Typography variant="body2">
                <strong>Big-4 Tip:</strong> Use standard account numbering: 1000-1999 (Assets), 2000-2999
                (Liabilities), 3000-3999 (Equity), 4000-4999 (Revenue), 5000-9999 (Expenses)
              </Typography>
            </Alert>
          </Box>
        );

      case 3:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Review & Generate Report
            </Typography>

            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="subtitle2" color="primary" gutterBottom>
                  Report Configuration Summary
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="body2" color="text.secondary">
                      Report Type:
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {reportTypes.find((t) => t.value === reportType)?.label}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="body2" color="text.secondary">
                      Entity Name:
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {reportData.entityName || 'Not specified'}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="body2" color="text.secondary">
                      Reporting Date:
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {reportData.reportingDate || 'Not specified'}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="body2" color="text.secondary">
                      Accounts Entered:
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {accounts.length} accounts
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>

            <Alert severity="success" sx={{ mb: 2 }}>
              <Typography variant="body2">
                Your report is ready to generate. This will produce a Big-4 standard formatted report with proper
                presentation, footnote references, and disclosure requirements.
              </Typography>
            </Alert>

            <Stack direction="row" spacing={2}>
              <Button variant="contained" startIcon={<PreviewIcon />} size="large" sx={{ flex: 1 }}>
                Preview Report
              </Button>
              <Button variant="contained" color="success" startIcon={<DownloadIcon />} size="large" sx={{ flex: 1 }}>
                Generate & Download
              </Button>
            </Stack>
          </Box>
        );

      default:
        return 'Unknown step';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Big-4 Financial Report Generator
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Create professional financial reports following Deloitte, PwC, EY, and KPMG standards
          </Typography>
        </Box>

        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <Box sx={{ minHeight: 400 }}>{renderStepContent(activeStep)}</Box>

        <Box sx={{ display: 'flex', flexDirection: 'row', pt: 3 }}>
          <Button color="inherit" disabled={activeStep === 0} onClick={handleBack} sx={{ mr: 1 }}>
            Back
          </Button>
          <Box sx={{ flex: '1 1 auto' }} />
          {activeStep < steps.length - 1 && (
            <Button variant="contained" onClick={handleNext}>
              Next
            </Button>
          )}
        </Box>
      </Paper>
    </Container>
  );
};
