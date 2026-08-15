# src/research_companion/app.py

import streamlit as st

from research_companion.agent import (
    ResearchCompanionAgent,
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


def initialize_session_state():

    if "agent" not in st.session_state:

        st.session_state.agent = (
            ResearchCompanionAgent()
        )

    if (
        "orchestrator"
        not in st.session_state
    ):

        st.session_state.orchestrator = (
            ResearchOrchestrator(
                st.session_state.agent
            )
        )

    if "run_state" not in st.session_state:

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

    run_state = (
        st.session_state.run_state
    )

    if run_state is not None:

        st.sidebar.metric(
            "Current Status",
            run_state.status,
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
        "A local, persistent, "
        "human-governed research agent"
    )

    research_tab, results_tab, memory_tab = (
        st.tabs(
            [
                "Research",
                "Results",
                "Memory",
            ]
        )
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


if __name__ == "__main__":
    main()