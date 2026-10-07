"""Critic / Fact-Checker Agent:
Audits gathered research, cross-checks claims, identifies contradictions,
and computes a Fact-Check Confidence Score.
"""

from typing import List, Dict, Any
from core.llm_client import LLMClient


class CriticAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def audit_evidence(self, topic: str, evidences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform peer-review critique on evidence."""
        evidence_summary = ""
        for i, ev in enumerate(evidences[:8], 1):
            evidence_summary += f"[{i}] {ev.get('title')}: {ev.get('snippet')}\n"

        system_instruction = (
            "You are a rigorous Scientific Peer-Reviewer & Fact-Checker Agent. "
            "Analyze the gathered evidence for factual consistency, citation reliability, "
            "and technical limitations. "
            "Provide:\n"
            "1. Verified Core Claims\n"
            "2. Identified Caveats & Conflicting Arguments\n"
            "3. Fact-Check Confidence Score (0-100)\n"
            "Be objective, critical, and rigorous."
        )

        prompt = (
            f"Topic: {topic}\n\n"
            f"Gathered Evidence:\n{evidence_summary}\n\n"
            f"Perform an exhaustive fact-checking audit and peer review."
        )

        audit_text = self.llm.generate(prompt=prompt, system_instruction=system_instruction)

        # Estimate a numeric score or parse from text
        score = 88
        for word in audit_text.split():
            clean = word.strip("/%:,.")
            if clean.isdigit():
                val = int(clean)
                if 50 <= val <= 100:
                    score = val
                    break

        return {
            "audit_report": audit_text,
            "confidence_score": score
        }
