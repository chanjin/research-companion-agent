# tests/workflow/test_orchestrator.py

from types import SimpleNamespace

from research_companion.orchestration.orchestrator import (
    ResearchOrchestrator,
)

def make_search_state(
    satisfied=True,
    paper_count=3,
):

    papers = []

    for index in range(paper_count):

        papers.append(
            {
                "title": f"Paper {index + 1}",
                "authors": ["Test Author"],
                "abstract": "Test abstract",
                "published": "2026-01-01",
                "url": (
                    f"https://example.com/"
                    f"{index + 1}"
                ),
                "pdf_url": (
                    f"https://example.com/"
                    f"{index + 1}.pdf"
                ),
                "relevance_score": 5,
                "relevance_reason": "Relevant",
            }
        )

    return SimpleNamespace(
        specification_satisfied=satisfied,

        search_queries=[
            "query 1",
            "query 2",
        ],

        candidate_papers=papers.copy(),

        deduplicated_papers=papers.copy(),

        evaluated_papers=papers.copy(),

        selected_papers=papers,

        current_step=(
            "complete"
            if satisfied
            else "needs_retry"
        ),
    )

def make_reading_state(
    satisfied=True,
    index=1,
):

    return SimpleNamespace(
        paper={
            "title": f"Paper {index}",
            "pdf_url": (
                f"https://example.com/"
                f"{index}.pdf"
            ),
        },

        analysis={
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
                f"Relevance {index}"
            ),
        },

        current_step=(
            "complete"
            if satisfied
            else "failed"
        ),

        specification_satisfied=satisfied,

        error=(
            None
            if satisfied
            else "Mock paper reading failure"
        ),
    )

def make_analysis_state(
    satisfied=True,
):

    return SimpleNamespace(
        specification_satisfied=(
            satisfied
        ),

        current_step=(
            "complete"
            if satisfied
            else "needs_retry"
        ),

        error=None,

        synthesis={
            "major_themes": [
                "Agent governance",
            ],

            "common_problems": [
                "Unauthorized behavior",
            ],

            "common_methods": [
                "Policy constraints",
            ],

            "methodological_differences": [
                "Static versus dynamic control",
            ],

            "common_findings": [
                "Constraints reduce failures",
            ],

            "recurring_limitations": [
                "Limited evaluation environments",
            ],

            "research_trends": [
                "Runtime governance",
            ],

            "research_gaps": [
                {
                    "gap": (
                        "Job-bounded agents "
                        "remain underexplored."
                    ),
                    "evidence": (
                        "Existing systems focus "
                        "on prompt-level controls."
                    ),
                    "confidence": (
                        "medium"
                    ),
                }
            ],

            "implications_for_current_rq": [
                "Direct comparison may be useful."
            ],
        },
    )

def make_partner_state(
    satisfied=True,
):

    return SimpleNamespace(
        specification_satisfied=(
            satisfied
        ),

        current_step=(
            "complete"
            if satisfied
            else "needs_retry"
        ),

        error=None,

        proposal={
            "rq_assessment": {
                "assessment": (
                    "reasonably_scoped"
                ),
                "reason": (
                    "The question supports "
                    "a measurable comparison."
                ),
            },

            "selected_gaps": [
                {
                    "gap": (
                        "Job-bounded agents "
                        "remain underexplored."
                    ),
                    "why_relevant": (
                        "Directly related "
                        "to the current RQ."
                    ),
                    "confidence": (
                        "medium"
                    ),
                }
            ],

            "refined_research_questions": [
                {
                    "rq": (
                        "Do explicit authority "
                        "boundaries reduce "
                        "unauthorized agent actions?"
                    ),
                    "rationale": (
                        "Creates a measurable "
                        "comparison."
                    ),
                }
            ],

            "candidate_hypotheses": [
                {
                    "hypothesis": (
                        "Explicit authority "
                        "boundaries reduce "
                        "unauthorized actions."
                    ),
                    "related_rq": (
                        "Do authority boundaries "
                        "reduce unauthorized actions?"
                    ),
                    "testability": (
                        "Compare violation rates."
                    ),
                }
            ],

            "proposed_research_designs": [
                {
                    "design": (
                        "Controlled comparison"
                    ),
                    "independent_variables": [
                        "Agent architecture"
                    ],
                    "dependent_variables": [
                        "Unauthorized action rate"
                    ],
                    "comparison": (
                        "Workflow vs job-bounded"
                    ),
                    "required_data": [
                        "Execution logs"
                    ],
                }
            ],

            "evaluation_metrics": [
                "Unauthorized action rate"
            ],

            "risks_and_assumptions": [
                "Synthetic scenarios"
            ],

            "recommended_next_actions": [
                "Define authority boundaries"
            ],
        },
    )

