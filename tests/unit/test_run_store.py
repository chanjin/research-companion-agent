# tests/unit/test_run_store.py

from research_companion.observability.models import (
    RunEvent,
    RunRecord,
)
from research_companion.observability.store import (
    SQLiteRunStore,
)


def test_save_and_get_run(
    tmp_path,
):

    store = SQLiteRunStore(
        db_path=(
            tmp_path / "runs.db"
        )
    )

    run = RunRecord.create(
        research_topic="Agent Governance",
        research_question="RQ1",
        user_request="Research this.",
    )

    store.save_run(
        run
    )

    loaded = store.get_run(
        run.run_id
    )

    assert loaded is not None

    assert (
        loaded.run_id
        == run.run_id
    )

    assert (
        loaded.research_question
        == "RQ1"
    )


def test_update_run(
    tmp_path,
):

    store = SQLiteRunStore(
        db_path=(
            tmp_path / "runs.db"
        )
    )

    run = RunRecord.create(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    store.save_run(
        run
    )

    run.set_status(
        "waiting_for_human"
    )

    store.update_run(
        run
    )

    loaded = store.get_run(
        run.run_id
    )

    assert (
        loaded.status
        == "waiting_for_human"
    )


def test_list_runs(
    tmp_path,
):

    store = SQLiteRunStore(
        db_path=(
            tmp_path / "runs.db"
        )
    )

    for index in range(3):

        store.save_run(
            RunRecord.create(
                research_topic="Topic",
                research_question=(
                    f"RQ {index}"
                ),
                user_request="Request",
            )
        )

    runs = store.list_runs(
        limit=10
    )

    assert len(runs) == 3


def test_save_and_get_events(
    tmp_path,
):

    store = SQLiteRunStore(
        db_path=(
            tmp_path / "runs.db"
        )
    )

    run = RunRecord.create(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    store.save_run(
        run
    )

    event1 = RunEvent.create(
        run_id=run.run_id,
        event_type="job_started",
        job="literature_scout",
    )

    event2 = RunEvent.create(
        run_id=run.run_id,
        event_type="job_completed",
        job="literature_scout",
        data={
            "selected_count": 5
        },
    )

    store.save_event(
        event1
    )

    store.save_event(
        event2
    )

    events = store.get_events(
        run.run_id
    )

    assert len(events) == 2

    assert (
        events[0].event_type
        == "job_started"
    )

    assert (
        events[1].data[
            "selected_count"
        ]
        == 5
    )


def test_runs_persist_across_store_instances(
    tmp_path,
):

    db_path = (
        tmp_path / "runs.db"
    )

    store1 = SQLiteRunStore(
        db_path=db_path
    )

    run = RunRecord.create(
        research_topic="Topic",
        research_question=(
            "Persistent RQ"
        ),
        user_request="Request",
    )

    store1.save_run(
        run
    )

    store2 = SQLiteRunStore(
        db_path=db_path
    )

    loaded = store2.get_run(
        run.run_id
    )

    assert loaded is not None

    assert (
        loaded.research_question
        == "Persistent RQ"
    )