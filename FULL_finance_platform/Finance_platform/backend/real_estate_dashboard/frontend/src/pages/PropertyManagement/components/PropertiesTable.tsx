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
import AddPropertyModal from './AddPropertyModal';

// Sample data
const sampleProperties = [
  {
    id: 1,
    propertyId: 'PROP-001',
    name: 'Maple Apartments',
    address: '123 Maple St, Portland, OR',
    type: 'Multifamily',
    units: 24,
    occupancy: 96,
    value: 3200000,
    noi: 18500,
    capRate: 6.9,
    status: 'Active',
  },
  {
    id: 2,
    propertyId: 'PROP-002',
    name: 'Oak Plaza',
    address: '456 Oak Ave, Denver, CO',
    type: 'Multifamily',
    units: 12,
    occupancy: 92,
    value: 1800000,
    noi: 9200,
    capRate: 6.1,
    status: 'Active',
  },
  {
    id: 3,
    propertyId: 'PROP-003',
    name: 'Pine Tower',
    address: '789 Pine Blvd, Seattle, WA',
    type: 'Commercial',
    units: 8,
    occupancy: 98,
    value: 2500000,
    noi: 15000,
    capRate: 7.2,
    status: 'Active',
  },
];

const PropertiesTable: React.FC = () => {
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
      valueFormatter: (params) => `$${(params.value / 1000000).toFixed(1)}M`,
    },
    {
      field: 'noi',
      headerName: 'Monthly NOI',
      width: 130,
      valueFormatter: (params) => `$${params.value.toLocaleString()}`,
    },
    {
      field: 'capRate',
      headerName: 'Cap Rate',
      width: 100,
      valueFormatter: (params) => `${params.value}%`,
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

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
        <Typography variant="h6" fontWeight="bold">
          Property Master List
        </Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={handleAddPropertyClick}>
          Add New Property
        </Button>
      </Stack>

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={sampleProperties}
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

      <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
        <Typography variant="caption" color="text.secondary">
          <strong>Tip:</strong> Click on any property to view detailed unit inventory, financials, and performance metrics.
          Use the filters and search to quickly find specific properties.
        </Typography>
      </Box>

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
