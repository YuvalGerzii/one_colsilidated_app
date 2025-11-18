import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  IconButton,
  Chip,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Fab,
  Tooltip,
  Avatar,
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  AttachMoney as MoneyIcon,
  Business as PropertyIcon,
  Person as PersonIcon,
  CalendarToday as CalendarIcon,
  TrendingUp as TrendingUpIcon,
  Flag as FlagIcon,
  ViewKanban as KanbanIcon,
  ViewList as ListIcon,
} from '@mui/icons-material';
import { useSnackbar } from 'notistack';
import { apiClient } from '../../services/apiClient';

// Deal types - Supporting multiple transaction types
const DEAL_TYPES = [
  { value: 'real_estate', label: 'Real Estate' },
  { value: 'company_acquisition', label: 'Company Acquisition' },
  { value: 'shares', label: 'Shares/Equity' },
  { value: 'commodities', label: 'Commodities' },
  { value: 'debt', label: 'Debt Instruments' },
  { value: 'other', label: 'Other' },
];

// Deal Stages
const DEAL_STAGES = [
  { id: 'research', label: 'Research', color: '#94a3b8' },
  { id: 'loi', label: 'LOI', color: '#3b82f6' },
  { id: 'due_diligence', label: 'Due Diligence', color: '#f59e0b' },
  { id: 'closing', label: 'Closing', color: '#8b5cf6' },
  { id: 'closed', label: 'Closed', color: '#10b981' },
  { id: 'dead', label: 'Dead', color: '#ef4444' },
];

const PROPERTY_TYPES = [
  'Multifamily',
  'Office',
  'Retail',
  'Industrial',
  'Hotel',
  'Mixed Use',
  'Land',
  'Self Storage',
];

const PRIORITY_LEVELS = [
  { value: 1, label: 'High', color: '#ef4444' },
  { value: 2, label: 'Medium-High', color: '#f59e0b' },
  { value: 3, label: 'Medium', color: '#3b82f6' },
  { value: 4, label: 'Medium-Low', color: '#94a3b8' },
  { value: 5, label: 'Low', color: '#64748b' },
];

interface Deal {
  id: string;
  deal_type: string; // New field: real_estate, company_acquisition, shares, commodities, debt, other
  deal_name?: string; // General deal name for non-real-estate deals
  property_name?: string; // For real estate deals
  property_address?: string;
  property_type?: string;
  market?: string;
  stage: string;
  status: string;
  asking_price?: number;
  offer_price?: number;
  estimated_value?: number;
  purchase_price?: number;
  currency?: string;
  units?: number;
  square_feet?: number;
  cap_rate?: number;
  irr_target?: number;
  // Company acquisition fields
  target_company?: string;
  sector?: string;
  // Shares/equity fields
  ticker_symbol?: string;
  quantity?: number;
  asset_class?: string;
  // Commodities fields
  commodity_type?: string;
  // Team & Timeline
  lead_analyst?: string;
  date_identified?: string;
  loi_date?: string;
  due_diligence_start?: string;
  due_diligence_end?: string;
  expected_closing?: string;
  actual_closing?: string;
  notes?: string;
  pros?: string;
  cons?: string;
  documents_url?: string;
  priority?: number;
  confidence_level?: number;
  created_at?: string;
  updated_at?: string;
}

