import { useEffect, useState } from 'react';
import { Turn } from '../../types';

interface Props {
  turn: Turn | null;
}

function formatCountdown(ms: number): string {
  if (ms <= 0) return '0:00:00';
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

export default function TurnTimer({ turn }: Props) {
  const [remaining, setRemaining] = useState<number>(0);

  useEffect(() => {
    if (!turn?.deadline) {
      setRemaining(0);
      return;
    }

    const update = () => {
      const diff = new Date(turn.deadline).getTime() - Date.now();
      setRemaining(Math.max(0, diff));
    };

    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, [turn?.deadline]);

  const isResolving = turn?.status === 'processing';
  const isExpired = remaining <= 0 && turn?.status === 'pending';

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
      <div className="text-gray-500 text-xs uppercase tracking-wider mb-1">
        Current Turn
      </div>
      <div className="text-amber-500 text-xl font-bold mb-2">
        {turn ? `Turn ${turn.turn_number}` : 'No active turn'}
      </div>
      {turn && (
        <div>
          {isResolving || isExpired ? (
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
              <span className="text-amber-400 text-sm font-medium">Resolving...</span>
            </div>
          ) : turn.status === 'completed' ? (
            <span className="text-green-400 text-sm">Completed</span>
          ) : (
            <div>
              <div className="text-gray-400 text-xs mb-1">Time Remaining</div>
              <div
                className={`text-lg font-mono font-bold ${
                  remaining < 3600000 ? 'text-red-400' : remaining < 7200000 ? 'text-yellow-400' : 'text-gray-200'
                }`}
              >
                {formatCountdown(remaining)}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
