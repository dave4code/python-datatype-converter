import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_dataframe(content):
    """
    Convert XML content to a pandas DataFrame
    
    Args:
        content: XML content as string or bytes
        
    Returns:
        pandas.DataFrame: DataFrame representation of the XML data
    """
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    
    root = ET.fromstring(content)
    data = []
    
    # Assuming XML structure with repeated elements for rows
    # Adjust this logic based on your XML structure
    for child in root:
        row = {}
        for element in child:
            row[element.tag] = element.text
        data.append(row)
    
    return pd.DataFrame(data)
