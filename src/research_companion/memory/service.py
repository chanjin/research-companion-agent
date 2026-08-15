# src/research_companion/memory/service.py

from research_companion.memory.models import Episode
from research_companion.memory.store import SQLiteMemoryStore


class MemoryService:

    def __init__(
        self,
        store: SQLiteMemoryStore | None = None,
    ):

        self.store = (
            store
            if store is not None
            else SQLiteMemoryStore()
        )

    def remember(
        self,
        episode_type: str,
        summary: str,
        details: str,
        research_question: str | None = None,
        source: str | None = None,
        importance: int = 3,
    ) -> Episode:

        episode = Episode.create(
            episode_type=episode_type,
            summary=summary,
            details=details,
            research_question=research_question,
            source=source,
            importance=importance,
        )

        self.store.save_episode(
            episode
        )

        return episode

    def recall(
        self,
        research_question: str | None = None,
        episode_type: str | None = None,
        limit: int = 5,
    ) -> list[Episode]:

        if research_question:

            return (
                self.store
                .find_by_research_question(
                    research_question=(
                        research_question
                    ),
                    limit=limit,
                )
            )

        if episode_type:

            return (
                self.store.find_by_type(
                    episode_type=episode_type,
                    limit=limit,
                )
            )

        return self.store.list_episodes(
            limit=limit
        )

    def build_memory_context(
        self,
        research_question: str | None = None,
        limit: int = 5,
    ) -> str:

        episodes = self.recall(
            research_question=research_question,
            limit=limit,
        )

        if not episodes:
            return (
                "No relevant episodic memory available."
            )

        lines = []

        for index, episode in enumerate(
            episodes,
            start=1,
        ):

            lines.append(
                f"""
Episode {index}
Type: {episode.episode_type}
Summary: {episode.summary}
Details: {episode.details}
Importance: {episode.importance}
""".strip()
            )

        return "\n\n".join(
            lines
        )