from pydantic import BaseModel, ConfigDict
from typing import Optional


class AttachmentBase(BaseModel):
    patient_id: int
    visit_id: int
    remarks: Optional[str] = ""
    doctor_id: Optional[int] = None


class AttachmentCreate(AttachmentBase):
    pass


class AttachmentOut(AttachmentBase):
    id: int
    file_name: str
    stored_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)