// src/pages/PropertyManagement/components/MaintenanceTable.tsx
import React from 'react';
import { Paper, Box, Typography, Chip } from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';

const sampleMaintenance = [
  { id: 1, property: 'Maple Apartments', unit: '1A', category: 'Plumbing', description: 'Leaky faucet', priority: 'Medium', status: 'Open', cost: 150, reported: '2024-11-01' },
  { id: 2, property: 'Oak Plaza', unit: '101', category: 'HVAC', description: 'No heat', priority: 'Emergency', status: 'In Progress', cost: 500, reported: '2024-11-04' },
];

const MaintenanceTable: React.FC = () => {
  const columns: GridColDef[] = [
    { field: 'property', headerName: 'Property', width: 180 },
    { field: 'unit', headerName: 'Unit', width: 100 },
    { field: 'category', headerName: 'Category', width: 120 },
    { field: 'description', headerName: 'Description', width: 200, flex: 1 },
    {
      field: 'priority',
      headerName: 'Priority',
      width: 120,
      renderCell: (params) => {
        const colors: any = { Emergency: 'error', High: 'warning', Medium: 'info', Low: 'success' };
        return <Chip label={params.value} size="small" color={colors[params.value]} />;
      },
    },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'cost', headerName: 'Cost', width: 100, valueFormatter: (params) => `$${params.value}` },
  ];

  return (
    <Box>
      <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
        Maintenance Tracker
      </Typography>
      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={sampleMaintenance}
          columns={columns}
          pageSizeOptions={[25, 50, 100]}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ toolbar: GridToolbar }}
        />
      </Paper>
    </Box>
  );
};

export default MaintenanceTable;
