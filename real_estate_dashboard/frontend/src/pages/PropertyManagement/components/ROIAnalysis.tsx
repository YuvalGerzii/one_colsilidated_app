// src/pages/PropertyManagement/components/ROIAnalysis.tsx
import React from 'react';
import { Paper, Box, Typography, Chip, Grid, Card, CardContent, Stack, Alert } from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';
import { TrendingUp as TrendingUpIcon } from '@mui/icons-material';
import { useCompany } from '../../../context/CompanyContext';

// NOTE: Sample data removed - ROI analysis is now company-specific
// Each company will have its own isolated financial performance metrics

const ROIAnalysis: React.FC = () => {
  const { selectedCompany } = useCompany();

  // Company-specific ROI data (currently empty - will be loaded from backend API)
  const roiData = selectedCompany ? [] : [];
  const hasData = roiData.length > 0;
  const columns: GridColDef[] = [
    { field: 'property', headerName: 'Property', width: 180, flex: 1 },
    { field: 'equity', headerName: 'Equity', width: 130, valueFormatter: (value: any) => `$${(value / 1000).toFixed(0)}K` },
    { field: 'value', headerName: 'Current Value', width: 140, valueFormatter: (value: any) => `$${(value / 1000000).toFixed(1)}M` },
    { field: 'appreciation', headerName: 'Appreciation', width: 140, valueFormatter: (value: any) => `$${(value / 1000).toFixed(0)}K` },
    { field: 'cashFlow', headerName: 'Annual CF', width: 130, valueFormatter: (value: any) => `$${(value / 1000).toFixed(0)}K` },
    { field: 'cashOnCash', headerName: 'CoC Return', width: 120, valueFormatter: (value: any) => `${value}%` },
    { field: 'totalROI', headerName: 'Total ROI', width: 120, valueFormatter: (value: any) => `${value}%` },
    { field: 'irr', headerName: 'IRR', width: 100, valueFormatter: (value: any) => `${value}%` },
  ];

  return (
    <Box>
      <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
        ROI Analysis & Performance Metrics {selectedCompany && `- ${selectedCompany.name}`}
      </Typography>

      {!selectedCompany ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          Please select a company to view ROI analysis.
        </Alert>
      ) : !hasData ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          No ROI data available for {selectedCompany.name}. ROI metrics are calculated from property financial performance data.
        </Alert>
      ) : null}

      {selectedCompany && hasData && (
        <>
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Stack direction="row" alignItems="center" spacing={1}>
                    <TrendingUpIcon color="success" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">Portfolio Avg CoC</Typography>
                      <Typography variant="h5" fontWeight="bold">0%</Typography>
                    </Box>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Typography variant="caption" color="text.secondary">Portfolio Avg IRR</Typography>
                  <Typography variant="h5" fontWeight="bold">0%</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Typography variant="caption" color="text.secondary">Total Appreciation</Typography>
                  <Typography variant="h5" fontWeight="bold">$0</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Typography variant="caption" color="text.secondary">Annual Cash Flow</Typography>
                  <Typography variant="h5" fontWeight="bold">$0</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </>
      )}

      <Paper sx={{ height: 500, width: '100%' }}>
        <DataGrid
          rows={roiData}
          columns={columns}
          pageSizeOptions={[25, 50, 100]}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ toolbar: GridToolbar }}
        />
      </Paper>

      {selectedCompany && (
        <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            <strong>Company-Specific Data:</strong> ROI analysis shown here is calculated only from {selectedCompany.name}'s properties.
            Switch companies to view different performance metrics.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default ROIAnalysis;
