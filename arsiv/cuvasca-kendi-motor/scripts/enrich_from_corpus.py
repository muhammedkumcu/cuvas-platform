# -*- coding: utf-8 -*-
"""
enrich_from_corpus.py — Corpus'taki sık TANINMAYAN kelimelerden eksik KÖKLERİ
otomatik keşfeder (üret-ve-doğrula / generate-and-verify yöntemi, Türkmence'deki gibi).

Her tanınmayan T için: en uzun p ön-eki bul ki p'nin isim paradigmasında T geçsin
(ör. облаҫӗ -> облаҫ). Yoksa T'nin kendisi kök kabul edilir (ör. раҫҫей).
Keşfedilen kökler `src:corpus` ile sözlüğe eklenir.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path("chuvash-fst")))
from chuvash_fst.generator import NounGenerator  # noqa: E402
from chuvash_fst import morphotactics as M  # noqa: E402

SEED = Path("chuvash-fst/data/chuvash_lexicon_seed.txt")
REPORT = Path("chuvash-fst/data/coverage_report.json")
STOP = {"км", "ао", "ам", "та", "ту", "са", "не", "пе"}  # kısaltma/ek-benzeri


def noun_forms(ng, stem):
    """Bir kökün üreteceği tüm isim yüzey biçimleri."""
    forms = set()
    for c in M.CASES:
        forms.add(ng.generate(stem, case=c).word)
        forms.add(ng.generate(stem, plural=True, case=c).word)
    for p in M.POSSESSIVES:
        for c in M.CASES:
            forms.add(ng.generate(stem, possessive=p, case=c).word)
    return forms


def discover_stem(ng, token):
    """En uzun (token'dan kısa) kök ön-ekini bul; yoksa token'ın kendisi."""
    for k in range(len(token) - 1, 2, -1):
        p = token[:k]
        if token in noun_forms(ng, p):
            return p
    return token


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    have = {l.split("\t")[0].strip().lower()
            for l in SEED.open(encoding="utf-8") if l.strip()}
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    ng = NounGenerator()  # sözlüksüz (gemination yok) — keşif için yeterli

    discovered = {}
    for token, freq in report["top_unrecognized"]:
        if freq < 3 or len(token) < 3 or token in STOP:
            continue
        stem = discover_stem(ng, token)
        if stem and stem not in have and stem not in discovered and len(stem) >= 3:
            discovered[stem] = freq

    with SEED.open("a", encoding="utf-8") as f:
        for stem, freq in sorted(discovered.items(), key=lambda x: -x[1]):
            f.write(f"{stem}\t%<n%>\tsrc:corpus\n")

    print(f"Keşfedilen ve eklenen kök: {len(discovered)}")
    print("Örnekler:", ", ".join(f"{s}({f})" for s, f in
                                  sorted(discovered.items(), key=lambda x: -x[1])[:25]))


if __name__ == "__main__":
    main()
