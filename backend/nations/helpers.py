from .models import NationModifier, NationPolicy
from .trait_constants import get_effective_trait_effects


def apply_government_modifiers(nation):
    """Create NationModifier entries based on government type."""
    from economy.constants import GOVERNMENT_TYPES

    govt = GOVERNMENT_TYPES.get(nation.government_type, {})
    _apply_modifier_set(nation, govt, NationModifier.Source.GOVERNMENT, f"Government: {nation.government_type}")


def get_nation_trait_effects(nation):
    """
    Return the merged trait effects dict for a nation.

    This is the primary way simulation code accesses trait bonuses.
    """
    return get_effective_trait_effects(nation.ideology_traits)


def create_default_policies(nation):
    """
    Bulk-create NationPolicy rows for all policy categories at their default levels.

    Safe to call on nation creation. Skips categories that already have a row.
    """
    from .policy_constants import POLICY_CATEGORIES

    existing = set(
        NationPolicy.objects.filter(nation=nation).values_list("category", flat=True)
    )
    to_create = []
    for cat_key, cat_def in POLICY_CATEGORIES.items():
        if cat_key not in existing:
            to_create.append(NationPolicy(
                nation=nation,
                category=cat_key,
                level=cat_def["default_level"],
            ))
    if to_create:
        NationPolicy.objects.bulk_create(to_create)


def _apply_modifier_set(nation, modifier_dict, source, name_prefix):
    """Generic helper to create NationModifier objects from a modifier dict."""
    # Remove old modifiers from same source
    NationModifier.objects.filter(nation=nation, source=source).delete()

    modifiers_to_create = []
    for category, value_or_dict in modifier_dict.items():
        if isinstance(value_or_dict, dict):
            for target, value in value_or_dict.items():
                modifiers_to_create.append(NationModifier(
                    nation=nation,
                    name=f"{name_prefix} - {target}",
                    category=_category_for(category),
                    target=target,
                    modifier_type=NationModifier.ModifierType.PERCENTAGE,
                    value=value,
                    source=source,
                ))
        else:
            modifiers_to_create.append(NationModifier(
                nation=nation,
                name=f"{name_prefix} - {category}",
                category=_category_for(category),
                target=category,
                modifier_type=NationModifier.ModifierType.FLAT if category == 'stability' else NationModifier.ModifierType.PERCENTAGE,
                value=value_or_dict,
                source=source,
            ))

    NationModifier.objects.bulk_create(modifiers_to_create)


def _category_for(key):
    """Map modifier dict keys to NationModifier.Category."""
    mapping = {
        'production': NationModifier.Category.ECONOMY,
        'integration': NationModifier.Category.ECONOMY,
        'stability': NationModifier.Category.STABILITY,
        'growth': NationModifier.Category.GROWTH,
        'consumption': NationModifier.Category.ECONOMY,
        'trade': NationModifier.Category.ECONOMY,
        'military': NationModifier.Category.MILITARY,
        'research': NationModifier.Category.ECONOMY,
        'diplomacy': NationModifier.Category.DIPLOMACY,
    }
    return mapping.get(key, NationModifier.Category.ECONOMY)
