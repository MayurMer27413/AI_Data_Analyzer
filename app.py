"""
AI Data Analyzer — Main Application
Premium SaaS-quality Streamlit interface for automated data analysis.
"""
import streamlit as st
import pandas as pd
import warnings
import time
import os

from utils.data_loader import load_data, get_dataset_info
from utils.eda import missing_values_summary, statistical_summary, correlation_matrix
from utils.visualization import generate_custom_chart, plot_heatmap
from utils.ai_insights import generate_insights
from utils.chat_engine import chat_with_data
from utils.theme import inject_theme
from utils.components import (
    stat_card,
    section_header,
    empty_state,
    top_bar,
    download_button,
    hero_section,
    feature_card,
    feature_grid,
)

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Page config — must be the first Streamlit command
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Data Analyzer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject the design system
inject_theme()


# ===========================================================================
# SESSION STATE INIT
# ===========================================================================
def _init_state():
    defaults = {
        "df": None,
        "file_name": None,
        "chat_history": [],
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "api_key": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ===========================================================================
# SIDEBAR
# ===========================================================================
def _render_sidebar():
    with st.sidebar:
        st.markdown(
            '<p style="font-size:1.25rem;font-weight:800;letter-spacing:-0.03em;'
            'margin-bottom:0.25rem;">✦ AI Data Analyzer</p>',
            unsafe_allow_html=True,
        )
        st.caption("Intelligent Analytics Platform")
        st.markdown("---")

        # ---- Data Upload ----
        st.markdown(
            '<p style="font-size:0.7rem;font-weight:700;color:#94A3B8;'
            'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">'
            "DATA SOURCE</p>",
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload Dataset",
            type=["csv", "xlsx", "xls"],
            label_visibility="collapsed",
        )

        if uploaded_file is not None:
            if st.session_state.file_name != uploaded_file.name:
                with st.spinner("Validating dataset…"):
                    df, error = load_data(uploaded_file)
                    if error:
                        st.error(error)
                    elif df.empty:
                        st.error("Uploaded dataset is empty.")
                    else:
                        st.session_state.df = df
                        st.session_state.file_name = uploaded_file.name
                        st.session_state.chat_history = []
                        if "insights" in st.session_state:
                            del st.session_state["insights"]
                        st.success("Dataset loaded!")

        # Show loaded file info
        if st.session_state.df is not None:
            info = get_dataset_info(st.session_state.df)
            st.markdown(
                f'<div style="background:#F8FAFC;border:1px solid #E2E8F0;'
                f'border-radius:10px;padding:12px 14px;margin-top:8px;">'
                f'<div style="font-size:0.75rem;font-weight:600;color:#0F172A;'
                f'margin-bottom:4px;">📄 {st.session_state.file_name}</div>'
                f'<div style="font-size:0.7rem;color:#64748B;">'
                f'{info["rows"]:,} rows · {info["cols"]:,} cols · '
                f'{info["missing"]:,} missing</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # ---- AI Configuration ----
        st.markdown(
            '<p style="font-size:0.7rem;font-weight:700;color:#94A3B8;'
            'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">'
            "AI CONFIGURATION</p>",
            unsafe_allow_html=True,
        )
        groq_model = st.selectbox(
            "Model",
            ["meta-llama/llama-4-scout-17b-16e-instruct"],
            index=0,
        )
        st.session_state.model = groq_model

        groq_api_key = st.text_input("Groq API Key", type="password")
        st.session_state.api_key = groq_api_key


# ===========================================================================
# LANDING PAGE (no dataset loaded)
# ===========================================================================
def _render_landing():
    st.markdown(hero_section(), unsafe_allow_html=True)

    cards = "".join([
        feature_card("📊", "Instant EDA",
                     "Automated missing-value analysis, descriptive statistics, "
                     "and correlation matrices in one click.", "indigo"),
        feature_card("📈", "Smart Visualizations",
                     "AI recommends the most insightful charts or build your own "
                     "with a drag-and-drop chart studio.", "emerald"),
        feature_card("🧠", "AI Business Insights",
                     "Leverage Groq-powered LLMs to extract KPIs, trends, "
                     "and anomalies from your data.", "amber"),
        feature_card("💬", "Chat with Data",
                     "Ask natural-language questions and get computed answers "
                     "backed by live Pandas queries.", "sky"),
        feature_card("🧪", "Evaluation Suite",
                     "Track model performance, capture user feedback, "
                     "and maintain an audit trail.", "rose"),
        feature_card("📄", "PDF Reports",
                     "Export publication-ready PDF reports combining AI insights "
                     "and selected visualizations.", "violet"),
    ])
    st.markdown(feature_grid(cards), unsafe_allow_html=True)


# ===========================================================================
# TAB: DATA PREVIEW
# ===========================================================================
def _tab_data_preview(df):
    st.markdown(
        section_header("Dataset Overview",
                       "A snapshot of your data and its structure."),
        unsafe_allow_html=True,
    )

    info = get_dataset_info(df)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(stat_card(f"{info['rows']:,}", "Total Rows", "📋", "indigo"),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(stat_card(f"{info['cols']:,}", "Columns", "📐", "emerald"),
                    unsafe_allow_html=True)
    with c3:
        st.markdown(stat_card(f"{info['missing']:,}", "Missing Cells", "⚠️", "amber"),
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df.head(100), use_container_width=True)

    with st.expander("Column Data Types"):
        st.table(df.dtypes.astype(str).to_frame(name="Data Type"))


# ===========================================================================
# TAB: AUTO EDA
# ===========================================================================
def _tab_eda(df):
    st.markdown(
        section_header("Exploratory Data Analysis",
                       "Automated statistical profiling of your dataset."),
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Missing Values")
        missing_df = missing_values_summary(df)
        if missing_df.empty:
            st.success("No missing values found.")
        else:
            st.dataframe(missing_df, use_container_width=True)

    with col2:
        st.markdown("##### Statistical Summary")
        stats_df = statistical_summary(df)
        if not stats_df.empty:
            st.dataframe(stats_df, use_container_width=True)
        else:
            st.info("No numeric columns available.")

    st.markdown("---")
    st.markdown("##### Correlation Matrix")
    corr = correlation_matrix(df)
    if not corr.empty:
        st.plotly_chart(plot_heatmap(corr), use_container_width=True)
    else:
        st.info("Not enough numeric columns for correlation.")


# ===========================================================================
# TAB: VISUALIZATIONS
# ===========================================================================
def _tab_visualizations(df):
    st.markdown(
        section_header("Interactive Visualizations",
                       "AI-generated charts or build your own with the manual studio."),
        unsafe_allow_html=True,
    )

    viz_mode = st.radio(
        "Mode",
        ["AI Auto-Generate", "Manual Chart Builder"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown("---")

    if viz_mode == "AI Auto-Generate":
        st.markdown("##### AI-Driven Auto-Visualizations")
        st.caption(
            "The AI analyzes your schema and generates the most insightful charts."
        )

        if st.button("Generate All Charts", type="primary"):
            with st.spinner(f"AI ({st.session_state.model}) is analyzing…"):
                try:
                    from utils.ai_insights import recommend_visualizations
                    recommendations = recommend_visualizations(
                        df, st.session_state.model, st.session_state.api_key
                    )
                    if "saved_charts" not in st.session_state:
                        st.session_state.saved_charts = []
                    st.session_state.ai_generated_charts = recommendations
                    st.success(
                        f"Generated {len(recommendations)} chart recommendations."
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

        if "ai_generated_charts" in st.session_state:
            st.markdown("---")
            for rec in st.session_state.ai_generated_charts:
                chart_type = rec.get("chart_type")
                x_col = rec.get("x_col")
                y_col = rec.get("y_col")
                color_col = rec.get("color_col")
                explanation = rec.get("explanation")

                title = f"{chart_type}: {y_col} vs {x_col}"
                if color_col:
                    title += f" (by {color_col})"
                st.markdown(f"##### {title}")

                if explanation:
                    st.caption(explanation)

                try:
                    fig = generate_custom_chart(df, chart_type, x_col, y_col, color_col)
                    safe_key = (
                        f"viz_{chart_type}_{y_col}_{x_col}"
                        .replace(" ", "_").replace("(", "").replace(")", "")
                    )
                    st.plotly_chart(
                        fig, use_container_width=True,
                        config={"displayModeBar": False}, key=safe_key,
                    )

                    if "saved_charts" not in st.session_state:
                        st.session_state.saved_charts = []
                    chart_name = f"AI {chart_type}: {y_col} vs {x_col}"
                    already_saved = any(
                        c["name"] == chart_name
                        for c in st.session_state.saved_charts
                    )
                    if not already_saved:
                        st.session_state.saved_charts.append(
                            {"name": chart_name, "fig": fig}
                        )
                except Exception as e:
                    st.warning(
                        f"Could not render {chart_type} for {y_col} vs {x_col}. "
                        f"Reason: {e}"
                    )
    else:
        _manual_chart_builder(df)


def _manual_chart_builder(df):
    st.markdown("##### Manual Chart Builder")

    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    chart_types = [
        "Bar Chart (Horizontal)", "Column Chart (Vertical)",
        "Stacked Bar Chart", "Stacked Column Chart",
        "Clustered Column Chart", "Clustered Bar Chart",
        "Pie Chart", "Donut Chart", "Line Chart", "Heat Map (2D Density)",
    ]

    selected_chart = st.selectbox("Chart Type", chart_types)

    c1, c2, c3 = st.columns(3)
    with c1:
        x_col = st.selectbox("X-Axis (or Names)", df.columns.tolist())
    with c2:
        y_col = st.selectbox("Y-Axis (or Values)", num_cols)
    with c3:
        color_col = st.selectbox(
            "Color / Group By (Optional)", ["None"] + cat_cols + num_cols
        )

    c_arg = None if color_col == "None" else color_col

    try:
        fig = generate_custom_chart(df, selected_chart, x_col, y_col, c_arg)
        safe_key = (
            f"viz_manual_{selected_chart}_{y_col}_{x_col}"
            .replace(" ", "_").replace("(", "").replace(")", "")
        )
        st.plotly_chart(fig, use_container_width=True, key=safe_key)

        if "saved_charts" not in st.session_state:
            st.session_state.saved_charts = []

        if st.button("Save to Gallery"):
            st.session_state.saved_charts.append(
                {"name": f"{selected_chart}: {y_col} vs {x_col}", "fig": fig}
            )
            st.success("Chart saved to the Export Gallery.")
    except Exception as e:
        st.error(f"Cannot generate {selected_chart} with these columns. Error: {e}")


# ===========================================================================
# TAB: AI INSIGHTS
# ===========================================================================
def _tab_insights(df):
    st.markdown(
        section_header("AI-Generated Insights",
                       "Extract KPIs, trends, and anomalies from your data automatically."),
        unsafe_allow_html=True,
    )

    if st.button("Generate Report", type="primary"):
        with st.spinner(f"Analyzing with {st.session_state.model}…"):
            try:
                t0 = time.time()
                insights = generate_insights(
                    df, st.session_state.model, st.session_state.api_key
                )
                st.session_state.analysis_time = time.time() - t0
                st.session_state.insights = insights
                st.success("Report generated successfully.")
            except Exception as e:
                st.error(str(e))

    if "insights" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.insights)


# ===========================================================================
# TAB: CHAT  (ChatGPT / Gemini-style UI)
# ===========================================================================
_SUGGESTED_PROMPTS = [
    "📊 What are the top 5 rows by highest value?",
    "📈 Show me the average of all numeric columns",
    "🔍 Which column has the most missing values?",
    "📉 What is the correlation between numeric columns?",
    "🗂️ How many unique values does each column have?",
    "⚡ Give me a quick summary of this dataset",
]
def _tab_chat(df):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ── Welcome screen with suggested prompts ─────────────────────────────
    if not st.session_state.chat_history:
        st.markdown(
            '<div class="chat-welcome">'
            '<div class="chat-welcome-icon">🤖</div>'
            '<h2 class="chat-welcome-title">Chat with your Data</h2>'
            '<p class="chat-welcome-sub">'
            'Ask anything in plain English — I will query your dataset and explain the results.'
            '</p></div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(2)
        for i, prompt_text in enumerate(_SUGGESTED_PROMPTS):
            with cols[i % 2]:
                if st.button(prompt_text, key=f"chip_{i}", use_container_width=True):
                    if "pending_ai_reply" in st.session_state:
                        del st.session_state["pending_ai_reply"]
                    st.session_state.chat_history.append(
                        {"role": "user", "content": prompt_text}
                    )
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    else:
        # ── Clear button ───────────────────────────────────────────────────
        _, c2 = st.columns([9, 1])
        with c2:
            if st.button("🗑️ Clear", key="clear_chat"):
                st.session_state.chat_history = []
                if "pending_ai_reply" in st.session_state:
                    del st.session_state["pending_ai_reply"]
                st.rerun()

        # ── Message thread ─────────────────────────────────────────────────
        st.markdown('<div class="chat-thread">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    '<div class="chat-row chat-row-user">'
                    f'<div class="chat-bubble chat-bubble-user">{msg["content"]}</div>'
                    '<div class="chat-avatar chat-avatar-user">You</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="chat-row chat-row-ai">'
                    '<div class="chat-avatar chat-avatar-ai">AI</div>'
                    f'<div class="chat-bubble chat-bubble-ai">{msg["content"]}</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Pending AI reply after rerun ───────────────────────────────────────
    last = st.session_state.chat_history
    if last and last[-1]["role"] == "user" and not st.session_state.get("pending_ai_reply"):
        st.session_state.pending_ai_reply = True
        latest_user_msg = last[-1]["content"]
        typing_ph = st.empty()
        typing_ph.markdown(
            '<div class="chat-row chat-row-ai">'
            '<div class="chat-avatar chat-avatar-ai">AI</div>'
            '<div class="chat-bubble chat-bubble-ai chat-typing">'
            '<span></span><span></span><span></span>'
            '</div></div>',
            unsafe_allow_html=True,
        )
        try:
            response = chat_with_data(
                df, latest_user_msg,
                st.session_state.chat_history[:-1],
                st.session_state.model,
                st.session_state.api_key,
            )
        except Exception as e:
            response = f"⚠️ Sorry, I ran into an error: {e}"
        typing_ph.empty()
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.session_state.pending_ai_reply = None
        st.rerun()

    # ── Bottom input bar ───────────────────────────────────────────────────
    if prompt := st.chat_input("Ask anything about your data…"):
        if "pending_ai_reply" in st.session_state:
            del st.session_state["pending_ai_reply"]
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.rerun()


# ===========================================================================
# TAB: EVALUATION
# ===========================================================================
def _tab_evaluation():
    st.markdown(
        section_header("System Evaluation",
                       "Track performance and provide feedback."),
        unsafe_allow_html=True,
    )

    # Performance metrics
    st.markdown("##### Performance")
    if "analysis_time" in st.session_state:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                stat_card(
                    f"{st.session_state.analysis_time:.2f}s",
                    "Last Analysis Time", "⏱️", "sky",
                ),
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                stat_card(
                    st.session_state.model.split("/")[-1],
                    "Active Model", "🧠", "indigo",
                ),
                unsafe_allow_html=True,
            )
    else:
        st.info("Run the AI Insights module to see performance metrics.")

    st.markdown("---")

    # Feedback form
    st.markdown("##### Feedback")
    with st.form("feedback_form"):
        rating = st.slider(
            "Rate the Quality of AI Insights",
            min_value=1, max_value=5, value=5,
            help="1 = Poor, 5 = Excellent",
        )
        feedback = st.text_area(
            "Comments",
            placeholder="How do the AI insights compare to manual analysis?",
        )
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            os.makedirs("outputs", exist_ok=True)
            fpath = "outputs/evaluation_results.csv"
            row = pd.DataFrame([{
                "timestamp": pd.Timestamp.now(),
                "model": st.session_state.model,
                "rating": rating,
                "feedback": feedback,
            }])
            if os.path.exists(fpath):
                row.to_csv(fpath, mode="a", header=False, index=False)
            else:
                row.to_csv(fpath, index=False)
            st.success("Feedback saved successfully.")


# ===========================================================================
# TAB: EXPORT GALLERY
# ===========================================================================
def _tab_gallery():
    st.markdown(
        section_header("Export Gallery",
                       "Select charts for your comprehensive PDF report."),
        unsafe_allow_html=True,
    )

    if "saved_charts" not in st.session_state or not st.session_state.saved_charts:
        st.markdown(
            empty_state("🖼️", "No charts saved yet",
                        "Head to the Visualizations tab to create and save charts."),
            unsafe_allow_html=True,
        )
        return

    selected_indices = []
    for i, chart_data in enumerate(st.session_state.saved_charts):
        safe_name = chart_data['name'].replace(" ", "_").replace(":", "").replace("(", "").replace(")", "")
        st.markdown(f"##### {chart_data['name']}")
        st.plotly_chart(
            chart_data["fig"], use_container_width=True, key=f"gallery_chart_{safe_name}_{i}"
        )
        if st.checkbox(
            f"Include in report", key=f"chk_{safe_name}_{i}", value=True
        ):
            selected_indices.append(i)

    if not (selected_indices or "insights" in st.session_state):
        return

    st.markdown("---")
    if st.button("Generate PDF Report", type="primary"):
        import io
        import base64

        try:
            import markdown
            from xhtml2pdf import pisa
        except ImportError:
            st.error("Missing PDF libraries. Run: `pip install xhtml2pdf markdown`")
            st.stop()

        with st.spinner("Generating PDF…"):
            html = (
                "<html><head><style>"
                "body { font-family: Helvetica, sans-serif; font-size: 14px; "
                "color: #0F172A; }"
                "h1 { color: #4F46E5; font-size: 26px; }"
                "h2, h3 { color: #334155; }"
                "img { margin: 10px 0 20px 0; }"
                "hr { border: none; border-top: 1px solid #E2E8F0; margin: 24px 0; }"
                "</style></head><body>"
                "<h1>AI Data Analysis Report</h1><hr/>"
            )

            if "insights" in st.session_state:
                html += markdown.markdown(st.session_state.insights) + "<hr/>"

            if selected_indices:
                html += "<h2>Visualizations</h2>"
                for idx in selected_indices:
                    chart = st.session_state.saved_charts[idx]
                    img_bytes = chart["fig"].to_image(
                        format="png", width=800, height=500, scale=2
                    )
                    b64_img = base64.b64encode(img_bytes).decode("utf-8")
                    html += f"<h3>{chart['name']}</h3>"
                    html += (
                        f'<img src="data:image/png;base64,{b64_img}" width="700"/><br/>'
                    )

            html += "</body></html>"

            pdf_file = io.BytesIO()
            pisa_status = pisa.CreatePDF(
                io.BytesIO(html.encode("utf-8")), dest=pdf_file
            )

            if not pisa_status.err:
                st.session_state.export_pdf = pdf_file.getvalue()
            else:
                st.error("Failed to generate PDF.")

    if "export_pdf" in st.session_state:
        import base64

        b64_pdf = base64.b64encode(st.session_state.export_pdf).decode("utf-8")
        href = f"data:application/pdf;base64,{b64_pdf}"
        st.markdown(
            download_button(href, "Download PDF Report"),
            unsafe_allow_html=True,
        )


# ===========================================================================
# MAIN ENTRYPOINT
# ===========================================================================
def main():
    _init_state()
    _render_sidebar()

    df = st.session_state.df

    if df is None:
        _render_landing()
        return

    # Top bar
    st.markdown(
        top_bar(
            "AI Data Analyzer",
            f"Analyzing {st.session_state.file_name}",
            badge_text="Dataset Loaded",
            badge_icon="●",
        ),
        unsafe_allow_html=True,
    )

    # Tabs
    tabs = st.tabs([
        "Data Preview",
        "Auto EDA",
        "Visualizations",
        "AI Insights",
        "Ask Data",
        "Evaluation",
        "Export Gallery",
    ])

    with tabs[0]:
        _tab_data_preview(df)
    with tabs[1]:
        _tab_eda(df)
    with tabs[2]:
        _tab_visualizations(df)
    with tabs[3]:
        _tab_insights(df)
    with tabs[4]:
        _tab_chat(df)
    with tabs[5]:
        _tab_evaluation()
    with tabs[6]:
        _tab_gallery()


if __name__ == "__main__":
    main()
