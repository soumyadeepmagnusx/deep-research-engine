"""Automated Test Suite for DeepResearch Multi-Agent Engine.
"""

import pytest
from core.llm_client import LLMClient
from core.search_tools import live_web_search
from agents.planner import PlannerAgent
from agents.critic import CriticAgent
from agents.synthesizer import SynthesizerAgent
from agents.orchestrator import ResearchOrchestrator


def test_search_tools_fallback():
    """Verify web search returns structured results even when offline."""
    results = live_web_search("Post-Quantum Cryptography", max_results=3)
    assert len(results) >= 2
    assert "title" in results[0]
    assert "url" in results[0]
    assert "snippet" in results[0]


def test_llm_client_fallback_mode():
    """Verify LLM client gracefully returns structured answers in offline simulation mode."""
    llm = LLMClient(api_key=None)
    assert not llm.is_live
    res = llm.generate("Decompose the topic into 4 research queries:")
    assert len(res) > 20


def test_planner_agent():
    """Test planner agent decomposes queries properly."""
    llm = LLMClient(api_key=None)
    planner = PlannerAgent(llm)
    queries = planner.plan_research("Solid State Batteries")
    assert isinstance(queries, list)
    assert len(queries) >= 3


def test_critic_agent():
    """Test critic agent provides an objective confidence score."""
    llm = LLMClient(api_key=None)
    critic = CriticAgent(llm)
    mock_evidences = [
        {"title": "Battery Breakthrough", "snippet": "Energy density improved by 40% in laboratory prototypes.", "url": "https://example.com"}
    ]
    audit = critic.audit_evidence("Solid State Batteries", mock_evidences)
    assert "confidence_score" in audit
    assert 50 <= audit["confidence_score"] <= 100


def test_orchestrator_pipeline_stream():
    """Test end-to-end multi-agent execution pipeline."""
    orchestrator = ResearchOrchestrator(api_key=None)
    events = list(orchestrator.run_stream("Rust vs C++"))
    
    stages = [e["stage"] for e in events]
    assert "init" in stages
    assert "planner" in stages
    assert "completed" in stages

    final_event = events[-1]
    assert final_event["stage"] == "completed"
    assert "report" in final_event
    assert len(final_event["report"]) > 100
