"""
Theme and styling definitions for RuleRoute.
Provides responsive, high-contrast, developer-oriented Light and Dark palettes.
"""

def get_theme_css(theme: str = "Light") -> str:
    """
    Generate CSS stylesheet based on selected theme mode.

    Args:
        theme: "Light" or "Dark"

    Returns:
        CSS string for st.markdown injection.
    """
    is_dark = (theme.lower() == "dark")

    if is_dark:
        bg_page = "#0b0f19"
        bg_surface = "#111827"
        bg_surface_alt = "#1e293b"
        bg_card = "#161f30"
        border_color = "#2d3748"
        border_light = "#1e293b"
        text_primary = "#f1f5f9"
        text_secondary = "#94a3b8"
        text_muted = "#64748b"
        accent = "#14b8a6"
        accent_hover = "#0d9488"
        accent_subtle = "rgba(20, 184, 166, 0.12)"
        tag_bg = "#1e293b"
        tag_text = "#38bdf8"
        code_bg = "#0f172a"
        badge_easy_bg = "rgba(34, 197, 94, 0.15)"
        badge_easy_text = "#4ade80"
        badge_med_bg = "rgba(245, 158, 11, 0.15)"
        badge_med_text = "#fbbf24"
        badge_hard_bg = "rgba(239, 68, 68, 0.15)"
        badge_hard_text = "#f87171"
        trace_step_bg = "#1e293b"
        trace_step_border = "#334155"
    else:
        bg_page = "#f8fafc"
        bg_surface = "#ffffff"
        bg_surface_alt = "#f1f5f9"
        bg_card = "#ffffff"
        border_color = "#e2e8f0"
        border_light = "#cbd5e1"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        text_muted = "#64748b"
        accent = "#0f766e"
        accent_hover = "#115e59"
        accent_subtle = "rgba(15, 118, 110, 0.08)"
        tag_bg = "#f1f5f9"
        tag_text = "#0284c7"
        code_bg = "#f1f5f9"
        badge_easy_bg = "#dcfce7"
        badge_easy_text = "#15803d"
        badge_med_bg = "#fef3c7"
        badge_med_text = "#b45309"
        badge_hard_bg = "#fee2e2"
        badge_hard_text = "#b91c1c"
        trace_step_bg = "#f8fafc"
        trace_step_border = "#e2e8f0"

    css = f"""
    <style>
    /* Global Base */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {bg_page} !important;
        color: {text_primary} !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}

    [data-testid="stHeader"] {{
        background-color: {bg_page} !important;
    }}

    .main .block-container {{
        max-width: 1040px;
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
    }}

    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: {text_primary} !important;
        font-weight: 600;
        letter-spacing: -0.015em;
    }}

    p, span, label, div {{
        color: {text_primary};
    }}

    .rr-muted {{
        color: {text_muted} !important;
    }}

    .rr-secondary-text {{
        color: {text_secondary} !important;
    }}

    /* Card System */
    .rr-card {{
        background-color: {bg_card};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s ease;
    }}

    .rr-card:hover {{
        border-color: {border_light};
    }}

    .rr-hero-banner {{
        background: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.75rem;
    }}

    /* Badge & Tag Elements */
    .rr-badge {{
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }}

    .rr-badge-easy {{
        background-color: {badge_easy_bg};
        color: {badge_easy_text};
        border: 1px solid {badge_easy_text}40;
    }}

    .rr-badge-medium {{
        background-color: {badge_med_bg};
        color: {badge_med_text};
        border: 1px solid {badge_med_text}40;
    }}

    .rr-badge-hard {{
        background-color: {badge_hard_bg};
        color: {badge_hard_text};
        border: 1px solid {badge_hard_text}40;
    }}

    .rr-tag {{
        display: inline-block;
        background-color: {tag_bg};
        color: {tag_text};
        padding: 0.2rem 0.55rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid {border_color};
    }}

    .rr-accent-tag {{
        display: inline-block;
        background-color: {accent_subtle};
        color: {accent};
        padding: 0.2rem 0.55rem;
        border-radius: 4px;
        font-size: 0.78rem;
        font-weight: 600;
        border: 1px solid {accent}40;
    }}

    /* Decision Trace Timeline */
    .rr-trace-container {{
        background-color: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 1.25rem;
        margin-top: 1rem;
    }}

    .rr-trace-step {{
        display: flex;
        gap: 1rem;
        padding: 0.85rem 0;
        border-bottom: 1px solid {border_color};
    }}

    .rr-trace-step:last-child {{
        border-bottom: none;
    }}

    .rr-step-number {{
        flex-shrink: 0;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        background-color: {accent_subtle};
        color: {accent};
        border: 1px solid {accent}80;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
    }}

    .rr-step-content {{
        flex-grow: 1;
    }}

    .rr-step-header {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.25rem;
    }}

    .rr-step-stage {{
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.05em;
        color: {accent};
    }}

    .rr-step-action {{
        font-size: 0.92rem;
        font-weight: 600;
        color: {text_primary};
        margin-bottom: 0.15rem;
    }}

    .rr-step-result {{
        font-size: 0.86rem;
        color: {text_secondary};
    }}

    /* Streamlit Widgets Theming Overrides */
    div[data-baseweb="select"] > div {{
        background-color: {bg_surface} !important;
        border-color: {border_color} !important;
        color: {text_primary} !important;
    }}

    div[data-baseweb="input"] {{
        background-color: {bg_surface} !important;
        border-color: {border_color} !important;
    }}

    input.st-ai, input.st-aj, input.st-ak, input.st-al, input.st-am, input.st-an, input.st-ao, input.st-ap {{
        color: {text_primary} !important;
    }}

    div[data-testid="stForm"] {{
        background-color: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 1.5rem;
    }}

    .stButton > button {{
        border-radius: 6px;
        font-weight: 600;
        letter-spacing: 0.01em;
        transition: all 0.15s ease-in-out;
    }}

    .stButton > button[kind="primary"] {{
        background-color: {accent} !important;
        color: #ffffff !important;
        border: none !important;
    }}

    .stButton > button[kind="primary"]:hover {{
        background-color: {accent_hover} !important;
    }}

    .stButton > button[kind="secondary"] {{
        background-color: {bg_surface_alt} !important;
        color: {text_primary} !important;
        border: 1px solid {border_color} !important;
    }}

    /* Streamlit Expander */
    [data-testid="stExpander"] {{
        background-color: {bg_surface} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
        margin-bottom: 0.75rem;
    }}

    /* Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        border-bottom: 1px solid {border_color};
    }}

    .stTabs [data-baseweb="tab"] {{
        padding: 8px 16px;
        border-radius: 4px 4px 0 0;
        font-weight: 500;
        color: {text_secondary} !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: {accent} !important;
        border-bottom: 2px solid {accent} !important;
        font-weight: 600;
    }}

    /* Code block */
    code, pre {{
        background-color: {code_bg} !important;
        color: {text_primary} !important;
        border-radius: 4px;
        border: 1px solid {border_color};
    }}
    </style>
    """
    return css

