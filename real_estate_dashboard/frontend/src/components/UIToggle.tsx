import React from 'react';
import { Box, ToggleButtonGroup, ToggleButton, Chip } from '@mui/material';
import { useUIMode } from '../contexts/UIModeContext';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import ClassicIcon from '@mui/icons-material/ViewComfy';

export function UIToggle() {
  const { uiMode, setUIMode } = useUIMode();

  const handleChange = (_event: React.MouseEvent<HTMLElement>, newMode: 'old' | 'new' | null) => {
    if (newMode !== null) {
      setUIMode(newMode);
    }
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      <ToggleButtonGroup
        value={uiMode}
        exclusive
        onChange={handleChange}
        size="small"
        sx={{
          '& .MuiToggleButton-root': {
            px: 2,
            py: 0.5,
            textTransform: 'none',
            fontSize: '0.875rem',
            fontWeight: 500,
          },
        }}
      >
        <ToggleButton value="old">
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <ClassicIcon fontSize="small" />
            Old UI
          </Box>
        </ToggleButton>
        <ToggleButton value="new">
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <AutoAwesomeIcon fontSize="small" />
            New UI
            <Chip
              label="BETA"
              size="small"
              color="primary"
              sx={{
                height: 16,
                fontSize: '0.65rem',
                fontWeight: 700,
                ml: 0.5
              }}
            />
          </Box>
        </ToggleButton>
      </ToggleButtonGroup>
    </Box>
  );
}
