from typing import Optional
from sqlmodel import SQLModel, Field


class Claim(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    service_date: str
    submitted_procedure: str
    quadrant: Optional[str] = None
    plan_group_number: str
    subscriber_number: str
    provider_npi: str
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float
    net_fee: float = Field(default=None)
    

