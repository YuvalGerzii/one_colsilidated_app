// src/pages/PropertyManagement/components/LeasesTable.tsx
import React from 'react';
import { Paper, Box, Typography, Chip, Alert } from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';
import { useCompany } from '../../../context/CompanyContext';

// NOTE: Sample data removed - leases are now company-specific
// Each company will have its own isolated lease records

const LeasesTable: React.FC = () => {
  const { selectedCompany } = useCompany();

  // Company-specific leases (currently empty - will be loaded from backend API)
  const leases = selectedCompany ? [] : [];
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
    { field: 'rent', headerName: 'Monthly Rent', width: 130, valueFormatter: (value: any) => `$${value}` },
  ];

  return (
    <Box>
      <Typography variant="h6" fontWeight="bold" sx={{ mb: 3 }}>
        Lease Schedule & Expiration Tracking {selectedCompany && `- ${selectedCompany.name}`}
      </Typography>

      {!selectedCompany ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          Please select a company to view lease schedule.
        </Alert>
      ) : leases.length === 0 ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          No leases found for {selectedCompany.name}. Leases are linked to units - add properties and units first.
        </Alert>
      ) : null}

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={leases}
          columns={columns}
          pageSizeOptions={[25, 50, 100]}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ toolbar: GridToolbar }}
        />
      </Paper>

      {selectedCompany && (
        <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            <strong>Company-Specific Data:</strong> Leases shown here belong only to {selectedCompany.name}'s properties.
            Switch companies to view different lease schedules.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default LeasesTable;
