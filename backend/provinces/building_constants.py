"""Building types and constants for the buildings system.

Manufactured goods (NationGoodStock):
  consumer_goods  - produced by factories/mills, consumed by population each turn
  arms            - produced by arms factories, used by military
  fuel            - produced by refineries, used by vehicles/military
  machinery       - produced by workshops, used by factories
  chemicals       - produced by chemical plants, used in pharma/fertilizers/plastics
  medicine        - produced by pharmaceutical labs, consumed by hospitals/clinics
  components      - produced by precision workshops/cement plants, used in electronics
  heavy_equipment - produced by heavy forges, used in extraction/construction
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

Use-it-or-lose-it effects:
  land_trade_capacity, naval_trade_capacity, air_trade_capacity and bureaucratic_capacity
  are computed fresh each turn from active buildings (summed nationally). They are NOT stockpiled.

Keys in per-level config:
  workers            - population drawn from province (not available for subsistence)
  input_goods        - good_key → amount consumed per turn
  output_goods       - good_key → amount produced per turn
  construction_cost  - basic resource key → amount deducted immediately on build
  construction_turns - months until building becomes active
  effects            - effect_key → value (additive, no scope annotation needed)
"""

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
    "march_speed_bonus",       # province-scope land travel speed (road_network, railway_station)
    "sea_transit_speed",       # province-scope sea embarkation speed (dock, port)
    "river_transit_speed",     # province-scope river crossing speed (dock, bridge)
    "air_transit_speed",       # province-scope air transition speed (airport)
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
]

