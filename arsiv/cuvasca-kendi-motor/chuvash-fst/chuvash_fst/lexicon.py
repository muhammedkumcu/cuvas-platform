# -*- coding: utf-8 -*-
"""
ChuvashFST — Sözlük Modülü (lexicon.py)

Sözlük formatı (Türkmence projesiyle uyumlu):
    lemma<TAB>%<pos%>[<TAB>özellik;özellik;...]

POS etiketleri: %<n%> %<v%> %<adj%> %<adv%> %<np%> %<num%> %<prn%> %<post%> %<cnj%> ...
Özellikler: ru:<gloss>, gemination, reduced_drop, no_harmony, vb.
Kökler Çuvaş Kiril (UTF-8) tutulur.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Iterable

from .phonology import normalize

_POS_RE = re.compile(r"%<([^>]+)%>")


@dataclass
class Entry:
    lemma: str
    pos: str
    features: Dict[str, str] = field(default_factory=dict)
    flags: frozenset = field(default_factory=frozenset)
    gloss_ru: str = ""

    def has(self, flag: str) -> bool:
        return flag in self.flags


class Lexicon:
    """Kök sözlüğünü yükler ve sorgular."""

    def __init__(self) -> None:
        # lemma -> [Entry, ...] (eş sesli kelimeler için liste)
        self._by_lemma: Dict[str, List[Entry]] = {}
        self._by_pos: Dict[str, List[Entry]] = {}
        self.count = 0

    # -- Yükleme --------------------------------------------------------------

    def load(self, path: str | Path) -> "Lexicon":
        path = Path(path)
        with path.open(encoding="utf-8") as f:
            for raw in f:
                line = raw.rstrip("\n")
                if not line or line.startswith("#"):
                    continue
                self._add_line(line)
        return self

    def _add_line(self, line: str) -> None:
        parts = line.split("\t")
        if len(parts) < 2:
            return
        lemma = normalize(parts[0].strip())
        m = _POS_RE.search(parts[1])
        pos = m.group(1) if m else parts[1].strip()

        flags = set()
        feats: Dict[str, str] = {}
        gloss = ""
        for chunk in parts[2:]:
            for tok in chunk.split(";"):
                tok = tok.strip()
                if not tok:
                    continue
                if tok.startswith("ru:"):
                    gloss = tok[3:].strip()
                elif ":" in tok:
                    k, _, v = tok.partition(":")
                    feats[k.strip()] = v.strip()
                else:
                    flags.add(tok)

        entry = Entry(lemma=lemma, pos=pos, features=feats,
                      flags=frozenset(flags), gloss_ru=gloss)
        self._by_lemma.setdefault(lemma, []).append(entry)
        self._by_pos.setdefault(pos, []).append(entry)
        self.count += 1

    # -- Sorgu ----------------------------------------------------------------

    def lookup(self, word: str) -> List[Entry]:
        return self._by_lemma.get(normalize(word), [])

    def __contains__(self, word: str) -> bool:
        return normalize(word) in self._by_lemma

    def by_pos(self, pos: str) -> List[Entry]:
        return self._by_pos.get(pos, [])

    def nouns(self) -> List[Entry]:
        return self.by_pos("n")

    def verbs(self) -> List[Entry]:
        return self.by_pos("v")

    def adjectives(self) -> List[Entry]:
        return self.by_pos("adj")

    def all_entries(self) -> Iterable[Entry]:
        for entries in self._by_lemma.values():
            yield from entries

    def stats(self) -> Dict[str, int]:
        return {pos: len(entries) for pos, entries in sorted(self._by_pos.items())}
