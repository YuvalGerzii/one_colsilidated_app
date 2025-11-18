import React from 'react';
import { Box, Container } from '@mui/material';
import { styled } from '@mui/material/styles';
import { EnhancedModelPage } from './EnhancedModelPage';
import { getModelConfig } from '../../config/modelConfig';

// Custom wrapper for full-page dark theme
const DarkThemeWrapper = styled(Box)(({ theme }) => ({
  background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
  minHeight: '100vh',
  margin: '-64px -24px 0 -24px', // Negative margins to break out of parent padding
  padding: '64px 0 0 0',
  width: 'calc(100% + 48px)', // Compensate for negative margins
  position: 'relative',

  // Override default theme colors for child components
  '& .MuiPaper-root': {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
  },

  '& .MuiTypography-root': {
    color: 'white',
  },

  '& .MuiTypography-body2, & .MuiTypography-caption': {
    color: 'rgba(255, 255, 255, 0.8)',
  },

  '& .MuiTab-root': {
    color: 'rgba(255, 255, 255, 0.7)',
    '&.Mui-selected': {
      color: 'white',
    },
  },

  '& .MuiTabs-root': {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderRadius: '12px',
  },

  '& .MuiTabs-indicator': {
    backgroundColor: 'white',
    height: '3px',
  },

  '& .MuiChip-root': {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    color: 'white',
    border: '1px solid rgba(255, 255, 255, 0.2)',
  },

  '& .MuiAlert-root': {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    color: 'white',
    '& .MuiAlert-icon': {
      color: 'white',
    },
  },

  '& .MuiButton-root': {
    '&.MuiButton-outlined': {
      color: 'white',
      borderColor: 'rgba(255, 255, 255, 0.3)',
      '&:hover': {
        borderColor: 'rgba(255, 255, 255, 0.5)',
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
      },
    },
    '&.MuiButton-contained': {
      backgroundColor: 'white',
      color: '#1e3c72',
      '&:hover': {
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
      },
    },
  },

  '& .MuiTextField-root': {
    '& .MuiOutlinedInput-root': {
      backgroundColor: 'rgba(255, 255, 255, 0.05)',
      color: 'white',
      '& fieldset': {
        borderColor: 'rgba(255, 255, 255, 0.2)',
      },
      '&:hover fieldset': {
        borderColor: 'rgba(255, 255, 255, 0.3)',
      },
      '&.Mui-focused fieldset': {
        borderColor: 'rgba(255, 255, 255, 0.5)',
      },
    },
    '& .MuiInputLabel-root': {
      color: 'rgba(255, 255, 255, 0.7)',
      '&.Mui-focused': {
        color: 'white',
      },
    },
  },

  '& .MuiCard-root': {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
  },

  '& .MuiDivider-root': {
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },

  '& .MuiTableCell-root': {
    color: 'white',
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },

  '& .MuiTableHead-root .MuiTableCell-root': {
    backgroundColor: 'rgba(255, 255, 255, 0.08)',
    color: 'white',
    fontWeight: 600,
  },

  '& .MuiTableBody-root .MuiTableRow-root': {
    '&:nth-of-type(odd)': {
      backgroundColor: 'rgba(255, 255, 255, 0.02)',
    },
    '&:hover': {
      backgroundColor: 'rgba(255, 255, 255, 0.05)',
    },
  },

  // Fix iframe loading overlay
  '& .MuiCircularProgress-root': {
    color: 'white',
  },

  // Breadcrumb styling
  '& a': {
    color: 'rgba(255, 255, 255, 0.9)',
    textDecoration: 'none',
    '&:hover': {
      textDecoration: 'underline',
    },
  },
}));

// Custom container for full width
const FullWidthContainer = styled(Container)(({ theme }) => ({
  maxWidth: '100% !important',
  padding: '0 !important',
  margin: 0,
}));

export const FixAndFlipPage: React.FC = () => {
  const modelConfig = getModelConfig('fix_and_flip');

  if (!modelConfig) {
    return <div>Model configuration not found</div>;
  }

  // Override the model config color to match the dark theme
  const themedModelConfig = {
    ...modelConfig,
    color: '#42a5f5', // Light blue for accents in dark theme
  };

  return (
    <DarkThemeWrapper>
      <FullWidthContainer>
        <Box sx={{ px: 4, py: 3 }}>
          <EnhancedModelPage modelConfig={themedModelConfig} />
        </Box>
      </FullWidthContainer>
    </DarkThemeWrapper>
  );
};
