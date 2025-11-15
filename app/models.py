from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from .db import Base

class ABAssignment(Base):
    __tablename__ = "ab_assignments"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True)
    variant_name = Column(String(50), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PageView(Base):
    __tablename__ = "page_views"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True)
    page = Column(String(255), index=True)
    variant_name = Column(String(50), index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True)
    event_name = Column(String(100), index=True)
    page_url = Column(String(255), index=True)
    variant_name = Column(String(50), index=True)
    event_metadata = Column("metadata", JSON, nullable=True)  # column called "metadata" in DB
    referrer = Column(Text, nullable=True)
    user_agent = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class UniversityQuote(Base):
    __tablename__ = "university_quotes"

    id = Column(Integer, primary_key=True, index=True)
    institution_name = Column(String(255))
    country = Column(String(100))
    quantity = Column(Integer)
    timeframe = Column(String(100))
    contact_email = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
