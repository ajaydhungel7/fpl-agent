"""Team analysis tools for FPL Assistant."""

from strands import tool
from fpl_client import FPLClient
from typing import List, Dict, Any
import os


client = FPLClient()


@tool
def get_my_team_summary(team_id: str = None) -> str:
    """
    Get summary of your FPL team including current points, rank, and value.

    Args:
        team_id: Your FPL team ID (optional if set in environment variable FPL_TEAM_ID)

    Returns:
        Summary of your team's performance and current status.
    """
    if not team_id:
        team_id = os.getenv('FPL_TEAM_ID')

    if not team_id:
        return "Please provide your FPL team ID or set FPL_TEAM_ID environment variable"

    try:
        team_id = int(team_id)
    except ValueError:
        return "Invalid team ID. Must be a number."

    try:
        team_info = client.get_team_info(team_id)
    except Exception as e:
        return f"Error fetching team information: {str(e)}"

    result = f"=== {team_info['name']} ===\n"
    result += f"Manager: {team_info['player_first_name']} {team_info['player_last_name']}\n\n"

    result += "Overall Performance:\n"
    result += f"  Overall Points: {team_info['summary_overall_points']:,}\n"
    result += f"  Overall Rank: {team_info['summary_overall_rank']:,}\n"
    result += f"  Gameweek Points: {team_info['summary_event_points']}\n"
    result += f"  Gameweek Rank: {team_info['summary_event_rank']:,}\n\n"

    result += "Team Value:\n"
    result += f"  Squad Value: £{team_info['last_deadline_value'] / 10:.1f}m\n"
    result += f"  Bank: £{team_info['last_deadline_bank'] / 10:.1f}m\n"
    result += f"  Total Value: £{(team_info['last_deadline_value'] + team_info['last_deadline_bank']) / 10:.1f}m\n\n"

    result += "Transfers:\n"
    result += f"  Total Transfers: {team_info['last_deadline_total_transfers']}\n"

    return result


@tool
def get_my_current_team(team_id: str = None) -> str:
    """
    Get your current FPL team lineup with player details.

    Args:
        team_id: Your FPL team ID (optional if set in environment variable FPL_TEAM_ID)

    Returns:
        Your current team lineup with player statistics.
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
        current_gw = client.get_current_gameweek()
        picks = client.get_team_picks(team_id, current_gw)
    except Exception as e:
        return f"Error fetching team picks: {str(e)}"

    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}
    position_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}

    result = f"=== Your Team (GW{current_gw}) ===\n\n"

    # Starting XI
    result += "Starting XI:\n"
    for pick in picks['picks'][:11]:
        player = client.get_player_by_id(pick['element'])
        if player:
            team_name = teams_map.get(player['team'], 'Unknown')
            position = position_map.get(player['element_type'], 'Unknown')
            price = player['now_cost'] / 10

            captain = " (C)" if pick['is_captain'] else " (VC)" if pick['is_vice_captain'] else ""

            result += f"  {position} | {player['web_name']}{captain} - {team_name} (£{price}m)\n"
            result += f"       Form: {player['form']} | Points: {player['total_points']}\n"

    result += "\nBench:\n"
    for pick in picks['picks'][11:]:
        player = client.get_player_by_id(pick['element'])
        if player:
            team_name = teams_map.get(player['team'], 'Unknown')
            position = position_map.get(player['element_type'], 'Unknown')
            price = player['now_cost'] / 10

            result += f"  {position} | {player['web_name']} - {team_name} (£{price}m)\n"

    # Active chip
    if picks.get('active_chip'):
        result += f"\nActive Chip: {picks['active_chip']}\n"

    return result


@tool
def analyze_team_fixtures(team_id: str = None, num_gameweeks: int = 5) -> str:
    """
    Analyze fixture difficulty for your team's players.

    Args:
        team_id: Your FPL team ID (optional if set in environment variable)
        num_gameweeks: Number of upcoming gameweeks to analyze (default: 5)

    Returns:
        Analysis of fixture difficulty for your players.
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
        current_gw = client.get_current_gameweek()
        picks = client.get_team_picks(team_id, current_gw)
    except Exception as e:
        return f"Error fetching team: {str(e)}"

    data = client.get_bootstrap_static()
    teams_map = {team['id']: team['name'] for team in data['teams']}

    result = f"=== Fixture Analysis (Next {num_gameweeks} GWs) ===\n\n"

    # Get unique player IDs from picks
    player_ids = [pick['element'] for pick in picks['picks']]

    # Analyze fixtures for each player
    for player_id in player_ids[:11]:  # Starting XI only
        player = client.get_player_by_id(player_id)
        if not player:
            continue

        summary = client.get_player_summary(player_id)
        fixtures = summary.get('fixtures', [])[:num_gameweeks]

        if not fixtures:
            continue

        team_name = teams_map.get(player['team'], 'Unknown')
        result += f"{player['web_name']} ({team_name}):\n"

        total_difficulty = 0
        for fixture in fixtures:
            is_home = fixture['is_home']
            opponent_id = fixture['team_a'] if is_home else fixture['team_h']
            opponent = teams_map.get(opponent_id, 'Unknown')
            difficulty = fixture['difficulty']
            total_difficulty += difficulty

            venue = "H" if is_home else "A"
            stars = '★' * difficulty

            result += f"  GW{fixture['event']}: {venue} vs {opponent} {stars}\n"

        avg_difficulty = total_difficulty / len(fixtures) if fixtures else 0
        result += f"  Avg Difficulty: {avg_difficulty:.1f}/5\n\n"

    return result


