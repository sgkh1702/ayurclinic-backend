from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.patient import Patient
from app.models.visit import Visit
from app.schemas.visit import VisitCreate, VisitOut, VisitUpdate
from app.utils.pdf_casepaper import build_visit_pdf

router = APIRouter(tags=["visits"])


@router.post("/visits", response_model=VisitOut)
def create_visit(payload: VisitCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if not any([
        (payload.symptoms or "").strip(),
        (payload.previous_treatment or "").strip(),
        (payload.notes or "").strip(),
        (payload.prescription or "").strip(),
        (payload.ref_by or "").strip(),
        (payload.diagnosis or "").strip(),
        (payload.advice or "").strip(),
        (payload.followup_notes or "").strip(),
    ]):
        raise HTTPException(status_code=400, detail="Blank visit cannot be saved")

    visit = Visit(**payload.model_dump())
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


@router.get("/patients/{patient_id}/visits")
def list_patient_visits(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    visits = (
        db.query(Visit)
        .filter(Visit.patient_id == patient_id)
        .order_by(Visit.id.desc())
        .all()
    )

    result = []
    for visit in visits:
        result.append({
            "id": visit.id,
            "patient_id": visit.patient_id,
            "case_no": visit.case_no,
            "visit_date": visit.visit_date,
            "ref_by": visit.ref_by,
            "symptoms": visit.symptoms,
            "previous_treatment": visit.previous_treatment,
            "notes": visit.notes,
            "prescription": visit.prescription,
            "doctor_id": visit.doctor_id,
            "diagnosis": visit.diagnosis,
            "advice": visit.advice,
            "followup_notes": visit.followup_notes,
            "next_followup_date": visit.next_followup_date,
            "casepaper_pdf_url": f"http://localhost:8000/visits/{visit.id}/casepaper/pdf",
        })

    return result


@router.get("/visits/{visit_id}", response_model=VisitOut)
def get_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@router.put("/visits/{visit_id}", response_model=VisitOut)
def update_visit(visit_id: int, payload: VisitUpdate, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    update_data = payload.model_dump(exclude_unset=True)

    merged = {
        "symptoms": update_data.get("symptoms", visit.symptoms or ""),
        "previous_treatment": update_data.get("previous_treatment", visit.previous_treatment or ""),
        "notes": update_data.get("notes", visit.notes or ""),
        "prescription": update_data.get("prescription", visit.prescription or ""),
        "ref_by": update_data.get("ref_by", visit.ref_by or ""),
        "diagnosis": update_data.get("diagnosis", visit.diagnosis or ""),
        "advice": update_data.get("advice", visit.advice or ""),
        "followup_notes": update_data.get("followup_notes", visit.followup_notes or ""),
    }

    if not any([(v or "").strip() for v in merged.values()]):
        raise HTTPException(status_code=400, detail="Blank visit cannot be saved")

    for key, value in update_data.items():
        setattr(visit, key, value)

    db.commit()
    db.refresh(visit)
    return visit


@router.get("/visits/{visit_id}/casepaper/pdf")
async def get_visit_casepaper_pdf(visit_id: int, db: Session = Depends(get_db)):
    try:
        visit = db.query(Visit).filter(Visit.id == visit_id).first()
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")

        patient = db.query(Patient).filter(Patient.id == visit.patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        pdf_bytes = await build_visit_pdf(patient, visit)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="visit_{visit.id}.pdf"'
            }
        )

    except Exception as e:
        return Response(
            content=f"PDF ERROR: {type(e).__name__}: {str(e)}",
            media_type="text/plain"
        )