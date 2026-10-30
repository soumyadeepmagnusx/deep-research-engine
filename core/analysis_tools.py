"""Analysis Tools:
Technical entity frequency analyzer, key concept extraction, and lexical diversity metrics.
"""

import re
from collections import Counter
from typing import List, Dict, Any

# Technical stopwords to filter out common noise
_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "else", "when", "at", "from",
    "by", "for", "with", "about", "against", "between", "into", "through", "during",
    "before", "after", "above", "below", "to", "of", "in", "on", "over", "under",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do",
    "does", "did", "can", "could", "shall", "should", "will", "would", "may", "might",
    "must", "such", "no", "not", "only", "own", "same", "so", "than", "too", "very",
    "just", "where", "how", "all", "any", "both", "each", "few", "more", "most", "other",
    "some", "this", "that", "these", "those", "what", "which", "who", "whom", "their",
    "theirs", "themselves", "we", "our", "ours", "us", "it", "its", "system", "systems",
    "research", "paper", "study", "analysis", "results", "based", "using", "approach"
}


def extract_key_concepts(text: str, top_n: int = 8) -> List[Dict[str, Any]]:
    """Extract prominent technical entities, acronyms, and compound key phrases from text."""
    if not text:
        return []

    # 1. Identify Acronyms (2 to 6 uppercase letters, optionally with dashes or numbers)
    acronym_matches = re.findall(r"\b[A-Z0-9]{2,6}(?:-[A-Z0-9]{2,6})*\b", text)
    acronym_counts = Counter(acronym_matches)

    # 2. Extract 2-word and 3-word technical n-grams
    words = [re.sub(r"[^\w-]", "", w.lower()) for w in text.split()]
    words = [w for w in words if len(w) > 2 and w not in _STOPWORDS]

    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)
               if words[i] not in _STOPWORDS and words[i+1] not in _STOPWORDS]
    
    ngram_counts = Counter(bigrams)
    word_counts = Counter(words)

    scored_concepts: Dict[str, Dict[str, Any]] = {}

    # Weight acronyms highly
    for acr, count in acronym_counts.items():
        if acr.upper() not in {"THE", "AND", "FOR", "NOT", "ALL"}:
            scored_concepts[acr] = {
                "term": acr,
                "frequency": count,
                "category": "ACRONYM",
                "relevance_score": min(99, 70 + count * 5)
            }

    # Add significant bigrams
    for bg, count in ngram_counts.most_common(top_n * 2):
        if count >= 1 and bg not in scored_concepts:
            scored_concepts[bg.title()] = {
                "term": bg.title(),
                "frequency": count,
                "category": "COMPOUND_TERM",
                "relevance_score": min(95, 60 + count * 6)
            }

    # Add dominant unigrams if needed
    for w, count in word_counts.most_common(top_n):
        cap_term = w.capitalize()
        if cap_term not in scored_concepts and not any(cap_term.lower() in k.lower() for k in scored_concepts):
            scored_concepts[cap_term] = {
                "term": cap_term,
                "frequency": count,
                "category": "KEY_CONCEPT",
                "relevance_score": min(90, 50 + count * 4)
            }

    sorted_concepts = sorted(
        scored_concepts.values(),
        key=lambda x: (x["relevance_score"], x["frequency"]),
        reverse=True
    )

    return sorted_concepts[:top_n]


def compute_lexical_diversity(text: str) -> Dict[str, Any]:
    """Compute vocabulary richness, lexical diversity, and readability stats."""
    raw_words = re.findall(r"\b\w+\b", text)
    total_tokens = len(raw_words)
    if total_tokens == 0:
        return {
            "total_tokens": 0,
            "unique_terms": 0,
            "type_token_ratio": 0.0,
            "lexical_density_percent": 0.0
        }

    lower_tokens = [w.lower() for w in raw_words]
    unique_tokens = len(set(lower_tokens))
    content_tokens = [w for w in lower_tokens if w not in _STOPWORDS]

    ttr = round(unique_tokens / total_tokens, 3)
    density = round((len(content_tokens) / total_tokens) * 100, 1)

    return {
        "total_tokens": total_tokens,
        "unique_terms": unique_tokens,
        "type_token_ratio": ttr,
        "lexical_density_percent": density
    }
