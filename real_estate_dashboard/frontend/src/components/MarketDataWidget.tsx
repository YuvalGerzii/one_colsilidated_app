/**
 * Market Data Widget Component
 *
 * Displays yfinance stock data, REITs, market indices, treasury rates,
 * and economics API data in a comprehensive dashboard widget.
 */

import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Stack,
  Divider,
  Avatar,
  useTheme,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  IconButton,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ShowChart as ChartIcon,
  Home as HomeIcon,
  Public as PublicIcon,
  AccountBalance as BankIcon,
  FilterList as FilterListIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import {
  useMarketIndices,
  useREITData,
  useTreasuryRates,
  useCountryOverview,
  useHousingData,
  useEconomicSummary,
} from '../hooks/useMarketIntelligence';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index } = props;
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ py: 2 }}>{children}</Box>}
    </div>
  );
}

// Available countries for filtering
const COUNTRIES = [
  { value: 'united-states', label: 'United States' },
  { value: 'israel', label: 'Israel' },
  { value: 'united-kingdom', label: 'United Kingdom' },
  { value: 'canada', label: 'Canada' },
  { value: 'australia', label: 'Australia' },
  { value: 'germany', label: 'Germany' },
  { value: 'france', label: 'France' },
  { value: 'japan', label: 'Japan' },
  { value: 'china', label: 'China' },
];

