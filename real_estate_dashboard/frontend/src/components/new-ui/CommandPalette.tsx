import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Search, Building2, Briefcase, FileText, Calculator, DollarSign,
  Users, ArrowRight, Home, TrendingUp, PieChart, Gavel, Settings
} from 'lucide-react';
import { useAppTheme } from '../../contexts/ThemeContext';

interface CommandItem {
  id: string;
  type: 'navigation' | 'action';
  label: string;
  sublabel?: string;
  icon: any;
  path?: string;
  action?: () => void;
}

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CommandPalette({ isOpen, onClose }: CommandPaletteProps) {
  const [search, setSearch] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const { theme } = useAppTheme();
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);

  const commands: CommandItem[] = [
    { id: 'home', type: 'navigation', label: 'Dashboard', sublabel: 'Home · Overview', icon: Home, path: '/' },
    { id: 'command-center', type: 'navigation', label: 'Command Center', sublabel: 'Operate · Overview', icon: TrendingUp, path: '/command-center' },
    { id: 'platform-overview', type: 'navigation', label: 'Platform Overview', sublabel: 'Operate · Overview', icon: PieChart, path: '/platform-overview' },
    { id: 'property-mgmt', type: 'navigation', label: 'Property Management', sublabel: 'Operate · Properties', icon: Building2, path: '/property-management' },
    { id: 'deal-pipeline', type: 'navigation', label: 'Deal Pipeline', sublabel: 'Invest · CRM', icon: Briefcase, path: '/crm/deals' },
    { id: 'market-intel', type: 'navigation', label: 'Market Intelligence', sublabel: 'Invest · Market Data', icon: TrendingUp, path: '/market-intelligence' },
    { id: 'portfolio', type: 'navigation', label: 'Portfolio Dashboard', sublabel: 'Analytics · Portfolio', icon: PieChart, path: '/portfolio-dashboard' },
    { id: 'fund-mgmt', type: 'navigation', label: 'Fund Management', sublabel: 'Capital · Funds', icon: DollarSign, path: '/fund-management' },
    { id: 'debt-mgmt', type: 'navigation', label: 'Debt Management', sublabel: 'Capital · Debt', icon: DollarSign, path: '/debt-management' },
    { id: 'legal', type: 'navigation', label: 'Legal Services', sublabel: 'Admin · Legal & Compliance', icon: Gavel, path: '/legal-services' },

    // Real Estate Models
    { id: 'fix-flip', type: 'navigation', label: 'Fix & Flip Calculator', sublabel: 'Models · Real Estate', icon: Calculator, path: '/real-estate-models/fix-and-flip' },
    { id: 'sfr', type: 'navigation', label: 'Single Family Rental', sublabel: 'Models · Real Estate', icon: Calculator, path: '/real-estate-models/single-family-rental' },
    { id: 'small-mf', type: 'navigation', label: 'Small Multifamily', sublabel: 'Models · Real Estate', icon: Calculator, path: '/real-estate-models/small-multifamily' },
    { id: 'high-rise', type: 'navigation', label: 'High-Rise Multifamily', sublabel: 'Models · Real Estate', icon: Calculator, path: '/real-estate-models/extended-multifamily' },
    { id: 'hotel', type: 'navigation', label: 'Hotel Model', sublabel: 'Models · Real Estate', icon: Calculator, path: '/real-estate-models/hotel' },
    { id: 'mixed-use', type: 'navigation', label: 'Mixed-Use Development', sublabel: 'Models · Real Estate', icon: Calculator, path: '/real-estate-models/mixed-use' },
    { id: 'lease-analyzer', type: 'navigation', label: 'Lease Analyzer', sublabel: 'Models · Analysis', icon: FileText, path: '/real-estate-models/lease-analyzer' },

    // Financial Models
    { id: 'dcf', type: 'navigation', label: 'DCF Valuation', sublabel: 'Models · Financial', icon: Calculator, path: '/financial-models/dcf' },
    { id: 'lbo', type: 'navigation', label: 'LBO Model', sublabel: 'Models · Financial', icon: Calculator, path: '/financial-models/lbo' },

    // Other
    { id: 'accounting', type: 'navigation', label: 'Accounting', sublabel: 'Admin · Accounting', icon: DollarSign, path: '/accounting' },
    { id: 'tax', type: 'navigation', label: 'Tax Strategy', sublabel: 'Admin · Tax', icon: FileText, path: '/tax-strategy' },
    { id: 'integrations', type: 'navigation', label: 'Integrations', sublabel: 'Admin · Settings', icon: Settings, path: '/integrations' },
  ];

  // Fuzzy search
  const filteredCommands = commands.filter(cmd => {
    const searchLower = search.toLowerCase();
    return cmd.label.toLowerCase().includes(searchLower) ||
           (cmd.sublabel?.toLowerCase().includes(searchLower) ?? false);
  });

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
      setSearch('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => (prev + 1) % filteredCommands.length);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => (prev - 1 + filteredCommands.length) % filteredCommands.length);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (filteredCommands[selectedIndex]) {
          const cmd = filteredCommands[selectedIndex];
          if (cmd.path) {
            navigate(cmd.path);
          } else if (cmd.action) {
            cmd.action();
          }
          onClose();
        }
      } else if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, selectedIndex, filteredCommands, onClose, navigate]);

  if (!isOpen) return null;

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'navigation': return theme === 'dark' ? 'text-blue-400' : 'text-blue-600';
      case 'action': return theme === 'dark' ? 'text-purple-400' : 'text-purple-600';
      default: return theme === 'dark' ? 'text-slate-400' : 'text-slate-600';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-32 px-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />

      <div
        className={`relative w-full max-w-2xl ${theme === 'dark' ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'} border rounded-xl shadow-2xl overflow-hidden`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search Input */}
        <div className={`flex items-center gap-3 px-4 py-4 border-b ${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'}`}>
          <Search className={`w-5 h-5 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}`} />
          <input
            ref={inputRef}
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search pages, models, tools... (⌘K)"
            className={`flex-1 bg-transparent outline-none text-lg ${theme === 'dark' ? 'text-white placeholder:text-slate-500' : 'text-slate-900 placeholder:text-slate-400'}`}
          />
          <kbd className={`px-2 py-1 text-xs rounded ${theme === 'dark' ? 'bg-slate-800 text-slate-400 border-slate-700' : 'bg-slate-100 text-slate-600 border-slate-300'} border`}>
            ESC
          </kbd>
        </div>

        {/* Results */}
        <div className="max-h-96 overflow-y-auto">
          {filteredCommands.length === 0 ? (
            <div className={`py-12 text-center ${theme === 'dark' ? 'text-slate-500' : 'text-slate-400'}`}>
              <Search className="w-12 h-12 mx-auto mb-3 opacity-40" />
              <p>No results found</p>
            </div>
          ) : (
            <div className="py-2">
              {filteredCommands.map((cmd, index) => (
                <button
                  key={cmd.id}
                  onClick={() => {
                    if (cmd.path) {
                      navigate(cmd.path);
                    } else if (cmd.action) {
                      cmd.action();
                    }
                    onClose();
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-3 transition-colors ${
                    selectedIndex === index
                      ? theme === 'dark' ? 'bg-slate-800/60' : 'bg-blue-50'
                      : theme === 'dark' ? 'hover:bg-slate-800/40' : 'hover:bg-slate-50'
                  }`}
                >
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                    theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-slate-100 border-slate-200'
                  } border`}>
                    <cmd.icon className={`w-4 h-4 ${getTypeColor(cmd.type)}`} />
                  </div>

                  <div className="flex-1 text-left">
                    <div className={`text-sm ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>
                      {cmd.label}
                    </div>
                    {cmd.sublabel && (
                      <div className={`text-xs ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>
                        {cmd.sublabel}
                      </div>
                    )}
                  </div>

                  <ArrowRight className={`w-4 h-4 ${theme === 'dark' ? 'text-slate-600' : 'text-slate-400'} ${selectedIndex === index ? 'opacity-100' : 'opacity-0'}`} />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className={`px-4 py-3 border-t ${theme === 'dark' ? 'border-slate-700 bg-slate-900/50' : 'border-slate-200 bg-slate-50'} flex items-center justify-between`}>
          <div className="flex items-center gap-4 text-xs">
            <div className={`flex items-center gap-1.5 ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>
              <kbd className={`px-1.5 py-0.5 rounded ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-300'} border`}>↑↓</kbd>
              Navigate
            </div>
            <div className={`flex items-center gap-1.5 ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>
              <kbd className={`px-1.5 py-0.5 rounded ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-300'} border`}>↵</kbd>
              Select
            </div>
          </div>
          <div className={`text-xs ${theme === 'dark' ? 'text-slate-600' : 'text-slate-500'}`}>
            {filteredCommands.length} {filteredCommands.length === 1 ? 'result' : 'results'}
          </div>
        </div>
      </div>
    </div>
  );
}
