"""Order validation logic."""


def validate_order(order):
    """Validate an order and return list of error strings."""
    errors = []

    validators = {
        "set_allocation": _validate_set_allocation,
        "trade_offer": _validate_trade_offer,
        "trade_response": _validate_trade_response,
        "policy_change": _validate_policy_change,
        "build_improvement": _validate_build_improvement,
        "train_unit": _validate_train_unit,
        "create_formation": _validate_create_formation,
        "assign_to_formation": _validate_assign_to_formation,
        "rename_formation": _validate_rename_formation,
        "create_group": _validate_create_group,
        "rename_group": _validate_rename_group,
        "assign_formation_to_group": _validate_assign_formation_to_group,
    }

    validator = validators.get(order.order_type)
    if validator:
        errors = validator(order)
    else:
        errors.append(f"Unknown order type: {order.order_type}")

    return errors


def _validate_set_allocation(order):
    """Validate sector allocation order.
    Payload: {"province_id": int, "allocations": [{"sector": str, "percentage": int}, ...]}
    """
    errors = []
    payload = order.payload

    if "province_id" not in payload:
        errors.append("Missing province_id")
        return errors

    if "allocations" not in payload:
        errors.append("Missing allocations")
        return errors

    allocations = payload["allocations"]
    valid_sectors = {"agriculture", "industry", "energy", "commerce", "military", "research"}

    sectors_seen = set()
    total = 0
    for alloc in allocations:
        sector = alloc.get("sector")
        pct = alloc.get("percentage", 0)

        if sector not in valid_sectors:
            errors.append(f"Invalid sector: {sector}")
        if sector in sectors_seen:
            errors.append(f"Duplicate sector: {sector}")
        sectors_seen.add(sector)

        if not isinstance(pct, int) or pct < 0 or pct > 100:
            errors.append(f"Invalid percentage for {sector}: {pct}")
        total += pct

    if sectors_seen != valid_sectors:
        missing = valid_sectors - sectors_seen
        errors.append(f"Missing sectors: {', '.join(missing)}")

    if total != 100:
        errors.append(f"Allocations must sum to 100, got {total}")

    # Verify province belongs to nation
    from provinces.models import Province
    try:
        province = Province.objects.get(pk=payload["province_id"])
        if province.nation_id != order.nation_id:
            errors.append("Province does not belong to this nation")
    except Province.DoesNotExist:
        errors.append("Province not found")

    return errors


def _validate_trade_offer(order):
    """Validate trade offer order.
    Payload: {"to_nation_id": int, "offering": {"resource": amount}, "requesting": {"resource": amount}}
    """
    errors = []
    payload = order.payload
    valid_resources = {"food", "materials", "energy", "wealth", "manpower", "research"}

    if "to_nation_id" not in payload:
        errors.append("Missing to_nation_id")

    for field in ["offering", "requesting"]:
        data = payload.get(field, {})
        if not data:
            errors.append(f"Missing or empty {field}")
            continue
        for key, val in data.items():
            if key not in valid_resources:
                errors.append(f"Invalid resource in {field}: {key}")
            if not isinstance(val, (int, float)) or val <= 0:
                errors.append(f"Invalid amount for {key} in {field}: {val}")

    return errors


def _validate_trade_response(order):
    """Validate trade response order.
    Payload: {"trade_offer_id": int, "action": "accept" | "reject"}
    """
    errors = []
    payload = order.payload

    if "trade_offer_id" not in payload:
        errors.append("Missing trade_offer_id")
    if payload.get("action") not in ("accept", "reject"):
        errors.append("Action must be 'accept' or 'reject'")

    return errors


