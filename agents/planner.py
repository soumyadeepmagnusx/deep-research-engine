"""Planner Agent:
Decomposes a complex research topic into targeted sub-questions and search queries.
"""

from typing import List
from core.llm_client import LLMClient


class PlannerAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def plan_research(self, topic: str, depth: int = 4, domain: str = "General") -> List[str]:
        """Generate targeted search queries based on desired depth and domain focus."""
        system_instruction = (
            f"You are the Lead Research Strategist Agent specializing in {domain}. Your role is to break down any topic "
            f"into exactly {depth} precise, diverse, highly targeted technical search queries that "
            "investigate architecture, industry benchmarks, vulnerabilities/risks, and future outlook. "
            f"Output ONLY the {depth} search queries, one per line, with no extra conversation."
        )
        prompt = (
            f"Topic: {topic}\n"
            f"Domain Focus: {domain}\n\n"
            f"Decompose the topic into {depth} targeted web research queries:"
        )

        raw_output = self.llm.generate(prompt=prompt, system_instruction=system_instruction)
        
        # Parse lines
        queries = []
        for line in raw_output.splitlines():
            line = line.strip()
            if line:
                cleaned = line.lstrip("0123456789.-* ")
                if cleaned and len(cleaned) > 5:
                    queries.append(cleaned)

        if not queries:
            base_templates = [
                f"{topic} core technical architecture and mechanisms",
                f"{topic} state of the art benchmarks and comparative evaluation",
                f"{topic} engineering challenges, security vulnerabilities and risks",
                f"{topic} industry standards and future roadmap",
                f"{topic} performance bottlenecks and algorithmic tradeoffs",
                f"{topic} empirical case studies and real world implementations"
            ]
            queries = base_templates[:depth]

        return queries[:depth]
