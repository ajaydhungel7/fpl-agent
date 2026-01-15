"""Transfer recommendation tools for FPL Assistant."""

from strands import tool
from fpl_client import FPLClient
from typing import List, Dict, Any


client = FPLClient()


@tool
def analyze_transfer_options(position: str, max_price: float, min_form: float = 0.0) -> str:
    """
    Find potential transfer targets based on position, price, and form.

    Args:
        position: Player position to search for ('GK', 'DEF', 'MID', 'FWD')
        max_price: Maximum price in millions (e.g., 8.5)
        min_form: Minimum form rating (default: 0.0)

    Returns:
        List of players matching the criteria with their statistics.
    """
    position_map = {'GK': 1, 'DEF': 2, 'MID': 3, 'FWD': 4}

    if position.upper() not in position_map:
        return "Invalid position. Use: GK, DEF, MID, or FWD"

    position_id = position_map[position.upper()]
    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}

    # Filter players
    candidates = []
    for player in data['elements']:
        price = player['now_cost'] / 10
        form = float(player['form']) if player['form'] else 0.0

        if (player['element_type'] == position_id and
            price <= max_price and
            form >= min_form and
            player['status'] == 'a'):  # Available
            candidates.append(player)

    # Sort by form and total points
    candidates.sort(key=lambda x: (float(x['form']) if x['form'] else 0, x['total_points']), reverse=True)

    if not candidates:
        return f"No {position.upper()} players found under £{max_price}m with form >= {min_form}"

    result = f"=== Transfer Targets: {position.upper()} under £{max_price}m ===\n\n"

    for i, player in enumerate(candidates[:15], 1):
        team_name = teams_map.get(player['team'], 'Unknown')
        price = player['now_cost'] / 10

        result += f"{i}. {player['web_name']} (ID: {player['id']})\n"
        result += f"   {team_name} | £{price}m\n"
        result += f"   Form: {player['form']} | Total Points: {player['total_points']} | PPG: {player['points_per_game']}\n"
        result += f"   Goals: {player['goals_scored']} | Assists: {player['assists']} | Selected by: {player['selected_by_percent']}%\n\n"

    return result


@tool
def find_differentials(max_ownership: float = 10.0, min_points: int = 20) -> str:
    """
    Find differential players (low ownership but good performance).

    Args:
        max_ownership: Maximum ownership percentage (default: 10.0)
        min_points: Minimum total points (default: 20)

    Returns:
        List of differential players with low ownership but good points.
    """
    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}
    position_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}

    differentials = []
    for player in data['elements']:
        ownership = float(player['selected_by_percent'])
        points = player['total_points']

        if ownership <= max_ownership and points >= min_points and player['status'] == 'a':
            differentials.append(player)

    # Sort by points per ownership ratio
    differentials.sort(key=lambda x: x['total_points'] / (float(x['selected_by_percent']) + 0.1), reverse=True)

    if not differentials:
        return f"No differentials found with ownership <= {max_ownership}% and points >= {min_points}"

    result = f"=== Differential Players (Ownership <= {max_ownership}%) ===\n\n"

    for i, player in enumerate(differentials[:15], 1):
        team_name = teams_map.get(player['team'], 'Unknown')
        position = position_map.get(player['element_type'], 'Unknown')
        price = player['now_cost'] / 10

        result += f"{i}. {player['web_name']} (ID: {player['id']})\n"
        result += f"   {team_name} | {position} | £{price}m\n"
        result += f"   Points: {player['total_points']} | Form: {player['form']} | Ownership: {player['selected_by_percent']}%\n\n"

    return result


@tool
def suggest_transfer_swap(player_out_id: int, budget: float) -> str:
    """
    Suggest replacement players for a specific player you want to transfer out.

    Args:
        player_out_id: ID of the player you want to transfer out
        budget: Total budget available for the transfer (player's selling price + any extra funds)

    Returns:
        List of recommended replacement players in the same position.
    """
    player_out = client.get_player_by_id(player_out_id)

    if not player_out:
        return f"Player with ID {player_out_id} not found"

    position_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}
    position = position_map.get(player_out['element_type'], 'Unknown')
    position_name = position

    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}

    result = f"=== Transfer Suggestions ===\n"
    result += f"Out: {player_out['web_name']} ({teams_map.get(player_out['team'], 'Unknown')})\n"
    result += f"Budget: £{budget}m | Position: {position_name}\n\n"

    # Find replacements
    replacements = []
    for player in data['elements']:
        price = player['now_cost'] / 10
        if (player['element_type'] == player_out['element_type'] and
            price <= budget and
            player['id'] != player_out_id and
            player['status'] == 'a'):
            replacements.append(player)

    # Sort by form and points
    replacements.sort(key=lambda x: (float(x['form']) if x['form'] else 0, x['total_points']), reverse=True)

    if not replacements:
        return result + f"No suitable replacements found under £{budget}m"

    result += "Recommended replacements:\n\n"

    for i, player in enumerate(replacements[:10], 1):
        team_name = teams_map.get(player['team'], 'Unknown')
        price = player['now_cost'] / 10

        result += f"{i}. {player['web_name']} (ID: {player['id']})\n"
        result += f"   {team_name} | £{price}m\n"
        result += f"   Form: {player['form']} | Total Points: {player['total_points']}\n"
        result += f"   Goals: {player['goals_scored']} | Assists: {player['assists']}\n\n"

    return result


@tool
def check_price_changes(min_change: float = 0.5) -> str:
    """
    Check which players have had significant price changes this season.

    Args:
        min_change: Minimum price change in millions to report (default: 0.5)

    Returns:
        List of players with significant price changes.
    """
    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}
    position_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}

    risers = []
    fallers = []

    for player in data['elements']:
        now_cost = player['now_cost'] / 10
        cost_change = player['cost_change_start'] / 10

        if cost_change >= min_change:
            risers.append(player)
        elif cost_change <= -min_change:
            fallers.append(player)

    result = "=== Significant Price Changes ===\n\n"

    if risers:
        risers.sort(key=lambda x: x['cost_change_start'], reverse=True)
        result += "Top Price Rises:\n\n"
        for i, player in enumerate(risers[:10], 1):
            team_name = teams_map.get(player['team'], 'Unknown')
            position = position_map.get(player['element_type'], 'Unknown')
            change = player['cost_change_start'] / 10

            result += f"{i}. {player['web_name']} ({team_name}, {position})\n"
            result += f"   Current: £{player['now_cost'] / 10}m | Change: +£{change}m\n"
            result += f"   Points: {player['total_points']} | Owned by: {player['selected_by_percent']}%\n\n"

    if fallers:
        fallers.sort(key=lambda x: x['cost_change_start'])
        result += "\nTop Price Falls:\n\n"
        for i, player in enumerate(fallers[:10], 1):
            team_name = teams_map.get(player['team'], 'Unknown')
            position = position_map.get(player['element_type'], 'Unknown')
            change = player['cost_change_start'] / 10

            result += f"{i}. {player['web_name']} ({team_name}, {position})\n"
            result += f"   Current: £{player['now_cost'] / 10}m | Change: £{change}m\n"
            result += f"   Points: {player['total_points']} | Owned by: {player['selected_by_percent']}%\n\n"

    if not risers and not fallers:
        result += f"No players found with price changes >= £{min_change}m"

    return result
