/**
 * Error Boundary Component
 *
 * Catches React errors in the component tree and displays a fallback UI
 * instead of crashing the entire application.
 *
 * Features:
 * - Catches rendering errors
 * - Provides user-friendly error UI
 * - Logs errors to console (can be extended to send to error tracking)
 * - Allows users to reset the error state
 */

import React, { Component, ErrorInfo, ReactNode } from 'react';
import {
  Box,
  Button,
  Container,
  Paper,
  Typography,
  Stack,
  Alert,
  Divider,
} from '@mui/material';
import {
  ErrorOutline as ErrorIcon,
  Refresh as RefreshIcon,
  Home as HomeIcon,
} from '@mui/icons-material';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error details for debugging
    console.error('Error Boundary caught an error:', error);
    console.error('Error Info:', errorInfo);

    // Update state with error details
    this.setState({
      error,
      errorInfo,
    });

    // TODO: Send error to error tracking service (Sentry, LogRocket, etc.)
    // Example:
    // Sentry.captureException(error, { extra: errorInfo });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  handleGoHome = () => {
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      // Custom fallback UI can be provided
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default fallback UI
      return (
        <Container maxWidth="md">
          <Box
            display="flex"
            flexDirection="column"
            justifyContent="center"
            alignItems="center"
            minHeight="100vh"
            py={4}
          >
            <Paper
              elevation={3}
              sx={{
                p: 4,
                width: '100%',
                textAlign: 'center',
              }}
            >
              <ErrorIcon
                sx={{
                  fontSize: 80,
                  color: 'error.main',
                  mb: 2,
                }}
              />

              <Typography variant="h4" gutterBottom fontWeight="bold">
                Oops! Something went wrong
              </Typography>

              <Typography variant="body1" color="text.secondary" paragraph>
                We're sorry, but something unexpected happened. The error has been logged
                and we'll look into it.
              </Typography>

              <Divider sx={{ my: 3 }} />

              <Stack spacing={2} direction="row" justifyContent="center">
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<RefreshIcon />}
                  onClick={this.handleReset}
                  size="large"
                >
                  Try Again
                </Button>

                <Button
                  variant="outlined"
                  startIcon={<HomeIcon />}
                  onClick={this.handleGoHome}
                  size="large"
                >
                  Go Home
                </Button>
              </Stack>

              {/* Show error details in development */}
              {import.meta.env.DEV && this.state.error && (
                <Box mt={4}>
                  <Alert severity="error" sx={{ textAlign: 'left' }}>
                    <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                      Error Details (Development Only):
                    </Typography>
                    <Typography
                      variant="body2"
                      component="pre"
                      sx={{
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word',
                        fontFamily: 'monospace',
                        fontSize: '0.75rem',
                      }}
                    >
                      {this.state.error.toString()}
                      {this.state.errorInfo?.componentStack}
                    </Typography>
                  </Alert>
                </Box>
              )}
            </Paper>
          </Box>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

/**
 * Hook-based error boundary for functional components
 * Note: This is a workaround since React doesn't have hook-based error boundaries yet
 */
export const useErrorHandler = () => {
  const [error, setError] = React.useState<Error | null>(null);

  React.useEffect(() => {
    if (error) {
      throw error;
    }
  }, [error]);

  return setError;
};
