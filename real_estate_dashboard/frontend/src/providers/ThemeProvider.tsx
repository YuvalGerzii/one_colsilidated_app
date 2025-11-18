import { useEffect } from 'react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';
import { useAppTheme } from '../contexts/ThemeContext';

export function TailwindThemeSync({ children }: { children: React.ReactNode }) {
  const { theme } = useAppTheme();

  useEffect(() => {
    // Sync MUI theme with Tailwind dark mode
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  return <>{children}</>;
}

export function TailwindThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <TailwindThemeSync>
        {children}
      </TailwindThemeSync>
    </NextThemesProvider>
  );
}
