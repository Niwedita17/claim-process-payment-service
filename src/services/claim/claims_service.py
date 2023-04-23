from sqlmodel import Session
from ...models.claims import Claim
import logging

log = logging.getLogger("uvicorn")

class ClaimService:
    def create_claim(self, claim: Claim, session: Session):
        log.info("Creating claim...")
        session.add(claim)
        session.commit()
        session.refresh(claim)


    def calculate_net_fee(self, claim):
        log.info("Calculate net fee for provider npi:"+claim.provider_npi)
        # Compute the net fee
        net_fee = claim.provider_fees + claim.member_coinsurance + claim.member_copay - claim.allowed_fees
        return net_fee
