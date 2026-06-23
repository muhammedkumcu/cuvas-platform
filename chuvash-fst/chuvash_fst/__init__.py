# -*- coding: utf-8 -*-
"""
ChuvashFST — Çuvaş Türkçesi için kural tabanlı morfolojik üretim/analiz motoru
ve ICALL öğrenme platformunun çekirdeği.

Düşük kaynaklı, Oğur (Bulgar) kolu Türk dili Çuvaşça (chv) için.
"""
from .phonology import Alphabet, Phonology, normalize, has_latin_homoglyph
from .lexicon import Lexicon, Entry
from .generator import NounGenerator, GenResult
from . import morphotactics

__version__ = "0.1.0"

__all__ = [
    "Alphabet",
    "Phonology",
    "normalize",
    "has_latin_homoglyph",
    "Lexicon",
    "Entry",
    "NounGenerator",
    "GenResult",
    "morphotactics",
]
