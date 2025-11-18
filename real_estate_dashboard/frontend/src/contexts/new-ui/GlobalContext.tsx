import React, { createContext, useContext, useState, ReactNode } from 'react';

export type Scope = 'all' | 'fund' | 'country' | 'strategy';
export type TimePeriod = 'ytd' | 'quarter' | 'month' | 'year' | 'all-time';
export type Currency = 'USD' | 'EUR' | 'GBP' | 'JPY';

interface GlobalContextType {
  scope: Scope;
  scopeValue: string; // e.g., "Fund III", "United States", "Value-Add"
  timePeriod: TimePeriod;
  currency: Currency;
  setScope: (scope: Scope, value: string) => void;
  setTimePeriod: (period: TimePeriod) => void;
  setCurrency: (currency: Currency) => void;
}

const GlobalContext = createContext<GlobalContextType | undefined>(undefined);

export function GlobalContextProvider({ children }: { children: ReactNode }) {
  const [scope, setScope] = useState<Scope>('all');
  const [scopeValue, setScopeValue] = useState<string>('All Holdings');
  const [timePeriod, setTimePeriod] = useState<TimePeriod>('quarter');
  const [currency, setCurrency] = useState<Currency>('USD');

  const handleSetScope = (newScope: Scope, value: string) => {
    setScope(newScope);
    setScopeValue(value);
  };

  return (
    <GlobalContext.Provider value={{
      scope,
      scopeValue,
      timePeriod,
      currency,
      setScope: handleSetScope,
      setTimePeriod,
      setCurrency
    }}>
      {children}
    </GlobalContext.Provider>
  );
}

export function useGlobalContext() {
  const context = useContext(GlobalContext);
  if (context === undefined) {
    throw new Error('useGlobalContext must be used within a GlobalContextProvider');
  }
  return context;
}
