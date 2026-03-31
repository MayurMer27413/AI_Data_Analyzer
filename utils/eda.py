import pandas as pd

def missing_values_summary(df):
    """Returns a dataframe summarizing missing values."""
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({'Missing Values': missing, 'Percentage (%)': missing_pct})
    return missing_df[missing_df['Missing Values'] > 0].sort_values(by='Missing Values', ascending=False)

def statistical_summary(df):
    """Returns descriptive statistics for numeric columns."""
    return df.describe().T

def correlation_matrix(df):
    """Returns correlation matrix for numeric columns."""
    num_df = df.select_dtypes(include=['number'])
    if len(num_df.columns) < 2:
        return pd.DataFrame()
    return num_df.corr()
