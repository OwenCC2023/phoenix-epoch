"""Five-component government system.

A nation's government is defined by ONE choice from each of five orthogonal axes:

  GOV_DIRECTION          — How authority flows within the state
  GOV_ECONOMIC_CATEGORY  — Economic philosophy and production focus
  GOV_STRUCTURE          — Organisational form of rule
  GOV_POWER_ORIGIN       — What legitimises the government's authority
  GOV_POWER_TYPE         — How decision-making power is distributed

Each option provides a modifier dict with the same keys as the former GOVERNMENT_TYPES
entries (production, stability, growth, building_efficiency, etc.) plus two new keys:

  policy_effectiveness   — dict of policy_group → bonus fraction (stub; wired when policy
                           effects are implemented)
  military_effectiveness — dict of condition/unit_type → bonus fraction (stub; wired when
                           the military simulation is built)

The combined government effect is the SUM of all five chosen components via
get_combined_government_effects().

Building efficiency bonuses per component are modest (~4–8 % each) because five
components stack — a focused combination can reach ~30–40 % in a given category.

Balance notes
-------------
- Each component contributes to 1-3 building categories at most.
- Stability contributions are flat (per-component values −3 … +4).
- Growth contributions are per-month fractional rates.
- All values are additive with the trait system (same principle as the old single-type).
"""

# ---------------------------------------------------------------------------
# Direction — how authority flows within the state
# ---------------------------------------------------------------------------

GOV_DIRECTION = {
    "top_down": {
        # Centralised command; strong at directing heavy industry and large projects.
        # Slight stability penalty from authoritarian friction.
        "integration": 0.08,
        "stability": -1,
        "building_efficiency": {
            "construction": 0.06,
            "heavy_manufacturing": 0.06,
            "extraction": 0.05,
        },
        "policy_effectiveness": {"economic_regulation": 0.15},   # stub
        "military_effectiveness": {"command_bonus": 0.10},        # stub
    },
    "bottom_up": {
        # Community-driven; strong at agriculture, light industry, and healthcare.
        # Growth bonus from grassroots participation; mild stability bonus.
        "growth": 0.002,
        "stability": 1,
        "building_efficiency": {
            "farming": 0.06,
            "light_manufacturing": 0.05,
            "healthcare": 0.05,
        },
        "policy_effectiveness": {"social_welfare": 0.15},         # stub
        "military_effectiveness": {"defensive_bonus": 0.10},      # stub
    },
    "none": {
        # No dominant directional authority; less friction, more stability.
        # No building efficiency bonuses — genuinely neutral.
        "stability": 2,
        "policy_effectiveness": {},                                # stub
        "military_effectiveness": {},                              # stub
    },
}

# ---------------------------------------------------------------------------
# Economic Category — economic philosophy and production focus
# ---------------------------------------------------------------------------

GOV_ECONOMIC_CATEGORY = {
    "liberal": {
        # Free markets; profit motive drives finance and trade networks.
        "production": {"wealth": 0.08},
        "trade": 0.10,
        "building_efficiency": {
            "financial": 0.08,
            "transport": 0.06,
        },
        "policy_effectiveness": {"trade_policy": 0.20},           # stub
        "military_effectiveness": {},                              # stub
    },
    "collectivist": {
        # Collective ownership; broad food/materials production; reduced consumption
        # waste; modest stability from shared purpose.
        "production": {"food": 0.04, "materials": 0.04},
        "stability": 2,
        "growth": 0.001,
        "consumption": -0.05,
        "building_efficiency": {
            "farming": 0.07,
            "light_manufacturing": 0.06,
        },
        "policy_effectiveness": {"labour_policy": 0.20},          # stub
        "military_effectiveness": {},                              # stub
    },
    "protectionist": {
        # Domestic industry protection; tariffs reduce trade but boost heavy industry.
        "production": {"materials": 0.06},
        "trade": -0.05,
        "building_efficiency": {
            "heavy_manufacturing": 0.08,
            "construction": 0.06,
        },
        "policy_effectiveness": {"trade_policy": 0.20},           # stub
        "military_effectiveness": {},                              # stub
    },
    "resource": {
        # Extraction economy; deep focus on raw materials and energy.
        "production": {"materials": 0.05, "energy": 0.05},
        "building_efficiency": {
            "extraction": 0.10,
            "refining": 0.06,
        },
        "policy_effectiveness": {"resource_management": 0.20},    # stub
        "military_effectiveness": {},                              # stub
    },
    "autarkic": {
        # Self-sufficient, minimal foreign dependency.
        # Trade penalty offset by broad domestic production bonuses.
        "production": {"food": 0.05, "materials": 0.04},
        "trade": -0.15,
        "building_efficiency": {
            "farming": 0.05,
            "extraction": 0.05,
            "heavy_manufacturing": 0.04,
        },
        "policy_effectiveness": {"self_sufficiency": 0.20},       # stub
        "military_effectiveness": {},                              # stub
    },
    "subsistence": {
        # Bare survival economy; strongest food bonus of any economic category;
        # growth bonus from plentiful basic goods.
        "production": {"food": 0.08},
        "growth": 0.002,
        "stability": 1,
        "building_efficiency": {
            "farming": 0.10,
            "extraction": 0.04,
        },
        "policy_effectiveness": {"basic_needs": 0.20},            # stub
        "military_effectiveness": {},                              # stub
    },
}

