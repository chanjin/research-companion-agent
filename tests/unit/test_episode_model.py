# tests/unit/test_episode_model.py

import pytest

from research_companion.memory.models import (
    Episode,
)


def test_episode_create():

    episode = Episode.create(
        episode_type="research_decision",
        summary="Selected research direction",
        details="Focus on job-bounded agents.",
        research_question="Test RQ",
        source="researcher",
        importance=5,
    )

    assert episode.id

    assert episode.timestamp

    assert (
        episode.episode_type
        == "research_decision"
    )

    assert (
        episode.summary
        == "Selected research direction"
    )

    assert (
        episode.research_question
        == "Test RQ"
    )

    assert (
        episode.importance
        == 5
    )


def test_episode_invalid_importance():

    with pytest.raises(
        ValueError,
        match="importance must be between 1 and 5",
    ):

        Episode.create(
            episode_type="test",
            summary="Test",
            details="Test",
            importance=10,
        )