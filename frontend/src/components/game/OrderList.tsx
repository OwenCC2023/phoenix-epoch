import { Order } from '../../types';
import { useTurnStore } from '../../store/turnStore';

interface Props {
  gameId: number;
  orders: Order[];
}

const STATUS_COLORS: Record<string, string> = {
  draft: 'bg-gray-600 text-gray-200',
  submitted: 'bg-blue-600/30 text-blue-400',
  validated: 'bg-green-600/30 text-green-400',
  executed: 'bg-green-700/30 text-green-300',
  failed: 'bg-red-600/30 text-red-400',
};

function summarizePayload(order: Order): string {
  const p = order.payload;
  switch (order.order_type) {
    case 'set_allocation':
      return `Province #${p.province_id} allocation`;
    case 'build_building':
      return `Build ${(p.building_type || '').replace(/_/g, ' ')} in province #${p.province_id}`;
    case 'trade_offer':
      return `Trade offer to nation #${p.to_nation}`;
    case 'trade_response':
      return `Trade response: ${p.action}`;
    case 'policy_change':
      return `Change ${p.change_type} to ${p.new_value}`;
    default:
      return order.order_type;
  }
}

export default function OrderList({ gameId, orders }: Props) {
  const deleteOrder = useTurnStore((s) => s.deleteOrder);

  if (orders.length === 0) {
    return (
      <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
        <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
          Orders
        </h3>
        <p className="text-gray-500 text-sm text-center py-4">No orders yet this turn.</p>
      </div>
    );
  }

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
        Orders ({orders.length})
      </h3>
      <div className="space-y-2">
        {orders.map((order) => (
          <div
            key={order.id}
            className="flex items-center justify-between bg-[#0f0f0f] rounded p-3"
          >
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-gray-200 text-sm font-medium">
                  {order.order_type.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded ${STATUS_COLORS[order.status] || 'bg-gray-600 text-gray-200'}`}>
                  {order.status}
                </span>
              </div>
              <div className="text-gray-500 text-xs">{summarizePayload(order)}</div>
              {order.validation_errors.length > 0 && (
                <div className="text-red-400 text-xs mt-1">
                  {order.validation_errors.join('; ')}
                </div>
              )}
            </div>
            {order.status === 'draft' && (
              <button
                onClick={() => deleteOrder(gameId, order.id)}
                className="text-red-400 hover:text-red-300 text-xs ml-3 cursor-pointer"
              >
                Delete
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
