import React, { useState, useMemo } from 'react';
import {
  Box,
  Typography,
  Badge,
  Chip,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Collapse,
  Tabs,
  Tab,
  Button,
  Tooltip,
  Divider,
  Alert as MuiAlert,
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  CheckCircle,
  ExpandMore,
  ExpandLess,
  Notifications,
  TrendingUp,
  AttachMoney,
  Build,
  Gavel,
  Assessment,
  FilterList,
  Close,
} from '@mui/icons-material';
import { GlassCard, GlassMetricCard, MicroInteraction } from '../ui/GlassComponents';

// Alert types matching backend
interface Alert {
  id?: string;
  property_id?: number;
  property_name?: string;
  category: 'financial' | 'operational' | 'market' | 'compliance' | 'opportunity' | 'predictive';
  severity: 'info' | 'warning' | 'error' | 'critical';
  title: string;
  message: string;
  metric_name?: string;
  current_value?: number;
  expected_value?: number;
  threshold?: number;
  deviation_percentage?: number;
  timestamp: string | Date;
  resolved: boolean;
  action_items?: string[];
}

interface AlertsPanelProps {
  alerts?: Alert[];
  onResolveAlert?: (alertId: string) => void;
  onDismissAlert?: (alertId: string) => void;
}

const AlertsPanel: React.FC<AlertsPanelProps> = ({
  alerts = [],
  onResolveAlert,
  onDismissAlert,
}) => {
  const [activeTab, setActiveTab] = useState(0);
  const [expandedAlerts, setExpandedAlerts] = useState<Set<string>>(new Set());
  const [filterSeverity, setFilterSeverity] = useState<string | null>(null);

  // Sample data if no alerts provided
  const sampleAlerts: Alert[] = alerts.length > 0 ? alerts : [
    {
      id: '1',
      property_id: 101,
      property_name: 'Oak Street Apartments',
      category: 'operational',
      severity: 'warning',
      title: 'Vacancy Rate Spike Detected',
      message: 'Vacancy rate of 15.0% is 50.0% higher than 3-month average of 10.0%',
      metric_name: 'vacancy_rate',
      current_value: 0.15,
      expected_value: 0.10,
      deviation_percentage: 50.0,
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
      resolved: false,
      action_items: [
        'Investigate recent tenant turnover patterns',
        'Review lease renewal strategies',
        'Conduct market analysis for competitive positioning'
      ]
    },
    {
      id: '2',
      property_id: 102,
      property_name: 'Maple Plaza',
      category: 'financial',
      severity: 'error',
      title: 'Significant NOI Decline',
      message: 'NOI of $85,000 has declined 12.0% from average of $95,000',
      metric_name: 'noi',
      current_value: 85000,
      expected_value: 95000,
      deviation_percentage: -12.0,
      timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
      resolved: false,
      action_items: [
        'Conduct detailed income and expense analysis',
        'Review property management effectiveness',
        'Develop action plan to restore NOI',
        'Consider property repositioning strategy'
      ]
    },
    {
      id: '3',
      property_id: 103,
      property_name: 'Pine Ridge Condos',
      category: 'opportunity',
      severity: 'info',
      title: 'Value-Add Opportunity Identified',
      message: 'Market rent of $2,500 is 18.0% higher than current rent of $2,100. Potential additional revenue: $240,000/year',
      metric_name: 'rent_gap',
      current_value: 2100,
      expected_value: 2500,
      deviation_percentage: 18.0,
      timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
      resolved: false,
      action_items: [
        'Conduct unit renovation cost-benefit analysis',
        'Develop phased renovation plan',
        'Model pro forma with upgraded units',
        'Assess financing options for improvements'
      ]
    },
    {
      id: '4',
      property_id: 104,
      property_name: 'Cedar Commons',
      category: 'financial',
      severity: 'critical',
      title: 'Low Debt Service Coverage Ratio',
      message: 'DSCR of 0.98x is below minimum threshold of 1.25x',
      metric_name: 'dscr',
      current_value: 0.98,
      threshold: 1.25,
      timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
      resolved: false,
      action_items: [
        'Review debt structure and refinancing options',
        'Implement revenue enhancement initiatives',
        'Reduce operating expenses where possible',
        'Consider additional equity injection if needed'
      ]
    },
    {
      id: '5',
      property_id: 105,
      property_name: 'Elm Tower',
      category: 'operational',
      severity: 'warning',
      title: 'High Maintenance Costs',
      message: 'Maintenance costs represent 18.0% of revenue, exceeding 15.0% threshold',
      metric_name: 'maintenance_ratio',
      current_value: 0.18,
      threshold: 0.15,
      timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
      resolved: false,
      action_items: [
        'Analyze maintenance work orders for patterns',
        'Consider preventive maintenance program',
        'Evaluate age of major building systems',
        'Plan capital improvements if needed'
      ]
    }
  ];

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <Error sx={{ color: '#d32f2f' }} />;
      case 'error': return <Error sx={{ color: '#f44336' }} />;
      case 'warning': return <Warning sx={{ color: '#ff9800' }} />;
      case 'info': return <Info sx={{ color: '#2196f3' }} />;
      default: return <Info />;
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'financial': return <AttachMoney />;
      case 'operational': return <Build />;
      case 'market': return <TrendingUp />;
      case 'compliance': return <Gavel />;
      case 'opportunity': return <TrendingUp />;
      case 'predictive': return <Assessment />;
      default: return <Info />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'error';
      case 'error': return 'error';
      case 'warning': return 'warning';
      case 'info': return 'info';
      default: return 'default';
    }
  };

  const toggleAlert = (alertId: string) => {
    setExpandedAlerts(prev => {
      const newSet = new Set(prev);
      if (newSet.has(alertId)) {
        newSet.delete(alertId);
      } else {
        newSet.add(alertId);
      }
      return newSet;
    });
  };

  const filteredAlerts = useMemo(() => {
    let filtered = sampleAlerts;

    // Filter by tab (category)
    if (activeTab === 1) filtered = filtered.filter(a => a.category === 'financial');
    else if (activeTab === 2) filtered = filtered.filter(a => a.category === 'operational');
    else if (activeTab === 3) filtered = filtered.filter(a => a.category === 'opportunity');

    // Filter by severity
    if (filterSeverity) filtered = filtered.filter(a => a.severity === filterSeverity);

    // Sort by severity (critical first) and timestamp (newest first)
    const severityOrder = { critical: 4, error: 3, warning: 2, info: 1 };
    return filtered.sort((a, b) => {
      const severityDiff = (severityOrder[b.severity as keyof typeof severityOrder] || 0) - (severityOrder[a.severity as keyof typeof severityOrder] || 0);
      if (severityDiff !== 0) return severityDiff;
      return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
    });
  }, [sampleAlerts, activeTab, filterSeverity]);

  const alertCounts = useMemo(() => {
    return {
      total: sampleAlerts.length,
      critical: sampleAlerts.filter(a => a.severity === 'critical').length,
      error: sampleAlerts.filter(a => a.severity === 'error').length,
      warning: sampleAlerts.filter(a => a.severity === 'warning').length,
      info: sampleAlerts.filter(a => a.severity === 'info').length,
      financial: sampleAlerts.filter(a => a.category === 'financial').length,
      operational: sampleAlerts.filter(a => a.category === 'operational').length,
      opportunity: sampleAlerts.filter(a => a.category === 'opportunity').length,
    };
  }, [sampleAlerts]);

  const formatValue = (value: number | undefined, metricName?: string): string => {
    if (value === undefined) return 'N/A';
    if (metricName?.includes('rate') || metricName?.includes('ratio')) {
      return `${(value * 100).toFixed(1)}%`;
    }
    if (metricName?.includes('amount') || metricName?.includes('value') || value > 100) {
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);
    }
    return value.toFixed(2);
  };

  const formatTimestamp = (timestamp: string | Date): string => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = diffMs / (1000 * 60 * 60);

    if (diffHours < 1) {
      const diffMinutes = Math.floor(diffMs / (1000 * 60));
      return `${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      return `${Math.floor(diffHours)} hour${Math.floor(diffHours) !== 1 ? 's' : ''} ago`;
    } else {
      const diffDays = Math.floor(diffHours / 24);
      return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
          <Notifications />
          Smart Alerts
          <Badge badgeContent={alertCounts.critical + alertCounts.error} color="error" sx={{ ml: 2 }}>
            <span />
          </Badge>
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Filter by severity">
            <Button
              size="small"
              startIcon={<FilterList />}
              onClick={() => setFilterSeverity(filterSeverity ? null : 'critical')}
            >
              Filter
            </Button>
          </Tooltip>
        </Box>
      </Box>

      {/* Summary Cards */}
      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 2, mb: 3 }}>
        <MicroInteraction variant="lift">
          <GlassMetricCard sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="caption" color="text.secondary">Critical</Typography>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'error.main' }}>
                  {alertCounts.critical}
                </Typography>
              </Box>
              <Error sx={{ fontSize: 40, color: 'error.main', opacity: 0.3 }} />
            </Box>
          </GlassMetricCard>
        </MicroInteraction>

        <MicroInteraction variant="lift">
          <GlassMetricCard sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="caption" color="text.secondary">Errors</Typography>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'error.main' }}>
                  {alertCounts.error}
                </Typography>
              </Box>
              <Error sx={{ fontSize: 40, color: 'error.main', opacity: 0.3 }} />
            </Box>
          </GlassMetricCard>
        </MicroInteraction>

        <MicroInteraction variant="lift">
          <GlassMetricCard sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="caption" color="text.secondary">Warnings</Typography>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'warning.main' }}>
                  {alertCounts.warning}
                </Typography>
              </Box>
              <Warning sx={{ fontSize: 40, color: 'warning.main', opacity: 0.3 }} />
            </Box>
          </GlassMetricCard>
        </MicroInteraction>

        <MicroInteraction variant="lift">
          <GlassMetricCard sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="caption" color="text.secondary">Opportunities</Typography>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'success.main' }}>
                  {alertCounts.opportunity}
                </Typography>
              </Box>
              <TrendingUp sx={{ fontSize: 40, color: 'success.main', opacity: 0.3 }} />
            </Box>
          </GlassMetricCard>
        </MicroInteraction>
      </Box>

      {/* Tabs */}
      <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)} sx={{ mb: 2 }}>
        <Tab label={`All (${alertCounts.total})`} />
        <Tab label={`Financial (${alertCounts.financial})`} />
        <Tab label={`Operational (${alertCounts.operational})`} />
        <Tab label={`Opportunities (${alertCounts.opportunity})`} />
      </Tabs>

      {/* Alerts List */}
      <GlassCard>
        <List sx={{ p: 0 }}>
          {filteredAlerts.length === 0 ? (
            <Box sx={{ p: 4, textAlign: 'center' }}>
              <CheckCircle sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                No alerts in this category
              </Typography>
            </Box>
          ) : (
            filteredAlerts.map((alert, index) => (
              <React.Fragment key={alert.id || index}>
                <ListItem
                  sx={{
                    cursor: 'pointer',
                    '&:hover': { bgcolor: 'action.hover' },
                    borderLeft: `4px solid`,
                    borderColor: `${getSeverityColor(alert.severity)}.main`,
                  }}
                  onClick={() => toggleAlert(alert.id || String(index))}
                >
                  <ListItemIcon>
                    {getSeverityIcon(alert.severity)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          {alert.title}
                        </Typography>
                        <Chip
                          label={alert.category}
                          size="small"
                          icon={getCategoryIcon(alert.category)}
                          variant="outlined"
                        />
                        {alert.property_name && (
                          <Chip
                            label={alert.property_name}
                            size="small"
                            color="primary"
                            variant="outlined"
                          />
                        )}
                      </Box>
                    }
                    secondary={
                      <Box sx={{ mt: 0.5 }}>
                        <Typography variant="body2" color="text.secondary">
                          {alert.message}
                        </Typography>
                        <Typography variant="caption" color="text.disabled" sx={{ mt: 0.5, display: 'block' }}>
                          {formatTimestamp(alert.timestamp)}
                        </Typography>
                      </Box>
                    }
                  />
                  <IconButton size="small">
                    {expandedAlerts.has(alert.id || String(index)) ? <ExpandLess /> : <ExpandMore />}
                  </IconButton>
                </ListItem>

                <Collapse in={expandedAlerts.has(alert.id || String(index))} timeout="auto" unmountOnExit>
                  <Box sx={{ p: 3, bgcolor: 'action.hover', borderLeft: `4px solid`, borderColor: `${getSeverityColor(alert.severity)}.main` }}>
                    {/* Metrics */}
                    {(alert.current_value !== undefined || alert.expected_value !== undefined) && (
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
                          Metrics
                        </Typography>
                        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 2 }}>
                          {alert.current_value !== undefined && (
                            <Box>
                              <Typography variant="caption" color="text.secondary">Current Value</Typography>
                              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                {formatValue(alert.current_value, alert.metric_name)}
                              </Typography>
                            </Box>
                          )}
                          {alert.expected_value !== undefined && (
                            <Box>
                              <Typography variant="caption" color="text.secondary">Expected Value</Typography>
                              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                {formatValue(alert.expected_value, alert.metric_name)}
                              </Typography>
                            </Box>
                          )}
                          {alert.threshold !== undefined && (
                            <Box>
                              <Typography variant="caption" color="text.secondary">Threshold</Typography>
                              <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                {formatValue(alert.threshold, alert.metric_name)}
                              </Typography>
                            </Box>
                          )}
                          {alert.deviation_percentage !== undefined && (
                            <Box>
                              <Typography variant="caption" color="text.secondary">Deviation</Typography>
                              <Typography variant="body1" sx={{ fontWeight: 600, color: alert.deviation_percentage > 0 ? 'error.main' : 'success.main' }}>
                                {alert.deviation_percentage > 0 ? '+' : ''}{alert.deviation_percentage.toFixed(1)}%
                              </Typography>
                            </Box>
                          )}
                        </Box>
                      </Box>
                    )}

                    {/* Action Items */}
                    {alert.action_items && alert.action_items.length > 0 && (
                      <Box>
                        <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
                          Recommended Actions
                        </Typography>
                        <List dense sx={{ pl: 2 }}>
                          {alert.action_items.map((item, idx) => (
                            <ListItem key={idx} sx={{ py: 0.5 }}>
                              <ListItemText
                                primary={`${idx + 1}. ${item}`}
                                primaryTypographyProps={{ variant: 'body2' }}
                              />
                            </ListItem>
                          ))}
                        </List>
                      </Box>
                    )}

                    {/* Actions */}
                    <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                      <Button
                        variant="contained"
                        size="small"
                        onClick={() => onResolveAlert?.(alert.id || String(index))}
                      >
                        Mark Resolved
                      </Button>
                      <Button
                        variant="outlined"
                        size="small"
                        onClick={() => onDismissAlert?.(alert.id || String(index))}
                      >
                        Dismiss
                      </Button>
                    </Box>
                  </Box>
                </Collapse>

                {index < filteredAlerts.length - 1 && <Divider />}
              </React.Fragment>
            ))
          )}
        </List>
      </GlassCard>
    </Box>
  );
};

export default AlertsPanel;
