"""Position definitions, attribute weights, and roster requirements."""


# All positions in the game
POSITIONS = [
    "QB", "RB", "FB", "WR", "TE", "LT", "LG", "C", "RG", "RT",
    "DE", "DT", "OLB", "ILB", "CB", "FS", "SS",
    "K", "P"
]

OFFENSE_POSITIONS = ["QB", "RB", "FB", "WR", "TE", "LT", "LG", "C", "RG", "RT"]
DEFENSE_POSITIONS = ["DE", "DT", "OLB", "ILB", "CB", "FS", "SS"]
SPECIAL_TEAMS_POSITIONS = ["K", "P"]

# Attributes that matter for each position and their relative importance (0-1)
# Higher weight = more important for that position's overall rating
POSITION_ATTRIBUTE_WEIGHTS = {
    "QB": {
        "throw_power": 0.85, "throw_accuracy_short": 0.90, "throw_accuracy_mid": 0.90,
        "throw_accuracy_deep": 0.80, "throw_on_run": 0.60, "decision_making": 0.95,
        "pocket_awareness": 0.85, "speed": 0.30, "agility": 0.35,
        "strength": 0.20, "awareness": 0.90, "injury_resistance": 0.50,
        "stamina": 0.40, "leadership": 0.70, "clutch": 0.65,
    },
    "RB": {
        "speed": 0.85, "acceleration": 0.90, "agility": 0.90,
        "elusiveness": 0.85, "ball_carrier_vision": 0.90, "break_tackle": 0.75,
        "carrying": 0.80, "catching": 0.50, "pass_block": 0.30,
        "strength": 0.45, "stamina": 0.70, "awareness": 0.60,
        "injury_resistance": 0.55, "clutch": 0.40,
    },
    "FB": {
        "run_block": 0.90, "pass_block": 0.70, "strength": 0.85,
        "speed": 0.30, "carrying": 0.40, "catching": 0.45,
        "awareness": 0.60, "stamina": 0.50, "injury_resistance": 0.50,
        "break_tackle": 0.40, "acceleration": 0.35,
    },
    "WR": {
        "speed": 0.85, "acceleration": 0.80, "agility": 0.75,
        "catching": 0.95, "catch_in_traffic": 0.80, "spectacular_catch": 0.60,
        "route_running": 0.90, "release": 0.75, "elusiveness": 0.55,
        "awareness": 0.65, "stamina": 0.40, "injury_resistance": 0.45,
        "clutch": 0.50, "jumping": 0.50,
    },
    "TE": {
        "catching": 0.80, "catch_in_traffic": 0.75, "route_running": 0.65,
        "run_block": 0.70, "pass_block": 0.55, "speed": 0.55,
        "strength": 0.65, "awareness": 0.60, "stamina": 0.45,
        "injury_resistance": 0.50, "break_tackle": 0.40, "acceleration": 0.50,
    },
    "LT": {
        "pass_block": 0.95, "run_block": 0.80, "strength": 0.85,
        "awareness": 0.75, "agility": 0.50, "stamina": 0.45,
        "injury_resistance": 0.55, "acceleration": 0.25,
    },
    "LG": {
        "run_block": 0.90, "pass_block": 0.80, "strength": 0.90,
        "awareness": 0.70, "agility": 0.40, "stamina": 0.45,
        "injury_resistance": 0.55, "acceleration": 0.20,
    },
    "C": {
        "run_block": 0.85, "pass_block": 0.85, "strength": 0.85,
        "awareness": 0.80, "agility": 0.35, "stamina": 0.45,
        "injury_resistance": 0.55, "leadership": 0.40,
    },
    "RG": {
        "run_block": 0.90, "pass_block": 0.80, "strength": 0.90,
        "awareness": 0.70, "agility": 0.40, "stamina": 0.45,
        "injury_resistance": 0.55, "acceleration": 0.20,
    },
    "RT": {
        "pass_block": 0.85, "run_block": 0.85, "strength": 0.85,
        "awareness": 0.70, "agility": 0.45, "stamina": 0.45,
        "injury_resistance": 0.55, "acceleration": 0.25,
    },
    "DE": {
        "pass_rush": 0.95, "block_shedding": 0.80, "speed": 0.70,
        "acceleration": 0.75, "strength": 0.75, "tackle": 0.70,
        "awareness": 0.65, "stamina": 0.55, "agility": 0.50,
        "injury_resistance": 0.50, "pursuit": 0.70,
    },
    "DT": {
        "block_shedding": 0.90, "strength": 0.90, "pass_rush": 0.75,
        "tackle": 0.80, "awareness": 0.65, "stamina": 0.50,
        "pursuit": 0.55, "agility": 0.30, "injury_resistance": 0.50,
    },
    "OLB": {
        "tackle": 0.85, "pass_rush": 0.65, "speed": 0.70,
        "zone_coverage": 0.60, "man_coverage": 0.50, "block_shedding": 0.60,
        "pursuit": 0.80, "awareness": 0.70, "agility": 0.55,
        "strength": 0.55, "stamina": 0.50, "injury_resistance": 0.50,
        "acceleration": 0.60,
    },
    "ILB": {
        "tackle": 0.90, "zone_coverage": 0.70, "awareness": 0.85,
        "pursuit": 0.85, "speed": 0.60, "block_shedding": 0.65,
        "man_coverage": 0.45, "strength": 0.55, "agility": 0.50,
        "stamina": 0.50, "injury_resistance": 0.50, "leadership": 0.45,
        "acceleration": 0.55,
    },
    "CB": {
        "man_coverage": 0.95, "zone_coverage": 0.85, "speed": 0.85,
        "acceleration": 0.80, "agility": 0.75, "awareness": 0.75,
        "catching": 0.55, "tackle": 0.35, "jumping": 0.55,
        "stamina": 0.45, "injury_resistance": 0.45, "press": 0.70,
    },
    "FS": {
        "zone_coverage": 0.90, "speed": 0.80, "awareness": 0.85,
        "catching": 0.60, "tackle": 0.55, "man_coverage": 0.60,
        "pursuit": 0.65, "agility": 0.55, "acceleration": 0.65,
        "jumping": 0.45, "stamina": 0.45, "injury_resistance": 0.45,
    },
    "SS": {
        "tackle": 0.75, "zone_coverage": 0.75, "man_coverage": 0.55,
        "speed": 0.65, "strength": 0.55, "awareness": 0.75,
        "pursuit": 0.70, "catching": 0.45, "block_shedding": 0.40,
        "acceleration": 0.60, "stamina": 0.45, "injury_resistance": 0.45,
    },
    "K": {
        "kick_power": 0.90, "kick_accuracy": 0.95, "clutch": 0.70,
        "awareness": 0.30, "stamina": 0.20, "injury_resistance": 0.30,
    },
    "P": {
        "kick_power": 0.90, "kick_accuracy": 0.85, "awareness": 0.35,
        "stamina": 0.20, "injury_resistance": 0.30,
    },
}

