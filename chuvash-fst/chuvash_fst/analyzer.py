# -*- coding: utf-8 -*-
"""
ChuvashFST — Analiz Modülü (analyzer.py)

Üret-ve-doğrula (generate-and-verify) stratejisi: yüzey kelimeyi, sözlükteki
köklerden üretilebilecek tüm çekimlerle karşılaştırarak çözümler. Üretici
doğru kabul edildiği için analiz de tutarlıdır (round-trip garanti).

Aday kök = kelimenin sözlükte bulunan ön ekleri (prefix). r-düşmesi gibi
kökü kısaltan olaylar bu MVP'de kaçabilir (Gün 6'da genişletilecek).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from .phonology import normalize
from .lexicon import Lexicon
from .generator import NounGenerator, VerbGenerator
from . import morphotactics as M


@dataclass
class Parse:
    stem: str
    pos: str
    analysis: str            # кӗнеке<n><pl><loc>
    breakdown: str           # кӗнеке + сенче
    gloss_ru: str = ""

    def __hash__(self):
        return hash(self.analysis)


@dataclass
class AnalysisResult:
    word: str
    parses: List[Parse] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return bool(self.parses)


# İsim çekim kombinasyonları (generator.generate'in desteklediği yollar)
def _noun_combos():
    yield (None, False, "nom")
    yield (None, False, "attr")      # sıfat-fiil -ри/-чи
    for c in M.CASES:
        yield (None, False, c)
        yield (None, True, c)
    for p in M.POSSESSIVES:
        for c in M.CASES:            # iyelik + hal (3.şh dahil)
            yield (p, False, c)
        yield (p, True, "nom")
    yield ("px3sp", False, "attr")   # 3.şh + sıfat-fiil (районӗнчи)


# Üretken türetim ekleri (uzun -> kısa sıralı eşleşme) ve ürettiği POS
_DERIV_SUFFIXES = [
    ("чӑлӑх", "n"), ("чӗлӗх", "n"), ("лӑх", "n"), ("лӗх", "n"),
    ("сӑр", "adj"), ("сӗр", "adj"), ("ҫӑ", "n"), ("ҫӗ", "n"),
    ("лӑ", "adj"), ("лӗ", "adj"), ("лан", "v"), ("лен", "v"),
    ("ла", "v"), ("ле", "v"), ("ӑш", "n"), ("ӗш", "n"),
]


def _verb_combos():
    for tense in ("pres", "past", "fut"):
        for person in M.PERSONS:
            yield (tense, person, False)
            yield (tense, person, True)
    for person in M.PERSONS:
        yield ("imp", person, False)
    yield ("inf", None, False)
    # çekimsiz/yarı-çekimli: partisip, zarf-fiil, sıfat-fiiller
    for form in ("nar", "cvb", "ppres", "pfut"):
        yield (form, None, False)
    yield ("nar", None, True)


class Analyzer:
    def __init__(self, lexicon: Lexicon):
        self.lex = lexicon
        self.ng = NounGenerator(lexicon)
        self.vg = VerbGenerator(lexicon)

    def _candidate_stems(self, word: str):
        """Yüzey kelimeden olası kökleri topla (prefix + ünlü-restorasyonu +
        palatalizasyon tersine). Üret-ve-doğrula tam form eşleşmesiyle filtreler,
        bu yüzden fazla aday yalnızca recall artırır, precision'ı düşürmez."""
        cands = set()
        for k in range(2, len(word) + 1):
            p = word[:k]
            if self.lex.lookup(p):
                cands.add(p)
            # ünlü-sonu kök, iyelik/hal ile son ünlüyü değiştirmiş olabilir
            # (республик+а -> республик+и); ön-eke ünlü ekleyerek dene
            for v in "аеӑӗиоуӳ":
                if self.lex.lookup(p + v):
                    cands.add(p + v)
            # palatalizasyon: yüzeydeki ч, kökte т/д olabilir (ят -> ячӗ)
            if p.endswith("ч"):
                for c in "тд":
                    if self.lex.lookup(p[:-1] + c):
                        cands.add(p[:-1] + c)
        return cands

    def analyze(self, word: str) -> AnalysisResult:
        word = normalize(word.strip())
        seen = set()
        parses: List[Parse] = []

        for stem in self._candidate_stems(word):
            entries = self.lex.lookup(stem)
            poses = {e.pos for e in entries}
            gloss = next((e.gloss_ru for e in entries if e.gloss_ru), "")

            if poses & {"n", "np", "adj", "prn", "num"}:
                for poss, plural, case in _noun_combos():
                    r = self.ng.generate(stem, possessive=poss,
                                          plural=plural, case=case)
                    if r.valid and r.word == word and r.analysis not in seen:
                        seen.add(r.analysis)
                        parses.append(Parse(stem, "n", r.analysis,
                                            r.breakdown, gloss))

            if "v" in poses:
                for tense, person, neg in _verb_combos():
                    r = self.vg.generate(stem, tense, person, neg)
                    if r.word == word and r.analysis not in seen:
                        seen.add(r.analysis)
                        parses.append(Parse(stem, "v", r.analysis,
                                            r.breakdown, gloss))

        # Türetim: kelime = kök + üretken türetim eki (bare türetilmiş biçim)
        if not parses:
            for suf, outpos in _DERIV_SUFFIXES:
                if word.endswith(suf) and len(word) - len(suf) >= 2:
                    base = word[: -len(suf)]
                    if self.lex.lookup(base):
                        tag = f"{base}<{outpos}><der>"
                        if tag not in seen:
                            seen.add(tag)
                            g = next((e.gloss_ru for e in self.lex.lookup(base)
                                      if e.gloss_ru), "")
                            parses.append(Parse(base, outpos, tag,
                                                f"{base} + {suf}", g))
                        break

        # Çekimsiz/yalın sözlük kelimesi (zarf, bağlaç, edat, ünlem, yalın isim…):
        # üretici bir çekim bulamadıysa ama kelime aynen sözlükteyse tanı.
        if not parses:
            for e in self.lex.lookup(word):
                tag = f"{word}<{e.pos}>"
                if tag not in seen:
                    seen.add(tag)
                    parses.append(Parse(word, e.pos, tag, word, e.gloss_ru))

        return AnalysisResult(word, parses)

    def is_valid(self, word: str) -> bool:
        """Yazım denetimi: kelime geçerli bir Çuvaşça biçim mi?"""
        return self.analyze(word).success
