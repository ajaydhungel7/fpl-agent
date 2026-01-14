"""Test team picks endpoint - Current gameweek squad."""

import os
import sys
import json
sys.path.append('..')
from dotenv import load_dotenv
from fpl_client import FPLClient

load_dotenv()
client = FPLClient()
team_id = int(os.getenv('FPL_TEAM_ID'))
current_gw = client.get_current_gameweek()

print("=" * 80)
print("TEAM PICKS ENDPOINT")
print("=" * 80)
print(f"Endpoint: /api/entry/{team_id}/event/{current_gw}/picks/")
print("Description: Current gameweek squad, captain, active chip, entry_history")
print()

data = client.get_team_picks(team_id, current_gw)

print("Full Response:")
print("-" * 80)
print(json.dumps(data, indent=2))
