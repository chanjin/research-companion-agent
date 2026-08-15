# tests/workflow/test_paper_reader.py

from unittest.mock import patch

from research_companion.jobs.paper_reader import (
    PaperReader,
)


class FakeAgent:
    def __init__(
        self,
        analysis,
    ):
        self.analysis = analysis

    def analyze_paper(
        self,
        research_question,
        paper,
        paper_text,
    ):
        return self.analysis


@patch(
    "research_companion.jobs."
    "paper_reader.parse_pdf"
)
@patch(
    "research_companion.jobs."
    "paper_reader.download_pdf"
)
def test_paper_reader_success(
    mock_download_pdf,
    mock_parse_pdf,
    sample_paper,
    valid_analysis,
):
    mock_download_pdf.return_value = (
        "data/papers/test.pdf"
    )

    mock_parse_pdf.return_value = (
        "This paper studies explicit "
        "role boundaries and authority "
        "constraints in AI agents."
    )

    agent = FakeAgent(
        valid_analysis
    )

    reader = PaperReader(
        agent
    )

    state = reader.run(
        paper=sample_paper,
        research_question=(
            "Can explicit job boundaries "
            "reduce unintended agent behavior?"
        ),
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
        state.error
        is None
    )

    assert (
        state.pdf_path
        == "data/papers/test.pdf"
    )

    assert (
        "role boundaries"
        in state.paper_text
    )

    assert (
        state.analysis[
            "research_problem"
        ]
        == valid_analysis[
            "research_problem"
        ]
    )


@patch(
    "research_companion.jobs."
    "paper_reader.download_pdf"
)
def test_paper_reader_download_failure(
    mock_download_pdf,
    sample_paper,
    valid_analysis,
):
    mock_download_pdf.side_effect = (
        RuntimeError(
            "PDF download failed"
        )
    )

    agent = FakeAgent(
        valid_analysis
    )

    reader = PaperReader(
        agent
    )

    state = reader.run(
        paper=sample_paper,
        research_question="Test RQ",
    )

    assert (
        state.current_step
        == "failed"
    )

    assert (
        state.specification_satisfied
        is False
    )

    assert (
        "PDF download failed"
        in state.error
    )


@patch(
    "research_companion.jobs."
    "paper_reader.parse_pdf"
)
@patch(
    "research_companion.jobs."
    "paper_reader.download_pdf"
)
def test_paper_reader_parse_failure(
    mock_download_pdf,
    mock_parse_pdf,
    sample_paper,
    valid_analysis,
):
    mock_download_pdf.return_value = (
        "data/papers/test.pdf"
    )

    mock_parse_pdf.side_effect = (
        ValueError(
            "No text could be extracted "
            "from the PDF."
        )
    )

    agent = FakeAgent(
        valid_analysis
    )

    reader = PaperReader(
        agent
    )

    state = reader.run(
        paper=sample_paper,
        research_question="Test RQ",
    )

    assert (
        state.current_step
        == "failed"
    )

    assert (
        state.specification_satisfied
        is False
    )

    assert (
        "No text could be extracted"
        in state.error
    )


@patch(
    "research_companion.jobs."
    "paper_reader.parse_pdf"
)
@patch(
    "research_companion.jobs."
    "paper_reader.download_pdf"
)
def test_paper_reader_invalid_analysis(
    mock_download_pdf,
    mock_parse_pdf,
    sample_paper,
):
    mock_download_pdf.return_value = (
        "data/papers/test.pdf"
    )

    mock_parse_pdf.return_value = (
        "Paper content"
    )

    incomplete_analysis = {
        "research_problem": "Problem",
    }

    agent = FakeAgent(
        incomplete_analysis
    )

    reader = PaperReader(
        agent
    )

    state = reader.run(
        paper=sample_paper,
        research_question="Test RQ",
    )

    assert (
        state.current_step
        == "needs_retry"
    )

    assert (
        state.specification_satisfied
        is False
    )


def test_paper_reader_missing_pdf_url(
    sample_paper,
    valid_analysis,
):
    paper = sample_paper.copy()

    del paper["pdf_url"]

    agent = FakeAgent(
        valid_analysis
    )

    reader = PaperReader(
        agent
    )

    state = reader.run(
        paper=paper,
        research_question="Test RQ",
    )

    assert (
        state.current_step
        == "failed"
    )

    assert (
        state.specification_satisfied
        is False
    )

    assert (
        "does not contain a PDF URL"
        in state.error
    )