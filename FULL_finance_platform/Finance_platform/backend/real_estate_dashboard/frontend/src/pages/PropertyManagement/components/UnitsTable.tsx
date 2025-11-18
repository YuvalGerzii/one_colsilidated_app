// src/pages/PropertyManagement/components/UnitsTable.tsx
import React from 'react';
import { Paper, Box, Typography, Chip, Stack } from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';

const sampleUnits = [
  { id: 1, property: 'Maple Apartments', unit: '1A', type: '1BR/1BA', status: 'Occupied', tenant: 'John Smith', marketRent: 2500, currentRent: 2400, daysVacant: 0 },
  { id: 2, property: 'Maple Apartments', unit: '1B', type: '1BR/1BA', status: 'Vacant', tenant: null, marketRent: 2500, currentRent: 0, daysVacant: 15 },
  { id: 3, property: 'Oak Plaza', unit: '101', type: '2BR/1BA', status: 'Occupied', tenant: 'Jane Doe', marketRent: 1800, currentRent: 1750, daysVacant: 0 },
];

const UnitsTable: React.FC = () => {
  const columns: GridColDef[] = [
    { field: 'property', headerName: 'Property', width: 180 },
    { field: 'unit', headerName: 'Unit #', width: 100 },
    { field: 'type', headerName: 'Type', width: 120 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value}
          size="small"
          color={params.value === 'Occupied' ? 'success' : 'warning'}
        />
      ),
    },
    { field: 'tenant', headerName: 'Tenant', width: 150, flex: 1 },
    { field: 'marketRent', headerName: 'Market Rent', width: 120, valueFormatter: (params) => `$${params.value}` },
    { field: 'currentRent', headerName: 'Current Rent', width: 120, valueFormatter: (params) => `$${params.value}` },
    { field: 'daysVacant', headerName: 'Days Vacant', width: 110 },
  ];

  return (
    <Box>
      <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
        Unit Inventory
      </Typography>
      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={sampleUnits}
          columns={columns}
          pageSizeOptions={[25, 50, 100]}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ toolbar: GridToolbar }}
        />
      </Paper>
    </Box>
  );
};

export default UnitsTable;
