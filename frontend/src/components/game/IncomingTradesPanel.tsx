import { useState } from 'react';
import { TradeOffer } from '../../types';
import { useTurnStore } from '../../store/turnStore';

interface Props {
  gameId: number;
  trades: TradeOffer[];
}

function formatResources(res: Record<string, number>): string {
  return Object.entries(res)
    .filter(([, v]) => v > 0)
    .map(([k, v]) => `${v} ${k}`)
    .join(', ') || 'nothing';
}

export default function IncomingTradesPanel({ gameId, trades }: Props) {
  const createOrder = useTurnStore((s) => s.createOrder);
  const [respondingTo, setRespondingTo] = useState<number | null>(null);

  const handleRespond = async (trade: TradeOffer, action: 'accept' | 'reject') => {
    setRespondingTo(trade.id);
    try {
      await createOrder(gameId, 'trade_response', {
        trade_id: trade.id,
        action,
      });
    } catch {
      // handled by store
    } finally {
      setRespondingTo(null);
    }
  };

  if (trades.length === 0) {
    return (
      <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
        <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
          Incoming Trades
        </h3>
        <p className="text-gray-500 text-sm text-center py-4">No incoming trade offers.</p>
      </div>
    );
  }

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
        Incoming Trades ({trades.length})
      </h3>
      <div className="space-y-2">
        {trades.map((trade) => (
          <div key={trade.id} className="bg-[#0f0f0f] rounded p-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-200 text-sm font-medium">
                From: {trade.from_nation_name}
              </span>
              <span className="text-xs text-gray-500">Turn {trade.turn_number}</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs mb-3">
              <div>
                <span className="text-gray-500">They offer:</span>{' '}
                <span className="text-green-400">{formatResources(trade.offering)}</span>
              </div>
              <div>
                <span className="text-gray-500">They want:</span>{' '}
                <span className="text-red-400">{formatResources(trade.requesting)}</span>
              </div>
            </div>
            {trade.status === 'pending' && (
              <div className="flex gap-2">
                <button
                  onClick={() => handleRespond(trade, 'accept')}
                  disabled={respondingTo === trade.id}
                  className="flex-1 bg-green-700 hover:bg-green-600 disabled:opacity-50 text-white text-xs py-1.5 rounded transition-colors cursor-pointer"
                >
                  Accept
                </button>
                <button
                  onClick={() => handleRespond(trade, 'reject')}
                  disabled={respondingTo === trade.id}
                  className="flex-1 bg-red-700 hover:bg-red-600 disabled:opacity-50 text-white text-xs py-1.5 rounded transition-colors cursor-pointer"
                >
                  Reject
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
