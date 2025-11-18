import { createTheme, alpha } from '@mui/material/styles';

// Modern color palette for the freelance hub
const colors = {
  primary: {
    main: '#667eea',
    light: '#a8b3f5',
    dark: '#4c5fcf',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
  secondary: {
    main: '#f093fb',
    light: '#f5b3fd',
    dark: '#c76dd8',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  },
  success: {
    main: '#43e97b',
    light: '#6fef9a',
    dark: '#2fc564',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  },
  info: {
    main: '#4facfe',
    light: '#75bffe',
    dark: '#2a8ee6',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  },
  warning: {
    main: '#ffd93d',
    light: '#ffe261',
    dark: '#f5c518',
    gradient: 'linear-gradient(135deg, #ffd93d 0%, #ff9f00 100%)',
  },
  error: {
    main: '#f5576c',
    light: '#f77a8a',
    dark: '#e03649',
    gradient: 'linear-gradient(135deg, #f5576c 0%, #f093fb 100%)',
  },
  background: {
    default: '#f8f9fe',
    paper: '#ffffff',
    subtle: '#f5f7fa',
  },
  text: {
    primary: '#2d3748',
    secondary: '#718096',
    disabled: '#a0aec0',
  },
};

// Create the theme
export const freelanceTheme = createTheme({
  palette: {
    ...colors,
    mode: 'light',
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    h1: {
      fontWeight: 800,
      fontSize: '3.5rem',
      lineHeight: 1.2,
      letterSpacing: '-0.02em',
    },
    h2: {
      fontWeight: 700,
      fontSize: '3rem',
      lineHeight: 1.3,
      letterSpacing: '-0.01em',
    },
    h3: {
      fontWeight: 700,
      fontSize: '2.5rem',
      lineHeight: 1.3,
    },
    h4: {
      fontWeight: 700,
      fontSize: '2rem',
      lineHeight: 1.4,
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.5rem',
      lineHeight: 1.4,
    },
    h6: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.5,
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 500,
      lineHeight: 1.6,
    },
    subtitle2: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: 1.6,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.6,
    },
    button: {
      textTransform: 'none',
      fontWeight: 600,
      fontSize: '0.95rem',
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0 2px 8px rgba(0,0,0,0.06)',
    '0 4px 12px rgba(0,0,0,0.08)',
    '0 6px 16px rgba(0,0,0,0.08)',
    '0 8px 24px rgba(0,0,0,0.10)',
    '0 12px 32px rgba(0,0,0,0.12)',
    '0 16px 48px rgba(0,0,0,0.14)',
    '0 20px 64px rgba(0,0,0,0.16)',
    '0 24px 80px rgba(0,0,0,0.18)',
    '0 28px 96px rgba(0,0,0,0.20)',
    ...Array(15).fill('0 0 0 rgba(0,0,0,0)'),
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          textTransform: 'none',
          fontWeight: 600,
          padding: '10px 24px',
          boxShadow: 'none',
          transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            transform: 'translateY(-1px)',
          },
        },
        contained: {
          '&:hover': {
            boxShadow: '0 6px 20px rgba(0,0,0,0.2)',
          },
        },
        outlined: {
          borderWidth: 2,
          '&:hover': {
            borderWidth: 2,
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid rgba(0,0,0,0.06)',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
        elevation1: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
        },
        elevation2: {
          boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
        },
        elevation3: {
          boxShadow: '0 6px 16px rgba(0,0,0,0.08)',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
        filled: {
          borderWidth: 1,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 12,
            transition: 'all 0.2s ease',
            '&:hover': {
              '& .MuiOutlinedInput-notchedOutline': {
                borderColor: colors.primary.light,
              },
            },
            '&.Mui-focused': {
              '& .MuiOutlinedInput-notchedOutline': {
                borderWidth: 2,
              },
            },
          },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          fontSize: '0.95rem',
          minHeight: 64,
          '&.Mui-selected': {
            color: colors.primary.main,
          },
        },
      },
    },
    MuiTabs: {
      styleOverrides: {
        indicator: {
          height: 3,
          borderRadius: '3px 3px 0 0',
        },
      },
    },
    MuiAvatar: {
      styleOverrides: {
        root: {
          fontWeight: 600,
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          fontWeight: 500,
        },
        standard: {
          border: '1px solid',
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          height: 8,
        },
      },
    },
  },
});

// Dark theme variant
export const freelanceDarkTheme = createTheme({
  ...freelanceTheme,
  palette: {
    mode: 'dark',
    primary: colors.primary,
    secondary: colors.secondary,
    success: colors.success,
    info: colors.info,
    warning: colors.warning,
    error: colors.error,
    background: {
      default: '#0f1419',
      paper: '#1a1f2e',
      subtle: '#151a24',
    },
    text: {
      primary: '#e2e8f0',
      secondary: '#a0aec0',
      disabled: '#718096',
    },
  },
});

// Utility functions for gradients and effects
export const gradients = {
  primary: colors.primary.gradient,
  secondary: colors.secondary.gradient,
  success: colors.success.gradient,
  info: colors.info.gradient,
  warning: colors.warning.gradient,
  error: colors.error.gradient,

  // Additional creative gradients
  sunset: 'linear-gradient(135deg, #ff6b6b 0%, #ffd93d 100%)',
  ocean: 'linear-gradient(135deg, #667eea 0%, #00f2fe 100%)',
  forest: 'linear-gradient(135deg, #38ef7d 0%, #11998e 100%)',
  royal: 'linear-gradient(135deg, #667eea 0%, #f093fb 100%)',
  fire: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
};

// Glass morphism styles
export const glassMorphism = (theme) => ({
  background: alpha(theme.palette.background.paper, 0.8),
  backdropFilter: 'blur(20px)',
  border: `1px solid ${alpha(theme.palette.common.white, 0.2)}`,
  boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
});

// Neumorphism styles
export const neumorphism = (theme) => ({
  background: theme.palette.background.paper,
  boxShadow: `
    8px 8px 16px ${alpha(theme.palette.common.black, 0.1)},
    -8px -8px 16px ${alpha(theme.palette.common.white, 0.9)}
  `,
});

export default freelanceTheme;
