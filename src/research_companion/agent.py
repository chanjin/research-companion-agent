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


class ResearchCompanionAgent:

    def __init__(self):

        # ===================================
        # Static Agent Specification
        # ===================================

        system_prompt_path = Path(
            "prompts/system_prompt.md"
        )

        self.system_prompt = (
            system_prompt_path.read_text(
                encoding="utf-8"
            )
        )

        # ===================================
        # Paper Reader Specification
        # ===================================

        paper_reader_prompt_path = Path(
            "prompts/paper_reader/"
            "analyze_paper.md"
        )

        self.paper_reader_prompt = (
            paper_reader_prompt_path.read_text(
                encoding="utf-8"
            )
        )

        # ===================================
        # Research Analyst Specification
        # ===================================

        research_analyst_prompt_path = Path(
            "prompts/research_analyst/"
            "synthesize_research.md"
        )

        self.research_analyst_prompt = (
            research_analyst_prompt_path.read_text(
                encoding="utf-8"
            )
        )

        # ===================================
        # Research Partner Specification
        # ===================================

        research_partner_prompt_path = Path(
            "prompts/research_partner/"
            "propose_research.md"
        )

        self.research_partner_prompt = (
            research_partner_prompt_path.read_text(
                encoding="utf-8"
            )
        )

        # ===================================
        # Current Research Context
        # ===================================

        self.research_topic = None
        self.research_question = None

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
    # General Agent Interaction
    # =======================================

    def run(
        self,
        user_input: str,
    ) -> str:

        dynamic_context = f"""
# Current Research Context

Research Topic:
{self.research_topic or "Not specified"}

Research Question:
{self.research_question or "Not specified"}

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

        prompt = f"""
# Current Job

Literature Scout

# Task

Prepare an academic literature search strategy
for the research question below.

# Research Question

{research_question}

# Instructions

Do NOT generate one overly restrictive
Boolean query.

Generate complementary search queries covering
different conceptual dimensions.

Include:

- broad discovery queries
- related academic terminology
- narrower focused queries

Avoid excessive AND operators.

Prefer high recall.

# Required Output

Return exactly 6 search queries.

Return one query per line.

Do not number the queries.

Do not provide explanations.
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
                queries.append(query)

        return queries[:6]

    def evaluate_paper_relevance(
        self,
        research_question: str,
        paper: dict,
    ) -> dict:

        prompt = f"""
# Current Job

Literature Scout

# Current Workflow Step

Evaluate Paper Relevance

# Research Question

{research_question}

# Candidate Paper

Title:
{paper.get("title", "")}

Abstract:
{paper.get("abstract", "")}

# Evaluation Criteria

Evaluate based on:

1. agent architecture relevance
2. role, scope, responsibility or authority relevance
3. governance or behavioral control relevance
4. unintended or unauthorized behavior relevance
5. usefulness as evidence for the research question

# Required Output

Return valid JSON only.

{{
  "score": 1,
  "reason": "short explanation"
}}

Score must be between 1 and 5.

Do not include Markdown.
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

            return json.loads(
                response
            )

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

        user_prompt = f"""
{self.research_partner_prompt}

# Current Research Question

{research_question}

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