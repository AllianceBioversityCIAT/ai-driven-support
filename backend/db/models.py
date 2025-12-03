"""
Database Models
SQLAlchemy ORM models for tickets cache and analysis logs
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TicketCache(Base):
    """Cached FreshService tickets"""
    __tablename__ = "tickets_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, unique=True, index=True)
    subject = Column(String(255))
    status = Column(String(50))
    priority = Column(String(50))
    requester_id = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cached_at = Column(DateTime, default=datetime.utcnow)

class AnalysisLog(Base):
    """AI analysis logs"""
    __tablename__ = "analysis_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, index=True)
    summary = Column(Text)
    classification = Column(String(100))
    automation_opportunities = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
