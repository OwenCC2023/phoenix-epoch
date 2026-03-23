"""
Policy category definitions.

67 categories, each with 2-10 discrete levels. Policies interact with traits —
traits modify how popular or effective certain policy types are.

Each level has:
  - key: machine-readable identifier
  - name: display name
  - description: player-facing text
  - tags: list of strings for trait interaction (e.g. "authoritarian", "pacifist")
  - effects: dict of simulation effects (mostly stubs for now)

Tag vocabulary:
  conservative, progressive, redistributive, subsidy, authoritarian, libertarian,
  meritocratic, corrupt, patronage, militaristic, pacifist, isolationist,
  internationalist, nationalist, religious, secular, traditional, modern,
  industrial, ecological, collectivist, individualist
"""

POLICY_CATEGORIES = {
    # ===== MILITARY (7 categories) =====
    "military_service": {
        "name": "Military Service",
        "default_level": 1,
        "levels": [
            {"key": "disarmed_nation", "name": "Disarmed Nation", "description": "The country maintains only a token military force.", "tags": ["pacifist"], "effects": {}},
            {"key": "volunteer_only", "name": "Volunteer Only", "description": "Military relies entirely on volunteers.", "tags": [], "effects": {}},
            {"key": "limited_conscription", "name": "Limited Conscription", "description": "Selective service for a small portion of the population.", "tags": ["authoritarian"], "effects": {}},
            {"key": "extensive_conscription", "name": "Extensive Conscription", "description": "Most able-bodied citizens serve a period of military duty.", "tags": ["authoritarian", "militaristic"], "effects": {}},
            {"key": "universal_service", "name": "Universal Service", "description": "All citizens are required to serve.", "tags": ["authoritarian", "militaristic"], "effects": {}},
            {"key": "service_by_requirement", "name": "Service by Requirement", "description": "Citizens are called up based on national need.", "tags": ["authoritarian", "militaristic"], "effects": {}},
            {"key": "scraping_the_barrel", "name": "Scraping the Barrel", "description": "Everyone who can hold a weapon is conscripted.", "tags": ["authoritarian", "militaristic"], "effects": {}},
        ],
    },
    "military_spending": {
        "name": "Military Spending",
        "default_level": 1,
        "levels": [
            {"key": "minimal_military", "name": "Minimal Military Budget", "description": "Bare minimum military funding.", "tags": ["pacifist"], "effects": {}},
            {"key": "low_military", "name": "Low Military Budget", "description": "Below-average military spending.", "tags": [], "effects": {}},
            {"key": "moderate_military", "name": "Moderate Military Budget", "description": "Standard military funding.", "tags": [], "effects": {}},
            {"key": "high_military", "name": "High Military Budget", "description": "Above-average military spending.", "tags": ["militaristic"], "effects": {}},
            {"key": "war_economy", "name": "War Economy", "description": "The economy is geared toward military production.", "tags": ["militaristic", "authoritarian"], "effects": {}},
        ],
    },
    "military_doctrine": {
        "name": "Military Doctrine",
        "default_level": 0,
        "levels": [
            {"key": "static_defence", "name": "Static Defence", "description": "Focus on fortifications and defensive positions.", "tags": ["conservative"], "effects": {}},
            {"key": "mobile_warfare", "name": "Mobile Warfare", "description": "Emphasis on rapid movement and flanking.", "tags": ["modern"], "effects": {}},
            {"key": "guerrilla_warfare", "name": "Guerrilla Warfare", "description": "Asymmetric tactics and ambushes.", "tags": [], "effects": {}},
            {"key": "combined_arms", "name": "Combined Arms", "description": "Coordinated use of infantry, armour, and support.", "tags": ["modern"], "effects": {}},
        ],
    },
    "veterans_policy": {
        "name": "Veterans Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_veterans_support", "name": "No Support", "description": "Veterans receive no special treatment.", "tags": [], "effects": {}},
            {"key": "basic_veterans_care", "name": "Basic Care", "description": "Minimal medical care for wounded veterans.", "tags": [], "effects": {}},
            {"key": "veterans_benefits", "name": "Veterans Benefits", "description": "Land grants and pensions for service.", "tags": ["subsidy"], "effects": {}},
            {"key": "hero_worship", "name": "Hero Worship", "description": "Veterans are elevated to a privileged class.", "tags": ["militaristic", "nationalist"], "effects": {}},
        ],
    },
    "border_policy": {
        "name": "Border Policy",
        "default_level": 1,
        "levels": [
            {"key": "open_borders", "name": "Open Borders", "description": "Free movement across national boundaries.", "tags": ["internationalist", "libertarian"], "effects": {}},
            {"key": "monitored_borders", "name": "Monitored Borders", "description": "Border crossings are tracked but not restricted.", "tags": [], "effects": {}},
            {"key": "controlled_borders", "name": "Controlled Borders", "description": "Entry requires documentation and approval.", "tags": ["nationalist"], "effects": {}},
            {"key": "restricted_borders", "name": "Restricted Borders", "description": "Only approved travellers may enter.", "tags": ["nationalist", "authoritarian"], "effects": {}},
            {"key": "closed_borders", "name": "Closed Borders", "description": "No foreign entry permitted.", "tags": ["isolationist", "authoritarian"], "effects": {}},
        ],
    },
    "weapons_policy": {
        "name": "Weapons Policy",
        "default_level": 1,
        "levels": [
            {"key": "universal_arms", "name": "Universal Right to Arms", "description": "All citizens may bear weapons freely.", "tags": ["libertarian", "militaristic"], "effects": {}},
            {"key": "licensed_arms", "name": "Licensed Ownership", "description": "Weapons require registration and licensing.", "tags": [], "effects": {}},
            {"key": "restricted_arms", "name": "Restricted Ownership", "description": "Only approved citizens may own weapons.", "tags": ["authoritarian"], "effects": {}},
            {"key": "state_monopoly_arms", "name": "State Monopoly on Arms", "description": "Only the military and police may possess weapons.", "tags": ["authoritarian", "pacifist"], "effects": {}},
        ],
    },
    "intelligence_policy": {
        "name": "Intelligence Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_intelligence", "name": "No Intelligence Service", "description": "The nation has no organised intelligence apparatus.", "tags": ["pacifist"], "effects": {}},
            {"key": "basic_intelligence", "name": "Basic Intelligence", "description": "A small intelligence bureau handles basic information.", "tags": [], "effects": {}},
            {"key": "active_intelligence", "name": "Active Intelligence", "description": "Dedicated intelligence service with foreign operations.", "tags": ["authoritarian"], "effects": {}},
            {"key": "pervasive_surveillance", "name": "Pervasive Surveillance", "description": "Comprehensive domestic and foreign intelligence.", "tags": ["authoritarian"], "effects": {}},
        ],
    },

    # ===== ECONOMY (12 categories) =====
    "economic_system": {
        "name": "Economic System",
        "default_level": 2,
        "levels": [
            {"key": "free_market", "name": "Free Market", "description": "Minimal government intervention in the economy.", "tags": ["libertarian", "individualist"], "effects": {}},
            {"key": "mixed_economy", "name": "Mixed Economy", "description": "Government regulates key sectors while allowing private enterprise.", "tags": [], "effects": {}},
            {"key": "managed_economy", "name": "Managed Economy", "description": "Government directs major economic decisions.", "tags": ["authoritarian"], "effects": {}},
            {"key": "command_economy", "name": "Command Economy", "description": "The state controls all production and distribution.", "tags": ["authoritarian", "collectivist"], "effects": {}},
            {"key": "barter_economy", "name": "Barter Economy", "description": "Trade is conducted through direct exchange of goods.", "tags": ["traditional"], "effects": {}},
        ],
    },
    "taxation": {
        "name": "Taxation",
        "default_level": 2,
        "levels": [
            {"key": "no_taxes", "name": "No Taxation", "description": "The government does not levy taxes.", "tags": ["libertarian"], "effects": {}},
            {"key": "low_taxes", "name": "Low Taxation", "description": "Minimal taxation to fund basic services.", "tags": ["individualist"], "effects": {}},
            {"key": "moderate_taxes", "name": "Moderate Taxation", "description": "Standard taxation to fund government operations.", "tags": [], "effects": {}},
            {"key": "high_taxes", "name": "High Taxation", "description": "Heavy taxation to fund extensive government programs.", "tags": ["collectivist", "redistributive"], "effects": {}},
            {"key": "confiscatory_taxes", "name": "Confiscatory Taxation", "description": "Near-total appropriation of private wealth.", "tags": ["authoritarian", "collectivist"], "effects": {}},
        ],
    },
    "trade_policy": {
        "name": "Trade Policy",
        "default_level": 1,
        "levels": [
            {"key": "free_trade", "name": "Free Trade", "description": "No restrictions on imports or exports.", "tags": ["internationalist", "libertarian"], "effects": {}},
            {"key": "moderate_tariffs", "name": "Moderate Tariffs", "description": "Tariffs on selected goods to protect local industry.", "tags": [], "effects": {}},
            {"key": "protectionist", "name": "Protectionist", "description": "High tariffs and import quotas.", "tags": ["nationalist", "isolationist"], "effects": {}},
            {"key": "autarky", "name": "Autarky", "description": "Complete economic self-sufficiency; no foreign trade.", "tags": ["isolationist", "nationalist"], "effects": {}},
        ],
    },
    "currency_policy": {
        "name": "Currency Policy",
        "default_level": 1,
        "levels": [
            {"key": "commodity_money", "name": "Commodity Money", "description": "Trade uses physical commodities as currency.", "tags": ["traditional"], "effects": {}},
            {"key": "backed_currency", "name": "Backed Currency", "description": "Paper currency backed by material reserves.", "tags": ["conservative"], "effects": {}},
            {"key": "fiat_currency", "name": "Fiat Currency", "description": "Government-issued currency not backed by commodities.", "tags": ["modern"], "effects": {}},
        ],
    },
    "property_rights": {
        "name": "Property Rights",
        "default_level": 1,
        "levels": [
            {"key": "communal_property", "name": "Communal Property", "description": "All major property is communally owned.", "tags": ["collectivist"], "effects": {}},
            {"key": "mixed_property", "name": "Mixed Property", "description": "Private property with significant state ownership.", "tags": [], "effects": {}},
            {"key": "strong_property", "name": "Strong Property Rights", "description": "Robust legal protection of private property.", "tags": ["individualist", "libertarian"], "effects": {}},
        ],
    },
    "labour_policy": {
        "name": "Labour Policy",
        "default_level": 1,
        "levels": [
            {"key": "forced_labour", "name": "Forced Labour", "description": "The state can compel labour for public works.", "tags": ["authoritarian"], "effects": {}},
            {"key": "regulated_labour", "name": "Regulated Labour", "description": "Basic labour protections and working standards.", "tags": [], "effects": {}},
            {"key": "worker_councils", "name": "Worker Councils", "description": "Workers have significant say in workplace decisions.", "tags": ["collectivist", "progressive"], "effects": {}},
            {"key": "free_labour", "name": "Free Labour Market", "description": "No government regulation of labour.", "tags": ["libertarian", "individualist"], "effects": {}},
        ],
    },
    "banking_policy": {
        "name": "Banking Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_banking", "name": "No Formal Banking", "description": "No organised banking system exists.", "tags": ["traditional"], "effects": {}},
            {"key": "state_banking", "name": "State Banking", "description": "All banking is conducted through state institutions.", "tags": ["collectivist", "authoritarian"], "effects": {}},
            {"key": "regulated_banking", "name": "Regulated Banking", "description": "Private banks operate under government oversight.", "tags": [], "effects": {}},
            {"key": "free_banking", "name": "Free Banking", "description": "Banks operate with minimal regulation.", "tags": ["libertarian"], "effects": {}},
        ],
    },
    "resource_extraction": {
        "name": "Resource Extraction",
        "default_level": 1,
        "levels": [
            {"key": "state_extraction", "name": "State Monopoly", "description": "All natural resources are extracted by the state.", "tags": ["collectivist", "authoritarian"], "effects": {}},
            {"key": "licensed_extraction", "name": "Licensed Extraction", "description": "Private companies may extract resources with government licences.", "tags": [], "effects": {}},
            {"key": "unregulated_extraction", "name": "Unregulated Extraction", "description": "Anyone can extract resources freely.", "tags": ["libertarian"], "effects": {}},
            {"key": "conservation_priority", "name": "Conservation Priority", "description": "Extraction is heavily limited to protect the environment.", "tags": ["ecological"], "effects": {}},
        ],
    },
    "food_distribution": {
        "name": "Food Distribution",
        "default_level": 1,
        "levels": [
            {"key": "free_market_food", "name": "Free Market", "description": "Food is bought and sold on the open market.", "tags": ["individualist"], "effects": {}},
            {"key": "subsidised_food", "name": "Subsidised Food", "description": "Government subsidies keep basic food affordable.", "tags": ["subsidy"], "effects": {}},
            {"key": "rationing", "name": "Rationing", "description": "Food is distributed through government ration cards.", "tags": ["authoritarian", "collectivist"], "effects": {}},
            {"key": "communal_kitchens", "name": "Communal Kitchens", "description": "Community-run kitchens feed the population.", "tags": ["collectivist"], "effects": {}},
        ],
    },
    "infrastructure_policy": {
        "name": "Infrastructure Policy",
        "default_level": 1,
        "levels": [
            {"key": "neglected_infrastructure", "name": "Neglected", "description": "Infrastructure receives minimal maintenance.", "tags": [], "effects": {}},
            {"key": "maintained_infrastructure", "name": "Maintained", "description": "Existing infrastructure is kept in working order.", "tags": [], "effects": {}},
            {"key": "expanding_infrastructure", "name": "Expanding", "description": "Active construction of new infrastructure.", "tags": ["industrial"], "effects": {}},
            {"key": "megaproject_infrastructure", "name": "Megaprojects", "description": "Ambitious large-scale infrastructure programs.", "tags": ["industrial", "authoritarian"], "effects": {}},
        ],
    },
    "energy_policy": {
        "name": "Energy Policy",
        "default_level": 1,
        "levels": [
            {"key": "biomass_energy", "name": "Biomass Only", "description": "Energy comes from wood, dung, and organic waste.", "tags": ["traditional"], "effects": {}},
            {"key": "fossil_fuel_energy", "name": "Fossil Fuels", "description": "Oil and coal drive energy production.", "tags": ["industrial"], "effects": {}},
            {"key": "mixed_energy", "name": "Mixed Sources", "description": "A combination of fuel types.", "tags": [], "effects": {}},
            {"key": "renewable_energy", "name": "Renewable Focus", "description": "Investment in wind, water, and solar energy.", "tags": ["ecological", "modern"], "effects": {}},
        ],
    },

    # ===== SOCIAL (12 categories) =====
    "education_policy": {
        "name": "Education Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_education", "name": "No Public Education", "description": "Education is left to families and communities.", "tags": ["traditional"], "effects": {}},
            {"key": "basic_education", "name": "Basic Literacy", "description": "Government provides basic reading and writing instruction.", "tags": [], "effects": {}},
            {"key": "primary_education", "name": "Primary Education", "description": "Free primary schooling for all children.", "tags": ["progressive"], "effects": {}},
            {"key": "secondary_education", "name": "Secondary Education", "description": "Free education through secondary school.", "tags": ["progressive"], "effects": {}},
            {"key": "universal_education", "name": "Universal Education", "description": "Free education at all levels including higher education.", "tags": ["progressive", "collectivist"], "effects": {}},
        ],
    },
    "healthcare_policy": {
        "name": "Healthcare Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_healthcare", "name": "No Public Healthcare", "description": "Healthcare is entirely private.", "tags": ["libertarian"], "effects": {}},
            {"key": "basic_healthcare", "name": "Basic Healthcare", "description": "Government provides basic medical care.", "tags": [], "effects": {}},
            {"key": "public_healthcare", "name": "Public Healthcare", "description": "Comprehensive government-funded healthcare.", "tags": ["collectivist", "progressive"], "effects": {}},
            {"key": "universal_healthcare", "name": "Universal Healthcare", "description": "Free healthcare for all citizens.", "tags": ["collectivist", "progressive"], "effects": {}},
        ],
    },
    "housing_policy": {
        "name": "Housing Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_housing_policy", "name": "No Government Housing", "description": "Housing is entirely market-driven.", "tags": ["libertarian"], "effects": {}},
            {"key": "housing_assistance", "name": "Housing Assistance", "description": "Government provides housing subsidies.", "tags": ["subsidy"], "effects": {}},
            {"key": "public_housing", "name": "Public Housing", "description": "Government builds and maintains housing blocks.", "tags": ["collectivist"], "effects": {}},
            {"key": "assigned_housing", "name": "Assigned Housing", "description": "Government assigns housing to all citizens.", "tags": ["authoritarian", "collectivist"], "effects": {}},
        ],
    },
    "welfare_policy": {
        "name": "Welfare Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_welfare", "name": "No Welfare", "description": "No government welfare programs.", "tags": ["libertarian", "individualist"], "effects": {}},
            {"key": "minimal_welfare", "name": "Minimal Safety Net", "description": "Basic support for the destitute.", "tags": [], "effects": {}},
            {"key": "moderate_welfare", "name": "Moderate Welfare", "description": "Support for the unemployed and disadvantaged.", "tags": ["progressive", "redistributive"], "effects": {}},
            {"key": "comprehensive_welfare", "name": "Comprehensive Welfare", "description": "Extensive social safety net.", "tags": ["collectivist", "redistributive"], "effects": {}},
            {"key": "universal_income", "name": "Universal Income", "description": "All citizens receive a basic income.", "tags": ["collectivist", "progressive", "redistributive"], "effects": {}},
        ],
    },
    "religion_policy": {
        "name": "Religion Policy",
        "default_level": 1,
        "levels": [
            {"key": "state_atheism", "name": "State Atheism", "description": "Religion is officially discouraged or banned.", "tags": ["authoritarian", "secular"], "effects": {}},
            {"key": "secular_state", "name": "Secular State", "description": "Government is separate from religion.", "tags": ["secular"], "effects": {}},
            {"key": "religious_tolerance", "name": "Religious Tolerance", "description": "All religions are accepted and protected.", "tags": [], "effects": {}},
            {"key": "state_religion", "name": "State Religion", "description": "One religion is officially endorsed.", "tags": ["religious", "conservative"], "effects": {}},
            {"key": "theocratic_law", "name": "Theocratic Law", "description": "Religious law is the law of the land.", "tags": ["religious", "authoritarian", "conservative"], "effects": {}},
        ],
    },
    "press_freedom": {
        "name": "Press Freedom",
        "default_level": 1,
        "levels": [
            {"key": "free_press", "name": "Free Press", "description": "No government control over media.", "tags": ["libertarian", "progressive"], "effects": {}},
            {"key": "regulated_press", "name": "Regulated Press", "description": "Government oversight of media with some restrictions.", "tags": [], "effects": {}},
            {"key": "censored_press", "name": "Censored Press", "description": "Government actively censors critical media.", "tags": ["authoritarian"], "effects": {}},
            {"key": "state_media", "name": "State Media Only", "description": "All media is owned and operated by the state.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "justice_system": {
        "name": "Justice System",
        "default_level": 1,
        "levels": [
            {"key": "tribal_justice", "name": "Tribal Justice", "description": "Disputes are settled by community elders.", "tags": ["traditional"], "effects": {}},
            {"key": "codified_law", "name": "Codified Law", "description": "Written laws and formal courts.", "tags": [], "effects": {}},
            {"key": "restorative_justice", "name": "Restorative Justice", "description": "Focus on rehabilitation and reconciliation.", "tags": ["progressive"], "effects": {}},
            {"key": "harsh_penalties", "name": "Harsh Penalties", "description": "Severe punishments to deter crime.", "tags": ["authoritarian", "conservative"], "effects": {}},
        ],
    },
    "assembly_rights": {
        "name": "Assembly Rights",
        "default_level": 1,
        "levels": [
            {"key": "free_assembly", "name": "Free Assembly", "description": "Citizens may gather and organise freely.", "tags": ["libertarian", "progressive"], "effects": {}},
            {"key": "regulated_assembly", "name": "Regulated Assembly", "description": "Public gatherings require permits.", "tags": [], "effects": {}},
            {"key": "restricted_assembly", "name": "Restricted Assembly", "description": "Only government-approved gatherings are permitted.", "tags": ["authoritarian"], "effects": {}},
            {"key": "no_assembly", "name": "No Assembly", "description": "Public gatherings are banned.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "citizenship_policy": {
        "name": "Citizenship Policy",
        "default_level": 1,
        "levels": [
            {"key": "open_citizenship", "name": "Open Citizenship", "description": "Anyone can become a citizen with minimal requirements.", "tags": ["internationalist", "progressive"], "effects": {}},
            {"key": "residency_citizenship", "name": "Residency-Based", "description": "Citizenship after a period of residency.", "tags": [], "effects": {}},
            {"key": "blood_citizenship", "name": "Blood-Based", "description": "Citizenship is hereditary only.", "tags": ["nationalist", "conservative"], "effects": {}},
            {"key": "merit_citizenship", "name": "Merit-Based", "description": "Citizenship requires demonstrated contribution.", "tags": ["meritocratic"], "effects": {}},
        ],
    },
    "migration_policy": {
        "name": "Migration Policy",
        "default_level": 1,
        "levels": [
            {"key": "welcome_migrants", "name": "Welcome Migrants", "description": "Active recruitment of foreign settlers.", "tags": ["internationalist", "progressive"], "effects": {}},
            {"key": "accept_migrants", "name": "Accept Migrants", "description": "Migrants are accepted if they meet basic criteria.", "tags": [], "effects": {}},
            {"key": "restrict_migrants", "name": "Restrict Migrants", "description": "Strict limits on immigration.", "tags": ["nationalist"], "effects": {}},
            {"key": "no_immigration", "name": "No Immigration", "description": "Borders are closed to all newcomers.", "tags": ["isolationist", "nationalist"], "effects": {}},
        ],
    },
    "social_mobility": {
        "name": "Social Mobility",
        "default_level": 1,
        "levels": [
            {"key": "caste_system", "name": "Caste System", "description": "Social position is fixed at birth.", "tags": ["traditional", "conservative"], "effects": {}},
            {"key": "limited_mobility", "name": "Limited Mobility", "description": "Social advancement is possible but difficult.", "tags": [], "effects": {}},
            {"key": "meritocratic_mobility", "name": "Meritocratic", "description": "Advancement is based on ability and effort.", "tags": ["meritocratic", "progressive"], "effects": {}},
            {"key": "egalitarian_mobility", "name": "Egalitarian", "description": "Active efforts to eliminate class barriers.", "tags": ["collectivist", "progressive", "redistributive"], "effects": {}},
        ],
    },
    "minority_rights": {
        "name": "Minority Rights",
        "default_level": 1,
        "levels": [
            {"key": "persecution", "name": "Persecution", "description": "Minorities face active discrimination.", "tags": ["authoritarian", "nationalist"], "effects": {}},
            {"key": "tolerance", "name": "Tolerance", "description": "Minorities are tolerated but not protected.", "tags": [], "effects": {}},
            {"key": "protection", "name": "Protected Rights", "description": "Legal protections for minority groups.", "tags": ["progressive"], "effects": {}},
            {"key": "full_equality", "name": "Full Equality", "description": "Active efforts to ensure equal treatment.", "tags": ["progressive", "internationalist"], "effects": {}},
        ],
    },

    # ===== GOVERNANCE (10 categories) =====
    "government_transparency": {
        "name": "Government Transparency",
        "default_level": 1,
        "levels": [
            {"key": "total_secrecy", "name": "Total Secrecy", "description": "Government operations are completely opaque.", "tags": ["authoritarian"], "effects": {}},
            {"key": "selective_disclosure", "name": "Selective Disclosure", "description": "Government shares information selectively.", "tags": [], "effects": {}},
            {"key": "open_government", "name": "Open Government", "description": "Government records are publicly available.", "tags": ["progressive", "libertarian"], "effects": {}},
        ],
    },
    "corruption_policy": {
        "name": "Anti-Corruption Policy",
        "default_level": 1,
        "levels": [
            {"key": "endemic_corruption", "name": "Endemic Corruption", "description": "Corruption is widespread and accepted.", "tags": ["corrupt"], "effects": {}},
            {"key": "tolerated_corruption", "name": "Tolerated Corruption", "description": "Corruption exists but is not actively addressed.", "tags": ["corrupt"], "effects": {}},
            {"key": "anti_corruption", "name": "Anti-Corruption Measures", "description": "Active efforts to reduce corruption.", "tags": [], "effects": {}},
            {"key": "zero_tolerance", "name": "Zero Tolerance", "description": "Harsh penalties for any form of corruption.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "bureaucratic_structure": {
        "name": "Bureaucratic Structure",
        "default_level": 1,
        "levels": [
            {"key": "minimal_bureaucracy", "name": "Minimal Bureaucracy", "description": "Government functions with a skeleton staff.", "tags": ["libertarian"], "effects": {}},
            {"key": "functional_bureaucracy", "name": "Functional Bureaucracy", "description": "Adequate staffing for government functions.", "tags": [], "effects": {}},
            {"key": "expansive_bureaucracy", "name": "Expansive Bureaucracy", "description": "Large government apparatus with many departments.", "tags": ["authoritarian"], "effects": {}},
            {"key": "total_administration", "name": "Total Administration", "description": "Government administers nearly all aspects of life.", "tags": ["authoritarian", "collectivist"], "effects": {}},
        ],
    },
    "political_parties": {
        "name": "Political Parties",
        "default_level": 1,
        "levels": [
            {"key": "no_parties", "name": "No Parties", "description": "Political parties are banned.", "tags": ["authoritarian"], "effects": {}},
            {"key": "single_party", "name": "Single Party", "description": "Only one political party is permitted.", "tags": ["authoritarian"], "effects": {}},
            {"key": "limited_parties", "name": "Limited Parties", "description": "A few approved political parties exist.", "tags": [], "effects": {}},
            {"key": "multi_party", "name": "Multi-Party", "description": "Multiple parties compete freely.", "tags": ["progressive", "libertarian"], "effects": {}},
        ],
    },
    "local_governance": {
        "name": "Local Governance",
        "default_level": 1,
        "levels": [
            {"key": "centralised", "name": "Centralised", "description": "All decisions come from the capital.", "tags": ["authoritarian"], "effects": {}},
            {"key": "delegated", "name": "Delegated Authority", "description": "Local officials carry out central directives.", "tags": [], "effects": {}},
            {"key": "devolved", "name": "Devolved Government", "description": "Provinces have significant autonomy.", "tags": ["libertarian"], "effects": {}},
            {"key": "federal", "name": "Federal System", "description": "Provinces are self-governing in most matters.", "tags": ["libertarian"], "effects": {}},
        ],
    },
    "succession_policy": {
        "name": "Succession Policy",
        "default_level": 1,
        "levels": [
            {"key": "hereditary", "name": "Hereditary", "description": "Leadership passes through family lines.", "tags": ["traditional", "conservative"], "effects": {}},
            {"key": "appointed_successor", "name": "Appointed Successor", "description": "Current leader chooses their successor.", "tags": ["authoritarian"], "effects": {}},
            {"key": "elected_leader", "name": "Elected Leader", "description": "Leadership is determined by election.", "tags": ["progressive"], "effects": {}},
            {"key": "council_selected", "name": "Council Selected", "description": "A governing council selects the leader.", "tags": [], "effects": {}},
        ],
    },
    "civil_service": {
        "name": "Civil Service",
        "default_level": 1,
        "levels": [
            {"key": "patronage_system", "name": "Patronage System", "description": "Government positions are awarded based on loyalty.", "tags": ["patronage", "corrupt"], "effects": {}},
            {"key": "basic_civil_service", "name": "Basic Civil Service", "description": "Government workers are hired on basic qualifications.", "tags": [], "effects": {}},
            {"key": "professional_civil_service", "name": "Professional Civil Service", "description": "Merit-based hiring with career progression.", "tags": ["meritocratic"], "effects": {}},
            {"key": "technocratic_service", "name": "Technocratic Service", "description": "Government positions require technical expertise.", "tags": ["meritocratic", "modern"], "effects": {}},
        ],
    },
    "emergency_powers": {
        "name": "Emergency Powers",
        "default_level": 1,
        "levels": [
            {"key": "no_emergency_powers", "name": "No Emergency Powers", "description": "Government has no special crisis authority.", "tags": ["libertarian"], "effects": {}},
            {"key": "limited_emergency", "name": "Limited Emergency Powers", "description": "Government can take limited action in crises.", "tags": [], "effects": {}},
            {"key": "broad_emergency", "name": "Broad Emergency Powers", "description": "Government can suspend rights during emergencies.", "tags": ["authoritarian"], "effects": {}},
            {"key": "permanent_emergency", "name": "Permanent State of Emergency", "description": "Emergency powers are always in effect.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "diplomatic_stance": {
        "name": "Diplomatic Stance",
        "default_level": 1,
        "levels": [
            {"key": "isolationism", "name": "Isolationism", "description": "Minimal engagement with other nations.", "tags": ["isolationist"], "effects": {}},
            {"key": "cautious_engagement", "name": "Cautious Engagement", "description": "Selective diplomatic relationships.", "tags": [], "effects": {}},
            {"key": "active_diplomacy", "name": "Active Diplomacy", "description": "Vigorous pursuit of international relationships.", "tags": ["internationalist"], "effects": {}},
            {"key": "alliance_seeking", "name": "Alliance Seeking", "description": "Actively building alliance blocs.", "tags": ["internationalist"], "effects": {}},
        ],
    },
    "propaganda_policy": {
        "name": "Propaganda Policy",
        "default_level": 0,
        "levels": [
            {"key": "no_propaganda", "name": "No Propaganda", "description": "Government does not engage in propaganda.", "tags": ["libertarian"], "effects": {}},
            {"key": "public_information", "name": "Public Information", "description": "Government information campaigns on factual matters.", "tags": [], "effects": {}},
            {"key": "state_messaging", "name": "State Messaging", "description": "Government promotes its narrative through media.", "tags": ["authoritarian"], "effects": {}},
            {"key": "total_propaganda", "name": "Total Propaganda", "description": "All information is filtered through government messaging.", "tags": ["authoritarian"], "effects": {}},
        ],
    },

    # ===== INDUSTRY & PRODUCTION (8 categories) =====
    "industrial_policy": {
        "name": "Industrial Policy",
        "default_level": 1,
        "levels": [
            {"key": "agrarian_focus", "name": "Agrarian Focus", "description": "The economy prioritises agriculture.", "tags": ["traditional"], "effects": {}},
            {"key": "balanced_development", "name": "Balanced Development", "description": "Even investment across sectors.", "tags": [], "effects": {}},
            {"key": "industrialisation_drive", "name": "Industrialisation Drive", "description": "Aggressive push toward factory production.", "tags": ["industrial", "modern"], "effects": {}},
            {"key": "high_tech_focus", "name": "High-Tech Focus", "description": "Investment in advanced manufacturing and research.", "tags": ["modern"], "effects": {}},
        ],
    },
    "construction_regulation": {
        "name": "Construction Regulation",
        "default_level": 1,
        "levels": [
            {"key": "no_regulations", "name": "No Regulations", "description": "Build anything, anywhere.", "tags": ["libertarian"], "effects": {}},
            {"key": "basic_codes", "name": "Basic Building Codes", "description": "Minimal safety and planning requirements.", "tags": [], "effects": {}},
            {"key": "comprehensive_planning", "name": "Comprehensive Planning", "description": "Government approves all construction projects.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "environmental_policy": {
        "name": "Environmental Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_environmental", "name": "No Environmental Policy", "description": "No environmental protections.", "tags": ["industrial"], "effects": {}},
            {"key": "basic_environmental", "name": "Basic Protections", "description": "Minimal environmental standards.", "tags": [], "effects": {}},
            {"key": "strict_environmental", "name": "Strict Protections", "description": "Strong environmental regulations.", "tags": ["ecological"], "effects": {}},
            {"key": "deep_ecology", "name": "Deep Ecology", "description": "Environment takes priority over economic growth.", "tags": ["ecological"], "effects": {}},
        ],
    },
    "agriculture_policy": {
        "name": "Agriculture Policy",
        "default_level": 1,
        "levels": [
            {"key": "subsistence_farming", "name": "Subsistence Farming", "description": "Each community grows its own food.", "tags": ["traditional"], "effects": {}},
            {"key": "mixed_agriculture", "name": "Mixed Agriculture", "description": "Combination of small and large farms.", "tags": [], "effects": {}},
            {"key": "collective_farms", "name": "Collective Farms", "description": "Government-organised collective agriculture.", "tags": ["collectivist"], "effects": {}},
            {"key": "industrial_agriculture", "name": "Industrial Agriculture", "description": "Large-scale mechanised farming.", "tags": ["industrial", "modern"], "effects": {}},
        ],
    },
    "manufacturing_policy": {
        "name": "Manufacturing Policy",
        "default_level": 1,
        "levels": [
            {"key": "cottage_industry", "name": "Cottage Industry", "description": "Small-scale home-based production.", "tags": ["traditional"], "effects": {}},
            {"key": "workshop_economy", "name": "Workshop Economy", "description": "Organised workshops and small factories.", "tags": [], "effects": {}},
            {"key": "factory_system", "name": "Factory System", "description": "Large-scale factory production.", "tags": ["industrial"], "effects": {}},
            {"key": "automated_production", "name": "Automated Production", "description": "Highly mechanised production lines.", "tags": ["modern", "industrial"], "effects": {}},
        ],
    },
    "research_policy": {
        "name": "Research Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_research_policy", "name": "No Organised Research", "description": "Research happens informally.", "tags": ["traditional"], "effects": {}},
            {"key": "practical_research", "name": "Practical Research", "description": "Research focused on immediate practical needs.", "tags": [], "effects": {}},
            {"key": "academic_research", "name": "Academic Research", "description": "Formal research institutions and universities.", "tags": ["modern", "progressive"], "effects": {}},
            {"key": "state_research", "name": "State-Directed Research", "description": "Government sets research priorities.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "salvage_policy": {
        "name": "Salvage Policy",
        "default_level": 1,
        "levels": [
            {"key": "free_salvage", "name": "Free Salvage", "description": "Anyone can loot old-world ruins.", "tags": ["libertarian"], "effects": {}},
            {"key": "regulated_salvage", "name": "Regulated Salvage", "description": "Salvage rights are licensed by government.", "tags": [], "effects": {}},
            {"key": "state_salvage", "name": "State Salvage", "description": "Only government teams may enter ruins.", "tags": ["authoritarian", "collectivist"], "effects": {}},
        ],
    },
    "technology_adoption": {
        "name": "Technology Adoption",
        "default_level": 1,
        "levels": [
            {"key": "tech_rejection", "name": "Technology Rejection", "description": "Old-world technology is feared and avoided.", "tags": ["traditional"], "effects": {}},
            {"key": "cautious_adoption", "name": "Cautious Adoption", "description": "New technology is tested carefully before widespread use.", "tags": ["conservative"], "effects": {}},
            {"key": "enthusiastic_adoption", "name": "Enthusiastic Adoption", "description": "New technology is eagerly embraced.", "tags": ["modern", "progressive"], "effects": {}},
        ],
    },
    "rationing": {
        "name": "Rationing",
        "default_level": 0,
        "levels": [
            {
                "key": "no_rationing",
                "name": "No Rationing",
                "description": "All sectors compete for goods on equal terms. Shortages are shared proportionally across civilian, military, and government buildings, and military units.",
                "tags": ["libertarian"],
                "effects": {},
            },
            {
                "key": "civilian_priority",
                "name": "Civilian Priority",
                "description": "Civilian production is fully served before military or government buildings receive inputs. Military units and government buildings share whatever remains, with units given priority within the military allocation.",
                "tags": ["collectivist"],
                "effects": {},
            },
            {
                "key": "military_priority",
                "name": "Military Priority",
                "description": "Military is fully served first: units receive inputs before military buildings, then military buildings are served. Civilian and government buildings share whatever remains proportionally.",
                "tags": ["militaristic", "authoritarian"],
                "effects": {},
            },
            {
                "key": "government_priority",
                "name": "Government Priority",
                "description": "Government infrastructure and services are fully served first. Civilian and military (units before buildings) share whatever remains proportionally.",
                "tags": ["authoritarian"],
                "effects": {},
            },
        ],
    },

    # ===== CULTURE & IDENTITY (8 categories) =====
    "cultural_policy": {
        "name": "Cultural Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_cultural_policy", "name": "No Cultural Policy", "description": "Culture develops organically.", "tags": ["libertarian"], "effects": {}},
            {"key": "cultural_preservation", "name": "Cultural Preservation", "description": "Government protects traditional culture.", "tags": ["conservative", "traditional"], "effects": {}},
            {"key": "cultural_promotion", "name": "Cultural Promotion", "description": "Government actively promotes national culture.", "tags": ["nationalist"], "effects": {}},
            {"key": "cultural_revolution", "name": "Cultural Revolution", "description": "Active transformation of cultural values.", "tags": ["progressive", "authoritarian"], "effects": {}},
        ],
    },
    "language_policy": {
        "name": "Language Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_language_policy", "name": "No Language Policy", "description": "People speak whatever language they choose.", "tags": ["libertarian"], "effects": {}},
            {"key": "official_language", "name": "Official Language", "description": "One language is used for government business.", "tags": [], "effects": {}},
            {"key": "multilingual", "name": "Multilingual", "description": "Multiple languages are officially recognised.", "tags": ["internationalist"], "effects": {}},
            {"key": "language_enforcement", "name": "Language Enforcement", "description": "All citizens must speak the national language.", "tags": ["nationalist", "authoritarian"], "effects": {}},
        ],
    },
    "arts_policy": {
        "name": "Arts & Entertainment",
        "default_level": 1,
        "levels": [
            {"key": "no_arts_policy", "name": "No Support", "description": "The arts receive no government support.", "tags": ["libertarian"], "effects": {}},
            {"key": "arts_patronage", "name": "Patronage", "description": "Government sponsors artists and performers.", "tags": [], "effects": {}},
            {"key": "state_art", "name": "State Art", "description": "Art must serve the interests of the state.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "historical_narrative": {
        "name": "Historical Narrative",
        "default_level": 1,
        "levels": [
            {"key": "no_official_history", "name": "No Official History", "description": "Each community tells its own story of the past.", "tags": [], "effects": {}},
            {"key": "preservation_narrative", "name": "Preservation Narrative", "description": "Focus on preserving accurate records of the old world.", "tags": ["conservative"], "effects": {}},
            {"key": "rebirth_narrative", "name": "Rebirth Narrative", "description": "The apocalypse was a chance to start fresh.", "tags": ["progressive", "modern"], "effects": {}},
            {"key": "glory_narrative", "name": "Glory Narrative", "description": "The nation is destined for greatness.", "tags": ["nationalist"], "effects": {}},
        ],
    },
    "family_policy": {
        "name": "Family Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_family_policy", "name": "No Family Policy", "description": "Family matters are private.", "tags": ["libertarian"], "effects": {}},
            {"key": "pro_natalist", "name": "Pro-Natalist", "description": "Government encourages large families.", "tags": ["conservative", "nationalist"], "effects": {}},
            {"key": "family_planning", "name": "Family Planning", "description": "Government provides family planning resources.", "tags": ["progressive", "modern"], "effects": {}},
            {"key": "population_control", "name": "Population Control", "description": "Government limits family size.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "youth_policy": {
        "name": "Youth Policy",
        "default_level": 0,
        "levels": [
            {"key": "no_youth_policy", "name": "No Youth Policy", "description": "Children learn from their families.", "tags": [], "effects": {}},
            {"key": "youth_education", "name": "Youth Education", "description": "Government provides structured youth education.", "tags": ["progressive"], "effects": {}},
            {"key": "youth_organisations", "name": "Youth Organisations", "description": "Government-sponsored youth groups.", "tags": ["nationalist"], "effects": {}},
            {"key": "youth_militias", "name": "Youth Militias", "description": "Military training begins in youth.", "tags": ["militaristic", "authoritarian"], "effects": {}},
        ],
    },
    "gender_policy": {
        "name": "Gender Policy",
        "default_level": 1,
        "levels": [
            {"key": "traditional_roles", "name": "Traditional Roles", "description": "Traditional gender roles are enforced.", "tags": ["traditional", "conservative"], "effects": {}},
            {"key": "mixed_roles", "name": "Mixed Roles", "description": "Gender roles are flexible but not enforced.", "tags": [], "effects": {}},
            {"key": "full_equality", "name": "Full Equality", "description": "Complete gender equality in all spheres.", "tags": ["progressive"], "effects": {}},
        ],
    },
    "elder_policy": {
        "name": "Elder Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_elder_policy", "name": "No Support", "description": "Elderly are cared for by their families.", "tags": ["traditional"], "effects": {}},
            {"key": "basic_elder_care", "name": "Basic Care", "description": "Government provides basic elderly care.", "tags": [], "effects": {}},
            {"key": "elder_councils", "name": "Elder Councils", "description": "Elders serve as advisors and community leaders.", "tags": ["traditional", "conservative"], "effects": {}},
        ],
    },

    # ===== PUBLIC ORDER (5 categories) =====
    "policing_policy": {
        "name": "Policing Policy",
        "default_level": 1,
        "levels": [
            {"key": "community_watch", "name": "Community Watch", "description": "Volunteers maintain local order.", "tags": ["libertarian"], "effects": {}},
            {"key": "local_police", "name": "Local Police", "description": "Each community has its own police force.", "tags": [], "effects": {}},
            {"key": "national_police", "name": "National Police", "description": "Centralised police force under government control.", "tags": ["authoritarian"], "effects": {}},
            {"key": "military_police", "name": "Military Police", "description": "The military maintains civil order.", "tags": ["authoritarian", "militaristic"], "effects": {}},
        ],
    },
    "prison_policy": {
        "name": "Prison Policy",
        "default_level": 1,
        "levels": [
            {"key": "exile_punishment", "name": "Exile", "description": "Criminals are banished from the community.", "tags": ["traditional"], "effects": {}},
            {"key": "basic_prisons", "name": "Basic Prisons", "description": "Simple detention facilities.", "tags": [], "effects": {}},
            {"key": "rehabilitation", "name": "Rehabilitation", "description": "Focus on reforming criminals.", "tags": ["progressive"], "effects": {}},
            {"key": "labour_camps", "name": "Labour Camps", "description": "Prisoners perform forced labour.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "drug_policy": {
        "name": "Drug Policy",
        "default_level": 1,
        "levels": [
            {"key": "unregulated_drugs", "name": "Unregulated", "description": "No drug regulation.", "tags": ["libertarian"], "effects": {}},
            {"key": "medical_only", "name": "Medical Only", "description": "Drugs restricted to medical use.", "tags": [], "effects": {}},
            {"key": "total_prohibition", "name": "Total Prohibition", "description": "All recreational drugs are banned.", "tags": ["authoritarian", "conservative"], "effects": {}},
        ],
    },
    "curfew_policy": {
        "name": "Curfew Policy",
        "default_level": 0,
        "levels": [
            {"key": "no_curfew", "name": "No Curfew", "description": "Citizens are free to move at any time.", "tags": ["libertarian"], "effects": {}},
            {"key": "recommended_curfew", "name": "Recommended Curfew", "description": "Government suggests staying home at night.", "tags": [], "effects": {}},
            {"key": "mandatory_curfew", "name": "Mandatory Curfew", "description": "All citizens must be indoors by nightfall.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "identity_documents": {
        "name": "Identity Documents",
        "default_level": 1,
        "levels": [
            {"key": "no_documents", "name": "No Documents", "description": "No identity documents are required.", "tags": ["libertarian"], "effects": {}},
            {"key": "basic_registration", "name": "Basic Registration", "description": "Citizens are registered but carry no documents.", "tags": [], "effects": {}},
            {"key": "identity_cards", "name": "Identity Cards", "description": "All citizens carry government-issued identity.", "tags": ["authoritarian"], "effects": {}},
            {"key": "biometric_tracking", "name": "Biometric Tracking", "description": "Citizens are identified by biometric data.", "tags": ["authoritarian", "modern"], "effects": {}},
        ],
    },

    # ===== FOREIGN RELATIONS (5 categories) =====
    "alliance_policy": {
        "name": "Alliance Policy",
        "default_level": 1,
        "levels": [
            {"key": "no_alliances", "name": "No Alliances", "description": "The nation stands alone.", "tags": ["isolationist"], "effects": {}},
            {"key": "defensive_pacts", "name": "Defensive Pacts", "description": "Mutual defence agreements with select nations.", "tags": [], "effects": {}},
            {"key": "military_alliances", "name": "Military Alliances", "description": "Full military cooperation with allies.", "tags": ["internationalist", "militaristic"], "effects": {}},
            {"key": "federation_seeking", "name": "Federation Seeking", "description": "Working toward political union with allies.", "tags": ["internationalist"], "effects": {}},
        ],
    },
    "foreign_aid": {
        "name": "Foreign Aid",
        "default_level": 0,
        "levels": [
            {"key": "no_foreign_aid", "name": "No Foreign Aid", "description": "Resources stay at home.", "tags": ["isolationist", "nationalist"], "effects": {}},
            {"key": "strategic_aid", "name": "Strategic Aid", "description": "Aid given to advance national interests.", "tags": [], "effects": {}},
            {"key": "humanitarian_aid", "name": "Humanitarian Aid", "description": "Aid given based on need.", "tags": ["internationalist", "progressive"], "effects": {}},
        ],
    },
    "treaty_compliance": {
        "name": "Treaty Compliance",
        "default_level": 1,
        "levels": [
            {"key": "treaty_optional", "name": "Treaties Are Optional", "description": "Treaties are followed only when convenient.", "tags": [], "effects": {}},
            {"key": "treaty_respected", "name": "Treaties Respected", "description": "Treaties are generally honoured.", "tags": [], "effects": {}},
            {"key": "treaty_sacred", "name": "Treaties Are Sacred", "description": "Breaking a treaty is unthinkable.", "tags": ["conservative"], "effects": {}},
        ],
    },
    "espionage_stance": {
        "name": "Espionage Stance",
        "default_level": 1,
        "levels": [
            {"key": "no_espionage", "name": "No Espionage", "description": "The nation does not engage in espionage.", "tags": ["pacifist"], "effects": {}},
            {"key": "defensive_espionage", "name": "Defensive Espionage", "description": "Counter-intelligence only.", "tags": [], "effects": {}},
            {"key": "active_espionage", "name": "Active Espionage", "description": "Full intelligence operations abroad.", "tags": [], "effects": {}},
            {"key": "aggressive_espionage", "name": "Aggressive Espionage", "description": "Sabotage, assassination, and destabilisation.", "tags": ["authoritarian"], "effects": {}},
        ],
    },
    "war_policy": {
        "name": "War Policy",
        "default_level": 1,
        "levels": [
            {"key": "absolute_pacifism", "name": "Absolute Pacifism", "description": "War is never justified.", "tags": ["pacifist"], "effects": {}},
            {"key": "defensive_war", "name": "Defensive War Only", "description": "War only in self-defence.", "tags": ["pacifist"], "effects": {}},
            {"key": "just_war", "name": "Just War", "description": "War for legitimate causes.", "tags": [], "effects": {}},
            {"key": "preemptive_war", "name": "Preemptive War", "description": "Strike first to prevent threats.", "tags": ["militaristic"], "effects": {}},
            {"key": "total_war", "name": "Total War", "description": "War by any means necessary.", "tags": ["militaristic", "authoritarian"], "effects": {}},
        ],
    },
}

# Convenience: total number of policy categories
POLICY_CATEGORY_COUNT = len(POLICY_CATEGORIES)


# =============================================================================
# POLICY_EFFECTS — Context-dependent effects for all 67 categories
#
# Structure per level:
#   {
#       "base": {<effect_key>: <value>, ...},
#       "government_modifiers": {<gov_type>: {<effect_key>: <value>, ...}, ...},
#       "trait_modifiers": {<trait_key>: {<effect_key>: <value>, ...}, ...},
#   }
#
# Merge: start with base, add matching government_modifiers, add all matching
# trait_modifiers.  All numeric values are additive.  building_efficiency_bonus
# dicts merge by category key.
# =============================================================================

POLICY_EFFECTS = {
    # =========================================================================
    # MILITARY (7 categories)
    # =========================================================================
    "military_service": {
        0: {  # disarmed_nation
            "base": {
                "stability_bonus": 2.0,
                "growth_bonus": 0.0005,
                "manpower_bonus": -0.50,
                "army_training_speed_bonus": -0.30,
            },
            "government_modifiers": {
                "military_power": {"stability_penalty": -6.0},
            },
            "trait_modifiers": {
                "pacifist": {"stability_bonus": 2.0},
                "militarist": {"stability_penalty": -4.0},
            },
        },
        1: {"base": {}},  # volunteer_only (default)
        2: {  # limited_conscription
            "base": {
                "manpower_bonus": 0.10,
                "growth_penalty": -0.0003,
                "stability_penalty": -1.0,
            },
            "government_modifiers": {
                "elections": {"stability_penalty": -1.0},
                "military_power": {"stability_bonus": 1.0},
                "singular": {"stability_bonus": 0.5},
            },
            "trait_modifiers": {
                "libertarian": {"stability_penalty": -1.5},
                "authoritarian": {"stability_bonus": 0.5},
                "pacifist": {"stability_penalty": -1.0},
            },
        },
        3: {  # extensive_conscription
            "base": {
                "manpower_bonus": 0.25,
                "growth_penalty": -0.0008,
                "stability_penalty": -2.0,
                "wealth_production_bonus": -0.03,
            },
            "government_modifiers": {
                "elections": {"stability_penalty": -3.0},
                "collectivist": {"stability_penalty": -1.0},
                "military_power": {"stability_bonus": 2.0},
                "singular": {"stability_bonus": 1.0},
            },
            "trait_modifiers": {
                "libertarian": {"stability_penalty": -3.0},
                "militarist": {"stability_bonus": 1.0, "manpower_bonus": 0.05},
                "pacifist": {"stability_penalty": -2.0},
                "authoritarian": {"stability_bonus": 1.0},
            },
        },
        4: {  # universal_service
            "base": {
                "manpower_bonus": 0.40,
                "growth_penalty": -0.001,
                "stability_penalty": -3.0,
                "wealth_production_bonus": -0.05,
                "army_upkeep_reduction": 0.04,
            },
            "government_modifiers": {
                "elections": {"stability_penalty": -5.0},
                "subsistence": {"stability_penalty": -3.0},
                "military_power": {"stability_bonus": 3.0},
                "singular": {"stability_bonus": 2.0},
            },
            "trait_modifiers": {
                "libertarian": {"stability_penalty": -5.0},
                "militarist": {"stability_bonus": 2.0, "manpower_bonus": 0.10},
                "nationalist": {"stability_bonus": 1.0},
                "pacifist": {"stability_penalty": -4.0, "growth_penalty": -0.001},
            },
        },
        5: {  # service_by_requirement
            "base": {
                "manpower_bonus": 0.35,
                "growth_penalty": -0.0008,
                "stability_penalty": -2.0,
                "army_upkeep_reduction": 0.03,
                "navy_upkeep_reduction": 0.02,
            },
            "government_modifiers": {
                "elections": {"stability_penalty": -2.0},
                "military_power": {"stability_bonus": 2.0},
            },
            "trait_modifiers": {
                "militarist": {"manpower_bonus": 0.05},
                "authoritarian": {"stability_bonus": 1.0},
            },
        },
        6: {  # scraping_the_barrel
            "base": {
                "manpower_bonus": 0.60,
                "growth_penalty": -0.002,
                "stability_penalty": -5.0,
                "wealth_production_bonus": -0.10,
                "food_production_bonus": -0.05,
                "army_upkeep_reduction": 0.06,
                "navy_upkeep_reduction": 0.03,
                "air_upkeep_reduction": 0.02,
            },
            "government_modifiers": {
                "military_power": {"stability_bonus": 2.0},
            },
            "trait_modifiers": {
                "militarist": {"stability_bonus": 1.0},
                "nationalist": {"stability_bonus": 1.0},
            },
        },
    },

    "military_spending": {
        0: {  # minimal_military
            "base": {
                "stability_bonus": 1.0,
                "upkeep_reduction": 0.05,
                "military_upkeep_reduction": -0.15,
                "army_upkeep_reduction": 0.06,
                "navy_upkeep_reduction": 0.06,
                "air_upkeep_reduction": 0.06,
            },
            "trait_modifiers": {
                "pacifist": {"stability_bonus": 1.0},
                "militarist": {"stability_penalty": -3.0},
            },
        },
        1: {"base": {}},  # low_military (default)
        2: {  # moderate_military
            "base": {
                "upkeep_reduction": -0.02,
            },
            "trait_modifiers": {
                "militarist": {"army_combat_bonus": 0.03},
            },
        },
        3: {  # high_military
            "base": {
                "upkeep_reduction": -0.05,
                "army_combat_bonus": 0.05,
                "navy_combat_bonus": 0.05,
                "air_combat_bonus": 0.05,
                "stability_penalty": -1.0,
                "army_upkeep_reduction": -0.03,
            },
            "government_modifiers": {
                "military_power": {"stability_bonus": 1.0, "army_combat_bonus": 0.03},
                "elections": {"stability_penalty": -1.0},
                "collectivist": {"stability_penalty": -1.0},
            },
            "trait_modifiers": {
                "militarist": {"army_combat_bonus": 0.05, "stability_bonus": 1.0},
                "pacifist": {"stability_penalty": -2.0},
            },
        },
        4: {  # war_economy
            "base": {
                "upkeep_reduction": -0.10,
                "army_combat_bonus": 0.08,
                "navy_combat_bonus": 0.08,
                "air_combat_bonus": 0.08,
                "army_training_speed_bonus": 0.15,
                "navy_training_speed_bonus": 0.15,
                "air_training_speed_bonus": 0.15,
                "stability_penalty": -3.0,
                "growth_penalty": -0.001,
                "wealth_production_bonus": -0.08,
                "building_efficiency_bonus": {"heavy_manufacturing": 0.05},
                "navy_upkeep_reduction": -0.05,
                "air_upkeep_reduction": -0.05,
            },
            "government_modifiers": {
                "military_power": {"stability_bonus": 3.0, "building_efficiency_bonus": {"heavy_manufacturing": 0.05}},
                "singular": {"stability_bonus": 1.0},
                "elections": {"stability_penalty": -4.0},
                "liberal": {"stability_penalty": -2.0, "wealth_production_bonus": -0.05},
            },
            "trait_modifiers": {
                "militarist": {
                    "stability_bonus": 2.0,
                    "army_combat_bonus": 0.05,
                    "building_efficiency_bonus": {"heavy_manufacturing": 0.03},
                },
                "pacifist": {"stability_penalty": -5.0, "growth_penalty": -0.001},
                "industrialist": {"building_efficiency_bonus": {"heavy_manufacturing": 0.05}},
            },
        },
    },

    "military_doctrine": {
        0: {  # static_defence
            "base": {
                "army_combat_bonus": 0.03,
                "march_speed_bonus": -0.05,
            },
            "trait_modifiers": {
                "traditionalist": {"army_combat_bonus": 0.02},
            },
        },
        1: {  # mobile_warfare
            "base": {
                "march_speed_bonus": 0.05,
                "army_combat_bonus": 0.02,
            },
            "trait_modifiers": {
                "modern": {"march_speed_bonus": 0.02},
            },
        },
        2: {  # guerrilla_warfare
            "base": {
                "army_combat_bonus": 0.02,
                "army_upkeep_reduction": 0.05,
            },
            "trait_modifiers": {
                "libertarian": {"army_combat_bonus": 0.02},
                "authoritarian": {"army_combat_bonus": -0.02},
            },
        },
        3: {  # combined_arms
            "base": {
                "army_combat_bonus": 0.05,
                "navy_combat_bonus": 0.03,
                "air_combat_bonus": 0.03,
                "sea_transit_speed": 0.03,
                "air_transit_speed": 0.03,
            },
            "trait_modifiers": {
                "modern": {"army_combat_bonus": 0.03},
                "traditionalist": {"army_combat_bonus": -0.02},
            },
        },
    },

    "veterans_policy": {
        0: {  # no_veterans_support
            "base": {
                "stability_penalty": -0.5,
            },
            "trait_modifiers": {
                "militarist": {"stability_penalty": -1.5},
            },
        },
        1: {"base": {}},  # basic_veterans_care (default)
        2: {  # veterans_benefits
            "base": {
                "stability_bonus": 1.0,
                "upkeep_reduction": -0.02,
                "growth_bonus": 0.0003,
                "army_upkeep_reduction": -0.02,
            },
            "trait_modifiers": {
                "militarist": {"stability_bonus": 0.5},
                "nationalist": {"stability_bonus": 0.5},
            },
        },
        3: {  # hero_worship
            "base": {
                "stability_bonus": 2.0,
                "manpower_bonus": 0.05,
                "upkeep_reduction": -0.03,
                "army_combat_bonus": 0.02,
                "stability_recovery_bonus": 0.03,
            },
            "government_modifiers": {
                "military_power": {"stability_bonus": 1.0, "manpower_bonus": 0.03},
                "elections": {"stability_penalty": -1.0},
            },
            "trait_modifiers": {
                "militarist": {"stability_bonus": 1.0, "manpower_bonus": 0.05},
                "pacifist": {"stability_penalty": -2.0},
                "nationalist": {"stability_bonus": 1.0},
            },
        },
    },

    "border_policy": {
        0: {  # open_borders
            "base": {
                "growth_bonus": 0.001,
                "stability_penalty": -1.0,
                "land_trade_capacity": 100,
                "naval_trade_capacity": 50,
            },
            "government_modifiers": {
                "subsistence": {"stability_penalty": -2.0},
            },
            "trait_modifiers": {
                "internationalist": {"stability_bonus": 1.0, "growth_bonus": 0.0005},
                "nationalist": {"stability_penalty": -3.0},
            },
        },
        1: {"base": {}},  # monitored_borders (default)
        2: {  # controlled_borders
            "base": {
                "stability_bonus": 0.5,
                "growth_penalty": -0.0003,
            },
            "trait_modifiers": {
                "nationalist": {"stability_bonus": 0.5},
            },
        },
        3: {  # restricted_borders
            "base": {
                "stability_bonus": 1.0,
                "growth_penalty": -0.0005,
                "land_trade_capacity": -75,
                "march_speed_bonus": -0.03,
            },
            "trait_modifiers": {
                "nationalist": {"stability_bonus": 1.0},
                "internationalist": {"stability_penalty": -1.0},
            },
        },
        4: {  # closed_borders
            "base": {
                "stability_bonus": 1.5,
                "growth_penalty": -0.001,
                "land_trade_capacity": -150,
                "naval_trade_capacity": -100,
                "air_trade_capacity": -50,
            },
            "government_modifiers": {
                "liberal": {"stability_penalty": -2.0, "wealth_production_bonus": -0.05},
            },
            "trait_modifiers": {
                "nationalist": {"stability_bonus": 1.5},
                "internationalist": {"stability_penalty": -3.0},
            },
        },
    },

    "weapons_policy": {
        0: {  # universal_arms
            "base": {
                "manpower_bonus": 0.08,
                "stability_penalty": -1.0,
                "army_training_speed_bonus": 0.05,
                "army_upkeep_reduction": 0.03,
            },
            "government_modifiers": {
                "singular": {"stability_penalty": -2.0},
                "military_power": {"stability_penalty": -2.0},
            },
            "trait_modifiers": {
                "libertarian": {"stability_bonus": 1.0},
                "militarist": {"manpower_bonus": 0.03},
                "authoritarian": {"stability_penalty": -1.5},
            },
        },
        1: {"base": {}},  # licensed_arms (default)
        2: {  # restricted_arms
            "base": {
                "stability_bonus": 0.5,
                "manpower_bonus": -0.05,
            },
            "trait_modifiers": {
                "authoritarian": {"stability_bonus": 0.5},
                "libertarian": {"stability_penalty": -1.0},
            },
        },
        3: {  # state_monopoly_arms
            "base": {
                "stability_bonus": 1.0,
                "manpower_bonus": -0.10,
                "army_training_speed_bonus": -0.05,
                "army_upkeep_reduction": -0.03,
            },
            "government_modifiers": {
                "elections": {"stability_penalty": -1.5},
            },
            "trait_modifiers": {
                "authoritarian": {"stability_bonus": 1.0},
                "libertarian": {"stability_penalty": -3.0},
                "pacifist": {"stability_bonus": 1.0},
            },
        },
    },

    "intelligence_policy": {
        0: {  # no_intelligence
            "base": {
                "upkeep_reduction": 0.02,
            },
            "trait_modifiers": {
                "devious": {"stability_penalty": -1.0},
            },
        },
        1: {"base": {}},  # basic_intelligence (default)
        2: {  # active_intelligence
            "base": {
                "upkeep_reduction": -0.02,
                "stability_bonus": 0.5,
                "building_efficiency_bonus": {"government_security": 0.03},
            },
            "trait_modifiers": {
                "devious": {"stability_bonus": 0.5},
            },
        },
        3: {  # pervasive_surveillance
            "base": {
                "upkeep_reduction": -0.04,
                "stability_bonus": 2.0,
                "growth_penalty": -0.0003,
                "research_penalty": -0.03,
                "building_efficiency_bonus": {"government_security": 0.05},
            },
            "government_modifiers": {
                "elections": {"stability_penalty": -4.0},
                "collectivist": {"stability_penalty": -2.0},
                "singular": {"stability_bonus": 1.0},
                "military_power": {"stability_bonus": 1.0},
            },
            "trait_modifiers": {
                "libertarian": {"stability_penalty": -5.0},
                "authoritarian": {"stability_bonus": 2.0},
                "devious": {"stability_bonus": 1.0},
                "honorable": {"stability_penalty": -2.0},
            },
        },
    },

    # =========================================================================
    # ECONOMY (12 categories)
    # =========================================================================
    "economic_system": {
        0: {  # free_market
            "base": {
                "wealth_production_bonus": 0.08,
                "building_efficiency_bonus": {"financial": 0.06, "light_manufacturing": 0.04},
                "integration_bonus": 0.03,
                "stability_penalty": -1.0,
                "urban_output_bonus": 0.04,
                "land_trade_capacity": 100,
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": 0.05, "stability_bonus": 1.0},
                "collectivist": {"stability_penalty": -4.0},
                "singular": {"stability_penalty": -1.0},
            },
            "trait_modifiers": {
                "individualist": {"wealth_production_bonus": 0.04, "stability_bonus": 1.0},
                "collectivist": {"stability_penalty": -2.0},
                "libertarian": {"stability_bonus": 1.0, "wealth_production_bonus": 0.03},
            },
        },
        1: {  # mixed_economy
            "base": {
                "wealth_production_bonus": 0.03,
                "stability_bonus": 0.5,
            },
        },
        2: {"base": {}},  # managed_economy (default)
        3: {  # command_economy
            "base": {
                "building_efficiency_bonus": {"heavy_manufacturing": 0.06, "extraction": 0.04, "construction": 0.04},
                "wealth_production_bonus": -0.05,
                "integration_bonus": 0.05,
                "stability_penalty": -1.0,
                "rural_output_bonus": 0.03,
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 2.0, "building_efficiency_bonus": {"farming": 0.04}},
                "singular": {"stability_bonus": 1.0, "integration_bonus": 0.03},
                "elections": {"stability_penalty": -4.0},
                "liberal": {"stability_penalty": -5.0},
            },
            "trait_modifiers": {
                "collectivist": {"stability_bonus": 2.0, "integration_bonus": 0.03},
                "individualist": {"stability_penalty": -3.0, "wealth_production_bonus": -0.05},
                "authoritarian": {"stability_bonus": 1.0},
                "libertarian": {"stability_penalty": -4.0},
            },
        },
        4: {  # barter_economy
            "base": {
                "wealth_production_bonus": -0.10,
                "land_trade_capacity": -150,
                "naval_trade_capacity": -100,
            },
            "trait_modifiers": {
                "individualist": {"stability_bonus": 0.5},
            },
        },
    },

    "taxation": {
        0: {  # no_taxes
            "base": {
                "wealth_production_bonus": 0.06,
                "upkeep_reduction": -0.15,
                "stability_bonus": 1.0,
                "building_efficiency_bonus": {"government_management": -0.06, "government_welfare": -0.06},
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": 0.03},
            },
            "trait_modifiers": {
                "libertarian": {"stability_bonus": 1.0},
                "collectivist": {"stability_penalty": -2.0},
            },
        },
        1: {  # low_taxes
            "base": {
                "wealth_production_bonus": 0.03,
                "upkeep_reduction": -0.05,
                "growth_bonus": 0.0002,
            },
            "trait_modifiers": {
                "individualist": {"wealth_production_bonus": 0.02},
            },
        },
        2: {"base": {}},  # moderate_taxes (default)
        3: {  # high_taxes
            "base": {
                "wealth_production_bonus": -0.04,
                "upkeep_reduction": 0.06,
                "integration_bonus": 0.03,
                "stability_penalty": -1.0,
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 1.0},
                "singular": {"integration_bonus": 0.02},
            },
            "trait_modifiers": {
                "collectivist": {"stability_bonus": 0.5},
                "libertarian": {"stability_penalty": -2.0},
            },
        },
        4: {  # confiscatory_taxes
            "base": {
                "wealth_production_bonus": -0.08,
                "upkeep_reduction": 0.10,
                "integration_bonus": 0.05,
                "stability_penalty": -2.5,
                "growth_penalty": -0.0003,
            },
            "government_modifiers": {
                "singular": {"stability_bonus": 1.0},
                "liberal": {"stability_penalty": -3.0},
            },
            "trait_modifiers": {
                "authoritarian": {"stability_bonus": 1.0},
                "libertarian": {"stability_penalty": -3.0},
                "individualist": {"stability_penalty": -2.0},
            },
        },
    },

    "trade_policy": {
        0: {  # free_trade
            "base": {
                "wealth_production_bonus": 0.05,
                "land_trade_capacity": 200,
                "naval_trade_capacity": 150,
                "air_trade_capacity": 100,
                "building_efficiency_bonus": {"financial": 0.04, "transport": 0.03},
                "stability_penalty": -0.5,
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": 0.03, "naval_trade_capacity": 50},
                "collectivist": {"stability_penalty": -1.0},
            },
            "trait_modifiers": {
                "internationalist": {"wealth_production_bonus": 0.02, "land_trade_capacity": 50},
                "nationalist": {"stability_penalty": -1.0},
            },
        },
        1: {"base": {}},  # moderate_tariffs (default)
        2: {  # protectionist
            "base": {
                "building_efficiency_bonus": {"light_manufacturing": 0.03, "heavy_manufacturing": 0.03},
                "wealth_production_bonus": -0.03,
                "land_trade_capacity": -100,
                "naval_trade_capacity": -75,
                "stability_bonus": 0.5,
            },
            "government_modifiers": {
                "singular": {"building_efficiency_bonus": {"heavy_manufacturing": 0.02}},
            },
            "trait_modifiers": {
                "nationalist": {"stability_bonus": 0.5},
                "internationalist": {"stability_penalty": -1.0},
            },
        },
        3: {  # autarky
            "base": {
                "building_efficiency_bonus": {"heavy_manufacturing": 0.04, "farming": 0.03, "extraction": 0.03},
                "wealth_production_bonus": -0.06,
                "land_trade_capacity": -200,
                "naval_trade_capacity": -150,
                "air_trade_capacity": -100,
                "integration_bonus": 0.04,
                "stability_bonus": 1.0,
            },
            "government_modifiers": {
                "singular": {"stability_bonus": 1.0},
                "liberal": {"stability_penalty": -3.0, "wealth_production_bonus": -0.04},
            },
            "trait_modifiers": {
                "nationalist": {"stability_bonus": 1.0, "integration_bonus": 0.02},
                "internationalist": {"stability_penalty": -2.0},
            },
        },
    },

    "currency_policy": {
        0: {  # commodity_money
            "base": {
                "wealth_production_bonus": -0.04,
                "naval_trade_capacity": -50,
                "stability_bonus": 1.0,
            },
            "government_modifiers": {
                "subsistence": {"stability_bonus": 0.5},
            },
            "trait_modifiers": {
                "traditionalist": {"stability_bonus": 0.5},
            },
        },
        1: {"base": {}},  # backed_currency (default)
        2: {  # fiat_currency
            "base": {
                "wealth_production_bonus": 0.04,
                "land_trade_capacity": 100,
                "naval_trade_capacity": 50,
                "stability_penalty": -0.5,
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": 0.02},
                "elections": {"stability_bonus": 0.5},
            },
            "trait_modifiers": {
                "modern": {"wealth_production_bonus": 0.02},
                "traditionalist": {"stability_penalty": -1.0},
            },
        },
    },

    "property_rights": {
        0: {  # communal_property
            "base": {
                "integration_bonus": 0.04,
                "stability_bonus": 1.0,
                "wealth_production_bonus": -0.05,
                "building_efficiency_bonus": {"farming": 0.04},
                "rural_output_bonus": 0.03,
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 1.0, "rural_output_bonus": 0.02},
                "liberal": {"stability_penalty": -3.0},
            },
            "trait_modifiers": {
                "collectivist": {"stability_bonus": 0.5, "integration_bonus": 0.02},
                "individualist": {"stability_penalty": -2.0},
            },
        },
        1: {"base": {}},  # mixed_property (default)
        2: {  # strong_property
            "base": {
                "wealth_production_bonus": 0.05,
                "building_efficiency_bonus": {"financial": 0.04},
                "stability_penalty": -0.5,
                "urban_output_bonus": 0.03,
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": 0.03, "stability_bonus": 0.5},
                "collectivist": {"stability_penalty": -2.0},
            },
            "trait_modifiers": {
                "individualist": {"wealth_production_bonus": 0.02},
                "libertarian": {"stability_bonus": 0.5},
            },
        },
    },

    "labour_policy": {
        0: {  # forced_labour
            "base": {
                "building_efficiency_bonus": {"construction": 0.05, "extraction": 0.04, "heavy_manufacturing": 0.03},
                "stability_penalty": -2.0,
                "growth_penalty": -0.0005,
                "manpower_bonus": 0.08,
            },
            "government_modifiers": {
                "military_power": {"stability_bonus": 1.0, "manpower_bonus": 0.04},
                "elections": {"stability_penalty": -4.0},
            },
            "trait_modifiers": {
                "authoritarian": {"stability_bonus": 1.0},
                "egalitarian": {"stability_penalty": -3.0},
                "libertarian": {"stability_penalty": -3.0},
            },
        },
        1: {"base": {}},  # regulated_labour (default)
        2: {  # worker_councils
            "base": {
                "stability_bonus": 1.0,
                "building_efficiency_bonus": {"light_manufacturing": 0.03, "farming": 0.03},
                "wealth_production_bonus": -0.02,
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 1.0, "building_efficiency_bonus": {"light_manufacturing": 0.02}},
                "liberal": {"stability_penalty": -1.5},
            },
            "trait_modifiers": {
                "collectivist": {"stability_bonus": 0.5, "integration_bonus": 0.02},
                "individualist": {"stability_penalty": -1.0},
            },
        },
        3: {  # free_labour
            "base": {
                "wealth_production_bonus": 0.04,
                "growth_bonus": 0.0003,
                "stability_penalty": -0.5,
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": 0.03},
            },
            "trait_modifiers": {
                "libertarian": {"stability_bonus": 0.5},
                "individualist": {"wealth_production_bonus": 0.02},
            },
        },
    },

    "banking_policy": {
        0: {  # no_banking
            "base": {
                "wealth_production_bonus": -0.05,
                "building_efficiency_bonus": {"financial": -0.08},
                "stability_bonus": 0.5,
            },
            "government_modifiers": {
                "subsistence": {"stability_bonus": 1.0},
            },
            "trait_modifiers": {
                "traditionalist": {"stability_bonus": 0.5},
            },
        },
        1: {"base": {}},  # state_banking (default)
        2: {  # regulated_banking
            "base": {
                "wealth_production_bonus": 0.03,
                "building_efficiency_bonus": {"financial": 0.04},
                "land_trade_capacity": 75,
            },
            "government_modifiers": {
                "elections": {"stability_bonus": 0.5},
                "liberal": {"wealth_production_bonus": 0.02},
            },
        },
        3: {  # free_banking
            "base": {
                "wealth_production_bonus": 0.05,
                "building_efficiency_bonus": {"financial": 0.06},
                "land_trade_capacity": 150,
                "stability_penalty": -0.5,
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": 0.03, "stability_bonus": 0.5},
                "collectivist": {"stability_penalty": -1.5},
            },
            "trait_modifiers": {
                "individualist": {"wealth_production_bonus": 0.02},
                "collectivist": {"stability_penalty": -1.0},
            },
        },
    },

    "resource_extraction": {
        0: {  # state_extraction
            "base": {
                "building_efficiency_bonus": {"extraction": 0.05},
                "integration_bonus": 0.03,
                "wealth_production_bonus": -0.03,
            },
            "government_modifiers": {
                "singular": {"building_efficiency_bonus": {"extraction": 0.03}},
                "collectivist": {"integration_bonus": 0.02},
            },
            "trait_modifiers": {
                "collectivist": {"integration_bonus": 0.02},
            },
        },
        1: {"base": {}},  # licensed_extraction (default)
        2: {  # unregulated_extraction
            "base": {
                "building_efficiency_bonus": {"extraction": 0.06},
                "wealth_production_bonus": 0.03,
                "stability_penalty": -0.5,
                "growth_penalty": -0.0002,
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": 0.02},
            },
            "trait_modifiers": {
                "industrialist": {"building_efficiency_bonus": {"extraction": 0.03}},
                "ecologist": {"stability_penalty": -2.0},
            },
        },
        3: {  # conservation_priority
            "base": {
                "building_efficiency_bonus": {"extraction": -0.06, "green_energy": 0.04},
                "stability_bonus": 0.5,
                "farming_bonus": 0.03,
                "growth_bonus": 0.0002,
            },
            "trait_modifiers": {
                "ecologist": {"stability_bonus": 1.0, "farming_bonus": 0.02},
                "industrialist": {"stability_penalty": -1.5},
            },
        },
    },

    "food_distribution": {
        0: {  # free_market_food
            "base": {
                "wealth_production_bonus": 0.02,
                "food_production_bonus": -0.03,
                "land_trade_capacity": 50,
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": 0.02},
            },
            "trait_modifiers": {
                "individualist": {"wealth_production_bonus": 0.01},
            },
        },
        1: {"base": {}},  # subsidised_food (default)
        2: {  # rationing
            "base": {
                "food_production_bonus": 0.04,
                "stability_penalty": -1.0,
                "growth_bonus": 0.0003,
                "upkeep_reduction": 0.03,
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 1.0},
                "military_power": {"stability_bonus": 0.5},
            },
            "trait_modifiers": {
                "authoritarian": {"stability_bonus": 0.5},
                "libertarian": {"stability_penalty": -2.0},
            },
        },
        3: {  # communal_kitchens
            "base": {
                "food_production_bonus": 0.03,
                "stability_bonus": 0.5,
                "growth_bonus": 0.0004,
                "farming_bonus": 0.02,
                "stability_recovery_bonus": 0.05,
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 1.0, "growth_bonus": 0.0002},
                "liberal": {"stability_penalty": -1.0},
            },
            "trait_modifiers": {
                "collectivist": {"stability_bonus": 0.5, "farming_bonus": 0.01},
                "individualist": {"stability_penalty": -1.0},
            },
        },
    },

    "infrastructure_policy": {
        0: {  # neglected_infrastructure
            "base": {
                "march_speed_bonus": -0.05,
                "building_efficiency_bonus": {"transport": -0.05},
                "upkeep_reduction": 0.03,
                "river_transit_speed": -0.03,
            },
        },
        1: {"base": {}},  # maintained_infrastructure (default)
        2: {  # expanding_infrastructure
            "base": {
                "building_efficiency_bonus": {"transport": 0.04, "construction": 0.04},
                "march_speed_bonus": 0.03,
                "upkeep_reduction": -0.03,
                "sea_transit_speed": 0.02,
                "river_transit_speed": 0.02,
            },
            "trait_modifiers": {
                "industrialist": {"building_efficiency_bonus": {"construction": 0.03}},
            },
        },
        3: {  # megaproject_infrastructure
            "base": {
                "building_efficiency_bonus": {"transport": 0.08, "construction": 0.08},
                "march_speed_bonus": 0.06,
                "upkeep_reduction": -0.06,
                "stability_penalty": -1.0,
                "sea_transit_speed": 0.04,
                "river_transit_speed": 0.04,
                "air_transit_speed": 0.03,
            },
            "government_modifiers": {
                "singular": {"stability_bonus": 1.0},
                "military_power": {"stability_bonus": 1.0, "building_efficiency_bonus": {"construction": 0.03}},
                "elections": {"stability_penalty": -1.0},
            },
            "trait_modifiers": {
                "industrialist": {"building_efficiency_bonus": {"construction": 0.05}},
                "authoritarian": {"stability_bonus": 0.5},
                "ecologist": {"stability_penalty": -2.0},
            },
        },
    },

    "energy_policy": {
        0: {  # biomass_energy
            "base": {
                "building_efficiency_bonus": {"refining": -0.05, "green_energy": -0.04},
                "food_production_bonus": -0.02,
                "rural_output_bonus": 0.02,
            },
            "trait_modifiers": {
                "traditionalist": {"stability_bonus": 0.5},
                "ecologist": {"stability_bonus": 0.5},
            },
        },
        1: {  # fossil_fuel_energy
            "base": {
                "building_efficiency_bonus": {"refining": 0.05, "heavy_manufacturing": 0.03},
            },
            "trait_modifiers": {
                "industrialist": {"building_efficiency_bonus": {"refining": 0.03}},
                "ecologist": {"stability_penalty": -1.5},
            },
        },
        2: {"base": {}},  # mixed_energy (default)
        3: {  # renewable_energy
            "base": {
                "building_efficiency_bonus": {"green_energy": 0.08},
                "stability_bonus": 0.5,
                "upkeep_reduction": -0.02,
            },
            "trait_modifiers": {
                "ecologist": {"stability_bonus": 1.0, "building_efficiency_bonus": {"green_energy": 0.05}},
                "industrialist": {"stability_penalty": -1.0},
                "modern": {"building_efficiency_bonus": {"green_energy": 0.03}},
            },
        },
    },

    # =========================================================================
    # INDUSTRY & PRODUCTION (8 categories)
    # =========================================================================
    "industrial_policy": {
        0: {  # agrarian_focus
            "base": {
                "food_production_bonus": 0.05,
                "building_efficiency_bonus": {"farming": 0.06, "heavy_manufacturing": -0.04, "light_manufacturing": -0.04},
                "farming_bonus": 0.04,
                "rural_output_bonus": 0.04,
                "urban_output_bonus": -0.03,
            },
            "government_modifiers": {
                "subsistence": {"food_production_bonus": 0.03, "stability_bonus": 1.0},
            },
            "trait_modifiers": {
                "traditionalist": {"food_production_bonus": 0.03},
                "ecologist": {"building_efficiency_bonus": {"farming": 0.04}},
                "industrialist": {"stability_penalty": -1.5},
            },
        },
        1: {"base": {}},  # balanced_development (default)
        2: {  # industrialisation_drive
            "base": {
                "building_efficiency_bonus": {"heavy_manufacturing": 0.06, "light_manufacturing": 0.04, "construction": 0.04},
                "food_production_bonus": -0.03,
                "stability_penalty": -1.0,
                "urban_threshold_reduction": 5000,
                "urban_output_bonus": 0.04,
            },
            "government_modifiers": {
                "singular": {"building_efficiency_bonus": {"heavy_manufacturing": 0.03}},
                "military_power": {"building_efficiency_bonus": {"construction": 0.03}},
                "liberal": {"building_efficiency_bonus": {"light_manufacturing": 0.03}},
            },
            "trait_modifiers": {
                "industrialist": {"building_efficiency_bonus": {"heavy_manufacturing": 0.05}, "stability_bonus": 1.0},
                "ecologist": {"stability_penalty": -3.0},
                "modern": {"building_efficiency_bonus": {"light_manufacturing": 0.02}},
            },
        },
        3: {  # high_tech_focus
            "base": {
                "research_bonus": 0.08,
                "building_efficiency_bonus": {"communications": 0.05, "pharmaceutical": 0.04},
                "food_production_bonus": -0.03,
                "upkeep_reduction": -0.03,
                "urban_output_bonus": 0.06,
            },
            "government_modifiers": {
                "liberal": {"research_bonus": 0.03},
                "subsistence": {"stability_penalty": -2.0},
            },
            "trait_modifiers": {
                "positivist": {"research_bonus": 0.05},
                "modern": {"research_bonus": 0.03, "building_efficiency_bonus": {"communications": 0.03}},
                "traditionalist": {"stability_penalty": -2.0, "research_penalty": -0.03},
            },
        },
    },

    "construction_regulation": {
        0: {  # no_regulations
            "base": {
                "construction_cost_reduction": 0.08,
                "construction_time_reduction": 0.10,
                "stability_penalty": -0.5,
                "building_efficiency_bonus": {"construction": 0.04},
            },
            "trait_modifiers": {
                "libertarian": {"stability_bonus": 0.5},
            },
        },
        1: {"base": {}},  # basic_codes (default)
        2: {  # comprehensive_planning
            "base": {
                "construction_cost_reduction": -0.05,
                "construction_time_reduction": -0.05,
                "building_efficiency_bonus": {"construction": 0.04, "government_regulatory": 0.04},
                "stability_bonus": 0.5,
            },
            "trait_modifiers": {
                "authoritarian": {"building_efficiency_bonus": {"construction": 0.02}},
            },
        },
    },

    "environmental_policy": {
        0: {  # no_environmental
            "base": {
                "building_efficiency_bonus": {"extraction": 0.05, "refining": 0.04, "green_energy": -0.06},
                "growth_penalty": -0.0003,
                "stability_penalty": -0.5,
            },
            "trait_modifiers": {
                "ecologist": {"stability_penalty": -3.0},
                "industrialist": {"building_efficiency_bonus": {"extraction": 0.03}},
            },
        },
        1: {"base": {}},  # basic_environmental (default)
        2: {  # strict_environmental
            "base": {
                "building_efficiency_bonus": {"extraction": -0.04, "green_energy": 0.05},
                "growth_bonus": 0.0002,
                "stability_bonus": 0.5,
                "farming_bonus": 0.02,
            },
            "trait_modifiers": {
                "ecologist": {"stability_bonus": 1.0, "building_efficiency_bonus": {"green_energy": 0.04}},
                "industrialist": {"stability_penalty": -1.5, "building_efficiency_bonus": {"extraction": -0.02}},
            },
        },
        3: {  # deep_ecology
            "base": {
                "building_efficiency_bonus": {"extraction": -0.10, "refining": -0.08, "green_energy": 0.10},
                "growth_bonus": 0.0003,
                "stability_penalty": -1.0,
                "farming_bonus": 0.04,
                "rural_output_bonus": 0.05,
                "urban_growth_penalty": -0.0005,
            },
            "government_modifiers": {
                "liberal": {"stability_penalty": -3.0},
                "subsistence": {"stability_bonus": 1.0},
            },
            "trait_modifiers": {
                "ecologist": {"stability_bonus": 3.0, "building_efficiency_bonus": {"green_energy": 0.06}},
                "industrialist": {"stability_penalty": -5.0},
                "modern": {"stability_penalty": -1.0},
            },
        },
    },

    "agriculture_policy": {
        0: {  # subsistence_farming
            "base": {
                "food_production_bonus": 0.04,
                "building_efficiency_bonus": {"farming": -0.05},
                "stability_bonus": 0.5,
                "farming_bonus": 0.03,
                "rural_output_bonus": 0.03,
            },
            "government_modifiers": {
                "subsistence": {"food_production_bonus": 0.03, "stability_bonus": 1.0},
            },
            "trait_modifiers": {
                "traditionalist": {"stability_bonus": 0.5},
            },
        },
        1: {"base": {}},  # mixed_agriculture (default)
        2: {  # collective_farms
            "base": {
                "building_efficiency_bonus": {"farming": 0.05},
                "food_production_bonus": 0.03,
                "stability_penalty": -1.0,
                "farming_bonus": 0.04,
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 2.0, "food_production_bonus": 0.03},
                "elections": {"stability_penalty": -1.0},
                "liberal": {"stability_penalty": -2.0},
            },
            "trait_modifiers": {
                "collectivist": {"stability_bonus": 1.5, "building_efficiency_bonus": {"farming": 0.03}},
                "individualist": {"stability_penalty": -2.0},
            },
        },
        3: {  # industrial_agriculture
            "base": {
                "building_efficiency_bonus": {"farming": 0.08, "chemical": 0.03},
                "food_production_bonus": 0.06,
                "upkeep_reduction": -0.02,
                "farming_bonus": 0.06,
            },
            "government_modifiers": {
                "liberal": {"building_efficiency_bonus": {"farming": 0.03}},
            },
            "trait_modifiers": {
                "industrialist": {"building_efficiency_bonus": {"farming": 0.04}},
                "ecologist": {"stability_penalty": -1.5},
                "modern": {"building_efficiency_bonus": {"farming": 0.02}},
            },
        },
    },

    "manufacturing_policy": {
        0: {  # cottage_industry
            "base": {
                "building_efficiency_bonus": {"light_manufacturing": -0.05, "heavy_manufacturing": -0.08},
                "wealth_production_bonus": 0.02,
                "rural_output_bonus": 0.02,
            },
            "trait_modifiers": {
                "traditionalist": {"stability_bonus": 0.5},
            },
        },
        1: {"base": {}},  # workshop_economy (default)
        2: {  # factory_system
            "base": {
                "building_efficiency_bonus": {"light_manufacturing": 0.05, "heavy_manufacturing": 0.05},
                "growth_penalty": -0.0002,
                "urban_threshold_reduction": 3000,
            },
            "trait_modifiers": {
                "industrialist": {"building_efficiency_bonus": {"heavy_manufacturing": 0.04}},
                "ecologist": {"stability_penalty": -1.0},
            },
        },
        3: {  # automated_production
            "base": {
                "building_efficiency_bonus": {"light_manufacturing": 0.08, "heavy_manufacturing": 0.08},
                "research_bonus": 0.03,
                "manpower_bonus": -0.05,
                "upkeep_reduction": -0.03,
                "urban_threshold_reduction": 5000,
            },
            "trait_modifiers": {
                "modern": {"building_efficiency_bonus": {"light_manufacturing": 0.04}},
                "traditionalist": {"stability_penalty": -1.5},
                "industrialist": {"building_efficiency_bonus": {"heavy_manufacturing": 0.04}},
            },
        },
    },

    "research_policy": {
        0: {  # no_research_policy
            "base": {
                "research_penalty": -0.05,
                "literacy_bonus": -0.03,
            },
        },
        1: {"base": {}},  # practical_research (default)
        2: {  # academic_research
            "base": {
                "research_bonus": 0.08,
                "upkeep_reduction": -0.03,
                "literacy_bonus": 0.04,
                "building_efficiency_bonus": {"government_education": 0.03},
            },
            "government_modifiers": {
                "religious": {"research_bonus": -0.03},
            },
            "trait_modifiers": {
                "positivist": {"research_bonus": 0.05},
                "modern": {"research_bonus": 0.03},
                "traditionalist": {"stability_penalty": -0.5},
            },
        },
        3: {  # state_research
            "base": {
                "research_bonus": 0.06,
                "building_efficiency_bonus": {"pharmaceutical": 0.03, "chemical": 0.03, "government_education": 0.04},
            },
            "government_modifiers": {
                "singular": {"research_bonus": 0.03},
                "military_power": {"research_bonus": 0.02, "building_efficiency_bonus": {"chemical": 0.03}},
            },
            "trait_modifiers": {
                "authoritarian": {"research_bonus": 0.03},
                "libertarian": {"stability_penalty": -1.0},
            },
        },
    },

    "salvage_policy": {
        0: {  # free_salvage
            "base": {
                "building_efficiency_bonus": {"extraction": 0.05},
                "stability_penalty": -0.5,
            },
        },
        1: {"base": {}},  # regulated_salvage (default)
        2: {  # state_salvage
            "base": {
                "research_bonus": 0.03,
                "integration_bonus": 0.02,
                "building_efficiency_bonus": {"extraction": 0.03},
            },
            "trait_modifiers": {
                "authoritarian": {"research_bonus": 0.02},
            },
        },
    },

    "technology_adoption": {
        0: {  # tech_rejection
            "base": {
                "research_penalty": -0.08,
                "stability_bonus": 1.0,
                "building_efficiency_bonus": {"communications": -0.08, "pharmaceutical": -0.03},
                "literacy_bonus": -0.03,
            },
            "trait_modifiers": {
                "traditionalist": {"stability_bonus": 1.0},
                "modern": {"stability_penalty": -3.0},
            },
        },
        1: {"base": {}},  # cautious_adoption (default)
        2: {  # enthusiastic_adoption
            "base": {
                "research_bonus": 0.05,
                "building_efficiency_bonus": {"communications": 0.04, "pharmaceutical": 0.03},
                "stability_penalty": -0.5,
                "literacy_bonus": 0.03,
                "urban_threshold_reduction": 3000,
            },
            "trait_modifiers": {
                "modern": {"research_bonus": 0.03, "stability_bonus": 0.5},
                "traditionalist": {"stability_penalty": -1.5},
                "positivist": {"research_bonus": 0.03},
            },
        },
    },

    "rationing": {
        0: {"base": {}},  # no_rationing (default) — effects handled by rationing system
        1: {"base": {}},  # civilian_priority
        2: {"base": {}},  # military_priority
        3: {"base": {}},  # government_priority
    },

    # =========================================================================
    # SOCIAL (12 categories)
    # =========================================================================
    "education_policy": {
        0: {  # no_education
            "base": {
                "research_penalty": -0.08,
                "upkeep_reduction": 0.03,
                "literacy_bonus": -0.05,
            },
        },
        1: {"base": {}},  # basic_education (default)
        2: {  # primary_education
            "base": {
                "research_bonus": 0.03,
                "upkeep_reduction": -0.02,
                "literacy_bonus": 0.03,
            },
        },
        3: {  # secondary_education
            "base": {
                "research_bonus": 0.06,
                "upkeep_reduction": -0.04,
                "building_efficiency_bonus": {"communications": 0.03},
                "literacy_bonus": 0.05,
            },
            "trait_modifiers": {
                "positivist": {"research_bonus": 0.03},
                "egalitarian": {"stability_bonus": 0.5},
            },
        },
        4: {  # universal_education
            "base": {
                "research_bonus": 0.10,
                "upkeep_reduction": -0.06,
                "building_efficiency_bonus": {"communications": 0.05, "pharmaceutical": 0.03},
                "growth_bonus": 0.0002,
                "literacy_bonus": 0.08,
            },
            "government_modifiers": {
                "liberal": {"wealth_production_bonus": -0.02},
                "collectivist": {"stability_bonus": 1.0},
            },
            "trait_modifiers": {
                "positivist": {"research_bonus": 0.05},
                "egalitarian": {"stability_bonus": 1.0, "research_bonus": 0.02},
                "elitist": {"stability_penalty": -1.0},
            },
        },
    },

    "healthcare_policy": {
        0: {  # no_healthcare
            "base": {
                "growth_penalty": -0.0005,
                "upkeep_reduction": 0.02,
            },
        },
        1: {"base": {}},  # basic_healthcare (default)
        2: {  # public_healthcare
            "base": {
                "growth_bonus": 0.0003,
                "stability_bonus": 0.5,
                "upkeep_reduction": -0.03,
            },
            "trait_modifiers": {
                "egalitarian": {"stability_bonus": 0.5},
                "collectivist": {"stability_bonus": 0.5},
            },
        },
        3: {  # universal_healthcare
            "base": {
                "growth_bonus": 0.0006,
                "stability_bonus": 1.5,
                "upkeep_reduction": -0.05,
                "stability_recovery_bonus": 0.05,
                "building_efficiency_bonus": {"healthcare": 0.04},
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 1.0},
                "liberal": {"upkeep_reduction": -0.03},
            },
            "trait_modifiers": {
                "egalitarian": {"stability_bonus": 1.0, "growth_bonus": 0.0002},
                "collectivist": {"stability_bonus": 1.0},
                "libertarian": {"stability_penalty": -1.0},
            },
        },
    },

    "housing_policy": {
        0: {"base": {"upkeep_reduction": 0.02}},
        1: {"base": {"upkeep_reduction": -0.01, "stability_bonus": 0.3}},
        2: {  # public_housing
            "base": {
                "upkeep_reduction": -0.03,
                "stability_bonus": 0.5,
                "growth_bonus": 0.0002,
                "urban_threshold_reduction": 5000,
            },
        },
        3: {  # assigned_housing
            "base": {
                "upkeep_reduction": -0.04,
                "stability_bonus": 0.5,
                "growth_bonus": 0.0003,
                "urban_threshold_reduction": 8000,
            },
            "government_modifiers": {"collectivist": {"stability_bonus": 1.0}},
            "trait_modifiers": {"collectivist": {"stability_bonus": 0.5}, "libertarian": {"stability_penalty": -1.5}},
        },
    },

    "welfare_policy": {
        0: {  # no_welfare
            "base": {
                "upkeep_reduction": 0.04,
                "stability_penalty": -1.0,
                "growth_penalty": -0.0003,
            },
            "trait_modifiers": {
                "libertarian": {"stability_bonus": 0.5},
                "egalitarian": {"stability_penalty": -2.0},
            },
        },
        1: {"base": {}},  # minimal_welfare (default)
        2: {  # moderate_welfare
            "base": {
                "stability_bonus": 0.5,
                "growth_bonus": 0.0002,
                "upkeep_reduction": -0.02,
            },
            "trait_modifiers": {
                "egalitarian": {"stability_bonus": 0.5},
                "collectivist": {"stability_bonus": 0.5},
            },
        },
        3: {  # comprehensive_welfare
            "base": {
                "stability_bonus": 1.5,
                "growth_bonus": 0.0004,
                "upkeep_reduction": -0.05,
                "stability_recovery_bonus": 0.04,
                "building_efficiency_bonus": {"government_welfare": 0.04},
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 1.0},
                "liberal": {"upkeep_reduction": -0.03},
            },
            "trait_modifiers": {
                "egalitarian": {"stability_bonus": 1.0},
                "collectivist": {"stability_bonus": 1.0},
                "individualist": {"stability_penalty": -1.0},
            },
        },
        4: {  # universal_income
            "base": {
                "stability_bonus": 2.0,
                "growth_bonus": 0.0006,
                "upkeep_reduction": -0.08,
                "wealth_production_bonus": -0.03,
                "building_efficiency_bonus": {"government_welfare": 0.06, "government_organization": 0.03},
            },
            "government_modifiers": {
                "collectivist": {"stability_bonus": 2.0},
                "liberal": {"stability_penalty": -3.0, "upkeep_reduction": -0.05},
            },
            "trait_modifiers": {
                "egalitarian": {"stability_bonus": 2.0, "growth_bonus": 0.0003},
                "collectivist": {"stability_bonus": 1.5},
                "individualist": {"stability_penalty": -2.0},
                "libertarian": {"stability_penalty": -1.0},
            },
        },
    },

    "religion_policy": {
        0: {  # state_atheism
            "base": {
                "research_bonus": 0.03,
                "building_efficiency_bonus": {"religious": -0.15},
                "stability_penalty": -2.0,
            },
            "government_modifiers": {
                "religious": {"stability_penalty": -10.0},
                "collectivist": {"stability_bonus": 1.0},
            },
            "trait_modifiers": {
                "spiritualist": {"stability_penalty": -5.0},
                "positivist": {"stability_bonus": 1.0},
            },
        },
        1: {  # secular_state
            "base": {
                "research_bonus": 0.02,
                "stability_bonus": 0.5,
            },
            "government_modifiers": {
                "religious": {"stability_penalty": -3.0},
            },
            "trait_modifiers": {
                "positivist": {"stability_bonus": 0.5},
                "spiritualist": {"stability_penalty": -1.0},
            },
        },
        2: {"base": {}},  # religious_tolerance (default)
        3: {  # state_religion
            "base": {
                "stability_bonus": 2.0,
                "building_efficiency_bonus": {"religious": 0.08, "healthcare": 0.03},
                "research_penalty": -0.03,
            },
            "government_modifiers": {
                "religious": {"stability_bonus": 2.0, "building_efficiency_bonus": {"religious": 0.05}},
                "liberal": {"stability_penalty": -1.0},
            },
            "trait_modifiers": {
                "spiritualist": {"stability_bonus": 2.0},
                "positivist": {"stability_penalty": -2.0, "research_penalty": -0.02},
            },
        },
        4: {  # theocratic_law
            "base": {
                "stability_bonus": 3.0,
                "building_efficiency_bonus": {"religious": 0.12},
                "research_penalty": -0.08,
                "growth_bonus": 0.0005,
            },
            "government_modifiers": {
                "religious": {"stability_bonus": 3.0, "building_efficiency_bonus": {"religious": 0.08}},
                "elections": {"stability_penalty": -5.0},
                "liberal": {"stability_penalty": -3.0},
                "military_power": {"stability_penalty": -1.0},
            },
            "trait_modifiers": {
                "spiritualist": {"stability_bonus": 3.0, "growth_bonus": 0.0003},
                "positivist": {"stability_penalty": -4.0, "research_penalty": -0.05},
                "libertarian": {"stability_penalty": -3.0},
                "modern": {"stability_penalty": -2.0},
            },
        },
    },

    "press_freedom": {
        0: {  # free_press
            "base": {
                "research_bonus": 0.03,
                "stability_penalty": -0.5,
                "literacy_bonus": 0.03,
                "building_efficiency_bonus": {"communications": 0.03},
            },
            "government_modifiers": {
                "elections": {"stability_bonus": 1.5},
                "singular": {"stability_penalty": -2.0},
                "military_power": {"stability_penalty": -2.0},
            },
            "trait_modifiers": {
                "libertarian": {"stability_bonus": 1.0},
                "authoritarian": {"stability_penalty": -1.5},
            },
        },
        1: {"base": {}},  # regulated_press (default)
        2: {  # censored_press
            "base": {
                "stability_bonus": 1.0,
                "research_penalty": -0.02,
            },
            "government_modifiers": {
                "elections": {"stability_penalty": -2.0},
            },
            "trait_modifiers": {
                "authoritarian": {"stability_bonus": 0.5},
                "libertarian": {"stability_penalty": -2.0},
            },
        },
        3: {  # state_media
            "base": {
                "stability_bonus": 2.0,
                "research_penalty": -0.04,
                "upkeep_reduction": -0.02,
                "building_efficiency_bonus": {"communications": 0.04},
            },
            "government_modifiers": {
                "elections": {"stability_penalty": -4.0},
                "singular": {"stability_bonus": 1.0},
                "military_power": {"stability_bonus": 1.0},
            },
            "trait_modifiers": {
                "authoritarian": {"stability_bonus": 1.5},
                "libertarian": {"stability_penalty": -4.0},
                "positivist": {"research_penalty": -0.02},
            },
        },
    },

    "family_policy": {
        0: {"base": {}},
        1: {  # pro_natalist
            "base": {
                "growth_bonus": 0.0008,
                "upkeep_reduction": -0.02,
                "urban_growth_penalty": -0.0002,
            },
            "trait_modifiers": {"nationalist": {"growth_bonus": 0.0003}},
        },
        2: {  # family_planning
            "base": {"growth_penalty": -0.0003, "research_bonus": 0.02, "literacy_bonus": 0.02},
        },
        3: {  # population_control
            "base": {"growth_penalty": -0.001, "stability_penalty": -2.0},
            "government_modifiers": {"elections": {"stability_penalty": -3.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 1.0}, "libertarian": {"stability_penalty": -3.0}},
        },
    },

    "policing_policy": {
        0: {"base": {"stability_penalty": -0.5, "upkeep_reduction": 0.02}},
        1: {"base": {}},  # local_police (default)
        2: {  # national_police
            "base": {
                "stability_bonus": 0.5,
                "upkeep_reduction": -0.02,
                "building_efficiency_bonus": {"government_security": 0.04},
            },
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}},
        },
        3: {  # military_police
            "base": {
                "stability_bonus": 1.0,
                "upkeep_reduction": -0.03,
                "growth_penalty": -0.0002,
                "building_efficiency_bonus": {"government_security": 0.06},
                "march_speed_bonus": 0.02,
            },
            "government_modifiers": {"military_power": {"stability_bonus": 1.0}},
            "trait_modifiers": {"militarist": {"stability_bonus": 0.5}, "libertarian": {"stability_penalty": -2.0}},
        },
    },

    "prison_policy": {
        0: {"base": {"stability_penalty": -0.5}},
        1: {"base": {}},  # basic_prisons (default)
        2: {"base": {"stability_bonus": 0.5, "growth_bonus": 0.0001, "upkeep_reduction": -0.01}},
        3: {  # labour_camps
            "base": {
                "building_efficiency_bonus": {"construction": 0.03, "extraction": 0.03},
                "stability_penalty": -1.5,
            },
            "government_modifiers": {"elections": {"stability_penalty": -2.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}, "egalitarian": {"stability_penalty": -2.0}},
        },
    },

    "war_policy": {
        0: {  # absolute_pacifism
            "base": {
                "stability_bonus": 2.0,
                "growth_bonus": 0.0005,
                "army_combat_bonus": -0.10,
                "navy_combat_bonus": -0.10,
                "air_combat_bonus": -0.10,
                "army_upkeep_reduction": 0.05,
                "navy_upkeep_reduction": 0.05,
                "air_upkeep_reduction": 0.05,
            },
            "trait_modifiers": {
                "pacifist": {"stability_bonus": 2.0},
                "militarist": {"stability_penalty": -5.0},
            },
        },
        1: {  # defensive_war
            "base": {
                "stability_bonus": 1.0,
                "army_combat_bonus": 0.02,
            },
            "trait_modifiers": {
                "pacifist": {"stability_bonus": 0.5},
            },
        },
        2: {"base": {}},  # just_war (default)
        3: {  # preemptive_war
            "base": {
                "army_combat_bonus": 0.03,
                "stability_penalty": -1.0,
                "army_upkeep_reduction": -0.02,
                "march_speed_bonus": 0.03,
            },
            "trait_modifiers": {
                "militarist": {"army_combat_bonus": 0.03, "stability_bonus": 0.5},
                "pacifist": {"stability_penalty": -3.0},
            },
        },
        4: {  # total_war
            "base": {
                "army_combat_bonus": 0.06,
                "navy_combat_bonus": 0.06,
                "air_combat_bonus": 0.06,
                "manpower_bonus": 0.10,
                "stability_penalty": -3.0,
                "growth_penalty": -0.001,
                "wealth_production_bonus": -0.05,
                "army_upkeep_reduction": -0.04,
                "navy_upkeep_reduction": -0.04,
                "air_upkeep_reduction": -0.04,
            },
            "government_modifiers": {
                "military_power": {"stability_bonus": 2.0, "army_combat_bonus": 0.03},
                "elections": {"stability_penalty": -4.0},
            },
            "trait_modifiers": {
                "militarist": {"stability_bonus": 2.0, "army_combat_bonus": 0.05},
                "pacifist": {"stability_penalty": -6.0},
                "nationalist": {"stability_bonus": 1.0},
            },
        },
    },

    # =========================================================================
    # GOVERNANCE (10 categories)
    # =========================================================================
    "government_transparency": {
        0: {  # total_secrecy
            "base": {"stability_penalty": -1.0, "upkeep_reduction": 0.03},
            "government_modifiers": {"elections": {"stability_penalty": -4.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 1.0}, "libertarian": {"stability_penalty": -3.0}},
        },
        1: {"base": {}},  # selective_disclosure (default)
        2: {  # open_government
            "base": {"stability_bonus": 1.0, "upkeep_reduction": -0.02, "research_bonus": 0.02},
            "government_modifiers": {"elections": {"stability_bonus": 1.5}, "singular": {"stability_penalty": -2.0}, "military_power": {"stability_penalty": -2.0}},
            "trait_modifiers": {"libertarian": {"stability_bonus": 1.0}, "authoritarian": {"stability_penalty": -1.5}},
        },
    },

    "corruption_policy": {
        0: {"base": {"upkeep_reduction": -0.08, "integration_bonus": -0.05, "wealth_production_bonus": -0.03, "stability_penalty": -2.0}},
        1: {"base": {"upkeep_reduction": -0.03, "stability_penalty": -0.5}},
        2: {"base": {}},  # anti_corruption (default)
        3: {
            "base": {"upkeep_reduction": -0.02, "stability_bonus": 1.0, "integration_bonus": 0.03},
            "government_modifiers": {"singular": {"stability_bonus": 0.5}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}, "honorable": {"stability_bonus": 1.0}},
        },
    },

    "bureaucratic_structure": {
        0: {  # minimal_bureaucracy
            "base": {
                "upkeep_reduction": 0.06,
                "integration_bonus": -0.05,
                "bureaucratic_capacity": -200,
                "building_efficiency_bonus": {"government_regulatory": -0.04, "government_oversight": -0.04},
            },
            "trait_modifiers": {"libertarian": {"stability_bonus": 1.0}},
        },
        1: {"base": {}},  # functional_bureaucracy (default)
        2: {
            "base": {"upkeep_reduction": -0.04, "integration_bonus": 0.03, "bureaucratic_capacity": 200},
            "trait_modifiers": {"authoritarian": {"integration_bonus": 0.02}},
        },
        3: {  # total_administration
            "base": {
                "upkeep_reduction": -0.08,
                "integration_bonus": 0.06,
                "bureaucratic_capacity": 500,
                "stability_penalty": -1.0,
                "wealth_production_bonus": -0.03,
                "building_efficiency_bonus": {"government_regulatory": 0.05, "government_oversight": 0.05, "government_management": 0.05},
            },
            "government_modifiers": {"elections": {"stability_penalty": -2.0}, "collectivist": {"stability_bonus": 1.0}, "singular": {"stability_bonus": 1.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 1.0, "integration_bonus": 0.03}, "libertarian": {"stability_penalty": -4.0}, "collectivist": {"stability_bonus": 1.0}},
        },
    },

    "political_parties": {
        0: {
            "base": {"stability_penalty": -1.0},
            "government_modifiers": {"elections": {"stability_penalty": -5.0}, "singular": {"stability_bonus": 1.0}, "military_power": {"stability_bonus": 1.0}},
        },
        1: {
            "base": {"stability_penalty": -0.5, "integration_bonus": 0.02},
            "government_modifiers": {"elections": {"stability_penalty": -3.0}, "collectivist": {"stability_bonus": 1.0}, "singular": {"stability_bonus": 0.5}},
        },
        2: {"base": {}},  # limited_parties (default)
        3: {
            "base": {"stability_bonus": 1.0, "research_bonus": 0.02},
            "government_modifiers": {"elections": {"stability_bonus": 2.0}, "singular": {"stability_penalty": -2.0}, "military_power": {"stability_penalty": -2.0}, "religious": {"stability_penalty": -1.0}},
            "trait_modifiers": {"libertarian": {"stability_bonus": 1.0}, "authoritarian": {"stability_penalty": -1.5}},
        },
    },

    "local_governance": {
        0: {  # centralised
            "base": {"integration_bonus": 0.05, "stability_penalty": -1.0, "rural_output_penalty": -0.02},
            "government_modifiers": {"singular": {"stability_bonus": 1.0}, "military_power": {"stability_bonus": 0.5}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5, "integration_bonus": 0.02}, "libertarian": {"stability_penalty": -2.0}},
        },
        1: {"base": {}},  # delegated (default)
        2: {
            "base": {"integration_bonus": -0.03, "stability_bonus": 1.0, "growth_bonus": 0.0002},
            "government_modifiers": {"subsistence": {"stability_bonus": 1.0}},
            "trait_modifiers": {"libertarian": {"stability_bonus": 1.0}, "authoritarian": {"stability_penalty": -1.0}},
        },
        3: {  # federal
            "base": {"integration_bonus": -0.05, "stability_bonus": 1.5, "growth_bonus": 0.0003, "research_bonus": 0.02, "rural_output_bonus": 0.03},
            "government_modifiers": {"elections": {"stability_bonus": 1.0}, "singular": {"stability_penalty": -3.0}, "military_power": {"stability_penalty": -3.0}},
            "trait_modifiers": {"libertarian": {"stability_bonus": 1.5}, "authoritarian": {"stability_penalty": -2.0}},
        },
    },

    "succession_policy": {
        0: {  # hereditary
            "base": {"stability_bonus": 1.5, "bureaucratic_capacity": -100, "research_penalty": -0.03},
            "government_modifiers": {"subsistence": {"stability_bonus": 1.0}, "elections": {"stability_penalty": -3.0}},
            "trait_modifiers": {"traditionalist": {"stability_bonus": 1.0}, "modern": {"stability_penalty": -1.0}},
        },
        1: {"base": {}},  # appointed_successor (default)
        2: {  # elected_leader
            "base": {"stability_bonus": 0.5, "research_bonus": 0.02, "bureaucratic_capacity": 100},
            "government_modifiers": {"elections": {"stability_bonus": 1.0}, "singular": {"stability_penalty": -2.0}, "military_power": {"stability_penalty": -2.0}},
            "trait_modifiers": {"egalitarian": {"stability_bonus": 0.5}},
        },
        3: {  # council_selected
            "base": {"stability_bonus": 1.0, "integration_bonus": 0.02},
            "government_modifiers": {"collectivist": {"stability_bonus": 0.5}, "subsistence": {"stability_bonus": 0.5}},
            "trait_modifiers": {"collectivist": {"stability_bonus": 0.5}},
        },
    },

    "civil_service": {
        0: {  # patronage_system
            "base": {"upkeep_reduction": -0.05, "integration_bonus": -0.03, "stability_penalty": -1.0, "building_efficiency_bonus": {"government_management": -0.04}},
        },
        1: {"base": {}},  # basic_civil_service (default)
        2: {
            "base": {"integration_bonus": 0.03, "bureaucratic_capacity": 100, "upkeep_reduction": -0.02},
            "trait_modifiers": {"elitist": {"integration_bonus": 0.02}},
        },
        3: {  # technocratic_service
            "base": {
                "research_bonus": 0.04,
                "integration_bonus": 0.04,
                "bureaucratic_capacity": 200,
                "upkeep_reduction": -0.03,
                "building_efficiency_bonus": {"government_management": 0.05, "government_education": 0.03},
                "literacy_bonus": 0.03,
            },
            "government_modifiers": {"subsistence": {"stability_penalty": -1.5}},
            "trait_modifiers": {"positivist": {"research_bonus": 0.03}, "modern": {"research_bonus": 0.02}, "elitist": {"integration_bonus": 0.02, "research_bonus": 0.02}, "traditionalist": {"stability_penalty": -1.0}},
        },
    },

    "emergency_powers": {
        0: {
            "base": {},
            "government_modifiers": {"military_power": {"stability_penalty": -2.0}, "singular": {"stability_penalty": -1.0}},
            "trait_modifiers": {"libertarian": {"stability_bonus": 1.0}},
        },
        1: {"base": {}},  # limited_emergency (default)
        2: {
            "base": {"stability_penalty": -0.5, "integration_bonus": 0.02},
            "government_modifiers": {"elections": {"stability_penalty": -1.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}, "libertarian": {"stability_penalty": -1.5}},
        },
        3: {  # permanent_emergency
            "base": {"stability_penalty": -2.0, "integration_bonus": 0.05, "manpower_bonus": 0.08, "growth_penalty": -0.0005},
            "government_modifiers": {"elections": {"stability_penalty": -5.0}, "collectivist": {"stability_penalty": -2.0}, "singular": {"stability_bonus": 1.0}, "military_power": {"stability_bonus": 2.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 2.0}, "libertarian": {"stability_penalty": -6.0}, "militarist": {"stability_bonus": 1.0, "manpower_bonus": 0.03}},
        },
    },

    "diplomatic_stance": {
        0: {  # isolationism
            "base": {"stability_bonus": 1.0, "land_trade_capacity": -150, "naval_trade_capacity": -100, "air_trade_capacity": -50, "integration_bonus": 0.03},
            "government_modifiers": {"subsistence": {"stability_bonus": 0.5}},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.5}, "internationalist": {"stability_penalty": -2.0}},
        },
        1: {"base": {}},  # cautious_engagement (default)
        2: {  # active_diplomacy
            "base": {"land_trade_capacity": 100, "naval_trade_capacity": 75, "air_trade_capacity": 50, "wealth_production_bonus": 0.03},
            "government_modifiers": {"elections": {"wealth_production_bonus": 0.02}},
            "trait_modifiers": {"internationalist": {"land_trade_capacity": 50}, "honorable": {"wealth_production_bonus": 0.01}},
        },
        3: {  # alliance_seeking
            "base": {"land_trade_capacity": 150, "naval_trade_capacity": 100, "air_trade_capacity": 75, "wealth_production_bonus": 0.04, "upkeep_reduction": -0.03},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}},
            "trait_modifiers": {"internationalist": {"land_trade_capacity": 75, "naval_trade_capacity": 50}, "nationalist": {"stability_penalty": -1.5}},
        },
    },

    "propaganda_policy": {
        0: {"base": {}, "trait_modifiers": {"libertarian": {"stability_bonus": 0.5}}},
        1: {"base": {"stability_bonus": 0.5}},
        2: {  # state_messaging
            "base": {"stability_bonus": 1.0, "upkeep_reduction": -0.02, "stability_recovery_bonus": 0.04},
            "government_modifiers": {"elections": {"stability_penalty": -1.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}, "libertarian": {"stability_penalty": -1.0}},
        },
        3: {  # total_propaganda
            "base": {"stability_bonus": 3.0, "research_penalty": -0.05, "upkeep_reduction": -0.04, "stability_recovery_bonus": 0.06},
            "government_modifiers": {"elections": {"stability_penalty": -5.0}, "singular": {"stability_bonus": 2.0}, "military_power": {"stability_bonus": 2.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 2.0}, "libertarian": {"stability_penalty": -5.0}, "positivist": {"research_penalty": -0.03}},
        },
    },

    # =========================================================================
    # CULTURE & IDENTITY (8 categories)
    # =========================================================================
    "cultural_policy": {
        0: {"base": {}},
        1: {  # cultural_preservation (default)
            "base": {"stability_bonus": 0.5, "building_efficiency_bonus": {"entertainment": 0.03}},
            "government_modifiers": {"religious": {"stability_bonus": 0.5}},
            "trait_modifiers": {"traditionalist": {"stability_bonus": 0.5}},
        },
        2: {  # cultural_promotion
            "base": {"stability_bonus": 1.0, "building_efficiency_bonus": {"entertainment": 0.04, "communications": 0.02}, "integration_bonus": 0.02},
            "government_modifiers": {"singular": {"stability_bonus": 0.5}},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.5, "integration_bonus": 0.01}},
        },
        3: {  # cultural_revolution
            "base": {"stability_penalty": -1.5, "research_bonus": 0.03, "building_efficiency_bonus": {"communications": 0.04}, "literacy_bonus": 0.02},
            "government_modifiers": {"collectivist": {"stability_bonus": 1.0}, "religious": {"stability_penalty": -2.0}},
            "trait_modifiers": {"modern": {"research_bonus": 0.02}, "traditionalist": {"stability_penalty": -2.0}},
        },
    },

    "language_policy": {
        0: {"base": {"integration_bonus": -0.02}},
        1: {"base": {}},  # official_language (default)
        2: {  # multilingual
            "base": {"stability_bonus": 0.5, "research_bonus": 0.02, "land_trade_capacity": 50, "naval_trade_capacity": 50, "literacy_bonus": 0.02},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}},
            "trait_modifiers": {"internationalist": {"research_bonus": 0.01, "land_trade_capacity": 25}},
        },
        3: {  # language_enforcement
            "base": {"integration_bonus": 0.03, "stability_penalty": -1.0, "bureaucratic_capacity": 50},
            "government_modifiers": {"singular": {"stability_bonus": 0.5}},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.5, "integration_bonus": 0.01}, "internationalist": {"stability_penalty": -1.0}},
        },
    },

    "arts_policy": {
        0: {"base": {"building_efficiency_bonus": {"entertainment": -0.04}}},
        1: {  # arts_patronage (default)
            "base": {"stability_bonus": 0.5, "building_efficiency_bonus": {"entertainment": 0.04}, "stability_recovery_bonus": 0.03},
            "government_modifiers": {"elections": {"stability_bonus": 0.3}},
        },
        2: {  # state_art
            "base": {"stability_bonus": 1.0, "building_efficiency_bonus": {"entertainment": 0.05}, "research_penalty": -0.02},
            "government_modifiers": {"singular": {"stability_bonus": 0.5}, "elections": {"stability_penalty": -1.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}, "libertarian": {"stability_penalty": -1.0}},
        },
    },

    "historical_narrative": {
        0: {"base": {}},
        1: {  # preservation_narrative (default)
            "base": {"research_bonus": 0.02, "building_efficiency_bonus": {"pharmaceutical": 0.02}},
            "trait_modifiers": {"positivist": {"research_bonus": 0.01}},
        },
        2: {  # rebirth_narrative
            "base": {"stability_bonus": 0.5, "growth_bonus": 0.0002, "urban_threshold_reduction": 3000},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}},
            "trait_modifiers": {"modern": {"growth_bonus": 0.0001, "urban_threshold_reduction": 2000}},
        },
        3: {  # glory_narrative
            "base": {"stability_bonus": 1.0, "manpower_bonus": 0.04, "research_penalty": -0.02},
            "government_modifiers": {"military_power": {"stability_bonus": 0.5, "manpower_bonus": 0.02}, "singular": {"stability_bonus": 0.5}},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.5, "manpower_bonus": 0.02}, "militarist": {"manpower_bonus": 0.02}},
        },
    },

    "family_policy": {
        # Already defined above in SOCIAL section
    },

    "youth_policy": {
        0: {"base": {}},  # no_youth_policy (default)
        1: {  # youth_education
            "base": {"research_bonus": 0.02, "literacy_bonus": 0.03, "growth_bonus": 0.0002},
            "government_modifiers": {"elections": {"research_bonus": 0.01}},
            "trait_modifiers": {"positivist": {"research_bonus": 0.01, "literacy_bonus": 0.01}, "egalitarian": {"growth_bonus": 0.0001}},
        },
        2: {  # youth_organisations
            "base": {"stability_bonus": 1.0, "manpower_bonus": 0.04, "integration_bonus": 0.02},
            "government_modifiers": {"singular": {"stability_bonus": 0.5}},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.5, "manpower_bonus": 0.02}},
        },
        3: {  # youth_militias
            "base": {"manpower_bonus": 0.08, "army_training_speed_bonus": 0.05, "stability_penalty": -0.5, "research_penalty": -0.02},
            "government_modifiers": {"military_power": {"manpower_bonus": 0.03, "stability_bonus": 0.5}, "elections": {"stability_penalty": -1.5}},
            "trait_modifiers": {"militarist": {"army_training_speed_bonus": 0.03, "manpower_bonus": 0.02}, "pacifist": {"stability_penalty": -2.0}},
        },
    },

    "gender_policy": {
        0: {  # traditional_roles
            "base": {"stability_bonus": 0.5, "growth_bonus": 0.0003, "manpower_bonus": -0.04, "research_penalty": -0.02},
            "government_modifiers": {"religious": {"stability_bonus": 0.5}},
            "trait_modifiers": {"traditionalist": {"stability_bonus": 0.5}, "egalitarian": {"stability_penalty": -1.5}},
        },
        1: {"base": {}},  # mixed_roles (default)
        2: {  # full_equality
            "base": {"manpower_bonus": 0.06, "research_bonus": 0.02, "growth_penalty": -0.0001},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}, "collectivist": {"stability_bonus": 0.5}},
            "trait_modifiers": {"egalitarian": {"stability_bonus": 0.5, "manpower_bonus": 0.02}, "modern": {"research_bonus": 0.01}, "traditionalist": {"stability_penalty": -1.0}},
        },
    },

    "elder_policy": {
        0: {"base": {"upkeep_reduction": 0.01}},
        1: {"base": {}},  # basic_elder_care (default)
        2: {  # elder_councils
            "base": {"stability_bonus": 1.0, "research_bonus": 0.02, "stability_recovery_bonus": 0.03, "building_efficiency_bonus": {"government_oversight": 0.03}},
            "government_modifiers": {"subsistence": {"stability_bonus": 1.0}},
            "trait_modifiers": {"traditionalist": {"stability_bonus": 0.5, "research_bonus": 0.01}, "modern": {"stability_penalty": -0.5}},
        },
    },

    # =========================================================================
    # PUBLIC ORDER (5 categories)
    # =========================================================================
    "assembly_rights": {
        0: {  # free_assembly
            "base": {"stability_penalty": -0.5, "research_bonus": 0.02, "growth_bonus": 0.0002},
            "government_modifiers": {"elections": {"stability_bonus": 1.0, "research_bonus": 0.01}, "singular": {"stability_penalty": -1.5}},
            "trait_modifiers": {"libertarian": {"stability_bonus": 0.5}, "authoritarian": {"stability_penalty": -1.0}},
        },
        1: {"base": {}},  # regulated_assembly (default)
        2: {
            "base": {"stability_bonus": 0.5, "research_penalty": -0.02},
            "government_modifiers": {"singular": {"stability_bonus": 0.5}, "elections": {"stability_penalty": -2.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.3}, "libertarian": {"stability_penalty": -1.5}},
        },
        3: {  # no_assembly
            "base": {"stability_bonus": 1.0, "research_penalty": -0.04, "growth_penalty": -0.0003, "building_efficiency_bonus": {"communications": -0.03}},
            "government_modifiers": {"military_power": {"stability_bonus": 1.0}, "elections": {"stability_penalty": -4.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}, "libertarian": {"stability_penalty": -3.0}, "egalitarian": {"stability_penalty": -1.5}},
        },
    },

    "curfew_policy": {
        0: {"base": {}},  # no_curfew (default)
        1: {"base": {"stability_bonus": 0.3, "stability_recovery_bonus": 0.02}},
        2: {  # mandatory_curfew
            "base": {"stability_bonus": 1.0, "stability_recovery_bonus": 0.05, "wealth_production_bonus": -0.03, "building_efficiency_bonus": {"entertainment": -0.04}, "growth_penalty": -0.0002},
            "government_modifiers": {"military_power": {"stability_bonus": 0.5}, "elections": {"stability_penalty": -2.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}, "libertarian": {"stability_penalty": -2.0}},
        },
    },

    "identity_documents": {
        0: {"base": {"growth_bonus": 0.0002, "integration_bonus": -0.02, "bureaucratic_capacity": -50}, "trait_modifiers": {"libertarian": {"stability_bonus": 0.3}}},
        1: {"base": {}},  # basic_registration (default)
        2: {
            "base": {"integration_bonus": 0.02, "bureaucratic_capacity": 75, "stability_bonus": 0.5},
            "government_modifiers": {"singular": {"integration_bonus": 0.01}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.3}, "libertarian": {"stability_penalty": -0.5}},
        },
        3: {  # biometric_tracking
            "base": {"integration_bonus": 0.04, "bureaucratic_capacity": 150, "stability_bonus": 1.0, "research_penalty": -0.02, "growth_penalty": -0.0002},
            "government_modifiers": {"singular": {"stability_bonus": 0.5}, "elections": {"stability_penalty": -2.0}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}, "modern": {"research_bonus": 0.02}, "libertarian": {"stability_penalty": -2.5}},
        },
    },

    "drug_policy": {
        0: {  # unregulated_drugs
            "base": {"stability_penalty": -0.5, "wealth_production_bonus": 0.02, "building_efficiency_bonus": {"pharmaceutical": 0.03}, "growth_penalty": -0.0002},
            "trait_modifiers": {"libertarian": {"stability_bonus": 0.5}},
        },
        1: {"base": {}},  # medical_only (default)
        2: {  # total_prohibition
            "base": {"stability_bonus": 0.5, "building_efficiency_bonus": {"pharmaceutical": -0.02}, "wealth_production_bonus": -0.01},
            "government_modifiers": {"religious": {"stability_bonus": 0.5}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.3}, "libertarian": {"stability_penalty": -1.0}, "spiritualist": {"stability_bonus": 0.5}},
        },
    },

    "justice_system": {
        0: {  # tribal_justice
            "base": {"stability_bonus": 0.5, "bureaucratic_capacity": -75, "upkeep_reduction": 0.02},
            "government_modifiers": {"subsistence": {"stability_bonus": 1.0}},
            "trait_modifiers": {"traditionalist": {"stability_bonus": 0.5}, "modern": {"stability_penalty": -1.0}},
        },
        1: {"base": {}},  # codified_law (default)
        2: {  # restorative_justice
            "base": {"stability_bonus": 0.5, "growth_bonus": 0.0002, "stability_recovery_bonus": 0.04},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}},
            "trait_modifiers": {"egalitarian": {"stability_bonus": 0.5, "growth_bonus": 0.0001}, "authoritarian": {"stability_penalty": -0.5}},
        },
        3: {  # harsh_penalties
            "base": {"stability_bonus": 1.0, "growth_penalty": -0.0003, "manpower_bonus": 0.03},
            "government_modifiers": {"military_power": {"stability_bonus": 0.5}, "elections": {"stability_penalty": -1.5}},
            "trait_modifiers": {"authoritarian": {"stability_bonus": 0.5}, "egalitarian": {"stability_penalty": -1.0}},
        },
    },

    # =========================================================================
    # FOREIGN RELATIONS (5 categories)
    # =========================================================================
    "alliance_policy": {
        0: {
            "base": {"stability_bonus": 0.5, "army_upkeep_reduction": 0.03, "navy_upkeep_reduction": 0.03, "air_upkeep_reduction": 0.03},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.5}},
        },
        1: {"base": {}},  # defensive_pacts (default)
        2: {
            "base": {"army_combat_bonus": 0.03, "navy_combat_bonus": 0.03, "air_combat_bonus": 0.03, "army_upkeep_reduction": -0.02, "navy_upkeep_reduction": -0.02, "stability_penalty": -0.5},
            "government_modifiers": {"military_power": {"army_combat_bonus": 0.02}},
            "trait_modifiers": {"militarist": {"army_combat_bonus": 0.02, "navy_combat_bonus": 0.01}, "pacifist": {"stability_penalty": -1.0}},
        },
        3: {  # federation_seeking
            "base": {"land_trade_capacity": 100, "naval_trade_capacity": 75, "integration_bonus": 0.03, "upkeep_reduction": -0.03},
            "government_modifiers": {"elections": {"stability_bonus": 1.0}, "singular": {"stability_penalty": -2.0}},
            "trait_modifiers": {"internationalist": {"land_trade_capacity": 50, "integration_bonus": 0.02}, "nationalist": {"stability_penalty": -2.0}},
        },
    },

    "foreign_aid": {
        0: {"base": {}},  # no_foreign_aid (default)
        1: {
            "base": {"wealth_production_bonus": -0.02, "land_trade_capacity": 50, "stability_bonus": 0.3},
            "government_modifiers": {"liberal": {"wealth_production_bonus": 0.01}},
            "trait_modifiers": {"devious": {"stability_bonus": 0.3}},
        },
        2: {
            "base": {"wealth_production_bonus": -0.04, "stability_bonus": 1.0, "growth_bonus": 0.0002},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}, "collectivist": {"stability_bonus": 0.5}},
            "trait_modifiers": {"internationalist": {"stability_bonus": 0.5}, "egalitarian": {"stability_bonus": 0.3}, "nationalist": {"stability_penalty": -1.0}},
        },
    },

    "treaty_compliance": {
        0: {
            "base": {"stability_penalty": -0.5, "wealth_production_bonus": 0.02},
            "trait_modifiers": {"devious": {"wealth_production_bonus": 0.02}, "honorable": {"stability_penalty": -2.0}},
        },
        1: {"base": {}},  # treaty_respected (default)
        2: {
            "base": {"stability_bonus": 1.0, "land_trade_capacity": 75, "naval_trade_capacity": 50},
            "government_modifiers": {"elections": {"stability_bonus": 0.3}},
            "trait_modifiers": {"honorable": {"stability_bonus": 1.0, "land_trade_capacity": 50}, "devious": {"stability_penalty": -1.5}},
        },
    },

    "espionage_stance": {
        0: {"base": {"stability_bonus": 0.5, "upkeep_reduction": 0.02}, "trait_modifiers": {"pacifist": {"stability_bonus": 0.3}}},
        1: {"base": {}},  # defensive_espionage (default)
        2: {
            "base": {"building_efficiency_bonus": {"government_security": 0.04}, "stability_penalty": -0.5, "upkeep_reduction": -0.02},
            "government_modifiers": {"singular": {"stability_bonus": 0.5}},
            "trait_modifiers": {"devious": {"building_efficiency_bonus": {"government_security": 0.02}}, "honorable": {"stability_penalty": -1.0}},
        },
        3: {  # aggressive_espionage
            "base": {"building_efficiency_bonus": {"government_security": 0.06}, "stability_penalty": -1.5, "upkeep_reduction": -0.04, "army_combat_bonus": 0.02},
            "government_modifiers": {"singular": {"stability_bonus": 1.0}, "military_power": {"stability_bonus": 0.5, "army_combat_bonus": 0.01}, "elections": {"stability_penalty": -3.0}},
            "trait_modifiers": {"devious": {"stability_bonus": 1.0, "army_combat_bonus": 0.01}, "honorable": {"stability_penalty": -3.0}, "authoritarian": {"stability_bonus": 0.5}},
        },
    },

    # =========================================================================
    # REMAINING SOCIAL (6 categories)
    # =========================================================================
    "citizenship_policy": {
        0: {
            "base": {"growth_bonus": 0.0006, "stability_penalty": -0.5, "integration_bonus": -0.02},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}},
            "trait_modifiers": {"internationalist": {"growth_bonus": 0.0002}, "nationalist": {"stability_penalty": -1.5}},
        },
        1: {"base": {}},  # residency_citizenship (default)
        2: {
            "base": {"stability_bonus": 0.5, "integration_bonus": 0.02, "growth_penalty": -0.0003},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.5, "integration_bonus": 0.01}, "internationalist": {"stability_penalty": -0.5}},
        },
        3: {  # merit_citizenship
            "base": {"research_bonus": 0.02, "wealth_production_bonus": 0.02, "bureaucratic_capacity": 75},
            "government_modifiers": {"liberal": {"wealth_production_bonus": 0.02}},
            "trait_modifiers": {"elitist": {"research_bonus": 0.02}, "egalitarian": {"stability_penalty": -1.0}},
        },
    },

    "migration_policy": {
        0: {
            "base": {"growth_bonus": 0.0008, "stability_penalty": -0.5, "urban_threshold_reduction": 5000},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}},
            "trait_modifiers": {"internationalist": {"growth_bonus": 0.0002}, "nationalist": {"stability_penalty": -2.0}},
        },
        1: {"base": {}},  # accept_migrants (default)
        2: {
            "base": {"stability_bonus": 0.5, "growth_penalty": -0.0002, "integration_bonus": 0.02},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.3}},
        },
        3: {
            "base": {"stability_bonus": 1.0, "growth_penalty": -0.0005, "integration_bonus": 0.04},
            "government_modifiers": {"singular": {"stability_bonus": 0.5}},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.5}, "internationalist": {"stability_penalty": -1.5}},
        },
    },

    "social_mobility": {
        0: {  # caste_system
            "base": {"stability_bonus": 1.0, "research_penalty": -0.03, "growth_penalty": -0.0002, "building_efficiency_bonus": {"government_management": 0.03}},
            "government_modifiers": {"religious": {"stability_bonus": 0.5}, "elections": {"stability_penalty": -3.0}},
            "trait_modifiers": {"traditionalist": {"stability_bonus": 0.5}, "egalitarian": {"stability_penalty": -3.0}},
        },
        1: {"base": {}},  # limited_mobility (default)
        2: {
            "base": {"research_bonus": 0.03, "wealth_production_bonus": 0.02, "building_efficiency_bonus": {"government_education": 0.04}},
            "government_modifiers": {"liberal": {"wealth_production_bonus": 0.02}},
            "trait_modifiers": {"elitist": {"research_bonus": 0.02}, "modern": {"research_bonus": 0.01}},
        },
        3: {  # egalitarian_mobility
            "base": {"stability_bonus": 1.0, "growth_bonus": 0.0003, "research_penalty": -0.02, "rural_output_bonus": 0.03},
            "government_modifiers": {"collectivist": {"stability_bonus": 1.0, "growth_bonus": 0.0001}, "liberal": {"stability_penalty": -1.5}},
            "trait_modifiers": {"egalitarian": {"stability_bonus": 0.5, "growth_bonus": 0.0001}, "elitist": {"stability_penalty": -1.5}, "collectivist": {"stability_bonus": 0.5}},
        },
    },

    "minority_rights": {
        0: {
            "base": {"stability_penalty": -1.0, "manpower_bonus": 0.04, "growth_penalty": -0.0005, "research_penalty": -0.03},
            "government_modifiers": {"military_power": {"stability_bonus": 0.5}, "elections": {"stability_penalty": -3.0}},
            "trait_modifiers": {"nationalist": {"stability_bonus": 0.5}, "egalitarian": {"stability_penalty": -3.0}, "internationalist": {"stability_penalty": -2.0}},
        },
        1: {"base": {}},  # tolerance (default)
        2: {
            "base": {"stability_bonus": 0.5, "growth_bonus": 0.0002, "research_bonus": 0.02},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}},
            "trait_modifiers": {"internationalist": {"stability_bonus": 0.3}},
        },
        3: {
            "base": {"stability_bonus": 1.0, "growth_bonus": 0.0003, "research_bonus": 0.03, "literacy_bonus": 0.02},
            "government_modifiers": {"elections": {"stability_bonus": 0.5}, "collectivist": {"stability_bonus": 0.5}},
            "trait_modifiers": {"egalitarian": {"stability_bonus": 1.0}, "internationalist": {"stability_bonus": 0.5, "research_bonus": 0.01}, "nationalist": {"stability_penalty": -1.5}},
        },
    },
}

