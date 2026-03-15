"""Player generation — creates realistic players with position-appropriate attributes."""

import random
from football_gm.core.player import Player
from football_gm.data.positions import POSITION_ATTRIBUTE_WEIGHTS, POSITION_AGE_PROFILES
from football_gm.data.names import FIRST_NAMES, LAST_NAMES


def generate_attributes(position, talent_level="average"):
    """Generate a full set of attributes for a given position.

    talent_level controls the baseline:
        'elite'   — 75-95 in key attributes
        'good'    — 65-85
        'average' — 50-75
        'below'   — 35-60
        'poor'    — 25-50
    """
    ranges = {
        "elite": (75, 95),
        "good": (65, 85),
        "average": (50, 75),
        "below": (35, 60),
        "poor": (25, 50),
    }
    base_low, base_high = ranges.get(talent_level, (50, 75))

    weights = POSITION_ATTRIBUTE_WEIGHTS.get(position, {})
    attributes = {}

    # All possible attributes across all positions
    all_attrs = set()
    for pos_weights in POSITION_ATTRIBUTE_WEIGHTS.values():
        all_attrs.update(pos_weights.keys())

    for attr in all_attrs:
        weight = weights.get(attr, 0.0)

        if weight >= 0.8:
            # Primary attribute — higher range
            val = random.randint(base_low + 5, min(99, base_high + 5))
        elif weight >= 0.5:
            # Secondary attribute — normal range
            val = random.randint(base_low, base_high)
        elif weight > 0:
            # Tertiary attribute — slightly lower
            val = random.randint(max(1, base_low - 10), base_high - 5)
        else:
            # Not relevant to position — much lower
            val = random.randint(max(1, base_low - 25), max(10, base_high - 25))

        # Add some random variance
        val += random.randint(-5, 5)
        attributes[attr] = max(1, min(99, val))

    return attributes


def generate_potential(talent_level="average"):
    """Generate a potential ceiling based on talent level."""
    potential_ranges = {
        "elite": (85, 99),
        "good": (72, 90),
        "average": (55, 78),
        "below": (40, 65),
        "poor": (25, 50),
    }
    low, high = potential_ranges.get(talent_level, (55, 78))
    return random.randint(low, high)


def generate_player(position, age=None, talent_level=None):
    """Generate a single random player."""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)

    if age is None:
        profile = POSITION_AGE_PROFILES.get(position, {})
        min_age, max_age = profile.get("draft_age", (21, 23))
        age = random.randint(min_age, max_age + 5)  # spread ages across the league

    if talent_level is None:
        # Distribution: ~5% elite, 15% good, 50% average, 20% below, 10% poor
        roll = random.random()
        if roll < 0.05:
            talent_level = "elite"
        elif roll < 0.20:
            talent_level = "good"
        elif roll < 0.70:
            talent_level = "average"
        elif roll < 0.90:
            talent_level = "below"
        else:
            talent_level = "poor"

    attributes = generate_attributes(position, talent_level)
    potential = generate_potential(talent_level)

    player = Player(
        first_name=first,
        last_name=last,
        position=position,
        age=age,
        attributes=attributes,
        potential=potential,
    )

    # Adjust attributes for age — older players should have already developed/declined
    profile = POSITION_AGE_PROFILES.get(position, {})
    peak_start = profile.get("peak_start", 26)

    if age > peak_start + 2:
        # Apply some simulated development then decline
        years_past_peak = age - profile.get("peak_end", 30)
        if years_past_peak > 0:
            decline_rate = profile.get("decline_rate", 0.05)
            for attr in player.attributes:
                if attr != "injury_resistance":
                    decline = round(decline_rate * player.attributes[attr] * years_past_peak * 0.5)
                    player.attributes[attr] = max(1, player.attributes[attr] - decline)

    player.experience = max(0, age - random.randint(21, 23))
    return player


def generate_roster(team):
    """Fill a team's roster with generated players to reach 53 man roster."""
    from football_gm.data.positions import ROSTER_REQUIREMENTS

    for position, count in ROSTER_REQUIREMENTS.items():
        for i in range(count):
            # Starters tend to be better
            if i == 0:
                talent = random.choice(["elite", "good", "good", "average"])
            elif i == 1:
                talent = random.choice(["good", "average", "average", "below"])
            else:
                talent = random.choice(["average", "below", "below", "poor"])

            player = generate_player(position, talent_level=talent)
            team.add_player(player)


def generate_draft_class(size=250):
    """Generate a class of draft-eligible prospects."""
    from football_gm.data.positions import POSITIONS

    # Position distribution roughly matching real NFL drafts
    position_weights = {
        "QB": 8, "RB": 15, "FB": 3, "WR": 25, "TE": 10,
        "LT": 10, "LG": 10, "C": 8, "RG": 10, "RT": 10,
        "DE": 18, "DT": 14, "OLB": 16, "ILB": 12,
        "CB": 22, "FS": 10, "SS": 10,
        "K": 4, "P": 4,
    }

    # Build weighted position list
    position_pool = []
    for pos, weight in position_weights.items():
        position_pool.extend([pos] * weight)

    prospects = []
    for _ in range(size):
        position = random.choice(position_pool)
        profile = POSITION_AGE_PROFILES.get(position, {})
        min_age, max_age = profile.get("draft_age", (21, 23))
        age = random.randint(min_age, max_age)

        # Draft classes are more weighted toward average/below with some gems
        roll = random.random()
        if roll < 0.03:
            talent = "elite"
        elif roll < 0.12:
            talent = "good"
        elif roll < 0.50:
            talent = "average"
        elif roll < 0.80:
            talent = "below"
        else:
            talent = "poor"

        prospect = generate_player(position, age=age, talent_level=talent)
        prospect.experience = 0
        prospects.append(prospect)

    # Sort by overall rating (simulates draft board)
    prospects.sort(key=lambda p: p.overall_rating, reverse=True)
    return prospects
