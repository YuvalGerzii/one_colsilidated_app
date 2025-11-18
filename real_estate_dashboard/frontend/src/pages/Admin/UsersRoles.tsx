/**
 * UsersRoles Component - User and role management
 *
 * @version 1.2.0
 * @created 2025-11-15
 * @updated 2025-11-15
 * @description Manage users, roles, and permissions with real database API integration
 */
import React, { useState, useEffect } from 'react';
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
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  FormControlLabel,
  Tabs,
  Tab,
  Tooltip,
  Avatar,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Checkbox,
  CircularProgress,
} from '@mui/material';
import {
  People as PeopleIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Security as SecurityIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
  AdminPanelSettings as AdminIcon,
  PersonAdd as InviteIcon,
} from '@mui/icons-material';
import { designTokens, alphaColor } from '../../theme/designTokens';
import { MetricCard } from '../../components/ui/MetricCard';
import { apiClient } from '../../services/apiClient';
import { useSnackbar } from 'notistack';

interface User {
  id: string;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  company_id?: string;
  is_active: boolean;
  is_verified: boolean;
  is_superuser: boolean;
  last_login?: string;
  created_at: string;
  updated_at: string;
}

interface UserFormData {
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  password?: string;
  company_id?: string;
  is_active?: boolean;
  is_verified?: boolean;
  is_superuser?: boolean;
}

interface Role {
  id: string;
  name: string;
  description: string;
  userCount: number;
  permissions: string[];
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index } = props;
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

const AVAILABLE_PERMISSIONS = [
  'view_properties',
  'edit_properties',
  'delete_properties',
  'view_deals',
  'edit_deals',
  'delete_deals',
  'view_reports',
  'create_reports',
  'view_users',
  'manage_users',
  'manage_roles',
  'view_analytics',
  'export_data',
  'manage_integrations',
  'system_settings',
];

