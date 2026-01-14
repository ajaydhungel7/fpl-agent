"""Test team transfers endpoint - All transfers made this season."""

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
print("TEAM TRANSFERS ENDPOINT")
print("=" * 80)
print(f"Endpoint: /api/entry/{team_id}/transfers/")
print("Description: All transfers made this season")
print()

data = client.get_team_transfers(team_id)

print(f"Total Transfers: {len(data)}")
print()

if data:
    print("Last 5 Transfers:")
    print("-" * 80)
    print(json.dumps(data[-5:], indent=2))
else:
    print("No transfers made yet this season")
