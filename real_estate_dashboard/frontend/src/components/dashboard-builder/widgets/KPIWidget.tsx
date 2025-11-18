import { TrendingUp, TrendingDown } from 'lucide-react';
import { Widget } from '../../../types/dashboard';
import { useTheme } from '../../../contexts/ThemeContext';

interface KPIWidgetProps {
  widget: Widget;
  data?: {
    value: string | number;
    change: number;
    label: string;
    subtitle?: string;
  };
}

export function KPIWidget({ widget, data }: KPIWidgetProps) {
  const { theme } = useTheme();
  const colorScheme = widget.config.colorScheme;

  // Sample data if not provided
  const displayData = data || {
    value: '$2.4M',
    change: 12.5,
    label: widget.config.title,
    subtitle: 'vs last month',
  };

  const isPositive = displayData.change >= 0;
  const backgroundColor = colorScheme?.background || (theme === 'dark' ? 'bg-slate-800/50' : 'bg-white');
  const primaryColor = colorScheme?.primary || (theme === 'dark' ? 'text-blue-400' : 'text-blue-600');
  const textColor = colorScheme?.text || (theme === 'dark' ? 'text-slate-200' : 'text-slate-800');

  return (
    <div className={`h-full ${backgroundColor} rounded-xl border ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-200'} p-6 relative overflow-hidden group hover:shadow-lg transition-all`}>
      {/* Background decoration */}
      {colorScheme?.gradient && (
        <div
          className="absolute inset-0 opacity-5"
          style={{
            background: `linear-gradient(135deg, ${colorScheme.gradient.from}, ${colorScheme.gradient.to})`,
          }}
        />
      )}

      <div className="relative z-10">
        <div className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'} mb-2`}>
          {displayData.label}
        </div>
        <div className={`text-3xl font-bold ${primaryColor} mb-2`}>
          {displayData.value}
        </div>
        <div className="flex items-center gap-2">
          <div className={`flex items-center gap-1 px-2 py-1 rounded-md ${
            isPositive
              ? theme === 'dark' ? 'bg-green-500/10 text-green-400' : 'bg-green-100 text-green-700'
              : theme === 'dark' ? 'bg-red-500/10 text-red-400' : 'bg-red-100 text-red-700'
          }`}>
            {isPositive ? (
              <TrendingUp className="w-3 h-3" />
            ) : (
              <TrendingDown className="w-3 h-3" />
            )}
            <span className="text-xs font-medium">
              {Math.abs(displayData.change)}%
            </span>
          </div>
          {displayData.subtitle && (
            <span className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>
              {displayData.subtitle}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
