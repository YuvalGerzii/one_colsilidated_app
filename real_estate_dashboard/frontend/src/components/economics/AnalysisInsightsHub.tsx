/**
 * AnalysisInsightsHub Component - Unified hub for economic and market analysis
 *
 * @version 1.1.0
 * @updated 2025-11-15
 * @description Redesigned with tabbed navigation, cleaner hero header, and design token system
 * @changelog
 *   v1.1.0 - Replaced accordion layout with tabs, simplified hero header, added design tokens
 */
import React, { useState } from 'react';
import {
  Box,
  Card,
  Typography,
  Tabs,
  Tab,
  Stack,
  alpha,
  IconButton,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Timeline as TimelineIcon,
  ShowChart as ChartIcon,
  CompareArrows as CompareIcon,
  LocationCity as LocationCityIcon,
  Assessment as AssessmentIcon,
  Home as HomeIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';
import { designTokens, alphaColor } from '../../theme/designTokens';
import { USAEconomicsAnalysis } from './USAEconomicsAnalysis';
import EconomicForecast from './EconomicForecast';
import { HistoricalCharts } from './HistoricalCharts';
import { CorrelationMatrix } from './CorrelationMatrix';
import { MarketDataVisualization } from './MarketDataVisualization';
import { MarketIntelligenceInsights } from './MarketIntelligenceInsights';
import AdvancedMarketData from './AdvancedMarketData';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 4 }}>{children}</Box>}
    </div>
  );
}

const ANALYSIS_TABS = [
  {
    id: 0,
    label: 'Economic Health',
    icon: TrendingUpIcon,
    color: '#3b82f6',
    description: 'Real-time economic health score and key indicators',
  },
  {
    id: 1,
    label: 'Forecasting',
    icon: TimelineIcon,
    color: '#8b5cf6',
    description: 'AI-powered economic forecasts and predictions',
  },
  {
    id: 2,
    label: 'Historical Trends',
    icon: ChartIcon,
    color: '#10b981',
    description: 'Multi-indicator historical analysis',
  },
  {
    id: 3,
    label: 'Correlations',
    icon: CompareIcon,
    color: '#f59e0b',
    description: 'Discover relationships between indicators',
  },
  {
    id: 4,
    label: 'Market Intelligence',
    icon: LocationCityIcon,
    color: '#06b6d4',
    description: 'Geographic and real estate market data',
  },
  {
    id: 5,
    label: 'Insights',
    icon: AssessmentIcon,
    color: '#ef4444',
    description: 'Hot zones, neighborhood scores, and transactions',
  },
  {
    id: 6,
    label: 'STR & Zoning',
    icon: HomeIcon,
    color: '#ec4899',
    description: 'Short-term rentals and zoning intelligence',
  },
];

export const AnalysisInsightsHub: React.FC = () => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const activeTabInfo = ANALYSIS_TABS[activeTab];

  return (
    <Box>
      {/* Cleaner Hero Header */}
      <Box
        sx={{
          p: { xs: 3, md: 4 },
          mb: 4,
          background: `linear-gradient(135deg, ${alphaColor(activeTabInfo.color, 0.08)} 0%, ${alphaColor(activeTabInfo.color, 0.03)} 100%)`,
          borderBottom: `1px solid ${alphaColor(activeTabInfo.color, 0.1)}`,
          borderRadius: designTokens.radius.xl,
        }}
      >
        <Stack direction="row" alignItems="center" spacing={3}>
          {/* Simpler icon treatment */}
          <Box
            sx={{
              width: 56,
              height: 56,
              borderRadius: designTokens.radius.lg,
              background: activeTabInfo.color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: `all ${designTokens.transitions.duration.base} ${designTokens.transitions.timing.inOut}`,
            }}
          >
            <activeTabInfo.icon sx={{ fontSize: 28, color: 'white' }} />
          </Box>

          <Box flex={1}>
            <Typography
              variant="h4"
              sx={{
                fontWeight: designTokens.typography.fontWeight.bold,
                mb: 0.5,
                fontSize: { xs: designTokens.typography.fontSize['2xl'], md: designTokens.typography.fontSize['3xl'] },
              }}
            >
              Analysis & Insights Hub
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ fontSize: designTokens.typography.fontSize.sm }}
            >
              {activeTabInfo.description}
            </Typography>
          </Box>

          {/* Action buttons */}
          <Stack direction="row" spacing={1} sx={{ display: { xs: 'none', sm: 'flex' } }}>
            <IconButton
              size="small"
              sx={{
                color: activeTabInfo.color,
                '&:hover': {
                  background: alphaColor(activeTabInfo.color, 0.1),
                },
              }}
            >
              <RefreshIcon fontSize="small" />
            </IconButton>
          </Stack>
        </Stack>
      </Box>

      {/* Cleaner Tab Navigation */}
      <Card
        sx={{
          mb: 4,
          overflow: 'visible',
          borderRadius: designTokens.radius.xl,
        }}
      >
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
          {ANALYSIS_TABS.map((tab) => (
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
          <USAEconomicsAnalysis />
        </TabPanel>

        <TabPanel value={activeTab} index={1}>
          <EconomicForecast />
        </TabPanel>

        <TabPanel value={activeTab} index={2}>
          <HistoricalCharts />
        </TabPanel>

        <TabPanel value={activeTab} index={3}>
          <CorrelationMatrix />
        </TabPanel>

        <TabPanel value={activeTab} index={4}>
          <MarketDataVisualization />
        </TabPanel>

        <TabPanel value={activeTab} index={5}>
          <MarketIntelligenceInsights />
        </TabPanel>

        <TabPanel value={activeTab} index={6}>
          <AdvancedMarketData />
        </TabPanel>
      </Box>
    </Box>
  );
};

export default AnalysisInsightsHub;
