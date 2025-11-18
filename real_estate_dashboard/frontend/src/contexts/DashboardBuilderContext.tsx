import { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Dashboard, Widget, WidgetType, WidgetColorScheme } from '../types/dashboard';

interface DashboardBuilderContextType {
  currentDashboard: Dashboard | null;
  dashboards: Dashboard[];
  selectedWidget: Widget | null;
  isEditMode: boolean;

  // Dashboard actions
  createDashboard: (name: string, description?: string) => void;
  loadDashboard: (id: string) => void;
  saveDashboard: () => void;
  deleteDashboard: (id: string) => void;
  updateDashboard: (updates: Partial<Dashboard>) => void;

  // Widget actions
  addWidget: (type: WidgetType) => void;
  updateWidget: (id: string, updates: Partial<Widget>) => void;
  deleteWidget: (id: string) => void;
  selectWidget: (id: string | null) => void;
  duplicateWidget: (id: string) => void;

  // Layout actions
  updateWidgetLayout: (layouts: Array<{ i: string; x: number; y: number; w: number; h: number }>) => void;

  // Color customization
  updateGlobalColorScheme: (colorScheme: WidgetColorScheme) => void;
  updateWidgetColorScheme: (id: string, colorScheme: WidgetColorScheme) => void;

  // Edit mode
  toggleEditMode: () => void;
}

const DashboardBuilderContext = createContext<DashboardBuilderContextType | undefined>(undefined);