# ---------------------------------------------------------------------------
# Government Structure — organisational form of rule
# ---------------------------------------------------------------------------

GOV_STRUCTURE = {
    "hereditary": {
        # Dynasty/inheritance; stable succession, financial networks backed by nobility.
        "stability": 3,
        "growth": 0.001,
        "building_efficiency": {
            "financial": 0.05,
            "religious": 0.06,
        },
        "policy_effectiveness": {"succession_law": 0.15},         # stub
        "military_effectiveness": {"cavalry_bonus": 0.08},        # stub
    },
    "power_consensus": {
        # Elite power-sharing; strong administrative integration.
        "integration": 0.05,
        "stability": 1,
        "building_efficiency": {
            "financial": 0.05,
            "government_management": 0.05,
        },
        "policy_effectiveness": {"status_quo": 0.15},             # stub
        "military_effectiveness": {},                              # stub
    },
    "federal": {
        # Regional autonomy; weaker central integration but robust infrastructure.
        "integration": -0.05,
        "stability": 2,
        "building_efficiency": {
            "transport": 0.06,
            "construction": 0.05,
        },
        "policy_effectiveness": {"regional_policy": 0.20},        # stub
        "military_effectiveness": {"territorial_defence": 0.08},  # stub
    },
    "representative": {
        # Elected representatives; commerce and communications benefit from open debate.
        "production": {"wealth": 0.04},
        "stability": 1,
        "building_efficiency": {
            "financial": 0.06,
            "communications": 0.05,
        },
        "policy_effectiveness": {"electoral_reform": 0.15},       # stub
        "military_effectiveness": {},                              # stub
    },
    "direct": {
        # Direct popular participation; strong community institutions.
        "stability": 2,
        "growth": 0.001,
        "building_efficiency": {
            "government_organization": 0.06,
            "healthcare": 0.05,
        },
        "policy_effectiveness": {"popular_mandate": 0.20},        # stub
        "military_effectiveness": {"militia_bonus": 0.10},        # stub
    },
}

# ---------------------------------------------------------------------------
# Power Origin — what legitimises the government's authority
# ---------------------------------------------------------------------------

GOV_POWER_ORIGIN = {
    "elections": {
        # Democratic mandate; open information environment boosts communications.
        "stability": 2,
        "building_efficiency": {
            "communications": 0.07,
            "financial": 0.05,
        },
        "policy_effectiveness": {"popular_mandate": 0.20},        # stub
        "military_effectiveness": {"morale_bonus": 0.08},         # stub
    },
    "economic_success": {
        # Technocratic/performance legitimacy; meritocracy drives research and finance.
        "production": {"wealth": 0.06},
        "research": 0.08,
        "building_efficiency": {
            "financial": 0.08,
            "government_management": 0.05,
        },
        "policy_effectiveness": {"economic_optimization": 0.20},  # stub
        "military_effectiveness": {"logistics_bonus": 0.10},      # stub
    },
    "law_and_order": {
        # Legal/institutional legitimacy; strong regulatory and oversight capacity.
        "stability": 3,
        "building_efficiency": {
            "government_regulatory": 0.07,
            "government_oversight": 0.06,
        },
        "policy_effectiveness": {"legal_reform": 0.20},           # stub
        "military_effectiveness": {"discipline_bonus": 0.08},     # stub
    },
    "military_power": {
        # Military rules; manpower and arms production favoured; civil stability suffers.
        "production": {"manpower": 0.10},
        "military": 0.10,
        "stability": -3,
        "building_efficiency": {
            "heavy_manufacturing": 0.07,
            "construction": 0.06,
        },
        "policy_effectiveness": {"military_policy": 0.20},        # stub
        "military_effectiveness": {"combat_bonus": 0.15},         # stub
    },
    "religious": {
        # Religious legitimacy; strong stability and growth, but research suffers.
        "stability": 4,
        "growth": 0.002,
        "research": -0.08,
        "building_efficiency": {
            "religious": 0.10,
            "healthcare": 0.07,
        },
        "policy_effectiveness": {"religious_law": 0.20},          # stub
        "military_effectiveness": {"morale_bonus": 0.10},         # stub
    },
    "ideology": {
        # Ideological legitimacy; propaganda infrastructure and education benefit.
        "stability": 1,
        "building_efficiency": {
            "communications": 0.06,
            "government_education": 0.06,
        },
        "policy_effectiveness": {"ideological_policy": 0.20},     # stub
        "military_effectiveness": {"morale_bonus": 0.08},         # stub
    },
}

