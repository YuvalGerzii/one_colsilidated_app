import React, { createContext, useContext, useState, ReactNode } from 'react';

type ScopeType = 'all' | 'fund' | 'asset-type' | 'country' | 'strategy';
type TimePeriod = 'ytd' | 'quarter' | 'month' | 'year' | 'all-time';
type Currency = 'USD' | 'EUR' | 'GBP' | 'JPY';

interface GlobalContextType {
  scope: ScopeType;
  scopeValue: string;
  timePeriod: TimePeriod;
  currency: Currency;
  setScope: (type: ScopeType, value: string) => void;
  setTimePeriod: (period: TimePeriod) => void;
  setCurrency: (currency: Currency) => void;
}

const GlobalContext = createContext<GlobalContextType | undefined>(undefined);

export function GlobalContextProvider({ children }: { children: ReactNode }) {
  const [scope, setGlobalScope] = useState<ScopeType>('all');
  const [scopeValue, setScopeValue] = useState('All Holdings');
  const [timePeriod, setTimePeriod] = useState<TimePeriod>('quarter');
  const [currency, setCurrency] = useState<Currency>('USD');

  const setScope = (type: ScopeType, value: string) => {
    setGlobalScope(type);
    setScopeValue(value);
  };

  return (
    <GlobalContext.Provider
      value={{
        scope,
        scopeValue,
        timePeriod,
        currency,
        setScope,
        setTimePeriod,
        setCurrency,
      }}
    >
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
