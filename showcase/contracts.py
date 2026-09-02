from enum import Enum

from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    MATCHED = "matched"
    NOT_FOUND = "not_found"
    AMBIGUOUS = "ambiguous"


class VerificationRequest(BaseModel):
    product_name: str = Field(
        min_length=1,
        max_length=200,
    )


class RegulatoryRecord(BaseModel):
    record_id: str
    product_name: str
    manufacturer: str


class VerificationResponse(BaseModel):
    status: VerificationStatus
    message: str
    matches: list[RegulatoryRecord]
