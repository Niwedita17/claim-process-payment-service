from fastapi import APIRouter, Depends, Request
from typing import List
from sqlmodel import Session
from fastapi_limiter.depends import RateLimiter
from ...models.claims import Claim
from ...schemas.claims import ClaimsInputSchema
from ...controllers.index import ClaimController
from ...database import init_db, get_session
import logging

log = logging.getLogger("uvicorn")
router = APIRouter()

claim_controller = ClaimController()

@router.post('/claims')
def create_claim(claim: ClaimsInputSchema, session: Session = Depends(get_session)):
    log.info("Running the post request on /claims")
    return claim_controller.create_claim(claim, session)

@router.get("/claims/{claim_id}", response_model=Claim)
def read_claim(claim_id: int, session: Session = Depends(get_session)):
    log.info("Running the get request on /claims/id")
    return claim_controller.get_claim_by_id(claim_id, session)

@router.get("/claims", response_model=List[Claim])
def read_claims(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    log.info("Running the get request on /claims")
    return claim_controller.get_claims(skip, limit, session)

# @router.get("/providers", response_model=List[str],dependencies=[Depends(RateLimiter(times=2, seconds=5))])
@router.get("/providers", response_model=List[str])
def read_providers(session: Session = Depends(get_session)):
    log.info("Running the get request on /providers")
    claims = claim_controller.get_claims_by_net_fee(session)
    return [claim.provider_npi for claim in claims]