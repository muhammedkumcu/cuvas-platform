# -*- coding: utf-8 -*-
"""REST API testleri (Flask test client)."""
import os
import sys
import pytest

_WEB = os.path.join(os.path.dirname(__file__), "..", "web")
sys.path.insert(0, _WEB)

flask = pytest.importorskip("flask")
import app as A  # noqa: E402


@pytest.fixture(scope="module")
def client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


def test_health(client):
    d = client.get("/api/health").get_json()
    assert d["status"] == "ok"
    assert d["lexicon_count"] > 20000


def test_analyze(client):
    d = client.post("/api/analyze", json={"word": "ҫынна"}).get_json()
    assert d["success"]
    assert any(p["analysis"] == "ҫын<n><dat>" for p in d["parses"])


def test_generate_noun(client):
    d = client.post("/api/generate/noun",
                    json={"stem": "кӗнеке", "plural": True, "case": "loc"}).get_json()
    assert d["word"] == "кӗнекесенче"


def test_generate_verb(client):
    d = client.post("/api/generate/verb",
                    json={"stem": "кил", "tense": "pres", "person": "p1sg"}).get_json()
    assert d["word"] == "килетӗп"


def test_paradigm_noun(client):
    d = client.get("/api/paradigm/noun?stem=хула").get_json()
    assert d["table"]["singular"]["loc"] == "хулара"


def test_spellcheck(client):
    assert client.post("/api/spellcheck", json={"word": "ҫынна"}).get_json()["correct"] is True
    assert client.post("/api/spellcheck", json={"word": "qwx"}).get_json()["correct"] is False


def test_exercise_answer_in_options(client):
    d = client.get("/api/exercise").get_json()
    assert d["answer"] in d["options"]
    assert len(d["options"]) >= 2


def test_homepage(client):
    assert client.get("/").status_code == 200
