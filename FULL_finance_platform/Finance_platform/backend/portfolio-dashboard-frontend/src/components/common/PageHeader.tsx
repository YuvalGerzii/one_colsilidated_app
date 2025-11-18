// src/components/common/PageHeader.tsx
import React, { ReactNode } from 'react';
import { Box, Typography, Button, Stack } from '@mui/material';
import { SvgIconComponent } from '@mui/icons-material';

interface PageHeaderProps {
  title: string;
  description?: string;
  icon?: SvgIconComponent;
  primaryAction?: {
    label: string;
    onClick: () => void;
    icon?: SvgIconComponent;
  };
  secondaryActions?: Array<{
    label: string;
    onClick: () => void;
    icon?: SvgIconComponent;
  }>;
  children?: ReactNode;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  description,
  icon: Icon,
  primaryAction,
  secondaryActions,
  children,
}) => {
  return (
    <Box sx={{ mb: 4 }}>
      <Stack
        direction={{ xs: 'column', sm: 'row' }}
        justifyContent="space-between"
        alignItems={{ xs: 'flex-start', sm: 'center' }}
        spacing={2}
        sx={{ mb: 2 }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {Icon && (
            <Box
              sx={{
                width: 48,
                height: 48,
                borderRadius: 2,
                bgcolor: 'primary.main',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
              }}
            >
              <Icon sx={{ fontSize: 28 }} />
            </Box>
          )}
          <Box>
            <Typography variant="h4" component="h1" gutterBottom={!!description} sx={{ fontWeight: 600 }}>
              {title}
            </Typography>
            {description && (
              <Typography variant="body1" color="text.secondary">
                {description}
              </Typography>
            )}
          </Box>
        </Box>

        {(primaryAction || secondaryActions) && (
          <Stack direction="row" spacing={1.5}>
            {secondaryActions?.map((action, index) => (
              <Button
                key={index}
                variant="outlined"
                onClick={action.onClick}
                startIcon={action.icon && <action.icon />}
              >
                {action.label}
              </Button>
            ))}
            {primaryAction && (
              <Button
                variant="contained"
                size="large"
                onClick={primaryAction.onClick}
                startIcon={primaryAction.icon && <primaryAction.icon />}
              >
                {primaryAction.label}
              </Button>
            )}
          </Stack>
        )}
      </Stack>
      {children}
    </Box>
  );
};
