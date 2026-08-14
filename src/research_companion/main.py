#from llm import ask_llm
from agent import ResearchCompanionAgent

def main():
    #prompt = "연구 질문이란 무엇인지 간단히 설명해줘."
    # prompt = """ 나는 AI Agent에 관한 연구를 시작하려고 한다. 이 연구 주제를 탐색하기 위해 고려할 수 있는 연구 질문 3개를 제안해줘."""

    agent = ResearchCompanionAgent()

    agent.research_topic = "AI Agents"
    agent.research_question = (
        "How does persistent memory affect the performance of research agents?"
    )
    response = agent.run(
        "현재 연구 질문을 평가하고 개선 방향을 제안해줘."
    )
    print(response)


if __name__ == "__main__":
    main()