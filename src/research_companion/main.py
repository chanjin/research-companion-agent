# src/research_companion/main.py

from research_companion.agent import (
    ResearchCompanionAgent,
)


ORIGINAL_RESEARCH_QUESTION = (
    "에이전트를 고정된 절차적 워크플로우의 "
    "실행 노드가 아닌 명확한 직무 경계(Scope), "
    "책임(Responsibility), 권한(Authority)을 가진 "
    "독립 주체로 정의할 때, 월권 행동이나 "
    "프롬프트 이탈과 같은 예기치 않은 시스템 "
    "오작동을 얼마나 효과적으로 통제할 수 있는가?"
)


def show_candidate_research_questions(
    proposal: dict,
) -> list[dict]:

    candidates = proposal.get(
        "refined_research_questions",
        [],
    )

    print()
    print("=" * 70)
    print("CANDIDATE RESEARCH QUESTIONS")
    print("=" * 70)

    for index, item in enumerate(
        candidates,
        start=1,
    ):

        print()
        print(
            f"[{index}] {item.get('rq', '')}"
        )

        print(
            "Rationale:",
            item.get(
                "rationale",
                "",
            ),
        )

    return candidates


def get_candidate_index(
    candidates: list[dict],
) -> int:

    while True:

        raw = input(
            "\nSelect a candidate number: "
        ).strip()

        try:
            selected = int(raw)

        except ValueError:
            print(
                "Please enter a number."
            )
            continue

        if (
            selected < 1
            or selected > len(candidates)
        ):
            print(
                "Invalid candidate number."
            )
            continue

        return selected - 1


def get_decision() -> str:

    valid = {
        "approve",
        "reject",
        "revise",
        "defer",
    }

    while True:

        decision = input(
            "\nDecision "
            "(approve/reject/revise/defer): "
        ).strip().lower()

        if decision in valid:
            return decision

        print(
            "Invalid decision."
        )


def demonstrate_human_decision():

    agent = ResearchCompanionAgent()

    agent.set_research_context(
        topic="Job-bounded AI Agents",
        research_question=(
            ORIGINAL_RESEARCH_QUESTION
        ),
    )

    # ===================================
    # M10 실습에서는 Research Partner의
    # 기존 결과가 있다고 가정한다.
    #
    # 실제 M8 pipeline 결과로 교체 가능하다.
    # ===================================

    example_proposal = {
        "refined_research_questions": [
            {
                "rq": (
                    "Do explicit Scope, "
                    "Responsibility, and Authority "
                    "boundaries reduce unauthorized "
                    "actions in autonomous AI agents?"
                ),
                "rationale": (
                    "This RQ focuses directly on "
                    "measurable authority violations."
                ),
            },
            {
                "rq": (
                    "How do job-bounded AI agents "
                    "compare with fixed workflow-node "
                    "agents in controlling scope "
                    "violations and prompt deviation?"
                ),
                "rationale": (
                    "This creates a direct architectural "
                    "comparison."
                ),
            },
            {
                "rq": (
                    "Which combinations of role, scope, "
                    "and authority constraints most "
                    "effectively reduce unintended "
                    "agent behavior?"
                ),
                "rationale": (
                    "This focuses on individual "
                    "governance mechanisms."
                ),
            },
        ]
    }

    candidates = (
        show_candidate_research_questions(
            example_proposal
        )
    )

    if not candidates:
        print(
            "No candidates available."
        )
        return

    candidate_index = (
        get_candidate_index(
            candidates
        )
    )

    selected_candidate = (
        candidates[
            candidate_index
        ]
    )

    original_content = (
        selected_candidate[
            "rq"
        ]
    )

    decision_value = (
        get_decision()
    )

    revised_content = None

    if decision_value == "revise":

        revised_content = input(
            "\nEnter revised research question:\n> "
        ).strip()

    reason = input(
        "\nReason for this decision:\n> "
    ).strip()

    # ===================================
    # Human Decision 생성 및 적용
    # ===================================

    decision = (
        agent.make_research_decision(
            decision_type="rq_selection",
            target_type="research_question",
            decision=decision_value,
            original_content=(
                original_content
            ),
            revised_content=(
                revised_content
            ),
            reason=reason,
        )
    )

    # ===================================
    # 결과 출력
    # ===================================

    print()
    print("=" * 70)
    print("RESEARCH DECISION")
    print("=" * 70)

    print(
        "Decision:",
        decision.decision,
    )

    print(
        "Original:",
        decision.original_content,
    )

    if decision.revised_content:

        print(
            "Revised:",
            decision.revised_content,
        )

    print(
        "Reason:",
        decision.reason,
    )

    print()
    print("=" * 70)
    print("CURRENT RESEARCH CONTEXT")
    print("=" * 70)

    print(
        "Current RQ:"
    )

    print(
        agent.research_question
    )

    # ===================================
    # Memory 확인
    # ===================================

    print()
    print("=" * 70)
    print("RECENT EPISODIC MEMORY")
    print("=" * 70)

    episodes = (
        agent.memory.recall(
            limit=5
        )
    )

    for index, episode in enumerate(
        episodes,
        start=1,
    ):

        print()
        print(
            f"[{index}] "
            f"{episode.episode_type}"
        )

        print(
            episode.summary
        )

        print(
            episode.details
        )


def main():

    demonstrate_human_decision()


if __name__ == "__main__":
    main()