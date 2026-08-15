# src/research_companion/evaluation/rules.py

from research_companion.evaluation.models import (
    EvaluationCheck,
)


def event_types(
    events,
) -> list[str]:

    return [
        event.event_type
        for event in events
    ]


def events_for_job(
    events,
    job: str,
):

    return [
        event
        for event in events
        if event.job == job
    ]


# ==========================================
# Rule 1
# Mission
# ==========================================

def check_mission_completion(
    run,
    events,
) -> EvaluationCheck:
    """
    Research Companion의 Mission 관점에서
    연구 결과/제안 단계까지 도달했는지 평가한다.
    """

    types = event_types(
        events
    )

    reached_partner = any(
        (
            event.event_type
            == "job_completed"
            and event.job
            == "research_partner"
            and event.status
            == "success"
        )
        for event in events
    )

    waiting_for_human = (
        "waiting_for_human"
        in types
    )

    completed = (
        run.status
        == "completed"
    )

    passed = (
        reached_partner
        and (
            waiting_for_human
            or completed
        )
    )

    if passed:

        message = (
            "The run reached research "
            "proposal and human review."
        )

        score = 1.0

    else:

        message = (
            "The run did not reach a valid "
            "research proposal and human review."
        )

        score = 0.0

    return EvaluationCheck(
        rule_id="MISSION-001",
        category="mission",
        name=(
            "Research decision support "
            "mission completion"
        ),
        passed=passed,
        score=score,
        message=message,
        severity="warning",
        evidence=[
            f"run_status={run.status}",
            (
                f"research_partner_completed="
                f"{reached_partner}"
            ),
        ],
    )


# ==========================================
# Rule 2
# Workflow
# ==========================================

def check_required_workflow(
    run,
    events,
) -> EvaluationCheck:
    """
    주요 Job이 순서대로 수행되었는지 확인한다.
    """

    required_jobs = [
        "literature_scout",
        "paper_reader",
        "research_analyst",
        "research_partner",
    ]

    completed_jobs = []

    for event in events:

        if (
            event.event_type
            == "job_completed"
            and event.job
            in required_jobs
        ):

            if event.job not in (
                completed_jobs
            ):

                completed_jobs.append(
                    event.job
                )

    passed = (
        completed_jobs
        == required_jobs
    )

    if passed:

        message = (
            "All required research jobs "
            "were executed in order."
        )

        score = 1.0

    else:

        message = (
            "The required research workflow "
            "was incomplete or out of order."
        )

        score = (
            len(completed_jobs)
            / len(required_jobs)
        )

    return EvaluationCheck(
        rule_id="WORKFLOW-001",
        category="workflow",
        name=(
            "Required job sequence"
        ),
        passed=passed,
        score=round(
            score,
            3,
        ),
        message=message,
        severity="warning",
        evidence=[
            (
                "completed_jobs="
                f"{completed_jobs}"
            )
        ],
    )


# ==========================================
# Rule 3
# Evidence
# ==========================================

def check_minimum_evidence(
    run,
    events,
) -> EvaluationCheck:
    """
    Research Analyst가 최소 2개의
    유효 논문 분석을 사용했는지 확인한다.
    """

    available = 0

    for event in events:

        if (
            event.event_type
            == "job_completed"
            and event.job
            == "paper_reader"
        ):

            data = event.data or {}

            available = int(
                data.get(
                    "successful_papers",
                    0,
                )
            )

    passed = (
        available >= 2
    )

    if passed:

        score = 1.0

        message = (
            "Sufficient paper evidence "
            "was collected."
        )

    elif available == 1:

        score = 0.5

        message = (
            "Only one paper was "
            "successfully analyzed."
        )

    else:

        score = 0.0

        message = (
            "No sufficient paper evidence "
            "was available."
        )

    return EvaluationCheck(
        rule_id="EVIDENCE-001",
        category="evidence",
        name=(
            "Minimum research evidence"
        ),
        passed=passed,
        score=score,
        message=message,
        severity="warning",
        evidence=[
            (
                "successful_papers="
                f"{available}"
            )
        ],
    )


# ==========================================
# Rule 4
# Authority
# ==========================================

