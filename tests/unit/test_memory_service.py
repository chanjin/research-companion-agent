# tests/workflow/test_memory_service.py

from research_companion.memory.service import (
    MemoryService,
)
from research_companion.memory.store import (
    SQLiteMemoryStore,
)


def test_memory_service_remember_and_recall(
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

    memory.remember(
        episode_type="research_decision",
        summary="Selected job-bounded agents",
        details=(
            "Researcher selected explicit "
            "Scope, Responsibility, Authority."
        ),
        research_question="RQ1",
        importance=5,
    )

    result = memory.recall(
        research_question="RQ1",
        limit=5,
    )

    assert len(result) == 1

    assert (
        result[0].summary
        == "Selected job-bounded agents"
    )


def test_memory_context_generation(
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

    memory.remember(
        episode_type="rq_revision",
        summary="RQ revised",
        details=(
            "Compare workflow-node "
            "and job-bounded agents."
        ),
        research_question="RQ1",
        importance=5,
    )

    context = (
        memory.build_memory_context(
            research_question="RQ1",
            limit=5,
        )
    )

    assert (
        "RQ revised"
        in context
    )

    assert (
        "job-bounded agents"
        in context
    )


def test_empty_memory_context(
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

    context = (
        memory.build_memory_context(
            research_question="UNKNOWN"
        )
    )

    assert (
        context
        == (
            "No relevant episodic "
            "memory available."
        )
    )