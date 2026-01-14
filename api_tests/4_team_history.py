"""Test team history endpoint - Season performance history."""

import os
import sys
import json
sys.path.append('..')
from dotenv import load_dotenv
from fpl_client import FPLClient

load_dotenv()
client = FPLClient()
team_id = int(os.getenv('FPL_TEAM_ID'))

print("=" * 80)
print("TEAM HISTORY ENDPOINT")
print("=" * 80)
print(f"Endpoint: /api/entry/{team_id}/history/")
print("Description: All gameweek history, chips used, past seasons")
print()

data = client.get_team_history(team_id)

print(f"Available Keys: {list(data.keys())}")
print()

print("Chips Used:")
print("-" * 80)
print(json.dumps(data.get('chips', []), indent=2))
print()

print("Current Season (Last 5 gameweeks):")
print("-" * 80)
print(json.dumps(data.get('current', [])[-5:], indent=2))
print()

print("Past Seasons:")
print("-" * 80)
print(json.dumps(data.get('past', []), indent=2))
