"""API and Route Configuration Tests for DeepResearch Engine."""

from app import app
from core.presets import get_all_presets, get_preset_by_id
from core.export_tools import generate_standalone_html_publication, markdown_to_clean_html


def test_app_configuration():
    assert app.title == "DeepResearch Swarm"
    routes = [r.path for r in app.routes]
    assert "/api/health" in routes
    assert "/api/metrics" in routes
    assert "/api/sessions" in routes
    assert "/api/presets" in routes
    assert "/api/presets/{preset_id}" in routes
    assert "/api/research/stream" in routes
    assert "/api/research/export" in routes


def test_presets_catalog():
    presets = get_all_presets()
    assert len(presets) >= 4
    first_id = presets[0]["id"]
    preset = get_preset_by_id(first_id)
    assert preset is not None
    assert preset["id"] == first_id
    assert get_preset_by_id("unknown-id-xyz") is None


def test_html_export_generator():
    topic = "Post-Quantum Cryptography Latency"
    markdown = (
        "## Abstract\n"
        "This is an empirical evaluation of ML-KEM algorithms.\n\n"
        "### Key Findings\n"
        "- Finding 1: Minimal overhead in TLS 1.3\n"
        "- Finding 2: Hardware acceleration improves throughput\n"
    )
    html = generate_standalone_html_publication(topic, markdown, {"domain": "Cryptography", "confidence_score": 95})
    assert "<!DOCTYPE html>" in html
    assert topic in html
    assert "Soumyadeep Ghosh" in html
    assert "two-column-layout" in html
    assert "<h2>Abstract</h2>" in html
    assert "Finding 1" in html
