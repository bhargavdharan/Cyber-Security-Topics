"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Index, BigInteger
from sqlalchemy.sql import func
from app.db.database import Base


class UserBaseline(Base):
    """Stores learned behavioral baselines for each user."""
    __tablename__ = "user_baselines"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False)
    
    known_devices = Column(JSON, default=list)
    known_ips = Column(JSON, default=list)
    
    known_locations = Column(JSON, default=list)
    typical_login_hour_start = Column(Integer, default=8)
    typical_login_hour_end = Column(Integer, default=18)
    
    avg_login_frequency_per_day = Column(Float, default=3.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_user_baselines_user_id', 'user_id'),
    )


class RiskAssessment(Base):
    """Audit log of all risk assessments performed."""
    __tablename__ = "risk_assessments"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False)
    
    ip_address = Column(String(45), nullable=False)
    device_fingerprint = Column(String(255))
    location = Column(JSON)
    user_agent = Column(String(512))
    
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    recommended_action = Column(String(20), nullable=False)
    
    factors = Column(JSON, default=list)
    
    action_taken = Column(String(20))
    blocked = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('ix_risk_assessments_user_id_created', 'user_id', 'created_at'),
        Index('ix_risk_assessments_risk_level', 'risk_level'),
    )


class AuthEvent(Base):
    """Raw authentication events for analytics and baseline learning."""
    __tablename__ = "auth_events"
    
    id = Column(BigInteger, primary_key=True)
    user_id = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False)
    
    ip_address = Column(String(45), nullable=False)
    device_fingerprint = Column(String(255))
    location = Column(JSON)
    user_agent = Column(String(512))
    
    success = Column(Boolean, nullable=False)
    failure_reason = Column(String(255))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('ix_auth_events_user_id_created', 'user_id', 'created_at'),
    )
