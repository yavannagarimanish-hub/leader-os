"""Repository layer for decision persistence.

This implementation uses an in-memory store and is intentionally small,
while keeping a clear contract for replacing it with a database later.
"""

from __future__ import annotations

from threading import Lock

from backend.leaderos.models import Decision, DecisionCreate, DecisionStatus


class DecisionRepository:
    """Thread-safe in-memory repository for decisions."""

    def __init__(self) -> None:
        self._decisions: dict[int, Decision] = {}
        self._next_id = 1
        self._lock = Lock()

    def create(self, payload: DecisionCreate) -> Decision:
        with self._lock:
            decision = Decision(
                id=self._next_id,
                title=payload.title,
                description=payload.description,
                status=DecisionStatus.pending,
            )
            self._decisions[decision.id] = decision
            self._next_id += 1
            return decision

    def list_all(self) -> list[Decision]:
        with self._lock:
            return sorted(self._decisions.values(), key=lambda d: d.id)

    def get(self, decision_id: int) -> Decision | None:
        with self._lock:
            return self._decisions.get(decision_id)

    def update_status(self, decision_id: int, status: DecisionStatus) -> Decision | None:
        with self._lock:
            decision = self._decisions.get(decision_id)
            if decision is None:
                return None
            updated = decision.model_copy(update={"status": status})
            self._decisions[decision_id] = updated
            return updated

    def delete(self, decision_id: int) -> bool:
        with self._lock:
            if decision_id not in self._decisions:
                return False
            del self._decisions[decision_id]
            return True