class FakeDecision:

    def __init__(
        self,
        decision,
        final_content,
    ):

        self.id = "decision-001"

        self.decision = decision

        self.final_content = (
            final_content
        )


class FakeAgent:

    def __init__(
        self,
    ):

        self.research_topic = None
        self.research_question = None

        self.search_state = (
            make_search_state()
        )

        self.reading_states = [
            make_reading_state(
                True,
                1,
            ),
            make_reading_state(
                True,
                2,
            ),
            make_reading_state(
                True,
                3,
            ),
        ]

        self.analysis_state = (
            make_analysis_state()
        )

        self.partner_state = (
            make_partner_state()
        )

    def set_research_context(
        self,
        topic,
        research_question,
    ):

        self.research_topic = topic

        self.research_question = (
            research_question
        )

    def recall_research_memory(
        self,
        research_question=None,
        limit=5,
    ):

        return [
            SimpleNamespace(
                summary="Past decision"
            )
        ]

    def search_literature(
        self,
        research_question,
        max_results=5,
        top_n=5,
    ):

        return self.search_state

    def read_paper(
        self,
        paper,
        research_question,
        max_pages=None,
    ):

        if self.reading_states:

            return (
                self.reading_states
                .pop(0)
            )

        return make_reading_state(
            False
        )

    def analyze_research_landscape(
        self,
        research_question,
        paper_analyses,
    ):

        return self.analysis_state

    def propose_research_direction(
        self,
        research_question,
        research_synthesis,
    ):

        return self.partner_state

    def make_research_decision(
        self,
        decision_type,
        target_type,
        decision,
        original_content,
        revised_content=None,
        reason="",
    ):

        if decision == "approve":

            self.research_question = (
                original_content
            )

            return FakeDecision(
                decision="approve",
                final_content=(
                    original_content
                ),
            )

        if decision == "revise":

            self.research_question = (
                revised_content
            )

            return FakeDecision(
                decision="revise",
                final_content=(
                    revised_content
                ),
            )

        return FakeDecision(
            decision=decision,
            final_content=None,
        )


def test_orchestrator_success_to_human_gate():

    agent = FakeAgent()

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request=(
            "Research this topic."
        ),
        research_topic=(
            "Agent Governance"
        ),
        research_question=(
            "Test RQ"
        ),
        papers_to_read=3,
    )

    assert (
        state.status
        == "waiting_for_human"
    )

    assert (
        state.pending_human_decision
        is True
    )

    assert (
        state.current_job
        == "human_review"
    )

    assert (
        state.search_state
        is not None
    )

    assert (
        len(
            state.reading_states
        )
        == 3
    )

    assert (
        state.analysis_state
        is not None
    )

    assert (
        state.partner_state
        is not None
    )


def test_orchestrator_search_failure():

    agent = FakeAgent()

    agent.search_state = (
        make_search_state(
            satisfied=False
        )
    )

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request="Test",
        research_question="Test RQ",
    )

    assert (
        state.status
        == "needs_retry"
    )

    assert (
        state.current_step
        == "literature_search_failed"
    )


def test_orchestrator_insufficient_papers():

    agent = FakeAgent()

    agent.search_state = (
        make_search_state(
            satisfied=True,
            paper_count=1,
        )
    )

    agent.reading_states = [
        make_reading_state(
            True,
            1,
        )
    ]

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request="Test",
        research_question="Test RQ",
        top_n=1,
        papers_to_read=1,
    )

    assert (
        state.status
        == "insufficient_evidence"
    )

    assert (
        state.current_step
        == "insufficient_paper_analyses"
    )