export const UsersRoles: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [tabValue, setTabValue] = useState(0);
  const [userDialogOpen, setUserDialogOpen] = useState(false);
  const [roleDialogOpen, setRoleDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState<UserFormData>({
    email: '',
    username: '',
    first_name: '',
    last_name: '',
    password: '',
    is_active: true,
    is_verified: false,
    is_superuser: false,
  });

  // Mock roles data (will be connected to API later if roles table is created)
  const [roles] = useState<Role[]>([
    {
      id: '1',
      name: 'Admin',
      description: 'Full system access',
      userCount: 0,
      permissions: AVAILABLE_PERMISSIONS,
    },
    {
      id: '2',
      name: 'Editor',
      description: 'Can view and edit content',
      userCount: 0,
      permissions: ['view_properties', 'edit_properties', 'view_deals', 'edit_deals', 'view_reports', 'create_reports'],
    },
    {
      id: '3',
      name: 'Viewer',
      description: 'Read-only access',
      userCount: 0,
      permissions: ['view_properties', 'view_deals', 'view_reports', 'view_analytics'],
    },
  ]);

  // Fetch users from API
  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<User[]>('/users/');
      setUsers(response || []);
    } catch (error) {
      console.error('Error fetching users:', error);
      enqueueSnackbar('Failed to load users', { variant: 'error' });
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  // Load users on mount
  useEffect(() => {
    fetchUsers();
  }, []);

  // Create or update user
  const handleSaveUser = async () => {
    try {
      if (selectedUser) {
        // Update existing user
        await apiClient.put(`/users/${selectedUser.id}`, formData);
        enqueueSnackbar('User updated successfully', { variant: 'success' });
      } else {
        // Create new user
        if (!formData.password || formData.password.length < 8) {
          enqueueSnackbar('Password must be at least 8 characters', { variant: 'error' });
          return;
        }
        await apiClient.post('/users/', formData);
        enqueueSnackbar('User created successfully', { variant: 'success' });
      }

      setUserDialogOpen(false);
      setSelectedUser(null);
      setFormData({
        email: '',
        username: '',
        first_name: '',
        last_name: '',
        password: '',
        is_active: true,
        is_verified: false,
        is_superuser: false,
      });
      fetchUsers();
    } catch (error: any) {
      console.error('Error saving user:', error);
      const errorMessage = error?.response?.data?.detail || 'Failed to save user';
      enqueueSnackbar(errorMessage, { variant: 'error' });
    }
  };

  // Delete user
  const handleDeleteUser = async (userId: string) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return;
    }

    try {
      await apiClient.delete(`/users/${userId}`);
      enqueueSnackbar('User deleted successfully', { variant: 'success' });
      fetchUsers();
    } catch (error: any) {
      console.error('Error deleting user:', error);
      const errorMessage = error?.response?.data?.detail || 'Failed to delete user';
      enqueueSnackbar(errorMessage, { variant: 'error' });
    }
  };

  // Toggle user active status
  const handleToggleUserStatus = async (user: User) => {
    try {
      const endpoint = user.is_active ? 'deactivate' : 'activate';
      await apiClient.patch(`/users/${user.id}/${endpoint}`);
      enqueueSnackbar(`User ${user.is_active ? 'deactivated' : 'activated'} successfully`, { variant: 'success' });
      fetchUsers();
    } catch (error: any) {
      console.error('Error toggling user status:', error);
      const errorMessage = error?.response?.data?.detail || 'Failed to update user status';
      enqueueSnackbar(errorMessage, { variant: 'error' });
    }
  };

  // Toggle admin privileges
  const handleToggleAdmin = async (user: User) => {
    try {
      const endpoint = user.is_superuser ? 'remove-admin' : 'make-admin';
      await apiClient.patch(`/users/${user.id}/${endpoint}`);
      enqueueSnackbar(`Admin privileges ${user.is_superuser ? 'removed' : 'granted'}`, { variant: 'success' });
      fetchUsers();
    } catch (error: any) {
      console.error('Error toggling admin privileges:', error);
      const errorMessage = error?.response?.data?.detail || 'Failed to update admin privileges';
      enqueueSnackbar(errorMessage, { variant: 'error' });
    }
  };

  // Open dialog for create/edit
  const openUserDialog = (user?: User) => {
    if (user) {
      setSelectedUser(user);
      setFormData({
        email: user.email,
        username: user.username,
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        is_active: user.is_active,
        is_verified: user.is_verified,
        is_superuser: user.is_superuser,
      });
    } else {
      setSelectedUser(null);
      setFormData({
        email: '',
        username: '',
        first_name: '',
        last_name: '',
        password: '',
        is_active: true,
        is_verified: false,
        is_superuser: false,
      });
    }
    setUserDialogOpen(true);
  };

  const getRoleFromUser = (user: User): string => {
    if (user.is_superuser) return 'Admin';
    if (user.is_verified) return 'Editor';
    return 'Viewer';
  };

  const getRoleColor = (user: User): string => {
    const role = getRoleFromUser(user);
    const colorMap: Record<string, string> = {
      Admin: designTokens.colors.semantic.error,
      Editor: designTokens.colors.chart.amber,
      Viewer: designTokens.colors.chart.blue,
    };
    return colorMap[role] || designTokens.colors.chart.blue;
  };

  const getUserDisplayName = (user: User): string => {
    if (user.first_name && user.last_name) {
      return `${user.first_name} ${user.last_name}`;
    }
    return user.username;
  };

  const adminCount = users.filter(u => u.is_superuser).length;
  const activeCount = users.filter(u => u.is_active).length;

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
            <PeopleIcon sx={{ fontSize: 28, color: 'white' }} />
          </Box>
          <Box flex={1}>
            <Typography variant="h4" sx={{ fontWeight: designTokens.typography.fontWeight.bold }}>
              Users & Roles
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage user accounts and permission roles
            </Typography>
          </Box>
          <Button
            variant="contained"
            startIcon={<InviteIcon />}
            sx={{ background: designTokens.colors.workspace.admin }}
            onClick={() => openUserDialog()}
          >
            Add User
          </Button>
        </Stack>
      </Box>

      {/* Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Total Users"
            value={users.length}
            change="+3"
            trend="up"
            icon={PeopleIcon}
            color={designTokens.colors.chart.blue}
            subtext="registered"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Active Users"
            value={activeCount}
            change="+2"
            trend="up"
            icon={ActiveIcon}
            color={designTokens.colors.semantic.success}
            subtext="currently active"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Roles Defined"
            value={roles.length}
            change="0"
            trend="neutral"
            icon={SecurityIcon}
            color={designTokens.colors.chart.purple}
            subtext="permission groups"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Admin Users"
            value={adminCount}
            change="0"
            trend="neutral"
            icon={AdminIcon}
            color={designTokens.colors.semantic.error}
            subtext="full access"
          />
        </Grid>
      </Grid>

      {/* Tabs */}
      <Card sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label="Users" icon={<PeopleIcon />} iconPosition="start" />
          <Tab label="Roles" icon={<SecurityIcon />} iconPosition="start" />
        </Tabs>
      </Card>

      {/* Users Tab */}
      <TabPanel value={tabValue} index={0}>
        <Card>
          <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
            <Stack direction="row" spacing={2} alignItems="center">
              <TextField
                size="small"
                placeholder="Search users..."
                sx={{ flexGrow: 1 }}
              />
              <Button variant="contained" startIcon={<AddIcon />} onClick={() => openUserDialog()}>
                Add User
              </Button>
            </Stack>
          </Box>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>User</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Role</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Last Login</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center" sx={{ py: 8 }}>
                      <CircularProgress />
                    </TableCell>
                  </TableRow>
                ) : users.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center" sx={{ py: 8 }}>
                      <Typography variant="body2" color="text.secondary">
                        No users found. Click "Add User" to create one.
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  users.map((user) => (
                    <TableRow key={user.id} hover>
                      <TableCell>
                        <Stack direction="row" spacing={2} alignItems="center">
                          <Avatar sx={{ bgcolor: getRoleColor(user) }}>
                            {user.username.charAt(0).toUpperCase()}
                          </Avatar>
                          <Box>
                            <Typography variant="body2" fontWeight={600}>
                              {getUserDisplayName(user)}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              @{user.username}
                            </Typography>
                          </Box>
                        </Stack>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{user.email}</Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={getRoleFromUser(user)}
                          size="small"
                          sx={{
                            background: alphaColor(getRoleColor(user), 0.1),
                            color: getRoleColor(user),
                            fontWeight: 600,
                          }}
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          icon={user.is_active ? <ActiveIcon fontSize="small" /> : <InactiveIcon fontSize="small" />}
                          label={user.is_active ? 'Active' : 'Inactive'}
                          size="small"
                          color={user.is_active ? 'success' : 'default'}
                          onClick={() => handleToggleUserStatus(user)}
                          sx={{ cursor: 'pointer' }}
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Tooltip title={user.is_superuser ? 'Remove Admin' : 'Make Admin'}>
                          <IconButton
                            size="small"
                            color={user.is_superuser ? 'error' : 'default'}
                            onClick={() => handleToggleAdmin(user)}
                          >
                            <AdminIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Edit">
                          <IconButton size="small" onClick={() => openUserDialog(user)}>
                            <EditIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete">
                          <IconButton size="small" color="error" onClick={() => handleDeleteUser(user.id)}>
                            <DeleteIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </Card>
      </TabPanel>

      {/* Roles Tab */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          {roles.map((role) => (
            <Grid item xs={12} md={4} key={role.id}>
              <Card sx={{ p: 3, height: '100%' }}>
                <Stack spacing={2}>
                  <Stack direction="row" justifyContent="space-between" alignItems="start">
                    <Box>
                      <Typography variant="h6" fontWeight={700}>
                        {role.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {role.description}
                      </Typography>
                    </Box>
                    <IconButton size="small" onClick={() => {
                      setSelectedRole(role);
                      setRoleDialogOpen(true);
                    }}>
                      <EditIcon fontSize="small" />
                    </IconButton>
                  </Stack>
                  <Box>
                    <Typography variant="caption" color="text.secondary">
                      Users with this role
                    </Typography>
                    <Typography variant="h4" fontWeight={700}>
                      {role.name === 'Admin' ? adminCount : role.name === 'Viewer' ? users.filter(u => !u.is_superuser && !u.is_verified).length : users.filter(u => !u.is_superuser && u.is_verified).length}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                      Permissions ({role.permissions.length})
                    </Typography>
                    <Stack direction="row" spacing={0.5} flexWrap="wrap" gap={0.5}>
                      {role.permissions.slice(0, 3).map((perm) => (
                        <Chip
                          key={perm}
                          label={perm.replace('_', ' ')}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                      {role.permissions.length > 3 && (
                        <Chip
                          label={`+${role.permissions.length - 3} more`}
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Stack>
                  </Box>
                </Stack>
              </Card>
            </Grid>
          ))}
          <Grid item xs={12} md={4}>
            <Card
              sx={{
                p: 3,
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: `2px dashed ${designTokens.colors.chart.blue}`,
                background: alphaColor(designTokens.colors.chart.blue, 0.05),
                cursor: 'pointer',
                '&:hover': {
                  background: alphaColor(designTokens.colors.chart.blue, 0.1),
                },
              }}
              onClick={() => setRoleDialogOpen(true)}
            >
              <Stack alignItems="center" spacing={2}>
                <AddIcon sx={{ fontSize: 48, color: designTokens.colors.chart.blue }} />
                <Typography color="primary" fontWeight={600}>
                  Create New Role
                </Typography>
              </Stack>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Edit User Dialog */}
      <Dialog open={userDialogOpen} onClose={() => setUserDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedUser ? 'Edit User' : 'Add User'}
        </DialogTitle>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 1 }}>
            <TextField
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              fullWidth
              required
            />
            <TextField
              label="Username"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              fullWidth
              required
            />
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="First Name"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Last Name"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  fullWidth
                />
              </Grid>
            </Grid>
            {!selectedUser && (
              <TextField
                label="Password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                fullWidth
                required
                helperText="Minimum 8 characters"
              />
            )}
            <FormControlLabel
              control={
                <Switch
                  checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                />
              }
              label="Active"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={formData.is_verified}
                  onChange={(e) => setFormData({ ...formData, is_verified: e.target.checked })}
                />
              }
              label="Verified"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={formData.is_superuser}
                  onChange={(e) => setFormData({ ...formData, is_superuser: e.target.checked })}
                />
              }
              label="Admin Privileges"
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUserDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleSaveUser}
            disabled={!formData.email || !formData.username}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Role Dialog */}
      <Dialog open={roleDialogOpen} onClose={() => setRoleDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedRole ? 'Edit Role' : 'Create Role'}
        </DialogTitle>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 1 }}>
            <TextField label="Role Name" defaultValue={selectedRole?.name} fullWidth />
            <TextField
              label="Description"
              defaultValue={selectedRole?.description}
              multiline
              rows={2}
              fullWidth
            />
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Permissions
              </Typography>
              <List>
                {AVAILABLE_PERMISSIONS.map((permission) => (
                  <ListItem key={permission} dense>
                    <ListItemIcon>
                      <Checkbox
                        edge="start"
                        defaultChecked={selectedRole?.permissions.includes(permission)}
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={permission.replace('_', ' ').toUpperCase()}
                      secondary={`Allow ${permission.replace('_', ' ')}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRoleDialogOpen(false)}>Cancel</Button>
          <Button variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UsersRoles;
