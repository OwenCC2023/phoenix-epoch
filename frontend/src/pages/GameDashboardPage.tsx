import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../components/Header';
import NationSummaryCard from '../components/game/NationSummaryCard';
import ResourceBar from '../components/game/ResourceBar';
import ProvinceList from '../components/game/ProvinceList';
import ProvinceDetail from '../components/game/ProvinceDetail';
import ProductionBreakdown from '../components/game/ProductionBreakdown';
import TurnTimer from '../components/game/TurnTimer';
import OrderForm from '../components/game/OrderForm';
import OrderList from '../components/game/OrderList';
import SubmitOrdersButton from '../components/game/SubmitOrdersButton';
import TurnResultsPanel from '../components/game/TurnResultsPanel';
import TradeOfferPanel from '../components/game/TradeOfferPanel';
import IncomingTradesPanel from '../components/game/IncomingTradesPanel';
import TurnHistoryPanel from '../components/game/TurnHistoryPanel';
import Notifications from '../components/Notifications';
import { useNationStore } from '../store/nationStore';
import { useTurnStore } from '../store/turnStore';
import { useNotificationStore } from '../store/notificationStore';
import useGameStore from '../store/gameStore';
import { getGame } from '../api/games';
import { listNations } from '../api/nations';
import { listTrades } from '../api/economy';
import useAuthStore from '../store/authStore';
import gameWebSocket from '../api/websocket';
import { Province, Nation, TradeOffer } from '../types';

type Tab = 'overview' | 'provinces' | 'economy' | 'turns' | 'trade' | 'history';

