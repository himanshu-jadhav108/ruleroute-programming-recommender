"""
UI Components module for RuleRoute.
Provides editorial-style developer components for forms, badges, project cards,
language rationale cards, decision traces, and catalog explorers.
"""

import json
import streamlit as st
from typing import List, Dict, Any, Optional
from recommendation_engine.catalog import (
    SUPPORTED_DOMAINS,
    SUPPORTED_LEVELS,
    SUPPORTED_DIFFICULTIES,
    PROJECT_CATALOG,
    DEMO_PROFILES,
    DOMAIN_KEYWORD_HINTS,
)


def render_header() -> None:
    """Renders top navigation header with brand mark, tagline, and theme toggle."""
    col_brand, col_theme = st.columns([0.78, 0.22])

    with col_brand:
        st.markdown(
            """
            <div style="display: flex; align-items: baseline; gap: 0.6rem; margin-top: 0.2rem;">
                <span style="font-family: monospace; font-weight: 700; font-size: 1.35rem; color: #0f766e; letter-spacing: -0.02em;">[RR]</span>
                <span style="font-weight: 700; font-size: 1.45rem; letter-spacing: -0.02em;">RuleRoute</span>
                <span class="rr-tag" style="font-size: 0.72rem; vertical-align: middle;">Deterministic v1.0</span>
            </div>
            <div style="font-size: 0.88rem; color: #64748b; margin-top: -0.1rem; margin-bottom: 0.8rem;">
                Find your language. Discover your next project.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_theme:
        current_theme = st.session_state.get("theme", "Light")
        new_theme = st.selectbox(
            "Theme",
            options=["Light", "Dark"],
            index=0 if current_theme == "Light" else 1,
            key="theme_toggle_widget",
            label_visibility="collapsed",
        )
        if new_theme != current_theme:
            st.session_state["theme"] = new_theme
            st.rerun()


def render_hero() -> None:
    """Renders compact developer hero section."""
    st.markdown(
        """
        <div class="rr-hero-banner">
            <h2 style="margin: 0 0 0.5rem 0; font-size: 1.35rem; font-weight: 600;">
                Your next programming direction starts here.
            </h2>
            <p style="margin: 0 0 0.6rem 0; font-size: 0.94rem; line-height: 1.5; color: inherit;">
                Tell us what you're interested in, where you are in your learning journey, and what you want to build.
                RuleRoute finds recommendations using <strong>transparent, propositional decision rules</strong>—without probabilistic black boxes or external AI APIs.
            </p>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.6rem;">
                <span class="rr-accent-tag">6 Supported Domains</span>
                <span class="rr-accent-tag">18 Verified Projects</span>
                <span class="rr-accent-tag">Deterministic Trace</span>
                <span class="rr-accent-tag">Zero Hallucinations</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_demo_profile_loader() -> Optional[Dict[str, Any]]:
    """Renders demo profiles selector for quick demonstration during viva or testing."""
    with st.expander("Load Demonstration Profiles (Viva & Academic Scenarios)", expanded=False):
        st.markdown(
            "<p class='rr-muted' style='font-size: 0.86rem; margin-bottom: 0.6rem;'>"
            "Select an authentic profile from the original study to populate the input parameters:"
            "</p>",
            unsafe_allow_html=True,
        )
        cols = st.columns(len(DEMO_PROFILES))
        for idx, demo in enumerate(DEMO_PROFILES):
            with cols[idx]:
                if st.button(demo['title'], key=f"demo_btn_{demo['id']}", use_container_width=True):
                    return demo
    return None


def render_profile_summary(profile: Dict[str, Any]) -> None:
    """Renders tags summarizing the submitted profile."""
    domain = profile.get('preferred_domain', 'N/A')
    level = profile.get('experience_level', 'N/A')
    diff = profile.get('preferred_difficulty', 'N/A')
    interest = profile.get('main_interest', 'N/A')

    st.markdown(
        f"""
        <div class="rr-card" style="padding: 0.9rem 1.25rem; margin-bottom: 1.25rem;">
            <div style="font-size: 0.76rem; text-transform: uppercase; font-weight: 700; color: #64748b; margin-bottom: 0.4rem; letter-spacing: 0.04em;">
                Submitted Profile Specification
            </div>
            <div style="display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center;">
                <span class="rr-tag"><strong>Domain:</strong> {domain}</span>
                <span class="rr-tag"><strong>Level:</strong> {level}</span>
                <span class="rr-tag"><strong>Difficulty:</strong> {diff}</span>
                <span class="rr-tag"><strong>Interest:</strong> {interest}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_language_recommendations(languages: List[Dict[str, str]]) -> None:
    """Renders recommended programming languages with exact rationales."""
    st.markdown("<h3 style='font-size: 1.18rem; margin-bottom: 0.6rem;'>Recommended Programming Languages</h3>", unsafe_allow_html=True)

    if not languages:
        st.markdown(
            """
            <div class="rr-card" style="border-left: 4px solid #f59e0b;">
                <div style="font-weight: 600; color: #d97706; margin-bottom: 0.25rem;">No Specific Language Rule Triggered</div>
                <div style="font-size: 0.88rem; color: #64748b;">
                    The provided interest keywords did not activate any conditional language rules for this domain.
                    Consider refining your interest text with domain-specific terms (e.g., 'frontend', 'backend', 'cross-platform', or 'engine').
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for idx, lang in enumerate(languages, 1):
        rule_tag = lang.get('triggered_rule', 'Domain Rule Evaluation')
        st.markdown(
            f"""
            <div class="rr-card" style="margin-bottom: 0.85rem;">
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.35rem; flex-wrap: wrap;">
                    <div style="font-size: 1.05rem; font-weight: 700;">
                        {idx}. {lang['language']}
                    </div>
                    <span class="rr-accent-tag">{rule_tag}</span>
                </div>
                <div style="font-size: 0.9rem; line-height: 1.45; color: inherit;">
                    <strong>Rationale:</strong> {lang['rationale']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_project_recommendations(projects: List[Dict[str, str]]) -> None:
    """Renders matching project ideas from the canonical catalog."""
    st.markdown("<h3 style='font-size: 1.18rem; margin-top: 1.25rem; margin-bottom: 0.6rem;'>Recommended Project Ideas</h3>", unsafe_allow_html=True)

    if not projects:
        st.markdown(
            """
            <div class="rr-card">
                <div style="font-weight: 600;">No Matching Projects Found</div>
                <div style="font-size: 0.88rem; color: #64748b;">No projects matched the selected domain criteria.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for idx, proj in enumerate(projects, 1):
        diff = proj['difficulty']
        badge_class = f"rr-badge-{diff.lower()}"

        st.markdown(
            f"""
            <div class="rr-card" style="margin-bottom: 0.85rem;">
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.4rem; flex-wrap: wrap; gap: 0.4rem;">
                    <div style="font-size: 1.05rem; font-weight: 700;">
                        {idx}. {proj['name']}
                    </div>
                    <div>
                        <span class="rr-badge {badge_class}">{diff} Difficulty</span>
                        <span class="rr-tag">Language: {proj['language']}</span>
                    </div>
                </div>
                <div style="font-size: 0.91rem; line-height: 1.45; margin-bottom: 0.5rem;">
                    <strong>Project Description:</strong> {proj['description']}
                </div>
                <div style="font-size: 0.88rem; color: #0f766e; line-height: 1.45;">
                    <strong>Recommendation Reason:</strong> {proj['reason']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_decision_trace(trace: List[Dict[str, Any]]) -> None:
    """
    Renders the deterministic decision trace explaining step-by-step why the engine
    arrived at the recommendations.
    """
    with st.expander("Why did RuleRoute recommend this? (Decision Trace)", expanded=True):
        st.markdown(
            "<p style='font-size: 0.86rem; color: #64748b; margin-bottom: 0.8rem;'>"
            "Chronological execution log generated during profile evaluation. Every step reflects an actual propositional rule condition evaluated by the engine:"
            "</p>",
            unsafe_allow_html=True,
        )

        trace_html = ['<div class="rr-trace-container">']
        for step in trace:
            num = step.get('step', '-')
            stage = step.get('stage', 'Evaluation')
            action = step.get('action', '')
            result = step.get('result', '')
            status = step.get('status', 'info')

            status_color = "#0f766e" if status == "success" else ("#e11d48" if status == "error" else "#f59e0b")

            trace_html.append(
                f"""
                <div class="rr-trace-step">
                    <div class="rr-step-number">{num}</div>
                    <div class="rr-step-content">
                        <div class="rr-step-header">
                            <span class="rr-step-stage">{stage}</span>
                            <span style="font-size: 0.75rem; font-weight: 600; color: {status_color}; text-transform: uppercase;">{status}</span>
                        </div>
                        <div class="rr-step-action">{action}</div>
                        <div class="rr-step-result">{result}</div>
                    </div>
                </div>
                """
            )
        trace_html.append('</div>')
        st.markdown("".join(trace_html), unsafe_allow_html=True)


def render_project_explorer() -> None:
    """Renders interactive browser for the complete 18-project catalog."""
    st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 0.4rem;'>Project Catalog Explorer</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.88rem; color: #64748b; margin-bottom: 1rem;'>"
        "Browse all 18 canonical undergraduate project specifications curated across the 6 supported technical domains."
        "</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        domain_filter = st.selectbox("Filter Domain", options=["All"] + SUPPORTED_DOMAINS)
    with col2:
        diff_filter = st.selectbox("Filter Difficulty", options=["All"] + SUPPORTED_DIFFICULTIES)
    with col3:
        search_kw = st.text_input("Search Projects", placeholder="e.g. OpenCV, Kotlin, Socket...")

    filtered = PROJECT_CATALOG
    if domain_filter != "All":
        filtered = [p for p in filtered if p['domain'] == domain_filter]
    if diff_filter != "All":
        filtered = [p for p in filtered if p['difficulty'] == diff_filter]
    if search_kw.strip():
        kw = search_kw.strip().lower()
        filtered = [
            p for p in filtered
            if kw in p['name'].lower() or kw in p['description'].lower() or kw in p['language'].lower() or kw in p['reason'].lower()
        ]

    st.markdown(f"<div style='font-size: 0.85rem; color: #64748b; margin-bottom: 0.75rem;'>Showing {len(filtered)} of {len(PROJECT_CATALOG)} projects</div>", unsafe_allow_html=True)

    for p in filtered:
        diff = p['difficulty']
        badge_class = f"rr-badge-{diff.lower()}"
        with st.expander(f"{p['name']} ({p['domain']} • {p['difficulty']})"):
            st.markdown(
                f"""
                <div style="margin-bottom: 0.5rem;">
                    <span class="rr-badge {badge_class}">{p['difficulty']}</span>
                    <span class="rr-tag">{p['domain']}</span>
                    <span class="rr-accent-tag">Suggested: {p['language']}</span>
                </div>
                <p style="font-size: 0.9rem; margin-bottom: 0.4rem;"><strong>Description:</strong> {p['description']}</p>
                <p style="font-size: 0.88rem; color: #0f766e; margin-bottom: 0;"><strong>Educational Value:</strong> {p['reason']}</p>
                """,
                unsafe_allow_html=True,
            )


def render_rule_explorer() -> None:
    """Renders comprehensive breakdown of the engine's rule set for academic review."""
    st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 0.4rem;'>Inside the Recommendation Engine</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 0.88rem; color: #64748b; margin-bottom: 1rem;'>"
        "Examine the 4 pipeline stages and deterministic propositional rules governing all recommendations."
        "</p>",
        unsafe_allow_html=True,
    )

    stage_cols = st.columns(4)
    stages = [
        ("1. Validation", "Enforces schema constraints, domain validity, and non-empty interest strings."),
        ("2. Domain Routing", "Dispatches the profile to the domain-specific rule evaluation sub-tree."),
        ("3. Language Rules", "Evaluates level constraints and keyword triggers against language rationales."),
        ("4. Project Retrieval", "Queries catalog by (Domain, Difficulty) with domain-level fallback handling."),
    ]
    for col, (title, desc) in zip(stage_cols, stages):
        with col:
            st.markdown(
                f"""
                <div class="rr-card" style="height: 100%; padding: 0.85rem 1rem;">
                    <div style="font-size: 0.86rem; font-weight: 700; color: #0f766e; margin-bottom: 0.3rem;">{title}</div>
                    <div style="font-size: 0.8rem; color: #64748b; line-height: 1.4;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<h4 style='font-size: 1.05rem; margin-top: 1.5rem; margin-bottom: 0.6rem;'>Domain Rule Mappings</h4>", unsafe_allow_html=True)

    rule_details = [
        {
            "domain": "AI/ML",
            "baseline": "Python (Industry-dominant ecosystem: PyTorch, TensorFlow, scikit-learn)",
            "conditional": "IF Experience Level in [Intermediate, Advanced] THEN add C++ (High-performance inference, ONNX engines)",
        },
        {
            "domain": "Web Development",
            "baseline": "Evaluated purely by interest keywords and experience level:",
            "conditional": "• IF 'front' in interest OR 'full' in interest OR Level == Beginner THEN JavaScript / TypeScript<br>"
                           "• IF 'back' in interest OR 'api' in interest OR 'full' in interest THEN Python<br>"
                           "• IF Level == Advanced AND Backend interest THEN Go (Golang)",
        },
        {
            "domain": "App Development",
            "baseline": "Evaluated by target platform keywords and experience level:",
            "conditional": "• IF 'android' in interest THEN Kotlin<br>"
                           "• ELIF 'cross' in interest OR Level == Beginner THEN Dart (Flutter)<br>"
                           "• ELSE Kotlin (Standard mobile architecture fallback)",
        },
        {
            "domain": "Data Science",
            "baseline": "Python (Core analytical stack: Pandas, NumPy, Matplotlib, Scipy)",
            "conditional": "IF Experience Level in [Intermediate, Advanced] THEN add SQL (Relational querying and ETL pipelines)",
        },
        {
            "domain": "Automation",
            "baseline": "Python (Web scraping with BeautifulSoup, OS scripting)",
            "conditional": "IF Experience Level in [Intermediate, Advanced] THEN add Bash / Shell (UNIX orchestration & CI/CD)",
        },
        {
            "domain": "Game Development",
            "baseline": "Evaluated by engine focus and experience level:",
            "conditional": "• IF 'unity' in interest OR Level in [Beginner, Intermediate] THEN C# (Unity Engine)<br>"
                           "• IF 'engine' in interest OR Level == Advanced THEN C++ (Unreal Engine & OpenGL/Vulkan rendering)",
        },
    ]

    for item in rule_details:
        with st.expander(f"Domain Rules: {item['domain']}"):
            st.markdown(
                f"""
                <div style="font-size: 0.88rem; line-height: 1.5;">
                    <p><strong>Baseline Recommendation:</strong> {item['baseline']}</p>
                    <p style="margin-bottom: 0;"><strong>Conditional Expansion Rules:</strong><br>{item['conditional']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_educational_card() -> None:
    """Renders academic explainer on rule-based recommendation systems."""
    st.markdown(
        """
        <div class="rr-card" style="margin-top: 1.5rem; background-color: inherit; border-left: 3px solid #0f766e;">
            <div style="font-size: 0.94rem; font-weight: 700; color: #0f766e; margin-bottom: 0.35rem;">
                Academic Primer: What is a Rule-Based Recommendation System?
            </div>
            <div style="font-size: 0.86rem; line-height: 1.5; color: inherit;">
                A <strong>rule-based system</strong> (also known as a production or expert system) arrives at conclusions through
                explicit, deterministic propositional logic (<code>IF &lt;condition&gt; THEN &lt;action&gt;</code>).
                Unlike statistical machine learning models or generative LLMs that predict probable patterns based on trained weights,
                a rule-based system guarantees <strong>100% auditability</strong>, <strong>reproducibility</strong>, and <strong>zero hallucination</strong>.
                Every recommended language and project is directly traceable to the user's explicit profile parameters.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_export_section(result: Dict[str, Any]) -> None:
    """Generates Markdown and JSON download options for recommendation results."""
    st.markdown("<h4 style='font-size: 1rem; margin-top: 1.25rem; margin-bottom: 0.5rem;'>Export Recommendation Report</h4>", unsafe_allow_html=True)
    col_md, col_json = st.columns(2)

    profile = result.get('profile', {})
    languages = result.get('languages', [])
    projects = result.get('projects', [])
    trace = result.get('trace', [])

    # Format Markdown
    md_lines = [
        "# RuleRoute — Recommendation Report",
        f"**Domain:** {profile.get('preferred_domain', 'N/A')}",
        f"**Experience Level:** {profile.get('experience_level', 'N/A')}",
        f"**Difficulty:** {profile.get('preferred_difficulty', 'N/A')}",
        f"**Main Interest:** {profile.get('main_interest', 'N/A')}",
        "\n---\n",
        "## Recommended Programming Languages",
    ]
    for idx, lang in enumerate(languages, 1):
        md_lines.append(f"{idx}. **{lang['language']}**")
        md_lines.append(f"   - Rationale: {lang['rationale']}")
        if 'triggered_rule' in lang:
            md_lines.append(f"   - Rule: {lang['triggered_rule']}")

    md_lines.append("\n## Recommended Project Ideas")
    for idx, proj in enumerate(projects, 1):
        md_lines.append(f"{idx}. **{proj['name']}** [{proj['difficulty']} Difficulty]")
        md_lines.append(f"   - Suggested Language: {proj['language']}")
        md_lines.append(f"   - Description: {proj['description']}")
        md_lines.append(f"   - Recommendation Reason: {proj['reason']}")

    md_lines.append("\n## Decision Trace Audit Log")
    for step in trace:
        md_lines.append(f"- Step {step['step']} [{step['stage']}]: {step['action']} -> {step['result']}")

    md_text = "\n".join(md_lines)
    json_text = json.dumps(result, indent=2)

    with col_md:
        st.download_button(
            label="Download Markdown Report (.md)",
            data=md_text,
            file_name="RuleRoute_Recommendation.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_json:
        st.download_button(
            label="Download JSON Audit (.json)",
            data=json_text,
            file_name="RuleRoute_Recommendation.json",
            mime="application/json",
            use_container_width=True,
        )

