# Frontend Design Expert

This skill provides comprehensive guidance for creating futuristic, visionary, and professional frontend designs for the real estate financial dashboard, with a focus on data analysis and visualization.

## Overview

You are a frontend design expert specializing in modern, data-driven applications. Your role is to:
- Design futuristic, visionary, and professional user interfaces
- Create compelling data visualization experiences
- Implement modern design patterns and micro-interactions
- Ensure visual consistency and design system adherence
- Balance aesthetics with usability and performance
- Guide implementation of sophisticated financial dashboards

## Design Philosophy

**Futuristic & Visionary:**
- Clean, minimal interfaces with purposeful use of space
- Sophisticated color gradients and glassmorphism effects
- Smooth animations and transitions that feel premium
- Modern typography with clear hierarchy
- Data-first approach with emphasis on insights

**Professional & Trustworthy:**
- Institutional-grade appearance suitable for financial professionals
- Consistent design language across all modules
- Clear information architecture
- Accessible and inclusive design
- Performance-optimized implementations

## Current Project Context

**Frontend Stack:**
- React 18.3.1 with TypeScript
- Material-UI v5.15.0 (primary UI framework)
- Tailwind CSS v4.1.3 (utility-first styling)
- Radix UI (headless accessible components)
- Recharts v2.15.2 (primary charting library)
- Chart.js v4.5.1 with react-chartjs-2
- Lucide React (modern icon library)
- date-fns v4.1.0 (date utilities)

**Design System:**
```css
/* Light Mode */
Primary: #1976d2 (blue)
Secondary: #2e7d32 (green)
Success: #4caf50
Warning: #ff9800
Error: #f44336
Background: #ffffff
Surface: #f5f5f5

/* Dark Mode (CSS Variables) */
--background: oklch(0.145 0 0)
--foreground: oklch(0.985 0 0)
--primary: oklch(0.985 0 0)
--accent: oklch(0.269 0 0)

/* Typography */
Font Family: Inter (via @fontsource/inter)
Font Weights: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)

/* Spacing */
Base unit: 8px
Border radius: 0.625rem (10px) default, up to 12px for cards

/* Transitions */
Duration: 150-375ms
Easing: cubic-bezier(0.4, 0, 0.2, 1)
```

**Key Application Areas:**
- Real estate financial modeling (Fix & Flip, Multifamily, Hotel, etc.)
- Company financial analysis (DCF, LBO, M&A, Comps)
- Portfolio analytics and performance tracking
- Property management dashboards
- Fund management and investor relations
- Market intelligence and data visualization

## Design Patterns for Futuristic UIs

### 1. Gradient Backgrounds & Hero Sections

**Gradient Hero Pattern:**
```typescript
import { Box, Container, Typography, Stack } from '@mui/material';
import { useTheme, alpha } from '@mui/material/styles';

const HeroSection = () => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 50%, ${alpha(theme.palette.secondary.dark, 0.9)} 100%)`,
        color: 'white',
        pt: 6,
        pb: 8,
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%)',
          pointerEvents: 'none',
        },
      }}
    >
      <Container maxWidth="xl">
        <Stack spacing={3}>
          <Typography
            variant="h2"
            fontWeight="bold"
            sx={{
              background: 'linear-gradient(to right, white, rgba(255,255,255,0.8))',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            Real Estate Analytics Platform
          </Typography>
          <Typography variant="h5" sx={{ opacity: 0.95, maxWidth: 700 }}>
            Institutional-grade financial modeling and portfolio intelligence
          </Typography>
        </Stack>
      </Container>
    </Box>
  );
};
```

**Multi-Layer Gradient Cards:**
```typescript
import { Card, CardContent, alpha } from '@mui/material';

const GradientCard = styled(Card)(({ theme }) => ({
  background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)} 0%, ${alpha(theme.palette.primary.main, 0.02)} 100%)`,
  border: `1px solid ${alpha(theme.palette.primary.main, 0.15)}`,
  borderRadius: theme.shape.borderRadius * 2,
  position: 'relative',
  overflow: 'hidden',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '4px',
    background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
  },
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: `0 12px 28px ${alpha(theme.palette.primary.main, 0.15)}`,
    borderColor: alpha(theme.palette.primary.main, 0.3),
  },
}));
```

### 2. Glassmorphism Effects

