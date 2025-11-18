/**
 * Workflow Dashboard
 * Monitor and manage multi-agent workflows in real-time
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  Card,
  CardContent,
  Button,
  TextField,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Chip,
  Alert,
  LinearProgress,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Collapse,
} from '@mui/material';
import {
  PlayArrow,
  CheckCircle,
  Error as ErrorIcon,
  Pending,
  ExpandMore,
  ExpandLess,
  Refresh,
  Timeline,
  AccountTree,
  Assessment,
  School,
  Work,
  LibraryBooks,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const WORKFLOW_TYPES = [
  {
    id: 'career_transition',
    name: 'Career Transition',
    description: 'Complete career transition with 5-agent collaboration',
    icon: <Work />,
    color: 'primary',
  },
  {
    id: 'learning_consensus',
    name: 'Learning Consensus',
    description: 'Agents negotiate optimal learning strategy',
    icon: <School />,
    color: 'secondary',
  },
  {
    id: 'market_analysis',
    name: 'Market Analysis',
    description: 'Distributed parallel job market analysis',
    icon: <Assessment />,
    color: 'success',
  },
  {
    id: 'resource_curation',
    name: 'Resource Curation',
    description: 'Collaborative resource discovery and curation',
    icon: <LibraryBooks />,
    color: 'info',
  },
];

const WorkflowDashboard = () => {
  const [workflows, setWorkflows] = useState([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [workflowProgress, setWorkflowProgress] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [newWorkflow, setNewWorkflow] = useState({
    type: '',
    worker_id: 1,
    target_role: '',
    target_skills: [],
    industry: '',
    region: '',
    topic: '',
    difficulty: 'intermediate',
  });
  const [expandedWorkflows, setExpandedWorkflows] = useState(new Set());

  useEffect(() => {
    // In real app, load workflows from backend
    loadWorkflows();
  }, []);

  useEffect(() => {
    if (selectedWorkflow) {
      loadWorkflowProgress(selectedWorkflow);
      const interval = setInterval(() => loadWorkflowProgress(selectedWorkflow), 2000);
      return () => clearInterval(interval);
    }
  }, [selectedWorkflow]);

  const loadWorkflows = async () => {
    // Mock workflow data
    setWorkflows([
      {
        workflow_id: 'wf_123',
        type: 'career_transition',
        status: 'completed',
        created_at: new Date().toISOString(),
        worker_id: 1,
        target_role: 'Data Scientist',
      },
      {
        workflow_id: 'wf_124',
        type: 'market_analysis',
        status: 'in_progress',
        created_at: new Date().toISOString(),
        industry: 'Technology',
        region: 'US',
      },
    ]);
  };

  const loadWorkflowProgress = async (workflowId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/mas/workflows/${workflowId}/progress`);
      setWorkflowProgress(response.data.progress);
    } catch (error) {
      console.error('Error loading workflow progress:', error);
    }
  };

  const startWorkflow = async () => {
    try {
      let response;
      const { type } = newWorkflow;

      if (type === 'career_transition') {
        response = await axios.post(`${API_BASE_URL}/mas/workflows/career-transition`, {
          worker_id: newWorkflow.worker_id,
          target_role: newWorkflow.target_role,
        });
      } else if (type === 'learning_consensus') {
        response = await axios.post(`${API_BASE_URL}/mas/workflows/learning-consensus`, {
          worker_id: newWorkflow.worker_id,
          target_skills: newWorkflow.target_skills,
          time_constraint_hours: 100,
        });
      } else if (type === 'market_analysis') {
        response = await axios.post(`${API_BASE_URL}/mas/workflows/market-analysis`, {
          industry: newWorkflow.industry,
          region: newWorkflow.region,
          skills: ['Python', 'SQL', 'Machine Learning'],
        });
      } else if (type === 'resource_curation') {
        response = await axios.post(`${API_BASE_URL}/mas/workflows/resource-curation`, {
          topic: newWorkflow.topic,
          difficulty_level: newWorkflow.difficulty,
          learner_preferences: {},
        });
      }

      if (response?.data?.success) {
        setDialogOpen(false);
        loadWorkflows();
      }
    } catch (error) {
      console.error('Error starting workflow:', error);
    }
  };

  const toggleWorkflowExpand = (workflowId) => {
    setExpandedWorkflows((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(workflowId)) {
        newSet.delete(workflowId);
      } else {
        newSet.add(workflowId);
      }
      return newSet;
    });
  };

  const getStatusIcon = (status) => {
    const icons = {
      pending: <Pending color="warning" />,
      in_progress: <PlayArrow color="info" />,
      completed: <CheckCircle color="success" />,
      failed: <ErrorIcon color="error" />,
    };
    return icons[status] || <Pending />;
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'warning',
      assigned: 'info',
      in_progress: 'info',
      completed: 'success',
      failed: 'error',
      cancelled: 'default',
    };
    return colors[status] || 'default';
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Workflow Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Monitor and manage multi-agent workflows
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<PlayArrow />} onClick={() => setDialogOpen(true)}>
          Start New Workflow
        </Button>
      </Box>

      {/* Workflow Types Overview */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {WORKFLOW_TYPES.map((workflow) => (
          <Grid item xs={12} sm={6} lg={3} key={workflow.id}>
            <Card
              sx={{
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 6,
                },
              }}
              onClick={() => {
                setNewWorkflow({ ...newWorkflow, type: workflow.id });
                setDialogOpen(true);
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ color: `${workflow.color}.main`, fontSize: 40, mr: 2 }}>
                    {workflow.icon}
                  </Box>
                  <Box>
                    <Typography variant="h6" fontWeight={600}>
                      {workflow.name}
                    </Typography>
                  </Box>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  {workflow.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Active Workflows */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" fontWeight={600} gutterBottom>
          Active Workflows
        </Typography>

        {workflows.length === 0 ? (
          <Alert severity="info">No workflows running. Start a new workflow to see it here.</Alert>
        ) : (
          <List>
            {workflows.map((workflow) => {
              const workflowType = WORKFLOW_TYPES.find((wt) => wt.id === workflow.type);
              const isExpanded = expandedWorkflows.has(workflow.workflow_id);

              return (
                <React.Fragment key={workflow.workflow_id}>
                  <ListItem
                    sx={{
                      border: 1,
                      borderColor: 'divider',
                      borderRadius: 2,
                      mb: 2,
                      bgcolor: 'background.paper',
                    }}
                  >
                    <ListItemIcon>{getStatusIcon(workflow.status)}</ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="h6" fontWeight={600}>
                            {workflowType?.name || workflow.type}
                          </Typography>
                          <Chip
                            label={workflow.status}
                            size="small"
                            color={getStatusColor(workflow.status)}
                          />
                        </Box>
                      }
                      secondary={
                        <>
                          <Typography variant="caption" color="text.secondary" display="block">
                            ID: {workflow.workflow_id}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Started: {new Date(workflow.created_at).toLocaleString()}
                          </Typography>
                        </>
                      }
                    />
                    <IconButton onClick={() => toggleWorkflowExpand(workflow.workflow_id)}>
                      {isExpanded ? <ExpandLess /> : <ExpandMore />}
                    </IconButton>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<Timeline />}
                      onClick={() => setSelectedWorkflow(workflow.workflow_id)}
                      sx={{ ml: 2 }}
                    >
                      View Details
                    </Button>
                  </ListItem>

                  <Collapse in={isExpanded}>
                    <Paper sx={{ p: 2, ml: 7, mb: 2, bgcolor: 'grey.50' }}>
                      {/* Workflow-specific details */}
                      {workflow.type === 'career_transition' && (
                        <Grid container spacing={2}>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              Worker ID
                            </Typography>
                            <Typography variant="body2" fontWeight={600}>
                              {workflow.worker_id}
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              Target Role
                            </Typography>
                            <Typography variant="body2" fontWeight={600}>
                              {workflow.target_role}
                            </Typography>
                          </Grid>
                        </Grid>
                      )}

                      {workflow.type === 'market_analysis' && (
                        <Grid container spacing={2}>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              Industry
                            </Typography>
                            <Typography variant="body2" fontWeight={600}>
                              {workflow.industry}
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              Region
                            </Typography>
                            <Typography variant="body2" fontWeight={600}>
                              {workflow.region}
                            </Typography>
                          </Grid>
                        </Grid>
                      )}
                    </Paper>
                  </Collapse>
                </React.Fragment>
              );
            })}
          </List>
        )}
      </Paper>

      {/* Workflow Progress Dialog */}
      {selectedWorkflow && workflowProgress && (
        <Dialog open={Boolean(selectedWorkflow)} onClose={() => setSelectedWorkflow(null)} maxWidth="md" fullWidth>
          <DialogTitle>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">Workflow Progress</Typography>
              <IconButton onClick={() => loadWorkflowProgress(selectedWorkflow)}>
                <Refresh />
              </IconButton>
            </Box>
          </DialogTitle>
          <DialogContent>
            <Box sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Overall Progress
                </Typography>
                <Typography variant="body2" fontWeight={600}>
                  {workflowProgress.progress_percentage?.toFixed(0) || 0}%
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={workflowProgress.progress_percentage || 0}
                sx={{ height: 8, borderRadius: 4 }}
              />
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                <Typography variant="caption" color="text.secondary">
                  {workflowProgress.completed} / {workflowProgress.total_tasks} tasks completed
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {workflowProgress.failed} failed, {workflowProgress.in_progress} in progress
                </Typography>
              </Box>
            </Box>

            <Stepper orientation="vertical">
              {workflowProgress.tasks?.map((task, index) => (
                <Step key={task.task_id} active={task.status === 'in_progress'} completed={task.status === 'completed'}>
                  <StepLabel
                    error={task.status === 'failed'}
                    StepIconComponent={() => getStatusIcon(task.status)}
                  >
                    <Typography variant="subtitle1" fontWeight={600}>
                      {task.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Assigned to: {task.assigned_agent || 'Pending'}
                    </Typography>
                  </StepLabel>
                  <StepContent>
                    <Chip label={task.status} size="small" color={getStatusColor(task.status)} sx={{ mt: 1 }} />
                  </StepContent>
                </Step>
              ))}
            </Stepper>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSelectedWorkflow(null)}>Close</Button>
          </DialogActions>
        </Dialog>
      )}

      {/* New Workflow Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Start New Workflow</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Workflow Type</InputLabel>
              <Select
                value={newWorkflow.type}
                label="Workflow Type"
                onChange={(e) => setNewWorkflow({ ...newWorkflow, type: e.target.value })}
              >
                {WORKFLOW_TYPES.map((wt) => (
                  <MenuItem key={wt.id} value={wt.id}>
                    {wt.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {newWorkflow.type === 'career_transition' && (
              <>
                <TextField
                  fullWidth
                  label="Worker ID"
                  type="number"
                  value={newWorkflow.worker_id}
                  onChange={(e) => setNewWorkflow({ ...newWorkflow, worker_id: parseInt(e.target.value) })}
                  sx={{ mb: 2 }}
                />
                <TextField
                  fullWidth
                  label="Target Role"
                  value={newWorkflow.target_role}
                  onChange={(e) => setNewWorkflow({ ...newWorkflow, target_role: e.target.value })}
                  placeholder="e.g., Data Scientist"
                />
              </>
            )}

            {newWorkflow.type === 'market_analysis' && (
              <>
                <TextField
                  fullWidth
                  label="Industry"
                  value={newWorkflow.industry}
                  onChange={(e) => setNewWorkflow({ ...newWorkflow, industry: e.target.value })}
                  sx={{ mb: 2 }}
                  placeholder="e.g., Technology"
                />
                <TextField
                  fullWidth
                  label="Region"
                  value={newWorkflow.region}
                  onChange={(e) => setNewWorkflow({ ...newWorkflow, region: e.target.value })}
                  placeholder="e.g., US, Europe"
                />
              </>
            )}

            {newWorkflow.type === 'resource_curation' && (
              <>
                <TextField
                  fullWidth
                  label="Topic"
                  value={newWorkflow.topic}
                  onChange={(e) => setNewWorkflow({ ...newWorkflow, topic: e.target.value })}
                  sx={{ mb: 2 }}
                  placeholder="e.g., Machine Learning"
                />
                <FormControl fullWidth>
                  <InputLabel>Difficulty</InputLabel>
                  <Select
                    value={newWorkflow.difficulty}
                    label="Difficulty"
                    onChange={(e) => setNewWorkflow({ ...newWorkflow, difficulty: e.target.value })}
                  >
                    <MenuItem value="beginner">Beginner</MenuItem>
                    <MenuItem value="intermediate">Intermediate</MenuItem>
                    <MenuItem value="advanced">Advanced</MenuItem>
                    <MenuItem value="expert">Expert</MenuItem>
                  </Select>
                </FormControl>
              </>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={startWorkflow}
            disabled={!newWorkflow.type}
            startIcon={<PlayArrow />}
          >
            Start Workflow
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default WorkflowDashboard;
