from showcase.contracts import (
    VerificationRequest,
    VerificationResponse,
    VerificationStatus,
)
from showcase.regulatory_source import RegulatorySource
from showcase.repository import VerificationRepository


class VerificationService:
    """
    Demonstrates service-layer orchestration only.

    The private product contains the production integration,
    matching, persistence, and verification workflow details.
    """

    def __init__(
        self,
        source: RegulatorySource,
        repository: VerificationRepository,
    ) -> None:
        self.source = source
        self.repository = repository

    def verify(
        self,
        request: VerificationRequest,
    ) -> VerificationResponse:
        matches = self.source.search(
            request.product_name,
        )

        self.repository.save_result(
            product_name=request.product_name,
            match_count=len(matches),
        )

        if not matches:
            return VerificationResponse(
                status=VerificationStatus.NOT_FOUND,
                message="No matching synthetic regulatory records found.",
                matches=[],
            )

        if len(matches) > 1:
            return VerificationResponse(
                status=VerificationStatus.AMBIGUOUS,
                message="Multiple synthetic regulatory records matched.",
                matches=matches,
            )

        return VerificationResponse(
            status=VerificationStatus.MATCHED,
            message="One synthetic regulatory record matched.",
            matches=matches,
        )
