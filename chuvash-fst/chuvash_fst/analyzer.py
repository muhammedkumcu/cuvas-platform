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
    for c in M.CASES:
        yield (None, False, c)
        yield (None, True, c)
    for p in M.POSSESSIVES:
        yield (p, False, "nom")
        yield (p, True, "nom")


def _verb_combos():
    for tense in ("pres", "past", "fut"):
        for person in M.PERSONS:
            yield (tense, person, False)
            yield (tense, person, True)
    for person in M.PERSONS:
        yield ("imp", person, False)
    yield ("inf", None, False)


class Analyzer:
    def __init__(self, lexicon: Lexicon):
        self.lex = lexicon
        self.ng = NounGenerator(lexicon)
        self.vg = VerbGenerator(lexicon)

    def analyze(self, word: str) -> AnalysisResult:
        word = normalize(word.strip())
        seen = set()
        parses: List[Parse] = []

        # aday kökler: kelimenin sözlükteki ön ekleri (+ tam kelime)
        for k in range(2, len(word) + 1):
            stem = word[:k]
            entries = self.lex.lookup(stem)
            if not entries:
                continue
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

        return AnalysisResult(word, parses)

    def is_valid(self, word: str) -> bool:
        """Yazım denetimi: kelime geçerli bir Çuvaşça biçim mi?"""
        return self.analyze(word).success
