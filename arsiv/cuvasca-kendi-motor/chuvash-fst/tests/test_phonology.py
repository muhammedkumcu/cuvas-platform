# -*- coding: utf-8 -*-
"""Fonoloji motoru birim testleri."""
from chuvash_fst.phonology import Alphabet, Phonology, normalize, has_latin_homoglyph


# -- Ünlü uyumu ---------------------------------------------------------------

def test_harmony_front():
    assert Phonology.harmony("кӗнеке") == "front"   # kitap
    assert Phonology.harmony("ӗҫ") == "front"        # iş
    assert Phonology.harmony("кил") == "front"       # gel-

def test_harmony_back():
    assert Phonology.harmony("хула") == "back"       # şehir
    assert Phonology.harmony("ҫын") == "back"        # insan
    assert Phonology.harmony("ту") == "back"         # yap- / dağ
    assert Phonology.harmony("ҫул") == "back"        # yol/yaş

def test_harmony_default_no_vowel():
    assert Phonology.harmony("") == "back"

def test_V_allomorph_selection():
    assert Phonology.V("ра", "ре", "хула") == "ра"
    assert Phonology.V("ра", "ре", "кӗнеке") == "ре"


# -- Homoglyph / normalizasyon ------------------------------------------------

def test_normalize_latin_homoglyph_to_cyrillic():
    # Latin 'c' (U+0063) -> Kiril 'с' (U+0441)
    assert normalize("cалам") == "салам"
    # saf Kiril değişmez
    assert normalize("хула") == "хула"

def test_has_latin_homoglyph():
    assert has_latin_homoglyph("cалам") is True
    assert has_latin_homoglyph("салам") is False

def test_normalize_idempotent():
    s = "кӗнекесем"
    assert normalize(normalize(s)) == normalize(s)


# -- Ek başı ünsüz asimilasyonu (loc/abl) -------------------------------------

def test_takes_t_allomorph():
    assert Phonology.takes_t_allomorph("кӗл") is True    # л
    assert Phonology.takes_t_allomorph("ҫын") is True    # н
    assert Phonology.takes_t_allomorph("ҫул") is True    # л
    assert Phonology.takes_t_allomorph("хула") is False  # ünlü
    assert Phonology.takes_t_allomorph("урам") is False  # м (likit/nazal değil)

def test_locative_allomorph():
    assert Phonology.locative("хула") == "ра"   # хулара
    assert Phonology.locative("кӗнеке") == "ре" # кӗнекере
    assert Phonology.locative("ҫул") == "та"    # ҫулта
    assert Phonology.locative("кӗл") == "те"    # кӗлте
    assert Phonology.locative("ӗҫ") == "ре"     # ӗҫре (ҫ likit/nazal değil)

def test_ablative_allomorph():
    assert Phonology.ablative("хула") == "ран"
    assert Phonology.ablative("ҫул") == "тан"
    assert Phonology.ablative("кӗл") == "тен"


# -- Ünlü yapısı --------------------------------------------------------------

def test_ends_with_vowel():
    assert Phonology.ends_with_vowel("хула") is True
    assert Phonology.ends_with_vowel("ҫын") is False

def test_ends_with_reduced():
    assert Phonology.ends_with_reduced("пулӑ") is True   # ӑ
    assert Phonology.ends_with_reduced("ҫын") is False

def test_last_vowel():
    assert Phonology.last_vowel("кӗнеке") == "е"
    assert Phonology.last_vowel("ҫын") == "ы"
    assert Phonology.last_vowel("кр") is None


# -- İndirgenmiş ünlü düşmesi / gemination ------------------------------------

def test_drop_final_reduced():
    # ünlüyle başlayan ek öncesi kök-sonu ӑ/ӗ düşer
    assert Phonology.drop_final_reduced("пулӑ", "ӑн") == "пул"
    # ünsüzle başlayan ek öncesi düşmez
    assert Phonology.drop_final_reduced("пулӑ", "сем") == "пулӑ"

def test_geminate_final():
    assert Phonology.geminate_final("ҫын") == "ҫынн"
    assert Phonology.geminate_final("хула") == "хула"  # ünlü-sonu değişmez

def test_alphabet_sets_disjoint():
    assert not (Alphabet.BACK_VOWELS & Alphabet.FRONT_VOWELS)
    assert Alphabet.REDUCED <= Alphabet.VOWELS
    assert not (Alphabet.VOWELS & Alphabet.CONSONANTS)
