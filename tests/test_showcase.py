from fastapi.testclient import TestClient

from showcase.app import app
from showcase.contracts import (
    RegulatoryRecord,
    VerificationRequest,
    VerificationStatus,
)
from showcase.regulatory_source import SyntheticRegulatorySource
from showcase.repository import InMemoryVerificationRepository
from showcase.service import VerificationService


def build_service(
    records: list[RegulatoryRecord],
) -> tuple[
    VerificationService,
    InMemoryVerificationRepository,
]:
    repository = InMemoryVerificationRepository()

    service = VerificationService(
        source=SyntheticRegulatorySource(
            records=records,
        ),
        repository=repository,
    )

    return service, repository


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


def test_verify_endpoint_returns_synthetic_match():
    client = TestClient(app)

    response = client.post(
        "/verify",
        json={
            "product_name": "Example Medicine",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "matched"
    assert len(response.json()["matches"]) == 1


def test_service_returns_not_found():
    service, repository = build_service([])

    result = service.verify(
        VerificationRequest(
            product_name="Unknown Medicine",
        )
    )

    assert result.status is VerificationStatus.NOT_FOUND
    assert result.matches == []
    assert repository.saved_results == [
        (
            "Unknown Medicine",
            0,
        )
    ]


def test_service_returns_single_match():
    service, repository = build_service(
        [
            RegulatoryRecord(
                record_id="synthetic-101",
                product_name="Example Medicine",
                manufacturer="Synthetic Manufacturer",
            )
        ]
    )

    result = service.verify(
        VerificationRequest(
            product_name="Example Medicine",
        )
    )

    assert result.status is VerificationStatus.MATCHED
    assert len(result.matches) == 1
    assert repository.saved_results == [
        (
            "Example Medicine",
            1,
        )
    ]


def test_service_returns_ambiguous_for_multiple_matches():
    service, _ = build_service(
        [
            RegulatoryRecord(
                record_id="synthetic-201",
                product_name="Example Medicine",
                manufacturer="Synthetic Manufacturer A",
            ),
            RegulatoryRecord(
                record_id="synthetic-202",
                product_name="Example Medicine",
                manufacturer="Synthetic Manufacturer B",
            ),
        ]
    )

    result = service.verify(
        VerificationRequest(
            product_name="Example Medicine",
        )
    )

    assert result.status is VerificationStatus.AMBIGUOUS
    assert len(result.matches) == 2


def test_synthetic_source_matching_is_case_insensitive():
    source = SyntheticRegulatorySource(
        [
            RegulatoryRecord(
                record_id="synthetic-301",
                product_name="Example Medicine",
                manufacturer="Synthetic Manufacturer",
            )
        ]
    )

    matches = source.search(
        "example medicine",
    )

    assert len(matches) == 1


def test_repository_records_multiple_results():
    repository = InMemoryVerificationRepository()

    repository.save_result(
        "Medicine A",
        1,
    )
    repository.save_result(
        "Medicine B",
        0,
    )

    assert repository.saved_results == [
        (
            "Medicine A",
            1,
        ),
        (
            "Medicine B",
            0,
        ),
    ]
