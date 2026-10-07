"""DeepResearch Engine: FastAPI Application Server
Provides REST endpoints and Server-Sent Events (SSE) for streaming multi-agent execution.
"""

import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from agents.orchestrator import ResearchOrchestrator

app = FastAPI(
    title="DeepResearch Engine",
    description="Automated Multi-Agent Deep Research & Fact-Checked Report Generator",
    version="1.0.0"
)

# Enable CORS for local testing & cloud deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATES_DIR = Path(__file__).parent / "templates"


class ResearchRequest(BaseModel):
    topic: str
    depth: Optional[int] = 4
    domain: Optional[str] = "General"
    api_key: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Template not found")
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "DeepResearch Multi-Agent Engine", "version": "1.0.0"}


@app.post("/api/research/stream")
async def stream_research(req: ResearchRequest):
    """Stream research pipeline events over Server-Sent Events (SSE)."""
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic must not be empty.")

    orchestrator = ResearchOrchestrator(api_key=req.api_key)

    def event_generator():
        for event in orchestrator.run_stream(req.topic, depth=req.depth or 4, domain=req.domain or "General"):
            payload = json.dumps(event)
            yield f"data: {payload}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("DeepResearch Engine running on: http://localhost:8000")
    print("=" * 60)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
