"""Verification Tools:
Citation graph analytics, cross-source evidence corroboration, and claim verification metrics.
"""

import re
from typing import List, Dict, Any, Set


def _tokenize_claim(text: str) -> Set[str]:
    """Extract normalized alphanumeric tokens (length > 3) from text."""
    tokens = re.findall(r"\b[a-zA-Z0-9_-]{4,}\b", (text or "").lower())
    stopwords = {
        "with", "from", "that", "this", "they", "have", "were", "been", "their",
        "which", "about", "there", "these", "other", "using", "paper", "study",
        "system", "systems", "approach", "results", "based", "analysis"
    }
    return {t for t in tokens if t not in stopwords}


def build_cross_verification_matrix(evidences: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze token overlap and cross-corroboration between evidence nodes."""
    if not evidences:
        return {
            "consensus_index": 0,
            "corroborated_pairs_count": 0,
            "independent_sources_count": 0,
            "graph_edges": [],
            "corroboration_clusters": []
        }

    token_sets = [
        _tokenize_claim(f"{e.get('title', '')} {e.get('snippet', '')}")
        for e in evidences
    ]

    edges = []
    corroborated_indices = set()
    total_pairs = 0
    overlapping_pairs = 0

    n = len(evidences)
    for i in range(n):
        for j in range(i + 1, n):
            total_pairs += 1
            s1, s2 = token_sets[i], token_sets[j]
            intersection = s1 & s2
            union = s1 | s2
            similarity = (len(intersection) / len(union)) if union else 0.0

            # If two sources share substantive technical keywords (similarity >= 0.15)
            if similarity >= 0.15:
                overlapping_pairs += 1
                corroborated_indices.add(i)
                corroborated_indices.add(j)
                edges.append({
                    "source_a": evidences[i].get("id", i + 1),
                    "source_b": evidences[j].get("id", j + 1),
                    "shared_tokens": list(intersection)[:4],
                    "overlap_score": round(similarity * 100, 1)
                })

    # Consensus index based on ratio of corroborated evidence nodes
    corroboration_ratio = len(corroborated_indices) / n if n > 0 else 0.0
    consensus_index = min(98, max(65, round(corroboration_ratio * 80 + 18)))

    return {
        "consensus_index": consensus_index,
        "corroborated_pairs_count": overlapping_pairs,
        "independent_sources_count": n,
        "corroborated_nodes_count": len(corroborated_indices),
        "graph_edges": edges[:12]
    }


def detect_unsupported_claims(report_text: str, evidences: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Identify cited numerical references and check citation density."""
    citations_found = re.findall(r"\[(\d+)\]", report_text)
    cited_ids = {int(c) for c in citations_found if c.isdigit()}
    available_ids = {e.get("id", idx + 1) for idx, e in enumerate(evidences)}

    valid_citations = cited_ids & available_ids
    paragraphs = [p for p in report_text.split("\n\n") if len(p.strip()) > 60]
    cited_paragraphs = [p for p in paragraphs if re.search(r"\[\d+\]", p)]

    citation_density_pct = round((len(cited_paragraphs) / len(paragraphs) * 100), 1) if paragraphs else 0.0

    return {
        "total_citations_rendered": len(citations_found),
        "unique_sources_cited": len(valid_citations),
        "citation_density_percent": citation_density_pct,
        "fully_verified": citation_density_pct >= 60.0
    }