# family_policy was duplicated in the SOCIAL section — remove the empty CULTURE stub
# (The real entry is in the SOCIAL block above)
POLICY_EFFECTS.pop("family_policy", None)
POLICY_EFFECTS["family_policy"] = {
    0: {"base": {}},
    1: {  # pro_natalist
        "base": {"growth_bonus": 0.0008, "upkeep_reduction": -0.02, "urban_growth_penalty": -0.0002},
        "trait_modifiers": {"nationalist": {"growth_bonus": 0.0003}},
    },
    2: {"base": {"growth_penalty": -0.0003, "research_bonus": 0.02, "literacy_bonus": 0.02}},
    3: {
        "base": {"growth_penalty": -0.001, "stability_penalty": -2.0},
        "government_modifiers": {"elections": {"stability_penalty": -3.0}},
        "trait_modifiers": {"authoritarian": {"stability_bonus": 1.0}, "libertarian": {"stability_penalty": -3.0}},
    },
}


# =============================================================================
# POLICY_REQUIREMENTS — prerequisites to select a policy level
#
# Keys: (category, level_index) -> dict with optional keys:
#   "gov_axis_required": nation must have at least one of these axis values
#                        (across all five axes: direction, economic_category,
#                        structure, power_origin, power_type)
#   "gov_axis_banned":   nation must not have any of these axis values
#   "traits_required":   list of trait keys (must have at least one)
#   "traits_banned":     list of trait keys (must not have any)
#   "policies_required": list of (category, min_level) tuples
# =============================================================================

