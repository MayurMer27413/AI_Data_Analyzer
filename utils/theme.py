"""
Design System — AI Data Analyzer
Centralized theme containing all CSS variables, component styles, and layout rules.
"""
import streamlit as st


def inject_theme():
    """Injects the complete design-system CSS into the Streamlit page. Call once at app start."""
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(_THEME_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Master stylesheet
# ---------------------------------------------------------------------------
_THEME_CSS = """
<style>
/* ======================================================================
   0. CSS VARIABLES — single source of truth
   ====================================================================== */
:root {
    /* --- Palette (Indigo / Slate) --- */
    --color-primary:        #4F46E5;
    --color-primary-hover:  #4338CA;
    --color-primary-light:  #EEF2FF;
    --color-primary-subtle: #C7D2FE;

    --color-surface:        #FFFFFF;
    --color-surface-alt:    #F8FAFC;
    --color-surface-hover:  #F1F5F9;

    --color-border:         #E2E8F0;
    --color-border-light:   #F1F5F9;

    --color-text:           #0F172A;
    --color-text-secondary: #64748B;
    --color-text-muted:     #94A3B8;
    --color-text-on-primary:#FFFFFF;

    --color-success:        #059669;
    --color-success-bg:     #ECFDF5;
    --color-warning:        #D97706;
    --color-warning-bg:     #FFFBEB;
    --color-danger:         #DC2626;
    --color-danger-bg:      #FEF2F2;
    --color-info:           #0284C7;
    --color-info-bg:        #F0F9FF;

    /* --- Typography --- */
    --font-family:          'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-size-xs:         0.75rem;   /* 12px */
    --font-size-sm:         0.8125rem; /* 13px */
    --font-size-base:       0.875rem;  /* 14px */
    --font-size-md:         1rem;      /* 16px */
    --font-size-lg:         1.125rem;  /* 18px */
    --font-size-xl:         1.5rem;    /* 24px */
    --font-size-2xl:        1.875rem;  /* 30px */
    --font-size-3xl:        2.25rem;   /* 36px */

    /* --- Spacing (8px grid) --- */
    --space-1:  0.25rem;  /* 4px  */
    --space-2:  0.5rem;   /* 8px  */
    --space-3:  0.75rem;  /* 12px */
    --space-4:  1rem;     /* 16px */
    --space-5:  1.25rem;  /* 20px */
    --space-6:  1.5rem;   /* 24px */
    --space-8:  2rem;     /* 32px */
    --space-10: 2.5rem;   /* 40px */
    --space-12: 3rem;     /* 48px */

    /* --- Radii --- */
    --radius-sm:  6px;
    --radius-md:  10px;
    --radius-lg:  14px;
    --radius-xl:  20px;
    --radius-full:9999px;

    /* --- Shadows --- */
    --shadow-xs:  0 1px 2px rgba(0,0,0,0.04);
    --shadow-sm:  0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md:  0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
    --shadow-lg:  0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);
    --shadow-xl:  0 20px 25px -5px rgba(0,0,0,0.08), 0 8px 10px -6px rgba(0,0,0,0.04);

    /* --- Transitions --- */
    --transition-fast:   150ms cubic-bezier(.4,0,.2,1);
    --transition-normal: 250ms cubic-bezier(.4,0,.2,1);
    --transition-slow:   350ms cubic-bezier(.4,0,.2,1);
}

/* ======================================================================
   1. GLOBAL RESET & BASE
   ====================================================================== */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
[data-testid="stMain"],
.stApp {
    font-family: var(--font-family) !important;
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Force white on inner content areas */
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],
.main, .block-container {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}

/* Streamlit main container */
.main .block-container {
    max-width: 1200px;
    padding: var(--space-8) var(--space-6) var(--space-12) var(--space-6);
}

/* All text elements should be dark on white */
p, li, span, div, label,
[data-testid="stMarkdownContainer"] * {
    color: #0F172A;
}

/* Muted/secondary text */
.text-muted, small, caption {
    color: #64748B !important;
}

/* ======================================================================
   2. TYPOGRAPHY
   ====================================================================== */
h1, h2, h3, h4, h5, h6,
[data-testid="stHeading"] {
    font-family: var(--font-family) !important;
    color: var(--color-text) !important;
    letter-spacing: -0.02em;
}
h1, [data-testid="stHeading"] h1 { font-size: var(--font-size-2xl) !important; font-weight: 800 !important; }
h2, [data-testid="stHeading"] h2 { font-size: var(--font-size-xl)  !important; font-weight: 700 !important; }
h3, [data-testid="stHeading"] h3 { font-size: var(--font-size-lg)  !important; font-weight: 600 !important; }

p, li, span, label, div {
    font-family: var(--font-family) !important;
}

/* ======================================================================
   3. SIDEBAR
   ====================================================================== */
section[data-testid="stSidebar"] {
    background: var(--color-surface) !important;
    border-right: 1px solid var(--color-border) !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding: var(--space-6) var(--space-5) !important;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-size: var(--font-size-sm) !important;
    font-weight: 600 !important;
    color: var(--color-text-secondary) !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: var(--space-3);
}

/* Sidebar dividers */
section[data-testid="stSidebar"] hr {
    border: none;
    border-top: 1px solid var(--color-border-light);
    margin: var(--space-5) 0;
}

/* ======================================================================
   4. BUTTONS
   ====================================================================== */
.stButton > button,
button[kind="primary"],
button[kind="secondary"] {
    font-family: var(--font-family) !important;
    font-weight: 600 !important;
    font-size: var(--font-size-sm) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.55rem 1.25rem !important;
    border: 1px solid transparent !important;
    transition: all var(--transition-fast) !important;
    cursor: pointer !important;
    letter-spacing: 0.01em;
}

/* Primary buttons */
.stButton > button[kind="primary"],
.stButton > button {
    background: var(--color-primary) !important;
    color: var(--color-text-on-primary) !important;
    box-shadow: var(--shadow-xs) !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button:hover {
    background: var(--color-primary-hover) !important;
    box-shadow: var(--shadow-sm) !important;
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0);
    box-shadow: var(--shadow-xs) !important;
}

/* Secondary / outline look for form submit */
.stFormSubmitButton > button {
    background: var(--color-primary) !important;
    color: var(--color-text-on-primary) !important;
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    transition: all var(--transition-fast) !important;
}
.stFormSubmitButton > button:hover {
    background: var(--color-primary-hover) !important;
    transform: translateY(-1px);
}

/* ======================================================================
   5. INPUTS & SELECTS
   ====================================================================== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    font-family: var(--font-family) !important;
    font-size: var(--font-size-base) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--color-border) !important;
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--color-primary) !important;
    box-shadow: 0 0 0 3px var(--color-primary-light) !important;
}

/* Labels */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stMultiSelect label,
.stSlider label,
.stCheckbox label,
.stRadio label {
    font-family: var(--font-family) !important;
    font-size: var(--font-size-sm) !important;
    font-weight: 500 !important;
    color: var(--color-text-secondary) !important;
}

/* ======================================================================
   6. FILE UPLOADER
   ====================================================================== */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--color-border) !important;
    border-radius: var(--radius-lg) !important;
    background: var(--color-surface-alt) !important;
    transition: border-color var(--transition-fast), background var(--transition-fast) !important;
    padding: var(--space-4) !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--color-primary-subtle) !important;
    background: var(--color-primary-light) !important;
}

/* ======================================================================
   7. TABS
   ====================================================================== */
.stTabs [data-baseweb="tab-list"] {
    gap: var(--space-1);
    border-bottom: 2px solid var(--color-border-light);
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-family) !important;
    font-size: var(--font-size-sm) !important;
    font-weight: 500;
    color: var(--color-text-secondary);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md) var(--radius-md) 0 0;
    border-bottom: 2px solid transparent;
    transition: all var(--transition-fast);
    margin-bottom: -2px;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--color-primary);
    background: var(--color-primary-light);
}
.stTabs [aria-selected="true"] {
    color: var(--color-primary) !important;
    font-weight: 600 !important;
    border-bottom-color: var(--color-primary) !important;
    background: transparent !important;
}

/* ======================================================================
   8. DATAFRAMES & TABLES
   ====================================================================== */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden;
}

/* ======================================================================
   9. EXPANDER
   ====================================================================== */
[data-testid="stExpander"] {
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden;
    transition: box-shadow var(--transition-fast);
}
[data-testid="stExpander"]:hover {
    box-shadow: var(--shadow-sm);
}
[data-testid="stExpander"] summary {
    font-family: var(--font-family) !important;
    font-weight: 600;
    font-size: var(--font-size-base);
    padding: var(--space-4) var(--space-5);
}

/* ======================================================================
   10. ALERTS & STATUS
   ====================================================================== */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: var(--radius-md) !important;
    font-family: var(--font-family) !important;
    font-size: var(--font-size-sm) !important;
}

/* ======================================================================
   11. CHAT MESSAGES
   ====================================================================== */
[data-testid="stChatMessage"] {
    border-radius: var(--radius-lg) !important;
    border: 1px solid var(--color-border) !important;
    padding: var(--space-4) var(--space-5) !important;
    margin-bottom: var(--space-3) !important;
    box-shadow: var(--shadow-xs);
    transition: box-shadow var(--transition-fast);
}
[data-testid="stChatMessage"]:hover {
    box-shadow: var(--shadow-sm);
}

[data-testid="stChatInput"] > div {
    border-radius: var(--radius-lg) !important;
    border: 1px solid var(--color-border) !important;
    transition: border-color var(--transition-fast) !important;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--color-primary) !important;
    box-shadow: 0 0 0 3px var(--color-primary-light) !important;
}

/* ======================================================================
   12. METRICS
   ====================================================================== */
[data-testid="stMetric"] {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-5);
    box-shadow: var(--shadow-xs);
}
[data-testid="stMetric"] label {
    font-size: var(--font-size-sm) !important;
    color: var(--color-text-secondary) !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ======================================================================
   13. CUSTOM COMPONENT CLASSES
   ====================================================================== */

/* --- Stat Cards --- */
.stat-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    text-align: center;
    transition: transform var(--transition-fast), box-shadow var(--transition-fast);
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--color-primary);
    opacity: 0;
    transition: opacity var(--transition-fast);
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
.stat-card:hover::before {
    opacity: 1;
}
.stat-card .stat-icon {
    font-size: 1.5rem;
    margin-bottom: var(--space-2);
    display: block;
}
.stat-card .stat-value {
    font-size: var(--font-size-2xl);
    font-weight: 800;
    color: var(--color-text);
    margin: var(--space-1) 0;
    letter-spacing: -0.03em;
    line-height: 1.2;
}
.stat-card .stat-label {
    font-size: var(--font-size-xs);
    font-weight: 600;
    color: var(--color-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Color variants for top bar */
.stat-card.indigo::before  { background: #4F46E5; opacity: 1; }
.stat-card.emerald::before { background: #059669; opacity: 1; }
.stat-card.amber::before   { background: #D97706; opacity: 1; }
.stat-card.rose::before    { background: #E11D48; opacity: 1; }
.stat-card.sky::before     { background: #0284C7; opacity: 1; }

/* --- Section Header --- */
.section-header {
    margin-bottom: var(--space-6);
    padding-bottom: var(--space-4);
    border-bottom: 1px solid var(--color-border-light);
}
.section-header h2 {
    margin: 0 0 var(--space-1) 0;
    font-size: var(--font-size-xl) !important;
    font-weight: 700 !important;
    color: var(--color-text) !important;
}
.section-header p {
    margin: 0;
    font-size: var(--font-size-base);
    color: var(--color-text-secondary);
    line-height: 1.5;
}

/* --- Empty State --- */
.empty-state {
    text-align: center;
    padding: var(--space-12) var(--space-8);
    color: var(--color-text-muted);
}
.empty-state .empty-icon {
    font-size: 3rem;
    margin-bottom: var(--space-4);
    display: block;
    opacity: 0.5;
}
.empty-state .empty-title {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--color-text-secondary);
    margin-bottom: var(--space-2);
}
.empty-state .empty-desc {
    font-size: var(--font-size-base);
    color: var(--color-text-muted);
    max-width: 400px;
    margin: 0 auto;
    line-height: 1.6;
}

/* --- Top Bar --- */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-4) 0;
    margin-bottom: var(--space-6);
    border-bottom: 1px solid var(--color-border-light);
}
.top-bar .top-bar-left h1 {
    margin: 0 !important;
    font-size: var(--font-size-2xl) !important;
    font-weight: 800 !important;
}
.top-bar .top-bar-left p {
    margin: var(--space-1) 0 0 0;
    font-size: var(--font-size-base);
    color: var(--color-text-secondary);
}
.top-bar .top-bar-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
    background: var(--color-success-bg);
    color: var(--color-success);
    border-radius: var(--radius-full);
    font-size: var(--font-size-xs);
    font-weight: 600;
}

/* --- Feature Cards (Landing Page) --- */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: var(--space-5);
    margin-top: var(--space-6);
}
.feature-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    transition: transform var(--transition-fast), box-shadow var(--transition-fast), border-color var(--transition-fast);
}
.feature-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
    border-color: var(--color-primary-subtle);
}
.feature-card .feature-icon {
    width: 44px;
    height: 44px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    margin-bottom: var(--space-4);
}
.feature-card .feature-icon.indigo  { background: #EEF2FF; }
.feature-card .feature-icon.emerald { background: #ECFDF5; }
.feature-card .feature-icon.amber   { background: #FFFBEB; }
.feature-card .feature-icon.sky     { background: #F0F9FF; }
.feature-card .feature-icon.rose    { background: #FFF1F2; }
.feature-card .feature-icon.violet  { background: #F5F3FF; }
.feature-card .feature-title {
    font-size: var(--font-size-md);
    font-weight: 600;
    color: var(--color-text);
    margin-bottom: var(--space-2);
}
.feature-card .feature-desc {
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    line-height: 1.55;
    margin: 0;
}

/* --- Hero Section --- */
.hero {
    text-align: center;
    padding: var(--space-12) var(--space-6);
}
.hero h1 {
    font-size: var(--font-size-3xl) !important;
    font-weight: 800 !important;
    color: var(--color-text) !important;
    margin-bottom: var(--space-4) !important;
    line-height: 1.15 !important;
}
.hero .hero-sub {
    font-size: var(--font-size-lg);
    color: var(--color-text-secondary);
    max-width: 560px;
    margin: 0 auto var(--space-8) auto;
    line-height: 1.6;
}
.hero .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
    background: var(--color-primary-light);
    color: var(--color-primary);
    border-radius: var(--radius-full);
    font-size: var(--font-size-xs);
    font-weight: 600;
    margin-bottom: var(--space-6);
    letter-spacing: 0.02em;
}

/* --- Download Button --- */
.download-btn {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-6);
    background: var(--color-text);
    color: var(--color-text-on-primary);
    text-decoration: none;
    border-radius: var(--radius-md);
    font-family: var(--font-family);
    font-weight: 600;
    font-size: var(--font-size-sm);
    transition: all var(--transition-fast);
    margin-top: var(--space-4);
}
.download-btn:hover {
    background: var(--color-primary);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
    color: var(--color-text-on-primary);
    text-decoration: none;
}

/* --- Plotly Charts Container --- */
[data-testid="stPlotlyChart"] {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-xs);
}

/* --- Dividers --- */
hr {
    border: none !important;
    border-top: 1px solid var(--color-border-light) !important;
    margin: var(--space-6) 0 !important;
}

/* --- Radio Group (Segmented Control look) --- */
.stRadio > div {
    gap: var(--space-2) !important;
}
.stRadio [role="radiogroup"] label {
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-md) !important;
    padding: var(--space-2) var(--space-4) !important;
    transition: all var(--transition-fast) !important;
    font-size: var(--font-size-sm) !important;
}
.stRadio [role="radiogroup"] label:hover {
    border-color: var(--color-primary-subtle) !important;
    background: var(--color-primary-light) !important;
}

/* --- Checkbox --- */
.stCheckbox label {
    font-size: var(--font-size-base) !important;
}

/* --- Slider --- */
.stSlider [data-testid="stTickBar"] {
    display: none;
}

/* --- Spinner override --- */
.stSpinner > div {
    border-color: var(--color-primary) transparent transparent transparent !important;
}

/* ======================================================================
   14. RESPONSIVE ADJUSTMENTS
   ====================================================================== */
@media (max-width: 768px) {
    .main .block-container {
        padding: var(--space-4) var(--space-3) var(--space-8) var(--space-3);
    }
    .feature-grid {
        grid-template-columns: 1fr;
    }
    .hero h1 {
        font-size: var(--font-size-xl) !important;
    }
    .stat-card .stat-value {
        font-size: var(--font-size-xl);
    }
}

/* ======================================================================
   15. ANIMATION KEYFRAMES
   ====================================================================== */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animate-in {
    animation: fadeInUp 0.4s ease-out both;
}

/* Stagger children */
.stagger > * { animation: fadeInUp 0.4s ease-out both; }
.stagger > *:nth-child(1) { animation-delay: 0.05s; }
.stagger > *:nth-child(2) { animation-delay: 0.10s; }
.stagger > *:nth-child(3) { animation-delay: 0.15s; }
.stagger > *:nth-child(4) { animation-delay: 0.20s; }
.stagger > *:nth-child(5) { animation-delay: 0.25s; }
.stagger > *:nth-child(6) { animation-delay: 0.30s; }

/* ======================================================================
   16. CHAT UI — ChatGPT / Gemini Style
   ====================================================================== */

/* Welcome screen */
.chat-welcome {
    text-align: center;
    padding: 3rem 1rem 1.5rem;
}
.chat-welcome-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    animation: fadeInUp 0.5s ease-out both;
}
.chat-welcome-title {
    font-size: 1.75rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    margin-bottom: 0.5rem !important;
    animation: fadeInUp 0.5s ease-out 0.1s both;
}
.chat-welcome-sub {
    font-size: 1rem;
    color: #64748B;
    max-width: 480px;
    margin: 0 auto 2rem;
    line-height: 1.6;
    animation: fadeInUp 0.5s ease-out 0.2s both;
}

/* Prompt chip buttons */
div[data-testid="stHorizontalBlock"] .stButton > button {
    background: #F8FAFC !important;
    color: #334155 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 0.65rem 1rem !important;
    transition: all 150ms ease !important;
    box-shadow: none !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: #EEF2FF !important;
    border-color: #C7D2FE !important;
    color: #4F46E5 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 8px rgba(79,70,229,.1) !important;
}

/* Message thread */
.chat-thread {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    padding: 0.5rem 0 1.5rem;
}
.chat-row {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    animation: fadeInUp 0.3s ease-out both;
}
.chat-row-user { flex-direction: row-reverse; }
.chat-row-ai   { flex-direction: row; }

/* Avatars */
.chat-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    font-size: 0.7rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    letter-spacing: 0.02em;
}
.chat-avatar-user { background: #4F46E5; color: #FFFFFF; }
.chat-avatar-ai   { background: #0F172A; color: #FFFFFF; }

/* Bubbles */
.chat-bubble {
    max-width: 72%;
    padding: 0.85rem 1.1rem;
    border-radius: 16px;
    font-size: 0.9rem;
    line-height: 1.6;
    word-break: break-word;
}
.chat-bubble-user {
    background: #4F46E5;
    color: #FFFFFF !important;
    border-bottom-right-radius: 4px;
}
.chat-bubble-ai {
    background: #F8FAFC;
    color: #0F172A !important;
    border: 1px solid #E2E8F0;
    border-bottom-left-radius: 4px;
}

/* Typing indicator */
.chat-typing {
    display: flex;
    align-items: center;
    gap: 5px;
    min-width: 64px;
}
.chat-typing span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #94A3B8;
    display: inline-block;
    animation: typingBounce 1.2s infinite ease-in-out;
}
.chat-typing span:nth-child(2) { animation-delay: 0.2s; }
.chat-typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
    30%            { transform: translateY(-6px); opacity: 1; }
}

</style>
"""
