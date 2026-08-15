# src/research_companion/agent.py

import json
from pathlib import Path

from research_companion.llm import ask_llm

from research_companion.jobs.literature_scout import (
    LiteratureScout,
)
from research_companion.jobs.paper_reader import (
    PaperReader,
)
from research_companion.jobs.research_analyst import (
    ResearchAnalyst,
)
from research_companion.jobs.research_partner import (
    ResearchPartner,
)

from research_companion.memory.service import (
    MemoryService,
)

from research_companion.decisions.service import (
    DecisionService,
)
from research_companion.decisions.models import (
    ResearchDecision,
)


class ResearchCompanionAgent:

    def __init__(
        self,
        memory_service: MemoryService | None = None,
    ):

        # ===================================
        # Static Agent Specification
        # ===================================

        self.system_prompt = Path(
            "prompts/system_prompt.md"
        ).read_text(
            encoding="utf-8"
        )

        # ===================================
        # Job Specifications
        # ===================================

        self.paper_reader_prompt = Path(
            "prompts/paper_reader/"
            "analyze_paper.md"
        ).read_text(
            encoding="utf-8"
        )

        self.research_analyst_prompt = Path(
            "prompts/research_analyst/"
            "synthesize_research.md"
        ).read_text(
            encoding="utf-8"
        )

        self.research_partner_prompt = Path(
            "prompts/research_partner/"
            "propose_research.md"
        ).read_text(
            encoding="utf-8"
        )

        # ===================================
        # Current Research Context
        # ===================================

        self.research_topic = None
        self.research_question = None

        # ===================================
        # Persistent Episodic Memory
        # ===================================

        self.memory = (
            memory_service
            if memory_service is not None
            else MemoryService()
        )

        # ===================================
        # Human Decision Layer
        # ===================================

        self.decisions = DecisionService(
            memory_service=self.memory
        )

        # ===================================
        # Jobs
        # ===================================

        self.literature_scout = (
            LiteratureScout(self)
        )

        self.paper_reader = (
            PaperReader(self)
        )

        self.research_analyst = (
            ResearchAnalyst(self)
        )

        self.research_partner = (
            ResearchPartner(self)
        )

    # =======================================
    # Research Context
    # =======================================

    def set_research_context(
        self,
        topic: str,
        research_question: str,
    ) -> None:

        self.research_topic = topic
        self.research_question = (
            research_question
        )

    # =======================================
    # Episodic Memory
    # =======================================

    def remember_research_event(
        self,
        episode_type: str,
        summary: str,
        details: str,
        research_question: str | None = None,
        source: str | None = None,
        importance: int = 3,
    ):

        return self.memory.remember(
            episode_type=episode_type,
            summary=summary,
            details=details,
            research_question=(
                research_question
                or self.research_question
            ),
            source=source,
            importance=importance,
        )

    def recall_research_memory(
        self,
        research_question: str | None = None,
        limit: int = 5,
    ):

        return self.memory.recall(
            research_question=(
                research_question
                or self.research_question
            ),
            limit=limit,
        )

    # =======================================
    # Human Decision Interface
    # =======================================

    def make_research_decision(
        self,
        decision_type: str,
        target_type: str,
        decision: str,
        original_content: str,
        revised_content: str | None = None,
        reason: str = "",
    ) -> ResearchDecision:
        """
        연구자의 Human Decision을 생성하고
        Episodic Memory에 저장한다.
        """

        result = (
            self.decisions.process_decision(
                decision_type=decision_type,
                target_type=target_type,
                decision=decision,
                original_content=original_content,
                revised_content=revised_content,
                reason=reason,
                research_question=(
                    self.research_question
                ),
            )
        )

        self.apply_research_decision(
            result
        )

        return result

    def apply_research_decision(
        self,
        decision: ResearchDecision,
    ) -> None:
        """
        Human Decision을 현재 Research Context에 반영한다.

        M10에서는 우선 Research Question에 대해서만
        실제 Context 변경을 적용한다.
        """

        if (
            decision.target_type
            != "research_question"
        ):
            return

        final_content = (
            decision.final_content
        )

        if final_content is None:
            return

        self.research_question = (
            final_content
        )

    # =======================================
    # General Agent Interaction
    # =======================================

    def run(
        self,
        user_input: str,
    ) -> str:

        memory_context = (
            self.memory.build_memory_context(
                research_question=(
                    self.research_question
                ),
                limit=5,
            )
        )

        dynamic_context = f"""
# Current Research Context

Research Topic:
{self.research_topic or "Not specified"}

Research Question:
{self.research_question or "Not specified"}

# Relevant Episodic Memory

{memory_context}

# Current Request

{user_input}
""".strip()

        return ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=dynamic_context,
        )

    # =======================================
    # Literature Scout
    # =======================================

    def generate_search_queries(
        self,
        research_question: str,
    ) -> list[str]:

        memory_context = (
            self.memory.build_memory_context(
                research_question=(
                    research_question
                ),
                limit=3,
            )
        )

        prompt = f"""
# Current Job

Literature Scout

# Research Question

{research_question}

# Relevant Episodic Memory

{memory_context}

# Task

Generate six complementary academic
search queries.

Use broad discovery queries and
focused queries.

Avoid excessive Boolean restrictions.

Return one query per line.
Do not number the queries.
""".strip()

        response = ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
        )

        queries = []

        for line in response.splitlines():

            query = line.strip()

            if not query:
                continue

            query = query.lstrip(
                "-•0123456789. "
            ).strip()

            if query:
                queries.append(
                    query
                )

        return queries[:6]

    def evaluate_paper_relevance(
        self,
        research_question: str,
        paper: dict,
    ) -> dict:

        prompt = f"""
# Current Job

Literature Scout

# Research Question

{research_question}

# Candidate Paper

Title:
{paper.get("title", "")}

Abstract:
{paper.get("abstract", "")}

# Required Output

Return valid JSON only.

{{
  "score": 1,
  "reason": "short explanation"
}}

Score must be between 1 and 5.
""".strip()

        response = ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
        )

        try:

            result = json.loads(
                response
            )

            score = int(
                result["score"]
            )

            score = max(
                1,
                min(
                    5,
                    score,
                ),
            )

            reason = str(
                result["reason"]
            ).strip()

        except (
            json.JSONDecodeError,
            KeyError,
            ValueError,
            TypeError,
        ):

            score = 1

            reason = (
                "Failed to parse LLM "
                "relevance evaluation."
            )

        return {
            **paper,
            "relevance_score": score,
            "relevance_reason": reason,
        }

    # =======================================
    # Paper Reader
    # =======================================

    def analyze_paper(
        self,
        research_question: str,
        paper: dict,
        paper_text: str,
    ) -> dict:

        user_prompt = f"""
{self.paper_reader_prompt}

# Current Research Question

{research_question}

# Selected Paper Metadata

Title:
{paper.get("title", "")}

Authors:
{", ".join(paper.get("authors", []))}

Published:
{paper.get("published", "")}

URL:
{paper.get("url", "")}

# Paper Content

{paper_text}
""".strip()

        response = ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )

        try:

            return json.loads(
                response
            )

        except json.JSONDecodeError:

            return {
                "research_problem": (
                    "Failed to parse LLM response."
                ),
                "research_gap": (
                    "Failed to parse LLM response."
                ),
                "research_objective": (
                    "Failed to parse LLM response."
                ),
                "method": (
                    "Failed to parse LLM response."
                ),
                "dataset": (
                    "Failed to parse LLM response."
                ),
                "experiment": (
                    "Failed to parse LLM response."
                ),
                "results": (
                    "Failed to parse LLM response."
                ),
                "contribution": (
                    "Failed to parse LLM response."
                ),
                "limitations": (
                    "Failed to parse LLM response."
                ),
                "relevance_to_current_rq": (
                    "Failed to parse LLM response."
                ),
            }

    # =======================================
    # Research Analyst
    # =======================================

    def synthesize_research(
        self,
        research_question: str,
        paper_analyses: list[dict],
    ) -> dict:

        evidence_json = json.dumps(
            paper_analyses,
            ensure_ascii=False,
            indent=2,
        )

        user_prompt = f"""
{self.research_analyst_prompt}

# Current Research Question

{research_question}

# Structured Paper Evidence

{evidence_json}
""".strip()

        response = ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return {
                "major_themes": [],
                "common_problems": [],
                "common_methods": [],
                "methodological_differences": [],
                "common_findings": [],
                "recurring_limitations": [],
                "research_trends": [],
                "research_gaps": [],
                "implications_for_current_rq": [],
            }

    # =======================================
    # Research Partner
    # =======================================

    def generate_research_proposal(
        self,
        research_question: str,
        research_synthesis: dict,
    ) -> dict:

        synthesis_json = json.dumps(
            research_synthesis,
            ensure_ascii=False,
            indent=2,
        )

        memory_context = (
            self.memory.build_memory_context(
                research_question=(
                    research_question
                ),
                limit=5,
            )
        )

        user_prompt = f"""
{self.research_partner_prompt}

# Current Research Question

{research_question}

# Relevant Researcher Decisions

{memory_context}

# Research Analyst Synthesis

{synthesis_json}
""".strip()

        response = ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )

        try:

            return json.loads(
                response
            )

        except json.JSONDecodeError:

            return {
                "rq_assessment": {
                    "assessment": (
                        "needs_reframing"
                    ),
                    "reason": (
                        "Failed to parse "
                        "LLM response."
                    ),
                },
                "selected_gaps": [],
                "refined_research_questions": [],
                "candidate_hypotheses": [],
                "proposed_research_designs": [],
                "evaluation_metrics": [],
                "risks_and_assumptions": [],
                "recommended_next_actions": [],
            }

    # =======================================
    # Job Interfaces
    # =======================================

    def search_literature(
        self,
        research_question: str,
        max_results: int = 10,
        top_n: int = 5,
    ):

        return self.literature_scout.run(
            research_question=research_question,
            max_results=max_results,
            top_n=top_n,
        )

    def read_paper(
        self,
        paper: dict,
        research_question: str,
        max_pages: int | None = None,
    ):

        return self.paper_reader.run(
            paper=paper,
            research_question=research_question,
            max_pages=max_pages,
        )

    def analyze_research_landscape(
        self,
        research_question: str,
        paper_analyses: list[dict],
    ):

        return self.research_analyst.run(
            research_question=research_question,
            paper_analyses=paper_analyses,
        )

    def propose_research_direction(
        self,
        research_question: str,
        research_synthesis: dict,
    ):

        return self.research_partner.run(
            research_question=research_question,
            research_synthesis=research_synthesis,
        )