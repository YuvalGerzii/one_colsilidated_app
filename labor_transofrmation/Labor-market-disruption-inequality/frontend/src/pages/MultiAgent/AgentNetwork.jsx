/**
 * Agent Network Visualization
 * Interactive visualization of multi-agent system interactions
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  Card,
  CardContent,
  Chip,
  Button,
  IconButton,
  Tooltip,
  Badge,
  LinearProgress,
  Alert,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
  Divider,
} from '@mui/material';
import {
  Psychology,
  Hub,
  TrendingUp,
  Refresh,
  PlayArrow,
  Pause,
  Visibility,
  Message,
  Speed,
  CheckCircle,
  Error as ErrorIcon,
  Warning,
  Info,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const AgentNetwork = () => {
  const [agents, setAgents] = useState([]);
  const [networkData, setNetworkData] = useState(null);
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    loadData();
    const interval = autoRefresh ? setInterval(loadData, 3000) : null;
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [agentsRes, networkRes, statusRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/mas/agents`),
        axios.get(`${API_BASE_URL}/mas/network/visualization`),
        axios.get(`${API_BASE_URL}/mas/status`),
      ]);

      setAgents(agentsRes.data.agents || []);
      setNetworkData(networkRes.data.network || null);
      setSystemStatus(statusRes.data.system || null);
    } catch (error) {
      console.error('Error loading agent network:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleAgentActive = async (agentId, currentActive) => {
    try {
      const endpoint = currentActive ? 'deactivate' : 'activate';
      await axios.post(`${API_BASE_URL}/mas/agents/${agentId}/${endpoint}`);
      loadData();
    } catch (error) {
      console.error('Error toggling agent:', error);
    }
  };

  const getAgentTypeColor = (agentType) => {
    const colors = {
      gap_analyzer: 'primary',
      opportunity_scout: 'success',
      learning_strategist: 'secondary',
      teaching_coach: 'info',
      career_navigator: 'warning',
      study_buddy: 'error',
      ui_designer: 'primary',
      marketing: 'secondary',
    };
    return colors[agentType] || 'default';
  };

  const getStatusIcon = (active) => {
    return active ? <CheckCircle color="success" /> : <Pause color="disabled" />;
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Multi-Agent System
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Real-time monitoring of agent interactions and collective intelligence
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant={autoRefresh ? 'contained' : 'outlined'}
            startIcon={autoRefresh ? <Pause /> : <PlayArrow />}
            onClick={() => setAutoRefresh(!autoRefresh)}
          >
            {autoRefresh ? 'Pause' : 'Resume'} Auto-Refresh
          </Button>
          <Button variant="outlined" startIcon={<Refresh />} onClick={loadData}>
            Refresh
          </Button>
        </Box>
      </Box>

      {/* System Status Cards */}
      {systemStatus && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                    <Psychology />
                  </Avatar>
                  <Box>
                    <Typography variant="h4" fontWeight={700}>
                      {systemStatus.agents?.total || 0}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Total Agents
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="body2" color="success.main">
                  {systemStatus.agents?.active || 0} active
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'secondary.main', mr: 2 }}>
                    <Hub />
                  </Avatar>
                  <Box>
                    <Typography variant="h4" fontWeight={700}>
                      {systemStatus.tasks?.total || 0}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Total Tasks
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="body2" color="info.main">
                  {Object.values(systemStatus.tasks?.by_status || {}).reduce((a, b) => a + b, 0)} completed
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                    <Message />
                  </Avatar>
                  <Box>
                    <Typography variant="h4" fontWeight={700}>
                      {systemStatus.messages?.conversations || 0}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Conversations
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="body2" color="warning.main">
                  {systemStatus.messages?.pending || 0} pending
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                    <TrendingUp />
                  </Avatar>
                  <Box>
                    <Typography variant="h4" fontWeight={700}>
                      {systemStatus.workflows?.total || 0}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Workflows
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="body2" color="success.main">
                  {systemStatus.workflows?.active || 0} active
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Main Content */}
      <Paper sx={{ p: 3 }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)} sx={{ mb: 3 }}>
          <Tab label="Agent Overview" />
          <Tab label="Network Graph" />
          <Tab label="Performance Metrics" />
        </Tabs>

        {/* Tab 0: Agent Overview */}
        {tabValue === 0 && (
          <Grid container spacing={3}>
            {agents.map((agent) => (
              <Grid item xs={12} md={6} lg={4} key={agent.agent_id}>
                <Card
                  variant="outlined"
                  sx={{
                    borderLeft: 4,
                    borderColor: `${getAgentTypeColor(agent.agent_type)}.main`,
                    transition: 'transform 0.2s, box-shadow 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 4,
                    },
                  }}
                >
                  <CardContent>
                    {/* Agent Header */}
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Avatar sx={{ bgcolor: `${getAgentTypeColor(agent.agent_type)}.main`, mr: 2 }}>
                          <Psychology />
                        </Avatar>
                        <Box>
                          <Typography variant="h6" fontWeight={600}>
                            {agent.agent_type.replace(/_/g, ' ').toUpperCase()}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {agent.agent_id}
                          </Typography>
                        </Box>
                      </Box>
                      <IconButton
                        size="small"
                        onClick={() => toggleAgentActive(agent.agent_id, agent.active)}
                      >
                        {getStatusIcon(agent.active)}
                      </IconButton>
                    </Box>

                    {/* Status */}
                    <Box sx={{ mb: 2 }}>
                      <Chip
                        label={agent.active ? 'Active' : 'Inactive'}
                        color={agent.active ? 'success' : 'default'}
                        size="small"
                        sx={{ mr: 1 }}
                      />
                      {agent.mas_enabled && (
                        <Chip
                          label="MAS Enabled"
                          color="primary"
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>

                    {/* Capabilities */}
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="caption" color="text.secondary" gutterBottom>
                        Capabilities:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                        {agent.capabilities.slice(0, 3).map((cap, idx) => (
                          <Chip key={idx} label={cap} size="small" variant="outlined" />
                        ))}
                        {agent.capabilities.length > 3 && (
                          <Chip label={`+${agent.capabilities.length - 3}`} size="small" variant="outlined" />
                        )}
                      </Box>
                    </Box>

                    {/* Performance Metrics */}
                    {agent.performance && (
                      <Box>
                        <Typography variant="caption" color="text.secondary" gutterBottom>
                          Performance:
                        </Typography>
                        <Box sx={{ mt: 1 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                            <Typography variant="caption">Success Rate</Typography>
                            <Typography variant="caption" fontWeight={600}>
                              {(agent.performance.success_rate * 100).toFixed(0)}%
                            </Typography>
                          </Box>
                          <LinearProgress
                            variant="determinate"
                            value={agent.performance.success_rate * 100}
                            sx={{ height: 6, borderRadius: 3 }}
                          />
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                          <Typography variant="caption" color="text.secondary">
                            Tasks: {agent.performance.tasks_completed || 0}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Collaborations: {agent.performance.collaborations || 0}
                          </Typography>
                        </Box>
                      </Box>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}

            {agents.length === 0 && !loading && (
              <Grid item xs={12}>
                <Alert severity="info">
                  No agents registered yet. Agents will appear here when they join the system.
                </Alert>
              </Grid>
            )}
          </Grid>
        )}

        {/* Tab 1: Network Graph */}
        {tabValue === 1 && (
          <Box>
            {networkData ? (
              <Box>
                <Alert severity="info" sx={{ mb: 3 }}>
                  Network visualization showing {networkData.nodes?.length || 0} agents and{' '}
                  {networkData.edges?.length || 0} communication edges
                </Alert>

                {/* Network Stats */}
                <Grid container spacing={2} sx={{ mb: 3 }}>
                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Agent Nodes
                      </Typography>
                      <List dense>
                        {networkData.nodes?.slice(0, 5).map((node) => (
                          <ListItem key={node.id}>
                            <ListItemIcon>
                              <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                                <Psychology sx={{ fontSize: 18 }} />
                              </Avatar>
                            </ListItemIcon>
                            <ListItemText
                              primary={node.type}
                              secondary={`${node.capabilities?.length || 0} capabilities`}
                            />
                            <Chip
                              label={node.active ? 'Active' : 'Inactive'}
                              size="small"
                              color={node.active ? 'success' : 'default'}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Paper>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Top Communication Channels
                      </Typography>
                      <List dense>
                        {networkData.edges
                          ?.sort((a, b) => b.weight - a.weight)
                          .slice(0, 5)
                          .map((edge, idx) => (
                            <ListItem key={idx}>
                              <ListItemText
                                primary={`${edge.from} → ${edge.to}`}
                                secondary={`${edge.weight} messages`}
                              />
                              <LinearProgress
                                variant="determinate"
                                value={Math.min(100, edge.weight * 10)}
                                sx={{ width: 100, ml: 2 }}
                              />
                            </ListItem>
                          ))}
                      </List>
                    </Paper>
                  </Grid>
                </Grid>

                <Alert severity="success">
                  Real-time graph visualization would be rendered here using a library like D3.js or Cytoscape.js
                </Alert>
              </Box>
            ) : (
              <Alert severity="info">No network data available yet</Alert>
            )}
          </Box>
        )}

        {/* Tab 2: Performance Metrics */}
        {tabValue === 2 && (
          <Grid container spacing={3}>
            {agents.map((agent) => (
              <Grid item xs={12} md={6} key={agent.agent_id}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    {agent.agent_type.replace(/_/g, ' ').toUpperCase()}
                  </Typography>
                  <Divider sx={{ mb: 2 }} />

                  {agent.performance ? (
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Tasks Completed
                        </Typography>
                        <Typography variant="h5" fontWeight={600}>
                          {agent.performance.tasks_completed || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Success Rate
                        </Typography>
                        <Typography variant="h5" fontWeight={600} color="success.main">
                          {(agent.performance.success_rate * 100).toFixed(1)}%
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Messages Sent
                        </Typography>
                        <Typography variant="h5" fontWeight={600}>
                          {agent.performance.messages_sent || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Collaborations
                        </Typography>
                        <Typography variant="h5" fontWeight={600}>
                          {agent.performance.collaborations || 0}
                        </Typography>
                      </Grid>
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary">
                          Avg Response Time
                        </Typography>
                        <Typography variant="h6" fontWeight={600}>
                          {agent.performance.avg_response_time?.toFixed(2) || 0}s
                        </Typography>
                      </Grid>
                    </Grid>
                  ) : (
                    <Alert severity="info">No performance data available</Alert>
                  )}
                </Paper>
              </Grid>
            ))}
          </Grid>
        )}
      </Paper>
    </Box>
  );
};

export default AgentNetwork;
