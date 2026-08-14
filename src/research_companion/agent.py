import json
from pathlib import Path

from research_companion.llm import ask_llm
from research_companion.jobs.literature_scout import LiteratureScout

class ResearchCompanionAgent:

    def __init__(self):
        prompt_path = Path("prompts/system_prompt.md")
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

        self.research_topic = None
        self.research_question = None
        self.literature_scout = LiteratureScout(self)



    def set_research_context(
        self,
        topic: str,
        research_question: str,    ):
        self.research_topic = topic
        self.research_question = research_question



#

    def run(self, user_input: str) -> str:
        dynamic_context = f"""
# Current Research Context
Research Topic: {self.research_topic  or "Not specified"}
Research Question:  {self.research_question  or "Not specified"}

# Current Request
{user_input}
""".strip()
        return ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=dynamic_context,
        )


    def generate_search_query(
        self, research_question: str, ) -> str:

        prompt = f"""
You are preparing a literature search strategy
for an academic research question.

# Research Question

{research_question}

# Task

Do NOT directly generate one Boolean query.

1. Identify the major conceptual dimensions
   of the research question.

2. Identify academic synonyms and related
   terminology for those concepts.

3. Generate complementary search queries
   with different levels of breadth.

4. Include broad discovery queries and
   narrower focused queries.

# Search Strategy

Avoid over-constraining queries with many
AND operators.

Prefer queries that maximize literature recall.

# Output

Return 6 academic search queries.

Return one query per line.
Do not number the queries.
Do not provide explanations.
"""
        
        return ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
        ).strip()


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
Title: {paper["title"]}
Abstract: {paper["abstract"]}

# Evaluation Criteria

Evaluate the paper based on:

1. Direct relevance to the research question
2. Conceptual relevance
3. Methodological relevance

# Required Output
Return valid JSON only.
Format:
{{
  "score": 1,
  "reason": "short explanation"
}}

The score must be an integer from 1 to 5.

Do not include markdown.
Do not include any text outside the JSON object.
""".strip()

        response = ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
        )

        try:
            result = json.loads(response)

            score = int(result["score"])
            score = max(1, min(5, score))

            reason = str(result["reason"])

        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            score = 1
            reason = "Failed to parse LLM relevance evaluation."

        return {
            **paper,
            "relevance_score": score,
            "relevance_reason": reason,
        }



    def search_literature(
        self,
        research_question: str,
        max_results: int = 20,
        top_n: int = 5,
    ):

        return self.literature_scout.run(
            research_question=research_question,
            max_results=max_results,
            top_n=top_n,
    )