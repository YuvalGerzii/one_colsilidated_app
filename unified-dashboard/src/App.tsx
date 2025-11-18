import { useState, useEffect } from 'react'
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  AppBar,
  Toolbar,
  Chip,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  CircularProgress,
} from '@mui/material'
import {
  Dashboard as DashboardIcon,
  AccountBalance as FinanceIcon,
  Home as RealEstateIcon,
  People as BondIcon,
  Storage as LegacyIcon,
  Work as LaborIcon,
  Menu as MenuIcon,
  Settings as SettingsIcon,
  Insights as InsightsIcon,
  Speed as SpeedIcon,
  CheckCircle as OnlineIcon,
  Cancel as OfflineIcon,
  OpenInNew as OpenIcon,
} from '@mui/icons-material'
import axios from 'axios'

interface PlatformService {
  id: string
  name: string
  description: string
  icon: React.ReactNode
  color: string
  apiUrl: string
  uiUrl: string
  port: number
  features: string[]
  status: 'online' | 'offline' | 'checking'
}

const platforms: PlatformService[] = [
  {
    id: 'finance',
    name: 'Finance Platform',
    description: 'Portfolio management, market data analysis, and investment tracking',
    icon: <FinanceIcon sx={{ fontSize: 40 }} />,
    color: '#10b981',
    apiUrl: 'http://localhost:8100',
    uiUrl: 'http://localhost:3102',
    port: 8100,
    features: ['Market Data', 'Portfolio Analytics', 'Trading Agents', 'Financial Models'],
    status: 'checking',
  },
  {
    id: 'realestate',
    name: 'Real Estate Dashboard',
    description: 'Property management, financial modeling, and deal analysis',
    icon: <RealEstateIcon sx={{ fontSize: 40 }} />,
    color: '#3b82f6',
    apiUrl: 'http://localhost:8101',
    uiUrl: 'http://localhost:3103',
    port: 8101,
    features: ['Property Management', 'Deal Analysis', 'Tax Optimization', 'Market Intelligence'],
    status: 'checking',
  },
  {
    id: 'bondai',
    name: 'Bond.AI',
    description: 'AI-powered connection intelligence and relationship scoring',
    icon: <BondIcon sx={{ fontSize: 40 }} />,
    color: '#8b5cf6',
    apiUrl: 'http://localhost:8102',
    uiUrl: 'http://localhost:3104',
    port: 8102,
    features: ['Connection Matching', 'Network Analysis', 'Opportunity Detection', '11 AI Agents'],
    status: 'checking',
  },
  {
    id: 'legacy',
    name: 'Legacy Systems',
    description: 'AI-powered legacy code transformation and process automation',
    icon: <LegacyIcon sx={{ fontSize: 40 }} />,
    color: '#f59e0b',
    apiUrl: 'http://localhost:8103',
    uiUrl: '',
    port: 8103,
    features: ['Code Analysis', 'Process Automation', 'Document Extraction', 'Knowledge Graphs'],
    status: 'checking',
  },
  {
    id: 'labor',
    name: 'Labor Transformation',
    description: 'Labor market analysis and freelance worker platform',
    icon: <LaborIcon sx={{ fontSize: 40 }} />,
    color: '#ec4899',
    apiUrl: 'http://localhost:8104',
    uiUrl: 'http://localhost:3105',
    port: 8104,
    features: ['Labor Market Analysis', 'Freelance Hub', 'Skills Matching', 'Study Buddy'],
    status: 'checking',
  },
]

const infrastructureServices = [
  { name: 'Traefik Dashboard', url: 'http://localhost:8181', description: 'API Gateway & Load Balancer' },
  { name: 'Grafana', url: 'http://localhost:3101', description: 'Monitoring Dashboards' },
  { name: 'Prometheus', url: 'http://localhost:9190', description: 'Metrics Collection' },
  { name: 'RabbitMQ', url: 'http://localhost:15772', description: 'Message Queue Management' },
]

