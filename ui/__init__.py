"""
UI package for RuleRoute application.
"""

from .theme import get_theme_css
from .components import (
    render_header,
    render_hero,
    render_demo_profile_loader,
    render_profile_summary,
    render_language_recommendations,
    render_project_recommendations,
    render_decision_trace,
    render_project_explorer,
    render_rule_explorer,
    render_educational_card,
    render_export_section,
)

__all__ = [
    'get_theme_css',
    'render_header',
    'render_hero',
    'render_demo_profile_loader',
    'render_profile_summary',
    'render_language_recommendations',
    'render_project_recommendations',
    'render_decision_trace',
    'render_project_explorer',
    'render_rule_explorer',
    'render_educational_card',
    'render_export_section',
]

