import { TRAIT_PAIRS, TraitDef } from '../../data/traitData';

export interface TraitSelection {
  strong: string;
  weak: string[];
}

interface Props {
  selection: TraitSelection;
  onSelect: (selection: TraitSelection) => void;
}

export default function TraitSelector({ selection, onSelect }: Props) {
  const selectedPairs = new Set<number>();
  if (selection.strong) {
    const t = findTrait(selection.strong);
    if (t) selectedPairs.add(t.pairIndex);
  }
  for (const w of selection.weak) {
    const t = findTrait(w);
    if (t) selectedPairs.add(t.pairIndex);
  }

  const handleClick = (trait: TraitDef) => {
    const key = trait.key;

    // Already strong → deselect entirely
    if (selection.strong === key) {
      onSelect({ strong: '', weak: selection.weak });
      return;
    }

    // Already weak → promote to strong (demote current strong to weak if exists)
    const weakIdx = selection.weak.indexOf(key);
    if (weakIdx !== -1) {
      const newWeak = [...selection.weak];
      newWeak.splice(weakIdx, 1);
      if (selection.strong) {
        newWeak.push(selection.strong);
      }
      onSelect({ strong: key, weak: newWeak });
      return;
    }

    // Not selected yet — check constraints
    // Can't pick opposing trait
    const pairIndex = trait.pairIndex;
    const pair = TRAIT_PAIRS[pairIndex];
    const opposing = pair.traits[0].key === key ? pair.traits[1].key : pair.traits[0].key;
    if (selection.strong === opposing || selection.weak.includes(opposing)) {
      return; // pair already occupied by the other side
    }

    // Can't exceed 3 traits total from 3 different pairs
    const totalSelected = (selection.strong ? 1 : 0) + selection.weak.length;
    if (totalSelected >= 3) return;

    // Can't pick from a pair that's already represented
    if (selectedPairs.has(pairIndex)) return;

    // Add as weak
    onSelect({ ...selection, weak: [...selection.weak, key] });
  };

  const getTraitState = (key: string): 'strong' | 'weak' | 'none' | 'disabled' => {
    if (selection.strong === key) return 'strong';
    if (selection.weak.includes(key)) return 'weak';

    const t = findTrait(key);
    if (!t) return 'disabled';

    // Check if opposing trait is selected
    const pair = TRAIT_PAIRS[t.pairIndex];
    const opposing = pair.traits[0].key === key ? pair.traits[1].key : pair.traits[0].key;
    if (selection.strong === opposing || selection.weak.includes(opposing)) return 'disabled';

    // Check if we're already at 3
    const totalSelected = (selection.strong ? 1 : 0) + selection.weak.length;
    if (totalSelected >= 3 && !selectedPairs.has(t.pairIndex)) return 'disabled';

    return 'none';
  };

  const stateStyles = {
    strong: 'border-amber-500 bg-amber-500/20 ring-1 ring-amber-500/50',
    weak: 'border-amber-500/50 bg-amber-500/10',
    none: 'border-[#2a2a2a] bg-[#1a1a1a] hover:border-[#3a3a3a]',
    disabled: 'border-[#2a2a2a] bg-[#1a1a1a] opacity-40 cursor-not-allowed',
  };

  const stateLabels = {
    strong: 'STRONG',
    weak: 'WEAK',
    none: '',
    disabled: '',
  };

  return (
    <div>
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-1">
        Ideology Traits
      </h3>
      <p className="text-gray-500 text-xs mb-3">
        Select 3 traits from 3 different pairs. Click to select (weak), click again to promote to strong. 1 strong + 2 weak.
      </p>
      <div className="space-y-2">
        {TRAIT_PAIRS.map((pair, pairIdx) => (
          <div key={pairIdx} className="flex gap-2">
            {pair.traits.map((trait) => {
              const state = getTraitState(trait.key);
              return (
                <button
                  key={trait.key}
                  type="button"
                  onClick={() => state !== 'disabled' && handleClick(trait)}
                  className={`flex-1 text-left p-3 rounded-lg border transition-all ${
                    state !== 'disabled' ? 'cursor-pointer' : ''
                  } ${stateStyles[state]}`}
                >
                  <div className="flex items-center justify-between mb-0.5">
                    <span className="text-gray-200 font-medium text-sm">{trait.name}</span>
                    {stateLabels[state] && (
                      <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${
                        state === 'strong'
                          ? 'bg-amber-500/30 text-amber-400'
                          : 'bg-amber-500/15 text-amber-500/70'
                      }`}>
                        {stateLabels[state]}
                      </span>
                    )}
                  </div>
                  <div className="text-gray-500 text-xs">{trait.description}</div>
                </button>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

function findTrait(key: string): TraitDef | undefined {
  for (const pair of TRAIT_PAIRS) {
    for (const t of pair.traits) {
      if (t.key === key) return t;
    }
  }
  return undefined;
}
