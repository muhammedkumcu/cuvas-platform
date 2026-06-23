# -*- coding: utf-8 -*-
"""
ChuvashFST — Üretim Modülü (generator.py)

Kök + morfolojik özellikler → çekimli yüzey biçimi (Kiril).
İsim çekimi: KÖK + [İYELİK] + [ÇOĞUL] + [HAL].

Pedagojik çekirdek: 8 hal × tekil/çoğul paradigması ve iyelik.
Gemination, sözlükteki `gemination` işaretine göre uygulanır (apertium {ː} verisi).

NOT (MVP sınırları): iyelik+hal etkileşimi ve t/d köklerde iyelik palatalizasyonu
(пӳрт→пӳрчӗ) henüz tam değil — Gün 6 corpus doğrulamasında rafine edilecek.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, List

from .phonology import Phonology as P
from . import morphotactics as M


@dataclass
class GenResult:
    word: str
    breakdown: str          # "кӗнеке + сен + че"
    analysis: str           # "кӗнеке<n><pl><loc>"
    valid: bool = True


# Çoğul paradigması — -сем/-сен donmuş (uyuma girmez), bu yüzden sabit:
#   nom/ins -> -сем(пе);  oblik haller -> -сен + (palatalize) hal eki
PLURAL_CASE_SUFFIX = {
    "nom": "сем",
    "ins": "семпе",
    "gen": "сен",
    "dat": "сене",
    "loc": "сенче",      # т→ч palatalizasyon (н sonrası)
    "abl": "сенчен",
    "abe": "сенсӗр",
    "ter": "сеншӗн",
}


class NounGenerator:
    def __init__(self, lexicon=None):
        self.lexicon = lexicon

    # -- yardımcılar ----------------------------------------------------------

    def _geminates(self, stem: str) -> bool:
        """Sözlükte gemination işareti var mı?"""
        if self.lexicon is None:
            return False
        for e in self.lexicon.lookup(stem):
            if e.has("gemination"):
                return True
        return False

    def _case_part(self, base: str, case: str, geminate: bool):
        """(gövde, ek) döndürür — tekil hal eki, allomorf + gemination dahil."""
        ev = P.ends_with_vowel(base)
        if case == "nom":
            return base, ""
        if case == "gen":
            if ev:
                return base, "н"
            b = P.geminate_final(base) if geminate else base
            return b, P.V("ӑн", "ӗн", base)
        if case == "dat":
            if ev:
                return base, P.V("на", "не", base)
            b = P.geminate_final(base) if geminate else base
            return b, P.V("а", "е", base)
        if case == "loc":
            return base, P.locative(base)
        if case == "abl":
            return base, P.ablative(base)
        if case == "ins":
            return base, P.V("па", "пе", base)
        if case == "abe":
            return base, P.V("сӑр", "сӗр", base)
        if case == "ter":
            return base, P.V("шӑн", "шӗн", base)
        raise ValueError(f"bilinmeyen hal: {case}")

    def _possessive_part(self, stem: str, person: str, geminate: bool):
        """(gövde, ek) döndürür — nominatif iyelik. Ünlü-sonu köklerde sağlam."""
        ev = P.ends_with_vowel(stem)
        # ünlü-sonu kökte 2sg/3sp/2pl son ünlüyü düşürür
        drop = stem[:-1] if ev else None
        if person == "px1sg":
            if ev:
                return stem, "м"
            b = P.geminate_final(stem) if geminate else stem
            return b, P.V("ӑм", "ӗм", stem)
        if person == "px2sg":
            if ev:
                return drop, P.V("у", "ӳ", stem)
            b = P.geminate_final(stem) if geminate else stem
            return b, P.V("у", "ӳ", stem)
        if person == "px3sp":
            if ev:
                return drop, "и"
            b = P.geminate_final(stem) if geminate else stem
            return b, "и"
        if person == "px1pl":
            if ev:
                return stem, P.V("мӑр", "мӗр", stem)
            b = P.geminate_final(stem) if geminate else stem
            return b, P.V("ӑмӑр", "ӗмӗр", stem)
        if person == "px2pl":
            if ev:
                return drop, P.V("ӑр", "ӗр", stem)
            b = P.geminate_final(stem) if geminate else stem
            return b, P.V("ӑр", "ӗр", stem)
        raise ValueError(f"bilinmeyen iyelik: {person}")

    # -- ana üretim -----------------------------------------------------------

    def generate(self, stem: str, possessive: Optional[str] = None,
                 plural: bool = False, case: str = "nom",
                 pos: str = "n") -> GenResult:
        stem = stem.strip()
        if not M.valid_noun_slots(possessive, plural, case):
            return GenResult(stem, stem, "", valid=False)

        geminate = self._geminates(stem)
        parts: List[str] = [stem]
        word = stem

        # 1) İYELİK (KÖK'ten hemen sonra)
        if possessive:
            b, suf = self._possessive_part(stem, possessive, geminate)
            word = b + suf
            parts = [b, suf]
            # iyelikten sonra hal: MVP — yalnız nominatif/çoğul desteklenir
            # (iyelik+hal etkileşimi Gün 6'da)

        # 2) ÇOĞUL (+ hal birleşik) — iyelik yokken tam paradigma
        if plural and not possessive:
            suf = PLURAL_CASE_SUFFIX[case]
            word = stem + suf
            parts = [stem, suf]
            return GenResult(word, " + ".join(parts),
                             stem + M.noun_analysis_tag(pos, None, True, case))

        if plural and possessive:
            # iyelik + çoğul (nominatif) — кӗнекемсем
            word = word + "сем"
            parts.append("сем")
            return GenResult(word, " + ".join(parts),
                             stem + M.noun_analysis_tag(pos, possessive, True, case))

        if possessive:
            return GenResult(word, " + ".join(parts),
                             stem + M.noun_analysis_tag(pos, possessive, False, "nom"))

        # 3) HAL (tekil, iyeliksiz)
        b, suf = self._case_part(stem, case, geminate)
        word = b + suf
        parts = [b, suf] if suf else [b]
        return GenResult(word, " + ".join(p for p in parts if p),
                         stem + M.noun_analysis_tag(pos, None, False, case))

    # -- paradigma ------------------------------------------------------------

    def case_paradigm(self, stem: str, plural: bool = False) -> Dict[str, GenResult]:
        """Bir ismin tüm hal çekimlerini döndürür (tekil veya çoğul)."""
        return {c: self.generate(stem, plural=plural, case=c) for c in M.CASES}

    def possessive_paradigm(self, stem: str) -> Dict[str, GenResult]:
        """Bir ismin tüm iyelik çekimlerini döndürür (nominatif)."""
        return {p: self.generate(stem, possessive=p) for p in M.POSSESSIVES}

    def full_table(self, stem: str) -> Dict[str, Dict[str, str]]:
        """Öğrenme platformu için düz tablo: {tekil:{hal:form}, çoğul:{...}, iyelik:{...}}"""
        return {
            "singular": {c: r.word for c, r in self.case_paradigm(stem, False).items()},
            "plural": {c: r.word for c, r in self.case_paradigm(stem, True).items()},
            "possessive": {p: r.word for p, r in self.possessive_paradigm(stem).items()},
        }
