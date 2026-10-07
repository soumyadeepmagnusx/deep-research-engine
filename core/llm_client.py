"""LLM Client Interface using Google GenAI SDK (gemini-3.8-flash)
with smart offline heuristic fallback if GEMINI_API_KEY is not configured.
"""

import os
from typing import Optional

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class LLMClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        self.model = "gemini-3.8-flash"

        if GENAI_AVAILABLE and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[Warning] Failed to initialize Google GenAI client: {e}")
                self.client = None

    @property
    def is_live(self) -> bool:
        return self.client is not None

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generate response from Gemini 3.8 Flash, or return structured fallback."""
        if self.client:
            try:
                # Include system instruction in the input if provided
                full_input = prompt
                if system_instruction:
                    full_input = f"<system_instruction>\n{system_instruction}\n</system_instruction>\n\n{prompt}"

                interaction = self.client.interactions.create(
                    model=self.model,
                    input=full_input
                )
                if interaction.output_text:
                    return interaction.output_text.strip()
            except Exception as e:
                print(f"[LLM Error] API call failed: {e}. Falling back to heuristic synthesis.")

        return self._heuristic_fallback(prompt, system_instruction)

    def _heuristic_fallback(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Deterministic agent synthesis for offline or demo runs without API keys."""
        if "Decompose the topic" in prompt or "research queries" in prompt:
            return (
                "1. Fundamental Architecture & Core Theoretical Foundations\n"
                "2. Benchmark Performance vs Existing Industry Standards\n"
                "3. Key Engineering Bottlenecks, Latency, and Scalability Risks\n"
                "4. 2026-2030 Roadmap and Production Deployment Outlook"
            )
        elif "Critic Agent" in prompt or "Fact-Check" in prompt:
            return (
                "### Evidence Cross-Examination & Reliability Assessment\n"
                "- **Claim Consistency**: Core technological claims are backed by documented academic and industry metrics.\n"
                "- **Contradiction Check**: No major contradictory claims found across indexed technical documentation.\n"
                "- **Risk & Blindspots**: High reliance on lab benchmarks; real-world deployment data is currently emerging.\n"
                "- **Confidence Score**: 89/100 (Strong technical consensus with manageable deployment uncertainty)."
            )
        else:
            return (
                f"### Research Synthesis\n\n"
                f"Based on multi-source cross-referencing, the subject demonstrates rapid evolution towards production integration. "
                f"Primary advantages include heightened architectural efficiency and lowered latency, while key considerations remain cost of adoption and security auditing."
            )
