# tests/unit/test_literature_utils.py

from research_companion.jobs.literature_scout import (
    deduplicate_papers,
    normalize_title,
    rank_papers,
    validate_results,
)
from research_companion.state import ResearchState


def test_normalize_title():
    title = "  Agent   Role   Boundaries  "

    result = normalize_title(title)

    assert result == "agent role boundaries"


def test_normalize_title_lowercase():
    title = "AUTONOMOUS AI AGENTS"

    result = normalize_title(title)

    assert result == "autonomous ai agents"


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

    result = deduplicate_papers(papers)

    assert len(result) == 2


def test_deduplicate_papers_ignores_case():
    papers = [
        {
            "title": "Agent Role Boundaries",
        },
        {
            "title": "agent role boundaries",
        },
    ]

    result = deduplicate_papers(papers)

    assert len(result) == 1


def test_deduplicate_papers_ignores_extra_spaces():
    papers = [
        {
            "title": "Agent Role Boundaries",
        },
        {
            "title": "Agent   Role   Boundaries",
        },
    ]

    result = deduplicate_papers(papers)

    assert len(result) == 1


def test_rank_papers():
    papers = [
        {
            "title": "Paper A",
            "relevance_score": 2,
        },
        {
            "title": "Paper B",
            "relevance_score": 5,
        },
        {
            "title": "Paper C",
            "relevance_score": 3,
        },
    ]

    result = rank_papers(papers)

    assert result[0]["title"] == "Paper B"
    assert result[1]["title"] == "Paper C"
    assert result[2]["title"] == "Paper A"


def test_rank_papers_missing_score():
    papers = [
        {
            "title": "Paper A",
        },
        {
            "title": "Paper B",
            "relevance_score": 4,
        },
    ]

    result = rank_papers(papers)

    assert result[0]["title"] == "Paper B"
    assert result[1]["title"] == "Paper A"


def make_valid_selected_paper(index):
    return {
        "title": f"Paper {index}",
        "authors": ["Alice Kim"],
        "abstract": "Abstract",
        "published": "2026-01-01",
        "url": f"https://example.com/{index}",
        "pdf_url": f"https://example.com/{index}.pdf",
        "relevance_score": 5,
        "relevance_reason": "Highly relevant.",
    }


def test_validate_results_success():
    state = ResearchState()

    state.selected_papers = [
        make_valid_selected_paper(index)
        for index in range(5)
    ]

    result = validate_results(
        state,
        minimum_papers=5,
    )

    assert result is True


def test_validate_results_not_enough_papers():
    state = ResearchState()

    state.selected_papers = [
        make_valid_selected_paper(index)
        for index in range(3)
    ]

    result = validate_results(
        state,
        minimum_papers=5,
    )

    assert result is False


def test_validate_results_missing_required_field():
    state = ResearchState()

    papers = [
        make_valid_selected_paper(index)
        for index in range(5)
    ]

    del papers[0]["pdf_url"]

    state.selected_papers = papers

    result = validate_results(
        state,
        minimum_papers=5,
    )

    assert result is False


def test_validate_results_invalid_score():
    state = ResearchState()

    papers = [
        make_valid_selected_paper(index)
        for index in range(5)
    ]

    papers[0]["relevance_score"] = 7

    state.selected_papers = papers

    result = validate_results(
        state,
        minimum_papers=5,
    )

    assert result is False