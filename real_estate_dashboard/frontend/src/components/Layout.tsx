import React, { useState } from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Container,
  Stack,
  useTheme,
  useMediaQuery,
  Divider,
  Paper,
  Tooltip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  HomeWork as HomeWorkIcon,
  Assessment as AssessmentIcon,
  Close as CloseIcon,
  BusinessCenter as BusinessCenterIcon,
  Dashboard as DashboardIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  LightMode as LightModeIcon,
  DarkMode as DarkModeIcon,
  Folder as FolderIcon,
  AccountBalance as TaxIcon,
  Apartment as PortfolioIcon,
  MonetizationOn as DebtIcon,
  ShowChart as MarketIcon,
  IntegrationInstructions as IntegrationIcon,
  Handshake as CRMIcon,
  Calculate as FinancialIcon,
  CloudUpload as PDFIcon,
  Assignment as ProjectIcon,
  Gavel as LegalIcon,
  People as PeopleIcon,
  Description as AuditIcon,
  AdminPanelSettings as AdminIcon,
  Business as CompanyIcon,
  Settings as SettingsIcon,
  Hub as HubIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { CompanySelector } from './common/CompanySelector';
import { useAppTheme } from '../contexts/ThemeContext';
import { UIToggle } from './UIToggle';
import { useUIMode } from '../contexts/UIModeContext';
import { NewLayout } from './new-ui/NewLayout';

