import { create } from 'zustand';

export interface Notification {
  id: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
}

interface NotificationState {
  notifications: Notification[];
  addNotification: (message: string, type?: Notification['type']) => void;
  removeNotification: (id: string) => void;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],

  addNotification: (message, type = 'info') => {
    const id = `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
    set((state) => ({
      notifications: [...state.notifications, { id, message, type }],
    }));
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      set((state) => ({
        notifications: state.notifications.filter((n) => n.id !== id),
      }));
    }, 5000);
  },

  removeNotification: (id) => {
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    }));
  },
}));
