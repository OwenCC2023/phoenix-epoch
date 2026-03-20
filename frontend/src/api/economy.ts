import client from './client';
import { NationResourcePool, ResourceLedger, Province, TradeOffer } from '../types';

export const getNationResources = (gameId: number, nationId: number) =>
  client.get<NationResourcePool>(`/games/${gameId}/nations/${nationId}/resources/`);

export const getNationLedger = (gameId: number, nationId: number) =>
  client.get<ResourceLedger[]>(`/games/${gameId}/nations/${nationId}/ledger/`);

export const listProvinces = (gameId: number, nationId?: number) => {
  const params = nationId ? { nation_id: nationId } : {};
  return client.get<Province[]>(`/games/${gameId}/provinces/`, { params });
};

export const getProvince = (gameId: number, provinceId: number) =>
  client.get<Province>(`/games/${gameId}/provinces/${provinceId}/`);

export const setProvinceAllocations = (gameId: number, provinceId: number, allocations: { sector: string; percentage: number }[]) =>
  client.post(`/games/${gameId}/provinces/${provinceId}/allocations/`, { allocations });

export const listTrades = (gameId: number) =>
  client.get<TradeOffer[]>(`/games/${gameId}/trades/`);

export const createTrade = (gameId: number, data: { to_nation: number; offering: Record<string, number>; requesting: Record<string, number> }) =>
  client.post<TradeOffer>(`/games/${gameId}/trades/`, data);

export const respondToTrade = (gameId: number, tradeId: number, action: 'accept' | 'reject') =>
  client.post(`/games/${gameId}/trades/${tradeId}/respond/`, { action });
