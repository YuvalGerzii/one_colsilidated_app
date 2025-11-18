import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Grid,
  MenuItem,
  Box,
  Typography,
  Alert,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { apiClient } from '@/services/apiClient';

interface AddPropertyModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

interface PropertyFormData {
  property_id: string;
  property_name: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  property_type: string;
  ownership_model: string;
  status: string;
  total_units: number;
  total_square_footage: number | null;
  year_built: number | null;
  purchase_price: number | null;
  purchase_date: Date | null;
  current_value: number | null;
  notes: string;
}

const propertyTypes = [
  { value: 'Multifamily', label: 'Multifamily' },
  { value: 'Single Family', label: 'Single Family' },
  { value: 'Commercial Office', label: 'Commercial Office' },
  { value: 'Retail', label: 'Retail' },
  { value: 'Industrial', label: 'Industrial' },
  { value: 'Mixed-Use', label: 'Mixed-Use' },
  { value: 'Hotel/Hospitality', label: 'Hotel/Hospitality' },
];

const ownershipModels = [
  { value: 'Full Ownership', label: 'Full Ownership' },
  { value: 'Master Lease', label: 'Master Lease' },
  { value: 'Sublease', label: 'Sublease' },
  { value: 'Rental Arbitrage (Airbnb/VRBO)', label: 'Rental Arbitrage (Airbnb/VRBO)' },
  { value: 'Joint Venture', label: 'Joint Venture' },
  { value: 'Management Contract Only', label: 'Management Contract Only' },
  { value: 'Ground Lease', label: 'Ground Lease' },
];

const propertyStatuses = [
  { value: 'Active', label: 'Active' },
  { value: 'Under Contract', label: 'Under Contract' },
  { value: 'Sold', label: 'Sold' },
  { value: 'Inactive', label: 'Inactive' },
];

