"""
Population growth/decline simulation.

Two distinct processes run each turn:

1. Growth (calculate_province_growth_rate)
   Births minus deaths, driven by three combined signals:
     - Local food production vs local consumption  (dominant)
     - National food stockpile                     (supplement, overrides local deficits)
     - National stability                          (secondary modifier)
   Result: each province's population changes (national total changes).

2. Migration (simulate_migration)
   Living people move from provinces where conditions are causing population
   decline to provinces where conditions allow growth.
   Trigger: the growth rate computed in step 1.
     - Declining province (growth_rate < 0) → outflow proportional to |growth_rate|
     - Growing province  (growth_rate > 0) → receives migrants weighted by growth_rate
   Result: local populations shift; national total is conserved.

Growth curve (effective food ratio → base food contribution)
  0.0   →  −STARVATION_DECLINE_RATE  (−5%)
  0–1   →  linear interpolation to BASE_GROWTH_RATE
  1.0   →  BASE_GROWTH_RATE (+2%)
  1–3   →  rising to BASE + FOOD_SURPLUS_BONUS (+5%)
  ≥ 3   →  plateau at +5%

Stability adds ±5 pp at extremes (0 or 100).
Hard floor: effective_ratio == 0 (no food anywhere) always declines by at
least STARVATION_FLOOR regardless of stability or government modifiers.

Extensibility hook
------------------
`modifiers` dict in calculate_province_growth_rate.  Currently only "growth"
is read.  Future keys: "disease", "healthcare", "climate", "war_attrition", ...
"""

from .constants import FOOD_CONSUMPTION_PER_POP
from .literacy_constants import LITERACY_MIGRATION_SENSITIVITY

# --- Growth curve constants ---------------------------------------------------
#
# Turns are months.  A full game lasts 30+ years = 360+ turns.
# All per-turn rates are monthly; annualised equivalents shown in comments.

BASE_GROWTH_RATE = 0.003         # +0.3 %/month → ~3.7 %/year at effective_ratio == 1.0
FOOD_SURPLUS_BONUS = 0.002       # up to +0.2 %/month extra → ~6.2 %/year at full surplus
FOOD_SATIATION_RATIO = 3         # effective_ratio at which full surplus bonus is reached
                                  # (renamed from FOOD_SATIATION_TURNS; it is a dimensionless ratio)
STARVATION_DECLINE_RATE = 0.005  # −0.5 %/month → ~−5.8 %/year at effective_ratio == 0

# National stockpile supplement cap (dimensionless ratio, unchanged).
# A well-stocked granary can cover 3 months of a province's food needs,
# keeping non-food provinces in the growth regime.
MAX_NATIONAL_FOOD_SUPPLEMENT = 3.0

# Stability contribution: ±0.005/month at extremes (0 or 100) → ±6 %/year.
# Scaled down 10× from the annual value so stability is a secondary modifier,
# not the dominant growth driver.
STABILITY_GROWTH_FACTOR = 0.0001  # per point above/below neutral
STABILITY_NEUTRAL = 50.0

MIN_GROWTH_RATE = -0.010   # −1 %/month → ~−11.4 %/year
MAX_GROWTH_RATE =  0.008   #  +0.8 %/month → ~+10 %/year

# Hard floor when there is genuinely no food anywhere.
STARVATION_FLOOR = 0.001   # at least −0.1 %/month regardless of stability

# Starvation migration: fraction of the natural decline rate that leaves as
# migrants rather than dying.  At −0.5 %/month, outflow ≈ 0.15 %/month.
MIGRATION_RATE = 0.3

# Economic migration: 2 %/month of eligible subsistence workers move toward
# unfilled building jobs.  Over a year ~21 % of the eligible pool migrates —
# gradual enough that provinces don't drain in a single season.
ECONOMIC_MIGRATION_RATE = 0.02


# --- Public API ---------------------------------------------------------------