# How many of each position a typical 53-man roster needs
ROSTER_REQUIREMENTS = {
    "QB": 3, "RB": 4, "FB": 1, "WR": 6, "TE": 3,
    "LT": 2, "LG": 2, "C": 2, "RG": 2, "RT": 2,
    "DE": 4, "DT": 3, "OLB": 4, "ILB": 3,
    "CB": 5, "FS": 2, "SS": 2,
    "K": 1, "P": 1,
}

# Age ranges and peak years by position
POSITION_AGE_PROFILES = {
    "QB":  {"draft_age": (21, 24), "peak_start": 27, "peak_end": 34, "decline_rate": 0.03},
    "RB":  {"draft_age": (21, 23), "peak_start": 23, "peak_end": 27, "decline_rate": 0.07},
    "FB":  {"draft_age": (22, 24), "peak_start": 25, "peak_end": 31, "decline_rate": 0.04},
    "WR":  {"draft_age": (21, 23), "peak_start": 25, "peak_end": 30, "decline_rate": 0.05},
    "TE":  {"draft_age": (21, 24), "peak_start": 25, "peak_end": 31, "decline_rate": 0.04},
    "LT":  {"draft_age": (21, 24), "peak_start": 26, "peak_end": 33, "decline_rate": 0.035},
    "LG":  {"draft_age": (21, 24), "peak_start": 26, "peak_end": 33, "decline_rate": 0.035},
    "C":   {"draft_age": (21, 24), "peak_start": 26, "peak_end": 33, "decline_rate": 0.035},
    "RG":  {"draft_age": (21, 24), "peak_start": 26, "peak_end": 33, "decline_rate": 0.035},
    "RT":  {"draft_age": (21, 24), "peak_start": 26, "peak_end": 33, "decline_rate": 0.035},
    "DE":  {"draft_age": (21, 23), "peak_start": 25, "peak_end": 30, "decline_rate": 0.05},
    "DT":  {"draft_age": (21, 24), "peak_start": 25, "peak_end": 31, "decline_rate": 0.04},
    "OLB": {"draft_age": (21, 23), "peak_start": 25, "peak_end": 30, "decline_rate": 0.05},
    "ILB": {"draft_age": (21, 23), "peak_start": 25, "peak_end": 30, "decline_rate": 0.05},
    "CB":  {"draft_age": (21, 23), "peak_start": 24, "peak_end": 29, "decline_rate": 0.06},
    "FS":  {"draft_age": (21, 23), "peak_start": 25, "peak_end": 30, "decline_rate": 0.05},
    "SS":  {"draft_age": (21, 23), "peak_start": 25, "peak_end": 30, "decline_rate": 0.05},
    "K":   {"draft_age": (22, 25), "peak_start": 26, "peak_end": 37, "decline_rate": 0.02},
    "P":   {"draft_age": (22, 25), "peak_start": 26, "peak_end": 36, "decline_rate": 0.02},
}
