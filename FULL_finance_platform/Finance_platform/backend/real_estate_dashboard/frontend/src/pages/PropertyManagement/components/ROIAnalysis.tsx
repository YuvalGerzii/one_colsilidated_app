// src/pages/PropertyManagement/components/ROIAnalysis.tsx
import React from 'react';
import { Paper, Box, Typography, Chip, Grid, Card, CardContent, Stack } from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';
import { TrendingUp as TrendingUpIcon } from '@mui/icons-material';

const sampleROI = [
  { id: 1, property: 'Maple Apartments', equity: 750000, value: 3200000, appreciation: 200000, cashFlow: 180000, cashOnCash: 12.5, totalROI: 50.7, irr: 15.2 },
  { id: 2, property: 'Oak Plaza', equity: 450000, value: 1800000, appreciation: 0, cashFlow: 96000, cashOnCash: 10.7, totalROI: 21.3, irr: 10.7 },
];

const ROIAnalysis: React.FC = () => {
  const columns: GridColDef[] = [
    { field: 'property', headerName: 'Property', width: 180, flex: 1 },
    { field: 'equity', headerName: 'Equity', width: 130, valueFormatter: (params) => `$${(params.value / 1000).toFixed(0)}K` },
    { field: 'value', headerName: 'Current Value', width: 140, valueFormatter: (params) => `$${(params.value / 1000000).toFixed(1)}M` },
    { field: 'appreciation', headerName: 'Appreciation', width: 140, valueFormatter: (params) => `$${(params.value / 1000).toFixed(0)}K` },
    { field: 'cashFlow', headerName: 'Annual CF', width: 130, valueFormatter: (params) => `$${(params.value / 1000).toFixed(0)}K` },
    { field: 'cashOnCash', headerName: 'CoC Return', width: 120, valueFormatter: (params) => `${params.value}%` },
    { field: 'totalROI', headerName: 'Total ROI', width: 120, valueFormatter: (params) => `${params.value}%` },
    { field: 'irr', headerName: 'IRR', width: 100, valueFormatter: (params) => `${params.value}%` },
  ];

  return (
    <Box>
      <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
        ROI Analysis & Performance Metrics
      </Typography>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Card elevation={3}>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={1}>
                <TrendingUpIcon color="success" />
                <Box>
                  <Typography variant="caption" color="text.secondary">Portfolio Avg CoC</Typography>
                  <Typography variant="h5" fontWeight="bold">11.6%</Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="caption" color="text.secondary">Portfolio Avg IRR</Typography>
              <Typography variant="h5" fontWeight="bold">13.0%</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="caption" color="text.secondary">Total Appreciation</Typography>
              <Typography variant="h5" fontWeight="bold">$200K</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="caption" color="text.secondary">Annual Cash Flow</Typography>
              <Typography variant="h5" fontWeight="bold">$276K</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ height: 500, width: '100%' }}>
        <DataGrid
          rows={sampleROI}
          columns={columns}
          pageSizeOptions={[25, 50, 100]}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ toolbar: GridToolbar }}
        />
      </Paper>
    </Box>
  );
};

export default ROIAnalysis;
