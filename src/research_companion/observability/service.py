# src/research_companion/observability/service.py

from research_companion.observability.models import (
    RunEvent,
    RunRecord,
    utc_now_iso,
)
from research_companion.observability.store import (
    SQLiteRunStore,
)


class ObservabilityService:

    def __init__(
        self,
        store: SQLiteRunStore | None = None,
    ):

        self.store = (
            store
            if store is not None
            else SQLiteRunStore()
        )

    # =======================================
    # Run Lifecycle
    # =======================================

    def start_run(
        self,
        research_topic: str,
        research_question: str,
        user_request: str,
    ) -> RunRecord:

        run = RunRecord.create(
            research_topic=research_topic,
            research_question=(
                research_question
            ),
            user_request=user_request,
        )

        run.set_status(
            "running"
        )

        self.store.save_run(
            run
        )

        self.log_event(
            run_id=run.run_id,
            event_type=(
                "orchestration_started"
            ),
            job="orchestrator",
            step="initialize",
            status="running",
            message=(
                "Research workflow started."
            ),
        )

        return run

    def update_run_status(
        self,
        run_id: str,
        status: str,
        error: str | None = None,
        research_question: str | None = None,
    ) -> RunRecord:

        run = self.store.get_run(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Run not found: {run_id}"
            )

        run.set_status(
            status
        )

        if research_question is not None:
            run.research_question = (
                research_question
            )

        if error is not None:
            run.error = error

        if status in {
            "completed",
            "failed",
            "needs_retry",
            "insufficient_evidence",
        }:
            run.completed_at = (
                utc_now_iso()
            )

        self.store.update_run(
            run
        )

        return run

    def complete_run(
        self,
        run_id: str,
        research_question: str | None = None,
    ) -> RunRecord:

        return self.update_run_status(
            run_id=run_id,
            status="completed",
            research_question=(
                research_question
            ),
        )

    def fail_run(
        self,
        run_id: str,
        error: str,
    ) -> RunRecord:

        self.log_event(
            run_id=run_id,
            event_type="run_failed",
            job="orchestrator",
            step="exception",
            status="failed",
            message=error,
        )

        return self.update_run_status(
            run_id=run_id,
            status="failed",
            error=error,
        )

    # =======================================
    # Events
    # =======================================

    def log_event(
        self,
        run_id: str,
        event_type: str,
        job: str | None = None,
        step: str | None = None,
        status: str | None = None,
        message: str | None = None,
        data: dict | None = None,
    ) -> RunEvent:

        event = RunEvent.create(
            run_id=run_id,
            event_type=event_type,
            job=job,
            step=step,
            status=status,
            message=message,
            data=data,
        )

        self.store.save_event(
            event
        )

        return event

    # =======================================
    # Query
    # =======================================

    def get_run(
        self,
        run_id: str,
    ) -> RunRecord | None:

        return self.store.get_run(
            run_id
        )

    def list_runs(
        self,
        limit: int = 20,
    ) -> list[RunRecord]:

        return self.store.list_runs(
            limit=limit
        )

    def get_events(
        self,
        run_id: str,
    ) -> list[RunEvent]:

        return self.store.get_events(
            run_id
        )