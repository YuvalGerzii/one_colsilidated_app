import React, { SyntheticEvent, useState } from 'react';
import {
  Avatar,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Grid,
  Stack,
  Switch,
  Tab,
  Tabs,
  TextField,
  Typography,
} from '@mui/material';
import {
  Email as EmailIcon,
  Business as BusinessIcon,
  Group as GroupIcon,
  Hub as HubIcon,
} from '@mui/icons-material';

interface TabPanelProps {
  value: number;
  index: number;
  children: React.ReactNode;
}

const TabPanel: React.FC<TabPanelProps> = ({ value, index, children }) => {
  return (
    <Box role="tabpanel" hidden={value !== index} sx={{ mt: value === index ? 3 : 0 }}>
      {value === index && children}
    </Box>
  );
};

export const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [integrations, setIntegrations] = useState({
    netsuite: true,
    salesforce: false,
    snowflake: true,
    quickbooks: false,
  });

  const handleTabChange = (_event: SyntheticEvent, newValue: number) => setActiveTab(newValue);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings & Administration
      </Typography>
      <Typography variant="body1" color="text.secondary" gutterBottom>
        Manage profile preferences, firm configuration, user roles, and data integrations.
      </Typography>

      <Tabs
        value={activeTab}
        onChange={handleTabChange}
        textColor="primary"
        indicatorColor="primary"
        sx={{ mt: 2 }}
        variant="scrollable"
        scrollButtons="auto"
      >
        <Tab label="Profile" icon={<EmailIcon />} iconPosition="start" />
        <Tab label="Company Info" icon={<BusinessIcon />} iconPosition="start" />
        <Tab label="Users" icon={<GroupIcon />} iconPosition="start" />
        <Tab label="Integrations" icon={<HubIcon />} iconPosition="start" />
      </Tabs>

      <TabPanel value={activeTab} index={0}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Profile preferences
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <TextField label="First name" fullWidth defaultValue="Jordan" />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="Last name" fullWidth defaultValue="Lee" />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="Email" type="email" fullWidth defaultValue="jordan@atlaspe.com" />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="Role" fullWidth defaultValue="Principal" />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="Phone" fullWidth placeholder="(+1) 555-123-4567" />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="Time zone" fullWidth defaultValue="EST" />
              </Grid>
            </Grid>
            <Stack direction="row" justifyContent="flex-end" mt={4}>
              <Button variant="contained">Save profile</Button>
            </Stack>
          </CardContent>
        </Card>
      </TabPanel>

      <TabPanel value={activeTab} index={1}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Firm configuration
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <TextField label="Firm name" fullWidth defaultValue="Atlas Private Equity" />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="AUM" fullWidth placeholder="$2.3B" />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="Headquarters" fullWidth defaultValue="New York, NY" />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="Default currency" fullWidth defaultValue="USD" />
              </Grid>
              <Grid item xs={12}>
                <TextField label="Brand tagline" fullWidth placeholder="Empowering growth stories" />
              </Grid>
            </Grid>
            <Stack direction="row" justifyContent="flex-end" mt={4}>
              <Button variant="contained">Save company info</Button>
            </Stack>
          </CardContent>
        </Card>
      </TabPanel>

      <TabPanel value={activeTab} index={2}>
        <Card>
          <CardContent>
            <Stack direction="row" justifyContent="space-between" alignItems="center" mb={3}>
              <Box>
                <Typography variant="h6">User directory</Typography>
                <Typography variant="body2" color="text.secondary">
                  Manage access levels, invite collaborators, and adjust role-based permissions.
                </Typography>
              </Box>
              <Button variant="contained">Invite user</Button>
            </Stack>
            <Grid container spacing={3}>
              {['Priya Patel', 'Alex Morgan', 'Jamie Chen', 'Chris Howard'].map((name, index) => (
                <Grid item xs={12} md={6} key={name}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" spacing={2} alignItems="center">
                        <Avatar>{name.split(' ').map((part) => part[0]).join('')}</Avatar>
                        <Box>
                          <Typography variant="subtitle1">{name}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {index === 0
                              ? 'Partner'
                              : index === 1
                              ? 'Principal'
                              : index === 2
                              ? 'VP, Portfolio Ops'
                              : 'Controller'}
                          </Typography>
                          <Stack direction="row" spacing={1} mt={1}>
                            <Chip label={index === 3 ? 'Finance' : 'Deal Team'} size="small" />
                            <Chip
                              label={index < 2 ? 'Admin' : 'Editor'}
                              color={index < 2 ? 'primary' : 'default'}
                              size="small"
                            />
                          </Stack>
                        </Box>
                      </Stack>
                      <Stack direction="row" justifyContent="flex-end" spacing={1} mt={3}>
                        <Button size="small" variant="outlined">
                          Reset MFA
                        </Button>
                        <Button size="small">Modify role</Button>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      </TabPanel>

      <TabPanel value={activeTab} index={3}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Integrations
            </Typography>
            <Stack spacing={3}>
              {(
                [
                  { key: 'netsuite', label: 'Oracle NetSuite', description: 'Sync GL data and chart of accounts nightly.' },
                  { key: 'salesforce', label: 'Salesforce', description: 'Pull pipeline metrics for revenue forecasting.' },
                  { key: 'snowflake', label: 'Snowflake', description: 'Stream operational KPIs for live dashboards.' },
                  { key: 'quickbooks', label: 'QuickBooks Online', description: 'Automate trial balance ingestion for QoE reviews.' },
                ] as const
              ).map((integration) => (
                <Stack key={integration.key} direction={{ xs: 'column', sm: 'row' }} alignItems={{ sm: 'center' }} spacing={2}>
                  <Box flex={1}>
                    <Typography variant="subtitle1">{integration.label}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {integration.description}
                    </Typography>
                  </Box>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <Typography variant="body2" color="text.secondary">
                      {integrations[integration.key] ? 'Enabled' : 'Disabled'}
                    </Typography>
                    <Switch
                      checked={integrations[integration.key]}
                      onChange={() =>
                        setIntegrations((prev) => ({ ...prev, [integration.key]: !prev[integration.key] }))
                      }
                    />
                  </Stack>
                </Stack>
              ))}
            </Stack>
            <Stack direction="row" justifyContent="flex-end" mt={4}>
              <Button variant="contained">Save integrations</Button>
            </Stack>
          </CardContent>
        </Card>
      </TabPanel>
    </Box>
  );
};
