# src/research_companion/observability/models.py

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4


VALID_RUN_STATUSES = {
    "created",
    "running",
    "needs_retry",
    "insufficient_evidence",
    "waiting_for_human",
    "completed",
    "failed",
}


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


@dataclass
class RunRecord:
    run_id: str

    started_at: str

    research_topic: str
    research_question: str
    user_request: str

    status: str

    completed_at: Optional[str] = None

    error: Optional[str] = None

    @classmethod
    def create(
        cls,
        research_topic: str,
        research_question: str,
        user_request: str,
    ) -> "RunRecord":

        return cls(
            run_id=str(uuid4()),
            started_at=utc_now_iso(),
            research_topic=research_topic,
            research_question=research_question,
            user_request=user_request,
            status="created",
        )

    def set_status(
        self,
        status: str,
    ) -> None:

        if status not in VALID_RUN_STATUSES:
            raise ValueError(
                f"Invalid run status: {status}"
            )

        self.status = status

    def complete(
        self,
    ) -> None:

        self.status = "completed"
        self.completed_at = (
            utc_now_iso()
        )

    def fail(
        self,
        error: str,
    ) -> None:

        self.status = "failed"
        self.error = error
        self.completed_at = (
            utc_now_iso()
        )


@dataclass
class RunEvent:
    id: str

    run_id: str
    timestamp: str

    event_type: str

    job: Optional[str] = None
    step: Optional[str] = None
    status: Optional[str] = None

    message: Optional[str] = None

    data: Optional[
        dict[str, Any]
    ] = None

    @classmethod
    def create(
        cls,
        run_id: str,
        event_type: str,
        job: str | None = None,
        step: str | None = None,
        status: str | None = None,
        message: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> "RunEvent":

        return cls(
            id=str(uuid4()),
            run_id=run_id,
            timestamp=utc_now_iso(),
            event_type=event_type,
            job=job,
            step=step,
            status=status,
            message=message,
            data=data or {},
        )