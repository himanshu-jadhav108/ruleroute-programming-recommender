"""
RuleRoute Recommendation Engine Package.
A transparent, rule-based recommendation platform that connects programming
interests with suitable languages and practical project ideas.
"""

from .catalog import (
    SUPPORTED_DOMAINS,
    SUPPORTED_LEVELS,
    SUPPORTED_DIFFICULTIES,
    PROJECT_CATALOG,
    DEMO_PROFILES,
    DOMAIN_KEYWORD_HINTS,
)
from .validation import validate_user_profile
from .diagnostics import DecisionTrace
from .rules import (
    evaluate_language_rules,
    evaluate_project_rules,
    recommend,
)

__all__ = [
    'SUPPORTED_DOMAINS',
    'SUPPORTED_LEVELS',
    'SUPPORTED_DIFFICULTIES',
    'PROJECT_CATALOG',
    'DEMO_PROFILES',
    'DOMAIN_KEYWORD_HINTS',
    'validate_user_profile',
    'DecisionTrace',
    'evaluate_language_rules',
    'evaluate_project_rules',
    'recommend',
]

