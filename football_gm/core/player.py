"""Player model — the core entity of the simulation."""

import random
from football_gm.data.positions import POSITION_ATTRIBUTE_WEIGHTS, POSITION_AGE_PROFILES


class Player:
    """Represents a football player with attributes, ratings, and career state."""

    _next_id = 1

    def __init__(self, first_name, last_name, position, age, attributes=None,
                 potential=None, player_id=None):
        if player_id is not None:
            self.id = player_id
        else:
            self.id = Player._next_id
            Player._next_id += 1

        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.age = age

        # Core attributes dict — values 1-99
        self.attributes = attributes or {}

        # Hidden potential ceiling (1-99) — determines how high a player can develop
        self.potential = potential or 50

        # Career tracking
        self.experience = 0  # years in league
        self.team_abbr = None  # None = free agent
        self.contract = None  # Contract object

        # Season state
        self.injured = False
        self.injury_weeks_remaining = 0
        self.injury_type = None

        # Career stats (accumulated across seasons)
        self.career_stats = {}
        self.season_stats = {}

        # Morale and intangibles
        self.morale = 70  # 1-100
        self.durability = self.attributes.get("injury_resistance", 50)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def overall_rating(self):
        """Calculate overall rating based on position-specific attribute weights."""
        weights = POSITION_ATTRIBUTE_WEIGHTS.get(self.position, {})
        if not weights:
            return 50

        total_weight = 0
        weighted_sum = 0
        for attr, weight in weights.items():
            if attr in self.attributes:
                weighted_sum += self.attributes[attr] * weight
                total_weight += weight

        if total_weight == 0:
            return 50
        return round(weighted_sum / total_weight)

    @property
    def is_free_agent(self):
        return self.team_abbr is None

    @property
    def age_profile(self):
        return POSITION_AGE_PROFILES.get(self.position, {})

    @property
    def is_pre_peak(self):
        profile = self.age_profile
        return self.age < profile.get("peak_start", 26)

    @property
    def is_in_peak(self):
        profile = self.age_profile
        return profile.get("peak_start", 26) <= self.age <= profile.get("peak_end", 30)

    @property
    def is_declining(self):
        profile = self.age_profile
        return self.age > profile.get("peak_end", 30)

    def develop(self):
        """Apply one year of development/regression based on age and potential."""
        profile = self.age_profile

        for attr_name, value in self.attributes.items():
            if attr_name == "injury_resistance":
                continue  # durability doesn't change much

            if self.is_pre_peak:
                # Young players grow toward their potential
                room_to_grow = self.potential - value
                if room_to_grow > 0:
                    growth = random.gauss(room_to_grow * 0.15, 2.0)
                    growth = max(0, growth)
                else:
                    growth = random.gauss(-0.5, 1.0)
                self.attributes[attr_name] = max(1, min(99, round(value + growth)))

            elif self.is_in_peak:
                # Peak years — small random fluctuations
                change = random.gauss(0.3, 1.5)
                self.attributes[attr_name] = max(1, min(99, round(value + change)))

            elif self.is_declining:
                # Post-peak — decline accelerates with age
                decline_rate = profile.get("decline_rate", 0.05)
                years_past_peak = self.age - profile.get("peak_end", 30)
                decline = random.gauss(decline_rate * value * (1 + years_past_peak * 0.1), 1.5)
                decline = max(0, decline)
                self.attributes[attr_name] = max(1, min(99, round(value - decline)))

        self.age += 1
        self.experience += 1

    def apply_injury(self, injury_type, weeks):
        """Put the player on the injury list."""
        self.injured = True
        self.injury_type = injury_type
        self.injury_weeks_remaining = weeks

    def heal_week(self):
        """Advance one week of injury recovery."""
        if self.injured:
            self.injury_weeks_remaining -= 1
            if self.injury_weeks_remaining <= 0:
                self.injured = False
                self.injury_type = None
                self.injury_weeks_remaining = 0

    def retire_check(self):
        """Determine if the player should retire. Returns True if retiring."""
        if self.age < 28:
            return False

        # Base retirement probability increases sharply with age
        base_prob = 0.0
        if self.age >= 38:
            base_prob = 0.60
        elif self.age >= 36:
            base_prob = 0.30
        elif self.age >= 34:
            base_prob = 0.15
        elif self.age >= 32:
            base_prob = 0.06
        elif self.age >= 30:
            base_prob = 0.03
        elif self.age >= 28:
            base_prob = 0.01

        # Low overall = more likely to retire
        ovr = self.overall_rating
        if ovr < 55:
            base_prob += 0.15
        elif ovr < 65:
            base_prob += 0.05

        # Free agents more likely to retire
        if self.is_free_agent:
            base_prob += 0.10

        return random.random() < base_prob

    def __repr__(self):
        return (f"Player({self.full_name}, {self.position}, "
                f"Age:{self.age}, OVR:{self.overall_rating})")
