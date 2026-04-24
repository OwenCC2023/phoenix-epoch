"""Building types and constants for the buildings system.

Buildings have unlimited levels. Each upgrade scales costs/workers/outputs from the base
(L1) values using power-law exponents. Effects scale logarithmically, asymptotically
approaching 90% additional gain by L10 relative to L1.

get_level_data(building_type, level) is the single entry point for all level-specific data.

Scaling formulas:
  workers  = round(base_workers  × N ^ worker_scale)     default worker_scale  = 0.85
  inputs   = round(base_inputs   × N ^ input_scale)      default input_scale   = 0.90
  outputs  = round(base_outputs  × N ^ output_scale, 2)  default output_scale  = 1.00
  cost     = round(base_cost     × N ^ cost_scale)       default cost_scale    = 1.50
  turns    = ceil (base_turns    × N ^ turns_scale)      default turns_scale   = 0.75
  effects  = base_effect × (1 + 0.9 × log10(N))          (L1 → base, L10 → 1.9×base)

Manufactured goods (NationGoodStock):
  consumer_goods  - produced by factories/mills, consumed by population each turn
  arms            - produced by arms factories, used by military
  fuel            - produced by refineries, used by vehicles/military
  machinery       - produced by workshops, used by factories
  chemicals       - produced by chemical plants, used in pharma/fertilizers/plastics
  medicine        - produced by pharmaceutical labs, consumed by hospitals/clinics
  components      - produced by precision workshops/cement plants, used in electronics
  heavy_equipment - produced by heavy forges, used in extraction/construction
  military_goods  - produced by weapons factories, consumed by military bases

Provincial effects (additive per province, summed from all buildings in that province):
  farming_bonus              - multiplier added to province food subsistence output
  research_bonus             - multiplier added to province research output
  integration_bonus          - additional fraction of province surplus reaching national pool
  growth_bonus               - flat monthly addition to population growth rate (+/month)
  stability_recovery_bonus   - addition to monthly stability recovery rate (+/month)
  construction_time_reduction- fraction reduction in construction turns for this province
  literacy_bonus             - multiplier for province literacy rate (stub — not yet wired)

National effects (summed across all provinces, applied nationally):
  construction_cost_reduction - fraction reduction in all construction costs
  upkeep_reduction            - fraction reduction in government upkeep
  bureaucratic_capacity       - total bureaucratic capacity (use-it-or-lose-it, stub)
  land_trade_capacity         - total land trade capacity (financial buildings + road transport)
  naval_trade_capacity        - total naval trade capacity (port, dock)
  air_trade_capacity          - total air trade capacity (airport, air_cargo_terminal)
  march_speed_bonus           - national land travel speed modifier
  sea_transit_speed           - national sea-to-sea travel speed modifier
  river_transit_speed         - national river-to-river travel speed modifier
  air_transit_speed           - national air-to-air travel speed modifier
"""

import math

# All manufactured good keys (stored in NationGoodStock)
GOOD_KEYS = [
    "consumer_goods", "arms", "fuel", "machinery",
    "chemicals", "medicine", "components", "heavy_equipment",
    "military_goods",
]

# Effect keys that apply at the province level
PROVINCE_EFFECT_KEYS = [
    "farming_bonus",
    "research_bonus",
    "integration_bonus",
    "growth_bonus",
    "stability_recovery_bonus",
    "construction_time_reduction",
    "literacy_bonus",
    "security",                # flat security points contributed to province.local_security
    "march_speed_bonus",       # province-scope land travel speed (road_network, railway_station)
    "sea_transit_speed",       # province-scope sea embarkation speed (dock, port)
    "river_transit_speed",     # province-scope river crossing speed (dock, bridge)
    "air_transit_speed",       # province-scope air transition speed (airport)
    "provincial_espionage_defense",  # provincial espionage defense from local_office
]

# Effect keys that apply at the national level (sum across all provinces)
NATIONAL_EFFECT_KEYS = [
    "construction_cost_reduction",
    "upkeep_reduction",
    "bureaucratic_capacity",
    "land_trade_capacity",          # from financial buildings + ground transport
    "naval_trade_capacity",         # from port, dock
    "air_trade_capacity",           # from airport, air_cargo_terminal
    "march_speed_bonus",            # national land travel speed (logistics_hub, railroad, train_depot)
    "sea_transit_speed",            # national sea-to-sea travel speed
    "river_transit_speed",          # national river-to-river travel speed
    "air_transit_speed",            # national air-to-air travel speed
    # Military college effects (stubs — wired when military simulation is built)
    "army_training_speed_bonus",    # reduces army unit training turns
    "navy_training_speed_bonus",    # reduces navy unit training turns
    "air_training_speed_bonus",     # reduces air unit training turns
    "army_combat_bonus",            # army combat effectiveness multiplier
    "navy_combat_bonus",            # navy combat effectiveness multiplier
    "air_combat_bonus",             # air combat effectiveness multiplier
    "army_upkeep_reduction",        # fraction reduction in army unit upkeep
    "navy_upkeep_reduction",        # fraction reduction in navy unit upkeep
    "air_upkeep_reduction",         # fraction reduction in air unit upkeep
    # Espionage effects
    "espionage_attack",             # national espionage attack from buildings
    "espionage_defense",            # national espionage defense from buildings
]

# All goods that can be traded between nations.
# Pool resources (NationResourcePool) + manufactured goods (NationGoodStock).
VALID_GOODS = frozenset([
    # Pool resources
    "food", "materials", "energy", "kapital", "manpower", "research",
    # Manufactured goods
    "consumer_goods", "arms", "fuel", "machinery", "chemicals",
    "medicine", "components", "heavy_equipment", "military_goods",
])

