"""FPL Assistant Agent - Your AI-powered Fantasy Premier League advisor."""

import os
from dotenv import load_dotenv
from strands import Agent

# Load environment variables
load_dotenv()

# Import all FPL tools
from tools.player_analysis import (
    search_player,
    get_player_details,
    get_player_fixtures,
    compare_players,
    get_top_players
)

from tools.transfer_tools import (
    analyze_transfer_options,
    find_differentials,
    suggest_transfer_swap,
    check_price_changes
)

from tools.team_tools import (
    get_my_team_summary,
    get_my_current_team,
    analyze_team_fixtures,
    get_transfer_history,
    get_chips_status,
    get_transfer_status
)

from tools.captain_tools import (
    suggest_captain,
    compare_captain_options,
    get_most_captained_players,
    analyze_captaincy_history
)


# System prompt for the FPL assistant
SYSTEM_PROMPT = """You are an expert Fantasy Premier League (FPL) assistant. Your role is to help users make informed decisions about their FPL team, including:

1. Transfer Recommendations: Analyze players' form, fixtures, and value to suggest optimal transfers
2. Captain Selection: Recommend the best captain choice based on fixtures and form
3. Team Analysis: Evaluate the user's team and identify areas for improvement
4. Player Research: Provide detailed statistics and analysis for any player
5. Strategy Advice: Offer strategic guidance on wildcards, chips, and long-term planning
6. Chips & Transfers: Track available chips, free transfers, and transfer costs

Key Principles:
- Always consider upcoming fixtures (fixture difficulty rating)
- Prioritize form over reputation
- Balance price with performance (value picks)
- Consider ownership for differentials vs safe picks
- Think about both short-term and long-term gains

When analyzing players or suggesting transfers:
- Look at their recent form (last 3-5 games)
- Check upcoming fixtures (next 3-5 gameweeks)
- Consider their price and value for money
- Factor in their role in the team (minutes, set pieces, penalty taker)
- Check for any injury concerns or news

When suggesting captains:
- Prioritize easy home fixtures
- Consider form and attacking returns
- Factor in the player's consistency
- Mention differentials vs template picks

When discussing transfers or strategy:
- Check available chips and their optimal usage timing
- IMPORTANT: The API only shows data from the last deadline. You cannot know current free transfers or pending transfers for this week. Always remind users to check the FPL website/app for their current free transfer count.
- Factor in transfer costs when suggesting multiple changes
- Recommend chip usage based on fixtures and team needs

Be conversational, insightful, and data-driven. Always explain your reasoning clearly.
"""


def create_fpl_agent():
    """Create and configure the FPL Assistant agent."""

    # Collect all tools
    tools = [
        # Player analysis tools
        search_player,
        get_player_details,
        get_player_fixtures,
        compare_players,
        get_top_players,

        # Transfer tools
        analyze_transfer_options,
        find_differentials,
        suggest_transfer_swap,
        check_price_changes,

        # Team tools
        get_my_team_summary,
        get_my_current_team,
        analyze_team_fixtures,
        get_transfer_history,
        get_chips_status,
        get_transfer_status,

        # Captain tools
        suggest_captain,
        compare_captain_options,
        get_most_captained_players,
        analyze_captaincy_history
    ]

    # Determine which LLM provider is configured
    model = os.getenv('MODEL')  # Optional override

    # Strands SDK auto-detects provider from environment variables:
    # - ANTHROPIC_API_KEY → Uses Anthropic Claude
    # - OPENAI_API_KEY → Uses OpenAI GPT
    # - GOOGLE_API_KEY → Uses Google Gemini
    # - AWS credentials → Uses AWS Bedrock
    # - OLLAMA_MODEL → Uses Ollama (local)

    agent_kwargs = {
        'tools': tools,
        'system_prompt': SYSTEM_PROMPT
    }

    # Add model override if specified
    if model:
        agent_kwargs['model'] = model

    # Create agent with tools and system prompt
    agent = Agent(**agent_kwargs)

    return agent


def main():
    """Run the FPL Assistant in interactive mode."""

    print("=" * 70)
    print("FPL ASSISTANT - Your AI-Powered Fantasy Premier League Advisor")
    print("=" * 70)
    print()
    print("Welcome! I'm here to help you make the best FPL decisions.")
    print()

    # Check LLM provider configuration
    llm_provider = None
    if os.getenv('ANTHROPIC_API_KEY'):
        llm_provider = "Anthropic Claude"
    elif os.getenv('OPENAI_API_KEY'):
        llm_provider = "OpenAI"
    elif os.getenv('GOOGLE_API_KEY'):
        llm_provider = "Google Gemini"
    elif os.getenv('AWS_ACCESS_KEY_ID'):
        llm_provider = "AWS Bedrock"
    elif os.getenv('OLLAMA_MODEL'):
        llm_provider = "Ollama (Local)"

    if llm_provider:
        print(f"✓ LLM Provider: {llm_provider}")
    else:
        print("⚠ No LLM API key detected. Please configure in .env file")
        print("  Supported: Anthropic, OpenAI, Google, AWS Bedrock, Ollama")
        return

    # Check if team ID is set
    team_id = os.getenv('FPL_TEAM_ID')
    if team_id:
        print(f"✓ Team ID configured: {team_id}")
    else:
        print("⚠ Team ID not set. Set FPL_TEAM_ID in .env file for personalized advice.")
    print()
    print("What would you like help with?")
    print("  • Transfer recommendations")
    print("  • Captain selection")
    print("  • Team analysis")
    print("  • Player research")
    print("  • Strategy advice")
    print("  • Chips & transfer status")
    print()
    print("Type 'quit' or 'exit' to end the session.")
    print("-" * 70)
    print()

    # Create agent
    agent = create_fpl_agent()

    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\nGood luck with your FPL team! 🏆")
                break

            print()

            # Get response from agent (streams automatically)
            response = agent(user_input)
            print()

        except KeyboardInterrupt:
            print("\n\nGood luck with your FPL team! 🏆")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
