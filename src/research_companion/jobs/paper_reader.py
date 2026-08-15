# src/research_companion/jobs/paper_reader.py

from research_companion.state import PaperReadingState
from research_companion.tools.pdf_downloader import download_pdf
from research_companion.tools.pdf_parser import parse_pdf


REQUIRED_ANALYSIS_FIELDS = [
    "research_problem",
    "research_gap",
    "research_objective",
    "method",
    "dataset",
    "experiment",
    "results",
    "contribution",
    "limitations",
    "relevance_to_current_rq",
]


def validate_paper_analysis(analysis: dict,) -> bool:
    """
    Paper Reader 결과가 최소 Specification을
    만족하는지 검사한다.
    """

    if not isinstance(analysis, dict, ):
        return False

    for field in REQUIRED_ANALYSIS_FIELDS:
        if field not in analysis:
            return False

        value = analysis[field]

        if not isinstance(value, str, ):
            return False

        if not value.strip():
            return False

    return True


class PaperReader:
    """
    선택된 한 편의 논문을 읽고 분석하는 Job.
    """

    def __init__(
        self,
        agent,
    ):
        self.agent = agent

    def run(
        self,
        paper: dict,
        research_question: str,
        max_pages: int | None = None,
    ) -> PaperReadingState:

        state = PaperReadingState(
            paper=paper,
            research_question=research_question,
        )

        try:

            # -----------------------------------
            # Step 1. PDF Download
            # -----------------------------------

            state.current_step = "download_pdf"

            pdf_url = paper.get(
                "pdf_url"
            )

            if not pdf_url:
                raise ValueError(
                    "Selected paper does not contain a PDF URL."
                )

            state.pdf_path = download_pdf(
                pdf_url=pdf_url,
                paper=paper,
            )

            # -----------------------------------
            # Step 2. PDF Parse
            # -----------------------------------

            state.current_step = "parse_pdf"

            state.paper_text = parse_pdf(
                pdf_path=state.pdf_path,
                max_pages=max_pages,
            )

            # -----------------------------------
            # Step 3. Paper Analysis
            # -----------------------------------

            state.current_step = "analyze_paper"

            state.analysis = (
                self.agent.analyze_paper(
                    research_question=research_question,
                    paper=paper,
                    paper_text=state.paper_text,
                )
            )

            # -----------------------------------
            # Step 4. Specification Validation
            # -----------------------------------

            state.current_step = "validate"

            state.specification_satisfied = (
                validate_paper_analysis(
                    state.analysis
                )
            )

            # -----------------------------------
            # Step 5. Complete
            # -----------------------------------

            if state.specification_satisfied:
                state.current_step = "complete"

            else:
                state.current_step = "needs_retry"

        except Exception as error:

            state.error = str(error)

            state.current_step = "failed"

            state.specification_satisfied = False

        return state