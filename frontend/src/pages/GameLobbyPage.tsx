import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import useGameStore from '../store/gameStore';
import useAuthStore from '../store/authStore';
import Header from '../components/Header';
import PlayerList from '../components/PlayerList';
import GameConfigPanel from '../components/GameConfigPanel';
import { getGame } from '../api/games';

export default function GameLobbyPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const fetchMe = useAuthStore((s) => s.fetchMe);
  const { currentGame, members, setCurrentGame, fetchMembers, joinGame, leaveGame, startGame } =
    useGameStore();
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState('');

  const gameId = Number(id);

  useEffect(() => {
    const init = async () => {
      try {
        await fetchMe();
        const game = await getGame(gameId);
        setCurrentGame(game);
        await fetchMembers(gameId);
      } catch {
        setError('Failed to load game.');
      } finally {
        setLoading(false);
      }
    };
    init();

    return () => setCurrentGame(null);
  }, [gameId, fetchMe, setCurrentGame, fetchMembers]);

  const isCreator = user && currentGame && user.id === currentGame.creator;
  const isMember = members.some((m) => m.user === user?.id);
  const canStart =
    isCreator &&
    currentGame?.status === 'lobby' &&
    members.length >= (currentGame?.min_players ?? 0);

  const handleJoin = async () => {
    setActionLoading(true);
    setError('');
    try {
      await joinGame(gameId);
    } catch {
      setError('Failed to join game.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleLeave = async () => {
    setActionLoading(true);
    setError('');
    try {
      await leaveGame(gameId);
    } catch {
      setError('Failed to leave game.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleStart = async () => {
    setActionLoading(true);
    setError('');
    try {
      await startGame(gameId);
    } catch {
      setError('Failed to start game.');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0f0f0f]">
        <Header />
        <main className="max-w-7xl mx-auto px-4 py-8">
          <p className="text-gray-500 text-sm">Loading game...</p>
        </main>
      </div>
    );
  }

  if (!currentGame) {
    return (
      <div className="min-h-screen bg-[#0f0f0f]">
        <Header />
        <main className="max-w-7xl mx-auto px-4 py-8">
          <p className="text-gray-500 text-sm">Game not found.</p>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0f0f0f]">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back button */}
        <button
          onClick={() => navigate('/games')}
          className="text-gray-500 hover:text-amber-500 text-sm mb-4 transition-colors cursor-pointer"
        >
          &larr; Back to Games
        </button>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-sm rounded p-3 mb-4">
            {error}
          </div>
        )}

        {/* Game header */}
        <div className="flex items-start justify-between mb-8">
          <div>
            <h1 className="text-gray-200 text-2xl font-bold">{currentGame.name}</h1>
            {currentGame.description && (
              <p className="text-gray-500 text-sm mt-1">{currentGame.description}</p>
            )}
            <p className="text-gray-600 text-xs mt-2">Created by {currentGame.creator_name}</p>
          </div>

          <div className="flex gap-3">
            {currentGame.status === 'lobby' && !isMember && (
              <button
                onClick={handleJoin}
                disabled={actionLoading}
                className="bg-amber-600 text-white rounded px-4 py-2 text-sm font-medium hover:bg-amber-700 transition-colors disabled:opacity-50 cursor-pointer"
              >
                {actionLoading ? 'Joining...' : 'Join Game'}
              </button>
            )}
            {currentGame.status === 'lobby' && isMember && !isCreator && (
              <button
                onClick={handleLeave}
                disabled={actionLoading}
                className="bg-[#2a2a2a] text-gray-300 rounded px-4 py-2 text-sm font-medium hover:bg-[#333] transition-colors disabled:opacity-50 cursor-pointer"
              >
                {actionLoading ? 'Leaving...' : 'Leave Game'}
              </button>
            )}
            {canStart && (
              <button
                onClick={handleStart}
                disabled={actionLoading}
                className="bg-green-600 text-white rounded px-4 py-2 text-sm font-medium hover:bg-green-700 transition-colors disabled:opacity-50 cursor-pointer"
              >
                {actionLoading ? 'Starting...' : 'Start Game'}
              </button>
            )}
          </div>
        </div>

        {/* Two column layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
              <h2 className="text-gray-300 font-semibold text-sm mb-4 uppercase tracking-wider">
                Players ({members.length}/{currentGame.max_players})
              </h2>
              <PlayerList members={members} />
            </div>
          </div>

          <div>
            <GameConfigPanel game={currentGame} />
          </div>
        </div>
      </main>
    </div>
  );
}