def calculate_province_growth_rate(
    food_produced: float,
    food_needed: float,
    national_stockpile: float,
    total_pop: int,
    national_stability: float,
    modifiers: dict | None = None,
) -> float:
    """
    Calculate the population growth rate for a single province this turn.

    Parameters
    ----------
    food_produced:
        Food produced by this province this turn (raw_production["food"]).
    food_needed:
        One turn's food consumption for this province's population
        (province.population × FOOD_CONSUMPTION_PER_POP).
    national_stockpile:
        Current NationResourcePool.food — the accumulated surplus including
        this turn's production.
    total_pop:
        Total national population across all provinces.  Used to compute the
        per-capita value of the national stockpile.
    national_stability:
        National stability (0–100).  Values above 50 add growth; below subtract.
    modifiers:
        Dict of named flat-rate offsets stacked after food + stability.
        Pass the full national_modifiers dict — only "growth" is consumed;
        unknown keys are silently ignored.

    Returns
    -------
    float
        Growth rate in [MIN_GROWTH_RATE, MAX_GROWTH_RATE].
        Positive → population grows; negative → population shrinks.
    """
    if modifiers is None:
        modifiers = {}

    # ------------------------------------------------------------------
    # 1. Effective food ratio
    # ------------------------------------------------------------------
    local_ratio = (food_produced / food_needed) if food_needed > 0 else 1.0
    local_ratio = max(0.0, local_ratio)

    # National supplement: per-capita stockpile expressed as turns of coverage.
    # A stockpile of 0 contributes nothing; large stockpiles are capped.
    if total_pop > 0 and FOOD_CONSUMPTION_PER_POP > 0:
        stockpile_per_cap = national_stockpile / total_pop
        national_supplement = min(
            stockpile_per_cap / FOOD_CONSUMPTION_PER_POP,
            MAX_NATIONAL_FOOD_SUPPLEMENT,
        )
    else:
        national_supplement = 0.0

    effective_ratio = local_ratio + national_supplement

    # ------------------------------------------------------------------
    # 2. Food contribution (piecewise growth curve)
    # ------------------------------------------------------------------
    if effective_ratio <= 0.0:
        food_rate = -STARVATION_DECLINE_RATE
    elif effective_ratio < 1.0:
        # Linear interpolation from starvation floor → base rate
        food_rate = -STARVATION_DECLINE_RATE + effective_ratio * (
            BASE_GROWTH_RATE + STARVATION_DECLINE_RATE
        )
    else:
        # Base rate + diminishing surplus bonus that plateaus at FOOD_SATIATION_TURNS
        surplus_progress = min(
            (effective_ratio - 1.0) / max(FOOD_SATIATION_RATIO - 1, 1),
            1.0,
        )
        food_rate = BASE_GROWTH_RATE + surplus_progress * FOOD_SURPLUS_BONUS

    # ------------------------------------------------------------------
    # 3. Stability contribution
    # ------------------------------------------------------------------
    stability_rate = (national_stability - STABILITY_NEUTRAL) * STABILITY_GROWTH_FACTOR

    # ------------------------------------------------------------------
    # 4. External modifiers
    # ------------------------------------------------------------------
    modifier_rate = modifiers.get("growth", 0.0)

    rate = food_rate + stability_rate + modifier_rate

    # Hard floor: no food anywhere (local + stockpile) → always decline.
    # Stability and modifiers can slow the decline but cannot reverse it.
    if effective_ratio <= 0.0:
        rate = min(rate, -STARVATION_FLOOR)

    return max(MIN_GROWTH_RATE, min(MAX_GROWTH_RATE, rate))


def simulate_migration(provinces, province_growth_rates):
    """
    Redistribute population from declining provinces to growing ones.

    Each province with a negative growth rate loses additional population to
    migration, proportional to the severity of its decline.  Where people go
    depends on whether any province in the nation is growing:

    - If growing provinces exist → internal migration.
      Migrants move to growing provinces weighted by their growth rate.
      National total population is conserved.

    - If ALL provinces are declining → external migration (nation-wide starvation).
      No internal destination exists, so migrants leave the nation entirely.
      National total population decreases by the migration outflow.

    Parameters
    ----------
    provinces:
        List of Province instances with up-to-date population values
        (i.e., after growth has been applied this turn).
    province_growth_rates:
        Dict of province.id → float growth rate as computed by
        calculate_province_growth_rate this turn.

    Returns
    -------
    dict[int, int]
        Net immigration count per province.id (positive = arrivals).
        Used by the security system to compute the immigration penalty.
    """
    sending = []    # list of (province, outflow_count)
    receiving = []  # list of (province, growth_rate_weight)
    net_immigration = {}  # province.id → migrants_in

    for province in provinces:
        rate = province_growth_rates.get(province.id, 0.0)
        if rate < 0:
            # Outflow proportional to decline severity; respect population floor.
            # Literate pops are more likely to migrate to better conditions.
            literacy_sensitivity = 1.0 + getattr(province, "literacy", 0.0) * LITERACY_MIGRATION_SENSITIVITY
            raw_outflow = int(province.population * abs(rate) * MIGRATION_RATE * literacy_sensitivity)
            actual_outflow = min(raw_outflow, province.population - 100)
            if actual_outflow > 0:
                sending.append((province, actual_outflow))
        elif rate > 0:
            # Weight destination by growth rate × happiness × security.
            # A province at base happiness (50) and security (30) is neutral.
            # Very unhappy or insecure provinces attract proportionally fewer migrants.
            happiness_mult = max(0.1, getattr(province, "local_happiness", 50.0) / 50.0)
            security_mult = max(0.1, getattr(province, "local_security", 30.0) / 50.0)
            weight = rate * happiness_mult * security_mult
            receiving.append((province, weight))

    if not sending:
        return net_immigration  # nobody is declining enough to trigger starvation migration

    total_migrants = sum(count for _, count in sending)

    # Deduct migrants from every declining province.
    for province, outflow in sending:
        province.population -= outflow
        province.save(update_fields=["population"])

    if not receiving:
        # Nation-wide starvation: no internal destination.
        # Migrants have already been deducted — they leave the nation entirely.
        return net_immigration

    # Internal migration: distribute to growing provinces weighted by growth rate.
    total_weight = sum(w for _, w in receiving)
    distributed = 0
    for i, (province, weight) in enumerate(receiving):
        if i == len(receiving) - 1:
            # Last province absorbs any rounding remainder.
            migrants_in = total_migrants - distributed
        else:
            migrants_in = int(total_migrants * weight / total_weight)
        province.population += migrants_in
        province.save(update_fields=["population"])
        distributed += migrants_in
        if migrants_in > 0:
            net_immigration[province.id] = net_immigration.get(province.id, 0) + migrants_in

    return net_immigration


