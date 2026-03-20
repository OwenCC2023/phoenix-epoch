export interface User {
  id: number;
  username: string;
  email: string;
  display_name: string;
  bio: string;
  games_played: number;
}

export interface Game {
  id: number;
  name: string;
  description: string;
  status: 'lobby' | 'active' | 'paused' | 'finished';
  creator: number;
  creator_name: string;
  max_players: number;
  min_players: number;
  turn_duration_hours: number;
  current_turn_number: number;
  starting_provinces: number;
  member_count: number;
  created_at: string;
}

export interface GameMembership {
  id: number;
  user: number;
  username: string;
  display_name: string;
  role: 'player' | 'gm' | 'observer';
  joined_at: string;
}

export interface IdeologyTraits {
  strong: string;
  weak: string[];
}

export interface Nation {
  id: number;
  game: number;
  player: number;
  name: string;
  description: string;
  government_type: string;
  ideology_traits: IdeologyTraits;
  motto: string;
  is_alive: boolean;
  created_at: string;
  policies?: NationPolicy[];
}

export interface NationPolicy {
  id: number;
  category: string;
  level: number;
  changed_turn: number | null;
}

export interface NationModifier {
  id: number;
  name: string;
  category: string;
  target: string;
  modifier_type: 'flat' | 'percentage';
  value: number;
  source: string;
  expires_turn: number | null;
}

export interface Province {
  id: number;
  game: number;
  nation: number | null;
  name: string;
  terrain_type: string;
  population: number;
  local_stability: number;
  designation: 'rural' | 'urban' | 'post_urban' | 'capital';
  is_capital: boolean;
  is_coastal: boolean;
  is_river: boolean;
  center_x: number | null;
  center_y: number | null;
  sea_border_distance: number | null;
  river_border_distance: number | null;
  air_zone: number | null;
  adjacent_province_ids: number[];
  adjacent_sea_zone_ids: number[];
  adjacent_river_zone_ids: number[];
  resources: ProvinceResources | null;
  buildings: Building[];
}

export interface AirZone {
  id: number;
  game: number;
  name: string;
  adjacent_air_zone_ids: number[];
}

export interface SeaZone {
  id: number;
  game: number;
  name: string;
  adjacent_sea_zone_ids: number[];
  adjacent_air_zone_ids: number[];
  river_zone_ids: number[];
}

export interface RiverZone {
  id: number;
  game: number;
  name: string;
  sea_zone: number | null;
  adjacent_river_zone_ids: number[];
  adjacent_air_zone_ids: number[];
}

export interface ProvinceResources {
  food: number;
  materials: number;
  energy: number;
  wealth: number;
  manpower: number;
  research: number;
}

export interface Building {
  id: number;
  province: number;
  building_type: string;
  level: number;
  is_active: boolean;
  under_construction: boolean;
  construction_turns_remaining: number;
}

export interface NationGoodStock {
  id: number;
  nation: number;
  consumer_goods: number;
  arms: number;
  fuel: number;
  machinery: number;
  chemicals: number;
  medicine: number;
  components: number;
  heavy_equipment: number;
  military_goods: number;
}

export type MilitaryDomain = 'army' | 'navy' | 'air';
export type FormationType = 'reserve' | 'active';

export interface MilitaryUnit {
  id: number;
  formation: number;
  unit_type: string;
  quantity: number;
  quantity_in_training: number;
  construction_turns_remaining: number;
  is_active: boolean;
  quantity_in_transit: number;
  transit_turns_remaining: number;
  training_province: number | null;
}

export interface Formation {
  id: number;
  nation: number;
  group: number | null;
  province: number | null;
  name: string;
  domain: MilitaryDomain;
  formation_type: FormationType;
  effective_strength: number;
  units: MilitaryUnit[];
}

export interface MilitaryGroup {
  id: number;
  nation: number;
  name: string;
  formations: Formation[];
}

export interface NationConstruction {
  buildings: ConstructionBuilding[];
  military_units: MilitaryUnitInTraining[];
}

export interface MilitaryUnitInTraining {
  id: number;
  unit_type: string;
  quantity_in_training: number;
  construction_turns_remaining: number;
  formation: number;
  training_province: number | null;
}

export interface ConstructionBuilding {
  id: number;
  province: number;
  province_name: string;
  building_type: string;
  level: number;
  construction_turns_remaining: number;
}


export interface SectorAllocation {
  sector: string;
  percentage: number;
}

export interface NationResourcePool {
  food: number;
  materials: number;
  energy: number;
  wealth: number;
  manpower: number;
  research: number;
  stability: number;
  total_population: number;
}

export interface ResourceLedger {
  id: number;
  turn_number: number;
  province_production_total: Record<string, number>;
  integration_losses: Record<string, number>;
  national_modifier_effects: Record<string, number>;
  trade_net: Record<string, number>;
  consumption: Record<string, number>;
  final_pools: Record<string, number>;
}

export interface TradeOffer {
  id: number;
  from_nation: number;
  from_nation_name: string;
  to_nation: number;
  to_nation_name: string;
  turn_number: number;
  offering: Record<string, number>;
  requesting: Record<string, number>;
  status: 'pending' | 'accepted' | 'rejected' | 'expired' | 'executed';
}

export interface Turn {
  id: number;
  turn_number: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  deadline: string;
  resolution_log: { events?: string[] };
  started_at: string;
  resolved_at: string | null;
}

export interface Order {
  id: number;
  turn: number;
  nation: number;
  order_type: 'set_allocation' | 'trade_offer' | 'trade_response' | 'policy_change' | 'build_building' | 'train_unit' | 'create_formation' | 'assign_to_formation' | 'rename_formation' | 'create_group' | 'rename_group' | 'assign_formation_to_group';
  status: 'draft' | 'submitted' | 'validated' | 'executed' | 'failed';
  payload: Record<string, any>;
  validation_errors: string[];
  created_at: string;
}

export interface GameEvent {
  id: number;
  title: string;
  description: string;
  scope: 'global' | 'targeted';
  effects: Record<string, any>;
  turn_number: number;
  expires_turn: number | null;
  created_at: string;
}

export interface AdminOverview {
  game: Game;
  nations: AdminNationData[];
  current_turn: {
    turn_number: number | null;
    deadline: string | null;
    submissions: { nation: string; submitted_at: string }[];
  };
}

export interface AdminNationData {
  id: number;
  name: string;
  player: string;
  government_type: string;
  ideology_traits: IdeologyTraits;
  is_alive: boolean;
  provinces: number;
  resources: NationResourcePool | null;
}
