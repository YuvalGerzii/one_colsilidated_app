/**
 * APIIntegrations Component - API and system health monitoring
 *
 * @version 1.1.0
 * @created 2025-11-15
 * @description Manage API keys, integrations, and monitor system health
 */
import React, { useState } from 'react';
import {
  Box,
  Card,
  Typography,
  Stack,
  Grid,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Switch,
  FormControlLabel,
  Tabs,
  Tab,
  LinearProgress,
  Tooltip,
  Alert,
} from '@mui/material';
import {
  Api as ApiIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  ContentCopy as CopyIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  Storage as StorageIcon,
  Speed as SpeedIcon,
  Memory as MemoryIcon,
  CloudQueue as CloudIcon,
} from '@mui/icons-material';
import { designTokens, alphaColor } from '../../theme/designTokens';
import { MetricCard } from '../../components/ui/MetricCard';

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

interface APIKey {
  id: string;
  name: string;
  key: string;
  status: 'active' | 'inactive';
  lastUsed: string;
  requests: number;
  createdAt: string;
}

interface Integration {
  id: string;
  name: string;
  type: string;
  status: 'connected' | 'disconnected' | 'error';
  lastSync: string;
  apiCalls: number;
}

interface SystemHealth {
  metric: string;
  value: number;
  status: 'healthy' | 'warning' | 'critical';
  threshold: number;
}

