import client from './client';
import type { Game, GameMembership } from '../types';

interface CreateGamePayload {
  name: string;
  description?: string;
  max_players: number;
  min_players: number;
  turn_duration_hours: number;
  starting_provinces: number;
}

export async function listGames(): Promise<Game[]> {
  const { data } = await client.get<Game[]>('/games/');
  return data;
}

export async function createGame(payload: CreateGamePayload): Promise<Game> {
  const { data } = await client.post<Game>('/games/', payload);
  return data;
}

export async function getGame(id: number): Promise<Game> {
  const { data } = await client.get<Game>(`/games/${id}/`);
  return data;
}

export async function joinGame(id: number): Promise<GameMembership> {
  const { data } = await client.post<GameMembership>(`/games/${id}/join/`);
  return data;
}

export async function leaveGame(id: number): Promise<void> {
  await client.post(`/games/${id}/leave/`);
}

export async function startGame(id: number): Promise<Game> {
  const { data } = await client.post<Game>(`/games/${id}/start/`);
  return data;
}

export async function getMembers(id: number): Promise<GameMembership[]> {
  const { data } = await client.get<GameMembership[]>(`/games/${id}/members/`);
  return data;
}