function App() {
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [platformStatuses, setPlatformStatuses] = useState<Record<string, 'online' | 'offline' | 'checking'>>({})

  useEffect(() => {
    const checkServices = async () => {
      const statuses: Record<string, 'online' | 'offline' | 'checking'> = {}

      for (const platform of platforms) {
        try {
          await axios.get(`${platform.apiUrl}/health`, { timeout: 3000 })
          statuses[platform.id] = 'online'
        } catch {
          try {
            await axios.get(`${platform.apiUrl}/api/v1/health`, { timeout: 3000 })
            statuses[platform.id] = 'online'
          } catch {
            statuses[platform.id] = 'offline'
          }
        }
      }

      setPlatformStatuses(statuses)
    }

    checkServices()
    const interval = setInterval(checkServices, 30000)
    return () => clearInterval(interval)
  }, [])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <OnlineIcon sx={{ color: '#10b981' }} />
      case 'offline':
        return <OfflineIcon sx={{ color: '#ef4444' }} />
      default:
        return <CircularProgress size={20} />
    }
  }

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, bgcolor: '#1e293b' }}>
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={() => setDrawerOpen(!drawerOpen)}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <DashboardIcon sx={{ mr: 1 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            Unified Platform Dashboard
          </Typography>
          <Chip
            label={`${Object.values(platformStatuses).filter(s => s === 'online').length}/${platforms.length} Online`}
            color="success"
            size="small"
          />
        </Toolbar>
      </AppBar>

      <Drawer
        variant="temporary"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        sx={{
          width: 280,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 280,
            boxSizing: 'border-box',
            bgcolor: '#1e293b',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto', p: 2 }}>
          <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
            PLATFORMS
          </Typography>
          <List>
            {platforms.map((platform) => (
              <ListItem
                key={platform.id}
                component="a"
                href={platform.uiUrl || '#'}
                target="_blank"
                sx={{
                  borderRadius: 1,
                  mb: 0.5,
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.05)' }
                }}
              >
                <ListItemIcon sx={{ color: platform.color, minWidth: 40 }}>
                  {platform.icon}
                </ListItemIcon>
                <ListItemText primary={platform.name} />
                {getStatusIcon(platformStatuses[platform.id] || 'checking')}
              </ListItem>
            ))}
          </List>

          <Divider sx={{ my: 2 }} />

          <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
            INFRASTRUCTURE
          </Typography>
          <List>
            {infrastructureServices.map((service) => (
              <ListItem
                key={service.name}
                component="a"
                href={service.url}
                target="_blank"
                sx={{
                  borderRadius: 1,
                  mb: 0.5,
                  '&:hover': { bgcolor: 'rgba(255,255,255,0.05)' }
                }}
              >
                <ListItemIcon sx={{ minWidth: 40 }}>
                  <SettingsIcon />
                </ListItemIcon>
                <ListItemText
                  primary={service.name}
                  secondary={service.description}
                />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        <Container maxWidth="xl">
          {/* Header Stats */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={3}>
              <Card sx={{ bgcolor: '#1e293b' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                      <Typography color="text.secondary" variant="body2">
                        Total Platforms
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700 }}>
                        {platforms.length}
                      </Typography>
                    </Box>
                    <DashboardIcon sx={{ fontSize: 40, color: '#6366f1' }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card sx={{ bgcolor: '#1e293b' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                      <Typography color="text.secondary" variant="body2">
                        Services Online
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: '#10b981' }}>
                        {Object.values(platformStatuses).filter(s => s === 'online').length}
                      </Typography>
                    </Box>
                    <OnlineIcon sx={{ fontSize: 40, color: '#10b981' }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card sx={{ bgcolor: '#1e293b' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                      <Typography color="text.secondary" variant="body2">
                        AI Agents
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700 }}>
                        26+
                      </Typography>
                    </Box>
                    <InsightsIcon sx={{ fontSize: 40, color: '#8b5cf6' }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card sx={{ bgcolor: '#1e293b' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                      <Typography color="text.secondary" variant="body2">
                        API Endpoints
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700 }}>
                        100+
                      </Typography>
                    </Box>
                    <SpeedIcon sx={{ fontSize: 40, color: '#f59e0b' }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Platform Cards */}
          <Typography variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
            Platform Services
          </Typography>
          <Grid container spacing={3}>
            {platforms.map((platform) => (
              <Grid item xs={12} md={6} lg={4} key={platform.id}>
                <Card
                  sx={{
                    bgcolor: '#1e293b',
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    borderTop: `3px solid ${platform.color}`,
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                    },
                  }}
                >
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Box sx={{ color: platform.color, mr: 2 }}>
                        {platform.icon}
                      </Box>
                      <Box sx={{ flexGrow: 1 }}>
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                          {platform.name}
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {getStatusIcon(platformStatuses[platform.id] || 'checking')}
                          <Typography variant="caption" color="text.secondary">
                            Port {platform.port}
                          </Typography>
                        </Box>
                      </Box>
                    </Box>

                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {platform.description}
                    </Typography>

                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {platform.features.map((feature) => (
                        <Chip
                          key={feature}
                          label={feature}
                          size="small"
                          sx={{
                            bgcolor: 'rgba(255,255,255,0.05)',
                            fontSize: '0.7rem',
                          }}
                        />
                      ))}
                    </Box>
                  </CardContent>

                  <CardActions sx={{ p: 2, pt: 0 }}>
                    {platform.uiUrl && (
                      <Button
                        variant="contained"
                        size="small"
                        href={platform.uiUrl}
                        target="_blank"
                        endIcon={<OpenIcon />}
                        sx={{ bgcolor: platform.color }}
                      >
                        Open UI
                      </Button>
                    )}
                    <Button
                      variant="outlined"
                      size="small"
                      href={`${platform.apiUrl}/docs`}
                      target="_blank"
                    >
                      API Docs
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Infrastructure Section */}
          <Typography variant="h5" sx={{ mt: 4, mb: 3, fontWeight: 600 }}>
            Infrastructure & Monitoring
          </Typography>
          <Grid container spacing={3}>
            {infrastructureServices.map((service) => (
              <Grid item xs={12} sm={6} md={3} key={service.name}>
                <Card
                  sx={{
                    bgcolor: '#1e293b',
                    cursor: 'pointer',
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                    },
                  }}
                  component="a"
                  href={service.url}
                  target="_blank"
                  style={{ textDecoration: 'none' }}
                >
                  <CardContent>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      {service.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {service.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Port Mapping Reference */}
          <Typography variant="h5" sx={{ mt: 4, mb: 3, fontWeight: 600 }}>
            Port Mapping Reference
          </Typography>
          <Card sx={{ bgcolor: '#1e293b' }}>
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    Gateway & Dashboard
                  </Typography>
                  <Typography variant="body2">8180 - Traefik (HTTP)</Typography>
                  <Typography variant="body2">8443 - Traefik (HTTPS)</Typography>
                  <Typography variant="body2">3100 - Unified Dashboard</Typography>
                  <Typography variant="body2">8181 - Traefik Dashboard</Typography>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    Backend APIs
                  </Typography>
                  <Typography variant="body2">8100 - Finance API</Typography>
                  <Typography variant="body2">8101 - Real Estate API</Typography>
                  <Typography variant="body2">8102 - Bond.AI API</Typography>
                  <Typography variant="body2">8103 - Legacy Systems API</Typography>
                  <Typography variant="body2">8104 - Labor API</Typography>
                  <Typography variant="body2">8105 - Bond.AI Agents</Typography>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    Infrastructure
                  </Typography>
                  <Typography variant="body2">5532 - PostgreSQL</Typography>
                  <Typography variant="body2">6479 - Redis</Typography>
                  <Typography variant="body2">5772/15772 - RabbitMQ</Typography>
                  <Typography variant="body2">11534 - Ollama LLM</Typography>
                  <Typography variant="body2">9190 - Prometheus</Typography>
                  <Typography variant="body2">3101 - Grafana</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Container>
      </Box>
    </Box>
  )
}

export default App
