import { NationResourcePool } from '../../types';

interface Props {
  resources: NationResourcePool;
}

const RESOURCE_CONFIG = [
  { key: 'food', label: 'Food', icon: 'F', color: 'text-green-400' },
  { key: 'materials', label: 'Materials', icon: 'M', color: 'text-orange-400' },
  { key: 'energy', label: 'Energy', icon: 'E', color: 'text-yellow-400' },
  { key: 'wealth', label: 'Wealth', icon: 'W', color: 'text-amber-400' },
  { key: 'manpower', label: 'Manpower', icon: 'P', color: 'text-blue-400' },
  { key: 'research', label: 'Research', icon: 'R', color: 'text-purple-400' },
  { key: 'stability', label: 'Stability', icon: 'S', color: 'text-cyan-400' },
  { key: 'total_population', label: 'Population', icon: 'Pop', color: 'text-gray-300' },
] as const;

export default function ResourceBar({ resources }: Props) {
  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
      <h3 className="text-gray-300 font-semibold text-xs uppercase tracking-wider mb-3">
        Resources
      </h3>
      <div className="grid grid-cols-2 gap-2">
        {RESOURCE_CONFIG.map(({ key, label, icon, color }) => (
          <div
            key={key}
            className="flex items-center gap-2 bg-[#0f0f0f] rounded px-2 py-1.5"
          >
            <span className={`${color} text-xs font-bold w-6 text-center`}>{icon}</span>
            <div className="flex-1 min-w-0">
              <div className="text-gray-500 text-[10px] leading-none">{label}</div>
              <div className={`${color} text-sm font-medium`}>
                {Math.round(resources[key as keyof NationResourcePool])}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
