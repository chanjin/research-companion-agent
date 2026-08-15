# tests/unit/test_research_proposal_validation.py

from research_companion.jobs.research_partner import (
    validate_research_proposal,
)


def make_valid_proposal():

    return {
        "rq_assessment": {
            "assessment": (
                "reasonably_scoped"
            ),
            "reason": (
                "The question defines "
                "a clear architectural comparison."
            ),
        },

        "selected_gaps": [
            {
                "gap": (
                    "Explicit job-bounded "
                    "agent architectures are "
                    "underexplored."
                ),
                "why_relevant": (
                    "The current RQ directly "
                    "tests this architectural idea."
                ),
                "confidence": "medium",
            }
        ],

        "refined_research_questions": [
            {
                "rq": (
                    "Do explicit Scope, "
                    "Responsibility, and Authority "
                    "boundaries reduce unauthorized "
                    "agent actions compared with "
                    "workflow-node agents?"
                ),
                "rationale": (
                    "This version introduces "
                    "a direct comparison and "
                    "measurable failure behavior."
                ),
            }
        ],

        "candidate_hypotheses": [
            {
                "hypothesis": (
                    "Job-bounded agents will "
                    "produce fewer unauthorized "
                    "actions than workflow-node agents."
                ),
                "related_rq": (
                    "Do explicit SRA boundaries "
                    "reduce unauthorized actions?"
                ),
                "testability": (
                    "Compare unauthorized-action "
                    "rates under controlled tasks."
                ),
            }
        ],

        "proposed_research_designs": [
            {
                "design": (
                    "Controlled comparative "
                    "agent architecture experiment."
                ),
                "independent_variables": [
                    "Agent architecture type",
                ],
                "dependent_variables": [
                    "Unauthorized action rate",
                    "Scope violation rate",
                ],
                "comparison": (
                    "Workflow-node agent versus "
                    "job-bounded agent."
                ),
                "required_data": [
                    "Agent execution logs",
                    "Failure scenario results",
                ],
            }
        ],

        "evaluation_metrics": [
            "Unauthorized action rate",
            "Scope violation rate",
            "Prompt deviation rate",
        ],

        "risks_and_assumptions": [
            (
                "Failure scenarios may not "
                "represent real deployments."
            )
        ],

        "recommended_next_actions": [
            (
                "Define operational measures "
                "for Scope, Responsibility, "
                "and Authority."
            )
        ],
    }


def test_validate_research_proposal_success():

    proposal = make_valid_proposal()

    result = (
        validate_research_proposal(
            proposal
        )
    )

    assert result is True


def test_validate_research_proposal_missing_field():

    proposal = make_valid_proposal()

    del proposal[
        "evaluation_metrics"
    ]

    result = (
        validate_research_proposal(
            proposal
        )
    )

    assert result is False


def test_validate_research_proposal_invalid_assessment():

    proposal = make_valid_proposal()

    proposal[
        "rq_assessment"
    ][
        "assessment"
    ] = "excellent"

    result = (
        validate_research_proposal(
            proposal
        )
    )

    assert result is False


def test_validate_research_proposal_no_refined_rq():

    proposal = make_valid_proposal()

    proposal[
        "refined_research_questions"
    ] = []

    result = (
        validate_research_proposal(
            proposal
        )
    )

    assert result is False


def test_validate_research_proposal_invalid_gap_confidence():

    proposal = make_valid_proposal()

    proposal[
        "selected_gaps"
    ][0][
        "confidence"
    ] = "very-high"

    result = (
        validate_research_proposal(
            proposal
        )
    )

    assert result is False


def test_validate_research_proposal_no_design():

    proposal = make_valid_proposal()

    proposal[
        "proposed_research_designs"
    ] = []

    result = (
        validate_research_proposal(
            proposal
        )
    )

    assert result is False


def test_validate_research_proposal_no_next_action():

    proposal = make_valid_proposal()

    proposal[
        "recommended_next_actions"
    ] = []

    result = (
        validate_research_proposal(
            proposal
        )
    )

    assert result is False


def test_validate_research_proposal_wrong_design_type():

    proposal = make_valid_proposal()

    proposal[
        "proposed_research_designs"
    ][0][
        "independent_variables"
    ] = "Agent architecture"

    result = (
        validate_research_proposal(
            proposal
        )
    )

    assert result is False