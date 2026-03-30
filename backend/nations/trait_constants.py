"""
Ideology trait definitions.

Each nation selects 3 traits from 3 different pairs: 1 strong + 2 weak.
Strong traits provide larger bonuses; weak traits provide smaller ones.

All values sourced from policy_effects_complete.xlsx "Traits Effects" sheet.

Effect key conventions (matching the 162-column system):
  stability_bonus        — flat national stability adjustment (additive)
  growth_bonus/rate      — per-month population growth rate
  integration_pct        — percentage integration modifier
  trade_pct              — percentage trade modifier
  research_bonus         — flat research bonus
  research_pct           — percentage research modifier
  military_pct           — percentage military modifier
  consumption_pct        — percentage consumption modifier
  production_*_pct       — percentage production modifiers per resource
  building_efficiency_bonus — dict of category → bonus (additive within trait, stacks with other sources)
  building_restrictions  — list of building types that cannot be constructed
  corruption_resistance  — new effect column (additive)
  environmental_health   — new effect column (additive)
  worker_productivity    — new effect column (additive, multiplier on building output)

Some effect keys (espionage, diplomacy, trade_capacity, arms_production, training_speed,
military_upkeep_reduction) await future systems but are tracked here for completeness.
"""

# The 9 mutually exclusive trait pairs.
# Each nation picks from 3 different pairs.
TRAIT_PAIRS = [
    ("internationalist", "nationalist"),
    ("spiritualist", "positivist"),
    ("libertarian", "authoritarian"),
    ("pacifist", "militarist"),
    ("devious", "honorable"),
    ("egalitarian", "elitist"),
    ("collectivist", "individualist"),
    ("industrialist", "ecologist"),
    ("modern", "traditionalist"),
]

