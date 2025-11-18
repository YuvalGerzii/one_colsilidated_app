import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Stack,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useCompany, CreateCompanyData } from '../../context/CompanyContext';

interface AddCompanyModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export const AddCompanyModal: React.FC<AddCompanyModalProps> = ({ open, onClose, onSuccess }) => {
  const { createCompany, selectCompany } = useCompany();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<CreateCompanyData>({
    name: '',
    details: '',
    region: '',
    contact_info: '',
  });

  const handleChange = (field: keyof CreateCompanyData) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: event.target.value,
    }));
    setError(null);
  };

  const handleSubmit = async () => {
    if (!formData.name.trim()) {
      setError('Company name is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const newCompany = await createCompany(formData);

      // Auto-select the newly created company
      selectCompany(newCompany);

      // Reset form
      setFormData({
        name: '',
        details: '',
        region: '',
        contact_info: '',
      });

      onSuccess?.();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to create company');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (!loading) {
      setFormData({
        name: '',
        details: '',
        region: '',
        contact_info: '',
      });
      setError(null);
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Add New Company</DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 2 }}>
          {error && <Alert severity="error">{error}</Alert>}

          <TextField
            label="Company Name"
            value={formData.name}
            onChange={handleChange('name')}
            required
            fullWidth
            autoFocus
            disabled={loading}
            placeholder="Enter company name"
          />

          <TextField
            label="Details"
            value={formData.details}
            onChange={handleChange('details')}
            multiline
            rows={3}
            fullWidth
            disabled={loading}
            placeholder="Company description and additional details"
          />

          <TextField
            label="Region"
            value={formData.region}
            onChange={handleChange('region')}
            fullWidth
            disabled={loading}
            placeholder="Primary region/location (e.g., North America, Europe)"
          />

          <TextField
            label="Contact Information"
            value={formData.contact_info}
            onChange={handleChange('contact_info')}
            multiline
            rows={2}
            fullWidth
            disabled={loading}
            placeholder="Email, phone, address, etc."
          />
        </Stack>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading || !formData.name.trim()}
          startIcon={loading && <CircularProgress size={20} />}
        >
          {loading ? 'Creating...' : 'Create Company'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
