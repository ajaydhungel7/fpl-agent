# FPL API Endpoint Tests

This folder contains individual test scripts for each FPL API endpoint.

## Usage

Run from the `fpl-assistant` directory:

```bash
cd /Users/ajaydhungel/Documents/strands/fpl-assistant
source venv/bin/activate
python api_tests/1_bootstrap_static.py
python api_tests/2_team_info.py
python api_tests/3_team_picks.py
python api_tests/4_team_history.py
python api_tests/5_team_transfers.py
python api_tests/6_player_summary.py
python api_tests/7_fixtures.py
```

## Endpoints

1. **bootstrap_static.py** - General game data (players, teams, gameweeks)
2. **team_info.py** - Manager's basic info and overall stats
3. **team_picks.py** - Current gameweek squad and selections
4. **team_history.py** - Performance history and chips used
5. **team_transfers.py** - All transfers made this season
6. **player_summary.py** - Detailed player statistics and fixtures
7. **fixtures.py** - Match fixtures for current gameweek

## Output

Each script displays:
- Endpoint URL
- Description
- Raw JSON response from the API

Use these to understand the data structure and available fields.
