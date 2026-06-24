# -*- coding: utf-8 -*-
"""Fiil üretim (generation) testleri.

Beklenen formlar apertium-chv lexc örnekleri ve referans gramerlerle doğrulandı:
кил- (gel-), пӗл- (bil-), уҫ- (aç-), пар- (ver-, r-drop), ӗҫле- (çalış-).
"""
from chuvash_fst.generator import VerbGenerator
from chuvash_fst import morphotactics as M

g = VerbGenerator()


# -- Şimdiki/geniş zaman (olumlu) --------------------------------------------

def test_present_kil():
    assert g.tense_paradigm("кил", "pres") == {
        "p1sg": "килетӗп", "p2sg": "килетӗн", "p3sg": "килет",
        "p1pl": "килетпӗр", "p2pl": "килетӗр", "p3pl": "килеҫҫӗ",
    }

def test_present_uҫ_backvowel_softsign():
    forms = g.tense_paradigm("уҫ", "pres")
    assert forms["p1sg"] == "уҫатӑп"
    assert forms["p3sg"] == "уҫать"      # art ünlü + т -> yumuşatma işareti
    assert forms["p3pl"] == "уҫаҫҫӗ"

def test_present_vowelfinal_drop():
    # ӗҫле- : kök-sonu е, {A}т öncesi düşer -> ӗҫлет-
    assert g.present("ӗҫле", "p1sg") == "ӗҫлетӗп"


# -- Şimdiki zaman (olumsuz, sentetik -мас/-мест) ----------------------------

def test_present_negative_pĕl():
    assert g.tense_paradigm("пӗл", "pres", neg=True) == {
        "p1sg": "пӗлместӗп", "p2sg": "пӗлместӗн", "p3sg": "пӗлмест",
        "p1pl": "пӗлместпӗр", "p2pl": "пӗлместӗр", "p3pl": "пӗлмеҫҫӗ",
    }

def test_present_negative_kil():
    forms = g.tense_paradigm("кил", "pres", neg=True)
    assert forms["p3sg"] == "килмест"
    assert forms["p1sg"] == "килместӗп"


# -- Belirli geçmiş zaman ({T} palatalizasyon + r-drop) ----------------------

def test_past_kil_palatalization():
    forms = g.tense_paradigm("кил", "past")
    assert forms["p1sg"] == "килтӗм"     # л -> т (reduced öncesi)
    assert forms["p3sg"] == "килчӗ"      # л -> ч (ӗ öncesi, palatalize)

def test_past_uҫ_default_r():
    forms = g.tense_paradigm("уҫ", "past")
    assert forms["p1sg"] == "уҫрӑм"
    assert forms["p3sg"] == "уҫрӗ"

def test_past_par_rdrop():
    forms = g.tense_paradigm("пар", "past")
    assert forms["p1sg"] == "патӑм"      # пар -> па (r-drop) + т
    assert forms["p3sg"] == "пачӗ"       # пар -> па + ч

def test_past_negative():
    forms = g.tense_paradigm("кил", "past", neg=True)
    assert forms["p1sg"] == "килмерӗм"
    assert forms["p3sg"] == "килмерӗ"


# -- Gelecek zaman ------------------------------------------------------------

def test_future_kil():
    forms = g.tense_paradigm("кил", "fut")
    assert forms["p1sg"] == "килӗп"
    assert forms["p3sg"] == "килӗ"
    assert forms["p3pl"] == "килӗҫ"

def test_future_negative():
    assert g.future("кил", "p1sg", neg=True) == "килмӗп"


# -- Emir + mastar ------------------------------------------------------------

def test_imperative_kil():
    assert g.imperative("кил", "p2sg") == "кил"
    assert g.imperative("кил", "p2pl") == "килӗр"
    assert g.imperative("кил", "p3sg") == "килтӗр"
    assert g.imperative("кил", "p1pl") == "килер"

def test_infinitive():
    assert g.infinitive("кил") == "килме"
    assert g.infinitive("уҫ") == "уҫма"
    assert g.infinitive("ӗҫле") == "ӗҫлеме"


# -- Analiz etiketi + tablo ---------------------------------------------------

def test_analysis_tag():
    r = g.generate("кил", "pres", "p1sg")
    assert r.word == "килетӗп"
    assert r.analysis == "кил<v><pres><p1><sg>"
    r2 = g.generate("кил", "pres", "p3sg", neg=True)
    assert r2.analysis == "кил<v><neg><pres><p3><sg>"

def test_conjugation_table_shape():
    t = g.conjugation_table("кил")
    assert {"pres", "pres_neg", "past", "fut", "imp", "inf"} <= set(t)
    assert t["inf"] == "килме"
    assert t["pres"]["p1sg"] == "килетӗп"


def test_nonfinite_forms():
    assert g.nonfinite("пул", "nar") == "пулнӑ"        # öğrenilen geçmiş
    assert g.nonfinite("кил", "cvb") == "килсе"        # zarf-fiil
    assert g.nonfinite("кил", "ppres") == "килекен"    # şimdiki sıfat-fiil
    assert g.nonfinite("кил", "pfut") == "килес"       # gelecek sıfat-fiil
