"""Test player summary endpoint - Detailed player info."""

import os
import sys
import json
sys.path.append('..')
from dotenv import load_dotenv
from fpl_client import FPLClient

load_dotenv()
client = FPLClient()

# Get a player from user's team
team_id = int(os.getenv('FPL_TEAM_ID'))
current_gw = client.get_current_gameweek()
picks = client.get_team_picks(team_id, current_gw)
player_id = picks['picks'][0]['element']  # First player in squad

print("=" * 80)
print("PLAYER SUMMARY ENDPOINT")
print("=" * 80)
print(f"Endpoint: /api/element-summary/{player_id}/")
print(f"Description: Detailed stats, fixtures, history for player ID {player_id}")
print()

data = client.get_player_summary(player_id)

print(f"Available Keys: {list(data.keys())}")
print()

print("Fixtures (Next 5):")
print("-" * 80)
print(json.dumps(data.get('fixtures', [])[:5], indent=2))
print()

print("History (Last 5 gameweeks):")
print("-" * 80)
print(json.dumps(data.get('history', [])[-5:], indent=2))
print()

print("Past Season History:")
print("-" * 80)
print(json.dumps(data.get('history_past', []), indent=2))
