# src/research_companion/main.py

from research_companion.agent import (
    ResearchCompanionAgent,
)


def print_research_partner_proposal(
    partner_state,
) -> None:

    print()
    print("=" * 70)
    print("RESEARCH PARTNER")
    print("=" * 70)

    if partner_state.error:

        print()
        print(
            "Research Partner failed:"
        )

        print(
            partner_state.error
        )

        return

    proposal = (
        partner_state.proposal
    )

    # ===================================
    # RQ Assessment
    # ===================================

    print()
    print("-" * 70)
    print("RQ Assessment")
    print("-" * 70)

    rq_assessment = proposal.get(
        "rq_assessment",
        {},
    )

    print(
        "Assessment:",
        rq_assessment.get(
            "assessment",
            "",
        ),
    )

    print(
        "Reason:",
        rq_assessment.get(
            "reason",
            "",
        ),
    )

    # ===================================
    # Selected Gaps
    # ===================================

    print()
    print("-" * 70)
    print("Selected Research Gaps")
    print("-" * 70)

    for index, gap in enumerate(
        proposal.get(
            "selected_gaps",
            [],
        ),
        start=1,
    ):

        print()
        print(
            f"Gap {index}:",
            gap.get(
                "gap",
                "",
            ),
        )

        print(
            "Why Relevant:",
            gap.get(
                "why_relevant",
                "",
            ),
        )

        print(
            "Confidence:",
            gap.get(
                "confidence",
                "",
            ),
        )

    # ===================================
    # Refined RQs
    # ===================================

    print()
    print("-" * 70)
    print("Refined Research Questions")
    print("-" * 70)

    for index, item in enumerate(
        proposal.get(
            "refined_research_questions",
            [],
        ),
        start=1,
    ):

        print()
        print(
            f"{index}. {item.get('rq', '')}"
        )

        print(
            "Rationale:",
            item.get(
                "rationale",
                "",
            ),
        )

    # ===================================
    # Hypotheses
    # ===================================

    print()
    print("-" * 70)
    print("Candidate Hypotheses")
    print("-" * 70)

    for index, item in enumerate(
        proposal.get(
            "candidate_hypotheses",
            [],
        ),
        start=1,
    ):

        print()
        print(
            f"{index}. "
            f"{item.get('hypothesis', '')}"
        )

        print(
            "Related RQ:",
            item.get(
                "related_rq",
                "",
            ),
        )

        print(
            "Testability:",
            item.get(
                "testability",
                "",
            ),
        )

    # ===================================
    # Research Designs
    # ===================================

    print()
    print("-" * 70)
    print("Proposed Research Designs")
    print("-" * 70)

    for index, design in enumerate(
        proposal.get(
            "proposed_research_designs",
            [],
        ),
        start=1,
    ):

        print()
        print(
            f"Design {index}:"
        )

        print(
            design.get(
                "design",
                "",
            )
        )

        print(
            "Independent Variables:"
        )

        for item in design.get(
            "independent_variables",
            [],
        ):
            print(
                f"- {item}"
            )

        print(
            "Dependent Variables:"
        )

        for item in design.get(
            "dependent_variables",
            [],
        ):
            print(
                f"- {item}"
            )

        print(
            "Comparison:",
            design.get(
                "comparison",
                "",
            ),
        )

        print(
            "Required Data:"
        )

        for item in design.get(
            "required_data",
            [],
        ):
            print(
                f"- {item}"
            )

    # ===================================
    # Evaluation Metrics
    # ===================================

    print()
    print("-" * 70)
    print("Evaluation Metrics")
    print("-" * 70)

    for item in proposal.get(
        "evaluation_metrics",
        [],
    ):
        print(
            f"- {item}"
        )

    # ===================================
    # Risks
    # ===================================

    print()
    print("-" * 70)
    print("Risks and Assumptions")
    print("-" * 70)

    for item in proposal.get(
        "risks_and_assumptions",
        [],
    ):
        print(
            f"- {item}"
        )

    # ===================================
    # Next Actions
    # ===================================

    print()
    print("-" * 70)
    print("Recommended Next Actions")
    print("-" * 70)

    for item in proposal.get(
        "recommended_next_actions",
        [],
    ):
        print(
            f"- {item}"
        )

    print()
    print("=" * 70)

    print(
        "Specification Satisfied:",
        partner_state
        .specification_satisfied,
    )

    print(
        "Final Workflow State:",
        partner_state.current_step,
    )


def main():

    agent = ResearchCompanionAgent()

    research_question = (
        "에이전트를 고정된 절차적 워크플로우의 "
        "실행 노드가 아닌 명확한 직무 경계(Scope), "
        "책임(Responsibility), 권한(Authority)을 가진 "
        "독립 주체로 정의할 때, 월권 행동이나 "
        "프롬프트 이탈과 같은 예기치 않은 시스템 "
        "오작동을 얼마나 효과적으로 통제할 수 있는가?"
    )

    # ===================================
    # Job 1. Literature Scout
    # ===================================

    search_state = (
        agent.search_literature(
            research_question=(
                research_question
            ),
            max_results=5,
            top_n=5,
        )
    )

    if not search_state.selected_papers:

        print(
            "No papers were selected."
        )

        return

    # ===================================
    # Job 2. Paper Reader
    # ===================================

    paper_analyses = []

    for index, paper in enumerate(
        search_state.selected_papers[:3],
        start=1,
    ):

        print()
        print(
            f"Reading paper {index}:"
        )

        print(
            paper["title"]
        )

        reading_state = (
            agent.read_paper(
                paper=paper,
                research_question=(
                    research_question
                ),
                max_pages=8,
            )
        )

        if (
            reading_state
            .specification_satisfied
        ):

            paper_analyses.append(
                reading_state.analysis
            )

            print(
                "Paper analysis complete."
            )

        else:

            print(
                "Paper analysis failed "
                "or needs retry."
            )

            if reading_state.error:

                print(
                    reading_state.error
                )

    if len(paper_analyses) < 2:

        print()
        print(
            "Not enough paper analyses "
            "for Research Analyst."
        )

        return

    # ===================================
    # Job 3. Research Analyst
    # ===================================

    analysis_state = (
        agent.analyze_research_landscape(
            research_question=(
                research_question
            ),
            paper_analyses=(
                paper_analyses
            ),
        )
    )

    if not (
        analysis_state
        .specification_satisfied
    ):

        print()
        print(
            "Research synthesis failed "
            "or needs retry."
        )

        if analysis_state.error:

            print(
                analysis_state.error
            )

        return

    # ===================================
    # Job 4. Research Partner
    # ===================================

    partner_state = (
        agent.propose_research_direction(
            research_question=(
                research_question
            ),
            research_synthesis=(
                analysis_state.synthesis
            ),
        )
    )

    print_research_partner_proposal(
        partner_state
    )


if __name__ == "__main__":
    main()