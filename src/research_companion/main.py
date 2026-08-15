# src/research_companion/main.py

from research_companion.agent import (
    ResearchCompanionAgent,
)


RESEARCH_QUESTION = (
    "에이전트를 고정된 절차적 워크플로우의 "
    "실행 노드가 아닌 명확한 직무 경계(Scope), "
    "책임(Responsibility), 권한(Authority)을 가진 "
    "독립 주체로 정의할 때, 월권 행동이나 "
    "프롬프트 이탈과 같은 예기치 않은 시스템 "
    "오작동을 얼마나 효과적으로 통제할 수 있는가?"
)


def print_episodes(
    episodes,
):

    print()
    print("=" * 70)
    print("EPISODIC MEMORY")
    print("=" * 70)

    if not episodes:

        print(
            "No episodes found."
        )

        return

    for index, episode in enumerate(
        episodes,
        start=1,
    ):

        print()
        print(
            f"[{index}] {episode.episode_type}"
        )

        print(
            "Timestamp:",
            episode.timestamp,
        )

        print(
            "Summary:",
            episode.summary,
        )

        print(
            "Details:",
            episode.details,
        )

        print(
            "Importance:",
            episode.importance,
        )


def main():

    # =======================================
    # Session 1
    # =======================================

    agent = ResearchCompanionAgent()

    agent.set_research_context(
        topic="Job-bounded AI Agents",
        research_question=(
            RESEARCH_QUESTION
        ),
    )

    print()
    print("=" * 70)
    print("SESSION 1")
    print("=" * 70)

    # -----------------------------------
    # 연구자의 중요한 결정 저장
    # -----------------------------------

    episode = (
        agent.remember_research_event(
            episode_type=(
                "research_decision"
            ),
            summary=(
                "Focus on Scope, "
                "Responsibility, and Authority."
            ),
            details=(
                "The researcher decided to focus "
                "on explicit job boundaries rather "
                "than prompt-level guardrails alone."
            ),
            research_question=(
                RESEARCH_QUESTION
            ),
            source="researcher",
            importance=5,
        )
    )

    print()
    print(
        "Stored Episode:"
    )

    print(
        episode.summary
    )

    # -----------------------------------
    # RQ refinement decision
    # -----------------------------------

    agent.remember_research_event(
        episode_type="rq_revision",
        summary=(
            "Compare workflow-node agents "
            "with job-bounded agents."
        ),
        details=(
            "The proposed experiment will compare "
            "a fixed workflow-node architecture "
            "against an agent architecture with "
            "explicit Scope, Responsibility, "
            "and Authority boundaries."
        ),
        research_question=(
            RESEARCH_QUESTION
        ),
        source="researcher",
        importance=5,
    )

    # =======================================
    # Session 종료를 흉내 낸다.
    # 새로운 Agent 객체 생성
    # =======================================

    print()
    print("=" * 70)
    print("SESSION 2")
    print("=" * 70)

    new_agent = (
        ResearchCompanionAgent()
    )

    new_agent.set_research_context(
        topic="Job-bounded AI Agents",
        research_question=(
            RESEARCH_QUESTION
        ),
    )

    # -----------------------------------
    # Persistent Memory Recall
    # -----------------------------------

    episodes = (
        new_agent
        .recall_research_memory(
            research_question=(
                RESEARCH_QUESTION
            ),
            limit=5,
        )
    )

    print_episodes(
        episodes
    )

    # -----------------------------------
    # Recall된 기억을 LLM Context에 사용
    # -----------------------------------

    print()
    print("=" * 70)
    print("MEMORY-AWARE AGENT RESPONSE")
    print("=" * 70)

    response = new_agent.run(
        (
            "지난 연구 결정에 맞추어 "
            "다음 연구 단계에서 가장 먼저 "
            "해야 할 일을 제안해줘."
        )
    )

    print()
    print(
        response
    )


if __name__ == "__main__":
    main()