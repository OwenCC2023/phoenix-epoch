"""
Disabling cascade rules — resolved to machine keys.

Auto-generated from policy_effects_complete.xlsx.
DO NOT EDIT MANUALLY. Re-generate with:
    ./backend/venv/Scripts/python.exe tools/import_from_excel.py

Disabling cascade:
    Traits -> Gov Options, Policies, Buildings
    Gov Options -> Policies
    Policies -> other Policies
"""


# Trait -> Gov Option disabling (17 rules)
# Key: (trait_name, strength) -> list of gov_option_key strings
TRAIT_GOV_DISABLES = {
    ('authoritarian', 'strong'): ['direct', 'elections'],
    ('devious', 'strong'): ['law_and_order'],
    ('ecologist', 'strong'): ['resource'],
    ('egalitarian', 'strong'): ['hereditary'],
    ('elitist', 'strong'): ['direct'],
    ('industrialist', 'strong'): ['subsistence'],
    ('internationalist', 'strong'): ['autarkic'],
    ('libertarian', 'strong'): ['singular'],
    ('militarist', 'strong'): ['direct'],
    ('modern', 'strong'): ['religious', 'hereditary'],
    ('nationalist', 'strong'): ['liberal'],
    ('pacifist', 'strong'): ['military_power'],
    ('positivist', 'strong'): ['religious'],
    ('spiritualist', 'strong'): ['liberal'],
    ('traditionalist', 'strong'): ['direct'],
}


# Trait -> Policy disabling (85 rules)
# Key: (trait_name, strength) -> list of (category_key, level_index) tuples
TRAIT_POLICY_DISABLES = {
    ('authoritarian', 'strong'): [('suffrage', 0), ('freedom_of_press', 4), ('freedom_of_speech', 3), ('freedom_of_association', 0), ('policing', 0)],
    ('collectivist', 'strong'): [('property_rights', 0), ('market', 0), ('firms', 3), ('income_tax', 3)],
    ('devious', 'strong'): [('anti_corruption_policy', 3), ('foreign_intelligence_agency', 0)],
    ('ecologist', 'strong'): [('conservation', 4), ('conservation', 3), ('resource_subsidies', 3)],
    ('egalitarian', 'strong'): [('slavery', 2), ('slavery', 3), ('racial_rights', 0), ('social_discrimination', 0), ('gender_rights', 3), ('suffrage', 4), ('land_ownership', 2)],
    ('elitist', 'strong'): [('suffrage', 0), ('income_tax', 4), ('land_ownership', 4), ('gift_and_estate_taxes', 2)],
    ('honorable', 'strong'): [('anti_corruption_policy', 0), ('policing', 2), ('punishments', 3), ('legal_system', 3), ('prison_system', 5), ('slavery', 2), ('slavery', 3)],
    ('individualist', 'strong'): [('property_rights', 3), ('market', 3), ('firms', 2), ('working_hours', 0), ('emmigration_policy', 0)],
    ('industrialist', 'strong'): [('conservation', 0), ('market', 4)],
    ('internationalist', 'strong'): [('immigration', 0), ('visa_policy', 0), ('emmigration_policy', 0), ('naturalization_laws', 6)],
    ('libertarian', 'strong'): [('martial_law', 0), ('freedom_of_movement', 3), ('freedom_of_association', 1), ('freedom_of_speech', 0), ('freedom_of_press', 0), ('domestic_intelligence_agency', 3), ('slavery', 2), ('slavery', 3), ('emmigration_policy', 0), ('property_rights', 3)],
    ('militarist', 'strong'): [('military_service', 0), ('mobilization', 0)],
    ('militarist', 'weak'): [('military_service', 0)],
    ('modern', 'strong'): [('education', 0), ('bureaucracy', 3), ('bureaucracy', 4), ('slavery', 2), ('slavery', 3)],
    ('nationalist', 'strong'): [('immigration', 3), ('immigration', 2), ('birthright_citizenship', 0), ('naturalization_laws', 1)],
    ('nationalist', 'weak'): [('immigration', 3)],
    ('pacifist', 'strong'): [('military_service', 5), ('military_service', 6), ('military_service', 7), ('mobilization', 2), ('mobilization', 3), ('martial_law', 0), ('child_labor', 3)],
    ('positivist', 'strong'): [('education', 0), ('drug_policy', 5), ('educational_philosophy', 1)],
    ('spiritualist', 'strong'): [('drug_policy', 0), ('vice', 0), ('sexuality', 3), ('educational_philosophy', 2)],
    ('traditionalist', 'strong'): [('sexuality', 3), ('gender_roles', 3), ('drug_policy', 0), ('educational_philosophy', 2), ('currency', 4)],
}


# Trait -> Building disabling (23 rules)
# Key: (trait_name, strength) -> list of building_type key strings
TRAIT_BUILDING_DISABLES = {
    ('authoritarian', 'strong'): ['workers_council'],
    ('collectivist', 'strong'): ['stock_exchange'],
    ('ecologist', 'strong'): ['refinery', 'advanced_refinery', 'oil_well', 'fuel_depot'],
    ('ecologist', 'weak'): ['refinery', 'advanced_refinery', 'oil_well', 'fuel_depot'],
    ('industrialist', 'strong'): ['wind_farm', 'solar_array'],
    ('libertarian', 'strong'): ['intelligence_agency'],
    ('pacifist', 'strong'): ['arms_factory', 'weapons_factory', 'military_academy', 'naval_war_college', 'air_force_academy'],
    ('pacifist', 'weak'): ['arms_factory', 'weapons_factory'],
    ('positivist', 'strong'): ['holy_site', 'madrasa'],
    ('spiritualist', 'strong'): ['theatre'],
}


