// src/pages/PropertyManagement/components/PropertiesTable.tsx
import React, { useState } from 'react';
import {
  Paper,
  Box,
  Typography,
  Button,
  Stack,
  Chip,
  IconButton,
  Tooltip,
  TextField,
  InputAdornment,
  Alert,
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridToolbar,
} from '@mui/x-data-grid';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as VisibilityIcon,
  Search as SearchIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useCompany } from '../../../context/CompanyContext';
import AddPropertyModal from './AddPropertyModal';

// NOTE: Sample data removed - properties are now company-specific
// Each company will have its own isolated property data

const PropertiesTable: React.FC = () => {
  const { selectedCompany } = useCompany();
  const [searchText, setSearchText] = useState('');
  const [addPropertyModalOpen, setAddPropertyModalOpen] = useState(false);

  const handleAddPropertyClick = () => {
    setAddPropertyModalOpen(true);
  };

  const handleAddPropertyClose = () => {
    setAddPropertyModalOpen(false);
  };

  const handleAddPropertySuccess = () => {
    // Refresh the properties list
    // This will be implemented when we connect to the backend
  };

  const columns: GridColDef[] = [
    {
      field: 'propertyId',
      headerName: 'Property ID',
      width: 120,
      renderCell: (params) => (
        <Chip label={params.value} size="small" color="primary" variant="outlined" />
      ),
    },
    {
      field: 'name',
      headerName: 'Property Name',
      width: 200,
      flex: 1,
    },
    {
      field: 'address',
      headerName: 'Address',
      width: 250,
      flex: 1,
    },
    {
      field: 'type',
      headerName: 'Type',
      width: 130,
      renderCell: (params) => (
        <Chip label={params.value} size="small" />
      ),
    },
    {
      field: 'units',
      headerName: 'Units',
      width: 80,
      align: 'center',
      headerAlign: 'center',
    },
    {
      field: 'occupancy',
      headerName: 'Occupancy',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={`${params.value}%`}
          size="small"
          color={params.value >= 95 ? 'success' : params.value >= 90 ? 'warning' : 'error'}
        />
      ),
    },
    {
      field: 'value',
      headerName: 'Value',
      width: 130,
      valueFormatter: (value: any) => `$${(value / 1000000).toFixed(1)}M`,
    },
    {
      field: 'noi',
      headerName: 'Monthly NOI',
      width: 130,
      valueFormatter: (value: any) => `$${value.toLocaleString()}`,
    },
    {
      field: 'capRate',
      headerName: 'Cap Rate',
      width: 100,
      valueFormatter: (value: any) => `${value}%`,
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value}
          size="small"
          color={params.value === 'Active' ? 'success' : 'default'}
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <Tooltip title="View Details">
            <IconButton size="small" color="primary">
              <VisibilityIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Edit">
            <IconButton size="small" color="info">
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton size="small" color="error">
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Stack>
      ),
    },
  ];

  // Company-specific properties (currently empty - will be loaded from backend API)
  const properties = selectedCompany ? [] : [];

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
        <Typography variant="h6" fontWeight="bold">
          Property Master List {selectedCompany && `- ${selectedCompany.name}`}
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddPropertyClick}
          disabled={!selectedCompany}
        >
          Add New Property
        </Button>
      </Stack>

      {!selectedCompany ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          Please select a company to view and manage properties.
        </Alert>
      ) : properties.length === 0 ? (
        <Alert severity="info" sx={{ mb: 3 }}>
          No properties found for {selectedCompany.name}. Click "Add New Property" to get started.
        </Alert>
      ) : null}

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={properties}
          columns={columns}
          pageSizeOptions={[10, 25, 50, 100]}
          initialState={{
            pagination: { paginationModel: { pageSize: 25 } },
          }}
          disableRowSelectionOnClick
          slots={{ toolbar: GridToolbar }}
          slotProps={{
            toolbar: {
              showQuickFilter: true,
              quickFilterProps: { debounceMs: 500 },
            },
          }}
        />
      </Paper>

      {selectedCompany && (
        <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            <strong>Company-Specific Data:</strong> Properties shown here belong only to {selectedCompany.name}.
            Switch companies to view different property portfolios.
          </Typography>
        </Box>
      )}

      {/* Add Property Modal */}
      <AddPropertyModal
        open={addPropertyModalOpen}
        onClose={handleAddPropertyClose}
        onSuccess={handleAddPropertySuccess}
      />
    </Box>
  );
};

export default PropertiesTable;
