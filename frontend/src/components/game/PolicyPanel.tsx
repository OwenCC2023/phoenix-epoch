import { POLICY_CATEGORIES } from '../../data/policyData';
import { NationPolicy } from '../../types';

interface Props {
  policies: NationPolicy[];
}

export default function PolicyPanel({ policies }: Props) {
  const policyMap = new Map<string, number>();
  for (const p of policies) {
    policyMap.set(p.category, p.level);
  }

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-4">
        National Policies
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {POLICY_CATEGORIES.map((cat) => {
          const currentLevel = policyMap.get(cat.key) ?? cat.defaultLevel;
          const level = cat.levels[currentLevel];
          return (
            <div key={cat.key} className="bg-[#0f0f0f] rounded p-3">
              <div className="text-gray-400 text-xs mb-1">{cat.name}</div>
              <div className="text-gray-200 text-sm font-medium">
                {level?.name ?? `Level ${currentLevel}`}
              </div>
              <div className="text-gray-500 text-xs mt-0.5">
                {level?.description ?? ''}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