@tool
def get_transfer_history(team_id: str = None) -> str:
    """
    Get your recent transfer history.

    Args:
        team_id: Your FPL team ID (optional if set in environment variable)

    Returns:
        List of recent transfers with player names and costs.
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
        transfers = client.get_team_transfers(team_id)
    except Exception as e:
        return f"Error fetching transfers: {str(e)}"

    if not transfers:
        return "No transfers made yet this season"

    result = "=== Transfer History ===\n\n"

    result += f"Total Transfers This Season: {len(transfers)}\n\n"

    # Group transfers by gameweek
    gw_transfers = {}
    for transfer in transfers:
        gw = transfer['event']
        if gw not in gw_transfers:
            gw_transfers[gw] = []
        gw_transfers[gw].append(transfer)

    # Show last 5 gameweeks with transfers
    sorted_gws = sorted(gw_transfers.keys(), reverse=True)[:5]

    for gw in sorted_gws:
        transfers_list = gw_transfers[gw]
        result += f"Gameweek {gw} ({len(transfers_list)} transfer{'s' if len(transfers_list) != 1 else ''}):\n"

        for transfer in transfers_list:
            player_in = client.get_player_by_id(transfer['element_in'])
            player_out = client.get_player_by_id(transfer['element_out'])

            if player_in and player_out:
                result += f"  OUT: {player_out['web_name']} (£{transfer['element_out_cost'] / 10}m)\n"
                result += f"  IN:  {player_in['web_name']} (£{transfer['element_in_cost'] / 10}m)\n"

        result += "\n"

    return result


@tool
def get_chips_status(team_id: str = None) -> str:
    """
    Get information about available and used chips.

    Args:
        team_id: Your FPL team ID (optional if set in environment variable)

    Returns:
        Status of all chips (Wildcard, Free Hit, Bench Boost, Triple Captain).
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
    except Exception as e:
        return f"Error fetching team history: {str(e)}"

    result = "=== Chips Status ===\n\n"

    chips_used = history.get('chips', [])

    # All available chips
    all_chips = {
        'wildcard': 'Wildcard',
        'freehit': 'Free Hit',
        'bboost': 'Bench Boost',
        '3xc': 'Triple Captain'
    }

    result += "Used Chips:\n"
    if chips_used:
        for chip in chips_used:
            chip_name = all_chips.get(chip['name'], chip['name'])
            result += f"  ✓ {chip_name} - Used in GW{chip['event']}\n"
    else:
        result += "  None used yet\n"

    result += "\nAvailable Chips:\n"
    used_chip_names = [chip['name'] for chip in chips_used]
    available = False
    for chip_key, chip_name in all_chips.items():
        if chip_key not in used_chip_names:
            result += f"  • {chip_name}\n"
            available = True

    if not available:
        result += "  All chips have been used\n"

    return result


