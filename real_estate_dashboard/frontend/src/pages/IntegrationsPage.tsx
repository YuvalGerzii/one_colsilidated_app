/**
 * Third-Party Integrations Management Page
 *
 * View and test third-party integrations status
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  CircularProgress,
  Alert,
  Divider,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Collapse,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Refresh as RefreshIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
} from '@mui/icons-material';
import { api } from '../services/apiClient';

interface Integration {
  name: string;
  category: string;
  status: string;
  is_free: boolean;
  available: boolean;
}

interface IntegrationStatus {
  integrations: Record<string, Integration>;
  total_count: number;
  active_count: number;
  categories: Record<string, number>;
}

interface IntegrationMetadata {
  metadata: {
    name: string;
    category: string;
    description: string;
    is_free: boolean;
    requires_api_key: boolean;
    documentation_url: string | null;
    features: string[];
  };
  status: string;
  available: boolean;
}

const IntegrationsPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [integrationStatus, setIntegrationStatus] = useState<IntegrationStatus | null>(null);
  const [expandedIntegration, setExpandedIntegration] = useState<string | null>(null);
  const [integrationMetadata, setIntegrationMetadata] = useState<Record<string, IntegrationMetadata>>({});
  const [testResults, setTestResults] = useState<Record<string, any>>({});
  const [testing, setTesting] = useState<Record<string, boolean>>({});
  const [cacheTimestamp, setCacheTimestamp] = useState<string | null>(null);
  const [usingCache, setUsingCache] = useState(false);

  // Cache keys
  const CACHE_KEY = 'integrations_status_cache';
  const CACHE_TIMESTAMP_KEY = 'integrations_cache_timestamp';
  const CACHE_EXPIRY_MS = 15 * 60 * 1000; // 15 minutes

  // Load from cache on mount
  useEffect(() => {
    loadFromCache();
    fetchIntegrationStatus();
  }, []);

  const loadFromCache = () => {
    try {
      const cached = localStorage.getItem(CACHE_KEY);
      const timestamp = localStorage.getItem(CACHE_TIMESTAMP_KEY);

      if (cached && timestamp) {
        const cacheAge = Date.now() - parseInt(timestamp);

        // Use cache if less than expiry time
        if (cacheAge < CACHE_EXPIRY_MS) {
          const parsedCache = JSON.parse(cached);
          setIntegrationStatus(parsedCache);
          setCacheTimestamp(new Date(parseInt(timestamp)).toLocaleString());
          setUsingCache(true);
          console.log('Loaded integrations from cache');
        } else {
          console.log('Cache expired, will fetch fresh data');
        }
      }
    } catch (err) {
      console.error('Failed to load from cache:', err);
    }
  };

  const saveToCache = (data: IntegrationStatus) => {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify(data));
      localStorage.setItem(CACHE_TIMESTAMP_KEY, Date.now().toString());
      setCacheTimestamp(new Date().toLocaleString());
      console.log('Saved integrations to cache');
    } catch (err) {
      console.error('Failed to save to cache:', err);
    }
  };

  const fetchIntegrationStatus = async (retryCount = 0) => {
    try {
      setLoading(true);
      setError(null);

      // Add timeout to prevent hanging
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout (government APIs can be slow)

      const response = await api.get('/integrations/status', {
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      // Save successful response to cache
      saveToCache(response.data);
      setIntegrationStatus(response.data);
      setUsingCache(false);

    } catch (err: any) {
      console.error('Integration status fetch error:', err);

      // Retry logic for network errors
      if (retryCount < 2 && (err.code === 'ECONNABORTED' || err.message?.includes('Network Error') || err.name === 'AbortError')) {
        console.log(`Retrying... attempt ${retryCount + 1}`);
        setTimeout(() => fetchIntegrationStatus(retryCount + 1), 1000 * (retryCount + 1));
        return;
      }

      // Try to use cache first if available
      try {
        const cached = localStorage.getItem(CACHE_KEY);
        if (cached) {
          const parsedCache = JSON.parse(cached);
          setIntegrationStatus(parsedCache);
          setUsingCache(true);
          setError(`API unavailable - showing cached data from ${cacheTimestamp || 'earlier'}. Error: ${err.message || 'Unknown error'}`);
          return;
        }
      } catch (cacheErr) {
        console.error('Failed to load from cache:', cacheErr);
      }

      // Use fallback data if cache not available
      console.warn('Using fallback integration data');
      const fallbackData: IntegrationStatus = {
        integrations: {
          bls: {
            name: 'Bureau of Labor Statistics',
            category: 'market_data',
            status: 'active',
            is_free: true,
            available: true
          },
          datagov_us: {
            name: 'Data.gov US',
            category: 'official_data',
            status: 'active',
            is_free: true,
            available: true
          },
          bank_of_israel: {
            name: 'Bank of Israel',
            category: 'official_data',
            status: 'active',
            is_free: true,
            available: true
          },
          hud: {
            name: 'HUD (Housing & Urban Development)',
            category: 'official_data',
            status: 'active',
            is_free: true,
            available: true
          },
          fhfa: {
            name: 'FHFA (Federal Housing Finance Agency)',
            category: 'official_data',
            status: 'active',
            is_free: true,
            available: true
          }
        },
        total_count: 5,
        active_count: 5,
        categories: {
          market_data: 1,
          official_data: 3
        }
      };

      setIntegrationStatus(fallbackData);
      setUsingCache(true);
      setError(`API unavailable - showing fallback data. Error: ${err.message || 'Unknown error'}`);

    } finally {
      setLoading(false);
    }
  };

  const fetchIntegrationMetadata = async (key: string) => {
    if (integrationMetadata[key]) return;

    try {
      const response = await api.get(`/integrations/metadata/${key}`);
      setIntegrationMetadata(prev => ({
        ...prev,
        [key]: response.data
      }));
    } catch (err: any) {
      console.error(`Failed to fetch metadata for ${key}:`, err);
    }
  };

  const testIntegration = async (key: string) => {
    try {
      setTesting(prev => ({ ...prev, [key]: true }));
      const response = await api.get(`/integrations/test/${key}`);
      setTestResults(prev => ({
        ...prev,
        [key]: response.data
      }));
    } catch (err: any) {
      setTestResults(prev => ({
        ...prev,
        [key]: { success: false, error: err.message }
      }));
    } finally {
      setTesting(prev => ({ ...prev, [key]: false }));
    }
  };

  const handleExpandIntegration = (key: string) => {
    if (expandedIntegration === key) {
      setExpandedIntegration(null);
    } else {
      setExpandedIntegration(key);
      fetchIntegrationMetadata(key);
    }
  };

  const getStatusIcon = (integration: Integration) => {
    if (integration.available) {
      return <CheckCircleIcon color="success" />;
    } else if (integration.status === 'not_configured') {
      return <WarningIcon color="warning" />;
    } else {
      return <ErrorIcon color="error" />;
    }
  };

  const getStatusColor = (integration: Integration) => {
    if (integration.available) return 'success';
    if (integration.status === 'not_configured') return 'warning';
    return 'error';
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, any> = {
      market_data: 'primary',
      property_data: 'secondary',
      banking: 'info',
      tools: 'success',
    };
    return colors[category] || 'default';
  };

  if (loading) {
    return (
      <Container sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error && !integrationStatus) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={() => fetchIntegrationStatus()}>
          Retry
        </Button>
      </Container>
    );
  }

  if (!integrationStatus) {
    return null;
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Warning if using fallback data */}
      {error && integrationStatus && (
        <Alert severity="warning" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Cache status indicator */}
      {usingCache && cacheTimestamp && !error && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Showing cached data from {cacheTimestamp}. Data refreshes automatically when API is available.
        </Alert>
      )}

      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="h4" component="h1">
              Third-Party Integrations
            </Typography>
            {usingCache && (
              <Chip
                label={`Cached: ${cacheTimestamp}`}
                size="small"
                color="info"
                icon={<InfoIcon />}
              />
            )}
          </Box>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={() => fetchIntegrationStatus()}
          >
            Refresh
          </Button>
        </Box>
        <Typography variant="body1" color="text.secondary">
          Manage and monitor third-party service integrations
        </Typography>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Integrations
              </Typography>
              <Typography variant="h3">
                {integrationStatus.total_count}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Active
              </Typography>
              <Typography variant="h3" color="success.main">
                {integrationStatus.active_count}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Not Configured
              </Typography>
              <Typography variant="h3" color="warning.main">
                {integrationStatus.total_count - integrationStatus.active_count}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Free Integrations
              </Typography>
              <Typography variant="h3" color="primary.main">
                {Object.values(integrationStatus.integrations).filter(i => i.is_free).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Integration Cards */}
      <Grid container spacing={3}>
        {Object.entries(integrationStatus.integrations).map(([key, integration]) => {
          const metadata = integrationMetadata[key];
          const testResult = testResults[key];
          const isTesting = testing[key];
          const isExpanded = expandedIntegration === key;

          return (
            <Grid item xs={12} md={6} lg={4} key={key}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getStatusIcon(integration)}
                      <Typography variant="h6">
                        {integration.name}
                      </Typography>
                    </Box>
                    <Chip
                      label={integration.is_free ? 'FREE' : 'PAID'}
                      size="small"
                      color={integration.is_free ? 'success' : 'warning'}
                    />
                  </Box>

                  <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                    <Chip
                      label={integration.category.replace('_', ' ')}
                      size="small"
                      color={getCategoryColor(integration.category)}
                    />
                    <Chip
                      label={integration.status.replace('_', ' ')}
                      size="small"
                      color={getStatusColor(integration)}
                    />
                  </Box>

                  {metadata && (
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {metadata.metadata.description}
                    </Typography>
                  )}

                  {testResult && (
                    <Alert
                      severity={testResult.success ? 'success' : 'error'}
                      sx={{ mb: 2 }}
                    >
                      {testResult.message || testResult.error}
                    </Alert>
                  )}
                </CardContent>

                <CardActions>
                  <Button
                    size="small"
                    onClick={() => testIntegration(key)}
                    disabled={!integration.available || isTesting}
                    startIcon={isTesting ? <CircularProgress size={16} /> : null}
                  >
                    {isTesting ? 'Testing...' : 'Test Connection'}
                  </Button>
                  <Button
                    size="small"
                    onClick={() => handleExpandIntegration(key)}
                    endIcon={isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                  >
                    {isExpanded ? 'Less' : 'More'}
                  </Button>
                </CardActions>

                <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                  <CardContent>
                    {metadata && (
                      <>
                        <Divider sx={{ mb: 2 }} />
                        <Typography variant="subtitle2" gutterBottom>
                          Features:
                        </Typography>
                        <List dense>
                          {metadata.metadata.features.map((feature, idx) => (
                            <ListItem key={idx}>
                              <ListItemText primary={`• ${feature}`} />
                            </ListItem>
                          ))}
                        </List>
                        {metadata.metadata.documentation_url && (
                          <Button
                            size="small"
                            href={metadata.metadata.documentation_url}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            View Documentation
                          </Button>
                        )}
                      </>
                    )}
                  </CardContent>
                </Collapse>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      {/* Market Intelligence Data Sources */}
      <Box sx={{ mt: 6, mb: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Market Intelligence Data Sources
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Imported data from government APIs and property listings
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Census Data
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Demographics and housing statistics from US Census Bureau
                </Typography>
                <Chip label="FREE" color="success" size="small" sx={{ mb: 2 }} />
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    Source: ACS 5-Year Estimates
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={async () => {
                    try {
                      await api.post('/market-intelligence/import/census');
                      alert('Census data imported successfully!');
                      fetchIntegrationStatus();
                    } catch (err: any) {
                      alert('Import failed: ' + err.message);
                    }
                  }}
                >
                  Import Data
                </Button>
              </CardActions>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  FRED Indicators
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Economic indicators from Federal Reserve Economic Data
                </Typography>
                <Chip label="FREE" color="success" size="small" sx={{ mb: 2 }} />
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    Mortgage rates, housing starts, home prices
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={async () => {
                    try {
                      await api.post('/market-intelligence/import/fred');
                      alert('FRED data imported successfully!');
                      fetchIntegrationStatus();
                    } catch (err: any) {
                      alert('Import failed: ' + err.message);
                    }
                  }}
                >
                  Import Data
                </Button>
              </CardActions>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  HUD Fair Market Rents
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Rental market data from Housing and Urban Development
                </Typography>
                <Chip label="FREE" color="success" size="small" sx={{ mb: 2 }} />
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    FMR by bedroom size, income limits
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={async () => {
                    try {
                      await api.post('/market-intelligence/import/hud');
                      alert('HUD data imported successfully!');
                      fetchIntegrationStatus();
                    } catch (err: any) {
                      alert('Import failed: ' + err.message);
                    }
                  }}
                >
                  Import Data
                </Button>
              </CardActions>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Property Listings
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Scraped property data from Zillow, Redfin, Realtor.com
                </Typography>
                <Chip label="SAMPLE DATA" color="info" size="small" sx={{ mb: 2 }} />
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    For sale and for rent listings
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={async () => {
                    try {
                      await api.post('/market-intelligence/import/property-listings');
                      alert('Property listings imported successfully!');
                      fetchIntegrationStatus();
                    } catch (err: any) {
                      alert('Import failed: ' + err.message);
                    }
                  }}
                >
                  Import Data
                </Button>
              </CardActions>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Yahoo Finance
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Stock market data, REITs, treasury rates, and market indices
                </Typography>
                <Chip label="FREE" color="success" size="small" sx={{ mb: 2 }} />
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    Real-time market data via yfinance API
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={async () => {
                    try {
                      const response = await api.get('/market-intelligence/yfinance/market-summary');
                      if (response.data.error) {
                        alert('Yahoo Finance test: Service returned errors but is functioning with graceful fallbacks');
                      } else {
                        alert('Yahoo Finance connection successful! Market data available.');
                      }
                    } catch (err: any) {
                      alert('Connection test failed: ' + err.message);
                    }
                  }}
                >
                  Test Connection
                </Button>
              </CardActions>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Economics API
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Global economic indicators from Trading Economics (500+ indicators)
                </Typography>
                <Chip label="FREE" color="success" size="small" sx={{ mb: 2 }} />
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    GDP, employment, inflation, housing data
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={async () => {
                    try {
                      const response = await api.get('/market-intelligence/economics/country/united-states/overview');
                      if (response.data.error) {
                        alert('Economics API test: Service returned errors but is functioning with graceful fallbacks');
                      } else {
                        alert('Economics API connection successful! Economic data available.');
                      }
                    } catch (err: any) {
                      alert('Connection test failed: ' + err.message);
                    }
                  }}
                >
                  Test Connection
                </Button>
              </CardActions>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="h6" gutterBottom>
                      Import All Data Sources
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Import sample data from all sources at once
                    </Typography>
                  </Box>
                  <Button
                    variant="contained"
                    onClick={async () => {
                      try {
                        const response = await api.post('/market-intelligence/import/all');
                        alert(`Data imported successfully!\n\nInserted: ${response.data.total_inserted} records\nUpdated: ${response.data.total_updated} records`);
                        fetchIntegrationStatus();
                      } catch (err: any) {
                        alert('Import failed: ' + err.message);
                      }
                    }}
                  >
                    Import All Data
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>

      {/* Setup Instructions */}
      <Paper sx={{ mt: 4, p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Setup Instructions
        </Typography>
        <Typography variant="body2" paragraph>
          To enable integrations, configure API keys in your backend <code>.env</code> file:
        </Typography>
        <Alert severity="info" sx={{ mb: 2 }}>
          <Typography variant="body2">
            <strong>Completely FREE integrations:</strong> Census Bureau, BLS, FRED, Slack, Google Drive, Plaid (sandbox), Stripe (test mode)
          </Typography>
        </Alert>
        <Alert severity="warning">
          <Typography variant="body2">
            <strong>Paid/Limited integrations:</strong> ATTOM Data (paid), Realtor.com (500 requests/month free)
          </Typography>
        </Alert>
      </Paper>
    </Container>
  );
};

export default IntegrationsPage;
