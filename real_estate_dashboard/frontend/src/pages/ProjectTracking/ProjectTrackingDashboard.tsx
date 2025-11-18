/**
 * Enhanced Project Tracking - Jira-style Kanban Board
 *
 * @version 2.0.0
 * @updated 2025-11-15
 * @description Modern Kanban board with drag-and-drop, employee management, and task tracking
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  Button,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Autocomplete,
  Stack,
  Alert,
  Avatar,
  AvatarGroup,
  Badge,
  Tooltip,
  Menu,
  ListItemIcon,
  ListItemText,
  Divider,
  Tab,
  Tabs,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  MoreVert as MoreIcon,
  Person as PersonIcon,
  Assignment as TaskIcon,
  ViewKanban as KanbanIcon,
  Group as GroupIcon,
  Flag as FlagIcon,
  CalendarToday as CalendarIcon,
  DragIndicator as DragIcon,
  AttachFile as AttachIcon,
  Comment as CommentIcon,
  CheckCircle as CheckIcon,
} from '@mui/icons-material';
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
  PointerSensor,
  useSensor,
  useSensors,
  closestCorners,
} from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { designTokens, alphaColor } from '../../theme/designTokens';
import { MetricCard } from '../../components/ui/MetricCard';
import { api } from '../../services/apiClient';

// Types
interface Employee {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  role: string;
  color: string;
}

interface Task {
  id: string;
  project_id: string;
  parent_task_id?: string;
  name: string;
  description?: string;
  status: string;
  priority: string;
  due_date?: string;
  assigned_to?: string[];
  tags: string[];
  is_overdue: boolean;
  subtask_count: number;
  completed_subtask_count: number;
  comments_count?: number;
  attachments_count?: number;
}

interface Project {
  id: string;
  name: string;
  project_type: string;
  status: string;
  description?: string;
  color: string;
  tags: string[];
  due_date?: string;
  completion_percentage: number;
  task_count: number;
  completed_task_count: number;
  is_overdue: boolean;
  owner?: string;
}

interface Column {
  id: string;
  title: string;
  taskIds: string[];
  color: string;
}

// Mock employees data
const MOCK_EMPLOYEES: Employee[] = [
  { id: '1', name: 'John Doe', email: 'john@example.com', role: 'Developer', color: '#3b82f6' },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'Designer', color: '#10b981' },
  { id: '3', name: 'Mike Johnson', email: 'mike@example.com', role: 'PM', color: '#f59e0b' },
  { id: '4', name: 'Sarah Williams', email: 'sarah@example.com', role: 'QA', color: '#8b5cf6' },
  { id: '5', name: 'Tom Brown', email: 'tom@example.com', role: 'Developer', color: '#ef4444' },
];

const KANBAN_COLUMNS = [
  { id: 'todo', title: 'To Do', status: 'Not Started', color: designTokens.colors.chart.blue },
  { id: 'in_progress', title: 'In Progress', status: 'In Progress', color: designTokens.colors.chart.amber },
  { id: 'in_review', title: 'In Review', status: 'In Review', color: designTokens.colors.chart.purple },
  { id: 'done', title: 'Done', status: 'Completed', color: designTokens.colors.semantic.success },
];

const TASK_PRIORITIES = ['Low', 'Medium', 'High', 'Critical'];
const PROJECT_TYPES = ['Work', 'Personal', 'Deal', 'Client Project', 'Real Estate', 'Business Development'];

// Draggable Task Card Component
const TaskCard: React.FC<{ task: Task; employees: Employee[]; onEdit: () => void; onDelete: () => void }> = ({
  task,
  employees,
  onEdit,
  onDelete,
}) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: task.id,
  });

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Critical':
        return designTokens.colors.semantic.error;
      case 'High':
        return designTokens.colors.semantic.warning;
      case 'Medium':
        return designTokens.colors.chart.blue;
      default:
        return designTokens.colors.chart.gray;
    }
  };

  const assignedEmployees = employees.filter((emp) => task.assigned_to?.includes(emp.id));

  return (
    <Card
      ref={setNodeRef}
      style={style}
      sx={{
        p: 2,
        mb: 2,
        cursor: isDragging ? 'grabbing' : 'grab',
        '&:hover': {
          boxShadow: `0 4px 12px ${alphaColor(designTokens.colors.chart.blue, 0.15)}`,
        },
        border: `1px solid ${alphaColor(designTokens.colors.chart.gray, 0.1)}`,
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 1.5 }}>
        <Box sx={{ flex: 1, display: 'flex', alignItems: 'center' }}>
          <Box {...attributes} {...listeners} sx={{ mr: 1, cursor: 'grab', color: 'text.secondary' }}>
            <DragIcon fontSize="small" />
          </Box>
          <Typography variant="subtitle2" sx={{ fontWeight: 600, flex: 1 }}>
            {task.name}
          </Typography>
        </Box>
        <IconButton
          size="small"
          onClick={(e) => setAnchorEl(e.currentTarget)}
          sx={{ ml: 1 }}
        >
          <MoreIcon fontSize="small" />
        </IconButton>
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={() => setAnchorEl(null)}
        >
          <MenuItem onClick={() => { onEdit(); setAnchorEl(null); }}>
            <ListItemIcon><EditIcon fontSize="small" /></ListItemIcon>
            <ListItemText>Edit</ListItemText>
          </MenuItem>
          <MenuItem onClick={() => { onDelete(); setAnchorEl(null); }}>
            <ListItemIcon><DeleteIcon fontSize="small" /></ListItemIcon>
            <ListItemText>Delete</ListItemText>
          </MenuItem>
        </Menu>
      </Box>

      {task.description && (
        <Typography
          variant="body2"
          color="text.secondary"
          sx={{
            mb: 1.5,
            fontSize: designTokens.typography.fontSize.sm,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
          }}
        >
          {task.description}
        </Typography>
      )}

      <Stack direction="row" spacing={0.5} sx={{ mb: 1.5, flexWrap: 'wrap', gap: 0.5 }}>
        <Chip
          icon={<FlagIcon sx={{ fontSize: 14 }} />}
          label={task.priority}
          size="small"
          sx={{
            height: 20,
            fontSize: designTokens.typography.fontSize.xs,
            bgcolor: alphaColor(getPriorityColor(task.priority), 0.1),
            color: getPriorityColor(task.priority),
            '& .MuiChip-icon': { color: getPriorityColor(task.priority) },
          }}
        />
        {task.is_overdue && (
          <Chip
            label="Overdue"
            size="small"
            color="error"
            sx={{ height: 20, fontSize: designTokens.typography.fontSize.xs }}
          />
        )}
        {task.subtask_count > 0 && (
          <Chip
            icon={<CheckIcon sx={{ fontSize: 14 }} />}
            label={`${task.completed_subtask_count}/${task.subtask_count}`}
            size="small"
            sx={{ height: 20, fontSize: designTokens.typography.fontSize.xs }}
          />
        )}
      </Stack>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Stack direction="row" spacing={1}>
          {task.comments_count !== undefined && task.comments_count > 0 && (
            <Tooltip title={`${task.comments_count} comments`}>
              <Stack direction="row" spacing={0.5} alignItems="center">
                <CommentIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
                <Typography variant="caption" color="text.secondary">{task.comments_count}</Typography>
              </Stack>
            </Tooltip>
          )}
          {task.attachments_count !== undefined && task.attachments_count > 0 && (
            <Tooltip title={`${task.attachments_count} attachments`}>
              <Stack direction="row" spacing={0.5} alignItems="center">
                <AttachIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
                <Typography variant="caption" color="text.secondary">{task.attachments_count}</Typography>
              </Stack>
            </Tooltip>
          )}
          {task.due_date && (
            <Tooltip title={`Due ${new Date(task.due_date).toLocaleDateString()}`}>
              <Stack direction="row" spacing={0.5} alignItems="center">
                <CalendarIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
                <Typography variant="caption" color="text.secondary">
                  {new Date(task.due_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </Typography>
              </Stack>
            </Tooltip>
          )}
        </Stack>

        {assignedEmployees.length > 0 && (
          <AvatarGroup max={3} sx={{ '& .MuiAvatar-root': { width: 24, height: 24, fontSize: 12 } }}>
            {assignedEmployees.map((emp) => (
              <Tooltip key={emp.id} title={emp.name}>
                <Avatar sx={{ bgcolor: emp.color }}>{emp.name.charAt(0)}</Avatar>
              </Tooltip>
            ))}
          </AvatarGroup>
        )}
      </Box>
    </Card>
  );
};

// Kanban Column Component
const KanbanColumn: React.FC<{
  column: { id: string; title: string; color: string };
  tasks: Task[];
  employees: Employee[];
  onEditTask: (task: Task) => void;
  onDeleteTask: (taskId: string) => void;
  onAddTask: (status: string) => void;
}> = ({ column, tasks, employees, onEditTask, onDeleteTask, onAddTask }) => {
  return (
    <Paper
      sx={{
        p: 2,
        bgcolor: alphaColor(column.color, 0.03),
        border: `1px solid ${alphaColor(column.color, 0.1)}`,
        borderRadius: designTokens.radius.lg,
        minHeight: 500,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Stack direction="row" spacing={1} alignItems="center">
          <Box
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              bgcolor: column.color,
            }}
          />
          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
            {column.title}
          </Typography>
          <Chip label={tasks.length} size="small" sx={{ height: 20, minWidth: 24 }} />
        </Stack>
        <Tooltip title="Add task">
          <IconButton size="small" onClick={() => onAddTask(column.id)}>
            <AddIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>

      <SortableContext items={tasks.map((t) => t.id)} strategy={verticalListSortingStrategy}>
        <Box sx={{ flex: 1, overflowY: 'auto' }}>
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              employees={employees}
              onEdit={() => onEditTask(task)}
              onDelete={() => onDeleteTask(task.id)}
            />
          ))}
        </Box>
      </SortableContext>
    </Paper>
  );
};

const ProjectTrackingDashboard: React.FC = () => {
  const [currentView, setCurrentView] = useState<'kanban' | 'employees'>('kanban');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Data states
  const [tasks, setTasks] = useState<Task[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [employees] = useState<Employee[]>(MOCK_EMPLOYEES);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [filter, setFilter] = useState<'all' | 'my_tasks'>('all');

  // Dialog states
  const [taskDialogOpen, setTaskDialogOpen] = useState(false);
  const [employeeDialogOpen, setEmployeeDialogOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Drag and drop state
  const [activeId, setActiveId] = useState<string | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  // Form state
  const [taskForm, setTaskForm] = useState({
    name: '',
    project_id: '',
    description: '',
    status: 'Not Started',
    priority: 'Medium',
    due_date: '',
    assigned_to: [] as string[],
    tags: [] as string[],
  });

  // Fetch data
  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await api.get('/project-tracking/projects');
      setProjects(response.data);
      if (response.data.length > 0 && !selectedProject) {
        setSelectedProject(response.data[0]);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch projects');
    } finally {
      setLoading(false);
    }
  };

  const fetchTasks = async (projectId?: string) => {
    try {
      setLoading(true);
      const url = projectId
        ? `/project-tracking/projects/${projectId}/tasks`
        : '/project-tracking/tasks';
      const response = await api.get(url);
      setTasks(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const createTask = async () => {
    try {
      setLoading(true);
      await api.post('/project-tracking/tasks', {
        ...taskForm,
        project_id: selectedProject?.id,
      });
      setTaskDialogOpen(false);
      fetchTasks(selectedProject?.id);
      resetTaskForm();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (taskId: string, updates: Partial<Task>) => {
    try {
      await api.put(`/project-tracking/tasks/${taskId}`, updates);
      fetchTasks(selectedProject?.id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update task');
    }
  };

  const deleteTask = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    try {
      await api.delete(`/project-tracking/tasks/${id}`);
      fetchTasks(selectedProject?.id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete task');
    }
  };

  const resetTaskForm = () => {
    setTaskForm({
      name: '',
      project_id: selectedProject?.id || '',
      description: '',
      status: 'Not Started',
      priority: 'Medium',
      due_date: '',
      assigned_to: [],
      tags: [],
    });
  };

  const openEditTask = (task: Task) => {
    setEditingTask(task);
    setTaskForm({
      name: task.name,
      project_id: task.project_id,
      description: task.description || '',
      status: task.status,
      priority: task.priority,
      due_date: task.due_date || '',
      assigned_to: task.assigned_to || [],
      tags: task.tags,
    });
    setTaskDialogOpen(true);
  };

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveId(null);

    if (!over) return;

    const activeTask = tasks.find((t) => t.id === active.id);
    if (!activeTask) return;

    // Find which column the task was dropped into
    const targetColumn = KANBAN_COLUMNS.find((col) => {
      const columnTasks = getTasksByStatus(col.status);
      return columnTasks.some((t) => t.id === over.id) || col.id === over.id;
    });

    if (targetColumn && activeTask.status !== targetColumn.status) {
      updateTask(activeTask.id, { ...activeTask, status: targetColumn.status });
    }
  };

  const getTasksByStatus = (status: string) => {
    let filteredTasks = tasks.filter((t) => t.status === status && !t.parent_task_id);

    if (filter === 'my_tasks') {
      // Filter to show only tasks assigned to current user (for demo, we'll use first employee)
      filteredTasks = filteredTasks.filter((t) => t.assigned_to?.includes(employees[0].id));
    }

    return filteredTasks;
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  useEffect(() => {
    if (selectedProject) {
      fetchTasks(selectedProject.id);
    }
  }, [selectedProject]);

  const activeTask = tasks.find((t) => t.id === activeId);

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
              background: designTokens.colors.workspace.operate,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <KanbanIcon sx={{ fontSize: 28, color: 'white' }} />
          </Box>
          <Box flex={1}>
            <Typography variant="h4" sx={{ fontWeight: designTokens.typography.fontWeight.bold }}>
              Project Tracking
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage tasks and team with Kanban board
            </Typography>
          </Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{ background: designTokens.colors.workspace.operate }}
            onClick={() => {
              resetTaskForm();
              setEditingTask(null);
              setTaskDialogOpen(true);
            }}
          >
            New Task
          </Button>
        </Stack>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Total Tasks"
            value={tasks.length}
            change="+5"
            trend="up"
            icon={TaskIcon}
            color={designTokens.colors.chart.blue}
            subtext="active tasks"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="In Progress"
            value={getTasksByStatus('In Progress').length}
            change="+2"
            trend="up"
            icon={KanbanIcon}
            color={designTokens.colors.chart.amber}
            subtext="being worked on"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Completed"
            value={getTasksByStatus('Completed').length}
            change="+8"
            trend="up"
            icon={CheckIcon}
            color={designTokens.colors.semantic.success}
            subtext="this week"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Team Members"
            value={employees.length}
            change="0"
            trend="neutral"
            icon={GroupIcon}
            color={designTokens.colors.chart.purple}
            subtext="active members"
          />
        </Grid>
      </Grid>

      {/* View Tabs and Filters */}
      <Card sx={{ mb: 3 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ p: 2 }}>
          <Tabs value={currentView} onChange={(e, v) => setCurrentView(v)}>
            <Tab value="kanban" label="Kanban Board" icon={<KanbanIcon />} iconPosition="start" />
            <Tab value="employees" label="Team" icon={<GroupIcon />} iconPosition="start" />
          </Tabs>

          {currentView === 'kanban' && (
            <Stack direction="row" spacing={2} alignItems="center">
              <FormControl size="small" sx={{ minWidth: 200 }}>
                <InputLabel>Project</InputLabel>
                <Select
                  value={selectedProject?.id || ''}
                  onChange={(e) => {
                    const project = projects.find((p) => p.id === e.target.value);
                    setSelectedProject(project || null);
                  }}
                  label="Project"
                >
                  {projects.map((project) => (
                    <MenuItem key={project.id} value={project.id}>
                      {project.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl size="small" sx={{ minWidth: 150 }}>
                <InputLabel>Filter</InputLabel>
                <Select
                  value={filter}
                  onChange={(e) => setFilter(e.target.value as 'all' | 'my_tasks')}
                  label="Filter"
                >
                  <MenuItem value="all">All Tasks</MenuItem>
                  <MenuItem value="my_tasks">My Tasks</MenuItem>
                </Select>
              </FormControl>
            </Stack>
          )}
        </Stack>
      </Card>

      {/* Kanban Board View */}
      {currentView === 'kanban' && (
        <DndContext
          sensors={sensors}
          collisionDetection={closestCorners}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >
          <Grid container spacing={2}>
            {KANBAN_COLUMNS.map((column) => (
              <Grid item xs={12} sm={6} md={3} key={column.id}>
                <KanbanColumn
                  column={column}
                  tasks={getTasksByStatus(column.status)}
                  employees={employees}
                  onEditTask={openEditTask}
                  onDeleteTask={deleteTask}
                  onAddTask={(status) => {
                    resetTaskForm();
                    setTaskForm((prev) => ({ ...prev, status: column.status }));
                    setEditingTask(null);
                    setTaskDialogOpen(true);
                  }}
                />
              </Grid>
            ))}
          </Grid>

          <DragOverlay>
            {activeTask && (
              <Card sx={{ p: 2, opacity: 0.8 }}>
                <Typography variant="subtitle2">{activeTask.name}</Typography>
              </Card>
            )}
          </DragOverlay>
        </DndContext>
      )}

      {/* Team View */}
      {currentView === 'employees' && (
        <Box>
          <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
            <Typography variant="h5">Team Members</Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              sx={{ background: designTokens.colors.workspace.operate }}
              onClick={() => setEmployeeDialogOpen(true)}
            >
              Add Member
            </Button>
          </Stack>

          <Grid container spacing={3}>
            {employees.map((employee) => {
              const employeeTasks = tasks.filter((t) => t.assigned_to?.includes(employee.id));
              const completedTasks = employeeTasks.filter((t) => t.status === 'Completed').length;

              return (
                <Grid item xs={12} sm={6} md={4} key={employee.id}>
                  <Card sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
                      <Avatar sx={{ bgcolor: employee.color, width: 48, height: 48, fontSize: 20 }}>
                        {employee.name.charAt(0)}
                      </Avatar>
                      <Box flex={1}>
                        <Typography variant="h6">{employee.name}</Typography>
                        <Typography variant="caption" color="text.secondary">
                          {employee.role}
                        </Typography>
                      </Box>
                    </Stack>

                    <Divider sx={{ my: 2 }} />

                    <Stack spacing={1}>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2" color="text.secondary">
                          Active Tasks
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {employeeTasks.length}
                        </Typography>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2" color="text.secondary">
                          Completed
                        </Typography>
                        <Typography variant="body2" fontWeight={600} color="success.main">
                          {completedTasks}
                        </Typography>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2" color="text.secondary">
                          In Progress
                        </Typography>
                        <Typography variant="body2" fontWeight={600} color="warning.main">
                          {employeeTasks.filter((t) => t.status === 'In Progress').length}
                        </Typography>
                      </Stack>
                    </Stack>

                    <Button
                      fullWidth
                      variant="outlined"
                      size="small"
                      sx={{ mt: 2 }}
                      onClick={() => {
                        setFilter('all');
                        setCurrentView('kanban');
                        // Could add specific filtering by employee
                      }}
                    >
                      View Tasks
                    </Button>
                  </Card>
                </Grid>
              );
            })}
          </Grid>
        </Box>
      )}

      {/* Task Dialog */}
      <Dialog open={taskDialogOpen} onClose={() => setTaskDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>{editingTask ? 'Edit Task' : 'New Task'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Task Name"
            value={taskForm.name}
            onChange={(e) => setTaskForm({ ...taskForm, name: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Description"
            value={taskForm.description}
            onChange={(e) => setTaskForm({ ...taskForm, description: e.target.value })}
            margin="normal"
            multiline
            rows={3}
          />
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <FormControl fullWidth margin="normal">
                <InputLabel>Status</InputLabel>
                <Select
                  value={taskForm.status}
                  onChange={(e) => setTaskForm({ ...taskForm, status: e.target.value })}
                  label="Status"
                >
                  {KANBAN_COLUMNS.map((col) => (
                    <MenuItem key={col.id} value={col.status}>
                      {col.title}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth margin="normal">
                <InputLabel>Priority</InputLabel>
                <Select
                  value={taskForm.priority}
                  onChange={(e) => setTaskForm({ ...taskForm, priority: e.target.value })}
                  label="Priority"
                >
                  {TASK_PRIORITIES.map((priority) => (
                    <MenuItem key={priority} value={priority}>
                      {priority}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
          <TextField
            fullWidth
            label="Due Date"
            type="date"
            value={taskForm.due_date}
            onChange={(e) => setTaskForm({ ...taskForm, due_date: e.target.value })}
            margin="normal"
            InputLabelProps={{ shrink: true }}
          />
          <Autocomplete
            multiple
            options={employees}
            getOptionLabel={(option) => option.name}
            value={employees.filter((emp) => taskForm.assigned_to.includes(emp.id))}
            onChange={(e, newValue) => {
              setTaskForm({ ...taskForm, assigned_to: newValue.map((emp) => emp.id) });
            }}
            renderInput={(params) => <TextField {...params} label="Assign To" margin="normal" />}
            renderOption={(props, option) => (
              <Box component="li" {...props}>
                <Avatar sx={{ width: 24, height: 24, mr: 1, bgcolor: option.color }}>
                  {option.name.charAt(0)}
                </Avatar>
                {option.name} - {option.role}
              </Box>
            )}
          />
          <Autocomplete
            multiple
            freeSolo
            options={[]}
            value={taskForm.tags}
            onChange={(e, newValue) => setTaskForm({ ...taskForm, tags: newValue })}
            renderInput={(params) => <TextField {...params} label="Tags" margin="normal" />}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTaskDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={editingTask ? () => updateTask(editingTask.id, taskForm) : createTask}
            variant="contained"
            disabled={!taskForm.name}
          >
            {editingTask ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Employee Dialog */}
      <Dialog open={employeeDialogOpen} onClose={() => setEmployeeDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Team Member</DialogTitle>
        <DialogContent>
          <TextField fullWidth label="Name" margin="normal" />
          <TextField fullWidth label="Email" type="email" margin="normal" />
          <FormControl fullWidth margin="normal">
            <InputLabel>Role</InputLabel>
            <Select label="Role">
              <MenuItem value="Developer">Developer</MenuItem>
              <MenuItem value="Designer">Designer</MenuItem>
              <MenuItem value="PM">Project Manager</MenuItem>
              <MenuItem value="QA">QA Engineer</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEmployeeDialogOpen(false)}>Cancel</Button>
          <Button variant="contained">Add Member</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ProjectTrackingDashboard;