TRAIT_DEFS = {
    # --- Pair 0: Internationalist / Nationalist ---
    "internationalist": {
        "name": "Internationalist",
        "description": "Embraces foreign cooperation. Better diplomacy and trade, but citizens expect inclusive policies.",
        "pair_index": 0,
        "strong_effects": {
            "stability_bonus": -1.0,
            "integration_pct": 0.06,
            "trade_pct": 0.10,
            "consumption_pct": 0.03,
            "trade_capacity_bonus": 0.20,
            "diplomatic_reputation_bonus": 0.10,
        },
        "weak_effects": {
            "stability_bonus": -0.5,
            "integration_pct": 0.03,
            "trade_pct": 0.05,
            "trade_capacity_bonus": 0.10,
            "diplomatic_reputation_bonus": 0.05,
        },
    },
    "nationalist": {
        "name": "Nationalist",
        "description": "Prioritises the homeland. Stronger domestic bonuses but worse foreign relations.",
        "pair_index": 0,
        "strong_effects": {
            "stability_bonus": 3.0,
            "integration_pct": 0.05,
            "military_pct": 0.04,
            "manpower_bonus": 0.06,
            "trade_capacity_penalty": -0.15,
            "diplomatic_reputation_penalty": -0.10,
        },
        "weak_effects": {
            "stability_bonus": 2.0,
            "integration_pct": 0.03,
            "manpower_bonus": 0.03,
            "trade_capacity_penalty": -0.08,
        },
    },

    # --- Pair 1: Spiritualist / Positivist ---
    "spiritualist": {
        "name": "Spiritualist",
        "description": "Faith guides the nation. Higher stability and population growth but slower research.",
        "pair_index": 1,
        "strong_effects": {
            "stability_bonus": 4.0,
            "growth_bonus": 0.001,
            "research_pct": -0.10,
            "corruption_resistance": -0.03,
            "building_efficiency_bonus": {
                "religious": 0.15,
                "healthcare": 0.06,
            },
        },
        "weak_effects": {
            "stability_bonus": 2.0,
            "growth_bonus": 0.001,
            "research_pct": -0.05,
            "building_efficiency_bonus": {
                "religious": 0.08,
            },
        },
    },
    "positivist": {
        "name": "Positivist",
        "description": "Science and reason above all. Faster research but less social cohesion.",
        "pair_index": 1,
        "strong_effects": {
            "stability_bonus": -2.0,
            "research_bonus": 0.15,
            "literacy_bonus": 0.04,
            "corruption_resistance": 0.03,
            "building_efficiency_bonus": {
                "communications": 0.08,
                "pharmaceutical": 0.06,
            },
        },
        "weak_effects": {
            "stability_bonus": -1.0,
            "research_bonus": 0.08,
            "literacy_bonus": 0.02,
            "building_efficiency_bonus": {
                "communications": 0.04,
            },
        },
    },

    # --- Pair 2: Libertarian / Authoritarian ---
    "libertarian": {
        "name": "Libertarian",
        "description": "Minimal government interference. Lower upkeep, but harder to enforce policies.",
        "pair_index": 2,
        "strong_effects": {
            "stability_bonus": -2.0,
            "trade_pct": 0.05,
            "upkeep_reduction": 0.12,
            "wealth_production_bonus": 0.08,
            "production_wealth_pct": 0.06,
            "corruption_resistance": 0.03,
        },
        "weak_effects": {
            "stability_bonus": -1.0,
            "trade_pct": 0.03,
            "upkeep_reduction": 0.06,
            "wealth_production_bonus": 0.04,
        },
    },
    "authoritarian": {
        "name": "Authoritarian",
        "description": "Strong central control. Higher manpower and stability, but lower growth.",
        "pair_index": 2,
        "strong_effects": {
            "stability_bonus": 3.0,
            "growth_rate": -0.001,
            "manpower_bonus": 0.12,
            "corruption_resistance": -0.04,
            "building_efficiency_bonus": {
                "government_security": 0.06,
            },
        },
        "weak_effects": {
            "stability_bonus": 2.0,
            "growth_rate": -0.001,
            "manpower_bonus": 0.06,
            "building_efficiency_bonus": {
                "government_security": 0.03,
            },
        },
    },

    # --- Pair 3: Pacifist / Militarist ---
    "pacifist": {
        "name": "Pacifist",
        "description": "Rejects military solutions. Lower military costs, but restricted arms production.",
        "pair_index": 3,
        "strong_effects": {
            "stability_bonus": 3.0,
            "growth_bonus": 0.001,
            "trade_pct": 0.04,
            "consumption_pct": 0.03,
            "military_upkeep_reduction": 0.25,
            "arms_production_penalty": -0.30,
            "building_restrictions": ["arms_factory", "weapons_factory"],
        },
        "weak_effects": {
            "stability_bonus": 2.0,
            "growth_bonus": 0.001,
            "trade_pct": 0.02,
            "military_upkeep_reduction": 0.12,
            "arms_production_penalty": -0.15,
        },
    },
    "militarist": {
        "name": "Militarist",
        "description": "Military strength is national strength. Better arms output but higher instability.",
        "pair_index": 3,
        "strong_effects": {
            "stability_bonus": -3.0,
            "military_pct": 0.06,
            "manpower_bonus": 0.15,
            "training_speed_bonus": 0.20,
            "arms_production_bonus": 0.20,
            "building_efficiency_bonus": {
                "heavy_manufacturing": 0.10,
                "chemical": 0.06,
            },
        },
        "weak_effects": {
            "stability_bonus": -2.0,
            "military_pct": 0.03,
            "manpower_bonus": 0.08,
            "training_speed_bonus": 0.10,
            "arms_production_bonus": 0.10,
            "building_efficiency_bonus": {
                "heavy_manufacturing": 0.05,
            },
        },
    },

    # --- Pair 4: Devious / Honorable ---
    "devious": {
        "name": "Devious",
        "description": "The ends justify the means. Better espionage but worse diplomatic reputation.",
        "pair_index": 4,
        "strong_effects": {
            "trade_pct": 0.03,
            "espionage_bonus": 0.25,
            "counter_espionage_bonus": 0.10,
            "diplomatic_reputation_penalty": -0.15,
            "corruption_resistance": -0.05,
        },
        "weak_effects": {
            "espionage_bonus": 0.12,
            "counter_espionage_bonus": 0.05,
            "diplomatic_reputation_penalty": -0.08,
            "corruption_resistance": -0.02,
        },
    },
    "honorable": {
        "name": "Honorable",
        "description": "Deals are sacred. Better diplomatic reputation but vulnerable to espionage.",
        "pair_index": 4,
        "strong_effects": {
            "stability_bonus": 2.0,
            "trade_pct": -0.02,
            "diplomatic_reputation_bonus": 0.15,
            "corruption_resistance": 0.04,
        },
        "weak_effects": {
            "stability_bonus": 1.0,
            "diplomatic_reputation_bonus": 0.08,
            "corruption_resistance": 0.02,
        },
    },

    # --- Pair 5: Egalitarian / Elitist ---
    "egalitarian": {
        "name": "Egalitarian",
        "description": "All citizens are equal. Higher growth and stability, but less research output.",
        "pair_index": 5,
        "strong_effects": {
            "stability_bonus": 2.0,
            "growth_bonus": 0.001,
            "integration_pct": 0.04,
            "research_pct": -0.05,
            "worker_productivity": 0.02,
            "building_efficiency_bonus": {
                "government_welfare": 0.04,
            },
        },
        "weak_effects": {
            "stability_bonus": 1.0,
            "growth_bonus": 0.001,
            "integration_pct": 0.02,
            "research_pct": -0.03,
            "worker_productivity": 0.01,
        },
    },
    "elitist": {
        "name": "Elitist",
        "description": "Merit and talent rise to the top. Better research and specialisation, but lower growth.",
        "pair_index": 5,
        "strong_effects": {
            "growth_rate": -0.001,
            "research_bonus": 0.12,
            "wealth_production_bonus": 0.06,
            "building_efficiency_bonus": {
                "financial": 0.08,
                "light_manufacturing": 0.06,
            },
        },
        "weak_effects": {
            "research_bonus": 0.06,
            "wealth_production_bonus": 0.03,
            "building_efficiency_bonus": {
                "financial": 0.04,
            },
        },
    },

    # --- Pair 6: Collectivist / Individualist ---
    "collectivist": {
        "name": "Collectivist",
        "description": "The community comes first. Better integration and food production.",
        "pair_index": 6,
        "strong_effects": {
            "integration_pct": 0.05,
            "production_food_pct": 0.04,
            "worker_productivity": 0.02,
            "building_efficiency_bonus": {
                "farming": 0.06,
                "construction": 0.06,
                "government_welfare": 0.03,
            },
        },
        "weak_effects": {
            "integration_pct": 0.03,
            "production_food_pct": 0.02,
            "worker_productivity": 0.01,
            "building_efficiency_bonus": {
                "farming": 0.03,
            },
        },
    },
    "individualist": {
        "name": "Individualist",
        "description": "Individual freedom drives innovation. Better commerce but less stability.",
        "pair_index": 6,
        "strong_effects": {
            "stability_bonus": -1.0,
            "wealth_production_bonus": 0.10,
            "production_wealth_pct": 0.06,
            "building_efficiency_bonus": {
                "financial": 0.08,
                "entertainment": 0.06,
            },
        },
        "weak_effects": {
            "wealth_production_bonus": 0.05,
            "production_wealth_pct": 0.03,
            "building_efficiency_bonus": {
                "financial": 0.04,
            },
        },
    },

    # --- Pair 7: Industrialist / Ecologist ---
    "industrialist": {
        "name": "Industrialist",
        "description": "Production above all. Urban provinces thrive, but rural areas suffer.",
        "pair_index": 7,
        "strong_effects": {
            "urban_output_bonus": 0.15,
            "urban_threshold_reduction": 15000,
            "rural_output_penalty": -0.05,
            "production_materials_pct": 0.06,
            "production_energy_pct": 0.04,
            "environmental_health": -0.06,
            "building_efficiency_bonus": {
                "heavy_manufacturing": 0.08,
                "refining": 0.06,
            },
        },
        "weak_effects": {
            "urban_output_bonus": 0.08,
            "urban_threshold_reduction": 8000,
            "production_materials_pct": 0.03,
            "environmental_health": -0.03,
            "building_efficiency_bonus": {
                "heavy_manufacturing": 0.04,
            },
        },
    },
    "ecologist": {
        "name": "Ecologist",
        "description": "Harmony with nature. Rural provinces produce more, but urban areas are penalised.",
        "pair_index": 7,
        "strong_effects": {
            "rural_output_bonus": 0.15,
            "urban_growth_penalty": -0.003,
            "environmental_health": 0.08,
            "building_restrictions": ["refinery", "advanced_refinery", "oil_well", "fuel_depot"],
            "building_efficiency_bonus": {
                "farming": 0.10,
                "extraction": 0.06,
                "green_energy": 0.15,
            },
        },
        "weak_effects": {
            "rural_output_bonus": 0.08,
            "urban_growth_penalty": -0.001,
            "environmental_health": 0.04,
            "building_restrictions": ["refinery", "advanced_refinery", "oil_well", "fuel_depot"],
            "building_efficiency_bonus": {
                "farming": 0.05,
                "green_energy": 0.08,
            },
        },
    },

    # --- Pair 8: Modern / Traditionalist ---
    "modern": {
        "name": "Modern",
        "description": "Embrace the new world. Faster research and communications, but less stability.",
        "pair_index": 8,
        "strong_effects": {
            "stability_bonus": -2.0,
            "research_bonus": 0.10,
            "literacy_bonus": 0.03,
            "corruption_resistance": 0.02,
            "building_efficiency_bonus": {
                "communications": 0.10,
                "light_manufacturing": 0.06,
            },
        },
        "weak_effects": {
            "stability_bonus": -1.0,
            "research_bonus": 0.05,
            "literacy_bonus": 0.01,
            "building_efficiency_bonus": {
                "communications": 0.05,
            },
        },
    },
    "traditionalist": {
        "name": "Traditionalist",
        "description": "Preserve what works. Higher stability and food output, but slower to adapt.",
        "pair_index": 8,
        "strong_effects": {
            "stability_bonus": 3.0,
            "food_production_bonus": 0.08,
            "research_pct": -0.08,
            "building_efficiency_bonus": {
                "farming": 0.08,
                "healthcare": 0.06,
                "religious": 0.04,
            },
        },
        "weak_effects": {
            "stability_bonus": 2.0,
            "food_production_bonus": 0.04,
            "research_pct": -0.04,
            "building_efficiency_bonus": {
                "farming": 0.04,
            },
        },
    },
}

