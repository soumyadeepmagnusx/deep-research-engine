# 🧠 DeepResearch Swarm: Autonomous Multi-Agent Academic Research Engine

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-3776AB.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.142.2-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Pytest](https://img.shields.io/badge/Tests-7%20Passed%20(100%25)-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](tests/)
[![UI](https://img.shields.io/badge/Frontend-Ultra%20Level%20Canvas%20%2B%20WebAudio-9333EA.svg?style=flat)](templates/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](LICENSE)
[![Author](https://img.shields.io/badge/Author-Soumyadeep%20Ghosh-orange.svg?style=flat)](https://github.com/soumyadeepmagnusx)

> An end-to-end distributed multi-agent academic research swarm engineered in Python and FastAPI. The engine decomposes complex technical queries, crawls live web sources, cross-checks claims via a peer-review Critic Agent, and synthesizes publication-grade, citation-backed academic reports in real time with an interactive particle canvas, synthetic Web Audio feedback, and speech readout.

---

## 🌟 Ultra-Level Features & Engineering Highlights

Unlike basic single-prompt chatbots, **DeepResearch Swarm** is built with modular agent abstraction and real-time streaming architectures:

- **🎯 Strategist Agent (Planner)**: Decomposes open-ended topics into 2, 4, or 6 orthogonal investigation vectors based on configured depth (Architecture, Benchmarks, Vulnerabilities, Future Roadmap).
- **🔍 Crawler Agent (Researcher)**: Crawls live web search results, parses DOM structures, and sanitizes unstructured text nodes.
- **⚖️ Skeptic Agent (Critic / Fact-Checker)**: Evaluates gathered evidence for credibility, cross-examines conflicting technical claims, and computes an objective **Fact-Check Confidence Score (0-100%)**.
- **📝 Synthesizer Agent**: Authors publication papers with inline citations `[1]`, `[2]`, comparative tables, and generates formal **BibTeX records (`.bib`)**.
- **🌌 Interactive Dynamic Topology Particle Graph**: Custom HTML5 Canvas rendering draggable nodes with real-time particle laser beams connecting topic roots, vectors, and crawled sources.
- **🔊 Web Audio API Synthesizer**: Native in-browser synthesized acoustic micro-feedback (frequency-modulated clicks, status pulses, and completion chord chimes — zero MP3 assets needed!).
- **🎙️ Web Speech API Synthetic Readout**: One-click audio player reading the Executive Summary aloud using browser speech synthesis.
- **🎛️ Multi-Rigor Tone Selector**:
  - 🎓 *IEEE/ACM Peer-Reviewed Academic Paper*
  - 💼 *C-Suite Strategic Executive Whitepaper*
  - 🛡️ *Red-Team Adversarial Security Audit*
- **📑 Multi-Format Academic Export Suite**: One-click export to Markdown (`.md`), formatted print-ready HTML (`.html`) for PDF generation, BibTeX citations (`.bib`), or clipboard copy.
- **🔍 Slide-Out Evidence Inspector Drawer**: Click any node or citation to inspect raw extracted text, source URL, and credibility rating.
- **🛡️ Zero-Fail Resilience**: Operates out-of-the-box with or without an active API key through deterministic heuristic modeling.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    User([User Investigation Query]) --> WebUI[Ultra-Level Glassmorphic Dashboard]
    WebUI --> Canvas[🌌 Interactive Particle Topology Graph]
    WebUI --> API[FastAPI Orchestrator / SSE Stream]
    
    subgraph Multi-Agent Swarm
        API --> Planner[🎯 Strategist Agent]
        Planner -->|N Investigation Vectors| Researcher[🔍 Crawler Agent]
        Researcher -->|Web Crawl & Extract| Evidence[(Sanitized Evidence Nodes)]
        Evidence --> Critic[⚖️ Skeptic / Critic Agent]
        Critic -->|Confidence Audit & Bias Check| Synthesizer[📝 Synthesizer Agent]
    end
    
    Synthesizer --> Report[📄 Cited Academic Paper & BibTeX]
    Report --> WebUI
    Evidence --> Canvas
```

---

## 📂 Project Structure

```text
deep-research-engine/
├── .github/
│   └── workflows/
│       └── ci.yml             # Automated CI pipeline running pytest on PRs
├── agents/
│   ├── __init__.py
│   ├── planner.py             # Formulates search queries & research angles
│   ├── researcher.py          # Web search executor & DOM content extractor
│   ├── critic.py              # Fact-checking auditor & confidence scorer
│   ├── synthesizer.py         # Academic paper synthesis & BibTeX generator
│   └── orchestrator.py        # Coordinates agent lifecycle with SSE event streaming
├── core/
│   ├── __init__.py
│   ├── llm_client.py          # LLM client interface with heuristic fallback
│   └── search_tools.py        # Live web crawling & extraction utilities
├── templates/
│   └── index.html             # Ultra-level glassmorphic UI with particle canvas & WebAudio
├── tests/
│   ├── test_agents.py         # Agent pipeline unit tests
│   └── test_api.py            # API endpoint integration tests
├── app.py                     # FastAPI application entrypoint
├── requirements.txt           # Production dependencies
├── LICENSE                    # MIT License
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/soumyadeepmagnusx/deep-research-engine.git
cd deep-research-engine

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

```bash
# Windows PowerShell:
$env:GEMINI_API_KEY="your-api-key"

# Linux / macOS:
export GEMINI_API_KEY="your-api-key"
```
*(If no key is configured, the system gracefully runs in heuristic simulation mode for offline demonstration).*

### 3. Launch the Server

```bash
python app.py
```
Open your browser at **`http://localhost:8000`** to experience the dashboard!

### 4. Run Automated Test Suite

```bash
python -m pytest tests/ -v
```

---

## 🌐 Free Cloud Deployment

### Option A: Deploy on Render (Recommended)
1. Sign in to [Render](https://render.com) with GitHub.
2. Click **New Web Service** and select `soumyadeepmagnusx/deep-research-engine`.
3. Configure:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Click **Deploy Web Service** — you get a public live URL to showcase on your resume and LinkedIn!

### Option B: Deploy on Railway
1. Sign in to [Railway](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Railway automatically recognizes the FastAPI server and provisions a live URL.

---

## 👨‍💻 Author

**Soumyadeep Ghosh** ([@soumyadeepmagnusx](https://github.com/soumyadeepmagnusx))  
*Department of Computer Science & Engineering*  
*Brainware University, Kolkata, India*  
Focus: Distributed Systems, Autonomous Agent Architecture, Low-Latency Full-Stack Engineering.

---

## 📜 License
Released under the [MIT License](LICENSE).
