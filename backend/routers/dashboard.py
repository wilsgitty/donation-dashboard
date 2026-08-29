from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Donor, Donation, Campaign
from schemas import DashboardSummary, DonationTrend, TrendPoint

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_summary(db: Session = Depends(get_db)):
    # Total distinct donors who have given a completed donation
    total_donors = (
        db.query(func.count(func.distinct(Donation.donor_id)))
        .filter(Donation.status == "completed")
        .scalar()
    ) or 0

    # Total amount donated (completed only)
    total_donated = (
        db.query(func.coalesce(func.sum(Donation.amount), 0))
        .filter(Donation.status == "completed")
        .scalar()
    )

    # Active campaign target (first active campaign found)
    active_campaign = db.query(Campaign).filter(Campaign.status == "active").first()
    target_amount = active_campaign.target_amount if active_campaign else None

    # Donation progress
    donation_progress_pct = None
    if target_amount and target_amount > 0:
        donation_progress_pct = round(float(total_donated) / float(target_amount) * 100, 1)

    # Repeat donor rate (donor engagement)
    donation_counts = (
        db.query(Donation.donor_id, func.count(Donation.id).label("cnt"))
        .filter(Donation.status == "completed")
        .group_by(Donation.donor_id)
        .all()
    )
    if donation_counts:
        repeat_donors = sum(1 for d in donation_counts if d.cnt > 1)
        repeat_donor_pct = round(repeat_donors / len(donation_counts) * 100, 1)
    else:
        repeat_donor_pct = 0.0

    return DashboardSummary(
        total_donors=total_donors,
        total_donated=total_donated,
        target_amount=target_amount,
        donation_progress_pct=donation_progress_pct,
        repeat_donor_pct=repeat_donor_pct,
    )

from datetime import date as date_type


@router.get("/trend", response_model=DonationTrend)
def get_trend(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.date(Donation.donated_at).label("day"),
            func.sum(Donation.amount).label("total"),
        )
        .filter(Donation.status == "completed")
        .group_by(func.date(Donation.donated_at))
        .order_by(func.date(Donation.donated_at))
        .all()
    )

    points = [
        TrendPoint(date=str(r.day), total=r.total)
        for r in results
    ]

    return DonationTrend(points=points)