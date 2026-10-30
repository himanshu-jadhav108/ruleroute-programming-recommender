"""
RuleRoute — Programming Language & Project Recommendation System
Main Streamlit Application Entrypoint.
"""

import os
import streamlit as st
import datetime
from typing import Dict, Any

from recommendation_engine.catalog import (
    SUPPORTED_DOMAINS,
    SUPPORTED_LEVELS,
    SUPPORTED_DIFFICULTIES,
    PROJECT_CATALOG,
    DEMO_PROFILES,
    DOMAIN_KEYWORD_HINTS,
)
from recommendation_engine.rules import recommend
from ui.theme import get_theme_css
from ui.components import (
    render_header,
    render_hero,
    render_clean_html,
    render_profile_summary,
    render_language_recommendations,
    render_project_recommendations,
    render_decision_trace,
    render_project_explorer,
    render_rule_explorer,
    render_educational_card,
    render_export_section,
)

# -----------------------------------------------------------------------------
# 1. Page Configuration & State Initialization
# -----------------------------------------------------------------------------
FAVICON_PATH = "assets/favicon.png" if os.path.exists("assets/favicon.png") else "🧭"

st.set_page_config(
    page_title="RuleRoute — Rule-Based Recommendation System",
    page_icon=FAVICON_PATH,
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "theme" not in st.session_state:
    st.session_state["theme"] = "Light"

if "history" not in st.session_state:
    st.session_state["history"] = []

if "recommendation_result" not in st.session_state:
    st.session_state["recommendation_result"] = None

# Form field states for demo loading & resetting
if "form_domain" not in st.session_state:
    st.session_state["form_domain"] = SUPPORTED_DOMAINS[0]

if "form_level" not in st.session_state:
    st.session_state["form_level"] = SUPPORTED_LEVELS[0]

if "form_diff" not in st.session_state:
    st.session_state["form_diff"] = SUPPORTED_DIFFICULTIES[0]

if "form_interest" not in st.session_state:
    st.session_state["form_interest"] = "Reflex Agents & Machine Learning"

if "active_demo_name" not in st.session_state:
    st.session_state["active_demo_name"] = None

# Inject CSS Theme
st.markdown(get_theme_css(st.session_state["theme"]), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Top Header and Hero
# -----------------------------------------------------------------------------
render_header()
render_hero()


# -----------------------------------------------------------------------------
# 3. Main Navigation Tabs
# -----------------------------------------------------------------------------
tab_studio, tab_projects, tab_rules, tab_methodology = st.tabs([
    "🎯 Recommendation Studio",
    "📚 Project Catalog (18)",
    "⚙️ Inside the Engine",
    "📖 Methodology & Viva Notes",
])


# -----------------------------------------------------------------------------
# Tab 1: Recommendation Studio
# -----------------------------------------------------------------------------
with tab_studio:
    # A. Demo Scenarios Selector
    with st.expander("⚡ Load Demonstration Profiles (Academic Scenarios & Edge Cases)", expanded=False):
        render_clean_html(
            "<p class='rr-muted' style='font-size: 0.86rem; margin-bottom: 0.6rem;'>"
            "Pre-populated profiles from the original study. Click any profile to automatically load its parameters:"
            "</p>"
        )
        demo_cols = st.columns(len(DEMO_PROFILES))
        for idx, demo in enumerate(DEMO_PROFILES):
            with demo_cols[idx]:
                if st.button(demo['title'], key=f"demo_btn_{demo['id']}", use_container_width=True):
                    p = demo['profile']
                    st.session_state["form_domain"] = p['preferred_domain']
                    st.session_state["form_level"] = p['experience_level']
                    st.session_state["form_diff"] = p['preferred_difficulty']
                    st.session_state["form_interest"] = p['main_interest']
                    st.session_state["active_demo_name"] = demo['subtitle']

                    # Immediately evaluate the demo profile
                    res = recommend(p)
                    st.session_state["recommendation_result"] = res

                    # Append to session history
                    st.session_state["history"].append({
                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                        "title": demo['title'],
                        "profile": dict(p),
                        "result": res,
                    })
                    st.rerun()

    if st.session_state.get("active_demo_name"):
        st.info(f"Loaded scenario: **{st.session_state['active_demo_name']}**")

    # B. Interactive Preference Form
    st.markdown("<h3 style='font-size: 1.15rem; margin-top: 0.5rem; margin-bottom: 0.5rem;'>Configure Profile Preferences</h3>", unsafe_allow_html=True)

    with st.form("preference_form", clear_on_submit=False):
        col_domain, col_level, col_diff = st.columns(3)

        # Domain selection
        domain_idx = 0
        if st.session_state["form_domain"] in SUPPORTED_DOMAINS:
            domain_idx = SUPPORTED_DOMAINS.index(st.session_state["form_domain"])
        with col_domain:
            selected_domain = st.selectbox(
                "Preferred Domain",
                options=SUPPORTED_DOMAINS,
                index=domain_idx,
                help="The engineering specialization domain.",
            )

        # Level selection
        level_idx = 0
        if st.session_state["form_level"] in SUPPORTED_LEVELS:
            level_idx = SUPPORTED_LEVELS.index(st.session_state["form_level"])
        with col_level:
            selected_level = st.selectbox(
                "Experience Level",
                options=SUPPORTED_LEVELS,
                index=level_idx,
                help="Your current familiarity with programming concepts.",
            )

        # Difficulty selection
        diff_idx = 0
        if st.session_state["form_diff"] in SUPPORTED_DIFFICULTIES:
            diff_idx = SUPPORTED_DIFFICULTIES.index(st.session_state["form_diff"])
        with col_diff:
            selected_diff = st.selectbox(
                "Preferred Difficulty",
                options=SUPPORTED_DIFFICULTIES,
                index=diff_idx,
                help="Target difficulty for recommended projects.",
            )

        # Keyword guidance card
        hint_data = DOMAIN_KEYWORD_HINTS.get(selected_domain, {})
        if hint_data:
            render_clean_html(
                f"""
                <div style="background-color: inherit; border: 1px dashed #64748b80; border-radius: 6px; padding: 0.6rem 0.9rem; margin-top: 0.2rem; margin-bottom: 0.6rem;">
                    <div style="font-size: 0.8rem; font-weight: 600; color: #0f766e;">Domain Keyword Influence ({selected_domain}):</div>
                    <div style="font-size: 0.82rem; color: #64748b; line-height: 1.4;">
                        {hint_data.get('hint', '')}<br>
                        <em>Rule behavior:</em> {hint_data.get('rule_note', '')}
                    </div>
                </div>
                """
            )

        # Main Interest free-text input
        selected_interest = st.text_input(
            "Main Interest / Keyword Focus",
            value=st.session_state["form_interest"],
            placeholder=f"e.g. {hint_data.get('example', 'Web scraping, full-stack, robotics...')}",
            help="Free-text input scanned for domain-specific rule triggers (e.g., 'front', 'api', 'android', 'unity').",
        )

        col_submit, col_reset = st.columns([0.75, 0.25])
        with col_submit:
            submit_btn = st.form_submit_button("Generate Recommendations", type="primary", use_container_width=True)
        with col_reset:
            reset_btn = st.form_submit_button("Reset Form", type="secondary", use_container_width=True)

    if reset_btn:
        st.session_state["form_domain"] = SUPPORTED_DOMAINS[0]
        st.session_state["form_level"] = SUPPORTED_LEVELS[0]
        st.session_state["form_diff"] = SUPPORTED_DIFFICULTIES[0]
        st.session_state["form_interest"] = "Reflex Agents & Machine Learning"
        st.session_state["active_demo_name"] = None
        st.session_state["recommendation_result"] = None
        st.rerun()

    if submit_btn:
        # Build candidate profile
        profile = {
            "preferred_domain": selected_domain,
            "experience_level": selected_level,
            "preferred_difficulty": selected_diff,
            "main_interest": selected_interest,
        }

        # Keep session state updated
        st.session_state["form_domain"] = selected_domain
        st.session_state["form_level"] = selected_level
        st.session_state["form_diff"] = selected_diff
        st.session_state["form_interest"] = selected_interest
        st.session_state["active_demo_name"] = None

        # Execute recommendation engine
        res = recommend(profile)
        st.session_state["recommendation_result"] = res

        # Record in session history
        st.session_state["history"].append({
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "title": f"{selected_domain} ({selected_level})",
            "profile": profile,
            "result": res,
        })
        st.rerun()

    # C. Display Recommendation Results
    res = st.session_state.get("recommendation_result")
    if res is not None:
        render_clean_html("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #e2e8f0;'>")

        if res.get("status") == "Error":
            st.error(f"**Validation Rejected:** {res.get('message')}")
            if res.get("trace"):
                render_decision_trace(res["trace"])
        else:
            st.success("Recommendations successfully generated via deterministic propositional rules.")
            render_profile_summary(res.get("profile", {}))
            render_language_recommendations(res.get("languages", []))
            render_project_recommendations(res.get("projects", []))
            render_decision_trace(res.get("trace", []))
            render_export_section(res)

    # D. Session History Section
    history = st.session_state.get("history", [])
    if history:
        with st.expander(f"🕒 Recent Session Evaluations ({len(history)} items)", expanded=False):
            render_clean_html(
                "<p class='rr-muted' style='font-size: 0.82rem; margin-bottom: 0.6rem;'>"
                "Temporary in-memory history of recommendations evaluated during this browser session:"
                "</p>"
            )
            for idx, item in enumerate(reversed(history)):
                hist_prof = item.get("profile", {})
                cols = st.columns([0.7, 0.3])
                with cols[0]:
                    render_clean_html(
                        f"**{item['title']}** — `{item['timestamp']}`<br>"
                        f"<span style='font-size: 0.84rem; color: #64748b;'>"
                        f"Domain: {hist_prof.get('preferred_domain')} | Level: {hist_prof.get('experience_level')} | "
                        f"Diff: {hist_prof.get('preferred_difficulty')} | Interest: \"{hist_prof.get('main_interest')}\""
                        f"</span>"
                    )
                with cols[1]:
                    if st.button("Restore Result", key=f"restore_hist_{idx}", use_container_width=True):
                        st.session_state["recommendation_result"] = item["result"]
                        st.session_state["form_domain"] = hist_prof.get("preferred_domain")
                        st.session_state["form_level"] = hist_prof.get("experience_level")
                        st.session_state["form_diff"] = hist_prof.get("preferred_difficulty")
                        st.session_state["form_interest"] = hist_prof.get("main_interest")
                        st.rerun()


# -----------------------------------------------------------------------------
# Tab 2: Project Catalog Explorer
# -----------------------------------------------------------------------------
with tab_projects:
    render_project_explorer()


# -----------------------------------------------------------------------------
# Tab 3: Inside the Engine (Rules & Architecture)
# -----------------------------------------------------------------------------
with tab_rules:
    render_rule_explorer()


# -----------------------------------------------------------------------------
# Tab 4: Methodology & Viva Notes
# -----------------------------------------------------------------------------
with tab_methodology:
    st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 0.5rem;'>Academic Methodology & Viva Guide</h3>", unsafe_allow_html=True)
    render_educational_card()

    render_clean_html(
        """
        <div class="rr-card" style="margin-top: 1rem;">
            <h4 style="font-size: 1rem; margin-top: 0;">1. System Architecture Overview</h4>
            <p style="font-size: 0.88rem; line-height: 1.5;">
                RuleRoute separates knowledge representation, inference logic, and presentation into strict architectural layers:
            </p>
            <ul style="font-size: 0.88rem; line-height: 1.5;">
                <li><strong>Knowledge Base (<code>catalog.py</code>):</strong> Declarative stores for 6 domains, 3 experience levels, 3 difficulty tiers, and 18 canonical project ideas.</li>
                <li><strong>Defensive Validator (<code>validation.py</code>):</strong> Type and constraint validation verifying schema integrity prior to rule execution.</li>
                <li><strong>Rule Engine (<code>rules.py</code>):</strong> Propositional rule trees evaluating domain baselines, level gating, and substring keyword matching.</li>
                <li><strong>Decision Tracer (<code>diagnostics.py</code>):</strong> Real-time deterministic audit logger generating explainable reasoning chains.</li>
                <li><strong>Presentation Layer (<code>app.py</code> & <code>ui/</code>):</strong> Streamlit reactive UI with high-contrast dual theme support and export utilities.</li>
            </ul>
        </div>

        <div class="rr-card">
            <h4 style="font-size: 1rem; margin-top: 0;">2. Key Viva / Presentation Questions Answered</h4>
            <div style="font-size: 0.88rem; line-height: 1.5;">
                <p><strong>Q1: Why use a rule-based system instead of a Machine Learning model or LLM?</strong><br>
                <em>Answer:</em> For educational advising and deterministic curricular guidance, rule-based systems guarantee 100% explainability, auditability, and zero hallucination. Unlike ML models which require large training corpora and may produce ungrounded recommendations, propositional rules represent domain knowledge curated directly by educators.</p>

                <p><strong>Q2: How does the system handle conflicting or unexpected inputs?</strong><br>
                <em>Answer:</em> The engine uses defensive boundaries in <code>validate_user_profile</code> to catch missing fields, unsupported categories, and empty strings. If an un-matched difficulty is encountered in catalog search, the system executes an explicit fallback match returning general projects for that domain.</p>

                <p><strong>Q3: How is the decision trace generated?</strong><br>
                <em>Answer:</em> An active <code>DecisionTrace</code> accumulator records every rule evaluation as it executes in real time. The resulting trace is returned alongside the recommendation data and rendered directly in the interface.</p>
            </div>
        </div>
        """
    )