export const MarketDataWidget: React.FC = () => {
  const theme = useTheme();
  const [tabValue, setTabValue] = useState(0);
  const [selectedCountry, setSelectedCountry] = useState<string>('united-states');
  const [showFilters, setShowFilters] = useState(false);

  // Fetch yfinance data
  const { data: indicesData, isLoading: indicesLoading } = useMarketIndices();
  const { data: reitsData, isLoading: reitsLoading } = useREITData();
  const { data: ratesData, isLoading: ratesLoading } = useTreasuryRates();

  // Fetch economics data (dynamic based on selected country)
  const { data: countryOverview, isLoading: countryLoading } = useCountryOverview(selectedCountry);
  const { data: countryHousing, isLoading: countryHousingLoading } = useHousingData(selectedCountry);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const formatNumber = (num: number | null | undefined, decimals: number = 2): string => {
    if (num === null || num === undefined) return 'N/A';
    return num.toLocaleString(undefined, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });
  };

  const formatPercent = (num: number | null | undefined): string => {
    if (num === null || num === undefined) return 'N/A';
    return `${num > 0 ? '+' : ''}${formatNumber(num, 2)}%`;
  };

  const renderChangeIndicator = (change: number | null | undefined) => {
    if (change === null || change === undefined) return null;
    const isPositive = change > 0;
    return (
      <Chip
        icon={isPositive ? <TrendingUpIcon /> : <TrendingDownIcon />}
        label={formatPercent(change)}
        size="small"
        color={isPositive ? 'success' : 'error'}
        sx={{ ml: 1 }}
      />
    );
  };

  return (
    <Card elevation={3}>
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
          <Box>
            <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0 }}>
              <ChartIcon />
              Market Intelligence Data
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Real-time market data from Yahoo Finance and global economic indicators
            </Typography>
          </Box>
          <Stack direction="row" spacing={1}>
            <IconButton
              size="small"
              onClick={() => setShowFilters(!showFilters)}
              sx={{
                bgcolor: showFilters ? 'primary.main' : 'transparent',
                color: showFilters ? 'white' : 'inherit',
                '&:hover': {
                  bgcolor: showFilters ? 'primary.dark' : 'action.hover',
                },
              }}
            >
              <FilterListIcon />
            </IconButton>
            <IconButton size="small" onClick={() => window.location.reload()}>
              <RefreshIcon />
            </IconButton>
          </Stack>
        </Stack>

        {/* Filter Controls */}
        {showFilters && (
          <Box sx={{ mb: 3, p: 2, bgcolor: 'action.hover', borderRadius: 1 }}>
            <Stack direction="row" spacing={2} alignItems="center">
              <FormControl size="small" sx={{ minWidth: 200 }}>
                <InputLabel>Country</InputLabel>
                <Select
                  value={selectedCountry}
                  label="Country"
                  onChange={(e) => setSelectedCountry(e.target.value)}
                >
                  {COUNTRIES.map((country) => (
                    <MenuItem key={country.value} value={country.value}>
                      {country.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <Button
                variant="outlined"
                size="small"
                onClick={() => setSelectedCountry('united-states')}
              >
                Reset Filters
              </Button>
            </Stack>
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              Filters apply to Economic Data tab. Market data (stocks, REITs, treasury rates) is US-focused.
            </Typography>
          </Box>
        )}

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange} variant="scrollable" scrollButtons="auto">
            <Tab label="Market Indices" />
            <Tab label="REITs" />
            <Tab label="Treasury Rates" />
            <Tab label="Economic Data" />
          </Tabs>
        </Box>

        {/* Market Indices Tab */}
        <TabPanel value={tabValue} index={0}>
          {indicesLoading ? (
            <Box display="flex" justifyContent="center" p={4}>
              <CircularProgress />
            </Box>
          ) : indicesData?.error ? (
            <Alert severity="warning">
              <Typography variant="subtitle2" gutterBottom>
                Can't Extract Data
              </Typography>
              <Typography variant="body2">
                Market indices data is temporarily unavailable. The service may be experiencing issues or rate limiting.
              </Typography>
              <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                Error: {indicesData.error}
              </Typography>
            </Alert>
          ) : !indicesData?.indices || indicesData.indices.length === 0 ? (
            <Alert severity="info">
              <Typography variant="body2">
                No market indices data available at this time. Please try again later.
              </Typography>
            </Alert>
          ) : (
            <TableContainer component={Paper} variant="outlined">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell><strong>Index</strong></TableCell>
                    <TableCell align="right"><strong>Value</strong></TableCell>
                    <TableCell align="right"><strong>Change</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {indicesData.indices.map((index: any) => (
                    <TableRow key={index.symbol}>
                      <TableCell>
                        <Typography variant="body2" fontWeight="600">
                          {index.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {index.symbol}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body1">
                          {formatNumber(index.value, 2)}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        {renderChangeIndicator(index.change_pct)}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          {indicesData && !indicesData.error && indicesData.indices && indicesData.indices.length > 0 && (
            <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
              Last updated: {new Date(indicesData.timestamp).toLocaleString()}
            </Typography>
          )}
        </TabPanel>

        {/* REITs Tab */}
        <TabPanel value={tabValue} index={1}>
          {reitsLoading ? (
            <Box display="flex" justifyContent="center" p={4}>
              <CircularProgress />
            </Box>
          ) : reitsData?.error || (!reitsData?.reits || reitsData.reits.length === 0) ? (
            <Alert severity="warning">
              <Typography variant="subtitle2" gutterBottom>
                Can't Extract Data
              </Typography>
              <Typography variant="body2">
                REIT data is temporarily unavailable. Yahoo Finance may be rate limiting or experiencing issues.
              </Typography>
              {reitsData?.error && (
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Error: {reitsData.error}
                </Typography>
              )}
            </Alert>
          ) : (
            <>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <HomeIcon />
                Real Estate Investment Trusts (REITs)
              </Typography>
              <Grid container spacing={2}>
                {reitsData.reits.slice(0, 6).map((reit: any) => (
                  <Grid item xs={12} sm={6} md={4} key={reit.ticker}>
                    <Card variant="outlined">
                      <CardContent>
                        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={1}>
                          <Typography variant="h6">{reit.ticker}</Typography>
                          {renderChangeIndicator(reit.price_change_pct)}
                        </Stack>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {reit.company_name}
                        </Typography>
                        <Divider sx={{ my: 1 }} />
                        <Stack spacing={1}>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="body2" color="text.secondary">Price:</Typography>
                            <Typography variant="body2" fontWeight="600">
                              ${formatNumber(reit.current_price, 2)}
                            </Typography>
                          </Stack>
                          {reit.dividend_yield && (
                            <Stack direction="row" justifyContent="space-between">
                              <Typography variant="body2" color="text.secondary">Div Yield:</Typography>
                              <Typography variant="body2" fontWeight="600" color="success.main">
                                {formatPercent(reit.dividend_yield * 100)}
                              </Typography>
                            </Stack>
                          )}
                          {reit.market_cap && (
                            <Stack direction="row" justifyContent="space-between">
                              <Typography variant="body2" color="text.secondary">Market Cap:</Typography>
                              <Typography variant="body2">
                                ${(reit.market_cap / 1000000000).toFixed(2)}B
                              </Typography>
                            </Stack>
                          )}
                        </Stack>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </>
          )}
          {reitsData && !reitsData.error && (
            <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
              Showing {reitsData.reits?.slice(0, 6).length} of {reitsData.count} REITs
            </Typography>
          )}
        </TabPanel>

        {/* Treasury Rates Tab */}
        <TabPanel value={tabValue} index={2}>
          {ratesLoading ? (
            <Box display="flex" justifyContent="center" p={4}>
              <CircularProgress />
            </Box>
          ) : ratesData?.error || (!ratesData?.rates || ratesData.rates.length === 0) ? (
            <Alert severity="warning">
              <Typography variant="subtitle2" gutterBottom>
                Can't Extract Data
              </Typography>
              <Typography variant="body2">
                Treasury rates data is temporarily unavailable. Please try again later.
              </Typography>
              {ratesData?.error && (
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Error: {ratesData.error}
                </Typography>
              )}
            </Alert>
          ) : (
            <>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <BankIcon />
                US Treasury Rates & Yields
              </Typography>
              <Grid container spacing={2}>
                {ratesData?.rates?.map((rate: any) => (
                  <Grid item xs={12} sm={6} key={rate.symbol}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                          {rate.name}
                        </Typography>
                        <Stack direction="row" alignItems="baseline" spacing={1}>
                          <Typography variant="h4" color="primary">
                            {formatNumber(rate.rate, 3)}%
                          </Typography>
                          {renderChangeIndicator(rate.change_pct)}
                        </Stack>
                        <Typography variant="caption" color="text.secondary">
                          {rate.symbol}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </>
          )}
        </TabPanel>

        {/* Economic Data Tab */}
        <TabPanel value={tabValue} index={3}>
          <Stack spacing={2}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PublicIcon />
                Economic Indicators - {COUNTRIES.find(c => c.value === selectedCountry)?.label}
              </Typography>
              {selectedCountry !== 'united-states' && (
                <Chip
                  label={`Showing ${COUNTRIES.find(c => c.value === selectedCountry)?.label} data`}
                  color="primary"
                  size="small"
                />
              )}
            </Box>

            {countryLoading ? (
              <Box display="flex" justifyContent="center" p={4}>
                <CircularProgress />
              </Box>
            ) : countryOverview?.error ? (
              <Alert severity="warning">
                <Typography variant="subtitle2" gutterBottom>
                  Can't Extract Economic Data
                </Typography>
                <Typography variant="body2">
                  Economic data for {COUNTRIES.find(c => c.value === selectedCountry)?.label} is temporarily unavailable.
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Error: {countryOverview.error}
                </Typography>
              </Alert>
            ) : (
              <Alert severity="info">
                <Typography variant="body2">
                  <strong>Data Source:</strong> Economics API (500+ economic indicators from Trading Economics)
                </Typography>
              </Alert>
            )}

            {countryHousingLoading ? (
              <Box display="flex" justifyContent="center" p={4}>
                <CircularProgress />
              </Box>
            ) : countryHousing?.error ? (
              <Alert severity="warning">
                <Typography variant="subtitle2" gutterBottom>
                  Can't Extract Housing Data
                </Typography>
                <Typography variant="body2">
                  Housing market data for {COUNTRIES.find(c => c.value === selectedCountry)?.label} is temporarily unavailable.
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Error: {countryHousing.error}
                </Typography>
              </Alert>
            ) : (
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    🏠 {COUNTRIES.find(c => c.value === selectedCountry)?.label} Housing Market Indicators
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Economic indicators including housing starts, building permits, and price indices from the Economics API.
                  </Typography>
                </CardContent>
              </Card>
            )}
          </Stack>
        </TabPanel>
      </CardContent>
    </Card>
  );
};

export default MarketDataWidget;
