import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Tabs,
  Tab,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Stack,
  Alert,
  CircularProgress,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Chip,
  Paper
} from '@mui/material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import LocationCityIcon from '@mui/icons-material/LocationCity';
import AssessmentIcon from '@mui/icons-material/Assessment';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import api from '../../services/api';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`insights-tabpanel-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82ca9d'];

export const MarketIntelligenceInsights: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Hot Zones State
  const [hotZones, setHotZones] = useState<any>(null);
  const [selectedMarket, setSelectedMarket] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  // Neighborhood Scores State
  const [neighborhoodScores, setNeighborhoodScores] = useState<any>(null);
  const [scoreCategory, setScoreCategory] = useState<string>('');

  // Transaction Insights State
  const [transactionInsights, setTransactionInsights] = useState<any>(null);
  const [insightCity, setInsightCity] = useState<string>('Manhattan');
  const [insightPropertyType, setInsightPropertyType] = useState<string>('multifamily');

  // Comparable Analysis State
  const [comparables, setComparables] = useState<any>(null);
  const [targetCity, setTargetCity] = useState<string>('Manhattan');
  const [targetState, setTargetState] = useState<string>('NY');
  const [targetPropertyType, setTargetPropertyType] = useState<string>('multifamily');
  const [targetUnits, setTargetUnits] = useState<number>(100);
  const [targetSF, setTargetSF] = useState<number>(80000);

  // Market Trends State
  const [marketTrends, setMarketTrends] = useState<any>(null);
  const [trendGeography, setTrendGeography] = useState<string>('NYC Metro');

  useEffect(() => {
    loadHotZones();
    loadNeighborhoodScores();
    loadTransactionInsights();
    loadMarketTrends();
  }, []);

  const loadHotZones = async () => {
    try {
      setLoading(true);
      const params: any = { limit: 100 };
      if (selectedMarket) params.market_name = selectedMarket;
      if (selectedCategory) params.metric_category = selectedCategory;

      const response = await api.get('/market-intelligence/data/hot-zones', { params });
      setHotZones(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load hot zones');
    } finally {
      setLoading(false);
    }
  };

  const loadNeighborhoodScores = async () => {
    try {
      setLoading(true);
      const params: any = { limit: 100 };
      if (scoreCategory) params.score_category = scoreCategory;

      const response = await api.get('/market-intelligence/data/neighborhood-scores', { params });
      setNeighborhoodScores(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load neighborhood scores');
    } finally {
      setLoading(false);
    }
  };

  const loadTransactionInsights = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (insightCity) params.city = insightCity;
      if (insightPropertyType) params.property_type = insightPropertyType;

      const response = await api.get('/market-intelligence/analysis/comparable-transactions/insights', { params });
      setTransactionInsights(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load transaction insights');
    } finally {
      setLoading(false);
    }
  };

  const loadMarketTrends = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (trendGeography) params.geography = trendGeography;

      const response = await api.get('/market-intelligence/analysis/market-intelligence/trends', { params });
      setMarketTrends(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load market trends');
    } finally {
      setLoading(false);
    }
  };

  const findComparables = async () => {
    try {
      setLoading(true);
      const params: any = {
        target_city: targetCity,
        target_state: targetState,
        target_property_type: targetPropertyType,
      };
      if (targetUnits) params.target_units = targetUnits;
      if (targetSF) params.target_sf = targetSF;

      const response = await api.get('/market-intelligence/analysis/comparable-analysis', { params });
      setComparables(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to find comparables');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  return (
    <Box sx={{ width: '100%', mt: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <AssessmentIcon fontSize="large" />
        Market Intelligence Insights
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Paper sx={{ width: '100%' }}>
        <Tabs value={activeTab} onChange={handleTabChange} aria-label="market intelligence tabs">
          <Tab icon={<TrendingUpIcon />} label="Hot Zones" />
          <Tab icon={<LocationCityIcon />} label="Neighborhood Scores" />
          <Tab icon={<AssessmentIcon />} label="Transaction Insights" />
          <Tab icon={<TrendingUpIcon />} label="Market Trends" />
          <Tab icon={<CompareArrowsIcon />} label="Comparable Analysis" />
        </Tabs>

        {/* Hot Zones Tab */}
        <TabPanel value={activeTab} index={0}>
          <Stack spacing={3}>
            <Stack direction="row" spacing={2}>
              <TextField
                label="Market Name"
                value={selectedMarket}
                onChange={(e) => setSelectedMarket(e.target.value)}
                placeholder="e.g., NYC, Miami"
                sx={{ minWidth: 200 }}
              />
              <TextField
                label="Metric Category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                placeholder="e.g., Price & Rent Momentum"
                sx={{ minWidth: 250 }}
              />
              <Button variant="contained" onClick={loadHotZones}>
                Load Hot Zones
              </Button>
            </Stack>

            {loading && <CircularProgress />}

            {hotZones && !loading && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Hot Zones Summary
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={4}>
                      <Typography variant="body2" color="text.secondary">Total Hot Zones</Typography>
                      <Typography variant="h4">{hotZones.total_hot_zones || 0}</Typography>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Typography variant="body2" color="text.secondary">Unique Markets</Typography>
                      <Typography variant="h4">{hotZones.unique_markets || 0}</Typography>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Typography variant="body2" color="text.secondary">Unique Neighborhoods</Typography>
                      <Typography variant="h4">{hotZones.unique_neighborhoods || 0}</Typography>
                    </Grid>
                  </Grid>

                  {hotZones.data && hotZones.data.length > 0 && (
                    <>
                      <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
                        Top Emerging Neighborhoods
                      </Typography>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Rank</TableCell>
                            <TableCell>Market</TableCell>
                            <TableCell>Neighborhood</TableCell>
                            <TableCell>Category</TableCell>
                            <TableCell>Metric</TableCell>
                            <TableCell align="right">Value</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {hotZones.data.slice(0, 10).map((zone: any, idx: number) => (
                            <TableRow key={idx}>
                              <TableCell>
                                <Chip
                                  label={zone.hot_zone_rank}
                                  size="small"
                                  color={zone.hot_zone_rank <= 3 ? 'success' : 'default'}
                                />
                              </TableCell>
                              <TableCell>{zone.market_name}</TableCell>
                              <TableCell>{zone.neighborhood_name}</TableCell>
                              <TableCell>{zone.metric_category}</TableCell>
                              <TableCell>{zone.metric_name}</TableCell>
                              <TableCell align="right">
                                {zone.metric_value?.toLocaleString()} {zone.metric_unit}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </>
                  )}
                </CardContent>
              </Card>
            )}
          </Stack>
        </TabPanel>

        {/* Neighborhood Scores Tab */}
        <TabPanel value={activeTab} index={1}>
          <Stack spacing={3}>
            <Stack direction="row" spacing={2}>
              <FormControl sx={{ minWidth: 250 }}>
                <InputLabel>Score Category</InputLabel>
                <Select
                  value={scoreCategory}
                  label="Score Category"
                  onChange={(e) => setScoreCategory(e.target.value)}
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="accessibility_score">Accessibility Score</MenuItem>
                  <MenuItem value="school_quality_score">School Quality Score</MenuItem>
                  <MenuItem value="safety_score">Safety Score</MenuItem>
                  <MenuItem value="amenity_score">Amenity Score</MenuItem>
                  <MenuItem value="investment_potential_score">Investment Potential</MenuItem>
                  <MenuItem value="livability_score">Livability Score</MenuItem>
                </Select>
              </FormControl>
              <Button variant="contained" onClick={loadNeighborhoodScores}>
                Load Scores
              </Button>
            </Stack>

            {loading && <CircularProgress />}

            {neighborhoodScores && !loading && neighborhoodScores.data && neighborhoodScores.data.length > 0 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Top Rated Neighborhoods
                  </Typography>

                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={neighborhoodScores.data.slice(0, 10)}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis
                        dataKey="neighborhood_name"
                        angle={-45}
                        textAnchor="end"
                        height={100}
                      />
                      <YAxis domain={[0, 100]} />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="score_value" fill="#0088FE" name="Score" />
                    </BarChart>
                  </ResponsiveContainer>

                  <Table size="small" sx={{ mt: 3 }}>
                    <TableHead>
                      <TableRow>
                        <TableCell>Market</TableCell>
                        <TableCell>Neighborhood</TableCell>
                        <TableCell>Category</TableCell>
                        <TableCell align="right">Score</TableCell>
                        <TableCell align="right">Market Rank</TableCell>
                        <TableCell align="right">National Rank</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {neighborhoodScores.data.slice(0, 10).map((score: any, idx: number) => (
                        <TableRow key={idx}>
                          <TableCell>{score.market_name}</TableCell>
                          <TableCell>{score.neighborhood_name}</TableCell>
                          <TableCell>{score.score_category}</TableCell>
                          <TableCell align="right">
                            <Chip
                              label={score.score_value}
                              size="small"
                              color={score.score_value >= 80 ? 'success' : score.score_value >= 60 ? 'warning' : 'default'}
                            />
                          </TableCell>
                          <TableCell align="right">{score.rank_within_market || 'N/A'}</TableCell>
                          <TableCell align="right">{score.rank_nationally || 'N/A'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            )}
          </Stack>
        </TabPanel>

        {/* Transaction Insights Tab */}
        <TabPanel value={activeTab} index={2}>
          <Stack spacing={3}>
            <Stack direction="row" spacing={2}>
              <TextField
                label="City"
                value={insightCity}
                onChange={(e) => setInsightCity(e.target.value)}
                sx={{ minWidth: 150 }}
              />
              <FormControl sx={{ minWidth: 150 }}>
                <InputLabel>Property Type</InputLabel>
                <Select
                  value={insightPropertyType}
                  label="Property Type"
                  onChange={(e) => setInsightPropertyType(e.target.value)}
                >
                  <MenuItem value="multifamily">Multifamily</MenuItem>
                  <MenuItem value="office">Office</MenuItem>
                  <MenuItem value="industrial">Industrial</MenuItem>
                  <MenuItem value="mixed-use">Mixed-Use</MenuItem>
                </Select>
              </FormControl>
              <Button variant="contained" onClick={loadTransactionInsights}>
                Analyze
              </Button>
            </Stack>

            {loading && <CircularProgress />}

            {transactionInsights && !loading && transactionInsights.insights && (
              <Grid container spacing={3}>
                {/* Pricing Metrics */}
                <Grid item xs={12}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Pricing Metrics
                      </Typography>
                      <Grid container spacing={2}>
                        <Grid item xs={12} md={3}>
                          <Typography variant="body2" color="text.secondary">Total Volume</Typography>
                          <Typography variant="h5">
                            ${(transactionInsights.insights.pricing.total_volume / 1e9).toFixed(2)}B
                          </Typography>
                        </Grid>
                        <Grid item xs={12} md={3}>
                          <Typography variant="body2" color="text.secondary">Avg Sale Price</Typography>
                          <Typography variant="h5">
                            ${(transactionInsights.insights.pricing.average_sale_price / 1e6).toFixed(1)}M
                          </Typography>
                        </Grid>
                        <Grid item xs={12} md={3}>
                          <Typography variant="body2" color="text.secondary">Avg Price/Unit</Typography>
                          <Typography variant="h5">
                            ${transactionInsights.insights.pricing.average_price_per_unit?.toLocaleString() || 'N/A'}
                          </Typography>
                        </Grid>
                        <Grid item xs={12} md={3}>
                          <Typography variant="body2" color="text.secondary">Avg Cap Rate</Typography>
                          <Typography variant="h5">
                            {transactionInsights.insights.pricing.average_cap_rate?.toFixed(2) || 'N/A'}%
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>

                {/* Monthly Volume Trend */}
                {transactionInsights.insights.trends?.monthly_volume && (
                  <Grid item xs={12} md={8}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Monthly Transaction Volume
                        </Typography>
                        <ResponsiveContainer width="100%" height={300}>
                          <AreaChart data={transactionInsights.insights.trends.monthly_volume}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="month" />
                            <YAxis />
                            <Tooltip formatter={(value: number) => `$${(value / 1e6).toFixed(1)}M`} />
                            <Legend />
                            <Area
                              type="monotone"
                              dataKey="total_volume"
                              stroke="#0088FE"
                              fill="#0088FE"
                              name="Total Volume"
                            />
                          </AreaChart>
                        </ResponsiveContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                )}

                {/* Deal Type Distribution */}
                {transactionInsights.insights.transaction_characteristics?.deal_types && (
                  <Grid item xs={12} md={4}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Deal Type Distribution
                        </Typography>
                        <ResponsiveContainer width="100%" height={300}>
                          <PieChart>
                            <Pie
                              data={Object.entries(transactionInsights.insights.transaction_characteristics.deal_types).map(([name, value]) => ({
                                name,
                                value
                              }))}
                              cx="50%"
                              cy="50%"
                              labelLine={false}
                              label={(entry) => `${entry.name}: ${entry.value}`}
                              outerRadius={80}
                              fill="#8884d8"
                              dataKey="value"
                            >
                              {Object.keys(transactionInsights.insights.transaction_characteristics.deal_types).map((_, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                              ))}
                            </Pie>
                            <Tooltip />
                          </PieChart>
                        </ResponsiveContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                )}
              </Grid>
            )}
          </Stack>
        </TabPanel>

        {/* Market Trends Tab */}
        <TabPanel value={activeTab} index={3}>
          <Stack spacing={3}>
            <Stack direction="row" spacing={2}>
              <TextField
                label="Geography"
                value={trendGeography}
                onChange={(e) => setTrendGeography(e.target.value)}
                placeholder="e.g., NYC Metro"
                sx={{ minWidth: 200 }}
              />
              <Button variant="contained" onClick={loadMarketTrends}>
                Analyze Trends
              </Button>
            </Stack>

            {loading && <CircularProgress />}

            {marketTrends && !loading && marketTrends.trends && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Economic Indicator Trends
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Analyzing {marketTrends.total_indicators} data points across {marketTrends.unique_indicators} indicators
                  </Typography>

                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Geography</TableCell>
                        <TableCell>Indicator</TableCell>
                        <TableCell>Unit</TableCell>
                        <TableCell align="right">Data Points</TableCell>
                        <TableCell align="right">Total Growth</TableCell>
                        <TableCell align="right">CAGR</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {marketTrends.trends.map((trend: any, idx: number) => (
                        <TableRow key={idx}>
                          <TableCell>{trend.geography}</TableCell>
                          <TableCell>{trend.indicator_name}</TableCell>
                          <TableCell>{trend.indicator_unit}</TableCell>
                          <TableCell align="right">{trend.data_points?.length || 0}</TableCell>
                          <TableCell align="right">
                            {trend.total_growth_pct ? (
                              <Chip
                                label={`${trend.total_growth_pct.toFixed(2)}%`}
                                size="small"
                                color={trend.total_growth_pct > 0 ? 'success' : 'error'}
                              />
                            ) : 'N/A'}
                          </TableCell>
                          <TableCell align="right">
                            {trend.cagr_pct ? `${trend.cagr_pct.toFixed(2)}%` : 'N/A'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            )}
          </Stack>
        </TabPanel>

        {/* Comparable Analysis Tab */}
        <TabPanel value={activeTab} index={4}>
          <Stack spacing={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Target Property Details
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={3}>
                    <TextField
                      fullWidth
                      label="City"
                      value={targetCity}
                      onChange={(e) => setTargetCity(e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} md={2}>
                    <TextField
                      fullWidth
                      label="State"
                      value={targetState}
                      onChange={(e) => setTargetState(e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <FormControl fullWidth>
                      <InputLabel>Property Type</InputLabel>
                      <Select
                        value={targetPropertyType}
                        label="Property Type"
                        onChange={(e) => setTargetPropertyType(e.target.value)}
                      >
                        <MenuItem value="multifamily">Multifamily</MenuItem>
                        <MenuItem value="office">Office</MenuItem>
                        <MenuItem value="industrial">Industrial</MenuItem>
                        <MenuItem value="mixed-use">Mixed-Use</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} md={2}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Units"
                      value={targetUnits}
                      onChange={(e) => setTargetUnits(parseInt(e.target.value))}
                    />
                  </Grid>
                  <Grid item xs={12} md={2}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Square Feet"
                      value={targetSF}
                      onChange={(e) => setTargetSF(parseInt(e.target.value))}
                    />
                  </Grid>
                </Grid>
                <Button
                  variant="contained"
                  onClick={findComparables}
                  sx={{ mt: 2 }}
                >
                  Find Comparables
                </Button>
              </CardContent>
            </Card>

            {loading && <CircularProgress />}

            {comparables && !loading && (
              <Grid container spacing={3}>
                {/* Valuation Summary */}
                {comparables.estimated_value_range && (
                  <Grid item xs={12}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Estimated Property Value
                        </Typography>
                        <Grid container spacing={2}>
                          <Grid item xs={12} md={3}>
                            <Typography variant="body2" color="text.secondary">Low</Typography>
                            <Typography variant="h5">
                              ${(comparables.estimated_value_range.low / 1e6).toFixed(2)}M
                            </Typography>
                          </Grid>
                          <Grid item xs={12} md={3}>
                            <Typography variant="body2" color="text.secondary">Mid</Typography>
                            <Typography variant="h5" color="primary">
                              ${(comparables.estimated_value_range.mid / 1e6).toFixed(2)}M
                            </Typography>
                          </Grid>
                          <Grid item xs={12} md={3}>
                            <Typography variant="body2" color="text.secondary">High</Typography>
                            <Typography variant="h5">
                              ${(comparables.estimated_value_range.high / 1e6).toFixed(2)}M
                            </Typography>
                          </Grid>
                          <Grid item xs={12} md={3}>
                            <Typography variant="body2" color="text.secondary">Method</Typography>
                            <Typography variant="h6">
                              {comparables.estimated_value_range.method}
                            </Typography>
                          </Grid>
                        </Grid>
                      </CardContent>
                    </Card>
                  </Grid>
                )}

                {/* Comparables Table */}
                <Grid item xs={12}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Comparable Transactions ({comparables.total_comparables} found)
                      </Typography>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Match Score</TableCell>
                            <TableCell>Address</TableCell>
                            <TableCell>Sale Date</TableCell>
                            <TableCell align="right">Sale Price</TableCell>
                            <TableCell align="right">Price/Unit</TableCell>
                            <TableCell align="right">Cap Rate</TableCell>
                            <TableCell align="right">Units</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {comparables.comparables?.map((comp: any, idx: number) => (
                            <TableRow key={idx}>
                              <TableCell>
                                <Chip
                                  label={`${comp.similarity_score}%`}
                                  size="small"
                                  color={comp.similarity_score >= 90 ? 'success' : comp.similarity_score >= 70 ? 'warning' : 'default'}
                                />
                              </TableCell>
                              <TableCell>{comp.transaction.address}</TableCell>
                              <TableCell>{comp.transaction.sale_date}</TableCell>
                              <TableCell align="right">
                                ${(comp.transaction.sale_price / 1e6).toFixed(2)}M
                              </TableCell>
                              <TableCell align="right">
                                ${comp.transaction.price_per_unit?.toLocaleString() || 'N/A'}
                              </TableCell>
                              <TableCell align="right">
                                {comp.transaction.cap_rate ? `${(comp.transaction.cap_rate * 100).toFixed(2)}%` : 'N/A'}
                              </TableCell>
                              <TableCell align="right">{comp.transaction.units}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            )}
          </Stack>
        </TabPanel>
      </Paper>
    </Box>
  );
};
