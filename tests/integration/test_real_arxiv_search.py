# tests/integration/test_real_arxiv_search.py

import pytest

from research_companion.tools.arxiv_search import (
    search_arxiv,
)


@pytest.mark.integration
def test_real_arxiv_search():
    papers = search_arxiv(
        query=(
            "autonomous AI agents "
            "governance"
        ),
        max_results=3,
    )

    assert len(papers) > 0

    paper = papers[0]

    assert paper["title"]
    assert paper["authors"]
    assert paper["abstract"]
    assert paper["url"]
    assert paper["pdf_url"]