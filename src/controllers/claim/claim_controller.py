import logging
from fastapi import HTTPException, Depends
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from sqlmodel import Session
from ...database import get_session
from ...models.claims import Claim
from ...schemas.claims import PaymentInputSchema, ClaimsInputSchema
from ...services.index import ClaimService
from contextlib import closing

log = logging.getLogger("uvicorn")

class ClaimController:
    def __init__(self):
        self.claim_service = ClaimService()
        
    def create_claim(self,claim: ClaimsInputSchema, session: Session = Depends(get_session)):
        try:
            log.info("Create the claim with correct net_fee value")
            net_fee = self.claim_service.calculate_net_fee(claim)
            claim.net_fee = net_fee
            db_claim = Claim.from_orm(claim)
            res = self.claim_service.create_claim(db_claim, session)

            # Call the payments API to process the payment
            # We can use the HTTPClient to make a POST request to the payments API here
            return {"net_fee":net_fee}
        except Exception as e:
            log.error("create_claim error: ", e)
            raise HTTPException(status_code=500, detail="Internal server error")


    def get_claim_by_id(self, claim_id: int, session: Session = Depends(get_session)):
        try:
            task = session.get(Claim, claim_id)
            log.info("Got the claim by id")
            if not task:
                log.error("get_claim by_id error: ", e)
                raise HTTPException(status_code=404, detail="Task not found")
            return task
        except Exception as e:
            log.error(" get_claim_by_id error: ", e)
            raise HTTPException(status_code=500, detail="Internal server error")


    def get_claims(self, skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
        try:
            tasks = session.query(Claim).offset(skip).limit(limit).all()
            log.info("Got the claims")
            return tasks
        except Exception as e:
            log.error(" get_claims error: ", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_claims_by_net_fee(self, session: Session = Depends(get_session)):
            try:
                tasks = session.query(Claim).order_by(Claim.net_fee.desc()).limit(10).all()
                log.info("Got the claim by net_fee")
                return tasks
            except Exception as e:
                log.error(" get_claims error: ", e)
                raise HTTPException(status_code=500, detail="Internal server error")
