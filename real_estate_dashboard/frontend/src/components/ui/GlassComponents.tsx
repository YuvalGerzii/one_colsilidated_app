import React from 'react';
import { Card, Paper, Box, Button, styled, alpha } from '@mui/material';
import { motion } from 'framer-motion';

/**
 * Glassmorphism Design System Components
 * Based on advanced-ui-design skill specifications
 */

// Glass Card with blur effect and subtle borders
export const GlassCard = styled(Card)(({ theme }) => ({
  background: alpha(theme.palette.background.paper, 0.7),
  backdropFilter: 'blur(20px)',
  WebkitBackdropFilter: 'blur(20px)',
  border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
  boxShadow: `0 8px 32px 0 ${alpha(theme.palette.common.black, 0.1)}`,
  borderRadius: 16,
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',

  '&:hover': {
    background: alpha(theme.palette.background.paper, 0.8),
    boxShadow: `0 12px 48px 0 ${alpha(theme.palette.common.black, 0.15)}`,
    transform: 'translateY(-2px)',
    border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
  },
}));

// Animated Glass Card with Framer Motion
export const AnimatedGlassCard = motion.create(GlassCard);

// Glass metric card for dashboard KPIs
export const GlassMetricCard = styled(Card)(({ theme }) => ({
  background: `linear-gradient(135deg, ${alpha(theme.palette.background.paper, 0.8)}, ${alpha(theme.palette.background.paper, 0.6)})`,
  backdropFilter: 'blur(20px)',
  WebkitBackdropFilter: 'blur(20px)',
  border: `1px solid ${alpha(theme.palette.divider, 0.15)}`,
  boxShadow: `0 8px 32px 0 ${alpha(theme.palette.common.black, 0.12)}`,
  borderRadius: 20,
  padding: theme.spacing(3),
  position: 'relative',
  overflow: 'hidden',
  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',

  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '3px',
    background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
    opacity: 0,
    transition: 'opacity 0.3s ease',
  },

  '&:hover': {
    background: `linear-gradient(135deg, ${alpha(theme.palette.background.paper, 0.9)}, ${alpha(theme.palette.background.paper, 0.7)})`,
    boxShadow: `0 16px 64px 0 ${alpha(theme.palette.common.black, 0.2)}`,
    transform: 'translateY(-4px) scale(1.02)',
    border: `1px solid ${alpha(theme.palette.primary.main, 0.3)}`,

    '&::before': {
      opacity: 1,
    },
  },
}));

// Glass Paper for content sections
export const GlassPaper = styled(Paper)(({ theme }) => ({
  background: alpha(theme.palette.background.paper, 0.6),
  backdropFilter: 'blur(15px)',
  WebkitBackdropFilter: 'blur(15px)',
  border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
  boxShadow: `0 4px 24px 0 ${alpha(theme.palette.common.black, 0.08)}`,
  borderRadius: 12,
  transition: 'all 0.3s ease',
}));

// Glass Button with hover effects
export const GlassButton = styled(Button)(({ theme }) => ({
  background: alpha(theme.palette.primary.main, 0.1),
  backdropFilter: 'blur(10px)',
  WebkitBackdropFilter: 'blur(10px)',
  border: `1px solid ${alpha(theme.palette.primary.main, 0.3)}`,
  borderRadius: 12,
  padding: '10px 24px',
  fontWeight: 600,
  textTransform: 'none',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',

  '&:hover': {
    background: alpha(theme.palette.primary.main, 0.2),
    border: `1px solid ${alpha(theme.palette.primary.main, 0.5)}`,
    transform: 'translateY(-2px)',
    boxShadow: `0 8px 24px ${alpha(theme.palette.primary.main, 0.3)}`,
  },

  '&:active': {
    transform: 'translateY(0)',
  },
}));

// Neumorphic Card (soft UI)
export const NeumorphicCard = styled(Card)(({ theme }) => ({
  background: theme.palette.background.paper,
  borderRadius: 20,
  padding: theme.spacing(3),
  boxShadow: theme.palette.mode === 'light'
    ? `12px 12px 24px ${alpha(theme.palette.common.black, 0.1)}, -12px -12px 24px ${alpha(theme.palette.common.white, 0.8)}`
    : `12px 12px 24px ${alpha(theme.palette.common.black, 0.3)}, -12px -12px 24px ${alpha(theme.palette.common.white, 0.05)}`,
  transition: 'all 0.3s ease',
  border: 'none',

  '&:hover': {
    boxShadow: theme.palette.mode === 'light'
      ? `8px 8px 16px ${alpha(theme.palette.common.black, 0.12)}, -8px -8px 16px ${alpha(theme.palette.common.white, 0.9)}`
      : `8px 8px 16px ${alpha(theme.palette.common.black, 0.4)}, -8px -8px 16px ${alpha(theme.palette.common.white, 0.08)}`,
  },
}));

// Glass Container for page layouts
export const GlassContainer = styled(Box)(({ theme }) => ({
  background: alpha(theme.palette.background.default, 0.5),
  backdropFilter: 'blur(10px)',
  WebkitBackdropFilter: 'blur(10px)',
  borderRadius: 16,
  padding: theme.spacing(3),
  border: `1px solid ${alpha(theme.palette.divider, 0.08)}`,
}));

