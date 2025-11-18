/**
 * Authentication Service
 *
 * Handles all authentication-related API calls and token management.
 * Includes local development bypass for easy testing.
 */

import api from './api';

// Check if running in development mode (localhost)
const isDevelopment = import.meta.env.DEV || window.location.hostname === 'localhost';

// Mock user for development mode
const DEV_USER = {
  id: 'dev-user-123',
  email: 'dev@localhost',
  username: 'developer',
  first_name: 'Dev',
  last_name: 'User',
  company_name: 'Local Development',
  is_active: true,
  is_verified: true,
  created_at: new Date().toISOString(),
  last_login: new Date().toISOString(),
};

const DEV_TOKENS = {
  access_token: 'dev-access-token',
  refresh_token: 'dev-refresh-token',
  token_type: 'bearer',
};

export interface User {
  id: string;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  company_name?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  first_name?: string;
  last_name?: string;
  company_name?: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

class AuthService {
  private readonly TOKEN_KEY = 'auth_token';
  private readonly REFRESH_TOKEN_KEY = 'refresh_token';
  private readonly USER_KEY = 'user_data';

  /**
   * Check if authentication is bypassed in dev mode
   */
  isDevMode(): boolean {
    return isDevelopment;
  }

  /**
   * Register a new user
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    if (this.isDevMode()) {
      console.log('[DEV MODE] Mock registration:', data.email);
      return {
        ...DEV_TOKENS,
        user: { ...DEV_USER, email: data.email, username: data.username },
      };
    }

    const response = await api.post<AuthResponse>('/auth/register', data);
    this.setTokens(response.data.access_token, response.data.refresh_token);
    this.setUser(response.data.user);
    return response.data;
  }

  /**
   * Login with email and password
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    if (this.isDevMode()) {
      console.log('[DEV MODE] Mock login:', credentials.email);
      const authResponse = {
        ...DEV_TOKENS,
        user: { ...DEV_USER, email: credentials.email },
      };
      this.setTokens(authResponse.access_token, authResponse.refresh_token);
      this.setUser(authResponse.user);
      return authResponse;
    }

    const response = await api.post<AuthResponse>('/auth/login', credentials);
    this.setTokens(response.data.access_token, response.data.refresh_token);
    this.setUser(response.data.user);
    return response.data;
  }

  /**
   * Logout and clear tokens
   */
  async logout(): Promise<void> {
    if (this.isDevMode()) {
      console.log('[DEV MODE] Mock logout');
      this.clearAuth();
      return;
    }

    try {
      await api.post('/auth/logout');
    } finally {
      this.clearAuth();
    }
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<AuthResponse> {
    if (this.isDevMode()) {
      console.log('[DEV MODE] Mock token refresh');
      return {
        ...DEV_TOKENS,
        user: this.getUser() || DEV_USER,
      };
    }

    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await api.post<AuthResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    });

    this.setTokens(response.data.access_token, response.data.refresh_token);
    this.setUser(response.data.user);
    return response.data;
  }

  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<User> {
    if (this.isDevMode()) {
      console.log('[DEV MODE] Mock get current user');
      return this.getUser() || DEV_USER;
    }

    const response = await api.get<User>('/auth/me');
    this.setUser(response.data);
    return response.data;
  }

  /**
   * Update user profile
   */
  async updateProfile(data: Partial<User>): Promise<User> {
    if (this.isDevMode()) {
      console.log('[DEV MODE] Mock update profile:', data);
      const updatedUser = { ...DEV_USER, ...data };
      this.setUser(updatedUser);
      return updatedUser;
    }

    const response = await api.put<User>('/auth/me', data);
    this.setUser(response.data);
    return response.data;
  }

  /**
   * Change password
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    if (this.isDevMode()) {
      console.log('[DEV MODE] Mock password change');
      return;
    }

    await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  }

  // ===== Token Management =====

  /**
   * Set access and refresh tokens in localStorage
   */
  setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.TOKEN_KEY, accessToken);
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
  }

  /**
   * Get access token
   */
  getAccessToken(): string | null {
    if (this.isDevMode()) {
      return DEV_TOKENS.access_token;
    }
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Get refresh token
   */
  getRefreshToken(): string | null {
    if (this.isDevMode()) {
      return DEV_TOKENS.refresh_token;
    }
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    if (this.isDevMode()) {
      return true; // Always authenticated in dev mode
    }
    return !!this.getAccessToken();
  }

  /**
   * Set user data in localStorage
   */
  setUser(user: User): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
  }

  /**
   * Get user data from localStorage
   */
  getUser(): User | null {
    if (this.isDevMode() && !localStorage.getItem(this.USER_KEY)) {
      return DEV_USER;
    }

    const userData = localStorage.getItem(this.USER_KEY);
    if (!userData) return null;

    try {
      return JSON.parse(userData);
    } catch {
      return null;
    }
  }

  /**
   * Clear all authentication data
   */
  clearAuth(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
  }
}

export const authService = new AuthService();
export default authService;
