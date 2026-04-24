"""
Province job system.

Every province has two tiers of employment:

1. Subsistence  (always available, automatic)
   - Employs all population not working in buildings
   - Produces the terrain's primary resource at SUBSISTENCE_RATE
   - Low output per worker; baseline production regardless of infrastructure

2. Building jobs  (high-productivity, requires construction)
   - Each active, completed building at level N provides
     BUILDING_TYPES[type]["levels"][N-1]["workers"] job slots
   - Workers fill building slots before doing subsistence
   - If province population < building job capacity, buildings operate at
     partial capacity (worker_capacity_factor < 1.0)

Manpower is a special case: no terrain naturally specialises in it, so every
province produces a small baseline from population (MANPOWER_PER_POP).

Extensibility
-------------
To add a new job-providing structure type (e.g. military units, infrastructure):
  1. Implement  _<type>_job_capacity(province) -> int
  2. Append it to  _JOB_CAPACITY_PROVIDERS

That's all.  get_province_total_job_capacity() and get_province_job_status()
pick it up automatically.
"""

from .building_constants import BUILDING_TYPES
from .constants import (
    TERRAIN_TYPES,
    SECTOR_RESOURCE_MAP,
    URBAN_BUILDING_WEIGHT,
    URBAN_THRESHOLD,
    URBAN_RUINS_URBAN_THRESHOLD,
)

# --- Constants ----------------------------------------------------------------

# Subsistence output per worker per turn.
# Calibrated so a plains province at 10 000 pop produces ~900 food/turn (with
# rural designation bonus), enough to generate a stockpile surplus that can
# supplement 1–2 importing provinces.  Deliberately lower than building output
# to make industrial investment meaningfully rewarding.
# Food kept at 0.05 (numéraire); non-food raised to 0.06 so manufactured-good
# inputs become cheaper to produce and non-food base prices fall proportionally.
SUBSISTENCE_RATE_FOOD = 0.05
SUBSISTENCE_RATE_NONFOOD = 0.06
# Back-compat alias; new code should use the _FOOD / _NONFOOD constants.
SUBSISTENCE_RATE = SUBSISTENCE_RATE_FOOD


def subsistence_rate_for(resource_key: str) -> float:
    """Return the per-worker subsistence output rate for the given resource."""
    return SUBSISTENCE_RATE_FOOD if resource_key == "food" else SUBSISTENCE_RATE_NONFOOD

# Manpower baseline produced per population unit per turn.
# Represents the latent military potential of a province.
# Scaled with the 10 000-pop baseline so a small 3-province nation accumulates
# ~500 manpower (Arms Factory L1 cost) in roughly 8–10 turns.
MANPOWER_PER_POP = 0.003


# --- Terrain helpers ----------------------------------------------------------

def terrain_primary_resource(terrain_type: str) -> str:
    """
    Return the resource key that this terrain is best suited to producing.

    Uses the highest sector multiplier in the terrain definition to pick the
    sector, then maps it to the corresponding resource via SECTOR_RESOURCE_MAP.
    Subsistence workers all produce this resource.
    """
    multipliers = TERRAIN_TYPES.get(terrain_type, {}).get("multipliers", {})
    if not multipliers:
        return "food"
    best_sector = max(multipliers, key=multipliers.get)
    return SECTOR_RESOURCE_MAP.get(best_sector, "food")


def terrain_best_multiplier(terrain_type: str) -> float:
    """Return the highest sector multiplier for this terrain type."""
    multipliers = TERRAIN_TYPES.get(terrain_type, {}).get("multipliers", {})
    return max(multipliers.values()) if multipliers else 1.0


# --- Per-type capacity functions (extensibility hook) -------------------------

def _building_job_capacity(province) -> int:
    """Job slots provided by active, completed buildings in a province."""
    total = 0
    for building in province.buildings.filter(is_active=True, under_construction=False):
        b_def = BUILDING_TYPES.get(building.building_type)
        if b_def and building.level >= 1:
            from provinces.building_constants import get_level_data
            total += get_level_data(building.building_type, building.level)["workers"]
    return total


# Registry: one entry per job-providing structure type.
# Add new callables here when new constructible types are introduced.
_JOB_CAPACITY_PROVIDERS = [
    _building_job_capacity,
    # Future: _military_unit_job_capacity,
    # Future: _infrastructure_job_capacity,
]


# --- Public API ---------------------------------------------------------------

def get_province_total_job_capacity(province) -> int:
    """Total high-productivity job slots across all structure types in a province."""
    return sum(fn(province) for fn in _JOB_CAPACITY_PROVIDERS)


def get_province_job_status(province) -> dict:
    """
    Return a complete employment snapshot for a province.

    Returns
    -------
    dict with keys:
        job_capacity          int    total building job slots
        filled_jobs           int    workers currently in building jobs
        unfilled_jobs         int    empty building slots (demand for migrants)
        subsistence_workers   int    workers in subsistence employment
        worker_capacity_factor float fraction of building slots filled (0.0–1.0)
    """
    job_capacity = get_province_total_job_capacity(province)
    filled_jobs = min(province.population, job_capacity)
    unfilled_jobs = max(0, job_capacity - filled_jobs)
    subsistence_workers = province.population - filled_jobs
    worker_capacity_factor = (filled_jobs / job_capacity) if job_capacity > 0 else 0.0

    return {
        "job_capacity": job_capacity,
        "filled_jobs": filled_jobs,
        "unfilled_jobs": unfilled_jobs,
        "subsistence_workers": subsistence_workers,
        "worker_capacity_factor": worker_capacity_factor,
    }


def calculate_province_designation(province, urban_threshold_reduction=0) -> str:
    """
    Determine the province's designation.

    Priority:
      1. capital  — overrides all others while is_capital is True.
                    Government-building bonuses are not yet implemented;
                    the designation is a placeholder for that future system.
      2. urban    — score ≥ threshold (threshold varies by terrain).
      3. post_urban — urban_ruins terrain below the urban threshold.
      4. rural    — everything else.

    Score = population + active completed buildings × URBAN_BUILDING_WEIGHT.

    Parameters
    ----------
    urban_threshold_reduction : int
        Flat reduction to the urban threshold (e.g. from industrialist trait).
    """
    if province.is_capital:
        return "capital"

    active_buildings = province.buildings.filter(
        is_active=True, under_construction=False
    ).count()
    score = province.population + active_buildings * URBAN_BUILDING_WEIGHT

    effective_threshold = max(10000, URBAN_THRESHOLD - urban_threshold_reduction)
    effective_ruins_threshold = max(10000, URBAN_RUINS_URBAN_THRESHOLD - urban_threshold_reduction)

    if province.terrain_type == "urban_ruins":
        return "urban" if score >= effective_ruins_threshold else "post_urban"
    return "urban" if score >= effective_threshold else "rural"
