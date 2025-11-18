import React, { createContext, useContext, useState, ReactNode } from 'react';

export type UserRole = 'CEO' | 'CIO' | 'Asset Manager' | 'Fund Manager' | 'Analyst' | 'Controller';

interface RoleContextType {
  role: UserRole;
  setRole: (role: string) => void;
  getDefaultWorkspace: () => string;
  getDefaultModule: () => string;
}

const RoleContext = createContext<RoleContextType | undefined>(undefined);

// Role-based defaults
const roleDefaults: Record<UserRole, { workspace: string; module: string }> = {
  'CEO': { workspace: 'operate', module: 'command-center' },
  'CIO': { workspace: 'invest', module: 'deal-pipeline' },
  'Asset Manager': { workspace: 'operate', module: 'properties' },
  'Fund Manager': { workspace: 'capital', module: 'fund-management' },
  'Analyst': { workspace: 'operate', module: 'command-center' },
  'Controller': { workspace: 'operate', module: 'accounting' },
};

export function RoleProvider({ children }: { children: ReactNode }) {
  const [role, setRole] = useState<UserRole>('CEO');

  const handleSetRole = (newRole: string) => {
    setRole(newRole as UserRole);
  };

  const getDefaultWorkspace = () => roleDefaults[role].workspace;
  const getDefaultModule = () => roleDefaults[role].module;

  return (
    <RoleContext.Provider value={{ 
      role, 
      setRole: handleSetRole,
      getDefaultWorkspace,
      getDefaultModule
    }}>
      {children}
    </RoleContext.Provider>
  );
}

export function useRole() {
  const context = useContext(RoleContext);
  if (context === undefined) {
    throw new Error('useRole must be used within a RoleProvider');
  }
  return context;
}