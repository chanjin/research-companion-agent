# src/research_companion/ui/memory_view.py

import streamlit as st


def render_memory_view(
    agent,
):

    st.subheader(
        "Persistent Episodic Memory"
    )

    limit = st.slider(
        "Number of memories",
        min_value=1,
        max_value=50,
        value=10,
    )

    episodes = (
        agent.memory.recall(
            limit=limit
        )
    )

    if not episodes:

        st.info(
            "No episodic memory has "
            "been stored yet."
        )

        return

    for index, episode in enumerate(
        episodes,
        start=1,
    ):

        with st.expander(
            (
                f"{index}. "
                f"{episode.episode_type} — "
                f"{episode.summary}"
            )
        ):

            st.write(
                f"**Timestamp:** episode.timestamp,",
                
            )

            st.write(
                f"**Source:** {episode.source
                                or "unknown"},",
                
            )

            st.write(
                f"**Importance:**  {episode.importance,}",
               
            )

            st.write(
                "**Research Question:**"
            )

            st.write(
                episode.research_question
                or "Not specified"
            )

            st.write(
                "**Details:**"
            )

            st.text(
                episode.details
            )