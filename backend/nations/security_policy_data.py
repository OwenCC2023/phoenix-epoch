"""
Security policy multipliers — maps (category, level_index) -> security_multiplier.

All multipliers are applied multiplicatively to the province's raw security value.
Missing entries default to 1.0 (no effect).

Design constraint: policing at max (1.30) should roughly compensate for two to three
detrimental policies at ~0.90 each (0.90^3 = 0.729; 0.729 × 1.30 ≈ 0.95).

Level indices match the order in POLICY_CATEGORIES[cat]["levels"].
"""

SECURITY_POLICY_MULTIPLIERS = {

    # =========================================================
    # CATEGORY A — Strong security impact (0.70-1.30)
    # =========================================================

    # policing levels: what_police(0), town_watch(1), corrupt(2),
    #   protect_and_serve(3), policing_through_fear(4), paramilitary_tactics(5)
    'policing': {
        0: 0.70,   # what_police   — no law enforcement whatsoever
        1: 0.85,   # town_watch    — minimal, volunteer-based
        2: 0.90,   # corrupt       — police exist but are unreliable/predatory
        3: 1.30,   # protect_and_serve — professional, trusted policing
        4: 1.15,   # policing_through_fear — effective but oppressive
        5: 1.05,   # paramilitary_tactics — order through force, some backlash
    },

    # punishments: retribution(0), restitution(1), rehabilitation(2), arbitrary(3)
    'punishments': {
        0: 1.05,   # retribution   — clear deterrence
        1: 0.93,   # restitution   — victim-centred, lower deterrence
        2: 0.90,   # rehabilitation — long-term good but weak short-term deterrence
        3: 0.80,   # arbitrary     — unpredictable justice breeds fear and crime
    },

    # prison_system: penal_colony(0), correctional_facilities(1), labour_camp(2),
    #   solitary_confinement(3), home_confinement(4), experimentation(5),
    #   penal_brigades(6), none(7)
    'prison_system': {
        0: 0.88,   # penal_colony   — removes offenders but deeply destabilising
        1: 1.05,   # correctional_facilities — proper incarceration improves security
        2: 0.95,   # labour_camp   — coercive, creates resentment
        3: 0.98,   # solitary_confinement — effective but limited scope
        4: 1.00,   # home_confinement — neutral
        5: 0.85,   # experimentation — grotesque, severely damages civil trust
        6: 0.95,   # penal_brigades — keeps offenders active in dangerous roles
        7: 0.75,   # none          — no consequence for crime
    },

    # martial_law: on(0), off(1)
    'martial_law': {
        0: 1.15,   # on  — immediate security gains; long-term stability cost elsewhere
        # 1: 1.00 — off, no modifier
    },

    # domestic_intelligence_agency: nonexistent(0), minimal(1), established(2), expansive(3)
    'domestic_intelligence_agency': {
        0: 0.90,   # nonexistent
        1: 0.95,   # minimal
        2: 1.05,   # established
        3: 1.10,   # expansive
    },

    # civilian_firearm_ownership: citizen_service(0), unrestricted(1), controlled(2), banned(3)
    'civilian_firearm_ownership': {
        0: 1.05,   # citizen_service — militia culture, community self-defence
        1: 0.90,   # unrestricted  — high gun density increases violent crime risk
        # 2: 1.00 — controlled, neutral
        3: 0.95,   # banned        — disarmed population, harder to enforce peacefully
    },

    # =========================================================
    # CATEGORY B — Moderate security impact (0.85-1.15)
    # =========================================================

    # legal_system: common_law(0), civil_code(1), hammurabis_code(2), arbitrary(3)
    'legal_system': {
        0: 1.05,   # common_law    — stable precedent-based system
        1: 1.05,   # civil_code    — codified, predictable rules
        # 2: 1.00 — hammurabis_code, neutral
        3: 0.85,   # arbitrary     — rule of person not law; severe insecurity
    },

    # anti_corruption_policy: corruption_overlooked(0), mild_penalties(1),
    #   heavy_penalties(2), zero_tolerance(3)
    'anti_corruption_policy': {
        0: 0.90,   # corruption_overlooked — endemic corruption undermines all security
        1: 0.95,   # mild_penalties
        2: 1.05,   # heavy_penalties
        3: 1.10,   # zero_tolerance
    },

    # immigration: closed_borders(0), visa_program(1), open_borders(2), no_borders(3)
    # Note: immigration also triggers per-turn province penalty in compute_province_security.
    'immigration': {
        # 0: 1.00 — closed_borders
        # 1: 1.00 — visa_program
        2: 0.95,   # open_borders  — integration challenges, cultural friction
        3: 0.90,   # no_borders    — very high influx strains public order systems
    },

    # drug_policy: all_drugs_are_legal(0), uncontrolled_recreational_use(1),
    #   limited_controls(2), tightly_controlled(3), prohibition(4), christian_science(5)
    'drug_policy': {
        0: 0.85,   # all_drugs_are_legal  — dependency, disorder, black market collapses
        1: 0.90,   # uncontrolled_recreational_use
        2: 0.97,   # limited_controls
        3: 1.05,   # tightly_controlled
        4: 0.92,   # prohibition   — creates organised crime networks
        # 5: 1.00 — christian_science, neutral
    },

    # vice: universally_legal(0), some_legal(1), geographic_restrictions(2),
    #   decriminalized(3), prohibited(4)
    'vice': {
        0: 0.88,   # universally_legal   — disorder from unchecked vice
        1: 0.93,   # some_legal
        2: 0.97,   # geographic_restrictions
        3: 0.96,   # decriminalized      — organised crime partially displaced
        4: 0.92,   # prohibited          — black market + organised crime
    },

    # slavery: illegal(0), rare(1), common(2), slave_society(3)
    'slavery': {
        0: 1.03,   # illegal             — stable, free society baseline
        1: 0.95,   # rare
        2: 0.88,   # common              — endemic resistance and unrest
        3: 0.80,   # slave_society       — permanent insurgency risk
    },

    # slavery_type: serfdom(0), bondage_slavery(1), informal_servitude(2),
    #   chattel_slavery(3), pow_slavery(4)
    'slavery_type': {
        0: 0.95,   # serfdom
        1: 0.90,   # bondage_slavery
        2: 0.97,   # informal_servitude  — less visible coercion
        3: 0.85,   # chattel_slavery     — worst form; constant revolt risk
        4: 0.90,   # pow_slavery
    },

    # property_rights: private_property_only(0), limited_intervention(1),
    #   unrestricted_seizure(2), private_property_illegal(3)
    'property_rights': {
        0: 1.05,   # private_property_only — strong rights, clear legal basis
        # 1: 1.00 — limited_intervention
        2: 0.88,   # unrestricted_seizure  — arbitrary confiscation breeds distrust
        3: 0.80,   # private_property_illegal — no ownership = fundamental insecurity
    },

    # land_ownership: unrestricted(0), restricted(1), elites_only(2),
    #   homesteading(3), communal_ownership(4)
    'land_ownership': {
        # 0: 1.00 — unrestricted
        1: 0.95,   # restricted
        2: 0.90,   # elites_only         — peasant resentment
        3: 1.05,   # homesteading        — stake in society improves security
        # 4: 1.00 — communal_ownership
    },

    # freedom_of_movement: unrestricted(0), restricted(1), elites_only(2), illegal(3)
    'freedom_of_movement': {
        # 0: 1.00 — unrestricted
        1: 0.95,   # restricted
        2: 0.90,   # elites_only
        3: 0.85,   # illegal             — internal passports breed resentment
    },

    # mobilization: civilian_economy(0), partial_mobilization(1),
    #   war_economy(2), total_mobilization(3)
    'mobilization': {
        # 0: 1.00 — civilian_economy
        # 1: 1.00 — partial_mobilization
        2: 0.95,   # war_economy         — civilian scarcity strains social order
        3: 0.88,   # total_mobilization  — extreme pressure on civilian life
    },

    # =========================================================
    # CATEGORY C — Mild security impact (0.93-1.05)
    # =========================================================

    # military_service: disarmed_nation(0), volunteer_only(1), limited_conscription(2),
    #   extensive_conscription(3), service_by_requirement(4), all_adults_serve(5),
    #   scraping_the_barrel(6), defense_of_berlin(7)
    'military_service': {
        # 0: 1.00 — disarmed_nation
        # 1: 1.00 — volunteer_only
        2: 0.98,   # limited_conscription
        3: 0.95,   # extensive_conscription
        4: 0.93,   # service_by_requirement
        5: 0.90,   # all_adults_serve    — depletes civilian workforce and morale
        6: 0.87,   # scraping_the_barrel — severe social disruption
        7: 0.85,   # defense_of_berlin   — total desperation, societal breakdown
    },

    # income_tax: none(0), flat(1), progressive(2), regressive(3), wealth_redistribution(4)
    'income_tax': {
        # 0: 1.00 — none
        # 1: 1.00 — flat
        2: 1.02,   # progressive         — reduces inequality, lowers resentment
        3: 0.97,   # regressive          — disproportionate burden on poor
        4: 0.95,   # wealth_redistribution — heavy top-down redistribution, backlash
    },

    # consumption_tax: none(0), basic_goods_exempted(1), all_goods(2), sin_tax(3), health_tax(4)
    'consumption_tax': {
        # 0: 1.00
        # 1: 1.00
        2: 0.98,   # all_goods
        3: 0.98,   # sin_tax
        # 4: 1.00
    },

    # land_tax: none(0), property_tax(1), land_value_tax(2), both(3)
    'land_tax': {
        # 0: 1.00
        1: 0.99,   # property_tax
        # 2: 1.00
        3: 0.98,   # both
    },

    # education: no_public_schools(0), mandatory_primary_education(1),
    #   mandatory_secondary_education(2), mandatory_secondary_and_free_tertiary(3)
    'education': {
        0: 0.93,   # no_public_schools   — illiterate, disenfranchised population
        # 1: 1.00
        2: 1.03,   # mandatory_secondary_education
        3: 1.05,   # mandatory_secondary_and_free_tertiary — most educated, most civic
    },

    # suffrage: universal_suffrage(0), unequal_value_votes(1), universal_single_class(2),
    #   limited(3), no_suffrage(4)
    'suffrage': {
        0: 1.03,   # universal_suffrage  — legitimate government = higher security
        # 1: 1.00
        # 2: 1.00
        3: 0.97,   # limited
        4: 0.93,   # no_suffrage         — illegitimate rule, chronic unrest
    },

    # racial_rights: exclusivity(0), separate_but_equal(1), castes(2), equal_rights(3)
    'racial_rights': {
        0: 0.90,   # exclusivity         — exclusion creates hostile underclass
        1: 0.93,   # separate_but_equal
        2: 0.88,   # castes              — rigid hierarchy breeds resistance
        3: 1.03,   # equal_rights
    },

    # gender_rights: equal_rights(0), allowed_to_work(1), battle_thralls(2), homemakers(3)
    'gender_rights': {
        0: 1.02,   # equal_rights
        # 1: 1.00
        2: 0.88,   # battle_thralls      — coercive, deeply resentful population
        3: 0.96,   # homemakers          — moderate restriction
    },

    # freedom_of_press: government_owned(0), heavily_censored(1), limited_censorship(2),
    #   press_barons(3), unrestricted(4)
    'freedom_of_press': {
        0: 0.95,   # government_owned    — propaganda, distrust
        1: 0.93,   # heavily_censored
        # 2: 1.00
        # 3: 1.00
        4: 1.02,   # unrestricted        — transparent society builds trust
    },

    # freedom_of_speech: criticism_forbidden(0), restricted(1), limited(2), unrestricted(3)
    'freedom_of_speech': {
        0: 0.93,   # criticism_forbidden — resentment festers silently
        1: 0.95,   # restricted
        2: 0.98,   # limited
        3: 1.02,   # unrestricted
    },

    # freedom_of_association: unrestricted(0), approved_organizations_only(1),
    #   non_unions_only(2), none(3)
    'freedom_of_association': {
        # 0: 1.00
        1: 0.97,   # approved_organizations_only
        2: 0.95,   # non_unions_only
        3: 0.92,   # none                — no civil society, trust collapses
    },

    # consumer_protections: none(0), minimal(1), some(2), good(3), excellent(4)
    'consumer_protections': {
        0: 0.95,   # no_consumer_protections
        1: 0.97,   # minimal
        # 2: 1.00
        3: 1.02,   # good
        4: 1.03,   # excellent
    },

    # health_and_safety_regulations: none(0), minimal(1), some(2), good(3), excellent(4)
    'health_and_safety_regulations': {
        0: 0.95,   # no_health_and_safety — industrial accidents breed unrest
        1: 0.97,   # minimal
        # 2: 1.00
        3: 1.02,   # good
        4: 1.03,   # excellent
    },

    # government_benefits: parasitic(0), high(1), competitive(2), low(3), minimal(4)
    'government_benefits': {
        0: 0.92,   # parasitic           — extractive, zero welfare
        1: 1.02,   # high
        # 2: 1.00
        3: 0.98,   # low
        4: 0.95,   # minimal
    },

    # working_hours: live_to_work(0), 60_hours(1), 40_hours(2), work_to_live(3)
    'working_hours': {
        0: 0.92,   # live_to_work        — exhausted, resentful workforce
        1: 0.95,   # 60_hours
        # 2: 1.00
        3: 1.03,   # work_to_live        — healthy work-life balance
    },

    # minimum_wage: state_determined(0), collective_bargaining(1), monopoly_set(2),
    #   symbolic(3), none(4)
    'minimum_wage': {
        0: 0.98,   # state_determined
        # 1: 1.00
        2: 0.95,   # monopoly_set        — exploitative, breeds resentment
        3: 0.97,   # symbolic            — meaningless protection
        4: 0.93,   # none                — race to the bottom
    },

    # unions: illegal(0), legal_but_unprotected(1), guilds_and_legal_monopolies(2),
    #   legally_protected(3)
    'unions': {
        0: 0.95,   # illegal             — labour grievances have no outlet
        1: 0.97,   # legal_but_unprotected
        # 2: 1.00
        3: 1.02,   # legally_protected   — legitimate labour voice reduces unrest
    },

    # market: free_and_unregulated(0), loosely_regulated(1), tightly_regulated(2),
    #   command_economy(3), alternative(4)
    'market': {
        0: 0.97,   # free_and_unregulated — predatory capitalism, social instability
        # 1: 1.00
        2: 0.98,   # tightly_regulated   — minor friction
        3: 0.95,   # command_economy     — shortages and black markets
        4: 0.98,   # alternative
    },

    # firms: predominantly_illegal(0), predominantly_worker_owned(1),
    #   predominantly_state_owned(2), predominantly_privately_owned(3)
    'firms': {
        0: 0.90,   # predominantly_illegal — shadow economy breeds criminality
        # 1: 1.00
        2: 0.97,   # predominantly_state_owned — inefficiency, corruption risk
        # 3: 1.00
    },

    # firm_size: small(0), medium(1), large(2), all_encompassing(3)
    'firm_size': {
        # 0: 1.00
        # 1: 1.00
        2: 0.97,   # large               — monopoly power, worker exploitation risk
        3: 0.95,   # all_encompassing    — company towns, dependency and control
    },

    # social_discrimination: enshrined_in_law(0), extensive(1), common(2),
    #   limited(3), minimal(4), none(5)
    'social_discrimination': {
        0: 0.85,   # enshrined_in_law    — institutionalised oppression
        1: 0.90,   # extensive
        2: 0.93,   # common
        3: 0.97,   # limited
        # 4: 1.00
        5: 1.03,   # none
    },

    # sexuality: rigid(0), conservative(1), liberal(2), open(3)
    'sexuality': {
        0: 0.92,   # rigid               — criminalisation creates persecution and fear
        1: 0.95,   # conservative
        # 2: 1.00
        3: 1.02,   # open
    },

    # conservation: priority(0), important(1), unimportant(2), irrelevant(3), humanity_first(4)
    'conservation': {
        0: 1.02,   # priority            — environmental safety = physical security
        # 1: 1.00
        2: 0.98,   # unimportant
        3: 0.97,   # irrelevant
        4: 0.95,   # humanity_first      — environmental degradation, health costs
    },

    # healthcare: private(0), subsidized(1), universal(2)
    'healthcare': {
        0: 0.97,   # private             — unequal access breeds resentment
        # 1: 1.00
        2: 1.03,   # universal
    },

    # pensions: none(0), low(1), medium(2), high(3)
    'pensions': {
        0: 0.95,   # none                — elderly insecurity creates social tension
        1: 0.97,   # low
        # 2: 1.00
        3: 1.03,   # high
    },

    # birthright_citizenship: jus_soli(0), jus_sanguinis(1), jus_soli_and_sanguinis(2),
    #   leges_sanguinis(3), fieri_nequit(4)
    'birthright_citizenship': {
        # 0: 1.00 — jus_soli
        1: 0.97,   # jus_sanguinis
        # 2: 1.00
        3: 0.95,   # leges_sanguinis     — very restrictive citizenship
        4: 0.90,   # fieri_nequit        — permanent statelessness for residents
    },

    # naturalization_laws: none(0), 1_3_years(1), 4_7_years(2), 8_10_years(3),
    #   11_years(4), special(5), never(6)
    'naturalization_laws': {
        # 0: 1.00
        # 1: 1.00
        2: 0.98,   # 4_7_years
        3: 0.97,   # 8_10_years
        4: 0.95,   # 11_years
        5: 0.95,   # special
        6: 0.92,   # never               — permanent residents with no path to citizenship
    },

    # visa_policy: closed_system(0), tourism_only(1), invitation_only(2),
    #   visa_on_arrival(3), none(4)
    'visa_policy': {
        0: 0.97,   # closed_system
        1: 0.98,   # tourism_only
        # 2: 1.00
        # 3: 1.00
        4: 0.95,   # none                — no entry controls
    },

    # emmigration_policy: no_emmigration(0), government_permission_required_strict(1),
    #   government_permission_required_relaxed(2), no_limits(3)
    'emmigration_policy': {
        0: 0.92,   # no_emmigration      — trapped population, desperation and unrest
        1: 0.95,   # government_permission_required_strict
        2: 0.98,   # government_permission_required_relaxed
        # 3: 1.00
    },

    # child_labor: illegal(0), regulated(1), unrestricted(2), unrestricted_child_soldiers(3)
    'child_labor': {
        0: 1.02,   # illegal             — safe childhoods improve long-term security
        1: 0.98,   # regulated
        2: 0.93,   # unrestricted
        3: 0.88,   # unrestricted_child_soldiers — societal breakdown
    },

    # =========================================================
    # CATEGORY D — Minor adjustments only
    # =========================================================

    # bureaucracy: mandarin_system(0), ecclesiastical_system(1), patronage_system(2),
    #   familial_system(3), racial_system(4), sortition(5), elected_officials(6),
    #   appointment(7), military(8), skill_challenge_system(9)
    'bureaucracy': {
        # 0: 1.00
        # 1: 1.00
        2: 0.95,   # patronage_system    — cronyism undermines rule of law
        3: 0.93,   # familial_system     — nepotism at all levels
        4: 0.90,   # racial_system       — excludes majority from civic participation
        # 5-9: neutral
    },

    # gender_roles: strictly_enforced(0), expected(1), regularly_defied(2),
    #   minimal(3), none(4)
    'gender_roles': {
        0: 0.90,   # strictly_enforced   — rigid roles breed suppressed resentment
        1: 0.95,   # expected
        # 2: 1.00
        3: 1.02,   # minimal
        4: 1.03,   # none
    },

    # government_salary: parasitic(0), high(1), competitive(2), low(3), minimal(4)
    'government_salary': {
        0: 0.92,   # parasitic           — officials extracting from public
        1: 1.02,   # high                — well-paid officials less corruptible
        # 2: 1.00
        3: 0.97,   # low                 — underpaid officials prone to corruption
        4: 0.95,   # minimal
    },

    # family_planning: battle_for_births(0), subsidized_childcare(1),
    #   contraceptives_illegal(2), contraceptives_legal(3),
    #   family_planning_outreach(4), one_child_policy(5)
    'family_planning': {
        0: 0.97,   # battle_for_births   — coercive pro-natalism
        # 1: 1.00
        2: 0.97,   # contraceptives_illegal — bodily autonomy violation
        # 3: 1.00
        # 4: 1.00
        5: 0.95,   # one_child_policy    — state coercion of family life
    },

    # foreign_intelligence_agency: nonexistent(0), minimal(1), established(2), expansive(3)
    'foreign_intelligence_agency': {
        # 0-2: neutral
        3: 0.97,   # expansive           — diverts resources; minor blowback risk
    },
}