# ---------------------------------------------------------------------------
# Power Type — how decision-making power is distributed
# ---------------------------------------------------------------------------

GOV_POWER_TYPE = {
    "singular": {
        # One supreme ruler; decisive action, but civil liberty friction.
        "integration": 0.08,
        "stability": -2,
        "military": 0.05,
        "building_efficiency": {
            "heavy_manufacturing": 0.06,
            "construction": 0.06,
        },
        "policy_effectiveness": {"executive_decree": 0.20},       # stub
        "military_effectiveness": {"command_unity": 0.10},        # stub
    },
    "council": {
        # Small governing council; balanced integration and stability.
        "integration": 0.03,
        "stability": 1,
        "building_efficiency": {
            "financial": 0.05,
            "government_management": 0.06,
        },
        "policy_effectiveness": {"council_mandate": 0.15},        # stub
        "military_effectiveness": {},                              # stub
    },
    "large_body": {
        # Parliament/legislature; broad legitimacy boosts wealth and communications.
        "production": {"wealth": 0.04},
        "stability": 2,
        "building_efficiency": {
            "communications": 0.06,
            "government_organization": 0.05,
        },
        "policy_effectiveness": {"legislative_mandate": 0.15},    # stub
        "military_effectiveness": {},                              # stub
    },
    "multi_body": {
        # Multiple competing/cooperating bodies; competition stimulates trade and finance.
        "trade": 0.05,
        "stability": -1,
        "building_efficiency": {
            "financial": 0.04,
            "transport": 0.05,
        },
        "policy_effectiveness": {"compromise_policy": 0.15},      # stub
        "military_effectiveness": {"coordination_penalty": -0.10},  # stub
    },
    "staggered_groups": {
        # Rotating overlapping power groups; institutional continuity and oversight.
        "stability": 2,
        "integration": 0.02,
        "building_efficiency": {
            "government_management": 0.06,
            "government_oversight": 0.04,
        },
        "policy_effectiveness": {"gradual_reform": 0.20},         # stub
        "military_effectiveness": {},                              # stub
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
        Multiplied: combined = product(1 + bonus_i) − 1.
        Diminishing returns on stacking; penalties also compound slightly less harshly.

    Nested percentage dicts (production, building_efficiency,
    policy_effectiveness, military_effectiveness):
        Each sub-key is multiplied independently with the same formula.

    The returned dict uses the same structure as individual component entries —
    percentage keys hold net bonus fractions (combined multiplier − 1).
    Downstream code adds 1.0 before applying (unchanged interface).
    """
    _ADDITIVE_KEYS = {"stability", "growth"}
    _SCALAR_PCT_KEYS = {"integration", "trade", "research", "military", "consumption"}
    _NESTED_PCT_KEYS = {"production", "building_efficiency",
                        "policy_effectiveness", "military_effectiveness"}

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

    # Scalar percentage: product(1 + bonus) − 1
    for key in _SCALAR_PCT_KEYS:
        factor = 1.0
        for comp in components:
            if key in comp:
                factor *= (1.0 + comp[key])
        net = factor - 1.0
        if net:
            merged[key] = net

    # Nested percentage dicts: per-subkey product(1 + bonus) − 1
    for key in _NESTED_PCT_KEYS:
        sub_factors = {}
        for comp in components:
            for subkey, bonus in comp.get(key, {}).items():
                sub_factors.setdefault(subkey, 1.0)
                sub_factors[subkey] *= (1.0 + bonus)
        if sub_factors:
            merged[key] = {sk: f - 1.0 for sk, f in sub_factors.items()}

    return merged
