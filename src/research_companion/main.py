# src/research_companion/main.py

from research_companion.agent import (
    ResearchCompanionAgent,
)


def print_research_synthesis(
    analysis_state,
) -> None:

    print()
    print("=" * 70)
    print("RESEARCH ANALYST")
    print("=" * 70)

    if analysis_state.error:

        print()
        print("Research Analyst failed:")
        print(analysis_state.error)

        return

    synthesis = (
        analysis_state.synthesis
    )

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

    for title, key in sections:

        print()
        print("-" * 70)
        print(title)
        print("-" * 70)

        items = synthesis.get(
            key,
            [],
        )

        for index, item in enumerate(
            items,
            start=1,
        ):
            print(
                f"{index}. {item}"
            )

    print()
    print("-" * 70)
    print("Research Gaps")
    print("-" * 70)

    gaps = synthesis.get(
        "research_gaps",
        [],
    )

    for index, gap in enumerate(
        gaps,
        start=1,
    ):

        print()
        print(
            f"Gap {index}: "
            f"{gap.get('gap', '')}"
        )

        print(
            "Evidence:",
            gap.get(
                "evidence",
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

    print()
    print("=" * 70)

    print(
        "Specification Satisfied:",
        analysis_state.specification_satisfied,
    )

    print(
        "Final Workflow State:",
        analysis_state.current_step,
    )


def main():

    agent = ResearchCompanionAgent()

    research_question = (
        "에이전트를 고정된 절차적 워크플로우의 "
        "실행 노드가 아닌 명확한 직무 경계(Scope), "
        "책임과 권한을 가진 독립 주체로 정의할 때, "
        "월권 행동이나 프롬프트 이탈과 같은 "
        "예기치 않은 시스템 오작동을 얼마나 "
        "효과적으로 통제할 수 있는가?"
    )

    # =======================================
    # Job 1. Literature Scout
    # =======================================

    search_state = (
        agent.search_literature(
            research_question=research_question,
            max_results=5,
            top_n=5,
        )
    )

    if not search_state.selected_papers:

        print(
            "No papers were selected."
        )

        return

    # =======================================
    # Job 2. Paper Reader
    # =======================================

    paper_analyses = []

    for index, paper in enumerate(
        search_state.selected_papers[:3],
        start=1,
    ):

        print()
        print("=" * 70)
        print(
            f"READING PAPER {index}"
        )
        print("=" * 70)

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

    # =======================================
    # 최소 Evidence 확인
    # =======================================

    if len(paper_analyses) < 2:

        print()
        print(
            "Not enough successfully analyzed "
            "papers for cross-paper synthesis."
        )

        return

    # =======================================
    # Job 3. Research Analyst
    # =======================================

    analysis_state = (
        agent.analyze_research_landscape(
            research_question=(
                research_question
            ),
            paper_analyses=paper_analyses,
        )
    )

    print_research_synthesis(
        analysis_state
    )


if __name__ == "__main__":
    main()