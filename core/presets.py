"""Curated Research Presets:
Provides pre-configured investigation templates across systems, security, and distributed computing.
"""

from typing import List, Dict, Any, Optional

RESEARCH_PRESETS: List[Dict[str, Any]] = [
    {
        "id": "pqc-migration",
        "title": "Post-Quantum Cryptography: Migration Bottlenecks for Financial Infrastructure by 2030",
        "domain": "Cybersecurity & Cryptography",
        "depth": 4,
        "rigor_tone": "Academic",
        "badge": "PQC",
        "icon": "fa-shield-halved"
    },
    {
        "id": "zk-rollups",
        "title": "Zero-Knowledge STARKs vs SNARKs: Prover Overhead & Tail Latency in L2 Rollups",
        "domain": "Distributed Systems & Cloud",
        "depth": 4,
        "rigor_tone": "Academic",
        "badge": "ZK-Proofs",
        "icon": "fa-cube"
    },
    {
        "id": "distributed-consensus",
        "title": "Byzantine Fault Tolerance Under Asynchronous Network Partitions: Paxos vs Raft Tradeoffs",
        "domain": "Computer Systems & Architecture",
        "depth": 4,
        "rigor_tone": "Academic",
        "badge": "Consensus",
        "icon": "fa-network-wired"
    },
    {
        "id": "llm-inference",
        "title": "Speculative Decoding and PagedAttention: Memory Bandwidth Saturation in Multi-GPU Inference",
        "domain": "Artificial Intelligence & Agents",
        "depth": 4,
        "rigor_tone": "Executive",
        "badge": "Inference",
        "icon": "fa-microchip"
    }
]


def get_all_presets() -> List[Dict[str, Any]]:
    """Return all available research presets."""
    return RESEARCH_PRESETS


def get_preset_by_id(preset_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single preset by unique identifier."""
    for p in RESEARCH_PRESETS:
        if p["id"] == preset_id:
            return p
    return None