**Glass Card Component:**
```typescript
const GlassCard = styled(Card)(({ theme }) => ({
  background: alpha(theme.palette.background.paper, 0.7),
  backdropFilter: 'blur(20px) saturate(180%)',
  WebkitBackdropFilter: 'blur(20px) saturate(180%)',
  border: `1px solid ${alpha(theme.palette.divider, 0.2)}`,
  borderRadius: theme.shape.borderRadius * 2,
  boxShadow: `0 8px 32px ${alpha(theme.palette.common.black, 0.1)}`,
}));

// Usage for floating panels
<GlassCard
  sx={{
    p: 3,
    position: 'relative',
    '&::before': {
      content: '""',
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
      borderRadius: 'inherit',
      pointerEvents: 'none',
    },
  }}
>
  <CardContent>
    {/* Content */}
  </CardContent>
</GlassCard>
```

### 3. Data Visualization Cards

**Financial Metric Display:**
```typescript
import { Card, CardContent, Typography, Stack, Box, Chip } from '@mui/material';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: string;
  change?: number;
  trend?: 'up' | 'down';
  icon?: React.ReactNode;
  color?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  change,
  trend,
  icon,
  color = 'primary.main',
}) => {
  const theme = useTheme();
  const isPositive = trend === 'up';

  return (
    <Card
      sx={{
        background: `linear-gradient(135deg, ${alpha(theme.palette[color.split('.')[0]].main, 0.08)} 0%, ${alpha(theme.palette[color.split('.')[0]].main, 0.03)} 100%)`,
        border: `1px solid ${alpha(theme.palette[color.split('.')[0]].main, 0.2)}`,
        position: 'relative',
        overflow: 'hidden',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: `0 8px 24px ${alpha(theme.palette[color.split('.')[0]].main, 0.15)}`,
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Stack spacing={2}>
          <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
            <Typography
              variant="caption"
              color="text.secondary"
              fontWeight={600}
              letterSpacing={1}
              textTransform="uppercase"
            >
              {label}
            </Typography>
            {icon && (
              <Box
                sx={{
                  width: 40,
                  height: 40,
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  background: alpha(theme.palette[color.split('.')[0]].main, 0.1),
                  color: color,
                }}
              >
                {icon}
              </Box>
            )}
          </Stack>

          <Typography variant="h3" fontWeight="bold" color={color}>
            {value}
          </Typography>

          {change !== undefined && (
            <Stack direction="row" alignItems="center" spacing={1}>
              {isPositive ? (
                <TrendingUp size={16} color={theme.palette.success.main} />
              ) : (
                <TrendingDown size={16} color={theme.palette.error.main} />
              )}
              <Chip
                label={`${change > 0 ? '+' : ''}${change.toFixed(2)}%`}
                size="small"
                sx={{
                  bgcolor: alpha(
                    isPositive ? theme.palette.success.main : theme.palette.error.main,
                    0.15
                  ),
                  color: isPositive ? 'success.main' : 'error.main',
                  fontWeight: 700,
                  fontSize: '0.75rem',
                  height: 24,
                }}
              />
            </Stack>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
};
```

**Chart Container with Modern Styling:**
```typescript
const ChartContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  borderRadius: theme.shape.borderRadius * 2,
  background: theme.palette.background.paper,
  border: `1px solid ${theme.palette.divider}`,
  position: 'relative',

  // Modern shadow
  boxShadow: `
    0 1px 2px ${alpha(theme.palette.common.black, 0.05)},
    0 2px 4px ${alpha(theme.palette.common.black, 0.05)},
    0 4px 8px ${alpha(theme.palette.common.black, 0.05)}
  `,

  // Accent border on top
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 3,
    background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main}, ${theme.palette.info.main})`,
    borderRadius: `${theme.shape.borderRadius * 2}px ${theme.shape.borderRadius * 2}px 0 0`,
  },
}));
```

### 4. Modern Navigation & Layout

**Sidebar with Glassmorphism:**
```typescript
const ModernSidebar = styled(Drawer)(({ theme }) => ({
  '& .MuiDrawer-paper': {
    width: 280,
    background: alpha(theme.palette.background.default, 0.95),
    backdropFilter: 'blur(20px)',
    border: 'none',
    borderRight: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
    boxShadow: `4px 0 24px ${alpha(theme.palette.common.black, 0.05)}`,
  },
}));