BUILDING_TYPES = {
    # ============================================================
    # ORIGINAL CORE BUILDINGS
    # ============================================================
    "workshop": {
        "label": "Workshop",
        "category": "heavy_manufacturing",
        "description": "Converts raw materials into machinery.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"materials": 200},
                "output_goods": {"machinery": 100},
                "construction_cost": {"materials": 1000, "wealth": 500},
                "construction_turns": 6,
                "effects": {},
            },
            {
                "workers": 500,
                "input_goods": {"materials": 500},
                "output_goods": {"machinery": 250},
                "construction_cost": {"materials": 2000, "wealth": 1000},
                "construction_turns": 12,
                "effects": {},
            },
            {
                "workers": 900,
                "input_goods": {"materials": 900},
                "output_goods": {"machinery": 500},
                "construction_cost": {"materials": 3500, "wealth": 1500},
                "construction_turns": 18,
                "effects": {},
            },
        ],
    },
    "factory": {
        "label": "Factory",
        "category": "light_manufacturing",
        "description": "Produces consumer goods using materials, energy, and machinery.",
        "max_level": 4,
        "levels": [
            {
                "workers": 400,
                "input_goods": {"materials": 300, "energy": 200, "machinery": 100},
                "output_goods": {"consumer_goods": 200},
                "construction_cost": {"materials": 1500, "wealth": 800},
                "construction_turns": 12,
                "effects": {},
            },
            {
                "workers": 800,
                "input_goods": {"materials": 600, "energy": 400, "machinery": 200},
                "output_goods": {"consumer_goods": 450},
                "construction_cost": {"materials": 2800, "wealth": 1500},
                "construction_turns": 18,
                "effects": {},
            },
            {
                "workers": 1200,
                "input_goods": {"materials": 1000, "energy": 700, "machinery": 350},
                "output_goods": {"consumer_goods": 800},
                "construction_cost": {"materials": 4500, "wealth": 2500},
                "construction_turns": 24,
                "effects": {},
            },
            {
                "workers": 1800,
                "input_goods": {"materials": 1500, "energy": 1000, "machinery": 550},
                "output_goods": {"consumer_goods": 1300},
                "construction_cost": {"materials": 7000, "wealth": 4000},
                "construction_turns": 36,
                "effects": {},
            },
        ],
    },
    "refinery": {
        "label": "Refinery",
        "category": "refining",
        "description": "Converts materials and energy into fuel.",
        "max_level": 3,
        "levels": [
            {
                "workers": 300,
                "input_goods": {"materials": 250, "energy": 300},
                "output_goods": {"fuel": 150},
                "construction_cost": {"materials": 1200, "wealth": 700},
                "construction_turns": 9,
                "effects": {},
            },
            {
                "workers": 700,
                "input_goods": {"materials": 550, "energy": 700},
                "output_goods": {"fuel": 350},
                "construction_cost": {"materials": 2500, "wealth": 1400},
                "construction_turns": 15,
                "effects": {},
            },
            {
                "workers": 1200,
                "input_goods": {"materials": 1000, "energy": 1200},
                "output_goods": {"fuel": 700},
                "construction_cost": {"materials": 4000, "wealth": 2200},
                "construction_turns": 24,
                "effects": {},
            },
        ],
    },
    "arms_factory": {
        "label": "Arms Factory",
        "category": "heavy_manufacturing",
        "description": "Produces arms using materials, energy, and fuel.",
        "max_level": 3,
        "levels": [
            {
                "workers": 400,
                "input_goods": {"materials": 400, "energy": 200, "fuel": 100},
                "output_goods": {"arms": 150},
                "construction_cost": {"materials": 2000, "wealth": 1000, "manpower": 500},
                "construction_turns": 12,
                "effects": {},
            },
            {
                "workers": 800,
                "input_goods": {"materials": 800, "energy": 400, "fuel": 200},
                "output_goods": {"arms": 350},
                "construction_cost": {"materials": 4000, "wealth": 2000, "manpower": 1000},
                "construction_turns": 18,
                "effects": {},
            },
            {
                "workers": 1400,
                "input_goods": {"materials": 1400, "energy": 700, "fuel": 350},
                "output_goods": {"arms": 700},
                "construction_cost": {"materials": 7000, "wealth": 3500, "manpower": 1750},
                "construction_turns": 30,
                "effects": {},
            },
        ],
    },

    # ============================================================
    # FINANCIAL
    # ============================================================
    "trading_post": {
        "label": "Trading Post",
        "category": "financial",
        "description": "Improves local trade networks, increasing how much of the province surplus reaches the national pool.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 100},
                "output_goods": {},
                "construction_cost": {"materials": 600, "wealth": 400},
                "construction_turns": 4,
                "effects": {"integration_bonus": 0.05, "land_trade_capacity": 50},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 200},
                "output_goods": {},
                "construction_cost": {"materials": 1200, "wealth": 800},
                "construction_turns": 8,
                "effects": {"integration_bonus": 0.10, "land_trade_capacity": 120},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 350},
                "output_goods": {},
                "construction_cost": {"materials": 2200, "wealth": 1500},
                "construction_turns": 12,
                "effects": {"integration_bonus": 0.15, "land_trade_capacity": 250},
            },
        ],
    },
    "bank": {
        "label": "Bank",
        "category": "financial",
        "description": "Reduces government upkeep nationally through efficient wealth management.",
        "max_level": 3,
        "levels": [
            {
                "workers": 150,
                "input_goods": {"wealth": 200},
                "output_goods": {},
                "construction_cost": {"materials": 800, "wealth": 1000},
                "construction_turns": 6,
                "effects": {"upkeep_reduction": 0.03, "land_trade_capacity": 80},
            },
            {
                "workers": 300,
                "input_goods": {"wealth": 400},
                "output_goods": {},
                "construction_cost": {"materials": 1500, "wealth": 2000},
                "construction_turns": 12,
                "effects": {"upkeep_reduction": 0.06, "land_trade_capacity": 200},
            },
            {
                "workers": 500,
                "input_goods": {"wealth": 600},
                "output_goods": {},
                "construction_cost": {"materials": 2500, "wealth": 4000},
                "construction_turns": 18,
                "effects": {"upkeep_reduction": 0.10, "land_trade_capacity": 400},
            },
        ],
    },
    "stock_exchange": {
        "label": "Stock Exchange",
        "category": "financial",
        "description": "Centralised capital market that reduces construction costs nationwide through efficient resource allocation.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"wealth": 300, "research": 50},
                "output_goods": {},
                "construction_cost": {"materials": 1500, "wealth": 2000},
                "construction_turns": 12,
                "effects": {"construction_cost_reduction": 0.05, "land_trade_capacity": 150},
            },
            {
                "workers": 400,
                "input_goods": {"wealth": 600, "research": 100},
                "output_goods": {},
                "construction_cost": {"materials": 3000, "wealth": 4000},
                "construction_turns": 18,
                "effects": {"construction_cost_reduction": 0.10, "land_trade_capacity": 350},
            },
            {
                "workers": 700,
                "input_goods": {"wealth": 1000, "research": 150},
                "output_goods": {},
                "construction_cost": {"materials": 5000, "wealth": 7000},
                "construction_turns": 24,
                "effects": {"construction_cost_reduction": 0.15, "land_trade_capacity": 700},
            },
        ],
    },

    # ============================================================
    # LIGHT MANUFACTURING
    # ============================================================
    "textile_mill": {
        "label": "Textile Mill",
        "category": "light_manufacturing",
        "description": "Produces basic consumer goods from materials. An accessible early-game alternative to the factory.",
        "max_level": 3,
        "levels": [
            {
                "workers": 300,
                "input_goods": {"materials": 200, "manpower": 100},
                "output_goods": {"consumer_goods": 120},
                "construction_cost": {"materials": 800, "wealth": 400},
                "construction_turns": 6,
                "effects": {},
            },
            {
                "workers": 600,
                "input_goods": {"materials": 400, "manpower": 200},
                "output_goods": {"consumer_goods": 260},
                "construction_cost": {"materials": 1600, "wealth": 800},
                "construction_turns": 10,
                "effects": {},
            },
            {
                "workers": 1000,
                "input_goods": {"materials": 700, "manpower": 300},
                "output_goods": {"consumer_goods": 440},
                "construction_cost": {"materials": 2800, "wealth": 1400},
                "construction_turns": 15,
                "effects": {},
            },
        ],
    },
    "electronics_factory": {
        "label": "Electronics Factory",
        "category": "light_manufacturing",
        "description": "Produces high-quality consumer goods from components and stimulates local research.",
        "max_level": 4,
        "levels": [
            {
                "workers": 350,
                "input_goods": {"materials": 250, "energy": 200, "components": 100},
                "output_goods": {"consumer_goods": 250},
                "construction_cost": {"materials": 1800, "wealth": 1200},
                "construction_turns": 12,
                "effects": {"research_bonus": 0.10},
            },
            {
                "workers": 700,
                "input_goods": {"materials": 500, "energy": 400, "components": 200},
                "output_goods": {"consumer_goods": 550},
                "construction_cost": {"materials": 3500, "wealth": 2400},
                "construction_turns": 18,
                "effects": {"research_bonus": 0.20},
            },
            {
                "workers": 1100,
                "input_goods": {"materials": 800, "energy": 650, "components": 350},
                "output_goods": {"consumer_goods": 950},
                "construction_cost": {"materials": 6000, "wealth": 4000},
                "construction_turns": 24,
                "effects": {"research_bonus": 0.30},
            },
            {
                "workers": 1600,
                "input_goods": {"materials": 1200, "energy": 1000, "components": 550},
                "output_goods": {"consumer_goods": 1500},
                "construction_cost": {"materials": 9000, "wealth": 6000},
                "construction_turns": 30,
                "effects": {"research_bonus": 0.40},
            },
        ],
    },
    "precision_workshop": {
        "label": "Precision Workshop",
        "category": "light_manufacturing",
        "description": "Converts materials and machinery into precision components for advanced manufacturing.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"materials": 200, "machinery": 100},
                "output_goods": {"components": 150},
                "construction_cost": {"materials": 1200, "wealth": 700},
                "construction_turns": 9,
                "effects": {},
            },
            {
                "workers": 450,
                "input_goods": {"materials": 450, "machinery": 220},
                "output_goods": {"components": 350},
                "construction_cost": {"materials": 2400, "wealth": 1400},
                "construction_turns": 15,
                "effects": {},
            },
            {
                "workers": 800,
                "input_goods": {"materials": 800, "machinery": 400},
                "output_goods": {"components": 650},
                "construction_cost": {"materials": 4000, "wealth": 2500},
                "construction_turns": 21,
                "effects": {},
            },
        ],
    },

    # ============================================================
    # HEAVY MANUFACTURING
    # ============================================================
    "heavy_forge": {
        "label": "Heavy Forge",
        "category": "heavy_manufacturing",
        "description": "Produces heavy industrial equipment from raw materials. Unlocks advanced extraction and construction.",
        "max_level": 4,
        "levels": [
            {
                "workers": 350,
                "input_goods": {"materials": 400, "energy": 300},
                "output_goods": {"heavy_equipment": 150},
                "construction_cost": {"materials": 1800, "wealth": 900},
                "construction_turns": 12,
                "effects": {},
            },
            {
                "workers": 700,
                "input_goods": {"materials": 800, "energy": 600},
                "output_goods": {"heavy_equipment": 320},
                "construction_cost": {"materials": 3500, "wealth": 1800},
                "construction_turns": 18,
                "effects": {},
            },
            {
                "workers": 1100,
                "input_goods": {"materials": 1200, "energy": 1000},
                "output_goods": {"heavy_equipment": 550},
                "construction_cost": {"materials": 5500, "wealth": 3000},
                "construction_turns": 24,
                "effects": {},
            },
            {
                "workers": 1600,
                "input_goods": {"materials": 1800, "energy": 1500},
                "output_goods": {"heavy_equipment": 850},
                "construction_cost": {"materials": 8000, "wealth": 4500},
                "construction_turns": 30,
                "effects": {},
            },
        ],
    },
    "industrial_complex": {
        "label": "Industrial Complex",
        "category": "heavy_manufacturing",
        "description": "Large production complex outputting both consumer goods and machinery.",
        "max_level": 4,
        "levels": [
            {
                "workers": 600,
                "input_goods": {"materials": 600, "energy": 400, "heavy_equipment": 100},
                "output_goods": {"consumer_goods": 300, "machinery": 150},
                "construction_cost": {"materials": 3000, "wealth": 1500},
                "construction_turns": 18,
                "effects": {},
            },
            {
                "workers": 1100,
                "input_goods": {"materials": 1100, "energy": 750, "heavy_equipment": 200},
                "output_goods": {"consumer_goods": 600, "machinery": 300},
                "construction_cost": {"materials": 5500, "wealth": 3000},
                "construction_turns": 24,
                "effects": {},
            },
            {
                "workers": 1600,
                "input_goods": {"materials": 1600, "energy": 1100, "heavy_equipment": 350},
                "output_goods": {"consumer_goods": 1000, "machinery": 550},
                "construction_cost": {"materials": 8000, "wealth": 5000},
                "construction_turns": 30,
                "effects": {},
            },
            {
                "workers": 2200,
                "input_goods": {"materials": 2200, "energy": 1500, "heavy_equipment": 550},
                "output_goods": {"consumer_goods": 1500, "machinery": 900},
                "construction_cost": {"materials": 12000, "wealth": 7500},
                "construction_turns": 42,
                "effects": {},
            },
        ],
    },
    "shipyard": {
        "label": "Shipyard",
        "category": "heavy_manufacturing",
        "description": "Produces arms via large-vehicle construction. Engineering expertise reduces province construction times.",
        "max_level": 3,
        "levels": [
            {
                "workers": 500,
                "input_goods": {"materials": 500, "fuel": 100, "heavy_equipment": 150},
                "output_goods": {"arms": 200},
                "construction_cost": {"materials": 2500, "wealth": 1500},
                "construction_turns": 15,
                "effects": {"construction_time_reduction": 0.08},
            },
            {
                "workers": 1000,
                "input_goods": {"materials": 1000, "fuel": 200, "heavy_equipment": 300},
                "output_goods": {"arms": 450},
                "construction_cost": {"materials": 5000, "wealth": 3000},
                "construction_turns": 24,
                "effects": {"construction_time_reduction": 0.15},
            },
            {
                "workers": 1600,
                "input_goods": {"materials": 1600, "fuel": 350, "heavy_equipment": 500},
                "output_goods": {"arms": 800},
                "construction_cost": {"materials": 8000, "wealth": 5000},
                "construction_turns": 36,
                "effects": {"construction_time_reduction": 0.22},
            },
        ],
    },

    # ============================================================
    # REFINING
    # ============================================================
    "advanced_refinery": {
        "label": "Advanced Refinery",
        "category": "refining",
        "description": "Higher-throughput refinery that also produces chemicals as a byproduct.",
        "max_level": 4,
        "levels": [
            {
                "workers": 350,
                "input_goods": {"materials": 300, "energy": 350},
                "output_goods": {"fuel": 200, "chemicals": 80},
                "construction_cost": {"materials": 1600, "wealth": 900},
                "construction_turns": 10,
                "effects": {},
            },
            {
                "workers": 700,
                "input_goods": {"materials": 600, "energy": 700},
                "output_goods": {"fuel": 420, "chemicals": 170},
                "construction_cost": {"materials": 3000, "wealth": 1800},
                "construction_turns": 16,
                "effects": {},
            },
            {
                "workers": 1100,
                "input_goods": {"materials": 950, "energy": 1100},
                "output_goods": {"fuel": 700, "chemicals": 280},
                "construction_cost": {"materials": 5000, "wealth": 3000},
                "construction_turns": 22,
                "effects": {},
            },
            {
                "workers": 1600,
                "input_goods": {"materials": 1400, "energy": 1600},
                "output_goods": {"fuel": 1050, "chemicals": 420},
                "construction_cost": {"materials": 7500, "wealth": 4500},
                "construction_turns": 30,
                "effects": {},
            },
        ],
    },
    "fuel_depot": {
        "label": "Fuel Depot",
        "category": "refining",
        "description": "Storage and distribution hub that reduces national government upkeep.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"materials": 80},
                "output_goods": {},
                "construction_cost": {"materials": 600, "wealth": 300},
                "construction_turns": 4,
                "effects": {"upkeep_reduction": 0.02},
            },
            {
                "workers": 200,
                "input_goods": {"materials": 150},
                "output_goods": {},
                "construction_cost": {"materials": 1200, "wealth": 600},
                "construction_turns": 8,
                "effects": {"upkeep_reduction": 0.04},
            },
            {
                "workers": 300,
                "input_goods": {"materials": 220},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1000},
                "construction_turns": 12,
                "effects": {"upkeep_reduction": 0.07},
            },
        ],
    },
    "biofuel_plant": {
        "label": "Biofuel Plant",
        "category": "refining",
        "description": "Converts agricultural surplus into fuel and chemicals. Pairs well with farming provinces.",
        "max_level": 3,
        "levels": [
            {
                "workers": 250,
                "input_goods": {"food": 200, "energy": 100},
                "output_goods": {"fuel": 120, "chemicals": 60},
                "construction_cost": {"materials": 1000, "wealth": 600},
                "construction_turns": 8,
                "effects": {},
            },
            {
                "workers": 500,
                "input_goods": {"food": 400, "energy": 200},
                "output_goods": {"fuel": 260, "chemicals": 130},
                "construction_cost": {"materials": 2000, "wealth": 1200},
                "construction_turns": 14,
                "effects": {},
            },
            {
                "workers": 800,
                "input_goods": {"food": 650, "energy": 350},
                "output_goods": {"fuel": 440, "chemicals": 220},
                "construction_cost": {"materials": 3400, "wealth": 2000},
                "construction_turns": 20,
                "effects": {},
            },
        ],
    },

    # ============================================================
    # CHEMICAL
    # ============================================================
    "chemical_plant": {
        "label": "Chemical Plant",
        "category": "chemical",
        "description": "Primary producer of industrial chemicals used in pharmaceuticals, agriculture, and manufacturing.",
        "max_level": 4,
        "levels": [
            {
                "workers": 300,
                "input_goods": {"materials": 300, "energy": 250},
                "output_goods": {"chemicals": 200},
                "construction_cost": {"materials": 1400, "wealth": 800},
                "construction_turns": 10,
                "effects": {},
            },
            {
                "workers": 600,
                "input_goods": {"materials": 600, "energy": 500},
                "output_goods": {"chemicals": 430},
                "construction_cost": {"materials": 2800, "wealth": 1600},
                "construction_turns": 16,
                "effects": {},
            },
            {
                "workers": 950,
                "input_goods": {"materials": 950, "energy": 800},
                "output_goods": {"chemicals": 700},
                "construction_cost": {"materials": 4500, "wealth": 2800},
                "construction_turns": 22,
                "effects": {},
            },
            {
                "workers": 1400,
                "input_goods": {"materials": 1400, "energy": 1200},
                "output_goods": {"chemicals": 1050},
                "construction_cost": {"materials": 6800, "wealth": 4200},
                "construction_turns": 30,
                "effects": {},
            },
        ],
    },
    "fertilizer_plant": {
        "label": "Fertilizer Plant",
        "category": "chemical",
        "description": "Converts chemicals into agricultural fertilizers, significantly boosting province food output.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"chemicals": 100, "energy": 80},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 600},
                "construction_turns": 8,
                "effects": {"farming_bonus": 0.15},
            },
            {
                "workers": 400,
                "input_goods": {"chemicals": 200, "energy": 160},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1200},
                "construction_turns": 14,
                "effects": {"farming_bonus": 0.25},
            },
            {
                "workers": 650,
                "input_goods": {"chemicals": 350, "energy": 280},
                "output_goods": {},
                "construction_cost": {"materials": 3500, "wealth": 2200},
                "construction_turns": 20,
                "effects": {"farming_bonus": 0.35},
            },
        ],
    },
    "plastics_factory": {
        "label": "Plastics Factory",
        "category": "chemical",
        "description": "Converts chemicals into consumer goods and components. A versatile chemicals consumer.",
        "max_level": 3,
        "levels": [
            {
                "workers": 300,
                "input_goods": {"chemicals": 150, "energy": 150},
                "output_goods": {"consumer_goods": 120, "components": 80},
                "construction_cost": {"materials": 1200, "wealth": 700},
                "construction_turns": 9,
                "effects": {},
            },
            {
                "workers": 600,
                "input_goods": {"chemicals": 300, "energy": 300},
                "output_goods": {"consumer_goods": 260, "components": 170},
                "construction_cost": {"materials": 2400, "wealth": 1400},
                "construction_turns": 15,
                "effects": {},
            },
            {
                "workers": 950,
                "input_goods": {"chemicals": 500, "energy": 500},
                "output_goods": {"consumer_goods": 440, "components": 290},
                "construction_cost": {"materials": 4000, "wealth": 2400},
                "construction_turns": 21,
                "effects": {},
            },
        ],
    },

    # ============================================================
    # PHARMACEUTICAL
    # ============================================================
    "pharmaceutical_lab": {
        "label": "Pharmaceutical Lab",
        "category": "pharmaceutical",
        "description": "Produces medicine from chemicals and research. Improves population growth.",
        "max_level": 3,
        "levels": [
            {
                "workers": 150,
                "input_goods": {"chemicals": 100, "research": 50},
                "output_goods": {"medicine": 80},
                "construction_cost": {"materials": 1000, "wealth": 800},
                "construction_turns": 9,
                "effects": {"growth_bonus": 0.001},
            },
            {
                "workers": 300,
                "input_goods": {"chemicals": 200, "research": 100},
                "output_goods": {"medicine": 170},
                "construction_cost": {"materials": 2000, "wealth": 1600},
                "construction_turns": 15,
                "effects": {"growth_bonus": 0.002},
            },
            {
                "workers": 500,
                "input_goods": {"chemicals": 350, "research": 175},
                "output_goods": {"medicine": 290},
                "construction_cost": {"materials": 3500, "wealth": 2800},
                "construction_turns": 21,
                "effects": {"growth_bonus": 0.003},
            },
        ],
    },
    "medical_supply_depot": {
        "label": "Medical Supply Depot",
        "category": "pharmaceutical",
        "description": "Distributes medicine to the province, accelerating stability recovery.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"medicine": 60},
                "output_goods": {},
                "construction_cost": {"materials": 600, "wealth": 500},
                "construction_turns": 5,
                "effects": {"stability_recovery_bonus": 0.10},
            },
            {
                "workers": 200,
                "input_goods": {"medicine": 120},
                "output_goods": {},
                "construction_cost": {"materials": 1200, "wealth": 1000},
                "construction_turns": 9,
                "effects": {"stability_recovery_bonus": 0.20},
            },
            {
                "workers": 350,
                "input_goods": {"medicine": 210},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1800},
                "construction_turns": 14,
                "effects": {"stability_recovery_bonus": 0.30},
            },
        ],
    },
    "research_institute": {
        "label": "Research Institute",
        "category": "pharmaceutical",
        "description": "Advanced research facility that boosts province research output and improves population health.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"wealth": 200, "energy": 100},
                "output_goods": {"research": 100},
                "construction_cost": {"materials": 1200, "wealth": 1000},
                "construction_turns": 10,
                "effects": {"research_bonus": 0.15, "growth_bonus": 0.001},
            },
            {
                "workers": 400,
                "input_goods": {"wealth": 400, "energy": 200},
                "output_goods": {"research": 220},
                "construction_cost": {"materials": 2400, "wealth": 2000},
                "construction_turns": 16,
                "effects": {"research_bonus": 0.30, "growth_bonus": 0.002},
            },
            {
                "workers": 650,
                "input_goods": {"wealth": 650, "energy": 350},
                "output_goods": {"research": 380},
                "construction_cost": {"materials": 4000, "wealth": 3500},
                "construction_turns": 24,
                "effects": {"research_bonus": 0.45, "growth_bonus": 0.003},
            },
        ],
    },

    # ============================================================
    # FARMING
    # ============================================================
    "irrigation_network": {
        "label": "Irrigation Network",
        "category": "farming",
        "description": "Water management infrastructure that significantly boosts province food output.",
        "max_level": 3,
        "levels": [
            {
                "workers": 150,
                "input_goods": {"energy": 100, "materials": 80},
                "output_goods": {},
                "construction_cost": {"materials": 900, "wealth": 400},
                "construction_turns": 8,
                "effects": {"farming_bonus": 0.15},
            },
            {
                "workers": 300,
                "input_goods": {"energy": 200, "materials": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1800, "wealth": 800},
                "construction_turns": 14,
                "effects": {"farming_bonus": 0.25},
            },
            {
                "workers": 500,
                "input_goods": {"energy": 350, "materials": 280},
                "output_goods": {},
                "construction_cost": {"materials": 3200, "wealth": 1500},
                "construction_turns": 20,
                "effects": {"farming_bonus": 0.35},
            },
        ],
    },
    "grain_silo": {
        "label": "Grain Silo",
        "category": "farming",
        "description": "Food storage infrastructure that boosts province stability by guaranteeing food security.",
        "max_level": 3,
        "levels": [
            {
                "workers": 80,
                "input_goods": {"materials": 60},
                "output_goods": {},
                "construction_cost": {"materials": 500, "wealth": 250},
                "construction_turns": 4,
                "effects": {"stability_recovery_bonus": 0.10},
            },
            {
                "workers": 150,
                "input_goods": {"materials": 120},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 500},
                "construction_turns": 7,
                "effects": {"stability_recovery_bonus": 0.20},
            },
            {
                "workers": 250,
                "input_goods": {"materials": 200},
                "output_goods": {},
                "construction_cost": {"materials": 1700, "wealth": 850},
                "construction_turns": 10,
                "effects": {"stability_recovery_bonus": 0.30},
            },
        ],
    },
    "agricultural_station": {
        "label": "Agricultural Station",
        "category": "farming",
        "description": "Research-driven farming improvements that boost food output and population health.",
        "max_level": 3,
        "levels": [
            {
                "workers": 120,
                "input_goods": {"research": 60, "energy": 80},
                "output_goods": {},
                "construction_cost": {"materials": 800, "wealth": 600},
                "construction_turns": 8,
                "effects": {"farming_bonus": 0.10, "growth_bonus": 0.001},
            },
            {
                "workers": 240,
                "input_goods": {"research": 120, "energy": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1600, "wealth": 1200},
                "construction_turns": 14,
                "effects": {"farming_bonus": 0.20, "growth_bonus": 0.002},
            },
            {
                "workers": 400,
                "input_goods": {"research": 200, "energy": 280},
                "output_goods": {},
                "construction_cost": {"materials": 2800, "wealth": 2200},
                "construction_turns": 20,
                "effects": {"farming_bonus": 0.30, "growth_bonus": 0.003},
            },
        ],
    },

    # ============================================================
    # EXTRACTION
    # ============================================================
    "mine": {
        "label": "Mine",
        "category": "extraction",
        "description": "Deep extraction operation producing large quantities of raw materials.",
        "max_level": 4,
        "levels": [
            {
                "workers": 400,
                "input_goods": {"energy": 200, "heavy_equipment": 80},
                "output_goods": {"materials": 400},
                "construction_cost": {"materials": 1500, "wealth": 800},
                "construction_turns": 10,
                "effects": {},
            },
            {
                "workers": 800,
                "input_goods": {"energy": 400, "heavy_equipment": 160},
                "output_goods": {"materials": 850},
                "construction_cost": {"materials": 3000, "wealth": 1600},
                "construction_turns": 16,
                "effects": {},
            },
            {
                "workers": 1200,
                "input_goods": {"energy": 650, "heavy_equipment": 260},
                "output_goods": {"materials": 1400},
                "construction_cost": {"materials": 5000, "wealth": 2800},
                "construction_turns": 22,
                "effects": {},
            },
            {
                "workers": 1800,
                "input_goods": {"energy": 1000, "heavy_equipment": 400},
                "output_goods": {"materials": 2200},
                "construction_cost": {"materials": 7500, "wealth": 4200},
                "construction_turns": 30,
                "effects": {},
            },
        ],
    },
    "oil_well": {
        "label": "Oil Well",
        "category": "extraction",
        "description": "Extracts petroleum, producing fuel and raw materials as a byproduct.",
        "max_level": 3,
        "levels": [
            {
                "workers": 300,
                "input_goods": {"energy": 150, "heavy_equipment": 60},
                "output_goods": {"fuel": 250, "materials": 80},
                "construction_cost": {"materials": 1300, "wealth": 700},
                "construction_turns": 9,
                "effects": {},
            },
            {
                "workers": 600,
                "input_goods": {"energy": 300, "heavy_equipment": 120},
                "output_goods": {"fuel": 540, "materials": 170},
                "construction_cost": {"materials": 2600, "wealth": 1400},
                "construction_turns": 15,
                "effects": {},
            },
            {
                "workers": 1000,
                "input_goods": {"energy": 500, "heavy_equipment": 200},
                "output_goods": {"fuel": 900, "materials": 280},
                "construction_cost": {"materials": 4400, "wealth": 2400},
                "construction_turns": 22,
                "effects": {},
            },
        ],
    },
    "logging_camp": {
        "label": "Logging Camp",
        "category": "extraction",
        "description": "Low-tech forest extraction producing materials and food. Accessible in the early rebuilding era.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"manpower": 100},
                "output_goods": {"materials": 180, "food": 60},
                "construction_cost": {"materials": 500, "wealth": 250},
                "construction_turns": 4,
                "effects": {},
            },
            {
                "workers": 400,
                "input_goods": {"manpower": 200},
                "output_goods": {"materials": 380, "food": 130},
                "construction_cost": {"materials": 1000, "wealth": 500},
                "construction_turns": 7,
                "effects": {},
            },
            {
                "workers": 650,
                "input_goods": {"manpower": 350},
                "output_goods": {"materials": 640, "food": 220},
                "construction_cost": {"materials": 1700, "wealth": 850},
                "construction_turns": 11,
                "effects": {},
            },
        ],
    },

    # ============================================================
    # CONSTRUCTION
    # ============================================================
    "construction_yard": {
        "label": "Construction Yard",
        "category": "construction",
        "description": "Organises local construction capacity, reducing build times for province buildings.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"materials": 150, "heavy_equipment": 50},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 500},
                "construction_turns": 8,
                "effects": {"construction_time_reduction": 0.10},
            },
            {
                "workers": 400,
                "input_goods": {"materials": 300, "heavy_equipment": 100},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1000},
                "construction_turns": 14,
                "effects": {"construction_time_reduction": 0.20},
            },
            {
                "workers": 650,
                "input_goods": {"materials": 500, "heavy_equipment": 175},
                "output_goods": {},
                "construction_cost": {"materials": 3500, "wealth": 1750},
                "construction_turns": 20,
                "effects": {"construction_time_reduction": 0.30},
            },
        ],
    },
    "cement_plant": {
        "label": "Cement Plant",
        "category": "construction",
        "description": "Produces construction-grade components from raw materials and energy.",
        "max_level": 3,
        "levels": [
            {
                "workers": 250,
                "input_goods": {"materials": 300, "energy": 200},
                "output_goods": {"components": 200},
                "construction_cost": {"materials": 1100, "wealth": 600},
                "construction_turns": 8,
                "effects": {},
            },
            {
                "workers": 500,
                "input_goods": {"materials": 600, "energy": 400},
                "output_goods": {"components": 430},
                "construction_cost": {"materials": 2200, "wealth": 1200},
                "construction_turns": 14,
                "effects": {},
            },
            {
                "workers": 800,
                "input_goods": {"materials": 950, "energy": 650},
                "output_goods": {"components": 700},
                "construction_cost": {"materials": 3700, "wealth": 2000},
                "construction_turns": 20,
                "effects": {},
            },
        ],
    },
    "infrastructure_bureau": {
        "label": "Infrastructure Bureau",
        "category": "construction",
        "description": "Administrative hub improving province integration and reducing construction costs nationwide.",
        "max_level": 3,
        "levels": [
            {
                "workers": 150,
                "input_goods": {"wealth": 150, "research": 50},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 800},
                "construction_turns": 9,
                "effects": {"integration_bonus": 0.05, "construction_cost_reduction": 0.04},
            },
            {
                "workers": 300,
                "input_goods": {"wealth": 300, "research": 100},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1600},
                "construction_turns": 15,
                "effects": {"integration_bonus": 0.10, "construction_cost_reduction": 0.08},
            },
            {
                "workers": 500,
                "input_goods": {"wealth": 500, "research": 175},
                "output_goods": {},
                "construction_cost": {"materials": 3500, "wealth": 2800},
                "construction_turns": 21,
                "effects": {"integration_bonus": 0.15, "construction_cost_reduction": 0.12},
            },
        ],
    },

    # ============================================================
    # TRANSPORT
    # ============================================================
    "road_network": {
        "label": "Road Network",
        "category": "transport",
        "description": "Paved road infrastructure that improves how efficiently province surplus reaches the national pool.",
        "max_level": 3,
        "levels": [
            {
                "workers": 150,
                "input_goods": {"materials": 150, "fuel": 50},
                "output_goods": {},
                "construction_cost": {"materials": 1200, "wealth": 500},
                "construction_turns": 9,
                "effects": {"integration_bonus": 0.05, "march_speed_bonus": 0.05},
            },
            {
                "workers": 300,
                "input_goods": {"materials": 300, "fuel": 100},
                "output_goods": {},
                "construction_cost": {"materials": 2400, "wealth": 1000},
                "construction_turns": 15,
                "effects": {"integration_bonus": 0.10, "march_speed_bonus": 0.10},
            },
            {
                "workers": 500,
                "input_goods": {"materials": 500, "fuel": 170},
                "output_goods": {},
                "construction_cost": {"materials": 4000, "wealth": 1800},
                "construction_turns": 21,
                "effects": {"integration_bonus": 0.15, "march_speed_bonus": 0.15},
            },
        ],
    },
    "railway_station": {
        "label": "Railway Station",
        "category": "transport",
        "description": "Rail infrastructure that dramatically improves integration and speeds up provincial construction.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"materials": 200, "energy": 150, "heavy_equipment": 80},
                "output_goods": {},
                "construction_cost": {"materials": 2500, "wealth": 1200},
                "construction_turns": 15,
                "effects": {"integration_bonus": 0.08, "construction_time_reduction": 0.05, "march_speed_bonus": 0.10},
            },
            {
                "workers": 400,
                "input_goods": {"materials": 400, "energy": 300, "heavy_equipment": 160},
                "output_goods": {},
                "construction_cost": {"materials": 5000, "wealth": 2400},
                "construction_turns": 24,
                "effects": {"integration_bonus": 0.15, "construction_time_reduction": 0.10, "march_speed_bonus": 0.20},
            },
            {
                "workers": 650,
                "input_goods": {"materials": 650, "energy": 500, "heavy_equipment": 260},
                "output_goods": {},
                "construction_cost": {"materials": 8500, "wealth": 4000},
                "construction_turns": 36,
                "effects": {"integration_bonus": 0.22, "construction_time_reduction": 0.15, "march_speed_bonus": 0.30},
            },
        ],
    },
    "logistics_hub": {
        "label": "Logistics Hub",
        "category": "transport",
        "description": "Centralised distribution network improving province integration and reducing national upkeep.",
        "max_level": 3,
        "levels": [
            {
                "workers": 175,
                "input_goods": {"wealth": 150, "fuel": 80},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 700},
                "construction_turns": 8,
                "effects": {"integration_bonus": 0.04, "upkeep_reduction": 0.02, "march_speed_bonus": 0.03, "river_transit_speed": 0.03},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 300, "fuel": 160},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1400},
                "construction_turns": 14,
                "effects": {"integration_bonus": 0.08, "upkeep_reduction": 0.04, "march_speed_bonus": 0.05, "river_transit_speed": 0.05},
            },
            {
                "workers": 575,
                "input_goods": {"wealth": 500, "fuel": 270},
                "output_goods": {},
                "construction_cost": {"materials": 3400, "wealth": 2400},
                "construction_turns": 20,
                "effects": {"integration_bonus": 0.12, "upkeep_reduction": 0.06, "march_speed_bonus": 0.08, "river_transit_speed": 0.08},
            },
        ],
    },

    "dock": {
        "label": "Dock",
        "category": "transport",
        "description": (
            "Port infrastructure enabling naval access. Required for province↔sea zone movement. "
            "Reduces transition time from this province to adjacent sea and river zones."
        ),
        "max_level": 3,
        "levels": [
            {"workers": 200, "input_goods": {"materials": 180, "fuel": 60},  "output_goods": {},
             "construction_cost": {"materials": 1800, "wealth": 900},  "construction_turns": 12,
             "effects": {"sea_transit_speed": 0.25, "river_transit_speed": 0.15}},
            {"workers": 400, "input_goods": {"materials": 360, "fuel": 120}, "output_goods": {},
             "construction_cost": {"materials": 3600, "wealth": 1800}, "construction_turns": 20,
             "effects": {"sea_transit_speed": 0.50, "river_transit_speed": 0.30}},
            {"workers": 650, "input_goods": {"materials": 600, "fuel": 200}, "output_goods": {},
             "construction_cost": {"materials": 6000, "wealth": 3000}, "construction_turns": 30,
             "effects": {"sea_transit_speed": 1.00, "river_transit_speed": 0.50}},
        ],
    },
    "port": {
        "label": "Port",
        "category": "transport",
        "description": "Commercial harbour for naval trade. Generates naval trade capacity and speeds sea access.",
        "max_level": 3,
        "levels": [
            {"workers": 300, "input_goods": {"materials": 200, "fuel": 80}, "output_goods": {},
             "construction_cost": {"materials": 2500, "wealth": 1200}, "construction_turns": 15,
             "effects": {"naval_trade_capacity": 50, "sea_transit_speed": 0.10}},
            {"workers": 600, "input_goods": {"materials": 400, "fuel": 160}, "output_goods": {},
             "construction_cost": {"materials": 5000, "wealth": 2400}, "construction_turns": 25,
             "effects": {"naval_trade_capacity": 120, "sea_transit_speed": 0.20}},
            {"workers": 1000, "input_goods": {"materials": 700, "fuel": 270}, "output_goods": {},
             "construction_cost": {"materials": 8500, "wealth": 4000}, "construction_turns": 38,
             "effects": {"naval_trade_capacity": 250, "sea_transit_speed": 0.35}},
        ],
    },
    "bridge": {
        "label": "Bridge",
        "category": "transport",
        "description": "River crossing enabling movement and trade across river zones.",
        "max_level": 3,
        "levels": [
            {"workers": 150, "input_goods": {"materials": 150}, "output_goods": {},
             "construction_cost": {"materials": 1000, "wealth": 400}, "construction_turns": 8,
             "effects": {"land_trade_capacity": 30, "river_transit_speed": 0.20}},
            {"workers": 300, "input_goods": {"materials": 300}, "output_goods": {},
             "construction_cost": {"materials": 2000, "wealth": 800}, "construction_turns": 14,
             "effects": {"land_trade_capacity": 70, "river_transit_speed": 0.40}},
            {"workers": 500, "input_goods": {"materials": 500}, "output_goods": {},
             "construction_cost": {"materials": 3500, "wealth": 1400}, "construction_turns": 22,
             "effects": {"land_trade_capacity": 150, "river_transit_speed": 0.60}},
        ],
    },
    "railroad": {
        "label": "Railroad",
        "category": "transport",
        "description": "Rail track infrastructure connecting provinces. Improves march speed and land trade capacity.",
        "max_level": 3,
        "levels": [
            {"workers": 400, "input_goods": {"materials": 300, "heavy_equipment": 50, "fuel": 80}, "output_goods": {},
             "construction_cost": {"materials": 3000, "wealth": 1500}, "construction_turns": 18,
             "effects": {"march_speed_bonus": 0.15, "land_trade_capacity": 60}},
            {"workers": 800, "input_goods": {"materials": 600, "heavy_equipment": 100, "fuel": 160}, "output_goods": {},
             "construction_cost": {"materials": 6000, "wealth": 3000}, "construction_turns": 30,
             "effects": {"march_speed_bonus": 0.30, "land_trade_capacity": 140}},
            {"workers": 1300, "input_goods": {"materials": 1000, "heavy_equipment": 180, "fuel": 270}, "output_goods": {},
             "construction_cost": {"materials": 10000, "wealth": 5000}, "construction_turns": 45,
             "effects": {"march_speed_bonus": 0.50, "land_trade_capacity": 280}},
        ],
    },
    "train_depot": {
        "label": "Train Depot",
        "category": "transport",
        "description": "Rail freight depot. Increases land trade capacity and national march speed.",
        "max_level": 3,
        "levels": [
            {"workers": 200, "input_goods": {"materials": 150, "fuel": 100}, "output_goods": {},
             "construction_cost": {"materials": 1500, "wealth": 700}, "construction_turns": 10,
             "effects": {"land_trade_capacity": 40, "march_speed_bonus": 0.05}},
            {"workers": 400, "input_goods": {"materials": 300, "fuel": 200}, "output_goods": {},
             "construction_cost": {"materials": 3000, "wealth": 1400}, "construction_turns": 18,
             "effects": {"land_trade_capacity": 90, "march_speed_bonus": 0.10}},
            {"workers": 650, "input_goods": {"materials": 500, "fuel": 340}, "output_goods": {},
             "construction_cost": {"materials": 5000, "wealth": 2400}, "construction_turns": 28,
             "effects": {"land_trade_capacity": 180, "march_speed_bonus": 0.15}},
        ],
    },
    "train_station": {
        "label": "Train Station",
        "category": "transport",
        "description": "Rail passenger station. Speeds troop movement through this province.",
        "max_level": 3,
        "levels": [
            {"workers": 250, "input_goods": {"materials": 180, "energy": 100}, "output_goods": {},
             "construction_cost": {"materials": 2000, "wealth": 1000}, "construction_turns": 12,
             "effects": {"march_speed_bonus": 0.10, "land_trade_capacity": 50}},
            {"workers": 500, "input_goods": {"materials": 360, "energy": 200}, "output_goods": {},
             "construction_cost": {"materials": 4000, "wealth": 2000}, "construction_turns": 20,
             "effects": {"march_speed_bonus": 0.20, "land_trade_capacity": 110}},
            {"workers": 800, "input_goods": {"materials": 600, "energy": 340}, "output_goods": {},
             "construction_cost": {"materials": 7000, "wealth": 3500}, "construction_turns": 32,
             "effects": {"march_speed_bonus": 0.30, "land_trade_capacity": 220}},
        ],
    },
    "train_cargo_terminal": {
        "label": "Train Cargo Terminal",
        "category": "transport",
        "description": "Rail bulk cargo terminal. Large land trade capacity.",
        "max_level": 3,
        "levels": [
            {"workers": 350, "input_goods": {"materials": 250, "fuel": 120}, "output_goods": {},
             "construction_cost": {"materials": 2500, "wealth": 1200}, "construction_turns": 14,
             "effects": {"land_trade_capacity": 80}},
            {"workers": 700, "input_goods": {"materials": 500, "fuel": 240}, "output_goods": {},
             "construction_cost": {"materials": 5000, "wealth": 2400}, "construction_turns": 24,
             "effects": {"land_trade_capacity": 190}},
            {"workers": 1100, "input_goods": {"materials": 850, "fuel": 400}, "output_goods": {},
             "construction_cost": {"materials": 8500, "wealth": 4000}, "construction_turns": 36,
             "effects": {"land_trade_capacity": 380}},
        ],
    },
    "airport": {
        "label": "Airport",
        "category": "transport",
        "description": "Civilian air terminal. Enables civilian air zone access and generates air trade capacity.",
        "max_level": 3,
        "levels": [
            {"workers": 300, "input_goods": {"materials": 200, "energy": 150, "fuel": 100}, "output_goods": {},
             "construction_cost": {"materials": 3000, "wealth": 1800}, "construction_turns": 16,
             "effects": {"air_transit_speed": 0.15, "air_trade_capacity": 40}},
            {"workers": 600, "input_goods": {"materials": 400, "energy": 300, "fuel": 200}, "output_goods": {},
             "construction_cost": {"materials": 6000, "wealth": 3600}, "construction_turns": 26,
             "effects": {"air_transit_speed": 0.30, "air_trade_capacity": 100}},
            {"workers": 1000, "input_goods": {"materials": 700, "energy": 500, "fuel": 340}, "output_goods": {},
             "construction_cost": {"materials": 10000, "wealth": 6000}, "construction_turns": 40,
             "effects": {"air_transit_speed": 0.50, "air_trade_capacity": 200}},
        ],
    },
    "air_cargo_terminal": {
        "label": "Air Cargo Terminal",
        "category": "transport",
        "description": "Air freight facility. Generates large air trade capacity.",
        "max_level": 3,
        "levels": [
            {"workers": 250, "input_goods": {"materials": 180, "fuel": 150}, "output_goods": {},
             "construction_cost": {"materials": 2500, "wealth": 1500}, "construction_turns": 13,
             "effects": {"air_trade_capacity": 60}},
            {"workers": 500, "input_goods": {"materials": 360, "fuel": 300}, "output_goods": {},
             "construction_cost": {"materials": 5000, "wealth": 3000}, "construction_turns": 22,
             "effects": {"air_trade_capacity": 140}},
            {"workers": 800, "input_goods": {"materials": 600, "fuel": 500}, "output_goods": {},
             "construction_cost": {"materials": 8500, "wealth": 5000}, "construction_turns": 34,
             "effects": {"air_trade_capacity": 280}},
        ],
    },

    # ============================================================
    # COMMUNICATIONS
    # ============================================================
    "radio_tower": {
        "label": "Radio Tower",
        "category": "communications",
        "description": "Broadcasts information and morale messages, improving province stability recovery.",
        "max_level": 3,
        "levels": [
            {
                "workers": 80,
                "input_goods": {"materials": 60, "energy": 80},
                "output_goods": {},
                "construction_cost": {"materials": 700, "wealth": 400},
                "construction_turns": 5,
                "effects": {"stability_recovery_bonus": 0.10},
            },
            {
                "workers": 150,
                "input_goods": {"materials": 120, "energy": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1400, "wealth": 800},
                "construction_turns": 9,
                "effects": {"stability_recovery_bonus": 0.20},
            },
            {
                "workers": 250,
                "input_goods": {"materials": 200, "energy": 280},
                "output_goods": {},
                "construction_cost": {"materials": 2400, "wealth": 1400},
                "construction_turns": 14,
                "effects": {"stability_recovery_bonus": 0.30},
            },
        ],
    },
    "telegraph_network": {
        "label": "Telegraph Network",
        "category": "communications",
        "description": "Rapid information exchange that boosts research output and province stability.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 100, "energy": 80},
                "output_goods": {},
                "construction_cost": {"materials": 800, "wealth": 600},
                "construction_turns": 6,
                "effects": {"research_bonus": 0.10, "stability_recovery_bonus": 0.08},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 200, "energy": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1600, "wealth": 1200},
                "construction_turns": 11,
                "effects": {"research_bonus": 0.20, "stability_recovery_bonus": 0.15},
            },
            {
                "workers": 330,
                "input_goods": {"wealth": 330, "energy": 280},
                "output_goods": {},
                "construction_cost": {"materials": 2800, "wealth": 2200},
                "construction_turns": 17,
                "effects": {"research_bonus": 0.30, "stability_recovery_bonus": 0.22},
            },
        ],
    },
    "broadcasting_station": {
        "label": "Broadcasting Station",
        "category": "communications",
        "description": "High-power media broadcast that significantly improves province morale and stability recovery.",
        "max_level": 3,
        "levels": [
            {
                "workers": 120,
                "input_goods": {"energy": 150, "wealth": 100},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 700},
                "construction_turns": 7,
                "effects": {"stability_recovery_bonus": 0.15},
            },
            {
                "workers": 250,
                "input_goods": {"energy": 300, "wealth": 200},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1400},
                "construction_turns": 12,
                "effects": {"stability_recovery_bonus": 0.30},
            },
            {
                "workers": 400,
                "input_goods": {"energy": 500, "wealth": 350},
                "output_goods": {},
                "construction_cost": {"materials": 3500, "wealth": 2500},
                "construction_turns": 18,
                "effects": {"stability_recovery_bonus": 0.45},
            },
        ],
    },

    # ============================================================
    # ENTERTAINMENT / TOURISM
    # ============================================================
    "tavern": {
        "label": "Tavern",
        "category": "entertainment",
        "description": "A public gathering place providing modest stability benefits at low cost.",
        "max_level": 3,
        "levels": [
            {
                "workers": 60,
                "input_goods": {"food": 100, "wealth": 60},
                "output_goods": {},
                "construction_cost": {"materials": 300, "wealth": 200},
                "construction_turns": 3,
                "effects": {"stability_recovery_bonus": 0.08},
            },
            {
                "workers": 120,
                "input_goods": {"food": 200, "wealth": 120},
                "output_goods": {},
                "construction_cost": {"materials": 600, "wealth": 400},
                "construction_turns": 5,
                "effects": {"stability_recovery_bonus": 0.15},
            },
            {
                "workers": 200,
                "input_goods": {"food": 320, "wealth": 200},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 700},
                "construction_turns": 8,
                "effects": {"stability_recovery_bonus": 0.22},
            },
        ],
    },
    "theatre": {
        "label": "Theatre",
        "category": "entertainment",
        "description": "Cultural venue that improves stability and attracts population growth.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 150},
                "output_goods": {},
                "construction_cost": {"materials": 700, "wealth": 500},
                "construction_turns": 6,
                "effects": {"stability_recovery_bonus": 0.12, "growth_bonus": 0.001},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 300},
                "output_goods": {},
                "construction_cost": {"materials": 1400, "wealth": 1000},
                "construction_turns": 10,
                "effects": {"stability_recovery_bonus": 0.22, "growth_bonus": 0.002},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 500},
                "output_goods": {},
                "construction_cost": {"materials": 2500, "wealth": 1800},
                "construction_turns": 15,
                "effects": {"stability_recovery_bonus": 0.32, "growth_bonus": 0.003},
            },
        ],
    },
    "resort": {
        "label": "Resort",
        "category": "entertainment",
        "description": "Tourism destination that generates trade capacity and improves province stability.",
        "max_level": 3,
        "levels": [
            {
                "workers": 250,
                "input_goods": {"wealth": 200, "consumer_goods": 100, "fuel": 60},
                "output_goods": {},
                "construction_cost": {"materials": 1200, "wealth": 1000},
                "construction_turns": 10,
                "effects": {"stability_recovery_bonus": 0.15, "trade_capacity": 280},
            },
            {
                "workers": 500,
                "input_goods": {"wealth": 400, "consumer_goods": 200, "fuel": 120},
                "output_goods": {},
                "construction_cost": {"materials": 2400, "wealth": 2000},
                "construction_turns": 16,
                "effects": {"stability_recovery_bonus": 0.28, "trade_capacity": 580},
            },
            {
                "workers": 800,
                "input_goods": {"wealth": 650, "consumer_goods": 340, "fuel": 200},
                "output_goods": {},
                "construction_cost": {"materials": 4000, "wealth": 3500},
                "construction_turns": 24,
                "effects": {"stability_recovery_bonus": 0.40, "trade_capacity": 950},
            },
        ],
    },

    # ============================================================
    # HEALTHCARE
    # ============================================================
    "clinic": {
        "label": "Clinic",
        "category": "healthcare",
        "description": "Basic medical facility improving population health, growth, and stability.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"medicine": 50, "wealth": 80},
                "output_goods": {},
                "construction_cost": {"materials": 700, "wealth": 500},
                "construction_turns": 6,
                "effects": {"growth_bonus": 0.001, "stability_recovery_bonus": 0.08},
            },
            {
                "workers": 200,
                "input_goods": {"medicine": 100, "wealth": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1400, "wealth": 1000},
                "construction_turns": 10,
                "effects": {"growth_bonus": 0.002, "stability_recovery_bonus": 0.15},
            },
            {
                "workers": 350,
                "input_goods": {"medicine": 175, "wealth": 280},
                "output_goods": {},
                "construction_cost": {"materials": 2500, "wealth": 1800},
                "construction_turns": 15,
                "effects": {"growth_bonus": 0.003, "stability_recovery_bonus": 0.22},
            },
        ],
    },
    "hospital": {
        "label": "Hospital",
        "category": "healthcare",
        "description": "Full medical facility that significantly boosts population growth through advanced healthcare.",
        "max_level": 3,
        "levels": [
            {
                "workers": 350,
                "input_goods": {"medicine": 120, "energy": 100, "wealth": 150},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1500},
                "construction_turns": 14,
                "effects": {"growth_bonus": 0.002},
            },
            {
                "workers": 700,
                "input_goods": {"medicine": 250, "energy": 200, "wealth": 300},
                "output_goods": {},
                "construction_cost": {"materials": 4000, "wealth": 3000},
                "construction_turns": 22,
                "effects": {"growth_bonus": 0.004},
            },
            {
                "workers": 1100,
                "input_goods": {"medicine": 420, "energy": 350, "wealth": 500},
                "output_goods": {},
                "construction_cost": {"materials": 6500, "wealth": 5000},
                "construction_turns": 30,
                "effects": {"growth_bonus": 0.006},
            },
        ],
    },
    "sanitation_works": {
        "label": "Sanitation Works",
        "category": "healthcare",
        "description": "Public health infrastructure that improves population growth through disease prevention.",
        "max_level": 3,
        "levels": [
            {
                "workers": 150,
                "input_goods": {"materials": 120, "energy": 80},
                "output_goods": {},
                "construction_cost": {"materials": 800, "wealth": 400},
                "construction_turns": 7,
                "effects": {"growth_bonus": 0.001},
            },
            {
                "workers": 300,
                "input_goods": {"materials": 250, "energy": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1600, "wealth": 800},
                "construction_turns": 12,
                "effects": {"growth_bonus": 0.002},
            },
            {
                "workers": 500,
                "input_goods": {"materials": 420, "energy": 280},
                "output_goods": {},
                "construction_cost": {"materials": 2800, "wealth": 1400},
                "construction_turns": 18,
                "effects": {"growth_bonus": 0.003},
            },
        ],
    },

    # ============================================================
    # RELIGIOUS
    # ============================================================
    "church": {
        "label": "Church",
        "category": "religious",
        "description": "Centre of community and administration. Provides the largest bureaucratic capacity bonus of any religious building.",
        "max_level": 3,
        "levels": [
            {
                "workers": 80,
                "input_goods": {"wealth": 60},
                "output_goods": {},
                "construction_cost": {"materials": 500, "wealth": 300},
                "construction_turns": 5,
                "effects": {"bureaucratic_capacity": 15, "stability_recovery_bonus": 0.05, "literacy_bonus": 0.03},
            },
            {
                "workers": 160,
                "input_goods": {"wealth": 120},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 600},
                "construction_turns": 9,
                "effects": {"bureaucratic_capacity": 35, "stability_recovery_bonus": 0.10, "literacy_bonus": 0.06},
            },
            {
                "workers": 280,
                "input_goods": {"wealth": 200},
                "output_goods": {},
                "construction_cost": {"materials": 1800, "wealth": 1100},
                "construction_turns": 14,
                "effects": {"bureaucratic_capacity": 60, "stability_recovery_bonus": 0.15, "literacy_bonus": 0.09},
            },
        ],
    },
    "madrasa": {
        "label": "Madrasa",
        "category": "religious",
        "description": "Religious school combining spiritual teaching with practical education. Provides the largest literacy bonus of any religious building.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 80, "research": 30},
                "output_goods": {},
                "construction_cost": {"materials": 600, "wealth": 400},
                "construction_turns": 6,
                "effects": {"literacy_bonus": 0.10, "research_bonus": 0.08, "bureaucratic_capacity": 8},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 160, "research": 60},
                "output_goods": {},
                "construction_cost": {"materials": 1200, "wealth": 800},
                "construction_turns": 10,
                "effects": {"literacy_bonus": 0.20, "research_bonus": 0.15, "bureaucratic_capacity": 18},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 280, "research": 100},
                "output_goods": {},
                "construction_cost": {"materials": 2200, "wealth": 1500},
                "construction_turns": 16,
                "effects": {"literacy_bonus": 0.30, "research_bonus": 0.22, "bureaucratic_capacity": 30},
            },
        ],
    },
    "holy_site": {
        "label": "Holy Site",
        "category": "religious",
        "description": "Sacred pilgrimage destination that inspires devotion and unity. Provides the largest stability bonus of any religious building.",
        "max_level": 3,
        "levels": [
            {
                "workers": 60,
                "input_goods": {"wealth": 80},
                "output_goods": {},
                "construction_cost": {"materials": 700, "wealth": 500},
                "construction_turns": 8,
                "effects": {"stability_recovery_bonus": 0.20, "growth_bonus": 0.001, "bureaucratic_capacity": 5},
            },
            {
                "workers": 120,
                "input_goods": {"wealth": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1400, "wealth": 1000},
                "construction_turns": 14,
                "effects": {"stability_recovery_bonus": 0.40, "growth_bonus": 0.002, "bureaucratic_capacity": 12},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 280},
                "output_goods": {},
                "construction_cost": {"materials": 2500, "wealth": 1800},
                "construction_turns": 20,
                "effects": {"stability_recovery_bonus": 0.60, "growth_bonus": 0.003, "bureaucratic_capacity": 20},
            },
        ],
    },

    # ============================================================
    # GREEN ENERGY
    # Renewable alternatives to fossil-fuel energy. Less output per
    # building but fewer workers, allowing more to be built.
    # Essential for Ecologist nations (who cannot build oil_well,
    # refinery, advanced_refinery, or fuel_depot).
    # ============================================================
    "wind_farm": {
        "label": "Wind Farm",
        "category": "green_energy",
        "description": "Turbine array generating clean energy from wind. Low worker cost allows multiple installations.",
        "max_level": 3,
        "levels": [
            {
                "workers": 60,
                "input_goods": {"materials": 40},
                "output_goods": {"energy": 100},
                "construction_cost": {"materials": 600, "wealth": 300},
                "construction_turns": 5,
                "effects": {},
            },
            {
                "workers": 120,
                "input_goods": {"materials": 80},
                "output_goods": {"energy": 220},
                "construction_cost": {"materials": 1200, "wealth": 600},
                "construction_turns": 9,
                "effects": {},
            },
            {
                "workers": 200,
                "input_goods": {"materials": 140},
                "output_goods": {"energy": 380},
                "construction_cost": {"materials": 2000, "wealth": 1000},
                "construction_turns": 14,
                "effects": {},
            },
        ],
    },
    "solar_array": {
        "label": "Solar Array",
        "category": "green_energy",
        "description": "Photovoltaic panel installation producing clean energy. Higher output than wind but needs more components.",
        "max_level": 3,
        "levels": [
            {
                "workers": 80,
                "input_goods": {"materials": 50, "components": 30},
                "output_goods": {"energy": 130},
                "construction_cost": {"materials": 800, "wealth": 500},
                "construction_turns": 6,
                "effects": {},
            },
            {
                "workers": 160,
                "input_goods": {"materials": 100, "components": 60},
                "output_goods": {"energy": 280},
                "construction_cost": {"materials": 1600, "wealth": 1000},
                "construction_turns": 10,
                "effects": {},
            },
            {
                "workers": 260,
                "input_goods": {"materials": 170, "components": 100},
                "output_goods": {"energy": 480},
                "construction_cost": {"materials": 2800, "wealth": 1800},
                "construction_turns": 16,
                "effects": {},
            },
        ],
    },
    "hydroelectric_dam": {
        "label": "Hydroelectric Dam",
        "category": "green_energy",
        "description": "Large-scale water-powered generator. Highest green energy output but significant construction investment.",
        "max_level": 3,
        "levels": [
            {
                "workers": 120,
                "input_goods": {"materials": 80, "heavy_equipment": 40},
                "output_goods": {"energy": 200},
                "construction_cost": {"materials": 1500, "wealth": 800},
                "construction_turns": 10,
                "effects": {},
            },
            {
                "workers": 240,
                "input_goods": {"materials": 160, "heavy_equipment": 80},
                "output_goods": {"energy": 430},
                "construction_cost": {"materials": 3000, "wealth": 1600},
                "construction_turns": 16,
                "effects": {},
            },
            {
                "workers": 400,
                "input_goods": {"materials": 280, "heavy_equipment": 140},
                "output_goods": {"energy": 720},
                "construction_cost": {"materials": 5000, "wealth": 2800},
                "construction_turns": 24,
                "effects": {},
            },
        ],
    },

    # ============================================================
    # GOVERNMENT — REGULATORY
    # Affects economic regulation policies. Improves integration
    # (how efficiently province output reaches national pool).
    # ============================================================
    "regulatory_office": {
        "label": "Regulatory Office",
        "category": "government_regulatory",
        "description": "Establishes trade standards and market rules, improving province integration efficiency.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 80},
                "output_goods": {},
                "construction_cost": {"materials": 500, "wealth": 400},
                "construction_turns": 5,
                "effects": {"integration_bonus": 0.04, "bureaucratic_capacity": 10},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 800},
                "construction_turns": 9,
                "effects": {"integration_bonus": 0.08, "bureaucratic_capacity": 22},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 280},
                "output_goods": {},
                "construction_cost": {"materials": 1800, "wealth": 1400},
                "construction_turns": 14,
                "effects": {"integration_bonus": 0.12, "bureaucratic_capacity": 38},
            },
        ],
    },
    "standards_bureau": {
        "label": "Standards Bureau",
        "category": "government_regulatory",
        "description": "Sets quality and safety standards for industry, reducing construction costs through standardised practices.",
        "max_level": 3,
        "levels": [
            {
                "workers": 120,
                "input_goods": {"wealth": 100, "research": 30},
                "output_goods": {},
                "construction_cost": {"materials": 600, "wealth": 500},
                "construction_turns": 6,
                "effects": {"construction_cost_reduction": 0.03, "bureaucratic_capacity": 12},
            },
            {
                "workers": 240,
                "input_goods": {"wealth": 200, "research": 60},
                "output_goods": {},
                "construction_cost": {"materials": 1200, "wealth": 1000},
                "construction_turns": 10,
                "effects": {"construction_cost_reduction": 0.06, "bureaucratic_capacity": 25},
            },
            {
                "workers": 400,
                "input_goods": {"wealth": 340, "research": 100},
                "output_goods": {},
                "construction_cost": {"materials": 2200, "wealth": 1800},
                "construction_turns": 16,
                "effects": {"construction_cost_reduction": 0.10, "bureaucratic_capacity": 42},
            },
        ],
    },

    # ============================================================
    # GOVERNMENT — OVERSIGHT
    # Affects accountability/anti-corruption policies. Reduces
    # government upkeep through efficiency and waste reduction.
    # ============================================================
    "inspector_general": {
        "label": "Inspector General",
        "category": "government_oversight",
        "description": "Anti-corruption and accountability office that reduces government waste and upkeep costs.",
        "max_level": 3,
        "levels": [
            {
                "workers": 80,
                "input_goods": {"wealth": 60},
                "output_goods": {},
                "construction_cost": {"materials": 400, "wealth": 350},
                "construction_turns": 4,
                "effects": {"upkeep_reduction": 0.03, "bureaucratic_capacity": 8},
            },
            {
                "workers": 160,
                "input_goods": {"wealth": 120},
                "output_goods": {},
                "construction_cost": {"materials": 800, "wealth": 700},
                "construction_turns": 8,
                "effects": {"upkeep_reduction": 0.06, "bureaucratic_capacity": 18},
            },
            {
                "workers": 280,
                "input_goods": {"wealth": 210},
                "output_goods": {},
                "construction_cost": {"materials": 1500, "wealth": 1200},
                "construction_turns": 13,
                "effects": {"upkeep_reduction": 0.10, "bureaucratic_capacity": 32},
            },
        ],
    },
    "audit_commission": {
        "label": "Audit Commission",
        "category": "government_oversight",
        "description": "Financial oversight body that improves integration efficiency through transparent accounting.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 80, "research": 20},
                "output_goods": {},
                "construction_cost": {"materials": 500, "wealth": 450},
                "construction_turns": 5,
                "effects": {"integration_bonus": 0.03, "upkeep_reduction": 0.02, "bureaucratic_capacity": 10},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 160, "research": 40},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 900},
                "construction_turns": 9,
                "effects": {"integration_bonus": 0.06, "upkeep_reduction": 0.04, "bureaucratic_capacity": 22},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 280, "research": 70},
                "output_goods": {},
                "construction_cost": {"materials": 1800, "wealth": 1600},
                "construction_turns": 15,
                "effects": {"integration_bonus": 0.09, "upkeep_reduction": 0.06, "bureaucratic_capacity": 38},
            },
        ],
    },

    # ============================================================
    # GOVERNMENT — MANAGEMENT
    # Affects administrative/bureaucratic policies. Provides the
    # largest bureaucratic capacity bonuses of any building type.
    # ============================================================
    "civil_service_academy": {
        "label": "Civil Service Academy",
        "category": "government_management",
        "description": "Trains government administrators, providing large bureaucratic capacity and literacy gains.",
        "max_level": 3,
        "levels": [
            {
                "workers": 120,
                "input_goods": {"wealth": 100, "research": 40},
                "output_goods": {},
                "construction_cost": {"materials": 700, "wealth": 600},
                "construction_turns": 7,
                "effects": {"bureaucratic_capacity": 25, "literacy_bonus": 0.05},
            },
            {
                "workers": 250,
                "input_goods": {"wealth": 200, "research": 80},
                "output_goods": {},
                "construction_cost": {"materials": 1400, "wealth": 1200},
                "construction_turns": 12,
                "effects": {"bureaucratic_capacity": 55, "literacy_bonus": 0.10},
            },
            {
                "workers": 420,
                "input_goods": {"wealth": 350, "research": 140},
                "output_goods": {},
                "construction_cost": {"materials": 2500, "wealth": 2200},
                "construction_turns": 18,
                "effects": {"bureaucratic_capacity": 90, "literacy_bonus": 0.15},
            },
        ],
    },
    "administrative_center": {
        "label": "Administrative Center",
        "category": "government_management",
        "description": "Central government hub coordinating provincial administration. Reduces upkeep and provides bureaucratic capacity.",
        "max_level": 3,
        "levels": [
            {
                "workers": 150,
                "input_goods": {"wealth": 120},
                "output_goods": {},
                "construction_cost": {"materials": 800, "wealth": 700},
                "construction_turns": 8,
                "effects": {"bureaucratic_capacity": 30, "upkeep_reduction": 0.02},
            },
            {
                "workers": 300,
                "input_goods": {"wealth": 250},
                "output_goods": {},
                "construction_cost": {"materials": 1600, "wealth": 1400},
                "construction_turns": 14,
                "effects": {"bureaucratic_capacity": 65, "upkeep_reduction": 0.04},
            },
            {
                "workers": 500,
                "input_goods": {"wealth": 420},
                "output_goods": {},
                "construction_cost": {"materials": 2800, "wealth": 2500},
                "construction_turns": 20,
                "effects": {"bureaucratic_capacity": 100, "upkeep_reduction": 0.07},
            },
        ],
    },

    # ============================================================
    # GOVERNMENT — SECURITY
    # Affects law enforcement and internal security policies.
    # Improves stability recovery.
    # ============================================================
    "police_headquarters": {
        "label": "Police Headquarters",
        "category": "government_security",
        "description": "Law enforcement centre that maintains public order and accelerates stability recovery.",
        "max_level": 3,
        "levels": [
            {
                "workers": 150,
                "input_goods": {"wealth": 100, "arms": 30},
                "output_goods": {},
                "construction_cost": {"materials": 700, "wealth": 500},
                "construction_turns": 6,
                "effects": {"stability_recovery_bonus": 0.15, "bureaucratic_capacity": 8},
            },
            {
                "workers": 300,
                "input_goods": {"wealth": 200, "arms": 60},
                "output_goods": {},
                "construction_cost": {"materials": 1400, "wealth": 1000},
                "construction_turns": 10,
                "effects": {"stability_recovery_bonus": 0.30, "bureaucratic_capacity": 18},
            },
            {
                "workers": 500,
                "input_goods": {"wealth": 350, "arms": 100},
                "output_goods": {},
                "construction_cost": {"materials": 2500, "wealth": 1800},
                "construction_turns": 16,
                "effects": {"stability_recovery_bonus": 0.45, "bureaucratic_capacity": 30},
            },
        ],
    },
    "intelligence_agency": {
        "label": "Intelligence Agency",
        "category": "government_security",
        "description": "Covert operations centre providing stability through information control and threat prevention.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 120, "research": 40},
                "output_goods": {},
                "construction_cost": {"materials": 600, "wealth": 600},
                "construction_turns": 7,
                "effects": {"stability_recovery_bonus": 0.10, "integration_bonus": 0.03, "bureaucratic_capacity": 12},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 240, "research": 80},
                "output_goods": {},
                "construction_cost": {"materials": 1200, "wealth": 1200},
                "construction_turns": 12,
                "effects": {"stability_recovery_bonus": 0.20, "integration_bonus": 0.06, "bureaucratic_capacity": 25},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 400, "research": 140},
                "output_goods": {},
                "construction_cost": {"materials": 2200, "wealth": 2200},
                "construction_turns": 18,
                "effects": {"stability_recovery_bonus": 0.30, "integration_bonus": 0.09, "bureaucratic_capacity": 42},
            },
        ],
    },

    # ============================================================
    # GOVERNMENT — EDUCATION
    # Affects education policies. Provides literacy and research bonuses.
    # ============================================================
    "public_school": {
        "label": "Public School",
        "category": "government_education",
        "description": "State-funded basic education providing broad literacy improvements at low cost.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 80},
                "output_goods": {},
                "construction_cost": {"materials": 500, "wealth": 350},
                "construction_turns": 5,
                "effects": {"literacy_bonus": 0.08, "growth_bonus": 0.001},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 700},
                "construction_turns": 9,
                "effects": {"literacy_bonus": 0.16, "growth_bonus": 0.002},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 280},
                "output_goods": {},
                "construction_cost": {"materials": 1800, "wealth": 1200},
                "construction_turns": 14,
                "effects": {"literacy_bonus": 0.24, "growth_bonus": 0.003},
            },
        ],
    },
    "university": {
        "label": "University",
        "category": "government_education",
        "description": "Advanced institution of learning producing research output and high literacy gains.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"wealth": 150, "research": 50},
                "output_goods": {"research": 80},
                "construction_cost": {"materials": 1000, "wealth": 800},
                "construction_turns": 8,
                "effects": {"literacy_bonus": 0.06, "research_bonus": 0.15},
            },
            {
                "workers": 400,
                "input_goods": {"wealth": 300, "research": 100},
                "output_goods": {"research": 180},
                "construction_cost": {"materials": 2000, "wealth": 1600},
                "construction_turns": 14,
                "effects": {"literacy_bonus": 0.12, "research_bonus": 0.30},
            },
            {
                "workers": 650,
                "input_goods": {"wealth": 500, "research": 170},
                "output_goods": {"research": 320},
                "construction_cost": {"materials": 3500, "wealth": 2800},
                "construction_turns": 20,
                "effects": {"literacy_bonus": 0.18, "research_bonus": 0.45},
            },
        ],
    },

    # ============================================================
    # GOVERNMENT — ORGANIZATION
    # Affects labour and organizational policies. Improves
    # construction efficiency through organised labour.
    # ============================================================
    "labor_bureau": {
        "label": "Labor Bureau",
        "category": "government_organization",
        "description": "Coordinates workforce allocation and labour standards, reducing construction times.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 80},
                "output_goods": {},
                "construction_cost": {"materials": 500, "wealth": 400},
                "construction_turns": 5,
                "effects": {"construction_time_reduction": 0.06, "bureaucratic_capacity": 10},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 160},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 800},
                "construction_turns": 9,
                "effects": {"construction_time_reduction": 0.12, "bureaucratic_capacity": 22},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 280},
                "output_goods": {},
                "construction_cost": {"materials": 1800, "wealth": 1400},
                "construction_turns": 14,
                "effects": {"construction_time_reduction": 0.18, "bureaucratic_capacity": 38},
            },
        ],
    },
    "workers_council": {
        "label": "Workers' Council",
        "category": "government_organization",
        "description": "Representative body for workers that improves construction costs through collective bargaining.",
        "max_level": 3,
        "levels": [
            {
                "workers": 80,
                "input_goods": {"wealth": 60},
                "output_goods": {},
                "construction_cost": {"materials": 400, "wealth": 300},
                "construction_turns": 4,
                "effects": {"construction_cost_reduction": 0.03, "stability_recovery_bonus": 0.05, "bureaucratic_capacity": 8},
            },
            {
                "workers": 160,
                "input_goods": {"wealth": 120},
                "output_goods": {},
                "construction_cost": {"materials": 800, "wealth": 600},
                "construction_turns": 8,
                "effects": {"construction_cost_reduction": 0.06, "stability_recovery_bonus": 0.10, "bureaucratic_capacity": 18},
            },
            {
                "workers": 280,
                "input_goods": {"wealth": 210},
                "output_goods": {},
                "construction_cost": {"materials": 1500, "wealth": 1100},
                "construction_turns": 13,
                "effects": {"construction_cost_reduction": 0.10, "stability_recovery_bonus": 0.15, "bureaucratic_capacity": 30},
            },
        ],
    },

    # ============================================================
    # GOVERNMENT — WELFARE
    # Affects social welfare policies. Improves population growth
    # through social safety nets.
    # ============================================================
    "social_services_office": {
        "label": "Social Services Office",
        "category": "government_welfare",
        "description": "Coordinates welfare programs that improve population growth through social support.",
        "max_level": 3,
        "levels": [
            {
                "workers": 100,
                "input_goods": {"wealth": 100, "consumer_goods": 40},
                "output_goods": {},
                "construction_cost": {"materials": 500, "wealth": 400},
                "construction_turns": 5,
                "effects": {"growth_bonus": 0.002, "stability_recovery_bonus": 0.05},
            },
            {
                "workers": 200,
                "input_goods": {"wealth": 200, "consumer_goods": 80},
                "output_goods": {},
                "construction_cost": {"materials": 1000, "wealth": 800},
                "construction_turns": 9,
                "effects": {"growth_bonus": 0.004, "stability_recovery_bonus": 0.10},
            },
            {
                "workers": 350,
                "input_goods": {"wealth": 350, "consumer_goods": 140},
                "output_goods": {},
                "construction_cost": {"materials": 1800, "wealth": 1400},
                "construction_turns": 14,
                "effects": {"growth_bonus": 0.006, "stability_recovery_bonus": 0.15},
            },
        ],
    },
    "public_housing": {
        "label": "Public Housing",
        "category": "government_welfare",
        "description": "State-built housing that attracts population growth and improves stability through housing security.",
        "max_level": 3,
        "levels": [
            {
                "workers": 80,
                "input_goods": {"materials": 80, "wealth": 60},
                "output_goods": {},
                "construction_cost": {"materials": 600, "wealth": 300},
                "construction_turns": 5,
                "effects": {"growth_bonus": 0.003, "stability_recovery_bonus": 0.08},
            },
            {
                "workers": 160,
                "input_goods": {"materials": 160, "wealth": 120},
                "output_goods": {},
                "construction_cost": {"materials": 1200, "wealth": 600},
                "construction_turns": 9,
                "effects": {"growth_bonus": 0.005, "stability_recovery_bonus": 0.15},
            },
            {
                "workers": 280,
                "input_goods": {"materials": 280, "wealth": 210},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1100},
                "construction_turns": 14,
                "effects": {"growth_bonus": 0.008, "stability_recovery_bonus": 0.22},
            },
        ],
    },

    # ============================================================
    # MILITARY
    # Weapons Factory converts arms + machinery + components into
    # military_goods — the supply chain input for all base buildings.
    # Bases consume military_goods as operational upkeep; they do not
    # produce output goods but unlock unit training.
    # ============================================================
    "weapons_factory": {
        "label": "Weapons Factory",
        "category": "heavy_manufacturing",
        "description": "Assembles military equipment packages from arms, machinery, and components.",
        "max_level": 3,
        "levels": [
            {
                "workers": 500,
                "input_goods": {"arms": 150, "machinery": 100, "components": 80},
                "output_goods": {"military_goods": 150},
                "construction_cost": {"materials": 2500, "wealth": 1500, "manpower": 500},
                "construction_turns": 15,
                "effects": {},
            },
            {
                "workers": 1000,
                "input_goods": {"arms": 300, "machinery": 200, "components": 160},
                "output_goods": {"military_goods": 330},
                "construction_cost": {"materials": 5000, "wealth": 3000, "manpower": 1000},
                "construction_turns": 24,
                "effects": {},
            },
            {
                "workers": 1600,
                "input_goods": {"arms": 550, "machinery": 380, "components": 300},
                "output_goods": {"military_goods": 620},
                "construction_cost": {"materials": 9000, "wealth": 5500, "manpower": 1800},
                "construction_turns": 36,
                "effects": {},
            },
        ],
    },
    "army_base": {
        "label": "Army Base",
        "category": "military_army",
        "description": "Garrison and training facility for ground forces.",
        "max_level": 3,
        "levels": [
            {
                "workers": 300,
                "input_goods": {"wealth": 100, "military_goods": 50},
                "output_goods": {},
                "construction_cost": {"materials": 1500, "wealth": 800, "manpower": 500},
                "construction_turns": 10,
                "effects": {},
            },
            {
                "workers": 600,
                "input_goods": {"wealth": 200, "military_goods": 120},
                "output_goods": {},
                "construction_cost": {"materials": 3000, "wealth": 1600, "manpower": 1000},
                "construction_turns": 18,
                "effects": {},
            },
            {
                "workers": 1000,
                "input_goods": {"wealth": 350, "military_goods": 250},
                "output_goods": {},
                "construction_cost": {"materials": 5500, "wealth": 3000, "manpower": 2000},
                "construction_turns": 28,
                "effects": {},
            },
        ],
    },
    "naval_base": {
        "label": "Naval Base",
        "category": "military_naval",
        "description": "Port and drydock facility for naval forces. Requires coastal or river access.",
        "max_level": 3,
        "levels": [
            {
                "workers": 300,
                "input_goods": {"wealth": 130, "military_goods": 65, "fuel": 30},
                "output_goods": {},
                "construction_cost": {"materials": 2000, "wealth": 1200, "manpower": 600},
                "construction_turns": 13,
                "effects": {},
            },
            {
                "workers": 600,
                "input_goods": {"wealth": 260, "military_goods": 160, "fuel": 60},
                "output_goods": {},
                "construction_cost": {"materials": 4000, "wealth": 2400, "manpower": 1200},
                "construction_turns": 23,
                "effects": {},
            },
            {
                "workers": 1000,
                "input_goods": {"wealth": 450, "military_goods": 320, "fuel": 120},
                "output_goods": {},
                "construction_cost": {"materials": 7000, "wealth": 4200, "manpower": 2400},
                "construction_turns": 36,
                "effects": {},
            },
        ],
    },
    "air_base": {
        "label": "Air Base",
        "category": "military_air",
        "description": "Airfield and hangar complex for aerial forces. Cheap to establish but fuel-intensive to operate.",
        "max_level": 3,
        "levels": [
            {
                "workers": 200,
                "input_goods": {"wealth": 80, "military_goods": 40, "fuel": 120},
                "output_goods": {},
                "construction_cost": {"materials": 800, "wealth": 600, "manpower": 300},
                "construction_turns": 6,
                "effects": {},
            },
            {
                "workers": 400,
                "input_goods": {"wealth": 150, "military_goods": 100, "fuel": 240},
                "output_goods": {},
                "construction_cost": {"materials": 1600, "wealth": 1200, "manpower": 600},
                "construction_turns": 12,
                "effects": {},
            },
            {
                "workers": 650,
                "input_goods": {"wealth": 250, "military_goods": 200, "fuel": 450},
                "output_goods": {},
                "construction_cost": {"materials": 3000, "wealth": 2200, "manpower": 1000},
                "construction_turns": 20,
                "effects": {},
            },
        ],
    },

    # ============================================================
    # MILITARY EDUCATION
    # Nation-unique buildings (unique_per_nation = True).
    # One per nation regardless of province. All effects are
    # national-scope. Combat and upkeep-reduction effects are stubs
    # wired when the military simulation is built.
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
        "max_level": 3,
        "unique_per_nation": True,
        "levels": [
            {
                "workers": 350,
                "input_goods": {"wealth": 500, "research": 100, "consumer_goods": 150},
                "output_goods": {},
                "construction_cost": {"materials": 5000, "wealth": 4000},
                "construction_turns": 24,
                "effects": {
                    "army_training_speed_bonus": 0.08,
                    "army_combat_bonus": 0.04,
                    "march_speed_bonus": 0.03,
                    "army_upkeep_reduction": 0.04,
                },
            },
            {
                "workers": 600,
                "input_goods": {"wealth": 900, "research": 200, "consumer_goods": 250},
                "output_goods": {},
                "construction_cost": {"materials": 10000, "wealth": 8000},
                "construction_turns": 36,
                "effects": {
                    "army_training_speed_bonus": 0.15,
                    "army_combat_bonus": 0.08,
                    "march_speed_bonus": 0.05,
                    "army_upkeep_reduction": 0.08,
                },
            },
            {
                "workers": 900,
                "input_goods": {"wealth": 1400, "research": 350, "consumer_goods": 400},
                "output_goods": {},
                "construction_cost": {"materials": 18000, "wealth": 14000},
                "construction_turns": 52,
                "effects": {
                    "army_training_speed_bonus": 0.25,
                    "army_combat_bonus": 0.13,
                    "march_speed_bonus": 0.08,
                    "army_upkeep_reduction": 0.13,
                },
            },
        ],
    },
    "naval_war_college": {
        "label": "Naval War College",
        "category": "military_education",
        "description": (
            "Maritime officer academy and strategic studies institute. "
            "Improves navy training speed, combat effectiveness, sea transit speed, and unit upkeep efficiency. "
            "Nation-unique and coastal-only."
        ),
        "max_level": 3,
        "unique_per_nation": True,
        "levels": [
            {
                "workers": 350,
                "input_goods": {"wealth": 500, "research": 100, "fuel": 150},
                "output_goods": {},
                "construction_cost": {"materials": 5000, "wealth": 4000},
                "construction_turns": 24,
                "effects": {
                    "navy_training_speed_bonus": 0.08,
                    "navy_combat_bonus": 0.04,
                    "sea_transit_speed": 0.03,
                    "navy_upkeep_reduction": 0.04,
                },
            },
            {
                "workers": 600,
                "input_goods": {"wealth": 900, "research": 200, "fuel": 250},
                "output_goods": {},
                "construction_cost": {"materials": 10000, "wealth": 8000},
                "construction_turns": 36,
                "effects": {
                    "navy_training_speed_bonus": 0.15,
                    "navy_combat_bonus": 0.08,
                    "sea_transit_speed": 0.05,
                    "navy_upkeep_reduction": 0.08,
                },
            },
            {
                "workers": 900,
                "input_goods": {"wealth": 1400, "research": 350, "fuel": 400},
                "output_goods": {},
                "construction_cost": {"materials": 18000, "wealth": 14000},
                "construction_turns": 52,
                "effects": {
                    "navy_training_speed_bonus": 0.25,
                    "navy_combat_bonus": 0.13,
                    "sea_transit_speed": 0.08,
                    "navy_upkeep_reduction": 0.13,
                },
            },
        ],
    },
    "air_force_academy": {
        "label": "Air Force Academy",
        "category": "military_education",
        "description": (
            "Precision flight and tactics school for aerial forces. "
            "Improves air training speed, combat effectiveness, air transit speed, and unit upkeep efficiency. "
            "Nation-unique — only one may exist across all provinces."
        ),
        "max_level": 3,
        "unique_per_nation": True,
        "levels": [
            {
                "workers": 350,
                "input_goods": {"wealth": 500, "research": 120, "fuel": 100, "components": 50},
                "output_goods": {},
                "construction_cost": {"materials": 5000, "wealth": 4500},
                "construction_turns": 26,
                "effects": {
                    "air_training_speed_bonus": 0.08,
                    "air_combat_bonus": 0.04,
                    "air_transit_speed": 0.03,
                    "air_upkeep_reduction": 0.04,
                },
            },
            {
                "workers": 600,
                "input_goods": {"wealth": 900, "research": 220, "fuel": 180, "components": 100},
                "output_goods": {},
                "construction_cost": {"materials": 10000, "wealth": 9000},
                "construction_turns": 40,
                "effects": {
                    "air_training_speed_bonus": 0.15,
                    "air_combat_bonus": 0.08,
                    "air_transit_speed": 0.05,
                    "air_upkeep_reduction": 0.08,
                },
            },
            {
                "workers": 900,
                "input_goods": {"wealth": 1400, "research": 380, "fuel": 280, "components": 160},
                "output_goods": {},
                "construction_cost": {"materials": 18000, "wealth": 16000},
                "construction_turns": 56,
                "effects": {
                    "air_training_speed_bonus": 0.25,
                    "air_combat_bonus": 0.13,
                    "air_transit_speed": 0.08,
                    "air_upkeep_reduction": 0.13,
                },
            },
        ],
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

# Industry clustering: each additional active building of the same category
# in the province adds +5% output efficiency to all buildings of that category.
# Rewards industrial districts — a province with 3 chemical buildings each
# get +2 × 0.05 = +10% from clustering.
# Capped in practice by the finite number of buildings per category (≤3–4).
INDUSTRY_CLUSTER_BONUS = 0.05
