# src/research_companion/orchestration/orchestrator.py

from research_companion.orchestration.state import (
    AgentRunState,
)


class ResearchOrchestrator:
    """
    Research Companion의 여러 Job을
    하나의 상위 Workflow로 연결하고 제어한다.
    """

    def __init__(
        self,
        agent,
    ):
        self.agent = agent

    def run(
        self,
        user_request: str,
        research_question: str,
        research_topic: str = "",
        max_results_per_query: int = 5,
        top_n: int = 5,
        papers_to_read: int = 3,
        max_pages_per_paper: int | None = 8,
    ) -> AgentRunState:

        state = AgentRunState(
            user_request=user_request,
            research_topic=research_topic,
            research_question=research_question,
        )

        try:

            # ===================================
            # START
            # ===================================

            state.set_status(
                "running"
            )

            state.current_step = (
                "initialize"
            )

            self.agent.set_research_context(
                topic=research_topic,
                research_question=research_question,
            )

            # ===================================
            # STEP 1. Recall Episodic Memory
            # ===================================

            state.current_job = (
                "memory"
            )

            state.current_step = (
                "recall_memory"
            )

            state.recalled_memory = (
                self.agent
                .recall_research_memory(
                    research_question=(
                        research_question
                    ),
                    limit=5,
                )
            )

            # ===================================
            # STEP 2. Literature Scout
            # ===================================

            state.current_job = (
                "literature_scout"
            )

            state.current_step = (
                "search_literature"
            )

            state.search_state = (
                self.agent
                .search_literature(
                    research_question=(
                        research_question
                    ),
                    max_results=(
                        max_results_per_query
                    ),
                    top_n=top_n,
                )
            )

            # 검색 Workflow가 실패
            if (
                state.search_state
                is None
            ):

                state.set_status(
                    "failed"
                )

                state.error = (
                    "Literature Scout "
                    "returned no state."
                )

                return state

            # 검색 결과가 Specification을
            # 만족하지 못한 경우
            if not (
                state.search_state
                .specification_satisfied
            ):

                state.set_status(
                    "needs_retry"
                )

                state.current_step = (
                    "literature_search_failed"
                )

                return state

            selected_papers = (
                state.search_state
                .selected_papers
            )

            if not selected_papers:

                state.set_status(
                    "insufficient_evidence"
                )

                state.current_step = (
                    "no_selected_papers"
                )

                return state

            # ===================================
            # STEP 3. Paper Reader
            # ===================================

            state.current_job = (
                "paper_reader"
            )

            state.current_step = (
                "read_papers"
            )

            papers = selected_papers[
                :papers_to_read
            ]

            for paper in papers:

                reading_state = (
                    self.agent
                    .read_paper(
                        paper=paper,
                        research_question=(
                            research_question
                        ),
                        max_pages=(
                            max_pages_per_paper
                        ),
                    )
                )

                state.reading_states.append(
                    reading_state
                )

            # -----------------------------------
            # 성공한 Paper 분석만 사용
            # -----------------------------------

            valid_readings = [
                reading_state
                for reading_state
                in state.reading_states
                if (
                    reading_state
                    .specification_satisfied
                )
            ]

            # Research Analyst는 최소 2편 필요
            if len(valid_readings) < 2:

                state.set_status(
                    "insufficient_evidence"
                )

                state.current_step = (
                    "insufficient_paper_analyses"
                )

                return state

            # ===================================
            # STEP 4. Research Analyst
            # ===================================

            state.current_job = (
                "research_analyst"
            )

            state.current_step = (
                "synthesize_research"
            )

            paper_analyses = [
                reading_state.analysis
                for reading_state
                in valid_readings
            ]

            state.analysis_state = (
                self.agent
                .analyze_research_landscape(
                    research_question=(
                        research_question
                    ),
                    paper_analyses=(
                        paper_analyses
                    ),
                )
            )

            if (
                state.analysis_state
                is None
            ):

                state.set_status(
                    "failed"
                )

                state.error = (
                    "Research Analyst "
                    "returned no state."
                )

                return state

            if not (
                state.analysis_state
                .specification_satisfied
            ):

                state.set_status(
                    "needs_retry"
                )

                state.current_step = (
                    "research_analysis_failed"
                )

                return state

            # ===================================
            # STEP 5. Research Partner
            # ===================================

            state.current_job = (
                "research_partner"
            )

            state.current_step = (
                "propose_research_direction"
            )

            state.partner_state = (
                self.agent
                .propose_research_direction(
                    research_question=(
                        research_question
                    ),
                    research_synthesis=(
                        state.analysis_state
                        .synthesis
                    ),
                )
            )

            if (
                state.partner_state
                is None
            ):

                state.set_status(
                    "failed"
                )

                state.error = (
                    "Research Partner "
                    "returned no state."
                )

                return state

            if not (
                state.partner_state
                .specification_satisfied
            ):

                state.set_status(
                    "needs_retry"
                )

                state.current_step = (
                    "research_proposal_failed"
                )

                return state

            # ===================================
            # STEP 6. Human Approval Gate
            # ===================================

            state.current_job = (
                "human_review"
            )

            state.current_step = (
                "waiting_for_human_decision"
            )

            state.pending_human_decision = (
                True
            )

            state.set_status(
                "waiting_for_human"
            )

            return state

        except Exception as error:

            state.error = str(
                error
            )

            state.current_job = (
                "orchestrator"
            )

            state.current_step = (
                "exception"
            )

            state.set_status(
                "failed"
            )

            return state

    # =======================================
    # Human Decision
    # =======================================

    def apply_human_decision(
        self,
        state: AgentRunState,
        candidate_index: int,
        decision: str,
        revised_content: str | None = None,
        reason: str = "",
    ) -> AgentRunState:
        """
        Research Partner가 제안한 RQ 후보에 대해
        Human Decision을 적용한다.
        """

        try:

            if (
                state.status
                != "waiting_for_human"
            ):

                raise ValueError(
                    "Run is not waiting "
                    "for human decision."
                )

            if (
                state.partner_state
                is None
            ):

                raise ValueError(
                    "Research Partner state "
                    "is missing."
                )

            proposal = (
                state.partner_state
                .proposal
            )

            candidates = (
                proposal.get(
                    "refined_research_questions",
                    [],
                )
            )

            if not candidates:

                raise ValueError(
                    "No candidate research "
                    "questions are available."
                )

            if (
                candidate_index < 0
                or candidate_index
                >= len(candidates)
            ):

                raise ValueError(
                    "Invalid candidate index."
                )

            selected = (
                candidates[
                    candidate_index
                ]
            )

            original_content = (
                selected.get(
                    "rq",
                    "",
                )
            )

            if not original_content:

                raise ValueError(
                    "Selected candidate "
                    "does not contain an RQ."
                )

            # ===================================
            # Human Decision 처리
            # ===================================

            research_decision = (
                self.agent
                .make_research_decision(
                    decision_type=(
                        "rq_selection"
                    ),
                    target_type=(
                        "research_question"
                    ),
                    decision=decision,
                    original_content=(
                        original_content
                    ),
                    revised_content=(
                        revised_content
                    ),
                    reason=reason,
                )
            )

            state.human_decision_id = (
                research_decision.id
            )

            state.pending_human_decision = (
                False
            )

            # ===================================
            # Decision 결과
            # ===================================

            if decision in {
                "approve",
                "revise",
            }:

                state.research_question = (
                    self.agent
                    .research_question
                )

                state.current_job = (
                    "completed"
                )

                state.current_step = (
                    "human_decision_applied"
                )

                state.set_status(
                    "completed"
                )

            elif decision == "reject":

                state.current_job = (
                    "human_review"
                )

                state.current_step = (
                    "proposal_rejected"
                )

                state.set_status(
                    "needs_retry"
                )

            elif decision == "defer":

                state.current_job = (
                    "human_review"
                )

                state.current_step = (
                    "decision_deferred"
                )

                # 아직 완료되지 않았으므로
                # 다시 human review 상태로 둔다.
                state.pending_human_decision = (
                    True
                )

                state.set_status(
                    "waiting_for_human"
                )

            return state

        except Exception as error:

            state.error = str(
                error
            )

            state.current_step = (
                "human_decision_failed"
            )

            state.set_status(
                "failed"
            )

            return state