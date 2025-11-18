import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Container
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import WorkIcon from '@mui/icons-material/Work';
import SchoolIcon from '@mui/icons-material/School';
import BusinessIcon from '@mui/icons-material/Business';

function Home() {
  const navigate = useNavigate();

  const features = [
    {
      title: 'Skill-Gap Analytics',
      description: 'Identify gaps between current skills and market demand with AI-powered analysis',
      icon: <TrendingUpIcon sx={{ fontSize: 60, color: 'primary.main' }} />,
      action: () => navigate('/skill-gap')
    },
    {
      title: 'Job Matching',
      description: 'Smart matching engine connecting displaced workers with new opportunities',
      icon: <WorkIcon sx={{ fontSize: 60, color: 'primary.main' }} />,
      action: () => navigate('/jobs')
    },
    {
      title: 'Reskilling Pathways',
      description: 'Personalized learning recommendations and training program matching',
      icon: <SchoolIcon sx={{ fontSize: 60, color: 'primary.main' }} />,
      action: () => navigate('/worker')
    },
    {
      title: 'Enterprise HR Tools',
      description: 'Workforce planning, risk assessment, and training ROI analytics',
      icon: <BusinessIcon sx={{ fontSize: 60, color: 'primary.main' }} />,
      action: () => navigate('/enterprise')
    }
  ];

  return (
    <Container>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Workforce Transition Platform
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          AI-powered platform addressing labor market disruption and inequality
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 800, mx: 'auto' }}>
          Navigate the future of work with intelligent tools for skill development, job matching,
          and workforce planning in the age of automation.
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {features.map((feature, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box sx={{ mb: 2 }}>
                  {feature.icon}
                </Box>
                <Typography variant="h5" component="h2" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
              <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                <Button
                  size="large"
                  variant="contained"
                  onClick={feature.action}
                >
                  Learn More
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 6, p: 4, bgcolor: 'primary.main', color: 'white', borderRadius: 2 }}>
        <Typography variant="h4" gutterBottom>
          The Challenge
        </Typography>
        <Typography variant="body1" paragraph>
          Automation threatens millions of jobs. Inequality grows. Skill mismatch widens.
        </Typography>
        <Typography variant="h4" gutterBottom sx={{ mt: 3 }}>
          Our Solution
        </Typography>
        <Typography variant="body1">
          A comprehensive platform combining predictive analytics, personalized reskilling,
          and intelligent job matching to help workers and organizations navigate the
          future of work.
        </Typography>
      </Box>
    </Container>
  );
}

export default Home;
