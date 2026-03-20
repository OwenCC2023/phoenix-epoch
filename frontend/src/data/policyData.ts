export interface PolicyLevel {
  key: string;
  name: string;
  description: string;
}

export interface PolicyCategory {
  key: string;
  name: string;
  defaultLevel: number;
  levels: PolicyLevel[];
}

const cat = (key: string, name: string, defaultLevel: number, levels: PolicyLevel[]): PolicyCategory => ({
  key, name, defaultLevel, levels,
});
const lv = (key: string, name: string, description: string): PolicyLevel => ({ key, name, description });

export const POLICY_CATEGORIES: PolicyCategory[] = [
  // MILITARY
  cat('military_service', 'Military Service', 1, [
    lv('disarmed_nation', 'Disarmed Nation', 'The country maintains only a token military force.'),
    lv('volunteer_only', 'Volunteer Only', 'Military relies entirely on volunteers.'),
    lv('limited_conscription', 'Limited Conscription', 'Selective service for a small portion of the population.'),
    lv('extensive_conscription', 'Extensive Conscription', 'Most able-bodied citizens serve.'),
    lv('universal_service', 'Universal Service', 'All citizens are required to serve.'),
    lv('service_by_requirement', 'Service by Requirement', 'Citizens are called up based on need.'),
    lv('scraping_the_barrel', 'Scraping the Barrel', 'Everyone who can hold a weapon is conscripted.'),
  ]),
  cat('military_spending', 'Military Spending', 1, [
    lv('minimal_military', 'Minimal Budget', 'Bare minimum military funding.'),
    lv('low_military', 'Low Budget', 'Below-average military spending.'),
    lv('moderate_military', 'Moderate Budget', 'Standard military funding.'),
    lv('high_military', 'High Budget', 'Above-average military spending.'),
    lv('war_economy', 'War Economy', 'Economy geared toward military production.'),
  ]),
  cat('military_doctrine', 'Military Doctrine', 0, [
    lv('static_defence', 'Static Defence', 'Focus on fortifications.'),
    lv('mobile_warfare', 'Mobile Warfare', 'Emphasis on rapid movement.'),
    lv('guerrilla_warfare', 'Guerrilla Warfare', 'Asymmetric tactics.'),
    lv('combined_arms', 'Combined Arms', 'Coordinated use of all forces.'),
  ]),
  cat('veterans_policy', 'Veterans Policy', 1, [
    lv('no_veterans_support', 'No Support', 'Veterans receive no special treatment.'),
    lv('basic_veterans_care', 'Basic Care', 'Minimal medical care for wounded veterans.'),
    lv('veterans_benefits', 'Veterans Benefits', 'Land grants and pensions.'),
    lv('hero_worship', 'Hero Worship', 'Veterans are a privileged class.'),
  ]),
  cat('border_policy', 'Border Policy', 1, [
    lv('open_borders', 'Open Borders', 'Free movement across boundaries.'),
    lv('monitored_borders', 'Monitored Borders', 'Crossings tracked but not restricted.'),
    lv('controlled_borders', 'Controlled Borders', 'Entry requires documentation.'),
    lv('restricted_borders', 'Restricted Borders', 'Only approved travellers may enter.'),
    lv('closed_borders', 'Closed Borders', 'No foreign entry permitted.'),
  ]),
  cat('weapons_policy', 'Weapons Policy', 1, [
    lv('universal_arms', 'Universal Right to Arms', 'All citizens may bear weapons.'),
    lv('licensed_arms', 'Licensed Ownership', 'Weapons require licensing.'),
    lv('restricted_arms', 'Restricted Ownership', 'Only approved citizens may own weapons.'),
    lv('state_monopoly_arms', 'State Monopoly', 'Only military and police may possess weapons.'),
  ]),
  cat('intelligence_policy', 'Intelligence Policy', 1, [
    lv('no_intelligence', 'No Intelligence Service', 'No organised intelligence.'),
    lv('basic_intelligence', 'Basic Intelligence', 'Small intelligence bureau.'),
    lv('active_intelligence', 'Active Intelligence', 'Dedicated service with foreign operations.'),
    lv('pervasive_surveillance', 'Pervasive Surveillance', 'Comprehensive domestic and foreign intelligence.'),
  ]),

  // ECONOMY
  cat('economic_system', 'Economic System', 2, [
    lv('free_market', 'Free Market', 'Minimal government intervention.'),
    lv('mixed_economy', 'Mixed Economy', 'Government regulates key sectors.'),
    lv('managed_economy', 'Managed Economy', 'Government directs major decisions.'),
    lv('command_economy', 'Command Economy', 'State controls all production.'),
    lv('barter_economy', 'Barter Economy', 'Direct exchange of goods.'),
  ]),
  cat('taxation', 'Taxation', 2, [
    lv('no_taxes', 'No Taxation', 'No taxes levied.'),
    lv('low_taxes', 'Low Taxation', 'Minimal taxation.'),
    lv('moderate_taxes', 'Moderate Taxation', 'Standard taxation.'),
    lv('high_taxes', 'High Taxation', 'Heavy taxation.'),
    lv('confiscatory_taxes', 'Confiscatory Taxation', 'Near-total appropriation of wealth.'),
  ]),
  cat('trade_policy', 'Trade Policy', 1, [
    lv('free_trade', 'Free Trade', 'No restrictions on imports or exports.'),
    lv('moderate_tariffs', 'Moderate Tariffs', 'Tariffs on selected goods.'),
    lv('protectionist', 'Protectionist', 'High tariffs and import quotas.'),
    lv('autarky', 'Autarky', 'Complete self-sufficiency.'),
  ]),
  cat('currency_policy', 'Currency Policy', 1, [
    lv('commodity_money', 'Commodity Money', 'Physical commodities as currency.'),
    lv('backed_currency', 'Backed Currency', 'Currency backed by reserves.'),
    lv('fiat_currency', 'Fiat Currency', 'Government-issued unbacked currency.'),
  ]),
  cat('property_rights', 'Property Rights', 1, [
    lv('communal_property', 'Communal Property', 'Major property is communally owned.'),
    lv('mixed_property', 'Mixed Property', 'Private property with state ownership.'),
    lv('strong_property', 'Strong Property Rights', 'Robust legal protection.'),
  ]),
  cat('labour_policy', 'Labour Policy', 1, [
    lv('forced_labour', 'Forced Labour', 'State can compel labour.'),
    lv('regulated_labour', 'Regulated Labour', 'Basic labour protections.'),
    lv('worker_councils', 'Worker Councils', 'Workers have significant say.'),
    lv('free_labour', 'Free Labour Market', 'No government regulation.'),
  ]),
  cat('banking_policy', 'Banking Policy', 1, [
    lv('no_banking', 'No Formal Banking', 'No organised banking.'),
    lv('state_banking', 'State Banking', 'All banking through state.'),
    lv('regulated_banking', 'Regulated Banking', 'Private banks with oversight.'),
    lv('free_banking', 'Free Banking', 'Minimal regulation.'),
  ]),
  cat('resource_extraction', 'Resource Extraction', 1, [
    lv('state_extraction', 'State Monopoly', 'All resources extracted by state.'),
    lv('licensed_extraction', 'Licensed Extraction', 'Private with licences.'),
    lv('unregulated_extraction', 'Unregulated', 'Anyone can extract freely.'),
    lv('conservation_priority', 'Conservation Priority', 'Extraction heavily limited.'),
  ]),
  cat('food_distribution', 'Food Distribution', 1, [
    lv('free_market_food', 'Free Market', 'Food on the open market.'),
    lv('subsidised_food', 'Subsidised Food', 'Government keeps food affordable.'),
    lv('rationing', 'Rationing', 'Government ration cards.'),
    lv('communal_kitchens', 'Communal Kitchens', 'Community-run kitchens.'),
  ]),
  cat('infrastructure_policy', 'Infrastructure Policy', 1, [
    lv('neglected_infrastructure', 'Neglected', 'Minimal maintenance.'),
    lv('maintained_infrastructure', 'Maintained', 'Kept in working order.'),
    lv('expanding_infrastructure', 'Expanding', 'Active new construction.'),
    lv('megaproject_infrastructure', 'Megaprojects', 'Ambitious large-scale programs.'),
  ]),
  cat('energy_policy', 'Energy Policy', 1, [
    lv('biomass_energy', 'Biomass Only', 'Wood, dung, organic waste.'),
    lv('fossil_fuel_energy', 'Fossil Fuels', 'Oil and coal.'),
    lv('mixed_energy', 'Mixed Sources', 'Combination of types.'),
    lv('renewable_energy', 'Renewable Focus', 'Wind, water, solar.'),
  ]),

  // SOCIAL
  cat('education_policy', 'Education Policy', 1, [
    lv('no_education', 'No Public Education', 'Left to families.'),
    lv('basic_education', 'Basic Literacy', 'Reading and writing.'),
    lv('primary_education', 'Primary Education', 'Free primary schooling.'),
    lv('secondary_education', 'Secondary Education', 'Free through secondary.'),
    lv('universal_education', 'Universal Education', 'Free at all levels.'),
  ]),
  cat('healthcare_policy', 'Healthcare Policy', 1, [
    lv('no_healthcare', 'No Public Healthcare', 'Entirely private.'),
    lv('basic_healthcare', 'Basic Healthcare', 'Basic medical care.'),
    lv('public_healthcare', 'Public Healthcare', 'Comprehensive government-funded.'),
    lv('universal_healthcare', 'Universal Healthcare', 'Free for all citizens.'),
  ]),
  cat('housing_policy', 'Housing Policy', 1, [
    lv('no_housing_policy', 'No Government Housing', 'Market-driven.'),
    lv('housing_assistance', 'Housing Assistance', 'Government subsidies.'),
    lv('public_housing', 'Public Housing', 'Government-built housing.'),
    lv('assigned_housing', 'Assigned Housing', 'Government assigns housing.'),
  ]),
  cat('welfare_policy', 'Welfare Policy', 1, [
    lv('no_welfare', 'No Welfare', 'No welfare programs.'),
    lv('minimal_welfare', 'Minimal Safety Net', 'Basic support.'),
    lv('moderate_welfare', 'Moderate Welfare', 'Support for unemployed.'),
    lv('comprehensive_welfare', 'Comprehensive Welfare', 'Extensive safety net.'),
    lv('universal_income', 'Universal Income', 'Basic income for all.'),
  ]),
  cat('religion_policy', 'Religion Policy', 1, [
    lv('state_atheism', 'State Atheism', 'Religion discouraged or banned.'),
    lv('secular_state', 'Secular State', 'Government separate from religion.'),
    lv('religious_tolerance', 'Religious Tolerance', 'All religions accepted.'),
    lv('state_religion', 'State Religion', 'One religion officially endorsed.'),
    lv('theocratic_law', 'Theocratic Law', 'Religious law is the law.'),
  ]),
  cat('press_freedom', 'Press Freedom', 1, [
    lv('free_press', 'Free Press', 'No government control.'),
    lv('regulated_press', 'Regulated Press', 'Some restrictions.'),
    lv('censored_press', 'Censored Press', 'Active censorship.'),
    lv('state_media', 'State Media Only', 'All media state-owned.'),
  ]),
  cat('justice_system', 'Justice System', 1, [
    lv('tribal_justice', 'Tribal Justice', 'Community elders settle disputes.'),
    lv('codified_law', 'Codified Law', 'Written laws and formal courts.'),
    lv('restorative_justice', 'Restorative Justice', 'Focus on rehabilitation.'),
    lv('harsh_penalties', 'Harsh Penalties', 'Severe punishments.'),
  ]),
  cat('assembly_rights', 'Assembly Rights', 1, [
    lv('free_assembly', 'Free Assembly', 'Gather and organise freely.'),
    lv('regulated_assembly', 'Regulated Assembly', 'Gatherings require permits.'),
    lv('restricted_assembly', 'Restricted Assembly', 'Only government-approved.'),
    lv('no_assembly', 'No Assembly', 'Public gatherings banned.'),
  ]),
  cat('citizenship_policy', 'Citizenship Policy', 1, [
    lv('open_citizenship', 'Open Citizenship', 'Minimal requirements.'),
    lv('residency_citizenship', 'Residency-Based', 'After a period of residency.'),
    lv('blood_citizenship', 'Blood-Based', 'Hereditary only.'),
    lv('merit_citizenship', 'Merit-Based', 'Requires demonstrated contribution.'),
  ]),
  cat('migration_policy', 'Migration Policy', 1, [
    lv('welcome_migrants', 'Welcome Migrants', 'Active recruitment of settlers.'),
    lv('accept_migrants', 'Accept Migrants', 'Accepted with basic criteria.'),
    lv('restrict_migrants', 'Restrict Migrants', 'Strict limits on immigration.'),
    lv('no_immigration', 'No Immigration', 'Borders closed to newcomers.'),
  ]),
  cat('social_mobility', 'Social Mobility', 1, [
    lv('caste_system', 'Caste System', 'Social position fixed at birth.'),
    lv('limited_mobility', 'Limited Mobility', 'Advancement possible but difficult.'),
    lv('meritocratic_mobility', 'Meritocratic', 'Based on ability and effort.'),
    lv('egalitarian_mobility', 'Egalitarian', 'Active efforts to eliminate class barriers.'),
  ]),
  cat('minority_rights', 'Minority Rights', 1, [
    lv('persecution', 'Persecution', 'Active discrimination.'),
    lv('tolerance', 'Tolerance', 'Tolerated but not protected.'),
    lv('protection', 'Protected Rights', 'Legal protections.'),
    lv('full_equality', 'Full Equality', 'Active equal treatment.'),
  ]),

  // GOVERNANCE
  cat('government_transparency', 'Government Transparency', 1, [
    lv('total_secrecy', 'Total Secrecy', 'Completely opaque.'),
    lv('selective_disclosure', 'Selective Disclosure', 'Shares selectively.'),
    lv('open_government', 'Open Government', 'Records publicly available.'),
  ]),
  cat('corruption_policy', 'Anti-Corruption Policy', 1, [
    lv('endemic_corruption', 'Endemic Corruption', 'Widespread and accepted.'),
    lv('tolerated_corruption', 'Tolerated Corruption', 'Exists but not addressed.'),
    lv('anti_corruption', 'Anti-Corruption Measures', 'Active efforts to reduce.'),
    lv('zero_tolerance', 'Zero Tolerance', 'Harsh penalties.'),
  ]),
  cat('bureaucratic_structure', 'Bureaucratic Structure', 1, [
    lv('minimal_bureaucracy', 'Minimal', 'Skeleton staff.'),
    lv('functional_bureaucracy', 'Functional', 'Adequate staffing.'),
    lv('expansive_bureaucracy', 'Expansive', 'Large government apparatus.'),
    lv('total_administration', 'Total Administration', 'Administers all aspects.'),
  ]),
  cat('political_parties', 'Political Parties', 1, [
    lv('no_parties', 'No Parties', 'Parties banned.'),
    lv('single_party', 'Single Party', 'Only one party.'),
    lv('limited_parties', 'Limited Parties', 'A few approved parties.'),
    lv('multi_party', 'Multi-Party', 'Multiple parties compete.'),
  ]),
  cat('local_governance', 'Local Governance', 1, [
    lv('centralised', 'Centralised', 'All decisions from the capital.'),
    lv('delegated', 'Delegated Authority', 'Local officials carry out directives.'),
    lv('devolved', 'Devolved Government', 'Provinces have significant autonomy.'),
    lv('federal', 'Federal System', 'Provinces self-governing.'),
  ]),
  cat('succession_policy', 'Succession Policy', 1, [
    lv('hereditary', 'Hereditary', 'Passes through family lines.'),
    lv('appointed_successor', 'Appointed Successor', 'Leader chooses successor.'),
    lv('elected_leader', 'Elected Leader', 'Determined by election.'),
    lv('council_selected', 'Council Selected', 'Council selects leader.'),
  ]),
  cat('civil_service', 'Civil Service', 1, [
    lv('patronage_system', 'Patronage System', 'Positions awarded by loyalty.'),
    lv('basic_civil_service', 'Basic Civil Service', 'Hired on basic qualifications.'),
    lv('professional_civil_service', 'Professional', 'Merit-based hiring.'),
    lv('technocratic_service', 'Technocratic Service', 'Requires technical expertise.'),
  ]),
  cat('emergency_powers', 'Emergency Powers', 1, [
    lv('no_emergency_powers', 'No Emergency Powers', 'No special crisis authority.'),
    lv('limited_emergency', 'Limited Emergency', 'Limited crisis action.'),
    lv('broad_emergency', 'Broad Emergency', 'Can suspend rights.'),
    lv('permanent_emergency', 'Permanent Emergency', 'Always in effect.'),
  ]),
  cat('diplomatic_stance', 'Diplomatic Stance', 1, [
    lv('isolationism', 'Isolationism', 'Minimal engagement.'),
    lv('cautious_engagement', 'Cautious Engagement', 'Selective relationships.'),
    lv('active_diplomacy', 'Active Diplomacy', 'Vigorous pursuit of relations.'),
    lv('alliance_seeking', 'Alliance Seeking', 'Building alliance blocs.'),
  ]),
  cat('propaganda_policy', 'Propaganda Policy', 0, [
    lv('no_propaganda', 'No Propaganda', 'No government propaganda.'),
    lv('public_information', 'Public Information', 'Factual information campaigns.'),
    lv('state_messaging', 'State Messaging', 'Government promotes its narrative.'),
    lv('total_propaganda', 'Total Propaganda', 'All information filtered through government.'),
  ]),

  // INDUSTRY & PRODUCTION
  cat('industrial_policy', 'Industrial Policy', 1, [
    lv('agrarian_focus', 'Agrarian Focus', 'Economy prioritises agriculture.'),
    lv('balanced_development', 'Balanced Development', 'Even investment.'),
    lv('industrialisation_drive', 'Industrialisation Drive', 'Push toward factories.'),
    lv('high_tech_focus', 'High-Tech Focus', 'Advanced manufacturing.'),
  ]),
  cat('construction_regulation', 'Construction Regulation', 1, [
    lv('no_regulations', 'No Regulations', 'Build anything, anywhere.'),
    lv('basic_codes', 'Basic Building Codes', 'Minimal safety requirements.'),
    lv('comprehensive_planning', 'Comprehensive Planning', 'Government approves all projects.'),
  ]),
  cat('environmental_policy', 'Environmental Policy', 1, [
    lv('no_environmental', 'No Policy', 'No environmental protections.'),
    lv('basic_environmental', 'Basic Protections', 'Minimal standards.'),
    lv('strict_environmental', 'Strict Protections', 'Strong regulations.'),
    lv('deep_ecology', 'Deep Ecology', 'Environment over growth.'),
  ]),
  cat('agriculture_policy', 'Agriculture Policy', 1, [
    lv('subsistence_farming', 'Subsistence Farming', 'Each community grows own food.'),
    lv('mixed_agriculture', 'Mixed Agriculture', 'Small and large farms.'),
    lv('collective_farms', 'Collective Farms', 'Government-organised collectives.'),
    lv('industrial_agriculture', 'Industrial Agriculture', 'Large-scale mechanised farming.'),
  ]),
  cat('manufacturing_policy', 'Manufacturing Policy', 1, [
    lv('cottage_industry', 'Cottage Industry', 'Small-scale home production.'),
    lv('workshop_economy', 'Workshop Economy', 'Organised workshops.'),
    lv('factory_system', 'Factory System', 'Large-scale production.'),
    lv('automated_production', 'Automated Production', 'Highly mechanised.'),
  ]),
  cat('research_policy', 'Research Policy', 1, [
    lv('no_research_policy', 'No Organised Research', 'Research happens informally.'),
    lv('practical_research', 'Practical Research', 'Immediate practical needs.'),
    lv('academic_research', 'Academic Research', 'Formal institutions.'),
    lv('state_research', 'State-Directed Research', 'Government sets priorities.'),
  ]),
  cat('salvage_policy', 'Salvage Policy', 1, [
    lv('free_salvage', 'Free Salvage', 'Anyone can loot ruins.'),
    lv('regulated_salvage', 'Regulated Salvage', 'Licensed salvage rights.'),
    lv('state_salvage', 'State Salvage', 'Only government teams.'),
  ]),
  cat('technology_adoption', 'Technology Adoption', 1, [
    lv('tech_rejection', 'Technology Rejection', 'Old-world tech feared.'),
    lv('cautious_adoption', 'Cautious Adoption', 'Tested carefully.'),
    lv('enthusiastic_adoption', 'Enthusiastic Adoption', 'Eagerly embraced.'),
  ]),

  // CULTURE & IDENTITY
  cat('cultural_policy', 'Cultural Policy', 1, [
    lv('no_cultural_policy', 'No Cultural Policy', 'Culture develops organically.'),
    lv('cultural_preservation', 'Cultural Preservation', 'Traditional culture protected.'),
    lv('cultural_promotion', 'Cultural Promotion', 'Promotes national culture.'),
    lv('cultural_revolution', 'Cultural Revolution', 'Active transformation of values.'),
  ]),
  cat('language_policy', 'Language Policy', 1, [
    lv('no_language_policy', 'No Language Policy', 'People speak freely.'),
    lv('official_language', 'Official Language', 'One language for government.'),
    lv('multilingual', 'Multilingual', 'Multiple languages recognised.'),
    lv('language_enforcement', 'Language Enforcement', 'Must speak national language.'),
  ]),
  cat('arts_policy', 'Arts & Entertainment', 1, [
    lv('no_arts_policy', 'No Support', 'No government support.'),
    lv('arts_patronage', 'Patronage', 'Government sponsors artists.'),
    lv('state_art', 'State Art', 'Art serves the state.'),
  ]),
  cat('historical_narrative', 'Historical Narrative', 1, [
    lv('no_official_history', 'No Official History', 'Each community tells its story.'),
    lv('preservation_narrative', 'Preservation Narrative', 'Preserving old world records.'),
    lv('rebirth_narrative', 'Rebirth Narrative', 'A chance to start fresh.'),
    lv('glory_narrative', 'Glory Narrative', 'Destined for greatness.'),
  ]),
  cat('family_policy', 'Family Policy', 1, [
    lv('no_family_policy', 'No Family Policy', 'Family matters are private.'),
    lv('pro_natalist', 'Pro-Natalist', 'Encourages large families.'),
    lv('family_planning', 'Family Planning', 'Family planning resources.'),
    lv('population_control', 'Population Control', 'Limits family size.'),
  ]),
  cat('youth_policy', 'Youth Policy', 0, [
    lv('no_youth_policy', 'No Youth Policy', 'Children learn from families.'),
    lv('youth_education', 'Youth Education', 'Structured youth education.'),
    lv('youth_organisations', 'Youth Organisations', 'Government-sponsored groups.'),
    lv('youth_militias', 'Youth Militias', 'Military training begins in youth.'),
  ]),
  cat('gender_policy', 'Gender Policy', 1, [
    lv('traditional_roles', 'Traditional Roles', 'Traditional roles enforced.'),
    lv('mixed_roles', 'Mixed Roles', 'Flexible but not enforced.'),
    lv('full_equality', 'Full Equality', 'Complete equality.'),
  ]),
  cat('elder_policy', 'Elder Policy', 1, [
    lv('no_elder_policy', 'No Support', 'Cared for by families.'),
    lv('basic_elder_care', 'Basic Care', 'Basic elderly care.'),
    lv('elder_councils', 'Elder Councils', 'Elders as advisors and leaders.'),
  ]),

  // PUBLIC ORDER
  cat('policing_policy', 'Policing Policy', 1, [
    lv('community_watch', 'Community Watch', 'Volunteers maintain order.'),
    lv('local_police', 'Local Police', 'Community police force.'),
    lv('national_police', 'National Police', 'Centralised police.'),
    lv('military_police', 'Military Police', 'Military maintains civil order.'),
  ]),
  cat('prison_policy', 'Prison Policy', 1, [
    lv('exile_punishment', 'Exile', 'Criminals banished.'),
    lv('basic_prisons', 'Basic Prisons', 'Simple detention.'),
    lv('rehabilitation', 'Rehabilitation', 'Focus on reforming.'),
    lv('labour_camps', 'Labour Camps', 'Forced labour.'),
  ]),
  cat('drug_policy', 'Drug Policy', 1, [
    lv('unregulated_drugs', 'Unregulated', 'No drug regulation.'),
    lv('medical_only', 'Medical Only', 'Restricted to medical use.'),
    lv('total_prohibition', 'Total Prohibition', 'All recreational drugs banned.'),
  ]),
  cat('curfew_policy', 'Curfew Policy', 0, [
    lv('no_curfew', 'No Curfew', 'Free to move at any time.'),
    lv('recommended_curfew', 'Recommended Curfew', 'Stay home at night suggested.'),
    lv('mandatory_curfew', 'Mandatory Curfew', 'Must be indoors by nightfall.'),
  ]),
  cat('identity_documents', 'Identity Documents', 1, [
    lv('no_documents', 'No Documents', 'No identity documents.'),
    lv('basic_registration', 'Basic Registration', 'Registered but no documents.'),
    lv('identity_cards', 'Identity Cards', 'Government-issued identity.'),
    lv('biometric_tracking', 'Biometric Tracking', 'Identified by biometric data.'),
  ]),

  // FOREIGN RELATIONS
  cat('alliance_policy', 'Alliance Policy', 1, [
    lv('no_alliances', 'No Alliances', 'The nation stands alone.'),
    lv('defensive_pacts', 'Defensive Pacts', 'Mutual defence agreements.'),
    lv('military_alliances', 'Military Alliances', 'Full military cooperation.'),
    lv('federation_seeking', 'Federation Seeking', 'Toward political union.'),
  ]),
  cat('foreign_aid', 'Foreign Aid', 0, [
    lv('no_foreign_aid', 'No Foreign Aid', 'Resources stay at home.'),
    lv('strategic_aid', 'Strategic Aid', 'Aid to advance interests.'),
    lv('humanitarian_aid', 'Humanitarian Aid', 'Aid based on need.'),
  ]),
  cat('treaty_compliance', 'Treaty Compliance', 1, [
    lv('treaty_optional', 'Optional', 'Followed only when convenient.'),
    lv('treaty_respected', 'Respected', 'Generally honoured.'),
    lv('treaty_sacred', 'Sacred', 'Breaking a treaty is unthinkable.'),
  ]),
  cat('espionage_stance', 'Espionage Stance', 1, [
    lv('no_espionage', 'No Espionage', 'No espionage.'),
    lv('defensive_espionage', 'Defensive', 'Counter-intelligence only.'),
    lv('active_espionage', 'Active', 'Full operations abroad.'),
    lv('aggressive_espionage', 'Aggressive', 'Sabotage and destabilisation.'),
  ]),
  cat('war_policy', 'War Policy', 1, [
    lv('absolute_pacifism', 'Absolute Pacifism', 'War is never justified.'),
    lv('defensive_war', 'Defensive War Only', 'War only in self-defence.'),
    lv('just_war', 'Just War', 'War for legitimate causes.'),
    lv('preemptive_war', 'Preemptive War', 'Strike first to prevent threats.'),
    lv('total_war', 'Total War', 'War by any means necessary.'),
  ]),
];

export const POLICY_MAP: Record<string, PolicyCategory> = {};
for (const cat of POLICY_CATEGORIES) {
  POLICY_MAP[cat.key] = cat;
}
