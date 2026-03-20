import { create } from 'zustand';
import { Formation, MilitaryGroup, Nation, NationResourcePool, Province, ResourceLedger } from '../types';
import * as nationsApi from '../api/nations';
import * as economyApi from '../api/economy';

interface NationState {
  nation: Nation | null;
  resources: NationResourcePool | null;
  provinces: Province[];
  ledger: ResourceLedger[];
  formations: Formation[];
  militaryGroups: MilitaryGroup[];
  loading: boolean;
  error: string | null;

  fetchNation: (gameId: number, nationId: number) => Promise<void>;
  fetchResources: (gameId: number, nationId: number) => Promise<void>;
  fetchProvinces: (gameId: number, nationId?: number) => Promise<void>;
  fetchLedger: (gameId: number, nationId: number) => Promise<void>;
  fetchFormations: (gameId: number, nationId: number, domain?: string) => Promise<void>;
  fetchMilitaryGroups: (gameId: number, nationId: number) => Promise<void>;
  createNation: (gameId: number, data: {
    name: string;
    description?: string;
    government_type: string;
    ideology_traits: { strong: string; weak: string[] };
    motto?: string;
  }) => Promise<Nation>;
  setAllocations: (gameId: number, provinceId: number, allocations: { sector: string; percentage: number }[]) => Promise<void>;
  clearNation: () => void;
}

export const useNationStore = create<NationState>((set) => ({
  nation: null,
  resources: null,
  provinces: [],
  ledger: [],
  formations: [],
  militaryGroups: [],
  loading: false,
  error: null,

  fetchNation: async (gameId, nationId) => {
    set({ loading: true, error: null });
    try {
      const { data } = await nationsApi.getNation(gameId, nationId);
      set({ nation: data, loading: false });
    } catch (err: any) {
      set({ error: err.response?.data?.detail || 'Failed to fetch nation', loading: false });
    }
  },

  fetchResources: async (gameId, nationId) => {
    try {
      const { data } = await economyApi.getNationResources(gameId, nationId);
      set({ resources: data });
    } catch { /* may not exist yet */ }
  },

  fetchProvinces: async (gameId, nationId?) => {
    try {
      const { data } = await economyApi.listProvinces(gameId, nationId);
      set({ provinces: data });
    } catch { /* ignore */ }
  },

  fetchLedger: async (gameId, nationId) => {
    try {
      const { data } = await economyApi.getNationLedger(gameId, nationId);
      set({ ledger: data });
    } catch { /* ignore */ }
  },

  createNation: async (gameId, nationData) => {
    set({ loading: true, error: null });
    try {
      const { data } = await nationsApi.createNation(gameId, nationData);
      set({ nation: data, loading: false });
      return data;
    } catch (err: any) {
      set({ error: err.response?.data?.detail || 'Failed to create nation', loading: false });
      throw err;
    }
  },

  fetchFormations: async (gameId, nationId, domain?) => {
    try {
      const { data } = await nationsApi.getNationFormations(gameId, nationId, domain);
      set({ formations: data });
    } catch { /* ignore */ }
  },

  fetchMilitaryGroups: async (gameId, nationId) => {
    try {
      const { data } = await nationsApi.getNationMilitaryGroups(gameId, nationId);
      set({ militaryGroups: data });
    } catch { /* ignore */ }
  },

  setAllocations: async (gameId, provinceId, allocations) => {
    await economyApi.setProvinceAllocations(gameId, provinceId, allocations);
  },

  clearNation: () => set({
    nation: null, resources: null, provinces: [], ledger: [],
    formations: [], militaryGroups: [],
  }),
}));
