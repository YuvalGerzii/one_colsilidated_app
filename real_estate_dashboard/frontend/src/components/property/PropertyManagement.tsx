import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Button,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Chip,
  Alert,
  CircularProgress,
  Menu,
  MenuItem,
  Stack,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  MoreVert as MoreVertIcon,
  Home as HomeIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { api } from '../../services/apiClient';
import { useCompany } from '../../context/CompanyContext';
import { Property, PropertyDialog } from './PropertyDialog';

export const PropertyManagement: React.FC = () => {
  const { selectedCompany } = useCompany();
  const [properties, setProperties] = useState<Property[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(null);
  const [dialogMode, setDialogMode] = useState<'create' | 'edit'>('create');
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [menuProperty, setMenuProperty] = useState<Property | null>(null);

  useEffect(() => {
    if (selectedCompany) {
      loadProperties();
    } else {
      setProperties([]);
      setLoading(false);
    }
  }, [selectedCompany]);

  const loadProperties = async () => {
    if (!selectedCompany) return;

    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/property-management/properties', {
        params: { company_id: selectedCompany.id },
      });
      setProperties(response.data);
    } catch (err: any) {
      console.error('Error loading properties:', err);
      setError('Failed to load properties. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddProperty = () => {
    setSelectedProperty(null);
    setDialogMode('create');
    setDialogOpen(true);
  };

  const handleEditProperty = (property: Property) => {
    setSelectedProperty(property);
    setDialogMode('edit');
    setDialogOpen(true);
    handleMenuClose();
  };

  const handleDeleteClick = (property: Property) => {
    setSelectedProperty(property);
    setDeleteDialogOpen(true);
    handleMenuClose();
  };

  const handleDeleteConfirm = async () => {
    if (!selectedProperty?.id) return;

    setLoading(true);
    try {
      await api.delete(`/property-management/properties/${selectedProperty.id}`);
      setDeleteDialogOpen(false);
      setSelectedProperty(null);
      await loadProperties();
    } catch (err: any) {
      console.error('Error deleting property:', err);
      setError('Failed to delete property. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, property: Property) => {
    setAnchorEl(event.currentTarget);
    setMenuProperty(property);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setMenuProperty(null);
  };

  const getStatusColor = (status: string): 'success' | 'warning' | 'error' | 'default' => {
    switch (status) {
      case 'ACTIVE':
        return 'success';
      case 'UNDER_CONTRACT':
        return 'warning';
      case 'SOLD':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatCurrency = (value?: number) => {
    if (!value) return '-';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  if (!selectedCompany) {
    return (
      <Card>
        <CardContent>
          <Alert severity="info">
            Please select a company to view and manage properties.
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <Box>
      <Card>
        <CardContent>
          {/* Header */}
          <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <HomeIcon sx={{ fontSize: 28, color: 'primary.main' }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Property Portfolio
              </Typography>
              <Chip
                label={`${properties.length} ${properties.length === 1 ? 'Property' : 'Properties'}`}
                size="small"
                color="primary"
              />
            </Box>
            <Stack direction="row" spacing={1}>
              <Tooltip title="Refresh">
                <IconButton onClick={loadProperties} disabled={loading} size="small">
                  <RefreshIcon />
                </IconButton>
              </Tooltip>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAddProperty}
                disabled={loading}
              >
                Add Property
              </Button>
            </Stack>
          </Stack>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}

          {/* Table */}
          {loading && properties.length === 0 ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
              <CircularProgress />
            </Box>
          ) : properties.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 8 }}>
              <HomeIcon sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                No Properties Yet
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Add your first property to get started with portfolio management.
              </Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAddProperty}
              >
                Add First Property
              </Button>
            </Box>
          ) : (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ fontWeight: 600 }}>Property</TableCell>
                    <TableCell sx={{ fontWeight: 600 }}>Type</TableCell>
                    <TableCell sx={{ fontWeight: 600 }}>Location</TableCell>
                    <TableCell sx={{ fontWeight: 600 }} align="right">
                      Units
                    </TableCell>
                    <TableCell sx={{ fontWeight: 600 }} align="right">
                      Purchase Price
                    </TableCell>
                    <TableCell sx={{ fontWeight: 600 }} align="right">
                      Current Value
                    </TableCell>
                    <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
                    <TableCell sx={{ fontWeight: 600 }} align="right">
                      Actions
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {properties.map((property) => (
                    <TableRow key={property.id} hover>
                      <TableCell>
                        <Box>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {property.property_name}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {property.property_id}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={property.property_type.replace('_', ' ')}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {property.city && property.state
                            ? `${property.city}, ${property.state}`
                            : property.city || property.state || '-'}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">{property.total_units}</Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {formatCurrency(property.purchase_price)}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {formatCurrency(property.current_value)}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={property.status}
                          size="small"
                          color={getStatusColor(property.status)}
                        />
                      </TableCell>
                      <TableCell align="right">
                        <IconButton
                          size="small"
                          onClick={(e) => handleMenuOpen(e, property)}
                        >
                          <MoreVertIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </CardContent>
      </Card>

      {/* Action Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem onClick={() => menuProperty && handleEditProperty(menuProperty)}>
          <EditIcon fontSize="small" sx={{ mr: 1 }} />
          Edit
        </MenuItem>
        <MenuItem onClick={() => menuProperty && handleDeleteClick(menuProperty)}>
          <DeleteIcon fontSize="small" sx={{ mr: 1 }} />
          Delete
        </MenuItem>
      </Menu>

      {/* Property Dialog */}
      <PropertyDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onSave={loadProperties}
        property={selectedProperty}
        mode={dialogMode}
      />

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)} maxWidth="xs">
        <DialogTitle>Delete Property?</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete <strong>{selectedProperty?.property_name}</strong>?
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
