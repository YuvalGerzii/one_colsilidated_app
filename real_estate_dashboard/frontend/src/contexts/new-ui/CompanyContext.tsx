import { createContext, useContext, useState, ReactNode } from 'react';

export interface Company {
  id: string;
  name: string;
  shortName: string;
  logo: string;
  brandColor: {
    primary: string;
    secondary: string;
    gradient: string;
  };
}

const companies: Company[] = [
  {
    id: 'abc-properties',
    name: 'ABC Properties LLC',
    shortName: 'ABC Properties',
    logo: '🏢',
    brandColor: {
      primary: 'blue',
      secondary: 'cyan',
      gradient: 'from-blue-500 via-blue-600 to-cyan-600'
    }
  },
  {
    id: 'xyz-real-estate',
    name: 'XYZ Real Estate',
    shortName: 'XYZ Realty',
    logo: '🏗️',
    brandColor: {
      primary: 'emerald',
      secondary: 'teal',
      gradient: 'from-emerald-500 via-emerald-600 to-teal-600'
    }
  },
  {
    id: 'metro-investments',
    name: 'Metro Investments',
    shortName: 'Metro Capital',
    logo: '🌆',
    brandColor: {
      primary: 'purple',
      secondary: 'indigo',
      gradient: 'from-purple-500 via-purple-600 to-indigo-600'
    }
  },
  {
    id: 'summit-holdings',
    name: 'Summit Holdings Group',
    shortName: 'Summit Holdings',
    logo: '⛰️',
    brandColor: {
      primary: 'amber',
      secondary: 'orange',
      gradient: 'from-amber-500 via-amber-600 to-orange-600'
    }
  },
  {
    id: 'coastal-partners',
    name: 'Coastal Partners LP',
    shortName: 'Coastal Partners',
    logo: '🌊',
    brandColor: {
      primary: 'sky',
      secondary: 'blue',
      gradient: 'from-sky-500 via-sky-600 to-blue-600'
    }
  }
];

interface CompanyContextType {
  currentCompany: Company;
  companies: Company[];
  setCompany: (companyId: string) => void;
}

const CompanyContext = createContext<CompanyContextType | undefined>(undefined);

export function CompanyProvider({ children }: { children: ReactNode }) {
  const [currentCompany, setCurrentCompany] = useState<Company>(companies[0]);

  const setCompany = (companyId: string) => {
    const company = companies.find(c => c.id === companyId);
    if (company) {
      setCurrentCompany(company);
    }
  };

  return (
    <CompanyContext.Provider value={{ currentCompany, companies, setCompany }}>
      {children}
    </CompanyContext.Provider>
  );
}

export function useCompany() {
  const context = useContext(CompanyContext);
  if (context === undefined) {
    throw new Error('useCompany must be used within a CompanyProvider');
  }
  return context;
}
