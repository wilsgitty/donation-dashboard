import uuid
from sqlalchemy import Column, String, Text, DECIMAL, Date, DateTime, Boolean, ForeignKey, JSON # type: ignore
from sqlalchemy.sql import func # type: ignore
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    target_amount = Column(DECIMAL(14, 2), nullable=False)
    currency = Column(String(3), default="USD")
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Donor(Base):
    __tablename__ = "donors"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    phone = Column(String(50))
    source = Column(String(100))
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())


class Donation(Base):
    __tablename__ = "donations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    donor_id = Column(String(36), ForeignKey("donors.id"), nullable=False)
    campaign_id = Column(String(36), ForeignKey("campaigns.id"))
    amount = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(String(3), default="USD")
    payment_method = Column(String(50))
    status = Column(String(20), default="completed")
    external_ref = Column(String(255))
    donated_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())


class EngagementEvent(Base):
    __tablename__ = "engagement_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    donor_id = Column(String(36), ForeignKey("donors.id"), nullable=False)
    event_type = Column(String(50), nullable=False)
    metadata_json = Column("metadata", JSON)
    occurred_at = Column(DateTime, server_default=func.now())