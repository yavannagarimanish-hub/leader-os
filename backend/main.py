"""LeaderOS FastAPI entrypoint."""

from fastapi import FastAPI, Response, status

from backend.leaderos.models import DashboardMetrics, Decision, DecisionCreate, DecisionUpdate
from backend.leaderos.repository import DecisionRepository
from backend.leaderos.service import DecisionService

app = FastAPI(
    title="LeaderOS",
    version="1.0.0",
    description="Execution intelligence API for leadership decision tracking.",
)

repository = DecisionRepository()
service = DecisionService(repository)


@app.get("/", tags=["health"])
def home() -> dict[str, str]:
    """Liveness endpoint for operational checks."""
    return {"product": "LeaderOS", "status": "running"}


@app.post("/decision", response_model=Decision, status_code=status.HTTP_201_CREATED, tags=["decisions"])
def create_decision(payload: DecisionCreate) -> Decision:
    """Create a new decision with validated input."""
    return service.create_decision(payload)


@app.get("/decisions", response_model=list[Decision], tags=["decisions"])
def get_decisions() -> list[Decision]:
    """List all decisions sorted by ID."""
    return service.list_decisions()


@app.put("/decision/{decision_id}", response_model=Decision, tags=["decisions"])
def update_decision(decision_id: int, payload: DecisionUpdate) -> Decision:
    """Update only mutable fields for a decision."""
    return service.update_status(decision_id=decision_id, status_value=payload.status)


@app.delete("/decision/{decision_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["decisions"])
def delete_decision(decision_id: int) -> Response:
    """Delete a decision resource by ID."""
    service.delete_decision(decision_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/dashboard", response_model=DashboardMetrics, tags=["analytics"])
def dashboard() -> DashboardMetrics:
    """Return aggregate execution metrics."""
    return service.dashboard()
