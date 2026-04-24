"""Five-component government system.

A nation's government is defined by ONE choice from each of five orthogonal axes:

  GOV_DIRECTION          — How authority flows within the state
  GOV_ECONOMIC_CATEGORY  — Economic philosophy and production focus
  GOV_STRUCTURE          — Organisational form of rule
  GOV_POWER_ORIGIN       — What legitimises the government's authority
  GOV_POWER_TYPE         — How decision-making power is distributed

Each option provides a modifier dict with:
  stability              — flat stability contribution (additive)
  growth                 — per-month population growth rate (additive)
  integration/trade/research/military/consumption — percentage bonuses (multiplicative)
  production             — dict of resource → percentage bonus (multiplicative per-key)
  building_efficiency    — dict of category → bonus (multiplicative per-key)

The combined government effect is computed by get_combined_government_effects().

Building efficiency bonuses per component are modest (~4–8 % each) because five
components stack — a focused combination can reach ~30–40 % in a given category.

All values sourced from policy_effects_complete.xlsx "Government Options" sheet.
"""

# ---------------------------------------------------------------------------
# Direction — how authority flows within the state
# ---------------------------------------------------------------------------

GOV_DIRECTION = {
    "top_down": {
        "stability": -1,
        "integration": 0.08,
        "tax_efficiency": -0.06,
        "building_efficiency": {
            "heavy_manufacturing": 0.06,
            "extraction": 0.05,
            "construction": 0.06,
        },
    },
    "bottom_up": {
        "stability": 1,
        "growth": 0.002,
        "tax_efficiency": 0.06,
        "building_efficiency": {
            "light_manufacturing": 0.05,
            "farming": 0.06,
            "healthcare": 0.05,
        },
    },
    "none": {
        "stability": 2,
    },
}

# ---------------------------------------------------------------------------
# Economic Category — economic philosophy and production focus
# ---------------------------------------------------------------------------

GOV_ECONOMIC_CATEGORY = {
    "liberal": {
        "trade": 0.10,
        "production": {"kapital": 0.08},
        "building_efficiency": {
            "financial": 0.08,
            "transport": 0.06,
        },
    },
    "collectivist": {
        "stability": 2,
        "growth": 0.001,
        "consumption": -0.05,
        "tax_efficiency": 0.06,
        "production": {"food": 0.04, "materials": 0.04},
        "building_efficiency": {
            "light_manufacturing": 0.06,
            "farming": 0.07,
        },
    },
    "protectionist": {
        "trade": -0.05,
        "production": {"materials": 0.06},
        "building_efficiency": {
            "heavy_manufacturing": 0.08,
            "construction": 0.06,
        },
    },
    "resource": {
        "tax_efficiency": -0.06,
        "production": {"materials": 0.05, "energy": 0.05},
        "building_efficiency": {
            "extraction": 0.10,
            "refining": 0.06,
        },
    },
    "autarkic": {
        "trade": -0.15,
        "production": {"food": 0.05, "materials": 0.04},
        "building_efficiency": {
            "heavy_manufacturing": 0.04,
            "farming": 0.05,
            "extraction": 0.05,
        },
    },
    "subsistence": {
        "stability": 1,
        "growth": 0.002,
        "tax_efficiency": -0.06,
        "production": {"food": 0.08},
        "building_efficiency": {
            "farming": 0.10,
            "extraction": 0.04,
        },
    },
}

# ---------------------------------------------------------------------------
# Government Structure — organisational form of rule
# ---------------------------------------------------------------------------

GOV_STRUCTURE = {
    "hereditary": {
        "stability": 3,
        "growth": 0.001,
        "tax_efficiency": 0.05,
        "building_efficiency": {
            "financial": 0.05,
            "religious": 0.06,
        },
    },
    "power_consensus": {
        "integration": 0.05,
        "stability": 1,
        "tax_efficiency": -0.05,
        "building_efficiency": {
            "financial": 0.05,
            "government_management": 0.05,
        },
    },
    "federal": {
        "integration": -0.05,
        "stability": 2,
        "building_efficiency": {
            "construction": 0.05,
            "transport": 0.06,
        },
    },
    "representative": {
        "stability": 1,
        "tax_efficiency": 0.05,
        "production": {"kapital": 0.04},
        "building_efficiency": {
            "financial": 0.06,
            "communications": 0.05,
        },
    },
    "direct": {
        "stability": 2,
        "growth": 0.001,
        "building_efficiency": {
            "healthcare": 0.05,
            "government_organization": 0.06,
        },
    },
}

# ---------------------------------------------------------------------------
# Power Origin — what legitimises the government's authority
# ---------------------------------------------------------------------------