def test_orchestrator_paper_reader_partial_failure():

    agent = FakeAgent()

    agent.reading_states = [
        make_reading_state(
            True,
            1,
        ),
        make_reading_state(
            False,
            2,
        ),
        make_reading_state(
            True,
            3,
        ),
    ]

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request="Test",
        research_question="Test RQ",
        papers_to_read=3,
    )

    # 3편 중 2편 성공했으므로
    # Research Analyst까지 진행 가능
    assert (
        state.status
        == "waiting_for_human"
    )


def test_orchestrator_research_analysis_failure():

    agent = FakeAgent()

    agent.analysis_state = (
        make_analysis_state(
            satisfied=False
        )
    )

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request="Test",
        research_question="Test RQ",
    )

    assert (
        state.status
        == "needs_retry"
    )

    assert (
        state.current_step
        == "research_analysis_failed"
    )


def test_orchestrator_research_partner_failure():

    agent = FakeAgent()

    agent.partner_state = (
        make_partner_state(
            satisfied=False
        )
    )

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request="Test",
        research_question="Test RQ",
    )

    assert (
        state.status
        == "needs_retry"
    )

    assert (
        state.current_step
        == "research_proposal_failed"
    )


def test_human_approve_completes_run():

    agent = FakeAgent()

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request="Test",
        research_question="Original RQ",
    )

    assert (
        state.status
        == "waiting_for_human"
    )

    state = (
        orchestrator
        .apply_human_decision(
            state=state,
            candidate_index=0,
            decision="approve",
            reason=(
                "Clear and measurable."
            ),
        )
    )

    assert (
        state.status
        == "completed"
    )

    assert (
        state.pending_human_decision
        is False
    )

    assert (
        state.human_decision_id
        == "decision-001"
    )

    assert (
        state.research_question
        == (
            "Do explicit authority "
            "boundaries reduce "
            "unauthorized agent actions?"
        )
    )


def test_human_revision_completes_run():

    agent = FakeAgent()

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request="Test",
        research_question="Original RQ",
    )

    revised_rq = (
        "Do explicit Scope, Responsibility, "
        "and Authority boundaries reduce "
        "unauthorized actions?"
    )

    state = (
        orchestrator
        .apply_human_decision(
            state=state,
            candidate_index=0,
            decision="revise",
            revised_content=(
                revised_rq
            ),
            reason=(
                "Include all authority dimensions."
            ),
        )
    )

    assert (
        state.status
        == "completed"
    )

    assert (
        state.research_question
        == revised_rq
    )


def test_human_reject_requires_retry():

    agent = FakeAgent()

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request="Test",
        research_question="Original RQ",
    )

    state = (
        orchestrator
        .apply_human_decision(
            state=state,
            candidate_index=0,
            decision="reject",
            reason="Not suitable.",
        )
    )

    assert (
        state.status
        == "needs_retry"
    )

    assert (
        state.current_step
        == "proposal_rejected"
    )


def test_human_defer_keeps_waiting():

    agent = FakeAgent()

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    state = orchestrator.run(
        user_request="Test",
        research_question="Original RQ",
    )

    state = (
        orchestrator
        .apply_human_decision(
            state=state,
            candidate_index=0,
            decision="defer",
            reason=(
                "Need more evidence."
            ),
        )
    )

    assert (
        state.status
        == "waiting_for_human"
    )

    assert (
        state.pending_human_decision
        is True
    )


def test_human_decision_before_gate_fails():

    agent = FakeAgent()

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    from research_companion.orchestration.state import (
        AgentRunState,
    )

    state = AgentRunState(
        research_question="Test RQ"
    )

    state = (
        orchestrator
        .apply_human_decision(
            state=state,
            candidate_index=0,
            decision="approve",
        )
    )

    assert (
        state.status
        == "failed"
    )

    assert (
        "not waiting"
        in state.error
    )