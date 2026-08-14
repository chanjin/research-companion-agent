from dataclasses import dataclass, field


@dataclass
class ResearchState:
    research_question: str = ""

    search_query: str = ""

    candidate_papers: list[dict] = field(default_factory=list)

    current_step: str = ""