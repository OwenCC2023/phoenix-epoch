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
