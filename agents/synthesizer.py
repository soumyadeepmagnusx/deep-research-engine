"""Synthesizer Agent:
Compiles verified evidence and critical analysis into an authoritative,
citation-backed research report in GitHub Markdown format.
"""

from typing import List, Dict, Any
from core.llm_client import LLMClient


class SynthesizerAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def synthesize_report(
        self,
        topic: str,
        queries: List[str],
        evidences: List[Dict[str, Any]],
        critique: Dict[str, Any]
    ) -> str:
        """Generate final academic-quality Markdown report with inline citations."""
        evidence_context = ""
        for i, ev in enumerate(evidences[:10], 1):
            evidence_context += f"Source [{i}] '{ev.get('title')}': {ev.get('content', '')[:400]}\nURL: {ev.get('url')}\n\n"

        system_instruction = (
            "You are the Principal Research Synthesizer. Your objective is to author an authoritative, "
            "comprehensive, academic-grade research paper in Markdown. "
            "Use clear headings, markdown comparison tables, inline numerical citations like [1], [2], "
            "and embed the Critic's confidence audit. "
            "Include an Executive Summary, System Architecture/Principles, State of the Art & Benchmarks, "
            "Bottlenecks & Security/Practical Constraints, and Future 2026-2030 Outlook."
        )

        prompt = (
            f"# Topic: {topic}\n\n"
            f"Research Queries Investigated:\n" + "\n".join(f"- {q}" for q in queries) + "\n\n"
            f"Verified Evidence Collected:\n{evidence_context}\n\n"
            f"Critic Audit & Confidence:\n{critique.get('audit_report')}\n"
            f"Fact-Check Score: {critique.get('confidence_score')}/100\n\n"
            f"Write the comprehensive, deeply technical, citation-backed Markdown report now."
        )

        report = self.llm.generate(prompt=prompt, system_instruction=system_instruction)

        # Append structured bibliography if not present
        if "### References" not in report and "## References" not in report:
            bib = "\n\n## References & Verified Citations\n"
            for i, ev in enumerate(evidences[:8], 1):
                bib += f"- **[{i}]** [{ev.get('title')}]({ev.get('url')}) - *{ev.get('snippet')[:120]}...*\n"
            report += bib

        return report
