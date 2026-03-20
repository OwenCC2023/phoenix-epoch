import { useState } from 'react';
import { Formation, MilitaryDomain, Province, Nation } from '../../types';
import { useTurnStore } from '../../store/turnStore';
import { GOVERNMENT_TYPES } from '../../data/gameData';
import { POLICY_CATEGORIES } from '../../data/policyData';

type OrderTab =
  | 'set_allocation'
  | 'build_improvement'
  | 'trade_offer'
  | 'policy_change'
  | 'train_unit'
  | 'create_formation'
  | 'assign_to_formation'
  | 'create_group';

const UNIT_TYPES_BY_DOMAIN: Record<MilitaryDomain, string[]> = {
  army: ['militia', 'infantry', 'motorized', 'armored', 'artillery'],
  navy: ['patrol_boat', 'frigate', 'transport'],
  air: ['scout_plane', 'fighter', 'bomber'],
};

interface Props {
  gameId: number;
  provinces: Province[];
  otherNations: Nation[];
  formations?: Formation[];
}

const IMPROVEMENT_TYPES = [
  // Core
  'workshop', 'factory', 'refinery', 'arms_factory',
  // Financial
  'trading_post', 'bank', 'stock_exchange',
  // Light manufacturing
  'textile_mill', 'electronics_factory', 'precision_workshop',
  // Heavy manufacturing
  'heavy_forge', 'industrial_complex', 'shipyard',
  // Refining
  'advanced_refinery', 'fuel_depot', 'biofuel_plant',
  // Chemical
  'chemical_plant', 'fertilizer_plant', 'plastics_factory',
  // Pharmaceutical
  'pharmaceutical_lab', 'medical_supply_depot', 'research_institute',
  // Farming
  'irrigation_network', 'grain_silo', 'agricultural_station',
  // Extraction
  'mine', 'oil_well', 'logging_camp',
  // Construction
  'construction_yard', 'cement_plant', 'infrastructure_bureau',
  // Transport
  'road_network', 'railway_station', 'logistics_hub',
  // Communications
  'radio_tower', 'telegraph_network', 'broadcasting_station',
  // Entertainment
  'tavern', 'theatre', 'resort',
  // Healthcare
  'clinic', 'hospital', 'sanitation_works',
  // Religious
  'church', 'madrasa', 'holy_site',
  // Green energy
  'wind_farm', 'solar_array', 'hydroelectric_dam',
  // Government
  'regulatory_office', 'standards_bureau',
  'inspector_general', 'audit_commission',
  'civil_service_academy', 'administrative_center',
  'police_headquarters', 'intelligence_agency',
  'public_school', 'university',
  'labor_bureau', 'workers_council',
  'social_services_office', 'public_housing',
];

const SECTORS = ['food', 'materials', 'energy', 'wealth', 'manpower', 'research'];
const RESOURCES = ['food', 'materials', 'energy', 'wealth', 'manpower', 'research'];

