import strawberry
import logging
from typing import Optional
from strawberry.types.info import Info
from http.client import HTTPException
from pydantic import validator

log = logging.getLogger("uvicorn")
    
# Mutation
@strawberry.input
class ClaimsInputSchema:
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
    
    @validator('submitted_procedure')
    def validate_submitted_procedure(cls, v):
        if not v.startswith('D'):
            raise ValueError('Submitted procedure must start with D')
        return v
    
    @validator('provider_npi')
    def validate_provider_npi(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Provider NPI must be a 10 digit number')
        return v
    
    @validator('service_date', 'submitted_procedure', 'plan_group_number', 'subscriber_number', 'provider_npi', 'provider_fees', 'allowed_fees', 'member_coinsurance', 'member_copay')
    def validate_required_fields(cls, v, field):
        if not v:
            raise HTTPException(status_code=400, detail=f"{field['alias']} is required")
        return v
    
    
@strawberry.type
class ClaimsResponseSchema:
    id: int
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
    net_fee: float
   
@strawberry.type
class ClaimMutation:
    @strawberry.field
    def create_claim(self, request_input: ClaimsInputSchema, info: Info) -> ClaimsResponseSchema:
        claim = info.context.claim_service
        claim_dict=claim.dict()
        claim_dict.update(request_input.dict())
        info.context.claim_service =  claim(**claim_dict)
        return ClaimsResponseSchema(**claim.dict())
    
# Query
@strawberry.type
class ClaimQuery:
    @strawberry.field
    def Claim(self, info: Info) -> ClaimsResponseSchema:
        claim = info.context.claim_service
        return ClaimsResponseSchema(**claim.dict())

@strawberry.input
class PaymentInputSchema:
    id: int
    claim_id: int
    net_fee: float