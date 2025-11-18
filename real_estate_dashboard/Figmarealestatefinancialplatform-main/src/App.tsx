import { useState } from 'react';
import { Building2, Home, BarChart3, TrendingUp, Sun, Moon, LayoutGrid } from 'lucide-react';
import { PropertyManagement } from './components/PropertyManagement';
import { RealEstateModels } from './components/RealEstateModels';
import { Dashboard } from './components/Dashboard';
import { DashboardBuilder } from './components/dashboard-builder/DashboardBuilder';
import { ThemeProvider, useTheme } from './contexts/ThemeContext';
import { DashboardBuilderProvider } from './contexts/DashboardBuilderContext';

function AppContent() {
  const [currentView, setCurrentView] = useState<'home' | 'property' | 'models' | 'builder'>('home');
  const { theme, toggleTheme, colors } = useTheme();

  return (
    <div className={`flex h-screen ${theme === 'dark' ? 'bg-[#0a0e17]' : 'bg-white'}`}>
      {/* Sidebar */}
      <aside className={`w-64 ${theme === 'dark' ? 'bg-gradient-to-b from-[#0f1419] to-[#0a0e17]' : 'bg-gradient-to-b from-white to-blue-50'} border-r ${colors.border.primary} flex flex-col relative overflow-hidden shadow-sm`}>
        {/* Decorative gradient */}
        <div className={`absolute inset-0 ${theme === 'dark' ? 'bg-gradient-to-b from-blue-600/5 via-transparent to-transparent' : 'bg-gradient-to-b from-blue-50 via-transparent to-transparent'} pointer-events-none`} />
        
        {/* Logo/Brand */}
        <div className={`p-6 border-b ${colors.border.primary} relative z-10`}>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-11 h-11 bg-gradient-to-br from-blue-500 via-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20 relative">
              <div className="absolute inset-0 bg-gradient-to-t from-white/20 to-transparent rounded-xl" />
              <Building2 className="w-6 h-6 text-white relative z-10" />
            </div>
            <div>
              <div className={`text-lg ${colors.text.primary}`}>RE Capital</div>
              <div className={`text-xs ${colors.text.secondary}`}>Analytics Platform</div>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 relative z-10">
          <div className={`text-xs uppercase tracking-wider ${colors.text.tertiary} mb-3 px-3`}>Navigation</div>
          <button
            onClick={() => setCurrentView('home')}
            className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all relative group ${
              currentView === 'home'
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-500/30'
                : `${colors.text.secondary} hover:${colors.text.primary} ${theme === 'dark' ? 'hover:bg-slate-800/40' : 'hover:bg-slate-100'}`
            }`}
          >
            {currentView === 'home' && (
              <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent rounded-xl" />
            )}
            <Home className="w-4 h-4 relative z-10" />
            <span className="text-sm relative z-10">Dashboard</span>
            {currentView === 'home' && (
              <div className="ml-auto w-1.5 h-1.5 bg-green-400 rounded-full shadow-lg shadow-green-400/50" />
            )}
          </button>

          <button
            onClick={() => setCurrentView('property')}
            className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl mt-1.5 transition-all relative group ${
              currentView === 'property'
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-500/30'
                : `${colors.text.secondary} hover:${colors.text.primary} ${theme === 'dark' ? 'hover:bg-slate-800/40' : 'hover:bg-slate-100'}`
            }`}
          >
            {currentView === 'property' && (
              <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent rounded-xl" />
            )}
            <Building2 className="w-4 h-4 relative z-10" />
            <span className="text-sm relative z-10">Portfolio</span>
            {currentView === 'property' && (
              <div className="ml-auto w-1.5 h-1.5 bg-green-400 rounded-full shadow-lg shadow-green-400/50" />
            )}
          </button>

          <button
            onClick={() => setCurrentView('models')}
            className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl mt-1.5 transition-all relative group ${
              currentView === 'models'
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-500/30'
                : `${colors.text.secondary} hover:${colors.text.primary} ${theme === 'dark' ? 'hover:bg-slate-800/40' : 'hover:bg-slate-100'}`
            }`}
          >
            {currentView === 'models' && (
              <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent rounded-xl" />
            )}
            <BarChart3 className="w-4 h-4 relative z-10" />
            <span className="text-sm relative z-10">Financial Models</span>
            {currentView === 'models' && (
              <div className="ml-auto w-1.5 h-1.5 bg-green-400 rounded-full shadow-lg shadow-green-400/50" />
            )}
          </button>

          <button
            onClick={() => setCurrentView('builder')}
            className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl mt-1.5 transition-all relative group ${
              currentView === 'builder'
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg shadow-blue-500/30'
                : `${colors.text.secondary} hover:${colors.text.primary} ${theme === 'dark' ? 'hover:bg-slate-800/40' : 'hover:bg-slate-100'}`
            }`}
          >
            {currentView === 'builder' && (
              <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent rounded-xl" />
            )}
            <LayoutGrid className="w-4 h-4 relative z-10" />
            <span className="text-sm relative z-10">Dashboard Builder</span>
            {currentView === 'builder' && (
              <div className="ml-auto w-1.5 h-1.5 bg-green-400 rounded-full shadow-lg shadow-green-400/50" />
            )}
          </button>

          {/* Market Stats */}
          <div className={`mt-8 p-4 ${theme === 'dark' ? 'bg-gradient-to-br from-slate-800/40 to-slate-900/40' : 'bg-slate-50'} rounded-xl border ${colors.border.secondary} backdrop-blur-sm`}>
            <div className={`text-xs ${colors.text.secondary} mb-3`}>Market Pulse</div>
            <div className="space-y-2.5">
              <div className="flex items-center justify-between">
                <span className={`text-xs ${colors.text.tertiary}`}>S&P 500</span>
                <div className="flex items-center gap-1.5">
                  <span className={`text-xs ${colors.text.primary}`}>4,783</span>
                  <TrendingUp className="w-3 h-3 text-green-400" />
                  <span className="text-xs text-green-400">+0.8%</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className={`text-xs ${colors.text.tertiary}`}>10Y Treasury</span>
                <div className="flex items-center gap-1.5">
                  <span className={`text-xs ${colors.text.primary}`}>4.15%</span>
                  <span className="text-xs text-red-400">-0.02</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className={`text-xs ${colors.text.tertiary}`}>Cap Rate Avg</span>
                <div className="flex items-center gap-1.5">
                  <span className={`text-xs ${colors.text.primary}`}>6.2%</span>
                  <span className="text-xs text-green-400">↑</span>
                </div>
              </div>
            </div>
          </div>

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className={`mt-4 w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${theme === 'dark' ? 'bg-slate-800/40 hover:bg-slate-800/60' : 'bg-slate-100 hover:bg-slate-200'} ${colors.text.secondary} hover:${colors.text.primary}`}
          >
            {theme === 'dark' ? (
              <>
                <Sun className="w-4 h-4" />
                <span className="text-sm">Light Mode</span>
              </>
            ) : (
              <>
                <Moon className="w-4 h-4" />
                <span className="text-sm">Dark Mode</span>
              </>
            )}
          </button>
        </nav>

        <div className={`p-4 border-t ${colors.border.primary} relative z-10`}>
          <div className={`flex items-center gap-2 text-xs ${colors.text.tertiary}`}>
            <div className="w-2 h-2 bg-green-400 rounded-full shadow-lg shadow-green-400/50 animate-pulse" />
            <span>Live Data</span>
            <span className="ml-auto">v2.4.1</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className={`flex-1 overflow-auto ${theme === 'dark' ? 'bg-gradient-to-br from-[#0a0e17] via-[#0f1419] to-[#0a0e17]' : 'bg-gradient-to-br from-white via-blue-50/30 to-white'}`}>
        {currentView === 'home' && <Dashboard onNavigate={setCurrentView} />}
        {currentView === 'property' && <PropertyManagement />}
        {currentView === 'models' && <RealEstateModels />}
        {currentView === 'builder' && <DashboardBuilder />}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <DashboardBuilderProvider>
        <AppContent />
      </DashboardBuilderProvider>
    </ThemeProvider>
  );
}