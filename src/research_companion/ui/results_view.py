# src/research_companion/ui/results_view.py

import streamlit as st

from research_companion.ui.helpers import (
    can_apply_human_decision,
    get_candidate_research_questions,
    get_run_status_summary,
)


def render_status(
    state,
):

    summary = (
        get_run_status_summary(
            state
        )
    )

    st.subheader(
        "Workflow Status"
    )

    col1, col2, col3 = st.columns(
        3
    )

    col1.metric(
        "Status",
        summary["status"],
    )

    col2.metric(
        "Current Job",
        summary["current_job"]
        or "-",
    )

    col3.metric(
        "Current Step",
        summary["current_step"]
        or "-",
    )

    if summary["error"]:

        st.error(
            summary["error"]
        )


def render_literature_results(
    state,
):

    search_state = getattr(
        state,
        "search_state",
        None,
    )

    if search_state is None:
        return

    with st.expander(
        "Literature Scout",
        expanded=True,
    ):

        st.markdown(
            "### Search Queries"
        )

        for query in getattr(
            search_state,
            "search_queries",
            [],
        ):

            st.write(
                f"- {query}"
            )

        st.markdown(
            "### Search Summary"
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        col1.metric(
            "Candidates",
            len(
                getattr(
                    search_state,
                    "candidate_papers",
                    [],
                )
            ),
        )

        col2.metric(
            "Evaluated",
            len(
                getattr(
                    search_state,
                    "evaluated_papers",
                    [],
                )
            ),
        )

        col3.metric(
            "Selected",
            len(
                getattr(
                    search_state,
                    "selected_papers",
                    [],
                )
            ),
        )

        st.markdown(
            "### Selected Papers"
        )

        selected_papers = getattr(
            search_state,
            "selected_papers",
            [],
        )

        for index, paper in enumerate(
            selected_papers,
            start=1,
        ):

            st.markdown(
                f"**{index}. "
                f"{paper.get('title', '')}**"
            )

            st.write(
                "Score:",
                paper.get(
                    "relevance_score",
                    "",
                ),
            )

            st.write(
                "Reason:",
                paper.get(
                    "relevance_reason",
                    "",
                ),
            )

            st.write(
                "Authors:",
                ", ".join(
                    paper.get(
                        "authors",
                        [],
                    )
                ),
            )

            st.write(
                "Published:",
                paper.get(
                    "published",
                    "",
                ),
            )

            st.write(
                "PDF:",
                paper.get(
                    "pdf_url",
                    "",
                ),
            )

            st.divider()


def render_paper_reader_results(
    state,
):

    reading_states = getattr(
        state,
        "reading_states",
        [],
    )

    if not reading_states:
        return

    with st.expander(
        "Paper Reader",
        expanded=False,
    ):

        for index, reading_state in enumerate(
            reading_states,
            start=1,
        ):

            paper = (
                getattr(
                    reading_state,
                    "paper",
                    None,
                )
                or {}
            )

            title = paper.get(
                "title",
                f"Paper {index}",
            )

            st.markdown(
                f"### {index}. {title}"
            )

            if getattr(
                reading_state,
                "error",
                None,
            ):

                st.error(
                    reading_state.error
                )

                continue

            analysis = getattr(
                reading_state,
                "analysis",
                {},
            )

            fields = [
                (
                    "Research Problem",
                    "research_problem",
                ),
                (
                    "Research Gap",
                    "research_gap",
                ),
                (
                    "Research Objective",
                    "research_objective",
                ),
                (
                    "Method",
                    "method",
                ),
                (
                    "Dataset",
                    "dataset",
                ),
                (
                    "Experiment",
                    "experiment",
                ),
                (
                    "Results",
                    "results",
                ),
                (
                    "Contribution",
                    "contribution",
                ),
                (
                    "Limitations",
                    "limitations",
                ),
                (
                    "Relevance to Current RQ",
                    "relevance_to_current_rq",
                ),
            ]

            for label, key in fields:

                st.markdown(
                    f"**{label}**"
                )

                st.write(
                    analysis.get(
                        key,
                        "Not available",
                    )
                )

            st.divider()


def render_research_analysis(
    state,
):

    analysis_state = getattr(
        state,
        "analysis_state",
        None,
    )

    if analysis_state is None:
        return

    synthesis = getattr(
        analysis_state,
        "synthesis",
        {},
    )

    with st.expander(
        "Research Analyst",
        expanded=True,
    ):

        sections = [
            (
                "Major Themes",
                "major_themes",
            ),
            (
                "Common Problems",
                "common_problems",
            ),
            (
                "Common Methods",
                "common_methods",
            ),
            (
                "Methodological Differences",
                "methodological_differences",
            ),
            (
                "Common Findings",
                "common_findings",
            ),
            (
                "Recurring Limitations",
                "recurring_limitations",
            ),
            (
                "Research Trends",
                "research_trends",
            ),
            (
                "Implications for Current RQ",
                "implications_for_current_rq",
            ),
        ]

        for label, key in sections:

            st.markdown(
                f"### {label}"
            )

            items = synthesis.get(
                key,
                [],
            )

            if not items:

                st.write(
                    "No data."
                )

            for item in items:

                st.write(
                    f"- {item}"
                )

        st.markdown(
            "### Research Gaps"
        )

        for index, gap in enumerate(
            synthesis.get(
                "research_gaps",
                [],
            ),
            start=1,
        ):

            st.markdown(
                f"**Gap {index}**"
            )

            st.write(
                gap.get(
                    "gap",
                    "",
                )
            )

            st.write(
                "**Evidence:**",
                gap.get(
                    "evidence",
                    "",
                ),
            )

            st.write(
                "**Confidence:**",
                gap.get(
                    "confidence",
                    "",
                ),
            )

            st.divider()


def render_research_partner(
    state,
    orchestrator,
):

    partner_state = getattr(
        state,
        "partner_state",
        None,
    )

    if partner_state is None:
        return

    proposal = getattr(
        partner_state,
        "proposal",
        {},
    )

    with st.expander(
        "Research Partner",
        expanded=True,
    ):

        rq_assessment = proposal.get(
            "rq_assessment",
            {},
        )

        st.markdown(
            "### RQ Assessment"
        )

        st.write(
            "Assessment:",
            rq_assessment.get(
                "assessment",
                "",
            ),
        )

        st.write(
            "Reason:",
            rq_assessment.get(
                "reason",
                "",
            ),
        )

        st.markdown(
            "### Recommended Next Actions"
        )

        for item in proposal.get(
            "recommended_next_actions",
            [],
        ):

            st.write(
                f"- {item}"
            )

        if not can_apply_human_decision(
            state
        ):
            return

        st.divider()

        render_human_review(
            state=state,
            orchestrator=orchestrator,
        )


def render_human_review(
    state,
    orchestrator,
):

    st.markdown(
        "## Human Review"
    )

    candidates = (
        get_candidate_research_questions(
            state
        )
    )

    if not candidates:

        st.warning(
            "No candidate research "
            "questions are available."
        )

        return

    selected_index = st.radio(
        "Select a candidate research question",
        options=list(
            range(
                len(candidates)
            )
        ),
        format_func=lambda index: (
            candidates[index]
            .get(
                "rq",
                "",
            )
        ),
        key="candidate_rq",
    )

    selected = candidates[
        selected_index
    ]

    st.caption(
        selected.get(
            "rationale",
            "",
        )
    )

    decision = st.radio(
        "Decision",
        options=[
            "approve",
            "revise",
            "reject",
            "defer",
        ],
        horizontal=True,
        key="human_decision",
    )

    revised_content = None

    if decision == "revise":

        revised_content = (
            st.text_area(
                "Revised Research Question",
                value=selected.get(
                    "rq",
                    "",
                ),
                height=120,
            )
        )

    reason = st.text_area(
        "Reason for Decision",
        height=100,
    )

    apply_decision = st.button(
        "Apply Decision",
        type="primary",
    )

    if not apply_decision:
        return

    if (
        decision == "revise"
        and not (
            revised_content
            or ""
        ).strip()
    ):

        st.error(
            "A revised research question "
            "is required."
        )

        return

    updated_state = (
        orchestrator
        .apply_human_decision(
            state=state,
            candidate_index=(
                selected_index
            ),
            decision=decision,
            revised_content=(
                revised_content
            ),
            reason=reason,
        )
    )

    st.session_state[
        "run_state"
    ] = updated_state

    if updated_state.status == (
        "completed"
    ):

        st.success(
            "Decision applied. "
            "Research run completed."
        )

        st.write(
            "Final Research Question:"
        )

        st.write(
            updated_state
            .research_question
        )

    elif updated_state.status == (
        "waiting_for_human"
    ):

        st.info(
            "Decision deferred."
        )

    elif updated_state.status == (
        "needs_retry"
    ):

        st.warning(
            "Proposal rejected. "
            "A new research proposal is needed."
        )

    else:

        st.error(
            updated_state.error
            or "Decision application failed."
        )


def render_results_view(
    state,
    orchestrator,
):

    if state is None:

        st.info(
            "Start a research run "
            "from the Research tab."
        )

        return

    render_status(
        state
    )

    render_literature_results(
        state
    )

    render_paper_reader_results(
        state
    )

    render_research_analysis(
        state
    )

    render_research_partner(
        state,
        orchestrator,
    )