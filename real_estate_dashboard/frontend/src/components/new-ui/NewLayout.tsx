import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Building2, TrendingUp, DollarSign, BarChart3, Settings,
  Search, Sun, Moon, Menu, X, Command, Home, Radio, Calculator
} from 'lucide-react';
import { useAppTheme } from '../../contexts/ThemeContext';
import { CommandPalette } from './CommandPalette';
import { CompanySelector } from '../common/CompanySelector';
import { GlobalContextBar } from './GlobalContextBar';
import { EnhancedNavigation } from './EnhancedNavigation';
import { WorkspaceSidebar } from './WorkspaceSidebar';
import { UIToggle } from '../UIToggle';
import { Box } from '@mui/material';

type Workspace = 'main' | 'operate' | 'modeling' | 'invest' | 'capital' | 'analytics' | 'realtime' | 'admin';

interface WorkspaceConfig {
  id: Workspace;
  label: string;
  icon: any;
  color: string;
  routes: string[];
}

const workspaces: WorkspaceConfig[] = [
  {
    id: 'main',
    label: 'Main Dashboard',
    icon: Home,
    color: 'indigo',
    routes: ['/main-dashboard']
  },
  {
    id: 'operate',
    label: 'Operate',
    icon: Building2,
    color: 'blue',
    routes: ['/command-center', '/platform-overview', '/operate-summary', '/property-management', '/accounting', '/operate-intelligence', '/project-tracking']
  },
  {
    id: 'modeling',
    label: 'Modeling & Analysis',
    icon: Calculator,
    color: 'violet',
    routes: [
      '/real-estate-models',
      '/real-estate-tools',
      '/real-estate-models/fix-and-flip',
      '/real-estate-models/single-family-rental',
      '/real-estate-models/small-multifamily',
      '/real-estate-models/extended-multifamily',
      '/real-estate-models/hotel',
      '/real-estate-models/mixed-use',
      '/real-estate-models/subdivision',
      '/real-estate-models/small-multifamily-acquisition',
      '/real-estate-models/lease-analyzer',
      '/real-estate-models/renovation-budget',
      '/financial-models',
      '/financial-models/dcf',
      '/financial-models/lbo',
      '/financial-models/merger',
      '/financial-models/dd',
      '/financial-models/comps'
    ]
  },
  {
    id: 'invest',
    label: 'Invest & Deals',
    icon: TrendingUp,
    color: 'emerald',
    routes: [
      '/crm/deals',
      '/market-intelligence'
    ]
  },
  {
    id: 'capital',
    label: 'Capital & Structure',
    icon: DollarSign,
    color: 'purple',
    routes: [
      '/fund-management',
      '/debt-management',
      '/tax-strategy',
      '/real-estate-models/tax-strategy',
      '/legal-services',
      '/legal-services/compliance',
      '/capital-analysis'
    ]
  },
  {
    id: 'analytics',
    label: 'Analytics & Reporting',
    icon: BarChart3,
    color: 'cyan',
    routes: ['/portfolio-dashboard', '/reports', '/saved-reports', '/pdf-extraction']
  },
  {
    id: 'realtime',
    label: 'Real-Time Data',
    icon: Radio,
    color: 'teal',
    routes: ['/real-time-data', '/market-intelligence', '/integrations']
  },
  {
    id: 'admin',
    label: 'Admin',
    icon: Settings,
    color: 'amber',
    routes: [
      '/admin/users-roles',
      '/admin/audit-log',
      '/admin/companies',
      '/admin/api-integrations',
      '/admin/system-settings'
    ]
  },
];

interface NewLayoutProps {
  children: React.ReactNode;
}

