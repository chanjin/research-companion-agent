# src/research_companion/memory/store.py

import sqlite3
from pathlib import Path

from research_companion.memory.models import Episode


class SQLiteMemoryStore:

    def __init__(
        self,
        db_path: str | Path = (
            "data/memory/research_memory.db"
        ),
    ):
        self.db_path = Path(
            db_path
        )

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(self):
        return sqlite3.connect(
            self.db_path
        )

    def _initialize_database(
        self,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS episodes (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    episode_type TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    details TEXT NOT NULL,
                    research_question TEXT,
                    source TEXT,
                    importance INTEGER NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_episodes_type
                ON episodes(episode_type)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_episodes_rq
                ON episodes(research_question)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_episodes_importance
                ON episodes(importance)
                """
            )

            connection.commit()

    def save_episode(
        self,
        episode: Episode,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO episodes (
                    id,
                    timestamp,
                    episode_type,
                    summary,
                    details,
                    research_question,
                    source,
                    importance
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    episode.id,
                    episode.timestamp,
                    episode.episode_type,
                    episode.summary,
                    episode.details,
                    episode.research_question,
                    episode.source,
                    episode.importance,
                ),
            )

            connection.commit()

    def get_episode(
        self,
        episode_id: str,
    ) -> Episode | None:

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT
                    id,
                    timestamp,
                    episode_type,
                    summary,
                    details,
                    research_question,
                    source,
                    importance
                FROM episodes
                WHERE id = ?
                """,
                (
                    episode_id,
                ),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_episode(
            row
        )

    def list_episodes(
        self,
        limit: int = 20,
    ) -> list[Episode]:

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT
                    id,
                    timestamp,
                    episode_type,
                    summary,
                    details,
                    research_question,
                    source,
                    importance
                FROM episodes
                ORDER BY
                    importance DESC,
                    timestamp DESC
                LIMIT ?
                """,
                (
                    limit,
                ),
            )

            rows = cursor.fetchall()

        return [
            self._row_to_episode(row)
            for row in rows
        ]

    def find_by_type(
        self,
        episode_type: str,
        limit: int = 10,
    ) -> list[Episode]:

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT
                    id,
                    timestamp,
                    episode_type,
                    summary,
                    details,
                    research_question,
                    source,
                    importance
                FROM episodes
                WHERE episode_type = ?
                ORDER BY
                    importance DESC,
                    timestamp DESC
                LIMIT ?
                """,
                (
                    episode_type,
                    limit,
                ),
            )

            rows = cursor.fetchall()

        return [
            self._row_to_episode(row)
            for row in rows
        ]

    def find_by_research_question(
        self,
        research_question: str,
        limit: int = 10,
    ) -> list[Episode]:

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT
                    id,
                    timestamp,
                    episode_type,
                    summary,
                    details,
                    research_question,
                    source,
                    importance
                FROM episodes
                WHERE research_question = ?
                ORDER BY
                    importance DESC,
                    timestamp DESC
                LIMIT ?
                """,
                (
                    research_question,
                    limit,
                ),
            )

            rows = cursor.fetchall()

        return [
            self._row_to_episode(row)
            for row in rows
        ]

    def delete_all(
        self,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                "DELETE FROM episodes"
            )

            connection.commit()

    @staticmethod
    def _row_to_episode(
        row,
    ) -> Episode:

        return Episode(
            id=row[0],
            timestamp=row[1],
            episode_type=row[2],
            summary=row[3],
            details=row[4],
            research_question=row[5],
            source=row[6],
            importance=row[7],
        )