POLICY_REQUIREMENTS = {
    ("intelligence_policy", 3): {"gov_axis_banned": ["elections"]},
    ("religion_policy", 4): {"gov_axis_required": ["religious"]},
    ("religion_policy", 3): {"gov_axis_banned": ["collectivist"]},
    ("religion_policy", 0): {"gov_axis_banned": ["religious"]},
    ("economic_system", 3): {"gov_axis_banned": ["liberal"]},
    ("military_spending", 4): {"policies_required": [("military_service", 2)]},
    ("military_service", 6): {"policies_required": [("military_spending", 4), ("emergency_powers", 2)]},
    ("military_service", 4): {"policies_required": [("military_spending", 2)]},
    ("military_doctrine", 3): {"policies_required": [("manufacturing_policy", 2)]},
    ("propaganda_policy", 3): {"policies_required": [("press_freedom", 2)]},
    ("emergency_powers", 3): {"gov_axis_banned": ["elections"]},
    ("manufacturing_policy", 3): {"policies_required": [("research_policy", 2)]},
    ("industrial_policy", 3): {"policies_required": [("education_policy", 3)]},
    ("political_parties", 3): {"gov_axis_banned": ["singular", "military_power"]},
    ("political_parties", 0): {"gov_axis_banned": ["elections"]},
    ("currency_policy", 2): {"policies_required": [("banking_policy", 2)]},
    ("prison_policy", 3): {"gov_axis_banned": ["elections", "collectivist"]},
    ("labour_policy", 0): {"gov_axis_banned": ["elections"]},
    ("war_policy", 4): {"policies_required": [("military_service", 3)]},
    ("war_policy", 0): {"gov_axis_banned": ["military_power"]},
}


