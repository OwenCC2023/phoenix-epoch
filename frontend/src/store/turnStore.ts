import { create } from 'zustand';
import { Turn, Order } from '../types';
import * as turnsApi from '../api/turns';

interface TurnState {
  currentTurn: Turn | null;
  orders: Order[];
  turnHistory: Turn[];
  loading: boolean;
  error: string | null;

  fetchCurrentTurn: (gameId: number) => Promise<void>;
  fetchOrders: (gameId: number) => Promise<void>;
  fetchTurnHistory: (gameId: number) => Promise<void>;
  createOrder: (gameId: number, orderType: string, payload: Record<string, any>) => Promise<Order>;
  deleteOrder: (gameId: number, orderId: number) => Promise<void>;
  submitOrders: (gameId: number) => Promise<void>;
  setCurrentTurn: (turn: Turn) => void;
}

export const useTurnStore = create<TurnState>((set) => ({
  currentTurn: null,
  orders: [],
  turnHistory: [],
  loading: false,
  error: null,

  fetchCurrentTurn: async (gameId) => {
    try {
      const { data } = await turnsApi.getCurrentTurn(gameId);
      set({ currentTurn: data });
    } catch { /* no current turn */ }
  },

  fetchOrders: async (gameId) => {
    try {
      const { data } = await turnsApi.listOrders(gameId);
      set({ orders: data });
    } catch { /* ignore */ }
  },

  fetchTurnHistory: async (gameId) => {
    try {
      const { data } = await turnsApi.listTurns(gameId);
      set({ turnHistory: data });
    } catch { /* ignore */ }
  },

  createOrder: async (gameId, orderType, payload) => {
    const { data } = await turnsApi.createOrder(gameId, { order_type: orderType, payload });
    set((state) => ({ orders: [...state.orders, data] }));
    return data;
  },

  deleteOrder: async (gameId, orderId) => {
    await turnsApi.deleteOrder(gameId, orderId);
    set((state) => ({ orders: state.orders.filter((o) => o.id !== orderId) }));
  },

  submitOrders: async (gameId) => {
    await turnsApi.submitOrders(gameId);
    const { data } = await turnsApi.listOrders(gameId);
    set({ orders: data });
  },

  setCurrentTurn: (turn) => set({ currentTurn: turn }),
}));
