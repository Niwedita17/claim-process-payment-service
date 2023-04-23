from fastapi.testclient import TestClient
from ..src.main import app
from ..src.models.claims import Claim
from ..src.schemas.claims import ClaimsInputSchema
client = TestClient(app)

def test_create_claim():
    claim_input = ClaimsInputSchema(
        service_date="2022-01-01",
        submitted_procedure="DHospital",
        quadrant="GHVHG",
        plan_group_number="555-1234",
        subscriber_number="675756",
        provider_npi="1234578934",
        provider_fees=89,
        allowed_fees=80.0,
        member_coinsurance=0.0,
        member_copay=20.0,
    )
    response = client.post("/claims", json=claim_input.dict())
    assert response.status_code == 200
    assert isinstance(response.json(), float)


def test_read_claim():
    claim_id = 1  # assuming claim with ID 1 exists in the database
    response = client.get(f"/claims/{claim_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["id"] == claim_id


def test_read_claims():
    response = client.get("/claims")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for claim in response.json():
        assert isinstance(claim, dict)
        assert isinstance(claim["id"], int)
        assert isinstance(claim["service_date"], str)
        # Add more assertions for other claim fields as needed
