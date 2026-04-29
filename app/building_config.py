BUILDINGS = {
    "command_center": {
        "category": "infrastructure",
        "max_per_city": 1,
        "starting_level": 1,
        "effects": {
            "unlock_limits": True
        },
        "base_cost": {
            "money": 500,
            "food": 200,
            "oil": 100,
            "tech": 50
        },
        "growth_cost": 1.8,
        "base_time": 60
    },

    "farm": {
        "category": "economy",
        "max_per_city": 10,
        "starting_level": 0,
        "production": {"food": 2},
        "base_cost": {"money": 100},
        "growth_cost": 1.5,
        "base_time": 20
    },

    "bank": {
        "category": "economy",
        "max_per_city": 5,
        "starting_level": 0,
        "production": {"money": 2},
        "base_cost": {"money": 200, "food": 100},
        "growth_cost": 1.55,
        "base_time": 25
    },

    "oil_rig": {
        "category": "economy",
        "max_per_city": 6,
        "starting_level": 0,
        "production": {"oil": 1},
        "base_cost": {"money": 200, "food": 150},
        "growth_cost": 1.6,
        "base_time": 30
    },

    "research_lab": {
        "category": "economy",
        "max_per_city": 2,
        "starting_level": 0,
        "production": {"tech": 1},
        "base_cost": {"money": 200, "food": 200, "oil": 100},
        "growth_cost": 1.7,
        "base_time": 40
    },

    "barracks": {
        "category": "military",
        "max_per_city": 3,
        "starting_level": 0,
        "unlocks": "infantry",
        "base_cost": {"money": 200, "food": 50},
        "growth_cost": 1.7,
        "base_time": 35
    },

    "armory": {
        "category": "military",
        "max_per_city": 2,
        "starting_level": 0,
        "unlocks": "vehicles",
        "base_cost": {"money": 1000, "food": 500, "oil": 200, "tech": 200},
        "growth_cost": 1.75,
        "base_time": 45
    },

    "wall_tower": {
        "category": "defense",
        "max_per_city": 1,
        "starting_level": 0,
        "effects": {"defense_bonus": 0.1},
        "base_cost": {"money": 250, "oil": 100, "tech": 75},
        "growth_cost": 1.9,
        "base_time": 60,
        "effects": {
            "defense_bonus": 0.1
        }
    },

    "houses": {
        "category": "population",
        "max_per_city": 10,
        "starting_level": 0,
        "effects": {"population_growth": 1},
        "base_cost": {"money": 80},
        "growth_cost": 1.45,
        "base_time": 15
    },

    "airfield": {
        "category": "military",
        "max_per_city": 2,
        "starting_level": 0,
        "unlocks": "air_units",
        "base_cost": {"money": 1000, "food": 500, "oil": 200, "tech": 200},
        "growth_cost": 1.75,
        "base_time": 70
    },

    "naval_base": {
        "category": "military",
        "max_per_city": 2,
        "starting_level": 0,
        "unlocks": "navy_units",
        "base_cost": {"money": 1000, "food": 500, "oil": 200, "tech": 200},
        "growth_cost": 1.75,
        "base_time": 70
    },

    "warehouse": {
        "category": "utility",
        "max_per_city": 5,
        "starting_level": 0,
        "effects": {"storage_bonus": 1000},
        "base_cost": {"money": 100, "food": 100},
        "growth_cost": 1.5,
        "base_time": 20
    }
}