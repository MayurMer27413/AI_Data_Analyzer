import pandas as pd

def load_data(file):
    """Loads CSV or Excel data into a pandas DataFrame."""
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file), None
        elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
            return pd.read_excel(file), None
        else:
            return None, "Unsupported file format. Please upload a CSV or Excel file."
    except Exception as e:
        return None, f"Error processing file: {str(e)}"

def get_dataset_info(df):
    """Returns basic dataset geometry and missing values count."""
    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "missing": df.isna().sum().sum()
    }
