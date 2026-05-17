from pydantic import BaseModel, ConfigDict
from typing import Optional


class PatientBase(BaseModel):
    patient_name: str
    mobile: Optional[str] = ""
    email: Optional[str] = ""
    address: Optional[str] = ""
    birth_date: Optional[str] = ""
    birth_time: Optional[str] = ""
    age: Optional[str] = ""
    weight: Optional[str] = ""
    education: Optional[str] = ""
    occupation: Optional[str] = ""
    gender: Optional[str] = ""
    family_history: Optional[str] = ""
    ref_by: Optional[str] = ""
    doctor_id: Optional[int] = None
    patient_code: Optional[str] = ""
    baseline_notes: Optional[str] = ""


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    patient_name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[str] = None
    birth_time: Optional[str] = None
    age: Optional[str] = None
    weight: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    gender: Optional[str] = None
    family_history: Optional[str] = None
    ref_by: Optional[str] = None
    doctor_id: Optional[int] = None
    patient_code: Optional[str] = None
    baseline_notes: Optional[str] = None


class PatientOut(PatientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)