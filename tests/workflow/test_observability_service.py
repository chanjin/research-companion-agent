# tests/workflow/test_observability_service.py

from research_companion.observability.service import (
    ObservabilityService,
)
from research_companion.observability.store import (
    SQLiteRunStore,
)


def build_observer(
    tmp_path,
):

    store = SQLiteRunStore(
        db_path=(
            tmp_path / "runs.db"
        )
    )

    return ObservabilityService(
        store=store
    )


def test_start_run(
    tmp_path,
):

    observer = build_observer(
        tmp_path
    )

    run = observer.start_run(
        research_topic="Agent Governance",
        research_question="RQ1",
        user_request="Research this.",
    )

    assert (
        run.status
        == "running"
    )

    loaded = observer.get_run(
        run.run_id
    )

    assert loaded is not None

    assert (
        loaded.status
        == "running"
    )

    events = observer.get_events(
        run.run_id
    )

    assert len(events) == 1

    assert (
        events[0].event_type
        == "orchestration_started"
    )


def test_log_event(
    tmp_path,
):

    observer = build_observer(
        tmp_path
    )

    run = observer.start_run(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    observer.log_event(
        run_id=run.run_id,
        event_type="job_completed",
        job="literature_scout",
        status="success",
        data={
            "selected_count": 5
        },
    )

    events = observer.get_events(
        run.run_id
    )

    assert len(events) == 2

    assert (
        events[1].data[
            "selected_count"
        ]
        == 5
    )


def test_complete_run(
    tmp_path,
):

    observer = build_observer(
        tmp_path
    )

    run = observer.start_run(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    observer.complete_run(
        run_id=run.run_id,
        research_question=(
            "Revised RQ"
        ),
    )

    loaded = observer.get_run(
        run.run_id
    )

    assert (
        loaded.status
        == "completed"
    )

    assert (
        loaded.research_question
        == "Revised RQ"
    )

    assert (
        loaded.completed_at
        is not None
    )


def test_fail_run(
    tmp_path,
):

    observer = build_observer(
        tmp_path
    )

    run = observer.start_run(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    observer.fail_run(
        run_id=run.run_id,
        error="Test failure",
    )

    loaded = observer.get_run(
        run.run_id
    )

    assert (
        loaded.status
        == "failed"
    )

    assert (
        loaded.error
        == "Test failure"
    )

    events = observer.get_events(
        run.run_id
    )

    assert any(
        event.event_type
        == "run_failed"
        for event in events
    )


def test_run_and_events_persist(
    tmp_path,
):

    db_path = (
        tmp_path / "runs.db"
    )

    store1 = SQLiteRunStore(
        db_path=db_path
    )

    observer1 = (
        ObservabilityService(
            store=store1
        )
    )

    run = observer1.start_run(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    observer1.log_event(
        run_id=run.run_id,
        event_type=(
            "test_event"
        ),
        message=(
            "Persistent event"
        ),
    )

    store2 = SQLiteRunStore(
        db_path=db_path
    )

    observer2 = (
        ObservabilityService(
            store=store2
        )
    )

    loaded_run = (
        observer2.get_run(
            run.run_id
        )
    )

    events = (
        observer2.get_events(
            run.run_id
        )
    )

    assert loaded_run is not None

    assert any(
        event.message
        == "Persistent event"
        for event in events
    )