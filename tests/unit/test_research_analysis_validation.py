# tests/unit/test_research_analysis_validation.py

from research_companion.jobs.research_analyst import (
    normalize_analyses,
    validate_research_synthesis,
)


def make_valid_synthesis():
    return {
        "major_themes": [
            "Agent governance",
        ],
        "common_problems": [
            "Unintended agent behavior",
        ],
        "common_methods": [
            "Policy constraints",
        ],
        "methodological_differences": [
            "Different enforcement mechanisms",
        ],
        "common_findings": [
            "Constraints reduce some failures",
        ],
        "recurring_limitations": [
            "Limited evaluation environments",
        ],
        "research_trends": [
            "Increasing focus on runtime governance",
        ],
        "research_gaps": [
            {
                "gap": (
                    "Explicit job-bounded agent "
                    "architectures remain underexplored."
                ),
                "evidence": (
                    "Most studies focus on prompts "
                    "or tool permissions."
                ),
                "confidence": "medium",
            }
        ],
        "implications_for_current_rq": [
            (
                "A comparative evaluation of workflow-node "
                "and job-bounded agents may be useful."
            )
        ],
    }


def test_normalize_analyses():

    analyses = [
        {
            "research_problem": "Problem A",
            "method": "Method A",
            "results": "Result A",
            "limitations": "Limitation A",
        }
    ]

    result = normalize_analyses(
        analyses
    )

    assert len(result) == 1

    assert (
        result[0]["paper_id"]
        == 1
    )

    assert (
        result[0]["research_problem"]
        == "Problem A"
    )

    assert (
        result[0]["method"]
        == "Method A"
    )


def test_validate_research_synthesis_success():

    synthesis = make_valid_synthesis()

    result = validate_research_synthesis(
        synthesis=synthesis,
        minimum_papers=3,
    )

    assert result is True


def test_validate_research_synthesis_requires_two_papers():

    synthesis = make_valid_synthesis()

    result = validate_research_synthesis(
        synthesis=synthesis,
        minimum_papers=1,
    )

    assert result is False


def test_validate_research_synthesis_missing_field():

    synthesis = make_valid_synthesis()

    del synthesis[
        "research_trends"
    ]

    result = validate_research_synthesis(
        synthesis=synthesis,
        minimum_papers=3,
    )

    assert result is False


def test_validate_research_synthesis_invalid_gap():

    synthesis = make_valid_synthesis()

    synthesis["research_gaps"] = [
        {
            "gap": "Test gap",
        }
    ]

    result = validate_research_synthesis(
        synthesis=synthesis,
        minimum_papers=3,
    )

    assert result is False


def test_validate_research_synthesis_invalid_confidence():

    synthesis = make_valid_synthesis()

    synthesis["research_gaps"][0][
        "confidence"
    ] = "very-high"

    result = validate_research_synthesis(
        synthesis=synthesis,
        minimum_papers=3,
    )

    assert result is False