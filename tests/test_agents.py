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
from core.verification_tools import build_cross_verification_matrix, detect_unsupported_claims
from core.export_tools import generate_standalone_html_publication, markdown_to_clean_html
from core.bias_detector import analyze_source_stance, compute_corpus_bias_distribution
from core.gap_analyzer import identify_research_gaps, compute_frontier_maturity_index
from core.tradeoff_evaluator import extract_tradeoff_matrix, compute_pareto_balance_score
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


def test_cross_verification_matrix():
    """Verify evidence cross-corroboration matrix and consensus index."""
    mock_evidences = [
        {"id": 1, "title": "NIST PQC Standards", "snippet": "ML-KEM lattice key exchange standardization by NIST."},
        {"id": 2, "title": "Post-Quantum Migration", "snippet": "Migration to ML-KEM lattice cryptography in financial protocols."},
        {"id": 3, "title": "Zero-Knowledge Rollups", "snippet": "Ethereum layer-2 state scaling via STARK proofs."}
    ]
    matrix = build_cross_verification_matrix(mock_evidences)
    assert matrix["independent_sources_count"] == 3
    assert matrix["corroborated_pairs_count"] >= 1
    assert 50 <= matrix["consensus_index"] <= 100
    assert len(matrix["graph_edges"]) >= 1


def test_detect_unsupported_claims():
    """Verify citation density and claim verification detection."""
    report = (
        "Post-Quantum Cryptography represents a critical security shift [1].\n\n"
        "Lattice-based key exchange ensures quantum immunity [2].\n\n"
        "Uncited speculative assertion without formal benchmarks."
    )
    evidences = [{"id": 1}, {"id": 2}]
    stats = detect_unsupported_claims(report, evidences)
    assert stats["total_citations_rendered"] == 2
    assert stats["unique_sources_cited"] == 2
    assert stats["citation_density_percent"] > 50.0


def test_critic_verification_matrix_integration():
    """Verify critic agent incorporates cross-verification matrix in audit."""
    llm = LLMClient(api_key=None)
    critic = CriticAgent(llm)
    evidences = [
        {"id": 1, "title": "PQC Key Encapsulation", "snippet": "ML-KEM lattice cryptography."},
        {"id": 2, "title": "NIST Standards 2026", "snippet": "Standardization of ML-KEM post-quantum cryptography."}
    ]
    audit = critic.audit_evidence("Post-Quantum Cryptography", evidences)
    assert "verification_matrix" in audit
    v_matrix = audit["verification_matrix"]
    assert "consensus_index" in v_matrix
    assert "corroborated_pairs_count" in v_matrix
    assert 50 <= audit["confidence_score"] <= 100


def test_export_tools_formatting_pipeline():
    """Verify HTML publication generator formats codeblocks, headers, and metadata."""
    md = "# Title\n\nSome text with `inline code`.\n\n```python\nprint('hello')\n```\n\n- Item 1\n- Item 2"
    clean_html = markdown_to_clean_html(md)
    assert "<h1>Title</h1>" in clean_html
    assert "<code>inline code</code>" in clean_html
    assert "<pre><code>" in clean_html
    assert "<ul>" in clean_html

    doc = generate_standalone_html_publication("Distributed Consensus Benchmarks", md)
    assert "<!DOCTYPE html>" in doc
    assert "Distributed Consensus Benchmarks" in doc
    assert "Soumyadeep Ghosh" in doc


def test_analyze_source_stance():
    """Verify classification of epistemic research stance."""
    emp_text = "Microbenchmarks show 35% throughput speedup and 12ms latency reduction on GPU clusters."
    emp_res = analyze_source_stance(emp_text)
    assert emp_res["primary_stance"] == "EMPIRICAL_BENCHMARK"
    assert emp_res["empirical_score"] > 0
    assert emp_res["objectivity_ratio"] >= 80.0

    crit_text = "Severe side-channel leakage vulnerability and latency bottleneck detected under peak load."
    crit_res = analyze_source_stance(crit_text)
    assert crit_res["primary_stance"] == "CRITICAL_SKEPTICISM"
    assert crit_res["critical_score"] > 0


def test_compute_corpus_bias_distribution():
    """Verify corpus-wide stance distribution and objectivity index computation."""
    evidences = [
        {"title": "PQC Benchmark", "snippet": "Measured throughput and latency microbenchmark dataset."},
        {"title": "Theoretical Hardness", "snippet": "Mathematical proof and complexity bound reductions."},
        {"title": "Security Vulnerability", "snippet": "Timing attack hazard and side-channel constraints."}
    ]
    dist = compute_corpus_bias_distribution(evidences)
    assert "objectivity_index" in dist
    assert "stance_distribution" in dist
    assert 50 <= dist["objectivity_index"] <= 100
    assert "EMPIRICAL_BENCHMARK" in dist["stance_distribution"]
    assert all("stance" in ev for ev in evidences)


