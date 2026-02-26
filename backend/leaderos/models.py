"""Domain models and API schemas for LeaderOS."""

from enum import Enum

from pydantic import BaseModel, Field


class DecisionStatus(str, Enum):
    """Valid lifecycle states for a decision."""

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"


class DecisionCreate(BaseModel):
    """Payload for creating a decision."""

    title: str = Field(..., min_length=3, max_length=120, description="Short decision title")
    description: str = Field(..., min_length=5, max_length=1000, description="Decision details")


class DecisionUpdate(BaseModel):
    """Payload for updating a decision's status."""

    status: DecisionStatus


class Decision(BaseModel):
    """Decision resource representation."""

    id: int = Field(..., ge=1)
    title: str
    description: str
    status: DecisionStatus


class DashboardMetrics(BaseModel):
    """High-level execution metrics for the dashboard."""

    total_decisions: int = Field(..., ge=0)
    completed: int = Field(..., ge=0)
    pending: int = Field(..., ge=0)
    in_progress: int = Field(..., ge=0)
    blocked: int = Field(..., ge=0)
    execution_score: float = Field(..., ge=0, le=100)
