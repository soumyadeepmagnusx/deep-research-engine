"""DeepResearch Swarm: FastAPI Application Server
Provides REST endpoints and Server-Sent Events (SSE) for streaming multi-agent execution.
"""

import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from agents.orchestrator import ResearchOrchestrator
from core.search_tools import get_search_cache_stats
from core.session_store import GLOBAL_SESSION_STORE

app = FastAPI(
    title="DeepResearch Swarm",
    description="Autonomous Multi-Agent Academic Research & Fact-Checked Paper Synthesis Engine",
    version="1.3.0"
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
    rigor_tone: Optional[str] = "Academic"
    api_key: Optional[str] = None


class ExportRequest(BaseModel):
    topic: str
    content: str
    export_format: str = "markdown"  # "markdown", "bibtex", or "json"



@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Template not found")
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "DeepResearch Multi-Agent Swarm",
        "version": "1.3.0"
    }


@app.get("/api/metrics")
async def get_metrics():
    """Retrieve runtime swarm telemetry and cache statistics."""
    return {
        "status": "active",
        "version": "1.3.0",
        "cache": get_search_cache_stats(),
        "runtime": "FastAPI + Multi-Agent Swarm"
    }


@app.get("/api/sessions")
async def get_sessions(limit: int = 10):
    """Retrieve recent research execution history."""
    return {
        "sessions": GLOBAL_SESSION_STORE.get_recent_sessions(limit=limit),
        "total_recorded": len(GLOBAL_SESSION_STORE.get_recent_sessions(limit=50))
    }


@app.post("/api/research/export")
async def export_research_document(req: ExportRequest):
    """Generate and stream formatted research artifact files for download."""
    sanitized = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in req.topic.strip())[:40] or "research_paper"
    
    if req.export_format == "bibtex":
        media_type = "application/x-bibtex"
        filename = f"{sanitized}.bib"
    elif req.export_format == "json":
        media_type = "application/json"
        filename = f"{sanitized}.json"
    else:
        media_type = "text/markdown; charset=utf-8"
        filename = f"{sanitized}.md"

    return Response(
        content=req.content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@app.post("/api/research/stream")
async def stream_research(req: ResearchRequest):
    """Stream research pipeline events over Server-Sent Events (SSE)."""
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic must not be empty.")

    orchestrator = ResearchOrchestrator(api_key=req.api_key)

    def event_generator():
        for event in orchestrator.run_stream(
            topic=req.topic,
            depth=req.depth or 4,
            domain=req.domain or "General",
            rigor_tone=req.rigor_tone or "Academic"
        ):
            if event.get("stage") == "completed":
                report_text = event.get("report", "")
                word_count = len(report_text.split())
                top_terms = [c["term"] for c in event.get("key_concepts", [])[:5]]
                GLOBAL_SESSION_STORE.record_session(
                    topic=req.topic,
                    domain=req.domain or "General",
                    rigor_tone=req.rigor_tone or "Academic",
                    confidence_score=event.get("confidence_score", 90),
                    word_count=word_count,
                    source_count=event.get("source_count", 0),
                    key_concepts=top_terms
                )
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
    print("DeepResearch Swarm running on: http://localhost:8000")
    print("=" * 60)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
