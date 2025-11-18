// src/components/common/EmptyState.tsx
import React from 'react';
import { Box, Typography, Button, Stack } from '@mui/material';
import { SvgIconComponent } from '@mui/icons-material';

interface EmptyStateProps {
  icon?: SvgIconComponent;
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  secondaryActionLabel?: string;
  onSecondaryAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  secondaryActionLabel,
  onSecondaryAction,
}) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        py: 8,
        px: 2,
        textAlign: 'center',
      }}
    >
      {Icon && (
        <Box
          sx={{
            width: 80,
            height: 80,
            borderRadius: '50%',
            bgcolor: 'action.hover',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            mb: 3,
          }}
        >
          <Icon sx={{ fontSize: 40, color: 'text.secondary' }} />
        </Box>
      )}
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
        {title}
      </Typography>
      {description && (
        <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 500, mb: 3 }}>
          {description}
        </Typography>
      )}
      {(actionLabel || secondaryActionLabel) && (
        <Stack direction="row" spacing={2}>
          {actionLabel && (
            <Button variant="contained" size="large" onClick={onAction}>
              {actionLabel}
            </Button>
          )}
          {secondaryActionLabel && (
            <Button variant="outlined" size="large" onClick={onSecondaryAction}>
              {secondaryActionLabel}
            </Button>
          )}
        </Stack>
      )}
    </Box>
  );
};
