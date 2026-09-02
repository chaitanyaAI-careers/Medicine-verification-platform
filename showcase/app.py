from fastapi import FastAPI

from showcase.contracts import (
    RegulatoryRecord,
    VerificationRequest,
    VerificationResponse,
)
from showcase.regulatory_source import SyntheticRegulatorySource
from showcase.repository import InMemoryVerificationRepository
from showcase.service import VerificationService


app = FastAPI(
    title="Medicine Verification Showcase API",
    description=(
        "Recruiter-safe example demonstrating FastAPI, "
        "service boundaries, repository abstraction, and "
        "synthetic external-data verification."
    ),
)


_source = SyntheticRegulatorySource(
    records=[
        RegulatoryRecord(
            record_id="synthetic-001",
            product_name="Example Medicine",
            manufacturer="Example Manufacturer",
        )
    ]
)

_repository = InMemoryVerificationRepository()

_service = VerificationService(
    source=_source,
    repository=_repository,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
    }


@app.post(
    "/verify",
    response_model=VerificationResponse,
)
def verify(
    request: VerificationRequest,
) -> VerificationResponse:
    return _service.verify(request)
