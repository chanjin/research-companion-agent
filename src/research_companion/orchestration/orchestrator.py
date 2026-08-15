# src/research_companion/orchestration/orchestrator.py

import time

from research_companion.observability.service import (
    ObservabilityService,
)
from research_companion.orchestration.state import (
    AgentRunState,
)


class ResearchOrchestrator:

    def __init__(
        self,
        agent,
        observability: (
            ObservabilityService | None
        ) = None,
    ):

        self.agent = agent

        self.observability = (
            observability
            if observability is not None
            else ObservabilityService()
        )

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

        # ===================================
        # Persistent Run 생성
        # ===================================

        run_record = (
            self.observability
            .start_run(
                research_topic=(
                    research_topic
                ),
                research_question=(
                    research_question
                ),
                user_request=(
                    user_request
                ),
            )
        )

        state = AgentRunState(
            run_id=run_record.run_id,
            user_request=user_request,
            research_topic=research_topic,
            research_question=research_question,
        )

        try:

            state.set_status(
                "running"
            )

            state.current_step = (
                "initialize"
            )

            self.agent.set_research_context(
                topic=research_topic,
                research_question=(
                    research_question
                ),
            )

            # ===================================
            # STEP 1. Memory Recall
            # ===================================

            state.current_job = "memory"
            state.current_step = (
                "recall_memory"
            )

            start_time = (
                time.perf_counter()
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

            duration = (
                time.perf_counter()
                - start_time
            )

            self.observability.log_event(
                run_id=state.run_id,
                event_type=(
                    "memory_recalled"
                ),
                job="memory",
                step="recall_memory",
                status="success",
                data={
                    "memory_count": len(
                        state.recalled_memory
                    ),
                    "duration_seconds": (
                        duration
                    ),
                },
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

            self.observability.log_event(
                run_id=state.run_id,
                event_type="job_started",
                job="literature_scout",
                step="search_literature",
                status="running",
            )

            start_time = (
                time.perf_counter()
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

            duration = (
                time.perf_counter()
                - start_time
            )

            if state.search_state is None:

                state.error = (
                    "Literature Scout "
                    "returned no state."
                )

                state.current_step = (
                    "literature_search_failed"
                )

                state.set_status(
                    "failed"
                )

                self.observability.log_event(
                    run_id=state.run_id,
                    event_type="job_failed",
                    job="literature_scout",
                    step=state.current_step,
                    status="failed",
                    message=state.error,
                    data={
                        "duration_seconds": (
                            duration
                        )
                    },
                )

                self.observability.fail_run(
                    state.run_id,
                    state.error,
                )

                return state

            search_metrics = {
                "query_count": len(
                    state.search_state
                    .search_queries
                ),
                "candidate_count": len(
                    state.search_state
                    .candidate_papers
                ),
                "deduplicated_count": len(
                    state.search_state
                    .deduplicated_papers
                ),
                "evaluated_count": len(
                    state.search_state
                    .evaluated_papers
                ),
                "selected_count": len(
                    state.search_state
                    .selected_papers
                ),
                "duration_seconds": (
                    duration
                ),
            }

            self.observability.log_event(
                run_id=state.run_id,
                event_type="job_completed",
                job="literature_scout",
                step="search_literature",
                status=(
                    "success"
                    if (
                        state.search_state
                        .specification_satisfied
                    )
                    else "needs_retry"
                ),
                data=search_metrics,
            )

            if not (
                state.search_state
                .specification_satisfied
            ):

                state.current_step = (
                    "literature_search_failed"
                )

                state.set_status(
                    "needs_retry"
                )

                self.observability.update_run_status(
                    run_id=state.run_id,
                    status="needs_retry",
                )

                return state

            selected_papers = (
                state.search_state
                .selected_papers
            )

            if not selected_papers:

                state.current_step = (
                    "no_selected_papers"
                )

                state.set_status(
                    "insufficient_evidence"
                )

                self.observability.log_event(
                    run_id=state.run_id,
                    event_type=(
                        "insufficient_evidence"
                    ),
                    job="literature_scout",
                    step=state.current_step,
                    status=(
                        "insufficient_evidence"
                    ),
                    message=(
                        "No papers were selected."
                    ),
                )

                self.observability.update_run_status(
                    run_id=state.run_id,
                    status=(
                        "insufficient_evidence"
                    ),
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

            self.observability.log_event(
                run_id=state.run_id,
                event_type="job_started",
                job="paper_reader",
                step="read_papers",
                status="running",
                data={
                    "requested_papers": len(
                        papers
                    )
                },
            )

            paper_reader_start = (
                time.perf_counter()
            )

            for index, paper in enumerate(
                papers,
                start=1,
            ):

                paper_start = (
                    time.perf_counter()
                )

                self.observability.log_event(
                    run_id=state.run_id,
                    event_type=(
                        "paper_read_started"
                    ),
                    job="paper_reader",
                    step="read_paper",
                    status="running",
                    data={
                        "paper_index": index,
                        "title": paper.get(
                            "title",
                            "",
                        ),
                    },
                )

                reading_state = (
                    self.agent.read_paper(
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

                paper_duration = (
                    time.perf_counter()
                    - paper_start
                )

                if (
                    reading_state
                    .specification_satisfied
                ):

                    self.observability.log_event(
                        run_id=state.run_id,
                        event_type=(
                            "paper_read_completed"
                        ),
                        job="paper_reader",
                        step="read_paper",
                        status="success",
                        data={
                            "paper_index": (
                                index
                            ),
                            "title": paper.get(
                                "title",
                                "",
                            ),
                            "duration_seconds": (
                                paper_duration
                            ),
                        },
                    )

                else:

                    self.observability.log_event(
                        run_id=state.run_id,
                        event_type=(
                            "paper_read_failed"
                        ),
                        job="paper_reader",
                        step="read_paper",
                        status="failed",
                        message=getattr(
                            reading_state,
                            "error",
                            None,
                        ),
                        data={
                            "paper_index": (
                                index
                            ),
                            "title": paper.get(
                                "title",
                                "",
                            ),
                            "workflow_step": getattr(
                                reading_state,
                                "current_step",
                                "",
                            ),
                            "duration_seconds": (
                                paper_duration
                            ),
                        },
                    )

            paper_reader_duration = (
                time.perf_counter()
                - paper_reader_start
            )

            valid_readings = [
                reading_state
                for reading_state
                in state.reading_states
                if (
                    reading_state
                    .specification_satisfied
                )
            ]

            failed_readings = (
                len(state.reading_states)
                - len(valid_readings)
            )

            self.observability.log_event(
                run_id=state.run_id,
                event_type="job_completed",
                job="paper_reader",
                step="read_papers",
                status="success",
                data={
                    "requested_papers": len(
                        papers
                    ),
                    "successful_papers": len(
                        valid_readings
                    ),
                    "failed_papers": (
                        failed_readings
                    ),
                    "duration_seconds": (
                        paper_reader_duration
                    ),
                },
            )

            if len(valid_readings) < 2:

                state.current_step = (
                    "insufficient_paper_analyses"
                )

                state.set_status(
                    "insufficient_evidence"
                )

                self.observability.log_event(
                    run_id=state.run_id,
                    event_type=(
                        "insufficient_evidence"
                    ),
                    job="paper_reader",
                    step=state.current_step,
                    status=(
                        "insufficient_evidence"
                    ),
                    data={
                        "required": 2,
                        "available": len(
                            valid_readings
                        ),
                    },
                )

                self.observability.update_run_status(
                    run_id=state.run_id,
                    status=(
                        "insufficient_evidence"
                    ),
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

            self.observability.log_event(
                run_id=state.run_id,
                event_type="job_started",
                job="research_analyst",
                step="synthesize_research",
                status="running",
                data={
                    "evidence_count": len(
                        paper_analyses
                    )
                },
            )

            start_time = (
                time.perf_counter()
            )

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

            duration = (
                time.perf_counter()
                - start_time
            )

            if (
                state.analysis_state
                is None
            ):

                state.error = (
                    "Research Analyst "
                    "returned no state."
                )

                state.set_status(
                    "failed"
                )

                self.observability.fail_run(
                    state.run_id,
                    state.error,
                )

                return state

            analyst_status = (
                "success"
                if (
                    state.analysis_state
                    .specification_satisfied
                )
                else "needs_retry"
            )

            self.observability.log_event(
                run_id=state.run_id,
                event_type="job_completed",
                job="research_analyst",
                step="synthesize_research",
                status=analyst_status,
                data={
                    "evidence_count": len(
                        paper_analyses
                    ),
                    "gap_count": len(
                        state.analysis_state
                        .synthesis.get(
                            "research_gaps",
                            [],
                        )
                    ),
                    "duration_seconds": (
                        duration
                    ),
                },
            )

            if not (
                state.analysis_state
                .specification_satisfied
            ):

                state.current_step = (
                    "research_analysis_failed"
                )

                state.set_status(
                    "needs_retry"
                )

                self.observability.update_run_status(
                    run_id=state.run_id,
                    status="needs_retry",
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

            self.observability.log_event(
                run_id=state.run_id,
                event_type="job_started",
                job="research_partner",
                step=(
                    "propose_research_direction"
                ),
                status="running",
            )

            start_time = (
                time.perf_counter()
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

            duration = (
                time.perf_counter()
                - start_time
            )

            if state.partner_state is None:

                state.error = (
                    "Research Partner "
                    "returned no state."
                )

                state.set_status(
                    "failed"
                )

                self.observability.fail_run(
                    state.run_id,
                    state.error,
                )

                return state

            partner_status = (
                "success"
                if (
                    state.partner_state
                    .specification_satisfied
                )
                else "needs_retry"
            )

            candidate_count = len(
                state.partner_state
                .proposal.get(
                    "refined_research_questions",
                    [],
                )
            )

            self.observability.log_event(
                run_id=state.run_id,
                event_type="job_completed",
                job="research_partner",
                step=(
                    "propose_research_direction"
                ),
                status=partner_status,
                data={
                    "candidate_rq_count": (
                        candidate_count
                    ),
                    "duration_seconds": (
                        duration
                    ),
                },
            )

            if not (
                state.partner_state
                .specification_satisfied
            ):

                state.current_step = (
                    "research_proposal_failed"
                )

                state.set_status(
                    "needs_retry"
                )

                self.observability.update_run_status(
                    run_id=state.run_id,
                    status="needs_retry",
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

            self.observability.log_event(
                run_id=state.run_id,
                event_type=(
                    "waiting_for_human"
                ),
                job="human_review",
                step=(
                    "waiting_for_human_decision"
                ),
                status="waiting_for_human",
                data={
                    "candidate_rq_count": (
                        candidate_count
                    )
                },
            )

            self.observability.update_run_status(
                run_id=state.run_id,
                status="waiting_for_human",
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

            self.observability.fail_run(
                state.run_id,
                state.error,
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

        try:

            if (
                state.status
                != "waiting_for_human"
            ):

                raise ValueError(
                    "Run is not waiting "
                    "for human decision."
                )

            if state.partner_state is None:

                raise ValueError(
                    "Research Partner state "
                    "is missing."
                )

            candidates = (
                state.partner_state
                .proposal.get(
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

            selected = candidates[
                candidate_index
            ]

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

            self.observability.log_event(
                run_id=state.run_id,
                event_type="human_decision",
                job="human_review",
                step="apply_decision",
                status=decision,
                message=reason,
                data={
                    "decision": decision,
                    "candidate_index": (
                        candidate_index
                    ),
                    "original_rq": (
                        original_content
                    ),
                    "revised_rq": (
                        revised_content
                    ),
                    "decision_id": (
                        research_decision.id
                    ),
                },
            )

            state.pending_human_decision = (
                False
            )

            # -----------------------------------
            # APPROVE / REVISE
            # -----------------------------------

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

                self.observability.log_event(
                    run_id=state.run_id,
                    event_type=(
                        "run_completed"
                    ),
                    job="orchestrator",
                    step=(
                        "human_decision_applied"
                    ),
                    status="completed",
                )

                self.observability.complete_run(
                    run_id=state.run_id,
                    research_question=(
                        state.research_question
                    ),
                )

            # -----------------------------------
            # REJECT
            # -----------------------------------

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

                self.observability.update_run_status(
                    run_id=state.run_id,
                    status="needs_retry",
                )

            # -----------------------------------
            # DEFER
            # -----------------------------------

            elif decision == "defer":

                state.current_job = (
                    "human_review"
                )

                state.current_step = (
                    "decision_deferred"
                )

                state.pending_human_decision = (
                    True
                )

                state.set_status(
                    "waiting_for_human"
                )

                self.observability.update_run_status(
                    run_id=state.run_id,
                    status="waiting_for_human",
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

            if state.run_id:

                self.observability.fail_run(
                    state.run_id,
                    state.error,
                )

            return state