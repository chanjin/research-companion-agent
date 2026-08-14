# tests/test_literature_scout.py

from research_companion.jobs.literature_scout import (
    deduplicate_papers,
    rank_papers,
)


def test_deduplicate_papers():

    papers = [
        {
            "title": "Agent Memory",
        },
        {
            "title": "Agent Memory",
        },
        {
            "title": "Research Agents",
        },
    ]

    result = deduplicate_papers(
        papers
    )

    assert len(result) == 2


def test_deduplicate_papers_ignores_case():

    papers = [
        {
            "title": "Agent Memory",
        },
        {
            "title": "agent memory",
        },
    ]

    result = deduplicate_papers(
        papers
    )

    assert len(result) == 1


def test_rank_papers():

    papers = [
        {
            "title": "Paper A",
            "relevance_score": 3,
        },
        {
            "title": "Paper B",
            "relevance_score": 5,
        },
        {
            "title": "Paper C",
            "relevance_score": 1,
        },
    ]

    result = rank_papers(
        papers
    )

    assert result[0]["title"] == "Paper B"
    assert result[1]["title"] == "Paper A"
    assert result[2]["title"] == "Paper C"