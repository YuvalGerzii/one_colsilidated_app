/**
 * Project Tracking Widget - Compact Kanban for Main Dashboard
 *
 * @version 2.0.0
 * @created 2025-11-15
 * @description Compact project tracking widget with team and task management
 */
import React, { useState } from 'react';
import {
  Box,
  Card,
  Typography,
  Stack,
  IconButton,
  Chip,
  Avatar,
  AvatarGroup,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Autocomplete,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Checkbox,
  Grid,
  Divider,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  MoreVert as MoreIcon,
  DragIndicator as DragIcon,
  Flag as FlagIcon,
  CheckCircle as CheckIcon,
  Person as PersonIcon,
  Group as GroupIcon,
  CalendarToday as CalendarIcon,
  ViewKanban as KanbanIcon,
  KeyboardArrowRight as ArrowIcon,
} from '@mui/icons-material';
import { designTokens, alphaColor } from '../../theme/designTokens';

// Types
interface Employee {
  id: string;
  name: string;
  email: string;
  role: string;
  color: string;
}

interface SubTask {
  id: string;
  title: string;
  completed: boolean;
}

interface Task {
  id: string;
  name: string;
  description?: string;
  status: string;
  priority: string;
  due_date?: string;
  assigned_to: string[];
  subtasks: SubTask[];
}

const INITIAL_EMPLOYEES: Employee[] = [
  { id: '1', name: 'John Doe', email: 'john@example.com', role: 'Developer', color: '#3b82f6' },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'Designer', color: '#10b981' },
  { id: '3', name: 'Mike Johnson', email: 'mike@example.com', role: 'PM', color: '#f59e0b' },
];

const INITIAL_TASKS: Task[] = [
  {
    id: '1',
    name: 'Design new landing page',
    description: 'Create mockups for the new landing page with modern design',
    status: 'In Progress',
    priority: 'High',
    due_date: '2025-11-20',
    assigned_to: ['2'],
    subtasks: [
      { id: '1-1', title: 'Research competitors', completed: true },
      { id: '1-2', title: 'Create wireframes', completed: true },
      { id: '1-3', title: 'Design mockups', completed: false },
    ],
  },
  {
    id: '2',
    name: 'Implement user authentication',
    description: 'Add JWT-based authentication system',
    status: 'To Do',
    priority: 'Critical',
    due_date: '2025-11-18',
    assigned_to: ['1'],
    subtasks: [
      { id: '2-1', title: 'Setup JWT library', completed: false },
      { id: '2-2', title: 'Create login API', completed: false },
    ],
  },
  {
    id: '3',
    name: 'Write documentation',
    description: 'Update API documentation',
    status: 'In Review',
    priority: 'Medium',
    assigned_to: ['3'],
    subtasks: [],
  },
  {
    id: '4',
    name: 'Fix reported bugs',
    description: 'Address issues from QA testing',
    status: 'Done',
    priority: 'High',
    assigned_to: ['1', '2'],
    subtasks: [
      { id: '4-1', title: 'Fix login bug', completed: true },
      { id: '4-2', title: 'Fix UI alignment', completed: true },
    ],
  },
];

const KANBAN_COLUMNS = [
  { id: 'todo', title: 'To Do', status: 'To Do', color: designTokens.colors.chart.blue },
  { id: 'in_progress', title: 'In Progress', status: 'In Progress', color: designTokens.colors.chart.amber },
  { id: 'in_review', title: 'In Review', status: 'In Review', color: designTokens.colors.chart.purple },
  { id: 'done', title: 'Done', status: 'Done', color: designTokens.colors.semantic.success },
];

const PRIORITIES = ['Low', 'Medium', 'High', 'Critical'];

