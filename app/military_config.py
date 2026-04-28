MILITARY = {
    "soldier": {
        "type": "infantry",
        "attack": 10,
        "defense": 12,
        "hp": 100,
        "speed": 1.0,
        "cost": {
            "money": 100,
            "food": 50
        },
        "trained_in": "barracks",
        "training_time": 10
    },

    "tank": {
        "type": "vehicle",
        "attack": 18,
        "defense": 10,
        "hp": 150,
        "speed": 1.5,
        "cost": {
            "money": 200,
            "oil": 75
        },
        "trained_in": "armory",
        "training_time": 20
    },

    "artillery": {
        "type": "artillery",
        "attack": 30,
        "defense": 5,
        "hp": 80,
        "speed": 0.7,
        "cost": {
            "money": 250,
            "oil": 100,
            "tech": 50
        },
        "trained_in": "armory",
        "training_time": 30
    }
}