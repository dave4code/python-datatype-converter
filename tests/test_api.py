import pytest
import json
import io
from app.api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_inlet_no_data(client):
    response = client.post('/inlet')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_inlet_csv(client):
    csv_data = "name,age\nJohn,30\nJane,25"
    response = client.post(
        '/inlet?format=csv',
        data={'data': csv_data},
        content_type='multipart/form-data'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["rows"] == 2
    assert "name" in data["columns"]
    assert "age" in data["columns"]

def test_inlet_json(client):
    json_data = json.dumps([{"name": "John", "age": 30}, {"name": "Jane", "age": 25}])
    response = client.post(
        '/inlet?format=json',
        data={'data': json_data},
        content_type='multipart/form-data'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["rows"] == 2
    assert "name" in data["columns"]
    assert "age" in data["columns"]

def test_outlet_no_data(client):
    response = client.get('/outlet')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data

def test_outlet_formats(client):
    # First upload some data
    csv_data = "name,age\nJohn,30\nJane,25"
    client.post(
        '/inlet?format=csv',
        data={'data': csv_data},
        content_type='multipart/form-data'
    )
    
    # Test JSON output
    response = client.get('/outlet?format=json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data
    assert len(data["data"]) == 2
    
    # Test text output
    response = client.get('/outlet?format=text')
    assert response.status_code == 200
    assert b'+' in response.data  # Simple check for table formatting
    
    # Test HTML output
    response = client.get('/outlet?format=html')
    assert response.status_code == 200
    assert b'<table' in response.data
