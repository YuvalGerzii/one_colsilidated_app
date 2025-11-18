/**
 * Main Navigation Component
 * Responsive sidebar navigation with collapsible menu
 */
import React, { useState } from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Box,
  Typography,
  Avatar,
  Divider,
  Collapse,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Dashboard,
  School,
  TrendingUp,
  Business,
  WorkOutline,
  PeopleAlt,
  Assessment,
  Settings,
  MenuBook,
  Psychology,
  Groups,
  AttachMoney,
  ExpandLess,
  ExpandMore,
  Menu as MenuIcon,
  ChevronLeft,
} from '@mui/icons-material';

const DRAWER_WIDTH = 280;

const navigationItems = [
  {
    title: 'Overview',
    icon: <Dashboard />,
    path: '/dashboard',
  },
  {
    title: 'Workforce Digital Twin',
    icon: <Psychology />,
    path: '/digital-twin',
    submenu: [
      { title: 'Market Overview', path: '/digital-twin/market' },
      { title: 'Risk Assessment', path: '/digital-twin/risk' },
      { title: 'Displacement Predictions', path: '/digital-twin/predictions' },
      { title: 'Scenario Modeling', path: '/digital-twin/scenarios' },
    ],
  },
  {
    title: 'AI Agents',
    icon: <PeopleAlt />,
    path: '/agents',
    submenu: [
      { title: 'Gap Analyzer', path: '/agents/gap-analyzer' },
      { title: 'Opportunity Scout', path: '/agents/opportunity' },
      { title: 'Learning Strategist', path: '/agents/learning' },
      { title: 'Teaching Coach', path: '/agents/teaching' },
      { title: 'Career Navigator', path: '/agents/career' },
    ],
  },
  {
    title: 'Study Buddy',
    icon: <School />,
    path: '/study-buddy',
    badge: 'New',
    submenu: [
      { title: 'Knowledge Library', path: '/study-buddy/library' },
      { title: 'My Learning Paths', path: '/study-buddy/paths' },
      { title: 'Learning Analytics', path: '/study-buddy/analytics' },
      { title: 'Study Groups', path: '/study-buddy/groups' },
      { title: 'Q&A Forum', path: '/study-buddy/qa' },
      { title: 'Contributors', path: '/study-buddy/contributors' },
      { title: 'Earnings', path: '/study-buddy/earnings' },
    ],
  },
  {
    title: 'Economic Copilot',
    icon: <AttachMoney />,
    path: '/economic-copilot',
    submenu: [
      { title: 'Job Offer Analyzer', path: '/economic-copilot/job-offer' },
      { title: 'Retirement Planner', path: '/economic-copilot/retirement' },
      { title: 'Debt vs Reskilling', path: '/economic-copilot/debt' },
      { title: 'Family Planner', path: '/economic-copilot/family' },
      { title: 'Life Decision Engine', path: '/economic-copilot/decisions' },
    ],
  },
  {
    title: 'Gig Economy',
    icon: <WorkOutline />,
    path: '/gig',
    submenu: [
      { title: 'Gig Matcher', path: '/gig/matcher' },
      { title: 'Income Optimizer', path: '/gig/optimizer' },
      { title: 'Portfolio Manager', path: '/gig/portfolio' },
      { title: 'Benefits Calculator', path: '/gig/benefits' },
      { title: 'Hybrid Scheduler', path: '/gig/scheduler' },
    ],
  },
  {
    title: 'Corporate Tools',
    icon: <Business />,
    path: '/corporate',
    submenu: [
      { title: 'Transformation Dashboard', path: '/corporate/dashboard' },
      { title: 'Job Matching', path: '/corporate/matching' },
      { title: 'Automation Scanner', path: '/corporate/automation' },
      { title: 'Risk Calculator', path: '/corporate/risk' },
      { title: 'Union Simulator', path: '/corporate/union' },
      { title: 'Hiring Insights', path: '/corporate/hiring' },
      { title: 'Fairness Engine', path: '/corporate/fairness' },
    ],
  },
  {
    title: 'Progress & Goals',
    icon: <TrendingUp />,
    path: '/progress',
  },
  {
    title: 'Analytics',
    icon: <Assessment />,
    path: '/analytics',
  },
];

