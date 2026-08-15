# tests/unit/test_research_decision.py

import pytest

from research_companion.decisions.models import (
    ResearchDecision,
)


def test_approve_decision():

    decision = ResearchDecision.create(
        decision_type="rq_selection",
        target_type="research_question",
        decision="approve",
        original_content="Original RQ",
        reason="Good research question.",
        research_question="Current RQ",
    )

    assert (
        decision.decision
        == "approve"
    )

    assert (
        decision.final_content
        == "Original RQ"
    )


def test_revise_decision():

    decision = ResearchDecision.create(
        decision_type="rq_revision",
        target_type="research_question",
        decision="revise",
        original_content="Original RQ",
        revised_content="Revised RQ",
        reason="Needs stronger authority concept.",
    )

    assert (
        decision.decision
        == "revise"
    )

    assert (
        decision.final_content
        == "Revised RQ"
    )


def test_reject_decision():

    decision = ResearchDecision.create(
        decision_type="rq_selection",
        target_type="research_question",
        decision="reject",
        original_content="Rejected RQ",
        reason="Too broad.",
    )

    assert (
        decision.final_content
        is None
    )


def test_defer_decision():

    decision = ResearchDecision.create(
        decision_type="rq_selection",
        target_type="research_question",
        decision="defer",
        original_content="Pending RQ",
    )

    assert (
        decision.final_content
        is None
    )


def test_invalid_decision():

    with pytest.raises(
        ValueError,
        match="Invalid decision",
    ):

        ResearchDecision.create(
            decision_type="rq_selection",
            target_type="research_question",
            decision="accept",
            original_content="Test RQ",
        )


def test_invalid_target_type():

    with pytest.raises(
        ValueError,
        match="Invalid target_type",
    ):

        ResearchDecision.create(
            decision_type="test",
            target_type="unknown",
            decision="approve",
            original_content="Test",
        )


def test_revise_requires_revised_content():

    with pytest.raises(
        ValueError,
        match="revised_content is required",
    ):

        ResearchDecision.create(
            decision_type="rq_revision",
            target_type="research_question",
            decision="revise",
            original_content="Old RQ",
        )


def test_original_content_required():

    with pytest.raises(
        ValueError,
        match="original_content",
    ):

        ResearchDecision.create(
            decision_type="rq_selection",
            target_type="research_question",
            decision="approve",
            original_content="",
        )