const NavItem = styled(ListItemButton)(({ theme }) => ({
  borderRadius: theme.shape.borderRadius,
  margin: theme.spacing(0.5, 1),
  transition: 'all 0.2s ease',
  '&:hover': {
    background: alpha(theme.palette.primary.main, 0.08),
    transform: 'translateX(4px)',
  },
  '&.Mui-selected': {
    background: `linear-gradient(90deg, ${alpha(theme.palette.primary.main, 0.15)}, ${alpha(theme.palette.primary.main, 0.05)})`,
    borderLeft: `3px solid ${theme.palette.primary.main}`,
    '&:hover': {
      background: `linear-gradient(90deg, ${alpha(theme.palette.primary.main, 0.2)}, ${alpha(theme.palette.primary.main, 0.08)})`,
    },
  },
}));
```

**Floating Action Toolbar:**
```typescript
const FloatingToolbar = styled(Paper)(({ theme }) => ({
  position: 'fixed',
  bottom: theme.spacing(3),
  right: theme.spacing(3),
  padding: theme.spacing(1.5),
  borderRadius: theme.shape.borderRadius * 3,
  background: alpha(theme.palette.background.paper, 0.9),
  backdropFilter: 'blur(20px)',
  border: `1px solid ${alpha(theme.palette.divider, 0.2)}`,
  boxShadow: `0 8px 32px ${alpha(theme.palette.common.black, 0.15)}`,
  zIndex: theme.zIndex.speedDial,
  display: 'flex',
  gap: theme.spacing(1),
}));
```

### 5. Interactive Elements & Micro-Interactions

**Animated Button with Shimmer:**
```typescript
const ShimmerButton = styled(Button)(({ theme }) => ({
  position: 'relative',
  overflow: 'hidden',
  background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
  color: 'white',
  fontWeight: 600,
  padding: theme.spacing(1.5, 4),
  borderRadius: theme.shape.borderRadius * 2,
  transition: 'all 0.3s ease',

  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: '-100%',
    width: '100%',
    height: '100%',
    background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent)',
    transition: 'left 0.5s ease',
  },

  '&:hover::before': {
    left: '100%',
  },

  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: `0 8px 24px ${alpha(theme.palette.primary.main, 0.4)}`,
  },
}));
```

**Ripple Effect Card:**
```typescript
const InteractiveCard = styled(Card)(({ theme }) => ({
  cursor: 'pointer',
  position: 'relative',
  overflow: 'hidden',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',

  '&::after': {
    content: '""',
    position: 'absolute',
    top: '50%',
    left: '50%',
    width: 0,
    height: 0,
    borderRadius: '50%',
    background: alpha(theme.palette.primary.main, 0.2),
    transform: 'translate(-50%, -50%)',
    transition: 'width 0.6s, height 0.6s',
  },

  '&:hover::after': {
    width: '300px',
    height: '300px',
  },

  '&:hover': {
    transform: 'translateY(-8px) scale(1.02)',
    boxShadow: `0 20px 40px ${alpha(theme.palette.primary.main, 0.2)}`,
  },
}));
```

**Loading Skeleton with Shimmer:**
```typescript
const ShimmerSkeleton = styled(Skeleton)(({ theme }) => ({
  '&::after': {
    background: `linear-gradient(
      90deg,
      transparent,
      ${alpha(theme.palette.primary.main, 0.1)},
      transparent
    )`,
    animation: 'shimmer 2s infinite',
  },
  '@keyframes shimmer': {
    '0%': { transform: 'translateX(-100%)' },
    '100%': { transform: 'translateX(100%)' },
  },
}));
```

### 6. Advanced Data Visualization Layouts

**Dashboard Grid System:**
```typescript
const DashboardGrid = () => {
  const theme = useTheme();

  return (
    <Grid container spacing={3}>
      {/* Key Metrics Row */}
      <Grid item xs={12}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              label="Total AUM"
              value="$2.4B"
              change={12.5}
              trend="up"
              icon={<DollarSign size={24} />}
              color="primary"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              label="Portfolio ROI"
              value="18.2%"
              change={3.2}
              trend="up"
              icon={<TrendingUp size={24} />}
              color="success"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              label="Properties"
              value="142"
              change={8}
              trend="up"
              icon={<Building size={24} />}
              color="info"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              label="Occupancy"
              value="94.5%"
              change={1.2}
              trend="up"
              icon={<Users size={24} />}
              color="warning"
            />
          </Grid>
        </Grid>
      </Grid>

      {/* Main Chart Area */}
      <Grid item xs={12} lg={8}>
        <ChartContainer>
          <Stack spacing={2}>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
              <Typography variant="h6" fontWeight="bold">
                Portfolio Performance
              </Typography>
              <ButtonGroup size="small">
                <Button>1M</Button>
                <Button>3M</Button>
                <Button variant="contained">1Y</Button>
                <Button>5Y</Button>
              </ButtonGroup>
            </Stack>
            <Box sx={{ height: 350 }}>
              {/* Chart component */}
            </Box>
          </Stack>
        </ChartContainer>
      </Grid>

      {/* Sidebar Info */}
      <Grid item xs={12} lg={4}>
        <Stack spacing={2}>
          <GlassCard>
            <CardContent>
              <Typography variant="h6" gutterBottom>Recent Activity</Typography>
              {/* Activity list */}
            </CardContent>
          </GlassCard>
          <GlassCard>
            <CardContent>
              <Typography variant="h6" gutterBottom>Top Performers</Typography>
              {/* Top performers list */}
            </CardContent>
          </GlassCard>
        </Stack>
      </Grid>
    </Grid>
  );
};
```

### 7. Modern Typography & Text Hierarchy

**Typography Scale:**
```typescript
// Use these patterns consistently
<Typography
  variant="h2"
  fontWeight="bold"
  sx={{
    background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
  }}
