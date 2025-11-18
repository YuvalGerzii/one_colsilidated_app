/**
 * AuditLog Component - Admin audit trail viewer
 *
 * @version 1.1.0
 * @created 2025-11-15
 * @description Comprehensive audit log viewer with filtering, search, and real-time updates
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  Typography,
  Stack,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  IconButton,
  Chip,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
 Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tooltip,
  alpha,
} from '@mui/material';
import {
  Description as LogIcon,
  FilterList as FilterIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  Visibility as ViewIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Person as UserIcon,
  Computer as SystemIcon,
  Key as KeyIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';
import { designTokens, alphaColor } from '../../theme/designTokens';
import { MetricCard } from '../../components/ui/MetricCard';

interface AuditLogEntry {
  id: string;
  user_email: string | null;
  action: string;
  resource_type: string | null;
  resource_id: string | null;
  description: string | null;
  changes: any;
  ip_address: string | null;
  timestamp: string;
  success: string;
  error_message: string | null;
}

export const AuditLog: React.FC = () => {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [totalLogs, setTotalLogs] = useState(0);
  const [filterAction, setFilterAction] = useState('all');
  const [filterUser, setFilterUser] = useState('');
  const [filterSuccess, setFilterSuccess] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLog, setSelectedLog] = useState<AuditLogEntry | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);

  // Mock data for demonstration
  const mockLogs: AuditLogEntry[] = [
    {
      id: '1',
      user_email: 'admin@example.com',
      action: 'login',
      resource_type: null,
      resource_id: null,
      description: 'User logged in successfully',
      changes: null,
      ip_address: '192.168.1.100',
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      success: 'success',
      error_message: null,
    },
    {
      id: '2',
      user_email: 'john.doe@example.com',
      action: 'update',
      resource_type: 'property',
      resource_id: 'prop-123',
      description: 'Updated property status',
      changes: { status: { old: 'active', new: 'sold' } },
      ip_address: '192.168.1.101',
      timestamp: new Date(Date.now() - 7200000).toISOString(),
      success: 'success',
      error_message: null,
    },
    {
      id: '3',
      user_email: 'admin@example.com',
      action: 'user_create',
      resource_type: 'user',
      resource_id: 'user-456',
      description: 'Created new user account',
      changes: { email: 'newuser@example.com', role: 'viewer' },
      ip_address: '192.168.1.100',
      timestamp: new Date(Date.now() - 10800000).toISOString(),
      success: 'success',
      error_message: null,
    },
    {
      id: '4',
      user_email: 'system',
      action: 'api_key_generated',
      resource_type: 'api_key',
      resource_id: 'key-789',
      description: 'Generated new API key for integration',
      changes: { name: 'Third Party Integration' },
      ip_address: null,
      timestamp: new Date(Date.now() - 14400000).toISOString(),
      success: 'success',
      error_message: null,
    },
    {
      id: '5',
      user_email: 'jane.smith@example.com',
      action: 'login_failed',
      resource_type: null,
      resource_id: null,
      description: 'Failed login attempt - invalid password',
      changes: null,
      ip_address: '192.168.1.102',
      timestamp: new Date(Date.now() - 18000000).toISOString(),
      success: 'failure',
      error_message: 'Invalid credentials',
    },
    {
      id: '6',
      user_email: 'admin@example.com',
      action: 'permission_change',
      resource_type: 'user',
      resource_id: 'user-456',
      description: 'Updated user permissions',
      changes: { role: { old: 'viewer', new: 'editor' } },
      ip_address: '192.168.1.100',
      timestamp: new Date(Date.now() - 21600000).toISOString(),
      success: 'success',
      error_message: null,
    },
  ];

  useEffect(() => {
    loadAuditLogs();
  }, [page, rowsPerPage, filterAction, filterUser, filterSuccess]);

  const loadAuditLogs = async () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      let filteredLogs = [...mockLogs];

      if (filterAction !== 'all') {
        filteredLogs = filteredLogs.filter(log => log.action === filterAction);
      }
      if (filterUser) {
        filteredLogs = filteredLogs.filter(log =>
          log.user_email?.toLowerCase().includes(filterUser.toLowerCase())
        );
      }
      if (filterSuccess !== 'all') {
        filteredLogs = filteredLogs.filter(log => log.success === filterSuccess);
      }
      if (searchTerm) {
        filteredLogs = filteredLogs.filter(log =>
          log.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          log.resource_type?.toLowerCase().includes(searchTerm.toLowerCase())
        );
      }

      setTotalLogs(filteredLogs.length);
      setLogs(filteredLogs.slice(page * rowsPerPage, (page + 1) * rowsPerPage));
      setLoading(false);
    }, 500);
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleViewDetails = (log: AuditLogEntry) => {
    setSelectedLog(log);
    setDetailsOpen(true);
  };

  const handleExport = () => {
    const csv = [
      ['Timestamp', 'User', 'Action', 'Resource', 'Status', 'IP Address'],
      ...logs.map(log => [
        new Date(log.timestamp).toLocaleString(),
        log.user_email || 'System',
        log.action,
        log.resource_type ? `${log.resource_type}:${log.resource_id}` : '-',
        log.success,
        log.ip_address || '-',
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `audit-log-${new Date().toISOString()}.csv`;
    a.click();
  };

  const getActionColor = (action: string) => {
    const colorMap: Record<string, string> = {
      login: designTokens.colors.semantic.success,
      logout: designTokens.colors.chart.blue,
      login_failed: designTokens.colors.semantic.error,
      create: designTokens.colors.chart.emerald,
      update: designTokens.colors.chart.amber,
      delete: designTokens.colors.semantic.error,
      user_create: designTokens.colors.chart.purple,
      permission_change: designTokens.colors.chart.pink,
      api_key_generated: designTokens.colors.chart.cyan,
    };
    return colorMap[action] || designTokens.colors.chart.blue;
  };

  const getActionIcon = (action: string) => {
    if (action.includes('user')) return <UserIcon fontSize="small" />;
    if (action.includes('api')) return <KeyIcon fontSize="small" />;
    if (action.includes('permission')) return <SecurityIcon fontSize="small" />;
    return <LogIcon fontSize="small" />;
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
            <LogIcon sx={{ fontSize: 28, color: 'white' }} />
          </Box>
          <Box flex={1}>
            <Typography variant="h4" sx={{ fontWeight: designTokens.typography.fontWeight.bold }}>
              Audit Log
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Track all system changes and user actions
            </Typography>
          </Box>
          <Stack direction="row" spacing={1}>
            <Tooltip title="Export to CSV">
              <IconButton onClick={handleExport} color="primary">
                <DownloadIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Refresh">
              <IconButton onClick={loadAuditLogs} color="primary">
                <RefreshIcon />
              </IconButton>
            </Tooltip>
          </Stack>
        </Stack>
      </Box>

      {/* Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Total Actions"
            value={totalLogs.toLocaleString()}
            change="+12%"
            trend="up"
            icon={LogIcon}
            color={designTokens.colors.chart.blue}
            subtext="last 24h"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Successful"
            value={logs.filter(l => l.success === 'success').length}
            change="+8%"
            trend="up"
            icon={SuccessIcon}
            color={designTokens.colors.semantic.success}
            subtext="success rate: 98%"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Failed Actions"
            value={logs.filter(l => l.success === 'failure').length}
            change="-2%"
            trend="down"
            icon={ErrorIcon}
            color={designTokens.colors.semantic.error}
            subtext="trending down"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Active Users"
            value={new Set(logs.filter(l => l.user_email).map(l => l.user_email)).size}
            change="+5"
            trend="up"
            icon={UserIcon}
            color={designTokens.colors.chart.purple}
            subtext="unique users"
          />
        </Grid>
      </Grid>

      {/* Filters */}
      <Card sx={{ mb: 3, p: 3 }}>
        <Stack direction="row" spacing={2} alignItems="center" flexWrap="wrap">
          <FilterIcon color="action" />
          <TextField
            size="small"
            placeholder="Search description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{ minWidth: 200 }}
          />
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Action</InputLabel>
            <Select
              value={filterAction}
              label="Action"
              onChange={(e) => setFilterAction(e.target.value)}
            >
              <MenuItem value="all">All Actions</MenuItem>
              <MenuItem value="login">Login</MenuItem>
              <MenuItem value="logout">Logout</MenuItem>
              <MenuItem value="create">Create</MenuItem>
              <MenuItem value="update">Update</MenuItem>
              <MenuItem value="delete">Delete</MenuItem>
              <MenuItem value="user_create">User Create</MenuItem>
              <MenuItem value="permission_change">Permission Change</MenuItem>
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={filterSuccess}
              label="Status"
              onChange={(e) => setFilterSuccess(e.target.value)}
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="success">Success</MenuItem>
              <MenuItem value="failure">Failure</MenuItem>
            </Select>
          </FormControl>
          <TextField
            size="small"
            placeholder="Filter by user..."
            value={filterUser}
            onChange={(e) => setFilterUser(e.target.value)}
            sx={{ minWidth: 200 }}
          />
          <Button
            variant="outlined"
            onClick={() => {
              setFilterAction('all');
              setFilterUser('');
              setFilterSuccess('all');
              setSearchTerm('');
            }}
          >
            Clear Filters
          </Button>
        </Stack>
      </Card>

      {/* Table */}
      <Card>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Timestamp</TableCell>
                <TableCell>User</TableCell>
                <TableCell>Action</TableCell>
                <TableCell>Resource</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>IP Address</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {logs.map((log) => (
                <TableRow key={log.id} hover>
                  <TableCell>
                    <Typography variant="body2">
                      {new Date(log.timestamp).toLocaleString()}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Stack direction="row" spacing={1} alignItems="center">
                      {log.user_email === 'system' ? <SystemIcon fontSize="small" /> : <UserIcon fontSize="small" />}
                      <Typography variant="body2">{log.user_email || 'System'}</Typography>
                    </Stack>
                  </TableCell>
                  <TableCell>
                    <Chip
                      icon={getActionIcon(log.action)}
                      label={log.action.replace('_', ' ')}
                      size="small"
                      sx={{
                        background: alphaColor(getActionColor(log.action), 0.1),
                        color: getActionColor(log.action),
                        fontWeight: 600,
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {log.resource_type ? `${log.resource_type}:${log.resource_id}` : '-'}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" noWrap sx={{ maxWidth: 300 }}>
                      {log.description || '-'}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontFamily="monospace">
                      {log.ip_address || '-'}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      icon={log.success === 'success' ? <SuccessIcon fontSize="small" /> : <ErrorIcon fontSize="small" />}
                      label={log.success}
                      size="small"
                      color={log.success === 'success' ? 'success' : 'error'}
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="View Details">
                      <IconButton size="small" onClick={() => handleViewDetails(log)}>
                        <ViewIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[10, 25, 50, 100]}
          component="div"
          count={totalLogs}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Card>

      {/* Details Dialog */}
      <Dialog open={detailsOpen} onClose={() => setDetailsOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Audit Log Details</DialogTitle>
        <DialogContent>
          {selectedLog && (
            <Stack spacing={2}>
              <Box>
                <Typography variant="caption" color="text.secondary">Timestamp</Typography>
                <Typography variant="body1">{new Date(selectedLog.timestamp).toLocaleString()}</Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">User</Typography>
                <Typography variant="body1">{selectedLog.user_email || 'System'}</Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">Action</Typography>
                <Typography variant="body1">{selectedLog.action}</Typography>
              </Box>
              {selectedLog.resource_type && (
                <Box>
                  <Typography variant="caption" color="text.secondary">Resource</Typography>
                  <Typography variant="body1">
                    {selectedLog.resource_type}:{selectedLog.resource_id}
                  </Typography>
                </Box>
              )}
              <Box>
                <Typography variant="caption" color="text.secondary">Description</Typography>
                <Typography variant="body1">{selectedLog.description}</Typography>
              </Box>
              {selectedLog.changes && (
                <Box>
                  <Typography variant="caption" color="text.secondary">Changes</Typography>
                  <Box
                    component="pre"
                    sx={{
                      p: 2,
                      background: alphaColor(designTokens.colors.chart.blue, 0.05),
                      borderRadius: 1,
                      overflow: 'auto',
                      fontFamily: 'monospace',
                      fontSize: '0.875rem',
                    }}
                  >
                    {JSON.stringify(selectedLog.changes, null, 2)}
                  </Box>
                </Box>
              )}
              <Box>
                <Typography variant="caption" color="text.secondary">IP Address</Typography>
                <Typography variant="body1" fontFamily="monospace">
                  {selectedLog.ip_address || 'N/A'}
                </Typography>
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">Status</Typography>
                <Chip
                  label={selectedLog.success}
                  size="small"
                  color={selectedLog.success === 'success' ? 'success' : 'error'}
                />
              </Box>
              {selectedLog.error_message && (
                <Box>
                  <Typography variant="caption" color="text.secondary">Error Message</Typography>
                  <Typography variant="body1" color="error">{selectedLog.error_message}</Typography>
                </Box>
              )}
            </Stack>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailsOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AuditLog;
