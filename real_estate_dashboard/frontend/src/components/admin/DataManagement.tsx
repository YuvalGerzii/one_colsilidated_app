import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  Stack,
  Divider,
  Box,
  Chip,
} from '@mui/material';
import {
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { useCompany } from '../../context/CompanyContext';
import { clearLegacyLocalStorage, clearCompanyData, debugLocalStorage } from '../../utils/clearOldData';

export const DataManagement: React.FC = () => {
  const { selectedCompany } = useCompany();
  const [message, setMessage] = useState<{ type: 'success' | 'info' | 'warning'; text: string } | null>(null);

  const handleClearLegacyData = () => {
    const cleared = clearLegacyLocalStorage();
    setMessage({
      type: 'success',
      text: `Cleared ${cleared} legacy localStorage keys. Page will reload.`
    });
    setTimeout(() => window.location.reload(), 1500);
  };

  const handleClearCompanyData = () => {
    if (!selectedCompany) {
      setMessage({
        type: 'warning',
        text: 'No company selected. Please select a company first.'
      });
      return;
    }

    if (window.confirm(`Are you sure you want to clear all localStorage data for "${selectedCompany.name}"? This cannot be undone.`)) {
      clearCompanyData(selectedCompany.id);
      setMessage({
        type: 'success',
        text: `Cleared all data for ${selectedCompany.name}. Page will reload.`
      });
      setTimeout(() => window.location.reload(), 1500);
    }
  };

  const handleClearAllLocalStorage = () => {
    if (window.confirm('Are you sure you want to clear ALL localStorage data? This will remove data for all companies and settings. This cannot be undone.')) {
      localStorage.clear();
      setMessage({
        type: 'success',
        text: 'All localStorage cleared. Page will reload.'
      });
      setTimeout(() => window.location.reload(), 1500);
    }
  };

  const handleDebugLocalStorage = () => {
    debugLocalStorage();
    setMessage({
      type: 'info',
      text: 'LocalStorage contents logged to console. Open DevTools to view.'
    });
  };

  const getLocalStorageInfo = () => {
    const keys = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key) keys.push(key);
    }
    return keys;
  };

  const localStorageKeys = getLocalStorageInfo();
  const hasLegacyKeys = localStorageKeys.some(key =>
    key === 'portfolioProperties' || key === 'savedReports'
  );

  return (
    <Card>
      <CardContent>
        <Stack spacing={3}>
          <Box>
            <Typography variant="h6" gutterBottom>
              Data Management
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage browser localStorage data and ensure clean company isolation.
            </Typography>
          </Box>

          {message && (
            <Alert severity={message.type} onClose={() => setMessage(null)}>
              {message.text}
            </Alert>
          )}

          <Divider />

          {/* Current State Info */}
          <Box>
            <Typography variant="subtitle2" gutterBottom>
              Current State
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap" gap={1}>
              <Chip
                label={`${localStorageKeys.length} localStorage keys`}
                color={localStorageKeys.length === 0 ? 'success' : 'default'}
                size="small"
              />
              {hasLegacyKeys && (
                <Chip
                  label="Legacy data detected"
                  color="warning"
                  size="small"
                  icon={<InfoIcon />}
                />
              )}
              {selectedCompany && (
                <Chip
                  label={`Company: ${selectedCompany.name}`}
                  color="primary"
                  size="small"
                />
              )}
            </Stack>
          </Box>

          <Divider />

          {/* Actions */}
          <Stack spacing={2}>
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Quick Actions
              </Typography>
              <Stack spacing={1.5}>

                {/* Clear Legacy Data */}
                {hasLegacyKeys && (
                  <Box>
                    <Button
                      variant="outlined"
                      color="warning"
                      startIcon={<DeleteIcon />}
                      onClick={handleClearLegacyData}
                      fullWidth
                    >
                      Clear Legacy Data (Recommended)
                    </Button>
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                      Removes old non-company-specific data that may cause issues
                    </Typography>
                  </Box>
                )}

                {/* Clear Current Company Data */}
                <Box>
                  <Button
                    variant="outlined"
                    color="secondary"
                    startIcon={<DeleteIcon />}
                    onClick={handleClearCompanyData}
                    disabled={!selectedCompany}
                    fullWidth
                  >
                    Clear Current Company Data
                  </Button>
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                    Removes localStorage data for {selectedCompany ? selectedCompany.name : 'selected company'}
                  </Typography>
                </Box>

                {/* Clear All localStorage */}
                <Box>
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={<DeleteIcon />}
                    onClick={handleClearAllLocalStorage}
                    fullWidth
                  >
                    Clear All Browser Data
                  </Button>
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                    Removes ALL localStorage data (all companies, all settings)
                  </Typography>
                </Box>

                {/* Debug */}
                <Box>
                  <Button
                    variant="text"
                    startIcon={<InfoIcon />}
                    onClick={handleDebugLocalStorage}
                    fullWidth
                  >
                    View localStorage in Console
                  </Button>
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                    Logs all localStorage contents to browser console for debugging
                  </Typography>
                </Box>
              </Stack>
            </Box>
          </Stack>

          <Divider />

          {/* Info Box */}
          <Alert severity="info" icon={<InfoIcon />}>
            <Typography variant="body2">
              <strong>New companies always start with zero data.</strong>
              <br />
              If you see data after creating a new company, use "Clear Legacy Data" above.
            </Typography>
          </Alert>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default DataManagement;
