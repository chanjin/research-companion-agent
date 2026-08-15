# src/research_companion/orchestration/state.py

from dataclasses import dataclass, field
from typing import Optional

from research_companion.state import (
    ResearchState,
    PaperReadingState,
    ResearchAnalysisState,
    ResearchPartnerState,
)


VALID_RUN_STATUSES = {
    "created",
    "running",
    "needs_retry",
    "insufficient_evidence",
    "waiting_for_human",
    "completed",
    "failed",
}


@dataclass
class AgentRunState:
    """
    Research Companion 전체 Workflow의
    상위 실행 상태.

    각 Job의 세부 State를 내부에 보유하며,
    전체 실행 위치와 상태를 관리한다.
    """

    user_request: str = ""

    research_topic: str = ""

    research_question: str = ""

    current_job: str = ""

    current_step: str = ""

    status: str = "created"

    # -----------------------------------
    # Memory
    # -----------------------------------

    recalled_memory: list = field(
        default_factory=list
    )

    # -----------------------------------
    # Job States
    # -----------------------------------

    search_state: Optional[
        ResearchState
    ] = None

    reading_states: list[
        PaperReadingState
    ] = field(
        default_factory=list
    )

    analysis_state: Optional[
        ResearchAnalysisState
    ] = None

    partner_state: Optional[
        ResearchPartnerState
    ] = None

    # -----------------------------------
    # Human Gate
    # -----------------------------------

    pending_human_decision: bool = False

    human_decision_id: Optional[str] = None

    # -----------------------------------
    # Error
    # -----------------------------------

    error: Optional[str] = None

    def set_status(
        self,
        status: str,
    ) -> None:

        if status not in VALID_RUN_STATUSES:

            raise ValueError(
                f"Invalid run status: {status}"
            )

        self.status = status