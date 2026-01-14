"""Player analysis tools for FPL Assistant."""

from strands import tool
from fpl_client import FPLClient
from typing import List, Dict, Any


client = FPLClient()


@tool
def search_player(name: str) -> str:
    """
    Search for FPL players by name.

    Args:
        name: The player's name to search for (e.g., "Salah", "Haaland")

    Returns:
        Formatted string with player information including ID, name, team, position, price, and form.
    """
    players = client.search_players(name, limit=5)

    if not players:
        return f"No players found matching '{name}'"

    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}
    position_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}

    result = f"Found {len(players)} player(s) matching '{name}':\n\n"

    for player in players:
        team_name = teams_map.get(player['team'], 'Unknown')
        position = position_map.get(player['element_type'], 'Unknown')
        price = player['now_cost'] / 10

        result += f"• {player['web_name']} (ID: {player['id']})\n"
        result += f"  {team_name} | {position} | £{price}m\n"
        result += f"  Form: {player['form']} | Total Points: {player['total_points']}\n"
        result += f"  Selected by: {player['selected_by_percent']}%\n\n"

    return result


@tool
def get_player_details(player_id: int) -> str:
    """
    Get detailed statistics for a specific player.

    Args:
        player_id: The FPL player ID

    Returns:
        Detailed player statistics including form, fixtures, and performance metrics.
    """
    player = client.get_player_by_id(player_id)

    if not player:
        return f"Player with ID {player_id} not found"

    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}
    position_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}

    team_name = teams_map.get(player['team'], 'Unknown')
    position = position_map.get(player['element_type'], 'Unknown')
    price = player['now_cost'] / 10

    result = f"=== {player['web_name']} ({player['first_name']} {player['second_name']}) ===\n\n"
    result += f"Team: {team_name}\n"
    result += f"Position: {position}\n"
    result += f"Price: £{price}m\n\n"

    result += "Performance:\n"
    result += f"  Total Points: {player['total_points']}\n"
    result += f"  Form: {player['form']}\n"
    result += f"  Points per Game: {player['points_per_game']}\n"
    result += f"  Minutes Played: {player['minutes']}\n\n"

    result += "Statistics:\n"
    result += f"  Goals: {player['goals_scored']}\n"
    result += f"  Assists: {player['assists']}\n"
    result += f"  Clean Sheets: {player['clean_sheets']}\n"
    result += f"  Bonus Points: {player['bonus']}\n\n"

    result += "Value:\n"
    result += f"  Selected by: {player['selected_by_percent']}%\n"
    result += f"  ICT Index: {player['ict_index']}\n"
    result += f"  Influence: {player['influence']}\n"
    result += f"  Creativity: {player['creativity']}\n"
    result += f"  Threat: {player['threat']}\n\n"

    result += "Status:\n"
    result += f"  Availability: {player['status']}\n"
    result += f"  News: {player['news'] if player['news'] else 'None'}\n"

    return result


@tool
def get_player_fixtures(player_id: int, num_fixtures: int = 5) -> str:
    """
    Get upcoming fixtures for a player with difficulty ratings.

    Args:
        player_id: The FPL player ID
        num_fixtures: Number of upcoming fixtures to show (default: 5)

    Returns:
        Formatted string with upcoming fixtures and difficulty ratings.
    """
    player = client.get_player_by_id(player_id)

    if not player:
        return f"Player with ID {player_id} not found"

    summary = client.get_player_summary(player_id)
    fixtures = summary.get('fixtures', [])[:num_fixtures]

    if not fixtures:
        return f"No upcoming fixtures found for {player['web_name']}"

    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}

    result = f"=== Upcoming Fixtures for {player['web_name']} ===\n\n"

    for fixture in fixtures:
        is_home = fixture['is_home']
        opponent_id = fixture['team_a'] if is_home else fixture['team_h']
        opponent = teams_map.get(opponent_id, 'Unknown')
        difficulty = fixture['difficulty']
        event = fixture['event']

        venue = "Home" if is_home else "Away"
        difficulty_stars = '★' * difficulty

        result += f"GW{event}: {venue} vs {opponent}\n"
        result += f"  Difficulty: {difficulty_stars} ({difficulty}/5)\n\n"

    return result


@tool
def compare_players(player_ids: str) -> str:
    """
    Compare multiple players side by side.

    Args:
        player_ids: Comma-separated player IDs to compare (e.g., "234,345,456")

    Returns:
        Side-by-side comparison of player statistics.
    """
    try:
        ids = [int(pid.strip()) for pid in player_ids.split(',')]
    except ValueError:
        return "Invalid player IDs format. Use comma-separated numbers like '234,345,456'"

    if len(ids) < 2:
        return "Please provide at least 2 player IDs to compare"

    if len(ids) > 5:
        return "Maximum 5 players can be compared at once"

    players = []
    for pid in ids:
        player = client.get_player_by_id(pid)
        if player:
            players.append(player)
        else:
            return f"Player with ID {pid} not found"

    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}

    result = "=== Player Comparison ===\n\n"

    for player in players:
        team_name = teams_map.get(player['team'], 'Unknown')
        price = player['now_cost'] / 10

        result += f"{player['web_name']} ({team_name}) - £{price}m\n"
        result += f"  Total Points: {player['total_points']} | Form: {player['form']} | PPG: {player['points_per_game']}\n"
        result += f"  Goals: {player['goals_scored']} | Assists: {player['assists']} | Bonus: {player['bonus']}\n"
        result += f"  Selected by: {player['selected_by_percent']}% | ICT: {player['ict_index']}\n\n"

    return result


@tool
def get_top_players(position: str = "all", limit: int = 10) -> str:
    """
    Get the top performing players by total points.

    Args:
        position: Filter by position: 'GK', 'DEF', 'MID', 'FWD', or 'all' (default: 'all')
        limit: Number of players to return (default: 10)

    Returns:
        List of top performing players with their statistics.
    """
    data = client.get_bootstrap_static()
    players = data['elements']

    position_map = {'GK': 1, 'DEF': 2, 'MID': 3, 'FWD': 4}

    if position.upper() != 'ALL':
        if position.upper() not in position_map:
            return f"Invalid position. Use: GK, DEF, MID, FWD, or ALL"
        position_id = position_map[position.upper()]
        players = [p for p in players if p['element_type'] == position_id]

    # Sort by total points
    players.sort(key=lambda x: x['total_points'], reverse=True)
    top_players = players[:limit]

    teams_map = {team['id']: team['name'] for team in data['teams']}

    result = f"=== Top {limit} {position.upper()} Players by Total Points ===\n\n"

    for i, player in enumerate(top_players, 1):
        team_name = teams_map.get(player['team'], 'Unknown')
        price = player['now_cost'] / 10

        result += f"{i}. {player['web_name']} (ID: {player['id']})\n"
        result += f"   {team_name} | £{price}m\n"
        result += f"   Points: {player['total_points']} | Form: {player['form']} | PPG: {player['points_per_game']}\n"
        result += f"   Goals: {player['goals_scored']} | Assists: {player['assists']}\n\n"

    return result
