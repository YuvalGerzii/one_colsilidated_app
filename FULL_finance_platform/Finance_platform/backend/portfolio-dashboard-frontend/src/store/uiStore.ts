// src/store/uiStore.ts
import create from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  
  snackbar: {
    open: boolean;
    message: string;
    severity: 'success' | 'error' | 'warning' | 'info';
  };
  showSnackbar: (message: string, severity?: 'success' | 'error' | 'warning' | 'info') => void;
  hideSnackbar: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  
  snackbar: {
    open: false,
    message: '',
    severity: 'info',
  },
  showSnackbar: (message, severity = 'info') =>
    set({ snackbar: { open: true, message, severity } }),
  hideSnackbar: () =>
    set((state) => ({ snackbar: { ...state.snackbar, open: false } })),
}));
