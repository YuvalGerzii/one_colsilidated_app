/**
 * Authentication Context
 *
 * Provides authentication state and methods throughout the app.
 * Automatically bypasses authentication in local development mode.
 */

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import authService, { User, LoginCredentials, RegisterData } from '../services/authService';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isDevMode: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  updateProfile: (data: Partial<User>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const isDevMode = authService.isDevMode();

  // Initialize auth state on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          // In dev mode, this will return the mock user
          // In production, this will fetch from API
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
        }
      } catch (error) {
        console.error('Failed to initialize auth:', error);
        // Clear invalid auth data
        authService.clearAuth();
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  // Display dev mode notification
  useEffect(() => {
    if (isDevMode && !sessionStorage.getItem('dev_mode_notified')) {
      console.log(
        '%c🔓 DEV MODE: Authentication Bypassed',
        'background: #4caf50; color: white; padding: 8px 12px; font-size: 14px; font-weight: bold; border-radius: 4px;'
      );
      console.log(
        'Running in local development mode. All authentication is automatically handled.',
        '\nNo login required!'
      );
      sessionStorage.setItem('dev_mode_notified', 'true');
    }
  }, [isDevMode]);

  const login = useCallback(async (credentials: LoginCredentials) => {
    setIsLoading(true);
    try {
      const response = await authService.login(credentials);
      setUser(response.user);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (data: RegisterData) => {
    setIsLoading(true);
    try {
      const response = await authService.register(data);
      setUser(response.user);
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    setIsLoading(true);
    try {
      await authService.logout();
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
      // Still clear user state even if API call fails
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const refreshUser = useCallback(async () => {
    try {
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      console.error('Failed to refresh user:', error);
      throw error;
    }
  }, []);

  const updateProfile = useCallback(async (data: Partial<User>) => {
    try {
      const updatedUser = await authService.updateProfile(data);
      setUser(updatedUser);
    } catch (error) {
      console.error('Failed to update profile:', error);
      throw error;
    }
  }, []);

  const value: AuthContextType = {
    user,
    isAuthenticated: authService.isAuthenticated(),
    isLoading,
    isDevMode,
    login,
    register,
    logout,
    refreshUser,
    updateProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
