// src/pages/PropertyManagement/PropertyManagement.tsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Tabs,
  Tab,
  Paper,
  Grid,
  Card,
  CardContent,
  Stack,
  Chip,
  Button,
  IconButton,
  Tooltip,
  Alert,
  AlertTitle,
  Fade,
  Grow,
  Divider,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  HomeWork as HomeWorkIcon,
  MeetingRoom as MeetingRoomIcon,
  Description as DescriptionIcon,
  Build as BuildIcon,
  Assessment as AssessmentIcon,
  Add as AddIcon,
  Refresh as RefreshIcon,
  Warning as WarningIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';

import PropertyDashboard from './components/PropertyDashboard';
import PropertiesTable from './components/PropertiesTable';
import UnitsTable from './components/UnitsTable';
import LeasesTable from './components/LeasesTable';
import MaintenanceTable from './components/MaintenanceTable';
import ROIAnalysis from './components/ROIAnalysis';
import AddPropertyModal from './components/AddPropertyModal';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`property-tabpanel-${index}`}
      aria-labelledby={`property-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ py: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export const PropertyManagement: React.FC = () => {
  const [currentTab, setCurrentTab] = useState(0);
  const [refreshKey, setRefreshKey] = useState(0);
  const [addPropertyModalOpen, setAddPropertyModalOpen] = useState(false);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
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

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
          <Stack direction="row" alignItems="center" spacing={2}>
            <HomeWorkIcon sx={{ fontSize: 40, color: 'primary.main' }} />
            <Box>
              <Typography variant="h4" component="h1" fontWeight="bold">
                Property Management
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Comprehensive portfolio tracking and analytics
              </Typography>
            </Box>
          </Stack>

          <Stack direction="row" spacing={2}>
            <Tooltip title="Refresh data">
              <IconButton onClick={handleRefresh} color="primary">
                <RefreshIcon />
              </IconButton>
            </Tooltip>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleAddPropertyClick}
            >
              Add Property
            </Button>
          </Stack>
        </Stack>

        {/* Quick Stats Bar */}
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={0} sx={{ bgcolor: 'primary.main', color: 'white' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="caption" sx={{ opacity: 0.8 }}>
                      Total Properties
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                      12
                    </Typography>
                  </Box>
                  <HomeWorkIcon sx={{ fontSize: 48, opacity: 0.3 }} />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={0} sx={{ bgcolor: 'success.main', color: 'white' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="caption" sx={{ opacity: 0.8 }}>
                      Total Units
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                      148
                    </Typography>
                  </Box>
                  <MeetingRoomIcon sx={{ fontSize: 48, opacity: 0.3 }} />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={0} sx={{ bgcolor: 'info.main', color: 'white' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="caption" sx={{ opacity: 0.8 }}>
                      Occupancy Rate
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                      94.6%
                    </Typography>
                  </Box>
                  <TrendingUpIcon sx={{ fontSize: 48, opacity: 0.3 }} />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card elevation={0} sx={{ bgcolor: 'warning.main', color: 'white' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="caption" sx={{ opacity: 0.8 }}>
                      Monthly NOI
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                      $85.2K
                    </Typography>
                  </Box>
                  <AssessmentIcon sx={{ fontSize: 48, opacity: 0.3 }} />
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Alerts */}
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12} md={6}>
            <Alert severity="warning" variant="outlined">
              <AlertTitle>Leases Expiring Soon</AlertTitle>
              <strong>3 leases</strong> are expiring within the next 60 days. Review renewal status.
            </Alert>
          </Grid>
          <Grid item xs={12} md={6}>
            <Alert severity="error" variant="outlined">
              <AlertTitle>Emergency Maintenance</AlertTitle>
              <strong>2 emergency requests</strong> require immediate attention.
            </Alert>
          </Grid>
        </Grid>
      </Box>

      {/* Navigation Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={currentTab}
          onChange={handleTabChange}
          aria-label="property management tabs"
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab
            icon={<DashboardIcon />}
            iconPosition="start"
            label="Dashboard"
            id="property-tab-0"
          />
          <Tab
            icon={<HomeWorkIcon />}
            iconPosition="start"
            label="Properties"
            id="property-tab-1"
          />
          <Tab
            icon={<MeetingRoomIcon />}
            iconPosition="start"
            label="Units"
            id="property-tab-2"
          />
          <Tab
            icon={<DescriptionIcon />}
            iconPosition="start"
            label="Leases"
            id="property-tab-3"
          />
          <Tab
            icon={<BuildIcon />}
            iconPosition="start"
            label="Maintenance"
            id="property-tab-4"
          />
          <Tab
            icon={<AssessmentIcon />}
            iconPosition="start"
            label="ROI Analysis"
            id="property-tab-5"
          />
        </Tabs>
      </Paper>

      {/* Tab Panels */}
      <TabPanel value={currentTab} index={0}>
        <PropertyDashboard key={refreshKey} />
      </TabPanel>

      <TabPanel value={currentTab} index={1}>
        <PropertiesTable key={refreshKey} />
      </TabPanel>

      <TabPanel value={currentTab} index={2}>
        <UnitsTable key={refreshKey} />
      </TabPanel>

      <TabPanel value={currentTab} index={3}>
        <LeasesTable key={refreshKey} />
      </TabPanel>

      <TabPanel value={currentTab} index={4}>
        <MaintenanceTable key={refreshKey} />
      </TabPanel>

      <TabPanel value={currentTab} index={5}>
        <ROIAnalysis key={refreshKey} />
      </TabPanel>

      {/* Footer Info */}
      <Box sx={{ mt: 4, p: 3, bgcolor: 'background.paper', borderRadius: 2 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Stack direction="row" spacing={1} alignItems="center">
              <CheckCircleIcon color="success" />
              <Box>
                <Typography variant="body2" fontWeight="bold">
                  Real-time Updates
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  All metrics update automatically
                </Typography>
              </Box>
            </Stack>
          </Grid>
          <Grid item xs={12} md={4}>
            <Stack direction="row" spacing={1} alignItems="center">
              <TrendingUpIcon color="primary" />
              <Box>
                <Typography variant="body2" fontWeight="bold">
                  Institutional-Grade Analytics
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  ROI, IRR, and Cap Rate calculations
                </Typography>
              </Box>
            </Stack>
          </Grid>
          <Grid item xs={12} md={4}>
            <Stack direction="row" spacing={1} alignItems="center">
              <HomeWorkIcon color="info" />
              <Box>
                <Typography variant="body2" fontWeight="bold">
                  Multi-Model Support
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Full ownership, leases, and more
                </Typography>
              </Box>
            </Stack>
          </Grid>
        </Grid>
      </Box>

      {/* Add Property Modal */}
      <AddPropertyModal
        open={addPropertyModalOpen}
        onClose={handleAddPropertyClose}
        onSuccess={handleAddPropertySuccess}
      />
    </Container>
  );
};

export default PropertyManagement;
