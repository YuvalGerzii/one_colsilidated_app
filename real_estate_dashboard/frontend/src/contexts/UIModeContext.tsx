import React, { createContext, useContext, useState, ReactNode } from 'react';

type UIMode = 'old' | 'new';

interface UIModeContextType {
  uiMode: UIMode;
  setUIMode: (mode: UIMode) => void;
  toggleUIMode: () => void;
}

const UIModeContext = createContext<UIModeContextType | undefined>(undefined);

export function UIModeProvider({ children }: { children: ReactNode }) {
  const [uiMode, setUIMode] = useState<UIMode>(() => {
    // Check localStorage for saved preference
    const saved = localStorage.getItem('uiMode');
    return (saved === 'new' || saved === 'old') ? saved : 'new';
  });

  const handleSetUIMode = (mode: UIMode) => {
    setUIMode(mode);
    localStorage.setItem('uiMode', mode);
  };

  const toggleUIMode = () => {
    const newMode = uiMode === 'old' ? 'new' : 'old';
    handleSetUIMode(newMode);
  };

  return (
    <UIModeContext.Provider value={{ uiMode, setUIMode: handleSetUIMode, toggleUIMode }}>
      {children}
    </UIModeContext.Provider>
  );
}

export function useUIMode() {
  const context = useContext(UIModeContext);
  if (context === undefined) {
    throw new Error('useUIMode must be used within a UIModeProvider');
  }
  return context;
}
