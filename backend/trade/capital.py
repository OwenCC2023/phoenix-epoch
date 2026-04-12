"""
Capital relocation helpers.

Provides:
  initiate_capital_relocation(nation, target_province, current_turn, wartime)
      Deducts cost, creates CapitalRelocation row, returns it.

  process_capital_relocations(game, current_turn)
      Called each turn: completes any relocations that have matured.

  is_wartime_capital_loss(nation)
      True if the nation's current capital_province is owned by a different nation
      (enemy capture during wartime). Used to gate cheaper/instant relocation.
"""

from .constants import (
    CAPITAL_MOVE_COST_WEALTH_PEACE,
    CAPITAL_MOVE_COST_MATERIALS_PEACE,
    CAPITAL_MOVE_DELAY_TURNS,
    CAPITAL_MOVE_COST_WEALTH_WAR,
    CAPITAL_MOVE_COST_MATERIALS_WAR,
    CAPITAL_MOVE_DELAY_TURNS_WAR,
)
from .models import CapitalRelocation


def is_wartime_capital_loss(nation) -> bool:
    """Return True if the nation's current capital is held by an enemy nation."""
    cap = nation.capital_province
    if cap is None:
        return False
    return cap.nation_id != nation.pk


def get_relocation_cost(wartime: bool) -> dict:
    """Return the resource cost dict for a capital relocation."""
    if wartime:
        return {
            "wealth": CAPITAL_MOVE_COST_WEALTH_WAR,
            "materials": CAPITAL_MOVE_COST_MATERIALS_WAR,
        }
    return {
        "wealth": CAPITAL_MOVE_COST_WEALTH_PEACE,
        "materials": CAPITAL_MOVE_COST_MATERIALS_PEACE,
    }


def get_relocation_delay(wartime: bool) -> int:
    """Return the number of turns until the relocation completes."""
    return CAPITAL_MOVE_DELAY_TURNS_WAR if wartime else CAPITAL_MOVE_DELAY_TURNS


def validate_capital_relocation(nation, target_province, pool) -> list[str]:
    """Validate that a capital relocation can be initiated.

    Parameters
    ----------
    nation : Nation instance
    target_province : Province instance — proposed new capital
    pool : NationResourcePool instance

    Returns
    -------
    list[str] — error messages (empty = valid).
    """
    errors = []

    # Target must belong to this nation
    if target_province.nation_id != nation.pk:
        errors.append("Target province is not owned by your nation.")

    # Cannot relocate to current capital
    if nation.capital_province_id == target_province.pk:
        errors.append("That province is already the capital.")

    # Only one relocation in progress at a time
    if CapitalRelocation.objects.filter(nation=nation).exists():
        errors.append("A capital relocation is already in progress.")

    wartime = is_wartime_capital_loss(nation)
    cost = get_relocation_cost(wartime)

    if getattr(pool, "wealth", 0) < cost["wealth"]:
        errors.append(
            f"Insufficient wealth: need {cost['wealth']}, have {getattr(pool, 'wealth', 0):.0f}."
        )
    if getattr(pool, "materials", 0) < cost["materials"]:
        errors.append(
            f"Insufficient materials: need {cost['materials']}, have {getattr(pool, 'materials', 0):.0f}."
        )

    return errors


def initiate_capital_relocation(nation, target_province, pool, current_turn: int) -> CapitalRelocation:
    """Deduct costs, create CapitalRelocation, return the new row.

    Assumes validate_capital_relocation() was called and returned no errors.
    """
    wartime = is_wartime_capital_loss(nation)
    cost = get_relocation_cost(wartime)
    delay = get_relocation_delay(wartime)

    # Deduct resources
    pool.wealth -= cost["wealth"]
    pool.materials -= cost["materials"]
    pool.save(update_fields=["wealth", "materials"])

    relocation = CapitalRelocation.objects.create(
        nation=nation,
        target_province=target_province,
        started_turn=current_turn,
        completes_turn=current_turn + delay,
        cost_paid=cost,
    )
    return relocation


def process_capital_relocations(game, current_turn: int):
    """Complete any pending relocations whose completes_turn has arrived.

    Called from the turn engine after orders are processed.
    For each completed relocation:
      - Sets nation.capital_province to the target.
      - Updates Province.is_capital flags (old capital loses it, new gains it).
      - Inactivates all trade routes for the nation (path must be recomputed next turn).
      - Deletes the CapitalRelocation row.
    """
    from nations.models import Nation
    from provinces.models import Province
    from .models import TradeRoute

    ready = CapitalRelocation.objects.filter(
        nation__game=game,
        completes_turn__lte=current_turn,
    ).select_related("nation", "target_province")

    for relocation in ready:
        nation = relocation.nation
        new_capital = relocation.target_province

        # Clear old capital flag
        if nation.capital_province_id:
            Province.objects.filter(pk=nation.capital_province_id).update(is_capital=False)

        # Set new capital
        Province.objects.filter(pk=new_capital.pk).update(is_capital=True)
        nation.capital_province = new_capital
        nation.save(update_fields=["capital_province"])

        # Inactivate all trade routes — paths are based on capital position
        TradeRoute.objects.filter(
            game=game,
        ).filter(
            from_nation=nation,
        ).update(status=TradeRoute.Status.INACTIVE_WAR)

        TradeRoute.objects.filter(
            game=game,
        ).filter(
            to_nation=nation,
        ).update(status=TradeRoute.Status.INACTIVE_WAR)

        relocation.delete()
