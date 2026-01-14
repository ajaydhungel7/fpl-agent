"""Test bootstrap-static endpoint - General game data."""

import os
import sys
import json
sys.path.append('..')
from dotenv import load_dotenv
from fpl_client import FPLClient

load_dotenv()
client = FPLClient()

print("=" * 80)
print("BOOTSTRAP STATIC ENDPOINT")
print("=" * 80)
print("Endpoint: /api/bootstrap-static/")
print("Description: Contains all static game data - players, teams, gameweeks")
print()

data = client.get_bootstrap_static()

print(f"Available Keys: {list(data.keys())}")
print()

print("Sample Data:")
print("-" * 80)
print(json.dumps({
    "events": data['events'][:2],  # First 2 gameweeks
    "teams": data['teams'][:2],     # First 2 teams
    "elements": data['elements'][:2],  # First 2 players
    "element_types": data['element_types'],  # All positions
    "element_stats": data['element_stats'][:5]  # First 5 stat types
}, indent=2))
