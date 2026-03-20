import { useState } from 'react';
import useGameStore from '../store/gameStore';

interface CreateGameModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: (gameId: number) => void;
}

export default function CreateGameModal({ isOpen, onClose, onCreated }: CreateGameModalProps) {
  const createGame = useGameStore((s) => s.createGame);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [maxPlayers, setMaxPlayers] = useState(8);
  const [minPlayers, setMinPlayers] = useState(2);
  const [turnDuration, setTurnDuration] = useState(24);
  const [startingProvinces, setStartingProvinces] = useState(3);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const game = await createGame({
        name,
        description,
        max_players: maxPlayers,
        min_players: minPlayers,
        turn_duration_hours: turnDuration,
        starting_provinces: startingProvinces,
      });
      onCreated(game.id);
      onClose();
    } catch {
      setError('Failed to create game. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="relative bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6 w-full max-w-md mx-4">
        <h2 className="text-gray-200 text-xl font-semibold mb-4">Create New Game</h2>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-sm rounded p-3 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-gray-400 text-sm mb-1">Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm focus:outline-none focus:border-amber-500/50"
            />
          </div>

          <div>
            <label className="block text-gray-400 text-sm mb-1">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm focus:outline-none focus:border-amber-500/50 resize-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-400 text-sm mb-1">Min Players</label>
              <input
                type="number"
                value={minPlayers}
                onChange={(e) => setMinPlayers(Number(e.target.value))}
                min={2}
                required
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm focus:outline-none focus:border-amber-500/50"
              />
            </div>
            <div>
              <label className="block text-gray-400 text-sm mb-1">Max Players</label>
              <input
                type="number"
                value={maxPlayers}
                onChange={(e) => setMaxPlayers(Number(e.target.value))}
                min={2}
                required
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm focus:outline-none focus:border-amber-500/50"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-400 text-sm mb-1">Turn Duration (hours)</label>
              <input
                type="number"
                value={turnDuration}
                onChange={(e) => setTurnDuration(Number(e.target.value))}
                min={1}
                required
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm focus:outline-none focus:border-amber-500/50"
              />
            </div>
            <div>
              <label className="block text-gray-400 text-sm mb-1">Starting Provinces</label>
              <input
                type="number"
                value={startingProvinces}
                onChange={(e) => setStartingProvinces(Number(e.target.value))}
                min={1}
                required
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm focus:outline-none focus:border-amber-500/50"
              />
            </div>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-[#2a2a2a] text-gray-300 rounded py-2 text-sm font-medium hover:bg-[#333] transition-colors cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-amber-600 text-white rounded py-2 text-sm font-medium hover:bg-amber-700 transition-colors disabled:opacity-50 cursor-pointer"
            >
              {loading ? 'Creating...' : 'Create Game'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
