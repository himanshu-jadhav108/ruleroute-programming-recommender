"""
Validation module for RuleRoute Recommendation Engine.
Performs defensive input verification against domain boundaries and schema requirements.
"""

from typing import Tuple, Dict, Any
from .catalog import SUPPORTED_DOMAINS, SUPPORTED_LEVELS, SUPPORTED_DIFFICULTIES


def validate_user_profile(profile: Any) -> Tuple[bool, str]:
    """
    Validates user profile keys, data types, and categorical constraints.

    Args:
        profile: Dictionary representing user preferences.

    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if not isinstance(profile, dict):
        return False, f"Invalid input profile type: Expected a dictionary, received {type(profile).__name__}."

    required_keys = ['experience_level', 'preferred_domain', 'main_interest', 'preferred_difficulty']
    for key in required_keys:
        if key not in profile:
            return False, f"Missing required profile field: '{key}'"

    # Type check for main_interest
    interest = profile['main_interest']
    if not isinstance(interest, str):
        return False, f"Invalid main interest type: Expected a string, received {type(interest).__name__}."

    # Non-empty / whitespace-only check for main_interest
    if not interest.strip():
        return False, "Main interest cannot be empty or whitespace only. Please provide a topic or focus area."

    # Domain constraint
    if profile['preferred_domain'] not in SUPPORTED_DOMAINS:
        return False, (
            f"Unsupported domain '{profile['preferred_domain']}'. "
            f"Permitted domains: {SUPPORTED_DOMAINS}"
        )

    # Experience level constraint
    if profile['experience_level'] not in SUPPORTED_LEVELS:
        return False, (
            f"Unsupported experience level '{profile['experience_level']}'. "
            f"Permitted: {SUPPORTED_LEVELS}"
        )

    # Difficulty constraint
    if profile['preferred_difficulty'] not in SUPPORTED_DIFFICULTIES:
        return False, (
            f"Unsupported difficulty '{profile['preferred_difficulty']}'. "
            f"Permitted: {SUPPORTED_DIFFICULTIES}"
        )

    return True, "Profile is valid."

