import client from './client';
import { Turn, Order } from '../types';

export const listTurns = (gameId: number) =>
  client.get<Turn[]>(`/games/${gameId}/turns/`);

export const getCurrentTurn = (gameId: number) =>
  client.get<Turn>(`/games/${gameId}/turns/current/`);

export const listOrders = (gameId: number) =>
  client.get<Order[]>(`/games/${gameId}/turns/current/orders/`);

export const createOrder = (gameId: number, data: { order_type: string; payload: Record<string, any> }) =>
  client.post<Order>(`/games/${gameId}/turns/current/orders/`, data);

export const deleteOrder = (gameId: number, orderId: number) =>
  client.delete(`/games/${gameId}/turns/current/orders/${orderId}/`);

export const submitOrders = (gameId: number) =>
  client.post(`/games/${gameId}/turns/current/submit/`);

export const getTurnByNumber = (gameId: number, turnNumber: number) =>
  client.get<Turn>(`/games/${gameId}/turns/${turnNumber}/`);