export default function OrderForm({ gameId, provinces, otherNations, formations = [] }: Props) {
  const createOrder = useTurnStore((s) => s.createOrder);
  const [activeTab, setActiveTab] = useState<OrderTab>('set_allocation');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Set Allocation state
  const [allocProvince, setAllocProvince] = useState<number>(provinces[0]?.id ?? 0);
  const [allocations, setAllocations] = useState<Record<string, number>>(
    Object.fromEntries(SECTORS.map((s) => [s, Math.floor(100 / 6)]))
  );

  // Build Improvement state
  const [buildProvince, setBuildProvince] = useState<number>(provinces[0]?.id ?? 0);
  const [improvementType, setImprovementType] = useState(IMPROVEMENT_TYPES[0]);

  // Trade Offer state
  const [tradeNation, setTradeNation] = useState<number>(otherNations[0]?.id ?? 0);
  const [offering, setOffering] = useState<Record<string, number>>({});
  const [requesting, setRequesting] = useState<Record<string, number>>({});

  // Policy Change state
  const [policyType, setPolicyType] = useState<'government' | 'policy_level'>('government');
  const [policyValue, setPolicyValue] = useState('');
  const [policyCategory, setPolicyCategory] = useState(POLICY_CATEGORIES[0]?.key ?? '');
  const [policyLevel, setPolicyLevel] = useState(0);

  // Train Unit state
  const [trainProvince, setTrainProvince] = useState<number>(provinces[0]?.id ?? 0);
  const [trainDomain, setTrainDomain] = useState<MilitaryDomain>('army');
  const [trainUnitType, setTrainUnitType] = useState(UNIT_TYPES_BY_DOMAIN.army[0]);
  const [trainQuantity, setTrainQuantity] = useState(1);
  const [trainFormationId, setTrainFormationId] = useState<number | ''>('');

  // Create Formation state
  const [formationName, setFormationName] = useState('');
  const [formationDomain, setFormationDomain] = useState<MilitaryDomain>('army');
  const [formationProvince, setFormationProvince] = useState<number>(provinces[0]?.id ?? 0);

  // Assign to Formation state
  const [assignUnitType, setAssignUnitType] = useState('militia');
  const [assignQuantity, setAssignQuantity] = useState(1);
  const [assignSourceId, setAssignSourceId] = useState<number | ''>(formations[0]?.id ?? '');
  const [assignTargetId, setAssignTargetId] = useState<number | ''>(formations[1]?.id ?? '');

  // Create Group state
  const [groupName, setGroupName] = useState('');

  const handleAllocChange = (sector: string, value: number) => {
    setAllocations((prev) => ({ ...prev, [sector]: value }));
  };

  const allocTotal = Object.values(allocations).reduce((a, b) => a + b, 0);

  const handleSubmit = async () => {
    setSubmitting(true);
    setError(null);
    setSuccess(null);
    try {
      let payload: Record<string, any> = {};

      switch (activeTab) {
        case 'set_allocation':
          if (allocTotal !== 100) {
            setError('Allocations must sum to 100');
            setSubmitting(false);
            return;
          }
          payload = {
            province_id: allocProvince,
            allocations: SECTORS.map((s) => ({ sector: s, percentage: allocations[s] })),
          };
          break;
        case 'build_improvement':
          payload = {
            province_id: buildProvince,
            improvement_type: improvementType,
          };
          break;
        case 'trade_offer':
          payload = {
            to_nation: tradeNation,
            offering,
            requesting,
          };
          break;
        case 'policy_change':
          if (policyType === 'government') {
            payload = {
              change_type: 'government',
              new_value: policyValue,
            };
          } else {
            payload = {
              change_type: 'policy_level',
              category: policyCategory,
              new_level: policyLevel,
            };
          }
          break;
        case 'train_unit':
          payload = {
            province_id: trainProvince,
            unit_type: trainUnitType,
            quantity: trainQuantity,
            ...(trainFormationId !== '' && { formation_id: trainFormationId }),
          };
          break;
        case 'create_formation':
          if (!formationName.trim()) {
            setError('Formation name is required');
            setSubmitting(false);
            return;
          }
          payload = {
            name: formationName.trim(),
            domain: formationDomain,
            province_id: formationProvince,
          };
          break;
        case 'assign_to_formation':
          if (assignSourceId === '' || assignTargetId === '') {
            setError('Select both source and target formations');
            setSubmitting(false);
            return;
          }
          payload = {
            unit_type: assignUnitType,
            quantity: assignQuantity,
            source_formation_id: assignSourceId,
            target_formation_id: assignTargetId,
          };
          break;
        case 'create_group':
          if (!groupName.trim()) {
            setError('Group name is required');
            setSubmitting(false);
            return;
          }
          payload = { name: groupName.trim() };
          break;
      }

      await createOrder(gameId, activeTab, payload);
      setSuccess('Order created successfully');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create order');
    } finally {
      setSubmitting(false);
    }
  };

  const tabs: { key: OrderTab; label: string }[] = [
    { key: 'set_allocation', label: 'Allocations' },
    { key: 'build_improvement', label: 'Build' },
    { key: 'trade_offer', label: 'Trade' },
    { key: 'policy_change', label: 'Policy' },
    { key: 'train_unit', label: 'Train' },
    { key: 'create_formation', label: 'Formation' },
    { key: 'assign_to_formation', label: 'Assign' },
    { key: 'create_group', label: 'Group' },
  ];

  return (
    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-4">
        Create Order
      </h3>

      {/* Tab selector */}
      <div className="flex gap-1 mb-4 border-b border-[#2a2a2a]">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => { setActiveTab(tab.key); setError(null); setSuccess(null); }}
            className={`px-3 py-2 text-xs font-medium transition-colors cursor-pointer ${
              activeTab === tab.key
                ? 'text-amber-500 border-b-2 border-amber-500 -mb-px'
                : 'text-gray-500 hover:text-gray-300'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Set Allocation */}
      {activeTab === 'set_allocation' && (
        <div className="space-y-3">
          <div>
            <label className="text-gray-400 text-xs block mb-1">Province</label>
            <select
              value={allocProvince}
              onChange={(e) => setAllocProvince(Number(e.target.value))}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
            >
              {provinces.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          {SECTORS.map((sector) => (
            <div key={sector} className="flex items-center gap-3">
              <span className="text-gray-400 text-xs capitalize w-20">{sector}</span>
              <input
                type="range"
                min={0}
                max={100}
                value={allocations[sector] ?? 0}
                onChange={(e) => handleAllocChange(sector, Number(e.target.value))}
                className="flex-1 accent-amber-500"
              />
              <span className="text-gray-200 text-xs w-8 text-right">{allocations[sector] ?? 0}%</span>
            </div>
          ))}
          <div className={`text-xs text-right ${allocTotal === 100 ? 'text-green-400' : 'text-red-400'}`}>
            Total: {allocTotal}%
          </div>
        </div>
      )}

      {/* Build Improvement */}
      {activeTab === 'build_improvement' && (
        <div className="space-y-3">
          <div>
            <label className="text-gray-400 text-xs block mb-1">Province</label>
            <select
              value={buildProvince}
              onChange={(e) => setBuildProvince(Number(e.target.value))}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
            >
              {provinces.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-gray-400 text-xs block mb-1">Improvement Type</label>
            <select
              value={improvementType}
              onChange={(e) => setImprovementType(e.target.value)}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
            >
              {IMPROVEMENT_TYPES.map((t) => (
                <option key={t} value={t}>{t.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}</option>
              ))}
            </select>
          </div>
        </div>
      )}

      {/* Trade Offer */}
      {activeTab === 'trade_offer' && (
        <div className="space-y-3">
          <div>
            <label className="text-gray-400 text-xs block mb-1">Target Nation</label>
            <select
              value={tradeNation}
              onChange={(e) => setTradeNation(Number(e.target.value))}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
            >
              {otherNations.map((n) => (
                <option key={n.id} value={n.id}>{n.name}</option>
              ))}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-gray-400 text-xs mb-2 font-medium">Offering</div>
              {RESOURCES.map((r) => (
                <div key={r} className="flex items-center gap-2 mb-1">
                  <span className="text-gray-500 text-xs capitalize w-16">{r}</span>
                  <input
                    type="number"
                    min={0}
                    value={offering[r] ?? 0}
                    onChange={(e) => setOffering((prev) => ({ ...prev, [r]: Number(e.target.value) }))}
                    className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-2 py-1 text-gray-200 text-xs"
                  />
                </div>
              ))}
            </div>
            <div>
              <div className="text-gray-400 text-xs mb-2 font-medium">Requesting</div>
              {RESOURCES.map((r) => (
                <div key={r} className="flex items-center gap-2 mb-1">
                  <span className="text-gray-500 text-xs capitalize w-16">{r}</span>
                  <input
                    type="number"
                    min={0}
                    value={requesting[r] ?? 0}
                    onChange={(e) => setRequesting((prev) => ({ ...prev, [r]: Number(e.target.value) }))}
                    className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-2 py-1 text-gray-200 text-xs"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Policy Change */}
      {activeTab === 'policy_change' && (
        <div className="space-y-3">
          <div>
            <label className="text-gray-400 text-xs block mb-1">Change Type</label>
            <select
              value={policyType}
              onChange={(e) => { setPolicyType(e.target.value as 'government' | 'policy_level'); setPolicyValue(''); }}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
            >
              <option value="government">Government Type</option>
              <option value="policy_level">Policy Level</option>
            </select>
          </div>
          {policyType === 'government' && (
            <div>
              <label className="text-gray-400 text-xs block mb-1">New Government</label>
              <select
                value={policyValue}
                onChange={(e) => setPolicyValue(e.target.value)}
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
              >
                <option value="">Select...</option>
                {GOVERNMENT_TYPES.map((opt) => (
                  <option key={opt.key} value={opt.key}>{opt.name}</option>
                ))}
              </select>
            </div>
          )}
          {policyType === 'policy_level' && (
            <>
              <div>
                <label className="text-gray-400 text-xs block mb-1">Policy Category</label>
                <select
                  value={policyCategory}
                  onChange={(e) => {
                    setPolicyCategory(e.target.value);
                    const cat = POLICY_CATEGORIES.find((c) => c.key === e.target.value);
                    setPolicyLevel(cat?.defaultLevel ?? 0);
                  }}
                  className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
                >
                  {POLICY_CATEGORIES.map((cat) => (
                    <option key={cat.key} value={cat.key}>{cat.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-gray-400 text-xs block mb-1">Level</label>
                <select
                  value={policyLevel}
                  onChange={(e) => setPolicyLevel(Number(e.target.value))}
                  className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
                >
                  {(POLICY_CATEGORIES.find((c) => c.key === policyCategory)?.levels ?? []).map((lv, i) => (
                    <option key={lv.key} value={i}>{lv.name} — {lv.description}</option>
                  ))}
                </select>
              </div>
            </>
          )}
        </div>
      )}

      {/* Train Unit */}
      {activeTab === 'train_unit' && (
        <div className="space-y-3">
          <div>
            <label className="text-gray-400 text-xs block mb-1">Province (training base)</label>
            <select value={trainProvince} onChange={(e) => setTrainProvince(Number(e.target.value))}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm">
              {provinces.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </div>
          <div>
            <label className="text-gray-400 text-xs block mb-1">Domain</label>
            <select value={trainDomain} onChange={(e) => {
              const d = e.target.value as MilitaryDomain;
              setTrainDomain(d);
              setTrainUnitType(UNIT_TYPES_BY_DOMAIN[d][0]);
            }} className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm">
              {(['army', 'navy', 'air'] as MilitaryDomain[]).map((d) => (
                <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-gray-400 text-xs block mb-1">Unit Type</label>
            <select value={trainUnitType} onChange={(e) => setTrainUnitType(e.target.value)}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm">
              {UNIT_TYPES_BY_DOMAIN[trainDomain].map((u) => (
                <option key={u} value={u}>{u.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-gray-400 text-xs block mb-1">Quantity</label>
            <input type="number" min={1} value={trainQuantity}
              onChange={(e) => setTrainQuantity(Math.max(1, Number(e.target.value)))}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm" />
          </div>
          {formations.length > 0 && (
            <div>
              <label className="text-gray-400 text-xs block mb-1">Formation (optional — uses reserve if blank)</label>
              <select value={trainFormationId}
                onChange={(e) => setTrainFormationId(e.target.value === '' ? '' : Number(e.target.value))}
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm">
                <option value="">Reserve (auto)</option>
                {formations.filter((f) => f.domain === trainDomain).map((f) => (
                  <option key={f.id} value={f.id}>{f.name} [{f.formation_type}]</option>
                ))}
              </select>
            </div>
          )}
        </div>
      )}

      {/* Create Formation */}
      {activeTab === 'create_formation' && (
        <div className="space-y-3">
          <div>
            <label className="text-gray-400 text-xs block mb-1">Formation Name</label>
            <input type="text" value={formationName} onChange={(e) => setFormationName(e.target.value)}
              placeholder="e.g. 1st Army Division"
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm" />
          </div>
          <div>
            <label className="text-gray-400 text-xs block mb-1">Domain</label>
            <select value={formationDomain} onChange={(e) => setFormationDomain(e.target.value as MilitaryDomain)}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm">
              {(['army', 'navy', 'air'] as MilitaryDomain[]).map((d) => (
                <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-gray-400 text-xs block mb-1">Province</label>
            <select value={formationProvince} onChange={(e) => setFormationProvince(Number(e.target.value))}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm">
              {provinces.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </div>
        </div>
      )}

      {/* Assign to Formation */}
      {activeTab === 'assign_to_formation' && (
        <div className="space-y-3">
          <div>
            <label className="text-gray-400 text-xs block mb-1">Unit Type</label>
            <input type="text" value={assignUnitType} onChange={(e) => setAssignUnitType(e.target.value)}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm" />
          </div>
          <div>
            <label className="text-gray-400 text-xs block mb-1">Quantity</label>
            <input type="number" min={1} value={assignQuantity}
              onChange={(e) => setAssignQuantity(Math.max(1, Number(e.target.value)))}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm" />
          </div>
          <div>
            <label className="text-gray-400 text-xs block mb-1">Source Formation</label>
            <select value={assignSourceId}
              onChange={(e) => setAssignSourceId(e.target.value === '' ? '' : Number(e.target.value))}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm">
              <option value="">Select...</option>
              {formations.map((f) => <option key={f.id} value={f.id}>{f.name} [{f.domain}]</option>)}
            </select>
          </div>
          <div>
            <label className="text-gray-400 text-xs block mb-1">Target Formation</label>
            <select value={assignTargetId}
              onChange={(e) => setAssignTargetId(e.target.value === '' ? '' : Number(e.target.value))}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm">
              <option value="">Select...</option>
              {formations.map((f) => <option key={f.id} value={f.id}>{f.name} [{f.domain}]</option>)}
            </select>
          </div>
        </div>
      )}

      {/* Create Group */}
      {activeTab === 'create_group' && (
        <div className="space-y-3">
          <div>
            <label className="text-gray-400 text-xs block mb-1">Group Name</label>
            <input type="text" value={groupName} onChange={(e) => setGroupName(e.target.value)}
              placeholder="e.g. Northern Front"
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm" />
          </div>
        </div>
      )}

      {error && <p className="text-red-400 text-xs mt-3">{error}</p>}
      {success && <p className="text-green-400 text-xs mt-3">{success}</p>}

      <button
        onClick={handleSubmit}
        disabled={submitting}
        className="mt-4 w-full bg-amber-600 hover:bg-amber-700 disabled:opacity-50 text-white text-sm font-medium py-2 rounded transition-colors cursor-pointer"
      >
        {submitting ? 'Creating...' : 'Create Order'}
      </button>
    </div>
  );
}