# =============================================================================
# POLICY_BANS — cross-policy incompatibilities
#
# When a nation has (category, level), the listed (category, level) combos
# become unavailable.  Checked symmetrically: both sides are listed.
# =============================================================================

POLICY_BANS = {
    ("war_policy", 0): [
        ("military_spending", 4),
        ("rationing", 2),
        ("military_service", 3),
        ("military_service", 4),
        ("military_service", 5),
        ("military_service", 6),
    ],
    ("military_spending", 4): [
        ("war_policy", 0),
        ("war_policy", 1),
    ],
    ("economic_system", 3): [
        ("banking_policy", 3),
        ("labour_policy", 3),
        ("property_rights", 2),
    ],
    ("economic_system", 0): [
        ("banking_policy", 1),
        ("property_rights", 0),
    ],
    ("trade_policy", 3): [
        ("alliance_policy", 3),
    ],
    ("propaganda_policy", 3): [
        ("government_transparency", 2),
    ],
    ("government_transparency", 2): [
        ("propaganda_policy", 3),
        ("intelligence_policy", 3),
    ],
    ("military_service", 0): [
        ("military_spending", 3),
        ("military_spending", 4),
        ("rationing", 2),
    ],
    ("religion_policy", 0): [
        ("religion_policy", 3),
        ("religion_policy", 4),
    ],
    ("religion_policy", 4): [
        ("religion_policy", 0),
        ("religion_policy", 1),
        ("research_policy", 2),
    ],
    ("environmental_policy", 3): [
        ("industrial_policy", 2),
        ("resource_extraction", 2),
        ("energy_policy", 1),
    ],
    ("environmental_policy", 0): [
        ("resource_extraction", 3),
    ],
}


