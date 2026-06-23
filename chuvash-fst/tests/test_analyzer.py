# -*- coding: utf-8 -*-
"""Analiz motoru + round-trip (üret↔çözümle) tutarlılık testleri."""
import os
import pytest
from chuvash_fst.lexicon import Lexicon
from chuvash_fst.generator import NounGenerator, VerbGenerator
from chuvash_fst.analyzer import Analyzer
from chuvash_fst import morphotactics as M

SEED = os.path.join(os.path.dirname(__file__), "..", "data", "chuvash_lexicon_seed.txt")


@pytest.fixture(scope="module")
def lex():
    return Lexicon().load(SEED)


@pytest.fixture(scope="module")
def az(lex):
    return Analyzer(lex)


# -- Temel analiz -------------------------------------------------------------

def test_analyze_noun_plural_locative(az):
    res = az.analyze("кӗнекесенче")
    assert res.success
    analyses = [p.analysis for p in res.parses]
    assert "кӗнеке<n><pl><loc>" in analyses

def test_analyze_noun_dative_gemination(az):
    res = az.analyze("ҫынна")
    assert "ҫын<n><dat>" in [p.analysis for p in res.parses]

def test_analyze_invalid_word(az):
    assert not az.analyze("блаблабла").success


# -- Fiil analizi (sözlükte fiil olan bir kökle) ------------------------------

def test_analyze_verb_present(lex, az):
    # 'пар' sözlükte fiil mi? (apertium seed'inden)
    if not any(e.pos == "v" for e in lex.lookup("пар")):
        pytest.skip("пар sözlükte fiil değil")
    res = az.analyze("паратӑп")
    assert "пар<v><pres><p1><sg>" in [p.analysis for p in res.parses]


# -- Round-trip: üret -> çözümle -> aynı analiz --------------------------------

def test_roundtrip_noun_cases(lex):
    ng = NounGenerator(lex)
    az = Analyzer(lex)
    for stem in ["кӗнеке", "хула", "ҫын"]:
        for case in M.CASES:
            for plural in (False, True):
                r = ng.generate(stem, plural=plural, case=case)
                got = [p.analysis for p in az.analyze(r.word).parses]
                assert r.analysis in got, f"{r.word} -> {r.analysis} bulunamadı: {got}"


def test_roundtrip_verb_present(lex):
    if not any(e.pos == "v" for e in lex.lookup("пар")):
        pytest.skip("пар fiil değil")
    vg = VerbGenerator(lex)
    az = Analyzer(lex)
    for person in M.PERSONS:
        r = vg.generate("пар", "pres", person)
        got = [p.analysis for p in az.analyze(r.word).parses]
        assert r.analysis in got, f"{r.word} -> {r.analysis} bulunamadı"


# -- Yazım denetimi -----------------------------------------------------------

def test_is_valid(az):
    assert az.is_valid("кӗнекесем") is True
    assert az.is_valid("ҫынна") is True
    assert az.is_valid("qwzxcv") is False
