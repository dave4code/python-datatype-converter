import pandas as pd
import json

def json_to_dataframe(content):
    """
    Convert JSON content to a pandas DataFrame
    
    Args:
        content: JSON content as string or bytes
        
    Returns:
        pandas.DataFrame: DataFrame representation of the JSON data
    """
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    
    data = json.loads(content)
    
    # Handle different JSON structures
    if isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        if 'data' in data and isinstance(data['data'], list):
            return pd.DataFrame(data['data'])
        else:
            # Try to convert nested dict to DataFrame
            return pd.DataFrame.from_dict(data, orient='index').reset_index()
    else:
        raise ValueError("Unsupported JSON structure")
