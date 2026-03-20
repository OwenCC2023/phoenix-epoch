import { GOVERNMENT_TYPES, GovernmentTypeDef } from '../../data/gameData';

interface Props {
  selected: string;
  onSelect: (key: string) => void;
}

export default function GovernmentTypeSelector({ selected, onSelect }: Props) {
  return (
    <div>
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
        Government Type
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
        {GOVERNMENT_TYPES.map((govt: GovernmentTypeDef) => (
          <button
            key={govt.key}
            type="button"
            onClick={() => onSelect(govt.key)}
            className={`text-left p-4 rounded-lg border transition-all cursor-pointer ${
              selected === govt.key
                ? 'border-amber-500 bg-amber-500/10'
                : 'border-[#2a2a2a] bg-[#1a1a1a] hover:border-[#3a3a3a]'
            }`}
          >
            <div className="text-gray-200 font-medium text-sm mb-1">{govt.name}</div>
            <div className="text-gray-500 text-xs mb-2">{govt.description}</div>
            <div className="space-y-1">
              {govt.modifiers.map((mod, i) => (
                <div
                  key={i}
                  className={`text-xs ${mod.value >= 0 ? 'text-green-400' : 'text-red-400'}`}
                >
                  {mod.label}
                </div>
              ))}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
