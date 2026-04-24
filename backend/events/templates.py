"""Pre-built event templates for GMs to use."""

EVENT_TEMPLATES = {
    "drought": {
        "title": "Severe Drought",
        "description": "A devastating drought has struck the land, reducing food production across all affected regions.",
        "scope": "global",
        "effects": {
            "modifiers": [
                {"category": "economy", "target": "food", "modifier_type": "percentage", "value": -0.25, "duration": 3}
            ]
        },
    },
    "gold_rush": {
        "title": "Resource Discovery",
        "description": "Prospectors have discovered rich mineral deposits, boosting material and kapital production.",
        "scope": "targeted",
        "effects": {
            "modifiers": [
                {"category": "economy", "target": "materials", "modifier_type": "percentage", "value": 0.20, "duration": 5},
                {"category": "economy", "target": "kapital", "modifier_type": "percentage", "value": 0.10, "duration": 5},
            ]
        },
    },
    "plague": {
        "title": "Plague Outbreak",
        "description": "A virulent disease is spreading through the population, threatening growth and stability.",
        "scope": "global",
        "effects": {
            "modifiers": [
                {"category": "growth", "target": "growth", "modifier_type": "percentage", "value": -0.05, "duration": 4},
                {"category": "stability", "target": "stability", "modifier_type": "flat", "value": -10, "duration": 4},
            ]
        },
    },
    "trade_boom": {
        "title": "Trade Route Opened",
        "description": "New trade routes have been established, boosting commerce for connected nations.",
        "scope": "targeted",
        "effects": {
            "modifiers": [
                {"category": "economy", "target": "kapital", "modifier_type": "percentage", "value": 0.25, "duration": 6},
            ]
        },
    },
    "refugee_influx": {
        "title": "Refugee Influx",
        "description": "A wave of refugees arrives seeking shelter, boosting population but straining resources.",
        "scope": "targeted",
        "effects": {
            "population_change": 500,
            "modifiers": [
                {"category": "stability", "target": "stability", "modifier_type": "flat", "value": -5, "duration": 2},
            ]
        },
    },
    "tech_breakthrough": {
        "title": "Technological Breakthrough",
        "description": "Researchers have made a significant discovery, boosting research and energy output.",
        "scope": "targeted",
        "effects": {
            "modifiers": [
                {"category": "economy", "target": "research", "modifier_type": "percentage", "value": 0.30, "duration": 4},
                {"category": "economy", "target": "energy", "modifier_type": "percentage", "value": 0.10, "duration": 4},
            ]
        },
    },
    "civil_unrest": {
        "title": "Civil Unrest",
        "description": "The population is growing restless. Stability plummets as protests erupt.",
        "scope": "targeted",
        "effects": {
            "modifiers": [
                {"category": "stability", "target": "stability", "modifier_type": "flat", "value": -15, "duration": 2},
                {"category": "economy", "target": "kapital", "modifier_type": "percentage", "value": -0.10, "duration": 2},
            ]
        },
    },
    "bountiful_harvest": {
        "title": "Bountiful Harvest",
        "description": "Perfect weather conditions have led to an exceptional harvest season.",
        "scope": "global",
        "effects": {
            "modifiers": [
                {"category": "economy", "target": "food", "modifier_type": "percentage", "value": 0.30, "duration": 2},
            ]
        },
    },
}
