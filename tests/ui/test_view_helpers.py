# tests/ui/test_view_helpers.py

from types import SimpleNamespace

from research_companion.ui.helpers import (
    can_apply_human_decision,
    get_candidate_research_questions,
    get_run_status_summary,
    get_selected_papers,
)


def test_get_run_status_summary():

    state = SimpleNamespace(
        status="waiting_for_human",
        current_job="human_review",
        current_step=(
            "waiting_for_human_decision"
        ),
        research_question="Test RQ",
        error=None,
    )

    result = (
        get_run_status_summary(
            state
        )
    )

    assert (
        result["status"]
        == "waiting_for_human"
    )

    assert (
        result["current_job"]
        == "human_review"
    )

    assert (
        result["research_question"]
        == "Test RQ"
    )


def test_get_run_status_summary_none():

    result = (
        get_run_status_summary(
            None
        )
    )

    assert (
        result["status"]
        == "not_started"
    )


def test_get_selected_papers():

    state = SimpleNamespace(
        search_state=(
            SimpleNamespace(
                selected_papers=[
                    {
                        "title": "Paper A"
                    },
                    {
                        "title": "Paper B"
                    },
                ]
            )
        )
    )

    result = (
        get_selected_papers(
            state
        )
    )

    assert len(result) == 2

    assert (
        result[0]["title"]
        == "Paper A"
    )


def test_get_candidate_research_questions():

    state = SimpleNamespace(
        partner_state=(
            SimpleNamespace(
                proposal={
                    "refined_research_questions": [
                        {
                            "rq": "RQ 1",
                            "rationale": (
                                "Reason 1"
                            ),
                        },
                        {
                            "rq": "RQ 2",
                            "rationale": (
                                "Reason 2"
                            ),
                        },
                    ]
                }
            )
        )
    )

    result = (
        get_candidate_research_questions(
            state
        )
    )

    assert len(result) == 2

    assert (
        result[1]["rq"]
        == "RQ 2"
    )


def test_can_apply_human_decision():

    state = SimpleNamespace(
        status=(
            "waiting_for_human"
        ),
        pending_human_decision=True,
    )

    assert (
        can_apply_human_decision(
            state
        )
        is True
    )


def test_cannot_apply_human_decision():

    state = SimpleNamespace(
        status="running",
        pending_human_decision=False,
    )

    assert (
        can_apply_human_decision(
            state
        )
        is False
    )