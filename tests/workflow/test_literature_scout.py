# tests/workflow/test_literature_scout.py

from unittest.mock import patch

from research_companion.jobs.literature_scout import (
    LiteratureScout,
)


class FakeAgent:
    def generate_search_queries(
        self,
        research_question,
    ):
        return [
            "autonomous AI agent governance",
            "LLM agent authority constraints",
        ]

    def evaluate_paper_relevance(
        self,
        research_question,
        paper,
    ):
        score = (
            5
            if "governance" in paper["title"].lower()
            else 3
        )

        return {
            **paper,
            "relevance_score": score,
            "relevance_reason": (
                "Test relevance evaluation."
            ),
        }


def make_paper(
    index,
    title,
):
    return {
        "title": title,
        "authors": [
            "Test Author"
        ],
        "abstract": (
            "This paper discusses "
            "autonomous agent safety."
        ),
        "published": "2026-01-01",
        "url": (
            f"https://example.com/{index}"
        ),
        "pdf_url": (
            f"https://example.com/{index}.pdf"
        ),
    }


@patch(
    "research_companion.jobs."
    "literature_scout.search_arxiv"
)
def test_literature_scout_success(
    mock_search,
):
    mock_search.side_effect = [
        [
            make_paper(
                1,
                "Agent Governance",
            ),
            make_paper(
                2,
                "Agent Safety",
            ),
            make_paper(
                3,
                "Role Constraints",
            ),
        ],
        [
            make_paper(
                1,
                "Agent Governance",
            ),
            make_paper(
                4,
                "Authority Control",
            ),
            make_paper(
                5,
                "Policy Enforcement",
            ),
        ],
    ]

    agent = FakeAgent()

    scout = LiteratureScout(
        agent
    )

    state = scout.run(
        research_question=(
            "Can explicit job boundaries "
            "reduce unintended agent behavior?"
        ),
        max_results=5,
        top_n=5,
    )

    assert (
        state.current_step
        == "complete"
    )

    assert (
        state.specification_satisfied
        is True
    )

    assert (
        len(state.search_queries)
        == 2
    )

    assert (
        len(state.candidate_papers)
        == 6
    )

    # Agent Governance가 중복되므로 5개
    assert (
        len(
            state.deduplicated_papers
        )
        == 5
    )

    assert (
        len(
            state.evaluated_papers
        )
        == 5
    )

    assert (
        len(
            state.selected_papers
        )
        == 5
    )

    assert (
        state.selected_papers[0]
        ["title"]
        == "Agent Governance"
    )


@patch(
    "research_companion.jobs."
    "literature_scout.search_arxiv"
)
def test_literature_scout_not_enough_results(
    mock_search,
):
    mock_search.return_value = [
        make_paper(
            1,
            "Agent Governance",
        ),
    ]

    agent = FakeAgent()

    scout = LiteratureScout(
        agent
    )

    state = scout.run(
        research_question="Test RQ",
        max_results=5,
        top_n=5,
    )

    assert (
        state.specification_satisfied
        is False
    )

    assert (
        state.current_step
        == "needs_retry"
    )


@patch(
    "research_companion.jobs."
    "literature_scout.search_arxiv"
)
def test_literature_scout_empty_search(
    mock_search,
):
    mock_search.return_value = []

    agent = FakeAgent()

    scout = LiteratureScout(
        agent
    )

    state = scout.run(
        research_question="Test RQ",
        top_n=5,
    )

    assert (
        len(
            state.candidate_papers
        )
        == 0
    )

    assert (
        len(
            state.selected_papers
        )
        == 0
    )

    assert (
        state.specification_satisfied
        is False
    )

    assert (
        state.current_step
        == "needs_retry"
    )