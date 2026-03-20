import { Turn, ResourceLedger } from '../../types';

interface Props {
  turn: Turn | null;
  ledger: ResourceLedger[];
}

const RESOURCE_KEYS = ['food', 'materials', 'energy', 'wealth', 'manpower', 'research'];

export default function TurnResultsPanel({ turn, ledger }: Props) {
  if (!turn || turn.status !== 'completed') {
    return (
      <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
        <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
          Turn Results
        </h3>
        <p className="text-gray-500 text-sm text-center py-4">
          No results available yet.
        </p>
      </div>
    );
  }

  // Find the ledger entry for this turn and the previous one
  const currentLedger = ledger.find((l) => l.turn_number === turn.turn_number);
  const previousLedger = ledger.find((l) => l.turn_number === turn.turn_number - 1);

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5 space-y-4">
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider">
        Turn {turn.turn_number} Results
      </h3>

      {/* Resource Deltas */}
      {currentLedger && (
        <div>
          <h4 className="text-gray-400 text-xs uppercase tracking-wider mb-2">Resource Changes</h4>
          <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
            {RESOURCE_KEYS.map((key) => {
              const current = currentLedger.final_pools[key] ?? 0;
              const previous = previousLedger?.final_pools[key] ?? 0;
              const delta = current - previous;
              return (
                <div key={key} className="bg-[#0f0f0f] rounded p-2 text-center">
                  <div className="text-gray-500 text-xs capitalize mb-1">{key}</div>
                  <div className="text-gray-200 text-sm font-bold">{Math.round(current)}</div>
                  {previousLedger && (
                    <div className={`text-xs ${delta >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {delta >= 0 ? '+' : ''}{Math.round(delta)}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Trade Net */}
      {currentLedger && Object.keys(currentLedger.trade_net).length > 0 && (
        <div>
          <h4 className="text-gray-400 text-xs uppercase tracking-wider mb-2">Trade Outcomes</h4>
          <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
            {RESOURCE_KEYS.map((key) => {
              const net = currentLedger.trade_net[key] ?? 0;
              if (net === 0) return null;
              return (
                <div key={key} className="bg-[#0f0f0f] rounded p-2 text-center">
                  <div className="text-gray-500 text-xs capitalize mb-1">{key}</div>
                  <div className={`text-sm font-bold ${net >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {net >= 0 ? '+' : ''}{Math.round(net)}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Resolution Log */}
      {turn.resolution_log?.events && turn.resolution_log.events.length > 0 && (
        <div>
          <h4 className="text-gray-400 text-xs uppercase tracking-wider mb-2">Events</h4>
          <div className="space-y-1">
            {turn.resolution_log.events.map((event, i) => (
              <div key={i} className="bg-[#0f0f0f] rounded px-3 py-2 text-gray-300 text-xs">
                {event}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
