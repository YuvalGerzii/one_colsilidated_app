// src/pages/PropertyManagement/components/MaintenanceTable.tsx
import React from 'react';
import { Paper, Box, Typography, Chip, Alert } from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';
import { useCompany } from '../../../context/CompanyContext';

// NOTE: Sample data removed - maintenance tickets are now company-specific
// Each company will have its own isolated maintenance records

const MaintenanceTable: React.FC = () => {
  const { selectedCompany } = useCompany();

  // Company-specific maintenance tickets (currently empty - will be loaded from backend API)
  const maintenanceTickets = selectedCompany ? [] : [];
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
    { field: 'cost', headerName: 'Cost', width: 100, valueFormatter: (value: any) => `$${value}` },
  ];

  return (
    <Box>
      <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
        Maintenance Tracker {selectedCompany && `- ${selectedCompany.name}`}
      </Typography>

      {!selectedCompany ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          Please select a company to view maintenance requests.
        </Alert>
      ) : maintenanceTickets.length === 0 ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          No maintenance requests found for {selectedCompany.name}. Maintenance is linked to properties and units.
        </Alert>
      ) : null}

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={maintenanceTickets}
          columns={columns}
          pageSizeOptions={[25, 50, 100]}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ toolbar: GridToolbar }}
        />
      </Paper>

      {selectedCompany && (
        <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            <strong>Company-Specific Data:</strong> Maintenance requests shown here belong only to {selectedCompany.name}'s properties.
            Switch companies to view different maintenance records.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default MaintenanceTable;