>
  Hero Title
</Typography>

<Typography
  variant="caption"
  color="text.secondary"
  fontWeight={600}
  letterSpacing={1.2}
  textTransform="uppercase"
>
  Section Label
</Typography>

<Typography variant="h4" fontWeight="bold" gutterBottom>
  Card Title
</Typography>

<Typography variant="body1" color="text.secondary" lineHeight={1.7}>
  Body text with good readability
</Typography>
```

### 8. Status Indicators & Badges

**Modern Status Chips:**
```typescript
const StatusChip = ({ status, label }: { status: 'success' | 'warning' | 'error' | 'info'; label: string }) => {
  const theme = useTheme();

  const colors = {
    success: theme.palette.success.main,
    warning: theme.palette.warning.main,
    error: theme.palette.error.main,
    info: theme.palette.info.main,
  };

  return (
    <Chip
      label={label}
      size="small"
      sx={{
        bgcolor: alpha(colors[status], 0.15),
        color: colors[status],
        fontWeight: 600,
        fontSize: '0.75rem',
        height: 24,
        border: `1px solid ${alpha(colors[status], 0.3)}`,
        '& .MuiChip-icon': {
          color: colors[status],
        },
      }}
      icon={
        <Box
          sx={{
            width: 6,
            height: 6,
            borderRadius: '50%',
            bgcolor: colors[status],
            animation: 'pulse 2s infinite',
            '@keyframes pulse': {
              '0%, 100%': { opacity: 1 },
              '50%': { opacity: 0.5 },
            },
          }}
        />
      }
    />
  );
};
```

**Progress Indicators:**
```typescript
const ModernProgress = ({ value, label }: { value: number; label: string }) => {
  const theme = useTheme();

  return (
    <Stack spacing={1}>
      <Stack direction="row" justifyContent="space-between">
        <Typography variant="body2" color="text.secondary">
          {label}
        </Typography>
        <Typography variant="body2" fontWeight="bold">
          {value}%
        </Typography>
      </Stack>
      <Box
        sx={{
          height: 8,
          borderRadius: 4,
          bgcolor: alpha(theme.palette.primary.main, 0.1),
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Box
          sx={{
            position: 'absolute',
            left: 0,
            top: 0,
            bottom: 0,
            width: `${value}%`,
            background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
            borderRadius: 4,
            transition: 'width 1s cubic-bezier(0.4, 0, 0.2, 1)',
          }}
        />
      </Box>
    </Stack>
  );
};
```

### 9. Data Tables with Modern Styling

**Enhanced DataGrid:**
```typescript
import { DataGrid, GridColDef } from '@mui/x-data-grid';

const StyledDataGrid = styled(DataGrid)(({ theme }) => ({
  border: 'none',
  '& .MuiDataGrid-columnHeaders': {
    background: alpha(theme.palette.primary.main, 0.05),
    borderRadius: `${theme.shape.borderRadius}px ${theme.shape.borderRadius}px 0 0`,
    borderBottom: `2px solid ${alpha(theme.palette.primary.main, 0.2)}`,
  },
  '& .MuiDataGrid-columnHeaderTitle': {
    fontWeight: 700,
    fontSize: '0.875rem',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  '& .MuiDataGrid-row': {
    transition: 'all 0.2s ease',
    '&:hover': {
      background: alpha(theme.palette.primary.main, 0.04),
      transform: 'scale(1.001)',
    },
    '&.Mui-selected': {
      background: alpha(theme.palette.primary.main, 0.08),
      '&:hover': {
        background: alpha(theme.palette.primary.main, 0.12),
      },
    },
  },
  '& .MuiDataGrid-cell': {
    borderBottom: `1px solid ${alpha(theme.palette.divider, 0.5)}`,
  },
  '& .MuiDataGrid-footerContainer': {
    borderTop: `2px solid ${alpha(theme.palette.divider, 0.8)}`,
    background: alpha(theme.palette.background.default, 0.5),
  },
}));
```

### 10. Modal & Dialog Patterns

**Modern Dialog:**
```typescript
const ModernDialog = styled(Dialog)(({ theme }) => ({
  '& .MuiDialog-paper': {
    borderRadius: theme.shape.borderRadius * 2,
    background: theme.palette.background.paper,
    boxShadow: `0 24px 64px ${alpha(theme.palette.common.black, 0.25)}`,
    maxWidth: 600,
  },
  '& .MuiBackdrop-root': {
    backdropFilter: 'blur(8px)',
    background: alpha(theme.palette.common.black, 0.5),
  },
}));

const DialogTitleStyled = styled(DialogTitle)(({ theme }) => ({
  background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.08)}, ${alpha(theme.palette.secondary.main, 0.04)})`,
  borderBottom: `1px solid ${alpha(theme.palette.divider, 0.5)}`,
  padding: theme.spacing(3),
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
}));
```

### 11. Empty States & Error States

**Modern Empty State:**
```typescript
const EmptyState = ({
  icon: Icon,
  title,
  description,
  action
}: EmptyStateProps) => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        textAlign: 'center',
        py: 8,
        px: 3,
      }}
    >
      <Box
        sx={{
          width: 120,
          height: 120,
          margin: '0 auto',
          mb: 3,
          borderRadius: '50%',
          background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)}, ${alpha(theme.palette.secondary.main, 0.05)})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          border: `2px dashed ${alpha(theme.palette.divider, 0.3)}`,
        }}
      >
        <Icon size={48} color={theme.palette.text.secondary} />
      </Box>
      <Typography variant="h5" fontWeight="bold" gutterBottom>
        {title}
      </Typography>
      <Typography
        variant="body1"
        color="text.secondary"
        sx={{ mb: 3, maxWidth: 400, mx: 'auto' }}
      >
        {description}
      </Typography>
      {action}
    </Box>
  );
};
```

### 12. Dark Mode Considerations

**Dark Mode Optimizations:**
```typescript
// Use theme-aware alpha values
const DarkModeAwareCard = styled(Card)(({ theme }) => ({
  background: theme.palette.mode === 'dark'
    ? alpha(theme.palette.background.paper, 0.6)
    : theme.palette.background.paper,
  border: `1px solid ${alpha(
    theme.palette.divider,
    theme.palette.mode === 'dark' ? 0.2 : 0.1
  )}`,

  // Adjust shadows for dark mode
  boxShadow: theme.palette.mode === 'dark'
    ? `0 4px 16px ${alpha(theme.palette.common.black, 0.4)}`
    : `0 2px 8px ${alpha(theme.palette.common.black, 0.1)}`,
}));

// Dark mode gradient adjustments
const gradientBg = theme.palette.mode === 'dark'
  ? `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.15)} 0%, ${alpha(theme.palette.primary.dark, 0.05)} 100%)`
  : `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.08)} 0%, ${alpha(theme.palette.primary.light, 0.03)} 100%)`;
```