# Sector classification for all building types.
# Used by the rationing system to determine input-goods allocation priority.
#   civilian   - production, extraction, healthcare, entertainment, religious, green energy
#   military   - arms/weapons production, military bases, military education
#   government - financial, transport, communications, all government_* categories
BUILDING_SECTOR = {
    # ----- Heavy manufacturing -----
    "workshop":              "civilian",
    "arms_factory":          "military",
    "heavy_forge":           "civilian",
    "industrial_complex":    "civilian",
    "shipyard":              "civilian",
    "weapons_factory":       "military",
    # ----- Light manufacturing -----
    "factory":               "civilian",
    "textile_mill":          "civilian",
    "electronics_factory":   "civilian",
    "precision_workshop":    "civilian",
    # ----- Refining -----
    "refinery":              "civilian",
    "advanced_refinery":     "civilian",
    "fuel_depot":            "civilian",
    "biofuel_plant":         "civilian",
    # ----- Chemical -----
    "chemical_plant":        "civilian",
    "fertilizer_plant":      "civilian",
    "plastics_factory":      "civilian",
    # ----- Pharmaceutical -----
    "pharmaceutical_lab":    "civilian",
    "medical_supply_depot":  "civilian",
    "research_institute":    "civilian",
    # ----- Farming -----
    "irrigation_network":    "civilian",
    "grain_silo":            "civilian",
    "agricultural_station":  "civilian",
    # ----- Extraction -----
    "mine":                  "civilian",
    "oil_well":              "civilian",
    "logging_camp":          "civilian",
    # ----- Construction -----
    "construction_yard":     "civilian",
    "cement_plant":          "civilian",
    "infrastructure_bureau": "civilian",
    # ----- Financial -----
    "trading_post":          "government",
    "bank":                  "government",
    "stock_exchange":        "government",
    # ----- Transport -----
    "road_network":          "government",
    "railway_station":       "government",
    "logistics_hub":         "government",
    "dock":                  "government",
    "port":                  "government",
    "bridge":                "government",
    "railroad":              "government",
    "train_depot":           "government",
    "train_station":         "government",
    "train_cargo_terminal":  "government",
    "airport":               "government",
    "air_cargo_terminal":    "government",
    # ----- Communications -----
    "radio_tower":           "government",
    "telegraph_network":     "government",
    "broadcasting_station":  "government",
    # ----- Entertainment -----
    "tavern":                "civilian",
    "theatre":               "civilian",
    "resort":                "civilian",
    # ----- Healthcare -----
    "clinic":                "civilian",
    "hospital":              "civilian",
    "sanitation_works":      "civilian",
    # ----- Religious -----
    "church":                "civilian",
    "madrasa":               "civilian",
    "holy_site":             "civilian",
    # ----- Green energy -----
    "wind_farm":             "civilian",
    "solar_array":           "civilian",
    "hydroelectric_dam":     "civilian",
    # ----- Government regulatory/oversight/management/security -----
    "regulatory_office":     "government",
    "standards_bureau":      "government",
    "inspector_general":     "government",
    "audit_commission":      "government",
    "civil_service_academy": "government",
    "administrative_center": "government",
    "police_headquarters":   "government",
    "police_station":        "government",
    "sheriffs_office":       "government",
    "fire_house":            "government",
    "disaster_management":   "government",
    # ----- Government education -----
    "public_school":         "government",
    "university":            "government",
    # ----- Government organization/welfare -----
    "labor_bureau":          "government",
    "workers_council":       "government",
    "social_services_office": "government",
    "public_housing":        "government",
    # ----- Military bases and education -----
    "army_base":             "military",
    "naval_base":            "military",
    "air_base":              "military",
    "military_academy":      "military",
    "naval_war_college":     "military",
    "air_force_academy":     "military",
    # ----- Espionage -----
    "foreign_intel_hq":      "government",
    "branch_office":         "government",
    "domestic_intel_hq":     "government",
    "local_office":          "government",
}


def get_level_data(building_type: str, level: int) -> dict:
    """
    Compute the level-specific data dict for any building at any level >= 1.

    Uses power-law scaling for workers/inputs/outputs/costs, and logarithmic
    scaling for effects (asymptotically approaching 90% additional gain by L10).

    Parameters
    ----------
    building_type : str
        Key in BUILDING_TYPES.
    level : int
        Target level (1 = base values, 2+ = scaled).

    Returns
    -------
    dict with keys: workers, input_goods, output_goods, construction_cost,
                    construction_turns, effects
    """
    bt = BUILDING_TYPES[building_type]
    N = max(1, level)

    ws = bt.get("worker_scale", 0.85)
    ins = bt.get("input_scale", 0.90)
    outs = bt.get("output_scale", 1.00)
    cs = bt.get("cost_scale", 1.50)
    ts = bt.get("turns_scale", 0.75)

    workers = max(1, round(bt["base_workers"] * (N ** ws)))
    inputs = {k: max(1, round(v * (N ** ins))) for k, v in bt["base_inputs"].items()}
    outputs = {k: round(v * (N ** outs), 2) for k, v in bt["base_outputs"].items()}
    cost = {k: max(1, round(v * (N ** cs))) for k, v in bt["base_construction_cost"].items()}
    turns = max(1, math.ceil(bt["base_construction_turns"] * (N ** ts)))

    if N == 1:
        effects = dict(bt.get("base_effects", {}))
    else:
        effects = {
            k: round(v * (1.0 + 0.9 * math.log10(N)), 6)
            for k, v in bt.get("base_effects", {}).items()
        }

    return {
        "workers": workers,
        "input_goods": inputs,
        "output_goods": outputs,
        "construction_cost": cost,
        "construction_turns": turns,
        "effects": effects,
    }


