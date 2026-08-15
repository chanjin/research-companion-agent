# src/research_companion/main.py

from research_companion.agent import (
    ResearchCompanionAgent,
)
from research_companion.orchestration.orchestrator import (
    ResearchOrchestrator,
)


RESEARCH_TOPIC = (
    "Job-bounded AI Agent Governance"
)


RESEARCH_QUESTION = (
    "에이전트를 고정된 절차적 워크플로우의 "
    "실행 노드가 아닌 명확한 직무 경계(Scope), "
    "책임(Responsibility), 권한(Authority)을 가진 "
    "독립 주체로 정의할 때, 월권 행동이나 "
    "프롬프트 이탈과 같은 예기치 않은 시스템 "
    "오작동을 얼마나 효과적으로 통제할 수 있는가?"
)


USER_REQUEST = (
    "현재 연구 질문과 관련된 문헌을 조사하고, "
    "핵심 연구 Gap을 분석한 뒤 "
    "다음 연구 방향을 제안해줘."
)


def print_run_summary(
    state,
) -> None:

    print()
    print("=" * 70)
    print("RESEARCH COMPANION RUN")
    print("=" * 70)

    print(
        "Status:",
        state.status,
    )

    print(
        "Current Job:",
        state.current_job,
    )

    print(
        "Current Step:",
        state.current_step,
    )

    print(
        "Research Question:"
    )

    print(
        state.research_question
    )

    if state.error:

        print()
        print(
            "Error:"
        )

        print(
            state.error
        )


def print_partner_candidates(
    state,
) -> list[dict]:

    if (
        state.partner_state
        is None
    ):
        return []

    proposal = (
        state.partner_state
        .proposal
    )

    candidates = (
        proposal.get(
            "refined_research_questions",
            [],
        )
    )

    print()
    print("=" * 70)
    print("CANDIDATE RESEARCH QUESTIONS")
    print("=" * 70)

    for index, candidate in enumerate(
        candidates,
        start=1,
    ):

        print()
        print(
            f"[{index}] "
            f"{candidate.get('rq', '')}"
        )

        print(
            "Rationale:",
            candidate.get(
                "rationale",
                "",
            ),
        )

    return candidates


def get_candidate_index(
    candidates: list[dict],
) -> int:

    while True:

        raw_value = input(
            "\nSelect candidate number: "
        ).strip()

        try:

            selected = int(
                raw_value
            )

        except ValueError:

            print(
                "Please enter a number."
            )

            continue

        if (
            selected < 1
            or selected > len(
                candidates
            )
        ):

            print(
                "Invalid candidate number."
            )

            continue

        return selected - 1


def get_human_decision() -> str:

    valid_decisions = {
        "approve",
        "reject",
        "revise",
        "defer",
    }

    while True:

        value = input(
            "\nDecision "
            "(approve/reject/revise/defer): "
        ).strip().lower()

        if value in valid_decisions:

            return value

        print(
            "Invalid decision."
        )


def main():

    # ===================================
    # Agent
    # ===================================

    agent = (
        ResearchCompanionAgent()
    )

    # ===================================
    # Orchestrator
    # ===================================

    orchestrator = (
        ResearchOrchestrator(
            agent
        )
    )

    # ===================================
    # Automatic Agent Workflow
    # ===================================

    state = orchestrator.run(
        user_request=(
            USER_REQUEST
        ),
        research_topic=(
            RESEARCH_TOPIC
        ),
        research_question=(
            RESEARCH_QUESTION
        ),

        # 각 검색 query당 최대 5편
        max_results_per_query=5,

        # Literature Scout 최종 선택
        top_n=5,

        # M11 실습에서는 3편 읽기
        papers_to_read=3,

        # 로컬 LLM 부담 제한
        max_pages_per_paper=8,
    )

    print_run_summary(
        state
    )

    # ===================================
    # Workflow가 Human Gate에
    # 도달하지 못한 경우 종료
    # ===================================

    if (
        state.status
        != "waiting_for_human"
    ):

        print()
        print(
            "Workflow stopped before "
            "human review."
        )

        return

    # ===================================
    # Human Approval Gate
    # ===================================

    candidates = (
        print_partner_candidates(
            state
        )
    )

    if not candidates:

        print(
            "No candidate research "
            "questions available."
        )

        return

    candidate_index = (
        get_candidate_index(
            candidates
        )
    )

    decision = (
        get_human_decision()
    )

    revised_content = None

    if decision == "revise":

        revised_content = input(
            "\nEnter revised research question:\n> "
        ).strip()

    reason = input(
        "\nReason for decision:\n> "
    ).strip()

    # ===================================
    # Resume Workflow
    # ===================================

    state = (
        orchestrator
        .apply_human_decision(
            state=state,
            candidate_index=(
                candidate_index
            ),
            decision=decision,
            revised_content=(
                revised_content
            ),
            reason=reason,
        )
    )

    # ===================================
    # Final Status
    # ===================================

    print()
    print("=" * 70)
    print("FINAL RUN STATUS")
    print("=" * 70)

    print(
        "Status:",
        state.status,
    )

    print(
        "Current Step:",
        state.current_step,
    )

    print(
        "Current Research Question:"
    )

    print(
        state.research_question
    )

    if state.human_decision_id:

        print(
            "Decision ID:",
            state.human_decision_id,
        )

    if state.error:

        print(
            "Error:",
            state.error,
        )


if __name__ == "__main__":
    main()