import { useNavigate, useLocation } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import {
  Home, Building2, TrendingUp, DollarSign, BarChart3, Settings,
  FileText, Calculator, Briefcase, PieChart, Landmark, Scale,
  Wrench, Hotel, Users, Calendar, Target, Radio, Activity,
  Database, BookOpen, Globe, Map, LineChart, Package,
  Shield, FileCheck, Layers, Command, Bell
} from 'lucide-react';

type Workspace = 'main' | 'operate' | 'modeling' | 'invest' | 'capital' | 'analytics' | 'realtime' | 'admin';

interface MenuItem {
  label: string;
  path: string;
  icon: any;
}

interface MenuSection {
  header?: string;
  items: MenuItem[];
}

interface WorkspaceSidebarConfig {
  [key: string]: MenuSection[];
}

const sidebarConfig: WorkspaceSidebarConfig = {
  main: [
    {
      items: [
        { label: 'Command Center', path: '/', icon: Command },
        { label: 'README', path: '/readme', icon: FileText },
      ]
    },
    {
      header: 'DASHBOARD',
      items: [
        { label: 'Overview', path: '/', icon: Home },
        { label: 'Main Dashboard', path: '/dashboard', icon: BarChart3 },
      ]
    }
  ],

  operate: [
    {
      items: [
        { label: 'Command Center', path: '/command-center', icon: Command },
        { label: 'README', path: '/readme', icon: FileText },
      ]
    },
    {
      header: 'OPERATE',
      items: [
        { label: 'Overview', path: '/operate-summary', icon: Home },
      ]
    },
    {
      header: 'Property Management',
      items: [
        { label: 'Property Management', path: '/property-management', icon: Building2 },
      ]
    },
    {
      header: 'Leasing',
      items: [
        { label: 'Leases & Tenants', path: '/leases', icon: Users },
      ]
    },
    {
      header: 'Operations',
      items: [
        { label: 'Maintenance', path: '/maintenance', icon: Wrench },
      ]
    },
    {
      header: 'Accounting & Bookkeeping',
      items: [
        { label: 'Accounting', path: '/accounting', icon: DollarSign },
      ]
    },
    {
      header: 'Market Data',
      items: [
        { label: 'Market Snapshot', path: '/market-intelligence?workspace=operate', icon: Activity },
      ]
    }
  ],

  modeling: [
    {
      header: 'MODELING & ANALYSIS',
      items: [
        { label: 'Overview', path: '/real-estate-models', icon: Home },
      ]
    },
    {
      header: 'Real Estate Models',
      items: [
        { label: 'Fix & Flip', path: '/real-estate-models/fix-and-flip', icon: Wrench },
        { label: 'Single Family Rental', path: '/real-estate-models/single-family-rental', icon: Home },
        { label: 'Small Multifamily', path: '/real-estate-models/small-multifamily', icon: Building2 },
        { label: 'Extended Multifamily', path: '/real-estate-models/extended-multifamily', icon: Building2 },
        { label: 'Hotel Development', path: '/real-estate-models/hotel', icon: Hotel },
        { label: 'Mixed-Use', path: '/real-estate-models/mixed-use', icon: Building2 },
        { label: 'Subdivision', path: '/real-estate-models/subdivision', icon: TrendingUp },
        { label: 'Small MF Acquisition', path: '/real-estate-models/small-multifamily-acquisition', icon: Building2 },
      ]
    },
    {
      header: 'Analysis Tools',
      items: [
        { label: 'Lease Analyzer', path: '/real-estate-models/lease-analyzer', icon: FileText },
        { label: 'Renovation Budget', path: '/real-estate-models/renovation-budget', icon: Wrench },
      ]
    },
    {
      header: 'Financial Models',
      items: [
        { label: 'DCF Valuation', path: '/financial-models/dcf', icon: Calculator },
        { label: 'LBO Analysis', path: '/financial-models/lbo', icon: Briefcase },
        { label: 'M&A Models', path: '/financial-models/merger', icon: TrendingUp },
        { label: 'Due Diligence', path: '/financial-models/dd', icon: FileText },
        { label: 'Comparable Analysis', path: '/financial-models/comps', icon: PieChart },
      ]
    },
    {
      header: 'Saved Work',
      items: [
        { label: 'Saved Calculations', path: '/saved-calculations', icon: FileCheck },
      ]
    },
    {
      header: 'Market Data',
      items: [
        { label: 'Market Snapshot', path: '/market-intelligence?workspace=modeling', icon: Activity },
      ]
    }
  ],

  invest: [
    {
      header: 'INVEST & UNDERWRITE',
      items: [
        { label: 'Overview', path: '/invest-overview', icon: Home },
      ]
    },
    {
      header: 'Deals',
      items: [
        { label: 'Deal Pipeline & CRM', path: '/crm/deals', icon: Target },
      ]
    },
    {
      header: 'Models',
      items: [
        { label: 'Real Estate Models', path: '/real-estate-models', icon: Building2 },
        { label: 'Institutional Models', path: '/financial-models', icon: Briefcase },
        { label: 'Saved Calculations', path: '/saved-calculations', icon: FileCheck },
      ]
    },
    {
      header: 'Data',
      items: [
        { label: 'PDF Extraction', path: '/pdf-extraction', icon: FileText },
        { label: 'Market Intelligence', path: '/market-intelligence', icon: Globe },
      ]
    },
    {
      header: 'Shared Market',
      items: [
        { label: 'Market Snapshot', path: '/market-intelligence?workspace=invest', icon: Activity },
      ]
    }
  ],

  capital: [
    {
      header: 'CAPITAL & STRUCTURE',
      items: [
        { label: 'Overview', path: '/capital-overview', icon: Home },
      ]
    },
    {
      header: 'Capital',
      items: [
        { label: 'Fund Management', path: '/fund-management', icon: Landmark },
        { label: 'Debt Management', path: '/debt-management', icon: DollarSign },
      ]
    },
    {
      header: 'Tax & Compliance',
      items: [
        { label: 'Tax Strategy', path: '/real-estate-models/tax-strategy', icon: Calculator },
        { label: 'Legal & Compliance', path: '/legal-services', icon: Scale },
      ]
    },
    {
      header: 'Shared Market',
      items: [
        { label: 'Market Snapshot', path: '/market-intelligence?workspace=capital', icon: Activity },
      ]
    }
  ],

  analytics: [
    {
      header: 'ANALYTICS & REPORTING',
      items: [
        { label: 'Overview', path: '/analytics-overview', icon: Home },
      ]
    },
    {
      header: 'Portfolio',
      items: [
        { label: 'Portfolio Dashboard', path: '/portfolio-dashboard', icon: PieChart },
        { label: 'Interactive Dashboards', path: '/interactive-dashboards', icon: BarChart3 },
      ]
    },
    {
      header: 'Reporting',
      items: [
        { label: 'Reports Library', path: '/reports', icon: FileText },
      ]
    },
    {
      header: 'Data',
      items: [
        { label: 'Data Integrations', path: '/integrations', icon: Database },
        { label: 'Model Library', path: '/model-templates', icon: BookOpen },
      ]
    },
    {
      header: 'Shared Market',
      items: [
        { label: 'Market Snapshot', path: '/market-intelligence?workspace=analytics', icon: Activity },
      ]
    }
  ],

  realtime: [
    {
      header: 'REAL-TIME DATA',
      items: [
        { label: 'Overview', path: '/real-time-data', icon: Home },
      ]
    },
    {
      header: 'Market Data',
      items: [
        { label: 'System Health', path: '/real-time-data', icon: Activity },
        { label: 'Market Intelligence', path: '/market-intelligence', icon: Globe },
        { label: 'Market Snapshot', path: '/market-intelligence?workspace=realtime', icon: LineChart },
      ]
    },
    {
      header: 'Integrations',
      items: [
        { label: 'Data Integrations', path: '/integrations', icon: Database },
        { label: 'Integration Status', path: '/integration-status', icon: Radio },
      ]
    }
  ],

  admin: [
    {
      header: 'ADMIN',
      items: [
        { label: 'Overview', path: '/admin-overview', icon: Home },
      ]
    },
    {
      header: 'Project Management',
      items: [
        { label: 'Project Tracking', path: '/project-tracking', icon: Calendar },
      ]
    },
    {
      header: 'Document Processing',
      items: [
        { label: 'PDF Extraction', path: '/pdf-extraction', icon: FileText },
      ]
    },
    {
      header: 'Legal & Compliance',
      items: [
        { label: 'Legal Services', path: '/legal-services', icon: Scale },
      ]
    },
    {
      header: 'System',
      items: [
        { label: 'Settings', path: '/settings', icon: Settings },
        { label: 'Notifications', path: '/notifications', icon: Bell },
      ]
    },
    {
      header: 'Market Data',
      items: [
        { label: 'Market Snapshot', path: '/market-intelligence?workspace=admin', icon: Activity },
      ]
    }
  ]
};