export function DashboardBuilderProvider({ children }: { children: ReactNode }) {
  const [dashboards, setDashboards] = useState<Dashboard[]>([]);
  const [currentDashboard, setCurrentDashboard] = useState<Dashboard | null>(null);
  const [selectedWidget, setSelectedWidget] = useState<Widget | null>(null);
  const [isEditMode, setIsEditMode] = useState(true);

  const createDashboard = useCallback((name: string, description?: string) => {
    const newDashboard: Dashboard = {
      id: `dashboard-${Date.now()}`,
      name,
      description,
      widgets: [],
      layout: 'grid',
      columns: 12,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    setDashboards(prev => [...prev, newDashboard]);
    setCurrentDashboard(newDashboard);

    // Save to localStorage
    localStorage.setItem('dashboards', JSON.stringify([...dashboards, newDashboard]));
  }, [dashboards]);

  const loadDashboard = useCallback((id: string) => {
    const dashboard = dashboards.find(d => d.id === id);
    if (dashboard) {
      setCurrentDashboard(dashboard);
      setSelectedWidget(null);
    }
  }, [dashboards]);

  const saveDashboard = useCallback(() => {
    if (!currentDashboard) return;

    const updatedDashboard = {
      ...currentDashboard,
      updatedAt: new Date(),
    };

    setDashboards(prev =>
      prev.map(d => d.id === updatedDashboard.id ? updatedDashboard : d)
    );
    setCurrentDashboard(updatedDashboard);

    // Save to localStorage
    const allDashboards = dashboards.map(d =>
      d.id === updatedDashboard.id ? updatedDashboard : d
    );
    localStorage.setItem('dashboards', JSON.stringify(allDashboards));
  }, [currentDashboard, dashboards]);

  const deleteDashboard = useCallback((id: string) => {
    setDashboards(prev => prev.filter(d => d.id !== id));
    if (currentDashboard?.id === id) {
      setCurrentDashboard(null);
    }

    // Update localStorage
    const updated = dashboards.filter(d => d.id !== id);
    localStorage.setItem('dashboards', JSON.stringify(updated));
  }, [currentDashboard, dashboards]);

  const updateDashboard = useCallback((updates: Partial<Dashboard>) => {
    if (!currentDashboard) return;

    const updated = { ...currentDashboard, ...updates, updatedAt: new Date() };
    setCurrentDashboard(updated);
  }, [currentDashboard]);

  const addWidget = useCallback((type: WidgetType) => {
    if (!currentDashboard) return;

    const newWidget: Widget = {
      id: `widget-${Date.now()}`,
      type,
      config: {
        title: `New ${type} Widget`,
        dataSource: 'portfolio-value',
        showLegend: true,
        showGrid: true,
        drillDown: {
          enabled: false,
          levels: [],
        },
      },
      layout: {
        x: 0,
        y: Infinity, // Puts it at the bottom
        w: type === 'kpi' ? 3 : 6,
        h: type === 'kpi' ? 2 : 4,
        minW: 2,
        minH: 2,
      },
    };

    const updated = {
      ...currentDashboard,
      widgets: [...currentDashboard.widgets, newWidget],
      updatedAt: new Date(),
    };

    setCurrentDashboard(updated);
  }, [currentDashboard]);

  const updateWidget = useCallback((id: string, updates: Partial<Widget>) => {
    if (!currentDashboard) return;

    const updated = {
      ...currentDashboard,
      widgets: currentDashboard.widgets.map(w =>
        w.id === id ? { ...w, ...updates } : w
      ),
      updatedAt: new Date(),
    };

    setCurrentDashboard(updated);
  }, [currentDashboard]);

  const deleteWidget = useCallback((id: string) => {
    if (!currentDashboard) return;

    const updated = {
      ...currentDashboard,
      widgets: currentDashboard.widgets.filter(w => w.id !== id),
      updatedAt: new Date(),
    };

    setCurrentDashboard(updated);
    if (selectedWidget?.id === id) {
      setSelectedWidget(null);
    }
  }, [currentDashboard, selectedWidget]);

  const selectWidget = useCallback((id: string | null) => {
    if (!id) {
      setSelectedWidget(null);
      return;
    }

    const widget = currentDashboard?.widgets.find(w => w.id === id);
    if (widget) {
      setSelectedWidget(widget);
    }
  }, [currentDashboard]);

  const duplicateWidget = useCallback((id: string) => {
    if (!currentDashboard) return;

    const widget = currentDashboard.widgets.find(w => w.id === id);
    if (!widget) return;

    const newWidget: Widget = {
      ...widget,
      id: `widget-${Date.now()}`,
      layout: {
        ...widget.layout,
        y: Infinity, // Puts it at the bottom
      },
    };

    const updated = {
      ...currentDashboard,
      widgets: [...currentDashboard.widgets, newWidget],
      updatedAt: new Date(),
    };

    setCurrentDashboard(updated);
  }, [currentDashboard]);

  const updateWidgetLayout = useCallback((layouts: Array<{ i: string; x: number; y: number; w: number; h: number }>) => {
    if (!currentDashboard) return;

    const updated = {
      ...currentDashboard,
      widgets: currentDashboard.widgets.map(widget => {
        const layout = layouts.find(l => l.i === widget.id);
        if (layout) {
          return {
            ...widget,
            layout: {
              ...widget.layout,
              x: layout.x,
              y: layout.y,
              w: layout.w,
              h: layout.h,
            },
          };
        }
        return widget;
      }),
      updatedAt: new Date(),
    };

    setCurrentDashboard(updated);
  }, [currentDashboard]);

  const updateGlobalColorScheme = useCallback((colorScheme: WidgetColorScheme) => {
    if (!currentDashboard) return;

    const updated = {
      ...currentDashboard,
      globalColorScheme: colorScheme,
      updatedAt: new Date(),
    };

    setCurrentDashboard(updated);
  }, [currentDashboard]);

  const updateWidgetColorScheme = useCallback((id: string, colorScheme: WidgetColorScheme) => {
    if (!currentDashboard) return;

    const updated = {
      ...currentDashboard,
      widgets: currentDashboard.widgets.map(w =>
        w.id === id
          ? { ...w, config: { ...w.config, colorScheme } }
          : w
      ),
      updatedAt: new Date(),
    };

    setCurrentDashboard(updated);
  }, [currentDashboard]);

  const toggleEditMode = useCallback(() => {
    setIsEditMode(prev => !prev);
  }, []);

  return (
    <DashboardBuilderContext.Provider
      value={{
        currentDashboard,
        dashboards,
        selectedWidget,
        isEditMode,
        createDashboard,
        loadDashboard,
        saveDashboard,
        deleteDashboard,
        updateDashboard,
        addWidget,
        updateWidget,
        deleteWidget,
        selectWidget,
        duplicateWidget,
        updateWidgetLayout,
        updateGlobalColorScheme,
        updateWidgetColorScheme,
        toggleEditMode,
      }}
    >
      {children}
    </DashboardBuilderContext.Provider>
  );
}

export function useDashboardBuilder() {
  const context = useContext(DashboardBuilderContext);
  if (context === undefined) {
    throw new Error('useDashboardBuilder must be used within a DashboardBuilderProvider');
  }
  return context;
}