const Navigation = ({ open, onToggle, currentPath, onNavigate }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [expandedItems, setExpandedItems] = useState({});

  const handleExpandClick = (title) => {
    setExpandedItems((prev) => ({
      ...prev,
      [title]: !prev[title],
    }));
  };

  const handleNavigate = (path) => {
    if (onNavigate) {
      onNavigate(path);
    }
    if (isMobile && onToggle) {
      onToggle();
    }
  };

  const drawerContent = (
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        background: 'linear-gradient(180deg, #1976D2 0%, #1565C0 100%)',
        color: 'white',
      }}
    >
      {/* Header */}
      <Box
        sx={{
          p: 3,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Avatar
            sx={{
              width: 40,
              height: 40,
              bgcolor: 'rgba(255, 255, 255, 0.2)',
            }}
          >
            <Psychology />
          </Avatar>
          <Typography variant="h6" fontWeight={700}>
            WorkForce AI
          </Typography>
        </Box>
        {!isMobile && (
          <IconButton onClick={onToggle} sx={{ color: 'white' }}>
            <ChevronLeft />
          </IconButton>
        )}
      </Box>

      <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.1)' }} />

      {/* Navigation Items */}
      <List sx={{ flex: 1, px: 2, py: 2 }}>
        {navigationItems.map((item) => (
          <React.Fragment key={item.title}>
            <ListItem disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                onClick={() => {
                  if (item.submenu) {
                    handleExpandClick(item.title);
                  } else {
                    handleNavigate(item.path);
                  }
                }}
                selected={currentPath === item.path}
                sx={{
                  borderRadius: 2,
                  color: 'white',
                  '&.Mui-selected': {
                    bgcolor: 'rgba(255, 255, 255, 0.2)',
                    '&:hover': {
                      bgcolor: 'rgba(255, 255, 255, 0.25)',
                    },
                  },
                  '&:hover': {
                    bgcolor: 'rgba(255, 255, 255, 0.1)',
                  },
                }}
              >
                <ListItemIcon sx={{ color: 'white', minWidth: 40 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.title}
                  primaryTypographyProps={{
                    fontWeight: currentPath === item.path ? 600 : 400,
                    fontSize: '0.95rem',
                  }}
                />
                {item.badge && (
                  <Box
                    sx={{
                      bgcolor: '#4CAF50',
                      color: 'white',
                      px: 1,
                      py: 0.25,
                      borderRadius: 1,
                      fontSize: '0.7rem',
                      fontWeight: 700,
                    }}
                  >
                    {item.badge}
                  </Box>
                )}
                {item.submenu &&
                  (expandedItems[item.title] ? <ExpandLess /> : <ExpandMore />)}
              </ListItemButton>
            </ListItem>

            {/* Submenu */}
            {item.submenu && (
              <Collapse in={expandedItems[item.title]} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                  {item.submenu.map((subItem) => (
                    <ListItemButton
                      key={subItem.path}
                      onClick={() => handleNavigate(subItem.path)}
                      selected={currentPath === subItem.path}
                      sx={{
                        pl: 7,
                        borderRadius: 2,
                        color: 'rgba(255, 255, 255, 0.8)',
                        '&.Mui-selected': {
                          bgcolor: 'rgba(255, 255, 255, 0.15)',
                          color: 'white',
                        },
                        '&:hover': {
                          bgcolor: 'rgba(255, 255, 255, 0.1)',
                          color: 'white',
                        },
                      }}
                    >
                      <ListItemText
                        primary={subItem.title}
                        primaryTypographyProps={{
                          fontSize: '0.875rem',
                        }}
                      />
                    </ListItemButton>
                  ))}
                </List>
              </Collapse>
            )}
          </React.Fragment>
        ))}
      </List>

      <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.1)' }} />

      {/* User Profile Footer */}
      <Box sx={{ p: 2 }}>
        <ListItemButton
          onClick={() => handleNavigate('/settings')}
          sx={{
            borderRadius: 2,
            '&:hover': {
              bgcolor: 'rgba(255, 255, 255, 0.1)',
            },
          }}
        >
          <ListItemIcon sx={{ color: 'white', minWidth: 40 }}>
            <Settings />
          </ListItemIcon>
          <ListItemText
            primary="Settings"
            primaryTypographyProps={{
              fontSize: '0.95rem',
            }}
          />
        </ListItemButton>

        <Box
          sx={{
            mt: 2,
            p: 2,
            borderRadius: 2,
            bgcolor: 'rgba(255, 255, 255, 0.1)',
            display: 'flex',
            alignItems: 'center',
            gap: 2,
          }}
        >
          <Avatar
            sx={{ width: 40, height: 40 }}
            src="/api/placeholder/40/40"
            alt="User"
          />
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography
              variant="body2"
              fontWeight={600}
              noWrap
              sx={{ color: 'white' }}
            >
              Sarah Chen
            </Typography>
            <Typography
              variant="caption"
              sx={{ color: 'rgba(255, 255, 255, 0.7)' }}
            >
              Pro Plan
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );

  return (
    <>
      {isMobile ? (
        <Drawer
          anchor="left"
          open={open}
          onClose={onToggle}
          sx={{
            '& .MuiDrawer-paper': {
              width: DRAWER_WIDTH,
              boxSizing: 'border-box',
            },
          }}
        >
          {drawerContent}
        </Drawer>
      ) : (
        <Drawer
          variant="permanent"
          open={open}
          sx={{
            width: open ? DRAWER_WIDTH : 0,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: DRAWER_WIDTH,
              boxSizing: 'border-box',
              transition: theme.transitions.create('width', {
                easing: theme.transitions.easing.sharp,
                duration: theme.transitions.duration.enteringScreen,
              }),
            },
          }}
        >
          {drawerContent}
        </Drawer>
      )}
    </>
  );
};

export default Navigation;
