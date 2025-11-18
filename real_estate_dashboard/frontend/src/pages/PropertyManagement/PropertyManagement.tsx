// src/pages/PropertyManagement/PropertyManagement.tsx
import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Stack,
  Button,
  Typography,
  Alert,
  AlertTitle,
  Grow,
  alpha,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
} from '@mui/material';
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  HomeWork as HomeWorkIcon,
  MeetingRoom as MeetingRoomIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';
import { Building2, Home, Users, DollarSign } from 'lucide-react';
import { useAppTheme } from '../../contexts/ThemeContext';
import { useCompany } from '../../context/CompanyContext';
import { EntityLayout } from '../../components/layout/EntityLayout';
import { MarketSnapshot } from '../../components/market/MarketSnapshot';
import { StatsCard } from '../../components/ui/StatsCard';

import PropertyDashboard from './components/PropertyDashboard';
import PropertiesTable from './components/PropertiesTable';
import UnitsTable from './components/UnitsTable';
import LeasesTable from './components/LeasesTable';
import MaintenanceTable from './components/MaintenanceTable';
import ROIAnalysis from './components/ROIAnalysis';
import AddPropertyModal from './components/AddPropertyModal';

export const PropertyManagement: React.FC = () => {
  const [currentTab, setCurrentTab] = useState('overview');
  const [refreshKey, setRefreshKey] = useState(0);
  const [addPropertyModalOpen, setAddPropertyModalOpen] = useState(false);
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterLocation, setFilterLocation] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const { theme } = useAppTheme();
  const { selectedCompany } = useCompany();
  const isDark = theme === 'dark';

  const handleTabChange = (tab: string) => {
    setCurrentTab(tab);
  };

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1);
  };

  const handleAddPropertyClick = () => {
    setAddPropertyModalOpen(true);
  };

  const handleAddPropertyClose = () => {
    setAddPropertyModalOpen(false);
  };

  const handleAddPropertySuccess = () => {
    setRefreshKey(prev => prev + 1);
  };

  const tabs = [
    { label: 'Overview', value: 'overview', icon: <HomeWorkIcon /> },
    { label: 'Properties', value: 'properties', icon: <HomeWorkIcon /> },
    { label: 'Units', value: 'units', icon: <MeetingRoomIcon /> },
    { label: 'Leases & Tenants', value: 'leases', icon: <AssessmentIcon /> },
    { label: 'Maintenance', value: 'maintenance', icon: <WarningIcon /> },
    { label: 'Financials', value: 'financials', icon: <TrendingUpIcon /> },
    { label: 'Market & Comps', value: 'market', icon: <AssessmentIcon /> },
  ];

  // Company-specific data (currently empty - will be loaded from backend API)
  // These will be calculated from actual property data
  const companyProperties = selectedCompany ? [] : [];
  const totalProperties = companyProperties.length;
  const totalUnits = 0; // Will be sum of all units across properties
  const occupancyRate = 0; // Will be calculated from occupied units
  const monthlyNOI = 0; // Will be sum of property NOI

  const kpis = [
    {
      label: 'Total Properties',
      value: totalProperties,
      prefix: '',
      suffix: '',
      decimals: 0,
      change: selectedCompany ? '0' : 'N/A',
      trend: 'neutral' as const,
      icon: Building2,
      gradient: 'blue' as const,
      subtitle: selectedCompany ? selectedCompany.name : 'Select company',
      sparkline: []
    },
    {
      label: 'Total Units',
      value: totalUnits,
      prefix: '',
      suffix: '',
      decimals: 0,
      change: '0',
      trend: 'neutral' as const,
      icon: Home,
      gradient: 'green' as const,
      subtitle: 'across all properties',
      sparkline: []
    },
    {
      label: 'Occupancy Rate',
      value: occupancyRate,
      prefix: '',
      suffix: '%',
      decimals: 1,
      change: '0%',
      trend: 'neutral' as const,
      icon: Users,
      gradient: 'purple' as const,
      subtitle: 'current',
      sparkline: []
    },
    {
      label: 'Monthly NOI',
      value: monthlyNOI,
      prefix: '$',
      suffix: '',
      decimals: 0,
      change: '$0',
      trend: 'neutral' as const,
      icon: DollarSign,
      gradient: 'amber' as const,
      subtitle: 'from properties',
      sparkline: []
    },
  ];

  const actions = [
    {
      label: 'Export Data',
      onClick: () => console.log('Export data'),
    },
    {
      label: 'Generate Report',
      onClick: () => console.log('Generate report'),
    },
    {
      label: 'Settings',
      onClick: () => console.log('Settings'),
    },
  ];

  return (
    <Box sx={{ maxWidth: '100%' }}>
      <EntityLayout
        entityType="Portfolio"
        entityName={selectedCompany ? `Property Management - ${selectedCompany.name}` : 'Property Management'}
        entityStatus={selectedCompany ? "Active" : "No Company Selected"}
        statusColor={selectedCompany ? "#10b981" : "#94a3b8"}
        breadcrumbs={[
          { label: 'Operate', href: '/operate-summary' },
          { label: 'Property Management' },
        ]}
        actions={actions}
        headerMetrics={[
          { label: 'Total Properties', value: totalProperties.toString(), subtext: selectedCompany ? selectedCompany.name : 'Select company' },
          { label: 'Total Units', value: totalUnits.toString(), subtext: 'across portfolio' },
        ]}
        tabs={tabs}
        defaultTab="overview"
        onTabChange={handleTabChange}
      >
        {/* Filters Bar - Right aligned */}
        <Box sx={{ mb: 3 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="center" flexWrap="wrap" spacing={2}>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              {tabs.find(t => t.value === currentTab)?.label}
            </Typography>

            <Stack direction="row" spacing={2} alignItems="center">
              <TextField
                size="small"
                placeholder="Search properties..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                sx={{ minWidth: 200 }}
              />
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Status</InputLabel>
                <Select
                  value={filterStatus}
                  label="Status"
                  onChange={(e) => setFilterStatus(e.target.value)}
                >
                  <MenuItem value="all">All</MenuItem>
                  <MenuItem value="active">Active</MenuItem>
                  <MenuItem value="vacant">Vacant</MenuItem>
                  <MenuItem value="maintenance">Maintenance</MenuItem>
                </Select>
              </FormControl>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Location</InputLabel>
                <Select
                  value={filterLocation}
                  label="Location"
                  onChange={(e) => setFilterLocation(e.target.value)}
                >
                  <MenuItem value="all">All</MenuItem>
                  <MenuItem value="downtown">Downtown</MenuItem>
                  <MenuItem value="suburbs">Suburbs</MenuItem>
                  <MenuItem value="uptown">Uptown</MenuItem>
                </Select>
              </FormControl>
              <Button
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={handleRefresh}
                size="small"
              >
                Refresh
              </Button>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAddPropertyClick}
                size="small"
              >
                Add Property
              </Button>
            </Stack>
          </Stack>
        </Box>

        {/* KPIs Row - Enhanced with animations and sparklines */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          {kpis.map((kpi, index) => (
            <StatsCard
              key={index}
              label={kpi.label}
              value={kpi.value}
              icon={kpi.icon}
              gradient={kpi.gradient}
              trend={kpi.trend}
              trendValue={kpi.change}
              subtitle={kpi.subtitle}
              sparklineData={kpi.sparkline}
              animated={true}
              prefix={kpi.prefix}
              suffix={kpi.suffix}
              decimals={kpi.decimals}
            />
          ))}
        </div>

        {/* Alerts Row - Company-specific */}
        {!selectedCompany ? (
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12}>
              <Alert severity="info" variant="outlined">
                <AlertTitle sx={{ fontWeight: 600 }}>Select a Company</AlertTitle>
                <Typography variant="body2">
                  Please select a company to view property management alerts and metrics
                </Typography>
              </Alert>
            </Grid>
          </Grid>
        ) : totalProperties === 0 ? (
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12}>
              <Alert severity="info" variant="outlined">
                <AlertTitle sx={{ fontWeight: 600 }}>No Properties Yet</AlertTitle>
                <Typography variant="body2">
                  Get started by adding your first property for <strong>{selectedCompany.name}</strong>
                </Typography>
              </Alert>
            </Grid>
          </Grid>
        ) : (
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} md={4}>
              <Alert severity="info" variant="outlined" icon={<WarningIcon />}>
                <AlertTitle sx={{ fontWeight: 600 }}>Leases Expiring</AlertTitle>
                <Typography variant="body2">
                  <strong>0 leases</strong> expiring in next 60 days
                </Typography>
              </Alert>
            </Grid>
            <Grid item xs={12} md={4}>
              <Alert severity="info" variant="outlined" icon={<ErrorIcon />}>
                <AlertTitle sx={{ fontWeight: 600 }}>Maintenance</AlertTitle>
                <Typography variant="body2">
                  <strong>0 requests</strong> pending
                </Typography>
              </Alert>
            </Grid>
            <Grid item xs={12} md={4}>
              <Alert severity="info" variant="outlined">
                <AlertTitle sx={{ fontWeight: 600 }}>Portfolio Status</AlertTitle>
                <Typography variant="body2">
                  All metrics calculated from properties
                </Typography>
              </Alert>
            </Grid>
          </Grid>
        )}

        {/* Main Content Area: Left 2/3 Table, Right 1/3 Market Snapshot */}
        <Grid container spacing={3}>
          {/* Left: Table Content (2/3 width) */}
          <Grid item xs={12} lg={8}>
            <Box>
              {currentTab === 'overview' && <PropertyDashboard key={refreshKey} />}
              {currentTab === 'properties' && <PropertiesTable key={refreshKey} />}
              {currentTab === 'units' && <UnitsTable key={refreshKey} />}
              {currentTab === 'leases' && <LeasesTable key={refreshKey} />}
              {currentTab === 'maintenance' && <MaintenanceTable key={refreshKey} />}
              {currentTab === 'financials' && <ROIAnalysis key={refreshKey} />}
              {currentTab === 'market' && (
                <Card>
                  <CardContent>
                    <Typography variant="h6" sx={{ mb: 2 }}>Market & Comparables</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Detailed market analysis and comparable properties will be displayed here.
                    </Typography>
                  </CardContent>
                </Card>
              )}
            </Box>
          </Grid>

          {/* Right: Market Snapshot (1/3 width) */}
          <Grid item xs={12} lg={4}>
            <Box sx={{ position: 'sticky', top: 16 }}>
              <MarketSnapshot
                scope="portfolio"
                timeRange="current"
                entity="Property Portfolio"
                compact={false}
                workspaceFilter="operate"
              />
            </Box>
          </Grid>
        </Grid>
      </EntityLayout>

      {/* Add Property Modal */}
      <AddPropertyModal
        open={addPropertyModalOpen}
        onClose={handleAddPropertyClose}
        onSuccess={handleAddPropertySuccess}
      />
    </Box>
  );
};

export default PropertyManagement;
