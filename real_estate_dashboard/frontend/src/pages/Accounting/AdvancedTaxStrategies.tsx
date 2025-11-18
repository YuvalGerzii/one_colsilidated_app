import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Stack,
  Chip,
  Alert,
  Divider,
  Tabs,
  Tab,
  useTheme,
  alpha,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  AccountBalance as BankIcon,
  Public as GlobalIcon,
  Gavel as LegalIcon,
  Business as BusinessIcon,
  LocalGasStation as OilIcon,
  VolunteerActivism as CharityIcon,
  WarningAmber as WarningIcon,
  InfoOutlined as InfoIcon,
  Shield as ShieldIcon,
  Compare as CompareIcon,
  Calculate as CalculateIcon,
} from '@mui/icons-material';

interface Strategy {
  id: string;
  title: string;
  description: string;
  riskLevel: 'LOW' | 'MODERATE' | 'HIGH' | 'EXTREME';
  irsScrutiny: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  minInvestment: string;
  potentialSavings: string;
  complexity: 'Simple' | 'Moderate' | 'Complex' | 'Expert Only';
  icon: any;
  category: 'depreciation' | 'structure' | 'trust' | 'international' | 'investment' | 'evaluation';
  requires: string[];
  warnings: string[];
}

export const AdvancedTaxStrategies: React.FC = () => {
  const theme = useTheme();
  const [activeCategory, setActiveCategory] = useState<string>('all');

  const strategies: Strategy[] = [
    {
      id: 'section-179-optimizer',
      title: 'Section 179 & Bonus Depreciation Optimizer',
      description: 'Optimize between Section 179 ($1.22M max in 2024) and Bonus Depreciation (60% in 2024) for maximum Year 1 deductions.',
      riskLevel: 'LOW',
      irsScrutiny: 'LOW',
      minInvestment: '$50K+',
      potentialSavings: '20-60% of equipment cost Year 1',
      complexity: 'Moderate',
      icon: CalculateIcon,
      category: 'depreciation',
      requires: ['Business equipment purchases', 'Positive business income', 'Asset-by-asset allocation strategy'],
      warnings: [
        'Section 179 limited by business income',
        'Bonus depreciation phases out: 60% (2024), 40% (2025), 20% (2026)',
        'State conformity varies'
      ]
    },
    {
      id: 'dst-1031',
      title: 'Delaware Statutory Trust (DST) 1031 Exchange',
      description: 'Defer capital gains tax using fractional ownership in institutional-grade properties via DST. IRS Revenue Ruling 2004-86 approved.',
      riskLevel: 'MODERATE',
      irsScrutiny: 'LOW',
      minInvestment: '$100K-$500K',
      potentialSavings: 'Defer 100% of capital gains + 25% recapture',
      complexity: 'Complex',
      icon: BankIcon,
      category: 'structure',
      requires: ['Investment property sale', '45-day identification', 'Equal or greater replacement value'],
      warnings: [
        'Illiquid - typically 5-10 year hold',
        'No control over property management',
        'Sponsor dependency',
        'Securities registration required'
      ]
    },
    {
      id: 'captive-insurance',
      title: '831(b) Micro-Captive Insurance',
      description: 'Captive insurance with up to $2.8M annual premium (2024), taxed only on investment income. WARNING: IRS listed transaction if loss ratio <30%.',
      riskLevel: 'EXTREME',
      irsScrutiny: 'CRITICAL',
      minInvestment: '$500K+',
      potentialSavings: '$400K+ annual (if properly structured)',
      complexity: 'Expert Only',
      icon: ShieldIcon,
      category: 'structure',
      requires: ['Operating company >$5M revenue', 'Real insurance risks', 'Loss ratio >40%', 'Actuarial study'],
      warnings: [
        '🚨 IRS FINAL REGULATIONS January 2025 - Listed Transaction',
        'Loss ratio must be >30% over 5 years',
        'NO loans/financing back to insured',
        'IRS won multiple Tax Court cases 2024',
        'Form 8886 disclosure required if listed transaction',
        'Penalties up to 75% if disallowed'
      ]
    },
    {
      id: 'charitable-remainder-trust',
      title: 'Charitable Remainder Trust (CRT/CRUT)',
      description: 'Donate appreciated assets to trust, receive income stream, get charitable deduction, and avoid capital gains tax on sale inside trust.',
      riskLevel: 'LOW',
      irsScrutiny: 'LOW',
      minInvestment: '$100K+',
      potentialSavings: 'Avoid 20-23.8% capital gains + 37% deduction',
      complexity: 'Complex',
      icon: CharityIcon,
      category: 'trust',
      requires: ['Highly appreciated assets', 'Charitable intent', 'Qualified 501(c)(3) remainder beneficiary'],
      warnings: [
        'Irrevocable - cannot change',
        'Annual admin costs $2K-$5K',
        'Distributions are taxed as ordinary income first',
        'Must pay 5-50% annually'
      ]
    },
    {
      id: 'oil-gas',
      title: 'Oil & Gas Working Interest',
      description: 'Deduct 70-85% of investment in Year 1 via Intangible Drilling Costs (IDCs). Plus 15% percentage depletion allowance on production.',
      riskLevel: 'HIGH',
      irsScrutiny: 'MODERATE',
      minInvestment: '$25K+',
      potentialSavings: '70-85% Year 1 deduction + ongoing depletion',
      complexity: 'Complex',
      icon: OilIcon,
      category: 'investment',
      requires: ['Working interest (not royalty)', 'Accredited investor', 'High income (37% bracket)', 'Long-term hold'],
      warnings: [
        'Dry hole risk - may produce nothing',
        'Commodity price volatility',
        'Illiquid investment',
        'Environmental/regulatory risks'
      ]
    },
    {
      id: 'tax-shelter-evaluator',
      title: 'Tax Shelter Risk Evaluator',
      description: 'Evaluate ANY tax strategy for IRS risk using Economic Substance Doctrine, deduction ratios, and listed transaction criteria.',
      riskLevel: 'LOW',
      irsScrutiny: 'LOW',
      minInvestment: 'N/A - Evaluation Tool',
      potentialSavings: 'Avoid penalties by identifying abusive shelters',
      complexity: 'Moderate',
      icon: WarningIcon,
      category: 'evaluation',
      requires: ['Strategy details', 'Investment amount', 'Expected deductions/losses'],
      warnings: [
        'Abusive tax shelters carry 20-40% penalties',
        'Listed transactions require Form 8886 disclosure',
        'Economic substance doctrine MUST be satisfied'
      ]
    },
    {
      id: 'shelf-company',
      title: 'Shelf Company Analysis',
      description: 'Analyze aged corporations for legitimate uses like contract bidding. WARNING: Using for credit fraud is federal crime.',
      riskLevel: 'MODERATE',
      irsScrutiny: 'MODERATE',
      minInvestment: '$650-$10K',
      potentialSavings: 'Time savings + meet age requirements',
      complexity: 'Simple',
      icon: BusinessIcon,
      category: 'structure',
      requires: ['Legitimate business purpose', 'Due diligence on prior liabilities', 'FinCEN beneficial owner filing'],
      warnings: [
        'Banks scrutinize shelf companies',
        'Cannot use for credit fraud',
        '2024 Corporate Transparency Act requires disclosure',
        'Prior liabilities may exist'
      ]
    },
    {
      id: 'international',
      title: 'International Tax Planning',
      description: 'Analyze foreign structures for LEGAL tax planning with real economic substance. Includes GILTI, FTC, and treaty benefits.',
      riskLevel: 'HIGH',
      irsScrutiny: 'HIGH',
      minInvestment: '$2M+ foreign revenue',
      potentialSavings: '5-15% effective rate reduction',
      complexity: 'Expert Only',
      icon: GlobalIcon,
      category: 'international',
      requires: ['Real foreign operations', '2+ foreign employees', 'Actual business substance', 'Transfer pricing docs'],
      warnings: [
        'MUST have economic substance - not mailbox company',
        'GILTI taxes low-taxed foreign income',
        'Form 5471, 8992, 1118, 8938, FBAR required',
        'IRS challenges structures without business purpose',
        'Compliance costs $80K+ annually'
      ]
    }
  ];

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'LOW':
        return theme.palette.success.main;
      case 'MODERATE':
        return theme.palette.info.main;
      case 'HIGH':
        return theme.palette.warning.main;
      case 'EXTREME':
      case 'CRITICAL':
        return theme.palette.error.main;
      default:
        return theme.palette.grey[500];
    }
  };

  const filteredStrategies = activeCategory === 'all'
    ? strategies
    : strategies.filter(s => s.category === activeCategory);

  const categories = [
    { value: 'all', label: 'All Strategies', count: strategies.length },
    { value: 'depreciation', label: 'Depreciation', count: strategies.filter(s => s.category === 'depreciation').length },
    { value: 'structure', label: 'Entity Structures', count: strategies.filter(s => s.category === 'structure').length },
    { value: 'trust', label: 'Trusts', count: strategies.filter(s => s.category === 'trust').length },
    { value: 'investment', label: 'Investments', count: strategies.filter(s => s.category === 'investment').length },
    { value: 'international', label: 'International', count: strategies.filter(s => s.category === 'international').length },
    { value: 'evaluation', label: 'Evaluation Tools', count: strategies.filter(s => s.category === 'evaluation').length },
  ];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Hero Section */}
      <Box
        sx={{
          background: `linear-gradient(135deg, ${theme.palette.error.dark} 0%, ${theme.palette.warning.dark} 100%)`,
          color: 'white',
          pt: 6,
          pb: 8,
        }}
      >
        <Container maxWidth="lg">
          <Stack spacing={2}>
            <Chip
              icon={<LegalIcon />}
              label="EXPERT-LEVEL TAX STRATEGIES"
              sx={{
                bgcolor: alpha(theme.palette.common.white, 0.2),
                color: 'white',
                fontWeight: 600,
                width: 'fit-content',
              }}
            />
            <Typography variant="h3" fontWeight="bold">
              Advanced Tax Planning
            </Typography>
            <Typography variant="h6" sx={{ opacity: 0.9, maxWidth: '900px' }}>
              Sophisticated strategies for high net worth individuals and businesses. These tools analyze complex tax
              structures including listed transactions, tax shelters, and international planning.
            </Typography>
          </Stack>
        </Container>
      </Box>

      <Container maxWidth="lg" sx={{ mt: -4, mb: 6 }}>
        {/* Warning Alert */}
        <Alert severity="error" icon={<WarningIcon fontSize="large" />} sx={{ mb: 4 }}>
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            ⚠️ PROFESSIONAL GUIDANCE REQUIRED
          </Typography>
          <Typography variant="body2">
            These advanced strategies involve significant legal and tax complexity. Many are under intense IRS scrutiny.
            <strong> Always consult licensed tax attorneys and CPAs before implementation.</strong> Some strategies are
            "listed transactions" requiring Form 8886 disclosure. Penalties for abusive tax shelters range from 20-75% plus
            interest.
          </Typography>
        </Alert>

        {/* Category Tabs */}
        <Paper sx={{ mb: 4 }}>
          <Tabs
            value={activeCategory}
            onChange={(e, newValue) => setActiveCategory(newValue)}
            variant="scrollable"
            scrollButtons="auto"
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
            {categories.map((cat) => (
              <Tab
                key={cat.value}
                value={cat.value}
                label={
                  <Stack direction="row" spacing={1} alignItems="center">
                    <span>{cat.label}</span>
                    <Chip label={cat.count} size="small" />
                  </Stack>
                }
              />
            ))}
          </Tabs>
        </Paper>

        {/* Strategy Cards */}
        <Grid container spacing={3}>
          {filteredStrategies.map((strategy) => {
            const Icon = strategy.icon;
            return (
              <Grid item xs={12} md={6} key={strategy.id}>
                <Card
                  sx={{
                    height: '100%',
                    transition: 'all 0.3s',
                    border: strategy.riskLevel === 'EXTREME' ? 2 : 0,
                    borderColor: strategy.riskLevel === 'EXTREME' ? 'error.main' : 'transparent',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: 6,
                    },
                  }}
                >
                  <CardActionArea sx={{ height: '100%' }}>
                    <CardContent sx={{ p: 3 }}>
                      <Stack spacing={2}>
                        {/* Header */}
                        <Stack direction="row" spacing={2} alignItems="flex-start">
                          <Box
                            sx={{
                              width: 56,
                              height: 56,
                              borderRadius: 2,
                              bgcolor: alpha(getRiskColor(strategy.riskLevel), 0.1),
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                            }}
                          >
                            <Icon sx={{ fontSize: 32, color: getRiskColor(strategy.riskLevel) }} />
                          </Box>
                          <Box flex={1}>
                            <Typography variant="h6" fontWeight="bold" gutterBottom>
                              {strategy.title}
                            </Typography>
                            <Stack direction="row" spacing={1} flexWrap="wrap" gap={0.5}>
                              <Chip
                                label={`Risk: ${strategy.riskLevel}`}
                                size="small"
                                sx={{
                                  bgcolor: alpha(getRiskColor(strategy.riskLevel), 0.1),
                                  color: getRiskColor(strategy.riskLevel),
                                  fontWeight: 600,
                                }}
                              />
                              <Chip
                                label={`IRS: ${strategy.irsScrutiny}`}
                                size="small"
                                color={
                                  strategy.irsScrutiny === 'CRITICAL'
                                    ? 'error'
                                    : strategy.irsScrutiny === 'HIGH'
                                    ? 'warning'
                                    : 'default'
                                }
                                variant="outlined"
                              />
                            </Stack>
                          </Box>
                        </Stack>

                        <Typography variant="body2" color="text.secondary">
                          {strategy.description}
                        </Typography>

                        <Divider />

                        {/* Details Grid */}
                        <Grid container spacing={2}>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              Min Investment
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {strategy.minInvestment}
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              Complexity
                            </Typography>
                            <Typography variant="body2" fontWeight="bold">
                              {strategy.complexity}
                            </Typography>
                          </Grid>
                          <Grid item xs={12}>
                            <Typography variant="caption" color="text.secondary">
                              Potential Savings
                            </Typography>
                            <Typography variant="body2" fontWeight="bold" color="success.main">
                              {strategy.potentialSavings}
                            </Typography>
                          </Grid>
                        </Grid>

                        {/* Requirements */}
                        {strategy.requires.length > 0 && (
                          <Box>
                            <Typography variant="caption" fontWeight="bold" color="text.secondary" gutterBottom>
                              Requirements:
                            </Typography>
                            {strategy.requires.slice(0, 2).map((req, idx) => (
                              <Typography key={idx} variant="caption" display="block" color="text.secondary">
                                • {req}
                              </Typography>
                            ))}
                            {strategy.requires.length > 2 && (
                              <Typography variant="caption" color="primary">
                                +{strategy.requires.length - 2} more...
                              </Typography>
                            )}
                          </Box>
                        )}

                        {/* Warnings */}
                        {strategy.warnings.length > 0 && strategy.riskLevel !== 'LOW' && (
                          <Alert
                            severity={strategy.riskLevel === 'EXTREME' ? 'error' : 'warning'}
                            icon={<WarningIcon />}
                            sx={{ py: 0 }}
                          >
                            <Typography variant="caption" fontWeight="bold">
                              {strategy.warnings[0]}
                            </Typography>
                          </Alert>
                        )}
                      </Stack>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            );
          })}
        </Grid>

        {/* Educational Section */}
        <Paper sx={{ p: 4, mt: 6, bgcolor: 'grey.50' }}>
          <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 3 }}>
            <InfoIcon color="primary" fontSize="large" />
            <Typography variant="h5" fontWeight="bold">
              Understanding Tax Strategy Risk Levels
            </Typography>
          </Stack>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" color="success.main" gutterBottom>
                    LOW RISK - Safe Harbor Strategies
                  </Typography>
                  <Typography variant="body2" paragraph>
                    Established IRS guidance, long legal precedent, minimal audit risk. Examples: Depreciation, Retirement
                    Accounts, 1031 Exchanges.
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Audit Risk:</strong> &lt;5% | <strong>Professional Required:</strong> CPA
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" color="info.main" gutterBottom>
                    MODERATE RISK - Enhanced Documentation
                  </Typography>
                  <Typography variant="body2" paragraph>
                    Legitimate strategies requiring robust documentation of business purpose and economic substance.
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Audit Risk:</strong> 10-30% | <strong>Professional Required:</strong> Tax Attorney
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" color="warning.main" gutterBottom>
                    HIGH RISK - Aggressive Planning
                  </Typography>
                  <Typography variant="body2" paragraph>
                    Complex structures with significant IRS scrutiny. Requires meticulous compliance and may need opinion
                    letters.
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Audit Risk:</strong> 40-70% | <strong>Professional Required:</strong> Tax Counsel Team
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ border: 2, borderColor: 'error.main' }}>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" color="error.main" gutterBottom>
                    EXTREME/CRITICAL - Listed Transactions
                  </Typography>
                  <Typography variant="body2" paragraph>
                    IRS "Dirty Dozen" tax schemes. Form 8886 disclosure required. Penalties 20-75% plus potential criminal
                    charges.
                  </Typography>
                  <Typography variant="body2" color="error">
                    <strong>Audit Risk:</strong> 90%+ | <strong>DO NOT PROCEED</strong> without multiple attorney
                    opinions
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Alert severity="info" sx={{ mt: 3 }}>
            <Typography variant="body2">
              <strong>Economic Substance Doctrine:</strong> All tax strategies must have (1) objective economic substance
              (potential for profit aside from tax benefits) AND (2) subjective business purpose (legitimate business reason
              beyond tax avoidance). Failing either test can result in complete disallowance plus penalties.
            </Typography>
          </Alert>
        </Paper>
      </Container>
    </Box>
  );
};
