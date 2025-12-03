"""
Tests for AI analysis service
"""
import pytest
from services.ai_analysis import AIAnalyzer

@pytest.fixture
def analyzer():
    """Create analyzer instance"""
    return AIAnalyzer()

@pytest.fixture
def sample_ticket():
    """Create sample ticket"""
    return {
        "id": 1,
        "subject": "Password reset request",
        "description": "User needs password reset",
        "type": "incident",
        "priority": "high",
        "status": "open"
    }

def test_analyzer_initialization(analyzer):
    """Test analyzer initialization"""
    assert analyzer.openai_api_key is None
    assert "Access" in analyzer.classifications
    assert "Bug" in analyzer.classifications

def test_summarize_ticket(analyzer, sample_ticket):
    """Test ticket summarization"""
    summary = analyzer.summarize(sample_ticket)
    
    assert summary is not None
    assert "Password reset request" in summary
    assert "high" in summary

def test_classify_access_ticket(analyzer):
    """Test classifying access ticket"""
    ticket = {
        "id": 1,
        "subject": "User access request",
        "description": "Need admin role access",
        "type": "request",
        "priority": "medium",
        "status": "open"
    }
    
    classification = analyzer.classify(ticket)
    assert classification == "Access"

def test_classify_bug_ticket(analyzer):
    """Test classifying bug ticket"""
    ticket = {
        "id": 2,
        "subject": "Application crash",
        "description": "App crashes on startup",
        "type": "incident",
        "priority": "high",
        "status": "open"
    }
    
    classification = analyzer.classify(ticket)
    assert classification == "Bug"

def test_classify_question_ticket(analyzer):
    """Test classifying question ticket"""
    ticket = {
        "id": 3,
        "subject": "How to configure X?",
        "description": "How do I configure this?",
        "type": "question",
        "priority": "low",
        "status": "open"
    }
    
    classification = analyzer.classify(ticket)
    assert classification == "General Question"

def test_find_automation_opportunities(analyzer):
    """Test finding automation opportunities"""
    ticket = {
        "id": 1,
        "subject": "Password reset request",
        "description": "User needs password reset",
        "type": "request",
        "priority": "high",
        "status": "open"
    }
    
    opportunities = analyzer.find_automation_opportunities(ticket)
    
    assert opportunities is not None
    assert len(opportunities) > 0
    assert any("password" in opp.lower() for opp in opportunities)
