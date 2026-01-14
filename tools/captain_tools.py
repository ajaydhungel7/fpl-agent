"""Captain selection tools for FPL Assistant."""

from strands import tool
from fpl_client import FPLClient
from typing import List, Dict, Any
import os


client = FPLClient()


@tool
def suggest_captain(team_id: str = None) -> str:
    """
    Suggest the best captain choice from your current team based on fixtures and form.

    Args:
        team_id: Your FPL team ID (optional if set in environment variable)

    Returns:
        Recommended captain choices with reasoning based on fixtures and form.
    """
    if not team_id:
        team_id = os.getenv('FPL_TEAM_ID')

    if not team_id:
        return "Please provide your FPL team ID or set FPL_TEAM_ID environment variable"

    try:
        team_id = int(team_id)
    except ValueError:
        return "Invalid team ID"

    try:
        next_gw = client.get_next_gameweek()
        current_gw = client.get_current_gameweek()
        # Use current GW if next is not set
        gw = next_gw if next_gw > current_gw else current_gw
        picks = client.get_team_picks(team_id, current_gw)
    except Exception as e:
        return f"Error fetching team: {str(e)}"

    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}

    # Analyze each player in the starting XI
    captain_candidates = []

    for pick in picks['picks'][:11]:  # Starting XI only
        player = client.get_player_by_id(pick['element'])
        if not player:
            continue

        summary = client.get_player_summary(pick['element'])
        fixtures = summary.get('fixtures', [])

        if not fixtures:
            continue

        # Get next fixture
        next_fixture = fixtures[0]
        is_home = next_fixture['is_home']
        opponent_id = next_fixture['team_a'] if is_home else next_fixture['team_h']
        opponent = teams_map.get(opponent_id, 'Unknown')
        difficulty = next_fixture['difficulty']

        # Calculate captain score (lower difficulty is better)
        form_score = float(player['form']) if player['form'] else 0
        fixture_score = (6 - difficulty)  # Invert difficulty (easier = higher score)
        home_bonus = 0.5 if is_home else 0

        captain_score = (form_score * 2) + fixture_score + home_bonus

        captain_candidates.append({
            'player': player,
            'fixture': next_fixture,
            'is_home': is_home,
            'opponent': opponent,
            'difficulty': difficulty,
            'score': captain_score
        })

    # Sort by captain score
    captain_candidates.sort(key=lambda x: x['score'], reverse=True)

    result = f"=== Captain Suggestions for GW{gw} ===\n\n"

    for i, candidate in enumerate(captain_candidates[:5], 1):
        player = candidate['player']
        team_name = teams_map.get(player['team'], 'Unknown')
        venue = "Home" if candidate['is_home'] else "Away"
        difficulty_stars = '★' * candidate['difficulty']

        result += f"{i}. {player['web_name']} ({team_name})\n"
        result += f"   Fixture: {venue} vs {candidate['opponent']} {difficulty_stars}\n"
        result += f"   Form: {player['form']} | Total Points: {player['total_points']}\n"
        result += f"   Goals: {player['goals_scored']} | Assists: {player['assists']}\n"
        result += f"   Captain Score: {candidate['score']:.1f}\n\n"

    if captain_candidates:
        top_pick = captain_candidates[0]
        result += f"Recommendation: Captain {top_pick['player']['web_name']} "
        result += f"({'easy' if top_pick['difficulty'] <= 2 else 'favorable' if top_pick['difficulty'] == 3 else 'tough'} fixture)\n"

    return result


@tool
def compare_captain_options(player_ids: str) -> str:
    """
    Compare specific players as captain options for the next gameweek.

    Args:
        player_ids: Comma-separated player IDs to compare (e.g., "234,345,456")

    Returns:
        Detailed captain comparison including fixtures, form, and historical performance.
    """
    try:
        ids = [int(pid.strip()) for pid in player_ids.split(',')]
    except ValueError:
        return "Invalid player IDs format. Use comma-separated numbers like '234,345,456'"

    if len(ids) < 2:
        return "Please provide at least 2 player IDs to compare"

    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}

    result = "=== Captain Comparison ===\n\n"

    for player_id in ids:
        player = client.get_player_by_id(player_id)
        if not player:
            result += f"Player ID {player_id} not found\n\n"
            continue

        summary = client.get_player_summary(player_id)
        fixtures = summary.get('fixtures', [])

        team_name = teams_map.get(player['team'], 'Unknown')

        result += f"{player['web_name']} ({team_name})\n"
        result += f"  Form: {player['form']} | PPG: {player['points_per_game']}\n"
        result += f"  Total Points: {player['total_points']}\n"
        result += f"  Goals: {player['goals_scored']} | Assists: {player['assists']}\n"

        if fixtures:
            next_fixture = fixtures[0]
            is_home = next_fixture['is_home']
            opponent_id = next_fixture['team_a'] if is_home else next_fixture['team_h']
            opponent = teams_map.get(opponent_id, 'Unknown')
            difficulty = next_fixture['difficulty']
            venue = "Home" if is_home else "Away"
            stars = '★' * difficulty

            result += f"  Next Fixture: {venue} vs {opponent} {stars}\n"

            # Show next few fixtures
            if len(fixtures) > 1:
                result += f"  Upcoming: "
                for i, fix in enumerate(fixtures[1:4], 2):
                    opp_id = fix['team_a'] if fix['is_home'] else fix['team_h']
                    opp = teams_map.get(opp_id, 'Unknown')[:3]
                    v = "H" if fix['is_home'] else "A"
                    result += f"{v}:{opp}({fix['difficulty']}) "
                result += "\n"

        result += "\n"

    return result


