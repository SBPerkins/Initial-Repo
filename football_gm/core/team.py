"""Team model — roster management, cap tracking, and team identity."""

from football_gm.core.contract import SALARY_CAP


class Team:
    """Represents an NFL franchise."""

    def __init__(self, city, name, abbr, conference, division):
        self.city = city
        self.name = name
        self.abbr = abbr
        self.conference = conference
        self.division = division

        # Roster
        self.players = []  # list of Player objects

        # Season record
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.points_for = 0
        self.points_against = 0

        # Salary cap
        self.salary_cap = SALARY_CAP
        self.dead_cap = 0  # accumulated dead money
        self.cap_carryover = 0  # unused cap from previous year

        # Draft picks: list of {"year": int, "round": int, "original_team": str}
        self.draft_picks = []

        # Coaching staff (simplified for now)
        self.head_coach_quality = 50  # 1-99
        self.offensive_scheme = "balanced"  # balanced, pass_heavy, run_heavy
        self.defensive_scheme = "balanced"  # balanced, aggressive, conservative

        # Franchise history
        self.championships = 0
        self.playoff_appearances = 0

    @property
    def full_name(self):
        return f"{self.city} {self.name}"

    @property
    def record(self):
        if self.ties > 0:
            return f"{self.wins}-{self.losses}-{self.ties}"
        return f"{self.wins}-{self.losses}"

    @property
    def win_pct(self):
        games = self.wins + self.losses + self.ties
        if games == 0:
            return 0.0
        return (self.wins + self.ties * 0.5) / games

    @property
    def point_differential(self):
        return self.points_for - self.points_against

    @property
    def roster_size(self):
        return len(self.players)

    @property
    def total_cap_used(self):
        """Total salary cap space currently committed."""
        total = self.dead_cap
        for player in self.players:
            if player.contract:
                total += player.contract.current_cap_hit
        return total

    @property
    def cap_space(self):
        """Available salary cap room."""
        effective_cap = self.salary_cap + self.cap_carryover
        return effective_cap - self.total_cap_used

    @property
    def overall_rating(self):
        """Team overall based on average of player ratings."""
        if not self.players:
            return 0
        return round(sum(p.overall_rating for p in self.players) / len(self.players))

    def add_player(self, player):
        """Add a player to the roster."""
        player.team_abbr = self.abbr
        self.players.append(player)

    def remove_player(self, player):
        """Remove a player from the roster (cut, trade, etc)."""
        if player in self.players:
            self.players.remove(player)
            # If they have a contract, apply dead cap
            if player.contract:
                self.dead_cap += player.contract.dead_cap_if_cut
            player.team_abbr = None
            player.contract = None

    def get_players_by_position(self, position):
        """Get all rostered players at a specific position."""
        return [p for p in self.players if p.position == position]

    def get_starters(self):
        """Get the best player at each position (simplified starter selection)."""
        from football_gm.data.positions import POSITIONS
        starters = {}
        for pos in POSITIONS:
            players_at_pos = self.get_players_by_position(pos)
            if players_at_pos:
                # Best available (not injured)
                available = [p for p in players_at_pos if not p.injured]
                if available:
                    starters[pos] = max(available, key=lambda p: p.overall_rating)
                elif players_at_pos:
                    starters[pos] = max(players_at_pos, key=lambda p: p.overall_rating)
        return starters

    def reset_season(self):
        """Reset wins/losses for a new season."""
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.points_for = 0
        self.points_against = 0

    def advance_contracts(self):
        """Advance all contracts by one year. Returns list of expired-contract players."""
        expired = []
        for player in self.players[:]:
            if player.contract:
                if player.contract.advance_year():
                    expired.append(player)
                    player.contract = None
        # Clear dead cap at start of new league year
        self.dead_cap = 0
        return expired

    def __repr__(self):
        return f"Team({self.full_name} [{self.abbr}], {self.record}, OVR:{self.overall_rating})"