BUILDING_TYPES = {
    # ============================================================
    # HEAVY MANUFACTURING
    # ============================================================
    "workshop": {
        "label": "Workshop",
        "category": "heavy_manufacturing",
        "description": "Converts raw materials into machinery.",
        "base_workers": 200,
        "base_inputs": {"materials": 200},
        "base_outputs": {"machinery": 100},
        "base_construction_cost": {"materials": 1000, "kapital": 500},
        "base_construction_turns": 6,
        "base_effects": {},
    },
    "arms_factory": {
        "label": "Arms Factory",
        "category": "heavy_manufacturing",
        "description": "Produces arms using materials, energy, and fuel.",
        "base_workers": 400,
        "base_inputs": {"materials": 400, "energy": 200, "fuel": 100},
        "base_outputs": {"arms": 150},
        "base_construction_cost": {"materials": 2000, "kapital": 1000, "manpower": 500},
        "base_construction_turns": 12,
        "base_effects": {},
    },
    "heavy_forge": {
        "label": "Heavy Forge",
        "category": "heavy_manufacturing",
        "description": "Produces heavy industrial equipment from raw materials. Unlocks advanced extraction and construction.",
        "base_workers": 350,
        "base_inputs": {"materials": 400, "energy": 300},
        "base_outputs": {"heavy_equipment": 150},
        "base_construction_cost": {"materials": 1800, "kapital": 900},
        "base_construction_turns": 12,
        "base_effects": {},
    },
    "industrial_complex": {
        "label": "Industrial Complex",
        "category": "heavy_manufacturing",
        "description": "Large production complex outputting both consumer goods and machinery.",
        "base_workers": 600,
        "base_inputs": {"materials": 600, "energy": 400, "heavy_equipment": 100},
        "base_outputs": {"consumer_goods": 300, "machinery": 150},
        "base_construction_cost": {"materials": 3000, "kapital": 1500},
        "base_construction_turns": 18,
        "base_effects": {},
    },
    "shipyard": {
        "label": "Shipyard",
        "category": "heavy_manufacturing",
        "description": "Produces arms via large-vehicle construction. Engineering expertise reduces province construction times.",
        "base_workers": 500,
        "base_inputs": {"materials": 500, "fuel": 100, "heavy_equipment": 150},
        "base_outputs": {"arms": 200},
        "base_construction_cost": {"materials": 2500, "kapital": 1500},
        "base_construction_turns": 15,
        "base_effects": {"construction_time_reduction": 0.08},
    },
    "weapons_factory": {
        "label": "Weapons Factory",
        "category": "heavy_manufacturing",
        "description": "Assembles military equipment packages from arms, machinery, and components.",
        "base_workers": 500,
        "base_inputs": {"arms": 150, "machinery": 100, "components": 80},
        "base_outputs": {"military_goods": 150},
        "base_construction_cost": {"materials": 2500, "kapital": 1500, "manpower": 500},
        "base_construction_turns": 15,
        "base_effects": {},
    },

    # ============================================================
    # LIGHT MANUFACTURING
    # ============================================================
    "factory": {
        "label": "Factory",
        "category": "light_manufacturing",
        "description": "Produces consumer goods using materials, energy, and machinery.",
        "base_workers": 400,
        "base_inputs": {"materials": 300, "energy": 200, "machinery": 100},
        "base_outputs": {"consumer_goods": 200},
        "base_construction_cost": {"materials": 1500, "kapital": 800},
        "base_construction_turns": 12,
        "base_effects": {},
    },
    "textile_mill": {
        "label": "Textile Mill",
        "category": "light_manufacturing",
        "description": "Produces basic consumer goods from materials. An accessible early-game alternative to the factory.",
        "base_workers": 300,
        "base_inputs": {"materials": 200, "manpower": 100},
        "base_outputs": {"consumer_goods": 120},
        "base_construction_cost": {"materials": 800, "kapital": 400},
        "base_construction_turns": 6,
        "base_effects": {},
    },
    "electronics_factory": {
        "label": "Electronics Factory",
        "category": "light_manufacturing",
        "description": "Produces high-quality consumer goods from components and stimulates local research.",
        "base_workers": 350,
        "base_inputs": {"materials": 250, "energy": 200, "components": 100},
        "base_outputs": {"consumer_goods": 250},
        "base_construction_cost": {"materials": 1800, "kapital": 1200},
        "base_construction_turns": 12,
        "base_effects": {"research_bonus": 0.10},
    },
    "precision_workshop": {
        "label": "Precision Workshop",
        "category": "light_manufacturing",
        "description": "Converts materials and machinery into precision components for advanced manufacturing.",
        "base_workers": 200,
        "base_inputs": {"materials": 200, "machinery": 100},
        "base_outputs": {"components": 150},
        "base_construction_cost": {"materials": 1200, "kapital": 700},
        "base_construction_turns": 9,
        "base_effects": {},
    },

    # ============================================================
    # REFINING
    # ============================================================
    "refinery": {
        "label": "Refinery",
        "category": "refining",
        "description": "Converts materials and energy into fuel.",
        "base_workers": 300,
        "base_inputs": {"materials": 250, "energy": 300},
        "base_outputs": {"fuel": 150},
        "base_construction_cost": {"materials": 1200, "kapital": 700},
        "base_construction_turns": 9,
        "base_effects": {},
    },
    "advanced_refinery": {
        "label": "Advanced Refinery",
        "category": "refining",
        "description": "Higher-throughput refinery that also produces chemicals as a byproduct.",
        "base_workers": 350,
        "base_inputs": {"materials": 300, "energy": 350},
        "base_outputs": {"fuel": 200, "chemicals": 80},
        "base_construction_cost": {"materials": 1600, "kapital": 900},
        "base_construction_turns": 10,
        "base_effects": {},
    },
    "fuel_depot": {
        "label": "Fuel Depot",
        "category": "refining",
        "description": "Storage and distribution hub that reduces national government upkeep.",
        "base_workers": 100,
        "base_inputs": {"materials": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 600, "kapital": 300},
        "base_construction_turns": 4,
        "base_effects": {"upkeep_reduction": 0.02},
    },
    "biofuel_plant": {
        "label": "Biofuel Plant",
        "category": "refining",
        "description": "Converts agricultural surplus into fuel and chemicals. Pairs well with farming provinces.",
        "base_workers": 250,
        "base_inputs": {"food": 200, "energy": 100},
        "base_outputs": {"fuel": 120, "chemicals": 60},
        "base_construction_cost": {"materials": 1000, "kapital": 600},
        "base_construction_turns": 8,
        "base_effects": {},
    },

    # ============================================================
    # CHEMICAL
    # ============================================================
    "chemical_plant": {
        "label": "Chemical Plant",
        "category": "chemical",
        "description": "Primary producer of industrial chemicals used in pharmaceuticals, agriculture, and manufacturing.",
        "base_workers": 300,
        "base_inputs": {"materials": 300, "energy": 250},
        "base_outputs": {"chemicals": 200},
        "base_construction_cost": {"materials": 1400, "kapital": 800},
        "base_construction_turns": 10,
        "base_effects": {},
    },
    "fertilizer_plant": {
        "label": "Fertilizer Plant",
        "category": "chemical",
        "description": "Converts chemicals into agricultural fertilizers, significantly boosting province food output.",
        "base_workers": 200,
        "base_inputs": {"chemicals": 100, "energy": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1000, "kapital": 600},
        "base_construction_turns": 8,
        "base_effects": {"farming_bonus": 0.15},
    },
    "plastics_factory": {
        "label": "Plastics Factory",
        "category": "chemical",
        "description": "Converts chemicals into consumer goods and components. A versatile chemicals consumer.",
        "base_workers": 300,
        "base_inputs": {"chemicals": 150, "energy": 150},
        "base_outputs": {"consumer_goods": 120, "components": 80},
        "base_construction_cost": {"materials": 1200, "kapital": 700},
        "base_construction_turns": 9,
        "base_effects": {},
    },

    # ============================================================
    # PHARMACEUTICAL
    # ============================================================
    "pharmaceutical_lab": {
        "label": "Pharmaceutical Lab",
        "category": "pharmaceutical",
        "description": "Produces medicine from chemicals and research. Improves population growth.",
        "base_workers": 150,
        "base_inputs": {"chemicals": 100, "research": 50},
        "base_outputs": {"medicine": 80},
        "base_construction_cost": {"materials": 1000, "kapital": 800},
        "base_construction_turns": 9,
        "base_effects": {"growth_bonus": 0.001},
    },
    "medical_supply_depot": {
        "label": "Medical Supply Depot",
        "category": "pharmaceutical",
        "description": "Distributes medicine to the province, accelerating stability recovery.",
        "base_workers": 100,
        "base_inputs": {"medicine": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 600, "kapital": 500},
        "base_construction_turns": 5,
        "base_effects": {"stability_recovery_bonus": 0.10},
    },
    "research_institute": {
        "label": "Research Institute",
        "category": "pharmaceutical",
        "description": "Advanced research facility that boosts province research output and improves population health.",
        "base_workers": 200,
        "base_inputs": {"kapital": 200, "energy": 100},
        "base_outputs": {"research": 100},
        "base_construction_cost": {"materials": 1200, "kapital": 1000},
        "base_construction_turns": 10,
        "base_effects": {"research_bonus": 0.15, "growth_bonus": 0.001},
    },

    # ============================================================
    # FARMING
    # ============================================================
    "irrigation_network": {
        "label": "Irrigation Network",
        "category": "farming",
        "description": "Water management infrastructure that significantly boosts province food output.",
        "base_workers": 150,
        "base_inputs": {"energy": 100, "materials": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 900, "kapital": 400},
        "base_construction_turns": 8,
        "base_effects": {"farming_bonus": 0.15},
    },
    "grain_silo": {
        "label": "Grain Silo",
        "category": "farming",
        "description": "Food storage infrastructure that boosts province stability by guaranteeing food security.",
        "base_workers": 80,
        "base_inputs": {"materials": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 500, "kapital": 250},
        "base_construction_turns": 4,
        "base_effects": {"stability_recovery_bonus": 0.10},
    },
    "agricultural_station": {
        "label": "Agricultural Station",
        "category": "farming",
        "description": "Research-driven farming improvements that boost food output and population health.",
        "base_workers": 120,
        "base_inputs": {"research": 60, "energy": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 800, "kapital": 600},
        "base_construction_turns": 8,
        "base_effects": {"farming_bonus": 0.10, "growth_bonus": 0.001},
    },

    # ============================================================
    # EXTRACTION
    # ============================================================
    "mine": {
        "label": "Mine",
        "category": "extraction",
        "description": "Deep extraction operation producing large quantities of raw materials.",
        "base_workers": 400,
        "base_inputs": {"energy": 200, "heavy_equipment": 80},
        "base_outputs": {"materials": 400},
        "base_construction_cost": {"materials": 1500, "kapital": 800},
        "base_construction_turns": 10,
        "base_effects": {},
    },
    "oil_well": {
        "label": "Oil Well",
        "category": "extraction",
        "description": "Extracts petroleum, producing fuel and raw materials as a byproduct.",
        "base_workers": 300,
        "base_inputs": {"energy": 150, "heavy_equipment": 60},
        "base_outputs": {"fuel": 250, "materials": 80},
        "base_construction_cost": {"materials": 1300, "kapital": 700},
        "base_construction_turns": 9,
        "base_effects": {},
    },
    "logging_camp": {
        "label": "Logging Camp",
        "category": "extraction",
        "description": "Low-tech forest extraction producing materials and food. Accessible in the early rebuilding era.",
        "base_workers": 200,
        "base_inputs": {"manpower": 100},
        "base_outputs": {"materials": 180, "food": 60},
        "base_construction_cost": {"materials": 500, "kapital": 250},
        "base_construction_turns": 4,
        "base_effects": {},
    },

    # ============================================================
    # CONSTRUCTION
    # ============================================================
    "construction_yard": {
        "label": "Construction Yard",
        "category": "construction",
        "description": "Organises local construction capacity, reducing build times for province buildings.",
        "base_workers": 200,
        "base_inputs": {"materials": 150, "heavy_equipment": 50},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1000, "kapital": 500},
        "base_construction_turns": 8,
        "base_effects": {"construction_time_reduction": 0.10},
    },
    "cement_plant": {
        "label": "Cement Plant",
        "category": "construction",
        "description": "Produces construction-grade components from raw materials and energy.",
        "base_workers": 250,
        "base_inputs": {"materials": 300, "energy": 200},
        "base_outputs": {"components": 200},
        "base_construction_cost": {"materials": 1100, "kapital": 600},
        "base_construction_turns": 8,
        "base_effects": {},
    },
    "infrastructure_bureau": {
        "label": "Infrastructure Bureau",
        "category": "construction",
        "description": "Administrative hub improving province integration and reducing construction costs nationwide.",
        "base_workers": 150,
        "base_inputs": {"kapital": 150, "research": 50},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1000, "kapital": 800},
        "base_construction_turns": 9,
        "base_effects": {"integration_bonus": 0.05, "construction_cost_reduction": 0.04},
    },

    # ============================================================
    # FINANCIAL
    # ============================================================
    "trading_post": {
        "label": "Trading Post",
        "category": "financial",
        "description": "Improves local trade networks, increasing how much of the province surplus reaches the national pool.",
        "base_workers": 100,
        "base_inputs": {"kapital": 100},
        "base_outputs": {},
        "base_construction_cost": {"materials": 600, "kapital": 400},
        "base_construction_turns": 4,
        "base_effects": {"integration_bonus": 0.05, "land_trade_capacity": 50, "literacy_bonus": 0.02},
    },
    "bank": {
        "label": "Bank",
        "category": "financial",
        "description": "Reduces government upkeep nationally through efficient kapital management.",
        "base_workers": 150,
        "base_inputs": {"kapital": 200},
        "base_outputs": {},
        "base_construction_cost": {"materials": 800, "kapital": 1000},
        "base_construction_turns": 6,
        "base_effects": {"upkeep_reduction": 0.03, "land_trade_capacity": 80},
    },
    "stock_exchange": {
        "label": "Stock Exchange",
        "category": "financial",
        "description": "Centralised capital market that reduces construction costs nationwide through efficient resource allocation.",
        "base_workers": 200,
        "base_inputs": {"kapital": 300, "research": 50},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1500, "kapital": 2000},
        "base_construction_turns": 12,
        "base_effects": {"construction_cost_reduction": 0.05, "land_trade_capacity": 150},
    },

    # ============================================================
    # TRANSPORT
    # ============================================================
    "road_network": {
        "label": "Road Network",
        "category": "transport",
        "description": "Paved road infrastructure that improves how efficiently province surplus reaches the national pool.",
        "base_workers": 150,
        "base_inputs": {"materials": 150, "fuel": 50},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1200, "kapital": 500},
        "base_construction_turns": 9,
        "base_effects": {"integration_bonus": 0.05, "march_speed_bonus": 0.05},
    },
    "railway_station": {
        "label": "Railway Station",
        "category": "transport",
        "description": "Rail infrastructure that dramatically improves integration and speeds up provincial construction.",
        "base_workers": 200,
        "base_inputs": {"materials": 200, "energy": 150, "heavy_equipment": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 2500, "kapital": 1200},
        "base_construction_turns": 15,
        "base_effects": {"integration_bonus": 0.08, "construction_time_reduction": 0.05, "march_speed_bonus": 0.10},
    },
    "logistics_hub": {
        "label": "Logistics Hub",
        "category": "transport",
        "description": "Centralised distribution network improving province integration and reducing national upkeep.",
        "base_workers": 175,
        "base_inputs": {"kapital": 150, "fuel": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1000, "kapital": 700},
        "base_construction_turns": 8,
        "base_effects": {"integration_bonus": 0.04, "upkeep_reduction": 0.02, "march_speed_bonus": 0.03, "river_transit_speed": 0.03},
    },
    "dock": {
        "label": "Dock",
        "category": "transport",
        "description": (
            "Port infrastructure enabling naval access. Required for province↔sea zone movement. "
            "Reduces transition time from this province to adjacent sea and river zones."
        ),
        "base_workers": 200,
        "base_inputs": {"materials": 180, "fuel": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1800, "kapital": 900},
        "base_construction_turns": 12,
        "base_effects": {"sea_transit_speed": 0.25, "river_transit_speed": 0.15},
    },
    "port": {
        "label": "Port",
        "category": "transport",
        "description": "Commercial harbour for naval trade. Generates naval trade capacity and speeds sea access.",
        "base_workers": 300,
        "base_inputs": {"materials": 200, "fuel": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 2500, "kapital": 1200},
        "base_construction_turns": 15,
        "base_effects": {"naval_trade_capacity": 50, "sea_transit_speed": 0.10},
    },
    "bridge": {
        "label": "Bridge",
        "category": "transport",
        "description": "River crossing enabling movement and trade across river zones.",
        "base_workers": 150,
        "base_inputs": {"materials": 150},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1000, "kapital": 400},
        "base_construction_turns": 8,
        "base_effects": {"land_trade_capacity": 30, "river_transit_speed": 0.20},
    },
    "railroad": {
        "label": "Railroad",
        "category": "transport",
        "description": "Rail track infrastructure connecting provinces. Improves march speed and land trade capacity.",
        "base_workers": 400,
        "base_inputs": {"materials": 300, "heavy_equipment": 50, "fuel": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 3000, "kapital": 1500},
        "base_construction_turns": 18,
        "base_effects": {"march_speed_bonus": 0.15, "land_trade_capacity": 60},
    },
    "train_depot": {
        "label": "Train Depot",
        "category": "transport",
        "description": "Rail freight depot. Increases land trade capacity and national march speed.",
        "base_workers": 200,
        "base_inputs": {"materials": 150, "fuel": 100},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1500, "kapital": 700},
        "base_construction_turns": 10,
        "base_effects": {"land_trade_capacity": 40, "march_speed_bonus": 0.05},
    },
    "train_station": {
        "label": "Train Station",
        "category": "transport",
        "description": "Rail passenger station. Speeds troop movement through this province.",
        "base_workers": 250,
        "base_inputs": {"materials": 180, "energy": 100},
        "base_outputs": {},
        "base_construction_cost": {"materials": 2000, "kapital": 1000},
        "base_construction_turns": 12,
        "base_effects": {"march_speed_bonus": 0.10, "land_trade_capacity": 50},
    },
    "train_cargo_terminal": {
        "label": "Train Cargo Terminal",
        "category": "transport",
        "description": "Rail bulk cargo terminal. Large land trade capacity.",
        "base_workers": 350,
        "base_inputs": {"materials": 250, "fuel": 120},
        "base_outputs": {},
        "base_construction_cost": {"materials": 2500, "kapital": 1200},
        "base_construction_turns": 14,
        "base_effects": {"land_trade_capacity": 80},
    },
    "airport": {
        "label": "Airport",
        "category": "transport",
        "description": "Civilian air terminal. Enables civilian air zone access and generates air trade capacity.",
        "base_workers": 300,
        "base_inputs": {"materials": 200, "energy": 150, "fuel": 100},
        "base_outputs": {},
        "base_construction_cost": {"materials": 3000, "kapital": 1800},
        "base_construction_turns": 16,
        "base_effects": {"air_transit_speed": 0.15, "air_trade_capacity": 40},
    },
    "air_cargo_terminal": {
        "label": "Air Cargo Terminal",
        "category": "transport",
        "description": "Air freight facility. Generates large air trade capacity.",
        "base_workers": 250,
        "base_inputs": {"materials": 180, "fuel": 150},
        "base_outputs": {},
        "base_construction_cost": {"materials": 2500, "kapital": 1500},
        "base_construction_turns": 13,
        "base_effects": {"air_trade_capacity": 60},
    },

    # ============================================================
    # COMMUNICATIONS
    # ============================================================
    "radio_tower": {
        "label": "Radio Tower",
        "category": "communications",
        "description": "Broadcasts information and morale messages, improving province stability recovery.",
        "base_workers": 80,
        "base_inputs": {"materials": 60, "energy": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 700, "kapital": 400},
        "base_construction_turns": 5,
        "base_effects": {"stability_recovery_bonus": 0.10},
    },
    "telegraph_network": {
        "label": "Telegraph Network",
        "category": "communications",
        "description": "Rapid information exchange that boosts research output and province stability.",
        "base_workers": 100,
        "base_inputs": {"kapital": 100, "energy": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 800, "kapital": 600},
        "base_construction_turns": 6,
        "base_effects": {"research_bonus": 0.10, "stability_recovery_bonus": 0.08, "security": 2},
    },
    "broadcasting_station": {
        "label": "Broadcasting Station",
        "category": "communications",
        "description": "High-power media broadcast that significantly improves province morale and stability recovery.",
        "base_workers": 120,
        "base_inputs": {"energy": 150, "kapital": 100},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1000, "kapital": 700},
        "base_construction_turns": 7,
        "base_effects": {"stability_recovery_bonus": 0.15},
    },

    # ============================================================
    # ENTERTAINMENT / TOURISM
    # ============================================================
    "tavern": {
        "label": "Tavern",
        "category": "entertainment",
        "description": "A public gathering place providing modest stability benefits at low cost.",
        "base_workers": 60,
        "base_inputs": {"food": 100, "kapital": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 300, "kapital": 200},
        "base_construction_turns": 3,
        "base_effects": {"stability_recovery_bonus": 0.08},
    },
    "theatre": {
        "label": "Theatre",
        "category": "entertainment",
        "description": "Cultural venue that improves stability and attracts population growth.",
        "base_workers": 100,
        "base_inputs": {"kapital": 150},
        "base_outputs": {},
        "base_construction_cost": {"materials": 700, "kapital": 500},
        "base_construction_turns": 6,
        "base_effects": {"stability_recovery_bonus": 0.12, "growth_bonus": 0.001},
    },
    "resort": {
        "label": "Resort",
        "category": "entertainment",
        "description": "Tourism destination that generates trade capacity and improves province stability.",
        "base_workers": 250,
        "base_inputs": {"kapital": 200, "consumer_goods": 100, "fuel": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1200, "kapital": 1000},
        "base_construction_turns": 10,
        "base_effects": {"stability_recovery_bonus": 0.15, "land_trade_capacity": 280},
    },

    # ============================================================
    # HEALTHCARE
    # ============================================================
    "clinic": {
        "label": "Clinic",
        "category": "healthcare",
        "description": "Basic medical facility improving population health, growth, and stability.",
        "base_workers": 100,
        "base_inputs": {"medicine": 50, "kapital": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 700, "kapital": 500},
        "base_construction_turns": 6,
        "base_effects": {"growth_bonus": 0.001, "stability_recovery_bonus": 0.08},
    },
    "hospital": {
        "label": "Hospital",
        "category": "healthcare",
        "description": "Full medical facility that significantly boosts population growth through advanced healthcare.",
        "base_workers": 350,
        "base_inputs": {"medicine": 120, "energy": 100, "kapital": 150},
        "base_outputs": {},
        "base_construction_cost": {"materials": 2000, "kapital": 1500},
        "base_construction_turns": 14,
        "base_effects": {"growth_bonus": 0.002},
    },
    "sanitation_works": {
        "label": "Sanitation Works",
        "category": "healthcare",
        "description": "Public health infrastructure that improves population growth through disease prevention.",
        "base_workers": 150,
        "base_inputs": {"materials": 120, "energy": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 800, "kapital": 400},
        "base_construction_turns": 7,
        "base_effects": {"growth_bonus": 0.001},
    },

    # ============================================================
    # RELIGIOUS
    # ============================================================
    "church": {
        "label": "Church",
        "category": "religious",
        "description": "Centre of community and administration. Provides the largest bureaucratic capacity bonus of any religious building.",
        "base_workers": 80,
        "base_inputs": {"kapital": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 500, "kapital": 300},
        "base_construction_turns": 5,
        "base_effects": {"bureaucratic_capacity": 15, "stability_recovery_bonus": 0.05, "literacy_bonus": 0.03},
    },
    "madrasa": {
        "label": "Madrasa",
        "category": "religious",
        "description": "Religious school combining spiritual teaching with practical education. Provides the largest literacy bonus of any religious building.",
        "base_workers": 100,
        "base_inputs": {"kapital": 80, "research": 30},
        "base_outputs": {},
        "base_construction_cost": {"materials": 600, "kapital": 400},
        "base_construction_turns": 6,
        "base_effects": {"literacy_bonus": 0.06, "research_bonus": 0.08, "bureaucratic_capacity": 8},
    },
    "holy_site": {
        "label": "Holy Site",
        "category": "religious",
        "description": "Sacred pilgrimage destination that inspires devotion and unity. Provides the largest stability bonus of any religious building.",
        "base_workers": 60,
        "base_inputs": {"kapital": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 700, "kapital": 500},
        "base_construction_turns": 8,
        "base_effects": {"stability_recovery_bonus": 0.20, "growth_bonus": 0.001, "bureaucratic_capacity": 5},
    },

    # ============================================================
    # GREEN ENERGY
    # Renewable alternatives to fossil-fuel energy.
    # ============================================================
    "wind_farm": {
        "label": "Wind Farm",
        "category": "green_energy",
        "description": "Turbine array generating clean energy from wind. Low worker cost allows multiple installations.",
        "base_workers": 60,
        "base_inputs": {"materials": 40},
        "base_outputs": {"energy": 100},
        "base_construction_cost": {"materials": 600, "kapital": 300},
        "base_construction_turns": 5,
        "base_effects": {},
    },
    "solar_array": {
        "label": "Solar Array",
        "category": "green_energy",
        "description": "Photovoltaic panel installation producing clean energy. Higher output than wind but needs more components.",
        "base_workers": 80,
        "base_inputs": {"materials": 50, "components": 30},
        "base_outputs": {"energy": 130},
        "base_construction_cost": {"materials": 800, "kapital": 500},
        "base_construction_turns": 6,
        "base_effects": {},
    },
    "hydroelectric_dam": {
        "label": "Hydroelectric Dam",
        "category": "green_energy",
        "description": "Large-scale water-powered generator. Highest green energy output but significant construction investment.",
        "base_workers": 120,
        "base_inputs": {"materials": 80, "heavy_equipment": 40},
        "base_outputs": {"energy": 200},
        "base_construction_cost": {"materials": 1500, "kapital": 800},
        "base_construction_turns": 10,
        "base_effects": {},
    },

    # ============================================================
    # GOVERNMENT — REGULATORY
    # ============================================================
    "regulatory_office": {
        "label": "Regulatory Office",
        "category": "government_regulatory",
        "description": "Establishes trade standards and market rules, improving province integration efficiency.",
        "base_workers": 100,
        "base_inputs": {"kapital": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 500, "kapital": 400},
        "base_construction_turns": 5,
        "base_effects": {"integration_bonus": 0.04, "bureaucratic_capacity": 10},
    },
    "standards_bureau": {
        "label": "Standards Bureau",
        "category": "government_regulatory",
        "description": "Sets quality and safety standards for industry, reducing construction costs through standardised practices.",
        "base_workers": 120,
        "base_inputs": {"kapital": 100, "research": 30},
        "base_outputs": {},
        "base_construction_cost": {"materials": 600, "kapital": 500},
        "base_construction_turns": 6,
        "base_effects": {"construction_cost_reduction": 0.03, "bureaucratic_capacity": 12},
    },

    # ============================================================
    # GOVERNMENT — OVERSIGHT
    # ============================================================
    "inspector_general": {
        "label": "Inspector General",
        "category": "government_oversight",
        "description": "Anti-corruption and accountability office that reduces government waste and upkeep costs.",
        "base_workers": 80,
        "base_inputs": {"kapital": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 400, "kapital": 350},
        "base_construction_turns": 4,
        "base_effects": {"upkeep_reduction": 0.03, "bureaucratic_capacity": 8},
    },
    "audit_commission": {
        "label": "Audit Commission",
        "category": "government_oversight",
        "description": "Financial oversight body that improves integration efficiency through transparent accounting.",
        "base_workers": 100,
        "base_inputs": {"kapital": 80, "research": 20},
        "base_outputs": {},
        "base_construction_cost": {"materials": 500, "kapital": 450},
        "base_construction_turns": 5,
        "base_effects": {"integration_bonus": 0.03, "upkeep_reduction": 0.02, "bureaucratic_capacity": 10},
    },

    # ============================================================
    # GOVERNMENT — MANAGEMENT
    # ============================================================
    "civil_service_academy": {
        "label": "Civil Service Academy",
        "category": "government_management",
        "description": "Trains government administrators, providing large bureaucratic capacity and literacy gains.",
        "base_workers": 120,
        "base_inputs": {"kapital": 100, "research": 40},
        "base_outputs": {},
        "base_construction_cost": {"materials": 700, "kapital": 600},
        "base_construction_turns": 7,
        "base_effects": {"bureaucratic_capacity": 25, "literacy_bonus": 0.05},
    },
    "administrative_center": {
        "label": "Administrative Center",
        "category": "government_management",
        "description": "Central government hub coordinating provincial administration. Reduces upkeep and provides bureaucratic capacity.",
        "base_workers": 150,
        "base_inputs": {"kapital": 120},
        "base_outputs": {},
        "base_construction_cost": {"materials": 800, "kapital": 700},
        "base_construction_turns": 8,
        "base_effects": {"bureaucratic_capacity": 30, "upkeep_reduction": 0.02},
    },

    # ============================================================
    # GOVERNMENT — SECURITY
    # ============================================================
    "police_headquarters": {
        "label": "Security Center",
        "category": "government_security",
        "description": "Major law enforcement hub providing significant public security and accelerating stability recovery. Urban provinces only.",
        "urban_only": True,
        "base_workers": 200,
        "base_inputs": {"kapital": 150, "arms": 50},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1200, "kapital": 900},
        "base_construction_turns": 9,
        "base_effects": {"security": 10, "stability_recovery_bonus": 0.15, "bureaucratic_capacity": 8},
    },
    "police_station": {
        "label": "Police Station",
        "category": "government_security",
        "description": "Local policing post maintaining order in urban neighbourhoods. Urban provinces only.",
        "urban_only": True,
        "base_workers": 80,
        "base_inputs": {"kapital": 60, "arms": 15},
        "base_outputs": {},
        "base_construction_cost": {"materials": 400, "kapital": 300},
        "base_construction_turns": 4,
        "base_effects": {"security": 4},
    },
    "sheriffs_office": {
        "label": "Sheriff's Office",
        "category": "government_security",
        "description": "Rural law enforcement post providing security across dispersed countryside communities. Rural provinces only.",
        "rural_only": True,
        "base_workers": 60,
        "base_inputs": {"kapital": 40},
        "base_outputs": {},
        "base_construction_cost": {"materials": 250, "kapital": 200},
        "base_construction_turns": 3,
        "base_effects": {"security": 5},
    },
    "fire_house": {
        "label": "Fire House",
        "category": "government_security",
        "description": "Fire and emergency response station reducing disaster risk and improving community safety.",
        "base_workers": 50,
        "base_inputs": {"kapital": 30},
        "base_outputs": {},
        "base_construction_cost": {"materials": 200, "kapital": 150},
        "base_construction_turns": 3,
        "base_effects": {"security": 2},
    },
    "disaster_management": {
        "label": "Disaster Management Facility",
        "category": "government_security",
        "description": "Centralised crisis coordination hub for urban areas, providing major security improvements. Urban provinces only.",
        "urban_only": True,
        "base_workers": 120,
        "base_inputs": {"kapital": 80, "energy": 40},
        "base_outputs": {},
        "base_construction_cost": {"materials": 600, "kapital": 450},
        "base_construction_turns": 5,
        "base_effects": {"security": 8},
    },

    # ============================================================
    # GOVERNMENT — EDUCATION
    # ============================================================
    "public_school": {
        "label": "Public School",
        "category": "government_education",
        "description": "State-funded basic education providing broad literacy improvements at low cost.",
        "base_workers": 100,
        "base_inputs": {"kapital": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 500, "kapital": 350},
        "base_construction_turns": 5,
        "base_effects": {"literacy_bonus": 0.08, "growth_bonus": 0.001},
    },
    "university": {
        "label": "University",
        "category": "government_education",
        "description": "Advanced institution of learning producing research output and high literacy gains.",
        "base_workers": 200,
        "base_inputs": {"kapital": 150, "research": 50},
        "base_outputs": {"research": 80},
        "base_construction_cost": {"materials": 1000, "kapital": 800},
        "base_construction_turns": 8,
        "base_effects": {"literacy_bonus": 0.06, "research_bonus": 0.15},
    },

    # ============================================================
    # GOVERNMENT — ORGANIZATION
    # ============================================================
    "labor_bureau": {
        "label": "Labor Bureau",
        "category": "government_organization",
        "description": "Coordinates workforce allocation and labour standards, reducing construction times.",
        "base_workers": 100,
        "base_inputs": {"kapital": 80},
        "base_outputs": {},
        "base_construction_cost": {"materials": 500, "kapital": 400},
        "base_construction_turns": 5,
        "base_effects": {"construction_time_reduction": 0.06, "bureaucratic_capacity": 10},
    },
    "workers_council": {
        "label": "Workers' Council",
        "category": "government_organization",
        "description": "Representative body for workers that improves construction costs through collective bargaining.",
        "base_workers": 80,
        "base_inputs": {"kapital": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 400, "kapital": 300},
        "base_construction_turns": 4,
        "base_effects": {"construction_cost_reduction": 0.03, "stability_recovery_bonus": 0.05, "bureaucratic_capacity": 8},
    },

    # ============================================================
    # GOVERNMENT — WELFARE
    # ============================================================
    "social_services_office": {
        "label": "Social Services Office",
        "category": "government_welfare",
        "description": "Coordinates welfare programs that improve population growth through social support.",
        "base_workers": 100,
        "base_inputs": {"kapital": 100, "consumer_goods": 40},
        "base_outputs": {},
        "base_construction_cost": {"materials": 500, "kapital": 400},
        "base_construction_turns": 5,
        "base_effects": {"growth_bonus": 0.002, "stability_recovery_bonus": 0.05},
    },
    "public_housing": {
        "label": "Public Housing",
        "category": "government_welfare",
        "description": "State-built housing that attracts population growth and improves stability through housing security.",
        "base_workers": 80,
        "base_inputs": {"materials": 80, "kapital": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 600, "kapital": 300},
        "base_construction_turns": 5,
        "base_effects": {"growth_bonus": 0.003, "stability_recovery_bonus": 0.08},
    },

    # ============================================================
    # MILITARY BASES
    # Bases consume military_goods as operational upkeep.
    # They do not produce output goods but unlock unit training.
    # ============================================================
    "army_base": {
        "label": "Army Base",
        "category": "military_army",
        "description": "Garrison and training facility for ground forces.",
        "base_workers": 300,
        "base_inputs": {"kapital": 100, "military_goods": 50},
        "base_outputs": {},
        "base_construction_cost": {"materials": 1500, "kapital": 800, "manpower": 500},
        "base_construction_turns": 10,
        "base_effects": {},
    },
    "naval_base": {
        "label": "Naval Base",
        "category": "military_naval",
        "description": "Port and drydock facility for naval forces. Requires coastal or river access.",
        "base_workers": 300,
        "base_inputs": {"kapital": 130, "military_goods": 65, "fuel": 30},
        "base_outputs": {},
        "base_construction_cost": {"materials": 2000, "kapital": 1200, "manpower": 600},
        "base_construction_turns": 13,
        "base_effects": {},
    },
    "air_base": {
        "label": "Air Base",
        "category": "military_air",
        "description": "Airfield and hangar complex for aerial forces. Cheap to establish but fuel-intensive to operate.",
        "base_workers": 200,
        "base_inputs": {"kapital": 80, "military_goods": 40, "fuel": 120},
        "base_outputs": {},
        "base_construction_cost": {"materials": 800, "kapital": 600, "manpower": 300},
        "base_construction_turns": 6,
        "base_effects": {},
    },

    # ============================================================
    # MILITARY EDUCATION
    # Nation-unique (unique_per_nation = True). One per nation.
    # All effects are national-scope. Uses steeper cost scaling
    # (cost_scale=1.80) to make high levels extremely expensive.
    # Naval War College is coastal-only (requires is_coastal).
    # ============================================================
    "military_academy": {
        "label": "Military Academy",
        "category": "military_education",
        "description": (
            "Elite officer training institution for ground forces. "
            "Improves army training speed, combat effectiveness, march speed, and unit upkeep efficiency. "
            "Nation-unique — only one may exist across all provinces."
        ),
        "unique_per_nation": True,
        "cost_scale": 1.80,
        "base_workers": 350,
        "base_inputs": {"kapital": 500, "research": 100, "consumer_goods": 150},
        "base_outputs": {},
        "base_construction_cost": {"materials": 5000, "kapital": 4000},
        "base_construction_turns": 24,
        "base_effects": {
            "army_training_speed_bonus": 0.08,
            "army_combat_bonus": 0.04,
            "march_speed_bonus": 0.03,
            "army_upkeep_reduction": 0.04,
        },
    },
    "naval_war_college": {
        "label": "Naval War College",
        "category": "military_education",
        "description": (
            "Maritime officer academy and strategic studies institute. "
            "Improves navy training speed, combat effectiveness, sea transit speed, and unit upkeep efficiency. "
            "Nation-unique and coastal-only."
        ),
        "unique_per_nation": True,
        "cost_scale": 1.80,
        "base_workers": 350,
        "base_inputs": {"kapital": 500, "research": 100, "fuel": 150},
        "base_outputs": {},
        "base_construction_cost": {"materials": 5000, "kapital": 4000},
        "base_construction_turns": 24,
        "base_effects": {
            "navy_training_speed_bonus": 0.08,
            "navy_combat_bonus": 0.04,
            "sea_transit_speed": 0.03,
            "navy_upkeep_reduction": 0.04,
        },
    },
    "air_force_academy": {
        "label": "Air Force Academy",
        "category": "military_education",
        "description": (
            "Precision flight and tactics school for aerial forces. "
            "Improves air training speed, combat effectiveness, air transit speed, and unit upkeep efficiency. "
            "Nation-unique — only one may exist across all provinces."
        ),
        "unique_per_nation": True,
        "cost_scale": 1.80,
        "base_workers": 350,
        "base_inputs": {"kapital": 500, "research": 120, "fuel": 100, "components": 50},
        "base_outputs": {},
        "base_construction_cost": {"materials": 5000, "kapital": 4500},
        "base_construction_turns": 26,
        "base_effects": {
            "air_training_speed_bonus": 0.08,
            "air_combat_bonus": 0.04,
            "air_transit_speed": 0.03,
            "air_upkeep_reduction": 0.04,
        },
    },

    # ============================================================
    # ESPIONAGE
    # Two attack buildings (espionage_attack category) and two
    # defense buildings (espionage_defense category).
    # Foreign Intel HQ and Domestic Intel HQ are nation-unique.
    # ============================================================
    "foreign_intel_hq": {
        "label": "Foreign Intelligence Agency HQ",
        "category": "espionage_attack",
        "description": (
            "Central command for foreign intelligence operations. "
            "Each level enables one additional simultaneous foreign espionage target. "
            "Nation-unique — only one may exist across all provinces."
        ),
        "unique_per_nation": True,
        "base_workers": 150,
        "base_inputs": {"kapital": 200, "research": 60},
        "base_outputs": {},
        "base_construction_cost": {"materials": 800, "kapital": 1200},
        "base_construction_turns": 10,
        "base_effects": {"espionage_attack": 8},
    },
    "branch_office": {
        "label": "Intelligence Branch Office",
        "category": "espionage_attack",
        "description": (
            "Regional intelligence office. Must be specialized in a foreign action "
            "after construction via a separate order. Each level allows one additional "
            "simultaneous use of its specialized action."
        ),
        "base_workers": 80,
        "base_inputs": {"kapital": 80, "research": 20},
        "base_outputs": {},
        "base_construction_cost": {"materials": 400, "kapital": 500},
        "base_construction_turns": 6,
        "base_effects": {"espionage_attack": 3},
    },
    "domestic_intel_hq": {
        "label": "Domestic Intelligence Agency HQ",
        "category": "espionage_defense",
        "description": (
            "Counter-intelligence headquarters. Boosts national defense and enables "
            "Suppress Foreign Operations actions. "
            "Nation-unique — only one may exist across all provinces."
        ),
        "unique_per_nation": True,
        "base_workers": 140,
        "base_inputs": {"kapital": 180, "research": 40},
        "base_outputs": {},
        "base_construction_cost": {"materials": 700, "kapital": 900},
        "base_construction_turns": 8,
        "base_effects": {"espionage_defense": 8},
    },
    "local_office": {
        "label": "Local Intelligence Office",
        "category": "espionage_defense",
        "description": (
            "Provincial counter-intelligence office. Boosts this province's defense "
            "against foreign espionage operations."
        ),
        "base_workers": 50,
        "base_inputs": {"kapital": 50},
        "base_outputs": {},
        "base_construction_cost": {"materials": 250, "kapital": 300},
        "base_construction_turns": 5,
        "base_effects": {"provincial_espionage_defense": 5},
    },
}

