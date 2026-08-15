# src/research_companion/app.py

import streamlit as st

from research_companion.agent import (
    ResearchCompanionAgent,
)
from research_companion.observability.service import (
    ObservabilityService,
)
from research_companion.orchestration.orchestrator import (
    ResearchOrchestrator,
)
from research_companion.ui.memory_view import (
    render_memory_view,
)
from research_companion.ui.research_view import (
    render_research_view,
)
from research_companion.ui.results_view import (
    render_results_view,
)
from research_companion.ui.runs_view import (
    render_runs_view,
)


def initialize_session_state():

    if "agent" not in st.session_state:

        st.session_state.agent = (
            ResearchCompanionAgent()
        )

    if (
        "observability"
        not in st.session_state
    ):

        st.session_state.observability = (
            ObservabilityService()
        )

    if (
        "orchestrator"
        not in st.session_state
    ):

        st.session_state.orchestrator = (
            ResearchOrchestrator(
                agent=(
                    st.session_state
                    .agent
                ),
                observability=(
                    st.session_state
                    .observability
                ),
            )
        )

    if (
        "run_state"
        not in st.session_state
    ):

        st.session_state.run_state = (
            None
        )


def render_sidebar():

    st.sidebar.title(
        "Research Companion"
    )

    st.sidebar.markdown(
        """
Local Research Agent

- Literature Scout
- Paper Reader
- Research Analyst
- Research Partner
- Persistent Memory
- Human Approval
- Run Observability
"""
    )

    st.sidebar.divider()

    agent = (
        st.session_state.agent
    )

    episodes = (
        agent.memory.recall(
            limit=1000
        )
    )

    st.sidebar.metric(
        "Stored Memories",
        len(episodes),
    )

    runs = (
        st.session_state
        .observability
        .list_runs(
            limit=1000
        )
    )

    st.sidebar.metric(
        "Recorded Runs",
        len(runs),
    )

    run_state = (
        st.session_state.run_state
    )

    if run_state is not None:

        st.sidebar.metric(
            "Current Status",
            run_state.status,
        )

        st.sidebar.caption(
            f"Run ID: "
            f"{run_state.run_id}"
        )


def main():

    st.set_page_config(
        page_title=(
            "Research Companion"
        ),
        page_icon="🔬",
        layout="wide",
    )

    initialize_session_state()

    render_sidebar()

    st.title(
        "Research Companion"
    )

    st.caption(
        "Local, persistent, "
        "human-governed and observable "
        "research agent"
    )

    (
        research_tab,
        results_tab,
        memory_tab,
        runs_tab,
    ) = st.tabs(
        [
            "Research",
            "Results",
            "Memory",
            "Runs",
        ]
    )

    with research_tab:

        render_research_view(
            orchestrator=(
                st.session_state
                .orchestrator
            )
        )

    with results_tab:

        render_results_view(
            state=(
                st.session_state
                .run_state
            ),
            orchestrator=(
                st.session_state
                .orchestrator
            ),
        )

    with memory_tab:

        render_memory_view(
            agent=(
                st.session_state
                .agent
            )
        )

    with runs_tab:

        render_runs_view(
            observability=(
                st.session_state
                .observability
            )
        )


if __name__ == "__main__":
    main()