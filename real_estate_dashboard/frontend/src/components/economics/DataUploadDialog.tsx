import React, { useState, useCallback } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Alert,
  LinearProgress,
  Stack,
  Paper,
  Chip,
  IconButton,
  FormControlLabel,
  Switch,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Description as FileIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Download as DownloadIcon,
  Close as CloseIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';
import { api } from '../../services/apiClient';

interface DataUploadDialogProps {
  open: boolean;
  onClose: () => void;
  onUploadSuccess?: () => void;
}

interface UploadResult {
  success: boolean;
  file_name: string;
  indicators_parsed: number;
  indicators_saved?: number;
  indicators_updated?: number;
  indicators_skipped?: number;
  errors?: string[];
  validation_errors?: string[];
  message: string;
}

export const DataUploadDialog: React.FC<DataUploadDialogProps> = ({
  open,
  onClose,
  onUploadSuccess,
}) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [overwrite, setOverwrite] = useState(false);
  const [downloadingTemplate, setDownloadingTemplate] = useState(false);

  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      const validExtensions = ['.csv', '.xlsx', '.xls'];
      const fileExtension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));

      if (!validExtensions.includes(fileExtension)) {
        setError(`Invalid file type. Please upload a ${validExtensions.join(', ')} file.`);
        setSelectedFile(null);
        return;
      }

      setSelectedFile(file);
      setError(null);
      setUploadResult(null);
    }
  }, []);

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setUploading(true);
      setError(null);
      setUploadResult(null);

      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await api.post(
        `/market-intelligence/data/usa-economics/upload?overwrite=${overwrite}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setUploadResult(response.data);

      if (response.data.success && onUploadSuccess) {
        // Call success callback after a short delay to show results
        setTimeout(() => {
          onUploadSuccess();
        }, 2000);
      }
    } catch (err: any) {
      console.error('Upload error:', err);
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleDownloadTemplate = async (format: 'csv' | 'excel') => {
    try {
      setDownloadingTemplate(true);
      setError(null);

      const response = await api.get(
        `/market-intelligence/data/usa-economics/template?format=${format}`,
        {
          responseType: 'blob',
        }
      );

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `economic_indicators_template.${format === 'csv' ? 'csv' : 'xlsx'}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      console.error('Template download error:', err);
      setError('Failed to download template');
    } finally {
      setDownloadingTemplate(false);
    }
  };

  const handleClose = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setError(null);
    setOverwrite(false);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle sx={{ pb: 1 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Stack direction="row" alignItems="center" spacing={1}>
            <UploadIcon sx={{ color: '#3b82f6' }} />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Upload Economic Data
            </Typography>
          </Stack>
          <IconButton onClick={handleClose} size="small">
            <CloseIcon />
          </IconButton>
        </Stack>
      </DialogTitle>

      <DialogContent>
        <Stack spacing={3}>
          {/* Instructions */}
          <Alert severity="info" icon={<InfoIcon />}>
            <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
              Upload CSV or Excel files with economic indicators
            </Typography>
            <Typography variant="caption" component="div">
              • Supported formats: .csv, .xlsx, .xls
            </Typography>
            <Typography variant="caption" component="div">
              • Required columns: indicator, category, value, unit
            </Typography>
            <Typography variant="caption" component="div">
              • Optional columns: previous, date, highest, lowest
            </Typography>
          </Alert>

          {/* Template Download */}
          <Paper sx={{ p: 2, bgcolor: isDark ? 'rgba(59, 130, 246, 0.05)' : 'rgba(59, 130, 246, 0.02)' }}>
            <Stack spacing={1}>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                Download Template
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Not sure about the format? Download a template file to see the required structure.
              </Typography>
              <Stack direction="row" spacing={1}>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={() => handleDownloadTemplate('csv')}
                  disabled={downloadingTemplate}
                >
                  CSV Template
                </Button>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={() => handleDownloadTemplate('excel')}
                  disabled={downloadingTemplate}
                >
                  Excel Template
                </Button>
              </Stack>
            </Stack>
          </Paper>

          <Divider />

          {/* File Upload */}
          <Box>
            <input
              type="file"
              id="file-upload"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            <label htmlFor="file-upload">
              <Button
                component="span"
                variant="outlined"
                startIcon={<FileIcon />}
                fullWidth
                sx={{ py: 2 }}
              >
                {selectedFile ? selectedFile.name : 'Select File'}
              </Button>
            </label>
          </Box>

          {/* Selected File Info */}
          {selectedFile && (
            <Paper sx={{ p: 2, bgcolor: isDark ? 'rgba(16, 185, 129, 0.05)' : 'rgba(16, 185, 129, 0.02)' }}>
              <Stack direction="row" alignItems="center" spacing={2}>
                <FileIcon sx={{ color: '#10b981', fontSize: 32 }} />
                <Box sx={{ flex: 1 }}>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    {selectedFile.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {(selectedFile.size / 1024).toFixed(2)} KB
                  </Typography>
                </Box>
                <Chip label="Ready" color="success" size="small" />
              </Stack>
            </Paper>
          )}

          {/* Overwrite Option */}
          {selectedFile && (
            <FormControlLabel
              control={
                <Switch
                  checked={overwrite}
                  onChange={(e) => setOverwrite(e.target.checked)}
                  color="primary"
                />
              }
              label={
                <Typography variant="body2">
                  Overwrite existing indicators with same name
                </Typography>
              }
            />
          )}

          {/* Upload Progress */}
          {uploading && (
            <Box>
              <LinearProgress />
              <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
                Uploading and processing file...
              </Typography>
            </Box>
          )}

          {/* Error Message */}
          {error && (
            <Alert severity="error" icon={<ErrorIcon />}>
              {error}
            </Alert>
          )}

          {/* Upload Result */}
          {uploadResult && (
            <Paper
              sx={{
                p: 2,
                bgcolor: uploadResult.success
                  ? isDark ? 'rgba(16, 185, 129, 0.1)' : 'rgba(16, 185, 129, 0.05)'
                  : isDark ? 'rgba(239, 68, 68, 0.1)' : 'rgba(239, 68, 68, 0.05)',
                border: `1px solid ${uploadResult.success ? '#10b981' : '#ef4444'}`,
              }}
            >
              <Stack spacing={2}>
                <Stack direction="row" alignItems="center" spacing={1}>
                  {uploadResult.success ? (
                    <SuccessIcon sx={{ color: '#10b981' }} />
                  ) : (
                    <ErrorIcon sx={{ color: '#ef4444' }} />
                  )}
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    {uploadResult.message}
                  </Typography>
                </Stack>

                {uploadResult.success && (
                  <Stack direction="row" spacing={2}>
                    <Chip
                      label={`${uploadResult.indicators_parsed} Parsed`}
                      size="small"
                      sx={{ bgcolor: isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)' }}
                    />
                    {uploadResult.indicators_saved !== undefined && (
                      <Chip
                        label={`${uploadResult.indicators_saved} Saved`}
                        size="small"
                        color="success"
                      />
                    )}
                    {uploadResult.indicators_updated !== undefined && uploadResult.indicators_updated > 0 && (
                      <Chip
                        label={`${uploadResult.indicators_updated} Updated`}
                        size="small"
                        sx={{ bgcolor: isDark ? 'rgba(245, 158, 11, 0.2)' : 'rgba(245, 158, 11, 0.1)' }}
                      />
                    )}
                    {uploadResult.indicators_skipped !== undefined && uploadResult.indicators_skipped > 0 && (
                      <Chip
                        label={`${uploadResult.indicators_skipped} Skipped`}
                        size="small"
                        sx={{ bgcolor: isDark ? 'rgba(156, 163, 175, 0.2)' : 'rgba(156, 163, 175, 0.1)' }}
                      />
                    )}
                  </Stack>
                )}

                {/* Errors List */}
                {(uploadResult.errors && uploadResult.errors.length > 0) && (
                  <Box>
                    <Typography variant="caption" sx={{ fontWeight: 600, color: '#ef4444' }}>
                      Errors ({uploadResult.errors.length}):
                    </Typography>
                    <List dense>
                      {uploadResult.errors.slice(0, 5).map((err, idx) => (
                        <ListItem key={idx} sx={{ py: 0.5 }}>
                          <ListItemIcon sx={{ minWidth: 32 }}>
                            <ErrorIcon sx={{ fontSize: 16, color: '#ef4444' }} />
                          </ListItemIcon>
                          <ListItemText
                            primary={err}
                            primaryTypographyProps={{ variant: 'caption' }}
                          />
                        </ListItem>
                      ))}
                      {uploadResult.errors.length > 5 && (
                        <Typography variant="caption" color="text.secondary" sx={{ pl: 2 }}>
                          ... and {uploadResult.errors.length - 5} more errors
                        </Typography>
                      )}
                    </List>
                  </Box>
                )}

                {/* Validation Errors */}
                {(uploadResult.validation_errors && uploadResult.validation_errors.length > 0) && (
                  <Box>
                    <Typography variant="caption" sx={{ fontWeight: 600, color: '#ef4444' }}>
                      Validation Errors:
                    </Typography>
                    <List dense>
                      {uploadResult.validation_errors.map((err, idx) => (
                        <ListItem key={idx} sx={{ py: 0.5 }}>
                          <ListItemIcon sx={{ minWidth: 32 }}>
                            <ErrorIcon sx={{ fontSize: 16, color: '#ef4444' }} />
                          </ListItemIcon>
                          <ListItemText
                            primary={err}
                            primaryTypographyProps={{ variant: 'caption' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                )}
              </Stack>
            </Paper>
          )}
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={handleClose} disabled={uploading}>
          {uploadResult?.success ? 'Close' : 'Cancel'}
        </Button>
        {!uploadResult?.success && (
          <Button
            variant="contained"
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
            startIcon={<UploadIcon />}
          >
            Upload
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};
