# -*- coding: utf-8 -*-
"""
enrich_from_hunspell.py — Hunspell cv_RU sözlüğünden (Çuvaş yazım denetimi,
GPLv3/LGPLv3/MPL) kökleri ekler. Üçüncü bağımsız kaynak.

Flag -> POS (cv_RU.aff incelemesinden):
  1,2,9  -> n    (сем/ӗн/и hal-iyelik ekleri)
  5,6,10 -> adj  (скер/рах karşılaştırma)
  7,8    -> v    (атӑп/етӗп fiil çekimi)
  büyük harf başlangıç -> np
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path("chuvash-fst")))
from chuvash_fst.phonology import normalize  # noqa: E402

DIC = Path("sources/hunspell_cv/cv_RU.dic")
SEED = Path("chuvash-fst/data/chuvash_lexicon_seed.txt")

POS_BY_FLAG = {"1": "n", "2": "n", "9": "n",
               "5": "adj", "6": "adj", "10": "adj",
               "7": "v", "8": "v"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    have = {l.split("\t")[0].strip().lower()
            for l in SEED.open(encoding="utf-8") if l.strip()}

    lines = DIC.read_text(encoding="utf-8").splitlines()[1:]  # ilk satır = sayı
    new = {}  # lemma -> pos
    from collections import Counter
    pos_count = Counter()
    for raw in lines:
        if not raw.strip():
            continue
        word, _, flags = raw.partition("/")
        is_proper = word[:1].isupper()
        lemma = normalize(word).lower().strip()
        if not lemma or len(lemma) < 2:
            continue
        if is_proper:
            pos = "np"
        else:
            fset = set(flags.replace(",", " ").split())
            pos = next((POS_BY_FLAG[f] for f in fset if f in POS_BY_FLAG), "n")
        if lemma in have or lemma in new:
            continue
        new[lemma] = pos
        pos_count[pos] += 1

    with SEED.open("a", encoding="utf-8") as f:
        for lemma, pos in new.items():
            f.write(f"{lemma}\t%<{pos}%>\tsrc:hunspell\n")

    print(f"Hunspell girişi: {len(lines)} · sözlüğümüzde olmayan yeni kök: {len(new)}")
    print("POS dağılımı:", dict(pos_count))
    print(f"Yeni toplam: ~{len(have)+len(new)}")


if __name__ == "__main__":
    main()
