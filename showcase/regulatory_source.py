from typing import Protocol

from showcase.contracts import RegulatoryRecord


class RegulatorySource(Protocol):
    def search(
        self,
        product_name: str,
    ) -> list[RegulatoryRecord]:
        ...


class SyntheticRegulatorySource:
    """
    Synthetic external-data adapter.

    Production regulatory-data integration and matching details
    are intentionally excluded from this Career showcase.
    """

    def __init__(
        self,
        records: list[RegulatoryRecord] | None = None,
    ) -> None:
        self.records = records or []

    def search(
        self,
        product_name: str,
    ) -> list[RegulatoryRecord]:
        target = product_name.strip().casefold()

        return [
            record
            for record in self.records
            if record.product_name.casefold() == target
        ]
