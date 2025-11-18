// src/components/layout/Layout.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Box, Toolbar, Container } from '@mui/material';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { Breadcrumbs } from '../common/Breadcrumbs';
import { useUIStore } from '../../store/uiStore';

export const Layout: React.FC = () => {
  const { sidebarOpen } = useUIStore();

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <Header />
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${sidebarOpen ? 260 : 0}px)` },
          ml: { sm: sidebarOpen ? '260px' : 0 },
          transition: 'margin 0.3s, width 0.3s',
        }}
      >
        <Toolbar /> {/* Spacer for fixed header */}
        <Container maxWidth="xl" sx={{ mt: 2 }}>
          <Breadcrumbs />
          <Outlet />
        </Container>
      </Box>
    </Box>
  );
};
