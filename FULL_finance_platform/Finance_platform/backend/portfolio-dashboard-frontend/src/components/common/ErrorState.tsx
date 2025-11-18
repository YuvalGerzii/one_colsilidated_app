// src/components/common/ErrorState.tsx
import React from 'react';
import { Box, Typography, Button, Alert, Stack } from '@mui/material';
import { ErrorOutline as ErrorIcon, Refresh as RefreshIcon } from '@mui/icons-material';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  fullPage?: boolean;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Something went wrong',
  message = 'An error occurred while loading this content. Please try again.',
  onRetry,
  fullPage = false,
}) => {
  const content = (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        py: fullPage ? 12 : 6,
        px: 2,
        textAlign: 'center',
      }}
    >
      <Box
        sx={{
          width: 80,
          height: 80,
          borderRadius: '50%',
          bgcolor: 'error.lighter',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mb: 3,
        }}
      >
        <ErrorIcon sx={{ fontSize: 40, color: 'error.main' }} />
      </Box>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
        {title}
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 500, mb: 4 }}>
        {message}
      </Typography>
      {onRetry && (
        <Button variant="contained" size="large" startIcon={<RefreshIcon />} onClick={onRetry}>
          Try Again
        </Button>
      )}
    </Box>
  );

  if (fullPage) {
    return (
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          bgcolor: 'background.default',
        }}
      >
        {content}
      </Box>
    );
  }

  return content;
};

interface ErrorAlertProps {
  message: string;
  onRetry?: () => void;
  onDismiss?: () => void;
}

export const ErrorAlert: React.FC<ErrorAlertProps> = ({ message, onRetry, onDismiss }) => {
  return (
    <Alert
      severity="error"
      onClose={onDismiss}
      action={
        onRetry && (
          <Button color="inherit" size="small" onClick={onRetry}>
            Retry
          </Button>
        )
      }
      sx={{ mb: 2 }}
    >
      {message}
    </Alert>
  );
};
