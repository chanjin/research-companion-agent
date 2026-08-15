# src/research_companion/ui/research_view.py

import streamlit as st


DEFAULT_TOPIC = (
    "Job-bounded AI Agent Governance"
)


DEFAULT_RQ = (
    "에이전트를 고정된 절차적 워크플로우의 "
    "실행 노드가 아닌 명확한 직무 경계(Scope), "
    "책임(Responsibility), 권한(Authority)을 가진 "
    "독립 주체로 정의할 때, 월권 행동이나 "
    "프롬프트 이탈과 같은 예기치 않은 시스템 "
    "오작동을 얼마나 효과적으로 통제할 수 있는가?"
)


DEFAULT_REQUEST = (
    "현재 연구 질문과 관련된 문헌을 조사하고, "
    "핵심 연구 Gap을 분석한 뒤 "
    "다음 연구 방향을 제안해줘."
)


def render_research_view(
    orchestrator,
):

    st.subheader(
        "Research Setup"
    )

    research_topic = st.text_input(
        "Research Topic",
        value=st.session_state.get(
            "research_topic",
            DEFAULT_TOPIC,
        ),
    )

    research_question = st.text_area(
        "Research Question",
        value=st.session_state.get(
            "research_question",
            DEFAULT_RQ,
        ),
        height=160,
    )

    user_request = st.text_area(
        "Research Request",
        value=st.session_state.get(
            "user_request",
            DEFAULT_REQUEST,
        ),
        height=100,
    )

    st.divider()

    st.subheader(
        "Execution Settings"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:
        max_results = st.number_input(
            "Results per query",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
        )

    with col2:
        top_n = st.number_input(
            "Top papers",
            min_value=2,
            max_value=10,
            value=5,
            step=1,
        )

    with col3:
        papers_to_read = (
            st.number_input(
                "Papers to read",
                min_value=2,
                max_value=5,
                value=3,
                step=1,
            )
        )

    max_pages = st.number_input(
        "Maximum pages per paper",
        min_value=1,
        max_value=30,
        value=8,
        step=1,
    )

    st.divider()

    start = st.button(
        "Start Research",
        type="primary",
        use_container_width=True,
    )

    if not start:
        return

    if not research_question.strip():

        st.error(
            "Research Question is required."
        )

        return

    st.session_state[
        "research_topic"
    ] = research_topic

    st.session_state[
        "research_question"
    ] = research_question

    st.session_state[
        "user_request"
    ] = user_request

    with st.spinner(
        "Running research workflow..."
    ):

        state = orchestrator.run(
            user_request=user_request,
            research_topic=research_topic,
            research_question=(
                research_question
            ),
            max_results_per_query=int(
                max_results
            ),
            top_n=int(
                top_n
            ),
            papers_to_read=int(
                papers_to_read
            ),
            max_pages_per_paper=int(
                max_pages
            ),
        )

    st.session_state[
        "run_state"
    ] = state

    if state.status == (
        "waiting_for_human"
    ):

        st.success(
            "Research workflow completed. "
            "Human review is required."
        )

    elif state.status == (
        "completed"
    ):

        st.success(
            "Research workflow completed."
        )

    elif state.status in {
        "needs_retry",
        "insufficient_evidence",
    }:

        st.warning(
            "The workflow stopped before "
            "completion."
        )

    else:

        st.error(
            state.error
            or (
                "Research workflow failed."
            )
        )