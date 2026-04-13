# Bureaucratic Capacity System — Detailed Reference

> System 14 documentation. See `CLAUDE.md` for the system index.

Nations must build government infrastructure to sustain ambitious regulatory or welfare programs. High-tier policies consume bureaucratic capacity; running a deficit reduces policy effectiveness and destabilises the government.

---

## Key Files

| File | Role |
|------|------|
| `backend/nations/bureaucratic_constants.py` | All static configuration (costs, classifications, multipliers) |
| `backend/nations/bureaucratic_capacity.py` | Core logic: supply/demand computation, validation, deficit penalties |
| `backend/nations/policy_effects.py` | `validate_policy_change()` — calls capacity check as step 6 |
| `backend/economy/simulation.py` | Calls `compute_bureaucratic_supply/demand` per turn; applies penalties |

---

## Supply Side

**Formula:** `total = building_base × (1 + policy_bonus) × gov_multiplier × trait_multiplier`

### Building base

Summed from all active buildings via `get_national_building_effects()`. Government, religious, and organisation buildings contribute flat capacity. Key examples:

| Building | Capacity |
|---------|---------|
| Administrative Center | 30 |
| Civil Service Academy | 25 |
| Workers' Committee | 10 |
| Standards Bureau | 12 |
| Audit Commission | 10 |
| Religious College | 15 |

### Policy bonus (multiplicative on building base)

The `bureaucratic_capacity` key in merged policy effects. Policies like the `bureaucracy` category can add or subtract fractional amounts (e.g. `+0.06` = ×1.06, `−0.03` = ×0.97). These stack additively then multiply the building base.

### Government multiplier

Product of all 5 axis values, clamped to [0.50, 2.00]:

| Axis / Value | Multiplier |
|-------------|-----------|
| `top_down` | 1.20 |
| `none` | 0.95 |
| `collectivist` | 1.10 |
| `resource` | 0.90 |
| `representative` | 1.10 |
| `elections` | 1.10 |
| `law_and_order` | 1.05 |
| `military_power` | 0.90 |
| `singular` | 1.20 |
| `multi_body` | 0.90 |
| `staggered_groups` | 0.80 |
| All others | 1.00 or 0.95 |

### Trait multiplier

| Trait | Strong | Weak |
|-------|--------|------|
| Modern | 1.15× | 1.08× |
| Libertarian | 0.85× | 0.92× |

---

## Demand Side

### Consuming tier rules

Only the top N tiers of a policy consume capacity, based on total tier count:

| Total tiers | Consuming tiers |
|------------|----------------|
| ≤3 | Top 1 |
| 4–5 | Top 2 |
| 6–7 | Top 3 |
| 8+ | Top 4 |

### Cost formula

`cost = base × 2^(position) × category_multiplier`

Where `position` is 0 for the lowest consuming tier, increasing toward the top:

| Position | Base cost |
|---------|----------|
| 0 (lowest consuming) | 5 |
| 1 | 10 |
| 2 | 20 |
| 3 (top, 8+ tier policies) | 40 |

### Category multipliers

| Type | Multiplier | Examples |
|------|-----------|---------|
| Business | 0.8× | industrial_subsidies, firms, currency, unions |
| Neutral / Government | 1.0× | military_service, bureaucracy, income_tax, policing |
| Individual | 1.2× | healthcare, education, freedom_of_speech, immigration |

### Exemptions (zero cost)

**Always exempt** (feminist, anti-slavery, racial equity policies):
`gender_rights`, `gender_roles`, `slavery`, `slavery_type`, `racial_rights`, `social_discrimination`

**Ecologist exemption** (zero cost at consuming tiers only):
`conservation`, `health_and_safety_regulations`, `drug_policy`

---

## Enforcement

### Policy change gate

`validate_policy_change()` in `policy_effects.py` runs bureaucratic capacity as check #6. If the proposed change would push total demand above total supply, the change is blocked with an error message showing the numbers.

Nations at capacity cannot raise policies to consuming tiers unless they build more government infrastructure or change government options/traits to increase supply.

### Turn simulation deficit penalty

If supply drops below demand mid-turn (e.g. a building is destroyed):

1. **Stability penalty:** `min(deficit_ratio × 100 × 0.5, 10.0)` stability points per turn.
2. **Policy benefit reduction:** All positive policy effects are scaled down proportionally. The most expensive policies lose benefits first (waterfall allocation: available capacity funds the cheapest policies first).

Negative policy effects (drawbacks, penalties) always apply at full force regardless of deficit.

The `global_benefit_factor` is a weighted average of per-policy funded fractions, applied uniformly to all positive values in the merged policy effects dict before simulation continues.

---

## Treaty Stub

`compute_treaty_bureaucratic_cost()` in `bureaucratic_capacity.py` returns `TREATY_BUREAUCRATIC_BASE_COST = 10`, reduced by the Internationalist trait (strong: 30%, weak: 15%). This is a placeholder — the full diplomacy system will consume treaty capacity per active treaty per turn.

The `treaty_bureaucratic_reduction` key is declared on Internationalist in `trait_constants.py`.

---

## Worked example

A nation with:
- 1× Administrative Center (capacity 30) + 1× Civil Service Academy (capacity 25) → building base = 55
- Bureaucracy policy at Skill Challenge System level (+0.04 bonus) → policy multiplier = 1.04
- `top_down` (1.20) + `collectivist` (1.10) + `representative` (1.10) + `elections` (1.10) + `singular` (1.20) → gov mult = 1.20×1.10×1.10×1.10×1.20 ≈ 1.918 → clamped to 2.00
- `modern` strong → trait mult = 1.15

**Total supply = 55 × 1.04 × 2.00 × 1.15 ≈ 131.6**

With healthcare at top tier (cost = 5×2×1.2 = 12) and military_service at top tier (cost = 5×2×1.0 = 10):
**Total demand = 22** — well within capacity.
