"""Test free transfer calculation logic."""

def calculate_free_transfers(gameweeks_history, current_gw):
    """
    Test the free transfer calculation logic.

    Args:
        gameweeks_history: List of dicts with 'event' and 'event_transfers'
        current_gw: Current gameweek number

    Returns:
        Number of free transfers available
    """
    free_transfers = 1  # Everyone gets 1 FT per week

    # Look back through previous gameweeks
    for gw_data in reversed(gameweeks_history):
        if gw_data['event'] >= current_gw:
            continue  # Skip current or future
        if gw_data.get('event_transfers', 0) == 0:
            # No transfers made, bank one more (max 4)
            free_transfers = min(free_transfers + 1, 4)
        else:
            # Transfers were made, stop counting
            break

    return free_transfers


# Test Case 1: User has 4 FT and doesn't use them
print("Test Case 1: Already have 4 FT, don't use them")
print("=" * 60)
history1 = [
    {'event': 18, 'event_transfers': 0},
    {'event': 19, 'event_transfers': 0},
    {'event': 20, 'event_transfers': 0},
    {'event': 21, 'event_transfers': 0},  # Already at 4 FT
]
result1 = calculate_free_transfers(history1, current_gw=21)
print(f"GW18-21: No transfers → Should have 4 FT for GW22")
print(f"Result: {result1} FT ✓" if result1 == 4 else f"Result: {result1} FT ✗")
print()

# Test Case 2: User builds up from 0 to 4 FT
print("Test Case 2: Build up to 4 FT")
print("=" * 60)
history2 = [
    {'event': 17, 'event_transfers': 2},  # Used FT
    {'event': 18, 'event_transfers': 0},  # Bank 1
    {'event': 19, 'event_transfers': 0},  # Bank 1
    {'event': 20, 'event_transfers': 0},  # Bank 1
    {'event': 21, 'event_transfers': 0},  # Bank 1 (but cap at 4)
]
result2 = calculate_free_transfers(history2, current_gw=21)
print(f"GW17: Used FT, GW18-21: No transfers → Should have 4 FT for GW22")
print(f"Result: {result2} FT ✓" if result2 == 4 else f"Result: {result2} FT ✗")
print()

# Test Case 3: User uses some FT
print("Test Case 3: Use 2 out of 3 FT")
print("=" * 60)
history3 = [
    {'event': 19, 'event_transfers': 0},  # Bank 1
    {'event': 20, 'event_transfers': 0},  # Bank 1 (had 3 FT going into GW21)
    {'event': 21, 'event_transfers': 2},  # Used 2 FT
]
result3 = calculate_free_transfers(history3, current_gw=21)
print(f"GW19-20: No transfers (2 FT), GW21: Used 2 → Should have 1 FT for GW22")
print(f"Result: {result3} FT ✓" if result3 == 1 else f"Result: {result3} FT ✗")
print()

# Test Case 4: Standard scenario (1 FT per week)
print("Test Case 4: Standard 1 FT")
print("=" * 60)
history4 = [
    {'event': 20, 'event_transfers': 1},  # Used 1 FT
    {'event': 21, 'event_transfers': 1},  # Used 1 FT
]
result4 = calculate_free_transfers(history4, current_gw=21)
print(f"GW20-21: Used FT each week → Should have 1 FT for GW22")
print(f"Result: {result4} FT ✓" if result4 == 1 else f"Result: {result4} FT ✗")
print()

print("All tests passed!" if all([
    result1 == 4,
    result2 == 4,
    result3 == 1,
    result4 == 1
]) else "Some tests failed!")
