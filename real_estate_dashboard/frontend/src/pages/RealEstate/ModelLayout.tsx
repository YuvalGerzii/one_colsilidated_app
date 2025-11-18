import React, { useState } from 'react';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  useTheme,
  useMediaQuery,
  IconButton,
  Divider,
} from '@mui/material';
import {
  Home as HomeIcon,
  HomeWork as HomeWorkIcon,
  Apartment as ApartmentIcon,
  Hotel as HotelIcon,
  Business as BusinessIcon,
  Menu as MenuIcon,
  Domain as DomainIcon,
  Description as DescriptionIcon,
  Build as BuildIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const DRAWER_WIDTH = 280;

interface ModelItem {
  id: string;
  label: string;
  icon: React.ReactElement;
  path: string;
  color: string;
}

const MODEL_ITEMS: ModelItem[] = [
  {
    id: 'fix_and_flip',
    label: 'Fix & Flip',
    icon: <HomeIcon />,
    path: '/real-estate-models/fix-and-flip',
    color: '#1976d2',
  },
  {
    id: 'single_family_rental',
    label: 'Single Family Rental',
    icon: <HomeWorkIcon />,
    path: '/real-estate-models/single-family-rental',
    color: '#2e7d32',
  },
  {
    id: 'small_multifamily',
    label: 'Small Multifamily',
    icon: <ApartmentIcon />,
    path: '/real-estate-models/small-multifamily',
    color: '#9c27b0',
  },
  {
    id: 'extended_multifamily',
    label: 'High-Rise Multifamily',
    icon: <DomainIcon />,
    path: '/real-estate-models/extended-multifamily',
    color: '#7b1fa2',
  },
  {
    id: 'hotel',
    label: 'Hotel',
    icon: <HotelIcon />,
    path: '/real-estate-models/hotel',
    color: '#ed6c00',
  },
  {
    id: 'mixed_use',
    label: 'Mixed-Use',
    icon: <BusinessIcon />,
    path: '/real-estate-models/mixed-use',
    color: '#1565c0',
  },
  {
    id: 'lease_analyzer',
    label: 'Lease Analyzer',
    icon: <DescriptionIcon />,
    path: '/real-estate-models/lease-analyzer',
    color: '#0288d1',
  },
  {
    id: 'renovation_budget',
    label: 'Renovation Budget',
    icon: <BuildIcon />,
    path: '/real-estate-models/renovation-budget',
    color: '#f57c00',
  },
];

interface ModelLayoutProps {
  children: React.ReactNode;
}

export const ModelLayout: React.FC<ModelLayoutProps> = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      setMobileOpen(false);
    }
  };

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Toolbar>
        <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 600 }}>
          Real Estate Models
        </Typography>
      </Toolbar>
      <Divider />
      <List sx={{ px: 1, py: 2 }}>
        {MODEL_ITEMS.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <ListItem key={item.id} disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                onClick={() => handleNavigation(item.path)}
                sx={{
                  borderRadius: 2,
                  backgroundColor: isActive ? `${item.color}15` : 'transparent',
                  '&:hover': {
                    backgroundColor: isActive ? `${item.color}25` : 'rgba(255, 255, 255, 0.05)',
                  },
                  transition: 'all 0.2s',
                }}
              >
                <ListItemIcon
                  sx={{
                    color: isActive ? item.color : 'inherit',
                    minWidth: 40,
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.label}
                  primaryTypographyProps={{
                    fontWeight: isActive ? 600 : 400,
                    color: isActive ? item.color : 'inherit',
                  }}
                />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: 'calc(100vh - 64px)' }}>
      {/* Mobile drawer toggle */}
      {isMobile && (
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={handleDrawerToggle}
          sx={{
            position: 'fixed',
            top: 72,
            left: 16,
            zIndex: theme.zIndex.drawer + 1,
            backgroundColor: 'background.paper',
            boxShadow: 2,
            '&:hover': {
              backgroundColor: 'background.paper',
            },
          }}
        >
          <MenuIcon />
        </IconButton>
      )}

      {/* Sidebar */}
      <Box
        component="nav"
        sx={{ width: { md: DRAWER_WIDTH }, flexShrink: { md: 0 } }}
      >
        {isMobile ? (
          <Drawer
            variant="temporary"
            open={mobileOpen}
            onClose={handleDrawerToggle}
            ModalProps={{
              keepMounted: true, // Better open performance on mobile.
            }}
            sx={{
              '& .MuiDrawer-paper': {
                boxSizing: 'border-box',
                width: DRAWER_WIDTH,
                mt: '64px',
                height: 'calc(100% - 64px)',
              },
            }}
          >
            {drawer}
          </Drawer>
        ) : (
          <Drawer
            variant="permanent"
            sx={{
              '& .MuiDrawer-paper': {
                boxSizing: 'border-box',
                width: DRAWER_WIDTH,
                mt: '64px',
                height: 'calc(100% - 64px)',
                borderRight: '1px solid',
                borderColor: 'divider',
              },
            }}
            open
          >
            {drawer}
          </Drawer>
        )}
      </Box>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${DRAWER_WIDTH}px)` },
          ml: { xs: 0, md: 0 },
        }}
      >
        {children}
      </Box>
    </Box>
  );
};
