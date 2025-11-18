import React, { useState } from 'react';
import {
  Box,
  Button,
  Menu,
  MenuItem,
  Typography,
  Divider,
  CircularProgress,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  Business as BusinessIcon,
  Add as AddIcon,
  Check as CheckIcon,
  ExpandMore as ExpandMoreIcon,
} from '@mui/icons-material';
import { useCompany } from '../../context/CompanyContext';
import { AddCompanyModal } from './AddCompanyModal';

export const CompanySelector: React.FC = () => {
  const { selectedCompany, companies, loading, selectCompany } = useCompany();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleSelectCompany = (companyId: string) => {
    const company = companies.find((c) => c.id === companyId);
    if (company) {
      // Fetch full company details (for property_count, etc.)
      selectCompany({
        ...company,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        property_count: 0,
        details: undefined,
        contact_info: undefined,
        logo_url: undefined,
      });
    }
    handleClose();
  };

  const handleAddCompany = () => {
    handleClose();
    setModalOpen(true);
  };

  return (
    <>
      <Button
        onClick={handleClick}
        startIcon={<BusinessIcon />}
        endIcon={<ExpandMoreIcon />}
        sx={{
          textTransform: 'none',
          color: 'white',
          borderColor: 'rgba(255, 255, 255, 0.3)',
          '&:hover': {
            borderColor: 'rgba(255, 255, 255, 0.5)',
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
          },
        }}
        variant="outlined"
      >
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', ml: 1 }}>
          <Typography variant="caption" sx={{ fontSize: '0.65rem', opacity: 0.8 }}>
            Company
          </Typography>
          <Typography variant="body2" sx={{ fontWeight: 500 }}>
            {loading ? (
              <CircularProgress size={12} sx={{ color: 'white' }} />
            ) : selectedCompany ? (
              selectedCompany.name
            ) : (
              'Select Company'
            )}
          </Typography>
        </Box>
      </Button>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        PaperProps={{
          sx: {
            mt: 1,
            minWidth: 250,
            maxHeight: 400,
          },
        }}
      >
        <MenuItem disabled>
          <Typography variant="caption" color="text.secondary">
            SELECT COMPANY
          </Typography>
        </MenuItem>
        <Divider />

        {companies.length === 0 && !loading ? (
          <MenuItem disabled>
            <Typography variant="body2" color="text.secondary">
              No companies available
            </Typography>
          </MenuItem>
        ) : (
          companies.map((company) => (
            <MenuItem
              key={company.id}
              onClick={() => handleSelectCompany(company.id)}
              selected={selectedCompany?.id === company.id}
            >
              {selectedCompany?.id === company.id && (
                <ListItemIcon>
                  <CheckIcon fontSize="small" color="primary" />
                </ListItemIcon>
              )}
              <ListItemText
                primary={company.name}
                secondary={company.region}
                sx={{
                  ml: selectedCompany?.id === company.id ? 0 : 5,
                }}
              />
            </MenuItem>
          ))
        )}

        <Divider />
        <MenuItem onClick={handleAddCompany}>
          <ListItemIcon>
            <AddIcon fontSize="small" color="primary" />
          </ListItemIcon>
          <ListItemText primary="Add New Company" primaryTypographyProps={{ color: 'primary' }} />
        </MenuItem>
      </Menu>

      <AddCompanyModal open={modalOpen} onClose={() => setModalOpen(false)} />
    </>
  );
};
