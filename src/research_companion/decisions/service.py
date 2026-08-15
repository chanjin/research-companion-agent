# src/research_companion/decisions/service.py

from research_companion.decisions.models import (
    ResearchDecision,
)
from research_companion.memory.service import (
    MemoryService,
)


class DecisionService:

    def __init__(
        self,
        memory_service: MemoryService,
    ):
        self.memory = memory_service

    def create_decision(
        self,
        decision_type: str,
        target_type: str,
        decision: str,
        original_content: str,
        revised_content: str | None = None,
        reason: str = "",
        research_question: str | None = None,
    ) -> ResearchDecision:

        return ResearchDecision.create(
            decision_type=decision_type,
            target_type=target_type,
            decision=decision,
            original_content=original_content,
            revised_content=revised_content,
            reason=reason,
            research_question=research_question,
            source="researcher",
        )

    def remember_decision(
        self,
        decision: ResearchDecision,
    ):
        """
        ResearchDecision을 중요도가 높은
        Episodic Memory로 저장한다.
        """

        details = self._build_memory_details(
            decision
        )

        return self.memory.remember(
            episode_type=(
                f"decision:"
                f"{decision.decision_type}"
            ),
            summary=self._build_summary(
                decision
            ),
            details=details,
            research_question=(
                decision.research_question
            ),
            source=decision.source,
            importance=5,
        )

    def process_decision(
        self,
        decision_type: str,
        target_type: str,
        decision: str,
        original_content: str,
        revised_content: str | None = None,
        reason: str = "",
        research_question: str | None = None,
    ) -> ResearchDecision:
        """
        Decision 생성 + Memory 저장을 한 번에 수행한다.
        """

        result = self.create_decision(
            decision_type=decision_type,
            target_type=target_type,
            decision=decision,
            original_content=original_content,
            revised_content=revised_content,
            reason=reason,
            research_question=research_question,
        )

        self.remember_decision(
            result
        )

        return result

    @staticmethod
    def _build_summary(
        decision: ResearchDecision,
    ) -> str:

        return (
            f"Researcher {decision.decision}d "
            f"{decision.target_type}"
        )

    @staticmethod
    def _build_memory_details(
        decision: ResearchDecision,
    ) -> str:

        lines = [
            f"Decision type: "
            f"{decision.decision_type}",
            f"Target type: "
            f"{decision.target_type}",
            f"Decision: "
            f"{decision.decision}",
            f"Original content: "
            f"{decision.original_content}",
        ]

        if decision.revised_content:
            lines.append(
                "Revised content: "
                f"{decision.revised_content}"
            )

        if decision.reason:
            lines.append(
                f"Reason: {decision.reason}"
            )

        return "\n".join(
            lines
        )