import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Tabs,
  Tab,
  Stack,
  Chip,
  Paper,
  alpha,
  useTheme,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Divider,
  Switch,
  FormControlLabel,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  AccountBalance as TaxIcon,
  TrendingUp as TrendingUpIcon,
  AttachMoney as MoneyIcon,
  Business as BusinessIcon,
  Schedule as ScheduleIcon,
  Assessment as AssessmentIcon,
  Description as DescriptionIcon,
  ArrowBack as ArrowBackIcon,
  Percent as PercentIcon,
  Save as SaveIcon,
  PlayArrow as PlayArrowIcon,
  CompareArrows as CompareIcon,
  LocationCity as PropertyIcon,
  Gavel as LegalIcon,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  LineChart,
  Line,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import axios from 'axios';

interface TaxInputs {
  // Property Profile
  projectName: string;
  location: string;
  analyst: string;
  propertyValue: number;
  purchasePrice: number;
  purchaseDate: string;
  propertyType: string;
  landValuePct: number;

  // 1031 Exchange
  enable1031: boolean;
  saleDate: string;
  replacementPropertyValue: number;
  identificationDays: number;
  exchangeCompletionDays: number;

  // Cost Segregation
  enableCostSeg: boolean;
  costSegStudyCost: number;
  personalPropertyPct: number;
  landImprovementsPct: number;
  buildingPct: number;

  // Opportunity Zone
  enableOpportunityZone: boolean;
  ozInvestmentAmount: number;
  ozInvestmentDate: string;
  ozHoldPeriodYears: number;

  // Entity Structure
  currentEntityType: string;
  compareEntities: boolean;
  annualIncome: number;
  stateTaxRate: number;

  // Capital Gains
  holdingPeriodMonths: number;
  federalIncomeBracket: number;
  stateCapitalGainsRate: number;
  netInvestmentIncomeTax: number;

  // Depreciation
  accumulatedDepreciation: number;
  bonusDepreciationTaken: number;
  section179Taken: number;

  // Assumptions
  annualAppreciation: number;
  inflationRate: number;
  discountRate: number;
}

interface TableData {
  title: string;
  rows: Array<{ [key: string]: string | number }>;
  columns: string[];
}

interface ChartData {
  title: string;
  type: string;
  data: Array<{ [key: string]: any }>;
  xKey?: string;
  yKeys?: string[];
  dataKey?: string;
  nameKey?: string;
  colors?: string[];
}