export const ProjectTrackingWidget: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>(INITIAL_TASKS);
  const [employees, setEmployees] = useState<Employee[]>(INITIAL_EMPLOYEES);
  const [taskDialogOpen, setTaskDialogOpen] = useState(false);
  const [employeeDialogOpen, setEmployeeDialogOpen] = useState(false);
  const [teamDialogOpen, setTeamDialogOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [newSubtask, setNewSubtask] = useState('');

  const [taskForm, setTaskForm] = useState({
    name: '',
    description: '',
    status: 'To Do',
    priority: 'Medium',
    due_date: '',
    assigned_to: [] as string[],
    subtasks: [] as SubTask[],
  });

  const [employeeForm, setEmployeeForm] = useState({
    name: '',
    email: '',
    role: '',
  });

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

  const getTasksByStatus = (status: string) => {
    return tasks.filter((t) => t.status === status);
  };

  const handleCreateTask = () => {
    const newTask: Task = {
      id: Date.now().toString(),
      name: taskForm.name,
      description: taskForm.description,
      status: taskForm.status,
      priority: taskForm.priority,
      due_date: taskForm.due_date,
      assigned_to: taskForm.assigned_to,
      subtasks: taskForm.subtasks,
    };
    setTasks([...tasks, newTask]);
    setTaskDialogOpen(false);
    resetTaskForm();
  };

  const handleUpdateTask = () => {
    if (!editingTask) return;
    setTasks(tasks.map((t) => (t.id === editingTask.id ? { ...editingTask, ...taskForm } : t)));
    setTaskDialogOpen(false);
    setEditingTask(null);
    resetTaskForm();
  };

  const handleDeleteTask = (taskId: string) => {
    if (window.confirm('Delete this task?')) {
      setTasks(tasks.filter((t) => t.id !== taskId));
    }
  };

  const handleAddEmployee = () => {
    const newEmployee: Employee = {
      id: Date.now().toString(),
      name: employeeForm.name,
      email: employeeForm.email,
      role: employeeForm.role,
      color: `#${Math.floor(Math.random() * 16777215).toString(16)}`,
    };
    setEmployees([...employees, newEmployee]);
    setEmployeeDialogOpen(false);
    setEmployeeForm({ name: '', email: '', role: '' });
  };

  const handleDeleteEmployee = (employeeId: string) => {
    if (window.confirm('Remove this team member?')) {
      setEmployees(employees.filter((e) => e.id !== employeeId));
      // Remove from assigned tasks
      setTasks(tasks.map((t) => ({ ...t, assigned_to: t.assigned_to.filter((id) => id !== employeeId) })));
    }
  };

  const resetTaskForm = () => {
    setTaskForm({
      name: '',
      description: '',
      status: 'To Do',
      priority: 'Medium',
      due_date: '',
      assigned_to: [],
      subtasks: [],
    });
  };

  const openEditTask = (task: Task) => {
    setEditingTask(task);
    setTaskForm({
      name: task.name,
      description: task.description || '',
      status: task.status,
      priority: task.priority,
      due_date: task.due_date || '',
      assigned_to: task.assigned_to,
      subtasks: task.subtasks,
    });
    setTaskDialogOpen(true);
  };

  const addSubtask = () => {
    if (!newSubtask.trim()) return;
    setTaskForm({
      ...taskForm,
      subtasks: [...taskForm.subtasks, { id: Date.now().toString(), title: newSubtask, completed: false }],
    });
    setNewSubtask('');
  };

  const toggleSubtask = (subtaskId: string) => {
    setTaskForm({
      ...taskForm,
      subtasks: taskForm.subtasks.map((st) => (st.id === subtaskId ? { ...st, completed: !st.completed } : st)),
    });
  };

  const removeSubtask = (subtaskId: string) => {
    setTaskForm({
      ...taskForm,
      subtasks: taskForm.subtasks.filter((st) => st.id !== subtaskId),
    });
  };

  const completedSubtasks = (task: Task) => task.subtasks.filter((st) => st.completed).length;

  return (
    <Card sx={{ p: 3, height: '100%' }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
        <Stack direction="row" spacing={2} alignItems="center">
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: designTokens.radius.md,
              background: designTokens.colors.workspace.operate,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <KanbanIcon sx={{ fontSize: 20, color: 'white' }} />
          </Box>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Project Tracking
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {tasks.length} tasks · {employees.length} team members
            </Typography>
          </Box>
        </Stack>

        <Stack direction="row" spacing={1}>
          <Tooltip title="Manage Team">
            <IconButton
              size="small"
              onClick={() => setTeamDialogOpen(true)}
              sx={{
                bgcolor: alphaColor(designTokens.colors.chart.purple, 0.1),
                '&:hover': { bgcolor: alphaColor(designTokens.colors.chart.purple, 0.2) },
              }}
            >
              <GroupIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Button
            size="small"
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {
              resetTaskForm();
              setEditingTask(null);
              setTaskDialogOpen(true);
            }}
            sx={{ bgcolor: designTokens.colors.workspace.operate }}
          >
            Add Task
          </Button>
        </Stack>
      </Stack>

      {/* Compact Kanban Board */}
      <Grid container spacing={2}>
        {KANBAN_COLUMNS.map((column) => {
          const columnTasks = getTasksByStatus(column.status);
          return (
            <Grid item xs={12} sm={6} md={3} key={column.id}>
              <Box
                sx={{
                  bgcolor: alphaColor(column.color, 0.05),
                  borderRadius: designTokens.radius.md,
                  p: 1.5,
                  border: `1px solid ${alphaColor(column.color, 0.1)}`,
                }}
              >
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1.5 }}>
                  <Stack direction="row" spacing={0.5} alignItems="center">
                    <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: column.color }} />
                    <Typography variant="caption" sx={{ fontWeight: 600, fontSize: 11 }}>
                      {column.title}
                    </Typography>
                    <Chip label={columnTasks.length} size="small" sx={{ height: 16, fontSize: 10 }} />
                  </Stack>
                </Stack>

                <Stack spacing={1}>
                  {columnTasks.map((task) => {
                    const assignedEmps = employees.filter((emp) => task.assigned_to.includes(emp.id));
                    const subtaskProgress =
                      task.subtasks.length > 0 ? `${completedSubtasks(task)}/${task.subtasks.length}` : null;

                    return (
                      <Card
                        key={task.id}
                        sx={{
                          p: 1.5,
                          cursor: 'pointer',
                          '&:hover': {
                            boxShadow: `0 2px 8px ${alphaColor(designTokens.colors.chart.blue, 0.15)}`,
                          },
                        }}
                        onClick={() => openEditTask(task)}
                      >
                        <Typography variant="caption" sx={{ fontWeight: 600, fontSize: 11, display: 'block', mb: 0.5 }}>
                          {task.name}
                        </Typography>

                        <Stack direction="row" spacing={0.5} alignItems="center" justifyContent="space-between">
                          <Stack direction="row" spacing={0.5} alignItems="center">
                            <Chip
                              icon={<FlagIcon sx={{ fontSize: 10 }} />}
                              label={task.priority}
                              size="small"
                              sx={{
                                height: 16,
                                fontSize: 9,
                                bgcolor: alphaColor(getPriorityColor(task.priority), 0.1),
                                color: getPriorityColor(task.priority),
                                '& .MuiChip-icon': { fontSize: 10, ml: 0.5 },
                              }}
                            />
                            {subtaskProgress && (
                              <Chip
                                icon={<CheckIcon sx={{ fontSize: 10 }} />}
                                label={subtaskProgress}
                                size="small"
                                sx={{ height: 16, fontSize: 9 }}
                              />
                            )}
                          </Stack>

                          {assignedEmps.length > 0 && (
                            <AvatarGroup max={2} sx={{ '& .MuiAvatar-root': { width: 16, height: 16, fontSize: 8 } }}>
                              {assignedEmps.map((emp) => (
                                <Tooltip key={emp.id} title={emp.name}>
                                  <Avatar sx={{ bgcolor: emp.color }}>{emp.name.charAt(0)}</Avatar>
                                </Tooltip>
                              ))}
                            </AvatarGroup>
                          )}
                        </Stack>
                      </Card>
                    );
                  })}
                </Stack>
              </Box>
            </Grid>
          );
        })}
      </Grid>

      {/* Task Dialog */}
      <Dialog open={taskDialogOpen} onClose={() => setTaskDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>{editingTask ? 'Edit Task' : 'New Task'}</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 1 }}>
            <TextField
              fullWidth
              label="Task Name"
              value={taskForm.name}
              onChange={(e) => setTaskForm({ ...taskForm, name: e.target.value })}
              required
            />

            <TextField
              fullWidth
              label="Description"
              value={taskForm.description}
              onChange={(e) => setTaskForm({ ...taskForm, description: e.target.value })}
              multiline
              rows={3}
            />

            <Grid container spacing={2}>
              <Grid item xs={6}>
                <FormControl fullWidth>
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
                <FormControl fullWidth>
                  <InputLabel>Priority</InputLabel>
                  <Select
                    value={taskForm.priority}
                    onChange={(e) => setTaskForm({ ...taskForm, priority: e.target.value })}
                    label="Priority"
                  >
                    {PRIORITIES.map((priority) => (
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
              renderInput={(params) => <TextField {...params} label="Assign To" />}
              renderOption={(props, option) => (
                <Box component="li" {...props}>
                  <Avatar sx={{ width: 20, height: 20, mr: 1, bgcolor: option.color, fontSize: 12 }}>
                    {option.name.charAt(0)}
                  </Avatar>
                  {option.name} - {option.role}
                </Box>
              )}
            />

            <Divider />

            {/* Subtasks Section */}
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Subtasks
            </Typography>

            <Stack direction="row" spacing={1}>
              <TextField
                fullWidth
                size="small"
                placeholder="Add a subtask..."
                value={newSubtask}
                onChange={(e) => setNewSubtask(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    addSubtask();
                  }
                }}
              />
              <Button onClick={addSubtask} variant="outlined" size="small">
                Add
              </Button>
            </Stack>

            {taskForm.subtasks.length > 0 && (
              <List dense>
                {taskForm.subtasks.map((subtask) => (
                  <ListItem
                    key={subtask.id}
                    secondaryAction={
                      <IconButton edge="end" size="small" onClick={() => removeSubtask(subtask.id)}>
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    }
                  >
                    <ListItemIcon>
                      <Checkbox
                        edge="start"
                        checked={subtask.completed}
                        onChange={() => toggleSubtask(subtask.id)}
                        size="small"
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={subtask.title}
                      sx={{ textDecoration: subtask.completed ? 'line-through' : 'none' }}
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </Stack>
        </DialogContent>
        <DialogActions>
          {editingTask && (
            <Button onClick={() => handleDeleteTask(editingTask.id)} color="error" sx={{ mr: 'auto' }}>
              Delete Task
            </Button>
          )}
          <Button onClick={() => setTaskDialogOpen(false)}>Cancel</Button>
          <Button onClick={editingTask ? handleUpdateTask : handleCreateTask} variant="contained" disabled={!taskForm.name}>
            {editingTask ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Team Management Dialog */}
      <Dialog open={teamDialogOpen} onClose={() => setTeamDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">Team Members</Typography>
            <Button size="small" startIcon={<AddIcon />} onClick={() => setEmployeeDialogOpen(true)}>
              Add Member
            </Button>
          </Stack>
        </DialogTitle>
        <DialogContent>
          <List>
            {employees.map((employee) => (
              <ListItem
                key={employee.id}
                secondaryAction={
                  <IconButton edge="end" onClick={() => handleDeleteEmployee(employee.id)}>
                    <DeleteIcon />
                  </IconButton>
                }
              >
                <ListItemIcon>
                  <Avatar sx={{ bgcolor: employee.color, width: 32, height: 32 }}>{employee.name.charAt(0)}</Avatar>
                </ListItemIcon>
                <ListItemText primary={employee.name} secondary={`${employee.role} · ${employee.email}`} />
              </ListItem>
            ))}
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTeamDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Add Employee Dialog */}
      <Dialog open={employeeDialogOpen} onClose={() => setEmployeeDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Team Member</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ mt: 1 }}>
            <TextField
              fullWidth
              label="Name"
              value={employeeForm.name}
              onChange={(e) => setEmployeeForm({ ...employeeForm, name: e.target.value })}
            />
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={employeeForm.email}
              onChange={(e) => setEmployeeForm({ ...employeeForm, email: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Role</InputLabel>
              <Select
                value={employeeForm.role}
                onChange={(e) => setEmployeeForm({ ...employeeForm, role: e.target.value })}
                label="Role"
              >
                <MenuItem value="Developer">Developer</MenuItem>
                <MenuItem value="Designer">Designer</MenuItem>
                <MenuItem value="PM">Project Manager</MenuItem>
                <MenuItem value="QA">QA Engineer</MenuItem>
                <MenuItem value="Other">Other</MenuItem>
              </Select>
            </FormControl>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEmployeeDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleAddEmployee}
            variant="contained"
            disabled={!employeeForm.name || !employeeForm.email || !employeeForm.role}
          >
            Add Member
          </Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
};
