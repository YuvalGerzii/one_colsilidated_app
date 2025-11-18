import React from 'react';
import { Box, Typography, Button, Stack, Paper } from '@mui/material';
import { SvgIconComponent } from '@mui/icons-material';
import {
  HomeWork as HomeWorkIcon,
  AddCircleOutline as AddIcon,
  SearchOff as SearchOffIcon,
  ErrorOutline as ErrorIcon,
} from '@mui/icons-material';

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: SvgIconComponent;
  actionLabel?: string;
  onAction?: () => void;
  variant?: 'default' | 'error' | 'search';
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  icon: Icon,
  actionLabel,
  onAction,
  variant = 'default',
}) => {
  const getIcon = () => {
    if (Icon) return Icon;
    if (variant === 'error') return ErrorIcon;
    if (variant === 'search') return SearchOffIcon;
    return HomeWorkIcon;
  };

  const DisplayIcon = getIcon();

  return (
    <Paper
      elevation={0}
      sx={{
        p: 6,
        textAlign: 'center',
        bgcolor: 'background.default',
        border: '2px dashed',
        borderColor: 'divider',
        borderRadius: 3,
      }}
    >
      <Stack spacing={3} alignItems="center">
        <Box
          sx={{
            width: 80,
            height: 80,
            borderRadius: '50%',
            bgcolor: variant === 'error' ? 'error.lighter' : 'primary.lighter',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <DisplayIcon
            sx={{
              fontSize: 48,
              color: variant === 'error' ? 'error.main' : 'primary.main',
            }}
          />
        </Box>

        <Box>
          <Typography variant="h5" gutterBottom fontWeight="bold">
            {title}
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 500 }}>
            {description}
          </Typography>
        </Box>

        {actionLabel && onAction && (
          <Button
            variant="contained"
            size="large"
            startIcon={<AddIcon />}
            onClick={onAction}
            sx={{ mt: 2 }}
          >
            {actionLabel}
          </Button>
        )}
      </Stack>
    </Paper>
  );
};
