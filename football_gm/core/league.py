"""League model — the container for teams, schedule, standings, and season flow."""

import random
from football_gm.core.team import Team
from football_gm.data.teams import TEAMS


class League:
    """Represents the entire football league."""

    def __init__(self, year=2025):
        self.year = year
        self.week = 0  # 0 = offseason, 1-18 = regular season, 19+ = playoffs
        self.phase = "preseason"  # preseason, regular_season, playoffs, offseason

        # Create all 32 teams
        self.teams = {}
        for team_data in TEAMS:
            team = Team(
                city=team_data["city"],
                name=team_data["name"],
                abbr=team_data["abbr"],
                conference=team_data["conference"],
                division=team_data["division"],
            )
            self.teams[team.abbr] = team

        # All players in the league (including free agents)
        self.free_agents = []

        # Season schedule: list of weeks, each week is list of (home_abbr, away_abbr)
        self.schedule = []

        # Playoff bracket
        self.playoff_bracket = {}

        # Draft order
        self.draft_order = []

        # History
        self.history = []  # list of season summaries

    @property
    def all_players(self):
        """Every player in the league (rostered + free agents)."""
        players = list(self.free_agents)
        for team in self.teams.values():
            players.extend(team.players)
        return players

    def get_division_teams(self, conference, division):
        """Get all teams in a specific division."""
        return [t for t in self.teams.values()
                if t.conference == conference and t.division == division]

    def get_conference_teams(self, conference):
        """Get all teams in a conference."""
        return [t for t in self.teams.values() if t.conference == conference]

    def standings(self, conference=None, division=None):
        """Get teams sorted by record. Optionally filter by conference/division."""
        teams = list(self.teams.values())
        if conference:
            teams = [t for t in teams if t.conference == conference]
        if division:
            teams = [t for t in teams if t.division == division]

        # Sort by win%, then point differential as tiebreaker
        teams.sort(key=lambda t: (t.win_pct, t.point_differential), reverse=True)
        return teams

    def generate_schedule(self):
        """Generate an 18-week, 17-game NFL schedule (simplified)."""
        self.schedule = []
        team_abbrs = list(self.teams.keys())

        for week_num in range(1, 19):
            week_games = []
            shuffled = team_abbrs[:]
            random.shuffle(shuffled)

            # Pair teams up — each team plays roughly once per week
            # Some teams will have bye weeks
            used = set()
            for i in range(0, len(shuffled) - 1, 2):
                if shuffled[i] not in used and shuffled[i + 1] not in used:
                    week_games.append((shuffled[i], shuffled[i + 1]))
                    used.add(shuffled[i])
                    used.add(shuffled[i + 1])

            self.schedule.append(week_games)

        return self.schedule

    def get_week_games(self, week):
        """Get games for a specific week (1-indexed)."""
        if 1 <= week <= len(self.schedule):
            return self.schedule[week - 1]
        return []

    def advance_week(self):
        """Move the league forward by one week."""
        self.week += 1

        # Heal injured players
        for player in self.all_players:
            if player.injured:
                player.heal_week()

    def start_new_season(self):
        """Begin a new season."""
        self.week = 0
        self.phase = "preseason"

        for team in self.teams.values():
            team.reset_season()

        self.generate_schedule()
        self.phase = "regular_season"

    def determine_playoff_teams(self):
        """Select 14 playoff teams (7 per conference) based on standings."""
        playoff_teams = {"AC": [], "PC": []}

        for conf in ["AC", "PC"]:
            # Division winners (4)
            division_winners = []
            for div in ["East", "West", "North", "South"]:
                div_teams = self.get_division_teams(conf, div)
                div_teams.sort(key=lambda t: (t.win_pct, t.point_differential), reverse=True)
                if div_teams:
                    division_winners.append(div_teams[0])

            # Sort division winners by record for seeding
            division_winners.sort(key=lambda t: (t.win_pct, t.point_differential), reverse=True)

            # Wild cards (3) — best remaining teams
            conf_teams = self.get_conference_teams(conf)
            remaining = [t for t in conf_teams if t not in division_winners]
            remaining.sort(key=lambda t: (t.win_pct, t.point_differential), reverse=True)
            wild_cards = remaining[:3]

            playoff_teams[conf] = division_winners + wild_cards

        return playoff_teams

    def advance_to_offseason(self):
        """Transition to the offseason phase."""
        self.phase = "offseason"

        # Handle expiring contracts
        for team in self.teams.values():
            expired_players = team.advance_contracts()
            for player in expired_players:
                self.free_agents.append(player)

        # Player development
        for player in self.all_players:
            player.develop()

        # Retirements
        retired = []
        for player in self.all_players:
            if player.retire_check():
                retired.append(player)

        for player in retired:
            if player.team_abbr and player.team_abbr in self.teams:
                self.teams[player.team_abbr].remove_player(player)
            elif player in self.free_agents:
                self.free_agents.remove(player)

        self.year += 1
        return retired

    def __repr__(self):
        return f"League(Year:{self.year}, Week:{self.week}, Phase:{self.phase})"
