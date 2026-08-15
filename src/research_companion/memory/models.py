# src/research_companion/memory/models.py

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4


@dataclass
class Episode:
    id: str
    timestamp: str
    episode_type: str
    summary: str
    details: str

    research_question: Optional[str] = None
    source: Optional[str] = None

    importance: int = 3

    @classmethod
    def create(
        cls,
        episode_type: str,
        summary: str,
        details: str,
        research_question: str | None = None,
        source: str | None = None,
        importance: int = 3,
    ) -> "Episode":

        if importance < 1 or importance > 5:
            raise ValueError(
                "importance must be between 1 and 5"
            )

        return cls(
            id=str(uuid4()),
            timestamp=datetime.now(
                timezone.utc
            ).isoformat(),
            episode_type=episode_type,
            summary=summary,
            details=details,
            research_question=research_question,
            source=source,
            importance=importance,
        )