# tests/unit/test_paper_validation.py

from research_companion.jobs.paper_reader import (
    validate_paper_analysis,
)


def test_validate_paper_analysis_success(
    valid_analysis,
):
    result = validate_paper_analysis(
        valid_analysis
    )

    assert result is True


def test_validate_paper_analysis_missing_field(
    valid_analysis,
):
    analysis = valid_analysis.copy()

    del analysis[
        "limitations"
    ]

    result = validate_paper_analysis(
        analysis
    )

    assert result is False


def test_validate_paper_analysis_empty_field(
    valid_analysis,
):
    analysis = valid_analysis.copy()

    analysis[
        "research_problem"
    ] = ""

    result = validate_paper_analysis(
        analysis
    )

    assert result is False


def test_validate_paper_analysis_whitespace_only(
    valid_analysis,
):
    analysis = valid_analysis.copy()

    analysis[
        "method"
    ] = "   "

    result = validate_paper_analysis(
        analysis
    )

    assert result is False


def test_validate_paper_analysis_wrong_type(
    valid_analysis,
):
    analysis = valid_analysis.copy()

    analysis[
        "results"
    ] = [
        "Result 1",
        "Result 2",
    ]

    result = validate_paper_analysis(
        analysis
    )

    assert result is False


def test_validate_paper_analysis_not_dict():
    result = validate_paper_analysis(
        "invalid analysis"
    )

    assert result is False