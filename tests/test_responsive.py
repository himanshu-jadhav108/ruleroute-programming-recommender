"""
Responsive Design and Cross-Device Layout Unit Tests for RuleRoute.
Verifies responsive CSS rules, fluid typography clamp expressions, touch target rules,
media query declarations, and responsive grid structures.
"""

from ui.theme import get_theme_css
from ui.components import render_header, render_rule_explorer


def test_theme_contains_viewport_overflow_prevention():
    """Verify CSS resets prevent horizontal overflow on root viewports."""
    css_light = get_theme_css("Light")
    css_dark = get_theme_css("Dark")

    for css in [css_light, css_dark]:
        assert "overflow-x: hidden !important" in css
        assert "max-width: 100vw !important" in css
        assert "box-sizing: border-box" in css


def test_fluid_typography_clamps():
    """Verify fluid typography rules with CSS clamp() exist for headers."""
    css = get_theme_css("Light")
    assert "clamp(" in css
    # Check that h1, h2, h3, h4 have responsive font-size
    assert "h1" in css
    assert "h2" in css
    assert "h3" in css
    assert "h4" in css


def test_touch_target_accessibility():
    """Verify touch target minimum height of 44px is enforced on interactive widgets."""
    css = get_theme_css("Light")
    assert "min-height: 44px !important" in css
    assert 'div[data-testid="stFormSubmitButton"] > button' in css
    assert 'div[data-baseweb="select"] > div' in css
    assert 'div[data-baseweb="input"]' in css
    assert '.stTabs [data-baseweb="tab"]' in css


def test_mobile_media_queries_defined():
    """Verify specific mobile and tablet media queries are present in the stylesheet."""
    css = get_theme_css("Light")
    assert "@media (max-width: 640px)" in css
    assert "@media (max-width: 520px)" in css
    assert "@media (min-width: 641px) and (max-width: 860px)" in css


def test_tab_horizontal_scroll_support():
    """Verify tabs list supports smooth horizontal scrolling on narrow screens."""
    css = get_theme_css("Light")
    assert "-webkit-overflow-scrolling: touch !important" in css
    assert "overflow-x: auto !important" in css
    assert "scrollbar-width: none !important" in css


def test_responsive_stage_grid_class():
    """Verify .rr-stage-grid responsive auto-fit grid is configured in CSS."""
    css = get_theme_css("Light")
    assert ".rr-stage-grid" in css
    assert "grid-template-columns: repeat(auto-fit, minmax(210px, 1fr))" in css


def test_decision_trace_diagram_and_connector_track():
    """Verify flow diagram and vertical connector track classes exist in CSS."""
    css = get_theme_css("Light")
    assert ".rr-flow-diagram" in css
    assert ".rr-flow-node" in css
    assert ".rr-flow-badge" in css
    assert ".rr-trace-step:not(:last-child)::before" in css