export const DealTracker: React.FC = () => {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'kanban' | 'list'>('kanban');
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null);
  const [formData, setFormData] = useState<Partial<Deal>>({
    deal_type: 'real_estate',
    property_name: '',
    property_type: '',
    market: '',
    stage: 'research',
    status: 'active',
    priority: 3,
  });
  const { enqueueSnackbar } = useSnackbar();

  // Fetch deals from API
  const fetchDeals = async () => {
    try {
      setLoading(true);
      const data = await apiClient.get<Deal[]>('/deals/');
      setDeals(data || []);
    } catch (error) {
      console.error('Error fetching deals:', error);
      enqueueSnackbar('Failed to load deals', { variant: 'error' });
      setDeals([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDeals();
  }, []);

  // Create deal
  const handleCreateDeal = async () => {
    try {
      await apiClient.post('/deals/', formData);
      enqueueSnackbar('Deal created successfully', { variant: 'success' });
      setAddDialogOpen(false);
      setFormData({
        deal_type: 'real_estate',
        property_name: '',
        property_type: '',
        market: '',
        stage: 'research',
        status: 'active',
        priority: 3,
      });
      fetchDeals();
    } catch (error: any) {
      console.error('Error creating deal:', error);
      const errorMessage = error?.response?.data?.detail || 'Failed to create deal';
      enqueueSnackbar(errorMessage, { variant: 'error' });
    }
  };

  // Update deal
  const handleUpdateDeal = async () => {
    if (!selectedDeal) return;
    try {
      await apiClient.put(`/deals/${selectedDeal.id}`, formData);
      enqueueSnackbar('Deal updated successfully', { variant: 'success' });
      setEditDialogOpen(false);
      setSelectedDeal(null);
      fetchDeals();
    } catch (error: any) {
      console.error('Error updating deal:', error);
      const errorMessage = error?.response?.data?.detail || 'Failed to update deal';
      enqueueSnackbar(errorMessage, { variant: 'error' });
    }
  };

  // Delete deal
  const handleDeleteDeal = async () => {
    if (!selectedDeal) return;
    try {
      await apiClient.delete(`/deals/${selectedDeal.id}`);
      enqueueSnackbar('Deal deleted successfully', { variant: 'success' });
      setDeleteDialogOpen(false);
      setSelectedDeal(null);
      fetchDeals();
    } catch (error: any) {
      console.error('Error deleting deal:', error);
      const errorMessage = error?.response?.data?.detail || 'Failed to delete deal';
      enqueueSnackbar(errorMessage, { variant: 'error' });
    }
  };

  // Move deal to different stage
  const handleMoveDeal = async (deal: Deal, newStage: string) => {
    try {
      await apiClient.patch(`/deals/${deal.id}/stage?stage=${encodeURIComponent(newStage)}`);
      enqueueSnackbar(`Deal moved to ${DEAL_STAGES.find(s => s.id === newStage)?.label}`, { variant: 'success' });
      fetchDeals();
    } catch (error: any) {
      console.error('Error moving deal:', error);
      enqueueSnackbar('Failed to move deal', { variant: 'error' });
    }
  };

  const handleEditClick = (deal: Deal) => {
    setSelectedDeal(deal);
    setFormData(deal);
    setEditDialogOpen(true);
  };

  const handleDeleteClick = (deal: Deal) => {
    setSelectedDeal(deal);
    setDeleteDialogOpen(true);
  };

  const formatCurrency = (value?: number) => {
    if (!value) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getPriorityColor = (priority?: number) => {
    const level = PRIORITY_LEVELS.find(p => p.value === priority);
    return level?.color || '#64748b';
  };

  // Render Deal Card
  const renderDealCard = (deal: Deal) => {
    const stageColor = DEAL_STAGES.find(s => s.id === deal.stage)?.color || '#94a3b8';

    return (
      <Card
        key={deal.id}
        sx={{
          mb: 2,
          borderLeft: 4,
          borderColor: stageColor,
          '&:hover': {
            boxShadow: 6,
            transform: 'translateY(-2px)',
            transition: 'all 0.2s',
          },
        }}
      >
        <CardContent sx={{ pb: 1 }}>
          <Stack spacing={1}>
            {/* Header */}
            <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
              <Box flex={1}>
                <Typography variant="subtitle1" fontWeight={600}>
                  {deal.property_name}
                </Typography>
                {deal.property_address && (
                  <Typography variant="caption" color="text.secondary" display="block">
                    {deal.property_address}
                  </Typography>
                )}
              </Box>
              <Chip
                size="small"
                label={PRIORITY_LEVELS.find(p => p.value === deal.priority)?.label || 'Medium'}
                sx={{
                  bgcolor: getPriorityColor(deal.priority),
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '0.7rem',
                }}
              />
            </Stack>

            {/* Property Details */}
            <Stack direction="row" spacing={1} flexWrap="wrap">
              {deal.property_type && (
                <Chip
                  icon={<PropertyIcon />}
                  label={deal.property_type}
                  size="small"
                  variant="outlined"
                />
              )}
              {deal.market && (
                <Chip
                  label={deal.market}
                  size="small"
                  variant="outlined"
                />
              )}
            </Stack>

            {/* Financial Info */}
            <Box>
              {deal.asking_price && (
                <Typography variant="body2" color="text.secondary">
                  <strong>Asking:</strong> {formatCurrency(deal.asking_price)}
                </Typography>
              )}
              {deal.offer_price && (
                <Typography variant="body2" color="text.secondary">
                  <strong>Offer:</strong> {formatCurrency(deal.offer_price)}
                </Typography>
              )}
              {deal.cap_rate && (
                <Typography variant="body2" color="text.secondary">
                  <strong>Cap Rate:</strong> {deal.cap_rate.toFixed(2)}%
                </Typography>
              )}
            </Box>

            {/* Progress & Dates */}
            {deal.confidence_level && (
              <Box>
                <Stack direction="row" justifyContent="space-between" alignItems="center" mb={0.5}>
                  <Typography variant="caption" color="text.secondary">
                    Confidence
                  </Typography>
                  <Typography variant="caption" fontWeight={600}>
                    {deal.confidence_level}%
                  </Typography>
                </Stack>
                <LinearProgress
                  variant="determinate"
                  value={deal.confidence_level}
                  sx={{
                    height: 6,
                    borderRadius: 3,
                    bgcolor: 'rgba(0,0,0,0.1)',
                    '& .MuiLinearProgress-bar': {
                      bgcolor: deal.confidence_level > 70 ? '#10b981' : deal.confidence_level > 40 ? '#f59e0b' : '#ef4444',
                    },
                  }}
                />
              </Box>
            )}

            {deal.expected_closing && (
              <Stack direction="row" spacing={0.5} alignItems="center">
                <CalendarIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
                <Typography variant="caption" color="text.secondary">
                  Expected: {formatDate(deal.expected_closing)}
                </Typography>
              </Stack>
            )}

            {deal.lead_analyst && (
              <Stack direction="row" spacing={0.5} alignItems="center">
                <PersonIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
                <Typography variant="caption" color="text.secondary">
                  {deal.lead_analyst}
                </Typography>
              </Stack>
            )}
          </Stack>
        </CardContent>

        <CardActions sx={{ pt: 0, px: 2, pb: 2 }}>
          <Button
            size="small"
            startIcon={<EditIcon />}
            onClick={() => handleEditClick(deal)}
          >
            Edit
          </Button>
          <Button
            size="small"
            color="error"
            startIcon={<DeleteIcon />}
            onClick={() => handleDeleteClick(deal)}
          >
            Delete
          </Button>
          {/* Quick Move Buttons */}
          {deal.stage !== 'closed' && deal.stage !== 'dead' && (
            <Select
              size="small"
              value={deal.stage}
              onChange={(e) => handleMoveDeal(deal, e.target.value)}
              sx={{ ml: 'auto', minWidth: 100 }}
            >
              {DEAL_STAGES.filter(s => s.id !== 'closed' && s.id !== 'dead').map(stage => (
                <MenuItem key={stage.id} value={stage.id}>
                  {stage.label}
                </MenuItem>
              ))}
            </Select>
          )}
        </CardActions>
      </Card>
    );
  };

  // Kanban View
  const renderKanbanView = () => {
    const activeDeals = deals.filter(d => d.status === 'active');

    return (
      <Grid container spacing={2}>
        {DEAL_STAGES.map(stage => {
          const stageDeals = activeDeals.filter(d => d.stage === stage.id);
          const totalValue = stageDeals.reduce((sum, d) => sum + (d.asking_price || d.offer_price || 0), 0);

          return (
            <Grid item xs={12} md={6} lg={4} xl={2} key={stage.id}>
              <Paper
                sx={{
                  p: 2,
                  bgcolor: 'background.default',
                  minHeight: 'calc(100vh - 250px)',
                  borderTop: 3,
                  borderColor: stage.color,
                }}
              >
                <Stack spacing={2}>
                  {/* Stage Header */}
                  <Box>
                    <Typography variant="subtitle1" fontWeight={700} gutterBottom>
                      {stage.label}
                    </Typography>
                    <Stack direction="row" spacing={2}>
                      <Chip
                        label={`${stageDeals.length} deals`}
                        size="small"
                        sx={{ bgcolor: stage.color, color: 'white', fontWeight: 600 }}
                      />
                      <Typography variant="caption" color="text.secondary">
                        {formatCurrency(totalValue)}
                      </Typography>
                    </Stack>
                  </Box>

                  {/* Deals */}
                  <Box>
                    {stageDeals.map(deal => renderDealCard(deal))}
                    {stageDeals.length === 0 && (
                      <Typography variant="body2" color="text.secondary" align="center" sx={{ py: 4 }}>
                        No deals in this stage
                      </Typography>
                    )}
                  </Box>
                </Stack>
              </Paper>
            </Grid>
          );
        })}
      </Grid>
    );
  };

  // Stats Summary
  const renderStats = () => {
    const activeDeals = deals.filter(d => d.status === 'active');
    const totalValue = activeDeals.reduce((sum, d) => sum + (d.asking_price || d.offer_price || 0), 0);
    const avgCapRate = activeDeals.length > 0
      ? activeDeals.reduce((sum, d) => sum + (d.cap_rate || 0), 0) / activeDeals.filter(d => d.cap_rate).length
      : 0;

    return (
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Active Deals
            </Typography>
            <Typography variant="h4" fontWeight={700}>
              {activeDeals.length}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Total Pipeline Value
            </Typography>
            <Typography variant="h4" fontWeight={700}>
              {formatCurrency(totalValue)}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Avg Cap Rate
            </Typography>
            <Typography variant="h4" fontWeight={700}>
              {avgCapRate.toFixed(2)}%
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Closing Soon
            </Typography>
            <Typography variant="h4" fontWeight={700}>
              {deals.filter(d => d.stage === 'closing').length}
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    );
  };

  // Form Dialog Content
  const renderFormDialog = (isEdit: boolean) => (
    <Dialog
      open={isEdit ? editDialogOpen : addDialogOpen}
      onClose={() => isEdit ? setEditDialogOpen(false) : setAddDialogOpen(false)}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>{isEdit ? 'Edit Deal' : 'Add New Deal'}</DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mt: 0.5 }}>
          {/* Deal Type Selector */}
          <Grid item xs={12}>
            <FormControl fullWidth>
              <InputLabel>Deal Type</InputLabel>
              <Select
                value={formData.deal_type || 'real_estate'}
                label="Deal Type"
                onChange={(e) => setFormData({ ...formData, deal_type: e.target.value })}
              >
                {DEAL_TYPES.map(type => (
                  <MenuItem key={type.value} value={type.value}>{type.label}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          {/* Real Estate Fields */}
          {formData.deal_type === 'real_estate' && (
            <>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Property Name"
                  value={formData.property_name || ''}
                  onChange={(e) => setFormData({ ...formData, property_name: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Property Address"
                  value={formData.property_address || ''}
                  onChange={(e) => setFormData({ ...formData, property_address: e.target.value })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Property Type</InputLabel>
                  <Select
                    value={formData.property_type || ''}
                    label="Property Type"
                    onChange={(e) => setFormData({ ...formData, property_type: e.target.value })}
                  >
                    {PROPERTY_TYPES.map(type => (
                      <MenuItem key={type} value={type}>{type}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Market"
                  value={formData.market || ''}
                  onChange={(e) => setFormData({ ...formData, market: e.target.value })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Units"
                  type="number"
                  value={formData.units || ''}
                  onChange={(e) => setFormData({ ...formData, units: Number(e.target.value) })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Square Feet"
                  type="number"
                  value={formData.square_feet || ''}
                  onChange={(e) => setFormData({ ...formData, square_feet: Number(e.target.value) })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Cap Rate (%)"
                  type="number"
                  value={formData.cap_rate || ''}
                  onChange={(e) => setFormData({ ...formData, cap_rate: Number(e.target.value) })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="IRR Target (%)"
                  type="number"
                  value={formData.irr_target || ''}
                  onChange={(e) => setFormData({ ...formData, irr_target: Number(e.target.value) })}
                />
              </Grid>
            </>
          )}

          {/* Company Acquisition Fields */}
          {formData.deal_type === 'company_acquisition' && (
            <>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Target Company Name"
                  value={formData.target_company || ''}
                  onChange={(e) => setFormData({ ...formData, target_company: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Sector/Industry"
                  value={formData.sector || ''}
                  onChange={(e) => setFormData({ ...formData, sector: e.target.value })}
                />
              </Grid>
            </>
          )}

          {/* Shares/Equity Fields */}
          {formData.deal_type === 'shares' && (
            <>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Ticker Symbol"
                  value={formData.ticker_symbol || ''}
                  onChange={(e) => setFormData({ ...formData, ticker_symbol: e.target.value.toUpperCase() })}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Quantity (Shares)"
                  type="number"
                  value={formData.quantity || ''}
                  onChange={(e) => setFormData({ ...formData, quantity: Number(e.target.value) })}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Asset Class"
                  value={formData.asset_class || ''}
                  onChange={(e) => setFormData({ ...formData, asset_class: e.target.value })}
                  placeholder="e.g., Common Stock, Preferred Stock, ETF"
                />
              </Grid>
            </>
          )}

          {/* Commodities Fields */}
          {formData.deal_type === 'commodities' && (
            <>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Commodity Type"
                  value={formData.commodity_type || ''}
                  onChange={(e) => setFormData({ ...formData, commodity_type: e.target.value })}
                  placeholder="e.g., Gold, Oil, Natural Gas"
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Quantity"
                  type="number"
                  value={formData.quantity || ''}
                  onChange={(e) => setFormData({ ...formData, quantity: Number(e.target.value) })}
                  required
                />
              </Grid>
            </>
          )}

          {/* Other/Debt Fields */}
          {(formData.deal_type === 'debt' || formData.deal_type === 'other') && (
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Deal Name"
                value={formData.deal_name || ''}
                onChange={(e) => setFormData({ ...formData, deal_name: e.target.value })}
                required
              />
            </Grid>
          )}

          {/* Common Financial Fields - All Deal Types */}
          <Grid item xs={12}>
            <Typography variant="subtitle2" color="text.secondary" sx={{ mt: 1, mb: 1 }}>
              Financial Information
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Asking Price"
              type="number"
              value={formData.asking_price || ''}
              onChange={(e) => setFormData({ ...formData, asking_price: Number(e.target.value) })}
              InputProps={{
                startAdornment: '$',
              }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Offer Price"
              type="number"
              value={formData.offer_price || ''}
              onChange={(e) => setFormData({ ...formData, offer_price: Number(e.target.value) })}
              InputProps={{
                startAdornment: '$',
              }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Purchase Price"
              type="number"
              value={formData.purchase_price || ''}
              onChange={(e) => setFormData({ ...formData, purchase_price: Number(e.target.value) })}
              InputProps={{
                startAdornment: '$',
              }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Estimated Value"
              type="number"
              value={formData.estimated_value || ''}
              onChange={(e) => setFormData({ ...formData, estimated_value: Number(e.target.value) })}
              InputProps={{
                startAdornment: '$',
              }}
            />
          </Grid>

          {/* Deal Management Fields */}
          <Grid item xs={12}>
            <Typography variant="subtitle2" color="text.secondary" sx={{ mt: 1, mb: 1 }}>
              Deal Management
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Stage</InputLabel>
              <Select
                value={formData.stage || 'research'}
                label="Stage"
                onChange={(e) => setFormData({ ...formData, stage: e.target.value })}
              >
                {DEAL_STAGES.map(stage => (
                  <MenuItem key={stage.id} value={stage.id}>{stage.label}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Priority</InputLabel>
              <Select
                value={formData.priority || 3}
                label="Priority"
                onChange={(e) => setFormData({ ...formData, priority: Number(e.target.value) })}
              >
                {PRIORITY_LEVELS.map(level => (
                  <MenuItem key={level.value} value={level.value}>{level.label}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Lead Analyst"
              value={formData.lead_analyst || ''}
              onChange={(e) => setFormData({ ...formData, lead_analyst: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Confidence Level (%)"
              type="number"
              inputProps={{ min: 0, max: 100 }}
              value={formData.confidence_level || ''}
              onChange={(e) => setFormData({ ...formData, confidence_level: Number(e.target.value) })}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Expected Closing"
              type="date"
              InputLabelProps={{ shrink: true }}
              value={formData.expected_closing || ''}
              onChange={(e) => setFormData({ ...formData, expected_closing: e.target.value })}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Notes"
              multiline
              rows={3}
              value={formData.notes || ''}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => isEdit ? setEditDialogOpen(false) : setAddDialogOpen(false)}>
          Cancel
        </Button>
        <Button
          variant="contained"
          onClick={isEdit ? handleUpdateDeal : handleCreateDeal}
          disabled={
            (formData.deal_type === 'real_estate' && !formData.property_name) ||
            (formData.deal_type === 'company_acquisition' && !formData.target_company) ||
            (formData.deal_type === 'shares' && (!formData.ticker_symbol || !formData.quantity)) ||
            (formData.deal_type === 'commodities' && (!formData.commodity_type || !formData.quantity)) ||
            ((formData.deal_type === 'debt' || formData.deal_type === 'other') && !formData.deal_name)
          }
        >
          {isEdit ? 'Update' : 'Create'}
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <Box>
      {/* Header */}
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Deal Pipeline
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Track and manage your real estate acquisition pipeline
          </Typography>
        </Box>
        <Stack direction="row" spacing={2}>
          <Button
            variant="outlined"
            startIcon={viewMode === 'kanban' ? <ListIcon /> : <KanbanIcon />}
            onClick={() => setViewMode(viewMode === 'kanban' ? 'list' : 'kanban')}
          >
            {viewMode === 'kanban' ? 'List View' : 'Kanban View'}
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {
              setFormData({
                property_name: '',
                property_type: '',
                market: '',
                stage: 'research',
                status: 'active',
                priority: 3,
              });
              setAddDialogOpen(true);
            }}
          >
            Add Deal
          </Button>
        </Stack>
      </Stack>

      {/* Stats */}
      {renderStats()}

      {/* Loading */}
      {loading && <LinearProgress sx={{ mb: 2 }} />}

      {/* Main Content */}
      {viewMode === 'kanban' ? renderKanbanView() : (
        <Paper sx={{ p: 2 }}>
          <Typography variant="body2" color="text.secondary" align="center">
            List view coming soon...
          </Typography>
        </Paper>
      )}

      {/* Dialogs */}
      {renderFormDialog(false)}
      {renderFormDialog(true)}

      {/* Delete Confirmation */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Deal</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete "{selectedDeal?.property_name}"? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button color="error" variant="contained" onClick={handleDeleteDeal}>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
