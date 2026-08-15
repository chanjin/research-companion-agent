# tests/workflow/test_decision_service.py

from research_companion.decisions.service import (
    DecisionService,
)
from research_companion.memory.service import (
    MemoryService,
)
from research_companion.memory.store import (
    SQLiteMemoryStore,
)


def build_decision_service(
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

    service = DecisionService(
        memory_service=memory
    )

    return service, memory


def test_process_approve_decision(
    tmp_path,
):

    service, memory = (
        build_decision_service(
            tmp_path
        )
    )

    decision = (
        service.process_decision(
            decision_type="rq_selection",
            target_type="research_question",
            decision="approve",
            original_content="Candidate RQ",
            reason="Measurable and clear.",
            research_question="Current RQ",
        )
    )

    assert (
        decision.final_content
        == "Candidate RQ"
    )

    episodes = memory.recall(
        research_question="Current RQ",
        limit=5,
    )

    assert len(episodes) == 1

    assert (
        episodes[0].source
        == "researcher"
    )

    assert (
        episodes[0].importance
        == 5
    )


def test_process_revision(
    tmp_path,
):

    service, memory = (
        build_decision_service(
            tmp_path
        )
    )

    decision = (
        service.process_decision(
            decision_type="rq_revision",
            target_type="research_question",
            decision="revise",
            original_content="Old RQ",
            revised_content="New RQ",
            reason="Authority must be explicit.",
            research_question="Old RQ",
        )
    )

    assert (
        decision.final_content
        == "New RQ"
    )

    episodes = memory.recall(
        research_question="Old RQ"
    )

    assert len(episodes) == 1

    assert (
        "New RQ"
        in episodes[0].details
    )

    assert (
        "Authority must be explicit"
        in episodes[0].details
    )


def test_rejected_decision_is_remembered(
    tmp_path,
):

    service, memory = (
        build_decision_service(
            tmp_path
        )
    )

    decision = (
        service.process_decision(
            decision_type=(
                "research_direction"
            ),
            target_type=(
                "research_direction"
            ),
            decision="reject",
            original_content=(
                "Prompt-only comparison"
            ),
            reason=(
                "Architecture-level contribution "
                "is preferred."
            ),
            research_question="RQ1",
        )
    )

    assert (
        decision.final_content
        is None
    )

    episodes = memory.recall(
        research_question="RQ1"
    )

    assert len(episodes) == 1

    assert (
        "reject"
        in episodes[0].summary.lower()
    )


def test_decision_persists_across_services(
    tmp_path,
):

    db_path = (
        tmp_path / "memory.db"
    )

    store1 = SQLiteMemoryStore(
        db_path=db_path
    )

    memory1 = MemoryService(
        store=store1
    )

    service1 = DecisionService(
        memory_service=memory1
    )

    service1.process_decision(
        decision_type="rq_selection",
        target_type="research_question",
        decision="approve",
        original_content="Persistent RQ",
        reason="Selected by researcher.",
        research_question="RQ1",
    )

    # 새로운 Store / Memory / Service 생성
    store2 = SQLiteMemoryStore(
        db_path=db_path
    )

    memory2 = MemoryService(
        store=store2
    )

    episodes = memory2.recall(
        research_question="RQ1"
    )

    assert len(episodes) == 1

    assert (
        "Persistent RQ"
        in episodes[0].details
    )