def _validate_policy_change(order):
    """Validate policy change order.
    Payload for government component:
        {"change_type": "government", "component": str, "new_value": str}
        where component is one of: direction, economic_category, structure,
        power_origin, power_type.
    Payload for policy:
        {"change_type": "policy_level", "category": str, "new_level": int}
    """
    errors = []
    payload = order.payload

    change_type = payload.get("change_type")

    if change_type not in ("government", "policy_level"):
        errors.append("change_type must be 'government' or 'policy_level'")
        return errors

    if change_type == "government":
        from nations.government_constants import GOV_COMPONENTS
        component = payload.get("component")
        new_value = payload.get("new_value")
        if component not in GOV_COMPONENTS:
            valid = ", ".join(GOV_COMPONENTS.keys())
            errors.append(f"Invalid government component '{component}'. Choose from: {valid}")
        elif new_value not in GOV_COMPONENTS[component]:
            valid = ", ".join(GOV_COMPONENTS[component].keys())
            errors.append(
                f"Invalid value '{new_value}' for component '{component}'. "
                f"Choose from: {valid}"
            )
    elif change_type == "policy_level":
        from nations.policy_constants import POLICY_CATEGORIES
        category = payload.get("category")
        new_level = payload.get("new_level")

        if category not in POLICY_CATEGORIES:
            errors.append(f"Invalid policy category: {category}")
            return errors

        cat_def = POLICY_CATEGORIES[category]
        num_levels = len(cat_def["levels"])

        if not isinstance(new_level, int) or new_level < 0 or new_level >= num_levels:
            errors.append(f"Invalid level {new_level} for {category} (0-{num_levels - 1})")

    return errors


def _validate_build_improvement(order):
    """Validate build improvement order.
    Payload: {"province_id": int, "improvement_type": str}
    """
    errors = []
    payload = order.payload

    from provinces.constants import IMPROVEMENT_TYPES
    from provinces.models import Province, ProvinceImprovement

    province_id = payload.get("province_id")
    improvement_type = payload.get("improvement_type")

    if not province_id:
        errors.append("Missing province_id")
        return errors

    if improvement_type not in IMPROVEMENT_TYPES:
        errors.append(f"Invalid improvement type: {improvement_type}")
        return errors

    try:
        province = Province.objects.get(pk=province_id)
        if province.nation_id != order.nation_id:
            errors.append("Province does not belong to this nation")
            return errors
    except Province.DoesNotExist:
        errors.append("Province not found")
        return errors

    # Check if already at max level
    imp_def = IMPROVEMENT_TYPES[improvement_type]
    existing = ProvinceImprovement.objects.filter(
        province=province, improvement_type=improvement_type
    ).first()

    if existing:
        if existing.under_construction:
            errors.append("This improvement is already under construction")
        elif existing.level >= imp_def["max_level"]:
            errors.append(f"Already at max level ({imp_def['max_level']})")

    return errors


# ---------------------------------------------------------------------------
# Military order validators
# ---------------------------------------------------------------------------

