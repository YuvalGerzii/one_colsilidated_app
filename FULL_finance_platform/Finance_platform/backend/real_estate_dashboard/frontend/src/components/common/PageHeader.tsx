import React from 'react';
import { Box, Typography, Stack, Button, IconButton, Divider } from '@mui/material';
import { SvgIconComponent } from '@mui/icons-material';

interface PageHeaderAction {
  label: string;
  onClick: () => void;
  icon?: SvgIconComponent;
  variant?: 'contained' | 'outlined' | 'text';
  color?: 'primary' | 'secondary' | 'error' | 'warning' | 'info' | 'success';
}

interface PageHeaderProps {
  title: string;
  description?: string;
  icon?: SvgIconComponent;
  actions?: PageHeaderAction[];
  secondaryActions?: PageHeaderAction[];
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  description,
  icon: Icon,
  actions = [],
  secondaryActions = [],
}) => {
  return (
    <Box sx={{ mb: 4 }}>
      <Stack
        direction={{ xs: 'column', sm: 'row' }}
        alignItems={{ xs: 'flex-start', sm: 'center' }}
        justifyContent="space-between"
        spacing={2}
        sx={{ mb: 2 }}
      >
        <Stack direction="row" alignItems="center" spacing={2}>
          {Icon && (
            <Box
              sx={{
                width: 56,
                height: 56,
                borderRadius: 2,
                bgcolor: 'primary.main',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Icon sx={{ fontSize: 32 }} />
            </Box>
          )}
          <Box>
            <Typography
              variant="h4"
              component="h1"
              fontWeight="bold"
              sx={{
                background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              {title}
            </Typography>
            {description && (
              <Typography variant="body1" color="text.secondary" sx={{ mt: 0.5 }}>
                {description}
              </Typography>
            )}
          </Box>
        </Stack>

        {(actions.length > 0 || secondaryActions.length > 0) && (
          <Stack direction="row" spacing={1} flexWrap="wrap">
            {secondaryActions.map((action, index) => {
              const ActionIcon = action.icon;
              return (
                <IconButton
                  key={index}
                  onClick={action.onClick}
                  color={action.color || 'default'}
                  title={action.label}
                  sx={{
                    bgcolor: 'background.paper',
                    '&:hover': {
                      bgcolor: 'action.hover',
                    },
                  }}
                >
                  {ActionIcon && <ActionIcon />}
                </IconButton>
              );
            })}
            {actions.map((action, index) => {
              const ActionIcon = action.icon;
              return (
                <Button
                  key={index}
                  variant={action.variant || 'contained'}
                  color={action.color || 'primary'}
                  onClick={action.onClick}
                  startIcon={ActionIcon && <ActionIcon />}
                >
                  {action.label}
                </Button>
              );
            })}
          </Stack>
        )}
      </Stack>
      <Divider />
    </Box>
  );
};
