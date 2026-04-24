"""Tax policy rank → structure resolution for the Wealth & Taxation System.

The 4 tax policy categories (income_tax, consumption_tax, land_tax,
gift_estate_tax) each have a player-selectable rank.  Each rank corresponds
to a structure that determines how the nation-level `tax_rate` is applied.

Rank indices correspond 1:1 to the level ordering in
policy_effects_data.POLICY_CATEGORIES for the respective category.
"""
from __future__ import annotations


# --- Rank → structure-key maps --------------------------------------------

INCOME_TAX_STRUCTURES = (
    "none",
    "flat",
    "progressive",
    "regressive",
    "wealth_redistribution",
)

CONSUMPTION_TAX_STRUCTURES = (
    "none",
    "basic_goods_exempted",
    "all_goods",
    "sin_tax",
    "health_tax",
)

LAND_TAX_STRUCTURES = (
    "none",
    "property_tax",
    "land_value_tax",
    "both",
)

GIFT_ESTATE_STRUCTURES = (
    "none",
    "meritocratic_intentions",
    "strict_meritocracy",
    "communal_duties",
)

_STRUCTURE_TABLE = {
    "income_tax":       INCOME_TAX_STRUCTURES,
    "consumption_tax":  CONSUMPTION_TAX_STRUCTURES,
    "land_tax":         LAND_TAX_STRUCTURES,
    "gift_estate_tax":  GIFT_ESTATE_STRUCTURES,
}


# --- Accessor helpers ------------------------------------------------------

def _get_policy_level(nation, category: str, default: int = 0) -> int:
    """Return the nation's current rank for `category`, or `default`."""
    from .models import NationPolicy
    try:
        return NationPolicy.objects.get(nation=nation, category=category).level
    except NationPolicy.DoesNotExist:
        return default


def get_tax_structure(nation, category: str) -> str:
    """Return the structure key (e.g. 'flat', 'sin_tax') for this nation's rank."""
    ranks = _STRUCTURE_TABLE.get(category)
    if not ranks:
        return "none"
    level = _get_policy_level(nation, category, default=0)
    if level < 0 or level >= len(ranks):
        return ranks[0]
    return ranks[level]


def income_tax_structure(nation) -> str:
    return get_tax_structure(nation, "income_tax")


def consumption_tax_structure(nation) -> str:
    return get_tax_structure(nation, "consumption_tax")


def land_tax_structure(nation) -> str:
    return get_tax_structure(nation, "land_tax")


def gift_estate_structure(nation) -> str:
    return get_tax_structure(nation, "gift_estate_tax")
