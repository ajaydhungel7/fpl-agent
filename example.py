"""Example usage of the FPL Assistant."""

import os
from dotenv import load_dotenv
from agent import create_fpl_agent

# Load environment variables
load_dotenv()


def example_queries():
    """Run some example queries to demonstrate the FPL Assistant."""

    print("=" * 70)
    print("FPL ASSISTANT - Example Queries")
    print("=" * 70)
    print()

    # Create the agent
    agent = create_fpl_agent()

    # Example 1: Search for a player
    print("Example 1: Searching for a player")
    print("-" * 70)
    query = "Search for Mohamed Salah"
    print(f"Query: {query}\n")
    response = agent(query)
    print(f"Response:\n{response}\n")

    # Example 2: Get transfer suggestions
    print("\nExample 2: Transfer recommendations")
    print("-" * 70)
    query = "Show me midfielders under £8m with good form"
    print(f"Query: {query}\n")
    response = agent(query)
    print(f"Response:\n{response}\n")

    # Example 3: Captain suggestion (requires team ID)
    team_id = os.getenv('FPL_TEAM_ID')
    if team_id:
        print("\nExample 3: Captain recommendation")
        print("-" * 70)
        query = "Who should I captain this gameweek?"
        print(f"Query: {query}\n")
        response = agent(query)
        print(f"Response:\n{response}\n")

        # Example 4: Team analysis
        print("\nExample 4: Team analysis")
        print("-" * 70)
        query = "Show me my current team"
        print(f"Query: {query}\n")
        response = agent(query)
        print(f"Response:\n{response}\n")
    else:
        print("\nExamples 3-4 skipped (FPL_TEAM_ID not set)")
        print("Set FPL_TEAM_ID in .env to see personalized examples")

    # Example 5: Find differentials
    print("\nExample 5: Finding differential players")
    print("-" * 70)
    query = "Find me some differential players with less than 10% ownership"
    print(f"Query: {query}\n")
    response = agent(query)
    print(f"Response:\n{response}\n")

    print("\n" + "=" * 70)
    print("Examples complete! Try your own queries with agent.py")
    print("=" * 70)


if __name__ == "__main__":
    example_queries()
