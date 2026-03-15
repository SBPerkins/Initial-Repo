"""Contract and salary cap models."""


class Contract:
    """Represents a player's contract with full NFL salary cap mechanics."""

    def __init__(self, player_id, team_abbr, total_value, years, signing_bonus=0,
                 guaranteed_money=0, is_rookie_deal=False):
        self.player_id = player_id
        self.team_abbr = team_abbr
        self.total_value = total_value  # total contract value
        self.years = years  # total years
        self.years_remaining = years
        self.signing_bonus = signing_bonus
        self.guaranteed_money = guaranteed_money
        self.is_rookie_deal = is_rookie_deal

        # Build year-by-year salary breakdown
        # Signing bonus is prorated evenly across all years
        self.bonus_per_year = signing_bonus / years if years > 0 else 0

        # Base salaries escalate over the life of the contract
        remaining_value = total_value - signing_bonus
        self.yearly_salaries = self._build_salary_schedule(remaining_value, years)

        # Track which year of the contract we're in (0-indexed)
        self.current_year = 0

    def _build_salary_schedule(self, base_total, years):
        """Create escalating yearly base salaries."""
        if years <= 0:
            return []
        if years == 1:
            return [base_total]

        # Salaries escalate ~10-15% per year (typical NFL structure)
        escalation = 1.12
        # Calculate first year salary so total sums correctly
        # sum = s * (1 + r + r^2 + ... + r^(n-1)) = s * (r^n - 1) / (r - 1)
        geometric_sum = (escalation ** years - 1) / (escalation - 1)
        first_year = base_total / geometric_sum

        salaries = []
        for i in range(years):
            salaries.append(round(first_year * (escalation ** i)))
        return salaries

    @property
    def current_base_salary(self):
        """This year's base salary."""
        if self.current_year < len(self.yearly_salaries):
            return self.yearly_salaries[self.current_year]
        return 0

    @property
    def current_cap_hit(self):
        """This year's total cap hit = base salary + prorated bonus."""
        return round(self.current_base_salary + self.bonus_per_year)

    @property
    def dead_cap_if_cut(self):
        """Dead cap penalty if the player is cut right now.
        Remaining prorated signing bonus accelerates onto this year's cap."""
        remaining_bonus_years = self.years_remaining
        return round(self.bonus_per_year * remaining_bonus_years)

    @property
    def cap_savings_if_cut(self):
        """Cap space saved by cutting the player."""
        return self.current_cap_hit - self.dead_cap_if_cut

    @property
    def is_expiring(self):
        return self.years_remaining <= 1

    @property
    def average_annual_value(self):
        """AAV — the number fans and media talk about."""
        if self.years == 0:
            return 0
        return round(self.total_value / self.years)

    def advance_year(self):
        """Move to the next contract year. Returns True if contract has expired."""
        self.current_year += 1
        self.years_remaining -= 1
        return self.years_remaining <= 0

    def restructure(self):
        """Convert base salary to signing bonus to create cap space this year.
        Typical NFL restructure: convert most of base salary to bonus,
        spreading the cap hit over remaining years."""
        if self.years_remaining <= 1:
            return 0  # can't restructure expiring deals

        base = self.current_base_salary
        # Convert 80% of base salary to bonus (keep minimum base ~$1.2M)
        convertible = max(0, base - 1_200_000)
        converted = round(convertible * 0.80)

        if converted <= 0:
            return 0

        # Reduce this year's base salary
        self.yearly_salaries[self.current_year] -= converted

        # Add converted amount as new prorated bonus across remaining years
        new_proration = converted / self.years_remaining
        self.bonus_per_year += new_proration

        return converted  # cap savings this year

    def __repr__(self):
        return (f"Contract(${self.total_value:,}, {self.years}yr, "
                f"Cap:{self.current_cap_hit:,}, Yr {self.current_year + 1}/{self.years})")


# NFL salary cap constants (in dollars)
SALARY_CAP = 255_000_000  # ~2024 cap, can be adjusted per season
CAP_FLOOR = round(SALARY_CAP * 0.89)  # teams must spend at least 89% of cap
VETERAN_MINIMUM = 1_125_000
ROOKIE_MINIMUM = 795_000
PRACTICE_SQUAD_SALARY = 12_000  # per week
