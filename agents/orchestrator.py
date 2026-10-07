"""Multi-Agent Orchestrator:
Coordinates Planner, Researcher, Critic, and Synthesizer agents in sequence.
Yields real-time events for live progress visualization.
"""

from typing import Dict, Any, Generator
from core.llm_client import LLMClient
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.critic import CriticAgent
from agents.synthesizer import SynthesizerAgent


class ResearchOrchestrator:
    def __init__(self, api_key: str = None):
        self.llm = LLMClient(api_key=api_key)
        self.planner = PlannerAgent(self.llm)
        self.researcher = ResearcherAgent()
        self.critic = CriticAgent(self.llm)
        self.synthesizer = SynthesizerAgent(self.llm)

    def run_stream(self, topic: str, depth: int = 4, domain: str = "General") -> Generator[Dict[str, Any], None, None]:
        """Stream multi-agent workflow events in real time."""
        yield {
            "stage": "init",
            "message": f"Initializing Research Engine for topic: '{topic}' (Domain: {domain}, Depth: {depth} vectors)",
            "mode": "Active Inference Mode" if self.llm.is_live else "Heuristic Simulation Mode",
            "depth": depth,
            "domain": domain
        }

        # 1. Planner Stage
        yield {"stage": "planner", "message": f"🎯 Planner Agent: Formulating {depth} targeted research vectors in {domain}..."}
        queries = self.planner.plan_research(topic, depth=depth, domain=domain)
        yield {
            "stage": "planner_done",
            "message": f"🎯 Planner Agent: Formulated {len(queries)} research vectors.",
            "data": queries
        }

        # 2. Researcher Stage
        all_evidences = []
        for i, q in enumerate(queries, 1):
            yield {
                "stage": "researching",
                "message": f"🔍 Researcher Agent: Querying vector [{i}/{len(queries)}]: '{q}'..."
            }
            evidences = self.researcher.execute_query(q)
            all_evidences.extend(evidences)
            yield {
                "stage": "research_vector_done",
                "message": f"🔍 Extracted {len(evidences)} sources for vector {i}."
            }

        yield {
            "stage": "research_done",
            "message": f"🔍 Researcher Agent: Collected total {len(all_evidences)} verified evidence nodes.",
            "data": [{"title": e["title"], "url": e["url"]} for e in all_evidences]
        }

        # 3. Critic Stage
        yield {"stage": "critic", "message": "⚖️ Critic Agent: Cross-examining sources, auditing bias, and calculating confidence..."}
        critique = self.critic.audit_evidence(topic, all_evidences)
        yield {
            "stage": "critic_done",
            "message": f"⚖️ Critic Agent: Audit complete. Confidence Score: {critique['confidence_score']}/100.",
            "data": critique
        }

        # 4. Synthesizer Stage
        yield {"stage": "synthesizer", "message": "📝 Synthesizer Agent: Compiling academic research report with bibliography..."}
        report = self.synthesizer.synthesize_report(topic, queries, all_evidences, critique)
        yield {
            "stage": "completed",
            "message": "✅ Multi-Agent Deep Research Complete!",
            "report": report,
            "confidence_score": critique["confidence_score"],
            "source_count": len(all_evidences)
        }
