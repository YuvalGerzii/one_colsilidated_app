import { useState } from 'react';
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { Widget } from '../../../types/dashboard';
import { useTheme } from '../../../contexts/ThemeContext';

interface ChartWidgetProps {
  widget: Widget;
  data?: any[];
}

// Sample data generator
const generateSampleData = (type: string) => {
  if (type === 'pie-chart') {
    return [
      { name: 'Residential', value: 45 },
      { name: 'Commercial', value: 30 },
      { name: 'Industrial', value: 15 },
      { name: 'Mixed Use', value: 10 },
    ];
  }

  return [
    { month: 'Jan', value: 320000, target: 350000, comparison: 310000 },
    { month: 'Feb', value: 335000, target: 350000, comparison: 325000 },
    { month: 'Mar', value: 342000, target: 350000, comparison: 330000 },
    { month: 'Apr', value: 355000, target: 350000, comparison: 340000 },
    { month: 'May', value: 368000, target: 350000, comparison: 355000 },
    { month: 'Jun', value: 380000, target: 350000, comparison: 365000 },
  ];
};

export function ChartWidget({ widget, data }: ChartWidgetProps) {
  const { theme } = useTheme();
  const [drillDownLevel, setDrillDownLevel] = useState(0);
  const [breadcrumbs, setBreadcrumbs] = useState<string[]>([widget.config.title]);

  const colorScheme = widget.config.colorScheme;
  const chartData = data || generateSampleData(widget.type);

  const isDrillDownEnabled = widget.config.drillDown?.enabled;
  const drillDownLevels = widget.config.drillDown?.levels || [];

  const backgroundColor = colorScheme?.background || (theme === 'dark' ? 'bg-slate-800/50' : 'bg-white');
  const primaryColor = colorScheme?.primary || '#3b82f6';
  const secondaryColor = colorScheme?.secondary || '#10b981';
  const accentColor = colorScheme?.accent || '#8b5cf6';

  const COLORS = [primaryColor, secondaryColor, accentColor, '#f59e0b'];

  const handleDrillDown = (dataPoint: any) => {
    if (!isDrillDownEnabled || drillDownLevel >= drillDownLevels.length) return;

    setDrillDownLevel(prev => prev + 1);
    setBreadcrumbs(prev => [...prev, dataPoint.month || dataPoint.name]);
  };

  const handleBreadcrumbClick = (index: number) => {
    setDrillDownLevel(index);
    setBreadcrumbs(prev => prev.slice(0, index + 1));
  };

  const renderChart = () => {
    const commonProps = {
      data: chartData,
      onClick: handleDrillDown,
      style: { cursor: isDrillDownEnabled ? 'pointer' : 'default' },
    };

    const gridColor = theme === 'dark' ? '#334155' : '#cbd5e1';
    const textColor = theme === 'dark' ? '#64748b' : '#475569';

    switch (widget.type) {
      case 'line-chart':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart {...commonProps}>
              {widget.config.showGrid && (
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} opacity={0.3} />
              )}
              <XAxis dataKey="month" stroke={textColor} fontSize={12} />
              <YAxis stroke={textColor} fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff',
                  border: `1px solid ${gridColor}`,
                  borderRadius: '8px',
                  color: theme === 'dark' ? '#fff' : '#0f172a',
                }}
              />
              {widget.config.showLegend && <Legend />}
              <Line type="monotone" dataKey="value" stroke={primaryColor} strokeWidth={2} />
              {widget.config.comparison?.enabled && (
                <Line type="monotone" dataKey="comparison" stroke={secondaryColor} strokeWidth={2} strokeDasharray="5 5" />
              )}
            </LineChart>
          </ResponsiveContainer>
        );

      case 'area-chart':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart {...commonProps}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={primaryColor} stopOpacity={0.3} />
                  <stop offset="95%" stopColor={primaryColor} stopOpacity={0} />
                </linearGradient>
              </defs>
              {widget.config.showGrid && (
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} opacity={0.3} />
              )}
              <XAxis dataKey="month" stroke={textColor} fontSize={12} />
              <YAxis stroke={textColor} fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff',
                  border: `1px solid ${gridColor}`,
                  borderRadius: '8px',
                  color: theme === 'dark' ? '#fff' : '#0f172a',
                }}
              />
              {widget.config.showLegend && <Legend />}
              <Area
                type="monotone"
                dataKey="value"
                stroke={primaryColor}
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorValue)"
              />
            </AreaChart>
          </ResponsiveContainer>
        );

      case 'bar-chart':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart {...commonProps}>
              {widget.config.showGrid && (
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} opacity={0.3} />
              )}
              <XAxis dataKey="month" stroke={textColor} fontSize={12} />
              <YAxis stroke={textColor} fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff',
                  border: `1px solid ${gridColor}`,
                  borderRadius: '8px',
                  color: theme === 'dark' ? '#fff' : '#0f172a',
                }}
              />
              {widget.config.showLegend && <Legend />}
              <Bar dataKey="value" fill={primaryColor} radius={[8, 8, 0, 0]} />
              {widget.config.comparison?.enabled && (
                <Bar dataKey="target" fill={secondaryColor} radius={[8, 8, 0, 0]} opacity={0.5} />
              )}
            </BarChart>
          </ResponsiveContainer>
        );

      case 'pie-chart':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill={primaryColor}
                dataKey="value"
                onClick={handleDrillDown}
              >
                {chartData.map((entry: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: theme === 'dark' ? '#1e293b' : '#ffffff',
                  border: `1px solid ${gridColor}`,
                  borderRadius: '8px',
                  color: theme === 'dark' ? '#fff' : '#0f172a',
                }}
              />
              {widget.config.showLegend && <Legend />}
            </PieChart>
          </ResponsiveContainer>
        );

      default:
        return <div>Unsupported chart type</div>;
    }
  };

  return (
    <div className={`h-full ${backgroundColor} rounded-xl border ${theme === 'dark' ? 'border-slate-700/50' : 'border-slate-200'} p-6 flex flex-col`}>
      {/* Header */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className={`text-lg font-semibold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>
            {widget.config.title}
          </h3>
        </div>

        {/* Breadcrumbs for drill-down */}
        {isDrillDownEnabled && breadcrumbs.length > 1 && (
          <div className="flex items-center gap-2 text-sm">
            {breadcrumbs.map((crumb, index) => (
              <div key={index} className="flex items-center gap-2">
                <button
                  onClick={() => handleBreadcrumbClick(index)}
                  className={`${
                    index === breadcrumbs.length - 1
                      ? theme === 'dark' ? 'text-blue-400' : 'text-blue-600'
                      : theme === 'dark' ? 'text-slate-400 hover:text-slate-200' : 'text-slate-600 hover:text-slate-800'
                  } transition-colors`}
                >
                  {crumb}
                </button>
                {index < breadcrumbs.length - 1 && (
                  <ChevronRight className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-600' : 'text-slate-400'}`} />
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Chart */}
      <div className="flex-1 min-h-0">
        {renderChart()}
      </div>

      {/* Drill-down indicator */}
      {isDrillDownEnabled && drillDownLevel < drillDownLevels.length && (
        <div className={`mt-2 text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'} flex items-center gap-1`}>
          <ChevronDown className="w-3 h-3" />
          Click to drill down
        </div>
      )}
    </div>
  );
}