# =============================================================================
# BUILDING_POLICY_REQUIREMENTS — buildings that need specific policy levels
#
# Format: building_type -> list of (policy_category, min_level_index) tuples.
# ALL requirements must be met (AND logic).
# =============================================================================

BUILDING_POLICY_REQUIREMENTS = {
    "stock_exchange": [("banking_policy", 2)],
    "bank": [("banking_policy", 1)],
    "intelligence_agency": [("intelligence_policy", 2)],
    "army_base": [("military_service", 1)],
    "naval_base": [("military_service", 1)],
    "air_base": [("military_service", 1)],
    "weapons_factory": [("military_spending", 2)],
    "industrial_complex": [("manufacturing_policy", 2)],
    "electronics_factory": [("manufacturing_policy", 2)],
    "precision_workshop": [("manufacturing_policy", 1)],
    "research_institute": [("research_policy", 2)],
    "university": [("education_policy", 3)],
    "public_school": [("education_policy", 2)],
    "broadcasting_station": [("press_freedom", 1)],
    "advanced_refinery": [("energy_policy", 1)],
    "biofuel_plant": [("energy_policy", 2)],
    "wind_farm": [("environmental_policy", 1)],
    "solar_array": [("environmental_policy", 1)],
    "hydroelectric_dam": [("environmental_policy", 1)],
    "hospital": [("healthcare_policy", 1)],
    "sanitation_works": [("healthcare_policy", 1)],
    "holy_site": [("religion_policy", 3)],
    "infrastructure_bureau": [("infrastructure_policy", 2)],
    "airport": [("infrastructure_policy", 2)],
    "air_cargo_terminal": [("infrastructure_policy", 2)],
    "railroad": [("infrastructure_policy", 2)],
    "train_depot": [("infrastructure_policy", 2)],
    "train_station": [("infrastructure_policy", 2)],
    "train_cargo_terminal": [("infrastructure_policy", 2)],
}


