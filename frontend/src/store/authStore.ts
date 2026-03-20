import { create } from 'zustand';
import type { User } from '../types';
import * as authApi from '../api/auth';

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, displayName?: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
  setTokens: (access: string, refresh: string) => void;
}

const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('access_token'),
  refreshToken: localStorage.getItem('refresh_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),

  login: async (username: string, password: string) => {
    const { access, refresh } = await authApi.login({ username, password });
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    set({ token: access, refreshToken: refresh, isAuthenticated: true });

    const user = await authApi.getMe();
    set({ user });
  },

  register: async (username: string, email: string, password: string, displayName?: string) => {
    await authApi.register({
      username,
      email,
      password,
      display_name: displayName,
    });
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({ user: null, token: null, refreshToken: null, isAuthenticated: false });
  },

  fetchMe: async () => {
    try {
      const user = await authApi.getMe();
      set({ user });
    } catch {
      set({ user: null, isAuthenticated: false, token: null, refreshToken: null });
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  },

  setTokens: (access: string, refresh: string) => {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    set({ token: access, refreshToken: refresh, isAuthenticated: true });
  },
}));

export default useAuthStore;
