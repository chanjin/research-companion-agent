# src/research_companion/ui/helpers.py


def get_run_status_summary(state) -> dict:
    if state is None:
        return {
            "status": "not_started",
            "current_job": "",
            "current_step": "",
            "research_question": "",
            "error": None,
        }

    return {
        "status": getattr(
            state,
            "status",
            "",
        ),
        "current_job": getattr(
            state,
            "current_job",
            "",
        ),
        "current_step": getattr(
            state,
            "current_step",
            "",
        ),
        "research_question": getattr(
            state,
            "research_question",
            "",
        ),
        "error": getattr(
            state,
            "error",
            None,
        ),
    }


def get_selected_papers(state) -> list[dict]:
    if state is None:
        return []

    search_state = getattr(
        state,
        "search_state",
        None,
    )

    if search_state is None:
        return []

    return getattr(
        search_state,
        "selected_papers",
        [],
    )


def get_candidate_research_questions(
    state,
) -> list[dict]:

    if state is None:
        return []

    partner_state = getattr(
        state,
        "partner_state",
        None,
    )

    if partner_state is None:
        return []

    proposal = getattr(
        partner_state,
        "proposal",
        {},
    )

    if not isinstance(
        proposal,
        dict,
    ):
        return []

    return proposal.get(
        "refined_research_questions",
        [],
    )


def can_apply_human_decision(
    state,
) -> bool:

    if state is None:
        return False

    return (
        getattr(
            state,
            "status",
            None,
        )
        == "waiting_for_human"
        and getattr(
            state,
            "pending_human_decision",
            False,
        )
    )