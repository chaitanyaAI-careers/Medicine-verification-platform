from typing import Protocol

from showcase.contracts import RegulatoryRecord


class VerificationRepository(Protocol):
    def save_result(
        self,
        product_name: str,
        match_count: int,
    ) -> None:
        ...


class InMemoryVerificationRepository:
    """
    Minimal repository example for portfolio demonstration.

    Production persistence and storage implementation details
    remain private.
    """

    def __init__(self) -> None:
        self.saved_results: list[tuple[str, int]] = []

    def save_result(
        self,
        product_name: str,
        match_count: int,
    ) -> None:
        self.saved_results.append(
            (
                product_name,
                match_count,
            )
        )
