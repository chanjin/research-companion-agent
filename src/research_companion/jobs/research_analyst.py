# src/research_companion/jobs/research_analyst.py

from research_companion.state import ResearchAnalysisState


REQUIRED_SYNTHESIS_FIELDS = [
    "major_themes",
    "common_problems",
    "common_methods",
    "methodological_differences",
    "common_findings",
    "recurring_limitations",
    "research_trends",
    "research_gaps",
    "implications_for_current_rq",
]


def normalize_analyses(
    paper_analyses: list[dict],
) -> list[dict]:
    """
    Paper Reader의 분석 결과를
    Research Analyst가 비교하기 쉬운
    공통 구조로 정규화한다.
    """

    normalized = []

    for index, analysis in enumerate(
        paper_analyses,
        start=1,
    ):
        normalized.append(
            {
                "paper_id": index,
                "research_problem": analysis.get(
                    "research_problem",
                    "",
                ),
                "research_gap": analysis.get(
                    "research_gap",
                    "",
                ),
                "research_objective": analysis.get(
                    "research_objective",
                    "",
                ),
                "method": analysis.get(
                    "method",
                    "",
                ),
                "dataset": analysis.get(
                    "dataset",
                    "",
                ),
                "experiment": analysis.get(
                    "experiment",
                    "",
                ),
                "results": analysis.get(
                    "results",
                    "",
                ),
                "contribution": analysis.get(
                    "contribution",
                    "",
                ),
                "limitations": analysis.get(
                    "limitations",
                    "",
                ),
                "relevance_to_current_rq": analysis.get(
                    "relevance_to_current_rq",
                    "",
                ),
            }
        )

    return normalized


def validate_research_synthesis(
    synthesis: dict,
    minimum_papers: int,
) -> bool:
    """
    Research Analyst 결과가
    최소 Specification을 만족하는지 검사한다.
    """

    if minimum_papers < 2:
        return False

    if not isinstance(
        synthesis,
        dict,
    ):
        return False

    for field in REQUIRED_SYNTHESIS_FIELDS:
        if field not in synthesis:
            return False

        if not isinstance(
            synthesis[field],
            list,
        ):
            return False

    if not synthesis["major_themes"]:
        return False

    if not synthesis["research_gaps"]:
        return False

    for gap in synthesis["research_gaps"]:

        if not isinstance(
            gap,
            dict,
        ):
            return False

        required_gap_fields = [
            "gap",
            "evidence",
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

            if not gap[field].strip():
                return False

        if gap["confidence"] not in [
            "low",
            "medium",
            "high",
        ]:
            return False

    return True


class ResearchAnalyst:

    def __init__(
        self,
        agent,
    ):
        self.agent = agent

    def run(
        self,
        research_question: str,
        paper_analyses: list[dict],
    ) -> ResearchAnalysisState:

        state = ResearchAnalysisState(
            research_question=research_question,
            paper_analyses=paper_analyses,
        )

        try:

            # -----------------------------------
            # Step 1. Minimum Evidence Check
            # -----------------------------------

            state.current_step = "check_evidence"

            if len(paper_analyses) < 2:
                raise ValueError(
                    "Research Analyst requires at least "
                    "two paper analyses."
                )

            # -----------------------------------
            # Step 2. Normalize Evidence
            # -----------------------------------

            state.current_step = "normalize"

            state.normalized_evidence = (
                normalize_analyses(
                    paper_analyses
                )
            )

            # -----------------------------------
            # Step 3. Cross-paper Synthesis
            # -----------------------------------

            state.current_step = "synthesize"

            state.synthesis = (
                self.agent.synthesize_research(
                    research_question=research_question,
                    paper_analyses=(
                        state.normalized_evidence
                    ),
                )
            )

            # -----------------------------------
            # Step 4. Specification Validation
            # -----------------------------------

            state.current_step = "validate"

            state.specification_satisfied = (
                validate_research_synthesis(
                    synthesis=state.synthesis,
                    minimum_papers=len(
                        state.paper_analyses
                    ),
                )
            )

            # -----------------------------------
            # Step 5. Complete
            # -----------------------------------

            if state.specification_satisfied:
                state.current_step = "complete"

            else:
                state.current_step = "needs_retry"

        except Exception as error:

            state.error = str(error)

            state.current_step = "failed"

            state.specification_satisfied = False

        return state