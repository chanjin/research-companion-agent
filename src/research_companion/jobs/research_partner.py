# src/research_companion/jobs/research_partner.py

from research_companion.state import ResearchPartnerState


REQUIRED_PROPOSAL_FIELDS = [
    "rq_assessment",
    "selected_gaps",
    "refined_research_questions",
    "candidate_hypotheses",
    "proposed_research_designs",
    "evaluation_metrics",
    "risks_and_assumptions",
    "recommended_next_actions",
]


VALID_RQ_ASSESSMENTS = [
    "too_broad",
    "too_narrow",
    "reasonably_scoped",
    "needs_reframing",
]


VALID_CONFIDENCE_LEVELS = [
    "low",
    "medium",
    "high",
]


def validate_research_proposal(
    proposal: dict,
) -> bool:
    """
    Research Partner의 결과가
    최소 Specification을 만족하는지 검사한다.
    """

    if not isinstance(
        proposal,
        dict,
    ):
        return False

    # -----------------------------------
    # Required top-level fields
    # -----------------------------------

    for field in REQUIRED_PROPOSAL_FIELDS:

        if field not in proposal:
            return False

    # -----------------------------------
    # RQ Assessment
    # -----------------------------------

    rq_assessment = proposal[
        "rq_assessment"
    ]

    if not isinstance(
        rq_assessment,
        dict,
    ):
        return False

    if "assessment" not in rq_assessment:
        return False

    if "reason" not in rq_assessment:
        return False

    if (
        rq_assessment["assessment"]
        not in VALID_RQ_ASSESSMENTS
    ):
        return False

    if not isinstance(
        rq_assessment["reason"],
        str,
    ):
        return False

    if not rq_assessment[
        "reason"
    ].strip():
        return False

    # -----------------------------------
    # Selected Gaps
    # -----------------------------------

    selected_gaps = proposal[
        "selected_gaps"
    ]

    if not isinstance(
        selected_gaps,
        list,
    ):
        return False

    for gap in selected_gaps:

        if not isinstance(
            gap,
            dict,
        ):
            return False

        required_gap_fields = [
            "gap",
            "why_relevant",
            "confidence",
        ]

        for field in required_gap_fields:

            if field not in gap:
                return False

            if not isinstance(
                gap[field],
                str,
            ):
                return False

            if not gap[
                field
            ].strip():
                return False

        if (
            gap["confidence"]
            not in VALID_CONFIDENCE_LEVELS
        ):
            return False

    # -----------------------------------
    # Refined Research Questions
    # -----------------------------------

    refined_rqs = proposal[
        "refined_research_questions"
    ]

    if not isinstance(
        refined_rqs,
        list,
    ):
        return False

    if not refined_rqs:
        return False

    for item in refined_rqs:

        if not isinstance(
            item,
            dict,
        ):
            return False

        if "rq" not in item:
            return False

        if "rationale" not in item:
            return False

        if not isinstance(
            item["rq"],
            str,
        ):
            return False

        if not isinstance(
            item["rationale"],
            str,
        ):
            return False

        if not item[
            "rq"
        ].strip():
            return False

        if not item[
            "rationale"
        ].strip():
            return False

    # -----------------------------------
    # Candidate Hypotheses
    # -----------------------------------

    hypotheses = proposal[
        "candidate_hypotheses"
    ]

    if not isinstance(
        hypotheses,
        list,
    ):
        return False

    for hypothesis in hypotheses:

        if not isinstance(
            hypothesis,
            dict,
        ):
            return False

        required_hypothesis_fields = [
            "hypothesis",
            "related_rq",
            "testability",
        ]

        for field in required_hypothesis_fields:

            if field not in hypothesis:
                return False

            if not isinstance(
                hypothesis[field],
                str,
            ):
                return False

    # -----------------------------------
    # Research Designs
    # -----------------------------------

    designs = proposal[
        "proposed_research_designs"
    ]

    if not isinstance(
        designs,
        list,
    ):
        return False

    if not designs:
        return False

    for design in designs:

        if not isinstance(
            design,
            dict,
        ):
            return False

        required_design_fields = [
            "design",
            "independent_variables",
            "dependent_variables",
            "comparison",
            "required_data",
        ]

        for field in required_design_fields:

            if field not in design:
                return False

        if not isinstance(
            design["design"],
            str,
        ):
            return False

        if not isinstance(
            design["comparison"],
            str,
        ):
            return False

        if not isinstance(
            design["independent_variables"],
            list,
        ):
            return False

        if not isinstance(
            design["dependent_variables"],
            list,
        ):
            return False

        if not isinstance(
            design["required_data"],
            list,
        ):
            return False

    # -----------------------------------
    # List fields
    # -----------------------------------

    list_fields = [
        "evaluation_metrics",
        "risks_and_assumptions",
        "recommended_next_actions",
    ]

    for field in list_fields:

        value = proposal[field]

        if not isinstance(
            value,
            list,
        ):
            return False

        if not value:
            return False

        for item in value:

            if not isinstance(
                item,
                str,
            ):
                return False

            if not item.strip():
                return False

    return True


class ResearchPartner:

    def __init__(
        self,
        agent,
    ):
        self.agent = agent

    def run(
        self,
        research_question: str,
        research_synthesis: dict,
    ) -> ResearchPartnerState:

        state = ResearchPartnerState(
            research_question=research_question,
            research_synthesis=research_synthesis,
        )

        try:

            # -----------------------------------
            # Step 1. Check Input
            # -----------------------------------

            state.current_step = (
                "check_input"
            )

            if not research_synthesis:

                raise ValueError(
                    "Research Partner requires "
                    "research synthesis."
                )

            research_gaps = (
                research_synthesis.get(
                    "research_gaps",
                    [],
                )
            )

            if not research_gaps:

                raise ValueError(
                    "Research synthesis does not "
                    "contain research gaps."
                )

            # -----------------------------------
            # Step 2. Generate Proposal
            # -----------------------------------

            state.current_step = (
                "generate_proposal"
            )

            state.proposal = (
                self.agent
                .generate_research_proposal(
                    research_question=(
                        research_question
                    ),
                    research_synthesis=(
                        research_synthesis
                    ),
                )
            )

            # -----------------------------------
            # Step 3. Validate
            # -----------------------------------

            state.current_step = (
                "validate"
            )

            state.specification_satisfied = (
                validate_research_proposal(
                    state.proposal
                )
            )

            # -----------------------------------
            # Step 4. Complete
            # -----------------------------------

            if (
                state
                .specification_satisfied
            ):

                state.current_step = (
                    "complete"
                )

            else:

                state.current_step = (
                    "needs_retry"
                )

        except Exception as error:

            state.error = str(error)

            state.current_step = (
                "failed"
            )

            state.specification_satisfied = (
                False
            )

        return state