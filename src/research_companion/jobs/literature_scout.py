from research_companion.llm import ask_llm

from research_companion.state import ResearchState
from research_companion.tools.arxiv_search import search_arxiv

def normalize_title(
    title: str,
) -> str:

    return " ".join(
        title.lower().split()
    )


def deduplicate_papers(
    papers: list[dict],
) -> list[dict]:

    seen_titles = set()

    unique_papers = []

    for paper in papers:

        normalized_title = (
            normalize_title(
                paper["title"]
            )
        )

        if normalized_title in seen_titles:
            continue

        seen_titles.add(
            normalized_title
        )

        unique_papers.append(
            paper
        )

    return unique_papers


def rank_papers(
    papers: list[dict],
) -> list[dict]:

    return sorted(
        papers,
        key=lambda paper: paper.get(
            "relevance_score",
            0,
        ),
        reverse=True,
    )


def validate_results(
    state: ResearchState,
    minimum_papers: int = 5,
) -> bool:

    if (
        len(
            state.selected_papers
        )
        < minimum_papers
    ):
        return False

    required_fields = [
        "title",
        "authors",
        "abstract",
        "published",
        "url",
        "pdf_url",
        "relevance_score",
        "relevance_reason",
    ]

    for paper in state.selected_papers:

        for field in required_fields:

            if field not in paper:
                return False

        score = paper[
            "relevance_score"
        ]

        if not isinstance(
            score,
            int,
        ):
            return False

        if (
            score < 1
            or score > 5
        ):
            return False

    return True


class LiteratureScout:

    def __init__(
        self,
        agent,
    ):

        self.agent = agent

    def run(
        self,
        research_question: str,
        max_results: int = 10,
        top_n: int = 5,
    ) -> ResearchState:

        state = ResearchState(
            research_question=research_question
        )

        # ===================================
        # Step 1. Generate Search Queries
        # ===================================

        state.current_step = (
            "generate_queries"
        )

        state.search_queries = (
            self.agent.generate_search_queries(
                research_question
            )
        )

        # ===================================
        # Step 2. Multi-query Search
        # ===================================

        state.current_step = "search"

        all_papers = []

        for query in state.search_queries:

            papers = search_arxiv( query=query,
                max_results=max_results,
            )

            all_papers.extend(
                papers
            )

        state.candidate_papers = (
            all_papers
        )

        # ===================================
        # Step 3. Deduplicate
        # ===================================

        state.current_step = (
            "deduplicate"
        )

        state.deduplicated_papers = (
            deduplicate_papers(
                state.candidate_papers
            )
        )

        # ===================================
        # Step 4. Evaluate Relevance
        # ===================================

        state.current_step = "evaluate"

        evaluated_papers = []

        for paper in (
            state.deduplicated_papers
        ):

            evaluated = (
                self.agent
                .evaluate_paper_relevance(
                    research_question=(
                        research_question
                    ),
                    paper=paper,
                )
            )

            evaluated_papers.append(
                evaluated
            )

        state.evaluated_papers = (
            evaluated_papers
        )

        # ===================================
        # Step 5. Rank
        # ===================================

        state.current_step = "rank"

        ranked_papers = rank_papers(
            state.evaluated_papers
        )

        # ===================================
        # Step 6. Select Top-N
        # ===================================

        state.current_step = "select"

        state.selected_papers = (
            ranked_papers[:top_n]
        )

        # ===================================
        # Step 7. Validate Specification
        # ===================================

        state.current_step = "validate"

        state.specification_satisfied = (
            validate_results(
                state,
                minimum_papers=top_n,
            )
        )

        # ===================================
        # Step 8. Complete
        # ===================================

        if state.specification_satisfied:

            state.current_step = (
                "complete"
            )

        else:

            state.current_step = (
                "needs_retry"
            )

        return state