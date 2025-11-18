import { Widget } from '../../../types/dashboard';
import { useTheme } from '../../../contexts/ThemeContext';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';

interface BenchmarkWidgetProps {
  widget: Widget;
  data?: any[];
}

export function BenchmarkWidget({ widget, data }: BenchmarkWidgetProps) {
  const { theme } = useTheme();
  const colorScheme = widget.config.colorScheme;

  // Sample data if not provided
  const displayData = data || [
    { metric: 'NOI', portfolio: 1.02, market: 0.95, top: 1.15, unit: 'M' },
    { metric: 'Cap Rate', portfolio: 6.8, market: 6.2, top: 7.2, unit: '%' },
    { metric: 'Occupancy', portfolio: 94.6, market: 91.2, top: 96.5, unit: '%' },
    { metric: 'Rent/SqFt', portfolio: 32.5, market: 30.2, top: 35.8, unit: '$' },
  ];

  const backgroundColor = colorScheme?.background || (theme === 'dark' ? 'bg-slate-800/50' : 'bg-white');
  const primaryColor = colorScheme?.primary || '#3b82f6';
  const secondaryColor = colorScheme?.secondary || '#64748b';
  const accentColor = colorScheme?.accent || '#10b981';

  const gridColor = theme === 'dark' ? '#334155' : '#cbd5e1';
  const textColor = theme === 'dark' ? '#64748b' : '#475569';

  return (
    <div className={`h-full ${backgroundColor} rounded-xl border ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-200'} p-6 flex flex-col`}>
      <div className="mb-4">
        <h3 className={`text-lg font-semibold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'} mb-2`}>
          {widget.config.title}
        </h3>
        <p className={`text-sm ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
          Portfolio vs Market vs Top Quartile
        </p>
      </div>

      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={displayData} layout="vertical">
            {widget.config.showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke={gridColor} opacity={0.3} />
            )}
            <XAxis type="number" stroke={textColor} fontSize={12} />
            <YAxis type="category" dataKey="metric" stroke={textColor} fontSize={12} width={80} />
            <Tooltip
              contentStyle={{
                backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff',
                border: `1px solid ${gridColor}`,
                borderRadius: '8px',
                color: theme === 'dark' ? '#fff' : '#0f172a',
              }}
              formatter={(value: number, name: string, props: any) => [
                `${value}${props.payload.unit}`,
                name === 'portfolio' ? 'Your Portfolio' : name === 'market' ? 'Market Average' : 'Top Quartile'
              ]}
            />
            {widget.config.showLegend && <Legend />}
            <Bar dataKey="portfolio" fill={primaryColor} name="Your Portfolio" radius={[0, 4, 4, 0]} />
            <Bar dataKey="market" fill={secondaryColor} name="Market Average" radius={[0, 4, 4, 0]} />
            <Bar dataKey="top" fill={accentColor} name="Top Quartile" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Summary Stats */}
      <div className="mt-4 grid grid-cols-3 gap-3">
        {['Your Portfolio', 'Market Avg', 'Top Quartile'].map((label, index) => (
          <div key={label} className={`p-3 rounded-lg ${theme === 'dark' ? 'bg-slate-900/30' : 'bg-slate-50'} border ${theme === 'dark' ? 'border-slate-700/30' : 'border-slate-200'}`}>
            <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'} mb-1`}>
              {label}
            </div>
            <div className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: [primaryColor, secondaryColor, accentColor][index] }}
              />
              <div className={`text-sm font-semibold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>
                {index === 0 ? 'Above' : index === 1 ? 'Average' : 'Leader'}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