def simulate_economic_migration(provinces, province_growth_rates, province_job_status):
    """
    Move subsistence workers toward provinces that have unfilled building jobs.

    Source provinces: have subsistence workers AND no local unfilled jobs
                      (i.e. their workers have no high-productivity option locally).
    Destination provinces: have unfilled building job slots AND are not declining
                           (growth_rate >= 0 — declining destinations deter migrants).

    If there are no eligible destinations, no economic migration occurs.
    National population is always conserved — this is internal movement only.

    Parameters
    ----------
    provinces : list of Province
        Province instances with current (post-growth, post-starvation-migration)
        population values.
    province_growth_rates : dict[province.id, float]
        Growth rates computed this turn by calculate_province_growth_rate.
    province_job_status : dict[province.id, dict]
        Job status snapshot from get_province_job_status.  Uses the values
        computed at production time; slight staleness after starvation migration
        is acceptable given the small magnitudes involved.
    """
    # --- Destinations: growing/stable provinces with unfilled building jobs ---
    # Attractiveness = unfilled_jobs × happiness_mult × security_mult.
    # Very unhappy or insecure provinces attract fewer economic migrants.
    destinations = []
    for province in provinces:
        status = province_job_status.get(province.id, {})
        rate = province_growth_rates.get(province.id, 0.0)
        if status.get("unfilled_jobs", 0) > 0 and rate >= 0:
            happiness_mult = max(0.1, getattr(province, "local_happiness", 50.0) / 50.0)
            security_mult = max(0.1, getattr(province, "local_security", 30.0) / 50.0)
            attractiveness = status["unfilled_jobs"] * happiness_mult * security_mult
            destinations.append((province, attractiveness))

    if not destinations:
        return {}  # no economic pull anywhere

    total_demand = sum(d for _, d in destinations)

    # --- Sources: provinces whose workers have no local building jobs ----------
    sending = []
    for province in provinces:
        status = province_job_status.get(province.id, {})
        # Only send from provinces where all building slots are filled (or absent)
        # and there are still subsistence workers who could earn more elsewhere.
        if status.get("subsistence_workers", 0) > 0 and status.get("unfilled_jobs", 0) == 0:
            raw = int(status["subsistence_workers"] * ECONOMIC_MIGRATION_RATE)
            actual = min(raw, province.population - 100)
            if actual > 0:
                sending.append((province, actual))

    if not sending:
        return {}

    total_supply = sum(m for _, m in sending)
    # Cap outflow so we never send more people than there are jobs to fill.
    total_migrants = min(total_supply, total_demand)

    # Deduct from sending provinces proportional to their available outflow.
    actual_sent = 0
    for province, outflow in sending:
        to_send = int(outflow * total_migrants / total_supply)
        if to_send > 0:
            province.population -= to_send
            province.save(update_fields=["population"])
            actual_sent += to_send

    # Distribute to destinations proportional to unfilled job count.
    net_immigration = {}
    distributed = 0
    for i, (province, demand) in enumerate(destinations):
        if i == len(destinations) - 1:
            migrants_in = actual_sent - distributed
        else:
            migrants_in = int(actual_sent * demand / total_demand)
        if migrants_in > 0:
            province.population += migrants_in
            province.save(update_fields=["population"])
            net_immigration[province.id] = net_immigration.get(province.id, 0) + migrants_in
        distributed += migrants_in

    return net_immigration
