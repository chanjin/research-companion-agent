#from llm import ask_llm
from agent import ResearchCompanionAgent

def main():
    #prompt = "연구 질문이란 무엇인지 간단히 설명해줘."
    # prompt = """ 나는 AI Agent에 관한 연구를 시작하려고 한다. 이 연구 주제를 탐색하기 위해 고려할 수 있는 연구 질문 3개를 제안해줘."""

    agent = ResearchCompanionAgent()

    # agent.research_topic = "AI Agents"
    #agent.research_question = (
    #    "How does persistent memory affect the performance of research agents?"
    #)
    #response = agent.run(
    #    "현재 연구 질문을 평가하고 개선 방향을 제안해줘."
    #)
    #print(response)

    research_question = (
        "How does episodic memory affect "
        "the performance of autonomous AI agents?"
    )

    state = agent.search_literature(
        research_question=research_question,
        max_results=10,
    )

    print("=" * 60)
    print("Research Question")
    print("=" * 60)
    print(state.research_question)

    print()

    print("=" * 60)
    print("Generated Search Query")
    print("=" * 60)
    print(state.search_query)

    print()

    print("=" * 60)
    print("Candidate Papers")
    print("=" * 60)

    for index, paper in enumerate(
        state.candidate_papers,
        start=1,
    ):

        print()
        print(f"[{index}] {paper['title']}")

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
    print("Workflow State")
    print("=" * 60)

    print(
        "Current Step:",
        state.current_step
    )




if __name__ == "__main__":
    main()