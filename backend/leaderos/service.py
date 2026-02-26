"""Business logic layer for decision workflows."""

from fastapi import HTTPException, status

from backend.leaderos.models import DashboardMetrics, Decision, DecisionCreate, DecisionStatus
from backend.leaderos.repository import DecisionRepository


class DecisionService:
    """Encapsulates decision operations and analytics."""

    def __init__(self, repository: DecisionRepository) -> None:
        self._repository = repository

    def create_decision(self, payload: DecisionCreate) -> Decision:
        return self._repository.create(payload)

    def list_decisions(self) -> list[Decision]:
        return self._repository.list_all()

    def update_status(self, decision_id: int, status_value: DecisionStatus) -> Decision:
        updated = self._repository.update_status(decision_id, status_value)
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Decision not found")
        return updated

    def delete_decision(self, decision_id: int) -> None:
        deleted = self._repository.delete(decision_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Decision not found")

    def dashboard(self) -> DashboardMetrics:
        decisions = self._repository.list_all()

        total = len(decisions)
        completed = sum(1 for d in decisions if d.status == DecisionStatus.completed)
        pending = sum(1 for d in decisions if d.status == DecisionStatus.pending)
        in_progress = sum(1 for d in decisions if d.status == DecisionStatus.in_progress)
        blocked = sum(1 for d in decisions if d.status == DecisionStatus.blocked)

        execution_score = round((completed / total) * 100, 2) if total else 0.0

        return DashboardMetrics(
            total_decisions=total,
            completed=completed,
            pending=pending,
            in_progress=in_progress,
            blocked=blocked,
            execution_score=execution_score,
        )
