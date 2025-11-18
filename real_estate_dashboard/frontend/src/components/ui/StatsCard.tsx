import { ReactNode } from 'react';
import { LucideIcon } from 'lucide-react';
import { AreaChart, Area, ResponsiveContainer } from 'recharts';
import { useAppTheme } from '../../contexts/ThemeContext';
import { AnimatedCounter } from './AnimatedCounter';
import { GradientCard } from './GradientCard';

interface StatsCardProps {
  label: string;
  value: number | string;
  icon?: LucideIcon;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  subtitle?: string;
  sparklineData?: Array<{ value: number }>;
  gradient?: 'blue' | 'purple' | 'green' | 'emerald' | 'orange' | 'red' | 'cyan' | 'amber';
  animated?: boolean;
  prefix?: string;
  suffix?: string;
  decimals?: number;
}

export function StatsCard({
  label,
  value,
  icon: Icon,
  trend,
  trendValue,
  subtitle,
  sparklineData,
  gradient = 'blue',
  animated = true,
  prefix = '',
  suffix = '',
  decimals = 0
}: StatsCardProps) {
  const { theme } = useAppTheme();
  const currentTheme = theme || 'dark'; // Default to dark if theme is undefined

  const isNumericValue = typeof value === 'number';

  const trendColors = {
    up: currentTheme === 'dark' ? 'text-green-400' : 'text-green-700',
    down: currentTheme === 'dark' ? 'text-red-400' : 'text-red-700',
    neutral: currentTheme === 'dark' ? 'text-slate-400' : 'text-slate-600'
  };

  const iconColors = {
    blue: currentTheme === 'dark' ? 'text-blue-400' : 'text-blue-600',
    purple: currentTheme === 'dark' ? 'text-purple-400' : 'text-purple-600',
    green: currentTheme === 'dark' ? 'text-green-400' : 'text-green-600',
    emerald: currentTheme === 'dark' ? 'text-emerald-400' : 'text-emerald-600',
    orange: currentTheme === 'dark' ? 'text-orange-400' : 'text-orange-600',
    red: currentTheme === 'dark' ? 'text-red-400' : 'text-red-600',
    cyan: currentTheme === 'dark' ? 'text-cyan-400' : 'text-cyan-600',
    amber: currentTheme === 'dark' ? 'text-amber-400' : 'text-amber-600'
  };

  return (
    <GradientCard gradient={gradient} className="p-6">
      <div className="flex items-start justify-between mb-4">
        {Icon && (
          <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${
            currentTheme === 'dark'
              ? `from-${gradient}-500/20 to-${gradient}-600/10 border border-${gradient}-500/30`
              : `from-${gradient}-100 to-${gradient}-50 border border-${gradient}-200`
          } flex items-center justify-center`}>
            <Icon className={`w-6 h-6 ${iconColors[gradient]}`} />
          </div>
        )}
        {trend && trendValue && (
          <span className={`text-sm font-medium ${trendColors[trend]}`}>
            {trend === 'up' && '↑'} {trend === 'down' && '↓'} {trendValue}
          </span>
        )}
      </div>

      <div className={`text-sm font-medium mb-2 ${currentTheme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
        {label}
      </div>

      <div className={`text-3xl font-bold mb-1 ${currentTheme === 'dark' ? 'text-white' : 'text-slate-900'}`}>
        {animated && isNumericValue ? (
          <AnimatedCounter
            end={value as number}
            prefix={prefix}
            suffix={suffix}
            decimals={decimals}
          />
        ) : (
          `${prefix}${value}${suffix}`
        )}
      </div>

      {subtitle && (
        <div className={`text-xs ${currentTheme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>
          {subtitle}
        </div>
      )}

      {sparklineData && sparklineData.length > 0 && (
        <div className="mt-4 -mb-2">
          <ResponsiveContainer width="100%" height={40}>
            <AreaChart data={sparklineData}>
              <defs>
                <linearGradient id={`gradient-${gradient}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={gradient === 'blue' ? '#3b82f6' : gradient === 'green' ? '#10b981' : '#8b5cf6'} stopOpacity={0.3} />
                  <stop offset="95%" stopColor={gradient === 'blue' ? '#3b82f6' : gradient === 'green' ? '#10b981' : '#8b5cf6'} stopOpacity={0} />
                </linearGradient>
              </defs>
              <Area
                type="monotone"
                dataKey="value"
                stroke={gradient === 'blue' ? '#3b82f6' : gradient === 'green' ? '#10b981' : '#8b5cf6'}
                strokeWidth={2}
                fill={`url(#gradient-${gradient})`}
                isAnimationActive={true}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </GradientCard>
  );
}
