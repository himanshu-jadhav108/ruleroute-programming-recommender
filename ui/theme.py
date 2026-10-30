"""
Theme and styling definitions for RuleRoute.
Provides responsive, high-contrast, developer-oriented Light and Dark palettes
with mobile-first adaptive layout rules, touch accessibility, and fluid typography.
"""

def get_theme_css(theme: str = "Light") -> str:
    """
    Generate responsive CSS stylesheet based on selected theme mode.

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
        border_light = "#334155"
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
        shadow_card = "0 1px 3px rgba(0, 0, 0, 0.3)"
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
        shadow_card = "0 1px 3px rgba(0, 0, 0, 0.04)"

    css = f"""
    <style>
    /* -------------------------------------------------------------
       1. Base & Viewport Reset (Horizontal Overflow Prevention)
       ------------------------------------------------------------- */
    *, *::before, *::after {{
        box-sizing: border-box;
    }}

    html, body {{
        width: 100% !important;
        max-width: 100vw !important;
        overflow-x: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: {bg_page} !important;
        color: {text_primary} !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        width: 100% !important;
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }}

    [data-testid="stHeader"] {{
        background-color: {bg_page} !important;
    }}

    .main .block-container {{
        max-width: 1040px !important;
        width: 100% !important;
        padding-top: 1rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: clamp(0.75rem, 3.5vw, 1.75rem) !important;
        padding-right: clamp(0.75rem, 3.5vw, 1.75rem) !important;
        box-sizing: border-box !important;
        overflow-x: hidden !important;
    }}

    /* -------------------------------------------------------------
       2. Fluid Responsive Typography
       ------------------------------------------------------------- */
    h1 {{
        font-size: clamp(1.35rem, 4.5vw, 1.85rem) !important;
        color: {text_primary} !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.25 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }}

    h2 {{
        font-size: clamp(1.18rem, 3.8vw, 1.45rem) !important;
        color: {text_primary} !important;
        font-weight: 600 !important;
        letter-spacing: -0.015em !important;
        line-height: 1.3 !important;
    }}

    h3 {{
        font-size: clamp(1.05rem, 3.2vw, 1.25rem) !important;
        color: {text_primary} !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.35 !important;
    }}

    h4 {{
        font-size: clamp(0.92rem, 2.5vw, 1.05rem) !important;
        color: {text_primary} !important;
        font-weight: 600 !important;
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

    /* -------------------------------------------------------------
       3. Header & Brand Adaptivity
       ------------------------------------------------------------- */
    .rr-brand-group {{
        display: flex;
        align-items: center;
        gap: clamp(0.5rem, 2vw, 0.75rem);
        min-width: 0;
    }}

    .rr-brand-icon {{
        width: clamp(30px, 4vw, 38px);
        height: clamp(30px, 4vw, 38px);
        object-fit: contain;
        flex-shrink: 0;
        display: block;
    }}

    .rr-brand-meta {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-width: 0;
    }}

    .rr-brand-title-row {{
        display: flex;
        align-items: baseline;
        gap: 0.5rem;
        line-height: 1.2;
    }}

    .rr-brand-name {{
        font-weight: 700;
        font-size: clamp(1.15rem, 3.5vw, 1.45rem);
        letter-spacing: -0.02em;
        white-space: nowrap;
    }}

    .rr-brand-tagline {{
        font-size: clamp(0.76rem, 1.8vw, 0.86rem);
        color: {text_muted};
        margin-top: 0.15rem;
        line-height: 1.25;
        white-space: normal;
    }}

    /* Hide decorative tagline on small screens to avoid header crowding */
    @media (max-width: 520px) {{
        .rr-brand-tagline {{
            display: none !important;
        }}
        .rr-brand-tag {{
            display: none !important;
        }}
    }}

    /* Header row: lock brand left & theme selector right on all viewports */
    .main [data-testid="stHorizontalBlock"]:first-of-type {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }}

    .main [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="column"]:first-child {{
        min-width: 0 !important;
        flex: 1 1 auto !important;
    }}

    .main [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="column"]:last-child {{
        min-width: 105px !important;
        max-width: 130px !important;
        flex: 0 0 115px !important;
    }}

    /* -------------------------------------------------------------
       4. Card & Container System
       ------------------------------------------------------------- */
    .rr-card {{
        background-color: {bg_card};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: clamp(0.85rem, 2.5vw, 1.25rem) clamp(0.95rem, 3vw, 1.5rem);
        margin-bottom: 0.85rem;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: {shadow_card};
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        overflow-wrap: break-word;
        word-break: break-word;
    }}

    .rr-card:hover {{
        border-color: {border_light};
    }}

    .rr-hero-banner {{
        background: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: clamp(1rem, 3.2vw, 1.75rem) clamp(1rem, 3.8vw, 2rem);
        margin-bottom: 1.5rem;
        box-shadow: {shadow_card};
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }}

    .rr-hero-banner h2 {{
        margin: 0 0 0.5rem 0 !important;
    }}

    .rr-hero-banner p {{
        font-size: clamp(0.86rem, 2vw, 0.94rem);
        line-height: 1.55;
        margin: 0 0 0.6rem 0;
    }}

    /* -------------------------------------------------------------
       5. Badges & Tags
       ------------------------------------------------------------- */
    .rr-badge {{
        display: inline-block;
        padding: 0.22rem 0.55rem;
        border-radius: 4px;
        font-size: clamp(0.72rem, 1.8vw, 0.78rem);
        font-weight: 600;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
        white-space: nowrap;
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
        padding: 0.22rem 0.55rem;
        border-radius: 4px;
        font-size: clamp(0.72rem, 1.8vw, 0.8rem);
        font-weight: 500;
        border: 1px solid {border_color};
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
        white-space: normal;
        overflow-wrap: break-word;
    }}

    .rr-accent-tag {{
        display: inline-block;
        background-color: {accent_subtle};
        color: {accent};
        padding: 0.22rem 0.55rem;
        border-radius: 4px;
        font-size: clamp(0.72rem, 1.8vw, 0.78rem);
        font-weight: 600;
        border: 1px solid {accent}40;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
        white-space: normal;
    }}

    /* -------------------------------------------------------------
       6. Decision Trace Timeline
       ------------------------------------------------------------- */
    .rr-trace-container {{
        background-color: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: clamp(0.85rem, 2.5vw, 1.25rem);
        margin-top: 0.85rem;
        width: 100%;
        box-sizing: border-box;
    }}

    .rr-trace-step {{
        display: flex;
        gap: clamp(0.65rem, 2.5vw, 1rem);
        padding: 0.85rem 0;
        border-bottom: 1px solid {border_color};
        align-items: flex-start;
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
        font-size: 0.78rem;
        font-weight: 700;
        margin-top: 0.15rem;
    }}

    .rr-step-content {{
        flex-grow: 1;
        min-width: 0;
        overflow-wrap: break-word;
        word-break: break-word;
    }}

    .rr-step-header {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: 0.5rem;
        margin-bottom: 0.25rem;
        flex-wrap: wrap;
    }}

    .rr-step-stage {{
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.05em;
        color: {accent};
    }}

    .rr-step-action {{
        font-size: clamp(0.86rem, 2vw, 0.92rem);
        font-weight: 600;
        color: {text_primary};
        margin-bottom: 0.2rem;
    }}

    .rr-step-result {{
        font-size: clamp(0.8rem, 1.8vw, 0.86rem);
        color: {text_secondary};
        line-height: 1.45;
    }}

    /* -------------------------------------------------------------
       7. Responsive Pipeline Grid (Stage Cards)
       ------------------------------------------------------------- */
    .rr-stage-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 0.75rem;
        width: 100%;
        margin-bottom: 1.25rem;
    }}

    /* -------------------------------------------------------------
       8. Touch-Friendly Controls & Streamlit Overrides
       ------------------------------------------------------------- */
    /* Selectboxes */
    div[data-baseweb="select"] > div {{
        background-color: {bg_surface} !important;
        border-color: {border_color} !important;
        color: {text_primary} !important;
        min-height: 44px !important;
        border-radius: 6px !important;
    }}

    div[data-baseweb="select"] * {{
        color: {text_primary} !important;
    }}

    /* Inputs */
    div[data-baseweb="input"] {{
        background-color: {bg_surface} !important;
        border-color: {border_color} !important;
        min-height: 44px !important;
        border-radius: 6px !important;
    }}

    div[data-baseweb="input"] input {{
        min-height: 44px !important;
        font-size: 0.92rem !important;
        color: {text_primary} !important;
    }}

    /* Dropdown Popovers */
    div[data-baseweb="popover"] > div {{
        background-color: {bg_surface} !important;
        border: 1px solid {border_color} !important;
    }}

    div[data-baseweb="popover"] li {{
        background-color: {bg_surface} !important;
        color: {text_primary} !important;
    }}

    div[data-baseweb="popover"] li:hover {{
        background-color: {accent_subtle} !important;
        color: {accent} !important;
    }}

    /* Form Container */
    div[data-testid="stForm"] {{
        background-color: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: clamp(0.9rem, 2.5vw, 1.5rem);
        width: 100%;
        box-sizing: border-box;
    }}

    /* Buttons (44px min touch target) */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button {{
        min-height: 44px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: clamp(0.85rem, 2vw, 0.92rem) !important;
        letter-spacing: 0.01em !important;
        padding: 0.5rem 1rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.15s ease-in-out !important;
    }}

    .stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button[kind="primary"] {{
        background-color: {accent} !important;
        color: #ffffff !important;
        border: none !important;
    }}

    .stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {{
        background-color: {accent_hover} !important;
    }}

    .stButton > button[kind="secondary"],
    div[data-testid="stFormSubmitButton"] > button[kind="secondary"] {{
        background-color: {bg_surface_alt} !important;
        color: {text_primary} !important;
        border: 1px solid {border_color} !important;
    }}

    /* Download Buttons */
    .stDownloadButton > button {{
        min-height: 44px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: clamp(0.82rem, 1.8vw, 0.88rem) !important;
        padding: 0.5rem 0.85rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: normal !important;
        line-height: 1.3 !important;
    }}

    /* Expanders */
    [data-testid="stExpander"] {{
        background-color: {bg_surface} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
        margin-bottom: 0.75rem !important;
        width: 100% !important;
        overflow-wrap: break-word !important;
    }}

    [data-testid="stExpander"] details summary {{
        min-height: 44px !important;
        display: flex !important;
        align-items: center !important;
    }}

    /* Tabs (Scrollable on small screens, no overflow) */
    .stTabs [data-baseweb="tab-list"] {{
        display: flex !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: none !important;
        gap: 4px !important;
        border-bottom: 1px solid {border_color} !important;
        width: 100% !important;
        max-width: 100% !important;
        padding-bottom: 1px !important;
    }}

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
        display: none !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        min-height: 44px !important;
        padding: 8px clamp(10px, 2.5vw, 16px) !important;
        border-radius: 4px 4px 0 0 !important;
        font-weight: 500 !important;
        color: {text_secondary} !important;
        white-space: nowrap !important;
        flex-shrink: 0 !important;
        font-size: clamp(0.82rem, 2vw, 0.9rem) !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: {accent} !important;
        border-bottom: 2px solid {accent} !important;
        font-weight: 600 !important;
    }}

    /* Code & Pre */
    code, pre {{
        background-color: {code_bg} !important;
        color: {text_primary} !important;
        border-radius: 4px;
        border: 1px solid {border_color};
        max-width: 100% !important;
        overflow-x: auto !important;
        word-break: break-word !important;
    }}

    /* -------------------------------------------------------------
       9. Media Queries: Mobile & Tablet Column Stacking
       ------------------------------------------------------------- */
    /* Narrow screens: small & standard smartphones (320px - 640px) */
    @media (max-width: 640px) {{
        /* Stack all content columns (forms, demo buttons, filters, history, actions) */
        .main [data-testid="stHorizontalBlock"]:not(:first-of-type) {{
            flex-wrap: wrap !important;
            gap: 0.5rem !important;
        }}

        .main [data-testid="stHorizontalBlock"]:not(:first-of-type) > [data-testid="column"] {{
            min-width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 0.25rem !important;
        }}

        /* Buttons expand to full width on mobile for easy tapping */
        .stButton > button,
        div[data-testid="stFormSubmitButton"] > button,
        .stDownloadButton > button {{
            width: 100% !important;
        }}

        /* Adjust trace spacing for compact mobile view */
        .rr-trace-step {{
            gap: 0.65rem !important;
            padding: 0.75rem 0 !important;
        }}

        .rr-step-number {{
            width: 24px !important;
            height: 24px !important;
            font-size: 0.75rem !important;
        }}
    }}

    /* Tablet screens (641px - 860px) */
    @media (min-width: 641px) and (max-width: 860px) {{
        .main [data-testid="stHorizontalBlock"]:not(:first-of-type) {{
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
        }}
    }}
    </style>
    """
    return css
