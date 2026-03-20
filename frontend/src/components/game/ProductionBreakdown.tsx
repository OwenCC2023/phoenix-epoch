import { ResourceLedger } from '../../types';

interface Props {
  ledger: ResourceLedger[];
}

const RESOURCE_KEYS = ['food', 'materials', 'energy', 'wealth', 'manpower', 'research'];

const RESOURCE_COLORS: Record<string, string> = {
  food: 'text-green-400',
  materials: 'text-orange-400',
  energy: 'text-yellow-400',
  wealth: 'text-amber-400',
  manpower: 'text-blue-400',
  research: 'text-purple-400',
};

function formatValue(val: number | undefined): string {
  if (val === undefined || val === null) return '0';
  const rounded = Math.round(val);
  if (rounded >= 0) return `+${rounded}`;
  return `${rounded}`;
}

export default function ProductionBreakdown({ ledger }: Props) {
  if (ledger.length === 0) {
    return (
      <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
        <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
          Production Breakdown
        </h3>
        <p className="text-gray-500 text-sm py-4 text-center">No turn data yet.</p>
      </div>
    );
  }

  const latest = ledger[ledger.length - 1];

  const stages = [
    { label: 'Province Production', data: latest.province_production_total },
    { label: 'Integration Losses', data: latest.integration_losses },
    { label: 'National Modifiers', data: latest.national_modifier_effects },
    { label: 'Trade Net', data: latest.trade_net },
    { label: 'Consumption', data: latest.consumption },
    { label: 'Final Pools', data: latest.final_pools },
  ];

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-1">
        Production Breakdown
      </h3>
      <p className="text-gray-500 text-xs mb-4">Turn {latest.turn_number}</p>

      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="text-gray-500 uppercase tracking-wider border-b border-[#2a2a2a]">
              <th className="text-left py-2 px-2">Stage</th>
              {RESOURCE_KEYS.map((key) => (
                <th key={key} className={`text-right py-2 px-2 ${RESOURCE_COLORS[key]}`}>
                  {key.charAt(0).toUpperCase() + key.slice(1)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {stages.map((stage, idx) => (
              <tr
                key={stage.label}
                className={`border-b border-[#2a2a2a] ${
                  idx === stages.length - 1 ? 'bg-[#2a2a2a]/30 font-medium' : ''
                }`}
              >
                <td className="py-2 px-2 text-gray-300">{stage.label}</td>
                {RESOURCE_KEYS.map((key) => {
                  const val = stage.data?.[key];
                  const isLast = idx === stages.length - 1;
                  return (
                    <td
                      key={key}
                      className={`py-2 px-2 text-right ${
                        isLast
                          ? RESOURCE_COLORS[key]
                          : val !== undefined && val < 0
                          ? 'text-red-400'
                          : 'text-gray-400'
                      }`}
                    >
                      {isLast
                        ? Math.round(val ?? 0)
                        : formatValue(val)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
