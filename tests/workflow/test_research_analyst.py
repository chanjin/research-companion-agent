# tests/workflow/test_research_analyst.py

from research_companion.jobs.research_analyst import (
    ResearchAnalyst,
)


def make_valid_synthesis():

    return {
        "major_themes": [
            "Agent governance",
        ],
        "common_problems": [
            "Unintended behavior",
        ],
        "common_methods": [
            "Policy constraints",
        ],
        "methodological_differences": [
            "Static vs runtime controls",
        ],
        "common_findings": [
            "Constraints reduce failures",
        ],
        "recurring_limitations": [
            "Limited test environments",
        ],
        "research_trends": [
            "Runtime governance",
        ],
        "research_gaps": [
            {
                "gap": (
                    "Job-based authority boundaries "
                    "remain underexplored."
                ),
                "evidence": (
                    "Existing approaches focus primarily "
                    "on prompt or tool-level controls."
                ),
                "confidence": "medium",
            }
        ],
        "implications_for_current_rq": [
            (
                "A direct comparison between "
                "workflow-node and job-bounded agents "
                "could address this gap."
            )
        ],
    }


class FakeAgent:

    def synthesize_research(
        self,
        research_question,
        paper_analyses,
    ):

        return make_valid_synthesis()


def make_analysis(
    index,
):

    return {
        "research_problem": (
            f"Problem {index}"
        ),
        "research_gap": (
            f"Gap {index}"
        ),
        "research_objective": (
            f"Objective {index}"
        ),
        "method": (
            f"Method {index}"
        ),
        "dataset": (
            f"Dataset {index}"
        ),
        "experiment": (
            f"Experiment {index}"
        ),
        "results": (
            f"Results {index}"
        ),
        "contribution": (
            f"Contribution {index}"
        ),
        "limitations": (
            f"Limitations {index}"
        ),
        "relevance_to_current_rq": (
            f"Relevant {index}"
        ),
    }


def test_research_analyst_success():

    agent = FakeAgent()

    analyst = ResearchAnalyst(
        agent
    )

    analyses = [
        make_analysis(1),
        make_analysis(2),
        make_analysis(3),
    ]

    state = analyst.run(
        research_question="Test RQ",
        paper_analyses=analyses,
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
        len(
            state.normalized_evidence
        )
        == 3
    )

    assert (
        len(
            state.synthesis[
                "research_gaps"
            ]
        )
        == 1
    )


def test_research_analyst_requires_multiple_papers():

    agent = FakeAgent()

    analyst = ResearchAnalyst(
        agent
    )

    state = analyst.run(
        research_question="Test RQ",
        paper_analyses=[
            make_analysis(1)
        ],
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
        "at least two paper analyses"
        in state.error
    )


class InvalidFakeAgent:

    def synthesize_research(
        self,
        research_question,
        paper_analyses,
    ):

        return {
            "major_themes": [
                "Test"
            ]
        }


def test_research_analyst_invalid_synthesis():

    agent = InvalidFakeAgent()

    analyst = ResearchAnalyst(
        agent
    )

    analyses = [
        make_analysis(1),
        make_analysis(2),
    ]

    state = analyst.run(
        research_question="Test RQ",
        paper_analyses=analyses,
    )

    assert (
        state.current_step
        == "needs_retry"
    )

    assert (
        state.specification_satisfied
        is False
    )