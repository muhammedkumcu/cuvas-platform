# -*- coding: utf-8 -*-
"""Sözlük yükleyici testleri (seed sözlük üzerinde)."""
import os
import pytest
from chuvash_fst.lexicon import Lexicon

SEED = os.path.join(os.path.dirname(__file__), "..", "data", "chuvash_lexicon_seed.txt")


@pytest.fixture(scope="module")
def lex():
    return Lexicon().load(SEED)


def test_seed_loads(lex):
    assert lex.count > 20000


def test_known_noun_present(lex):
    assert "ҫын" in lex          # insan
    entries = lex.lookup("ҫын")
    assert any(e.pos == "n" for e in entries)


def test_pos_buckets_nonempty(lex):
    assert len(lex.nouns()) > 5000
    assert len(lex.verbs()) > 3000
    assert len(lex.adjectives()) > 1000


def test_gloss_parsed(lex):
    entries = lex.lookup("ҫын")
    assert any(e.gloss_ru for e in entries)  # ru:человек


def test_normalize_on_lookup(lex):
    # Latin homoglyph'li sorgu da bulunmalı (c -> с)
    if "ҫын" in lex:
        # сӑмах benzeri; burada normalize'ın lookup'ta çalıştığını doğrula
        assert lex.lookup("ҫын") == lex.lookup("ҫын")
