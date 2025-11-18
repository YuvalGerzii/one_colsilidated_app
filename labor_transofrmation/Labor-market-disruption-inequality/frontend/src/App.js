import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  CssBaseline,
  Box,
  Button
} from '@mui/material';
import WorkerDashboard from './pages/WorkerDashboard';
import EnterpriseDashboard from './pages/EnterpriseDashboard';
import JobMatching from './pages/JobMatching';
import SkillGapAnalysis from './pages/SkillGapAnalysis';
import MarketTrends from './pages/MarketTrends';
import Home from './pages/Home';
import DigitalTwinDashboard from './pages/DigitalTwinDashboard';
import GovernmentDashboard from './pages/GovernmentDashboard';
import AIAutopilot from './pages/AIAutopilot';
import CareerSimulator from './pages/CareerSimulator';
import AgentAssistant from './pages/AgentAssistant';
import LearningHub from './pages/LearningHub';
import ProgressDashboard from './pages/ProgressDashboard';
import CorporateTransformation from './pages/CorporateTransformation';
import GigEconomyHub from './pages/GigEconomyHub';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                Workforce Transition Platform 2.3
              </Typography>
              <Button color="inherit" component={Link} to="/">
                Home
              </Button>
              <Button color="inherit" component={Link} to="/progress">
                Progress
              </Button>
              <Button color="inherit" component={Link} to="/learning">
                Learning
              </Button>
              <Button color="inherit" component={Link} to="/agents">
                Agents
              </Button>
              <Button color="inherit" component={Link} to="/autopilot">
                Autopilot
              </Button>
              <Button color="inherit" component={Link} to="/digital-twin">
                Digital Twin
              </Button>
              <Button color="inherit" component={Link} to="/career-simulator">
                Career Sim
              </Button>
              <Button color="inherit" component={Link} to="/government">
                Government
              </Button>
              <Button color="inherit" component={Link} to="/corporate">
                Corporate
              </Button>
              <Button color="inherit" component={Link} to="/gig">
                Gig Economy
              </Button>
            </Toolbar>
          </AppBar>

          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/worker" element={<WorkerDashboard />} />
              <Route path="/enterprise" element={<EnterpriseDashboard />} />
              <Route path="/jobs" element={<JobMatching />} />
              <Route path="/skill-gap" element={<SkillGapAnalysis />} />
              <Route path="/trends" element={<MarketTrends />} />
              <Route path="/digital-twin" element={<DigitalTwinDashboard />} />
              <Route path="/government" element={<GovernmentDashboard />} />
              <Route path="/autopilot" element={<AIAutopilot />} />
              <Route path="/career-simulator" element={<CareerSimulator />} />
              <Route path="/agents" element={<AgentAssistant />} />
              <Route path="/learning" element={<LearningHub />} />
              <Route path="/progress" element={<ProgressDashboard />} />
              <Route path="/corporate" element={<CorporateTransformation />} />
              <Route path="/gig" element={<GigEconomyHub />} />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
