from pathlib import Path

from llm import ask_llm


class ResearchCompanionAgent:

    def __init__(self):
        prompt_path = Path("prompts/system_prompt.md")
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

        self.research_topic = None
        self.research_question = None

    def set_research_context(
        self,
        topic: str,
        research_question: str,    ):
        self.research_topic = topic
        self.research_question = research_question

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
