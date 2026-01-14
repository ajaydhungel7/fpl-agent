"""Test team info endpoint - Manager's basic information."""

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
print("TEAM INFO ENDPOINT")
print("=" * 80)
print(f"Endpoint: /api/entry/{team_id}/")
print("Description: Manager's basic info, overall rank, points, team value")
print()

data = client.get_team_info(team_id)

print("Full Response:")
print("-" * 80)
print(json.dumps(data, indent=2))
