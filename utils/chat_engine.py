import os
from groq import Groq
import pandas as pd

def chat_with_data(df, question, history, model_name, api_key):
    """
    An interface querying Groq for the user's natural language questions about their dataset.
    Uses a minimal ReAct approach: if it needs data, the LLM generates a pandas command, 
    we eval() it, and send the result back for a final answer.
    """
    columns = ", ".join(df.columns.tolist())
    shape = f"{df.shape[0]} rows, {df.shape[1]} columns"
    sample = df.head(3).to_string()
    
    history_text = ""
    for msg in history[-3:]: # Keep last 3 messages for conversational context
        role = "User" if msg["role"] == "user" else "AI"
        history_text += f"{role}: {msg['content']}\n"
    
    prompt = f"""
You are a Python Pandas expert. The user wants to ask a question about their dataset.
DataFrame `df` details:
- Shape: {shape}
- Columns: {columns}
- First 3 rows:
{sample}

Conversation History (if any):
{history_text}

User Question: {question}

If the question requires computing a value or filtering the dataset to answer accurately, you MUST reply with EXACTLY ONE line of Python code that evaluates to the answer.
- The code must start with `df` or standard pandas operations. 
- DO NOT use print(), DO NOT assign variables, DO NOT output markdown, NOT EVEN backticks. JUST the raw Python expression.
- Examples of valid outputs:
  - df['Customer_Segment'].value_counts().get('Corporate', 0)
  - df['Sales'].sum()
  - len(df[df['Status'] == 'Active'])

If you can confidently answer the question without computation (e.g., general advice, column meanings based on names, greetings), just answer it normally in natural language.
"""
    
    try:
        if not api_key:
            raise Exception("Groq API Key is missing. Please provide it in the sidebar.")
            
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model_name,
            temperature=0  # Use 0 for more deterministic code generation
        )
        
        initial_response = chat_completion.choices[0].message.content.strip()
        # Clean up in case the LLM returned markdown code blocks despite instructions
        clean_code = initial_response.replace('```python', '').replace('```', '').strip()
        
        # Check if the response looks like an intended Pandas python expression
        if clean_code.startswith("df") or "df[" in clean_code or "df." in clean_code or "len(df" in clean_code:
            try:
                # Safely evaluate the pandas expression
                result = eval(clean_code, {"df": df, "pd": pd})
                
                # Step 2: Formulate final answer
                final_prompt = f"The user asked: '{question}'. The computed result from the dataframe using Pandas is: '{result}'. Formulate a friendly, concise natural language answer."
                final_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": final_prompt}],
                    model=model_name,
                    temperature=0.3
                )
                return final_completion.choices[0].message.content
            except Exception as eval_err:
                return f"I tried to calculate this using Pandas, but encountered an error evaluating the code: `{clean_code}`. Error: {eval_err}. Please refine your question."
        
        return initial_response
    except Exception as e:
        raise Exception(str(e))
