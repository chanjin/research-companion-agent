# src/research_companion/evaluation/models.py

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


@dataclass
class EvaluationCheck:
    """
    하나의 Specification Rule 평가 결과.
    """

    rule_id: str

    category: str

    name: str

    passed: bool

    score: float

    message: str

    severity: str = "warning"

    evidence: list[str] = field(
        default_factory=list
    )


@dataclass
class EvaluationReport:
    """
    하나의 Agent Run에 대한 전체 평가 결과.
    """

    run_id: str

    evaluated_at: str

    overall_pass: bool

    overall_score: float

    checks: list[
        EvaluationCheck
    ] = field(
        default_factory=list
    )

    violations: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    @classmethod
    def create(
        cls,
        run_id: str,
        checks: list[EvaluationCheck],
    ) -> "EvaluationReport":

        if checks:

            overall_score = sum(
                check.score
                for check in checks
            ) / len(checks)

        else:

            overall_score = 0.0

        violations = [
            check.message
            for check in checks
            if (
                not check.passed
                and check.severity
                == "violation"
            )
        ]

        warnings = [
            check.message
            for check in checks
            if (
                not check.passed
                and check.severity
                == "warning"
            )
        ]

        overall_pass = (
            len(violations) == 0
        )

        return cls(
            run_id=run_id,
            evaluated_at=(
                utc_now_iso()
            ),
            overall_pass=(
                overall_pass
            ),
            overall_score=round(
                overall_score,
                3,
            ),
            checks=checks,
            violations=violations,
            warnings=warnings,
        )