/**
 * Companies Component - Company management
 *
 * @version 1.2.0
 * @created 2025-11-15
 * @updated 2025-11-15
 * @description Manage company accounts and settings with backend API integration
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  Typography,
  Stack,
  Grid,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Switch,
  FormControlLabel,
  Avatar,
  Tooltip,
  CircularProgress,
} from '@mui/material';
import {
  Business as CompanyIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { designTokens, alphaColor } from '../../theme/designTokens';
import { MetricCard } from '../../components/ui/MetricCard';
import { apiClient } from '../../services/apiClient';
import { useSnackbar } from 'notistack';

interface Company {
  id: string;
  name: string;
  details?: string;
  region?: string;
  contact_info?: string;
  logo_url?: string;
  created_at: string;
  updated_at: string;
  property_count: number;
  // Frontend-only fields for display
  industry?: string;
  users?: number;
  status?: 'active' | 'inactive';
  subscription?: string;
}

interface CompanyFormData {
  name: string;
  details?: string;
  region?: string;
  contact_info?: string;
  logo_url?: string;
}

export const Companies: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState<CompanyFormData>({
    name: '',
    details: '',
    region: '',
    contact_info: '',
    logo_url: '',
  });

  // Fetch companies from API
  const fetchCompanies = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/companies/');
      setCompanies(response || []);
    } catch (error) {
      console.error('Error fetching companies:', error);
      enqueueSnackbar('Failed to load companies', { variant: 'error' });
      setCompanies([]);
    } finally {
      setLoading(false);
    }
  };

  // Load companies on mount
  useEffect(() => {
    fetchCompanies();
  }, []);

  // Create or update company
  const handleSave = async () => {
    try {
      if (selectedCompany) {
        // Update existing company
        await apiClient.put(`/companies/${selectedCompany.id}`, formData);
        enqueueSnackbar('Company updated successfully', { variant: 'success' });
      } else {
        // Create new company
        await apiClient.post('/companies/', formData);
        enqueueSnackbar('Company created successfully', { variant: 'success' });
      }

      setDialogOpen(false);
      setSelectedCompany(null);
      setFormData({ name: '', details: '', region: '', contact_info: '', logo_url: '' });
      fetchCompanies();
    } catch (error: any) {
      console.error('Error saving company:', error);
      const errorMessage = error?.response?.data?.detail || 'Failed to save company';
      enqueueSnackbar(errorMessage, { variant: 'error' });
    }
  };

  // Delete company
  const handleDelete = async (companyId: string) => {
    if (!window.confirm('Are you sure you want to delete this company?')) {
      return;
    }

    try {
      await apiClient.delete(`/companies/${companyId}`);
      enqueueSnackbar('Company deleted successfully', { variant: 'success' });
      fetchCompanies();
    } catch (error: any) {
      console.error('Error deleting company:', error);
      const errorMessage = error?.response?.data?.detail || 'Failed to delete company';
      enqueueSnackbar(errorMessage, { variant: 'error' });
    }
  };

  // Open dialog for create/edit
  const openDialog = (company?: Company) => {
    if (company) {
      setSelectedCompany(company);
      setFormData({
        name: company.name,
        details: company.details || '',
        region: company.region || '',
        contact_info: company.contact_info || '',
        logo_url: company.logo_url || '',
      });
    } else {
      setSelectedCompany(null);
      setFormData({ name: '', details: '', region: '', contact_info: '', logo_url: '' });
    }
    setDialogOpen(true);
  };

  return (
    <Box sx={{ p: { xs: 3, md: 4 } }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
          <Box
            sx={{
              width: 56,
              height: 56,
              borderRadius: designTokens.radius.lg,
              background: designTokens.colors.workspace.admin,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <CompanyIcon sx={{ fontSize: 28, color: 'white' }} />
          </Box>
          <Box flex={1}>
            <Typography variant="h4" sx={{ fontWeight: designTokens.typography.fontWeight.bold }}>
              Companies
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage company accounts and settings
            </Typography>
          </Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{ background: designTokens.colors.workspace.admin }}
            onClick={() => openDialog()}
          >
            Add Company
          </Button>
        </Stack>
      </Box>

      {/* Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Total Companies"
            value={companies.length}
            change="+1"
            trend="up"
            icon={CompanyIcon}
            color={designTokens.colors.chart.blue}
            subtext="this month"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Active Companies"
            value={companies.filter(c => c.status === 'active').length}
            change="+2"
            trend="up"
            icon={ActiveIcon}
            color={designTokens.colors.semantic.success}
            subtext="currently active"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Total Users"
            value={companies.reduce((sum, c) => sum + (c.users || 0), 0)}
            change="+12"
            trend="up"
            icon={AddIcon}
            color={designTokens.colors.chart.purple}
            subtext="across all companies"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Total Properties"
            value={companies.reduce((sum, c) => sum + c.property_count, 0)}
            change="+45"
            trend="up"
            icon={CompanyIcon}
            color={designTokens.colors.chart.emerald}
            subtext="managed properties"
          />
        </Grid>
      </Grid>

      {/* Table */}
      <Card>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Company</TableCell>
                <TableCell>Region</TableCell>
                <TableCell>Properties</TableCell>
                <TableCell>Contact Info</TableCell>
                <TableCell>Created</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} align="center" sx={{ py: 8 }}>
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : companies.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center" sx={{ py: 8 }}>
                    <Typography variant="body2" color="text.secondary">
                      No companies found. Click "Add Company" to create one.
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                companies.map((company) => (
                  <TableRow key={company.id} hover>
                    <TableCell>
                      <Stack direction="row" spacing={2} alignItems="center">
                        <Avatar sx={{ bgcolor: designTokens.colors.chart.blue }}>
                          {company.name.charAt(0)}
                        </Avatar>
                        <Box>
                          <Typography variant="body2" fontWeight={600}>
                            {company.name}
                          </Typography>
                          {company.details && (
                            <Typography variant="caption" color="text.secondary">
                              {company.details}
                            </Typography>
                          )}
                        </Box>
                      </Stack>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{company.region || '-'}</Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{company.property_count}</Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {company.contact_info || '-'}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {new Date(company.created_at).toLocaleDateString()}
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Tooltip title="Edit">
                        <IconButton size="small" onClick={() => openDialog(company)}>
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Delete">
                        <IconButton size="small" color="error" onClick={() => handleDelete(company.id)}>
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Card>

      {/* Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedCompany ? 'Edit Company' : 'Add Company'}
        </DialogTitle>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 1 }}>
            <TextField
              label="Company Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              fullWidth
              required
            />
            <TextField
              label="Details"
              value={formData.details}
              onChange={(e) => setFormData({ ...formData, details: e.target.value })}
              fullWidth
              multiline
              rows={2}
            />
            <TextField
              label="Region"
              value={formData.region}
              onChange={(e) => setFormData({ ...formData, region: e.target.value })}
              fullWidth
            />
            <TextField
              label="Contact Info"
              value={formData.contact_info}
              onChange={(e) => setFormData({ ...formData, contact_info: e.target.value })}
              fullWidth
              multiline
              rows={2}
              placeholder="Email, phone, address, etc."
            />
            <TextField
              label="Logo URL"
              value={formData.logo_url}
              onChange={(e) => setFormData({ ...formData, logo_url: e.target.value })}
              fullWidth
              placeholder="https://example.com/logo.png"
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleSave} disabled={!formData.name.trim()}>
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Companies;
