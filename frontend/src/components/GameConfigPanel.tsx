import type { Game } from '../types';

interface GameConfigPanelProps {
  game: Game;
}

export default function GameConfigPanel({ game }: GameConfigPanelProps) {
  const configItems = [
    { label: 'Status', value: game.status },
    { label: 'Min Players', value: game.min_players },
    { label: 'Max Players', value: game.max_players },
    { label: 'Turn Duration', value: `${game.turn_duration_hours} hours` },
    { label: 'Starting Provinces', value: game.starting_provinces },
    { label: 'Current Turn', value: game.current_turn_number },
    { label: 'Created', value: new Date(game.created_at).toLocaleDateString() },
  ];

  return (
    <div className="bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg p-4">
      <h3 className="text-gray-300 font-semibold text-sm mb-3 uppercase tracking-wider">
        Configuration
      </h3>
      <dl className="space-y-2">
        {configItems.map((item) => (
          <div key={item.label} className="flex justify-between">
            <dt className="text-gray-500 text-sm">{item.label}</dt>
            <dd className="text-gray-300 text-sm font-medium">{item.value}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
