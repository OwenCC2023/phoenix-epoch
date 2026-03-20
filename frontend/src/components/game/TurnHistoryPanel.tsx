import { useState } from 'react';
import { Turn } from '../../types';

interface Props {
  turns: Turn[];
}

export default function TurnHistoryPanel({ turns }: Props) {
  const [expandedTurn, setExpandedTurn] = useState<number | null>(null);

  const sortedTurns = [...turns].sort((a, b) => b.turn_number - a.turn_number);

  if (sortedTurns.length === 0) {
    return (
      <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
        <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
          Turn History
        </h3>
        <p className="text-gray-500 text-sm text-center py-4">No turn history yet.</p>
      </div>
    );
  }

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
        Turn History
      </h3>
      <div className="space-y-1">
        {sortedTurns.map((turn) => (
          <div key={turn.id}>
            <button
              onClick={() => setExpandedTurn(expandedTurn === turn.id ? null : turn.id)}
              className="w-full flex items-center justify-between bg-[#0f0f0f] rounded px-3 py-2 hover:bg-[#151515] transition-colors cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <span className="text-gray-200 text-sm font-medium">Turn {turn.turn_number}</span>
                <span className={`text-xs px-2 py-0.5 rounded ${
                  turn.status === 'completed'
                    ? 'bg-green-600/30 text-green-400'
                    : turn.status === 'failed'
                    ? 'bg-red-600/30 text-red-400'
                    : 'bg-gray-600/30 text-gray-400'
                }`}>
                  {turn.status}
                </span>
              </div>
              <span className="text-gray-500 text-xs">
                {turn.resolved_at ? new Date(turn.resolved_at).toLocaleDateString() : 'In progress'}
              </span>
            </button>
            {expandedTurn === turn.id && (
              <div className="bg-[#0f0f0f] border-t border-[#2a2a2a] rounded-b px-3 py-3 -mt-px">
                <div className="text-xs space-y-1">
                  <div className="text-gray-500">
                    Started: {new Date(turn.started_at).toLocaleString()}
                  </div>
                  {turn.resolved_at && (
                    <div className="text-gray-500">
                      Resolved: {new Date(turn.resolved_at).toLocaleString()}
                    </div>
                  )}
                  {turn.resolution_log?.events && turn.resolution_log.events.length > 0 && (
                    <div className="mt-2">
                      <div className="text-gray-400 font-medium mb-1">Resolution Log:</div>
                      {turn.resolution_log.events.map((event, i) => (
                        <div key={i} className="text-gray-300 pl-2 border-l border-[#2a2a2a] ml-1 mb-1">
                          {event}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