GOV_POWER_ORIGIN = {
    "elections": {
        "stability": 2,
        "tax_efficiency": 0.05,
        "building_efficiency": {
            "financial": 0.05,
            "communications": 0.07,
        },
    },
    "economic_success": {
        "research": 0.08,
        "production": {"kapital": 0.06},
        "building_efficiency": {
            "financial": 0.08,
            "government_management": 0.05,
        },
    },
    "law_and_order": {
        "stability": 3,
        "building_efficiency": {
            "government_regulatory": 0.07,
            "government_oversight": 0.06,
        },
    },
    "military_power": {
        "stability": -3,
        "military": 0.10,
        "tax_efficiency": -0.06,
        "production": {"manpower": 0.10},
        "building_efficiency": {
            "heavy_manufacturing": 0.07,
            "construction": 0.06,
        },
    },
    "religious": {
        "stability": 4,
        "growth": 0.002,
        "research": -0.08,
        "building_efficiency": {
            "religious": 0.10,
            "healthcare": 0.07,
        },
    },
    "ideology": {
        "stability": 1,
        "building_efficiency": {
            "communications": 0.06,
            "government_education": 0.06,
        },
    },
}

# ---------------------------------------------------------------------------
# Power Type — how decision-making power is distributed
# ---------------------------------------------------------------------------

GOV_POWER_TYPE = {
    "singular": {
        "integration": 0.08,
        "stability": -2,
        "military": 0.05,
        "tax_efficiency": 0.05,
        "building_efficiency": {
            "heavy_manufacturing": 0.06,
            "construction": 0.06,
        },
    },
    "council": {
        "integration": 0.03,
        "stability": 1,
        "tax_efficiency": 0.05,
        "building_efficiency": {
            "financial": 0.05,
            "government_management": 0.06,
        },
    },
    "large_body": {
        "stability": 2,
        "production": {"kapital": 0.04},
        "building_efficiency": {
            "communications": 0.06,
            "government_organization": 0.05,
        },
    },
    "multi_body": {
        "trade": 0.05,
        "stability": -1,
        "tax_efficiency": -0.05,
        "building_efficiency": {
            "financial": 0.04,
            "transport": 0.05,
        },
    },
    "staggered_groups": {
        "stability": 2,
        "integration": 0.02,
        "tax_efficiency": -0.05,
        "building_efficiency": {
            "government_management": 0.06,
            "government_oversight": 0.04,
        },
    },
}

# ---------------------------------------------------------------------------
# Axis-to-dict mapping — used by validators and the engine
# ---------------------------------------------------------------------------

GOV_COMPONENTS = {
    "direction": GOV_DIRECTION,
    "economic_category": GOV_ECONOMIC_CATEGORY,
    "structure": GOV_STRUCTURE,
    "power_origin": GOV_POWER_ORIGIN,
    "power_type": GOV_POWER_TYPE,
}

# Default government — a cautious post-apocalyptic transitional authority.
GOV_DEFAULTS = {
    "gov_direction": "none",
    "gov_economic_category": "subsistence",
    "gov_structure": "power_consensus",
    "gov_power_origin": "law_and_order",
    "gov_power_type": "council",
}


# ---------------------------------------------------------------------------
# Effect aggregation
# ---------------------------------------------------------------------------

def get_combined_government_effects(gov_direction, gov_economic_category,
                                    gov_structure, gov_power_origin, gov_power_type):
    """
    Merge effects from all five government components into a single dict.

    Stacking rules
    --------------
    Flat / rate values (stability, growth):
        Summed additively.  These are absolute quantities, not multipliers.

    Scalar percentage bonuses (integration, trade, research, military, consumption):
        Multiplied: combined = product(1 + bonus_i) - 1.
        Diminishing returns on stacking; penalties also compound slightly less harshly.

    Nested percentage dicts (production, building_efficiency):
        Each sub-key is multiplied independently with the same formula.

    The returned dict uses the same structure as individual component entries --
    percentage keys hold net bonus fractions (combined multiplier - 1).
    Downstream code adds 1.0 before applying (unchanged interface).
    """
    _ADDITIVE_KEYS = {"stability", "growth", "tax_efficiency"}
    _SCALAR_PCT_KEYS = {"integration", "trade", "research", "military", "consumption"}
    _NESTED_PCT_KEYS = {"production", "building_efficiency"}

    components = [
        GOV_DIRECTION.get(gov_direction, {}),
        GOV_ECONOMIC_CATEGORY.get(gov_economic_category, {}),
        GOV_STRUCTURE.get(gov_structure, {}),
        GOV_POWER_ORIGIN.get(gov_power_origin, {}),
        GOV_POWER_TYPE.get(gov_power_type, {}),
    ]

    merged = {}

    # Flat / rate values: sum
    for key in _ADDITIVE_KEYS:
        total = sum(comp.get(key, 0) for comp in components)
        if total:
            merged[key] = total

    # Scalar percentage: product(1 + bonus) - 1
    for key in _SCALAR_PCT_KEYS:
        factor = 1.0
        for comp in components:
            if key in comp:
                factor *= (1.0 + comp[key])
        net = factor - 1.0
        if net:
            merged[key] = net

    # Nested percentage dicts: per-subkey product(1 + bonus) - 1
    for key in _NESTED_PCT_KEYS:
        sub_factors = {}
        for comp in components:
            for subkey, bonus in comp.get(key, {}).items():
                sub_factors.setdefault(subkey, 1.0)
                sub_factors[subkey] *= (1.0 + bonus)
        if sub_factors:
            merged[key] = {sk: f - 1.0 for sk, f in sub_factors.items()}

    return merged
