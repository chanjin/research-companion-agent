# tests/unit/test_evaluation_rules.py

from types import SimpleNamespace

from research_companion.evaluation.rules import (
    check_authority_boundary,
    check_human_gate,
    check_minimum_evidence,
    check_required_workflow,
)


def make_event(
    event_type,
    job=None,
    status=None,
    data=None,
):

    return SimpleNamespace(
        event_type=event_type,
        job=job,
        status=status,
        data=data or {},
    )


def test_required_workflow_success():

    run = SimpleNamespace(
        status="waiting_for_human"
    )

    events = [
        make_event(
            "job_completed",
            job="literature_scout",
            status="success",
        ),
        make_event(
            "job_completed",
            job="paper_reader",
            status="success",
        ),
        make_event(
            "job_completed",
            job="research_analyst",
            status="success",
        ),
        make_event(
            "job_completed",
            job="research_partner",
            status="success",
        ),
    ]

    result = check_required_workflow(
        run,
        events,
    )

    assert result.passed is True

    assert result.score == 1.0


def test_required_workflow_missing_job():

    run = SimpleNamespace(
        status="waiting_for_human"
    )

    events = [
        make_event(
            "job_completed",
            job="literature_scout",
            status="success",
        ),
        make_event(
            "job_completed",
            job="paper_reader",
            status="success",
        ),
        make_event(
            "job_completed",
            job="research_partner",
            status="success",
        ),
    ]

    result = check_required_workflow(
        run,
        events,
    )

    assert result.passed is False


def test_minimum_evidence_success():

    run = SimpleNamespace(
        status="running"
    )

    events = [
        make_event(
            "job_completed",
            job="paper_reader",
            status="success",
            data={
                "successful_papers": 3
            },
        )
    ]

    result = check_minimum_evidence(
        run,
        events,
    )

    assert result.passed is True


def test_minimum_evidence_failure():

    run = SimpleNamespace(
        status="running"
    )

    events = [
        make_event(
            "job_completed",
            job="paper_reader",
            status="success",
            data={
                "successful_papers": 1
            },
        )
    ]

    result = check_minimum_evidence(
        run,
        events,
    )

    assert result.passed is False

    assert result.score == 0.5


def test_authority_boundary_success():

    run = SimpleNamespace(
        status="completed"
    )

    events = [
        make_event(
            "human_decision"
        ),
        make_event(
            "run_completed"
        ),
    ]

    result = (
        check_authority_boundary(
            run,
            events,
        )
    )

    assert result.passed is True


def test_authority_boundary_violation():

    run = SimpleNamespace(
        status="completed"
    )

    events = [
        make_event(
            "run_completed"
        ),
        make_event(
            "human_decision"
        ),
    ]

    result = (
        check_authority_boundary(
            run,
            events,
        )
    )

    assert result.passed is False

    assert (
        result.severity
        == "violation"
    )


def test_human_gate_success():

    run = SimpleNamespace(
        status="waiting_for_human"
    )

    events = [
        make_event(
            "job_completed",
            job="research_partner",
            status="success",
        ),
        make_event(
            "waiting_for_human",
            job="human_review",
        ),
    ]

    result = check_human_gate(
        run,
        events,
    )

    assert result.passed is True


def test_human_gate_failure():

    run = SimpleNamespace(
        status="completed"
    )

    events = [
        make_event(
            "job_completed",
            job="research_partner",
            status="success",
        ),
        make_event(
            "run_completed"
        ),
    ]

    result = check_human_gate(
        run,
        events,
    )

    assert result.passed is False