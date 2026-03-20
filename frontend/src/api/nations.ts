import client from './client';
import { Formation, MilitaryGroup, Nation, NationPolicy } from '../types';

export const listNations = (gameId: number) =>
  client.get<Nation[]>(`/games/${gameId}/nations/`);

export const createNation = (gameId: number, data: {
  name: string;
  description?: string;
  government_type: string;
  ideology_traits: { strong: string; weak: string[] };
  motto?: string;
}) => client.post<Nation>(`/games/${gameId}/nations/`, data);

export const getNation = (gameId: number, nationId: number) =>
  client.get<Nation>(`/games/${gameId}/nations/${nationId}/`);

export const updateNation = (gameId: number, nationId: number, data: Partial<Nation>) =>
  client.patch<Nation>(`/games/${gameId}/nations/${nationId}/`, data);

export const getNationPolicies = (gameId: number, nationId: number) =>
  client.get<NationPolicy[]>(`/games/${gameId}/nations/${nationId}/policies/`);

export const getNationFormations = (gameId: number, nationId: number, domain?: string) =>
  client.get<Formation[]>(
    `/games/${gameId}/nations/${nationId}/military/formations/${domain ? `?domain=${domain}` : ''}`
  );

export const getNationMilitaryGroups = (gameId: number, nationId: number) =>
  client.get<MilitaryGroup[]>(`/games/${gameId}/nations/${nationId}/military/groups/`);