export function NewLayout({ children }: NewLayoutProps) {
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { theme, toggleTheme } = useAppTheme();
  const navigate = useNavigate();
  const location = useLocation();

  // Determine active workspace based on current route
  const activeWorkspace = workspaces.find(ws =>
    ws.routes.some(route => location.pathname.startsWith(route))
  )?.id || 'main';

  // Handle Cmd+K / Ctrl+K for command palette
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const getWorkspaceColor = (workspace: string, shade: number = 500) => {
    const colorMap: Record<string, string> = {
      indigo: theme === 'dark' ? `bg-indigo-${shade}/20` : `bg-indigo-${shade}/10`,
      blue: theme === 'dark' ? `bg-blue-${shade}/20` : `bg-blue-${shade}/10`,
      violet: theme === 'dark' ? `bg-violet-${shade}/20` : `bg-violet-${shade}/10`,
      emerald: theme === 'dark' ? `bg-emerald-${shade}/20` : `bg-emerald-${shade}/10`,
      purple: theme === 'dark' ? `bg-purple-${shade}/20` : `bg-purple-${shade}/10`,
      cyan: theme === 'dark' ? `bg-cyan-${shade}/20` : `bg-cyan-${shade}/10`,
      teal: theme === 'dark' ? `bg-teal-${shade}/20` : `bg-teal-${shade}/10`,
      amber: theme === 'dark' ? `bg-amber-${shade}/20` : `bg-amber-${shade}/10`,
    };
    return colorMap[workspace] || '';
  };

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-slate-950' : 'bg-slate-50'}`}>
      {/* Top Header */}
      <header className={`${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'} border-b sticky top-0 z-40`}>
        <div className="px-6 h-16 flex items-center justify-between">
          {/* Left: Logo & Workspace Switcher */}
          <div className="flex items-center gap-4">
            {/* Mobile Menu Toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-lg hover:bg-slate-800/50"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>

            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <Building2 className="w-5 h-5 text-white" />
              </div>
              <div className="hidden sm:block">
                <div className={`text-sm font-bold ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>
                  RE Capital
                </div>
                <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-600'}`}>
                  Analytics Platform
                </div>
              </div>
            </div>

            {/* Workspace Switcher */}
            <div className="hidden lg:flex items-center gap-1 ml-4 p-1 rounded-lg bg-slate-800/30">
              {workspaces.map((ws) => {
                const isActive = activeWorkspace === ws.id;
                const Icon = ws.icon;
                return (
                  <button
                    key={ws.id}
                    onClick={() => {
                      if (ws.routes[0]) navigate(ws.routes[0]);
                    }}
                    className={`
                      flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-all
                      ${isActive
                        ? theme === 'dark'
                          ? 'bg-slate-700 text-white shadow-sm'
                          : 'bg-white text-slate-900 shadow-sm'
                        : theme === 'dark'
                          ? 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                      }
                    `}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{ws.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Right: Actions */}
          <div className="flex items-center gap-3">
            {/* Command Palette Trigger */}
            <button
              onClick={() => setCommandPaletteOpen(true)}
              className={`hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg border transition-colors ${
                theme === 'dark'
                  ? 'bg-slate-800/50 border-slate-700 hover:bg-slate-800 text-slate-400 hover:text-white'
                  : 'bg-slate-100 border-slate-200 hover:bg-white text-slate-600 hover:text-slate-900'
              }`}
            >
              <Search className="w-4 h-4" />
              <span className="text-sm">Search...</span>
              <kbd className={`ml-2 px-1.5 py-0.5 text-xs rounded ${theme === 'dark' ? 'bg-slate-700 text-slate-400' : 'bg-white text-slate-600'}`}>
                ⌘K
              </kbd>
            </button>

            {/* Mobile Command Palette */}
            <button
              onClick={() => setCommandPaletteOpen(true)}
              className="md:hidden p-2 rounded-lg hover:bg-slate-800/50"
            >
              <Search className="w-5 h-5" />
            </button>

            {/* Company Selector */}
            <Box sx={{ '& > *': { color: theme === 'dark' ? 'white' : 'inherit' } }}>
              <CompanySelector />
            </Box>

            {/* UI Toggle */}
            <Box sx={{ '& > *': { color: theme === 'dark' ? 'white' : 'inherit' } }}>
              <UIToggle />
            </Box>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg transition-colors ${
                theme === 'dark'
                  ? 'hover:bg-slate-800 text-slate-400 hover:text-white'
                  : 'hover:bg-slate-100 text-slate-600 hover:text-slate-900'
              }`}
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Workspace Switcher */}
        {mobileMenuOpen && (
          <div className={`lg:hidden border-t ${theme === 'dark' ? 'border-slate-800 bg-slate-900/95' : 'border-slate-200 bg-white'} p-4`}>
            <div className="space-y-2">
              {workspaces.map((ws) => {
                const isActive = activeWorkspace === ws.id;
                const Icon = ws.icon;
                return (
                  <button
                    key={ws.id}
                    onClick={() => {
                      if (ws.routes[0]) navigate(ws.routes[0]);
                      setMobileMenuOpen(false);
                    }}
                    className={`
                      w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all
                      ${isActive
                        ? theme === 'dark'
                          ? 'bg-slate-800 text-white'
                          : 'bg-slate-100 text-slate-900'
                        : theme === 'dark'
                          ? 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                      }
                    `}
                  >
                    <Icon className="w-5 h-5" />
                    {ws.label}
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </header>

      {/* Global Context Bar */}
      <GlobalContextBar />

      {/* Enhanced Navigation with Model Dropdowns */}
      <EnhancedNavigation activeWorkspace={activeWorkspace} />

      {/* Main Content Area with Sidebar */}
      <div className="flex min-h-screen">
        {/* Left Sidebar */}
        <WorkspaceSidebar activeWorkspace={activeWorkspace} />

        {/* Main Content */}
        <main className="flex-1">
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>

      {/* Command Palette */}
      <CommandPalette
        isOpen={commandPaletteOpen}
        onClose={() => setCommandPaletteOpen(false)}
      />

      {/* Footer */}
      <footer className={`mt-12 border-t ${theme === 'dark' ? 'border-slate-800 bg-slate-900/50' : 'border-slate-200 bg-white'} py-6`}>
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between">
            <div className={`text-sm ${theme === 'dark' ? 'text-slate-500' : 'text-slate-600'}`}>
              <span className="flex items-center gap-2">
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  Live
                </span>
                <span className="text-slate-600">·</span>
                <span>v2.4.1</span>
              </span>
            </div>
            <div className={`text-xs ${theme === 'dark' ? 'text-slate-600' : 'text-slate-500'}`}>
              Press <kbd className={`px-1.5 py-0.5 rounded ${theme === 'dark' ? 'bg-slate-800' : 'bg-slate-100'}`}><Command className="w-3 h-3 inline" />K</kbd> to search
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
