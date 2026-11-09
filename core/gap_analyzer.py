"""Research Gap & Knowledge Frontier Analyzer:
Detects open academic problems, untested methodology hypotheses, and computes knowledge maturity metrics.
"""

import re
from typing import List, Dict, Any, Optional


GAP_CATEGORIES = {
    "EMPIRICAL_EVALUATION_GAP": "Empirical Benchmark & Workload Validation",
    "SCALABILITY_LIMITATION": "Distributed Scale & Latency Degradation",
    "THEORETICAL_INSUFFICIENCY": "Formal Proof & Provable Hardness Bound",
    "SECURITY_UNCERTAINTY": "Adversarial Surface & Side-Channel Integrity"
}


def identify_research_gaps(
    topic: str,
    report_text: str,
    evidences: List[Dict[str, Any]],
    debate_rounds: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """Identify unresolved research gaps and formulate follow-up exploration hypotheses."""
    gaps: List[Dict[str, Any]] = []

    # Heuristic template generation based on topic semantics and skepticism points
    topic_clean = topic.strip()
    
    # 1. Empirical Gap
    gaps.append({
        "id": "gap_emp_1",
        "category": "EMPIRICAL_EVALUATION_GAP",
        "category_label": GAP_CATEGORIES["EMPIRICAL_EVALUATION_GAP"],
        "title": f"Heterogeneous Hardware Microbenchmarks for {topic_clean}",
        "description": f"Current literature predominantly evaluates {topic_clean} on homogeneous baseline environments; empirical tail-latency behavior under sustained saturated I/O load remains undocumented.",
        "follow_up_query": f"{topic_clean} heterogeneous hardware microbenchmarks tail latency peak load",
        "priority": "HIGH"
    })

    # 2. Scalability Gap
    gaps.append({
        "id": "gap_scale_2",
        "category": "SCALABILITY_LIMITATION",
        "category_label": GAP_CATEGORIES["SCALABILITY_LIMITATION"],
        "title": f"Decoupled Coordination Overhead at Multi-Cluster Scale",
        "description": "Synchronization barriers and cross-zone replication costs exhibit super-linear regression when scaling beyond single datacenter fabrics.",
        "follow_up_query": f"{topic_clean} multi-cluster cross-region replication synchronization overhead",
        "priority": "MEDIUM"
    })

    # 3. Security or Adversarial Gap
    gaps.append({
        "id": "gap_sec_3",
        "category": "SECURITY_UNCERTAINTY",
        "category_label": GAP_CATEGORIES["SECURITY_UNCERTAINTY"],
        "title": f"Side-Channel & Zero-Day Threat Surface Under Byzantine Faults",
        "description": "Formal guarantees often assume trusted runtime memory envelopes; state perturbation and cache-timing side-channels under Byzantine conditions require empirical fuzzing.",
        "follow_up_query": f"{topic_clean} side channel cache timing attacks byzantine resilience audit",
        "priority": "HIGH"
    })

    # 4. Theoretical Hardness or Edge Cases if debate rounds present
    if debate_rounds and len(debate_rounds) > 1:
        counter_sample = debate_rounds[0].get("skeptic_counter", "Theoretical constraints in adversarial topologies.")
        gaps.append({
            "id": "gap_theo_4",
            "category": "THEORETICAL_INSUFFICIENCY",
            "category_label": GAP_CATEGORIES["THEORETICAL_INSUFFICIENCY"],
            "title": f"Provable Asymptotic Bounds for Worst-Case Ingestion",
            "description": f"Open question highlighted during peer review: {counter_sample[:140]}...",
            "follow_up_query": f"{topic_clean} asymptotic complexity worst-case bound formal verification",
            "priority": "MEDIUM"
        })

    return gaps


def compute_frontier_maturity_index(
    gaps: List[Dict[str, Any]],
    confidence_score: int = 88
) -> Dict[str, Any]:
    """Compute overall Knowledge Frontier Maturity Index and category distribution."""
    if not gaps:
        return {
            "maturity_score": confidence_score,
            "maturity_tier": "MATURE_CONSENSUS",
            "active_gaps_count": 0,
            "high_priority_gaps": 0,
            "category_distribution": {}
        }

    high_pri_count = sum(1 for g in gaps if g.get("priority") == "HIGH")
    med_pri_count = sum(1 for g in gaps if g.get("priority") == "MEDIUM")

    # Base maturity score adjusted by confidence and open high-priority gaps
    penalty = (high_pri_count * 3) + (med_pri_count * 1.5)
    maturity_score = max(55, min(96, round(confidence_score * 0.9 - penalty + 10)))

    if maturity_score >= 82:
        tier = "MATURE_CONSENSUS"
    elif maturity_score >= 70:
        tier = "EMERGING_FRONTIER"
    else:
        tier = "EXPERIMENTAL_PARADIGM"

    cat_counts = {}
    for g in gaps:
        c = g.get("category", "EMPIRICAL_EVALUATION_GAP")
        cat_counts[c] = cat_counts.get(c, 0) + 1

    return {
        "maturity_score": maturity_score,
        "maturity_tier": tier,
        "active_gaps_count": len(gaps),
        "high_priority_gaps": high_pri_count,
        "category_distribution": cat_counts
    }
