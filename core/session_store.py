"""Session Store:
In-memory ring buffer tracking active and completed multi-agent research sessions.
"""

import time
from typing import List, Dict, Any, Optional


class SessionStore:
    def __init__(self, max_entries: int = 25):
        self.max_entries = max_entries
        self._sessions: List[Dict[str, Any]] = []

    def record_session(
        self,
        topic: str,
        domain: str,
        rigor_tone: str,
        confidence_score: int,
        word_count: int,
        source_count: int,
        key_concepts: Optional[List[str]] = None,
        verification_score: Optional[int] = None,
        objectivity_index: Optional[int] = None,
        frontier_maturity: Optional[int] = None,
        decision_confidence: Optional[int] = None
    ) -> Dict[str, Any]:
        """Record completed research execution in the ring buffer."""
        entry = {
            "id": f"sess_{int(time.time() * 1000)}",
            "topic": topic,
            "domain": domain,
            "rigor_tone": rigor_tone,
            "confidence_score": confidence_score,
            "word_count": word_count,
            "source_count": source_count,
            "key_concepts": key_concepts or [],
            "verification_score": verification_score or confidence_score,
            "objectivity_index": objectivity_index if objectivity_index is not None else 90,
            "frontier_maturity": frontier_maturity if frontier_maturity is not None else 85,
            "decision_confidence": decision_confidence if decision_confidence is not None else 85,
            "timestamp": time.time()
        }
        self._sessions.insert(0, entry)
        if len(self._sessions) > self.max_entries:
            self._sessions.pop()
        return entry

    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return the most recent research executions."""
        return self._sessions[:limit]

    def clear(self) -> None:
        """Clear all recorded sessions."""
        self._sessions.clear()


GLOBAL_SESSION_STORE = SessionStore()
