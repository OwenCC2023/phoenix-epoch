import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useGameStore from '../store/gameStore';
import useAuthStore from '../store/authStore';
import Header from '../components/Header';
import GameCard from '../components/GameCard';
import CreateGameModal from '../components/CreateGameModal';
import type { Game } from '../types';

const statusTabs: Array<{ label: string; value: Game['status'] | 'all' }> = [
  { label: 'All', value: 'all' },
  { label: 'Lobby', value: 'lobby' },
  { label: 'Active', value: 'active' },
  { label: 'Paused', value: 'paused' },
  { label: 'Finished', value: 'finished' },
];

export default function LobbyListPage() {
  const { games, fetchGames } = useGameStore();
  const fetchMe = useAuthStore((s) => s.fetchMe);
  const navigate = useNavigate();
  const [filter, setFilter] = useState<Game['status'] | 'all'>('all');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      await Promise.all([fetchMe(), fetchGames()]);
      setLoading(false);
    };
    init();
  }, [fetchMe, fetchGames]);

  const filteredGames = filter === 'all' ? games : games.filter((g) => g.status === filter);

  return (
    <div className="min-h-screen bg-[#0f0f0f]">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-gray-200 text-2xl font-bold">Games</h1>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-amber-600 text-white rounded px-4 py-2 text-sm font-medium hover:bg-amber-700 transition-colors cursor-pointer"
          >
            Create Game
          </button>
        </div>

        {/* Status filter tabs */}
        <div className="flex gap-1 mb-6 bg-[#1a1a1a] rounded-lg p-1 w-fit">
          {statusTabs.map((tab) => (
            <button
              key={tab.value}
              onClick={() => setFilter(tab.value)}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors cursor-pointer ${
                filter === tab.value
                  ? 'bg-amber-600 text-white'
                  : 'text-gray-400 hover:text-gray-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Game list */}
        {loading ? (
          <p className="text-gray-500 text-sm">Loading games...</p>
        ) : filteredGames.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-gray-500 text-sm">No games found.</p>
            <p className="text-gray-600 text-xs mt-1">Create one to get started.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredGames.map((game) => (
              <GameCard key={game.id} game={game} onClick={() => navigate(`/games/${game.id}`)} />
            ))}
          </div>
        )}
      </main>

      <CreateGameModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreated={(id) => navigate(`/games/${id}`)}
      />
    </div>
  );
}
