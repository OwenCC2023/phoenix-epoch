# Security System — Detailed Reference

> System 8 documentation. See `CLAUDE.md` for the system index.

## Key files

```
economy/security_constants.py    — BASE_SECURITY, curve parameters, food/immigration penalty constants
economy/security.py              — get_security_stability_multiplier(), get_security_literacy_multiplier(),
                                   get_security_growth_bonus(), compute_province_security()
nations/security_policy_data.py  — SECURITY_POLICY_MULTIPLIERS (all 63 policy categories)
nations/policy_effects.py        — get_security_policy_multiplier(nation)
economy/literacy.py              — get_security_literacy_multiplier() called here
```

---

### 8. Security system

**What:** `Province.local_security` — a 0–100 metric (base 30) computed fresh each turn. Security acts as a multiplier on stability recovery and literacy, and provides a small growth bonus above 50.

**Formula:**
```
raw_security  = BASE_SECURITY (30) + sum(building "security" effects for this province)
modified      = raw_security × policy_security_mult × trait_security_mult
              + food_penalty (if food_ratio < 1.0)
              + immigration_penalty (if net migrants > 0 and not Internationalist)
province.local_security = clamp(modified, 0, 100)
```

**Downstream effects:**
- **Stability recovery:** `effective_recovery × get_security_stability_multiplier(security)` — linear 0→50 (0.5×–1.167×), logarithmic 50→100 (up to 1.5×). At base security 30: 0.9× multiplier.
- **Growth bonus:** `get_security_growth_bonus(security)` — 0.0 below 50; linear 0→+0.5%/month from 50→100.
- **Literacy:** `get_security_literacy_multiplier(security)` — linear 0→50 (0.7×–1.033×), logarithmic 50→100 (up to 1.2×). **Now wired** — multiplies literacy growth in `economy/literacy.py:compute_literacy_growth()`.

**Key constants** (`economy/security_constants.py`):
```
BASE_SECURITY = 30.0
SECURITY_FOOD_DEFICIT_PENALTY = -8.0   # food_ratio < 1.0
SECURITY_FOOD_SEVERE_PENALTY  = -15.0  # food_ratio < 0.5
SECURITY_IMMIGRATION_PENALTY_RATE = -0.5  # per 1% of pop that is new migrants
SECURITY_IMMIGRATION_PENALTY_CAP  = -10.0
```

**Policy security multipliers** (`nations/security_policy_data.py`):
- Stored separately from `POLICY_EFFECTS` (not merged into the additive effects dict).
- `SECURITY_POLICY_MULTIPLIERS[category][level]` → float (default 1.0 if absent).
- `get_security_policy_multiplier(nation)` in `policy_effects.py` returns the product of all active policy multipliers.
- Category A (policing, punishments, prison_system, martial_law, domestic_intelligence, firearm_ownership): range 0.70–1.30.
- Category B (legal_system, immigration, drug_policy, etc.): range 0.85–1.15.
- Category C (tax, education, civil rights, labour, market, etc.): range 0.93–1.05.
- Category D (currency, holidays, military admin, etc.): omitted = 1.0.

**Buildings producing security** (province-scope `"security"` effect key):
| Building | Security | Placement |
|----------|----------|-----------|
| `police_headquarters` | 10 | Urban only |
| `police_station` | 4 | Urban only |
| `sheriffs_office` | 5 | Rural only |
| `fire_house` | 2 | Any |
| `disaster_management` | 8 | Urban only |
| `telegraph_network` | 2 | Any |

**Placement flags** (`urban_only`, `rural_only` keys in `BUILDING_TYPES`): enforced in `BuildingView.post`. Urban = designation in `{"urban", "capital", "post_urban"}`; rural = `{"rural"}`.

**Immigration penalty timing:** Security is computed in the province loop before migration runs. After both `simulate_migration()` and `simulate_economic_migration()` complete (Step 13d), a corrective penalty is applied directly to `province.local_security` for provinces that received net immigrants this turn (waived if nation has `internationalist` as strong or weak trait).
