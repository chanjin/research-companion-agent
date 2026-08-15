# tests/integration/test_real_paper_reader.py

import pytest

from research_companion.agent import (
    ResearchCompanionAgent,
)
from research_companion.tools.arxiv_search import (
    search_arxiv,
)


@pytest.mark.integration
def test_real_paper_reader():
    papers = search_arxiv(
        query="AI agents safety",
        max_results=1,
    )

    assert len(papers) == 1

    paper = papers[0]

    assert paper["pdf_url"]

    agent = (
        ResearchCompanionAgent()
    )

    research_question = (
        "에이전트를 명확한 직무 범위와 "
        "책임을 가진 독립 주체로 설계하면 "
        "예기치 않은 행동을 더 효과적으로 "
        "통제할 수 있는가?"
    )

    state = agent.read_paper(
        paper=paper,
        research_question=(
            research_question
        ),

        # integration test가 너무 무거워지는 것을
        # 방지하기 위해 초기에는 5페이지만 읽는다.
        max_pages=5,
    )

    assert (
        state.current_step
        in [
            "complete",
            "needs_retry",
        ]
    )

    assert (
        state.error
        is None
    )

    assert state.pdf_path
    assert state.paper_text

    assert isinstance(
        state.analysis,
        dict,
    )

    assert (
        "research_problem"
        in state.analysis
    )