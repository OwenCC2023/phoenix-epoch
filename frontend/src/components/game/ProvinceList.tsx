import { Province } from '../../types';
import { TERRAIN_TYPES } from '../../data/gameData';

interface Props {
  provinces: Province[];
  onSelect: (province: Province) => void;
}

export default function ProvinceList({ provinces, onSelect }: Props) {
  if (provinces.length === 0) {
    return (
      <div className="text-gray-500 text-sm py-8 text-center">
        No provinces owned yet.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-gray-500 text-xs uppercase tracking-wider border-b border-[#2a2a2a]">
            <th className="text-left py-2 px-3">Name</th>
            <th className="text-left py-2 px-3">Terrain</th>
            <th className="text-right py-2 px-3">Population</th>
            <th className="text-right py-2 px-3">Stability</th>
            <th className="text-center py-2 px-3">Capital</th>
          </tr>
        </thead>
        <tbody>
          {provinces.map((province) => (
            <tr
              key={province.id}
              onClick={() => onSelect(province)}
              className="border-b border-[#2a2a2a] hover:bg-[#2a2a2a]/50 cursor-pointer transition-colors"
            >
              <td className="py-2.5 px-3 text-gray-200 font-medium">{province.name}</td>
              <td className="py-2.5 px-3 text-gray-400">
                {TERRAIN_TYPES[province.terrain_type]?.name || province.terrain_type}
              </td>
              <td className="py-2.5 px-3 text-gray-300 text-right">
                {province.population.toLocaleString()}
              </td>
              <td className="py-2.5 px-3 text-right">
                <span
                  className={
                    province.local_stability >= 70
                      ? 'text-green-400'
                      : province.local_stability >= 40
                      ? 'text-yellow-400'
                      : 'text-red-400'
                  }
                >
                  {province.local_stability}%
                </span>
              </td>
              <td className="py-2.5 px-3 text-center">
                {province.is_capital && (
                  <span className="text-amber-500 text-xs font-bold">★</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
