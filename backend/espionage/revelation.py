"""Information revelation system for the espionage transparency mechanic.

Given a transparency value (0.0–1.0), determines exactly which pieces of
information about a target nation are visible to an attacker. Categories
are revealed easiest-first; within each category, items from the most
populous provinces are revealed first.
"""

import random

from .constants import TRANSPARENCY_CATEGORIES, TRANSPARENCY_CATEGORY_WEIGHTS


def _count_category_items(target_nation, game, category, provinces, buildings_by_province):
    """Count total information items for a category.

    Returns a list of (item_key, sort_value) tuples where sort_value
    determines reveal order (higher = revealed first / easier).
    """
    if category == "building_locations":
        items = []
        for prov in provinces:
            prov_buildings = buildings_by_province.get(prov.id, [])
            for b in prov_buildings:
                items.append((
                    {"province_id": prov.id, "building_type": b.building_type},
                    prov.population,  # most populous = easiest
                ))
        return items

    elif category == "province_level_info":
        items = []
        for prov in provinces:
            for field in ("local_stability", "local_happiness", "local_security", "population"):
                items.append((
                    {"province_id": prov.id, "field": field, "value": getattr(prov, field)},
                    prov.population,
                ))
            # Wealth comes from the resource pool, use population as proxy
            items.append((
                {"province_id": prov.id, "field": "wealth", "value": None},
                prov.population,
            ))
        return items

    elif category == "positions_of_formations":
        # Stub — no military formations yet. Return empty.
        return []

    elif category == "cointel":
        from .models import EspionageAction
        suppress_actions = EspionageAction.objects.filter(
            game=game,
            nation=target_nation,
            action_type=EspionageAction.ActionType.SUPPRESS_FOREIGN_OPERATIONS,
            status=EspionageAction.Status.ACTIVE,
        ).select_related("target_province")

        items = []
        seen = set()
        for action in suppress_actions:
            if action.target_province_id and action.target_province_id not in seen:
                seen.add(action.target_province_id)
                pop = action.target_province.population if action.target_province else 0
                items.append((
                    {"province_id": action.target_province_id},
                    pop,
                ))
        return items

    elif category == "foreign_espionage":
        from .models import EspionageAction
        foreign_actions = EspionageAction.objects.filter(
            game=game,
            nation=target_nation,
            action_type__in=[
                EspionageAction.ActionType.INVESTIGATE_PROVINCE,
                EspionageAction.ActionType.PROMOTE_FOREIGN_IDEOLOGY,
                EspionageAction.ActionType.TERRORIST_ATTACK,
                EspionageAction.ActionType.SABOTAGE_BUILDING,
            ],
            status=EspionageAction.Status.ACTIVE,
        ).values_list("target_nation_id", flat=True).distinct()

        items = []
        for nation_id in foreign_actions:
            if nation_id is not None:
                items.append((
                    {"target_nation_id": nation_id},
                    1,  # all equally hard; revealed as whole increments
                ))
        return items

    return []


def compute_revealed_info(transparency, target_nation, game, voluntary_shares=None):
    """Compute what information is revealed about a target nation.

    Args:
        transparency: Float 0.0–1.0 representing attacker's transparency into target.
        target_nation: The Nation being spied on.
        game: The Game instance.
        voluntary_shares: Set of category strings that the target has voluntarily
            shared with the attacker (from IntelligenceSharing).

    Returns:
        Dict with category keys mapping to revealed information.
    """
    if voluntary_shares is None:
        voluntary_shares = set()

    result = {cat: {} for cat in TRANSPARENCY_CATEGORIES}

    # Fetch target provinces and buildings once
    provinces = list(
        target_nation.provinces.all().order_by("-population")
    )
    buildings_by_province = {}
    from provinces.models import Building
    for b in Building.objects.filter(
        province__nation=target_nation,
        is_active=True,
        under_construction=False,
    ).select_related("province"):
        buildings_by_province.setdefault(b.province_id, []).append(b)

    # Collect items per category
    category_items = {}
    for cat in TRANSPARENCY_CATEGORIES:
        items = _count_category_items(target_nation, game, cat, provinces, buildings_by_province)
        # Sort by sort_value descending (easiest / most populous first)
        items.sort(key=lambda x: x[1], reverse=True)
        category_items[cat] = items

    # Compute weighted total
    total_weighted = 0.0
    for cat in TRANSPARENCY_CATEGORIES:
        count = len(category_items[cat])
        weight = TRANSPARENCY_CATEGORY_WEIGHTS.get(cat, 0.0)
        total_weighted += count * weight

    if total_weighted == 0:
        # No information exists to reveal — merge voluntary shares and return
        for cat in voluntary_shares:
            if cat in result:
                result[cat] = _full_category(cat, category_items.get(cat, []))
        return result

    # Budget: how many weighted items we can reveal
    budget = total_weighted * transparency

    # Fill categories easiest-first
    for cat in TRANSPARENCY_CATEGORIES:
        if cat in voluntary_shares:
            # Voluntarily shared — reveal everything in this category
            result[cat] = _full_category(cat, category_items[cat])
            continue

        items = category_items[cat]
        weight = TRANSPARENCY_CATEGORY_WEIGHTS.get(cat, 0.0)
        if weight == 0 or not items:
            continue

        if cat == "foreign_espionage":
            # Special rule: only reveal if budget covers an entire increment
            increment_cost = weight  # cost of one item in this category
            revealable = int(budget / increment_cost) if increment_cost > 0 else 0
            revealable = min(revealable, len(items))
            if revealable > 0:
                # Select randomly from available items
                selected = random.sample(items, revealable)
                result[cat] = _format_foreign_espionage(selected)
                budget -= revealable * increment_cost
        else:
            # Reveal items in order (easiest first) until budget exhausted
            revealed = []
            for item_data, sort_val in items:
                cost = weight
                if budget >= cost:
                    revealed.append(item_data)
                    budget -= cost
                else:
                    break
            result[cat] = _format_category(cat, revealed)

    return result


def _full_category(cat, items):
    """Return all items in a category, fully revealed."""
    all_data = [item_data for item_data, _ in items]
    if cat == "foreign_espionage":
        return _format_foreign_espionage([(d, 0) for d in all_data])
    return _format_category(cat, all_data)


def _format_category(cat, items):
    """Format revealed items into the output structure for a category."""
    if cat == "building_locations":
        by_province = {}
        for item in items:
            pid = str(item["province_id"])
            by_province.setdefault(pid, []).append(item["building_type"])
        return by_province

    elif cat == "province_level_info":
        by_province = {}
        for item in items:
            pid = str(item["province_id"])
            by_province.setdefault(pid, {})[item["field"]] = item["value"]
        return by_province

    elif cat == "positions_of_formations":
        by_province = {}
        for item in items:
            pid = str(item.get("province_id", "unknown"))
            by_province.setdefault(pid, []).append(item)
        return by_province

    elif cat == "cointel":
        return [item["province_id"] for item in items]

    return items


def _format_foreign_espionage(items):
    """Format foreign espionage items (nation IDs being targeted)."""
    return [item_data["target_nation_id"] for item_data, _ in items]
