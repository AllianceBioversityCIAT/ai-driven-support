"""
Tests for FreshService client
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from api.freshservice_client import FreshServiceClient
import base64

@pytest.fixture
def client():
    """Create test client"""
    return FreshServiceClient(api_key="test_key", domain="testdomain")

@pytest.fixture
def mock_response():
    """Mock successful API response"""
    mock = Mock()
    mock.json.return_value = {
        "tickets": [
            {
                "id": 1,
                "subject": "Test Ticket",
                "status": "open",
                "priority": "high",
                "type": "incident"
            }
        ],
        "total_count": 1
    }
    mock.raise_for_status.return_value = None
    return mock

def test_client_initialization(client):
    """Test client initialization"""
    assert client.api_key == "test_key"
    assert client.domain == "testdomain"
    assert client.base_url == "https://testdomain.freshservice.com/api/v2"
    assert "Authorization" in client.headers
    assert "Basic" in client.headers["Authorization"]

def test_headers_generation(client):
    """Test authorization header generation"""
    expected_auth = base64.b64encode(b"test_key:X").decode()
    assert client.headers["Authorization"] == f"Basic {expected_auth}"
    assert client.headers["Content-Type"] == "application/json"

@patch('api.freshservice_client.requests.request')
def test_list_tickets(mock_request, client, mock_response):
    """Test listing tickets"""
    mock_request.return_value = mock_response
    
    result = client.list_tickets(page=1, per_page=30)
    
    assert result == mock_response.json.return_value
    assert mock_request.called
    assert mock_request.call_args[1]["params"]["page"] == 1
    assert mock_request.call_args[1]["params"]["per_page"] == 30

@patch('api.freshservice_client.requests.request')
def test_get_ticket(mock_request, client, mock_response):
    """Test getting ticket details"""
    mock_request.return_value = mock_response
    
    result = client.get_ticket(1)
    
    assert result == mock_response.json.return_value
    assert mock_request.called
    assert "/tickets/1" in mock_request.call_args[1]["url"]

@patch('api.freshservice_client.requests.request')
def test_get_ticket_conversations(mock_request, client, mock_response):
    """Test getting ticket conversations"""
    mock_request.return_value = mock_response
    
    result = client.get_ticket_conversations(1)
    
    assert result == mock_response.json.return_value
    assert "/tickets/1/conversations" in mock_request.call_args[1]["url"]

@patch('api.freshservice_client.requests.request')
def test_search_tickets(mock_request, client, mock_response):
    """Test searching tickets"""
    mock_request.return_value = mock_response
    
    result = client.search_tickets("password")
    
    assert result == mock_response.json.return_value
    assert mock_request.called
