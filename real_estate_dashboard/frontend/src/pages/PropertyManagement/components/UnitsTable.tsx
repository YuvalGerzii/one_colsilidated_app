// src/pages/PropertyManagement/components/UnitsTable.tsx
import React from 'react';
import { Paper, Box, Typography, Chip, Stack, Alert } from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';
import { useCompany } from '../../../context/CompanyContext';

// NOTE: Sample data removed - units are now company-specific
// Each company will have its own isolated unit inventory

const UnitsTable: React.FC = () => {
  const { selectedCompany } = useCompany();

  // Company-specific units (currently empty - will be loaded from backend API)
  const units = selectedCompany ? [] : [];
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
    { field: 'marketRent', headerName: 'Market Rent', width: 120, valueFormatter: (value: any) => `$${value}` },
    { field: 'currentRent', headerName: 'Current Rent', width: 120, valueFormatter: (value: any) => `$${value}` },
    { field: 'daysVacant', headerName: 'Days Vacant', width: 110 },
  ];

  return (
    <Box>
      <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
        Unit Inventory {selectedCompany && `- ${selectedCompany.name}`}
      </Typography>

      {!selectedCompany ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          Please select a company to view unit inventory.
        </Alert>
      ) : units.length === 0 ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          No units found for {selectedCompany.name}. Units are linked to properties - add properties first.
        </Alert>
      ) : null}

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={units}
          columns={columns}
          pageSizeOptions={[25, 50, 100]}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ toolbar: GridToolbar }}
        />
      </Paper>

      {selectedCompany && (
        <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            <strong>Company-Specific Data:</strong> Units shown here belong only to {selectedCompany.name}'s properties.
            Switch companies to view different unit inventories.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default UnitsTable;
