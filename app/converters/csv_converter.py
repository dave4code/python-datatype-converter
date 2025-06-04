import pandas as pd
import io

def csv_to_dataframe(content):
    """
    Convert CSV content to a pandas DataFrame
    
    Args:
        content: CSV content as string or bytes
        
    Returns:
        pandas.DataFrame: DataFrame representation of the CSV data
    """
    if isinstance(content, bytes):
        content = io.StringIO(content.decode('utf-8'))
    elif isinstance(content, str):
        content = io.StringIO(content)
    
    return pd.read_csv(content)