interface WorkspaceSidebarProps {
  activeWorkspace: Workspace;
}

export function WorkspaceSidebar({ activeWorkspace }: WorkspaceSidebarProps) {
  const { theme } = useAppTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const sections = sidebarConfig[activeWorkspace] || [];

  return (
    <div className={`w-64 ${theme === 'dark' ? 'bg-slate-900/50' : 'bg-white'} border-r ${theme === 'dark' ? 'border-slate-800' : 'border-slate-200'} h-full overflow-y-auto`}>
      <div className="py-4">
        {sections.map((section, idx) => (
          <div key={idx} className="mb-6">
            {section.header && (
              <div className={`px-6 mb-2 text-xs font-semibold tracking-wider ${theme === 'dark' ? 'text-slate-500' : 'text-slate-400'}`}>
                {section.header}
              </div>
            )}
            <div className="space-y-0.5 px-3">
              {section.items.map((item) => {
                const isActive = location.pathname === item.path;
                const Icon = item.icon;

                return (
                  <button
                    key={item.path}
                    onClick={() => navigate(item.path)}
                    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                      isActive
                        ? theme === 'dark'
                          ? 'bg-blue-500/20 text-blue-400 font-medium'
                          : 'bg-blue-50 text-blue-700 font-medium'
                        : theme === 'dark'
                        ? 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                        : 'text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    <Icon className="w-4 h-4 flex-shrink-0" />
                    <span className="truncate">{item.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
