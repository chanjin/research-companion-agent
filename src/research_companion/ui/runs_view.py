# src/research_companion/ui/runs_view.py

import streamlit as st


def render_run_summary(
    run,
):

    st.markdown(
        f"### {run.started_at}"
    )

    col1, col2 = st.columns(
        2
    )

    col1.write(
        f"**Status:** {run.status}",
    )

    col2.write(
        f"**Run ID:** {run.run_id}",
    )

    st.write(
        "**Research Topic:**",
        run.research_topic
        or "Not specified",
    )

    st.write(
        "**Research Question:**"
    )

    st.write(
        run.research_question
    )

    if run.error:

        st.error(
            run.error
        )


def render_event(
    event,
):

    title = (
        f"{event.timestamp} | "
        f"{event.event_type}"
    )

    with st.expander(
        title
    ):

        if event.job:

            st.write(
                f"**Job:** {event.job}",
            )

        if event.step:

            st.write(
                f"**Step:** {event.step}",
                
            )

        if event.status:

            st.write(
                f"**Status:** {event.status}",
            )

        if event.message:

            st.write(
                f"**Message:** {event.message}",
            )

        if event.data:

            st.write(
                "**Metrics / Data:**"
            )

            st.json(
                event.data
            )


def render_runs_view(
    observability,
):

    st.subheader(
        "Agent Run History"
    )

    limit = st.slider(
        "Number of runs",
        min_value=1,
        max_value=100,
        value=20,
        key="run_history_limit",
    )

    runs = (
        observability.list_runs(
            limit=limit
        )
    )

    if not runs:

        st.info(
            "No agent runs have "
            "been recorded yet."
        )

        return

    options = {
        (
            f"{run.started_at} | "
            f"{run.status} | "
            f"{run.research_question[:60]}"
        ): run.run_id
        for run in runs
    }

    selected_label = st.selectbox(
        "Select Run",
        options=list(
            options.keys()
        ),
    )

    selected_run_id = options[
        selected_label
    ]

    run = (
        observability.get_run(
            selected_run_id
        )
    )

    if run is None:

        st.error(
            "Run not found."
        )

        return

    render_run_summary(
        run
    )

    st.divider()

    st.markdown(
        "## Execution Timeline"
    )

    events = (
        observability.get_events(
            run.run_id
        )
    )

    if not events:

        st.info(
            "No events recorded."
        )

        return

    for event in events:

        render_event(
            event
        )