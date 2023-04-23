from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, create_engine
from ..src.main import app
from ..src.database import get_session,get_engine
from ..src.controllers.index import ClaimController
from ..src.models.claims import Claim
from ..src.schemas.claims import ClaimsInputSchema


SQLModel.metadata.create_all(get_engine())
client = TestClient(app)


def test_create_claim():
    with Session(get_engine()) as session:
        claim_input = ClaimsInputSchema(
            service_date="2022-01-01",
            submitted_procedure="D123",
            quadrant="UR",
            plan_group_number="12345",
            subscriber_number="67890",
            provider_npi="1234567890",
            provider_fees=100.0,
            allowed_fees=80.0,
            member_coinsurance=10.0,
            member_copay=10.0
        )
        controller = ClaimController()
        response = controller.create_claim(claim_input, session)
        assert response == 20.0


def test_get_claim_by_id():
    with Session(get_engine()) as session:
        claim = Claim(
            service_date="2022-01-01",
            submitted_procedure="D123",
            quadrant="UR",
            plan_group_number="12345",
            subscriber_number="67890",
            provider_npi="1234567890",
            provider_fees=100.0,
            allowed_fees=80.0,
            member_coinsurance=10.0,
            member_copay=10.0,
            net_fee=20.0
        )
        session.add(claim)
        session.commit()
        claim_id = claim.id
        controller = ClaimController()
        response = controller.get_claim_by_id(claim_id, session)
        assert response.id == claim_id
        assert response.service_date == "2022-01-01"


def test_get_claims():
    with Session(get_engine()) as session:
        claim1 = Claim(
            service_date="2022-01-01",
            submitted_procedure="D123",
            quadrant="UR",
            plan_group_number="12345",
            subscriber_number="67890",
            provider_npi="1234567890",
            provider_fees=100.0,
            allowed_fees=80.0,
            member_coinsurance=10.0,
            member_copay=10.0,
            net_fee=20.0
        )
        claim2 = Claim(
            service_date="2022-01-02",
            submitted_procedure="D234",
            quadrant="UL",
            plan_group_number="54321",
            subscriber_number="09876",
            provider_npi="0987654321",
            provider_fees=200.0,
            allowed_fees=160.0,
            member_coinsurance=20.0,
            member_copay=20.0,
            net_fee=40.0
        )
        session.add_all([claim1, claim2])
        session.commit()
        controller = ClaimController()
        response = controller.get_claims(session=session)
        assert len(response) == 2
        assert response[0].id == claim1.id
        assert response[1].id == claim2.id
