import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Grid,
  MenuItem,
  Alert,
  CircularProgress,
  Box,
  Typography,
  IconButton,
} from '@mui/material';
import {
  Close as CloseIcon,
  Save as SaveIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { api } from '../../services/apiClient';
import { useCompany } from '../../context/CompanyContext';

export interface Property {
  id?: string;
  property_id: string;
  property_name: string;
  address?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  property_type: string;
  ownership_model: string;
  status: string;
  total_units: number;
  purchase_price?: number;
  purchase_date?: string;
  current_value?: number;
  notes?: string;
  company_id?: string;
}

interface PropertyDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: () => void;
  property?: Property | null;
  mode: 'create' | 'edit';
}

const PROPERTY_TYPES = [
  { value: 'single_family', label: 'Single Family' },
  { value: 'multifamily', label: 'Multifamily' },
  { value: 'commercial', label: 'Commercial' },
  { value: 'mixed_use', label: 'Mixed Use' },
  { value: 'land', label: 'Land' },
  { value: 'industrial', label: 'Industrial' },
];

const OWNERSHIP_MODELS = [
  { value: 'direct', label: 'Direct Ownership' },
  { value: 'jv', label: 'Joint Venture' },
  { value: 'fund', label: 'Fund' },
  { value: 'syndication', label: 'Syndication' },
];

const PROPERTY_STATUSES = [
  { value: 'ACTIVE', label: 'Active' },
  { value: 'UNDER_CONTRACT', label: 'Under Contract' },
  { value: 'SOLD', label: 'Sold' },
  { value: 'INACTIVE', label: 'Inactive' },
];

const US_STATES = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
];

export const PropertyDialog: React.FC<PropertyDialogProps> = ({
  open,
  onClose,
  onSave,
  property,
  mode,
}) => {
  const { selectedCompany } = useCompany();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<Property>({
    property_id: '',
    property_name: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    property_type: 'single_family',
    ownership_model: 'direct',
    status: 'ACTIVE',
    total_units: 1,
    purchase_price: 0,
    purchase_date: '',
    current_value: 0,
    notes: '',
  });

  useEffect(() => {
    if (property && mode === 'edit') {
      setFormData(property);
    } else if (mode === 'create') {
      // Reset form for new property
      setFormData({
        property_id: `PROP-${Date.now()}`,
        property_name: '',
        address: '',
        city: '',
        state: '',
        zip_code: '',
        property_type: 'single_family',
        ownership_model: 'direct',
        status: 'ACTIVE',
        total_units: 1,
        purchase_price: 0,
        purchase_date: new Date().toISOString().split('T')[0],
        current_value: 0,
        notes: '',
      });
    }
  }, [property, mode, open]);

  const handleChange = (field: keyof Property) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;
    setFormData((prev) => ({
      ...prev,
      [field]: ['total_units', 'purchase_price', 'current_value'].includes(field)
        ? Number(value)
        : value,
    }));
  };

  const validateForm = (): string | null => {
    if (!formData.property_name.trim()) {
      return 'Property name is required';
    }
    if (!formData.property_id.trim()) {
      return 'Property ID is required';
    }
    if (formData.total_units < 1) {
      return 'Total units must be at least 1';
    }
    if (formData.purchase_price && formData.purchase_price < 0) {
      return 'Purchase price cannot be negative';
    }
    return null;
  };

  const handleSubmit = async () => {
    setError(null);
    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    if (!selectedCompany) {
      setError('Please select a company first');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        ...formData,
        company_id: selectedCompany.id,
      };

      if (mode === 'create') {
        await api.post('/property-management/properties', payload);
      } else if (mode === 'edit' && property?.id) {
        await api.patch(`/property-management/properties/${property.id}`, payload);
      }

      onSave();
      onClose();
    } catch (err: any) {
      console.error('Error saving property:', err);
      setError(
        err.response?.data?.detail ||
        `Failed to ${mode} property. Please try again.`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 2,
          maxHeight: '90vh',
        },
      }}
    >
      <DialogTitle sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', pb: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {mode === 'create' ? <AddIcon /> : <SaveIcon />}
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            {mode === 'create' ? 'Add New Property' : 'Edit Property'}
          </Typography>
        </Box>
        <IconButton onClick={onClose} size="small">
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers>
        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          {/* Property Information */}
          <Grid item xs={12}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 2, color: 'text.secondary' }}>
              Property Information
            </Typography>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Property Name"
              value={formData.property_name}
              onChange={handleChange('property_name')}
              required
              helperText="e.g., Sunset Apartments"
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Property ID"
              value={formData.property_id}
              onChange={handleChange('property_id')}
              required
              disabled={mode === 'edit'}
              helperText="Unique identifier"
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Property Type"
              value={formData.property_type}
              onChange={handleChange('property_type')}
              required
            >
              {PROPERTY_TYPES.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Ownership Model"
              value={formData.ownership_model}
              onChange={handleChange('ownership_model')}
              required
            >
              {OWNERSHIP_MODELS.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          {/* Location */}
          <Grid item xs={12}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 2, color: 'text.secondary', mt: 2 }}>
              Location
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Address"
              value={formData.address}
              onChange={handleChange('address')}
              helperText="Street address"
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
              select
              label="State"
              value={formData.state}
              onChange={handleChange('state')}
            >
              <MenuItem value="">Select State</MenuItem>
              {US_STATES.map((state) => (
                <MenuItem key={state} value={state}>
                  {state}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              label="ZIP Code"
              value={formData.zip_code}
              onChange={handleChange('zip_code')}
              inputProps={{ maxLength: 10 }}
            />
          </Grid>

          {/* Financial Details */}
          <Grid item xs={12}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 2, color: 'text.secondary', mt: 2 }}>
              Financial Details
            </Typography>
          </Grid>

          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              type="number"
              label="Total Units"
              value={formData.total_units}
              onChange={handleChange('total_units')}
              required
              inputProps={{ min: 1 }}
            />
          </Grid>

          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              type="number"
              label="Purchase Price"
              value={formData.purchase_price}
              onChange={handleChange('purchase_price')}
              InputProps={{
                startAdornment: <Typography sx={{ mr: 1, color: 'text.secondary' }}>$</Typography>,
              }}
              helperText="Total acquisition cost"
            />
          </Grid>

          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              type="date"
              label="Purchase Date"
              value={formData.purchase_date}
              onChange={handleChange('purchase_date')}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="number"
              label="Current Value"
              value={formData.current_value}
              onChange={handleChange('current_value')}
              InputProps={{
                startAdornment: <Typography sx={{ mr: 1, color: 'text.secondary' }}>$</Typography>,
              }}
              helperText="Current market value"
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Status"
              value={formData.status}
              onChange={handleChange('status')}
              required
            >
              {PROPERTY_STATUSES.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          {/* Notes */}
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={3}
              label="Notes"
              value={formData.notes}
              onChange={handleChange('notes')}
              placeholder="Additional property details..."
            />
          </Grid>
        </Grid>
      </DialogContent>

      <DialogActions sx={{ px: 3, py: 2 }}>
        <Button onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading}
          startIcon={loading ? <CircularProgress size={16} /> : <SaveIcon />}
        >
          {loading ? 'Saving...' : mode === 'create' ? 'Add Property' : 'Save Changes'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
