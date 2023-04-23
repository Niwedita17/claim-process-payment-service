from fastapi import Depends
from sqlmodel import Session
from ...database import get_session

from logging import getLogger

from strawberry.fastapi import BaseContext
from ...services.index import ClaimService

log = getLogger("uvicorn")

class ServiceContext(BaseContext):
    def _init_(self, session: Session = Depends(get_session)):
        self.session = session
        self.claim_service = ClaimService(session)


def get_context():
    log.info("Get the context class")
    return ServiceContext()
