# src/research_companion/evaluation/evaluator.py

from research_companion.evaluation.models import (
    EvaluationReport,
)
from research_companion.evaluation.rules import (
    ALL_RULES,
)


class SpecificationEvaluator:
    """
    Run Trace를 Specification Rule에
    비추어 평가한다.
    """

    def __init__(
        self,
        rules=None,
    ):

        self.rules = (
            rules
            if rules is not None
            else ALL_RULES
        )

    def evaluate(
        self,
        run,
        events,
    ) -> EvaluationReport:

        checks = []

        for rule in self.rules:

            check = rule(
                run,
                events,
            )

            checks.append(
                check
            )

        return EvaluationReport.create(
            run_id=run.run_id,
            checks=checks,
        )