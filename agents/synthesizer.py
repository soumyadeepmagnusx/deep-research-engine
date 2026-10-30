"""Synthesizer Agent:
Compiles verified evidence and critical analysis into an authoritative,
citation-backed research report in GitHub Markdown format.
"""

from typing import List, Dict, Any
from core.llm_client import LLMClient
from core.analysis_tools import extract_key_concepts


class SynthesizerAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def synthesize_report(
        self,
        topic: str,
        queries: List[str],
        evidences: List[Dict[str, Any]],
        critique: Dict[str, Any],
        rigor_tone: str = "Academic"
    ) -> str:
        """Generate final academic/executive/security Markdown report with inline citations."""
        evidence_context = ""
        for i, ev in enumerate(evidences[:12], 1):
            evidence_context += f"Source [{i}] '{ev.get('title')}': {ev.get('content', '')[:400]}\nURL: {ev.get('url')}\n\n"

        tone_guidelines = {
            "Academic": "Author an authoritative, peer-reviewed academic research paper adhering to IEEE/ACM technical rigor with formal terminology, comparative tables, and threats to validity.",
            "Executive": "Author a high-impact C-Suite Strategic Whitepaper focusing on operational viability, cost/latency tradeoffs, risk vectors, and 2026-2030 deployment ROI.",
            "RedTeam": "Author an adversarial Cyber-Security & Penetration Audit report identifying threat vectors, architectural flaws, zero-trust vulnerabilities, and remediation frameworks."
        }.get(rigor_tone, "Author an authoritative academic research paper.")

        system_instruction = (
            f"You are the Principal Research Synthesizer. Tone & Directive: {tone_guidelines} "
            "Use clear headings, markdown comparison tables, inline numerical citations like [1], [2], "
            "and embed the Critic's confidence audit. "
            "Include an Executive Summary, System Architecture/Principles, State of the Art & Benchmarks, "
            "Bottlenecks & Security/Practical Constraints, and Future 2026-2030 Outlook."
        )

        prompt = (
            f"# Topic: {topic}\n"
            f"Mode: {rigor_tone}\n\n"
            f"Research Queries Investigated:\n" + "\n".join(f"- {q}" for q in queries) + "\n\n"
            f"Verified Evidence Collected:\n{evidence_context}\n\n"
            f"Critic Audit & Confidence:\n{critique.get('audit_report')}\n"
            f"Fact-Check Score: {critique.get('confidence_score')}/100\n\n"
            f"Write the comprehensive, deeply technical, citation-backed Markdown report now."
        )

        report = self.llm.generate(prompt=prompt, system_instruction=system_instruction)

        # Append structured taxonomy index if not present
        if "## Technical Taxonomy" not in report and "### Technical Taxonomy" not in report:
            corpus = f"{topic}\n" + " ".join(e.get('title', '') + " " + e.get('snippet', '') for e in evidences)
            concepts = extract_key_concepts(corpus, top_n=6)
            if concepts:
                report += "\n\n" + self.generate_taxonomy_index(concepts)

        # Append structured bibliography if not present
        if "### References" not in report and "## References" not in report:
            bib = "\n\n## References & Verified Citations\n"
            for i, ev in enumerate(evidences[:10], 1):
                bib += f"- **[{i}]** [{ev.get('title')}]({ev.get('url')}) - *{ev.get('snippet')[:120]}...*\n"
            report += bib

        return report

    def generate_taxonomy_index(self, concepts: List[Dict[str, Any]]) -> str:
        """Format an indexed technical taxonomy table for the synthesized publication."""
        lines = [
            "## Technical Taxonomy & Concept Index",
            "",
            "| Concept / Identifier | Classification | Relevance Index | Frequency |",
            "| :--- | :--- | :--- | :--- |"
        ]
        for c in concepts:
            lines.append(
                f"| `{c['term']}` | **{c['category']}** | {c['relevance_score']}% | {c['frequency']}x |"
            )
        return "\n".join(lines)


    def generate_bibtex(self, topic: str, evidences: List[Dict[str, Any]]) -> str:
        """Generate formal BibTeX entries for academic citation management."""
        entries = []
        for i, ev in enumerate(evidences[:12], 1):
            key = f"source{i}_{topic[:10].replace(' ', '_').lower()}"
            title = ev.get('title', 'Unknown Title').replace('"', '')
            url = ev.get('url', 'https://arxiv.org')
            entry = (
                f"@misc{{{key},\n"
                f"  title = {{{{{title}}}}},\n"
                f"  howpublished = {{\\url{{{url}}}}},\n"
                f"  year = {{2026}},\n"
                f"  note = {{Accessed via DeepResearch Swarm}}\n"
                f"}}"
            )
            entries.append(entry)
        return "\n\n".join(entries)
