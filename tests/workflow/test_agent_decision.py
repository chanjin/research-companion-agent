# tests/workflow/test_agent_decision.py

from research_companion.agent import (
    ResearchCompanionAgent,
)
from research_companion.memory.service import (
    MemoryService,
)
from research_companion.memory.store import (
    SQLiteMemoryStore,
)


def build_agent(
    tmp_path,
):

    store = SQLiteMemoryStore(
        db_path=(
            tmp_path / "memory.db"
        )
    )

    memory = MemoryService(
        store=store
    )

    agent = ResearchCompanionAgent(
        memory_service=memory
    )

    return agent


def test_approved_rq_updates_context(
    tmp_path,
):

    agent = build_agent(
        tmp_path
    )

    agent.set_research_context(
        topic="AI Agent Governance",
        research_question="Original RQ",
    )

    agent.make_research_decision(
        decision_type="rq_selection",
        target_type="research_question",
        decision="approve",
        original_content="Approved RQ",
        reason="Clear and measurable.",
    )

    assert (
        agent.research_question
        == "Approved RQ"
    )


def test_revised_rq_updates_context(
    tmp_path,
):

    agent = build_agent(
        tmp_path
    )

    agent.set_research_context(
        topic="AI Agent Governance",
        research_question="Original RQ",
    )

    agent.make_research_decision(
        decision_type="rq_revision",
        target_type="research_question",
        decision="revise",
        original_content="Candidate RQ",
        revised_content=(
            "Revised RQ with explicit "
            "authority boundaries"
        ),
        reason=(
            "Authority should be measurable."
        ),
    )

    assert (
        agent.research_question
        == (
            "Revised RQ with explicit "
            "authority boundaries"
        )
    )


def test_rejected_rq_does_not_update_context(
    tmp_path,
):

    agent = build_agent(
        tmp_path
    )

    agent.set_research_context(
        topic="AI Agent Governance",
        research_question="Current RQ",
    )

    agent.make_research_decision(
        decision_type="rq_selection",
        target_type="research_question",
        decision="reject",
        original_content="Rejected RQ",
        reason="Too broad.",
    )

    assert (
        agent.research_question
        == "Current RQ"
    )


def test_decision_is_stored_in_memory(
    tmp_path,
):

    agent = build_agent(
        tmp_path
    )

    agent.set_research_context(
        topic="AI Agent Governance",
        research_question="Current RQ",
    )

    agent.make_research_decision(
        decision_type="rq_selection",
        target_type="research_question",
        decision="approve",
        original_content="Selected RQ",
        reason="Best candidate.",
    )

    episodes = (
        agent.recall_research_memory(
            research_question="Current RQ"
        )
    )

    assert len(episodes) == 1

    assert (
        "Selected RQ"
        in episodes[0].details
    )