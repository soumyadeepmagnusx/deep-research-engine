"""Automated Test Suite for DeepResearch Multi-Agent Engine.
"""

import pytest
from core.llm_client import LLMClient
from core.search_tools import (
    live_web_search,
    categorize_source_authority,
    compute_reading_metrics,
    deduplicate_evidence_claims
)
from core.session_store import SessionStore
from core.analysis_tools import extract_key_concepts, compute_lexical_diversity
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


def test_domain_authority_categorization():
    """Verify URL domain authority tag assignment."""
    assert categorize_source_authority("https://arxiv.org/abs/2401.0001") == "Peer-Reviewed / Academic"
    assert categorize_source_authority("https://csrc.nist.gov/publications") == "Standardization Body"
    assert categorize_source_authority("https://github.com/torvalds/linux") == "Open-Source / Reference"
    assert categorize_source_authority("https://unknown-domain-random-1234.org") == "Technical Publication"


def test_reading_metrics_computation():
    """Verify reading time and token metric calculations."""
    sample_text = "Word " * 450
    metrics = compute_reading_metrics(sample_text)
    assert metrics["word_count"] == 450
    assert metrics["est_reading_minutes"] == 2
    assert metrics["est_tokens"] > 500


def test_evidence_deduplication():
    """Verify that duplicate or near-identical evidence items are filtered."""
    raw_evidences = [
        {"title": "PQC Benchmark 2026", "snippet": "ML-KEM lattice key encapsulation benchmarking analysis and results."},
        {"title": "PQC Benchmark 2026", "snippet": "ML-KEM lattice key encapsulation benchmarking analysis and results."},
        {"title": "Decentralized Storage Protocols", "snippet": "Content addressing and IPFS distributed DHT DHT systems."}
    ]
    deduped = deduplicate_evidence_claims(raw_evidences, similarity_threshold=0.65)
    assert len(deduped) == 2
    assert deduped[0]["title"] == "PQC Benchmark 2026"
    assert deduped[1]["title"] == "Decentralized Storage Protocols"


def test_critic_executive_takeaways():
    """Verify critic extracts structured executive takeaways."""
    llm = LLMClient(api_key=None)
    critic = CriticAgent(llm)
    evidences = [
        {"title": "Test Title", "snippet": "Test snippet details."}
    ]
    audit = critic.audit_evidence("Post-Quantum Cryptography", evidences)
    assert "executive_takeaways" in audit
    takeaways = audit["executive_takeaways"]
    assert len(takeaways) >= 3
    assert any("Post-Quantum Cryptography" in t for t in takeaways)


def test_session_store_ring_buffer():
    """Verify session store maintains max entries and returns recent items in order."""
    store = SessionStore(max_entries=3)
    for i in range(5):
        store.record_session(
            topic=f"Topic {i}",
            domain="Computer Science",
            rigor_tone="Academic",
            confidence_score=85 + i,
            word_count=500 + i * 50,
            source_count=4
        )
    recent = store.get_recent_sessions(limit=10)
    assert len(recent) == 3
    assert recent[0]["topic"] == "Topic 4"
    assert recent[1]["topic"] == "Topic 3"
    assert recent[2]["topic"] == "Topic 2"


def test_extract_key_concepts():
    """Verify extraction of key concepts, acronyms, and compound terms."""
    sample_text = (
        "Post-Quantum Cryptography (PQC) and ML-KEM lattice key encapsulation "
        "provide quantum resilience. NIST standardization guidelines mandate PQC deployment."
    )
    concepts = extract_key_concepts(sample_text, top_n=5)
    assert len(concepts) > 0
    terms = [c["term"] for c in concepts]
    assert "PQC" in terms or "NIST" in terms or "ML-KEM" in terms
    assert all("relevance_score" in c for c in concepts)
    assert all("category" in c for c in concepts)


def test_compute_lexical_diversity():
    """Verify computation of vocabulary richness and lexical density."""
    sample_text = "Post-quantum algorithms replace classical RSA encryption across distributed financial ledgers."
    stats = compute_lexical_diversity(sample_text)
    assert stats["total_tokens"] > 0
    assert stats["unique_terms"] > 0
    assert 0.0 < stats["type_token_ratio"] <= 1.0
    assert stats["lexical_density_percent"] > 0.0


def test_synthesizer_taxonomy_indexing():
    """Verify synthesizer agent generates taxonomy markdown tables."""
    llm = LLMClient(api_key=None)
    synthesizer = SynthesizerAgent(llm)
    mock_concepts = [
        {"term": "ML-KEM", "category": "ACRONYM", "relevance_score": 95, "frequency": 4},
        {"term": "Lattice Cryptography", "category": "COMPOUND_TERM", "relevance_score": 88, "frequency": 3}
    ]
    table = synthesizer.generate_taxonomy_index(mock_concepts)
    assert "Technical Taxonomy" in table
    assert "ML-KEM" in table
    assert "ACRONYM" in table
    assert "95%" in table






