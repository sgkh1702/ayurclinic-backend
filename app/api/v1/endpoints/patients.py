from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.patient import Patient
from app.models.visit import Visit
from app.schemas.patient import PatientCreate, PatientOut, PatientUpdate
from app.utils.pdf_casepaper import build_patient_history_pdf

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("", response_model=PatientOut)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    existing = db.query(Patient).filter(
        Patient.patient_name == payload.patient_name,
        Patient.birth_date == payload.birth_date,
        Patient.mobile == payload.mobile
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists with same name, birth date, and mobile."
        )

    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("", response_model=List[PatientOut])
def list_patients(
    search: Optional[str] = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Patient)

    if search:
        like_term = f"%{search}%"
        query = query.filter(
            or_(
                Patient.patient_name.like(like_term),
                Patient.mobile.like(like_term),
                Patient.patient_code.like(like_term),
                Patient.email.like(like_term)
            )
        )

    return query.order_by(Patient.patient_name.asc()).all()


@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "id": patient.id,
        "patient_code": patient.patient_code,
        "patient_name": patient.patient_name,
        "mobile": patient.mobile,
        "email": patient.email,
        "birth_date": patient.birth_date,
        "birth_time": patient.birth_time,
        "age": patient.age,
        "gender": patient.gender,
        "weight": patient.weight,
        "occupation": patient.occupation,
        "education": patient.education,
        "address": patient.address,
        "baseline_notes": patient.baseline_notes,
        "family_history": patient.family_history,
        "ref_by": patient.ref_by,
        "doctor_id": patient.doctor_id,
        "consolidated_pdf_url": f"http://localhost:8000/patients/{patient.id}/casepapers/pdf",
    }


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return patient


@router.get("/{patient_id}/casepapers/pdf")
async def get_patient_casepapers_pdf(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    visits = (
        db.query(Visit)
        .filter(Visit.patient_id == patient_id)
        .order_by(Visit.id.desc())
        .all()
    )

    pdf_bytes = await build_patient_history_pdf(patient, visits)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="patient_{patient.id}_history.pdf"'
        }
    )