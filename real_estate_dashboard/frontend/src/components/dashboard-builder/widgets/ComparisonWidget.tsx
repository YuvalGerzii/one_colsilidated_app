import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { Widget } from '../../../types/dashboard';
import { useTheme } from '../../../contexts/ThemeContext';

interface ComparisonWidgetProps {
  widget: Widget;
  data?: {
    current: number;
    benchmark: number;
    label: string;
    benchmarkLabel: string;
  }[];
}

export function ComparisonWidget({ widget, data }: ComparisonWidgetProps) {
  const { theme } = useTheme();
  const colorScheme = widget.config.colorScheme;

  // Sample data if not provided
  const displayData = data || [
    { current: 94.6, benchmark: 91.2, label: 'Occupancy Rate', benchmarkLabel: 'Market Avg' },
    { current: 6.8, benchmark: 6.2, label: 'Cap Rate', benchmarkLabel: 'Market Avg' },
    { current: 1850, benchmark: 1920, label: 'Cost per SqFt', benchmarkLabel: 'Target' },
    { current: 12.5, benchmark: 11.8, label: 'IRR', benchmarkLabel: 'Target' },
  ];

  const backgroundColor = colorScheme?.background || (theme === 'dark' ? 'bg-slate-800/50' : 'bg-white');

  const getComparisonIndicator = (current: number, benchmark: number) => {
    const diff = ((current - benchmark) / benchmark) * 100;

    if (Math.abs(diff) < 1) {
      return {
        icon: Minus,
        color: theme === 'dark' ? 'text-slate-400' : 'text-slate-500',
        bgColor: theme === 'dark' ? 'bg-slate-700/50' : 'bg-slate-100',
        text: '~',
      };
    }

    if (diff > 0) {
      return {
        icon: TrendingUp,
        color: 'text-green-400',
        bgColor: theme === 'dark' ? 'bg-green-500/10' : 'bg-green-100',
        text: `+${diff.toFixed(1)}%`,
      };
    }

    return {
      icon: TrendingDown,
      color: 'text-red-400',
      bgColor: theme === 'dark' ? 'bg-red-500/10' : 'bg-red-100',
      text: `${diff.toFixed(1)}%`,
    };
  };

  return (
    <div className={`h-full ${backgroundColor} rounded-xl border ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-200'} p-6`}>
      <h3 className={`text-lg font-semibold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'} mb-6`}>
        {widget.config.title}
      </h3>

      <div className="space-y-4">
        {displayData.map((item, index) => {
          const indicator = getComparisonIndicator(item.current, item.benchmark);
          const Icon = indicator.icon;

          return (
            <div key={index} className={`p-4 rounded-lg ${theme === 'dark' ? 'bg-slate-900/30' : 'bg-slate-50'} border ${theme === 'dark' ? 'border-slate-700/30' : 'border-slate-200'}`}>
              <div className="flex items-center justify-between mb-3">
                <div>
                  <div className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
                    {item.label}
                  </div>
                  <div className={`text-2xl font-bold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>
                    {item.current.toLocaleString()}
                    {item.label.includes('Rate') || item.label.includes('IRR') ? '%' : ''}
                  </div>
                </div>
                <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg ${indicator.bgColor}`}>
                  <Icon className={`w-4 h-4 ${indicator.color}`} />
                  <span className={`text-sm font-medium ${indicator.color}`}>
                    {indicator.text}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="flex-1 h-2 bg-slate-700/20 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full transition-all"
                    style={{ width: `${Math.min((item.current / Math.max(item.current, item.benchmark)) * 100, 100)}%` }}
                  />
                </div>
                <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>
                  {item.benchmarkLabel}: {item.benchmark.toLocaleString()}
                  {item.label.includes('Rate') || item.label.includes('IRR') ? '%' : ''}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
