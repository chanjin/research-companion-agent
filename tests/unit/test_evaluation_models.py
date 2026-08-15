# tests/unit/test_evaluation_models.py

from research_companion.evaluation.models import (
    EvaluationCheck,
    EvaluationReport,
)


def test_evaluation_report_pass():

    checks = [
        EvaluationCheck(
            rule_id="R1",
            category="test",
            name="Rule 1",
            passed=True,
            score=1.0,
            message="Passed",
            severity="violation",
        ),
        EvaluationCheck(
            rule_id="R2",
            category="test",
            name="Rule 2",
            passed=True,
            score=0.8,
            message="Passed",
            severity="warning",
        ),
    ]

    report = EvaluationReport.create(
        run_id="run-1",
        checks=checks,
    )

    assert (
        report.overall_pass
        is True
    )

    assert (
        report.overall_score
        == 0.9
    )

    assert (
        report.violations
        == []
    )


def test_warning_does_not_fail_run():

    checks = [
        EvaluationCheck(
            rule_id="R1",
            category="evidence",
            name="Evidence",
            passed=False,
            score=0.5,
            message=(
                "Limited evidence."
            ),
            severity="warning",
        )
    ]

    report = EvaluationReport.create(
        run_id="run-1",
        checks=checks,
    )

    assert (
        report.overall_pass
        is True
    )

    assert len(
        report.warnings
    ) == 1


def test_violation_fails_report():

    checks = [
        EvaluationCheck(
            rule_id="AUTHORITY-001",
            category="authority",
            name="Authority",
            passed=False,
            score=0.0,
            message=(
                "Authority violation."
            ),
            severity="violation",
        )
    ]

    report = EvaluationReport.create(
        run_id="run-1",
        checks=checks,
    )

    assert (
        report.overall_pass
        is False
    )

    assert len(
        report.violations
    ) == 1