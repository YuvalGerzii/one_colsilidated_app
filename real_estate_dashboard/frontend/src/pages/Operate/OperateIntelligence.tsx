/**
 * OperateIntelligence Component - Operate workspace page
 *
 * @version 1.1.0
 * @updated 2025-11-15
 * @description Standalone page for real estate market data with MetricCard integration
 * @changelog
 *   v1.1.0 - Integrated design tokens, added MetricCard components, cleaner hero header
 */
import React, { useState } from 'react';
import {
  Box,
  Card,
  Typography,
  Tabs,
  Tab,
  Stack,
  Grid,
  IconButton,
} from '@mui/material';
import {
  LocationCity as LocationCityIcon,
  Home as HomeIcon,
  Business as BusinessIcon,
  Map as MapIcon,
  Assessment as AssessmentIcon,
  Apartment as ApartmentIcon,
  Refresh as RefreshIcon,
  ShowChart as ChartIcon,
  Storefront as StorefrontIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';
import {
  MarketDataVisualization,
  MarketIntelligenceInsights,
  AdvancedMarketData,
  STRDeepDive,
  ZoningIntelligence,
} from '../../components/economics';
import { MetricCard } from '../../components/ui/MetricCard';
import { designTokens, alphaColor } from '../../theme/designTokens';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

const OPERATE_TABS = [
  {
    id: 0,
    label: 'Market Overview',
    icon: LocationCityIcon,
    color: '#06b6d4',
    description: 'Geographic and real estate market intelligence',
  },
  {
    id: 1,
    label: 'Market Insights',
    icon: AssessmentIcon,
    color: '#ef4444',
    description: 'Hot zones, neighborhoods, and transactions',
  },
  {
    id: 2,
    label: 'STR Analytics',
    icon: HomeIcon,
    color: '#10b981',
    description: 'Short-term rental market analysis',
  },
  {
    id: 3,
    label: 'Zoning Intelligence',
    icon: MapIcon,
    color: '#f59e0b',
    description: 'Development opportunities and regulations',
  },
  {
    id: 4,
    label: 'Advanced Data',
    icon: BusinessIcon,
    color: '#8b5cf6',
    description: 'STR, zoning, and development deep dive',
  },
];

export const OperateIntelligence: React.FC = () => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const activeTabInfo = OPERATE_TABS[activeTab];

  return (
    <Box sx={{ p: { xs: 3, md: 4 } }}>
      {/* Cleaner Hero Header */}
      <Box
        sx={{
          mb: 4,
          p: { xs: 3, md: 4 },
          borderRadius: designTokens.radius.xl,
          background: `linear-gradient(135deg, ${alphaColor(designTokens.colors.workspace.operate, 0.08)} 0%, ${alphaColor(designTokens.colors.workspace.operate, 0.03)} 100%)`,
          borderBottom: `1px solid ${alphaColor(designTokens.colors.workspace.operate, 0.1)}`,
        }}
      >
        <Stack direction="row" alignItems="center" spacing={3}>
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
            <ApartmentIcon sx={{ fontSize: 28, color: 'white' }} />
          </Box>

          <Box flex={1}>
            <Typography
              variant="h3"
              sx={{
                fontWeight: designTokens.typography.fontWeight.bold,
                mb: 0.5,
                fontSize: { xs: designTokens.typography.fontSize['2xl'], md: designTokens.typography.fontSize['3xl'] },
              }}
            >
              Operate Intelligence
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ fontSize: designTokens.typography.fontSize.sm }}
            >
              {activeTabInfo.description}
            </Typography>
          </Box>

          <Stack direction="row" spacing={1} sx={{ display: { xs: 'none', sm: 'flex' } }}>
            <IconButton
              size="small"
              sx={{
                color: designTokens.colors.workspace.operate,
                '&:hover': {
                  background: alphaColor(designTokens.colors.workspace.operate, 0.1),
                },
              }}
            >
              <RefreshIcon fontSize="small" />
            </IconButton>
          </Stack>
        </Stack>
      </Box>

      {/* Key Metrics Grid with new MetricCard component */}
      <Grid container spacing={{ xs: 2, md: 3 }} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Active Listings"
            value="1,247"
            change="+8.3%"
            trend="up"
            icon={HomeIcon}
            color={designTokens.colors.chart.blue}
            subtext="vs last month"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Avg. Cap Rate"
            value="6.2%"
            change="+0.3%"
            trend="up"
            icon={AssessmentIcon}
            color={designTokens.colors.chart.emerald}
            subtext="annual yield"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="STR Occupancy"
            value="78%"
            change="-2.1%"
            trend="down"
            icon={StorefrontIcon}
            color={designTokens.colors.chart.amber}
            subtext="vs last quarter"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Market Heat Index"
            value="84/100"
            change="+5.2%"
            trend="up"
            icon={ChartIcon}
            color={designTokens.colors.chart.red}
            subtext="hot market"
          />
        </Grid>
      </Grid>

      {/* Cleaner Tab Navigation */}
      <Card sx={{ mb: 4, borderRadius: designTokens.radius.xl }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          allowScrollButtonsMobile
          sx={{
            px: 2,
            '& .MuiTab-root': {
              minHeight: 56,
              textTransform: 'none',
              fontSize: designTokens.typography.fontSize.sm,
              fontWeight: designTokens.typography.fontWeight.semibold,
              px: 3,
              py: 2,
              transition: `all ${designTokens.transitions.duration.base} ${designTokens.transitions.timing.inOut}`,
              '&.Mui-selected': {
                color: activeTabInfo.color,
              },
              '&:hover': {
                background: alphaColor(activeTabInfo.color, 0.04),
              },
            },
            '& .MuiTabs-indicator': {
              height: 3,
              borderRadius: '3px 3px 0 0',
              background: `linear-gradient(90deg, ${activeTabInfo.color} 0%, ${alphaColor(activeTabInfo.color, 0.7)} 100%)`,
            },
          }}
        >
          {OPERATE_TABS.map((tab) => (
            <Tab
              key={tab.id}
              icon={<tab.icon sx={{ fontSize: 20 }} />}
              iconPosition="start"
              label={tab.label}
              title={tab.description}
            />
          ))}
        </Tabs>
      </Card>

      {/* Tab Content */}
      <Box>
        <TabPanel value={activeTab} index={0}>
          <MarketDataVisualization />
        </TabPanel>

        <TabPanel value={activeTab} index={1}>
          <MarketIntelligenceInsights />
        </TabPanel>

        <TabPanel value={activeTab} index={2}>
          <STRDeepDive />
        </TabPanel>

        <TabPanel value={activeTab} index={3}>
          <ZoningIntelligence />
        </TabPanel>

        <TabPanel value={activeTab} index={4}>
          <AdvancedMarketData />
        </TabPanel>
      </Box>
    </Box>
  );
};

export default OperateIntelligence;
