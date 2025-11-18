import { ChevronDown, Globe, Calendar, DollarSign, Target } from 'lucide-react';
import { useAppTheme } from '../../contexts/ThemeContext';
import { useGlobalContext } from '../../contexts/GlobalContext';
import { useState, useEffect, useRef } from 'react';

export function GlobalContextBar() {
  const { theme } = useAppTheme();
  const { scope, scopeValue, timePeriod, currency, setScope, setTimePeriod, setCurrency } = useGlobalContext();
  const [showScopeMenu, setShowScopeMenu] = useState(false);
  const [showTimeMenu, setShowTimeMenu] = useState(false);
  const [showCurrencyMenu, setShowCurrencyMenu] = useState(false);

  const scopeRef = useRef<HTMLDivElement>(null);
  const timeRef = useRef<HTMLDivElement>(null);
  const currencyRef = useRef<HTMLDivElement>(null);

  const scopeOptions = [
    { id: 'all', label: 'All Holdings', value: 'All Holdings' },
    { id: 'fund', label: 'Fund III', value: 'Fund III' },
    { id: 'fund', label: 'Fund II', value: 'Fund II' },
    { id: 'asset-type', label: 'Real Estate', value: 'Real Estate' },
    { id: 'asset-type', label: 'Stocks & Securities', value: 'Stocks & Securities' },
    { id: 'country', label: 'United States', value: 'United States' },
    { id: 'country', label: 'Europe', value: 'Europe' },
    { id: 'country', label: 'Asia Pacific', value: 'Asia Pacific' },
  ];

  const timeOptions = [
    { id: 'ytd', label: 'Year to Date' },
    { id: 'quarter', label: 'This Quarter' },
    { id: 'month', label: 'This Month' },
    { id: 'year', label: 'This Year' },
    { id: 'all-time', label: 'All Time' },
  ];

  const currencyOptions = ['USD', 'EUR', 'GBP', 'JPY'];

  const getTimeLabel = () => {
    const option = timeOptions.find(t => t.id === timePeriod);
    return option?.label || 'This Quarter';
  };

  // Close menus when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (scopeRef.current && !scopeRef.current.contains(event.target as Node)) {
        setShowScopeMenu(false);
      }
      if (timeRef.current && !timeRef.current.contains(event.target as Node)) {
        setShowTimeMenu(false);
      }
      if (currencyRef.current && !currencyRef.current.contains(event.target as Node)) {
        setShowCurrencyMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={`${theme === 'dark' ? 'bg-slate-900/60 border-slate-700' : 'bg-slate-50/80 border-slate-200'} border-b px-8 py-3`}>
      <div className="flex items-center gap-6 flex-wrap">
        {/* Scope */}
        <div className="relative" ref={scopeRef}>
          <button
            onClick={() => {
              setShowScopeMenu(!showScopeMenu);
              setShowTimeMenu(false);
              setShowCurrencyMenu(false);
            }}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-colors ${
              theme === 'dark'
                ? 'hover:bg-slate-800/60 text-slate-300 hover:text-white'
                : 'hover:bg-white text-slate-700 hover:text-slate-900'
            }`}
          >
            <Target className="w-4 h-4" />
            <span className="text-sm">Scope:</span>
            <span className={`text-sm font-medium ${theme === 'dark' ? 'text-blue-400' : 'text-blue-700'}`}>
              {scopeValue}
            </span>
            <ChevronDown className="w-3.5 h-3.5" />
          </button>

          {showScopeMenu && (
            <div className={`absolute top-full mt-1 left-0 w-56 ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} border rounded-lg shadow-xl z-50`}>
              <div className="py-1 max-h-64 overflow-y-auto">
                {scopeOptions.map((option, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setScope(option.id as any, option.value);
                      setShowScopeMenu(false);
                    }}
                    className={`w-full text-left px-3 py-2 text-sm transition-colors ${
                      scopeValue === option.value
                        ? theme === 'dark' ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-50 text-blue-700'
                        : theme === 'dark' ? 'text-slate-300 hover:bg-slate-700/60' : 'text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className={`w-px h-5 ${theme === 'dark' ? 'bg-slate-700' : 'bg-slate-300'}`} />

        {/* Time Period */}
        <div className="relative" ref={timeRef}>
          <button
            onClick={() => {
              setShowTimeMenu(!showTimeMenu);
              setShowScopeMenu(false);
              setShowCurrencyMenu(false);
            }}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-colors ${
              theme === 'dark'
                ? 'hover:bg-slate-800/60 text-slate-300 hover:text-white'
                : 'hover:bg-white text-slate-700 hover:text-slate-900'
            }`}
          >
            <Calendar className="w-4 h-4" />
            <span className="text-sm">Time:</span>
            <span className={`text-sm font-medium ${theme === 'dark' ? 'text-purple-400' : 'text-purple-700'}`}>
              {getTimeLabel()}
            </span>
            <ChevronDown className="w-3.5 h-3.5" />
          </button>

          {showTimeMenu && (
            <div className={`absolute top-full mt-1 left-0 w-48 ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} border rounded-lg shadow-xl z-50`}>
              <div className="py-1">
                {timeOptions.map((option) => (
                  <button
                    key={option.id}
                    onClick={() => {
                      setTimePeriod(option.id as any);
                      setShowTimeMenu(false);
                    }}
                    className={`w-full text-left px-3 py-2 text-sm transition-colors ${
                      timePeriod === option.id
                        ? theme === 'dark' ? 'bg-purple-500/10 text-purple-400' : 'bg-purple-50 text-purple-700'
                        : theme === 'dark' ? 'text-slate-300 hover:bg-slate-700/60' : 'text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className={`w-px h-5 ${theme === 'dark' ? 'bg-slate-700' : 'bg-slate-300'}`} />

        {/* Currency */}
        <div className="relative" ref={currencyRef}>
          <button
            onClick={() => {
              setShowCurrencyMenu(!showCurrencyMenu);
              setShowScopeMenu(false);
              setShowTimeMenu(false);
            }}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-colors ${
              theme === 'dark'
                ? 'hover:bg-slate-800/60 text-slate-300 hover:text-white'
                : 'hover:bg-white text-slate-700 hover:text-slate-900'
            }`}
          >
            <DollarSign className="w-4 h-4" />
            <span className="text-sm">Currency:</span>
            <span className={`text-sm font-medium ${theme === 'dark' ? 'text-green-400' : 'text-green-700'}`}>
              {currency}
            </span>
            <ChevronDown className="w-3.5 h-3.5" />
          </button>

          {showCurrencyMenu && (
            <div className={`absolute top-full mt-1 left-0 w-32 ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} border rounded-lg shadow-xl z-50`}>
              <div className="py-1">
                {currencyOptions.map((curr) => (
                  <button
                    key={curr}
                    onClick={() => {
                      setCurrency(curr as any);
                      setShowCurrencyMenu(false);
                    }}
                    className={`w-full text-left px-3 py-2 text-sm transition-colors ${
                      currency === curr
                        ? theme === 'dark' ? 'bg-green-500/10 text-green-400' : 'bg-green-50 text-green-700'
                        : theme === 'dark' ? 'text-slate-300 hover:bg-slate-700/60' : 'text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    {curr}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
