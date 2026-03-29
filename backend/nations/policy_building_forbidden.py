"""
Auto-generated policy -> building forbidden mappings from policy_effects_complete.xlsx.

DO NOT EDIT MANUALLY. Re-generate with:
    ./backend/venv/Scripts/python.exe tools/import_from_excel.py

Structure: POLICY_BUILDING_FORBIDDEN[(category_key, level_index)] = set of building_type keys
"""


POLICY_BUILDING_FORBIDDEN = {
    ('conservation', 0): {
        'logging_camp',
        'mine',
        'oil_well',
    },
    ('conservation', 1): {
        'oil_well',
    },
    ('education', 0): {
        'public_school',
        'university',
    },
    ('military_service', 0): {
        'air_base',
        'air_force_academy',
        'army_base',
        'military_academy',
        'naval_base',
        'naval_war_college',
    },
    ('property_rights', 3): {
        'bank',
        'stock_exchange',
    },
}
