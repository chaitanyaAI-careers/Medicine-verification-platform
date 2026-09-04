# Medicine Verification Platform

A small backend service that demonstrates a layered FastAPI application — API, service, and data-access boundaries — through a medicine-verification use case backed by synthetic data.

## Problem

Verifying whether a medicine product name matches a known regulatory record is a common backend pattern: accept a request, query an external or authoritative data source, and return a structured, unambiguous result (no match, single match, or multiple/ambiguous matches). This repository shows that pattern end to end, using synthetic data in place of a real regulatory data source.

## What the System Does

The service exposes a REST API that accepts a product name and returns a verification result:

- `GET /health` — a liveness check.
- `POST /verify` — accepts a product name and returns a status (`matched`, `not_found`, or `ambiguous`) along with any matching records.

Each verification request is checked against an in-memory, synthetic set of regulatory records, and the outcome (product name and match count) is recorded through a repository abstraction.

## Architecture

The code is organized into distinct layers with explicit boundaries, defined as Python `Protocol` interfaces so the underlying implementation can be swapped without changing calling code:

- **API layer** (`showcase/app.py`) — a FastAPI app wiring HTTP routes to the service layer.
- **Contracts** (`showcase/contracts.py`) — Pydantic models and enums defining request/response schemas and validation rules.
- **Service layer** (`showcase/service.py`) — `VerificationService`, which orchestrates a lookup against a data source and a save through a repository, and decides the response status.
- **External-data adapter** (`showcase/regulatory_source.py`) — `RegulatorySource` protocol with a `SyntheticRegulatorySource` implementation, standing in for a real external/regulatory data integration.
- **Persistence adapter** (`showcase/repository.py`) — `VerificationRepository` protocol with an `InMemoryVerificationRepository` implementation, standing in for real persistence.

```
Client → FastAPI routes (app.py)
            → VerificationService (service.py)
                → RegulatorySource protocol (regulatory_source.py)
                → VerificationRepository protocol (repository.py)
```

This is a portfolio showcase: the synthetic data source and in-memory repository intentionally represent the integration and persistence boundaries without exposing or overstating capabilities that are outside the scope of this public repository.

## Implemented Capabilities

- REST API built with FastAPI, including a health endpoint and a POST endpoint with a typed response model.
- Request/response schema validation with Pydantic (`Field` constraints, `Enum`-based status values).
- Service-layer orchestration separated from HTTP and data-access concerns.
- Repository pattern via a `Protocol` interface with a concrete in-memory implementation.
- External-data-source abstraction via a `Protocol` interface with a concrete synthetic implementation, including case-insensitive matching.
- Three-way verification outcome handling: no match, exactly one match, and multiple/ambiguous matches.
- Automated tests covering the API layer (via `TestClient`), the service layer, the synthetic data source, and the repository.
- Continuous integration on GitHub Actions: dependency install, `pip check`, `compileall`, and `pytest` on every push/PR to `main`.

## Technology Stack

- **Language:** Python 3.11
- **Web framework:** FastAPI
- **Data validation:** Pydantic v2
- **Testing:** pytest, FastAPI's `TestClient` (via `httpx`)
- **CI:** GitHub Actions


## API / Backend Design

- Typed, schema-validated request and response models (`VerificationRequest`, `VerificationResponse`, `RegulatoryRecord`) defined with Pydantic.
- An explicit status enum (`VerificationStatus`) rather than ad hoc string/boolean results.
- Dependency direction flows from the API layer down through the service to abstract interfaces (`RegulatorySource`, `VerificationRepository`), so concrete adapters are injected rather than hard-coded into the service.
- A single `/verify` endpoint returns one of three well-defined outcomes instead of a bare boolean, making the contract explicit for API consumers.

## Testing

Tests are written with pytest and live in `tests/test_showcase.py`. They cover:

- The `/health` endpoint.
- The `/verify` endpoint end to end through FastAPI's `TestClient`.
- `VerificationService` behavior for no-match, single-match, and ambiguous-match cases.
- Case-insensitive matching in `SyntheticRegulatorySource`.
- Result recording in `InMemoryVerificationRepository`.

Tests run automatically in CI (`.github/workflows/ci.yml`) on every push and pull request to `main`.

## Repository Structure

```
.
├── showcase/
│   ├── app.py                # FastAPI app and route definitions
│   ├── contracts.py           # Pydantic request/response models and enums
│   ├── regulatory_source.py   # RegulatorySource protocol + synthetic implementation
│   ├── repository.py          # VerificationRepository protocol + in-memory implementation
│   └── service.py             # VerificationService orchestration logic
├── tests/
│   └── test_showcase.py       # API, service, source, and repository tests
├── .github/workflows/ci.yml   # CI: install, pip check, compileall, pytest
├── requirements.txt
└── pytest.ini
```

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run the API
uvicorn showcase.app:app --reload

# run the tests
pytest -q
```

`uvicorn` is not pinned in `requirements.txt`; install it separately (`pip install uvicorn`) if you want to run the app locally rather than just the test suite.

## Current Limitations

- The regulatory data source is synthetic and in-memory (`SyntheticRegulatorySource`) — there is no real external/regulatory API integration in this repository.
- Persistence is in-memory (`InMemoryVerificationRepository`) and non-durable — data does not survive a process restart, and there is no database in this codebase.
- Matching logic is an exact, case-insensitive string comparison; there is no fuzzy or partial matching.
- No authentication, authorization, or rate limiting on the API.
- No containerization (no Dockerfile) is present in this repository.
- This is a scoped engineering showcase and does not claim production readiness or scale.

## Roadmap

The following are potential extensions and are **not implemented** in this repository:

- Real database-backed persistence (e.g., SQLAlchemy models over PostgreSQL).
- Integration with an actual external/regulatory data source in place of the synthetic adapter.
- Containerized local development and deployment (Docker).
- Authentication/authorization on API endpoints.
- Expanded matching logic (fuzzy matching, partial name search).

---

## Portfolio Context

Medicine Verification Platform is the portfolio's primary project for **backend/API engineering, typed service boundaries, and verification workflows**.

**Chaitanya Sai — Applied AI Engineer**

Generative AI · LLMs · RAG · Agentic AI · AI Platform & Backend Engineering

[Portfolio](https://chaitanya-sai-portfolio.vercel.app) · [GitHub](https://github.com/chaitanyaAI-careers) · [LinkedIn](https://www.linkedin.com/in/chaitanyaai-careers/)
