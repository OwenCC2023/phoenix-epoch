import type { Game } from '../types';

interface GameCardProps {
  game: Game;
  onClick: () => void;
}

const statusColors: Record<Game['status'], string> = {
  lobby: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
  active: 'bg-green-500/20 text-green-400 border-green-500/30',
  paused: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  finished: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
};

export default function GameCard({ game, onClick }: GameCardProps) {
  return (
    <div
      onClick={onClick}
      className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5 cursor-pointer hover:border-amber-500/40 transition-colors"
    >
      <div className="flex items-start justify-between mb-3">
        <h3 className="text-gray-200 font-semibold text-lg">{game.name}</h3>
        <span
          className={`text-xs font-medium px-2 py-1 rounded border ${statusColors[game.status]}`}
        >
          {game.status}
        </span>
      </div>

      {game.description && (
        <p className="text-gray-500 text-sm mb-4 line-clamp-2">{game.description}</p>
      )}

      <div className="flex items-center gap-4 text-xs text-gray-500">
        <span>
          Players: {game.member_count}/{game.max_players}
        </span>
        <span>Creator: {game.creator_name}</span>
        <span>Turn: {game.turn_duration_hours}h</span>
      </div>
    </div>
  );
}