@tool
def get_most_captained_players(limit: int = 10) -> str:
    """
    Get the most captained players based on ownership and form.

    Args:
        limit: Number of players to return (default: 10)

    Returns:
        List of most popular captain choices among FPL managers.
    """
    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}

    # Filter for commonly captained players (high ownership + attacking)
    candidates = []
    for player in data['elements']:
        if (player['element_type'] in [3, 4] and  # MID or FWD
            float(player['selected_by_percent']) > 5.0 and
            player['total_points'] > 20):
            candidates.append(player)

    # Sort by ownership and form
    candidates.sort(
        key=lambda x: (float(x['selected_by_percent']), float(x['form']) if x['form'] else 0),
        reverse=True
    )

    result = f"=== Most Captained Players (High Ownership + Form) ===\n\n"

    for i, player in enumerate(candidates[:limit], 1):
        team_name = teams_map.get(player['team'], 'Unknown')
        price = player['now_cost'] / 10

        result += f"{i}. {player['web_name']} (ID: {player['id']})\n"
        result += f"   {team_name} | £{price}m\n"
        result += f"   Ownership: {player['selected_by_percent']}% | Form: {player['form']}\n"
        result += f"   Points: {player['total_points']} | Goals: {player['goals_scored']} | Assists: {player['assists']}\n\n"

    return result


@tool
def analyze_captaincy_history(team_id: str = None, num_gameweeks: int = 5) -> str:
    """
    Analyze your recent captaincy choices and their returns.

    Args:
        team_id: Your FPL team ID (optional if set in environment variable)
        num_gameweeks: Number of recent gameweeks to analyze (default: 5)

    Returns:
        Analysis of your recent captain choices and points scored.
    """
    if not team_id:
        team_id = os.getenv('FPL_TEAM_ID')

    if not team_id:
        return "Please provide your FPL team ID or set FPL_TEAM_ID environment variable"

    try:
        team_id = int(team_id)
    except ValueError:
        return "Invalid team ID"

    try:
        history = client.get_team_history(team_id)
        current_gw = client.get_current_gameweek()
    except Exception as e:
        return f"Error fetching history: {str(e)}"

    result = f"=== Captaincy History (Last {num_gameweeks} GWs) ===\n\n"

    total_captain_points = 0
    gws_analyzed = 0

    # Analyze recent gameweeks
    for gw in range(max(1, current_gw - num_gameweeks), current_gw):
        try:
            picks = client.get_team_picks(team_id, gw)
            gw_live = client.get_live_gameweek(gw)

            # Find captain
            for pick in picks['picks']:
                if pick['is_captain']:
                    player = client.get_player_by_id(pick['element'])
                    if not player:
                        continue

                    # Find player's points in live data
                    player_live = None
                    for elem in gw_live['elements']:
                        if elem['id'] == pick['element']:
                            player_live = elem
                            break

                    if player_live:
                        points = player_live['stats']['total_points']
                        captain_points = points * pick['multiplier']  # 2x for captain
                        total_captain_points += captain_points
                        gws_analyzed += 1

                        result += f"GW{gw}: {player['web_name']}\n"
                        result += f"  Points: {points} x {pick['multiplier']} = {captain_points}\n\n"

        except Exception:
            continue  # Skip if data not available

    if gws_analyzed > 0:
        avg_captain_points = total_captain_points / gws_analyzed
        result += f"Average Captain Points: {avg_captain_points:.1f} per GW\n"
        result += f"Total Captain Points: {total_captain_points}\n"
    else:
        result += "No captaincy data available for recent gameweeks\n"

    return result