# Consumer goods consumed per population unit per turn.
# At 10 000 pop this requires 100 consumer goods/turn.
CONSUMER_GOODS_PER_POP = 0.01

# Stability penalty applied when consumer goods are in deficit.
# Applied as: deficit_ratio × CONSUMER_GOODS_DEFICIT_PENALTY.
# Kept at 5.0: early-game universal deficit should warn, not collapse.
CONSUMER_GOODS_DEFICIT_PENALTY = 5.0

# ---------------------------------------------------------------------------
# Networking efficiency bonuses
# Applied as additive bonuses to the efficiency multiplier (on top of 1.0).
# ---------------------------------------------------------------------------

# Input co-location: province's terrain primary resource appears in a
# building's input_goods → +10% output efficiency.
# Rewards placing industry where its raw inputs are locally available.
# Example: workshop (needs materials) in a mountain province (+10%).
INPUT_COLOCATION_BONUS = 0.10

# Concentration bonuses: replace the old fixed INDUSTRY_CLUSTER_BONUS.
# Same-type (e.g. two workshops): +3% per level of the building type in province.
# Same-category (e.g. workshop + arms_factory, both heavy_manufacturing): +0.75% per level
# of OTHER buildings in the same category in the province.
# Formula: concentration_bonus = SAME_TYPE × own_level + SAME_CATEGORY × other_category_levels
# Rationale: category bonus is 1/4 the same-type bonus, encouraging specialisation
# within a province while still rewarding broader industrial districts.
SAME_TYPE_CONCENTRATION_BONUS = 0.03
SAME_CATEGORY_CONCENTRATION_BONUS = 0.0075
