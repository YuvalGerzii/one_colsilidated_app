import { ReactNode } from 'react';
import { useAppTheme } from '../../contexts/ThemeContext';

interface GradientCardProps {
  children: ReactNode;
  className?: string;
  gradient?: 'blue' | 'purple' | 'green' | 'emerald' | 'orange' | 'red' | 'cyan' | 'amber';
  onClick?: () => void;
  hoverable?: boolean;
}

const gradients = {
  blue: {
    dark: 'from-blue-600/10 to-transparent',
    light: 'from-blue-100/50 to-transparent'
  },
  purple: {
    dark: 'from-purple-600/10 to-transparent',
    light: 'from-purple-100/50 to-transparent'
  },
  green: {
    dark: 'from-green-600/10 to-transparent',
    light: 'from-green-100/50 to-transparent'
  },
  emerald: {
    dark: 'from-emerald-600/10 to-transparent',
    light: 'from-emerald-100/50 to-transparent'
  },
  orange: {
    dark: 'from-orange-600/10 to-transparent',
    light: 'from-orange-100/50 to-transparent'
  },
  red: {
    dark: 'from-red-600/10 to-transparent',
    light: 'from-red-100/50 to-transparent'
  },
  cyan: {
    dark: 'from-cyan-600/10 to-transparent',
    light: 'from-cyan-100/50 to-transparent'
  },
  amber: {
    dark: 'from-amber-600/10 to-transparent',
    light: 'from-amber-100/50 to-transparent'
  }
};

export function GradientCard({
  children,
  className = '',
  gradient = 'blue',
  onClick,
  hoverable = true
}: GradientCardProps) {
  const { theme } = useAppTheme();
  const currentTheme = theme || 'dark'; // Default to dark if theme is undefined

  const baseClasses = currentTheme === 'dark'
    ? 'bg-slate-900/40 border-slate-700/50 backdrop-blur-xl'
    : 'bg-white/60 border-slate-200 backdrop-blur-sm shadow-lg';

  const hoverClasses = hoverable
    ? currentTheme === 'dark'
      ? 'hover:border-slate-600/60 hover:shadow-xl'
      : 'hover:border-slate-300 hover:shadow-2xl'
    : '';

  const cursorClass = onClick ? 'cursor-pointer' : '';

  return (
    <div
      onClick={onClick}
      className={`relative overflow-hidden rounded-xl border transition-all duration-300 ${baseClasses} ${hoverClasses} ${cursorClass} ${className}`}
    >
      {/* Gradient overlay */}
      <div
        className={`absolute inset-0 bg-gradient-to-br ${
          currentTheme === 'dark' ? gradients[gradient].dark : gradients[gradient].light
        } pointer-events-none`}
      />

      {/* Content */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
}
