# tests/workflow/test_evaluation_service.py

from research_companion.evaluation.service import (
    EvaluationService,
)
from research_companion.observability.service import (
    ObservabilityService,
)
from research_companion.observability.store import (
    SQLiteRunStore,
)


def build_services(
    tmp_path,
):

    store = SQLiteRunStore(
        db_path=(
            tmp_path / "runs.db"
        )
    )

    observability = (
        ObservabilityService(
            store=store
        )
    )

    evaluation = (
        EvaluationService(
            observability=observability
        )
    )

    return (
        observability,
        evaluation,
    )


def create_successful_trace(
    observability,
):

    run = observability.start_run(
        research_topic=(
            "Agent Governance"
        ),
        research_question=(
            "Test RQ"
        ),
        user_request=(
            "Research this topic."
        ),
    )

    observability.log_event(
        run_id=run.run_id,
        event_type="job_completed",
        job="literature_scout",
        status="success",
    )

    observability.log_event(
        run_id=run.run_id,
        event_type="job_completed",
        job="paper_reader",
        status="success",
        data={
            "successful_papers": 3,
        },
    )

    observability.log_event(
        run_id=run.run_id,
        event_type="job_completed",
        job="research_analyst",
        status="success",
    )

    observability.log_event(
        run_id=run.run_id,
        event_type="job_completed",
        job="research_partner",
        status="success",
    )

    observability.log_event(
        run_id=run.run_id,
        event_type=(
            "waiting_for_human"
        ),
        job="human_review",
        status=(
            "waiting_for_human"
        ),
    )

    observability.update_run_status(
        run_id=run.run_id,
        status="waiting_for_human",
    )

    return run


def test_evaluate_waiting_for_human_run(
    tmp_path,
):

    (
        observability,
        evaluation,
    ) = build_services(
        tmp_path
    )

    run = create_successful_trace(
        observability
    )

    report = (
        evaluation.evaluate_run(
            run.run_id
        )
    )

    assert (
        report.run_id
        == run.run_id
    )

    assert (
        report.overall_pass
        is True
    )

    assert len(
        report.checks
    ) == 6


def test_completed_run_with_human_decision(
    tmp_path,
):

    (
        observability,
        evaluation,
    ) = build_services(
        tmp_path
    )

    run = create_successful_trace(
        observability
    )

    observability.log_event(
        run_id=run.run_id,
        event_type=(
            "human_decision"
        ),
        job="human_review",
        status="approve",
    )

    observability.log_event(
        run_id=run.run_id,
        event_type=(
            "run_completed"
        ),
        job="orchestrator",
        status="completed",
    )

    observability.complete_run(
        run_id=run.run_id,
        research_question=(
            "Approved RQ"
        ),
    )

    report = (
        evaluation.evaluate_run(
            run.run_id
        )
    )

    authority_checks = [
        check
        for check in report.checks
        if check.category
        == "authority"
    ]

    assert len(
        authority_checks
    ) == 1

    assert (
        authority_checks[0]
        .passed
        is True
    )

    assert (
        report.overall_pass
        is True
    )


def test_authority_violation_detected(
    tmp_path,
):

    (
        observability,
        evaluation,
    ) = build_services(
        tmp_path
    )

    run = create_successful_trace(
        observability
    )

    # Human decision 전에 completed
    observability.log_event(
        run_id=run.run_id,
        event_type=(
            "run_completed"
        ),
        job="orchestrator",
        status="completed",
    )

    observability.log_event(
        run_id=run.run_id,
        event_type=(
            "human_decision"
        ),
        job="human_review",
        status="approve",
    )

    observability.complete_run(
        run_id=run.run_id
    )

    report = (
        evaluation.evaluate_run(
            run.run_id
        )
    )

    assert (
        report.overall_pass
        is False
    )

    assert len(
        report.violations
    ) >= 1


def test_unknown_run_fails(
    tmp_path,
):

    (
        observability,
        evaluation,
    ) = build_services(
        tmp_path
    )

    try:

        evaluation.evaluate_run(
            "unknown-run"
        )

        assert False

    except ValueError as error:

        assert (
            "Run not found"
            in str(error)
        )