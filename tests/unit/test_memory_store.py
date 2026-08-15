# tests/unit/test_memory_store.py

from research_companion.memory.models import (
    Episode,
)
from research_companion.memory.store import (
    SQLiteMemoryStore,
)


def test_save_and_get_episode(
    tmp_path,
):

    db_path = (
        tmp_path / "memory.db"
    )

    store = SQLiteMemoryStore(
        db_path=db_path
    )

    episode = Episode.create(
        episode_type="research_decision",
        summary="Selected direction",
        details="Focus on agent authority.",
        research_question="RQ1",
        source="researcher",
        importance=5,
    )

    store.save_episode(
        episode
    )

    loaded = store.get_episode(
        episode.id
    )

    assert loaded is not None

    assert (
        loaded.id
        == episode.id
    )

    assert (
        loaded.summary
        == episode.summary
    )

    assert (
        loaded.importance
        == 5
    )


def test_list_episodes_ordered_by_importance(
    tmp_path,
):

    db_path = (
        tmp_path / "memory.db"
    )

    store = SQLiteMemoryStore(
        db_path=db_path
    )

    low = Episode.create(
        episode_type="note",
        summary="Low",
        details="Low priority",
        importance=1,
    )

    high = Episode.create(
        episode_type="decision",
        summary="High",
        details="High priority",
        importance=5,
    )

    store.save_episode(low)
    store.save_episode(high)

    episodes = store.list_episodes(
        limit=10
    )

    assert (
        episodes[0].summary
        == "High"
    )


def test_find_by_type(
    tmp_path,
):

    store = SQLiteMemoryStore(
        db_path=(
            tmp_path / "memory.db"
        )
    )

    store.save_episode(
        Episode.create(
            episode_type="rq_revision",
            summary="RQ changed",
            details="Details",
        )
    )

    store.save_episode(
        Episode.create(
            episode_type="paper_selection",
            summary="Paper selected",
            details="Details",
        )
    )

    result = store.find_by_type(
        "rq_revision"
    )

    assert len(result) == 1

    assert (
        result[0].episode_type
        == "rq_revision"
    )


def test_find_by_research_question(
    tmp_path,
):

    store = SQLiteMemoryStore(
        db_path=(
            tmp_path / "memory.db"
        )
    )

    store.save_episode(
        Episode.create(
            episode_type="decision",
            summary="RQ1 Decision",
            details="Details",
            research_question="RQ1",
        )
    )

    store.save_episode(
        Episode.create(
            episode_type="decision",
            summary="RQ2 Decision",
            details="Details",
            research_question="RQ2",
        )
    )

    result = (
        store.find_by_research_question(
            "RQ1"
        )
    )

    assert len(result) == 1

    assert (
        result[0].summary
        == "RQ1 Decision"
    )


def test_memory_persists_across_store_instances(
    tmp_path,
):

    db_path = (
        tmp_path / "memory.db"
    )

    store1 = SQLiteMemoryStore(
        db_path=db_path
    )

    episode = Episode.create(
        episode_type="research_decision",
        summary="Persistent Decision",
        details="This must survive.",
        importance=5,
    )

    store1.save_episode(
        episode
    )

    # 새로운 Store 객체 생성
    store2 = SQLiteMemoryStore(
        db_path=db_path
    )

    loaded = store2.get_episode(
        episode.id
    )

    assert loaded is not None

    assert (
        loaded.summary
        == "Persistent Decision"
    )