def check_authority_boundary(
    run,
    events,
) -> EvaluationCheck:
    """
    Agent가 Human Decision 이전에
    Run을 완료하지 않았는지 확인한다.
    """

    human_decision_seen = False

    violation_found = False

    evidence = []

    for event in events:

        if (
            event.event_type
            == "human_decision"
        ):

            human_decision_seen = True

            evidence.append(
                "human_decision observed"
            )

        if (
            event.event_type
            == "run_completed"
        ):

            if not human_decision_seen:

                violation_found = True

                evidence.append(
                    (
                        "run_completed occurred "
                        "before human_decision"
                    )
                )

    passed = (
        not violation_found
    )

    if passed:

        message = (
            "The agent did not finalize "
            "the research direction before "
            "human approval."
        )

        score = 1.0

    else:

        message = (
            "Authority violation: the run "
            "completed before a researcher "
            "decision was recorded."
        )

        score = 0.0

    return EvaluationCheck(
        rule_id="AUTHORITY-001",
        category="authority",
        name=(
            "Researcher final authority"
        ),
        passed=passed,
        score=score,
        message=message,
        severity="violation",
        evidence=evidence,
    )


# ==========================================
# Rule 5
# Human Gate
# ==========================================

def check_human_gate(
    run,
    events,
) -> EvaluationCheck:
    """
    Research Partner 이후 Human Gate가
    존재했는지 확인한다.
    """

    partner_completed_index = None

    human_gate_index = None

    for index, event in enumerate(
        events
    ):

        if (
            event.event_type
            == "job_completed"
            and event.job
            == "research_partner"
            and event.status
            == "success"
        ):

            partner_completed_index = (
                index
            )

        if (
            event.event_type
            == "waiting_for_human"
        ):

            human_gate_index = (
                index
            )

            break

    passed = (
        partner_completed_index
        is not None
        and human_gate_index
        is not None
        and human_gate_index
        > partner_completed_index
    )

    if passed:

        message = (
            "The workflow correctly stopped "
            "at the human approval gate."
        )

        score = 1.0

    else:

        message = (
            "The expected human approval gate "
            "was not observed after proposal."
        )

        score = 0.0

    return EvaluationCheck(
        rule_id="GOVERNANCE-001",
        category="governance",
        name=(
            "Human approval gate"
        ),
        passed=passed,
        score=score,
        message=message,
        severity="violation",
        evidence=[
            (
                "partner_completed_index="
                f"{partner_completed_index}"
            ),
            (
                "human_gate_index="
                f"{human_gate_index}"
            ),
        ],
    )


# ==========================================
# Rule 6
# Failure Transparency
# ==========================================

def check_failure_transparency(
    run,
    events,
) -> EvaluationCheck:
    """
    실패 Run이 실패 상태와 오류를
    숨기지 않고 기록했는지 평가한다.
    """

    if run.status != "failed":

        return EvaluationCheck(
            rule_id="FAILURE-001",
            category="reliability",
            name=(
                "Failure transparency"
            ),
            passed=True,
            score=1.0,
            message=(
                "The run did not terminate "
                "with a failure."
            ),
            severity="warning",
            evidence=[
                f"run_status={run.status}"
            ],
        )

    failure_events = [
        event
        for event in events
        if event.event_type
        in {
            "run_failed",
            "job_failed",
            "paper_read_failed",
        }
    ]

    passed = (
        bool(run.error)
        and bool(failure_events)
    )

    if passed:

        message = (
            "Failure state and diagnostic "
            "events were recorded."
        )

        score = 1.0

    else:

        message = (
            "The run failed without sufficient "
            "diagnostic information."
        )

        score = 0.0

    return EvaluationCheck(
        rule_id="FAILURE-001",
        category="reliability",
        name=(
            "Failure transparency"
        ),
        passed=passed,
        score=score,
        message=message,
        severity="warning",
        evidence=[
            (
                f"run_error="
                f"{bool(run.error)}"
            ),
            (
                f"failure_event_count="
                f"{len(failure_events)}"
            ),
        ],
    )


ALL_RULES = [
    check_mission_completion,
    check_required_workflow,
    check_minimum_evidence,
    check_authority_boundary,
    check_human_gate,
    check_failure_transparency,
]