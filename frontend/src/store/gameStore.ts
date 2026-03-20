import { create } from 'zustand';
import type { Game, GameMembership } from '../types';
import * as gamesApi from '../api/games';

interface GameState {
  games: Game[];
  currentGame: Game | null;
  members: GameMembership[];
  fetchGames: () => Promise<void>;
  createGame: (data: {
    name: string;
    description?: string;
    max_players: number;
    min_players: number;
    turn_duration_hours: number;
    starting_provinces: number;
  }) => Promise<Game>;
  joinGame: (id: number) => Promise<void>;
  leaveGame: (id: number) => Promise<void>;
  startGame: (id: number) => Promise<void>;
  fetchMembers: (id: number) => Promise<void>;
  setCurrentGame: (game: Game | null) => void;
}

const useGameStore = create<GameState>((set) => ({
  games: [],
  currentGame: null,
  members: [],

  fetchGames: async () => {
    const games = await gamesApi.listGames();
    set({ games });
  },

  createGame: async (data) => {
    const game = await gamesApi.createGame(data);
    set((state) => ({ games: [...state.games, game] }));
    return game;
  },

  joinGame: async (id: number) => {
    await gamesApi.joinGame(id);
    // Refresh game data and members
    const game = await gamesApi.getGame(id);
    const members = await gamesApi.getMembers(id);
    set({ currentGame: game, members });
  },

  leaveGame: async (id: number) => {
    await gamesApi.leaveGame(id);
    const game = await gamesApi.getGame(id);
    const members = await gamesApi.getMembers(id);
    set({ currentGame: game, members });
  },

  startGame: async (id: number) => {
    const game = await gamesApi.startGame(id);
    set({ currentGame: game });
  },

  fetchMembers: async (id: number) => {
    const members = await gamesApi.getMembers(id);
    set({ members });
  },

  setCurrentGame: (game: Game | null) => {
    set({ currentGame: game });
  },
}));

export default useGameStore;
