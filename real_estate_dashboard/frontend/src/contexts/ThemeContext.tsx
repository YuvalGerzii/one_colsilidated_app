import { createContext, useContext, useState, ReactNode, useEffect } from 'react';

type AppTheme = 'dark' | 'light';

interface ThemeContextType {
  theme: AppTheme;
  toggleTheme: () => void;
  colors: {
    bg: {
      primary: string;
      secondary: string;
      tertiary: string;
      card: string;
      cardHover: string;
      input: string;
    };
    border: {
      primary: string;
      secondary: string;
    };
    text: {
      primary: string;
      secondary: string;
      tertiary: string;
    };
    accent: {
      blue: string;
      green: string;
      purple: string;
      orange: string;
      red: string;
    };
  };
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const darkTheme = {
  bg: {
    primary: 'bg-[#0a0e17]',
    secondary: 'bg-[#0f1419]',
    tertiary: 'bg-slate-900',
    card: 'bg-gradient-to-br from-slate-800/40 to-slate-900/40',
    cardHover: 'hover:border-slate-600/50',
    input: 'bg-slate-900/50',
  },
  border: {
    primary: 'border-slate-800/50',
    secondary: 'border-slate-700/50',
  },
  text: {
    primary: 'text-white',
    secondary: 'text-slate-400',
    tertiary: 'text-slate-500',
  },
  accent: {
    blue: 'from-blue-600 to-blue-700',
    green: 'from-green-600 to-green-700',
    purple: 'from-purple-600 to-purple-700',
    orange: 'from-orange-600 to-orange-700',
    red: 'from-red-600 to-red-700',
  },
};

const lightTheme = {
  bg: {
    primary: 'bg-white',
    secondary: 'bg-blue-50',
    tertiary: 'bg-blue-100',
    card: 'bg-white',
    cardHover: 'hover:border-blue-300',
    input: 'bg-white',
  },
  border: {
    primary: 'border-blue-100',
    secondary: 'border-blue-200',
  },
  text: {
    primary: 'text-slate-900',
    secondary: 'text-slate-700',
    tertiary: 'text-slate-600',
  },
  accent: {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600',
    red: 'from-red-500 to-red-600',
  },
};

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<AppTheme>('dark');

  useEffect(() => {
    const savedTheme = localStorage.getItem('app-theme') as AppTheme;
    if (savedTheme) {
      setTheme(savedTheme);
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('app-theme', newTheme);
  };

  const colors = theme === 'dark' ? darkTheme : lightTheme;

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, colors }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useAppTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useAppTheme must be used within a ThemeProvider');
  }
  return context;
}

// Export as useTheme for compatibility
export { useAppTheme as useTheme };
