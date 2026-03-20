import { useState } from 'react';
import { Province } from '../../types';
import { TERRAIN_TYPES } from '../../data/gameData';

interface Props {
  province: Province;
  onSaveAllocations: (allocations: { sector: string; percentage: number }[]) => Promise<void>;
  onBack: () => void;
}

const SECTORS = ['food', 'materials', 'energy', 'wealth', 'manpower', 'research'];

const SECTOR_COLORS: Record<string, string> = {
  food: 'accent-green-400',
  materials: 'accent-orange-400',
  energy: 'accent-yellow-400',
  wealth: 'accent-amber-400',
  manpower: 'accent-blue-400',
  research: 'accent-purple-400',
};

export default function ProvinceDetail({ province, onSaveAllocations, onBack }: Props) {
  const [allocations, setAllocations] = useState<Record<string, number>>(() => {
    const defaults: Record<string, number> = {};
    SECTORS.forEach((s) => (defaults[s] = Math.floor(100 / SECTORS.length)));
    // Distribute remainder to food
    defaults.food += 100 - SECTORS.length * Math.floor(100 / SECTORS.length);
    return defaults;
  });
  const [saving, setSaving] = useState(false);

  const totalAllocated = Object.values(allocations).reduce((a, b) => a + b, 0);
  const remaining = 100 - totalAllocated;

  const handleSliderChange = (sector: string, value: number) => {
    setAllocations((prev) => ({ ...prev, [sector]: value }));
  };

  const handleSave = async () => {
    if (remaining !== 0) return;
    setSaving(true);
    try {
      await onSaveAllocations(
        SECTORS.map((sector) => ({ sector, percentage: allocations[sector] }))
      );
    } finally {
      setSaving(false);
    }
  };

  const terrain = TERRAIN_TYPES[province.terrain_type];

  return (
    <div className="space-y-4">
      <button
        onClick={onBack}
        className="text-gray-500 hover:text-amber-500 text-sm transition-colors cursor-pointer"
      >
        &larr; Back to Provinces
      </button>

      <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
        <div className="flex items-center gap-3 mb-4">
          <h2 className="text-gray-200 font-bold text-lg">{province.name}</h2>
          {province.is_capital && (
            <span className="text-amber-500 text-xs font-bold bg-amber-500/10 px-2 py-0.5 rounded">
              Capital
            </span>
          )}
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
          <div>
            <div className="text-gray-500 text-xs">Terrain</div>
            <div className="text-gray-200 text-sm">{terrain?.name || province.terrain_type}</div>
          </div>
          <div>
            <div className="text-gray-500 text-xs">Population</div>
            <div className="text-gray-200 text-sm">{province.population.toLocaleString()}</div>
          </div>
          <div>
            <div className="text-gray-500 text-xs">Stability</div>
            <div
              className={`text-sm ${
                province.local_stability >= 70
                  ? 'text-green-400'
                  : province.local_stability >= 40
                  ? 'text-yellow-400'
                  : 'text-red-400'
              }`}
            >
              {province.local_stability}%
            </div>
          </div>
        </div>

        {/* Resource Output */}
        {province.resources && (
          <div className="mb-4">
            <h3 className="text-gray-300 font-semibold text-xs uppercase tracking-wider mb-2">
              Resource Output
            </h3>
            <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
              {SECTORS.map((sector) => (
                <div key={sector} className="bg-[#0f0f0f] rounded p-2 text-center">
                  <div className="text-gray-500 text-[10px] capitalize">{sector}</div>
                  <div className="text-gray-200 text-sm font-medium">
                    {province.resources![sector as keyof typeof province.resources] ?? 0}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Buildings */}
        {province.buildings && province.buildings.length > 0 && (
          <div className="mb-4">
            <h3 className="text-gray-300 font-semibold text-xs uppercase tracking-wider mb-2">
              Buildings
            </h3>
            <div className="space-y-1">
              {province.buildings.map((b) => (
                <div
                  key={b.id}
                  className="flex items-center justify-between bg-[#0f0f0f] rounded px-3 py-2"
                >
                  <span className="text-gray-200 text-sm capitalize">
                    {b.building_type.replace(/_/g, ' ')}
                  </span>
                  <div className="flex items-center gap-3">
                    <span className="text-gray-400 text-xs">Lv. {b.level}</span>
                    {b.under_construction && (
                      <span className="text-amber-500 text-xs">
                        Building ({b.construction_turns_remaining} turns)
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Sector Allocations */}
        <div>
          <h3 className="text-gray-300 font-semibold text-xs uppercase tracking-wider mb-2">
            Sector Allocations
          </h3>
          <div className="space-y-3">
            {SECTORS.map((sector) => (
              <div key={sector} className="flex items-center gap-3">
                <span className="text-gray-400 text-xs capitalize w-20">{sector}</span>
                <input
                  type="range"
                  min={0}
                  max={100}
                  value={allocations[sector]}
                  onChange={(e) => handleSliderChange(sector, Number(e.target.value))}
                  className={`flex-1 h-1.5 rounded-lg appearance-none bg-[#2a2a2a] ${SECTOR_COLORS[sector]}`}
                />
                <span className="text-gray-300 text-xs w-10 text-right">
                  {allocations[sector]}%
                </span>
              </div>
            ))}
          </div>
          <div className="flex items-center justify-between mt-3 pt-3 border-t border-[#2a2a2a]">
            <span
              className={`text-xs ${
                remaining === 0
                  ? 'text-green-400'
                  : remaining > 0
                  ? 'text-yellow-400'
                  : 'text-red-400'
              }`}
            >
              {remaining === 0
                ? 'Fully allocated'
                : remaining > 0
                ? `${remaining}% remaining`
                : `${Math.abs(remaining)}% over-allocated`}
            </span>
            <button
              onClick={handleSave}
              disabled={remaining !== 0 || saving}
              className="bg-amber-600 text-white rounded px-4 py-1.5 text-xs font-medium hover:bg-amber-700 transition-colors disabled:opacity-50 cursor-pointer"
            >
              {saving ? 'Saving...' : 'Save Allocations'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
