import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Stack,
  Chip,
  TextField,
  MenuItem,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Divider,
  Select,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
  ComposedChart,
} from 'recharts';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  LocationOn as LocationIcon,
  Business as BusinessIcon,
  Timeline as TimelineIcon,
  CompareArrows as CompareIcon,
} from '@mui/icons-material';
import { api } from '../../services/apiClient';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const MarketDataVisualization: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Geographic Indicators State
  const [geoIndicators, setGeoIndicators] = useState<any>(null);
  const [selectedGeography, setSelectedGeography] = useState<string>('');
  const [selectedIndicator, setSelectedIndicator] = useState<string>('');
  const [timeseriesData, setTimeseriesData] = useState<any>(null);

  // Real Estate Market Data State
  const [marketData, setMarketData] = useState<any>(null);
  const [selectedMarket, setSelectedMarket] = useState<string>('');
  const [selectedPropertyType, setSelectedPropertyType] = useState<string>('multifamily');

  // Comparable Transactions State
  const [transactions, setTransactions] = useState<any>(null);
  const [transactionFilters, setTransactionFilters] = useState({
    city: '',
    state: 'NY',
    property_type: 'multifamily',
    buyer_type: '',
    seller_type: '',
    min_price: '',
    max_price: '',
  });

  // Load Geographic Indicators on mount
  useEffect(() => {
    loadGeographicIndicators();
    loadMarketData(); // Also load market data on mount
    loadTransactions(); // Also load transactions on mount
  }, []);

  // Load Time-series when geography/indicator changes
  useEffect(() => {
    if (selectedGeography && selectedIndicator) {
      loadTimeseries();
    }
  }, [selectedGeography, selectedIndicator]);

  // Load Market Data when filters change
  useEffect(() => {
    if (tabValue === 1) { // Only load when on market data tab
      loadMarketData();
    }
  }, [selectedMarket, selectedPropertyType]);

  // Load Transactions when filters change
  useEffect(() => {
    if (tabValue === 2) { // Only load when on transactions tab
      loadTransactions();
    }
  }, [transactionFilters]);

  const loadGeographicIndicators = async () => {
    try {
      setLoading(true);
      const response = await api.get('/market-intelligence/data/geographic-indicators', {
        params: { limit: 1000 }
      });
      setGeoIndicators(response.data);

      // Auto-select first geography and indicator if none selected
      if (response.data?.data && response.data.data.length > 0) {
        const uniqueGeos = [...new Set(response.data.data.map((d: any) => d.geography))];
        const uniqueInds = [...new Set(response.data.data.map((d: any) => d.indicator_name))];

        if (!selectedGeography && uniqueGeos.length > 0) {
          setSelectedGeography(uniqueGeos[0] as string);
        }
        if (!selectedIndicator && uniqueInds.length > 0) {
          setSelectedIndicator(uniqueInds[0] as string);
        }
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load geographic indicators');
    } finally {
      setLoading(false);
    }
  };

  const loadTimeseries = async () => {
    try {
      setLoading(true);
      const response = await api.get('/market-intelligence/data/geographic-indicators/timeseries', {
        params: {
          geography: selectedGeography,
          indicator_name: selectedIndicator
        }
      });
      setTimeseriesData(response.data);
    } catch (err: any) {
      console.error('Error loading timeseries:', err);
      setTimeseriesData(null);
    } finally {
      setLoading(false);
    }
  };

  const loadMarketData = async () => {
    try {
      setLoading(true);
      const params: any = {
        property_type: selectedPropertyType,
        limit: 1000
      };

      // Only add market_name filter if a value is selected
      if (selectedMarket) {
        params.market_name = selectedMarket;
      }

      const response = await api.get('/market-intelligence/data/real-estate-market', {
        params
      });
      setMarketData(response.data);

      // Auto-select first market if none selected
      if (!selectedMarket && response.data?.data && response.data.data.length > 0) {
        const uniqueMarkets = [...new Set(response.data.data.map((d: any) => d.market_name))];
        if (uniqueMarkets.length > 0) {
          setSelectedMarket(uniqueMarkets[0] as string);
        }
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load market data');
    } finally {
      setLoading(false);
    }
  };

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const params: any = {
        limit: 100
      };

      // Only add filters if they have values
      if (transactionFilters.city) {
        params.city = transactionFilters.city;
      }
      if (transactionFilters.state) {
        params.state = transactionFilters.state;
      }
      if (transactionFilters.property_type) {
        params.property_type = transactionFilters.property_type;
      }

      const response = await api.get('/market-intelligence/data/comparable-transactions', {
        params
      });
      setTransactions(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load transactions');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number | null) => {
    if (value === null || value === undefined) return 'N/A';
    if (value >= 1000000000) return `$${(value / 1000000000).toFixed(2)}B`;
    if (value >= 1000000) return `$${(value / 1000000).toFixed(2)}M`;
    if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
    return `$${value.toFixed(0)}`;
  };

  const formatNumber = (value: number | null) => {
    if (value === null || value === undefined) return 'N/A';
    return value.toLocaleString();
  };

  const formatPercentage = (value: number | null) => {
    if (value === null || value === undefined) return 'N/A';
    return `${(value * 100).toFixed(2)}%`;
  };

  // Get unique geographies and indicators for dropdowns
  const uniqueGeographies = geoIndicators?.data
    ? [...new Set(geoIndicators.data.map((d: any) => d.geography))]
    : [];

  const uniqueIndicators = geoIndicators?.data
    ? [...new Set(geoIndicators.data.map((d: any) => d.indicator_name))]
    : [];

  // Get unique markets for real estate dropdown
  const uniqueMarkets = marketData?.data
    ? [...new Set(marketData.data.map((d: any) => d.market_name))]
    : [];

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <TimelineIcon />
        Market Intelligence Data
      </Typography>

      <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)} sx={{ mb: 2 }}>
        <Tab label="Geographic Indicators" />
        <Tab label="Real Estate Market Metrics" />
        <Tab label="Comparable Transactions" />
      </Tabs>

      {/* Geographic Indicators Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          {/* Summary Cards */}
          <Grid item xs={12}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Total Records
                    </Typography>
                    <Typography variant="h4">
                      {geoIndicators?.total_records?.toLocaleString() || '0'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Unique Geographies
                    </Typography>
                    <Typography variant="h4">
                      {geoIndicators?.unique_geographies || '0'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Unique Indicators
                    </Typography>
                    <Typography variant="h4">
                      {geoIndicators?.unique_indicators || '0'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Grid>

          {/* Filters */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Stack direction="row" spacing={2} alignItems="center">
                  <FormControl sx={{ minWidth: 200 }}>
                    <InputLabel>Geography</InputLabel>
                    <Select
                      value={selectedGeography}
                      label="Geography"
                      onChange={(e) => setSelectedGeography(e.target.value)}
                    >
                      {uniqueGeographies.map((geo: string) => (
                        <MenuItem key={geo} value={geo}>{geo}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>

                  <FormControl sx={{ minWidth: 250 }}>
                    <InputLabel>Indicator</InputLabel>
                    <Select
                      value={selectedIndicator}
                      label="Indicator"
                      onChange={(e) => setSelectedIndicator(e.target.value)}
                    >
                      {uniqueIndicators.map((ind: string) => (
                        <MenuItem key={ind} value={ind}>{ind}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>

                  <Button
                    variant="contained"
                    onClick={loadTimeseries}
                    disabled={loading}
                  >
                    Load Time Series
                  </Button>
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Time Series Chart */}
          {timeseriesData && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {timeseriesData.geography} - {timeseriesData.indicator_name}
                  </Typography>

                  <Grid container spacing={2} sx={{ mb: 2 }}>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="textSecondary">Min</Typography>
                      <Typography variant="body2">{formatNumber(timeseriesData.trends?.min)}</Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="textSecondary">Max</Typography>
                      <Typography variant="body2">{formatNumber(timeseriesData.trends?.max)}</Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="textSecondary">Average</Typography>
                      <Typography variant="body2">{formatNumber(timeseriesData.trends?.avg)}</Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="textSecondary">Latest</Typography>
                      <Typography variant="body2">{formatNumber(timeseriesData.trends?.latest)}</Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="textSecondary">Total Change</Typography>
                      <Typography variant="body2">
                        {formatNumber(timeseriesData.trends?.total_change)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="textSecondary">Change %</Typography>
                      <Typography variant="body2" color={timeseriesData.trends?.total_change_percent >= 0 ? 'success.main' : 'error.main'}>
                        {timeseriesData.trends?.total_change_percent?.toFixed(2)}%
                      </Typography>
                    </Grid>
                  </Grid>

                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={timeseriesData.data}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="period" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Area
                        type="monotone"
                        dataKey="value"
                        stroke="#8884d8"
                        fill="#8884d8"
                        fillOpacity={0.3}
                        name={timeseriesData.indicator_name}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </TabPanel>

      {/* Real Estate Market Metrics Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          {/* Summary Cards */}
          <Grid item xs={12}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Total Records
                    </Typography>
                    <Typography variant="h4">
                      {marketData?.total_records?.toLocaleString() || '0'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Unique Markets
                    </Typography>
                    <Typography variant="h4">
                      {marketData?.unique_markets || '0'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Property Types
                    </Typography>
                    <Typography variant="h4">
                      {marketData?.unique_property_types || '0'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Grid>

          {/* Filters */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Stack direction="row" spacing={2}>
                  <FormControl sx={{ minWidth: 250 }}>
                    <InputLabel>Market Name</InputLabel>
                    <Select
                      value={selectedMarket}
                      label="Market Name"
                      onChange={(e) => setSelectedMarket(e.target.value)}
                    >
                      {uniqueMarkets.map((market: string) => (
                        <MenuItem key={market} value={market}>{market}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <FormControl sx={{ minWidth: 200 }}>
                    <InputLabel>Property Type</InputLabel>
                    <Select
                      value={selectedPropertyType}
                      label="Property Type"
                      onChange={(e) => setSelectedPropertyType(e.target.value)}
                    >
                      <MenuItem value="multifamily">Multifamily</MenuItem>
                      <MenuItem value="office">Office</MenuItem>
                      <MenuItem value="retail">Retail</MenuItem>
                      <MenuItem value="industrial">Industrial</MenuItem>
                    </Select>
                  </FormControl>
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Market Data Table */}
          {marketData && marketData.data && marketData.data.length > 0 && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {selectedMarket} - {selectedPropertyType} Market Metrics
                  </Typography>

                  <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
                    <Table stickyHeader size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Market</TableCell>
                          <TableCell>Submarket</TableCell>
                          <TableCell>Class</TableCell>
                          <TableCell>Metric</TableCell>
                          <TableCell align="right">Value</TableCell>
                          <TableCell>Unit</TableCell>
                          <TableCell>Period</TableCell>
                          <TableCell>Source</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {marketData.data.slice(0, 50).map((row: any) => (
                          <TableRow key={row.id} hover>
                            <TableCell>{row.market_name}</TableCell>
                            <TableCell>{row.submarket_name || '-'}</TableCell>
                            <TableCell>{row.property_class || '-'}</TableCell>
                            <TableCell>{row.metric_name}</TableCell>
                            <TableCell align="right">{formatNumber(row.metric_value)}</TableCell>
                            <TableCell>{row.metric_unit}</TableCell>
                            <TableCell>{new Date(row.period).toLocaleDateString()}</TableCell>
                            <TableCell>{row.data_source}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </TabPanel>

      {/* Comparable Transactions Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          {/* Summary Cards */}
          <Grid item xs={12}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Total Transactions
                    </Typography>
                    <Typography variant="h4">
                      {transactions?.total_transactions?.toLocaleString() || '0'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Unique Cities
                    </Typography>
                    <Typography variant="h4">
                      {transactions?.unique_cities || '0'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Grid>

          {/* Filters */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Stack spacing={2}>
                  <Stack direction="row" spacing={2}>
                    <TextField
                      label="City"
                      value={transactionFilters.city}
                      onChange={(e) => setTransactionFilters({ ...transactionFilters, city: e.target.value })}
                      sx={{ minWidth: 150 }}
                    />
                    <FormControl sx={{ minWidth: 120 }}>
                      <InputLabel>State</InputLabel>
                      <Select
                        value={transactionFilters.state}
                        label="State"
                        onChange={(e) => setTransactionFilters({ ...transactionFilters, state: e.target.value })}
                      >
                        <MenuItem value="">All</MenuItem>
                        <MenuItem value="NY">NY</MenuItem>
                        <MenuItem value="FL">FL</MenuItem>
                        <MenuItem value="CA">CA</MenuItem>
                        <MenuItem value="IL">IL</MenuItem>
                        <MenuItem value="TX">TX</MenuItem>
                      </Select>
                    </FormControl>
                    <FormControl sx={{ minWidth: 150 }}>
                      <InputLabel>Property Type</InputLabel>
                      <Select
                        value={transactionFilters.property_type}
                        label="Property Type"
                        onChange={(e) => setTransactionFilters({ ...transactionFilters, property_type: e.target.value })}
                      >
                        <MenuItem value="">All</MenuItem>
                        <MenuItem value="multifamily">Multifamily</MenuItem>
                        <MenuItem value="office">Office</MenuItem>
                        <MenuItem value="mixed-use">Mixed-Use</MenuItem>
                        <MenuItem value="industrial">Industrial</MenuItem>
                        <MenuItem value="sfr">SFR</MenuItem>
                      </Select>
                    </FormControl>
                    <TextField
                      label="Buyer Type"
                      value={transactionFilters.buyer_type}
                      onChange={(e) => setTransactionFilters({ ...transactionFilters, buyer_type: e.target.value })}
                      placeholder="e.g., REIT, Institutional"
                      sx={{ minWidth: 180 }}
                    />
                    <TextField
                      label="Seller Type"
                      value={transactionFilters.seller_type}
                      onChange={(e) => setTransactionFilters({ ...transactionFilters, seller_type: e.target.value })}
                      placeholder="e.g., Developer, Fund"
                      sx={{ minWidth: 180 }}
                    />
                  </Stack>
                  <Stack direction="row" spacing={2}>
                    <TextField
                      label="Min Price"
                      value={transactionFilters.min_price}
                      onChange={(e) => setTransactionFilters({ ...transactionFilters, min_price: e.target.value })}
                      placeholder="e.g., 1000000"
                      type="number"
                      sx={{ minWidth: 150 }}
                    />
                    <TextField
                      label="Max Price"
                      value={transactionFilters.max_price}
                      onChange={(e) => setTransactionFilters({ ...transactionFilters, max_price: e.target.value })}
                      placeholder="e.g., 100000000"
                      type="number"
                      sx={{ minWidth: 150 }}
                    />
                    <Button
                      variant="outlined"
                      onClick={() => setTransactionFilters({
                        city: '',
                        state: 'NY',
                        property_type: 'multifamily',
                        buyer_type: '',
                        seller_type: '',
                        min_price: '',
                        max_price: '',
                      })}
                    >
                      Clear Filters
                    </Button>
                  </Stack>
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Transactions Table */}
          {transactions && transactions.data && transactions.data.length > 0 && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Recent Comparable Transactions
                  </Typography>

                  <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
                    <Table stickyHeader size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Address</TableCell>
                          <TableCell>City</TableCell>
                          <TableCell>Property Type</TableCell>
                          <TableCell align="right">Sale Price</TableCell>
                          <TableCell align="right">Price/Unit</TableCell>
                          <TableCell align="right">Price/SF</TableCell>
                          <TableCell align="right">Cap Rate</TableCell>
                          <TableCell align="right">NOI</TableCell>
                          <TableCell align="right">Units</TableCell>
                          <TableCell>Year Built</TableCell>
                          <TableCell>Buyer Type</TableCell>
                          <TableCell>Seller Type</TableCell>
                          <TableCell align="right">LTV</TableCell>
                          <TableCell>Sale Date</TableCell>
                          <TableCell>Deal Type</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {transactions.data.map((txn: any) => (
                          <TableRow key={txn.id} hover>
                            <TableCell>{txn.address}</TableCell>
                            <TableCell>{txn.city}</TableCell>
                            <TableCell>
                              <Chip
                                label={txn.property_type}
                                size="small"
                                color={txn.property_class === 'A' ? 'success' : txn.property_class === 'B' ? 'primary' : 'default'}
                              />
                            </TableCell>
                            <TableCell align="right">{formatCurrency(txn.sale_price)}</TableCell>
                            <TableCell align="right">{formatCurrency(txn.price_per_unit)}</TableCell>
                            <TableCell align="right">{txn.price_per_sf ? `$${txn.price_per_sf.toFixed(0)}` : 'N/A'}</TableCell>
                            <TableCell align="right">{formatPercentage(txn.cap_rate)}</TableCell>
                            <TableCell align="right">{formatCurrency(txn.noi)}</TableCell>
                            <TableCell align="right">{formatNumber(txn.units)}</TableCell>
                            <TableCell>{txn.year_built || 'N/A'}</TableCell>
                            <TableCell>{txn.buyer_type || '-'}</TableCell>
                            <TableCell>{txn.seller_type || '-'}</TableCell>
                            <TableCell align="right">{txn.ltv ? `${(txn.ltv * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                            <TableCell>{new Date(txn.sale_date).toLocaleDateString()}</TableCell>
                            <TableCell>
                              <Chip label={txn.deal_type} size="small" variant="outlined" />
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </TabPanel>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};

export default MarketDataVisualization;
