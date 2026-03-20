import { useState } from 'react';
import { useTurnStore } from '../../store/turnStore';

interface Props {
  gameId: number;
}

export default function SubmitOrdersButton({ gameId }: Props) {
  const { orders, submitOrders } = useTurnStore();
  const [confirming, setConfirming] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const hasDraftOrders = orders.some((o) => o.status === 'draft');
  const allSubmitted = orders.length > 0 && orders.every((o) => o.status !== 'draft');

  const handleSubmit = async () => {
    if (!confirming) {
      setConfirming(true);
      return;
    }
    setSubmitting(true);
    try {
      await submitOrders(gameId);
    } catch {
      // handled by store
    } finally {
      setSubmitting(false);
      setConfirming(false);
    }
  };

  if (allSubmitted) {
    return (
      <div className="bg-green-900/20 border border-green-800/40 rounded-lg p-4 text-center">
        <span className="text-green-400 text-sm font-medium">Orders Submitted</span>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {confirming && (
        <div className="bg-amber-900/20 border border-amber-700/40 rounded-lg p-3 text-center">
          <p className="text-amber-400 text-xs mb-2">
            Submit all draft orders? This cannot be undone.
          </p>
          <button
            onClick={() => setConfirming(false)}
            className="text-gray-400 hover:text-gray-300 text-xs mr-3 cursor-pointer"
          >
            Cancel
          </button>
        </div>
      )}
      <button
        onClick={handleSubmit}
        disabled={!hasDraftOrders || submitting}
        className="w-full bg-amber-600 hover:bg-amber-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium py-3 rounded-lg transition-colors cursor-pointer"
      >
        {submitting ? 'Submitting...' : confirming ? 'Confirm Submit' : 'Submit Orders'}
      </button>
    </div>
  );
}