# Flat set of all valid trait keys
ALL_TRAITS = set(TRAIT_DEFS.keys())


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_pair_for_trait(trait_key):
    """Return the pair tuple containing this trait, or None."""
    idx = TRAIT_DEFS.get(trait_key, {}).get("pair_index")
    if idx is not None and 0 <= idx < len(TRAIT_PAIRS):
        return TRAIT_PAIRS[idx]
    return None


def get_opposing_trait(trait_key):
    """Return the other trait in this trait's pair, or None."""
    pair = get_pair_for_trait(trait_key)
    if not pair:
        return None
    return pair[1] if pair[0] == trait_key else pair[0]


def validate_trait_selection(strong, weak_list):
    """
    Validate a trait selection.

    Rules:
      - strong must be a valid trait key
      - weak_list must contain exactly 2 valid trait keys
      - All 3 traits must come from 3 different pairs
      - No two traits from the same pair

    Raises ValueError on invalid input.
    """
    if strong not in ALL_TRAITS:
        raise ValueError(f"Invalid strong trait: {strong}")

    if not isinstance(weak_list, (list, tuple)) or len(weak_list) != 2:
        raise ValueError("Must select exactly 2 weak traits")

    for w in weak_list:
        if w not in ALL_TRAITS:
            raise ValueError(f"Invalid weak trait: {w}")

    all_selected = [strong] + list(weak_list)

    # Check for duplicates
    if len(set(all_selected)) != 3:
        raise ValueError("All 3 traits must be unique")

    # Check all from different pairs
    pair_indices = set()
    for trait in all_selected:
        idx = TRAIT_DEFS[trait]["pair_index"]
        if idx in pair_indices:
            raise ValueError(f"Cannot select two traits from the same pair (pair {idx})")
        pair_indices.add(idx)


