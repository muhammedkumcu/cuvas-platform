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


class VerbGenerator:
    """
    Fiil çekimi: KÖK + [OLUMSUZ] + ZAMAN/KİP + ŞAHIS.
    Zaman ekleri ve şahıs setleri apertium-chv lexc (V-T*, V-PERS-*) verisinden.

    Desteklenen: şimdiki/geniş (pres), belirli geçmiş (past), gelecek (fut),
    emir (imp), mastar (inf). Sentetik olumsuzluk dahil.

    NOT (MVP): öğrenilen geçmiş (-нӑ), koşul, çatı yığılması ve düzensiz fiiller
    (ту→тӑв-) henüz dahil değil; past'taki -р- düşmesi sık fiillerle sınırlı liste.
    """

    # Kapalı sınıf: geçmiş/olumsuz/şimdiki önünde kök-sonu -р- düşen sık fiiller
    # (apertium twol "Final -р- ... deletes"). Sık örneklerle sınırlı — genişletilecek.
    R_DROP = frozenset({"пар", "тӑр", "кур", "кӗр", "хур", "сар", "яр", "вӗр", "тӑр"})

    def __init__(self, lexicon=None):
        self.lexicon = lexicon

    # -- yardımcılar ----------------------------------------------------------

    @staticmethod
    def _drop_final_ae(stem: str) -> str:
        """Şimdiki zaman {A}-başlı ek öncesi kök-sonu а/е düşer (ӗҫле→ӗҫл-)."""
        if stem and stem[-1] in "ае":
            return stem[:-1]
        return stem

    def _T_before_reduced(self, stem: str):
        """Geçmiş {T}, {Ă}-başlı şahıs eki (p1/p2) öncesi: р/л/н→т, r-drop, aksi→р."""
        if stem in self.R_DROP:
            return stem[:-1], "т"
        if stem and stem[-1] in "рлн":
            return stem, "т"
        return stem, "р"

    def _T_before_e(self, stem: str):
        """Geçmiş {T}, ӗ-başlı şahıs eki (p3) öncesi: р/л/н→ч (palatalize), r-drop→ч, aksi→р."""
        if stem in self.R_DROP:
            return stem[:-1], "ч"
        if stem and stem[-1] in "рлн":
            return stem, "ч"
        return stem, "р"

    # -- zamanlar -------------------------------------------------------------

    def present(self, stem: str, person: str, neg: bool = False) -> str:
        back = not P.is_front(stem)
        s = self._drop_final_ae(stem)
        if neg:
            base = s + P.V("маст", "мест", stem)
            if person == "p3sg":
                return base + ("ь" if back else "")
            if person == "p3pl":
                return s + P.V("маҫҫӗ", "меҫҫӗ", stem)
            end = {"p1sg": P.V("ӑп", "ӗп", stem), "p2sg": P.V("ӑн", "ӗн", stem),
                   "p1pl": P.V("пӑр", "пӗр", stem), "p2pl": P.V("ӑр", "ӗр", stem)}
            return base + end[person]
        base = s + P.V("ат", "ет", stem)
        if person == "p3sg":
            return base + ("ь" if back else "")
        if person == "p3pl":
            return s + P.V("аҫҫӗ", "еҫҫӗ", stem)
        end = {"p1sg": P.V("ӑп", "ӗп", stem), "p2sg": P.V("ӑн", "ӗн", stem),
               "p1pl": P.V("пӑр", "пӗр", stem), "p2pl": P.V("ӑр", "ӗр", stem)}
        return base + end[person]

    def future(self, stem: str, person: str, neg: bool = False) -> str:
        base = stem + ("м" if neg else "")
        end = {"p1sg": P.V("ӑп", "ӗп", stem), "p2sg": P.V("ӑн", "ӗн", stem),
               "p3sg": "ӗ", "p1pl": P.V("ӑпӑр", "ӗпӗр", stem),
               "p2pl": P.V("ӑр", "ӗр", stem), "p3pl": "ӗҫ"}
        return base + end[person]

    def _past_person_ending(self, stem: str, person: str) -> str:
        return {"p1sg": P.V("ӑм", "ӗм", stem), "p2sg": P.V("ӑн", "ӗн", stem),
                "p1pl": P.V("ӑмӑр", "ӗмӗр", stem), "p2pl": P.V("ӑр", "ӗр", stem),
                "p3sg": "ӗ", "p3pl": "ӗҫ"}[person]

    def past(self, stem: str, person: str, neg: bool = False) -> str:
        if neg:
            base = stem + P.V("мар", "мер", stem)
            return base + self._past_person_ending(base, person)
        if person in ("p1sg", "p2sg", "p1pl", "p2pl"):
            st, t = self._T_before_reduced(stem)
            return st + t + self._past_person_ending(stem, person)
        st, t = self._T_before_e(stem)
        return st + t + ("ӗ" if person == "p3sg" else "ӗҫ")

    def imperative(self, stem: str, person: str) -> str:
        return {
            "p2sg": stem,
            "p2pl": stem + P.V("ӑр", "ӗр", stem),
            "p3sg": stem + P.V("тӑр", "тӗр", stem),
            "p1sg": stem + P.V("ам", "ем", stem),
            "p1pl": stem + P.V("ар", "ер", stem),
            "p3pl": stem + P.V("ччӑр", "ччӗр", stem),
        }[person]

    def infinitive(self, stem: str) -> str:
        return stem + P.V("ма", "ме", stem)

    # -- birleşik API ---------------------------------------------------------

    def generate(self, stem: str, tense: str, person: Optional[str] = None,
                 neg: bool = False) -> GenResult:
        stem = stem.strip()
        if tense == "inf":
            w = self.infinitive(stem)
            return GenResult(w, w, stem + "<v><inf>")
        if tense == "imp":
            w = self.imperative(stem, person or "p2sg")
            return GenResult(w, w, stem + M.verb_analysis_tag("imp", person or "p2sg"))
        fn = {"pres": self.present, "past": self.past, "fut": self.future}[tense]
        w = fn(stem, person, neg)
        return GenResult(w, w, stem + M.verb_analysis_tag(tense, person, neg))

    def tense_paradigm(self, stem: str, tense: str, neg: bool = False) -> Dict[str, str]:
        """Bir zamanın 6 şahıs çekimi."""
        return {p: self.generate(stem, tense, p, neg).word for p in M.PERSONS}

    def conjugation_table(self, stem: str) -> Dict[str, Dict[str, str]]:
        """Öğrenme platformu için fiil çekim tablosu."""
        return {
            "pres": self.tense_paradigm(stem, "pres"),
            "pres_neg": self.tense_paradigm(stem, "pres", neg=True),
            "past": self.tense_paradigm(stem, "past"),
            "fut": self.tense_paradigm(stem, "fut"),
            "imp": {p: self.imperative(stem, p) for p in M.PERSONS},
            "inf": self.infinitive(stem),
        }