def _validate_train_unit(order):
    """Validate train unit order.
    Payload: {
        "province_id": int,
        "unit_type": str,
        "quantity": int,
        "formation_id": int  (optional — uses/creates reserve formation if omitted)
    }
    Checks: province ownership, base exists & active, unit domain matches base,
    naval base requires coastal/river, goods/manpower available, one domain
    queue per province.
    """
    errors = []
    payload = order.payload

    from provinces.military_constants import (
        UNIT_TYPES, DOMAIN_UNITS, UNIT_DOMAINS, DOMAIN_TO_BASE,
    )
    from provinces.models import Province, MilitaryUnit, Formation
    from economy.models import NationGoodStock, NationResourcePool

    province_id = payload.get("province_id")
    unit_type = payload.get("unit_type")
    quantity = payload.get("quantity")
    formation_id = payload.get("formation_id")

    if not province_id:
        errors.append("Missing province_id")
        return errors
    if unit_type not in UNIT_TYPES:
        errors.append(f"Invalid unit_type: {unit_type}")
        return errors
    if not isinstance(quantity, int) or quantity < 1:
        errors.append("quantity must be a positive integer")
        return errors

    try:
        province = Province.objects.get(pk=province_id)
    except Province.DoesNotExist:
        errors.append("Province not found")
        return errors

    if province.nation_id != order.nation_id:
        errors.append("Province does not belong to this nation")
        return errors

    unit_def = UNIT_TYPES[unit_type]
    domain = unit_def["domain"]
    base_key = DOMAIN_TO_BASE[domain]

    # Base must exist, be active, and not under construction
    base = province.buildings.filter(
        building_type=base_key, is_active=True, under_construction=False
    ).first()
    if not base:
        errors.append(f"No active {base_key} in this province")
        return errors

    # Naval base requires coastal or river access
    if base_key == "naval_base" and not (province.is_coastal or province.is_river):
        errors.append("Naval Base requires a coastal or river province")
        return errors

    # One training queue per domain per province
    already_training = MilitaryUnit.objects.filter(
        training_province=province,
        quantity_in_training__gt=0,
    ).select_related("formation")
    for existing_unit in already_training:
        from provinces.military_constants import UNIT_TYPES as UT
        existing_domain = UT.get(existing_unit.unit_type, {}).get("domain")
        if existing_domain == domain:
            errors.append(
                f"A {domain} unit is already in training in this province"
            )
            return errors

    # Formation must belong to this nation (if specified)
    if formation_id is not None:
        if not Formation.objects.filter(pk=formation_id, nation_id=order.nation_id).exists():
            errors.append("Formation not found or does not belong to this nation")
            return errors

    # Check nation resources
    try:
        pool = NationResourcePool.objects.get(nation_id=order.nation_id)
    except NationResourcePool.DoesNotExist:
        errors.append("Nation resource pool not found")
        return errors

    goods_needed = unit_def["military_goods_cost"] * quantity
    manpower_needed = unit_def["manpower_cost"] * quantity

    try:
        good_stock = NationGoodStock.objects.get(nation_id=order.nation_id)
    except NationGoodStock.DoesNotExist:
        errors.append("Nation good stock not found")
        return errors

    if good_stock.military_goods < goods_needed:
        errors.append(
            f"Insufficient military_goods: need {goods_needed}, have {good_stock.military_goods:.0f}"
        )
    if pool.manpower < manpower_needed:
        errors.append(
            f"Insufficient manpower: need {manpower_needed}, have {pool.manpower:.0f}"
        )

    return errors


def _validate_create_formation(order):
    """Validate create formation order.
    Payload: {
        "name": str,
        "domain": "army"|"navy"|"air",
        "province_id": int,
        "group_id": int  (optional)
    }
    """
    errors = []
    payload = order.payload

    from provinces.models import Province, MilitaryGroup

    name = payload.get("name", "").strip()
    domain = payload.get("domain")
    province_id = payload.get("province_id")
    group_id = payload.get("group_id")

    if not name:
        errors.append("Missing or empty name")
    if domain not in ("army", "navy", "air"):
        errors.append("domain must be 'army', 'navy', or 'air'")
    if not province_id:
        errors.append("Missing province_id")
        return errors

    try:
        province = Province.objects.get(pk=province_id)
    except Province.DoesNotExist:
        errors.append("Province not found")
        return errors

    if province.nation_id != order.nation_id:
        errors.append("Province does not belong to this nation")

    if group_id is not None:
        if not MilitaryGroup.objects.filter(pk=group_id, nation_id=order.nation_id).exists():
            errors.append("Group not found or does not belong to this nation")

    return errors


