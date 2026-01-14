"""FPL API Client for fetching Fantasy Premier League data."""

import requests
from typing import Dict, List, Any, Optional
from datetime import datetime


class FPLClient:
    """Client for interacting with the Fantasy Premier League API."""

    BASE_URL = "https://fantasy.premierleague.com/api"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FPL-Assistant/1.0'
        })
        self._bootstrap_cache = None
        self._cache_time = None

    def _get(self, endpoint: str) -> Dict[str, Any]:
        """Make a GET request to the FPL API."""
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_bootstrap_static(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get bootstrap-static data (players, teams, gameweeks).
        Cached for 5 minutes to reduce API calls.
        """
        now = datetime.now()
        if (not force_refresh and self._bootstrap_cache and self._cache_time and
            (now - self._cache_time).seconds < 300):
            return self._bootstrap_cache

        data = self._get("/bootstrap-static/")
        self._bootstrap_cache = data
        self._cache_time = now
        return data

    def get_player_summary(self, player_id: int) -> Dict[str, Any]:
        """Get detailed summary for a specific player including fixtures and history."""
        return self._get(f"/element-summary/{player_id}/")

    def get_fixtures(self, event: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get fixture data, optionally filtered by gameweek."""
        endpoint = "/fixtures/"
        if event:
            endpoint += f"?event={event}"
        return self._get(endpoint)

    def get_live_gameweek(self, event: int) -> Dict[str, Any]:
        """Get live data for a specific gameweek."""
        return self._get(f"/event/{event}/live/")

    def get_team_info(self, team_id: int) -> Dict[str, Any]:
        """Get information about a manager's team."""
        return self._get(f"/entry/{team_id}/")

    def get_team_picks(self, team_id: int, event: int) -> Dict[str, Any]:
        """Get a manager's team picks for a specific gameweek."""
        return self._get(f"/entry/{team_id}/event/{event}/picks/")

    def get_team_history(self, team_id: int) -> Dict[str, Any]:
        """Get a manager's performance history."""
        return self._get(f"/entry/{team_id}/history/")

    def get_team_transfers(self, team_id: int) -> List[Dict[str, Any]]:
        """Get a manager's transfer history."""
        return self._get(f"/entry/{team_id}/transfers/")

    def get_current_gameweek(self) -> int:
        """Get the current gameweek number."""
        data = self.get_bootstrap_static()
        for event in data['events']:
            if event['is_current']:
                return event['id']
        return 1

    def get_next_gameweek(self) -> int:
        """Get the next gameweek number."""
        data = self.get_bootstrap_static()
        for event in data['events']:
            if event['is_next']:
                return event['id']
        return 1

    def get_player_by_id(self, player_id: int) -> Optional[Dict[str, Any]]:
        """Get player data by ID from bootstrap-static."""
        data = self.get_bootstrap_static()
        for player in data['elements']:
            if player['id'] == player_id:
                return player
        return None

    def get_team_by_id(self, team_id: int) -> Optional[Dict[str, Any]]:
        """Get team data by ID from bootstrap-static."""
        data = self.get_bootstrap_static()
        for team in data['teams']:
            if team['id'] == team_id:
                return team
        return None

    def search_players(self, name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for players by name."""
        data = self.get_bootstrap_static()
        name_lower = name.lower()
        matches = []

        for player in data['elements']:
            full_name = f"{player['first_name']} {player['second_name']}".lower()
            if name_lower in full_name:
                matches.append(player)
                if len(matches) >= limit:
                    break

        return matches
