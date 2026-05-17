from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False, index=True)
    mobile = Column(String, nullable=True, index=True)
    email = Column(String, nullable=True, index=True)
    address = Column(Text, nullable=True)
    birth_date = Column(String, nullable=True)
    birth_time = Column(String, nullable=True)
    age = Column(String, nullable=True)
    weight = Column(String, nullable=True)
    education = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    gender = Column(String, nullable=True)

    family_history = Column(Text, nullable=True)
    ref_by = Column(Text, nullable=True)
    doctor_id = Column(Integer, nullable=True, index=True)
    patient_code = Column(String, nullable=True, index=True)
    baseline_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="patient", cascade="all, delete-orphan")