from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import Donor
from schemas import DonorCreate, DonorResponse

router = APIRouter(prefix="/donors", tags=["donors"])


@router.post("/", response_model=DonorResponse)
def create_donor(donor: DonorCreate, db: Session = Depends(get_db)):
    new_donor = Donor(**donor.model_dump())
    db.add(new_donor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="A donor with this email already exists")
    db.refresh(new_donor)
    return new_donor


@router.get("/", response_model=list[DonorResponse])
def list_donors(db: Session = Depends(get_db)):
    return db.query(Donor).all()