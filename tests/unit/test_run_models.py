# tests/unit/test_run_models.py

import pytest

from research_companion.observability.models import (
    RunEvent,
    RunRecord,
)


def test_create_run_record():

    run = RunRecord.create(
        research_topic="Agent Governance",
        research_question="Test RQ",
        user_request="Research this.",
    )

    assert run.run_id

    assert run.started_at

    assert (
        run.status
        == "created"
    )

    assert (
        run.research_question
        == "Test RQ"
    )


def test_run_status():

    run = RunRecord.create(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    run.set_status(
        "running"
    )

    assert (
        run.status
        == "running"
    )


def test_invalid_run_status():

    run = RunRecord.create(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    with pytest.raises(
        ValueError,
        match="Invalid run status",
    ):

        run.set_status(
            "unknown"
        )


def test_complete_run():

    run = RunRecord.create(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    run.complete()

    assert (
        run.status
        == "completed"
    )

    assert (
        run.completed_at
        is not None
    )


def test_fail_run():

    run = RunRecord.create(
        research_topic="Topic",
        research_question="RQ",
        user_request="Request",
    )

    run.fail(
        "Something failed"
    )

    assert (
        run.status
        == "failed"
    )

    assert (
        run.error
        == "Something failed"
    )


def test_create_event():

    event = RunEvent.create(
        run_id="run-1",
        event_type="job_completed",
        job="literature_scout",
        step="search",
        status="success",
        data={
            "selected_count": 5,
        },
    )

    assert event.id

    assert (
        event.run_id
        == "run-1"
    )

    assert (
        event.data[
            "selected_count"
        ]
        == 5
    )