export const TaxStrategyCalculator: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [currentTab, setCurrentTab] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [tables, setTables] = useState<TableData[]>([]);
  const [charts, setCharts] = useState<ChartData[]>([]);

  const [inputs, setInputs] = useState<TaxInputs>({
    // Property Profile
    projectName: 'Tax Strategy Analysis',
    location: 'California',
    analyst: 'Tax Advisor',
    propertyValue: 1000000,
    purchasePrice: 900000,
    purchaseDate: '2020-01-15',
    propertyType: 'Multifamily',
    landValuePct: 20,

    // 1031 Exchange
    enable1031: true,
    saleDate: '2025-12-01',
    replacementPropertyValue: 1200000,
    identificationDays: 45,
    exchangeCompletionDays: 180,

    // Cost Segregation
    enableCostSeg: true,
    costSegStudyCost: 8000,
    personalPropertyPct: 15,
    landImprovementsPct: 10,
    buildingPct: 55,

    // Opportunity Zone
    enableOpportunityZone: false,
    ozInvestmentAmount: 500000,
    ozInvestmentDate: '2024-01-01',
    ozHoldPeriodYears: 10,

    // Entity Structure
    currentEntityType: 'LLC',
    compareEntities: true,
    annualIncome: 200000,
    stateTaxRate: 9.3,

    // Capital Gains
    holdingPeriodMonths: 24,
    federalIncomeBracket: 24,
    stateCapitalGainsRate: 13.3,
    netInvestmentIncomeTax: 3.8,

    // Depreciation
    accumulatedDepreciation: 100000,
    bonusDepreciationTaken: 50000,
    section179Taken: 0,

    // Assumptions
    annualAppreciation: 3,
    inflationRate: 2.5,
    discountRate: 8,
  });

  const handleInputChange = (field: keyof TaxInputs, value: any) => {
    setInputs((prev) => ({ ...prev, [field]: value }));
  };

  const handleCalculate = async () => {
    setLoading(true);
    setShowResults(false);
    setSaveMessage('');

    try {
      const response = await axios.post('/api/v1/real-estate/tools/run', {
        model: 'tax_strategy',
        values: {
          project_name: inputs.projectName,
          location: inputs.location,
          analyst: inputs.analyst,
          property_value: inputs.propertyValue,
          purchase_price: inputs.purchasePrice,
          purchase_date: inputs.purchaseDate,
          property_type: inputs.propertyType,
          land_value_pct: inputs.landValuePct / 100,
          enable_1031: inputs.enable1031,
          sale_date: inputs.saleDate,
          replacement_property_value: inputs.replacementPropertyValue,
          identification_days: inputs.identificationDays,
          exchange_completion_days: inputs.exchangeCompletionDays,
          enable_cost_seg: inputs.enableCostSeg,
          cost_seg_study_cost: inputs.costSegStudyCost,
          personal_property_pct: inputs.personalPropertyPct / 100,
          land_improvements_pct: inputs.landImprovementsPct / 100,
          building_pct: inputs.buildingPct / 100,
          enable_opportunity_zone: inputs.enableOpportunityZone,
          oz_investment_amount: inputs.ozInvestmentAmount,
          oz_investment_date: inputs.ozInvestmentDate,
          oz_hold_period_years: inputs.ozHoldPeriodYears,
          current_entity_type: inputs.currentEntityType,
          compare_entities: inputs.compareEntities,
          annual_income: inputs.annualIncome,
          state_tax_rate: inputs.stateTaxRate / 100,
          holding_period_months: inputs.holdingPeriodMonths,
          federal_income_bracket: inputs.federalIncomeBracket / 100,
          state_capital_gains_rate: inputs.stateCapitalGainsRate / 100,
          net_investment_income_tax: inputs.netInvestmentIncomeTax / 100,
          accumulated_depreciation: inputs.accumulatedDepreciation,
          bonus_depreciation_taken: inputs.bonusDepreciationTaken,
          section_179_taken: inputs.section179Taken,
          annual_appreciation: inputs.annualAppreciation / 100,
          inflation_rate: inputs.inflationRate / 100,
          discount_rate: inputs.discountRate / 100,
        },
        save_to_db: false,
      });

      setTables(response.data.tables || []);
      setCharts(response.data.charts || []);
      setShowResults(true);
      setCurrentTab(1); // Switch to Results tab
    } catch (error) {
      console.error('Error calculating tax strategy:', error);
      setSaveMessage('Error calculating tax strategy. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setSaveMessage('');

    try {
      await axios.post('/api/v1/real-estate/tools/run', {
        model: 'tax_strategy',
        values: {
          project_name: inputs.projectName,
          location: inputs.location,
          analyst: inputs.analyst,
          property_value: inputs.propertyValue,
          purchase_price: inputs.purchasePrice,
          purchase_date: inputs.purchaseDate,
          property_type: inputs.propertyType,
          land_value_pct: inputs.landValuePct / 100,
          enable_1031: inputs.enable1031,
          sale_date: inputs.saleDate,
          replacement_property_value: inputs.replacementPropertyValue,
          identification_days: inputs.identificationDays,
          exchange_completion_days: inputs.exchangeCompletionDays,
          enable_cost_seg: inputs.enableCostSeg,
          cost_seg_study_cost: inputs.costSegStudyCost,
          personal_property_pct: inputs.personalPropertyPct / 100,
          land_improvements_pct: inputs.landImprovementsPct / 100,
          building_pct: inputs.buildingPct / 100,
          enable_opportunity_zone: inputs.enableOpportunityZone,
          oz_investment_amount: inputs.ozInvestmentAmount,
          oz_investment_date: inputs.ozInvestmentDate,
          oz_hold_period_years: inputs.ozHoldPeriodYears,
          current_entity_type: inputs.currentEntityType,
          compare_entities: inputs.compareEntities,
          annual_income: inputs.annualIncome,
          state_tax_rate: inputs.stateTaxRate / 100,
          holding_period_months: inputs.holdingPeriodMonths,
          federal_income_bracket: inputs.federalIncomeBracket / 100,
          state_capital_gains_rate: inputs.stateCapitalGainsRate / 100,
          net_investment_income_tax: inputs.netInvestmentIncomeTax / 100,
          accumulated_depreciation: inputs.accumulatedDepreciation,
          bonus_depreciation_taken: inputs.bonusDepreciationTaken,
          section_179_taken: inputs.section179Taken,
          annual_appreciation: inputs.annualAppreciation / 100,
          inflation_rate: inputs.inflationRate / 100,
          discount_rate: inputs.discountRate / 100,
        },
        save_to_db: true,
      });

      setSaveMessage('Tax strategy analysis saved successfully!');
      setTimeout(() => setSaveMessage(''), 3000);
    } catch (error) {
      console.error('Error saving:', error);
      setSaveMessage('Error saving report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderInputsTab = () => (
    <Box>
      <Grid container spacing={3}>
        {/* Property Profile Section */}
        <Grid item xs={12}>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <PropertyIcon /> Property Profile
          </Typography>
          <Divider sx={{ mb: 2 }} />
        </Grid>

        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Project Name"
            value={inputs.projectName}
            onChange={(e) => handleInputChange('projectName', e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Location (State)"
            value={inputs.location}
            onChange={(e) => handleInputChange('location', e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Analyst/Advisor"
            value={inputs.analyst}
            onChange={(e) => handleInputChange('analyst', e.target.value)}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="Current Property Value"
            type="number"
            value={inputs.propertyValue}
            onChange={(e) => handleInputChange('propertyValue', Number(e.target.value))}
            InputProps={{ startAdornment: '$' }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="Original Purchase Price"
            type="number"
            value={inputs.purchasePrice}
            onChange={(e) => handleInputChange('purchasePrice', Number(e.target.value))}
            InputProps={{ startAdornment: '$' }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="Purchase Date"
            type="date"
            value={inputs.purchaseDate}
            onChange={(e) => handleInputChange('purchaseDate', e.target.value)}
            InputLabelProps={{ shrink: true }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <FormControl fullWidth>
            <InputLabel>Property Type</InputLabel>
            <Select
              value={inputs.propertyType}
              label="Property Type"
              onChange={(e) => handleInputChange('propertyType', e.target.value)}
            >
              <MenuItem value="Single Family">Single Family</MenuItem>
              <MenuItem value="Multifamily">Multifamily</MenuItem>
              <MenuItem value="Commercial">Commercial</MenuItem>
              <MenuItem value="Mixed-Use">Mixed-Use</MenuItem>
              <MenuItem value="Industrial">Industrial</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="Land Value %"
            type="number"
            value={inputs.landValuePct}
            onChange={(e) => handleInputChange('landValuePct', Number(e.target.value))}
            InputProps={{ endAdornment: '%' }}
          />
        </Grid>

        {/* 1031 Exchange Section */}
        <Grid item xs={12} sx={{ mt: 3 }}>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <CompareIcon /> 1031 Exchange Analysis
          </Typography>
          <Divider sx={{ mb: 2 }} />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={inputs.enable1031}
                onChange={(e) => handleInputChange('enable1031', e.target.checked)}
              />
            }
            label="Enable 1031 Exchange Analysis"
          />
        </Grid>

        {inputs.enable1031 && (
          <>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Planned Sale Date"
                type="date"
                value={inputs.saleDate}
                onChange={(e) => handleInputChange('saleDate', e.target.value)}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Replacement Property Value"
                type="number"
                value={inputs.replacementPropertyValue}
                onChange={(e) => handleInputChange('replacementPropertyValue', Number(e.target.value))}
                InputProps={{ startAdornment: '$' }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Identification Period (Days)"
                type="number"
                value={inputs.identificationDays}
                onChange={(e) => handleInputChange('identificationDays', Number(e.target.value))}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Exchange Completion (Days)"
                type="number"
                value={inputs.exchangeCompletionDays}
                onChange={(e) => handleInputChange('exchangeCompletionDays', Number(e.target.value))}
              />
            </Grid>
          </>
        )}

        {/* Cost Segregation Section */}
        <Grid item xs={12} sx={{ mt: 3 }}>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <AssessmentIcon /> Cost Segregation Analysis
          </Typography>
          <Divider sx={{ mb: 2 }} />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={inputs.enableCostSeg}
                onChange={(e) => handleInputChange('enableCostSeg', e.target.checked)}
              />
            }
            label="Enable Cost Segregation Analysis"
          />
        </Grid>

        {inputs.enableCostSeg && (
          <>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Cost Seg Study Cost"
                type="number"
                value={inputs.costSegStudyCost}
                onChange={(e) => handleInputChange('costSegStudyCost', Number(e.target.value))}
                InputProps={{ startAdornment: '$' }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Personal Property %"
                type="number"
                value={inputs.personalPropertyPct}
                onChange={(e) => handleInputChange('personalPropertyPct', Number(e.target.value))}
                InputProps={{ endAdornment: '%' }}
                helperText="5-year property"
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Land Improvements %"
                type="number"
                value={inputs.landImprovementsPct}
                onChange={(e) => handleInputChange('landImprovementsPct', Number(e.target.value))}
                InputProps={{ endAdornment: '%' }}
                helperText="15-year property"
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Building %"
                type="number"
                value={inputs.buildingPct}
                onChange={(e) => handleInputChange('buildingPct', Number(e.target.value))}
                InputProps={{ endAdornment: '%' }}
                helperText="27.5/39-year property"
              />
            </Grid>
          </>
        )}

        {/* Opportunity Zone Section */}
        <Grid item xs={12} sx={{ mt: 3 }}>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <TrendingUpIcon /> Opportunity Zone Benefits
          </Typography>
          <Divider sx={{ mb: 2 }} />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={inputs.enableOpportunityZone}
                onChange={(e) => handleInputChange('enableOpportunityZone', e.target.checked)}
              />
            }
            label="Enable Opportunity Zone Analysis"
          />
        </Grid>

        {inputs.enableOpportunityZone && (
          <>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="OZ Investment Amount"
                type="number"
                value={inputs.ozInvestmentAmount}
                onChange={(e) => handleInputChange('ozInvestmentAmount', Number(e.target.value))}
                InputProps={{ startAdornment: '$' }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="OZ Investment Date"
                type="date"
                value={inputs.ozInvestmentDate}
                onChange={(e) => handleInputChange('ozInvestmentDate', e.target.value)}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="OZ Hold Period (Years)"
                type="number"
                value={inputs.ozHoldPeriodYears}
                onChange={(e) => handleInputChange('ozHoldPeriodYears', Number(e.target.value))}
                helperText="10+ years for full benefits"
              />
            </Grid>
          </>
        )}

        {/* Entity Structure Section */}
        <Grid item xs={12} sx={{ mt: 3 }}>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <BusinessIcon /> Entity Structure Comparison
          </Typography>
          <Divider sx={{ mb: 2 }} />
        </Grid>

        <Grid item xs={12} md={4}>
          <FormControl fullWidth>
            <InputLabel>Current Entity Type</InputLabel>
            <Select
              value={inputs.currentEntityType}
              label="Current Entity Type"
              onChange={(e) => handleInputChange('currentEntityType', e.target.value)}
            >
              <MenuItem value="LLC">LLC</MenuItem>
              <MenuItem value="S-Corp">S-Corp</MenuItem>
              <MenuItem value="C-Corp">C-Corp</MenuItem>
              <MenuItem value="Partnership">Partnership</MenuItem>
              <MenuItem value="Sole Proprietorship">Sole Proprietorship</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Annual Property Income"
            type="number"
            value={inputs.annualIncome}
            onChange={(e) => handleInputChange('annualIncome', Number(e.target.value))}
            InputProps={{ startAdornment: '$' }}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="State Tax Rate"
            type="number"
            value={inputs.stateTaxRate}
            onChange={(e) => handleInputChange('stateTaxRate', Number(e.target.value))}
            InputProps={{ endAdornment: '%' }}
          />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={inputs.compareEntities}
                onChange={(e) => handleInputChange('compareEntities', e.target.checked)}
              />
            }
            label="Compare All Entity Structures"
          />
        </Grid>

        {/* Capital Gains Section */}
        <Grid item xs={12} sx={{ mt: 3 }}>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <MoneyIcon /> Capital Gains Calculator
          </Typography>
          <Divider sx={{ mb: 2 }} />
        </Grid>

        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="Holding Period (Months)"
            type="number"
            value={inputs.holdingPeriodMonths}
            onChange={(e) => handleInputChange('holdingPeriodMonths', Number(e.target.value))}
            helperText="12+ months = long-term"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="Federal Income Bracket"
            type="number"
            value={inputs.federalIncomeBracket}
            onChange={(e) => handleInputChange('federalIncomeBracket', Number(e.target.value))}
            InputProps={{ endAdornment: '%' }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="State Capital Gains Rate"
            type="number"
            value={inputs.stateCapitalGainsRate}
            onChange={(e) => handleInputChange('stateCapitalGainsRate', Number(e.target.value))}
            InputProps={{ endAdornment: '%' }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="Net Investment Income Tax"
            type="number"
            value={inputs.netInvestmentIncomeTax}
            onChange={(e) => handleInputChange('netInvestmentIncomeTax', Number(e.target.value))}
            InputProps={{ endAdornment: '%' }}
            helperText="3.8% for high earners"
          />
        </Grid>

        {/* Depreciation Section */}
        <Grid item xs={12} sx={{ mt: 3 }}>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <PercentIcon /> Depreciation & Recapture
          </Typography>
          <Divider sx={{ mb: 2 }} />
        </Grid>

        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Accumulated Depreciation"
            type="number"
            value={inputs.accumulatedDepreciation}
            onChange={(e) => handleInputChange('accumulatedDepreciation', Number(e.target.value))}
            InputProps={{ startAdornment: '$' }}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Bonus Depreciation Taken"
            type="number"
            value={inputs.bonusDepreciationTaken}
            onChange={(e) => handleInputChange('bonusDepreciationTaken', Number(e.target.value))}
            InputProps={{ startAdornment: '$' }}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Section 179 Deduction"
            type="number"
            value={inputs.section179Taken}
            onChange={(e) => handleInputChange('section179Taken', Number(e.target.value))}
            InputProps={{ startAdornment: '$' }}
          />
        </Grid>

        {/* Financial Assumptions Section */}
        <Grid item xs={12} sx={{ mt: 3 }}>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <ScheduleIcon /> Financial Assumptions
          </Typography>
          <Divider sx={{ mb: 2 }} />
        </Grid>

        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Annual Appreciation Rate"
            type="number"
            value={inputs.annualAppreciation}
            onChange={(e) => handleInputChange('annualAppreciation', Number(e.target.value))}
            InputProps={{ endAdornment: '%' }}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Inflation Rate"
            type="number"
            value={inputs.inflationRate}
            onChange={(e) => handleInputChange('inflationRate', Number(e.target.value))}
            InputProps={{ endAdornment: '%' }}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Discount Rate"
            type="number"
            value={inputs.discountRate}
            onChange={(e) => handleInputChange('discountRate', Number(e.target.value))}
            InputProps={{ endAdornment: '%' }}
          />
        </Grid>

        {/* Action Buttons */}
        <Grid item xs={12} sx={{ mt: 3 }}>
          <Stack direction="row" spacing={2}>
            <Button
              variant="contained"
              size="large"
              startIcon={<PlayArrowIcon />}
              onClick={handleCalculate}
              disabled={loading}
              sx={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
                },
              }}
            >
              {loading ? 'Calculating...' : 'Calculate Tax Strategy'}
            </Button>
            {showResults && (
              <Button
                variant="outlined"
                size="large"
                startIcon={<SaveIcon />}
                onClick={handleSave}
                disabled={loading}
              >
                Save Report
              </Button>
            )}
          </Stack>
        </Grid>

        {saveMessage && (
          <Grid item xs={12}>
            <Alert severity={saveMessage.includes('Error') ? 'error' : 'success'}>
              {saveMessage}
            </Alert>
          </Grid>
        )}
      </Grid>
    </Box>
  );

  const renderResultsTab = () => {
    if (!showResults) {
      return (
        <Box textAlign="center" py={8}>
          <Typography variant="h6" color="text.secondary">
            Run the calculator to see tax strategy results
          </Typography>
        </Box>
      );
    }

    return (
      <Box>
        <Grid container spacing={3}>
          {/* Tables */}
          {tables.map((table, idx) => (
            <Grid item xs={12} key={idx}>
              <Card
                sx={{
                  background: isDark
                    ? alpha(muiTheme.palette.background.paper, 0.8)
                    : muiTheme.palette.background.paper,
                  backdropFilter: 'blur(10px)',
                }}
              >
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <TaxIcon color="primary" />
                    {table.title}
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          {table.columns.map((col) => (
                            <TableCell key={col} sx={{ fontWeight: 'bold' }}>
                              {col}
                            </TableCell>
                          ))}
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {table.rows.map((row, rowIdx) => (
                          <TableRow key={rowIdx}>
                            {table.columns.map((col) => (
                              <TableCell key={col}>{row[col]}</TableCell>
                            ))}
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
          ))}

          {/* Charts */}
          {charts.map((chart, idx) => (
            <Grid item xs={12} md={6} key={idx}>
              <Card
                sx={{
                  background: isDark
                    ? alpha(muiTheme.palette.background.paper, 0.8)
                    : muiTheme.palette.background.paper,
                  backdropFilter: 'blur(10px)',
                }}
              >
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {chart.title}
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    {chart.type === 'bar' ? (
                      <BarChart data={chart.data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey={chart.xKey} />
                        <YAxis />
                        <Tooltip formatter={(value: any) => `$${Number(value).toLocaleString()}`} />
                        <Legend />
                        {chart.yKeys?.map((key, i) => (
                          <Bar
                            key={key}
                            dataKey={key}
                            fill={chart.colors?.[i] || muiTheme.palette.primary.main}
                          />
                        ))}
                      </BarChart>
                    ) : chart.type === 'pie' ? (
                      <PieChart>
                        <Pie
                          data={chart.data}
                          dataKey={chart.dataKey}
                          nameKey={chart.nameKey}
                          cx="50%"
                          cy="50%"
                          outerRadius={100}
                          label
                        >
                          {chart.data.map((entry, index) => (
                            <Cell
                              key={`cell-${index}`}
                              fill={chart.colors?.[index] || muiTheme.palette.primary.main}
                            />
                          ))}
                        </Pie>
                        <Tooltip formatter={(value: any) => `$${Number(value).toLocaleString()}`} />
                        <Legend />
                      </PieChart>
                    ) : null}
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  };

  const renderDocumentationTab = () => (
    <Box>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Tax Strategy Integration Documentation
          </Typography>
          <Divider sx={{ my: 2 }} />

          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Overview
          </Typography>
          <Typography paragraph>
            The Tax Strategy Integration calculator provides comprehensive tax planning and optimization for real estate
            investments. It analyzes multiple strategies to minimize tax liability and maximize after-tax returns.
          </Typography>

          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Key Features
          </Typography>
          <Stack spacing={2}>
            <Box>
              <Typography variant="subtitle1" fontWeight="bold">
                1. 1031 Exchange Modeling
              </Typography>
              <Typography>
                Track timeline requirements (45-day identification, 180-day completion), replacement property requirements,
                and tax deferral benefits. Calculates boot and taxable portions.
              </Typography>
            </Box>

            <Box>
              <Typography variant="subtitle1" fontWeight="bold">
                2. Cost Segregation Analysis
              </Typography>
              <Typography>
                Analyze accelerated depreciation benefits by reclassifying assets into shorter recovery periods (5-year,
                15-year vs 27.5/39-year). Calculates ROI of cost segregation study.
              </Typography>
            </Box>

            <Box>
              <Typography variant="subtitle1" fontWeight="bold">
                3. Opportunity Zone Benefits
              </Typography>
              <Typography>
                Model tax deferral and elimination through Qualified Opportunity Zones. Includes 10% and 15% basis step-ups
                and permanent exclusion of appreciation after 10 years.
              </Typography>
            </Box>

            <Box>
              <Typography variant="subtitle1" fontWeight="bold">
                4. Entity Structure Comparison
              </Typography>
              <Typography>
                Compare tax implications across LLC, S-Corp, C-Corp, Partnership, and Sole Proprietorship. Analyzes
                self-employment taxes, pass-through treatment, and double taxation.
              </Typography>
            </Box>

            <Box>
              <Typography variant="subtitle1" fontWeight="bold">
                5. Capital Gains Calculator
              </Typography>
              <Typography>
                Calculate federal and state capital gains taxes, including long-term vs short-term treatment, Net Investment
                Income Tax (NIIT), and depreciation recapture at 25%.
              </Typography>
            </Box>

            <Box>
              <Typography variant="subtitle1" fontWeight="bold">
                6. Depreciation Recapture
              </Typography>
              <Typography>
                Automatically calculates depreciation recapture tax on property exit, including regular depreciation, bonus
                depreciation, and Section 179 deductions.
              </Typography>
            </Box>
          </Stack>

          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Best Practices
          </Typography>
          <Typography component="div">
            <ul>
              <li>Consult with a qualified tax professional before implementing any strategy</li>
              <li>1031 exchanges require strict timeline adherence - plan ahead</li>
              <li>Cost segregation is most beneficial for properties over $500K</li>
              <li>Opportunity Zone investments must be held 10+ years for full benefits</li>
              <li>Entity structure should align with investment strategy and exit timeline</li>
              <li>Document all tax positions and maintain thorough records</li>
            </ul>
          </Typography>

          <Alert severity="warning" sx={{ mt: 3 }}>
            <Typography variant="body2">
              <strong>Disclaimer:</strong> This calculator provides estimates for planning purposes only. Tax laws are complex
              and subject to change. Always consult with qualified tax and legal professionals before making tax-related
              decisions.
            </Typography>
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );

  return (
    <Box sx={{ minHeight: '100vh', pb: 4 }}>
      {/* Header */}
      <Paper
        elevation={0}
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: 4,
          px: 3,
          mb: 4,
          borderRadius: 0,
        }}
      >
        <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/real-estate-tools')}
            sx={{
              color: 'white',
              mb: 2,
              '&:hover': { bgcolor: alpha('#fff', 0.1) },
            }}
          >
            Back to Models
          </Button>
          <Typography variant="h3" fontWeight="700" gutterBottom>
            Tax Strategy Integration
          </Typography>
          <Typography variant="h6" sx={{ opacity: 0.95 }}>
            Comprehensive tax planning and optimization toolkit for real estate investments
          </Typography>
          <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
            <Chip
              icon={<CompareIcon />}
              label="1031 Exchange"
              sx={{ bgcolor: alpha('#fff', 0.2), color: 'white' }}
            />
            <Chip
              icon={<AssessmentIcon />}
              label="Cost Segregation"
              sx={{ bgcolor: alpha('#fff', 0.2), color: 'white' }}
            />
            <Chip
              icon={<TrendingUpIcon />}
              label="Opportunity Zones"
              sx={{ bgcolor: alpha('#fff', 0.2), color: 'white' }}
            />
            <Chip
              icon={<BusinessIcon />}
              label="Entity Comparison"
              sx={{ bgcolor: alpha('#fff', 0.2), color: 'white' }}
            />
          </Stack>
        </Box>
      </Paper>

      {/* Main Content */}
      <Box sx={{ maxWidth: 1400, mx: 'auto', px: 3 }}>
        <Paper sx={{ borderRadius: 2, overflow: 'hidden' }}>
          <Tabs
            value={currentTab}
            onChange={(_, newValue) => setCurrentTab(newValue)}
            sx={{
              borderBottom: 1,
              borderColor: 'divider',
              bgcolor: isDark ? alpha(muiTheme.palette.background.paper, 0.6) : '#f8f9fa',
            }}
          >
            <Tab label="Inputs" icon={<TaxIcon />} iconPosition="start" />
            <Tab label="Results" icon={<AssessmentIcon />} iconPosition="start" />
            <Tab label="Documentation" icon={<DescriptionIcon />} iconPosition="start" />
          </Tabs>

          <Box sx={{ p: 3 }}>
            {currentTab === 0 && renderInputsTab()}
            {currentTab === 1 && renderResultsTab()}
            {currentTab === 2 && renderDocumentationTab()}
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};
