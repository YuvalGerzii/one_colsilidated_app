import { ReactNode } from 'react';
import { GripVertical, Settings, Copy, Trash2 } from 'lucide-react';
import { useDashboardBuilder } from '../../contexts/DashboardBuilderContext';
import { useTheme } from '../../contexts/ThemeContext';
import { Widget } from '../../types/dashboard';

interface WidgetWrapperProps {
  widget: Widget;
  children: ReactNode;
}

export function WidgetWrapper({ widget, children }: WidgetWrapperProps) {
  const { deleteWidget, selectWidget, duplicateWidget, isEditMode, selectedWidget } = useDashboardBuilder();
  const { theme } = useTheme();

  const isSelected = selectedWidget?.id === widget.id;

  return (
    <div className={`h-full relative group ${isSelected ? 'ring-2 ring-blue-500 ring-offset-2 ring-offset-transparent' : ''}`}>
      {isEditMode && (
        <>
          {/* Drag Handle */}
          <div
            className={`drag-handle absolute -top-2 left-1/2 -translate-x-1/2 z-10 px-3 py-1 rounded-lg ${theme === 'dark' ? 'bg-slate-700 border-slate-600' : 'bg-white border-slate-300'} border shadow-sm opacity-0 group-hover:opacity-100 transition-all cursor-move flex items-center gap-1`}
          >
            <GripVertical className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`} />
            <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
              Drag
            </span>
          </div>

          {/* Action Buttons */}
          <div
            className={`absolute -top-2 -right-2 z-10 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all`}
          >
            <button
              onClick={() => selectWidget(widget.id)}
              className={`p-2 rounded-lg ${theme === 'dark' ? 'bg-slate-700 hover:bg-slate-600 border-slate-600' : 'bg-white hover:bg-slate-50 border-slate-300'} border shadow-sm transition-colors`}
              title="Configure widget"
            >
              <Settings className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`} />
            </button>
            <button
              onClick={() => duplicateWidget(widget.id)}
              className={`p-2 rounded-lg ${theme === 'dark' ? 'bg-slate-700 hover:bg-slate-600 border-slate-600' : 'bg-white hover:bg-slate-50 border-slate-300'} border shadow-sm transition-colors`}
              title="Duplicate widget"
            >
              <Copy className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`} />
            </button>
            <button
              onClick={() => deleteWidget(widget.id)}
              className={`p-2 rounded-lg ${theme === 'dark' ? 'bg-red-900/50 hover:bg-red-900/70 border-red-800/50' : 'bg-red-50 hover:bg-red-100 border-red-200'} border shadow-sm transition-colors`}
              title="Delete widget"
            >
              <Trash2 className="w-4 h-4 text-red-500" />
            </button>
          </div>
        </>
      )}

      {children}
    </div>
  );
}
