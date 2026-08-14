#from llm import ask_llm
from research_companion.agent import ResearchCompanionAgent

def main():
    agent = ResearchCompanionAgent()

    research_question = (
        "에이전트를 고정된 절차적 워크플로우의 실행 노드가 아닌 명확한 직무 경계(Scope)와 책임을 가진 독립 주체로 정의할 때, 예기치 않은 시스템 오작동(월권 행동, 프롬프트 이탈)을 얼마나 효과적으로 통제할 수 있는가?"
    )

    state = agent.search_literature(
        research_question=research_question,
        max_results=15,
        top_n=5,        
    )

    print("=" * 60)
    print("Research Question")
    print("=" * 60)
    print(state.research_question)

    print()

    print("=" * 60)
    print("Search Query")
    print("=" * 60)
    print(state.search_query)


    print("=" * 60)
    print("Workflow Summary")
    print("=" * 60)

    print()

    print(
        "Candidate Papers:",
        len(state.candidate_papers),
    )

    print(
        "After Deduplication:",
        len(state.deduplicated_papers),
    )

    print(
        "Evaluated Papers:",
        len(state.evaluated_papers),
    )

    print(
        "Selected Papers:",
        len(state.selected_papers),
    )

    print()


    print("=" * 60)
    print("Selected Papers")
    print("=" * 60)


    for index, paper in enumerate(
        state.selected_papers,
        start=1,
    ):
        print()
        print(f"[{index}] {paper['title']}")
        print("Score:", paper["relevance_score"],  )
        print("Reason:", paper["relevance_reason"],  )

        print(
            "Authors:",
            ", ".join(paper["authors"])
        )

        print(
            "Published:",
            paper["published"]
        )

        print(
            "URL:",
            paper["url"]
        )

    print()

    print("=" * 60)
    print("Specification Validation")
    print("=" * 60)


    print(
        "Satisfied:",
        state.specification_satisfied,
    )

    print(
        "Final Workflow State:",
        state.current_step,
    )

if __name__ == "__main__":
    main()