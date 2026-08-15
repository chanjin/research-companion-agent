# src/research_companion/observability/store.py

import json
import sqlite3
from pathlib import Path

from research_companion.observability.models import (
    RunEvent,
    RunRecord,
)


DEFAULT_RUN_DB = Path(
    "data/runs/research_runs.db"
)


class SQLiteRunStore:

    def __init__(
        self,
        db_path: str | Path = DEFAULT_RUN_DB,
    ):

        self.db_path = Path(
            db_path
        )

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(
        self,
    ) -> sqlite3.Connection:

        connection = sqlite3.connect(
            self.db_path
        )

        connection.row_factory = (
            sqlite3.Row
        )

        return connection

    def _initialize_database(
        self,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    research_topic TEXT,
                    research_question TEXT,
                    user_request TEXT,
                    status TEXT NOT NULL,
                    error TEXT
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    job TEXT,
                    step TEXT,
                    status TEXT,
                    message TEXT,
                    data_json TEXT,
                    FOREIGN KEY(run_id)
                        REFERENCES runs(run_id)
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_runs_started_at
                ON runs(started_at)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_runs_status
                ON runs(status)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_events_run_id
                ON events(run_id)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_events_timestamp
                ON events(timestamp)
                """
            )

            connection.commit()

    # =======================================
    # Run
    # =======================================

    def save_run(
        self,
        run: RunRecord,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO runs (
                    run_id,
                    started_at,
                    completed_at,
                    research_topic,
                    research_question,
                    user_request,
                    status,
                    error
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run.run_id,
                    run.started_at,
                    run.completed_at,
                    run.research_topic,
                    run.research_question,
                    run.user_request,
                    run.status,
                    run.error,
                ),
            )

            connection.commit()

    def update_run(
        self,
        run: RunRecord,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                UPDATE runs
                SET
                    completed_at = ?,
                    research_topic = ?,
                    research_question = ?,
                    user_request = ?,
                    status = ?,
                    error = ?
                WHERE run_id = ?
                """,
                (
                    run.completed_at,
                    run.research_topic,
                    run.research_question,
                    run.user_request,
                    run.status,
                    run.error,
                    run.run_id,
                ),
            )

            connection.commit()

    def get_run(
        self,
        run_id: str,
    ) -> RunRecord | None:

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT *
                FROM runs
                WHERE run_id = ?
                """,
                (
                    run_id,
                ),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_run(
            row
        )

    def list_runs(
        self,
        limit: int = 20,
    ) -> list[RunRecord]:

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT *
                FROM runs
                ORDER BY started_at DESC
                LIMIT ?
                """,
                (
                    limit,
                ),
            )

            rows = cursor.fetchall()

        return [
            self._row_to_run(row)
            for row in rows
        ]

    # =======================================
    # Event
    # =======================================

    def save_event(
        self,
        event: RunEvent,
    ) -> None:

        data_json = json.dumps(
            event.data or {},
            ensure_ascii=False,
        )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO events (
                    id,
                    run_id,
                    timestamp,
                    event_type,
                    job,
                    step,
                    status,
                    message,
                    data_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.id,
                    event.run_id,
                    event.timestamp,
                    event.event_type,
                    event.job,
                    event.step,
                    event.status,
                    event.message,
                    data_json,
                ),
            )

            connection.commit()

    def get_events(
        self,
        run_id: str,
    ) -> list[RunEvent]:

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT *
                FROM events
                WHERE run_id = ?
                ORDER BY timestamp ASC
                """,
                (
                    run_id,
                ),
            )

            rows = cursor.fetchall()

        return [
            self._row_to_event(row)
            for row in rows
        ]

    def delete_all(
        self,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                "DELETE FROM events"
            )

            connection.execute(
                "DELETE FROM runs"
            )

            connection.commit()

    # =======================================
    # Conversion
    # =======================================

    @staticmethod
    def _row_to_run(
        row,
    ) -> RunRecord:

        return RunRecord(
            run_id=row["run_id"],
            started_at=row["started_at"],
            completed_at=row[
                "completed_at"
            ],
            research_topic=row[
                "research_topic"
            ] or "",
            research_question=row[
                "research_question"
            ] or "",
            user_request=row[
                "user_request"
            ] or "",
            status=row["status"],
            error=row["error"],
        )

    @staticmethod
    def _row_to_event(
        row,
    ) -> RunEvent:

        data = {}

        if row["data_json"]:
            try:
                data = json.loads(
                    row["data_json"]
                )
            except json.JSONDecodeError:
                data = {}

        return RunEvent(
            id=row["id"],
            run_id=row["run_id"],
            timestamp=row["timestamp"],
            event_type=row[
                "event_type"
            ],
            job=row["job"],
            step=row["step"],
            status=row["status"],
            message=row["message"],
            data=data,
        )