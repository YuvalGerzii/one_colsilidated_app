// src/pages/Companies/CompanyList.tsx
import React, { useMemo, useState } from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import {
  Button,
  Box,
  Chip,
  Typography,
  Stack,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Tooltip,
  Card,
  InputAdornment,
  Badge,
} from '@mui/material';
import {
  VisibilityOutlined as VisibilityIcon,
  EditOutlined as EditIcon,
  DeleteOutline as DeleteIcon,
  Add as AddIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
  Clear as ClearIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useCompanies } from '../../hooks/useCompanies';
import { formatCurrency } from '../../utils/formatters';
import { PageHeader } from '../../components/common/PageHeader';
import { EmptyState } from '../../components/common/EmptyState';
import { ErrorState } from '../../components/common/ErrorState';
import { PageSkeleton } from '../../components/common/LoadingSkeleton';

export const CompanyList: React.FC = () => {
  const navigate = useNavigate();
  const { companies, loading, error, refetch } = useCompanies();

  const [search, setSearch] = useState('');
  const [sectorFilter, setSectorFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [regionFilter, setRegionFilter] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  // Check if any filters are active
  const hasActiveFilters = search || sectorFilter || statusFilter || regionFilter;
  const activeFilterCount = [search, sectorFilter, statusFilter, regionFilter].filter(Boolean).length;

  const sectors = useMemo(
    () => Array.from(new Set(companies.map((company) => company.sector).filter(Boolean))).sort(),
    [companies]
  );

  const statuses = useMemo(
    () => Array.from(new Set(companies.map((company) => company.company_status))).sort(),
    [companies]
  );

  const regions = useMemo(
    () =>
      Array.from(
        new Set(
          companies
            .map((company) => company.headquarters_country)
            .filter((country): country is string => Boolean(country))
        )
      ).sort(),
    [companies]
  );

  const filteredCompanies = useMemo(() => {
    return companies.filter((company) => {
      const matchesSearch = search
        ? [company.company_name, company.sector, company.headquarters_country]
            .join(' ')
            .toLowerCase()
            .includes(search.toLowerCase())
        : true;

      const matchesSector = sectorFilter ? company.sector === sectorFilter : true;
      const matchesStatus = statusFilter ? company.company_status === statusFilter : true;
      const matchesRegion = regionFilter
        ? company.headquarters_country === regionFilter
        : true;

      return matchesSearch && matchesSector && matchesStatus && matchesRegion;
    });
  }, [companies, search, sectorFilter, statusFilter, regionFilter]);

  const handleClearFilters = () => {
    setSearch('');
    setSectorFilter('');
    setStatusFilter('');
    setRegionFilter('');
  };

  const handleExportData = () => {
    // TODO: Implement CSV export
    console.log('Exporting data...', filteredCompanies);
  };

  // Show loading skeleton
  if (loading && companies.length === 0) {
    return <PageSkeleton type="table" />;
  }

  // Show error state
  if (error && companies.length === 0) {
    return (
      <ErrorState
        title="Failed to load companies"
        message="We couldn't load your portfolio companies. Please try again."
        onRetry={refetch}
      />
    );
  }

  // Show empty state
  if (!loading && companies.length === 0) {
    return (
      <EmptyState
        icon={BusinessIcon}
        title="No portfolio companies yet"
        description="Get started by adding your first portfolio company to track performance and generate insights."
        actionLabel="Add Company"
        onAction={() => navigate('/companies/new')}
      />
    );
  }

  const columns: GridColDef[] = [
    {
      field: 'company_name',
      headerName: 'Company',
      flex: 1,
      minWidth: 200,
      renderCell: (params) => (
        <Button
          variant="text"
          color="primary"
          onClick={() => navigate(`/companies/${params.row.company_id}`)}
        >
          {params.value}
        </Button>
      ),
    },
    { field: 'sector', headerName: 'Sector', flex: 0.8, minWidth: 140 },
    {
      field: 'entry_revenue',
      headerName: 'Revenue',
      flex: 0.8,
      minWidth: 140,
      valueFormatter: (params) => formatCurrency(params.value as number),
    },
    {
      field: 'company_status',
      headerName: 'Status',
      flex: 0.6,
      minWidth: 130,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={params.value === 'Active' ? 'success' : params.value === 'Exited' ? 'primary' : 'default'}
          size="small"
          variant="outlined"
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
      filterable: false,
      width: 140,
      renderCell: (params) => (
        <Stack direction="row" spacing={0.5}>
          <Tooltip title="View details">
            <IconButton
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                navigate(`/companies/${params.row.company_id}`);
              }}
            >
              <VisibilityIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Edit company">
            <IconButton
              size="small"
              color="primary"
              onClick={(e) => {
                e.stopPropagation();
                // TODO: Open edit dialog
              }}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton
              size="small"
              color="error"
              onClick={(e) => {
                e.stopPropagation();
                // TODO: Open delete confirmation
              }}
            >
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Stack>
      ),
    },
  ];

  return (
    <Stack spacing={3}>
      <PageHeader
        title="Portfolio Companies"
        description="Search, filter, and manage the companies in your portfolio."
        icon={BusinessIcon}
        primaryAction={{
          label: 'Add Company',
          onClick: () => navigate('/companies/new'),
          icon: AddIcon,
        }}
        secondaryActions={[
          {
            label: 'Export',
            onClick: handleExportData,
            icon: DownloadIcon,
          },
          {
            label: 'Refresh',
            onClick: refetch,
            icon: RefreshIcon,
          },
        ]}
      />

      <Card sx={{ p: 3 }}>
        <Stack spacing={3}>
          {/* Search and Filter Bar */}
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} alignItems="center">
            <TextField
              placeholder="Search companies..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              fullWidth
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
                endAdornment: search && (
                  <InputAdornment position="end">
                    <IconButton size="small" onClick={() => setSearch('')}>
                      <ClearIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Stack direction="row" spacing={1}>
              <Tooltip title={showFilters ? 'Hide filters' : 'Show filters'}>
                <IconButton
                  onClick={() => setShowFilters(!showFilters)}
                  color={hasActiveFilters ? 'primary' : 'default'}
                >
                  <Badge badgeContent={activeFilterCount} color="primary">
                    <FilterIcon />
                  </Badge>
                </IconButton>
              </Tooltip>
              {hasActiveFilters && (
                <Tooltip title="Clear all filters">
                  <IconButton onClick={handleClearFilters} color="primary">
                    <ClearIcon />
                  </IconButton>
                </Tooltip>
              )}
            </Stack>
          </Stack>

          {/* Advanced Filters */}
          {showFilters && (
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              spacing={2}
              sx={{
                p: 2,
                bgcolor: 'action.hover',
                borderRadius: 1,
              }}
            >
              <FormControl fullWidth size="small">
                <InputLabel>Sector</InputLabel>
                <Select
                  label="Sector"
                  value={sectorFilter}
                  onChange={(event) => setSectorFilter(event.target.value)}
                >
                  <MenuItem value="">
                    <em>All Sectors</em>
                  </MenuItem>
                  {sectors.map((sector) => (
                    <MenuItem key={sector} value={sector}>
                      {sector}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl fullWidth size="small">
                <InputLabel>Status</InputLabel>
                <Select
                  label="Status"
                  value={statusFilter}
                  onChange={(event) => setStatusFilter(event.target.value)}
                >
                  <MenuItem value="">
                    <em>All Statuses</em>
                  </MenuItem>
                  {statuses.map((status) => (
                    <MenuItem key={status} value={status}>
                      {status}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl fullWidth size="small">
                <InputLabel>Region</InputLabel>
                <Select
                  label="Region"
                  value={regionFilter}
                  onChange={(event) => setRegionFilter(event.target.value)}
                >
                  <MenuItem value="">
                    <em>All Regions</em>
                  </MenuItem>
                  {regions.map((region) => (
                    <MenuItem key={region} value={region}>
                      {region}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Stack>
          )}

          {/* Results Summary */}
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Typography variant="body2" color="text.secondary">
              Showing {filteredCompanies.length} of {companies.length} companies
              {hasActiveFilters && ' (filtered)'}
            </Typography>
          </Stack>

          {/* DataGrid */}
          <Box sx={{ height: 600, width: '100%' }}>
            <DataGrid
              rows={filteredCompanies}
              columns={columns}
              loading={loading}
              getRowId={(row) => row.company_id}
              pageSizeOptions={[10, 25, 50, 100]}
              initialState={{
                pagination: { paginationModel: { pageSize: 25 } },
                sorting: {
                  sortModel: [{ field: 'company_name', sort: 'asc' }],
                },
              }}
              onRowClick={(params) => navigate(`/companies/${params.id}`)}
              checkboxSelection
              disableRowSelectionOnClick
              sx={{
                '& .MuiDataGrid-row': {
                  cursor: 'pointer',
                  '&:hover': {
                    bgcolor: 'action.hover',
                  },
                },
              }}
            />
          </Box>

          {/* Empty Filtered State */}
          {filteredCompanies.length === 0 && hasActiveFilters && (
            <Box sx={{ py: 8, textAlign: 'center' }}>
              <EmptyState
                title="No companies match your filters"
                description="Try adjusting your search criteria or clearing filters."
                actionLabel="Clear Filters"
                onAction={handleClearFilters}
              />
            </Box>
          )}
        </Stack>
      </Card>
    </Stack>
  );
};
