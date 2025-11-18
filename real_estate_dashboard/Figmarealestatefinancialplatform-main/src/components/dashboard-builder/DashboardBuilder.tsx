import { useEffect } from 'react';
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import { useDashboardBuilder } from '../../contexts/DashboardBuilderContext';
import { useTheme } from '../../contexts/ThemeContext';
import { KPIWidget } from './widgets/KPIWidget';
import { ChartWidget } from './widgets/ChartWidget';
import { ComparisonWidget } from './widgets/ComparisonWidget';
import { BenchmarkWidget } from './widgets/BenchmarkWidget';
import { WidgetWrapper } from './WidgetWrapper';
import { DashboardToolbar } from './DashboardToolbar';
import { WidgetConfigPanel } from './WidgetConfigPanel';
import { Widget } from '../../types/dashboard';

export function DashboardBuilder() {
  const {
    currentDashboard,
    updateWidgetLayout,
    isEditMode,
    createDashboard,
  } = useDashboardBuilder();
  const { theme } = useTheme();

  // Create a default dashboard if none exists
  useEffect(() => {
    if (!currentDashboard) {
      createDashboard('My Dashboard', 'Custom interactive dashboard');
    }
  }, [currentDashboard, createDashboard]);

  if (!currentDashboard) {
    return (
      <div className={`flex items-center justify-center h-screen ${theme === 'dark' ? 'bg-[#0a0e17]' : 'bg-slate-50'}`}>
        <div className="text-center">
          <div className={`text-xl ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>
            Loading dashboard...
          </div>
        </div>
      </div>
    );
  }

  const layout = currentDashboard.widgets.map(widget => ({
    i: widget.id,
    x: widget.layout.x,
    y: widget.layout.y,
    w: widget.layout.w,
    h: widget.layout.h,
    minW: widget.layout.minW || 2,
    minH: widget.layout.minH || 2,
    maxW: widget.layout.maxW,
    maxH: widget.layout.maxH,
  }));

  const handleLayoutChange = (newLayout: any[]) => {
    if (isEditMode) {
      updateWidgetLayout(newLayout);
    }
  };

  const renderWidget = (widget: Widget) => {
    switch (widget.type) {
      case 'kpi':
        return <KPIWidget widget={widget} />;
      case 'line-chart':
      case 'area-chart':
      case 'bar-chart':
      case 'pie-chart':
        return <ChartWidget widget={widget} />;
      case 'comparison':
        return <ComparisonWidget widget={widget} />;
      case 'benchmark':
        return <BenchmarkWidget widget={widget} />;
      default:
        return (
          <div className={`h-full flex items-center justify-center ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
            Widget type not supported
          </div>
        );
    }
  };

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-[#0a0e17]' : 'bg-slate-50'}`}>
      <DashboardToolbar />

      <div className="p-6">
        {currentDashboard.widgets.length === 0 ? (
          <div className={`flex flex-col items-center justify-center h-[calc(100vh-200px)] ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
            <svg
              className="w-24 h-24 mb-4 opacity-50"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 13a1 1 0 011-1h4a1 1 0 011 1v6a1 1 0 01-1 1h-4a1 1 0 01-1-1v-6z"
              />
            </svg>
            <h3 className={`text-xl font-semibold mb-2 ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>
              Your dashboard is empty
            </h3>
            <p className="text-center max-w-md">
              Start building your custom dashboard by adding widgets from the toolbar above.
              <br />
              You can drag, resize, and customize each widget to fit your needs.
            </p>
          </div>
        ) : (
          <GridLayout
            className="layout"
            layout={layout}
            cols={currentDashboard.columns}
            rowHeight={60}
            width={1200}
            isDraggable={isEditMode}
            isResizable={isEditMode}
            onLayoutChange={handleLayoutChange}
            draggableHandle=".drag-handle"
            compactType="vertical"
            preventCollision={false}
            margin={[16, 16]}
            containerPadding={[0, 0]}
          >
            {currentDashboard.widgets.map(widget => (
              <div key={widget.id} className="dashboard-widget">
                <WidgetWrapper widget={widget}>
                  {renderWidget(widget)}
                </WidgetWrapper>
              </div>
            ))}
          </GridLayout>
        )}
      </div>

      <WidgetConfigPanel />

      {/* Custom styles for grid layout */}
      <style>{`
        .layout {
          position: relative;
          transition: height 200ms ease;
        }

        .dashboard-widget {
          transition: all 200ms ease;
        }

        .dashboard-widget .react-resizable-handle {
          opacity: 0;
          transition: opacity 200ms ease;
        }

        .dashboard-widget:hover .react-resizable-handle {
          opacity: 1;
        }

        .react-resizable-handle::after {
          content: '';
          position: absolute;
          right: 3px;
          bottom: 3px;
          width: 8px;
          height: 8px;
          border-right: 2px solid ${theme === 'dark' ? '#64748b' : '#94a3b8'};
          border-bottom: 2px solid ${theme === 'dark' ? '#64748b' : '#94a3b8'};
        }

        .react-grid-item.react-grid-placeholder {
          background: ${theme === 'dark' ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)'};
          border: 2px dashed ${theme === 'dark' ? 'rgba(59, 130, 246, 0.5)' : 'rgba(59, 130, 246, 0.3)'};
          border-radius: 12px;
          opacity: 1;
          transition: all 200ms ease;
        }

        .react-grid-item.react-draggable-dragging {
          transition: none;
          z-index: 100;
          will-change: transform;
        }
      `}</style>
    </div>
  );
}
