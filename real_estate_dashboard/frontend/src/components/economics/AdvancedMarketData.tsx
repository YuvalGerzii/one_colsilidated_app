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
  Paper,
  TextField
} from '@mui/material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  ScatterChart,
  Scatter,
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
import HomeWorkIcon from '@mui/icons-material/HomeWork';
import BuildIcon from '@mui/icons-material/Build';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
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
      id={`advanced-tabpanel-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82ca9d', '#ffc658'];

export const AdvancedMarketData: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Hot Zones State
  const [hotZones, setHotZones] = useState<any[]>([]);
  const [hotZonesStats, setHotZonesStats] = useState<any>(null);
  const [selectedHotMarket, setSelectedHotMarket] = useState<string>('');

  // STR Data State
  const [strHotNeighborhoods, setStrHotNeighborhoods] = useState<any[]>([]);
  const [strPerformance, setStrPerformance] = useState<any[]>([]);
  const [strMarketOverview, setStrMarketOverview] = useState<any[]>([]);
  const [strRegulatory, setStrRegulatory] = useState<any[]>([]);
  const [selectedStrMarket, setSelectedStrMarket] = useState<string>('');

  // Zoning State
  const [zoningDistricts, setZoningDistricts] = useState<any[]>([]);
  const [zoningReforms, setZoningReforms] = useState<any[]>([]);
  const [opportunityZones, setOpportunityZones] = useState<any[]>([]);
  const [underbuiltParcels, setUnderbuiltParcels] = useState<any[]>([]);
  const [selectedZoningMarket, setSelectedZoningMarket] = useState<string>('');

  // Development State
  const [developmentPipeline, setDevelopmentPipeline] = useState<any[]>([]);
  const [landCostEconomics, setLandCostEconomics] = useState<any[]>([]);
  const [selectedDevMarket, setSelectedDevMarket] = useState<string>('');

  // Neighborhood Scores State
  const [neighborhoodScores, setNeighborhoodScores] = useState<any[]>([]);
  const [selectedScoreMarket, setSelectedScoreMarket] = useState<string>('');

  // Load Hot Zones Data
  const loadHotZones = async () => {
    setLoading(true);
    setError(null);
    try {
      const params: any = { limit: 100 };
      if (selectedHotMarket) params.market = selectedHotMarket;

      const response = await api.get('/market-intelligence/data/hot-zones', { params });
      if (response.data.success) {
        setHotZones(response.data.data);
        setHotZonesStats({
          total: response.data.total_records,
          markets: response.data.unique_markets,
        });
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load hot zones');
    } finally {
      setLoading(false);
    }
  };

  // Load STR Data
  const loadStrData = async () => {
    setLoading(true);
    setError(null);
    try {
      const params: any = { limit: 50 };
      if (selectedStrMarket) params.market = selectedStrMarket;

      const [hotNeighborhoods, performance, marketOverview, regulatory] = await Promise.all([
        api.get('/market-intelligence/data/str-hot-neighborhoods', { params }),
        api.get('/market-intelligence/data/str-performance-metrics', { params }),
        api.get('/market-intelligence/data/str-market-overview', { params }),
        api.get('/market-intelligence/data/str-regulatory-environment', { params })
      ]);

      setStrHotNeighborhoods(hotNeighborhoods.data.data || []);
      setStrPerformance(performance.data.data || []);
      setStrMarketOverview(marketOverview.data.data || []);
      setStrRegulatory(regulatory.data.data || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load STR data');
    } finally {
      setLoading(false);
    }
  };

  // Load Zoning Data
  const loadZoningData = async () => {
    setLoading(true);
    setError(null);
    try {
      const params: any = { limit: 50 };
      if (selectedZoningMarket) params.market = selectedZoningMarket;

      const [districts, reforms, ozones, parcels] = await Promise.all([
        api.get('/market-intelligence/data/zoning-districts', { params }),
        api.get('/market-intelligence/data/zoning-reforms', { params }),
        api.get('/market-intelligence/data/opportunity-zones', { params }),
        api.get('/market-intelligence/data/underbuilt-parcels', { params })
      ]);

      setZoningDistricts(districts.data.data || []);
      setZoningReforms(reforms.data.data || []);
      setOpportunityZones(ozones.data.data || []);
      setUnderbuiltParcels(parcels.data.data || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load zoning data');
    } finally {
      setLoading(false);
    }
  };

  // Load Development Data
  const loadDevelopmentData = async () => {
    setLoading(true);
    setError(null);
    try {
      const params: any = { limit: 50 };
      if (selectedDevMarket) params.market = selectedDevMarket;

      const [pipeline, landCosts] = await Promise.all([
        api.get('/market-intelligence/data/development-pipeline', { params }),
        api.get('/market-intelligence/data/land-cost-economics', { params })
      ]);

      setDevelopmentPipeline(pipeline.data.data || []);
      setLandCostEconomics(landCosts.data.data || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load development data');
    } finally {
      setLoading(false);
    }
  };

  // Load Neighborhood Scores
  const loadNeighborhoodScores = async () => {
    setLoading(true);
    setError(null);
    try {
      const params: any = { limit: 100 };
      if (selectedScoreMarket) params.market = selectedScoreMarket;

      const response = await api.get('/market-intelligence/data/neighborhood-scores', { params });
      if (response.data.success) {
        setNeighborhoodScores(response.data.data || []);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load neighborhood scores');
    } finally {
      setLoading(false);
    }
  };

  // Load data when tab or filters change
  useEffect(() => {
    if (activeTab === 0) loadHotZones();
    else if (activeTab === 1) loadStrData();
    else if (activeTab === 2) loadZoningData();
    else if (activeTab === 3) loadDevelopmentData();
    else if (activeTab === 4) loadNeighborhoodScores();
  }, [activeTab, selectedHotMarket, selectedStrMarket, selectedZoningMarket, selectedDevMarket, selectedScoreMarket]);

  // Render Hot Zones Tab
  const renderHotZonesTab = () => {
    // Group by market for visualization
    const marketData = hotZones.reduce((acc: any, zone: any) => {
      const market = zone.market || 'Unknown';
      if (!acc[market]) acc[market] = { market, count: 0, avgValue: 0, totalValue: 0 };
      acc[market].count += 1;
      if (zone.metric_value) {
        acc[market].totalValue += zone.metric_value;
        acc[market].avgValue = acc[market].totalValue / acc[market].count;
      }
      return acc;
    }, {});

    const chartData = Object.values(marketData).slice(0, 10);

    return (
      <Box>
        <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
          <TextField
            label="Filter by Market"
            value={selectedHotMarket}
            onChange={(e) => setSelectedHotMarket(e.target.value)}
            variant="outlined"
            size="small"
            fullWidth
          />
          <Button variant="contained" onClick={loadHotZones}>
            Apply Filter
          </Button>
          <Button variant="outlined" onClick={() => { setSelectedHotMarket(''); setTimeout(loadHotZones, 100); }}>
            Clear
          </Button>
        </Stack>

        {hotZonesStats && (
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6">Total Hot Zone Records</Typography>
                  <Typography variant="h3" color="primary">{hotZonesStats.total}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6">Unique Markets</Typography>
                  <Typography variant="h3" color="secondary">{hotZonesStats.markets}</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>Hot Zone Metrics by Market</Typography>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="market" angle={-45} textAnchor="end" height={120} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#8884d8" name="Metrics Count" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>Hot Zone Details</Typography>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Market</TableCell>
                  <TableCell>Metric Name</TableCell>
                  <TableCell>Value</TableCell>
                  <TableCell>Category</TableCell>
                  <TableCell>Period</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {hotZones.slice(0, 20).map((zone: any, idx: number) => (
                  <TableRow key={idx}>
                    <TableCell>{zone.market}</TableCell>
                    <TableCell>{zone.metric_name}</TableCell>
                    <TableCell>
                      {zone.metric_value ? `${zone.metric_value.toFixed(2)} ${zone.metric_unit || ''}` : 'N/A'}
                    </TableCell>
                    <TableCell>
                      <Chip label={zone.metric_category || 'General'} size="small" />
                    </TableCell>
                    <TableCell>{zone.period || 'N/A'}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </Box>
    );
  };

  // Render STR Analysis Tab
  const renderStrTab = () => {
    return (
      <Box>
        <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
          <TextField
            label="Filter by Market"
            value={selectedStrMarket}
            onChange={(e) => setSelectedStrMarket(e.target.value)}
            variant="outlined"
            size="small"
            fullWidth
          />
          <Button variant="contained" onClick={loadStrData}>
            Apply Filter
          </Button>
          <Button variant="outlined" onClick={() => { setSelectedStrMarket(''); setTimeout(loadStrData, 100); }}>
            Clear
          </Button>
        </Stack>

        <Grid container spacing={3}>
          {/* Hot Neighborhoods */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Top STR Neighborhoods by Revenue</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={strHotNeighborhoods.slice(0, 10)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="neighborhood_name" angle={-45} textAnchor="end" height={120} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="avg_annual_revenue_per_listing" fill="#00C49F" name="Avg Annual Revenue" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Performance Metrics */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>STR Performance Metrics</Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Market</TableCell>
                      <TableCell>Property Type</TableCell>
                      <TableCell>ADR</TableCell>
                      <TableCell>Occupancy</TableCell>
                      <TableCell>RevPAR</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {strPerformance.slice(0, 10).map((perf: any, idx: number) => (
                      <TableRow key={idx}>
                        <TableCell>{perf.market}</TableCell>
                        <TableCell>{perf.property_type}</TableCell>
                        <TableCell>${perf.adr?.toFixed(2)}</TableCell>
                        <TableCell>{perf.occupancy_rate_pct?.toFixed(1)}%</TableCell>
                        <TableCell>${perf.revpar?.toFixed(2)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>

          {/* Market Overview */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>STR Market Overview</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={strMarketOverview.slice(0, 8)}
                      dataKey="total_listing_count"
                      nameKey="market"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      label
                    >
                      {strMarketOverview.slice(0, 8).map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Regulatory Environment */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>STR Regulatory Environment</Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Market</TableCell>
                      <TableCell>License Required</TableCell>
                      <TableCell>Permit Cost</TableCell>
                      <TableCell>Timeline (days)</TableCell>
                      <TableCell>Enforcement</TableCell>
                      <TableCell>Status</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {strRegulatory.map((reg: any, idx: number) => (
                      <TableRow key={idx}>
                        <TableCell>{reg.market}</TableCell>
                        <TableCell>
                          <Chip
                            label={reg.license_required ? 'Yes' : 'No'}
                            color={reg.license_required ? 'warning' : 'success'}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>${reg.permit_cost?.toFixed(0) || 'N/A'}</TableCell>
                        <TableCell>{reg.application_timeline_days || 'N/A'}</TableCell>
                        <TableCell>{reg.enforcement_severity || 'N/A'}</TableCell>
                        <TableCell>
                          <Chip label={reg.regulatory_status || 'Unknown'} size="small" />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  // Render Zoning & Development Tab
  const renderZoningTab = () => {
    return (
      <Box>
        <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
          <TextField
            label="Filter by Market"
            value={selectedZoningMarket}
            onChange={(e) => setSelectedZoningMarket(e.target.value)}
            variant="outlined"
            size="small"
            fullWidth
          />
          <Button variant="contained" onClick={loadZoningData}>
            Apply Filter
          </Button>
          <Button variant="outlined" onClick={() => { setSelectedZoningMarket(''); setTimeout(loadZoningData, 100); }}>
            Clear
          </Button>
        </Stack>

        <Grid container spacing={3}>
          {/* Zoning Districts FAR Analysis */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Zoning Districts - Max FAR</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={zoningDistricts.slice(0, 10)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="zone_code" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="max_far" fill="#8884d8" name="Max FAR" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Underbuilt Parcels */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Underbuilt Parcels - FAR Gap</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <ScatterChart>
                    <CartesianGrid />
                    <XAxis dataKey="utilized_far" name="Utilized FAR" />
                    <YAxis dataKey="max_allowable_far" name="Max FAR" />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Scatter name="Parcels" data={underbuiltParcels.slice(0, 50)} fill="#FF8042" />
                  </ScatterChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Zoning Reforms */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Recent Zoning Reforms</Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Market</TableCell>
                      <TableCell>Reform Type</TableCell>
                      <TableCell>Description</TableCell>
                      <TableCell>Announced</TableCell>
                      <TableCell>Implementation</TableCell>
                      <TableCell>Unit Capacity</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {zoningReforms.slice(0, 10).map((reform: any, idx: number) => (
                      <TableRow key={idx}>
                        <TableCell>{reform.market}</TableCell>
                        <TableCell>
                          <Chip label={reform.reform_type} size="small" color="primary" />
                        </TableCell>
                        <TableCell>{reform.reform_description?.substring(0, 60)}...</TableCell>
                        <TableCell>{reform.announcement_date}</TableCell>
                        <TableCell>{reform.implementation_date || 'Pending'}</TableCell>
                        <TableCell>{reform.estimated_unit_capacity_increase || 'N/A'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>

          {/* Opportunity Zones */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Opportunity Zones Investment</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={opportunityZones.slice(0, 10)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="oz_tract_code" angle={-45} textAnchor="end" height={100} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="total_investment_usd" fill="#00C49F" name="Total Investment (USD)" />
                    <Bar dataKey="project_count" fill="#FFBB28" name="Project Count" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  // Render Development Pipeline Tab
  const renderDevelopmentTab = () => {
    // Group pipeline by stage
    const stageData = developmentPipeline.reduce((acc: any, proj: any) => {
      const stage = proj.project_stage || 'Unknown';
      if (!acc[stage]) acc[stage] = { stage, count: 0, totalUnits: 0 };
      acc[stage].count += 1;
      acc[stage].totalUnits += proj.total_units || 0;
      return acc;
    }, {});

    const stageChartData = Object.values(stageData);

    return (
      <Box>
        <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
          <TextField
            label="Filter by Market"
            value={selectedDevMarket}
            onChange={(e) => setSelectedDevMarket(e.target.value)}
            variant="outlined"
            size="small"
            fullWidth
          />
          <Button variant="contained" onClick={loadDevelopmentData}>
            Apply Filter
          </Button>
          <Button variant="outlined" onClick={() => { setSelectedDevMarket(''); setTimeout(loadDevelopmentData, 100); }}>
            Clear
          </Button>
        </Stack>

        <Grid container spacing={3}>
          {/* Pipeline by Stage */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Development Pipeline by Stage</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={stageChartData}
                      dataKey="count"
                      nameKey="stage"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      label
                    >
                      {stageChartData.map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Land Cost Economics */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Land Costs by Market</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={landCostEconomics.slice(0, 10)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="market" angle={-45} textAnchor="end" height={120} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="land_price_per_sf" fill="#8884d8" name="Land Price/SF" />
                    <Bar dataKey="construction_cost_per_sf" fill="#82ca9d" name="Construction Cost/SF" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Pipeline Details Table */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Development Pipeline Projects</Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Market</TableCell>
                      <TableCell>Project Name</TableCell>
                      <TableCell>Stage</TableCell>
                      <TableCell>Property Type</TableCell>
                      <TableCell>Units</TableCell>
                      <TableCell>Total SF</TableCell>
                      <TableCell>Investment</TableCell>
                      <TableCell>Completion</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {developmentPipeline.slice(0, 15).map((proj: any, idx: number) => (
                      <TableRow key={idx}>
                        <TableCell>{proj.market}</TableCell>
                        <TableCell>{proj.project_name}</TableCell>
                        <TableCell>
                          <Chip label={proj.project_stage} size="small" color="primary" />
                        </TableCell>
                        <TableCell>{proj.property_type}</TableCell>
                        <TableCell>{proj.total_units}</TableCell>
                        <TableCell>{proj.total_sf?.toLocaleString()}</TableCell>
                        <TableCell>${proj.estimated_investment_usd?.toLocaleString()}</TableCell>
                        <TableCell>{proj.expected_completion_date || 'TBD'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>

          {/* Land Economics Details */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Land Cost Economics Details</Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Market</TableCell>
                      <TableCell>Property Type</TableCell>
                      <TableCell>Land Price/SF</TableCell>
                      <TableCell>Construction Cost/SF</TableCell>
                      <TableCell>Total Dev Cost/SF</TableCell>
                      <TableCell>Stabilized Value/SF</TableCell>
                      <TableCell>Dev Margin %</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {landCostEconomics.map((land: any, idx: number) => (
                      <TableRow key={idx}>
                        <TableCell>{land.market}</TableCell>
                        <TableCell>{land.property_type}</TableCell>
                        <TableCell>${land.land_price_per_sf?.toFixed(2)}</TableCell>
                        <TableCell>${land.construction_cost_per_sf?.toFixed(2)}</TableCell>
                        <TableCell>${land.total_development_cost_per_sf?.toFixed(2)}</TableCell>
                        <TableCell>${land.estimated_stabilized_value_per_sf?.toFixed(2)}</TableCell>
                        <TableCell>
                          <Chip
                            label={`${land.development_margin_pct?.toFixed(1)}%`}
                            color={land.development_margin_pct > 20 ? 'success' : 'warning'}
                            size="small"
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  // Render Neighborhood Scores Tab
  const renderNeighborhoodScoresTab = () => {
    // Group by score type
    const scoresByType = neighborhoodScores.reduce((acc: any, score: any) => {
      const type = score.score_type || 'Unknown';
      if (!acc[type]) acc[type] = [];
      acc[type].push(score);
      return acc;
    }, {});

    return (
      <Box>
        <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
          <TextField
            label="Filter by Market"
            value={selectedScoreMarket}
            onChange={(e) => setSelectedScoreMarket(e.target.value)}
            variant="outlined"
            size="small"
            fullWidth
          />
          <Button variant="contained" onClick={loadNeighborhoodScores}>
            Apply Filter
          </Button>
          <Button variant="outlined" onClick={() => { setSelectedScoreMarket(''); setTimeout(loadNeighborhoodScores, 100); }}>
            Clear
          </Button>
        </Stack>

        <Grid container spacing={3}>
          {Object.entries(scoresByType).slice(0, 6).map(([scoreType, scores]: [string, any], idx: number) => (
            <Grid item xs={12} md={6} key={idx}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>{scoreType}</Typography>
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={scores.slice(0, 8)}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="neighborhood_name" angle={-45} textAnchor="end" height={100} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="score_value" fill={COLORS[idx % COLORS.length]} />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          ))}

          {/* Full Scores Table */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Neighborhood Scores Details</Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Market</TableCell>
                      <TableCell>Neighborhood</TableCell>
                      <TableCell>Score Type</TableCell>
                      <TableCell>Value</TableCell>
                      <TableCell>Unit</TableCell>
                      <TableCell>Period</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {neighborhoodScores.slice(0, 30).map((score: any, idx: number) => (
                      <TableRow key={idx}>
                        <TableCell>{score.market}</TableCell>
                        <TableCell>{score.neighborhood_name}</TableCell>
                        <TableCell>{score.score_type}</TableCell>
                        <TableCell>{score.score_value?.toFixed(2)}</TableCell>
                        <TableCell>{score.score_unit}</TableCell>
                        <TableCell>{score.period || 'N/A'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    );
  };

  return (
    <Box>
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab icon={<TrendingUpIcon />} label="Hot Zones" />
          <Tab icon={<HomeWorkIcon />} label="STR Analysis" />
          <Tab icon={<BuildIcon />} label="Zoning & Opportunity" />
          <Tab icon={<LocationCityIcon />} label="Development Pipeline" />
          <Tab icon={<AccountBalanceIcon />} label="Neighborhood Scores" />
        </Tabs>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {loading && (
        <Box display="flex" justifyContent="center" p={5}>
          <CircularProgress />
        </Box>
      )}

      {!loading && (
        <>
          <TabPanel value={activeTab} index={0}>
            {renderHotZonesTab()}
          </TabPanel>
          <TabPanel value={activeTab} index={1}>
            {renderStrTab()}
          </TabPanel>
          <TabPanel value={activeTab} index={2}>
            {renderZoningTab()}
          </TabPanel>
          <TabPanel value={activeTab} index={3}>
            {renderDevelopmentTab()}
          </TabPanel>
          <TabPanel value={activeTab} index={4}>
            {renderNeighborhoodScoresTab()}
          </TabPanel>
        </>
      )}
    </Box>
  );
};

export default AdvancedMarketData;