def test_critic_bias_and_objectivity_integration():
    """Verify critic agent calculates and exposes bias analytics and objectivity index."""
    llm = LLMClient(api_key=None)
    critic = CriticAgent(llm)
    evidences = [
        {"title": "Empirical Benchmarking", "snippet": "Latency and throughput evaluated across GPU clusters.", "url": "https://arxiv.org"},
        {"title": "Formal Hardness Reduction", "snippet": "Theorem lemma proof and complexity bound.", "url": "https://iacr.org"}
    ]
    audit = critic.audit_evidence("Post-Quantum Key Exchange", evidences)
    assert "bias_analytics" in audit
    assert "objectivity_index" in audit
    assert 50 <= audit["objectivity_index"] <= 100
    assert "stance_distribution" in audit["bias_analytics"]


def test_identify_research_gaps():
    """Verify gap analyzer extracts structured open questions and follow-up queries."""
    topic = "Post-Quantum Cryptographic Migration"
    report = "Formal analysis of lattice-based schemes. Empirical overhead remains untested."
    evidences = [{"title": "PQC Benchmark", "snippet": "Latency baseline results."}]
    debates = [{"round": 1, "skeptic_counter": "Tail latency degrades under peak network contention."}]
    
    gaps = identify_research_gaps(topic, report, evidences, debates)
    assert len(gaps) >= 3
    assert any(g["category"] == "EMPIRICAL_EVALUATION_GAP" for g in gaps)
    assert any(g["category"] == "SECURITY_UNCERTAINTY" for g in gaps)
    assert all("follow_up_query" in g and "priority" in g for g in gaps)


def test_frontier_maturity_index():
    """Verify computation of frontier maturity score and priority breakdown."""
    mock_gaps = [
        {"id": "g1", "category": "EMPIRICAL_EVALUATION_GAP", "priority": "HIGH"},
        {"id": "g2", "category": "SCALABILITY_LIMITATION", "priority": "MEDIUM"}
    ]
    res = compute_frontier_maturity_index(mock_gaps, confidence_score=85)
    assert "maturity_score" in res
    assert 50 <= res["maturity_score"] <= 100
    assert res["active_gaps_count"] == 2
    assert res["high_priority_gaps"] == 1
    assert res["maturity_tier"] in ["MATURE_CONSENSUS", "EMERGING_FRONTIER", "EXPERIMENTAL_PARADIGM"]


def test_orchestrator_research_gaps_integration():
    """Verify orchestrator stream attaches research_gaps and frontier_maturity to completed payload."""
    orchestrator = ResearchOrchestrator(api_key=None)
    completed_event = None
    for event in orchestrator.run_stream("Fault-Tolerant Distributed Storage", depth=2):
        if event.get("stage") == "completed":
            completed_event = event
            break

    assert completed_event is not None
    assert "research_gaps" in completed_event
    assert "frontier_maturity" in completed_event
    assert len(completed_event["research_gaps"]) >= 3
    assert 50 <= completed_event["frontier_maturity"]["maturity_score"] <= 100


def test_extract_tradeoff_matrix():
    """Verify tradeoff matrix extraction across architectural dimensions."""
    topic = "Rust vs C++ Ultra-Low Latency Trading"
    report = "Microbenchmarks show low execution latency with strict memory safety guarantees."
    evidences = [{"title": "Memory Benchmark", "snippet": "Low RSS footprint."}]
    matrix = extract_tradeoff_matrix(topic, report, evidences)

    assert "decision_confidence" in matrix
    assert "pareto_frontier" in matrix
    assert "dimensions" in matrix
    assert len(matrix["dimensions"]) == 5
    assert 50 <= matrix["decision_confidence"] <= 100
    assert matrix["pareto_frontier"] in ["PARETO_OPTIMAL", "BALANCED_TRADEOFF", "SPECIALIZED_NICHE"]
    assert any("Latency" in d["dimension"] for d in matrix["dimensions"])


def test_compute_pareto_balance_score():
    """Verify Pareto score aggregation with penalty on dimensional bottlenecks."""
    balanced_dims = [
        {"dimension": "D1", "score": 85},
        {"dimension": "D2", "score": 88},
        {"dimension": "D3", "score": 80}
    ]
    score1 = compute_pareto_balance_score(balanced_dims)
    assert 80 <= score1 <= 90

    bottleneck_dims = [
        {"dimension": "D1", "score": 85},
        {"dimension": "D2", "score": 55}  # severe bottleneck
    ]
    score2 = compute_pareto_balance_score(bottleneck_dims)
    assert score2 < score1


def test_critic_tradeoff_integration():
    """Verify critic agent evaluates architectural tradeoffs and computes decision confidence."""
    llm = LLMClient(api_key=None)
    critic = CriticAgent(llm)
    evidences = [
        {"title": "Lattice PQC Benchmark", "snippet": "Execution latency evaluated against classical ECC.", "url": "https://nist.gov"}
    ]
    audit = critic.audit_evidence("Lattice Post-Quantum Cryptography", evidences)
    assert "tradeoff_matrix" in audit
    assert "decision_confidence" in audit
    assert len(audit["tradeoff_matrix"]["dimensions"]) >= 4
    assert 50 <= audit["decision_confidence"] <= 100















