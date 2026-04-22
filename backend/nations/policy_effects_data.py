"""
Auto-generated policy effects data from policy_effects_complete.xlsx.

DO NOT EDIT MANUALLY. Re-generate with:
    ./backend/venv/Scripts/python.exe tools/import_from_excel.py
"""


# 63 policy categories with their levels and display names.
# Each category has a unique key, a display name, a default_level (0),
# and a list of levels with key, name, and description.
POLICY_CATEGORIES = {
    'military_service': {
        "name": 'Military Service',
        "default_level": 0,
        "levels": [
            {"key": 'disarmed_nation', "name": 'Disarmed Nation', "description": "", "tags": [], "effects": {}},
            {"key": 'volunteer_only', "name": 'Volunteer Only', "description": "", "tags": [], "effects": {}},
            {"key": 'limited_conscription', "name": 'Limited Conscription', "description": "", "tags": [], "effects": {}},
            {"key": 'extensive_conscription', "name": 'Extensive Conscription', "description": "", "tags": [], "effects": {}},
            {"key": 'service_by_requirement', "name": 'Service By Requirement', "description": "", "tags": [], "effects": {}},
            {"key": 'all_adults_serve', "name": 'All Adults Serve', "description": "", "tags": [], "effects": {}},
            {"key": 'scraping_the_barrel', "name": 'Scraping the Barrel', "description": "", "tags": [], "effects": {}},
            {"key": 'defense_of_berlin', "name": 'Defense of Berlin', "description": "", "tags": [], "effects": {}},
        ],
    },
    'policing': {
        "name": 'Policing',
        "default_level": 0,
        "levels": [
            {"key": 'what_police', "name": 'What Police?', "description": "", "tags": [], "effects": {}},
            {"key": 'town_watch', "name": 'Town Watch', "description": "", "tags": [], "effects": {}},
            {"key": 'corrupt', "name": 'Corrupt', "description": "", "tags": [], "effects": {}},
            {"key": 'protect_and_serve', "name": 'Protect and Serve', "description": "", "tags": [], "effects": {}},
            {"key": 'policing_through_fear', "name": 'Policing Through Fear', "description": "", "tags": [], "effects": {}},
            {"key": 'paramilitary_tactics', "name": 'Paramilitary Tactics', "description": "", "tags": [], "effects": {}},
        ],
    },
    'domestic_intelligence_agency': {
        "name": 'Domestic Intelligence Agency',
        "default_level": 0,
        "levels": [
            {"key": 'nonexistent', "name": 'Nonexistent', "description": "", "tags": [], "effects": {}},
            {"key": 'minimal', "name": 'Minimal', "description": "", "tags": [], "effects": {}},
            {"key": 'established', "name": 'Established', "description": "", "tags": [], "effects": {}},
            {"key": 'expansive', "name": 'Expansive', "description": "", "tags": [], "effects": {}},
        ],
    },
    'foreign_intelligence_agency': {
        "name": 'Foreign Intelligence Agency',
        "default_level": 0,
        "levels": [
            {"key": 'nonexistent', "name": 'Nonexistent', "description": "", "tags": [], "effects": {}},
            {"key": 'minimal', "name": 'Minimal', "description": "", "tags": [], "effects": {}},
            {"key": 'established', "name": 'Established', "description": "", "tags": [], "effects": {}},
            {"key": 'expansive', "name": 'Expansive', "description": "", "tags": [], "effects": {}},
        ],
    },
    'martial_law': {
        "name": 'Martial Law',
        "default_level": 0,
        "levels": [
            {"key": 'on', "name": 'On', "description": "", "tags": [], "effects": {}},
            {"key": 'off', "name": 'Off', "description": "", "tags": [], "effects": {}},
        ],
    },
    'bureaucracy': {
        "name": 'Bureaucracy',
        "default_level": 0,
        "levels": [
            {"key": 'mandarin_system', "name": 'Mandarin System', "description": "", "tags": [], "effects": {}},
            {"key": 'ecclesiastical_system', "name": 'Ecclesiastical System', "description": "", "tags": [], "effects": {}},
            {"key": 'patronage_system', "name": 'Patronage System', "description": "", "tags": [], "effects": {}},
            {"key": 'familial_system', "name": 'Familial System', "description": "", "tags": [], "effects": {}},
            {"key": 'racial_system', "name": 'Racial System', "description": "", "tags": [], "effects": {}},
            {"key": 'sortition', "name": 'Sortition', "description": "", "tags": [], "effects": {}},
            {"key": 'elected_officials', "name": 'Elected Officials', "description": "", "tags": [], "effects": {}},
            {"key": 'appointment', "name": 'Appointment', "description": "", "tags": [], "effects": {}},
            {"key": 'military', "name": 'Military', "description": "", "tags": [], "effects": {}},
            {"key": 'skill_challenge_system', "name": 'Skill Challenge System', "description": "", "tags": [], "effects": {}},
        ],
    },
    'legal_system': {
        "name": 'Legal System',
        "default_level": 0,
        "levels": [
            {"key": 'common_law', "name": 'Common Law', "description": "", "tags": [], "effects": {}},
            {"key": 'civil_code', "name": 'Civil Code', "description": "", "tags": [], "effects": {}},
            {"key": 'hammurabis_code', "name": "Hammurabi's Code", "description": "", "tags": [], "effects": {}},
            {"key": 'arbitrary', "name": 'Arbitrary', "description": "", "tags": [], "effects": {}},
        ],
    },
    'punishments': {
        "name": 'Punishments',
        "default_level": 0,
        "levels": [
            {"key": 'retribution', "name": 'Retribution', "description": "", "tags": [], "effects": {}},
            {"key": 'restitution', "name": 'Restitution', "description": "", "tags": [], "effects": {}},
            {"key": 'rehabilitation', "name": 'Rehabilitation', "description": "", "tags": [], "effects": {}},
            {"key": 'arbitrary', "name": 'Arbitrary', "description": "", "tags": [], "effects": {}},
        ],
    },
    'child_labor': {
        "name": 'Child Labor',
        "default_level": 0,
        "levels": [
            {"key": 'illegal', "name": 'Illegal', "description": "", "tags": [], "effects": {}},
            {"key": 'regulated', "name": 'Regulated', "description": "", "tags": [], "effects": {}},
            {"key": 'unrestricted', "name": 'Unrestricted', "description": "", "tags": [], "effects": {}},
            {"key": 'unrestricted_child_soldiers', "name": 'Unrestricted + Child Soldiers', "description": "", "tags": [], "effects": {}},
        ],
    },
    'unions': {
        "name": 'Unions',
        "default_level": 0,
        "levels": [
            {"key": 'illegal', "name": 'Illegal', "description": "", "tags": [], "effects": {}},
            {"key": 'legal_but_unprotected', "name": 'Legal but Unprotected', "description": "", "tags": [], "effects": {}},
            {"key": 'guilds_and_legal_monopolies', "name": 'Guilds and Legal Monopolies', "description": "", "tags": [], "effects": {}},
            {"key": 'legally_protected', "name": 'Legally Protected', "description": "", "tags": [], "effects": {}},
        ],
    },
    'land_ownership': {
        "name": 'Land Ownership',
        "default_level": 0,
        "levels": [
            {"key": 'unrestricted', "name": 'Unrestricted', "description": "", "tags": [], "effects": {}},
            {"key": 'restricted', "name": 'Restricted', "description": "", "tags": [], "effects": {}},
            {"key": 'elites_only', "name": 'Elites Only', "description": "", "tags": [], "effects": {}},
            {"key": 'homesteading', "name": 'Homesteading', "description": "", "tags": [], "effects": {}},
            {"key": 'communal_ownership', "name": 'Communal Ownership', "description": "", "tags": [], "effects": {}},
        ],
    },
    'property_rights': {
        "name": 'Property Rights',
        "default_level": 0,
        "levels": [
            {"key": 'private_property_only', "name": 'Private Property Only', "description": "", "tags": [], "effects": {}},
            {"key": 'limited_intervention', "name": 'Limited Intervention', "description": "", "tags": [], "effects": {}},
            {"key": 'unrestricted_seizure', "name": 'Unrestricted Seizure', "description": "", "tags": [], "effects": {}},
            {"key": 'private_property_illegal', "name": 'Private Property Illegal', "description": "", "tags": [], "effects": {}},
        ],
    },
    'slavery': {
        "name": 'Slavery',
        "default_level": 0,
        "levels": [
            {"key": 'illegal', "name": 'Illegal', "description": "", "tags": [], "effects": {}},
            {"key": 'rare', "name": 'Rare', "description": "", "tags": [], "effects": {}},
            {"key": 'common', "name": 'Common', "description": "", "tags": [], "effects": {}},
            {"key": 'slave_society', "name": 'Slave Society', "description": "", "tags": [], "effects": {}},
        ],
    },
    'industrial_subsidies': {
        "name": 'Industrial Subsidies',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'low', "name": 'Low', "description": "", "tags": [], "effects": {}},
            {"key": 'medium', "name": 'Medium', "description": "", "tags": [], "effects": {}},
            {"key": 'high', "name": 'High', "description": "", "tags": [], "effects": {}},
        ],
    },
    'resource_subsidies': {
        "name": 'Resource Subsidies',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'low', "name": 'Low', "description": "", "tags": [], "effects": {}},
            {"key": 'medium', "name": 'Medium', "description": "", "tags": [], "effects": {}},
            {"key": 'high', "name": 'High', "description": "", "tags": [], "effects": {}},
        ],
    },
    'agricultural_subsidies': {
        "name": 'Agricultural Subsidies',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'low', "name": 'Low', "description": "", "tags": [], "effects": {}},
            {"key": 'medium', "name": 'Medium', "description": "", "tags": [], "effects": {}},
            {"key": 'high', "name": 'High', "description": "", "tags": [], "effects": {}},
        ],
    },
    'freedom_of_movement': {
        "name": 'Freedom of Movement',
        "default_level": 0,
        "levels": [
            {"key": 'unrestricted', "name": 'Unrestricted', "description": "", "tags": [], "effects": {}},
            {"key": 'restricted', "name": 'Restricted', "description": "", "tags": [], "effects": {}},
            {"key": 'elites_only', "name": 'Elites Only', "description": "", "tags": [], "effects": {}},
            {"key": 'illegal', "name": 'Illegal', "description": "", "tags": [], "effects": {}},
        ],
    },
    'freedom_of_association': {
        "name": 'Freedom of Association',
        "default_level": 0,
        "levels": [
            {"key": 'unrestricted', "name": 'Unrestricted', "description": "", "tags": [], "effects": {}},
            {"key": 'approved_organizations_only', "name": 'Approved Organizations Only', "description": "", "tags": [], "effects": {}},
            {"key": 'non_unions_only', "name": 'Non-Unions Only', "description": "", "tags": [], "effects": {}},
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
        ],
    },
    'freedom_of_press': {
        "name": 'Freedom of Press',
        "default_level": 0,
        "levels": [
            {"key": 'government_owned', "name": 'Government Owned', "description": "", "tags": [], "effects": {}},
            {"key": 'heavily_censored', "name": 'Heavily Censored', "description": "", "tags": [], "effects": {}},
            {"key": 'limited_censorship', "name": 'Limited Censorship', "description": "", "tags": [], "effects": {}},
            {"key": 'press_barons', "name": 'Press Barons', "description": "", "tags": [], "effects": {}},
            {"key": 'unrestricted', "name": 'Unrestricted', "description": "", "tags": [], "effects": {}},
        ],
    },
    'freedom_of_speech': {
        "name": 'Freedom of Speech',
        "default_level": 0,
        "levels": [
            {"key": 'criticism_forbidden', "name": 'Criticism Forbidden', "description": "", "tags": [], "effects": {}},
            {"key": 'restricted', "name": 'Restricted', "description": "", "tags": [], "effects": {}},
            {"key": 'limited', "name": 'Limited', "description": "", "tags": [], "effects": {}},
            {"key": 'unrestricted', "name": 'Unrestricted', "description": "", "tags": [], "effects": {}},
        ],
    },
    'education': {
        "name": 'Education',
        "default_level": 0,
        "levels": [
            {"key": 'no_public_schools', "name": 'No public schools', "description": "", "tags": [], "effects": {}},
            {"key": 'mandatory_primary_education', "name": 'Mandatory primary education', "description": "", "tags": [], "effects": {}},
            {"key": 'mandatory_secondary_education', "name": 'Mandatory secondary education', "description": "", "tags": [], "effects": {}},
            {"key": 'mandatory_secondary_and_free_tertiary', "name": 'Mandatory secondary and free tertiary', "description": "", "tags": [], "effects": {}},
        ],
    },
    'pensions': {
        "name": 'Pensions',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'low', "name": 'Low', "description": "", "tags": [], "effects": {}},
            {"key": 'medium', "name": 'Medium', "description": "", "tags": [], "effects": {}},
            {"key": 'high', "name": 'High', "description": "", "tags": [], "effects": {}},
        ],
    },
    'healthcare': {
        "name": 'Healthcare',
        "default_level": 0,
        "levels": [
            {"key": 'private', "name": 'Private', "description": "", "tags": [], "effects": {}},
            {"key": 'subsidized', "name": 'Subsidized', "description": "", "tags": [], "effects": {}},
            {"key": 'universal', "name": 'Universal', "description": "", "tags": [], "effects": {}},
        ],
    },
    'immigration': {
        "name": 'Immigration',
        "default_level": 0,
        "levels": [
            {"key": 'closed_borders', "name": 'Closed Borders', "description": "", "tags": [], "effects": {}},
            {"key": 'visa_program', "name": 'Visa Program', "description": "", "tags": [], "effects": {}},
            {"key": 'open_borders', "name": 'Open Borders', "description": "", "tags": [], "effects": {}},
            {"key": 'no_borders', "name": 'No Borders', "description": "", "tags": [], "effects": {}},
        ],
    },
    'vice': {
        "name": 'Vice',
        "default_level": 0,
        "levels": [
            {"key": 'universally_legal', "name": 'Universally Legal', "description": "", "tags": [], "effects": {}},
            {"key": 'some_legal', "name": 'Some Legal', "description": "", "tags": [], "effects": {}},
            {"key": 'geographic_restrictions', "name": 'Geographic Restrictions', "description": "", "tags": [], "effects": {}},
            {"key": 'decriminalized', "name": 'Decriminalized', "description": "", "tags": [], "effects": {}},
            {"key": 'prohibited', "name": 'Prohibited', "description": "", "tags": [], "effects": {}},
        ],
    },
    'civilian_firearm_ownership': {
        "name": 'Civilian Firearm Ownership',
        "default_level": 0,
        "levels": [
            {"key": 'citizen_service', "name": 'Citizen Service', "description": "", "tags": [], "effects": {}},
            {"key": 'unrestricted', "name": 'Unrestricted', "description": "", "tags": [], "effects": {}},
            {"key": 'controlled', "name": 'Controlled', "description": "", "tags": [], "effects": {}},
            {"key": 'banned', "name": 'Banned', "description": "", "tags": [], "effects": {}},
        ],
    },
    'suffrage': {
        "name": 'Suffrage',
        "default_level": 0,
        "levels": [
            {"key": 'universal_suffrage', "name": 'Universal Suffrage', "description": "", "tags": [], "effects": {}},
            {"key": 'unequal_value_votes', "name": 'Unequal Value Votes', "description": "", "tags": [], "effects": {}},
            {"key": 'universal_single_class', "name": 'Universal Single-Class', "description": "", "tags": [], "effects": {}},
            {"key": 'limited', "name": 'Limited', "description": "", "tags": [], "effects": {}},
            {"key": 'no_suffrage', "name": 'No Suffrage', "description": "", "tags": [], "effects": {}},
        ],
    },
    'gender_rights': {
        "name": 'Gender Rights',
        "default_level": 0,
        "levels": [
            {"key": 'equal_rights', "name": 'Equal Rights', "description": "", "tags": [], "effects": {}},
            {"key": 'allowed_to_work', "name": 'Allowed to Work', "description": "", "tags": [], "effects": {}},
            {"key": 'battle_thralls', "name": 'Battle Thralls', "description": "", "tags": [], "effects": {}},
            {"key": 'homemakers', "name": 'Homemakers', "description": "", "tags": [], "effects": {}},
        ],
    },
    'racial_rights': {
        "name": 'Racial Rights',
        "default_level": 0,
        "levels": [
            {"key": 'exclusivity', "name": 'Exclusivity', "description": "", "tags": [], "effects": {}},
            {"key": 'separate_but_equal', "name": 'Separate But Equal', "description": "", "tags": [], "effects": {}},
            {"key": 'castes', "name": 'Castes', "description": "", "tags": [], "effects": {}},
            {"key": 'equal_rights', "name": 'Equal Rights', "description": "", "tags": [], "effects": {}},
        ],
    },
    'income_tax': {
        "name": 'Income Tax',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'flat', "name": 'Flat', "description": "", "tags": [], "effects": {}},
            {"key": 'progressive', "name": 'Progressive', "description": "", "tags": [], "effects": {}},
            {"key": 'regressive', "name": 'Regressive', "description": "", "tags": [], "effects": {}},
            {"key": 'wealth_redistribution', "name": 'Wealth Redistribution', "description": "", "tags": [], "effects": {}},
        ],
    },
    'consumption_tax': {
        "name": 'Consumption Tax',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'basic_goods_exempted', "name": 'Basic Goods Exempted', "description": "", "tags": [], "effects": {}},
            {"key": 'all_goods', "name": 'All Goods', "description": "", "tags": [], "effects": {}},
            {"key": 'sin_tax', "name": 'Sin Tax', "description": "", "tags": [], "effects": {}},
            {"key": 'health_tax', "name": 'Health Tax', "description": "", "tags": [], "effects": {}},
        ],
    },
    'land_tax': {
        "name": 'Land Tax',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'property_tax', "name": 'Property Tax', "description": "", "tags": [], "effects": {}},
            {"key": 'land_value_tax', "name": 'Land Value Tax', "description": "", "tags": [], "effects": {}},
            {"key": 'both', "name": 'Both', "description": "", "tags": [], "effects": {}},
        ],
    },
    'gift_and_estate_taxes': {
        "name": 'Gift & Estate Taxes',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'meritocratic_intentions', "name": 'Meritocratic Intentions', "description": "", "tags": [], "effects": {}},
            {"key": 'strict_meritocracy', "name": 'Strict Meritocracy', "description": "", "tags": [], "effects": {}},
            {"key": 'communal_duties', "name": 'Communal Duties', "description": "", "tags": [], "effects": {}},
        ],
    },
    'gender_roles': {
        "name": 'Gender Roles',
        "default_level": 0,
        "levels": [
            {"key": 'strictly_enforced', "name": 'Strictly Enforced', "description": "", "tags": [], "effects": {}},
            {"key": 'expected', "name": 'Expected', "description": "", "tags": [], "effects": {}},
            {"key": 'regularly_defied', "name": 'Regularly Defied', "description": "", "tags": [], "effects": {}},
            {"key": 'minimal', "name": 'Minimal', "description": "", "tags": [], "effects": {}},
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
        ],
    },
    'social_discrimination': {
        "name": 'Social Discrimination',
        "default_level": 0,
        "levels": [
            {"key": 'enshrined_in_law', "name": 'Enshrined in Law', "description": "", "tags": [], "effects": {}},
            {"key": 'extensive', "name": 'Extensive', "description": "", "tags": [], "effects": {}},
            {"key": 'common', "name": 'Common', "description": "", "tags": [], "effects": {}},
            {"key": 'limited', "name": 'Limited', "description": "", "tags": [], "effects": {}},
            {"key": 'minimal', "name": 'Minimal', "description": "", "tags": [], "effects": {}},
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
        ],
    },
    'sexuality': {
        "name": 'Sexuality',
        "default_level": 0,
        "levels": [
            {"key": 'rigid', "name": 'Rigid', "description": "", "tags": [], "effects": {}},
            {"key": 'conservative', "name": 'Conservative', "description": "", "tags": [], "effects": {}},
            {"key": 'liberal', "name": 'Liberal', "description": "", "tags": [], "effects": {}},
            {"key": 'open', "name": 'Open', "description": "", "tags": [], "effects": {}},
        ],
    },
    'conservation': {
        "name": 'Conservation',
        "default_level": 0,
        "levels": [
            {"key": 'priority', "name": 'Priority', "description": "", "tags": [], "effects": {}},
            {"key": 'important', "name": 'Important', "description": "", "tags": [], "effects": {}},
            {"key": 'unimportant', "name": 'Unimportant', "description": "", "tags": [], "effects": {}},
            {"key": 'irrelevant', "name": 'Irrelevant', "description": "", "tags": [], "effects": {}},
            {"key": 'humanity_first', "name": 'Humanity First', "description": "", "tags": [], "effects": {}},
        ],
    },
    'prison_system': {
        "name": 'Prison System',
        "default_level": 0,
        "levels": [
            {"key": 'penal_colony', "name": 'Penal Colony', "description": "", "tags": [], "effects": {}},
            {"key": 'correctional_facilities', "name": 'Correctional Facilities', "description": "", "tags": [], "effects": {}},
            {"key": 'labour_camp', "name": 'Labour Camp', "description": "", "tags": [], "effects": {}},
            {"key": 'solitary_confinement', "name": 'Solitary Confinement', "description": "", "tags": [], "effects": {}},
            {"key": 'home_confinement', "name": 'Home Confinement', "description": "", "tags": [], "effects": {}},
            {"key": 'experimentation', "name": 'Experimentation', "description": "", "tags": [], "effects": {}},
            {"key": 'penal_brigades', "name": 'Penal Brigades', "description": "", "tags": [], "effects": {}},
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
        ],
    },
    'drug_policy': {
        "name": 'Drug Policy',
        "default_level": 0,
        "levels": [
            {"key": 'all_drugs_are_legal', "name": 'All Drugs are Legal', "description": "", "tags": [], "effects": {}},
            {"key": 'uncontrolled_recreational_use', "name": 'Uncontrolled Recreational Use', "description": "", "tags": [], "effects": {}},
            {"key": 'limited_controls', "name": 'Limited Controls', "description": "", "tags": [], "effects": {}},
            {"key": 'tightly_controlled', "name": 'Tightly Controlled', "description": "", "tags": [], "effects": {}},
            {"key": 'prohibition', "name": 'Prohibition', "description": "", "tags": [], "effects": {}},
            {"key": 'christian_science', "name": 'Christian Science', "description": "", "tags": [], "effects": {}},
        ],
    },
    'educational_philosophy': {
        "name": 'Educational Philosophy',
        "default_level": 0,
        "levels": [
            {"key": 'essentialist', "name": 'Essentialist', "description": "", "tags": [], "effects": {}},
            {"key": 'perennialist', "name": 'Perennialist', "description": "", "tags": [], "effects": {}},
            {"key": 'progressive', "name": 'Progressive', "description": "", "tags": [], "effects": {}},
        ],
    },
    'slavery_type': {
        "name": 'Slavery Type',
        "default_level": 0,
        "levels": [
            {"key": 'serfdom', "name": 'Serfdom', "description": "", "tags": [], "effects": {}},
            {"key": 'bondage_slavery', "name": 'Bondage Slavery', "description": "", "tags": [], "effects": {}},
            {"key": 'informal_servitude', "name": 'Informal Servitude', "description": "", "tags": [], "effects": {}},
            {"key": 'chattel_slavery', "name": 'Chattel Slavery', "description": "", "tags": [], "effects": {}},
            {"key": 'pow_slavery', "name": 'POW Slavery', "description": "", "tags": [], "effects": {}},
        ],
    },
    'firms': {
        "name": 'Firms',
        "default_level": 0,
        "levels": [
            {"key": 'predominantly_illegal', "name": 'Predominantly Illegal', "description": "", "tags": [], "effects": {}},
            {"key": 'predominantly_worker_owned', "name": 'Predominantly Worker Owned', "description": "", "tags": [], "effects": {}},
            {"key": 'predominantly_state_owned', "name": 'Predominantly State Owned', "description": "", "tags": [], "effects": {}},
            {"key": 'predominantly_privately_owned', "name": 'Predominantly Privately Owned', "description": "", "tags": [], "effects": {}},
        ],
    },
    'market': {
        "name": 'Market',
        "default_level": 0,
        "levels": [
            {"key": 'free_and_unregulated', "name": 'Free & Unregulated', "description": "", "tags": [], "effects": {}},
            {"key": 'loosely_regulated', "name": 'Loosely Regulated', "description": "", "tags": [], "effects": {}},
            {"key": 'tightly_regulated', "name": 'Tightly Regulated', "description": "", "tags": [], "effects": {}},
            {"key": 'command_economy', "name": 'Command Economy', "description": "", "tags": [], "effects": {}},
            {"key": 'alternative', "name": 'Alternative', "description": "", "tags": [], "effects": {}},
        ],
    },
    'firm_size': {
        "name": 'Firm Size',
        "default_level": 0,
        "levels": [
            {"key": 'small', "name": 'Small', "description": "", "tags": [], "effects": {}},
            {"key": 'medium', "name": 'Medium', "description": "", "tags": [], "effects": {}},
            {"key": 'large', "name": 'Large', "description": "", "tags": [], "effects": {}},
            {"key": 'all_encompassing', "name": 'All-Encompassing', "description": "", "tags": [], "effects": {}},
        ],
    },
    'currency': {
        "name": 'Currency',
        "default_level": 0,
        "levels": [
            {"key": 'fiat', "name": 'Fiat', "description": "", "tags": [], "effects": {}},
            {"key": 'single_commodity', "name": 'Single Commodity', "description": "", "tags": [], "effects": {}},
            {"key": 'multiple_commodity', "name": 'Multiple Commodity', "description": "", "tags": [], "effects": {}},
            {"key": 'ration_card', "name": 'Ration Card', "description": "", "tags": [], "effects": {}},
            {"key": 'energy_credit', "name": 'Energy Credit', "description": "", "tags": [], "effects": {}},
            {"key": 'foreign_currency', "name": 'Foreign Currency', "description": "", "tags": [], "effects": {}},
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
        ],
    },
    'government_salary': {
        "name": 'Government Salary',
        "default_level": 0,
        "levels": [
            {"key": 'parasitic', "name": 'Parasitic', "description": "", "tags": [], "effects": {}},
            {"key": 'high', "name": 'High', "description": "", "tags": [], "effects": {}},
            {"key": 'competitive', "name": 'Competitive', "description": "", "tags": [], "effects": {}},
            {"key": 'low', "name": 'Low', "description": "", "tags": [], "effects": {}},
            {"key": 'minimal', "name": 'Minimal', "description": "", "tags": [], "effects": {}},
        ],
    },
    'government_benefits': {
        "name": 'Government Benefits',
        "default_level": 0,
        "levels": [
            {"key": 'parasitic', "name": 'Parasitic', "description": "", "tags": [], "effects": {}},
            {"key": 'high', "name": 'High', "description": "", "tags": [], "effects": {}},
            {"key": 'competitive', "name": 'Competitive', "description": "", "tags": [], "effects": {}},
            {"key": 'low', "name": 'Low', "description": "", "tags": [], "effects": {}},
            {"key": 'minimal', "name": 'Minimal', "description": "", "tags": [], "effects": {}},
        ],
    },
    'naturalization_laws': {
        "name": 'Naturalization Laws',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": '1_3_years', "name": '1-3 Years', "description": "", "tags": [], "effects": {}},
            {"key": '4_7_years', "name": '4-7 Years', "description": "", "tags": [], "effects": {}},
            {"key": '8_10_years', "name": '8-10 Years', "description": "", "tags": [], "effects": {}},
            {"key": '11_years', "name": '11+ Years', "description": "", "tags": [], "effects": {}},
            {"key": 'special', "name": 'Special', "description": "", "tags": [], "effects": {}},
            {"key": 'never', "name": 'Never', "description": "", "tags": [], "effects": {}},
        ],
    },
    'visa_policy': {
        "name": 'Visa Policy',
        "default_level": 0,
        "levels": [
            {"key": 'closed_system', "name": 'Closed System', "description": "", "tags": [], "effects": {}},
            {"key": 'tourism_only', "name": 'Tourism Only', "description": "", "tags": [], "effects": {}},
            {"key": 'invitation_only', "name": 'Invitation Only', "description": "", "tags": [], "effects": {}},
            {"key": 'visa_on_arrival', "name": 'Visa on Arrival', "description": "", "tags": [], "effects": {}},
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
        ],
    },
    'birthright_citizenship': {
        "name": 'Birthright Citizenship',
        "default_level": 0,
        "levels": [
            {"key": 'jus_soli', "name": 'Jus Soli', "description": "", "tags": [], "effects": {}},
            {"key": 'jus_sanguinis', "name": 'Jus sanguinis', "description": "", "tags": [], "effects": {}},
            {"key": 'jus_soli_and_sanguinis', "name": 'Jus soli & sanguinis', "description": "", "tags": [], "effects": {}},
            {"key": 'leges_sanguinis', "name": 'Leges sanguinis', "description": "", "tags": [], "effects": {}},
            {"key": 'fieri_nequit', "name": 'Fieri Nequit', "description": "", "tags": [], "effects": {}},
        ],
    },
    'minimum_wage': {
        "name": 'Minimum Wage',
        "default_level": 0,
        "levels": [
            {"key": 'state_determined', "name": 'State Determined', "description": "", "tags": [], "effects": {}},
            {"key": 'collective_bargaining', "name": 'Collective Bargaining', "description": "", "tags": [], "effects": {}},
            {"key": 'monopoly_set', "name": 'Monopoly Set', "description": "", "tags": [], "effects": {}},
            {"key": 'symbolic', "name": 'Symbolic', "description": "", "tags": [], "effects": {}},
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
        ],
    },
    'working_hours': {
        "name": 'Working Hours',
        "default_level": 0,
        "levels": [
            {"key": 'live_to_work', "name": 'Live to Work', "description": "", "tags": [], "effects": {}},
            {"key": '60_hours', "name": '60 Hours', "description": "", "tags": [], "effects": {}},
            {"key": '40_hours', "name": '40 Hours', "description": "", "tags": [], "effects": {}},
            {"key": 'work_to_live', "name": 'Work to Live', "description": "", "tags": [], "effects": {}},
        ],
    },
    'holidays': {
        "name": 'Holidays',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'weekend_protections', "name": 'Weekend Protections', "description": "", "tags": [], "effects": {}},
            {"key": 'holidays_only', "name": 'Holidays Only', "description": "", "tags": [], "effects": {}},
            {"key": 'two_weeks', "name": 'Two Weeks', "description": "", "tags": [], "effects": {}},
            {"key": 'four_weeks', "name": 'Four Weeks', "description": "", "tags": [], "effects": {}},
        ],
    },
    'maternity_leave': {
        "name": 'Maternity Leave',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": '6_weeks', "name": '6 Weeks', "description": "", "tags": [], "effects": {}},
            {"key": '12_weeks', "name": '12 Weeks', "description": "", "tags": [], "effects": {}},
            {"key": '16_weeks', "name": '16 Weeks', "description": "", "tags": [], "effects": {}},
        ],
    },
    'paternity_leave': {
        "name": 'Paternity Leave',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": '6_weeks', "name": '6 Weeks', "description": "", "tags": [], "effects": {}},
            {"key": '12_weeks', "name": '12 Weeks', "description": "", "tags": [], "effects": {}},
            {"key": '16_weeks', "name": '16 Weeks', "description": "", "tags": [], "effects": {}},
        ],
    },
    'health_and_safety_regulations': {
        "name": 'Health & Safety Regulations',
        "default_level": 0,
        "levels": [
            {"key": 'no_health_and_safety', "name": 'No Health & Safety', "description": "", "tags": [], "effects": {}},
            {"key": 'minimal_health_and_safety', "name": 'Minimal Health & Safety', "description": "", "tags": [], "effects": {}},
            {"key": 'some_health_and_safety', "name": 'Some Health & Safety', "description": "", "tags": [], "effects": {}},
            {"key": 'good_health_and_safety', "name": 'Good Health & Safety', "description": "", "tags": [], "effects": {}},
            {"key": 'excellent_health_and_safety', "name": 'Excellent Health & Safety', "description": "", "tags": [], "effects": {}},
        ],
    },
    'consumer_protections': {
        "name": 'Consumer Protections',
        "default_level": 0,
        "levels": [
            {"key": 'no_consumer_protections', "name": 'No Consumer Protections', "description": "", "tags": [], "effects": {}},
            {"key": 'minimal_consumer_protections', "name": 'Minimal Consumer Protections', "description": "", "tags": [], "effects": {}},
            {"key": 'some_consumer_protections', "name": 'Some Consumer Protections', "description": "", "tags": [], "effects": {}},
            {"key": 'good_consumer_protections', "name": 'Good Consumer Protections', "description": "", "tags": [], "effects": {}},
            {"key": 'excellent_consumer_protections', "name": 'Excellent Consumer Protections', "description": "", "tags": [], "effects": {}},
        ],
    },
    'emmigration_policy': {
        "name": 'Emmigration Policy',
        "default_level": 0,
        "levels": [
            {"key": 'no_emmigration', "name": 'No Emmigration', "description": "", "tags": [], "effects": {}},
            {"key": 'government_permission_required_strict', "name": 'Government Permission Required (strict)', "description": "", "tags": [], "effects": {}},
            {"key": 'government_permission_required_relaxed', "name": 'Government Permission Required (relaxed)', "description": "", "tags": [], "effects": {}},
            {"key": 'no_limits', "name": 'No Limits', "description": "", "tags": [], "effects": {}},
        ],
    },
    'family_planning': {
        "name": 'Family Planning',
        "default_level": 0,
        "levels": [
            {"key": 'battle_for_births', "name": 'Battle for Births', "description": "", "tags": [], "effects": {}},
            {"key": 'subsidized_childcare', "name": 'Subsidized Childcare', "description": "", "tags": [], "effects": {}},
            {"key": 'contraceptives_illegal', "name": 'Contraceptives Illegal', "description": "", "tags": [], "effects": {}},
            {"key": 'contraceptives_legal', "name": 'Contraceptives Legal', "description": "", "tags": [], "effects": {}},
            {"key": 'family_planning_outreach', "name": 'Family Planning Outreach', "description": "", "tags": [], "effects": {}},
            {"key": 'one_child_policy', "name": 'One Child Policy', "description": "", "tags": [], "effects": {}},
        ],
    },
    'military_recruitment_standards': {
        "name": 'Military Recruitment Standards',
        "default_level": 0,
        "levels": [
            {"key": 'anyone_can_serve', "name": 'Anyone Can Serve', "description": "", "tags": [], "effects": {}},
            {"key": 'mild_literacy_requirement', "name": 'Mild Literacy Requirement', "description": "", "tags": [], "effects": {}},
            {"key": 'strict_literacy_requirement', "name": 'Strict Literacy Requirement', "description": "", "tags": [], "effects": {}},
            {"key": 'soldier_literacy_program', "name": 'Soldier Literacy Program', "description": "", "tags": [], "effects": {}},
            {"key": 'elites_only', "name": 'Elites Only', "description": "", "tags": [], "effects": {}},
            {"key": 'janissaries', "name": 'Janissaries', "description": "", "tags": [], "effects": {}},
        ],
    },
    'military_salaries': {
        "name": 'Military Salaries',
        "default_level": 0,
        "levels": [
            {"key": 'none', "name": 'None', "description": "", "tags": [], "effects": {}},
            {"key": 'low', "name": 'Low', "description": "", "tags": [], "effects": {}},
            {"key": 'competitive', "name": 'Competitive', "description": "", "tags": [], "effects": {}},
            {"key": 'high', "name": 'High', "description": "", "tags": [], "effects": {}},
            {"key": 'extremely_high', "name": 'Extremely High', "description": "", "tags": [], "effects": {}},
        ],
    },
    'anti_corruption_policy': {
        "name": 'Anti-Corruption Policy',
        "default_level": 0,
        "levels": [
            {"key": 'corruption_overlooked', "name": 'Corruption Overlooked', "description": "", "tags": [], "effects": {}},
            {"key": 'mild_penalties', "name": 'Mild Penalties', "description": "", "tags": [], "effects": {}},
            {"key": 'heavy_penalties', "name": 'Heavy Penalties', "description": "", "tags": [], "effects": {}},
            {"key": 'zero_tolerance', "name": 'Zero Tolerance', "description": "", "tags": [], "effects": {}},
        ],
    },
    'mobilization': {
        "name": 'Mobilization',
        "default_level": 0,
        "levels": [
            {"key": 'civilian_economy', "name": 'Civilian Economy', "description": "", "tags": [], "effects": {}},
            {"key": 'partial_mobilization', "name": 'Partial Mobilization', "description": "", "tags": [], "effects": {}},
            {"key": 'war_economy', "name": 'War Economy', "description": "", "tags": [], "effects": {}},
            {"key": 'total_mobilization', "name": 'Total Mobilization', "description": "", "tags": [], "effects": {}},
        ],
    },
}