def _validate_assign_to_formation(order):
    """Validate assign to formation order.
    Payload: {
        "unit_type": str,
        "quantity": int,
        "source_formation_id": int,
        "target_formation_id": int
    }
    """
    errors = []
    payload = order.payload

    from provinces.military_constants import UNIT_TYPES
    from provinces.models import Formation, MilitaryUnit

    unit_type = payload.get("unit_type")
    quantity = payload.get("quantity")
    source_id = payload.get("source_formation_id")
    target_id = payload.get("target_formation_id")

    if unit_type not in UNIT_TYPES:
        errors.append(f"Invalid unit_type: {unit_type}")
    if not isinstance(quantity, int) or quantity < 1:
        errors.append("quantity must be a positive integer")
    if not source_id or not target_id:
        errors.append("Missing source_formation_id or target_formation_id")
        return errors
    if source_id == target_id:
        errors.append("source and target formation must be different")
        return errors

    try:
        source = Formation.objects.get(pk=source_id, nation_id=order.nation_id)
    except Formation.DoesNotExist:
        errors.append("Source formation not found or does not belong to this nation")
        return errors

    try:
        target = Formation.objects.get(pk=target_id, nation_id=order.nation_id)
    except Formation.DoesNotExist:
        errors.append("Target formation not found or does not belong to this nation")
        return errors

    # Domain must match between formations
    from provinces.military_constants import UNIT_TYPES as UT
    unit_domain = UT.get(unit_type, {}).get("domain")
    if unit_domain and source.domain != unit_domain:
        errors.append(f"Unit {unit_type} is a {unit_domain} unit but source formation is {source.domain}")
    if unit_domain and target.domain != unit_domain:
        errors.append(f"Unit {unit_type} is a {unit_domain} unit but target formation is {target.domain}")

    # Check source has enough ready units
    if not errors:
        unit = MilitaryUnit.objects.filter(formation=source, unit_type=unit_type).first()
        if not unit or unit.quantity < quantity:
            available = unit.quantity if unit else 0
            errors.append(f"Source formation only has {available} {unit_type} (need {quantity})")

    return errors


def _validate_rename_formation(order):
    """Validate rename formation order.
    Payload: {"formation_id": int, "new_name": str}
    """
    errors = []
    payload = order.payload

    from provinces.models import Formation

    formation_id = payload.get("formation_id")
    new_name = payload.get("new_name", "").strip()

    if not formation_id:
        errors.append("Missing formation_id")
        return errors
    if not new_name:
        errors.append("Missing or empty new_name")

    if not Formation.objects.filter(pk=formation_id, nation_id=order.nation_id).exists():
        errors.append("Formation not found or does not belong to this nation")

    return errors


def _validate_create_group(order):
    """Validate create group order.
    Payload: {"name": str}
    """
    errors = []
    name = order.payload.get("name", "").strip()
    if not name:
        errors.append("Missing or empty name")
    return errors


def _validate_rename_group(order):
    """Validate rename group order.
    Payload: {"group_id": int, "new_name": str}
    """
    errors = []
    payload = order.payload

    from provinces.models import MilitaryGroup

    group_id = payload.get("group_id")
    new_name = payload.get("new_name", "").strip()

    if not group_id:
        errors.append("Missing group_id")
        return errors
    if not new_name:
        errors.append("Missing or empty new_name")

    if not MilitaryGroup.objects.filter(pk=group_id, nation_id=order.nation_id).exists():
        errors.append("Group not found or does not belong to this nation")

    return errors


def _validate_assign_formation_to_group(order):
    """Validate assign formation to group order.
    Payload: {"formation_id": int, "group_id": int | null}
    group_id null removes the formation from its current group.
    """
    errors = []
    payload = order.payload

    from provinces.models import Formation, MilitaryGroup

    formation_id = payload.get("formation_id")
    group_id = payload.get("group_id")

    if not formation_id:
        errors.append("Missing formation_id")
        return errors

    if not Formation.objects.filter(pk=formation_id, nation_id=order.nation_id).exists():
        errors.append("Formation not found or does not belong to this nation")
        return errors

    if group_id is not None:
        if not MilitaryGroup.objects.filter(pk=group_id, nation_id=order.nation_id).exists():
            errors.append("Group not found or does not belong to this nation")

    return errors
