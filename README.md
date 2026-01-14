# FPL Assistant - AI-Powered Fantasy Premier League Advisor

An intelligent FPL assistant built with the Strands Agents SDK that helps you make data-driven decisions for your Fantasy Premier League team.

## Features

- **Player Analysis**: Search players, compare statistics, and get detailed performance metrics
- **Transfer Recommendations**: Get smart transfer suggestions based on form, fixtures, and value
- **Captain Selection**: AI-powered captain recommendations for each gameweek
- **Team Analysis**: Evaluate your team's performance and fixture difficulty
- **Differential Finder**: Discover low-owned players with high potential
- **Price Change Tracking**: Monitor player price rises and falls

## Installation

1. **Clone or download this directory**

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add:
   - Your FPL Team ID (find it in your FPL URL: `fantasy.premierleague.com/entry/{TEAM_ID}/`)
   - Your API key for the LLM provider (Anthropic Claude or AWS Bedrock)

## Configuration

### Finding Your FPL Team ID

1. Go to https://fantasy.premierleague.com/
2. Log in to your account
3. Click on "Points" or "Transfers"
4. Look at the URL - it will be: `fantasy.premierleague.com/entry/{YOUR_TEAM_ID}/`
5. Copy that number and add it to your `.env` file

### LLM Provider Setup

#### Option 1: AWS Bedrock (Recommended for Production)
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

**Quick Setup:**
```bash
./setup_bedrock.sh
```

See **[AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md)** for detailed instructions.

**Benefits:**
- Enterprise-grade security and compliance
- Integrated AWS billing
- No separate API key management
- VPC/PrivateLink support

#### Option 2: Anthropic Claude (Easiest)
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key from: https://console.anthropic.com/

#### Option 3: Other Providers
See **[LLM_SETUP.md](LLM_SETUP.md)** for OpenAI, Google Gemini, and Ollama (local/free) options.

## Usage

### Interactive Mode

Run the assistant in interactive mode:

```bash
python agent.py
```

Then ask questions like:
- "Who should I captain this week?"
- "Suggest some midfielders under £8m with good fixtures"
- "Analyze my team's upcoming fixtures"
- "Compare Haaland and Kane as captain options"
- "Show me some differential options"

### Python API

Use the agent programmatically:

```python
from agent import create_fpl_agent

agent = create_fpl_agent()

# Get transfer suggestions
response = agent("Suggest midfielders under 8 million with good form")
print(response)

# Captain recommendation
response = agent("Who should I captain this gameweek?")
print(response)

# Team analysis
response = agent("Analyze my team's performance")
print(response)
```

## Available Tools

### Player Analysis
- `search_player(name)` - Search for players by name
- `get_player_details(player_id)` - Detailed player statistics
- `get_player_fixtures(player_id)` - Upcoming fixtures with difficulty
- `compare_players(player_ids)` - Side-by-side player comparison
- `get_top_players(position, limit)` - Top performers by position

### Transfer Tools
- `analyze_transfer_options(position, max_price, min_form)` - Find transfer targets
- `find_differentials(max_ownership, min_points)` - Low-owned gems
- `suggest_transfer_swap(player_out_id, budget)` - Direct replacement suggestions
- `check_price_changes(min_change)` - Track price changes

### Team Tools
- `get_my_team_summary(team_id)` - Your team's overall performance
- `get_my_current_team(team_id)` - Current squad with stats
- `analyze_team_fixtures(team_id, num_gameweeks)` - Fixture difficulty analysis
- `get_transfer_history(team_id)` - Recent transfer history

### Captain Tools
- `suggest_captain(team_id)` - AI captain recommendation
- `compare_captain_options(player_ids)` - Compare captain choices
- `get_most_captained_players(limit)` - Most popular captain picks
- `analyze_captaincy_history(team_id)` - Your captain performance history

## Example Queries

**Transfer Planning:**
```
"I need to replace my midfielder who's injured. I have £8.5m. Who should I get?"
"Show me some budget defenders under £4.5m"
"Find me differentials with less than 5% ownership"
```

**Captain Selection:**
```
"Who should I captain this week?"
"Compare Salah and Haaland as captain options"
"What are the most captained players this week?"
```

**Team Analysis:**
```
"How is my team performing?"
"Analyze my team's fixtures for the next 5 gameweeks"
"Show my recent transfers"
```

**Player Research:**
```
"Tell me about Bukayo Saka's recent form"
"Compare Son and Maddison"
"Show me the top 10 forwards"
```

## How It Works

The FPL Assistant uses:

1. **FPL API Client** (`fpl_client.py`) - Fetches data from the official FPL API
2. **Strands Tools** (`tools/`) - Python functions decorated with `@tool` that the AI can call
3. **Strands Agent** - LLM-powered agent that reasons about your questions and uses tools to provide answers

The agent understands your natural language queries, determines which tools to use, fetches the relevant data, and provides insightful recommendations based on form, fixtures, and FPL strategy.

## Architecture

```
fpl-assistant/
├── agent.py              # Main agent script
├── fpl_client.py         # FPL API client
├── requirements.txt      # Python dependencies
├── .env                  # Configuration (not committed)
├── .env.example          # Example configuration
└── tools/
    ├── player_analysis.py   # Player research tools
    ├── transfer_tools.py    # Transfer recommendation tools
    ├── team_tools.py        # Team analysis tools
    └── captain_tools.py     # Captain selection tools
```

## Data Source

All data comes from the official Fantasy Premier League API:
- No authentication required for most endpoints
- Real-time player statistics and fixtures
- Historical performance data
- Current gameweek information

## Limitations

- The FPL API is unofficial and may change without notice
- Some advanced features (like making actual transfers) require authentication
- Rate limiting: Be respectful with API calls
- The agent cannot make actual changes to your FPL team - it only provides advice

## Contributing

Feel free to add more tools or improve existing ones:

1. Create new tools in the `tools/` directory
2. Use the `@tool` decorator from `strands`
3. Add the tool to the agent in `agent.py`
4. Provide clear docstrings for the LLM to understand

## Troubleshooting

**"Player with ID X not found"**
- The player ID might be incorrect. Use `search_player()` to find the right ID.

**"Please provide your FPL team ID"**
- Set `FPL_TEAM_ID` in your `.env` file.

**"Error fetching data"**
- Check your internet connection
- The FPL API might be down during maintenance
- Try again in a few moments

**"Invalid API key"**
- Verify your API key is correctly set in `.env`
- Check that you're using the right provider (Anthropic or AWS)

## License

MIT License - feel free to use and modify for your FPL needs!

## Disclaimer

This is an unofficial tool and is not affiliated with the Premier League or Fantasy Premier League. Use at your own discretion for entertainment and research purposes.

---

Good luck with your FPL season! 🏆⚽
