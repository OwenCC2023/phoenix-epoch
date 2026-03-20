import client from './client';
import type { User } from '../types';

interface TokenResponse {
  access: string;
  refresh: string;
}

interface RegisterPayload {
  username: string;
  email: string;
  password: string;
  display_name?: string;
}

interface LoginPayload {
  username: string;
  password: string;
}

export async function register(payload: RegisterPayload): Promise<User> {
  const { data } = await client.post<User>('/auth/register/', payload);
  return data;
}

export async function login(payload: LoginPayload): Promise<TokenResponse> {
  const { data } = await client.post<TokenResponse>('/auth/token/', payload);
  return data;
}

export async function refresh(refreshToken: string): Promise<{ access: string }> {
  const { data } = await client.post<{ access: string }>('/auth/token/refresh/', {
    refresh: refreshToken,
  });
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await client.get<User>('/auth/me/');
  return data;
}

export async function updateMe(payload: Partial<User>): Promise<User> {
  const { data } = await client.patch<User>('/auth/me/', payload);
  return data;
}
