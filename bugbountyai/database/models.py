"""Database migration script untuk BugBountyAI v2"""

from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class Analysis(Base):
    """Analysis records"""
    __tablename__ = 'analyses'
    
    id = Column(String, primary_key=True)
    target_url = Column(String, nullable=False)
    status = Column(String, default='pending')
    risk_score = Column(Integer)
    vulnerabilities = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    user_id = Column(String)


class Vulnerability(Base):
    """Vulnerability records"""
    __tablename__ = 'vulnerabilities'
    
    id = Column(String, primary_key=True)
    analysis_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    severity = Column(String)
    description = Column(String)
    endpoint = Column(String)
    confidence = Column(Integer)
    poc = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Exploitation(Base):
    """Exploitation records"""
    __tablename__ = 'exploitations'
    
    id = Column(String, primary_key=True)
    vulnerability_id = Column(String, nullable=False)
    status = Column(String)
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class MonitoringSession(Base):
    """Monitoring session records"""
    __tablename__ = 'monitoring_sessions'
    
    id = Column(String, primary_key=True)
    targets = Column(JSON)
    interval = Column(Integer)
    status = Column(String, default='active')
    webhook_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String)


class Alert(Base):
    """Alert records"""
    __tablename__ = 'alerts'
    
    id = Column(String, primary_key=True)
    monitoring_id = Column(String)
    severity = Column(String)
    message = Column(String)
    target = Column(String)
    vulnerability_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    """User records"""
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default='analyst')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Team(Base):
    """Team records"""
    __tablename__ = 'teams'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)
    members = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    """Report records"""
    __tablename__ = 'reports'
    
    id = Column(String, primary_key=True)
    analysis_id = Column(String, nullable=False)
    format = Column(String)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


def init_database(database_url: str):
    """Initialize database with all tables"""
    try:
        engine = create_engine(database_url)
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise


def get_session(database_url: str):
    """Get database session"""
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()