export const APIIntegrations: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [showKey, setShowKey] = useState<Record<string, boolean>>({});

  const [apiKeys] = useState<APIKey[]>([
    {
      id: '1',
      name: 'Production API',
      key: 'sk_live_xxxxxxxxxxxxxxxxxxxxx',
      status: 'active',
      lastUsed: new Date(Date.now() - 3600000).toISOString(),
      requests: 12847,
      createdAt: new Date(Date.now() - 86400000 * 90).toISOString(),
    },
    {
      id: '2',
      name: 'Development API',
      key: 'sk_test_xxxxxxxxxxxxxxxxxxxxx',
      status: 'active',
      lastUsed: new Date(Date.now() - 86400000).toISOString(),
      requests: 3421,
      createdAt: new Date(Date.now() - 86400000 * 30).toISOString(),
    },
    {
      id: '3',
      name: 'Legacy API',
      key: 'sk_live_yyyyyyyyyyyyyyyyyyyyy',
      status: 'inactive',
      lastUsed: new Date(Date.now() - 86400000 * 30).toISOString(),
      requests: 0,
      createdAt: new Date(Date.now() - 86400000 * 180).toISOString(),
    },
  ]);

  const [integrations] = useState<Integration[]>([
    {
      id: '1',
      name: 'Stripe Payments',
      type: 'Payment Gateway',
      status: 'connected',
      lastSync: new Date(Date.now() - 1800000).toISOString(),
      apiCalls: 1247,
    },
    {
      id: '2',
      name: 'SendGrid Email',
      type: 'Email Service',
      status: 'connected',
      lastSync: new Date(Date.now() - 3600000).toISOString(),
      apiCalls: 5432,
    },
    {
      id: '3',
      name: 'AWS S3 Storage',
      type: 'Cloud Storage',
      status: 'connected',
      lastSync: new Date(Date.now() - 900000).toISOString(),
      apiCalls: 8921,
    },
    {
      id: '4',
      name: 'Google Maps',
      type: 'Mapping Service',
      status: 'error',
      lastSync: new Date(Date.now() - 86400000).toISOString(),
      apiCalls: 0,
    },
  ]);

  const [systemHealth] = useState<SystemHealth[]>([
    { metric: 'CPU Usage', value: 45, status: 'healthy', threshold: 80 },
    { metric: 'Memory Usage', value: 68, status: 'healthy', threshold: 85 },
    { metric: 'Disk Space', value: 72, status: 'warning', threshold: 90 },
    { metric: 'Response Time', value: 120, status: 'healthy', threshold: 500 },
    { metric: 'Error Rate', value: 0.5, status: 'healthy', threshold: 5 },
    { metric: 'Active Connections', value: 247, status: 'healthy', threshold: 1000 },
  ]);

  const handleCopyKey = (key: string) => {
    navigator.clipboard.writeText(key);
  };

  const toggleKeyVisibility = (id: string) => {
    setShowKey((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
      case 'connected':
      case 'healthy':
        return designTokens.colors.semantic.success;
      case 'warning':
        return designTokens.colors.semantic.warning;
      case 'error':
      case 'critical':
      case 'disconnected':
        return designTokens.colors.semantic.error;
      default:
        return designTokens.colors.chart.blue;
    }
  };

  const getHealthColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return designTokens.colors.semantic.success;
      case 'warning':
        return designTokens.colors.semantic.warning;
      case 'critical':
        return designTokens.colors.semantic.error;
      default:
        return designTokens.colors.chart.blue;
    }
  };

  return (
    <Box sx={{ p: { xs: 3, md: 4 } }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
          <Box
            sx={{
              width: 56,
              height: 56,
              borderRadius: designTokens.radius.lg,
              background: designTokens.colors.workspace.admin,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <ApiIcon sx={{ fontSize: 28, color: 'white' }} />
          </Box>
          <Box flex={1}>
            <Typography variant="h4" sx={{ fontWeight: designTokens.typography.fontWeight.bold }}>
              API & Integrations
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage API keys, integrations, and monitor system health
            </Typography>
          </Box>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            sx={{ borderColor: designTokens.colors.workspace.admin, color: designTokens.colors.workspace.admin }}
          >
            Refresh
          </Button>
        </Stack>
      </Box>

      {/* Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Total API Calls"
            value="16.3K"
            change="+12.5%"
            trend="up"
            icon={ApiIcon}
            color={designTokens.colors.chart.blue}
            subtext="last 24 hours"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Active Keys"
            value={apiKeys.filter((k) => k.status === 'active').length}
            change="+1"
            trend="up"
            icon={CheckIcon}
            color={designTokens.colors.semantic.success}
            subtext="currently active"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Connected Services"
            value={integrations.filter((i) => i.status === 'connected').length}
            change="0"
            trend="neutral"
            icon={CloudIcon}
            color={designTokens.colors.chart.purple}
            subtext="out of 4 total"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Avg Response Time"
            value="120ms"
            change="-15ms"
            trend="up"
            icon={SpeedIcon}
            color={designTokens.colors.chart.emerald}
            subtext="vs yesterday"
          />
        </Grid>
      </Grid>

      {/* Tabs */}
      <Card sx={{ mb: 4 }}>
        <Tabs
          value={activeTab}
          onChange={(e, v) => setActiveTab(v)}
          sx={{
            borderBottom: 1,
            borderColor: 'divider',
            px: 2,
          }}
        >
          <Tab label="API Keys" />
          <Tab label="Integrations" />
          <Tab label="System Health" />
        </Tabs>
      </Card>

      {/* Tab Panels */}
      <TabPanel value={activeTab} index={0}>
        <Stack spacing={2} sx={{ mb: 3 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">API Keys</Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              sx={{ background: designTokens.colors.workspace.admin }}
              onClick={() => setDialogOpen(true)}
            >
              Create Key
            </Button>
          </Stack>
        </Stack>

        <Card>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>API Key</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Last Used</TableCell>
                  <TableCell>Requests</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {apiKeys.map((key) => (
                  <TableRow key={key.id} hover>
                    <TableCell>
                      <Typography variant="body2" fontWeight={600}>
                        {key.name}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Stack direction="row" spacing={1} alignItems="center">
                        <Typography variant="body2" fontFamily="monospace">
                          {showKey[key.id] ? key.key : '••••••••••••••••••••••••'}
                        </Typography>
                        <Tooltip title={showKey[key.id] ? 'Hide' : 'Show'}>
                          <IconButton size="small" onClick={() => toggleKeyVisibility(key.id)}>
                            {showKey[key.id] ? (
                              <VisibilityOffIcon fontSize="small" />
                            ) : (
                              <VisibilityIcon fontSize="small" />
                            )}
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Copy">
                          <IconButton size="small" onClick={() => handleCopyKey(key.key)}>
                            <CopyIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </Stack>
                    </TableCell>
                    <TableCell>
                      <Chip
                        icon={
                          key.status === 'active' ? (
                            <CheckIcon fontSize="small" />
                          ) : (
                            <ErrorIcon fontSize="small" />
                          )
                        }
                        label={key.status}
                        size="small"
                        color={key.status === 'active' ? 'success' : 'default'}
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {new Date(key.lastUsed).toLocaleString()}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{key.requests.toLocaleString()}</Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {new Date(key.createdAt).toLocaleDateString()}
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Tooltip title="Edit">
                        <IconButton size="small">
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Delete">
                        <IconButton size="small" color="error">
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Card>
      </TabPanel>

      <TabPanel value={activeTab} index={1}>
        <Stack spacing={2} sx={{ mb: 3 }}>
          <Typography variant="h6">Third-Party Integrations</Typography>
          <Alert severity="info">
            Manage external service integrations and monitor their health status
          </Alert>
        </Stack>

        <Grid container spacing={3}>
          {integrations.map((integration) => (
            <Grid item xs={12} md={6} key={integration.id}>
              <Card sx={{ p: 3 }}>
                <Stack spacing={2}>
                  <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                    <Box>
                      <Typography variant="h6" sx={{ mb: 0.5 }}>
                        {integration.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {integration.type}
                      </Typography>
                    </Box>
                    <Chip
                      icon={
                        integration.status === 'connected' ? (
                          <CheckIcon fontSize="small" />
                        ) : (
                          <ErrorIcon fontSize="small" />
                        )
                      }
                      label={integration.status}
                      size="small"
                      sx={{
                        bgcolor: alphaColor(getStatusColor(integration.status), 0.1),
                        color: getStatusColor(integration.status),
                        borderColor: getStatusColor(integration.status),
                      }}
                    />
                  </Stack>

                  <Stack direction="row" spacing={4}>
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Last Sync
                      </Typography>
                      <Typography variant="body2" fontWeight={600}>
                        {new Date(integration.lastSync).toLocaleString()}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        API Calls (24h)
                      </Typography>
                      <Typography variant="body2" fontWeight={600}>
                        {integration.apiCalls.toLocaleString()}
                      </Typography>
                    </Box>
                  </Stack>

                  <Stack direction="row" spacing={1}>
                    <Button size="small" variant="outlined" startIcon={<RefreshIcon />}>
                      Test Connection
                    </Button>
                    <Button size="small" variant="outlined" startIcon={<EditIcon />}>
                      Configure
                    </Button>
                  </Stack>
                </Stack>
              </Card>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      <TabPanel value={activeTab} index={2}>
        <Stack spacing={2} sx={{ mb: 3 }}>
          <Typography variant="h6">System Health Metrics</Typography>
          <Alert severity="success">All systems operational</Alert>
        </Stack>

        <Grid container spacing={3}>
          {systemHealth.map((health) => (
            <Grid item xs={12} md={6} key={health.metric}>
              <Card sx={{ p: 3 }}>
                <Stack spacing={2}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Typography variant="body1" fontWeight={600}>
                      {health.metric}
                    </Typography>
                    <Chip
                      label={health.status}
                      size="small"
                      sx={{
                        bgcolor: alphaColor(getHealthColor(health.status), 0.1),
                        color: getHealthColor(health.status),
                        borderColor: getHealthColor(health.status),
                      }}
                    />
                  </Stack>

                  <Box>
                    <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
                      <Typography variant="h4" sx={{ color: getHealthColor(health.status) }}>
                        {health.value}
                        {health.metric.includes('Usage') || health.metric.includes('Rate') ? '%' : health.metric.includes('Time') ? 'ms' : ''}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Threshold: {health.threshold}
                        {health.metric.includes('Usage') || health.metric.includes('Rate') ? '%' : health.metric.includes('Time') ? 'ms' : ''}
                      </Typography>
                    </Stack>
                    <LinearProgress
                      variant="determinate"
                      value={(health.value / health.threshold) * 100}
                      sx={{
                        height: 8,
                        borderRadius: 1,
                        backgroundColor: alphaColor(getHealthColor(health.status), 0.1),
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: getHealthColor(health.status),
                        },
                      }}
                    />
                  </Box>
                </Stack>
              </Card>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      {/* Create API Key Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create API Key</DialogTitle>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 1 }}>
            <TextField label="Key Name" fullWidth placeholder="e.g., Production API" />
            <TextField
              label="Description"
              fullWidth
              multiline
              rows={3}
              placeholder="Brief description of what this key is used for"
            />
            <FormControlLabel control={<Switch defaultChecked />} label="Active" />
            <Alert severity="warning">
              The API key will be shown only once after creation. Make sure to copy and store it
              securely.
            </Alert>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button variant="contained">Create Key</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default APIIntegrations;
