import { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  ChevronDown, Home, Calculator, Building, TrendingUp, Hotel,
  Wrench, FileText, Landmark, Scale, PieChart, Briefcase, DollarSign, Table,
  Activity, Settings as SettingsIcon
} from 'lucide-react';
import { useAppTheme } from '../../contexts/ThemeContext';

interface ModelGroup {
  label: string;
  models: Array<{
    label: string;
    path: string;
    icon: any;
  }>;
}

interface NavConfig {
  workspace: string;
  groups: ModelGroup[];
}

const navConfigs: NavConfig[] = [
  {
    workspace: 'main',
    groups: [] // No dropdown for Main Dashboard
  },
  {
    workspace: 'modeling',
    groups: [
      {
        label: 'Real Estate Models',
        models: [
          { label: 'Fix & Flip', path: '/real-estate-models/fix-and-flip', icon: Wrench },
          { label: 'Single Family Rental', path: '/real-estate-models/single-family-rental', icon: Home },
          { label: 'Small Multifamily', path: '/real-estate-models/small-multifamily', icon: Building },
          { label: 'Extended Multifamily', path: '/real-estate-models/extended-multifamily', icon: Building },
          { label: 'Hotel Development', path: '/real-estate-models/hotel', icon: Hotel },
          { label: 'Mixed-Use', path: '/real-estate-models/mixed-use', icon: Building },
          { label: 'Subdivision', path: '/real-estate-models/subdivision', icon: TrendingUp },
          { label: 'Small MF Acquisition', path: '/real-estate-models/small-multifamily-acquisition', icon: Building },
        ]
      },
      {
        label: 'Analysis Tools',
        models: [
          { label: 'Lease Analyzer', path: '/real-estate-models/lease-analyzer', icon: FileText },
          { label: 'Renovation Budget', path: '/real-estate-models/renovation-budget', icon: Wrench },
        ]
      },
      {
        label: 'Financial Models',
        models: [
          { label: 'DCF Valuation', path: '/financial-models/dcf', icon: Calculator },
          { label: 'LBO Analysis', path: '/financial-models/lbo', icon: Briefcase },
          { label: 'M&A Models', path: '/financial-models/merger', icon: TrendingUp },
          { label: 'Due Diligence', path: '/financial-models/dd', icon: FileText },
          { label: 'Comparable Analysis', path: '/financial-models/comps', icon: PieChart },
        ]
      }
    ]
  },
  {
    workspace: 'invest',
    groups: [] // No dropdown - simplified for deals only
  },
  {
    workspace: 'capital',
    groups: [
      {
        label: 'Capital Models',
        models: [
          { label: 'Tax Strategy', path: '/real-estate-models/tax-strategy', icon: DollarSign },
          { label: 'Fund Management', path: '/fund-management', icon: Landmark },
          { label: 'Debt Management', path: '/debt-management', icon: FileText },
        ]
      }
    ]
  },
  {
    workspace: 'operate',
    groups: [
      {
        label: 'Overview',
        models: [
          { label: 'Command Center', path: '/command-center', icon: TrendingUp },
          { label: 'Platform Overview', path: '/platform-overview', icon: PieChart },
          { label: 'Operations Summary', path: '/operate-summary', icon: Table },
        ]
      },
      {
        label: 'Operations',
        models: [
          { label: 'Property Management', path: '/property-management', icon: Building },
          { label: 'Accounting', path: '/accounting', icon: DollarSign },
        ]
      }
    ]
  },
  {
    workspace: 'analytics',
    groups: [
      {
        label: 'Reporting',
        models: [
          { label: 'Portfolio Dashboard', path: '/portfolio-dashboard', icon: PieChart },
          { label: 'Reports Generator', path: '/reports', icon: FileText },
          { label: 'Saved Reports', path: '/saved-reports', icon: FileText },
        ]
      }
    ]
  },
  {
    workspace: 'realtime',
    groups: [
      {
        label: 'Data Sources',
        models: [
          { label: 'System Health', path: '/real-time-data', icon: Activity },
          { label: 'Market Intelligence', path: '/market-intelligence', icon: TrendingUp },
          { label: 'Integrations', path: '/integrations', icon: SettingsIcon },
        ]
      }
    ]
  },
  {
    workspace: 'admin',
    groups: [
      {
        label: 'Administration',
        models: [
          { label: 'Project Tracking', path: '/project-tracking', icon: FileText },
          { label: 'PDF Extraction', path: '/pdf-extraction', icon: FileText },
          { label: 'Legal Services', path: '/legal-services', icon: Scale },
        ]
      }
    ]
  }
];

interface EnhancedNavigationProps {
  activeWorkspace: string;
}

export function EnhancedNavigation({ activeWorkspace }: EnhancedNavigationProps) {
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const { theme } = useAppTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const dropdownRef = useRef<HTMLDivElement>(null);

  const config = navConfigs.find(c => c.workspace === activeWorkspace);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setOpenDropdown(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (!config || config.groups.length === 0) return null;

  return (
    <div className={`${theme === 'dark' ? 'bg-slate-900/80 border-slate-700' : 'bg-white border-slate-200'} border-b overflow-visible`} ref={dropdownRef}>
      <div className="px-6 h-12 flex items-center gap-1 overflow-x-auto overflow-y-visible">
        {config.groups.map((group) => (
          <div key={group.label} className="relative">
            <button
              onClick={() => setOpenDropdown(openDropdown === group.label ? null : group.label)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                openDropdown === group.label
                  ? theme === 'dark' ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-900'
                  : theme === 'dark'
                  ? 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {group.label}
              <ChevronDown className={`w-4 h-4 transition-transform ${openDropdown === group.label ? 'rotate-180' : ''}`} />
            </button>

            {openDropdown === group.label && (
              <div
                className={`absolute top-full mt-1 left-0 min-w-[240px] ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} border rounded-lg shadow-xl z-50`}
              >
                <div className="py-1">
                  {group.models.map((model) => {
                    const isActive = location.pathname === model.path;
                    const Icon = model.icon;
                    return (
                      <button
                        key={model.path}
                        onClick={() => {
                          navigate(model.path);
                          setOpenDropdown(null);
                        }}
                        className={`w-full text-left px-4 py-2.5 text-sm flex items-center gap-3 transition-colors ${
                          isActive
                            ? theme === 'dark' ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-50 text-blue-700'
                            : theme === 'dark' ? 'text-slate-300 hover:bg-slate-700/60 hover:text-white' : 'text-slate-700 hover:bg-slate-50'
                        }`}
                      >
                        <Icon className="w-4 h-4" />
                        {model.label}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
