import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import GovernmentTypeSelector from '../components/game/GovernmentTypeSelector';
import TraitSelector, { TraitSelection } from '../components/game/TraitSelector';
import { useNationStore } from '../store/nationStore';
import { GOVERNMENT_TYPES, ModifierDef } from '../data/gameData';

export default function NationCreatePage() {
  const { gameId } = useParams<{ gameId: string }>();
  const navigate = useNavigate();
  const { createNation, loading, error } = useNationStore();

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [motto, setMotto] = useState('');
  const [governmentType, setGovernmentType] = useState('');
  const [traitSelection, setTraitSelection] = useState<TraitSelection>({
    strong: '',
    weak: [],
  });

  const traitsValid =
    traitSelection.strong !== '' && traitSelection.weak.length === 2;

  const govModifiers = GOVERNMENT_TYPES.find((g) => g.key === governmentType)?.modifiers ?? [];

  const canSubmit = name.trim() && governmentType && traitsValid && !loading;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;
    try {
      await createNation(Number(gameId), {
        name: name.trim(),
        description: description.trim() || undefined,
        government_type: governmentType,
        ideology_traits: {
          strong: traitSelection.strong,
          weak: traitSelection.weak,
        },
        motto: motto.trim() || undefined,
      });
      navigate(`/games/${gameId}/dashboard`);
    } catch {
      // error is set in store
    }
  };

  return (
    <div className="min-h-screen bg-[#0f0f0f]">
      <Header />

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button
          onClick={() => navigate(`/games/${gameId}`)}
          className="text-gray-500 hover:text-amber-500 text-sm mb-4 transition-colors cursor-pointer"
        >
          &larr; Back to Lobby
        </button>

        <h1 className="text-gray-200 text-2xl font-bold mb-6">Found Your Nation</h1>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-sm rounded p-3 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5 space-y-4">
            <h2 className="text-gray-300 font-semibold text-sm uppercase tracking-wider">
              Nation Identity
            </h2>
            <div>
              <label className="block text-gray-400 text-xs mb-1">
                Nation Name <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="The Republic of New Dawn"
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm placeholder-gray-600 focus:border-amber-500 focus:outline-none transition-colors"
                maxLength={100}
              />
            </div>
            <div>
              <label className="block text-gray-400 text-xs mb-1">Motto</label>
              <input
                type="text"
                value={motto}
                onChange={(e) => setMotto(e.target.value)}
                placeholder="From the ashes, we rise"
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm placeholder-gray-600 focus:border-amber-500 focus:outline-none transition-colors"
                maxLength={200}
              />
            </div>
            <div>
              <label className="block text-gray-400 text-xs mb-1">Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="A brief description of your nation's backstory..."
                rows={3}
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm placeholder-gray-600 focus:border-amber-500 focus:outline-none transition-colors resize-none"
                maxLength={1000}
              />
            </div>
          </div>

          {/* Government Type */}
          <GovernmentTypeSelector selected={governmentType} onSelect={setGovernmentType} />

          {/* Ideology Traits */}
          <TraitSelector selection={traitSelection} onSelect={setTraitSelection} />

          {/* Government Modifier Preview */}
          {govModifiers.length > 0 && (
            <div className="bg-[#1a1a1a] border border-amber-500/30 rounded-lg p-5">
              <h3 className="text-amber-500 font-semibold text-sm uppercase tracking-wider mb-3">
                Government Modifiers
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {govModifiers.map((mod: ModifierDef, i: number) => (
                  <div
                    key={i}
                    className={`text-sm ${mod.value >= 0 ? 'text-green-400' : 'text-red-400'}`}
                  >
                    {mod.label}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Submit */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={!canSubmit}
              className="bg-amber-600 text-white rounded px-6 py-2.5 text-sm font-medium hover:bg-amber-700 transition-colors disabled:opacity-50 cursor-pointer"
            >
              {loading ? 'Founding...' : 'Found Nation'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}
