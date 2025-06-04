import pandas as pd
import pytest
from app.converters.csv_converter import csv_to_dataframe
from app.converters.json_converter import json_to_dataframe
from app.converters.xml_converter import xml_to_dataframe

def test_csv_converter():
    csv_data = "name,age\nJohn,30\nJane,25"
    df = csv_to_dataframe(csv_data)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['name', 'age']
    assert df.iloc[0]['name'] == 'John'
    assert df.iloc[1]['name'] == 'Jane'

def test_json_converter_list():
    json_data = '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]'
    df = json_to_dataframe(json_data)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['name', 'age']
    assert df.iloc[0]['name'] == 'John'
    assert df.iloc[1]['name'] == 'Jane'

def test_json_converter_dict():
    json_data = '{"data": [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]}'
    df = json_to_dataframe(json_data)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['name', 'age']
    assert df.iloc[0]['name'] == 'John'
    assert df.iloc[1]['name'] == 'Jane'

def test_xml_converter():
    xml_data = """
    <root>
        <person>
            <name>John</name>
            <age>30</age>
        </person>
        <person>
            <name>Jane</name>
            <age>25</age>
        </person>
    </root>
    """
    df = xml_to_dataframe(xml_data)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['name', 'age']
    assert df.iloc[0]['name'] == 'John'
    assert df.iloc[1]['name'] == 'Jane'
