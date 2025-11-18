import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Stack,
  Chip,
  Button,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
  List,
  ListItem,
  ListItemText,
  Divider,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Info as InfoIcon,
  Calculate as CalculateIcon,
  LocalAtm as MoneyIcon,
} from '@mui/icons-material';

interface TaxStrategy {
  id: string;
  name: string;
  category: string;
  complexity: string;
  potentialSavings: string;
  description: string;
  requirements: string[];
  bestFor: string[];
  risks: string[];
  tips: string[];
  irsCode?: string;
}

export const TaxStrategyAdvisor: React.FC = () => {
  const [entityType, setEntityType] = useState('property_management');
  const [income, setIncome] = useState('250000');
  const [expandedStrategy, setExpandedStrategy] = useState<string | false>(false);

  const strategies: TaxStrategy[] = [
    {
      id: '1',
      name: 'Cost Segregation with Bonus Depreciation',
      category: 'Real Estate',
      complexity: 'High',
      potentialSavings: '$50,000 - $200,000+ first year',
      description:
        'Accelerate depreciation by reclassifying property components from 27.5/39-year to 5, 7, and 15-year recovery periods. Combine with bonus depreciation for massive first-year deductions.',
      requirements: [
        'Own commercial or rental property worth $500K+',
        'Hire qualified cost segregation specialist',
        'File Form 3115 if applied retroactively',
        'Property must be in service',
      ],
      bestFor: [
        'Commercial properties over $1M',
        'High-income taxpayers in top brackets',
        'Properties with significant improvements',
        'Real estate professionals (REPS)',
      ],
      risks: [
        'IRS scrutiny if study not defensible',
        'Depreciation recapture upon sale (25% rate)',
        'May not benefit those with passive loss limitations',
        'Study costs $5K-$15K',
      ],
      tips: [
        'Most valuable in year of acquisition or major renovation',
        'Can be applied retroactively with catch-up depreciation',
        'Consider state tax conformity before implementing',
        'Typical ROI: 5-20x the cost of the study',
      ],
      irsCode: 'IRC §168(k), Rev. Proc. 2011-14',
    },
    {
      id: '2',
      name: 'Real Estate Professional Status (REPS)',
      category: 'Real Estate',
      complexity: 'Medium',
      potentialSavings: 'Unlimited passive loss deductions',
      description:
        'Qualify as real estate professional to deduct unlimited rental losses against W-2 income. Game-changer for high-income couples.',
      requirements: [
        '750+ hours per year in real property trades/businesses',
        'More than 50% of working time in real estate',
        'Material participation in each rental (100+ hours/property or other tests)',
        'Detailed time tracking required',
      ],
      bestFor: [
        'W-2 earner married to full-time real estate investor',
        'Full-time real estate investors',
        'Couples where one spouse can dedicate time to real estate',
        'Those with significant rental losses from cost segregation',
      ],
      risks: [
        'IRS frequently audits REPS claims',
        'Inadequate documentation leads to disallowance',
        'Spouse qualification affects both spouses',
        'Must meet tests every year',
      ],
      tips: [
        'Use time-tracking software for bulletproof records',
        'Include education, property search, and management time',
        'If both spouses work, have lower earner qualify as REPS',
        'Combine with cost segregation for $100K+ deductions against W-2',
      ],
      irsCode: 'IRC §469(c)(7)',
    },
    {
      id: '3',
      name: 'Short-Term Rental Loophole',
      category: 'Real Estate',
      complexity: 'Medium',
      potentialSavings: 'Deduct losses against W-2 without REPS',
      description:
        'Rent property on Airbnb/VRBO with average stays under 7 days to bypass passive loss rules. Losses become non-passive and offset W-2 income.',
      requirements: [
        'Average rental period ≤ 7 days',
        'Provide substantial services (cleaning, concierge)',
        'Material participation (500+ hours/year)',
        'Track average length of stay carefully',
      ],
      bestFor: [
        'W-2 employees who cannot qualify for REPS',
        'Vacation rental owners',
        'High-income professionals ($200K+ W-2)',
        'Properties suitable for short-term rentals',
      ],
      risks: [
        'Higher management burden than long-term rentals',
        'Local regulations may restrict STRs',
        'Material participation requirement still applies',
        'Average stay calculation must be precise',
      ],
      tips: [
        'Combine with cost segregation in year 1 for massive deductions',
        'Can have multiple STRs and aggregate hours',
        'Document substantial services provided',
        'Works for doctors, lawyers, executives with high W-2 income',
      ],
      irsCode: 'IRC §469(c)(7), Temp. Reg. 1.469-1T(e)(3)(ii)',
    },
    {
      id: '4',
      name: '1031 Like-Kind Exchange',
      category: 'Real Estate',
      complexity: 'Medium',
      potentialSavings: 'Defer 100% of capital gains',
      description:
        'Sell investment property and reinvest proceeds in like-kind property to defer all capital gains taxes indefinitely.',
      requirements: [
        'Both properties must be held for investment/business use',
        'Identify replacement within 45 days',
        'Close on replacement within 180 days',
        'Must use qualified intermediary',
        'Reinvest all proceeds + match or exceed debt',
      ],
      bestFor: [
        'Upgrading investment properties',
        'Diversifying into different markets',
        'Consolidating multiple properties',
        'Investors wanting to defer taxes',
      ],
      risks: [
        'Strict timing requirements',
        'Boot (cash or debt relief) is taxable',
        'Depreciation recapture still applies eventually',
        'Cannot touch proceeds during exchange',
      ],
      tips: [
        'Line up replacement property before selling',
        'Consider reverse exchange if needed',
        'Can combine with Opportunity Zone strategy',
        'Estate planning: Hold until death for step-up in basis',
      ],
      irsCode: 'IRC §1031',
    },
    {
      id: '5',
      name: 'S-Corp Election for Self-Employment Tax Savings',
      category: 'Business',
      complexity: 'Medium',
      potentialSavings: '15.3% on distributions above salary',
      description:
        'Elect S-Corp status to split income into salary (subject to SE tax) and distributions (no SE tax). Save thousands on self-employment taxes.',
      requirements: [
        'Form LLC or C-Corp and elect S-Corp (Form 2553)',
        'Pay yourself reasonable salary',
        'Run payroll (941, W-2, W-3)',
        'File Form 1120-S annually',
      ],
      bestFor: [
        'Self-employed making $60K+ net income',
        'Single-member LLCs',
        'Service-based businesses',
        'Consultants and contractors',
      ],
      risks: [
        'IRS watches for unreasonably low salaries',
        'Payroll tax compliance burden',
        'Additional costs ($500-2000/year for payroll)',
        'State-level S-Corp taxes in some states',
      ],
      tips: [
        'Rule of thumb: 40% salary, 60% distribution',
        'Benchmark salary against industry standards',
        'Makes sense at $60K+ net income',
        'Use payroll service to handle compliance',
      ],
      irsCode: 'IRC §1361-1379',
    },
    {
      id: '6',
      name: 'Augusta Rule - Tax-Free Home Rental',
      category: 'Business',
      complexity: 'Low',
      potentialSavings: '$2,000 - $10,000+ tax-free income',
      description:
        'Rent your home to your business for up to 14 days per year. Business deducts rent, you receive it tax-free.',
      requirements: [
        'Business rents your personal home',
        'Charge fair market rate',
        'Document with rental agreement',
        'Limited to 14 days per year',
        'Must be actual business use',
      ],
      bestFor: [
        'Business owners with home offices',
        'S-Corp owners',
        'Professional corporations',
        'Board meetings and strategy sessions',
      ],
      risks: [
        'IRS audits this frequently',
        'Exceeding 14 days makes all rental income taxable',
        'Must have legitimate business purpose',
        'Rates must be comparable to market',
      ],
      tips: [
        'Document with board minutes authorizing rental',
        'Keep attendee lists and agendas',
        'Compare to local conference center rates',
        'Use for genuine business purposes',
      ],
      irsCode: 'IRC §280A(g)',
    },
    {
      id: '7',
      name: 'Qualified Business Income (QBI) Deduction',
      category: 'Business',
      complexity: 'High',
      potentialSavings: 'Up to 20% of business income',
      description:
        'Deduct 20% of qualified business income from pass-through entities. Strategic planning needed to maximize.',
      requirements: [
        'Pass-through income (LLC, S-Corp, partnership)',
        'Taxable income under $383,800 (married) for full benefit',
        'If over threshold, need W-2 wages or qualified property',
        'Not specified service trade/business (SSTB) if over limit',
      ],
      bestFor: [
        'Pass-through business owners under income limits',
        'Real estate investors (not SSTB)',
        'Manufacturing and retail businesses',
        'Those who can optimize W-2 wages',
      ],
      risks: [
        'Complex phase-out calculations',
        'SSTB limitations for high earners',
        'May require increasing W-2 wages',
        'Scheduled to sunset in 2025 (may be extended)',
      ],
      tips: [
        'Keep taxable income below thresholds if possible',
        'Pay family members wages to increase W-2 limit',
        'Buy equipment before year-end for property basis',
        'Separate SSTB and non-SSTB income if possible',
      ],
      irsCode: 'IRC §199A',
    },
  ];

  const complexityColors: Record<string, 'success' | 'warning' | 'error'> = {
    Low: 'success',
    Medium: 'warning',
    High: 'error',
  };

  const filteredStrategies = strategies.filter((s) => {
    if (entityType === 'property_management') return s.category === 'Real Estate';
    if (entityType === 'small_business') return s.category === 'Business';
    return true;
  });

  const handleAccordionChange = (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
    setExpandedStrategy(isExpanded ? panel : false);
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Tax Strategy Advisor
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Expert tax strategies and loopholes used by Big-4 advisors. Maximize tax savings legally and ethically.
        </Typography>
      </Box>

      {/* Input Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Your Profile
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Entity Type</InputLabel>
              <Select value={entityType} label="Entity Type" onChange={(e) => setEntityType(e.target.value)}>
                <MenuItem value="property_management">Property Management / Real Estate</MenuItem>
                <MenuItem value="small_business">Small Business</MenuItem>
                <MenuItem value="high_net_worth">High Net Worth Individual</MenuItem>
                <MenuItem value="all">Show All Strategies</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Annual Income"
              type="number"
              value={income}
              onChange={(e) => setIncome(e.target.value)}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <Button variant="contained" fullWidth size="large" startIcon={<CalculateIcon />} sx={{ height: '56px' }}>
              Calculate Optimal Strategy
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Strategies List */}
      <Box>
        <Typography variant="h5" fontWeight="bold" gutterBottom>
          Recommended Tax Strategies ({filteredStrategies.length})
        </Typography>

        {filteredStrategies.map((strategy) => (
          <Accordion
            key={strategy.id}
            expanded={expandedStrategy === strategy.id}
            onChange={handleAccordionChange(strategy.id)}
            sx={{ mb: 2 }}
          >
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', gap: 2 }}>
                <TrendingUpIcon color="primary" />
                <Box sx={{ flex: 1 }}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {strategy.name}
                  </Typography>
                  <Stack direction="row" spacing={1} sx={{ mt: 0.5 }}>
                    <Chip label={strategy.category} size="small" color="primary" variant="outlined" />
                    <Chip
                      label={`Complexity: ${strategy.complexity}`}
                      size="small"
                      color={complexityColors[strategy.complexity]}
                      variant="outlined"
                    />
                    <Chip
                      label={strategy.potentialSavings}
                      size="small"
                      color="success"
                      icon={<MoneyIcon />}
                    />
                  </Stack>
                </Box>
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={3}>
                {/* Description */}
                <Box>
                  <Typography variant="body1" paragraph>
                    {strategy.description}
                  </Typography>
                  {strategy.irsCode && (
                    <Chip label={strategy.irsCode} size="small" color="info" variant="outlined" />
                  )}
                </Box>

                <Divider />

                {/* Requirements */}
                <Box>
                  <Typography variant="subtitle2" fontWeight="bold" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CheckCircleIcon color="primary" /> Requirements
                  </Typography>
                  <List dense>
                    {strategy.requirements.map((req, idx) => (
                      <ListItem key={idx}>
                        <ListItemText primary={`• ${req}`} />
                      </ListItem>
                    ))}
                  </List>
                </Box>

                {/* Best For */}
                <Box>
                  <Typography variant="subtitle2" fontWeight="bold" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <InfoIcon color="info" /> Best For
                  </Typography>
                  <List dense>
                    {strategy.bestFor.map((item, idx) => (
                      <ListItem key={idx}>
                        <ListItemText primary={`• ${item}`} />
                      </ListItem>
                    ))}
                  </List>
                </Box>

                {/* Risks */}
                <Alert severity="warning">
                  <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                    Risks & Considerations
                  </Typography>
                  <List dense>
                    {strategy.risks.map((risk, idx) => (
                      <ListItem key={idx} sx={{ py: 0 }}>
                        <ListItemText primary={`• ${risk}`} />
                      </ListItem>
                    ))}
                  </List>
                </Alert>

                {/* Expert Tips */}
                <Alert severity="success">
                  <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                    Expert Tips
                  </Typography>
                  <List dense>
                    {strategy.tips.map((tip, idx) => (
                      <ListItem key={idx} sx={{ py: 0 }}>
                        <ListItemText primary={`💡 ${tip}`} />
                      </ListItem>
                    ))}
                  </List>
                </Alert>

                <Button variant="contained" fullWidth>
                  Schedule Consultation with Tax Expert
                </Button>
              </Stack>
            </AccordionDetails>
          </Accordion>
        ))}
      </Box>

      {/* Disclaimer */}
      <Alert severity="warning" sx={{ mt: 4 }}>
        <Typography variant="body2">
          <strong>Important Disclaimer:</strong> These strategies should be implemented only after consultation with a
          licensed CPA or tax attorney. Tax laws are complex and change frequently. What works for one taxpayer may
          not work for another. Always get professional advice before implementing any tax strategy.
        </Typography>
      </Alert>
    </Container>
  );
};
