import { TradeOffer } from '../../types';

interface Props {
  trades: TradeOffer[];
}

const STATUS_COLORS: Record<string, string> = {
  pending: 'bg-yellow-600/30 text-yellow-400',
  accepted: 'bg-green-600/30 text-green-400',
  rejected: 'bg-red-600/30 text-red-400',
  expired: 'bg-gray-600/30 text-gray-400',
  executed: 'bg-green-700/30 text-green-300',
};

function formatResources(res: Record<string, number>): string {
  return Object.entries(res)
    .filter(([, v]) => v > 0)
    .map(([k, v]) => `${v} ${k}`)
    .join(', ') || 'nothing';
}

export default function TradeOfferPanel({ trades }: Props) {
  if (trades.length === 0) {
    return (
      <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
        <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
          Outgoing Trades
        </h3>
        <p className="text-gray-500 text-sm text-center py-4">No outgoing trade offers.</p>
      </div>
    );
  }

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
        Outgoing Trades ({trades.length})
      </h3>
      <div className="space-y-2">
        {trades.map((trade) => (
          <div key={trade.id} className="bg-[#0f0f0f] rounded p-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-200 text-sm font-medium">
                To: {trade.to_nation_name}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded ${STATUS_COLORS[trade.status] || ''}`}>
                {trade.status}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <span className="text-gray-500">Offering:</span>{' '}
                <span className="text-gray-300">{formatResources(trade.offering)}</span>
              </div>
              <div>
                <span className="text-gray-500">Requesting:</span>{' '}
                <span className="text-gray-300">{formatResources(trade.requesting)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
