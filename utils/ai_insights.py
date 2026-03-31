import os
import json
from groq import Groq
from .eda import statistical_summary

def generate_insights(df, model_name, api_key):
    """
    Sends dataset summary to Groq API to generate insights.
    """
    num_summary = statistical_summary(df).to_string()
    columns = ", ".join(df.columns.tolist())
    
    prompt = f"""
You are an expert Data Scientist and Business Analyst.
I have a dataset with the following columns: {columns}

Here is the statistical summary of the numeric columns:
{num_summary}

Based on this information:
1. First, define 5-7 Key Performance Indicators (KPIs) relevant to this dataset. You MUST extract and calculate their exact numerical values based entirely on the provided statistical summary (e.g., using mean, max, or sum if deducible). Display the exact number prominently next to the KPI name.
2. Second, provide deep, extensive business insights, trends, and actionable explanations based on the metrics. 
3. Third, mention potential anomalies or outliers to watch for.

CRITICAL FORMATTING RULES:
- Do NOT use ANY emojis. This is a highly professional corporate report.
- Do NOT use conversational filler like "Here are the insights". Output ONLY the report content.
- Use clean, distinct markdown headers (H2, H3), bold text for metric names, and properly spaced bullet points.
- Structure it cleanly so it reads like a pristine, human-written executive summary.
"""
    
    try:
        if not api_key:
            raise Exception("Groq API Key is missing. Please provide it in the sidebar.")
            
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model_name,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error during AI generation: {str(e)}")

def recommend_visualizations(df, model_name, api_key):
    """
    Sends dataset schema/summary to Groq API to autonomously decide what charts to render.
    """
    num_summary = statistical_summary(df).to_string()
    columns_info = ", ".join([f"{col} ({dtype})" for col, dtype in zip(df.columns, df.dtypes)])
    
    prompt = f"""
You are an expert Data Analyst building an automated dashboard.
Here is the dataset schema and types:
{columns_info}

Here is the statistical summary of numeric columns:
{num_summary}

Your task is to recommend between 5 to 10 meaningful and highly insightful charts to display to the user. 
CRITICAL READABILITY RULES:
1. You MUST NEVER use a primary key, UUID, or high-cardinality column (like Sale_ID, User_ID, Row_Index) for X/Y axes or groupings on ANY chart.
2. For Pie/Donut charts, the `x_col` (names) MUST have fewer than 10 unique values.
3. Choose logical combinations. If using Date/Time, recommend a Line Chart.

Return ONLY a valid, raw JSON array of objects. Do not use markdown blocks like ```json.
Each object must have the following exact keys:
- "chart_type": MUST be one of ["Bar Chart (Horizontal)", "Column Chart (Vertical)", "Stacked Bar Chart", "Stacked Column Chart", "Clustered Column Chart", "Clustered Bar Chart", "Pie Chart", "Donut Chart", "Line Chart", "Heat Map (2D Density)"]
- "x_col": exact column name from the schema for the X-axis (or names for pie).
- "y_col": exact column name from the schema for the Y-axis (or values for pie).
- "color_col": exact column name for grouping/color, or null if none.
- "explanation": A short, 1-sentence explanation of why this chart is insightful.

Output ONLY JSON.
"""
    try:
        if not api_key:
            raise Exception("Groq API Key is missing.")
            
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model_name,
            temperature=0.1
        )
        content = chat_completion.choices[0].message.content.strip()
        
        # Clean potential markdown JSON wrapping
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        return json.loads(content.strip())
    except Exception as e:
        raise Exception(f"AI Chart generation failed. The LLM may have returned malformed formatting: {str(e)}")
