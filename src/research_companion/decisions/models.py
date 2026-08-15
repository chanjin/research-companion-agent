# src/research_companion/decisions/models.py

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4


VALID_DECISIONS = {
    "approve",
    "reject",
    "revise",
    "defer",
}


VALID_TARGET_TYPES = {
    "research_question",
    "hypothesis",
    "research_design",
    "research_direction",
    "paper",
}


@dataclass
class ResearchDecision:
    id: str
    timestamp: str

    decision_type: str
    target_type: str

    decision: str

    original_content: str

    revised_content: Optional[str] = None

    reason: str = ""

    research_question: Optional[str] = None

    source: str = "researcher"

    @classmethod
    def create(
        cls,
        decision_type: str,
        target_type: str,
        decision: str,
        original_content: str,
        revised_content: str | None = None,
        reason: str = "",
        research_question: str | None = None,
        source: str = "researcher",
    ) -> "ResearchDecision":

        if decision not in VALID_DECISIONS:
            raise ValueError(
                f"Invalid decision: {decision}"
            )

        if target_type not in VALID_TARGET_TYPES:
            raise ValueError(
                f"Invalid target_type: {target_type}"
            )

        if not original_content.strip():
            raise ValueError(
                "original_content must not be empty"
            )

        if (
            decision == "revise"
            and (
                revised_content is None
                or not revised_content.strip()
            )
        ):
            raise ValueError(
                "revised_content is required "
                "when decision is revise"
            )

        return cls(
            id=str(uuid4()),
            timestamp=datetime.now(
                timezone.utc
            ).isoformat(),
            decision_type=decision_type,
            target_type=target_type,
            decision=decision,
            original_content=original_content,
            revised_content=revised_content,
            reason=reason,
            research_question=research_question,
            source=source,
        )

    @property
    def final_content(self) -> str | None:
        """
        Decision 적용 후 최종적으로 사용할 내용을 반환한다.
        """

        if self.decision == "approve":
            return self.original_content

        if self.decision == "revise":
            return self.revised_content

        if self.decision in {
            "reject",
            "defer",
        }:
            return None

        return None