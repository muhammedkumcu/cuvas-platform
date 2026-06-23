# -*- coding: utf-8 -*-
"""
ChuvashFST — Morfotaktik Modülü (morphotactics.py)

Çuvaşça ek diziliş (slot order) kurallarını ve geçerli ek envanterlerini tanımlar.
FST-ilhamlı; ek sırasını ve etiket setlerini merkezîleştirir.

İSİM slot sırası:  KÖK + [İYELİK] + [ÇOĞUL] + [HAL]   (Türkmence'den FARKLI!)
FİİL slot sırası:  KÖK + [ÇATI] + [OLUMSUZ] + ZAMAN/KİP + [ŞAHIS]

Kaynak: kurallar/KURALLAR_CUVASCA.md + apertium-chv lexc continuation class'ları.
"""
from __future__ import annotations

# -- İsim hal etiketleri (8 hal; dat ve acc birleşik) -------------------------
CASES = ["nom", "gen", "dat", "loc", "abl", "ins", "abe", "ter"]

CASE_NAMES_TR = {
    "nom": "Yalın",
    "gen": "İlgi (tamlayan)",
    "dat": "Yönelme-Belirtme",
    "loc": "Bulunma",
    "abl": "Ayrılma",
    "ins": "Vasıta",
    "abe": "Mahrumiyet",
    "ter": "Sebep-amaç",
}

# Nominatif ve enstrümantal dışındaki haller "oblik" — çoğul -сем yerine -сен alır
OBLIQUE_CASES = frozenset({"gen", "dat", "loc", "abl", "abe", "ter"})

# Gemination (ikizleşme) yalnız bu hallerden önce uygulanır (twol istisnalarına göre)
GEMINATING_CASES = frozenset({"gen", "dat"})

# -- İyelik etiketleri (5; 3. şahıs tekil/çoğul birleşik = px3sp) -------------
POSSESSIVES = ["px1sg", "px2sg", "px3sp", "px1pl", "px2pl"]

POSSESSIVE_NAMES_TR = {
    "px1sg": "1. tekil (benim)",
    "px2sg": "2. tekil (senin)",
    "px3sp": "3. şahıs (onun/onların)",
    "px1pl": "1. çoğul (bizim)",
    "px2pl": "2. çoğul (sizin)",
}

# -- Fiil zaman/kip etiketleri ------------------------------------------------
TENSES = ["pres", "past", "nar", "fut", "imp"]

TENSE_NAMES_TR = {
    "pres": "Şimdiki/geniş",
    "past": "Belirli geçmiş",
    "nar": "Öğrenilen geçmiş",
    "fut": "Gelecek",
    "imp": "Emir",
}

PERSONS = ["p1sg", "p2sg", "p3sg", "p1pl", "p2pl", "p3pl"]


def valid_noun_slots(possessive=None, plural=False, case="nom") -> bool:
    """İsim için verilen slot kombinasyonu morfotaktik olarak geçerli mi?"""
    if possessive is not None and possessive not in POSSESSIVES:
        return False
    if case not in CASES:
        return False
    return True


def noun_analysis_tag(pos, possessive=None, plural=False, case="nom") -> str:
    """apertium-stili analiz etiketi üretir: kĕneke<n><px1sg><pl><loc>"""
    tags = [f"<{pos}>"]
    if possessive:
        tags.append(f"<{possessive}>")
    if plural:
        tags.append("<pl>")
    tags.append(f"<{case}>")
    return "".join(tags)


# p1sg -> <p1><sg> ayrıştırması (apertium etiket stili)
_PERSON_TAGS = {
    "p1sg": "<p1><sg>", "p2sg": "<p2><sg>", "p3sg": "<p3><sg>",
    "p1pl": "<p1><pl>", "p2pl": "<p2><pl>", "p3pl": "<p3><pl>",
}


def verb_analysis_tag(tense, person=None, neg=False) -> str:
    """apertium-stili fiil etiketi: kil<v><pres><p1><sg> / kil<v><neg><pres>..."""
    tags = ["<v>"]
    if neg:
        tags.append("<neg>")
    tags.append(f"<{tense}>")
    if person:
        tags.append(_PERSON_TAGS[person])
    return "".join(tags)