const drawerWidth = 260;

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { uiMode } = useUIMode();

  // If New UI is selected, use the new layout
  if (uiMode === 'new') {
    return <NewLayout>{children}</NewLayout>;
  }

  // Otherwise, use the old layout
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const { theme: appTheme, toggleTheme } = useAppTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isHomePage = location.pathname === '/';
  const isModelPage = location.pathname.startsWith('/real-estate-models/');

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const menuItems = [
    {
      text: 'Home',
      icon: <DashboardIcon />,
      path: '/',
    },
    {
      text: 'Main Dashboard',
      icon: <DashboardIcon />,
      path: '/main-dashboard',
    },
    {
      text: 'Command Center',
      icon: <DashboardIcon />,
      path: '/command-center',
    },
    {
      text: 'Platform Overview',
      icon: <AssessmentIcon />,
      path: '/platform-overview',
    },
    {
      text: 'Operations Summary',
      icon: <AssessmentIcon />,
      path: '/operate-summary',
    },
    {
      text: 'Real-Time Data',
      icon: <AssessmentIcon />,
      path: '/real-time-data',
    },
    {
      text: 'Property Management',
      icon: <HomeWorkIcon />,
      path: '/property-management',
    },
    {
      text: 'Accounting',
      icon: <TaxIcon />,
      path: '/accounting',
    },
    {
      text: 'Real Estate Models',
      icon: <AssessmentIcon />,
      path: '/real-estate-tools',
    },
    {
      text: 'Company Financial Analysis',
      icon: <FinancialIcon />,
      path: '/financial-models',
    },
    {
      text: 'Fund Management',
      icon: <BusinessCenterIcon />,
      path: '/fund-management',
    },
    {
      text: 'Debt Management',
      icon: <DebtIcon />,
      path: '/debt-management',
    },
    {
      text: 'Project Tracking',
      icon: <ProjectIcon />,
      path: '/project-tracking',
    },
    {
      text: 'Legal Services',
      icon: <LegalIcon />,
      path: '/legal-services',
    },
    {
      text: 'Portfolio Dashboard',
      icon: <PortfolioIcon />,
      path: '/portfolio-dashboard',
    },
    {
      text: 'Deal Pipeline',
      icon: <CRMIcon />,
      path: '/crm/deals',
    },
    {
      text: 'Market Intelligence',
      icon: <MarketIcon />,
      path: '/market-intelligence',
    },
    {
      text: 'PDF Extraction',
      icon: <PDFIcon />,
      path: '/pdf-extraction',
    },
    {
      text: 'Tax Strategy',
      icon: <TaxIcon />,
      path: '/tax-strategy',
    },
    {
      text: 'Integrations',
      icon: <IntegrationIcon />,
      path: '/integrations',
    },
    {
      text: 'Saved Reports',
      icon: <FolderIcon />,
      path: '/saved-reports',
    },
    // Unified Platform Section
    {
      text: 'Unified Platform',
      icon: <HubIcon />,
      path: '/unified-platform',
    },
    // Admin Section
    {
      text: 'Users & Roles',
      icon: <PeopleIcon />,
      path: '/admin/users-roles',
    },
    {
      text: 'Audit Log',
      icon: <AuditIcon />,
      path: '/admin/audit-log',
    },
    {
      text: 'Companies',
      icon: <CompanyIcon />,
      path: '/admin/companies',
    },
    {
      text: 'API Integrations',
      icon: <IntegrationIcon />,
      path: '/admin/api-integrations',
    },
    {
      text: 'System Settings',
      icon: <SettingsIcon />,
      path: '/admin/system-settings',
    },
  ];

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Brand / Logo - Fixed at top */}
      <Box
        sx={{
          p: 2.5,
          borderBottom: '1px solid',
          borderColor: 'divider',
          cursor: 'pointer',
          flexShrink: 0,
          transition: 'background 0.2s',
          '&:hover': {
            bgcolor: 'action.hover',
          },
        }}
        onClick={() => {
          navigate('/');
          if (isMobile) {
            setMobileOpen(false);
          }
        }}
      >
        <Stack direction="row" alignItems="center" spacing={1.5}>
          <Box
            sx={{
              width: 36,
              height: 36,
              background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 2px 8px rgba(59, 130, 246, 0.3)',
            }}
          >
            <BusinessCenterIcon sx={{ fontSize: 20, color: 'white' }} />
          </Box>
          <Box>
            <Typography variant="subtitle2" sx={{ fontWeight: 700, color: 'text.primary', lineHeight: 1.3 }}>
              RE Capital
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.7rem', lineHeight: 1 }}>
              Analytics
            </Typography>
          </Box>
        </Stack>
      </Box>

      {/* Scrollable Navigation Area */}
      <Box
        sx={{
          flex: 1,
          overflowY: 'auto',
          overflowX: 'hidden',
          px: 2,
          py: 2,
          '&::-webkit-scrollbar': {
            width: '6px',
          },
          '&::-webkit-scrollbar-track': {
            background: 'transparent',
          },
          '&::-webkit-scrollbar-thumb': {
            background: 'rgba(0,0,0,0.2)',
            borderRadius: '3px',
            '&:hover': {
              background: 'rgba(0,0,0,0.3)',
            },
          },
        }}
      >
        <List sx={{ p: 0 }}>
          {menuItems.map((item) => {
            const isActive =
              location.pathname === item.path ||
              (item.path === '/real-estate-tools' && location.pathname.startsWith('/real-estate-models')) ||
              (item.path === '/financial-models' && location.pathname.startsWith('/financial-models'));
            return (
              <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
                <ListItemButton
                  selected={isActive}
                  onClick={() => {
                    navigate(item.path);
                    if (isMobile) {
                      setMobileOpen(false);
                    }
                  }}
                  sx={{
                    borderRadius: 2,
                    py: 1.25,
                    px: 2,
                    minHeight: 44,
                    transition: 'all 0.2s',
                    '&:hover': {
                      bgcolor: isActive ? 'primary.main' : 'action.hover',
                      transform: 'translateX(4px)',
                    },
                    '&.Mui-selected': {
                      bgcolor: 'primary.main',
                      '&:hover': {
                        bgcolor: 'primary.dark',
                      },
                    },
                  }}
                >
                  <ListItemIcon sx={{
                    color: isActive ? 'white' : 'text.secondary',
                    minWidth: 36,
                    '& .MuiSvgIcon-root': {
                      fontSize: '1.25rem',
                    },
                  }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={item.text}
                    primaryTypographyProps={{
                      fontSize: '0.8125rem',
                      fontWeight: isActive ? 600 : 500,
                      color: isActive ? 'white' : 'text.primary',
                      noWrap: true,
                    }}
                  />
                  {isActive && (
                    <Box
                      sx={{
                        width: 5,
                        height: 5,
                        borderRadius: '50%',
                        bgcolor: '#10b981',
                        boxShadow: '0 0 8px rgba(16, 185, 129, 0.6)',
                        ml: 1,
                      }}
                    />
                  )}
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </Box>

      {/* Footer - Fixed at bottom */}
      <Box
        sx={{
          p: 2,
          borderTop: '1px solid',
          borderColor: 'divider',
          flexShrink: 0,
        }}
      >
        <Stack direction="row" alignItems="center" spacing={1} justifyContent="center">
          <Box
            sx={{
              width: 6,
              height: 6,
              borderRadius: '50%',
              bgcolor: '#10b981',
              boxShadow: '0 0 8px rgba(16, 185, 129, 0.5)',
              animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
              '@keyframes pulse': {
                '0%, 100%': { opacity: 1 },
                '50%': { opacity: 0.5 },
              },
            }}
          />
          <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.7rem' }}>
            Live
          </Typography>
          <Typography variant="caption" sx={{ ml: 'auto', color: 'text.disabled', fontSize: '0.7rem' }}>
            v2.4.1
          </Typography>
        </Stack>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            {menuItems.find((item) => item.path === location.pathname)?.text || 'Dashboard'}
          </Typography>
          <Stack direction="row" spacing={2} alignItems="center">
            <UIToggle />
            <CompanySelector />
            <Tooltip title={`Switch to ${appTheme === 'dark' ? 'light' : 'dark'} mode`}>
              <IconButton
                onClick={toggleTheme}
                sx={{
                  color: 'white',
                  '&:hover': {
                    background: 'rgba(255, 255, 255, 0.1)',
                  }
                }}
              >
                {appTheme === 'dark' ? <LightModeIcon /> : <DarkModeIcon />}
              </IconButton>
            </Tooltip>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              v2.4.1
            </Typography>
          </Stack>
        </Toolbar>
      </AppBar>

      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 1 }}>
            <IconButton onClick={handleDrawerToggle}>
              <CloseIcon />
            </IconButton>
          </Box>
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: { md: `calc(100% - ${drawerWidth}px)` },
          minHeight: '100vh',
        }}
      >
        <Toolbar />
        {isHomePage || isModelPage ? (
          <Box sx={{ px: 3, py: 3 }}>
            {children}
          </Box>
        ) : (
          <Container maxWidth="xl" sx={{ py: 3 }}>
            {children}
          </Container>
        )}
      </Box>
    </Box>
  );
};
