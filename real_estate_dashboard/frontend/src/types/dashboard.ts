export type WidgetType =
  | 'kpi'
  | 'line-chart'
  | 'bar-chart'
  | 'area-chart'
  | 'pie-chart'
  | 'comparison'
  | 'benchmark'
  | 'metric-list'
  | 'heatmap';

export type DataSource =
  | 'portfolio-value'
  | 'noi'
  | 'occupancy'
  | 'cap-rate'
  | 'cash-flow'
  | 'revenue'
  | 'expenses'
  | 'market-trends'
  | 'property-performance'
  | 'custom';

export interface WidgetColorScheme {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  text: string;
  gradient?: {
    from: string;
    to: string;
  };
}

export interface WidgetConfig {
  title: string;
  dataSource: DataSource;
  customQuery?: string;
  refreshInterval?: number;
  showLegend?: boolean;
  showGrid?: boolean;
  colorScheme?: WidgetColorScheme;
  drillDown?: {
    enabled: boolean;
    levels: string[];
  };
  comparison?: {
    enabled: boolean;
    benchmarkType: 'market' | 'target' | 'previous';
  };
}

export interface Widget {
  id: string;
  type: WidgetType;
  config: WidgetConfig;
  layout: {
    x: number;
    y: number;
    w: number;
    h: number;
    minW?: number;
    minH?: number;
    maxW?: number;
    maxH?: number;
  };
}

export interface Dashboard {
  id: string;
  name: string;
  description?: string;
  widgets: Widget[];
  globalColorScheme?: WidgetColorScheme;
  layout: 'grid' | 'fluid';
  columns: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface DashboardTemplate {
  id: string;
  name: string;
  description: string;
  thumbnail?: string;
  widgets: Omit<Widget, 'id'>[];
  category: 'portfolio' | 'performance' | 'market' | 'custom';
}
