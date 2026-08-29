from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Donation, Donor, Campaign
from schemas import DonationCreate, DonationResponse

router = APIRouter(prefix="/donations", tags=["donations"])


@router.post("/", response_model=DonationResponse)
def create_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    # Verify the donor exists
    donor = db.query(Donor).filter(Donor.id == donation.donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    # Verify the campaign exists, if one was provided
    if donation.campaign_id:
        campaign = db.query(Campaign).filter(Campaign.id == donation.campaign_id).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

    new_donation = Donation(**donation.model_dump())
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)
    return new_donation


@router.get("/", response_model=list[DonationResponse])
def list_donations(db: Session = Depends(get_db)):
    return db.query(Donation).all()