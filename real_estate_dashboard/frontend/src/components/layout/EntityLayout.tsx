import React, { useState } from 'react';
import {
  Box,
  Card,
  Tabs,
  Tab,
  Stack,
  Typography,
  Breadcrumbs,
  Link,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  alpha,
} from '@mui/material';
import {
  Home as HomeIcon,
  AttachMoney as FinancialsIcon,
  ShowChart as MarketIcon,
  Description as DocumentsIcon,
  CheckCircle as TasksIcon,
  Timeline as ActivityIcon,
  MoreVert as MoreIcon,
  NavigateNext as NavigateNextIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';

interface TabConfig {
  label: string;
  value: string;
  icon: React.ReactNode;
}

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface EntityAction {
  label: string;
  onClick: () => void;
  icon?: React.ReactNode;
}

interface EntityLayoutProps {
  // Header props
  entityType: string; // e.g., "Property", "Deal", "Fund"
  entityName: string;
  entityStatus?: string;
  statusColor?: string;
  breadcrumbs?: BreadcrumbItem[];
  actions?: EntityAction[];
  headerMetrics?: Array<{ label: string; value: string | number; subtext?: string }>;

  // Tab props
  tabs?: TabConfig[];
  defaultTab?: string;
  onTabChange?: (tab: string) => void;

  // Content
  children: React.ReactNode;

  // Layout options
  showTabs?: boolean;
}

const DEFAULT_TABS: TabConfig[] = [
  { label: 'Overview', value: 'overview', icon: <HomeIcon /> },
  { label: 'Financials', value: 'financials', icon: <FinancialsIcon /> },
  { label: 'Market & Comps', value: 'market', icon: <MarketIcon /> },
  { label: 'Documents', value: 'documents', icon: <DocumentsIcon /> },
  { label: 'Tasks', value: 'tasks', icon: <TasksIcon /> },
  { label: 'Activity', value: 'activity', icon: <ActivityIcon /> },
];

export const EntityLayout: React.FC<EntityLayoutProps> = ({
  entityType,
  entityName,
  entityStatus,
  statusColor = '#10b981',
  breadcrumbs = [],
  actions = [],
  headerMetrics = [],
  tabs = DEFAULT_TABS,
  defaultTab = 'overview',
  onTabChange,
  children,
  showTabs = true,
}) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [currentTab, setCurrentTab] = useState(defaultTab);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: string) => {
    setCurrentTab(newValue);
    if (onTabChange) {
      onTabChange(newValue);
    }
  };

  const handleActionsMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleActionsMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box>
      {/* Breadcrumbs */}
      {breadcrumbs.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Breadcrumbs
            separator={<NavigateNextIcon fontSize="small" />}
            sx={{ color: 'text.secondary' }}
          >
            {breadcrumbs.map((crumb, index) => (
              crumb.href ? (
                <Link
                  key={index}
                  href={crumb.href}
                  sx={{
                    color: 'text.secondary',
                    textDecoration: 'none',
                    '&:hover': { textDecoration: 'underline' }
                  }}
                >
                  {crumb.label}
                </Link>
              ) : (
                <Typography key={index} color="text.primary" sx={{ fontWeight: 600 }}>
                  {crumb.label}
                </Typography>
              )
            ))}
          </Breadcrumbs>
        </Box>
      )}

      {/* Compact Header */}
      <Card sx={{ mb: 3 }}>
        <Box sx={{ p: 3 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="flex-start" spacing={2}>
            {/* Left: Title and Status */}
            <Stack spacing={1} sx={{ flex: 1 }}>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase', letterSpacing: 1 }}>
                  {entityType}
                </Typography>
                {entityStatus && (
                  <Chip
                    label={entityStatus}
                    size="small"
                    sx={{
                      bgcolor: alpha(statusColor, 0.1),
                      color: statusColor,
                      fontWeight: 600,
                      height: 24,
                    }}
                  />
                )}
              </Stack>
              <Typography variant="h5" sx={{ fontWeight: 700 }}>
                {entityName}
              </Typography>
            </Stack>

            {/* Right: Metrics and Actions */}
            <Stack direction="row" alignItems="center" spacing={3}>
              {/* Header Metrics */}
              {headerMetrics.map((metric, index) => (
                <Box key={index} sx={{ textAlign: 'right' }}>
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                    {metric.label}
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 700 }}>
                    {metric.value}
                  </Typography>
                  {metric.subtext && (
                    <Typography variant="caption" color="text.secondary">
                      {metric.subtext}
                    </Typography>
                  )}
                </Box>
              ))}

              {/* Actions Menu */}
              {actions.length > 0 && (
                <>
                  <IconButton
                    onClick={handleActionsMenuOpen}
                    sx={{
                      bgcolor: isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.02)',
                    }}
                  >
                    <MoreIcon />
                  </IconButton>
                  <Menu
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={handleActionsMenuClose}
                  >
                    {actions.map((action, index) => (
                      <MenuItem
                        key={index}
                        onClick={() => {
                          action.onClick();
                          handleActionsMenuClose();
                        }}
                      >
                        {action.icon && <Box sx={{ mr: 1, display: 'flex' }}>{action.icon}</Box>}
                        {action.label}
                      </MenuItem>
                    ))}
                  </Menu>
                </>
              )}
            </Stack>
          </Stack>
        </Box>

        {/* Tabs */}
        {showTabs && (
          <Box
            sx={{
              borderTop: `1px solid ${isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)}`,
            }}
          >
            <Tabs
              value={currentTab}
              onChange={handleTabChange}
              variant="scrollable"
              scrollButtons="auto"
              sx={{ px: 2 }}
            >
              {tabs.map((tab) => (
                <Tab
                  key={tab.value}
                  value={tab.value}
                  label={tab.label}
                  icon={tab.icon}
                  iconPosition="start"
                  sx={{
                    minHeight: 56,
                    textTransform: 'none',
                    fontWeight: 500,
                    fontSize: '0.9rem',
                  }}
                />
              ))}
            </Tabs>
          </Box>
        )}
      </Card>

      {/* Content Area */}
      <Box>{children}</Box>
    </Box>
  );
};
