# src/research_companion/evaluation/service.py

from research_companion.evaluation.evaluator import (
    SpecificationEvaluator,
)
from research_companion.observability.service import (
    ObservabilityService,
)


class EvaluationService:

    def __init__(
        self,
        observability: (
            ObservabilityService | None
        ) = None,
        evaluator: (
            SpecificationEvaluator | None
        ) = None,
    ):

        self.observability = (
            observability
            if observability is not None
            else ObservabilityService()
        )

        self.evaluator = (
            evaluator
            if evaluator is not None
            else SpecificationEvaluator()
        )

    def evaluate_run(
        self,
        run_id: str,
    ):

        run = (
            self.observability
            .get_run(
                run_id
            )
        )

        if run is None:

            raise ValueError(
                f"Run not found: {run_id}"
            )

        events = (
            self.observability
            .get_events(
                run_id
            )
        )

        return self.evaluator.evaluate(
            run=run,
            events=events,
        )