from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.leaderos.models import DecisionCreate, DecisionStatus
from backend.leaderos.repository import DecisionRepository
from backend.leaderos.service import DecisionService


def test_decision_lifecycle() -> None:
    service = DecisionService(DecisionRepository())

    created = service.create_decision(
        DecisionCreate(title="Launch v1", description="Prepare GTM execution plan")
    )
    assert created.id == 1
    assert created.status == DecisionStatus.pending

    updated = service.update_status(created.id, DecisionStatus.completed)
    assert updated.status == DecisionStatus.completed

    metrics = service.dashboard()
    assert metrics.total_decisions == 1
    assert metrics.completed == 1
    assert metrics.execution_score == 100.0

    service.delete_decision(created.id)
    assert service.list_decisions() == []


def test_invalid_title_is_rejected() -> None:
    try:
        DecisionCreate(title="No", description="Too short title")
        assert False, "Validation should fail for short title"
    except Exception as exc:
        assert "String should have at least 3 characters" in str(exc)
