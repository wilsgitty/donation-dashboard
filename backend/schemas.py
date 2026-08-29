from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class DonorCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    is_anonymous: bool = False

class DonorResponse(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    is_anonymous: bool
    created_at: datetime

    class Config:
        from_attributes = True

from decimal import Decimal

class DonationCreate(BaseModel):
    donor_id: str
    campaign_id: Optional[str] = None
    amount: Decimal
    currency: str = "USD"
    payment_method: Optional[str] = None
    status: str = "completed"
    external_ref: Optional[str] = None

class DonationResponse(BaseModel):
    id: str
    donor_id: str
    campaign_id: Optional[str] = None
    amount: Decimal
    currency: str
    payment_method: Optional[str] = None
    status: str
    external_ref: Optional[str] = None
    donated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class DonationCreate(BaseModel):
    donor_id: str
    campaign_id: Optional[str] = None
    amount: Decimal
    currency: str = "USD"
    payment_method: Optional[str] = None
    status: str = "completed"
    external_ref: Optional[str] = None

class DonationResponse(BaseModel):
    id: str
    donor_id: str
    campaign_id: Optional[str] = None
    amount: Decimal
    currency: str
    payment_method: Optional[str] = None
    status: str
    external_ref: Optional[str] = None
    donated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime, date

class CampaignCreate(BaseModel):
    name: str
    description: Optional[str] = None
    target_amount: Decimal
    currency: str = "USD"
    start_date: date
    end_date: Optional[date] = None
    status: str = "active"

class CampaignResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    target_amount: Decimal
    currency: str
    start_date: date
    end_date: Optional[date] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class DashboardSummary(BaseModel):
    total_donors: int
    total_donated: Decimal
    target_amount: Optional[Decimal] = None
    donation_progress_pct: Optional[float] = None
    repeat_donor_pct: float
class TrendPoint(BaseModel):
    date: str
    total: Decimal

class DonationTrend(BaseModel):
    points: list[TrendPoint]