/**
 * SystemSettings Component - System configuration and settings
 *
 * @version 1.1.0
 * @created 2025-11-15
 * @description System-wide configuration, environment settings, and maintenance tools
 */
import React, { useState } from 'react';
import {
  Box,
  Card,
  Typography,
  Stack,
  Grid,
  Button,
  TextField,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Settings as SettingsIcon,
  Save as SaveIcon,
  Refresh as RefreshIcon,
  CloudDownload as BackupIcon,
  Delete as ClearIcon,
  Check as CheckIcon,
  Close as CloseIcon,
  Storage as DatabaseIcon,
  Email as EmailIcon,
  Security as SecurityIcon,
  Notifications as NotificationIcon,
  Speed as PerformanceIcon,
  ViewList as LogIcon,
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

interface DatabaseStat {
  name: string;
  status: 'connected' | 'disconnected';
  size: string;
  tables: number;
  lastBackup: string;
}

interface CacheStat {
  name: string;
  hitRate: number;
  size: string;
  entries: number;
}

interface SystemLog {
  id: string;
  timestamp: string;
  level: 'info' | 'warning' | 'error';
  message: string;
  source: string;
}

export const SystemSettings: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [backupDialogOpen, setBackupDialogOpen] = useState(false);
  const [clearCacheDialogOpen, setClearCacheDialogOpen] = useState(false);

  const [settings, setSettings] = useState({
    siteName: 'Real Estate Dashboard',
    maintenanceMode: false,
    allowRegistration: true,
    requireEmailVerification: true,
    sessionTimeout: 30,
    maxUploadSize: 10,
    enableCache: true,
    enableNotifications: true,
    smtpHost: 'smtp.sendgrid.net',
    smtpPort: 587,
    smtpUser: 'apikey',
    fromEmail: 'noreply@dashboard.com',
  });

  const [databases] = useState<DatabaseStat[]>([
    {
      name: 'PostgreSQL (Primary)',
      status: 'connected',
      size: '2.4 GB',
      tables: 42,
      lastBackup: new Date(Date.now() - 86400000).toISOString(),
    },
    {
      name: 'Redis (Cache)',
      status: 'connected',
      size: '156 MB',
      tables: 1,
      lastBackup: 'N/A',
    },
  ]);

  const [cacheStats] = useState<CacheStat[]>([
    {
      name: 'Application Cache',
      hitRate: 87.5,
      size: '124 MB',
      entries: 15847,
    },
    {
      name: 'Query Cache',
      hitRate: 92.3,
      size: '68 MB',
      entries: 8234,
    },
    {
      name: 'Session Cache',
      hitRate: 95.1,
      size: '32 MB',
      entries: 3421,
    },
  ]);

  const [systemLogs] = useState<SystemLog[]>([
    {
      id: '1',
      timestamp: new Date(Date.now() - 300000).toISOString(),
      level: 'info',
      message: 'Database backup completed successfully',
      source: 'BackupService',
    },
    {
      id: '2',
      timestamp: new Date(Date.now() - 600000).toISOString(),
      level: 'warning',
      message: 'High memory usage detected (78%)',
      source: 'MonitoringService',
    },
    {
      id: '3',
      timestamp: new Date(Date.now() - 900000).toISOString(),
      level: 'info',
      message: 'Cache cleared successfully',
      source: 'CacheService',
    },
    {
      id: '4',
      timestamp: new Date(Date.now() - 1200000).toISOString(),
      level: 'error',
      message: 'Failed to send email notification',
      source: 'EmailService',
    },
    {
      id: '5',
      timestamp: new Date(Date.now() - 1800000).toISOString(),
      level: 'info',
      message: 'User authentication successful',
      source: 'AuthService',
    },
  ]);

  const handleSettingChange = (key: string, value: any) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  const handleSaveSettings = () => {
    console.log('Saving settings:', settings);
  };

  const getLogColor = (level: string) => {
    switch (level) {
      case 'error':
        return designTokens.colors.semantic.error;
      case 'warning':
        return designTokens.colors.semantic.warning;
      case 'info':
        return designTokens.colors.chart.blue;
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
            <SettingsIcon sx={{ fontSize: 28, color: 'white' }} />
          </Box>
          <Box flex={1}>
            <Typography variant="h4" sx={{ fontWeight: designTokens.typography.fontWeight.bold }}>
              System Settings
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Configure system-wide settings and monitor system health
            </Typography>
          </Box>
          <Stack direction="row" spacing={1}>
            <Button
              variant="outlined"
              startIcon={<BackupIcon />}
              sx={{ borderColor: designTokens.colors.workspace.admin, color: designTokens.colors.workspace.admin }}
              onClick={() => setBackupDialogOpen(true)}
            >
              Backup
            </Button>
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              sx={{ background: designTokens.colors.workspace.admin }}
              onClick={handleSaveSettings}
            >
              Save Changes
            </Button>
          </Stack>
        </Stack>
      </Box>

      {/* Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Uptime"
            value="99.8%"
            change="+0.1%"
            trend="up"
            icon={CheckIcon}
            color={designTokens.colors.semantic.success}
            subtext="last 30 days"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Database Size"
            value="2.4 GB"
            change="+120 MB"
            trend="up"
            icon={DatabaseIcon}
            color={designTokens.colors.chart.blue}
            subtext="vs last week"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Cache Hit Rate"
            value="91.6%"
            change="+2.3%"
            trend="up"
            icon={PerformanceIcon}
            color={designTokens.colors.chart.emerald}
            subtext="average across all"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Error Rate"
            value="0.2%"
            change="-0.1%"
            trend="up"
            icon={SecurityIcon}
            color={designTokens.colors.chart.purple}
            subtext="24 hour average"
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
          <Tab label="General" />
          <Tab label="Database" />
          <Tab label="Cache" />
          <Tab label="Email" />
          <Tab label="System Logs" />
        </Tabs>
      </Card>

      {/* Tab Panels */}
      <TabPanel value={activeTab} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 3 }}>
                General Settings
              </Typography>
              <Stack spacing={3}>
                <TextField
                  label="Site Name"
                  value={settings.siteName}
                  onChange={(e) => handleSettingChange('siteName', e.target.value)}
                  fullWidth
                />
                <TextField
                  label="Session Timeout (minutes)"
                  type="number"
                  value={settings.sessionTimeout}
                  onChange={(e) => handleSettingChange('sessionTimeout', parseInt(e.target.value))}
                  fullWidth
                />
                <TextField
                  label="Max Upload Size (MB)"
                  type="number"
                  value={settings.maxUploadSize}
                  onChange={(e) => handleSettingChange('maxUploadSize', parseInt(e.target.value))}
                  fullWidth
                />
              </Stack>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 3 }}>
                System Controls
              </Typography>
              <Stack spacing={2}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.maintenanceMode}
                      onChange={(e) => handleSettingChange('maintenanceMode', e.target.checked)}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant="body2" fontWeight={600}>
                        Maintenance Mode
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Restrict access to admins only
                      </Typography>
                    </Box>
                  }
                />
                <Divider />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.allowRegistration}
                      onChange={(e) => handleSettingChange('allowRegistration', e.target.checked)}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant="body2" fontWeight={600}>
                        Allow Registration
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Allow new users to register
                      </Typography>
                    </Box>
                  }
                />
                <Divider />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.requireEmailVerification}
                      onChange={(e) => handleSettingChange('requireEmailVerification', e.target.checked)}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant="body2" fontWeight={600}>
                        Require Email Verification
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Users must verify their email
                      </Typography>
                    </Box>
                  }
                />
                <Divider />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enableCache}
                      onChange={(e) => handleSettingChange('enableCache', e.target.checked)}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant="body2" fontWeight={600}>
                        Enable Cache
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Cache frequently accessed data
                      </Typography>
                    </Box>
                  }
                />
                <Divider />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enableNotifications}
                      onChange={(e) => handleSettingChange('enableNotifications', e.target.checked)}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant="body2" fontWeight={600}>
                        Enable Notifications
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Send system notifications
                      </Typography>
                    </Box>
                  }
                />
              </Stack>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={activeTab} index={1}>
        <Stack spacing={3}>
          <Alert severity="info">
            Database connection information and statistics. Last backup: {new Date(databases[0].lastBackup).toLocaleString()}
          </Alert>

          {databases.map((db) => (
            <Card key={db.name} sx={{ p: 3 }}>
              <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 3 }}>
                <Box>
                  <Typography variant="h6" sx={{ mb: 0.5 }}>
                    {db.name}
                  </Typography>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <Chip
                      icon={db.status === 'connected' ? <CheckIcon fontSize="small" /> : <CloseIcon fontSize="small" />}
                      label={db.status}
                      size="small"
                      color={db.status === 'connected' ? 'success' : 'error'}
                    />
                  </Stack>
                </Box>
                <Stack direction="row" spacing={1}>
                  <Button size="small" variant="outlined" startIcon={<RefreshIcon />}>
                    Test Connection
                  </Button>
                  <Button size="small" variant="outlined" startIcon={<BackupIcon />}>
                    Backup Now
                  </Button>
                </Stack>
              </Stack>

              <Grid container spacing={3}>
                <Grid item xs={4}>
                  <Typography variant="caption" color="text.secondary">
                    Size
                  </Typography>
                  <Typography variant="h6">{db.size}</Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="caption" color="text.secondary">
                    Tables
                  </Typography>
                  <Typography variant="h6">{db.tables}</Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="caption" color="text.secondary">
                    Last Backup
                  </Typography>
                  <Typography variant="h6">
                    {db.lastBackup !== 'N/A' ? new Date(db.lastBackup).toLocaleDateString() : 'N/A'}
                  </Typography>
                </Grid>
              </Grid>
            </Card>
          ))}
        </Stack>
      </TabPanel>

      <TabPanel value={activeTab} index={2}>
        <Stack spacing={3}>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Alert severity="success" sx={{ flex: 1 }}>
              Cache is operating efficiently with an average hit rate of 91.6%
            </Alert>
            <Button
              variant="outlined"
              color="error"
              startIcon={<ClearIcon />}
              sx={{ ml: 2 }}
              onClick={() => setClearCacheDialogOpen(true)}
            >
              Clear All Cache
            </Button>
          </Stack>

          {cacheStats.map((cache) => (
            <Card key={cache.name} sx={{ p: 3 }}>
              <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 3 }}>
                <Box>
                  <Typography variant="h6">{cache.name}</Typography>
                </Box>
                <Button size="small" variant="outlined" startIcon={<ClearIcon />}>
                  Clear
                </Button>
              </Stack>

              <Grid container spacing={3}>
                <Grid item xs={4}>
                  <Typography variant="caption" color="text.secondary">
                    Hit Rate
                  </Typography>
                  <Typography variant="h6" sx={{ color: designTokens.colors.semantic.success }}>
                    {cache.hitRate}%
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="caption" color="text.secondary">
                    Size
                  </Typography>
                  <Typography variant="h6">{cache.size}</Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="caption" color="text.secondary">
                    Entries
                  </Typography>
                  <Typography variant="h6">{cache.entries.toLocaleString()}</Typography>
                </Grid>
              </Grid>
            </Card>
          ))}
        </Stack>
      </TabPanel>

      <TabPanel value={activeTab} index={3}>
        <Card sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 3 }}>
            SMTP Configuration
          </Typography>
          <Stack spacing={3}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <TextField
                  label="SMTP Host"
                  value={settings.smtpHost}
                  onChange={(e) => handleSettingChange('smtpHost', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="SMTP Port"
                  type="number"
                  value={settings.smtpPort}
                  onChange={(e) => handleSettingChange('smtpPort', parseInt(e.target.value))}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="SMTP User"
                  value={settings.smtpUser}
                  onChange={(e) => handleSettingChange('smtpUser', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="From Email"
                  type="email"
                  value={settings.fromEmail}
                  onChange={(e) => handleSettingChange('fromEmail', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12}>
                <TextField label="SMTP Password" type="password" fullWidth />
              </Grid>
            </Grid>

            <Divider />

            <Stack direction="row" spacing={2}>
              <Button variant="outlined" startIcon={<EmailIcon />}>
                Send Test Email
              </Button>
              <Button variant="outlined" startIcon={<RefreshIcon />}>
                Verify Configuration
              </Button>
            </Stack>
          </Stack>
        </Card>
      </TabPanel>

      <TabPanel value={activeTab} index={4}>
        <Card>
          <List>
            {systemLogs.map((log, index) => (
              <React.Fragment key={log.id}>
                <ListItem>
                  <ListItemIcon>
                    <Box
                      sx={{
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        bgcolor: getLogColor(log.level),
                      }}
                    />
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Stack direction="row" spacing={2} alignItems="center">
                        <Typography variant="body2">{log.message}</Typography>
                        <Chip label={log.level} size="small" sx={{ bgcolor: alphaColor(getLogColor(log.level), 0.1), color: getLogColor(log.level) }} />
                      </Stack>
                    }
                    secondary={
                      <Stack direction="row" spacing={2} sx={{ mt: 0.5 }}>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(log.timestamp).toLocaleString()}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {log.source}
                        </Typography>
                      </Stack>
                    }
                  />
                </ListItem>
                {index < systemLogs.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Card>
      </TabPanel>

      {/* Backup Dialog */}
      <Dialog open={backupDialogOpen} onClose={() => setBackupDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create System Backup</DialogTitle>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 1 }}>
            <Alert severity="info">
              This will create a full backup of the database and system files. The process may take several minutes.
            </Alert>
            <FormControlLabel control={<Switch defaultChecked />} label="Include database" />
            <FormControlLabel control={<Switch defaultChecked />} label="Include uploaded files" />
            <FormControlLabel control={<Switch />} label="Include system logs" />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBackupDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" startIcon={<BackupIcon />}>
            Create Backup
          </Button>
        </DialogActions>
      </Dialog>

      {/* Clear Cache Dialog */}
      <Dialog open={clearCacheDialogOpen} onClose={() => setClearCacheDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Clear All Cache</DialogTitle>
        <DialogContent>
          <Alert severity="warning">
            This will clear all cached data. The system may experience slower performance until the cache is rebuilt.
          </Alert>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setClearCacheDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" color="error" startIcon={<ClearIcon />}>
            Clear Cache
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SystemSettings;
