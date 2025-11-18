import { useState } from 'react';
import {
  Plus, Save, Eye, Edit, LayoutGrid, Palette, Download, Upload,
  BarChart3, TrendingUp, PieChart, LineChart, AreaChart, GitCompare
} from 'lucide-react';
import { useDashboardBuilder } from '../../contexts/DashboardBuilderContext';
import { useTheme } from '../../contexts/ThemeContext';
import { WidgetType } from '../../types/dashboard';

export function DashboardToolbar() {
  const {
    currentDashboard,
    addWidget,
    saveDashboard,
    isEditMode,
    toggleEditMode,
  } = useDashboardBuilder();
  const { theme } = useTheme();

  // Define theme-based colors
  const colors = {
    text: {
      primary: theme === 'dark' ? 'text-gray-100' : 'text-gray-900',
      secondary: theme === 'dark' ? 'text-gray-400' : 'text-gray-600',
    },
    border: {
      primary: theme === 'dark' ? 'border-gray-800' : 'border-gray-200',
    },
  };
  const [showWidgetMenu, setShowWidgetMenu] = useState(false);

  const widgetTypes: Array<{ type: WidgetType; label: string; icon: any; description: string }> = [
    { type: 'kpi', label: 'KPI Card', icon: TrendingUp, description: 'Display key metrics' },
    { type: 'line-chart', label: 'Line Chart', icon: LineChart, description: 'Trend analysis' },
    { type: 'area-chart', label: 'Area Chart', icon: AreaChart, description: 'Filled trend chart' },
    { type: 'bar-chart', label: 'Bar Chart', icon: BarChart3, description: 'Compare values' },
    { type: 'pie-chart', label: 'Pie Chart', icon: PieChart, description: 'Show proportions' },
    { type: 'comparison', label: 'Comparison', icon: GitCompare, description: 'Compare metrics' },
    { type: 'benchmark', label: 'Benchmark', icon: BarChart3, description: 'Market benchmarks' },
  ];

  const handleAddWidget = (type: WidgetType) => {
    addWidget(type);
    setShowWidgetMenu(false);
  };

  const handleExport = () => {
    if (!currentDashboard) return;

    const dataStr = JSON.stringify(currentDashboard, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `dashboard-${currentDashboard.name.replace(/\s+/g, '-').toLowerCase()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <header className={`sticky top-0 z-30 ${theme === 'dark' ? 'bg-[#0f1419]/95' : 'bg-white/95'} backdrop-blur-xl border-b ${colors.border.primary} shadow-sm`}>
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Left: Dashboard Info */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <div className={`w-10 h-10 ${theme === 'dark' ? 'bg-blue-500/10 border-blue-500/20' : 'bg-blue-100 border-blue-200'} rounded-lg flex items-center justify-center border`}>
                <LayoutGrid className={`w-5 h-5 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
              </div>
              <div>
                <h1 className={`text-lg font-semibold ${colors.text.primary}`}>
                  {currentDashboard?.name || 'Dashboard Builder'}
                </h1>
                <p className={`text-xs ${colors.text.secondary}`}>
                  {currentDashboard?.description || 'Build your custom dashboard'}
                </p>
              </div>
            </div>
          </div>

          {/* Right: Actions */}
          <div className="flex items-center gap-2">
            {/* Add Widget Button */}
            <div className="relative">
              <button
                onClick={() => setShowWidgetMenu(!showWidgetMenu)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                  theme === 'dark'
                    ? 'bg-blue-600 hover:bg-blue-700 text-white'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                } transition-colors shadow-sm`}
              >
                <Plus className="w-4 h-4" />
                <span className="text-sm font-medium">Add Widget</span>
              </button>

              {showWidgetMenu && (
                <>
                  <div
                    className="fixed inset-0 z-40"
                    onClick={() => setShowWidgetMenu(false)}
                  />
                  <div className={`absolute top-full right-0 mt-2 w-72 ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} rounded-xl border shadow-xl z-50 overflow-hidden`}>
                    <div className={`p-3 border-b ${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'}`}>
                      <h3 className={`text-sm font-semibold ${colors.text.primary}`}>
                        Choose Widget Type
                      </h3>
                    </div>
                    <div className="p-2 max-h-96 overflow-y-auto">
                      {widgetTypes.map(({ type, label, icon: Icon, description }) => (
                        <button
                          key={type}
                          onClick={() => handleAddWidget(type)}
                          className={`w-full flex items-center gap-3 p-3 rounded-lg ${
                            theme === 'dark'
                              ? 'hover:bg-slate-700/50'
                              : 'hover:bg-slate-50'
                          } transition-colors text-left group`}
                        >
                          <div className={`w-10 h-10 ${theme === 'dark' ? 'bg-blue-500/10 group-hover:bg-blue-500/20' : 'bg-blue-100 group-hover:bg-blue-200'} rounded-lg flex items-center justify-center transition-colors`}>
                            <Icon className={`w-5 h-5 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
                          </div>
                          <div className="flex-1">
                            <div className={`text-sm font-medium ${colors.text.primary} mb-0.5`}>
                              {label}
                            </div>
                            <div className={`text-xs ${colors.text.secondary}`}>
                              {description}
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Edit Mode Toggle */}
            <button
              onClick={toggleEditMode}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                isEditMode
                  ? theme === 'dark'
                    ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                    : 'bg-blue-100 text-blue-700 border-blue-200'
                  : theme === 'dark'
                    ? 'bg-slate-800 text-slate-400 border-slate-700'
                    : 'bg-slate-100 text-slate-600 border-slate-200'
              } border transition-colors shadow-sm`}
            >
              {isEditMode ? (
                <>
                  <Edit className="w-4 h-4" />
                  <span className="text-sm">Editing</span>
                </>
              ) : (
                <>
                  <Eye className="w-4 h-4" />
                  <span className="text-sm">Preview</span>
                </>
              )}
            </button>

            {/* Save Button */}
            <button
              onClick={saveDashboard}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                theme === 'dark'
                  ? 'bg-green-500/10 hover:bg-green-500/20 text-green-400 border-green-500/20'
                  : 'bg-green-100 hover:bg-green-200 text-green-700 border-green-200'
              } border transition-colors shadow-sm`}
            >
              <Save className="w-4 h-4" />
              <span className="text-sm">Save</span>
            </button>

            {/* Export Button */}
            <button
              onClick={handleExport}
              className={`p-2 rounded-lg ${
                theme === 'dark'
                  ? 'bg-slate-800 hover:bg-slate-700 text-slate-400 border-slate-700'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-600 border-slate-200'
              } border transition-colors shadow-sm`}
              title="Export dashboard"
            >
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
