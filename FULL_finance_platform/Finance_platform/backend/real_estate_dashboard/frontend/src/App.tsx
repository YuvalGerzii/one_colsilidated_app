import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Box } from '@mui/material';
import { theme } from './theme';
import { Layout } from './components/Layout';
import { PropertyManagement } from './pages/PropertyManagement/PropertyManagement';
import { RealEstateTools } from './pages/RealEstate/RealEstateTools';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Navigate to="/property-management" replace />} />
            <Route path="/property-management" element={<PropertyManagement />} />
            <Route path="/real-estate-tools" element={<RealEstateTools />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
