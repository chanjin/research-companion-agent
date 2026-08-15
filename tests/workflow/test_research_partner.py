# tests/workflow/test_research_partner.py

from research_companion.jobs.research_partner import (
    ResearchPartner,
)


def make_valid_synthesis():

    return {
        "major_themes": [
            "Agent governance",
            "Authority constraints",
        ],

        "common_problems": [
            "Unintended agent behavior",
        ],

        "common_methods": [
            "Policy enforcement",
        ],

        "methodological_differences": [
            "Static versus runtime controls",
        ],

        "common_findings": [
            (
                "Constraints can reduce "
                "some unsafe behavior."
            )
        ],

        "recurring_limitations": [
            "Limited test environments",
        ],

        "research_trends": [
            (
                "Increasing attention "
                "to runtime governance."
            )
        ],

        "research_gaps": [
            {
                "gap": (
                    "Explicit job-bounded "
                    "agent architectures remain "
                    "underexplored."
                ),
                "evidence": (
                    "Most reviewed approaches "
                    "focus on prompt or tool-level "
                    "constraints."
                ),
                "confidence": "medium",
            }
        ],

        "implications_for_current_rq": [
            (
                "A comparison between "
                "workflow-node and job-bounded "
                "agents is potentially useful."
            )
        ],
    }


def make_valid_proposal():

    return {
        "rq_assessment": {
            "assessment": (
                "reasonably_scoped"
            ),
            "reason": (
                "The question supports "
                "a direct comparison."
            ),
        },

        "selected_gaps": [
            {
                "gap": (
                    "Job-bounded agent "
                    "architectures are underexplored."
                ),
                "why_relevant": (
                    "The current RQ directly "
                    "addresses this architecture."
                ),
                "confidence": "medium",
            }
        ],

        "refined_research_questions": [
            {
                "rq": (
                    "Do explicit authority "
                    "boundaries reduce unauthorized "
                    "actions in autonomous agents?"
                ),
                "rationale": (
                    "This creates a measurable "
                    "comparison."
                ),
            }
        ],

        "candidate_hypotheses": [
            {
                "hypothesis": (
                    "Agents with explicit authority "
                    "boundaries will produce fewer "
                    "unauthorized actions."
                ),
                "related_rq": (
                    "Do authority boundaries reduce "
                    "unauthorized actions?"
                ),
                "testability": (
                    "Measure unauthorized action "
                    "rates under identical tasks."
                ),
            }
        ],

        "proposed_research_designs": [
            {
                "design": (
                    "Controlled comparative "
                    "agent experiment."
                ),
                "independent_variables": [
                    "Agent architecture",
                ],
                "dependent_variables": [
                    "Unauthorized action rate",
                ],
                "comparison": (
                    "Workflow-node versus "
                    "job-bounded agent."
                ),
                "required_data": [
                    "Execution logs",
                ],
            }
        ],

        "evaluation_metrics": [
            "Unauthorized action rate",
        ],

        "risks_and_assumptions": [
            (
                "Synthetic scenarios may "
                "limit external validity."
            )
        ],

        "recommended_next_actions": [
            (
                "Operationalize Scope, "
                "Responsibility, and Authority."
            )
        ],
    }


class FakeAgent:

    def generate_research_proposal(
        self,
        research_question,
        research_synthesis,
    ):

        return make_valid_proposal()


def test_research_partner_success():

    agent = FakeAgent()

    partner = ResearchPartner(
        agent
    )

    state = partner.run(
        research_question="Test RQ",
        research_synthesis=(
            make_valid_synthesis()
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
        len(
            state.proposal[
                "refined_research_questions"
            ]
        )
        >= 1
    )


def test_research_partner_requires_synthesis():

    agent = FakeAgent()

    partner = ResearchPartner(
        agent
    )

    state = partner.run(
        research_question="Test RQ",
        research_synthesis={},
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
        "requires research synthesis"
        in state.error
    )


def test_research_partner_requires_gap():

    agent = FakeAgent()

    partner = ResearchPartner(
        agent
    )

    synthesis = (
        make_valid_synthesis()
    )

    synthesis[
        "research_gaps"
    ] = []

    state = partner.run(
        research_question="Test RQ",
        research_synthesis=synthesis,
    )

    assert (
        state.current_step
        == "failed"
    )

    assert (
        "does not contain research gaps"
        in state.error
    )


class InvalidFakeAgent:

    def generate_research_proposal(
        self,
        research_question,
        research_synthesis,
    ):

        return {
            "rq_assessment": {
                "assessment": (
                    "reasonably_scoped"
                ),
                "reason": "Test",
            }
        }


def test_research_partner_invalid_proposal():

    agent = InvalidFakeAgent()

    partner = ResearchPartner(
        agent
    )

    state = partner.run(
        research_question="Test RQ",
        research_synthesis=(
            make_valid_synthesis()
        ),
    )

    assert (
        state.current_step
        == "needs_retry"
    )

    assert (
        state.specification_satisfied
        is False
    )