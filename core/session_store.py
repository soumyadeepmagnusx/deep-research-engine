"""Session Store:
In-memory ring buffer tracking active and completed multi-agent research sessions.
"""

import time
from typing import List, Dict, Any


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
        source_count: int
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
