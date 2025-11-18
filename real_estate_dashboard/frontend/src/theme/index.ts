import { createTheme, ThemeOptions } from '@mui/material/styles';

// Create theme based on mode
export const createAppTheme = (mode: 'light' | 'dark') => {
  const isDark = mode === 'dark';

  const themeOptions: ThemeOptions = {
    palette: {
      mode,
    primary: {
      main: '#3b82f6', // blue-500
      light: '#60a5fa', // blue-400
      dark: '#2563eb', // blue-600
      contrastText: '#fff',
    },
    secondary: {
      main: '#8b5cf6', // violet-500
      light: '#a78bfa', // violet-400
      dark: '#7c3aed', // violet-600
      contrastText: '#fff',
    },
    success: {
      main: '#10b981', // emerald-500
      light: '#34d399', // emerald-400
      dark: '#059669', // emerald-600
    },
    warning: {
      main: '#f59e0b', // amber-500
      light: '#fbbf24', // amber-400
      dark: '#d97706', // amber-600
    },
    error: {
      main: '#ef4444', // red-500
      light: '#f87171', // red-400
      dark: '#dc2626', // red-600
    },
    info: {
      main: '#3b82f6', // blue-500
      light: '#60a5fa', // blue-400
      dark: '#2563eb', // blue-600
    },
    background: {
      default: isDark ? '#0a0e17' : '#ffffff',
      paper: isDark ? '#0f1419' : '#f8fafc',
    },
    text: {
      primary: isDark ? '#f8fafc' : '#0f172a',
      secondary: isDark ? '#94a3b8' : '#64748b',
      disabled: isDark ? '#64748b' : '#94a3b8',
    },
    divider: isDark ? 'rgba(148, 163, 184, 0.12)' : 'rgba(15, 23, 42, 0.12)',
  },
  transitions: {
    duration: {
      shortest: 150,
      shorter: 200,
      short: 250,
      standard: 300,
      complex: 375,
      enteringScreen: 225,
      leavingScreen: 195,
    },
    easing: {
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      sharp: 'cubic-bezier(0.4, 0, 0.6, 1)',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 700,
      lineHeight: 1.3,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.5,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
      lineHeight: 1.5,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.43,
    },
    button: {
      textTransform: 'none',
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          background: isDark
            ? 'linear-gradient(to bottom right, #0a0e17 0%, #0f1419 50%, #0a0e17 100%)'
            : 'linear-gradient(to bottom right, #ffffff 0%, #f8fafc 50%, #ffffff 100%)',
          backgroundAttachment: 'fixed',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          padding: '10px 24px',
          fontSize: '0.9375rem',
          fontWeight: 600,
          boxShadow: 'none',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            boxShadow: '0 4px 16px rgba(59, 130, 246, 0.3)',
            transform: 'translateY(-2px)',
          },
          '&:active': {
            transform: 'translateY(0)',
          },
        },
        contained: {
          background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%)',
            boxShadow: '0 8px 24px rgba(59, 130, 246, 0.4)',
          },
        },
        containedPrimary: {
          background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          backgroundImage: isDark
            ? 'linear-gradient(135deg, rgba(15, 20, 25, 0.6) 0%, rgba(15, 20, 25, 0.8) 100%)'
            : 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.95) 100%)',
          backdropFilter: 'blur(10px)',
          border: isDark ? '1px solid rgba(148, 163, 184, 0.1)' : '1px solid rgba(15, 23, 42, 0.1)',
          boxShadow: isDark ? '0 4px 24px rgba(0, 0, 0, 0.12)' : '0 4px 24px rgba(0, 0, 0, 0.05)',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            boxShadow: isDark ? '0 8px 32px rgba(0, 0, 0, 0.16)' : '0 8px 32px rgba(0, 0, 0, 0.08)',
            transform: 'translateY(-4px)',
            border: isDark ? '1px solid rgba(148, 163, 184, 0.15)' : '1px solid rgba(15, 23, 42, 0.15)',
          },
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'scale(1.1)',
            background: 'rgba(59, 130, 246, 0.1)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          backgroundImage: isDark
            ? 'linear-gradient(135deg, rgba(15, 20, 25, 0.6) 0%, rgba(15, 20, 25, 0.8) 100%)'
            : 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.95) 100%)',
          backdropFilter: 'blur(10px)',
          border: isDark ? '1px solid rgba(148, 163, 184, 0.1)' : '1px solid rgba(15, 23, 42, 0.1)',
        },
        elevation1: {
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.12)',
        },
        elevation2: {
          boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)',
        },
        elevation3: {
          boxShadow: '0 12px 32px rgba(0, 0, 0, 0.18)',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 600,
          backdropFilter: 'blur(10px)',
        },
        filled: {
          backgroundImage: 'linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%)',
          border: '1px solid rgba(59, 130, 246, 0.3)',
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        head: {
          fontWeight: 700,
          backgroundColor: 'rgba(15, 20, 25, 0.5)',
          borderBottom: '1px solid rgba(148, 163, 184, 0.12)',
        },
        root: {
          borderBottom: '1px solid rgba(148, 163, 184, 0.08)',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundImage: isDark
            ? 'linear-gradient(to bottom, #0f1419 0%, #0a0e17 100%)'
            : 'linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%)',
          borderRight: isDark ? '1px solid rgba(148, 163, 184, 0.1)' : '1px solid rgba(15, 23, 42, 0.1)',
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            backgroundColor: isDark ? 'rgba(148, 163, 184, 0.08)' : 'rgba(59, 130, 246, 0.08)',
          },
          '&.Mui-selected': {
            backgroundImage: 'linear-gradient(to right, #3b82f6, #2563eb)',
            boxShadow: '0 4px 16px rgba(59, 130, 246, 0.3)',
            color: '#ffffff',
            '&:hover': {
              backgroundImage: 'linear-gradient(to right, #60a5fa, #3b82f6)',
            },
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundImage: 'linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%)',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
        },
      },
    },
  },
  };

  return createTheme(themeOptions);
};

// Default dark theme export for backward compatibility
export const theme = createAppTheme('dark');
