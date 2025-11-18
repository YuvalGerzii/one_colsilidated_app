// src/components/layout/Header.tsx
import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Badge,
  Menu,
  MenuItem,
  Divider,
  ListItemIcon,
  ListItemText,
  Box,
  Avatar,
  Tooltip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  AccountCircle,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useUIStore } from '../../store/uiStore';

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { toggleSidebar } = useUIStore();

  const [userMenuAnchor, setUserMenuAnchor] = useState<null | HTMLElement>(null);
  const [notificationsAnchor, setNotificationsAnchor] = useState<null | HTMLElement>(null);

  const handleUserMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setUserMenuAnchor(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setUserMenuAnchor(null);
  };

  const handleNotificationsOpen = (event: React.MouseEvent<HTMLElement>) => {
    setNotificationsAnchor(event.currentTarget);
  };

  const handleNotificationsClose = () => {
    setNotificationsAnchor(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
    handleUserMenuClose();
  };

  // Get page title from current route
  const getPageTitle = () => {
    const path = location.pathname;
    if (path.includes('/dashboard')) return 'Dashboard';
    if (path.includes('/companies')) return 'Portfolio Companies';
    if (path.includes('/models')) return 'Model Generator';
    if (path.includes('/real-estate')) return 'Real Estate Models';
    if (path.includes('/finance-models')) return 'Corporate Finance';
    if (path.includes('/market-data')) return 'Market Data';
    if (path.includes('/documents/upload')) return 'Document Extraction';
    if (path.includes('/documents/library')) return 'Documents Library';
    if (path.includes('/financials')) return 'Financial Data Entry';
    if (path.includes('/reports')) return 'Reports';
    if (path.includes('/settings')) return 'Settings';
    return 'Portfolio Dashboard';
  };

  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="toggle sidebar"
          edge="start"
          onClick={toggleSidebar}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h6" noWrap component="div">
            {getPageTitle()}
          </Typography>
        </Box>

        {/* Notifications */}
        <Tooltip title="Notifications">
          <IconButton color="inherit" onClick={handleNotificationsOpen} sx={{ mr: 1 }}>
            <Badge badgeContent={3} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Tooltip>

        {/* User Menu */}
        <Tooltip title="Account">
          <IconButton color="inherit" onClick={handleUserMenuOpen}>
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.dark' }}>
              <AccountCircle />
            </Avatar>
          </IconButton>
        </Tooltip>

        {/* Notifications Menu */}
        <Menu
          anchorEl={notificationsAnchor}
          open={Boolean(notificationsAnchor)}
          onClose={handleNotificationsClose}
          PaperProps={{
            sx: { width: 320, maxHeight: 400 },
          }}
        >
          <Box sx={{ px: 2, py: 1.5 }}>
            <Typography variant="h6">Notifications</Typography>
          </Box>
          <Divider />
          <MenuItem onClick={handleNotificationsClose}>
            <ListItemText
              primary="Portfolio update completed"
              secondary="5 minutes ago"
              primaryTypographyProps={{ variant: 'body2' }}
              secondaryTypographyProps={{ variant: 'caption' }}
            />
          </MenuItem>
          <MenuItem onClick={handleNotificationsClose}>
            <ListItemText
              primary="New market data available"
              secondary="2 hours ago"
              primaryTypographyProps={{ variant: 'body2' }}
              secondaryTypographyProps={{ variant: 'caption' }}
            />
          </MenuItem>
          <MenuItem onClick={handleNotificationsClose}>
            <ListItemText
              primary="Quarterly report generated"
              secondary="1 day ago"
              primaryTypographyProps={{ variant: 'body2' }}
              secondaryTypographyProps={{ variant: 'caption' }}
            />
          </MenuItem>
        </Menu>

        {/* User Menu */}
        <Menu
          anchorEl={userMenuAnchor}
          open={Boolean(userMenuAnchor)}
          onClose={handleUserMenuClose}
          PaperProps={{
            sx: { width: 220 },
          }}
        >
          <Box sx={{ px: 2, py: 1.5 }}>
            <Typography variant="subtitle2">John Doe</Typography>
            <Typography variant="caption" color="text.secondary">
              john.doe@example.com
            </Typography>
          </Box>
          <Divider />
          <MenuItem
            onClick={() => {
              navigate('/settings');
              handleUserMenuClose();
            }}
          >
            <ListItemIcon>
              <PersonIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Profile</ListItemText>
          </MenuItem>
          <MenuItem
            onClick={() => {
              navigate('/settings');
              handleUserMenuClose();
            }}
          >
            <ListItemIcon>
              <SettingsIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Settings</ListItemText>
          </MenuItem>
          <Divider />
          <MenuItem onClick={handleLogout}>
            <ListItemIcon>
              <LogoutIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Logout</ListItemText>
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};
