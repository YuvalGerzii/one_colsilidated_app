import React, { useMemo, useRef, useState } from 'react';
import {
  Box,
  Button,
  Chip,
  Divider,
  LinearProgress,
  List,
  ListItem,
  ListItemSecondaryAction,
  ListItemText,
  Paper,
  Stack,
  Typography,
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  CheckCircle as CheckCircleIcon,
  ErrorOutline as ErrorOutlineIcon,
  AccessTime as AccessTimeIcon,
} from '@mui/icons-material';

interface ExtractionFile {
  id: string;
  name: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress: number;
  confidence?: number;
}

const getConfidenceColor = (confidence?: number) => {
  if (confidence === undefined) return 'default';
  if (confidence > 0.85) return 'success';
  if (confidence >= 0.7) return 'warning';
  return 'error';
};

const getStatusIcon = (status: ExtractionFile['status']) => {
  switch (status) {
    case 'completed':
      return <CheckCircleIcon color="success" fontSize="small" />;
    case 'failed':
      return <ErrorOutlineIcon color="error" fontSize="small" />;
    case 'processing':
      return <AccessTimeIcon color="warning" fontSize="small" />;
    default:
      return <CloudUploadIcon color="action" fontSize="small" />;
  }
};

export const DocumentExtraction: React.FC = () => {
  const [files, setFiles] = useState<ExtractionFile[]>([]);
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const addFiles = (fileList: FileList | File[]) => {
    const accepted = Array.from(fileList).filter((file) => {
      if (file.type === 'application/pdf') return true;
      if (file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') return true;
      const extension = file.name.split('.').pop()?.toLowerCase();
      return extension === 'pdf' || extension === 'xlsx';
    });

    if (!accepted.length) return;

    const newEntries = accepted.map<ExtractionFile>((file) => ({
      id: `${file.name}-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      name: file.name,
      status: 'processing',
      progress: 10,
    }));

    setFiles((previous) => [...newEntries, ...previous]);

    newEntries.forEach((entry) => {
      const totalDuration = 4000 + Math.random() * 4000;
      const steps = Math.ceil(totalDuration / 400);

      const interval = setInterval(() => {
        setFiles((previous) =>
          previous.map((file) =>
            file.id === entry.id
              ? {
                  ...file,
                  progress: Math.min(95, file.progress + 100 / steps),
                }
              : file
          )
        );
      }, 400);

      setTimeout(() => {
        clearInterval(interval);
        const succeeded = Math.random() > 0.08;
        setFiles((previous) =>
          previous.map((file) =>
            file.id === entry.id
              ? {
                  ...file,
                  status: succeeded ? 'completed' : 'failed',
                  progress: 100,
                  confidence: succeeded
                    ? Math.round((0.65 + Math.random() * 0.35) * 100) / 100
                    : undefined,
                }
              : file
          )
        );
      }, totalDuration);
    });
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      addFiles(event.target.files);
      event.target.value = '';
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragActive(true);
  };

  const handleDragLeave = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragActive(false);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragActive(false);
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      addFiles(event.dataTransfer.files);
      event.dataTransfer.clearData();
    }
  };

  const sortedFiles = useMemo(
    () =>
      [...files].sort((a, b) => {
        const statusPriority: Record<ExtractionFile['status'], number> = {
          processing: 0,
          queued: 1,
          completed: 2,
          failed: 3,
        };
        return statusPriority[a.status] - statusPriority[b.status];
      }),
    [files]
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        PDF Upload & Extraction
      </Typography>
      <Typography variant="body1" color="text.secondary" mb={4}>
        Drag and drop deal documents to extract key financials with automated confidence scoring.
      </Typography>

      <Paper
        variant="outlined"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        sx={{
          borderStyle: 'dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.400',
          backgroundColor: isDragActive ? 'primary.50' : 'background.paper',
          p: 6,
          textAlign: 'center',
          transition: 'all 0.2s ease-in-out',
        }}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          hidden
          accept=".pdf,.xlsx,application/pdf,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          onChange={handleInputChange}
        />
        <Stack spacing={2} alignItems="center">
          <CloudUploadIcon color="primary" sx={{ fontSize: 48 }} />
          <Box>
            <Typography variant="h6">Drop PDFs or spreadsheets here</Typography>
            <Typography variant="body2" color="text.secondary">
              {isDragActive
                ? 'Release to start extracting.'
                : 'or click to browse your files'}
            </Typography>
          </Box>
          <Button variant="contained" onClick={handleBrowseClick}>
            Browse files
          </Button>
        </Stack>
      </Paper>

      <Paper sx={{ mt: 5 }}>
        <Box px={3} py={2}>
          <Typography variant="h6">Extraction queue</Typography>
          <Typography variant="body2" color="text.secondary">
            Track parsing progress, OCR status, and AI-extracted metrics.
          </Typography>
        </Box>
        <Divider />
        {sortedFiles.length === 0 ? (
          <Box px={3} py={5} textAlign="center" color="text.secondary">
            No uploads yet. Start by dragging files into the dropzone above.
          </Box>
        ) : (
          <List>
            {sortedFiles.map((file) => (
              <ListItem key={file.id} divider>
                <ListItemText
                  primary={file.name}
                  secondary={
                    file.status === 'completed'
                      ? 'Extraction complete'
                      : file.status === 'failed'
                      ? 'Extraction failed – please retry'
                      : 'Processing extraction'
                  }
                />
                <Stack spacing={1} sx={{ minWidth: 200 }}>
                  <LinearProgress
                    variant="determinate"
                    value={Math.min(100, Math.round(file.progress))}
                  />
                  {file.confidence !== undefined && (
                    <Chip
                      label={`Confidence ${(file.confidence * 100).toFixed(0)}%`}
                      color={getConfidenceColor(file.confidence)}
                      size="small"
                    />
                  )}
                </Stack>
                <ListItemSecondaryAction>
                  {getStatusIcon(file.status)}
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        )}
      </Paper>

      <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="flex-end" mt={4} spacing={2}>
        <Button variant="outlined">Download logs</Button>
        <Button variant="contained" color="primary" size="large">
          Review & Approve
        </Button>
      </Stack>
    </Box>
  );
};
