// src/pages/PropertyManagement/components/LeasesTable.tsx
import React from 'react';
import { Paper, Box, Typography, Chip } from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';

const sampleLeases = [
  { id: 1, property: 'Maple Apartments', unit: '1A', tenant: 'John Smith', startDate: '2024-03-01', endDate: '2025-02-28', rent: 2400, daysToExpiry: 90, risk: 'MODERATE' },
  { id: 2, property: 'Oak Plaza', unit: '101', tenant: 'Jane Doe', startDate: '2024-01-01', endDate: '2024-12-31', rent: 1750, daysToExpiry: 30, risk: 'CRITICAL' },
];

const LeasesTable: React.FC = () => {
  const columns: GridColDef[] = [
    { field: 'property', headerName: 'Property', width: 180 },
    { field: 'unit', headerName: 'Unit', width: 100 },
    { field: 'tenant', headerName: 'Tenant', width: 150, flex: 1 },
    { field: 'endDate', headerName: 'Lease End', width: 120 },
    { field: 'daysToExpiry', headerName: 'Days to Expiry', width: 130 },
    {
      field: 'risk',
      headerName: 'Risk Level',
      width: 120,
      renderCell: (params) => {
        const colors: any = { CRITICAL: 'error', HIGH: 'warning', MODERATE: 'info', LOW: 'success' };
        return <Chip label={params.value} size="small" color={colors[params.value]} />;
      },
    },
    { field: 'rent', headerName: 'Monthly Rent', width: 130, valueFormatter: (params) => `$${params.value}` },
  ];

  return (
    <Box>
      <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
        Lease Schedule & Expiration Tracking
      </Typography>
      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={sampleLeases}
          columns={columns}
          pageSizeOptions={[25, 50, 100]}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ toolbar: GridToolbar }}
        />
      </Paper>
    </Box>
  );
};

export default LeasesTable;
