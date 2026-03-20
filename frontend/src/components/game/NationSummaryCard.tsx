import { Nation } from '../../types';
import { GOVERNMENT_TYPES } from '../../data/gameData';
import { ALL_TRAITS } from '../../data/traitData';

interface Props {
  nation: Nation;
}

export default function NationSummaryCard({ nation }: Props) {
  const govt = GOVERNMENT_TYPES.find((g) => g.key === nation.government_type);
  const traits = nation.ideology_traits;
  const strongTrait = traits?.strong ? ALL_TRAITS[traits.strong] : null;
  const weakTraits = (traits?.weak ?? []).map((k) => ALL_TRAITS[k]).filter(Boolean);

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-gray-200 font-bold text-lg">{nation.name}</h2>
        <span
          className={`text-xs px-2 py-0.5 rounded-full ${
            nation.is_alive
              ? 'bg-green-500/20 text-green-400'
              : 'bg-red-500/20 text-red-400'
          }`}
        >
          {nation.is_alive ? 'Active' : 'Eliminated'}
        </span>
      </div>
      {nation.motto && (
        <p className="text-gray-500 text-xs italic mb-3">"{nation.motto}"</p>
      )}
      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <span className="text-gray-500 text-xs w-20">Government</span>
          <span className="text-amber-500 text-xs font-medium">
            {govt?.name || nation.government_type}
          </span>
        </div>
        <div className="flex items-start gap-2">
          <span className="text-gray-500 text-xs w-20">Traits</span>
          <div className="flex flex-wrap gap-1">
            {strongTrait && (
              <span className="text-xs px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 font-medium">
                {strongTrait.name}
              </span>
            )}
            {weakTraits.map((t) => (
              <span key={t.key} className="text-xs px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-500/70">
                {t.name}
              </span>
            ))}
          </div>
        </div>
      </div>
      {nation.description && (
        <p className="text-gray-400 text-xs mt-3 border-t border-[#2a2a2a] pt-3">
          {nation.description}
        </p>
      )}
    </div>
  );
}
