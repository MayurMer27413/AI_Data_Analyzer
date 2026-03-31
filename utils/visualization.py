"""
Visualization Utilities — AI Data Analyzer
Generates Plotly charts styled to match the application's design system.
"""
import plotly.express as px


# ---------------------------------------------------------------------------
# Design-aligned chart defaults
# ---------------------------------------------------------------------------
_FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"

_COLOR_SEQUENCE = [
    "#4F46E5",  # indigo
    "#059669",  # emerald
    "#D97706",  # amber
    "#E11D48",  # rose
    "#0284C7",  # sky
    "#7C3AED",  # violet
    "#EA580C",  # orange
    "#0D9488",  # teal
    "#BE185D",  # pink
    "#1D4ED8",  # blue
]

_CHART_LAYOUT = dict(
    template="plotly_white",
    font=dict(family=_FONT_FAMILY, size=13, color="#334155"),
    title_font=dict(family=_FONT_FAMILY, size=15, color="#0F172A"),
    margin=dict(t=48, l=8, r=8, b=8),
    paper_bgcolor="rgba(255,255,255,1)",
    plot_bgcolor="rgba(255,255,255,1)",
    legend=dict(
        font=dict(size=12),
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
    ),
    colorway=_COLOR_SEQUENCE,
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family=_FONT_FAMILY,
    ),
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_custom_chart(df, chart_type, x_col, y_col, color_col=None):
    """Generates a Plotly figure for the given chart type and column mapping."""

    if chart_type == "Bar Chart (Horizontal)":
        fig = px.histogram(df, y=x_col, x=y_col, color=color_col,
                           orientation='h', histfunc='sum',
                           title=f"Horizontal Bar: {y_col} vs {x_col}",
                           color_discrete_sequence=_COLOR_SEQUENCE)

    elif chart_type == "Column Chart (Vertical)":
        fig = px.histogram(df, x=x_col, y=y_col, color=color_col,
                           orientation='v', histfunc='sum',
                           title=f"Column Chart: {y_col} vs {x_col}",
                           color_discrete_sequence=_COLOR_SEQUENCE)

    elif chart_type == "Stacked Bar Chart":
        fig = px.histogram(df, y=x_col, x=y_col, color=color_col,
                           orientation='h', barmode='relative', histfunc='sum',
                           title=f"Stacked Bar: {y_col} vs {x_col}",
                           color_discrete_sequence=_COLOR_SEQUENCE)

    elif chart_type == "Stacked Column Chart":
        fig = px.histogram(df, x=x_col, y=y_col, color=color_col,
                           orientation='v', barmode='relative', histfunc='sum',
                           title=f"Stacked Column: {y_col} vs {x_col}",
                           color_discrete_sequence=_COLOR_SEQUENCE)

    elif chart_type == "Clustered Column Chart":
        fig = px.histogram(df, x=x_col, y=y_col, color=color_col,
                           orientation='v', barmode='group', histfunc='sum',
                           title=f"Clustered Column: {y_col} vs {x_col}",
                           color_discrete_sequence=_COLOR_SEQUENCE)

    elif chart_type == "Clustered Bar Chart":
        fig = px.histogram(df, y=x_col, x=y_col, color=color_col,
                           orientation='h', barmode='group', histfunc='sum',
                           title=f"Clustered Bar: {y_col} vs {x_col}",
                           color_discrete_sequence=_COLOR_SEQUENCE)

    elif chart_type == "Pie Chart":
        fig = px.pie(df, names=x_col, values=y_col,
                     title=f"Pie Chart of {y_col} by {x_col}",
                     color_discrete_sequence=_COLOR_SEQUENCE)

    elif chart_type == "Donut Chart":
        fig = px.pie(df, names=x_col, values=y_col, hole=0.55,
                     title=f"Donut Chart of {y_col} by {x_col}",
                     color_discrete_sequence=_COLOR_SEQUENCE)

    elif chart_type == "Line Chart":
        groupby_cols = [x_col]
        if color_col:
            groupby_cols.append(color_col)
        agg_df = df.groupby(groupby_cols, as_index=False)[y_col].sum()
        fig = px.line(agg_df, x=x_col, y=y_col, color=color_col,
                      title=f"Line Chart: {y_col} vs {x_col}",
                      color_discrete_sequence=_COLOR_SEQUENCE)

    elif chart_type == "Heat Map (2D Density)":
        fig = px.density_heatmap(df, x=x_col, y=y_col,
                                 title=f"Heat Map: {y_col} vs {x_col}",
                                 color_continuous_scale="Viridis")
    else:
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                         title=f"{y_col} vs {x_col}",
                         color_discrete_sequence=_COLOR_SEQUENCE)

    fig.update_layout(**_CHART_LAYOUT)
    return fig


def plot_heatmap(corr_df):
    """Generates a styled correlation heatmap."""
    fig = px.imshow(
        corr_df,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        title="Correlation Heatmap",
    )
    fig.update_layout(
        font=dict(family=_FONT_FAMILY, size=13, color="#334155"),
        title_font=dict(family=_FONT_FAMILY, size=15, color="#0F172A"),
        margin=dict(t=48, l=8, r=8, b=8),
        paper_bgcolor="rgba(255,255,255,1)",
        plot_bgcolor="rgba(255,255,255,1)",
    )
    return fig