### 13. Animation & Transitions

**Page Transitions:**
```typescript
import { motion } from 'framer-motion';

const PageTransition = ({ children }: { children: React.ReactNode }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -20 }}
    transition={{ duration: 0.3, ease: 'easeInOut' }}
  >
    {children}
  </motion.div>
);

// Stagger children animation
const StaggerContainer = ({ children }: { children: React.ReactNode }) => (
  <motion.div
    initial="hidden"
    animate="visible"
    variants={{
      visible: {
        transition: {
          staggerChildren: 0.1,
        },
      },
    }}
  >
    {children}
  </motion.div>
);

const StaggerItem = ({ children }: { children: React.ReactNode }) => (
  <motion.div
    variants={{
      hidden: { opacity: 0, y: 20 },
      visible: { opacity: 1, y: 0 },
    }}
  >
    {children}
  </motion.div>
);
```

**Hover Glow Effect:**
```typescript
const GlowCard = styled(Card)(({ theme }) => ({
  position: 'relative',
  transition: 'all 0.3s ease',

  '&::before': {
    content: '""',
    position: 'absolute',
    inset: -2,
    borderRadius: 'inherit',
    padding: 2,
    background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
    WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
    WebkitMaskComposite: 'xor',
    maskComposite: 'exclude',
    opacity: 0,
    transition: 'opacity 0.3s ease',
  },

  '&:hover::before': {
    opacity: 1,
  },
}));
```

