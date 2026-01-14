"""Test fixtures endpoint - Match fixtures."""

import os
import sys
import json
sys.path.append('..')
from dotenv import load_dotenv
from fpl_client import FPLClient

load_dotenv()
client = FPLClient()
current_gw = client.get_current_gameweek()

print("=" * 80)
print("FIXTURES ENDPOINT")
print("=" * 80)
print(f"Endpoint: /api/fixtures/?event={current_gw}")
print(f"Description: All fixtures for gameweek {current_gw}")
print()

data = client.get_fixtures(current_gw)

print(f"Total Fixtures: {len(data)}")
print()

print("Sample Fixtures (First 5):")
print("-" * 80)
print(json.dumps(data[:5], indent=2))