# =============================================================================
# BUILDING_POLICY_BANS — buildings blocked by specific policy levels
#
# Format: building_type -> list of (policy_category, exact_level) tuples.
# ANY match blocks construction.
# =============================================================================

BUILDING_POLICY_BANS = {
    "stock_exchange": [("economic_system", 3), ("economic_system", 4)],
    "bank": [("economic_system", 4)],
    "holy_site": [("religion_policy", 0)],
    "church": [("religion_policy", 0)],
    "madrasa": [("religion_policy", 0)],
    "arms_factory": [("war_policy", 0)],
    "weapons_factory": [("war_policy", 0)],
    "army_base": [("military_service", 0)],
    "naval_base": [("military_service", 0)],
    "air_base": [("military_service", 0)],
    "oil_well": [("environmental_policy", 3)],
    "refinery": [("environmental_policy", 3)],
    "advanced_refinery": [("environmental_policy", 3)],
}


# =============================================================================
# UNIT_POLICY_REQUIREMENTS — unit types requiring specific policy levels
#
# Format: unit_type -> list of (policy_category, min_level) tuples.
# ALL requirements must be met.
# =============================================================================

UNIT_POLICY_REQUIREMENTS = {
    "militia": [],
    "infantry": [("military_spending", 1)],
    "motorized": [("military_spending", 2), ("manufacturing_policy", 2)],
    "armored": [("military_spending", 3), ("manufacturing_policy", 2), ("industrial_policy", 2)],
    "artillery": [("military_spending", 2), ("manufacturing_policy", 2)],
    "patrol_boat": [("military_spending", 1)],
    "frigate": [("military_spending", 3)],
    "transport": [("military_spending", 2)],
    "scout_plane": [("military_spending", 2)],
    "fighter": [("military_spending", 3), ("manufacturing_policy", 2)],
    "bomber": [("military_spending", 4), ("manufacturing_policy", 2), ("industrial_policy", 2)],
}


# =============================================================================
# UNIT_POLICY_BANS — unit types blocked by specific policy levels
#
# Format: unit_type -> list of (policy_category, exact_level) tuples.
# ANY match blocks training.
# =============================================================================

UNIT_POLICY_BANS = {
    "militia": [("military_service", 0)],
    "infantry": [("military_service", 0), ("war_policy", 0)],
    "motorized": [("military_service", 0), ("war_policy", 0)],
    "armored": [("military_service", 0), ("war_policy", 0)],
    "artillery": [("military_service", 0), ("war_policy", 0)],
    "patrol_boat": [("military_service", 0)],
    "frigate": [("military_service", 0), ("war_policy", 0)],
    "transport": [("military_service", 0)],
    "scout_plane": [("military_service", 0)],
    "fighter": [("military_service", 0), ("war_policy", 0)],
    "bomber": [("military_service", 0), ("war_policy", 0)],
}