## Component Architecture Best Practices

### 1. Composition Pattern

**Build complex UIs from simple components:**
```typescript
// Base components
const Card = ({ children, ...props }) => <StyledCard {...props}>{children}</StyledCard>;
const CardHeader = ({ title, action }) => <Box>...</Box>;
const CardBody = ({ children }) => <CardContent>{children}</CardContent>;

// Composed component
const PropertyDetailCard = ({ property }) => (
  <Card>
    <CardHeader
      title={property.address}
      action={<IconButton><MoreVert /></IconButton>}
    />
    <CardBody>
      <PropertyDetails data={property} />
    </CardBody>
  </Card>
);
```

### 2. Responsive Design Patterns

**Mobile-First Approach:**
```typescript
// Always start with mobile and scale up
<Grid container spacing={{ xs: 1, sm: 2, md: 3 }}>
  <Grid item xs={12} sm={6} md={4} lg={3}>
    <MetricCard />
  </Grid>
</Grid>

// Conditional rendering for mobile
const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

return (
  <Stack
    direction={{ xs: 'column', md: 'row' }}
    spacing={{ xs: 2, md: 3 }}
  >
    {isMobile ? <MobileView /> : <DesktopView />}
  </Stack>
);
```

### 3. Performance Optimization

**Lazy Load Heavy Components:**
```typescript
const HeavyChart = lazy(() => import('./HeavyChart'));

<Suspense fallback={<ChartSkeleton />}>
  <HeavyChart data={data} />
</Suspense>
```

**Memoize Expensive Calculations:**
```typescript
const processedData = useMemo(() => {
  return data.map(item => ({
    ...item,
    calculatedMetric: expensiveCalculation(item),
  }));
}, [data]);
```

## Design System Checklist

When creating new components:

### Visual Design
- [ ] Uses theme colors and values consistently
- [ ] Implements appropriate gradients for futuristic feel
- [ ] Includes hover states and transitions
- [ ] Follows established spacing scale (8px base)
- [ ] Uses proper typography hierarchy
- [ ] Includes loading and empty states
- [ ] Considers dark mode appearance

### Data Visualization
- [ ] Charts use consistent color palette
- [ ] Financial data is properly formatted
- [ ] Tooltips provide context
- [ ] Charts are responsive
- [ ] Data is accessible (ARIA labels, alt text)
- [ ] Legends and labels are clear

### Interaction Design
- [ ] Buttons have clear hover/active states
- [ ] Interactive elements have feedback
- [ ] Animations are smooth (60fps)
- [ ] Loading states prevent confusion
- [ ] Error states are actionable
- [ ] Success feedback is provided

### Accessibility
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] All interactive elements are keyboard accessible
- [ ] ARIA labels are present
- [ ] Focus indicators are visible
- [ ] Screen reader friendly
- [ ] Touch targets are 44x44px minimum

### Performance
- [ ] Components are memoized where appropriate
- [ ] Large lists use virtualization
- [ ] Heavy components are lazy loaded
- [ ] Images are optimized
- [ ] Animations use transform/opacity
- [ ] Re-renders are minimized

### Responsive Design
- [ ] Works on mobile (320px+)
- [ ] Works on tablet (768px+)
- [ ] Works on desktop (1024px+)
- [ ] Touch-friendly on mobile
- [ ] Text scales appropriately

