import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../components/Header';
import { AdminOverview, GameEvent, AdminNationData } from '../types';
import * as adminApi from '../api/admin';

export default function AdminPanelPage() {
  const { gameId } = useParams<{ gameId: string }>();
  const gId = Number(gameId);

  const [overview, setOverview] = useState<AdminOverview | null>(null);
  const [events, setEvents] = useState<GameEvent[]>([]);
  const [templates, setTemplates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Event form state
  const [eventTitle, setEventTitle] = useState('');
  const [eventDescription, setEventDescription] = useState('');
  const [eventScope, setEventScope] = useState<'global' | 'targeted'>('global');
  const [affectedNations, setAffectedNations] = useState<number[]>([]);
  const [effectsJson, setEffectsJson] = useState('{}');
  const [expiresTurn, setExpiresTurn] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, eventsRes, templatesRes] = await Promise.all([
          adminApi.getAdminOverview(gId),
          adminApi.listEvents(gId),
          adminApi.getEventTemplates(gId).catch(() => ({ data: [] })),
        ]);
        setOverview(overviewRes.data);
        setEvents(eventsRes.data);
        setTemplates(Array.isArray(templatesRes.data) ? templatesRes.data : []);
      } catch {
        setError('Failed to load admin data');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [gId]);

  const handleAction = async (action: 'pause' | 'resume' | 'force-resolve') => {
    setActionLoading(action);
    setError(null);
    try {
      if (action === 'pause') await adminApi.pauseGame(gId);
      else if (action === 'resume') await adminApi.resumeGame(gId);
      else await adminApi.forceResolve(gId);
      // Refresh overview
      const { data } = await adminApi.getAdminOverview(gId);
      setOverview(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || `Failed to ${action}`);
    } finally {
      setActionLoading(null);
    }
  };

  const handleTemplateSelect = (templateName: string) => {
    setSelectedTemplate(templateName);
    const template = templates.find((t: any) => t.name === templateName || t.title === templateName);
    if (template) {
      setEventTitle(template.title || template.name || '');
      setEventDescription(template.description || '');
      setEventScope(template.scope || 'global');
      setEffectsJson(JSON.stringify(template.effects || {}, null, 2));
    }
  };

  const handleCreateEvent = async () => {
    setActionLoading('event');
    setError(null);
    try {
      let effects: Record<string, any>;
      try {
        effects = JSON.parse(effectsJson);
      } catch {
        setError('Invalid effects JSON');
        setActionLoading(null);
        return;
      }

      await adminApi.createEvent(gId, {
        title: eventTitle,
        description: eventDescription,
        scope: eventScope,
        effects,
        affected_nation_ids: eventScope === 'targeted' ? affectedNations : undefined,
        expires_turn: expiresTurn ? Number(expiresTurn) : undefined,
      });

      // Refresh events
      const { data } = await adminApi.listEvents(gId);
      setEvents(data);

      // Reset form
      setEventTitle('');
      setEventDescription('');
      setEffectsJson('{}');
      setExpiresTurn('');
      setSelectedTemplate('');
      setAffectedNations([]);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create event');
    } finally {
      setActionLoading(null);
    }
  };

  const toggleNation = (nationId: number) => {
    setAffectedNations((prev) =>
      prev.includes(nationId) ? prev.filter((id) => id !== nationId) : [...prev, nationId]
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0f0f0f]">
        <Header />
        <main className="max-w-7xl mx-auto px-4 py-8">
          <p className="text-gray-500 text-sm">Loading admin panel...</p>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0f0f0f]">
      <Header />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-gray-200 text-xl font-bold">
            GM Admin Panel — {overview?.game.name}
          </h1>
          <span className={`text-xs px-3 py-1 rounded ${
            overview?.game.status === 'active' ? 'bg-green-600/30 text-green-400' :
            overview?.game.status === 'paused' ? 'bg-yellow-600/30 text-yellow-400' :
            'bg-gray-600/30 text-gray-400'
          }`}>
            {overview?.game.status}
          </span>
        </div>

        {error && (
          <div className="bg-red-900/20 border border-red-700/40 rounded-lg p-3">
            <p className="text-red-400 text-sm">{error}</p>
          </div>
        )}

        {/* Turn Control Panel */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
          <h2 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-4">
            Turn Control
          </h2>
          <div className="flex items-center gap-4 mb-4">
            <div className="text-gray-400 text-sm">
              Current Turn: <span className="text-amber-500 font-bold">
                {overview?.current_turn.turn_number ?? 'None'}
              </span>
            </div>
            {overview?.current_turn.deadline && (
              <div className="text-gray-400 text-sm">
                Deadline: <span className="text-gray-200">
                  {new Date(overview.current_turn.deadline).toLocaleString()}
                </span>
              </div>
            )}
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => handleAction('pause')}
              disabled={actionLoading !== null}
              className="bg-yellow-700 hover:bg-yellow-600 disabled:opacity-50 text-white text-sm px-4 py-2 rounded transition-colors cursor-pointer"
            >
              {actionLoading === 'pause' ? 'Pausing...' : 'Pause Game'}
            </button>
            <button
              onClick={() => handleAction('resume')}
              disabled={actionLoading !== null}
              className="bg-green-700 hover:bg-green-600 disabled:opacity-50 text-white text-sm px-4 py-2 rounded transition-colors cursor-pointer"
            >
              {actionLoading === 'resume' ? 'Resuming...' : 'Resume Game'}
            </button>
            <button
              onClick={() => handleAction('force-resolve')}
              disabled={actionLoading !== null}
              className="bg-red-700 hover:bg-red-600 disabled:opacity-50 text-white text-sm px-4 py-2 rounded transition-colors cursor-pointer"
            >
              {actionLoading === 'force-resolve' ? 'Resolving...' : 'Force Resolve'}
            </button>
          </div>
        </div>

        {/* Submissions Tracker */}
        {overview?.current_turn.submissions && overview.current_turn.submissions.length > 0 && (
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
            <h2 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
              Turn Submissions ({overview.current_turn.submissions.length} / {overview.nations.filter((n) => n.is_alive).length})
            </h2>
            <div className="space-y-1">
              {overview.current_turn.submissions.map((sub, i) => (
                <div key={i} className="flex items-center justify-between bg-[#0f0f0f] rounded px-3 py-2">
                  <span className="text-gray-200 text-sm">{sub.nation}</span>
                  <span className="text-gray-500 text-xs">{new Date(sub.submitted_at).toLocaleString()}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Nation Overview Table */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
          <h2 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-4">
            Nations Overview
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-500 text-xs uppercase border-b border-[#2a2a2a]">
                  <th className="text-left py-2 pr-4">Nation</th>
                  <th className="text-left py-2 pr-4">Player</th>
                  <th className="text-left py-2 pr-4">Gov / Traits</th>
                  <th className="text-right py-2 pr-4">Provinces</th>
                  <th className="text-right py-2 pr-4">Population</th>
                  <th className="text-right py-2 pr-4">Stability</th>
                  <th className="text-center py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {overview?.nations.map((nation: AdminNationData) => (
                  <tr key={nation.id} className="border-b border-[#2a2a2a]/50">
                    <td className="py-2 pr-4 text-gray-200 font-medium">{nation.name}</td>
                    <td className="py-2 pr-4 text-gray-400">{nation.player}</td>
                    <td className="py-2 pr-4 text-gray-400 capitalize">
                      {nation.government_type} / {nation.ideology_traits?.strong ?? '-'}
                    </td>
                    <td className="py-2 pr-4 text-gray-200 text-right">{nation.provinces}</td>
                    <td className="py-2 pr-4 text-gray-200 text-right">
                      {nation.resources?.total_population?.toLocaleString() ?? '-'}
                    </td>
                    <td className="py-2 pr-4 text-right">
                      <span className={
                        (nation.resources?.stability ?? 0) >= 70 ? 'text-green-400' :
                        (nation.resources?.stability ?? 0) >= 40 ? 'text-yellow-400' :
                        'text-red-400'
                      }>
                        {nation.resources?.stability ?? '-'}
                      </span>
                    </td>
                    <td className="py-2 text-center">
                      <span className={`text-xs px-2 py-0.5 rounded ${
                        nation.is_alive ? 'bg-green-600/30 text-green-400' : 'bg-red-600/30 text-red-400'
                      }`}>
                        {nation.is_alive ? 'Alive' : 'Fallen'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Event Trigger Form */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
          <h2 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-4">
            Trigger Event
          </h2>

          {templates.length > 0 && (
            <div className="mb-4">
              <label className="text-gray-400 text-xs block mb-1">Template</label>
              <select
                value={selectedTemplate}
                onChange={(e) => handleTemplateSelect(e.target.value)}
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
              >
                <option value="">Custom Event</option>
                {templates.map((t: any, i: number) => (
                  <option key={i} value={t.name || t.title}>{t.name || t.title}</option>
                ))}
              </select>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="text-gray-400 text-xs block mb-1">Title</label>
              <input
                type="text"
                value={eventTitle}
                onChange={(e) => setEventTitle(e.target.value)}
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
                placeholder="Event title"
              />
            </div>
            <div>
              <label className="text-gray-400 text-xs block mb-1">Scope</label>
              <select
                value={eventScope}
                onChange={(e) => setEventScope(e.target.value as 'global' | 'targeted')}
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
              >
                <option value="global">Global</option>
                <option value="targeted">Targeted</option>
              </select>
            </div>
          </div>

          <div className="mb-4">
            <label className="text-gray-400 text-xs block mb-1">Description</label>
            <textarea
              value={eventDescription}
              onChange={(e) => setEventDescription(e.target.value)}
              rows={2}
              className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm resize-none"
              placeholder="Describe the event..."
            />
          </div>

          {eventScope === 'targeted' && overview?.nations && (
            <div className="mb-4">
              <label className="text-gray-400 text-xs block mb-1">Affected Nations</label>
              <div className="flex flex-wrap gap-2">
                {overview.nations.map((nation) => (
                  <button
                    key={nation.id}
                    onClick={() => toggleNation(nation.id)}
                    className={`text-xs px-3 py-1 rounded cursor-pointer transition-colors ${
                      affectedNations.includes(nation.id)
                        ? 'bg-amber-600 text-white'
                        : 'bg-[#0f0f0f] text-gray-400 hover:text-gray-200'
                    }`}
                  >
                    {nation.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="text-gray-400 text-xs block mb-1">Effects (JSON modifiers)</label>
              <textarea
                value={effectsJson}
                onChange={(e) => setEffectsJson(e.target.value)}
                rows={4}
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-xs font-mono resize-none"
                placeholder='{"stability": -10, "food": -5}'
              />
            </div>
            <div>
              <label className="text-gray-400 text-xs block mb-1">Expires on Turn (optional)</label>
              <input
                type="number"
                value={expiresTurn}
                onChange={(e) => setExpiresTurn(e.target.value)}
                className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded px-3 py-2 text-gray-200 text-sm"
                placeholder="Leave empty for permanent"
              />
            </div>
          </div>

          <button
            onClick={handleCreateEvent}
            disabled={!eventTitle || actionLoading === 'event'}
            className="bg-amber-600 hover:bg-amber-700 disabled:opacity-50 text-white text-sm px-6 py-2 rounded transition-colors cursor-pointer"
          >
            {actionLoading === 'event' ? 'Creating...' : 'Trigger Event'}
          </button>
        </div>

        {/* Recent Events */}
        {events.length > 0 && (
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
            <h2 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-3">
              Recent Events
            </h2>
            <div className="space-y-2">
              {events.slice(0, 10).map((event) => (
                <div key={event.id} className="bg-[#0f0f0f] rounded p-3">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-gray-200 text-sm font-medium">{event.title}</span>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs px-2 py-0.5 rounded ${
                        event.scope === 'global' ? 'bg-blue-600/30 text-blue-400' : 'bg-purple-600/30 text-purple-400'
                      }`}>
                        {event.scope}
                      </span>
                      <span className="text-gray-500 text-xs">Turn {event.turn_number}</span>
                    </div>
                  </div>
                  <p className="text-gray-400 text-xs">{event.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
