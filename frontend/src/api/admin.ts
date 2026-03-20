import client from './client';
import { AdminOverview, GameEvent } from '../types';

export const pauseGame = (gameId: number) =>
  client.post(`/games/${gameId}/admin/pause/`);

export const resumeGame = (gameId: number) =>
  client.post(`/games/${gameId}/admin/resume/`);

export const forceResolve = (gameId: number) =>
  client.post(`/games/${gameId}/admin/force-resolve/`);

export const getAdminOverview = (gameId: number) =>
  client.get<AdminOverview>(`/games/${gameId}/admin/overview/`);

export const listEvents = (gameId: number) =>
  client.get<GameEvent[]>(`/games/${gameId}/events/`);

export const createEvent = (gameId: number, data: {
  title: string;
  description: string;
  scope: string;
  effects: Record<string, any>;
  affected_nation_ids?: number[];
  expires_turn?: number;
}) => client.post<GameEvent>(`/games/${gameId}/events/`, data);

export const getEventTemplates = (gameId: number) =>
  client.get(`/games/${gameId}/events/templates/`);