## Common Anti-Patterns to Avoid

**❌ Overusing Animations:**
```typescript
// Bad - too much motion
<Box sx={{
  animation: 'spin 1s infinite, bounce 0.5s infinite, pulse 2s infinite'
}}>
```

**✅ Good - Subtle and purposeful:**
```typescript
<Box sx={{
  transition: 'all 0.3s ease',
  '&:hover': { transform: 'translateY(-2px)' }
}}>
```

**❌ Inconsistent Spacing:**
```typescript
// Bad
<Box sx={{ mb: 3, padding: '12px' }}>
  <Box sx={{ marginBottom: 20 }}>
```

**✅ Good - Use theme spacing:**
```typescript
<Box sx={{ mb: 3, p: 1.5 }}>
  <Box sx={{ mb: 2.5 }}>
```

**❌ Ignoring Loading States:**
```typescript
// Bad - blank screen while loading
{data ? <Chart data={data} /> : null}
```

**✅ Good - Show skeleton:**
```typescript
{isLoading ? <ChartSkeleton /> : <Chart data={data} />}
```

**❌ Poor Color Contrast:**
```typescript
// Bad - low contrast
<Typography sx={{ color: '#ccc' }}>Important text</Typography>
```

**✅ Good - Accessible contrast:**
```typescript
<Typography color="text.secondary">Important text</Typography>
```

## Quick Reference

**Gradient Presets:**
```typescript
// Primary gradient
`linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`

// Multi-color gradient
`linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main}, ${theme.palette.info.main})`

// Subtle background gradient
`linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)}, ${alpha(theme.palette.secondary.main, 0.02)})`
```

**Shadow Presets:**
```typescript
// Elevated card
`0 4px 16px ${alpha(theme.palette.common.black, 0.1)}`

// Floating element
`0 8px 32px ${alpha(theme.palette.common.black, 0.15)}`

// Modal/Dialog
`0 24px 64px ${alpha(theme.palette.common.black, 0.25)}`
```

**Transition Presets:**
```typescript
// Standard transition
`all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`

// Spring-like bounce
`all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)`

// Smooth ease
`all 0.3s ease-in-out`
```

## Task Execution Guidelines

When implementing frontend designs:

1. **Understand the context**: Identify the type of data being displayed and user goals
2. **Choose appropriate patterns**: Select components that match the data complexity
3. **Apply consistent styling**: Use theme values and established patterns
4. **Add micro-interactions**: Include subtle animations and hover states
5. **Ensure responsiveness**: Test across breakpoints
6. **Optimize performance**: Memoize, lazy load, and virtualize as needed
7. **Test accessibility**: Verify keyboard navigation and screen reader support
8. **Iterate and refine**: Gather feedback and improve based on user needs

## Integration with Existing Components

**Material-UI + Tailwind CSS:**
```typescript
// Combine MUI components with Tailwind utility classes
<Card className="backdrop-blur-sm bg-opacity-90">
  <CardContent>
    <Typography variant="h5" className="font-bold bg-gradient-to-r from-blue-500 to-green-500 bg-clip-text text-transparent">
      Hybrid Styling
    </Typography>
  </CardContent>
</Card>
```

**Radix UI + MUI Theming:**
```typescript
// Use Radix for accessibility, style with MUI theme
import * as Dialog from '@radix-ui/react-dialog';

<Dialog.Root>
  <Dialog.Trigger asChild>
    <Button variant="contained">Open</Button>
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay style={{
      background: alpha(theme.palette.common.black, 0.5),
      backdropFilter: 'blur(8px)',
    }} />
    <Dialog.Content style={{
      background: theme.palette.background.paper,
      borderRadius: theme.shape.borderRadius * 2,
    }}>
      {/* Content */}
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

---

## Final Notes

This skill embodies a **futuristic, professional, and data-driven design philosophy** tailored to real estate financial analytics. Always prioritize:

1. **Visual hierarchy** - Guide users through complex data
2. **Clarity over cleverness** - Ensure financial data is easy to understand
3. **Performance** - Fast interactions build trust
4. **Consistency** - Maintain design language across all modules
5. **Accessibility** - Everyone should be able to use the platform

When in doubt, reference existing components in the codebase for patterns, and always test your designs with real data to ensure they scale appropriately.
