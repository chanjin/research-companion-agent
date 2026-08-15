# src/research_companion/state.py

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ResearchState:
    research_question: str = ""

    search_queries: list[str] = field(default_factory=list)

    candidate_papers: list[dict] = field(default_factory=list)
    deduplicated_papers: list[dict] = field(default_factory=list)
    evaluated_papers: list[dict] = field(default_factory=list)
    selected_papers: list[dict] = field(default_factory=list)

    current_step: str = ""

    specification_satisfied: bool = False


@dataclass
class PaperReadingState:
    paper: Optional[dict] = None

    research_question: str = ""

    pdf_path: str = ""
    paper_text: str = ""

    analysis: dict = field(default_factory=dict)

    current_step: str = ""

    specification_satisfied: bool = False

    error: Optional[str] = None


@dataclass
class ResearchAnalysisState:
    research_question: str = ""

    paper_analyses: list[dict] = field(default_factory=list)

    normalized_evidence: list[dict] = field(default_factory=list)

    synthesis: dict = field(default_factory=dict)

    current_step: str = ""

    specification_satisfied: bool = False

    error: Optional[str] = None