// Glass sidebar/navigation panel
export const GlassPanel = styled(Box)(({ theme }) => ({
  background: `linear-gradient(135deg, ${alpha(theme.palette.background.paper, 0.8)}, ${alpha(theme.palette.background.paper, 0.6)})`,
  backdropFilter: 'blur(30px)',
  WebkitBackdropFilter: 'blur(30px)',
  border: `1px solid ${alpha(theme.palette.divider, 0.12)}`,
  boxShadow: `0 8px 32px 0 ${alpha(theme.palette.common.black, 0.15)}`,
  borderRadius: 16,
  overflow: 'hidden',
}));

// Floating Action Glass Button
export const FloatingGlassButton = styled(Button)(({ theme }) => ({
  position: 'fixed',
  bottom: 32,
  right: 32,
  background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.9)}, ${alpha(theme.palette.secondary.main, 0.9)})`,
  backdropFilter: 'blur(10px)',
  WebkitBackdropFilter: 'blur(10px)',
  border: `1px solid ${alpha(theme.palette.common.white, 0.2)}`,
  borderRadius: '50%',
  width: 64,
  height: 64,
  minWidth: 64,
  boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.4)}`,
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',

  '&:hover': {
    background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
    transform: 'scale(1.1) translateY(-4px)',
    boxShadow: `0 12px 48px ${alpha(theme.palette.primary.main, 0.5)}`,
  },

  '&:active': {
    transform: 'scale(1.05) translateY(-2px)',
  },
}));

// Micro-interaction wrapper
interface MicroInteractionProps {
  children: React.ReactNode;
  variant?: 'scale' | 'lift' | 'glow' | 'pulse';
}

export const MicroInteraction: React.FC<MicroInteractionProps> = ({
  children,
  variant = 'scale'
}) => {
  const variants = {
    scale: {
      whileHover: { scale: 1.05 },
      whileTap: { scale: 0.95 },
      transition: { type: 'spring', stiffness: 400, damping: 17 }
    },
    lift: {
      whileHover: { y: -8, transition: { duration: 0.2 } },
      whileTap: { y: 0 },
    },
    glow: {
      whileHover: {
        boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)',
        transition: { duration: 0.3 }
      },
    },
    pulse: {
      animate: {
        scale: [1, 1.02, 1],
        transition: { duration: 2, repeat: Infinity }
      },
    },
  };

  return (
    <motion.div {...variants[variant]}>
      {children}
    </motion.div>
  );
};

// Shimmer loading effect for glass components
export const GlassShimmer = styled(Box)(({ theme }) => ({
  background: `linear-gradient(90deg,
    ${alpha(theme.palette.background.paper, 0.6)} 0%,
    ${alpha(theme.palette.background.paper, 0.8)} 50%,
    ${alpha(theme.palette.background.paper, 0.6)} 100%
  )`,
  backgroundSize: '200% 100%',
  animation: 'shimmer 2s infinite',
  borderRadius: 12,

  '@keyframes shimmer': {
    '0%': {
      backgroundPosition: '200% 0',
    },
    '100%': {
      backgroundPosition: '-200% 0',
    },
  },
}));

// Glass Badge for notifications/status
export const GlassBadge = styled(Box)(({ theme }) => ({
  background: alpha(theme.palette.error.main, 0.15),
  backdropFilter: 'blur(8px)',
  WebkitBackdropFilter: 'blur(8px)',
  border: `1px solid ${alpha(theme.palette.error.main, 0.3)}`,
  borderRadius: 12,
  padding: '4px 12px',
  fontSize: '0.75rem',
  fontWeight: 600,
  color: theme.palette.error.main,
  display: 'inline-block',
  transition: 'all 0.2s ease',

  '&:hover': {
    background: alpha(theme.palette.error.main, 0.25),
    transform: 'scale(1.05)',
  },
}));

// Gradient Glass Card (premium variant)
export const GradientGlassCard = styled(Card)(({ theme }) => ({
  background: `linear-gradient(135deg,
    ${alpha(theme.palette.primary.main, 0.1)},
    ${alpha(theme.palette.secondary.main, 0.1)}
  )`,
  backdropFilter: 'blur(20px)',
  WebkitBackdropFilter: 'blur(20px)',
  border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
  boxShadow: `0 8px 32px 0 ${alpha(theme.palette.primary.main, 0.15)}`,
  borderRadius: 20,
  position: 'relative',
  overflow: 'hidden',
  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',

  '&::after': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: `linear-gradient(135deg,
      ${alpha(theme.palette.primary.main, 0)},
      ${alpha(theme.palette.secondary.main, 0.1)}
    )`,
    opacity: 0,
    transition: 'opacity 0.3s ease',
    pointerEvents: 'none',
  },

  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: `0 16px 64px 0 ${alpha(theme.palette.primary.main, 0.25)}`,
    border: `1px solid ${alpha(theme.palette.primary.main, 0.4)}`,

    '&::after': {
      opacity: 1,
    },
  },
}));

export default {
  GlassCard,
  AnimatedGlassCard,
  GlassMetricCard,
  GlassPaper,
  GlassButton,
  NeumorphicCard,
  GlassContainer,
  GlassPanel,
  FloatingGlassButton,
  MicroInteraction,
  GlassShimmer,
  GlassBadge,
  GradientGlassCard,
};
