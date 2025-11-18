import { useState, useEffect } from 'react';
import { X, Palette, Settings, Database } from 'lucide-react';
import { useDashboardBuilder } from '../../contexts/DashboardBuilderContext';
import { useTheme } from '../../contexts/ThemeContext';
import { WidgetColorScheme, DataSource } from '../../types/dashboard';

export function WidgetConfigPanel() {
  const { selectedWidget, updateWidget, selectWidget } = useDashboardBuilder();
  const { theme, colors } = useTheme();

  const [title, setTitle] = useState('');
  const [dataSource, setDataSource] = useState<DataSource>('portfolio-value');
  const [showLegend, setShowLegend] = useState(true);
  const [showGrid, setShowGrid] = useState(true);
  const [drillDownEnabled, setDrillDownEnabled] = useState(false);
  const [comparisonEnabled, setComparisonEnabled] = useState(false);

  // Color customization
  const [customColors, setCustomColors] = useState<WidgetColorScheme>({
    primary: '#3b82f6',
    secondary: '#10b981',
    accent: '#8b5cf6',
    background: theme === 'dark' ? '#1e293b' : '#ffffff',
    text: theme === 'dark' ? '#e2e8f0' : '#1e293b',
  });

  useEffect(() => {
    if (selectedWidget) {
      setTitle(selectedWidget.config.title);
      setDataSource(selectedWidget.config.dataSource);
      setShowLegend(selectedWidget.config.showLegend ?? true);
      setShowGrid(selectedWidget.config.showGrid ?? true);
      setDrillDownEnabled(selectedWidget.config.drillDown?.enabled ?? false);
      setComparisonEnabled(selectedWidget.config.comparison?.enabled ?? false);

      if (selectedWidget.config.colorScheme) {
        setCustomColors(selectedWidget.config.colorScheme);
      }
    }
  }, [selectedWidget]);

  const handleSave = () => {
    if (!selectedWidget) return;

    updateWidget(selectedWidget.id, {
      config: {
        ...selectedWidget.config,
        title,
        dataSource,
        showLegend,
        showGrid,
        colorScheme: customColors,
        drillDown: {
          enabled: drillDownEnabled,
          levels: drillDownEnabled ? ['Monthly', 'Weekly', 'Daily'] : [],
        },
        comparison: {
          enabled: comparisonEnabled,
          benchmarkType: 'market',
        },
      },
    });
  };

  const dataSourceOptions: Array<{ value: DataSource; label: string }> = [
    { value: 'portfolio-value', label: 'Portfolio Value' },
    { value: 'noi', label: 'Net Operating Income' },
    { value: 'occupancy', label: 'Occupancy Rate' },
    { value: 'cap-rate', label: 'Cap Rate' },
    { value: 'cash-flow', label: 'Cash Flow' },
    { value: 'revenue', label: 'Revenue' },
    { value: 'expenses', label: 'Expenses' },
    { value: 'market-trends', label: 'Market Trends' },
    { value: 'property-performance', label: 'Property Performance' },
    { value: 'custom', label: 'Custom Query' },
  ];

  const presetColorSchemes: Array<{ name: string; colors: WidgetColorScheme }> = [
    {
      name: 'Ocean Blue',
      colors: {
        primary: '#3b82f6',
        secondary: '#06b6d4',
        accent: '#0ea5e9',
        background: theme === 'dark' ? '#1e293b' : '#ffffff',
        text: theme === 'dark' ? '#e2e8f0' : '#1e293b',
        gradient: { from: '#3b82f6', to: '#06b6d4' },
      },
    },
    {
      name: 'Forest Green',
      colors: {
        primary: '#10b981',
        secondary: '#34d399',
        accent: '#059669',
        background: theme === 'dark' ? '#1e293b' : '#ffffff',
        text: theme === 'dark' ? '#e2e8f0' : '#1e293b',
        gradient: { from: '#10b981', to: '#34d399' },
      },
    },
    {
      name: 'Royal Purple',
      colors: {
        primary: '#8b5cf6',
        secondary: '#a78bfa',
        accent: '#7c3aed',
        background: theme === 'dark' ? '#1e293b' : '#ffffff',
        text: theme === 'dark' ? '#e2e8f0' : '#1e293b',
        gradient: { from: '#8b5cf6', to: '#a78bfa' },
      },
    },
    {
      name: 'Sunset Orange',
      colors: {
        primary: '#f59e0b',
        secondary: '#fb923c',
        accent: '#ea580c',
        background: theme === 'dark' ? '#1e293b' : '#ffffff',
        text: theme === 'dark' ? '#e2e8f0' : '#1e293b',
        gradient: { from: '#f59e0b', to: '#fb923c' },
      },
    },
  ];

  if (!selectedWidget) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-96 z-50 flex flex-col shadow-2xl">
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black/20 backdrop-blur-sm -z-10"
        onClick={() => selectWidget(null)}
      />

      {/* Panel */}
      <div className={`flex-1 ${theme === 'dark' ? 'bg-slate-900' : 'bg-white'} border-l ${colors.border.primary} overflow-hidden flex flex-col`}>
        {/* Header */}
        <div className={`p-6 border-b ${colors.border.primary}`}>
          <div className="flex items-center justify-between mb-2">
            <h2 className={`text-xl font-semibold ${colors.text.primary}`}>
              Widget Settings
            </h2>
            <button
              onClick={() => selectWidget(null)}
              className={`p-2 rounded-lg ${theme === 'dark' ? 'hover:bg-slate-800' : 'hover:bg-slate-100'} transition-colors`}
            >
              <X className={`w-5 h-5 ${colors.text.secondary}`} />
            </button>
          </div>
          <p className={`text-sm ${colors.text.secondary}`}>
            Customize your widget appearance and data
          </p>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Basic Settings */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Settings className={`w-5 h-5 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
              <h3 className={`text-lg font-semibold ${colors.text.primary}`}>
                Basic Settings
              </h3>
            </div>

            <div className="space-y-4">
              <div>
                <label className={`block text-sm font-medium ${colors.text.secondary} mb-2`}>
                  Widget Title
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className={`w-full px-3 py-2 rounded-lg ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-300 text-slate-900'} border focus:outline-none focus:ring-2 focus:ring-blue-500`}
                />
              </div>

              <div>
                <label className={`block text-sm font-medium ${colors.text.secondary} mb-2`}>
                  Data Source
                </label>
                <select
                  value={dataSource}
                  onChange={(e) => setDataSource(e.target.value as DataSource)}
                  className={`w-full px-3 py-2 rounded-lg ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-300 text-slate-900'} border focus:outline-none focus:ring-2 focus:ring-blue-500`}
                >
                  {dataSourceOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Display Options */}
          {(selectedWidget.type.includes('chart')) && (
            <div>
              <h3 className={`text-lg font-semibold ${colors.text.primary} mb-4`}>
                Display Options
              </h3>

              <div className="space-y-3">
                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={showLegend}
                    onChange={(e) => setShowLegend(e.target.checked)}
                    className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className={`text-sm ${colors.text.secondary}`}>Show Legend</span>
                </label>

                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={showGrid}
                    onChange={(e) => setShowGrid(e.target.checked)}
                    className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className={`text-sm ${colors.text.secondary}`}>Show Grid</span>
                </label>

                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={drillDownEnabled}
                    onChange={(e) => setDrillDownEnabled(e.target.checked)}
                    className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className={`text-sm ${colors.text.secondary}`}>Enable Drill-Down</span>
                </label>

                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={comparisonEnabled}
                    onChange={(e) => setComparisonEnabled(e.target.checked)}
                    className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className={`text-sm ${colors.text.secondary}`}>Show Comparison</span>
                </label>
              </div>
            </div>
          )}

          {/* Color Customization */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Palette className={`w-5 h-5 ${theme === 'dark' ? 'text-purple-400' : 'text-purple-600'}`} />
              <h3 className={`text-lg font-semibold ${colors.text.primary}`}>
                Color Theme
              </h3>
            </div>

            {/* Preset Schemes */}
            <div className="grid grid-cols-2 gap-2 mb-4">
              {presetColorSchemes.map((preset) => (
                <button
                  key={preset.name}
                  onClick={() => setCustomColors(preset.colors)}
                  className={`p-3 rounded-lg border ${
                    theme === 'dark'
                      ? 'bg-slate-800 border-slate-700 hover:border-slate-600'
                      : 'bg-white border-slate-200 hover:border-slate-300'
                  } transition-all text-left`}
                >
                  <div className="flex gap-1 mb-2">
                    <div className="w-6 h-6 rounded" style={{ backgroundColor: preset.colors.primary }} />
                    <div className="w-6 h-6 rounded" style={{ backgroundColor: preset.colors.secondary }} />
                    <div className="w-6 h-6 rounded" style={{ backgroundColor: preset.colors.accent }} />
                  </div>
                  <div className={`text-xs font-medium ${colors.text.primary}`}>
                    {preset.name}
                  </div>
                </button>
              ))}
            </div>

            {/* Custom Colors */}
            <div className="space-y-3">
              {['primary', 'secondary', 'accent'].map((colorKey) => (
                <div key={colorKey}>
                  <label className={`block text-sm font-medium ${colors.text.secondary} mb-2 capitalize`}>
                    {colorKey} Color
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="color"
                      value={customColors[colorKey as keyof WidgetColorScheme] as string}
                      onChange={(e) => setCustomColors({ ...customColors, [colorKey]: e.target.value })}
                      className="w-12 h-10 rounded-lg cursor-pointer"
                    />
                    <input
                      type="text"
                      value={customColors[colorKey as keyof WidgetColorScheme] as string}
                      onChange={(e) => setCustomColors({ ...customColors, [colorKey]: e.target.value })}
                      className={`flex-1 px-3 py-2 rounded-lg ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-300 text-slate-900'} border focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm`}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className={`p-6 border-t ${colors.border.primary}`}>
          <button
            onClick={handleSave}
            className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors shadow-sm"
          >
            Apply Changes
          </button>
        </div>
      </div>
    </div>
  );
}
