from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)

    case_no = Column(String, nullable=False, index=True)
    visit_date = Column(String, nullable=False, index=True)
    ref_by = Column(String, nullable=True)

    symptoms = Column(Text, nullable=True)
    previous_treatment = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    prescription = Column(Text, nullable=True)

    doctor_id = Column(Integer, nullable=True, index=True)
    diagnosis = Column(Text, nullable=True)
    advice = Column(Text, nullable=True)
    followup_notes = Column(Text, nullable=True)
    next_followup_date = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    patient = relationship("Patient", back_populates="visits")
    attachments = relationship("Attachment", back_populates="visit", cascade="all, delete-orphan")