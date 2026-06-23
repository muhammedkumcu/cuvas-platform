# -*- coding: utf-8 -*-
"""İsim üretim (generation) testleri."""
import os
import pytest
from chuvash_fst.lexicon import Lexicon
from chuvash_fst.generator import NounGenerator

SEED = os.path.join(os.path.dirname(__file__), "..", "data", "chuvash_lexicon_seed.txt")


@pytest.fixture(scope="module")
def gen():
    lex = Lexicon().load(SEED)
    return NounGenerator(lex)


# -- Tekil hal paradigması (ünlü-sonu kök: кӗнеке "kitap", ön uyum) -----------

def test_case_paradigm_kĕneke(gen):
    forms = {c: r.word for c, r in gen.case_paradigm("кӗнеке").items()}
    assert forms == {
        "nom": "кӗнеке",
        "gen": "кӗнекен",
        "dat": "кӗнекене",
        "loc": "кӗнекере",
        "abl": "кӗнекерен",
        "ins": "кӗнекепе",
        "abe": "кӗнекесӗр",
        "ter": "кӗнекешӗн",
    }


# -- Tekil hal paradigması (ünlü-sonu, art uyum: хула "şehir") ---------------

def test_case_paradigm_hula(gen):
    forms = {c: r.word for c, r in gen.case_paradigm("хула").items()}
    assert forms["gen"] == "хулан"
    assert forms["dat"] == "хулана"
    assert forms["loc"] == "хулара"     # ünlü-sonu -> р-allomorf
    assert forms["abl"] == "хуларан"
    assert forms["ins"] == "хулапа"
    assert forms["ter"] == "хулашӑн"


# -- Ünsüz-sonu + gemination (ҫын "insan", apertium {ː}) ---------------------

def test_case_paradigm_ҫyn_gemination(gen):
    forms = {c: r.word for c, r in gen.case_paradigm("ҫын").items()}
    assert forms["gen"] == "ҫыннӑн"     # gemination + ӑн
    assert forms["dat"] == "ҫынна"      # gemination + а
    assert forms["loc"] == "ҫынта"      # gemination YOK (loc); н -> т-allomorf
    assert forms["abl"] == "ҫынтан"
    assert forms["ins"] == "ҫынпа"
    assert forms["abe"] == "ҫынсӑр"
    assert forms["ter"] == "ҫыншӑн"


# -- Çoğul paradigması (-сем/-сен oblik + palatalizasyon) --------------------

def test_plural_paradigm_kĕneke(gen):
    forms = {c: r.word for c, r in gen.case_paradigm("кӗнеке", plural=True).items()}
    assert forms["nom"] == "кӗнекесем"
    assert forms["gen"] == "кӗнекесен"
    assert forms["dat"] == "кӗнекесене"
    assert forms["loc"] == "кӗнекесенче"    # т→ч palatalizasyon
    assert forms["abl"] == "кӗнекесенчен"
    assert forms["ins"] == "кӗнекесемпе"     # ins -> -сем korunur

def test_plural_paradigm_ҫyn(gen):
    forms = {c: r.word for c, r in gen.case_paradigm("ҫын", plural=True).items()}
    assert forms["nom"] == "ҫынсем"          # gemination YOK (с öncesi)
    assert forms["dat"] == "ҫынсене"
    assert forms["loc"] == "ҫынсенче"
    assert forms["abl"] == "ҫынсенчен"
    assert forms["ins"] == "ҫынсемпе"


# -- İyelik paradigması (ünlü-sonu kök) --------------------------------------

def test_possessive_paradigm_kĕneke(gen):
    forms = {p: r.word for p, r in gen.possessive_paradigm("кӗнеке").items()}
    assert forms["px1sg"] == "кӗнекем"
    assert forms["px2sg"] == "кӗнекӳ"
    assert forms["px3sp"] == "кӗнеки"
    assert forms["px1pl"] == "кӗнекемӗр"

def test_possessive_hula(gen):
    forms = {p: r.word for p, r in gen.possessive_paradigm("хула").items()}
    assert forms["px1sg"] == "хулам"
    assert forms["px3sp"] == "хули"

def test_possessive_gemination_ҫyn(gen):
    forms = {p: r.word for p, r in gen.possessive_paradigm("ҫын").items()}
    assert forms["px1sg"] == "ҫыннӑм"
    assert forms["px3sp"] == "ҫынни"


# -- breakdown / analysis etiketi --------------------------------------------

def test_breakdown_and_analysis(gen):
    r = gen.generate("кӗнеке", plural=True, case="loc")
    assert r.word == "кӗнекесенче"
    assert r.breakdown == "кӗнеке + сенче"
    assert r.analysis == "кӗнеке<n><pl><loc>"

def test_full_table_shape(gen):
    t = gen.full_table("кӗнеке")
    assert set(t) == {"singular", "plural", "possessive"}
    assert t["singular"]["nom"] == "кӗнеке"
    assert t["plural"]["loc"] == "кӗнекесенче"
