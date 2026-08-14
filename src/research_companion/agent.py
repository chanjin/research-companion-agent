from pathlib import Path

from llm import ask_llm
from jobs.literature_scout import LiteratureScout

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
Research Topic: {self.research_topic}
Research Question:  {self.research_question}

# Current Request
{user_input}
"""
        return ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=dynamic_context,
        )


    def generate_search_query(
        self,
        research_question: str,
    ) -> str:

        prompt = f"""
# Task

Generate an academic search query for the following
research question.

# Research Question

{research_question}

# Requirements

- Identify the core academic concepts.
- Use concise academic keywords.
- Prefer English terminology suitable for arXiv search.
- Do not explain your reasoning.
- Return only the search query.
    """.strip()
        
        return ask_llm(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
        ).strip()


    # #####
    def search_literature(
    self,
    research_question: str,
    max_results: int = 10,
    ):
        return self.literature_scout.run(
            research_question=research_question,
            max_results=max_results,
        )
