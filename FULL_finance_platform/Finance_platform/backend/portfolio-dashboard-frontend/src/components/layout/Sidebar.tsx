// src/components/layout/Sidebar.tsx
import React, { useState } from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  Toolbar,
  Typography,
  Box,
  Collapse,
  Badge,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Business as BusinessIcon,
  Description as DescriptionIcon,
  CloudUpload as CloudUploadIcon,
  Folder as FolderIcon,
  TableChart as TableChartIcon,
  Assessment as AssessmentIcon,
  HomeWork as HomeWorkIcon,
  Timeline as TimelineIcon,
  Settings as SettingsIcon,
  ShowChart as MarketDataIcon,
  ExpandLess,
  ExpandMore,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useUIStore } from '../../store/uiStore';

const DRAWER_WIDTH = 260;

interface MenuItem {
  text: string;
  icon: React.ReactElement;
  path?: string;
  badge?: number;
  children?: MenuItem[];
}

const menuSections = [
  {
    title: 'Overview',
    items: [
      { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
      { text: 'Portfolio Companies', icon: <BusinessIcon />, path: '/companies' },
    ],
  },
  {
    title: 'Financial Models',
    items: [
      { text: 'Model Generator', icon: <DescriptionIcon />, path: '/models' },
      { text: 'Real Estate', icon: <HomeWorkIcon />, path: '/real-estate' },
      { text: 'Property Management', icon: <HomeWorkIcon />, path: '/property-management' },
      { text: 'Corporate Finance', icon: <TimelineIcon />, path: '/finance-models' },
    ],
  },
  {
    title: 'Data & Analysis',
    items: [
      { text: 'Market Data', icon: <MarketDataIcon />, path: '/market-data' },
      { text: 'Financial Data Entry', icon: <TableChartIcon />, path: '/financials/data-entry' },
      {
        text: 'Documents',
        icon: <FolderIcon />,
        children: [
          { text: 'Upload & Extract', icon: <CloudUploadIcon />, path: '/documents/upload' },
          { text: 'Library', icon: <FolderIcon />, path: '/documents/library' },
        ],
      },
    ],
  },
  {
    title: 'Reporting',
    items: [
      { text: 'Reports', icon: <AssessmentIcon />, path: '/reports', badge: 2 },
    ],
  },
];

export const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { sidebarOpen } = useUIStore();
  const [expandedMenus, setExpandedMenus] = useState<string[]>(['Documents']);

  const handleToggleMenu = (text: string) => {
    setExpandedMenus((prev) =>
      prev.includes(text) ? prev.filter((item) => item !== text) : [...prev, text]
    );
  };

  const isSelected = (path?: string) => {
    if (!path) return false;
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  const renderMenuItem = (item: MenuItem, level: number = 0) => {
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedMenus.includes(item.text);
    const selected = isSelected(item.path);

    return (
      <React.Fragment key={item.text}>
        <ListItem disablePadding>
          <ListItemButton
            selected={selected}
            onClick={() => {
              if (hasChildren) {
                handleToggleMenu(item.text);
              } else if (item.path) {
                navigate(item.path);
              }
            }}
            sx={{
              pl: 2 + level * 2,
              borderLeft: selected ? '3px solid' : 'none',
              borderColor: 'primary.main',
              bgcolor: selected ? 'action.selected' : 'transparent',
            }}
          >
            <ListItemIcon sx={{ minWidth: 40, color: selected ? 'primary.main' : 'inherit' }}>
              {item.badge ? (
                <Badge badgeContent={item.badge} color="error">
                  {item.icon}
                </Badge>
              ) : (
                item.icon
              )}
            </ListItemIcon>
            <ListItemText
              primary={item.text}
              primaryTypographyProps={{
                variant: 'body2',
                fontWeight: selected ? 600 : 400,
              }}
            />
            {hasChildren && (isExpanded ? <ExpandLess /> : <ExpandMore />)}
          </ListItemButton>
        </ListItem>
        {hasChildren && (
          <Collapse in={isExpanded} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {item.children?.map((child) => renderMenuItem(child, level + 1))}
            </List>
          </Collapse>
        )}
      </React.Fragment>
    );
  };

  return (
    <Drawer
      variant="persistent"
      open={sidebarOpen}
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          borderRight: '1px solid',
          borderColor: 'divider',
        },
      }}
    >
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, pl: 1 }}>
          <Box
            sx={{
              width: 36,
              height: 36,
              borderRadius: 1.5,
              bgcolor: 'primary.main',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontWeight: 700,
              fontSize: 18,
            }}
          >
            PF
          </Box>
          <Typography variant="h6" sx={{ fontWeight: 700, fontSize: 16 }}>
            Portfolio Finance
          </Typography>
        </Box>
      </Toolbar>
      <Divider />
      <Box sx={{ overflowY: 'auto', flexGrow: 1 }}>
        {menuSections.map((section, index) => (
          <React.Fragment key={section.title}>
            <Box sx={{ px: 2, pt: 2, pb: 1 }}>
              <Typography
                variant="overline"
                sx={{
                  fontSize: 11,
                  fontWeight: 700,
                  color: 'text.secondary',
                  letterSpacing: 1,
                }}
              >
                {section.title}
              </Typography>
            </Box>
            <List>
              {section.items.map((item) => renderMenuItem(item))}
            </List>
            {index < menuSections.length - 1 && <Divider sx={{ my: 1 }} />}
          </React.Fragment>
        ))}
      </Box>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton
            selected={location.pathname === '/settings'}
            onClick={() => navigate('/settings')}
          >
            <ListItemIcon>
              <SettingsIcon />
            </ListItemIcon>
            <ListItemText primary="Settings" />
          </ListItemButton>
        </ListItem>
      </List>
    </Drawer>
  );
};