@tool
def get_transfer_status(team_id: str = None) -> str:
    """
    Get current transfer status including free transfers available and transfer cost.

    Args:
        team_id: Your FPL team ID (optional if set in environment variable)

    Returns:
        Current free transfers, bank balance, and transfer costs.
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
        team_info = client.get_team_info(team_id)
        current_gw = client.get_current_gameweek()
        picks = client.get_team_picks(team_id, current_gw)
        history = client.get_team_history(team_id)
        bootstrap = client.get_bootstrap_static()
    except Exception as e:
        return f"Error fetching transfer status: {str(e)}"

    result = "=== Transfer Status ===\n\n"

    # Get current gameweek status
    current_gw_data = None
    next_gw_data = None
    for event in bootstrap['events']:
        if event['is_current']:
            current_gw_data = event
        if event['is_next']:
            next_gw_data = event

    # Entry history for current gameweek
    entry_history = picks.get('entry_history', {})
    transfers_made = entry_history.get('event_transfers', 0)
    transfer_cost = entry_history.get('event_transfers_cost', 0)
    active_chip = picks.get('active_chip')

    # Determine if we can calculate free transfers
    gw_finished = current_gw_data.get('finished', False) if current_gw_data else False

    result += "Current Status:\n"
    result += f"  Current Gameweek: {current_gw}\n"
    result += f"  GW Status: {'Finished' if gw_finished else 'In Progress'}\n"

    if next_gw_data:
        result += f"  Next Gameweek: {next_gw_data['id']}\n"
        result += f"  Next Deadline: {next_gw_data['deadline_time']}\n"
    result += "\n"

    # Calculate free transfers if gameweek is finished
    if gw_finished and next_gw_data:
        result += f"Free Transfers for GW{next_gw_data['id']}:\n"

        # Calculate exact FT by tracking through the entire season
        current_season = history.get('current', [])
        chips_used = history.get('chips', [])

        # Build a map of which chips were used in which gameweeks
        chip_map = {chip['event']: chip['name'] for chip in chips_used}

        ft_available = None  # Will be set to 1 when we hit GW2

        # Track through each gameweek to calculate exact FT
        for gw_data in current_season:
            if gw_data['event'] > current_gw:
                break  # Don't process future gameweeks

            gw_event = gw_data['event']
            transfers_made = gw_data.get('event_transfers', 0)
            transfer_cost = gw_data.get('event_transfers_cost', 0)

            # GW1 has unlimited transfers, skip it
            if gw_event == 1:
                ft_available = 1  # Start GW2 with 1 FT
                continue

            # GW16 AFCON bonus: Everyone topped up to 5 FT
            if gw_event == 16:
                ft_available = 5

            # Check if a chip was used this gameweek
            chip_used = chip_map.get(gw_event)

            if chip_used in ['wildcard', 'freehit']:
                # Chip used: FT are preserved (new rule)
                # Transfers during chip week don't consume FT
                ft_used = 0
                ft_remaining = ft_available
                # Next gameweek: add 1 new FT to existing (capped at 5)
                ft_available = min(ft_remaining + 1, 5)
            else:
                # Normal gameweek: calculate exact FT used
                # FT_used = transfers - (cost / 4)
                ft_used = transfers_made - (transfer_cost // 4)

                # FT remaining after this gameweek
                ft_remaining = max(0, ft_available - ft_used)

                # Next gameweek gets 1 new FT (capped at 5)
                ft_available = min(ft_remaining + 1, 5)

        free_transfers = ft_available if ft_available is not None else 1

        result += f"  ✓ {free_transfers} free transfer{'s' if free_transfers != 1 else ''} available (max 5)\n"
        result += f"  Additional transfers cost 4 points each\n\n"
    else:
        result += f"Free Transfers for GW{current_gw}:\n"
        result += "  ⚠️  Cannot determine - gameweek in progress\n"
        result += "  Transfers may have been made after deadline\n"
        result += "  Check FPL website/app for current status\n\n"

    result += f"Last Gameweek (GW{current_gw}):\n"
    result += f"  Transfers Made: {transfers_made}\n"
    result += f"  Points Deducted: {transfer_cost}\n"
    if active_chip:
        result += f"  Chip Used: {active_chip.upper()}\n"
    result += "\n"

    result += "Team Value:\n"
    result += f"  Squad Value: £{team_info['last_deadline_value'] / 10:.1f}m\n"
    result += f"  In The Bank: £{entry_history.get('bank', 0) / 10:.1f}m\n"
    result += f"  Total Budget: £{(team_info['last_deadline_value'] + entry_history.get('bank', 0)) / 10:.1f}m\n"

    return result