const AddPropertyModal: React.FC<AddPropertyModalProps> = ({ open, onClose, onSuccess }) => {
  const [formData, setFormData] = useState<PropertyFormData>({
    property_id: '',
    property_name: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    property_type: '',
    ownership_model: '',
    status: 'Active',
    total_units: 0,
    total_square_footage: null,
    year_built: null,
    purchase_price: null,
    purchase_date: null,
    current_value: null,
    notes: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: keyof PropertyFormData) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const value = event.target.value;
    setFormData((prev) => ({
      ...prev,
      [field]: value === '' ? null : value,
    }));
  };

  const handleNumberChange = (field: keyof PropertyFormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;
    setFormData((prev) => ({
      ...prev,
      [field]: value === '' ? null : Number(value),
    }));
  };

  const handleDateChange = (date: Date | null) => {
    setFormData((prev) => ({
      ...prev,
      purchase_date: date,
    }));
  };

  const handleSubmit = async () => {
    // Validation
    if (!formData.property_id || !formData.property_name || !formData.property_type || !formData.ownership_model) {
      setError('Please fill in all required fields (Property ID, Name, Type, and Ownership Model)');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Format the data for the API
      const apiData = {
        property_id: formData.property_id,
        property_name: formData.property_name,
        address: formData.address || null,
        city: formData.city || null,
        state: formData.state || null,
        zip_code: formData.zip_code || null,
        property_type: formData.property_type,
        ownership_model: formData.ownership_model,
        status: formData.status,
        total_units: formData.total_units || 0,
        purchase_price: formData.purchase_price,
        purchase_date: formData.purchase_date ? formData.purchase_date.toISOString().split('T')[0] : null,
        current_value: formData.current_value,
        notes: formData.notes || null,
      };

      await apiClient.post('/property-management/properties', apiData);

      // Reset form on success
      setFormData({
        property_id: '',
        property_name: '',
        address: '',
        city: '',
        state: '',
        zip_code: '',
        property_type: '',
        ownership_model: '',
        status: 'Active',
        total_units: 0,
        total_square_footage: null,
        year_built: null,
        purchase_price: null,
        purchase_date: null,
        current_value: null,
        notes: '',
      });
      onSuccess();
      onClose();
    } catch (err: any) {
      console.error('Error creating property:', err);
      setError(err.response?.data?.detail || 'Failed to create property. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      property_id: '',
      property_name: '',
      address: '',
      city: '',
      state: '',
      zip_code: '',
      property_type: '',
      ownership_model: '',
      status: 'Active',
      total_units: 0,
      total_square_footage: null,
      year_built: null,
      purchase_price: null,
      purchase_date: null,
      current_value: null,
      notes: '',
    });
    setError(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleCancel} maxWidth="md" fullWidth>
      <DialogTitle>Add New Property</DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Grid container spacing={2}>
            {/* Required Fields */}
            <Grid item xs={12}>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                Required Information
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                label="Property ID"
                value={formData.property_id}
                onChange={handleChange('property_id')}
                placeholder="e.g., PROP-001"
                helperText="Unique identifier for the property"
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                label="Property Name"
                value={formData.property_name}
                onChange={handleChange('property_name')}
                placeholder="e.g., Maple Apartments"
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                select
                label="Property Type"
                value={formData.property_type}
                onChange={handleChange('property_type')}
              >
                {propertyTypes.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                select
                label="Ownership Model"
                value={formData.ownership_model}
                onChange={handleChange('ownership_model')}
              >
                {ownershipModels.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {/* Location Information */}
            <Grid item xs={12} sx={{ mt: 2 }}>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                Location Information
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Address"
                value={formData.address}
                onChange={handleChange('address')}
                placeholder="e.g., 123 Main Street"
              />
            </Grid>

            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="City"
                value={formData.city}
                onChange={handleChange('city')}
              />
            </Grid>

            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="State"
                value={formData.state}
                onChange={handleChange('state')}
              />
            </Grid>

            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="ZIP Code"
                value={formData.zip_code}
                onChange={handleChange('zip_code')}
              />
            </Grid>

            {/* Property Details */}
            <Grid item xs={12} sx={{ mt: 2 }}>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                Property Details
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="Status"
                value={formData.status}
                onChange={handleChange('status')}
              >
                {propertyStatuses.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Total Units"
                value={formData.total_units || ''}
                onChange={handleNumberChange('total_units')}
                inputProps={{ min: 0 }}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Total Square Footage"
                value={formData.total_square_footage || ''}
                onChange={handleNumberChange('total_square_footage')}
                inputProps={{ min: 0 }}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Year Built"
                value={formData.year_built || ''}
                onChange={handleNumberChange('year_built')}
                inputProps={{ min: 1800, max: new Date().getFullYear() }}
              />
            </Grid>

            {/* Financial Information */}
            <Grid item xs={12} sx={{ mt: 2 }}>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                Financial Information
              </Typography>
            </Grid>

            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                type="number"
                label="Purchase Price"
                value={formData.purchase_price || ''}
                onChange={handleNumberChange('purchase_price')}
                inputProps={{ min: 0, step: 0.01 }}
                helperText="Leave empty if leased"
              />
            </Grid>

            <Grid item xs={12} sm={4}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DatePicker
                  label="Purchase Date"
                  value={formData.purchase_date}
                  onChange={handleDateChange}
                  slotProps={{
                    textField: {
                      fullWidth: true,
                    },
                  }}
                />
              </LocalizationProvider>
            </Grid>

            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                type="number"
                label="Current Value"
                value={formData.current_value || ''}
                onChange={handleNumberChange('current_value')}
                inputProps={{ min: 0, step: 0.01 }}
              />
            </Grid>

            {/* Additional Notes */}
            <Grid item xs={12} sx={{ mt: 2 }}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Notes"
                value={formData.notes}
                onChange={handleChange('notes')}
                placeholder="Any additional information about the property"
              />
            </Grid>
          </Grid>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel} disabled={loading}>
          Cancel
        </Button>
        <Button onClick={handleSubmit} variant="contained" disabled={loading}>
          {loading ? 'Creating...' : 'Create Property'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AddPropertyModal;