# Effects per policy level.
# Structure: category_key -> level_index -> {"base": {effect_key: value}}
POLICY_EFFECTS = {
    'military_service': {
        0: {
            "base": {
                'construction_time_reduction': 0.06,
                'growth_rate': 0.02,
                'manpower_bonus': -0.04,
                'military_pct': -0.06,
                'stability_bonus': 0.3,
                'upkeep_reduction': 0.06,
            },
        },
        1: {
            "base": {
                'army_training_speed_bonus': 0.02,
                'construction_time_reduction': 0.02,
                'military_pct': -0.02,
                'stability_bonus': 0.2,
                'upkeep_reduction': 0.02,
            },
        },
        2: {
            "base": {
                'construction_time_reduction': -0.01,
                'manpower_bonus': -0.01,
                'military_pct': 0.01,
                'stability_bonus': 0.1,
                'upkeep_reduction': -0.01,
            },
        },
        3: {
            "base": {
                'construction_time_reduction': -0.02,
                'manpower_bonus': -0.02,
                'military_pct': 0.03,
                'stability_bonus': -0.2,
                'upkeep_reduction': -0.02,
                'worker_productivity': -0.01,
            },
        },
        4: {
            "base": {
                'army_training_speed_bonus': 0.01,
                'construction_time_reduction': -0.03,
                'manpower_bonus': -0.03,
                'military_pct': 0.04,
                'stability_bonus': -0.3,
                'upkeep_reduction': -0.03,
            },
        },
        5: {
            "base": {
                'construction_time_reduction': -0.04,
                'manpower_bonus': -0.04,
                'military_pct': 0.05,
                'production_materials_pct': -0.02,
                'stability_bonus': -0.5,
                'upkeep_reduction': -0.04,
                'worker_productivity': -0.02,
            },
        },
        6: {
            "base": {
                'army_combat_bonus': -0.03,
                'construction_time_reduction': -0.05,
                'growth_rate': -0.03,
                'manpower_bonus': -0.06,
                'military_pct': 0.06,
                'production_materials_pct': -0.03,
                'stability_bonus': -1.0,
                'upkeep_reduction': -0.05,
                'worker_productivity': -0.03,
            },
        },
        7: {
            "base": {
                'army_combat_bonus': -0.04,
                'construction_time_reduction': -0.06,
                'growth_rate': -0.05,
                'manpower_bonus': -0.06,
                'military_pct': 0.06,
                'production_materials_pct': -0.04,
                'stability_bonus': -1.5,
                'upkeep_reduction': -0.06,
                'worker_productivity': -0.03,
            },
        },
    },
    'policing': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_security': -0.05,
                },
                'corruption_resistance': -0.03,
                'stability_bonus': -1.2,
                'trade_pct': -0.02,
                'upkeep_reduction': 0.04,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_security': -0.02,
                },
                'integration_pct': 0.02,
                'stability_bonus': -0.3,
                'upkeep_reduction': 0.03,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.01,
                },
                'corruption_resistance': -0.05,
                'production_wealth_pct': -0.01,
                'stability_bonus': -0.5,
                'trade_pct': -0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.04,
                },
                'corruption_resistance': 0.02,
                'stability_bonus': 0.8,
                'trade_pct': 0.01,
                'upkeep_reduction': -0.03,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.05,
                },
                'corruption_resistance': -0.02,
                'integration_pct': -0.03,
                'stability_bonus': 0.5,
                'upkeep_reduction': -0.02,
            },
        },
        5: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.06,
                },
                'corruption_resistance': -0.03,
                'integration_pct': -0.04,
                'military_pct': 0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.04,
            },
        },
    },
    'domestic_intelligence_agency': {
        0: {
            "base": {
                'corruption_resistance': -0.02,
                'counter_espionage_bonus': -0.04,
                'stability_bonus': -0.3,
                'upkeep_reduction': 0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.02,
                },
                'counter_espionage_bonus': 0.01,
                'stability_bonus': 0.1,
                'upkeep_reduction': -0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.04,
                },
                'corruption_resistance': 0.01,
                'counter_espionage_bonus': 0.03,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.05,
                },
                'counter_espionage_bonus': 0.05,
                'integration_pct': -0.02,
                'research_pct': -0.01,
                'stability_bonus': 0.5,
                'upkeep_reduction': -0.04,
            },
        },
    },
    'foreign_intelligence_agency': {
        0: {
            "base": {
                'espionage_bonus': -0.04,
                'trade_pct': -0.01,
                'upkeep_reduction': 0.02,
            },
        },
        1: {
            "base": {
                'espionage_bonus': 0.01,
                'trade_pct': 0.01,
                'upkeep_reduction': -0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                },
                'espionage_bonus': 0.03,
                'trade_pct': 0.02,
                'upkeep_reduction': -0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.04,
                },
                'espionage_bonus': 0.05,
                'stability_bonus': -0.2,
                'trade_pct': 0.03,
                'upkeep_reduction': -0.04,
            },
        },
    },
    'martial_law': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.06,
                },
                'growth_rate': -0.04,
                'integration_pct': -0.03,
                'military_pct': 0.04,
                'research_pct': -0.03,
                'stability_bonus': 1.0,
                'trade_pct': -0.04,
            },
        },
        1: {"base": {}},
    },
    'bureaucracy': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_education': 0.04,
                    'government_management': 0.04,
                },
                'bureaucratic_capacity': 0.06,
                'corruption_resistance': 0.03,
                'integration_pct': -0.03,
                'literacy_bonus': 0.04,
                'research_pct': 0.04,
                'stability_bonus': 0.5,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_education': 0.03,
                    'religious': 0.06,
                },
                'bureaucratic_capacity': 0.03,
                'integration_pct': 0.02,
                'literacy_bonus': 0.02,
                'research_pct': -0.03,
                'stability_bonus': 0.8,
                'upkeep_reduction': -0.02,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_management': -0.04,
                    'government_organization': -0.03,
                },
                'bureaucratic_capacity': -0.03,
                'corruption_resistance': -0.06,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.5,
                'upkeep_reduction': 0.03,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_management': -0.02,
                },
                'bureaucratic_capacity': -0.02,
                'corruption_resistance': -0.03,
                'integration_pct': -0.04,
                'manpower_bonus': -0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': 0.02,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.04,
                },
                'bureaucratic_capacity': -0.04,
                'corruption_resistance': -0.04,
                'integration_pct': -0.06,
                'manpower_bonus': -0.03,
                'research_pct': -0.03,
                'stability_bonus': -1.0,
            },
        },
        5: {
            "base": {
                'building_efficiency': {
                    'government_management': -0.02,
                },
                'bureaucratic_capacity': -0.01,
                'corruption_resistance': 0.05,
                'integration_pct': 0.03,
                'research_pct': -0.01,
                'stability_bonus': 0.3,
            },
        },
        6: {
            "base": {
                'building_efficiency': {
                    'government_management': 0.02,
                    'government_oversight': 0.03,
                },
                'bureaucratic_capacity': 0.02,
                'corruption_resistance': 0.02,
                'integration_pct': 0.02,
                'stability_bonus': 0.5,
                'upkeep_reduction': -0.04,
            },
        },
        7: {
            "base": {
                'building_efficiency': {
                    'government_management': 0.03,
                    'government_organization': 0.02,
                },
                'bureaucratic_capacity': 0.03,
                'corruption_resistance': -0.02,
                'research_pct': 0.01,
                'upkeep_reduction': -0.01,
            },
        },
        8: {
            "base": {
                'building_efficiency': {
                    'government_organization': 0.04,
                    'government_security': 0.06,
                },
                'bureaucratic_capacity': 0.02,
                'integration_pct': -0.02,
                'literacy_bonus': -0.01,
                'research_pct': -0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.03,
            },
        },
        9: {
            "base": {
                'building_efficiency': {
                    'government_education': 0.03,
                    'government_management': 0.03,
                },
                'bureaucratic_capacity': 0.04,
                'corruption_resistance': 0.04,
                'integration_pct': 0.01,
                'literacy_bonus': 0.03,
                'research_pct': 0.03,
                'stability_bonus': 0.2,
            },
        },
    },
    'legal_system': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.03,
                },
                'corruption_resistance': 0.02,
                'research_pct': 0.01,
                'stability_bonus': 0.5,
                'trade_pct': 0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.04,
                },
                'bureaucratic_capacity': 0.03,
                'corruption_resistance': 0.01,
                'stability_bonus': 0.4,
                'trade_pct': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                },
                'corruption_resistance': 0.01,
                'integration_pct': -0.02,
                'research_pct': -0.01,
                'stability_bonus': 0.3,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': -0.04,
                },
                'corruption_resistance': -0.05,
                'production_wealth_pct': -0.02,
                'stability_bonus': -1.0,
                'trade_pct': -0.03,
            },
        },
    },
    'punishments': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                },
                'integration_pct': -0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': 0.01,
                'worker_productivity': -0.01,
            },
        },
        1: {
            "base": {
                'corruption_resistance': 0.02,
                'integration_pct': 0.01,
                'production_wealth_pct': 0.01,
                'stability_bonus': 0.2,
                'upkeep_reduction': 0.02,
            },
        },
        2: {
            "base": {
                'integration_pct': 0.02,
                'manpower_bonus': 0.02,
                'stability_bonus': 0.1,
                'upkeep_reduction': -0.03,
                'worker_productivity': 0.02,
            },
        },
        3: {
            "base": {
                'corruption_resistance': -0.04,
                'integration_pct': -0.03,
                'stability_bonus': -0.8,
                'trade_pct': -0.02,
                'worker_productivity': -0.02,
            },
        },
    },
    'child_labor': {
        0: {
            "base": {
                'growth_rate': 0.01,
                'literacy_bonus': 0.03,
                'production_materials_pct': -0.01,
                'stability_bonus': 0.3,
                'worker_productivity': 0.02,
            },
        },
        1: {
            "base": {
                'literacy_bonus': 0.01,
                'production_materials_pct': 0.01,
                'stability_bonus': 0.1,
                'worker_productivity': 0.01,
            },
        },
        2: {
            "base": {
                'growth_rate': -0.02,
                'literacy_bonus': -0.03,
                'manpower_bonus': 0.02,
                'production_materials_pct': 0.03,
                'stability_bonus': -0.3,
                'worker_productivity': -0.02,
            },
        },
        3: {
            "base": {
                'army_combat_bonus': -0.03,
                'growth_rate': -0.03,
                'literacy_bonus': -0.04,
                'manpower_bonus': 0.04,
                'production_materials_pct': 0.03,
                'stability_bonus': -0.8,
                'worker_productivity': -0.03,
            },
        },
    },
    'unions': {
        0: {
            "base": {
                'consumption_pct': -0.02,
                'corruption_resistance': -0.02,
                'production_wealth_pct': 0.03,
                'stability_bonus': -0.5,
                'worker_productivity': -0.02,
            },
        },
        1: {
            "base": {
                'consumption_pct': -0.01,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.2,
                'worker_productivity': -0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'light_manufacturing': 0.02,
                },
                'production_wealth_pct': -0.01,
                'stability_bonus': 0.3,
                'trade_pct': -0.02,
                'worker_productivity': 0.01,
            },
        },
        3: {
            "base": {
                'consumption_pct': 0.03,
                'corruption_resistance': 0.02,
                'production_wealth_pct': -0.02,
                'stability_bonus': 0.5,
                'worker_productivity': 0.03,
            },
        },
    },
    'land_ownership': {
        0: {
            "base": {
                'building_efficiency': {
                    'farming': 0.02,
                },
                'production_wealth_pct': 0.01,
                'rural_output_bonus': 0.02,
                'stability_bonus': 0.2,
                'trade_pct': 0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                },
                'rural_output_bonus': 0.01,
                'stability_bonus': 0.3,
                'trade_pct': -0.01,
            },
        },
        2: {
            "base": {
                'integration_pct': -0.03,
                'manpower_bonus': -0.02,
                'production_wealth_pct': 0.02,
                'rural_output_bonus': 0.03,
                'stability_bonus': -0.5,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'farming': 0.03,
                },
                'food_production_bonus': 0.02,
                'growth_rate': 0.02,
                'rural_output_bonus': 0.03,
                'stability_bonus': 0.2,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'farming': 0.01,
                },
                'integration_pct': 0.03,
                'production_wealth_pct': -0.02,
                'rural_output_bonus': 0.01,
                'stability_bonus': 0.1,
            },
        },
    },
    'property_rights': {
        0: {
            "base": {
                'building_efficiency': {
                    'financial': 0.04,
                },
                'integration_pct': -0.01,
                'production_wealth_pct': 0.03,
                'stability_bonus': 0.3,
                'trade_pct': 0.03,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'financial': 0.02,
                    'government_regulatory': 0.02,
                },
                'production_wealth_pct': 0.01,
                'stability_bonus': 0.2,
                'trade_pct': 0.02,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'financial': -0.04,
                },
                'corruption_resistance': -0.04,
                'production_wealth_pct': -0.02,
                'stability_bonus': -1.0,
                'trade_pct': -0.04,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'financial': -0.05,
                },
                'integration_pct': 0.02,
                'production_wealth_pct': -0.04,
                'stability_bonus': -0.5,
                'trade_pct': -0.05,
            },
        },
    },
    'slavery': {
        0: {
            "base": {
                'integration_pct': 0.03,
                'manpower_bonus': -0.01,
                'stability_bonus': 0.5,
                'worker_productivity': 0.02,
            },
        },
        1: {
            "base": {
                'integration_pct': -0.01,
                'manpower_bonus': 0.01,
                'production_materials_pct': 0.01,
                'stability_bonus': 0.1,
            },
        },
        2: {
            "base": {
                'corruption_resistance': -0.02,
                'integration_pct': -0.04,
                'manpower_bonus': 0.03,
                'production_materials_pct': 0.03,
                'stability_bonus': -0.5,
                'worker_productivity': -0.02,
            },
        },
        3: {
            "base": {
                'corruption_resistance': -0.04,
                'integration_pct': -0.06,
                'manpower_bonus': 0.05,
                'production_materials_pct': 0.05,
                'research_pct': -0.03,
                'stability_bonus': -1.2,
                'worker_productivity': -0.03,
            },
        },
    },
    'industrial_subsidies': {
        0: {"base": {}},
        1: {
            "base": {
                'building_efficiency': {
                    'heavy_manufacturing': 0.1,
                    'light_manufacturing': 0.1,
                },
                'upkeep_reduction': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'heavy_manufacturing': 0.2,
                    'light_manufacturing': 0.2,
                },
                'production_materials_pct': 0.1,
                'upkeep_reduction': -0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'heavy_manufacturing': 0.4,
                    'light_manufacturing': 0.4,
                },
                'corruption_resistance': -0.02,
                'production_materials_pct': 0.3,
                'upkeep_reduction': -0.04,
            },
        },
    },
    'resource_subsidies': {
        0: {"base": {}},
        1: {
            "base": {
                'building_efficiency': {
                    'extraction': 0.1,
                    'refining': 0.1,
                },
                'upkeep_reduction': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'extraction': 0.2,
                    'refining': 0.2,
                },
                'production_energy_pct': 0.1,
                'upkeep_reduction': -0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'extraction': 0.4,
                    'refining': 0.4,
                },
                'environmental_health': -0.03,
                'production_energy_pct': 0.3,
                'upkeep_reduction': -0.04,
            },
        },
    },
    'agricultural_subsidies': {
        0: {"base": {}},
        1: {
            "base": {
                'building_efficiency': {
                    'farming': 0.1,
                },
                'food_production_bonus': 0.1,
                'upkeep_reduction': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'farming': 0.2,
                },
                'farming_bonus': 0.1,
                'food_production_bonus': 0.2,
                'upkeep_reduction': -0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'farming': 0.4,
                },
                'farming_bonus': 0.3,
                'food_production_bonus': 0.4,
                'rural_output_bonus': 0.2,
                'upkeep_reduction': -0.04,
            },
        },
    },
    'freedom_of_movement': {
        0: {
            "base": {
                'building_efficiency': {
                    'transport': 0.03,
                },
                'growth_rate': 0.02,
                'stability_bonus': -0.2,
                'trade_pct': 0.03,
                'urban_output_bonus': 0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'transport': -0.02,
                },
                'growth_rate': -0.01,
                'rural_output_bonus': 0.01,
                'stability_bonus': 0.3,
                'trade_pct': -0.01,
            },
        },
        2: {
            "base": {
                'integration_pct': -0.03,
                'production_manpower_pct': -0.02,
                'rural_output_bonus': 0.02,
                'stability_bonus': -0.5,
                'trade_pct': -0.03,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                    'transport': -0.04,
                },
                'growth_rate': -0.03,
                'production_manpower_pct': -0.04,
                'stability_bonus': -0.8,
                'trade_pct': -0.05,
            },
        },
    },
    'freedom_of_association': {
        0: {
            "base": {
                'corruption_resistance': 0.02,
                'integration_pct': 0.02,
                'research_pct': 0.02,
                'stability_bonus': -0.2,
                'worker_productivity': 0.01,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.02,
                },
                'corruption_resistance': -0.02,
                'integration_pct': -0.02,
                'research_pct': -0.01,
                'stability_bonus': 0.5,
            },
        },
        2: {
            "base": {
                'corruption_resistance': -0.01,
                'integration_pct': -0.01,
                'production_wealth_pct': 0.02,
                'stability_bonus': 0.3,
                'worker_productivity': -0.02,
            },
        },
        3: {"base": {}},
    },
    'freedom_of_press': {
        0: {
            "base": {
                'building_efficiency': {
                    'entertainment': -0.05,
                },
                'corruption_resistance': -0.03,
                'growth_rate': -0.03,
                'integration_pct': 0.02,
                'research_pct': -0.04,
                'stability_bonus': 1.5,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'entertainment': -0.03,
                },
                'growth_rate': -0.02,
                'integration_pct': 0.01,
                'research_pct': -0.02,
                'stability_bonus': 0.8,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.02,
                },
                'growth_rate': 0.01,
                'research_pct': 0.01,
                'stability_bonus': 0.3,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.04,
                },
                'growth_rate': 0.02,
                'integration_pct': -0.02,
                'production_wealth_pct': 0.02,
                'research_pct': 0.01,
                'stability_bonus': -0.3,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.06,
                },
                'corruption_resistance': 0.03,
                'growth_rate': 0.03,
                'integration_pct': -0.01,
                'research_pct': 0.04,
                'stability_bonus': -1.0,
            },
        },
    },
    'freedom_of_speech': {
        0: {
            "base": {
                'building_efficiency': {
                    'communications': -0.04,
                },
                'corruption_resistance': -0.04,
                'growth_rate': -0.02,
                'research_pct': -0.04,
                'stability_bonus': 1.2,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'communications': -0.02,
                },
                'corruption_resistance': -0.02,
                'research_pct': -0.02,
                'stability_bonus': 0.5,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'communications': 0.01,
                },
                'corruption_resistance': 0.01,
                'research_pct': 0.01,
                'stability_bonus': 0.1,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'communications': 0.04,
                },
                'corruption_resistance': 0.03,
                'growth_rate': 0.02,
                'research_pct': 0.03,
                'stability_bonus': -0.5,
            },
        },
    },
    'education': {
        0: {
            "base": {
                'literacy_bonus': -0.04,
                'research_pct': -0.03,
                'stability_bonus': -0.3,
                'upkeep_reduction': 0.03,
                'worker_productivity': -0.02,
            },
        },
        1: {
            "base": {
                'literacy_bonus': 0.02,
                'research_pct': 0.01,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.01,
                'worker_productivity': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_education': 0.03,
                },
                'literacy_bonus': 0.04,
                'research_pct': 0.03,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.03,
                'worker_productivity': 0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_education': 0.05,
                },
                'literacy_bonus': 0.06,
                'research_pct': 0.05,
                'stability_bonus': 0.4,
                'upkeep_reduction': -0.05,
                'worker_productivity': 0.03,
            },
        },
    },
    'pensions': {
        0: {"base": {}},
        1: {
            "base": {
                'consumption_pct': -0.01,
                'growth_rate': -0.01,
                'stability_bonus': -0.3,
                'upkeep_reduction': 0.02,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_welfare': 0.02,
                },
                'consumption_pct': 0.01,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_welfare': 0.04,
                },
                'consumption_pct': 0.02,
                'growth_rate': 0.01,
                'stability_bonus': 0.5,
                'upkeep_reduction': -0.04,
            },
        },
    },
    'healthcare': {
        0: {
            "base": {
                'building_efficiency': {
                    'healthcare': 0.02,
                },
                'growth_rate': -0.01,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.2,
                'upkeep_reduction': 0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'healthcare': 0.03,
                },
                'growth_rate': 0.01,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.02,
                'worker_productivity': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'healthcare': 0.05,
                },
                'growth_rate': 0.02,
                'manpower_bonus': 0.02,
                'stability_bonus': 0.5,
                'upkeep_reduction': -0.04,
                'worker_productivity': 0.02,
            },
        },
    },
    'immigration': {
        0: {
            "base": {
                'bureaucratic_capacity': 0.01,
                'growth_rate': -0.04,
                'integration_pct': -0.03,
                'manpower_bonus': -0.04,
                'stability_bonus': 1.0,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.03,
                },
                'bureaucratic_capacity': -0.01,
                'growth_rate': 0.02,
                'integration_pct': 0.01,
                'manpower_bonus': 0.02,
                'stability_bonus': 0.3,
            },
        },
        2: {
            "base": {
                'bureaucratic_capacity': -0.02,
                'consumption_pct': 0.02,
                'growth_rate': 0.04,
                'integration_pct': -0.02,
                'manpower_bonus': 0.04,
                'stability_bonus': -0.5,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_security': -0.03,
                },
                'bureaucratic_capacity': -0.04,
                'consumption_pct': 0.03,
                'growth_rate': 0.06,
                'integration_pct': -0.04,
                'manpower_bonus': 0.06,
                'stability_bonus': -1.5,
            },
        },
    },
    'vice': {
        0: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.04,
                },
                'consumption_pct': 0.04,
                'production_wealth_pct': 0.03,
                'stability_bonus': -0.5,
                'worker_productivity': -0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.02,
                },
                'consumption_pct': 0.02,
                'production_wealth_pct': 0.01,
                'stability_bonus': -0.1,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                },
                'consumption_pct': 0.01,
                'stability_bonus': 0.1,
                'urban_output_bonus': 0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.01,
                },
                'consumption_pct': 0.01,
                'stability_bonus': 0.2,
                'upkeep_reduction': 0.01,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                },
                'consumption_pct': -0.03,
                'corruption_resistance': -0.02,
                'production_wealth_pct': -0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.02,
            },
        },
    },
    'civilian_firearm_ownership': {
        0: {
            "base": {
                'army_training_speed_bonus': 0.02,
                'building_efficiency': {
                    'government_security': 0.02,
                },
                'manpower_bonus': 0.02,
                'military_pct': 0.02,
                'stability_bonus': 0.3,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_security': -0.02,
                },
                'manpower_bonus': 0.01,
                'military_pct': 0.01,
                'production_wealth_pct': 0.01,
                'stability_bonus': -0.5,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                    'government_security': 0.02,
                },
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                },
                'manpower_bonus': -0.01,
                'military_pct': -0.02,
                'stability_bonus': 0.5,
                'upkeep_reduction': -0.02,
            },
        },
    },
    'suffrage': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_oversight': 0.03,
                },
                'corruption_resistance': 0.03,
                'integration_pct': 0.03,
                'stability_bonus': 0.8,
                'upkeep_reduction': -0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_oversight': 0.01,
                },
                'corruption_resistance': -0.01,
                'integration_pct': -0.02,
                'stability_bonus': 0.2,
            },
        },
        2: {
            "base": {
                'corruption_resistance': 0.01,
                'integration_pct': 0.01,
                'production_wealth_pct': -0.02,
                'stability_bonus': 0.4,
                'worker_productivity': 0.01,
            },
        },
        3: {
            "base": {
                'corruption_resistance': -0.02,
                'integration_pct': -0.03,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.3,
                'upkeep_reduction': 0.02,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                },
                'corruption_resistance': -0.04,
                'integration_pct': -0.05,
                'stability_bonus': -1.0,
                'upkeep_reduction': 0.03,
            },
        },
    },
    'gender_rights': {
        0: {
            "base": {
                'growth_rate': 0.01,
                'manpower_bonus': 0.04,
                'research_pct': 0.02,
                'stability_bonus': 0.3,
                'worker_productivity': 0.02,
            },
        },
        1: {
            "base": {
                'manpower_bonus': 0.02,
                'research_pct': 0.01,
                'stability_bonus': 0.1,
                'worker_productivity': 0.01,
            },
        },
        2: {
            "base": {
                'integration_pct': -0.03,
                'manpower_bonus': 0.03,
                'military_pct': 0.02,
                'stability_bonus': -0.3,
                'worker_productivity': -0.01,
            },
        },
        3: {
            "base": {
                'growth_rate': 0.02,
                'manpower_bonus': -0.04,
                'research_pct': -0.02,
                'stability_bonus': 0.2,
                'worker_productivity': -0.02,
            },
        },
    },
    'racial_rights': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.04,
                },
                'integration_pct': -0.06,
                'manpower_bonus': -0.04,
                'research_pct': -0.03,
                'stability_bonus': -1.2,
            },
        },
        1: {
            "base": {
                'bureaucratic_capacity': -0.02,
                'integration_pct': -0.04,
                'manpower_bonus': -0.02,
                'stability_bonus': -0.5,
                'upkeep_reduction': -0.02,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_organization': 0.02,
                },
                'integration_pct': -0.03,
                'manpower_bonus': -0.01,
                'production_wealth_pct': 0.01,
                'stability_bonus': -0.3,
            },
        },
        3: {
            "base": {
                'integration_pct': 0.04,
                'manpower_bonus': 0.03,
                'research_pct': 0.02,
                'stability_bonus': 0.5,
                'worker_productivity': 0.02,
            },
        },
    },
    'income_tax': {
        0: {"base": {}},
        1: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.01,
                },
                'bureaucratic_capacity': 0.02,
                'consumption_pct': -0.01,
                'production_wealth_pct': 0.01,
                'stability_bonus': 0.1,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_welfare': 0.02,
                },
                'bureaucratic_capacity': -0.01,
                'consumption_pct': 0.02,
                'production_wealth_pct': -0.01,
                'stability_bonus': 0.3,
            },
        },
        3: {
            "base": {
                'consumption_pct': -0.02,
                'corruption_resistance': -0.02,
                'integration_pct': -0.02,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.5,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_welfare': 0.04,
                },
                'consumption_pct': 0.04,
                'integration_pct': 0.02,
                'production_wealth_pct': -0.03,
                'stability_bonus': 0.2,
            },
        },
    },
    'consumption_tax': {
        0: {"base": {}},
        1: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                },
                'consumption_pct': 0.01,
                'food_production_bonus': 0.01,
                'stability_bonus': 0.3,
            },
        },
        2: {
            "base": {
                'bureaucratic_capacity': 0.01,
                'consumption_pct': -0.02,
                'production_wealth_pct': 0.01,
                'stability_bonus': -0.2,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                },
                'consumption_pct': -0.01,
                'environmental_health': 0.02,
                'stability_bonus': 0.2,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                    'healthcare': 0.03,
                },
                'consumption_pct': -0.01,
                'environmental_health': 0.02,
                'stability_bonus': 0.1,
            },
        },
    },
    'land_tax': {
        0: {"base": {}},
        1: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                },
                'bureaucratic_capacity': 0.01,
                'rural_output_bonus': -0.01,
                'stability_bonus': 0.1,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'construction': 0.02,
                },
                'corruption_resistance': 0.01,
                'rural_output_bonus': 0.02,
                'stability_bonus': 0.2,
                'urban_output_bonus': 0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.03,
                },
                'bureaucratic_capacity': -0.01,
                'rural_output_bonus': 0.01,
                'stability_bonus': 0.1,
                'upkeep_reduction': -0.01,
            },
        },
    },
    'gift_and_estate_taxes': {
        0: {"base": {}},
        1: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.01,
                },
                'integration_pct': 0.01,
                'production_wealth_pct': 0.01,
                'stability_bonus': 0.1,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_oversight': 0.02,
                },
                'corruption_resistance': 0.02,
                'integration_pct': 0.02,
                'production_wealth_pct': -0.01,
                'stability_bonus': 0.2,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_welfare': 0.02,
                },
                'consumption_pct': 0.01,
                'integration_pct': 0.03,
                'production_wealth_pct': -0.02,
                'stability_bonus': 0.1,
            },
        },
    },
    'gender_roles': {
        0: {
            "base": {
                'growth_rate': 0.03,
                'manpower_bonus': -0.04,
                'research_pct': -0.02,
                'stability_bonus': 0.3,
                'worker_productivity': -0.02,
            },
        },
        1: {
            "base": {
                'growth_rate': 0.02,
                'manpower_bonus': -0.02,
                'stability_bonus': 0.1,
                'worker_productivity': -0.01,
            },
        },
        2: {
            "base": {
                'manpower_bonus': 0.02,
                'research_pct': 0.01,
                'stability_bonus': -0.1,
                'worker_productivity': 0.01,
            },
        },
        3: {
            "base": {
                'growth_rate': -0.01,
                'manpower_bonus': 0.04,
                'research_pct': 0.02,
                'stability_bonus': -0.2,
                'worker_productivity': 0.02,
            },
        },
        4: {"base": {}},
    },
    'social_discrimination': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                },
                'integration_pct': -0.06,
                'manpower_bonus': -0.04,
                'research_pct': -0.03,
                'stability_bonus': -1.0,
            },
        },
        1: {
            "base": {
                'integration_pct': -0.04,
                'manpower_bonus': -0.02,
                'research_pct': -0.02,
                'stability_bonus': -0.5,
            },
        },
        2: {
            "base": {
                'integration_pct': -0.02,
                'manpower_bonus': -0.01,
                'research_pct': -0.01,
                'stability_bonus': -0.2,
            },
        },
        3: {
            "base": {
                'integration_pct': 0.02,
                'research_pct': 0.01,
                'stability_bonus': 0.2,
                'worker_productivity': 0.01,
            },
        },
        4: {
            "base": {
                'integration_pct': 0.04,
                'manpower_bonus': 0.02,
                'research_pct': 0.02,
                'stability_bonus': 0.5,
                'worker_productivity': 0.02,
            },
        },
        5: {"base": {}},
    },
    'sexuality': {
        0: {
            "base": {
                'building_efficiency': {
                    'religious': 0.03,
                },
                'growth_rate': 0.02,
                'integration_pct': -0.03,
                'manpower_bonus': -0.01,
                'stability_bonus': 0.2,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'religious': 0.01,
                },
                'growth_rate': 0.01,
                'integration_pct': -0.01,
                'stability_bonus': 0.1,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.02,
                },
                'integration_pct': 0.01,
                'manpower_bonus': 0.01,
                'stability_bonus': -0.1,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.03,
                },
                'growth_rate': -0.01,
                'integration_pct': 0.03,
                'manpower_bonus': 0.02,
                'stability_bonus': -0.3,
            },
        },
    },
    'conservation': {
        0: {
            "base": {
                'building_efficiency': {
                    'construction': -0.02,
                    'extraction': -0.05,
                    'farming': 0.04,
                    'green_energy': 0.06,
                },
                'environmental_health': 0.1,
                'farming_bonus': 0.04,
                'food_production_bonus': 0.03,
                'production_materials_pct': -0.04,
                'stability_bonus': 0.5,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'extraction': -0.02,
                    'farming': 0.02,
                    'green_energy': 0.03,
                },
                'environmental_health': 0.05,
                'farming_bonus': 0.02,
                'production_materials_pct': -0.02,
                'stability_bonus': 0.2,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'extraction': 0.01,
                },
                'environmental_health': -0.02,
                'production_materials_pct': 0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'construction': 0.02,
                    'extraction': 0.04,
                },
                'environmental_health': -0.06,
                'farming_bonus': -0.02,
                'food_production_bonus': -0.02,
                'production_materials_pct': 0.03,
                'stability_bonus': -0.3,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'construction': 0.04,
                    'extraction': 0.06,
                    'farming': -0.03,
                },
                'environmental_health': -0.1,
                'farming_bonus': -0.04,
                'food_production_bonus': -0.04,
                'growth_rate': -0.02,
                'production_materials_pct': 0.06,
                'stability_bonus': -0.8,
            },
        },
    },
    'prison_system': {
        0: {
            "base": {
                'building_efficiency': {
                    'extraction': 0.02,
                },
                'integration_pct': -0.02,
                'manpower_bonus': -0.02,
                'stability_bonus': -0.3,
                'upkeep_reduction': 0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.02,
                },
                'manpower_bonus': 0.01,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.02,
                'worker_productivity': 0.01,
            },
        },
        2: {
            "base": {
                'integration_pct': -0.03,
                'manpower_bonus': 0.02,
                'production_materials_pct': 0.03,
                'stability_bonus': -0.5,
                'upkeep_reduction': 0.01,
                'worker_productivity': -0.02,
            },
        },
        3: {
            "base": {
                'integration_pct': -0.01,
                'manpower_bonus': -0.02,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.03,
            },
        },
        4: {
            "base": {
                'manpower_bonus': 0.01,
                'stability_bonus': -0.1,
                'upkeep_reduction': 0.02,
                'worker_productivity': 0.01,
            },
        },
        5: {
            "base": {
                'building_efficiency': {
                    'pharmaceutical': 0.03,
                },
                'corruption_resistance': -0.04,
                'integration_pct': -0.04,
                'research_pct': 0.03,
                'stability_bonus': -0.8,
            },
        },
        6: {
            "base": {
                'army_combat_bonus': -0.02,
                'integration_pct': -0.02,
                'manpower_bonus': 0.03,
                'military_pct': 0.03,
                'stability_bonus': -0.3,
            },
        },
        7: {"base": {}},
    },
    'drug_policy': {
        0: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.03,
                },
                'consumption_pct': 0.03,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.8,
                'worker_productivity': -0.03,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.02,
                },
                'consumption_pct': 0.02,
                'stability_bonus': -0.5,
                'worker_productivity': -0.02,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                },
                'consumption_pct': 0.01,
                'stability_bonus': 0.1,
                'worker_productivity': 0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.03,
                    'pharmaceutical': 0.02,
                },
                'consumption_pct': -0.01,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.02,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                },
                'consumption_pct': -0.02,
                'corruption_resistance': -0.02,
                'stability_bonus': 0.2,
                'trade_pct': -0.01,
                'upkeep_reduction': -0.03,
            },
        },
        5: {
            "base": {
                'building_efficiency': {
                    'healthcare': -0.04,
                    'religious': 0.04,
                },
                'consumption_pct': -0.02,
                'research_pct': -0.03,
                'stability_bonus': 0.3,
            },
        },
    },
    'educational_philosophy': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_education': 0.02,
                },
                'literacy_bonus': 0.02,
                'research_pct': -0.01,
                'stability_bonus': 0.2,
                'worker_productivity': 0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'religious': 0.02,
                },
                'integration_pct': 0.01,
                'literacy_bonus': 0.03,
                'research_pct': 0.01,
                'stability_bonus': 0.1,
            },
        },
        2: {
            "base": {
                'integration_pct': 0.02,
                'literacy_bonus': 0.01,
                'research_pct': 0.03,
                'stability_bonus': -0.1,
                'worker_productivity': 0.01,
            },
        },
    },
    'slavery_type': {
        0: {
            "base": {
                'building_efficiency': {
                    'farming': 0.02,
                },
                'food_production_bonus': 0.02,
                'integration_pct': -0.02,
                'rural_output_bonus': 0.03,
                'stability_bonus': -0.2,
            },
        },
        1: {
            "base": {
                'integration_pct': -0.03,
                'production_materials_pct': 0.02,
                'stability_bonus': -0.3,
                'upkeep_reduction': 0.01,
                'worker_productivity': -0.01,
            },
        },
        2: {
            "base": {
                'corruption_resistance': -0.03,
                'integration_pct': -0.01,
                'production_wealth_pct': 0.01,
                'stability_bonus': -0.1,
            },
        },
        3: {
            "base": {
                'integration_pct': -0.05,
                'production_materials_pct': 0.04,
                'stability_bonus': -0.8,
                'trade_pct': 0.02,
                'worker_productivity': -0.03,
            },
        },
        4: {
            "base": {
                'integration_pct': -0.03,
                'manpower_bonus': 0.02,
                'military_pct': 0.01,
                'production_materials_pct': 0.02,
                'stability_bonus': -0.3,
            },
        },
    },
    'firms': {
        0: {
            "base": {
                'building_efficiency': {
                    'financial': -0.05,
                },
                'corruption_resistance': -0.04,
                'production_wealth_pct': -0.04,
                'stability_bonus': -0.8,
                'trade_pct': -0.05,
            },
        },
        1: {
            "base": {
                'consumption_pct': 0.02,
                'integration_pct': 0.02,
                'production_wealth_pct': -0.01,
                'stability_bonus': 0.3,
                'worker_productivity': 0.03,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_management': 0.03,
                },
                'bureaucratic_capacity': -0.03,
                'production_wealth_pct': -0.02,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.03,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'financial': 0.03,
                },
                'production_wealth_pct': 0.03,
                'stability_bonus': -0.1,
                'trade_pct': 0.03,
                'worker_productivity': 0.01,
            },
        },
    },
    'market': {
        0: {
            "base": {
                'building_efficiency': {
                    'financial': 0.04,
                },
                'corruption_resistance': -0.02,
                'production_wealth_pct': 0.04,
                'stability_bonus': -0.5,
                'trade_pct': 0.05,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'financial': 0.02,
                    'government_regulatory': 0.02,
                },
                'production_wealth_pct': 0.02,
                'stability_bonus': 0.1,
                'trade_pct': 0.03,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.04,
                },
                'corruption_resistance': 0.02,
                'production_wealth_pct': -0.01,
                'stability_bonus': 0.3,
                'trade_pct': -0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_management': 0.04,
                },
                'bureaucratic_capacity': -0.04,
                'production_wealth_pct': -0.03,
                'stability_bonus': 0.2,
                'trade_pct': -0.04,
                'upkeep_reduction': -0.03,
            },
        },
        4: {
            "base": {
                'consumption_pct': 0.01,
                'integration_pct': 0.02,
                'research_pct': 0.01,
                'stability_bonus': -0.2,
                'trade_pct': -0.02,
            },
        },
    },
    'firm_size': {
        0: {
            "base": {
                'building_efficiency': {
                    'light_manufacturing': 0.02,
                },
                'corruption_resistance': 0.02,
                'production_wealth_pct': -0.01,
                'stability_bonus': 0.2,
                'trade_pct': -0.01,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'heavy_manufacturing': 0.01,
                    'light_manufacturing': 0.01,
                },
                'production_wealth_pct': 0.01,
                'trade_pct': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'heavy_manufacturing': 0.03,
                },
                'corruption_resistance': -0.02,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.2,
                'trade_pct': 0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'heavy_manufacturing': 0.04,
                },
                'corruption_resistance': -0.04,
                'production_wealth_pct': 0.03,
                'stability_bonus': -0.5,
                'trade_pct': 0.03,
                'worker_productivity': -0.01,
            },
        },
    },
    'currency': {
        0: {
            "base": {
                'building_efficiency': {
                    'financial': 0.03,
                },
                'bureaucratic_capacity': 0.02,
                'stability_bonus': 0.2,
                'trade_pct': 0.03,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'extraction': 0.02,
                },
                'production_wealth_pct': -0.01,
                'stability_bonus': 0.3,
                'trade_pct': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'extraction': 0.01,
                },
                'production_wealth_pct': -0.02,
                'stability_bonus': 0.4,
                'trade_pct': 0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_organization': 0.03,
                },
                'bureaucratic_capacity': -0.03,
                'consumption_pct': -0.03,
                'stability_bonus': -0.3,
                'trade_pct': -0.04,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'green_energy': 0.02,
                },
                'bureaucratic_capacity': 0.01,
                'production_energy_pct': 0.03,
                'stability_bonus': 0.1,
                'trade_pct': 0.01,
            },
        },
        5: {
            "base": {
                'building_efficiency': {
                    'financial': -0.02,
                },
                'bureaucratic_capacity': -0.02,
                'production_wealth_pct': -0.01,
                'stability_bonus': -0.5,
                'trade_pct': 0.02,
            },
        },
        6: {"base": {}},
    },
    'government_salary': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_management': -0.04,
                },
                'bureaucratic_capacity': -0.03,
                'corruption_resistance': -0.05,
                'stability_bonus': -0.8,
                'upkeep_reduction': -0.04,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_management': 0.03,
                },
                'bureaucratic_capacity': 0.02,
                'corruption_resistance': 0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.04,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_management': 0.02,
                },
                'corruption_resistance': 0.01,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_management': -0.02,
                },
                'corruption_resistance': -0.02,
                'stability_bonus': -0.2,
                'upkeep_reduction': 0.02,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_management': -0.03,
                },
                'bureaucratic_capacity': -0.02,
                'corruption_resistance': -0.04,
                'stability_bonus': -0.5,
                'upkeep_reduction': 0.04,
            },
        },
    },
    'government_benefits': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_welfare': -0.03,
                },
                'corruption_resistance': -0.05,
                'stability_bonus': -0.8,
                'upkeep_reduction': -0.05,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_welfare': 0.04,
                },
                'consumption_pct': 0.02,
                'stability_bonus': 0.4,
                'upkeep_reduction': -0.04,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_welfare': 0.02,
                },
                'consumption_pct': 0.01,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.02,
            },
        },
        3: {
            "base": {
                'consumption_pct': -0.01,
                'stability_bonus': -0.2,
                'upkeep_reduction': 0.02,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_welfare': -0.02,
                },
                'consumption_pct': -0.02,
                'stability_bonus': -0.5,
                'upkeep_reduction': 0.04,
            },
        },
    },
    'naturalization_laws': {
        0: {"base": {}},
        1: {
            "base": {
                'growth_rate': 0.02,
                'integration_pct': 0.04,
                'manpower_bonus': 0.02,
                'stability_bonus': -0.3,
            },
        },
        2: {
            "base": {
                'growth_rate': 0.01,
                'integration_pct': 0.02,
                'stability_bonus': 0.1,
            },
        },
        3: {
            "base": {
                'bureaucratic_capacity': 0.01,
                'integration_pct': 0.01,
                'stability_bonus': 0.2,
            },
        },
        4: {
            "base": {
                'bureaucratic_capacity': 0.01,
                'integration_pct': -0.01,
                'manpower_bonus': -0.01,
                'stability_bonus': 0.3,
            },
        },
        5: {
            "base": {
                'corruption_resistance': -0.02,
                'integration_pct': -0.02,
                'production_wealth_pct': 0.01,
                'stability_bonus': 0.1,
            },
        },
        6: {
            "base": {
                'growth_rate': -0.02,
                'integration_pct': -0.05,
                'manpower_bonus': -0.03,
                'stability_bonus': 0.3,
            },
        },
    },
    'visa_policy': {
        0: {
            "base": {
                'growth_rate': -0.01,
                'integration_pct': -0.02,
                'stability_bonus': 0.3,
                'trade_pct': -0.03,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.02,
                },
                'consumption_pct': 0.01,
                'stability_bonus': 0.1,
                'trade_pct': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.01,
                },
                'integration_pct': 0.01,
                'stability_bonus': 0.2,
                'trade_pct': 0.01,
            },
        },
        3: {
            "base": {
                'consumption_pct': 0.02,
                'growth_rate': 0.01,
                'integration_pct': 0.02,
                'stability_bonus': -0.2,
                'trade_pct': 0.03,
            },
        },
        4: {"base": {}},
    },
    'birthright_citizenship': {
        0: {
            "base": {
                'growth_rate': 0.02,
                'integration_pct': 0.03,
                'manpower_bonus': 0.02,
                'stability_bonus': -0.1,
            },
        },
        1: {
            "base": {
                'integration_pct': -0.02,
                'manpower_bonus': -0.01,
                'stability_bonus': 0.2,
            },
        },
        2: {
            "base": {
                'growth_rate': 0.01,
                'integration_pct': 0.02,
                'manpower_bonus': 0.01,
                'stability_bonus': 0.1,
            },
        },
        3: {
            "base": {
                'growth_rate': -0.01,
                'integration_pct': -0.04,
                'manpower_bonus': -0.02,
                'stability_bonus': 0.3,
            },
        },
        4: {
            "base": {
                'growth_rate': -0.03,
                'integration_pct': -0.06,
                'manpower_bonus': -0.04,
                'stability_bonus': 0.2,
            },
        },
    },
    'minimum_wage': {
        0: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.03,
                    'government_welfare': 0.03,
                },
                'consumption_pct': 0.03,
                'production_wealth_pct': -0.02,
                'stability_bonus': 0.8,
                'worker_productivity': 0.02,
            },
        },
        1: {
            "base": {
                'consumption_pct': 0.02,
                'corruption_resistance': 0.02,
                'production_wealth_pct': -0.01,
                'stability_bonus': 0.5,
                'worker_productivity': 0.03,
            },
        },
        2: {
            "base": {
                'consumption_pct': -0.03,
                'corruption_resistance': -0.03,
                'production_wealth_pct': 0.04,
                'stability_bonus': -1.0,
                'upkeep_reduction': 0.03,
                'worker_productivity': -0.03,
            },
        },
        3: {
            "base": {
                'consumption_pct': -0.01,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.3,
                'upkeep_reduction': 0.01,
                'worker_productivity': -0.01,
            },
        },
        4: {"base": {}},
    },
    'working_hours': {
        0: {
            "base": {
                'growth_rate': -0.01,
                'production_materials_pct': 0.03,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.5,
                'worker_productivity': -0.02,
            },
        },
        1: {
            "base": {
                'production_materials_pct': 0.02,
                'production_wealth_pct': 0.01,
                'stability_bonus': -0.2,
                'worker_productivity': -0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.02,
                },
                'consumption_pct': 0.01,
                'stability_bonus': 0.3,
                'worker_productivity': 0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.03,
                },
                'consumption_pct': 0.03,
                'production_materials_pct': -0.02,
                'stability_bonus': 0.5,
                'worker_productivity': 0.03,
            },
        },
    },
    'holidays': {
        0: {"base": {}},
        1: {
            "base": {
                'consumption_pct': 0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.01,
                'worker_productivity': 0.02,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'religious': 0.02,
                },
                'stability_bonus': 0.1,
                'worker_productivity': 0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.02,
                },
                'consumption_pct': 0.01,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.01,
                'worker_productivity': 0.02,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'entertainment': 0.03,
                },
                'consumption_pct': 0.02,
                'production_materials_pct': -0.01,
                'stability_bonus': 0.4,
                'upkeep_reduction': -0.02,
                'worker_productivity': 0.03,
            },
        },
    },
    'maternity_leave': {
        0: {"base": {}},
        1: {
            "base": {
                'growth_rate': 0.01,
                'stability_bonus': 0.1,
                'upkeep_reduction': -0.01,
                'worker_productivity': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_welfare': 0.02,
                },
                'growth_rate': 0.02,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.02,
                'worker_productivity': 0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_welfare': 0.03,
                },
                'growth_rate': 0.03,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.03,
                'worker_productivity': 0.02,
            },
        },
    },
    'paternity_leave': {
        0: {"base": {}},
        1: {
            "base": {
                'growth_rate': 0.01,
                'stability_bonus': 0.1,
                'upkeep_reduction': -0.01,
                'worker_productivity': 0.01,
            },
        },
        2: {
            "base": {
                'growth_rate': 0.01,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.02,
                'worker_productivity': 0.01,
            },
        },
        3: {
            "base": {
                'growth_rate': 0.02,
                'integration_pct': 0.01,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.03,
                'worker_productivity': 0.02,
            },
        },
    },
    'health_and_safety_regulations': {
        0: {
            "base": {
                'growth_rate': -0.01,
                'production_materials_pct': 0.03,
                'stability_bonus': -0.5,
                'upkeep_reduction': 0.03,
                'worker_productivity': -0.02,
            },
        },
        1: {
            "base": {
                'production_materials_pct': 0.01,
                'stability_bonus': -0.2,
                'upkeep_reduction': 0.01,
                'worker_productivity': -0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                },
                'stability_bonus': 0.1,
                'worker_productivity': 0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.03,
                },
                'growth_rate': 0.01,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.02,
                'worker_productivity': 0.02,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.04,
                },
                'growth_rate': 0.01,
                'production_materials_pct': -0.02,
                'stability_bonus': 0.5,
                'upkeep_reduction': -0.03,
                'worker_productivity': 0.03,
            },
        },
    },
    'consumer_protections': {
        0: {
            "base": {
                'consumption_pct': -0.01,
                'corruption_resistance': -0.03,
                'production_wealth_pct': 0.02,
                'stability_bonus': -0.3,
                'trade_pct': 0.02,
            },
        },
        1: {
            "base": {
                'corruption_resistance': -0.01,
                'stability_bonus': -0.1,
                'trade_pct': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.02,
                },
                'consumption_pct': 0.01,
                'corruption_resistance': 0.01,
                'stability_bonus': 0.1,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.03,
                },
                'consumption_pct': 0.02,
                'corruption_resistance': 0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.01,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'government_regulatory': 0.04,
                },
                'consumption_pct': 0.03,
                'corruption_resistance': 0.03,
                'production_wealth_pct': -0.01,
                'stability_bonus': 0.4,
                'upkeep_reduction': -0.03,
            },
        },
    },
    'emmigration_policy': {
        0: {
            "base": {
                'integration_pct': -0.03,
                'manpower_bonus': 0.03,
                'research_pct': -0.02,
                'stability_bonus': -0.5,
                'trade_pct': -0.02,
            },
        },
        1: {
            "base": {
                'integration_pct': -0.01,
                'manpower_bonus': 0.02,
                'stability_bonus': -0.2,
                'trade_pct': -0.01,
            },
        },
        2: {
            "base": {
                'manpower_bonus': 0.01,
                'stability_bonus': 0.1,
                'trade_pct': 0.01,
            },
        },
        3: {
            "base": {
                'integration_pct': 0.01,
                'manpower_bonus': -0.02,
                'research_pct': 0.01,
                'stability_bonus': 0.2,
                'trade_pct': 0.02,
            },
        },
    },
    'family_planning': {
        0: {
            "base": {
                'consumption_pct': -0.02,
                'growth_rate': 0.06,
                'manpower_bonus': 0.04,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.03,
            },
        },
        1: {
            "base": {
                'growth_rate': 0.03,
                'manpower_bonus': 0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.02,
                'worker_productivity': 0.02,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'religious': 0.02,
                },
                'growth_rate': 0.04,
                'manpower_bonus': 0.03,
                'stability_bonus': -0.3,
                'worker_productivity': -0.01,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'healthcare': 0.01,
                },
                'growth_rate': -0.01,
                'stability_bonus': 0.1,
                'worker_productivity': 0.01,
            },
        },
        4: {
            "base": {
                'building_efficiency': {
                    'healthcare': 0.02,
                },
                'growth_rate': -0.02,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.01,
                'worker_productivity': 0.01,
            },
        },
        5: {
            "base": {
                'building_efficiency': {
                    'government_security': 0.03,
                },
                'growth_rate': -0.05,
                'manpower_bonus': -0.04,
                'stability_bonus': -0.8,
                'upkeep_reduction': -0.02,
            },
        },
    },
    'military_recruitment_standards': {
        0: {
            "base": {
                'army_combat_bonus': -0.02,
                'integration_pct': 0.02,
                'manpower_bonus': 0.03,
                'military_pct': 0.01,
            },
        },
        1: {
            "base": {
                'army_combat_bonus': 0.01,
                'army_training_speed_bonus': 0.01,
                'literacy_bonus': 0.01,
                'manpower_bonus': 0.01,
            },
        },
        2: {
            "base": {
                'army_combat_bonus': 0.02,
                'army_training_speed_bonus': 0.02,
                'literacy_bonus': 0.02,
                'manpower_bonus': -0.02,
            },
        },
        3: {
            "base": {
                'army_combat_bonus': 0.01,
                'building_efficiency': {
                    'military_education': 0.03,
                },
                'literacy_bonus': 0.03,
                'manpower_bonus': 0.01,
                'upkeep_reduction': -0.02,
            },
        },
        4: {
            "base": {
                'army_combat_bonus': 0.03,
                'army_training_speed_bonus': 0.03,
                'integration_pct': -0.02,
                'manpower_bonus': -0.04,
                'stability_bonus': -0.3,
            },
        },
        5: {
            "base": {
                'army_combat_bonus': 0.04,
                'army_training_speed_bonus': 0.02,
                'building_efficiency': {
                    'military_education': 0.04,
                },
                'integration_pct': -0.04,
                'manpower_bonus': 0.02,
                'stability_bonus': -0.5,
            },
        },
    },
    'military_salaries': {
        0: {"base": {}},
        1: {
            "base": {
                'army_combat_bonus': -0.02,
                'corruption_resistance': -0.02,
                'stability_bonus': -0.3,
                'upkeep_reduction': 0.03,
            },
        },
        2: {
            "base": {
                'army_combat_bonus': 0.01,
                'stability_bonus': 0.1,
                'upkeep_reduction': -0.01,
            },
        },
        3: {
            "base": {
                'army_combat_bonus': 0.02,
                'corruption_resistance': 0.01,
                'stability_bonus': 0.2,
                'upkeep_reduction': -0.03,
            },
        },
        4: {
            "base": {
                'army_combat_bonus': 0.03,
                'corruption_resistance': 0.02,
                'production_wealth_pct': -0.02,
                'stability_bonus': 0.3,
                'upkeep_reduction': -0.05,
            },
        },
    },
    'anti_corruption_policy': {
        0: {
            "base": {
                'corruption_resistance': -0.06,
                'production_wealth_pct': 0.01,
                'stability_bonus': -0.5,
                'trade_pct': -0.02,
                'upkeep_reduction': 0.02,
            },
        },
        1: {
            "base": {
                'building_efficiency': {
                    'government_oversight': 0.02,
                },
                'corruption_resistance': -0.02,
                'stability_bonus': -0.1,
                'upkeep_reduction': 0.01,
            },
        },
        2: {
            "base": {
                'building_efficiency': {
                    'government_oversight': 0.04,
                },
                'corruption_resistance': 0.03,
                'stability_bonus': 0.3,
                'trade_pct': 0.02,
                'upkeep_reduction': -0.02,
            },
        },
        3: {
            "base": {
                'building_efficiency': {
                    'government_oversight': 0.05,
                },
                'corruption_resistance': 0.05,
                'research_pct': -0.01,
                'stability_bonus': 0.5,
                'trade_pct': 0.03,
                'upkeep_reduction': -0.04,
            },
        },
    },
    'mobilization': {
        0: {
            "base": {
                'consumption_pct': 0.02,
                'military_pct': -0.03,
                'production_wealth_pct': 0.02,
                'trade_pct': 0.02,
            },
        },
        1: {
            "base": {
                'arms_production_bonus': 0.02,
                'consumption_pct': -0.01,
                'military_pct': 0.02,
                'production_materials_pct': 0.02,
                'trade_pct': -0.01,
            },
        },
        2: {
            "base": {
                'arms_production_bonus': 0.04,
                'consumption_pct': -0.03,
                'military_pct': 0.04,
                'production_materials_pct': 0.04,
                'stability_bonus': -0.3,
                'trade_pct': -0.03,
                'worker_productivity': -0.01,
            },
        },
        3: {
            "base": {
                'arms_production_bonus': 0.06,
                'consumption_pct': -0.05,
                'growth_rate': -0.04,
                'military_pct': 0.06,
                'production_materials_pct': 0.06,
                'stability_bonus': -1.0,
                'trade_pct': -0.05,
                'worker_productivity': -0.02,
            },
        },
    },
}