def get_effective_trait_effects(ideology_traits):
    """
    Merge strong + weak trait effects into a single effects dict.

    Parameters
    ----------
    ideology_traits : dict
        {"strong": "trait_key", "weak": ["trait_key", "trait_key"]}

    Returns
    -------
    dict
        Merged effects. Numeric values are summed; lists are unioned;
        dicts are merged with values summed; booleans use OR.
    """
    if not ideology_traits:
        return {}

    merged = {}

    strong = ideology_traits.get("strong")
    weak_list = ideology_traits.get("weak", [])

    # Process strong trait
    if strong and strong in TRAIT_DEFS:
        _merge_effects(merged, TRAIT_DEFS[strong]["strong_effects"])

    # Process weak traits
    for w in weak_list:
        if w and w in TRAIT_DEFS:
            _merge_effects(merged, TRAIT_DEFS[w]["weak_effects"])

    return merged


def _merge_effects(target, source):
    """Merge source effects into target, handling different value types."""
    for key, value in source.items():
        if key not in target:
            # Deep copy dicts and lists to avoid mutation
            if isinstance(value, dict):
                target[key] = dict(value)
            elif isinstance(value, list):
                target[key] = list(value)
            else:
                target[key] = value
        elif isinstance(value, (int, float)) and isinstance(target[key], (int, float)):
            target[key] += value
        elif isinstance(value, dict) and isinstance(target[key], dict):
            for k, v in value.items():
                target[key][k] = target[key].get(k, 0) + v
        elif isinstance(value, list) and isinstance(target[key], list):
            # Union lists (e.g. building_restrictions)
            target[key] = list(set(target[key]) | set(value))
        elif isinstance(value, bool):
            target[key] = target[key] or value