# Gov Option -> Policy disabling (59 rules)
# Key: gov_option_key -> list of (category_key, level_index) tuples
GOV_POLICY_DISABLES = {
    'autarkic': [('immigration', 3), ('immigration', 2), ('currency', 5)],
    'bottom_up': [('martial_law', 0), ('domestic_intelligence_agency', 3), ('freedom_of_press', 0), ('freedom_of_speech', 0)],
    'collectivist': [('market', 0), ('property_rights', 0), ('firms', 3)],
    'direct': [('domestic_intelligence_agency', 3), ('policing', 5), ('freedom_of_speech', 0)],
    'economic_success': [('firms', 0), ('property_rights', 3)],
    'elections': [('suffrage', 4), ('freedom_of_press', 0), ('martial_law', 0), ('policing', 5)],
    'hereditary': [('suffrage', 0), ('bureaucracy', 6), ('bureaucracy', 5), ('gift_and_estate_taxes', 2)],
    'ideology': [('freedom_of_press', 4), ('freedom_of_speech', 3)],
    'large_body': [('martial_law', 0), ('domestic_intelligence_agency', 3)],
    'law_and_order': [('policing', 0), ('legal_system', 3), ('anti_corruption_policy', 0)],
    'liberal': [('market', 3), ('property_rights', 3), ('firms', 2), ('minimum_wage', 0)],
    'military_power': [('military_service', 0), ('suffrage', 0), ('unions', 3), ('freedom_of_press', 4), ('freedom_of_association', 0)],
    'multi_body': [('martial_law', 0)],
    'religious': [('freedom_of_speech', 3), ('sexuality', 3), ('drug_policy', 0), ('vice', 0), ('educational_philosophy', 2)],
    'representative': [('freedom_of_press', 0), ('suffrage', 4)],
    'singular': [('suffrage', 0), ('bureaucracy', 6), ('anti_corruption_policy', 3), ('freedom_of_press', 4)],
    'subsistence': [('industrial_subsidies', 3), ('firm_size', 3), ('firm_size', 2), ('currency', 0), ('healthcare', 2), ('education', 3)],
    'top_down': [('bureaucracy', 5), ('suffrage', 0)],
}


# Policy -> Policy disabling (48 rules)
# Each rule: (target_cat, target_level, when_cat, when_level)
# Meaning: target policy at target_level is disabled when when_cat is at when_level
POLICY_POLICY_DISABLES = [
    ('minimum_wage', 1, 'unions', 0),
    ('minimum_wage', 1, 'unions', 1),
    ('minimum_wage', 1, 'freedom_of_association', 2),
    ('minimum_wage', 1, 'freedom_of_association', 1),
    ('minimum_wage', 2, 'market', 3),
    ('minimum_wage', 2, 'firm_size', 0),
    ('minimum_wage', 0, 'market', 0),
    ('freedom_of_press', 4, 'freedom_of_speech', 0),
    ('freedom_of_press', 4, 'freedom_of_speech', 1),
    ('freedom_of_press', 3, 'firms', 2),
    ('freedom_of_press', 3, 'firms', 0),
    ('freedom_of_press', 0, 'market', 0),
    ('immigration', 3, 'emmigration_policy', 0),
    ('immigration', 0, 'visa_policy', 3),
    ('immigration', 2, 'emmigration_policy', 0),
    ('conservation', 0, 'property_rights', 2),
    ('bureaucracy', 6, 'suffrage', 4),
    ('bureaucracy', 4, 'racial_rights', 3),
    ('bureaucracy', 8, 'military_service', 0),
    ('bureaucracy', 0, 'education', 0),
    ('bureaucracy', 1, 'freedom_of_association', 0),
    ('suffrage', 0, 'freedom_of_speech', 0),
    ('slavery_type', 0, 'slavery', 0),
    ('slavery_type', 1, 'slavery', 0),
    ('slavery_type', 2, 'slavery', 0),
    ('slavery_type', 3, 'slavery', 0),
    ('slavery_type', 4, 'slavery', 0),
    ('child_labor', 3, 'military_service', 0),
    ('martial_law', 0, 'military_service', 0),
    ('military_recruitment_standards', 5, 'slavery', 0),
    ('military_recruitment_standards', 4, 'racial_rights', 3),
    ('family_planning', 2, 'healthcare', 2),
    ('family_planning', 5, 'freedom_of_association', 0),
    ('property_rights', 3, 'market', 0),
    ('property_rights', 3, 'firms', 3),
    ('firms', 3, 'property_rights', 3),
    ('working_hours', 3, 'mobilization', 3),
    ('working_hours', 3, 'mobilization', 2),
    ('gender_rights', 3, 'military_service', 5),
    ('gender_rights', 3, 'military_service', 6),
    ('drug_policy', 0, 'vice', 4),
    ('drug_policy', 5, 'healthcare', 2),
    ('civilian_firearm_ownership', 3, 'civilian_firearm_ownership', 0),
    ('educational_philosophy', 0, 'education', 0),
    ('educational_philosophy', 1, 'education', 0),
    ('educational_philosophy', 2, 'education', 0),
    ('government_salary', 0, 'anti_corruption_policy', 3),
    ('government_benefits', 0, 'anti_corruption_policy', 3),
]
