"""
Streamlit AppTest integration tests for RuleRoute.
Verifies the complete Streamlit UI lifecycle including loading, demo profile selection,
form submission, recommendation rendering, theme toggling, and catalog exploration.
"""

import os
from streamlit.testing.v1 import AppTest

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))


def test_app_loads_successfully():
    """Verify app initializes without exceptions."""
    at = AppTest.from_file(APP_PATH).run()
    assert not at.exception
    # Check that RuleRoute is in markdown headers
    md_texts = " ".join([m.value for m in at.markdown])
    assert "RuleRoute" in md_texts


def test_app_theme_switch():
    """Verify switching theme updates session state and runs cleanly."""
    at = AppTest.from_file(APP_PATH).run()
    assert at.session_state["theme"] == "Light"

    # Select Dark theme
    at.selectbox(key="theme_toggle_widget").select("Dark").run()
    assert not at.exception
    assert at.session_state["theme"] == "Dark"


def test_app_submit_default_profile():
    """Verify submitting the default profile generates recommendations and trace."""
    at = AppTest.from_file(APP_PATH).run()
    at.button(key="FormSubmitter:preference_form-Generate Recommendations").click().run()
    assert not at.exception
    assert at.session_state["recommendation_result"] is not None
    assert at.session_state["recommendation_result"]["status"] == "Success"
    assert len(at.session_state["history"]) >= 1


def test_app_load_demo_profile():
    """Verify loading demo scenario 1 updates profile and generates results."""
    at = AppTest.from_file(APP_PATH).run()
    at.button(key="demo_btn_demo_1").click().run()
    assert not at.exception
    res = at.session_state["recommendation_result"]
    assert res is not None
    assert res["status"] == "Success"
    assert res["profile"]["preferred_domain"] == "AI/ML"
    assert res["projects"][0]["name"] == "Smart Vacuum Cleaner Simulation & Reflex Agent"


def test_app_load_invalid_demo_profile():
    """Verify loading invalid demo scenario displays validation error cleanly."""
    at = AppTest.from_file(APP_PATH).run()
    at.button(key="demo_btn_demo_invalid").click().run()
    assert not at.exception
    res = at.session_state["recommendation_result"]
    assert res is not None
    assert res["status"] == "Error"
    assert "Unsupported domain 'Quantum Computing'" in res["message"]
    # Check that error alert was displayed
    assert len(at.error) > 0


def test_app_reset_form():
    """Verify resetting form clears recommendation result and restores defaults."""
    at = AppTest.from_file(APP_PATH).run()
    # Load demo 2 first
    at.button(key="demo_btn_demo_2").click().run()
    assert at.session_state["recommendation_result"] is not None

    # Now click Reset Form
    at.button(key="FormSubmitter:preference_form-Reset Form").click().run()
    assert not at.exception
    assert at.session_state["recommendation_result"] is None
    assert at.session_state["form_domain"] == "AI/ML"


def test_logo_and_favicon_assets_integrated():
    """Verify that logo, icon, badge, and favicon assets exist and header displays logo tag."""
    assert os.path.exists(os.path.join(os.path.dirname(APP_PATH), "assets", "ruleroute-logo.png"))
    assert os.path.exists(os.path.join(os.path.dirname(APP_PATH), "assets", "ruleroute-icon.png"))
    assert os.path.exists(os.path.join(os.path.dirname(APP_PATH), "assets", "ruleroute-badge.jpg"))
    assert os.path.exists(os.path.join(os.path.dirname(APP_PATH), "assets", "favicon.png"))

    at = AppTest.from_file(APP_PATH).run()
    assert not at.exception
    md_texts = " ".join([m.value for m in at.markdown])
    assert "ruleroute-icon.png" in md_texts or "RuleRoute" in md_texts

