from pydantic import BaseModel, ConfigDict
from typing import Optional


class VisitBase(BaseModel):
    patient_id: int
    case_no: str
    visit_date: str
    ref_by: Optional[str] = ""
    symptoms: Optional[str] = ""
    previous_treatment: Optional[str] = ""
    notes: Optional[str] = ""
    prescription: Optional[str] = ""
    doctor_id: Optional[int] = None
    diagnosis: Optional[str] = ""
    advice: Optional[str] = ""
    followup_notes: Optional[str] = ""
    next_followup_date: Optional[str] = ""


class VisitCreate(VisitBase):
    pass


class VisitUpdate(BaseModel):
    case_no: Optional[str] = None
    visit_date: Optional[str] = None
    ref_by: Optional[str] = None
    symptoms: Optional[str] = None
    previous_treatment: Optional[str] = None
    notes: Optional[str] = None
    prescription: Optional[str] = None
    doctor_id: Optional[int] = None
    diagnosis: Optional[str] = None
    advice: Optional[str] = None
    followup_notes: Optional[str] = None
    next_followup_date: Optional[str] = None


class VisitOut(VisitBase):
    id: int

    model_config = ConfigDict(from_attributes=True)