"""API and Route Configuration Tests for DeepResearch Engine."""

from app import app
from core.presets import get_all_presets, get_preset_by_id


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
