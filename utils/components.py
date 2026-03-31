"""
Reusable UI Components — AI Data Analyzer
Provides HTML component helpers that render premium, design-system-aligned markup.

IMPORTANT: All HTML strings are left-aligned (no leading spaces) to prevent
Streamlit from interpreting them as markdown code blocks.
"""


def stat_card(value, label, icon="📊", variant="indigo"):
    """Renders an animated stat card with a colored top accent bar."""
    return (
        f'<div class="stat-card {variant} animate-in">'
        f'<span class="stat-icon">{icon}</span>'
        f'<div class="stat-value">{value}</div>'
        f'<div class="stat-label">{label}</div>'
        f'</div>'
    )


def section_header(title, subtitle=""):
    """Renders a consistent section header with optional subtitle."""
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    return (
        f'<div class="section-header animate-in">'
        f'<h2>{title}</h2>'
        f'{sub}'
        f'</div>'
    )


def empty_state(icon, title, description=""):
    """Renders an elegant empty-state placeholder."""
    desc = f'<div class="empty-desc">{description}</div>' if description else ""
    return (
        f'<div class="empty-state animate-in">'
        f'<span class="empty-icon">{icon}</span>'
        f'<div class="empty-title">{title}</div>'
        f'{desc}'
        f'</div>'
    )


def top_bar(title, subtitle="", badge_text="", badge_icon=""):
    """Renders a top navigation bar with title and optional badge."""
    badge = ""
    if badge_text:
        badge = f'<div class="top-bar-badge">{badge_icon} {badge_text}</div>'
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    return (
        f'<div class="top-bar animate-in">'
        f'<div class="top-bar-left"><h1>{title}</h1>{sub}</div>'
        f'{badge}'
        f'</div>'
    )


def download_button(href, label="Download", icon="📥"):
    """Renders a styled download link."""
    return (
        f'<a href="{href}" download="AI_Data_Analyzer_Report.pdf" '
        f'class="download-btn">{icon} {label}</a>'
    )


def hero_section():
    """Renders the premium landing page hero section."""
    return (
        '<div class="hero animate-in">'
        '<div class="hero-badge">AI-POWERED ANALYTICS</div>'
        '<h1>Turn Raw Data Into<br/>Actionable Intelligence</h1>'
        '<p class="hero-sub">Upload any dataset and let AI handle the heavy lifting '
        '— automated EDA, intelligent visualizations, and deep business insights in seconds.</p>'
        '</div>'
    )


def feature_card(icon, title, description, color="indigo"):
    """Renders a single feature card for the landing page grid."""
    return (
        f'<div class="feature-card">'
        f'<div class="feature-icon {color}">{icon}</div>'
        f'<div class="feature-title">{title}</div>'
        f'<p class="feature-desc">{description}</p>'
        f'</div>'
    )


def feature_grid(cards_html):
    """Wraps multiple feature-card HTML strings in a responsive grid."""
    return f'<div class="feature-grid stagger">{cards_html}</div>'
