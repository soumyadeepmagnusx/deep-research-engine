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


def test_search_cache_mechanism():
    """Verify in-memory caching stores and retrieves queries without re-querying."""
    from core.search_tools import SearchCache
    cache = SearchCache(ttl_seconds=10)
    mock_data = [{"title": "Cached Paper", "snippet": "Test", "url": "https://example.com"}]
    
    # Initial miss
    assert cache.get("quantum computing") is None
    assert cache.misses == 1
    
    # Store and hit
    cache.set("quantum computing", mock_data)
    hit_data = cache.get("quantum computing")
    assert hit_data == mock_data
    assert cache.hits == 1
    
    # Verify stats calculation
    stats = cache.stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert "50.0%" in stats["hit_ratio"]


def test_critic_adversarial_debate_rounds():
    """Verify critic agent generates structured adversarial debate dialectic rounds."""
    llm = LLMClient(api_key=None)
    critic = CriticAgent(llm)
    mock_evidences = [
        {"title": "PQC Key Exchange", "snippet": "ML-KEM standardized by NIST.", "url": "https://nist.gov"}
    ]
    audit = critic.audit_evidence("Post-Quantum Cryptography", mock_evidences)
    assert "debate_rounds" in audit
    rounds = audit["debate_rounds"]
    assert len(rounds) >= 2
    assert "proponent_claim" in rounds[0]
    assert "skeptic_counter" in rounds[0]
    assert "verdict" in rounds[0]


def test_synthesizer_bibtex_generation():
    """Verify synthesizer agent formats valid BibTeX citation blocks."""
    llm = LLMClient(api_key=None)
    synthesizer = SynthesizerAgent(llm)
    mock_evidences = [
        {"title": "Quantum Resistance 2026", "url": "https://arxiv.org/abs/2601.12345", "snippet": "NIST post-quantum cryptographic standards."}
    ]
    bibtex = synthesizer.generate_bibtex("Quantum Resistance", mock_evidences)
    assert "@misc" in bibtex
    assert "Quantum Resistance 2026" in bibtex
    assert "arxiv.org" in bibtex

