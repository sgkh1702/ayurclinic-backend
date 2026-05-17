import os
import shutil
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.attachment import Attachment
from app.models.patient import Patient
from app.models.visit import Visit
from app.schemas.attachment import AttachmentOut

router = APIRouter(tags=["attachments"])

UPLOAD_DIR = r"D:\\Ayurclinic\\backend\\uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/visits/{visit_id}/attachments", response_model=AttachmentOut)
def upload_attachment(
    visit_id: int,
    patient_id: int = Form(...),
    remarks: str = Form(""),
    doctor_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    visit = db.query(Visit).filter(Visit.id == visit_id, Visit.patient_id == patient_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found for this patient")

    ext = os.path.splitext(file.filename or "")[1]
    stored_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, stored_name)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(save_path)

    attachment = Attachment(
        patient_id=patient_id,
        visit_id=visit_id,
        file_name=file.filename or stored_name,
        stored_name=stored_name,
        file_path=save_path,
        file_type=file.content_type,
        file_size=file_size,
        remarks=remarks,
        doctor_id=doctor_id,
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment


@router.get("/visits/{visit_id}/attachments", response_model=List[AttachmentOut])
def list_attachments(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    return (
        db.query(Attachment)
        .filter(Attachment.visit_id == visit_id)
        .order_by(Attachment.id.desc())
        .all()
    )


@router.delete("/attachments/{attachment_id}")
def delete_attachment(attachment_id: int, db: Session = Depends(get_db)):
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    if attachment.file_path and os.path.exists(attachment.file_path):
        os.remove(attachment.file_path)

    db.delete(attachment)
    db.commit()
    return {"message": "Attachment deleted successfully"}