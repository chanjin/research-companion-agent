from dataclasses import dataclass, field


@dataclass
class ResearchState:
    research_question: str = ""
    search_query: str = ""

    candidate_papers: list[dict] = field(default_factory=list)
    deduplicated_papers: list[dict] = field(default_factory=list)
    evaluated_papers: list[dict] = field(default_factory=list)
    selected_papers: list[dict] = field(default_factory=list)

    current_step: str = ""
    specification_satisfied: bool = False