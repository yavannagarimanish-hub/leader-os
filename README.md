# LeaderOS

LeaderOS is a lightweight decision-execution platform that helps teams track strategic decisions and monitor execution quality through real-time analytics.

## Why this project

This project is structured for maintainability and growth:
- **Layered backend architecture** (`API -> service -> repository`) for clear separation of concerns.
- **Strict request/response schemas** with validation to protect data quality.
- **Production-friendly API behavior** with typed responses and proper HTTP status codes.
- **Test coverage for core flows** to reduce regressions.

## Tech stack

- **Backend**: FastAPI, Pydantic
- **Runtime**: Uvicorn
- **Testing**: Pytest
- **Frontend**: Static HTML dashboard (`frontend/index.html`)

## Repository layout

```text
backend/
  main.py                  # FastAPI entrypoint
  leaderos/
    models.py              # Domain/API schemas
    repository.py          # Persistence abstraction (in-memory)
    service.py             # Business logic + analytics
frontend/
  index.html               # Lightweight dashboard UI
tests/
  test_service.py          # Service lifecycle + validation tests
```

## Quick start

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run the API

```bash
uvicorn backend.main:app --reload
```

API docs will be available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 3) Open the dashboard

Open `frontend/index.html` in your browser and click **Refresh Dashboard**.

## API examples

### Create a decision

```bash
curl -X POST http://127.0.0.1:8000/decision \
  -H "Content-Type: application/json" \
  -d '{"title": "Launch Q3 initiative", "description": "Finalize scope and staffing plan"}'
```

### Update status

```bash
curl -X PUT http://127.0.0.1:8000/decision/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

### View dashboard metrics

```bash
curl http://127.0.0.1:8000/dashboard
```

## Testing

Run automated tests with:

```bash
pytest -q
```

## Reliability and security notes

- Input constraints are enforced with Pydantic validation.
- Unknown resources return HTTP `404` instead of silent failures.
- The in-memory repository is protected with a lock for thread-safe mutation.
- Current persistence is ephemeral; use a database-backed repository for production durability.

## Suggested next improvements

- Replace in-memory storage with PostgreSQL + SQLAlchemy.
- Add authentication/authorization (JWT or OAuth2).
- Add structured logging and OpenTelemetry tracing.
- Add CI pipeline for tests, linting, and dependency scanning.