export default function GameDashboardPage() {
  const { gameId } = useParams<{ gameId: string }>();
  const gId = Number(gameId);

  const fetchMe = useAuthStore((s) => s.fetchMe);
  const { setCurrentGame } = useGameStore();
  const {
    nation,
    resources,
    provinces,
    ledger,
    formations,
    loading,
    fetchNation,
    fetchResources,
    fetchProvinces,
    fetchLedger,
    fetchFormations,
    fetchMilitaryGroups,
    setAllocations,
    clearNation,
  } = useNationStore();

  const {
    currentTurn,
    orders,
    turnHistory,
    fetchCurrentTurn,
    fetchOrders,
    fetchTurnHistory,
  } = useTurnStore();

  const addNotification = useNotificationStore((s) => s.addNotification);

  const [activeTab, setActiveTab] = useState<Tab>('overview');
  const [selectedProvince, setSelectedProvince] = useState<Province | null>(null);
  const [initLoading, setInitLoading] = useState(true);
  const [otherNations, setOtherNations] = useState<Nation[]>([]);
  const [outgoingTrades, setOutgoingTrades] = useState<TradeOffer[]>([]);
  const [incomingTrades, setIncomingTrades] = useState<TradeOffer[]>([]);

  useEffect(() => {
    const init = async () => {
      try {
        await fetchMe();
        const currentUser = useAuthStore.getState().user;
        const game = await getGame(gId);
        setCurrentGame(game);

        // Find the current user's nation
        const { data: nations } = await listNations(gId);
        const myNation = nations.find((n) => n.player === currentUser?.id);

        if (myNation) {
          await Promise.all([
            fetchNation(gId, myNation.id),
            fetchResources(gId, myNation.id),
            fetchProvinces(gId, myNation.id),
            fetchLedger(gId, myNation.id),
            fetchFormations(gId, myNation.id),
            fetchMilitaryGroups(gId, myNation.id),
            fetchCurrentTurn(gId),
            fetchOrders(gId),
            fetchTurnHistory(gId),
          ]);

          // Set other nations for trade
          setOtherNations(nations.filter((n) => n.id !== myNation.id));

          // Fetch trades
          try {
            const { data: trades } = await listTrades(gId);
            setOutgoingTrades(trades.filter((t) => t.from_nation === myNation.id));
            setIncomingTrades(trades.filter((t) => t.to_nation === myNation.id));
          } catch { /* no trades yet */ }
        }
      } catch {
        // handled by store errors
      } finally {
        setInitLoading(false);
      }
    };
    init();

    // Connect WebSocket
    gameWebSocket.connect(gId);

    return () => {
      clearNation();
      setCurrentGame(null);
      gameWebSocket.disconnect();
    };
  }, [gId]); // eslint-disable-line react-hooks/exhaustive-deps

  // Wire up WebSocket event handlers
  useEffect(() => {
    const unsubTurnStarted = gameWebSocket.on('turn_started', (data) => {
      addNotification(`Turn ${data.turn_number} has started!`, 'info');
      fetchCurrentTurn(gId);
      fetchOrders(gId);
    });

    const unsubTurnResolved = gameWebSocket.on('turn_resolved', (data) => {
      addNotification(`Turn ${data.turn_number} has been resolved.`, 'success');
      fetchCurrentTurn(gId);
      fetchTurnHistory(gId);
      if (nation) {
        fetchResources(gId, nation.id);
        fetchProvinces(gId, nation.id);
        fetchLedger(gId, nation.id);
      }
    });

    const unsubTradeReceived = gameWebSocket.on('trade_received', () => {
      addNotification('You have received a new trade offer!', 'info');
      if (nation) {
        listTrades(gId).then(({ data }) => {
          setIncomingTrades(data.filter((t) => t.to_nation === nation.id));
        }).catch(() => {});
      }
    });

    const unsubTradeResponse = gameWebSocket.on('trade_response', (data) => {
      addNotification(`Trade ${data.status}: ${data.message || ''}`, data.status === 'accepted' ? 'success' : 'warning');
      if (nation) {
        listTrades(gId).then(({ data: trades }) => {
          setOutgoingTrades(trades.filter((t) => t.from_nation === nation.id));
        }).catch(() => {});
      }
    });

    const unsubEvent = gameWebSocket.on('game_event', (data) => {
      addNotification(data.title || 'A new event has occurred!', 'warning');
    });

    const unsubGamePaused = gameWebSocket.on('game_paused', () => {
      addNotification('The game has been paused by the GM.', 'warning');
    });

    const unsubGameResumed = gameWebSocket.on('game_resumed', () => {
      addNotification('The game has been resumed.', 'info');
    });

    return () => {
      unsubTurnStarted();
      unsubTurnResolved();
      unsubTradeReceived();
      unsubTradeResponse();
      unsubEvent();
      unsubGamePaused();
      unsubGameResumed();
    };
  }, [gId, nation]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSaveAllocations = async (
    allocations: { sector: string; percentage: number }[]
  ) => {
    if (!selectedProvince) return;
    await setAllocations(gId, selectedProvince.id, allocations);
    if (nation) {
      await fetchProvinces(gId, nation.id);
    }
  };

  const tabs: { key: Tab; label: string }[] = [
    { key: 'overview', label: 'Overview' },
    { key: 'provinces', label: 'Provinces' },
    { key: 'economy', label: 'Economy' },
    { key: 'turns', label: 'Turn' },
    { key: 'trade', label: 'Trade' },
    { key: 'history', label: 'History' },
  ];

  if (initLoading || loading) {
    return (
      <div className="min-h-screen bg-[#0f0f0f]">
        <Header />
        <main className="max-w-7xl mx-auto px-4 py-8">
          <p className="text-gray-500 text-sm">Loading dashboard...</p>
        </main>
      </div>
    );
  }

  if (!nation) {
    return (
      <div className="min-h-screen bg-[#0f0f0f]">
        <Header />
        <main className="max-w-7xl mx-auto px-4 py-8">
          <p className="text-gray-500 text-sm">
            No nation found. You may need to create one first.
          </p>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0f0f0f]">
      <Header />
      <Notifications />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left Sidebar */}
          <div className="lg:w-72 flex-shrink-0 space-y-4">
            <NationSummaryCard nation={nation} />
            {resources && <ResourceBar resources={resources} />}
            <TurnTimer turn={currentTurn} />
          </div>

          {/* Main Content */}
          <div className="flex-1 min-w-0">
            {/* Tab Navigation */}
            <div className="flex gap-1 mb-4 border-b border-[#2a2a2a]">
              {tabs.map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => {
                    setActiveTab(tab.key);
                    setSelectedProvince(null);
                  }}
                  className={`px-4 py-2.5 text-sm font-medium transition-colors cursor-pointer ${
                    activeTab === tab.key
                      ? 'text-amber-500 border-b-2 border-amber-500 -mb-px'
                      : 'text-gray-500 hover:text-gray-300'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div>
              {activeTab === 'overview' && (
                <div className="space-y-4">
                  <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
                    <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-4">
                      National Overview
                    </h3>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                      <div className="bg-[#0f0f0f] rounded p-3 text-center">
                        <div className="text-gray-500 text-xs mb-1">Provinces</div>
                        <div className="text-gray-200 text-xl font-bold">{provinces.length}</div>
                      </div>
                      <div className="bg-[#0f0f0f] rounded p-3 text-center">
                        <div className="text-gray-500 text-xs mb-1">Population</div>
                        <div className="text-gray-200 text-xl font-bold">
                          {resources?.total_population?.toLocaleString() ?? 0}
                        </div>
                      </div>
                      <div className="bg-[#0f0f0f] rounded p-3 text-center">
                        <div className="text-gray-500 text-xs mb-1">Stability</div>
                        <div
                          className={`text-xl font-bold ${
                            (resources?.stability ?? 0) >= 70
                              ? 'text-green-400'
                              : (resources?.stability ?? 0) >= 40
                              ? 'text-yellow-400'
                              : 'text-red-400'
                          }`}
                        >
                          {resources?.stability ?? 0}
                        </div>
                      </div>
                      <div className="bg-[#0f0f0f] rounded p-3 text-center">
                        <div className="text-gray-500 text-xs mb-1">Status</div>
                        <div className={`text-xl font-bold ${nation.is_alive ? 'text-green-400' : 'text-red-400'}`}>
                          {nation.is_alive ? 'Active' : 'Fallen'}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Resource totals */}
                  {resources && (
                    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
                      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-4">
                        Resource Totals
                      </h3>
                      <div className="grid grid-cols-3 sm:grid-cols-6 gap-3">
                        {(['food', 'materials', 'energy', 'wealth', 'manpower', 'research'] as const).map(
                          (key) => (
                            <div key={key} className="bg-[#0f0f0f] rounded p-3 text-center">
                              <div className="text-gray-500 text-xs capitalize mb-1">{key}</div>
                              <div className="text-gray-200 text-lg font-bold">
                                {Math.round(resources[key])}
                              </div>
                            </div>
                          )
                        )}
                      </div>
                    </div>
                  )}

                  {/* Latest turn results */}
                  <TurnResultsPanel
                    turn={turnHistory.find((t) => t.status === 'completed') ?? null}
                    ledger={ledger}
                  />
                </div>
              )}

              {activeTab === 'provinces' && (
                <div>
                  {selectedProvince ? (
                    <ProvinceDetail
                      province={selectedProvince}
                      onSaveAllocations={handleSaveAllocations}
                      onBack={() => setSelectedProvince(null)}
                    />
                  ) : (
                    <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-5">
                      <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider mb-4">
                        Provinces ({provinces.length})
                      </h3>
                      <ProvinceList
                        provinces={provinces}
                        onSelect={setSelectedProvince}
                      />
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'economy' && (
                <ProductionBreakdown ledger={ledger} />
              )}

              {activeTab === 'turns' && (
                <div className="space-y-4">
                  <OrderForm
                    gameId={gId}
                    provinces={provinces}
                    otherNations={otherNations}
                    formations={formations}
                  />
                  <OrderList gameId={gId} orders={orders} />
                  <SubmitOrdersButton gameId={gId} />
                </div>
              )}

              {activeTab === 'trade' && (
                <div className="space-y-4">
                  <TradeOfferPanel trades={outgoingTrades} />
                  <IncomingTradesPanel gameId={gId} trades={incomingTrades} />
                </div>
              )}

              {activeTab === 'history' && (
                <TurnHistoryPanel turns={turnHistory} />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
