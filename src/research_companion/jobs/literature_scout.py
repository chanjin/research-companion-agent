from llm import ask_llm

from state import ResearchState
from tools.arxiv_search import search_arxiv

class LiteratureScout:

    def __init__(self, agent):
        self.agent = agent

    def run(
            self,
            research_question: str,
            max_results: int = 10,
        ) -> ResearchState:

        state = ResearchState(research_question=research_question)

        # Step 1
        state.current_step = "generate_query"

        state.search_query = (
            self.agent.generate_search_query(
                research_question
            )
        )

        # Step 2
        state.current_step = "search"

        state.candidate_papers = search_arxiv(
            state.search_query,
            max_results=max_results,
        )

        # Step 3
        state.current_step = "complete"

        return state


