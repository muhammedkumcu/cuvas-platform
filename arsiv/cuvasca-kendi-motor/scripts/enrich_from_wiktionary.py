# -*- coding: utf-8 -*-
"""
enrich_from_wiktionary.py — Wiktionary POS alt-kategorilerini çekip
sözlüğümüzde OLMAYAN Çuvaşça kelimeleri ekler (BAĞIMSIZ ikinci kaynak).

Sözlük çok-kaynaklı hale gelir: apertium-chv (birincil) + Wiktionary (CC BY-SA).
Eklenen girişler `src:wikt` özelliğiyle işaretlenir (köken takibi).
"""
from __future__ import annotations
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path

API = "https://en.wiktionary.org/w/api.php"
SEED = Path("chuvash-fst/data/chuvash_lexicon_seed.txt")
CYR = set("абвгдежзийклмнопрстуфхцчшщъыьэюяёӑӗҫӳ")

# Wiktionary alt-kategori -> bizim POS kodu
SUBCATS = {
    "Chuvash nouns": "n", "Chuvash verbs": "v", "Chuvash adjectives": "adj",
    "Chuvash adverbs": "adv", "Chuvash numerals": "num",
    "Chuvash proper nouns": "np", "Chuvash pronouns": "prn",
}


def fetch_category(cat):
    out, cont = [], None
    while True:
        p = {"action": "query", "list": "categorymembers", "cmtitle": f"Category:{cat}",
             "cmlimit": "500", "cmtype": "page", "format": "json"}
        if cont:
            p["cmcontinue"] = cont
        req = urllib.request.Request(API + "?" + urllib.parse.urlencode(p),
                                     headers={"User-Agent": "ChuvashFST-research/0.1"})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        out += [m["title"] for m in d["query"]["categorymembers"]]
        cont = d.get("continue", {}).get("cmcontinue")
        if not cont:
            break
        time.sleep(0.3)
    return out


def is_cyr_word(t):
    t = t.strip().lower()
    return bool(t) and " " not in t and not t.startswith("-") and len(t) >= 2 \
        and all(c in CYR or c == "-" for c in t)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    # mevcut sözlük (lemma,pos)
    have = set()
    have_lemma = set()
    for line in SEED.open(encoding="utf-8"):
        if line.strip():
            parts = line.split("\t")
            lemma = parts[0].strip().lower()
            pos = parts[1].strip("%<>") if len(parts) > 1 else ""
            have.add((lemma, pos))
            have_lemma.add(lemma)

    wikt = {}  # lemma -> pos (ilk gelen POS)
    for cat, pos in SUBCATS.items():
        print(f"çekiliyor: {cat} …")
        for t in fetch_category(cat):
            w = t.strip().lower()
            if is_cyr_word(w) and w not in wikt:
                wikt[w] = pos

    print(f"\nWiktionary POS'lu Çuvaşça kelime: {len(wikt)}")
    # eklenecekler: bizde HİÇ olmayan lemmalar (yeni içerik)
    new = {w: p for w, p in wikt.items() if w not in have_lemma}
    print(f"Sözlüğümüzde hiç olmayan (eklenecek): {len(new)}")

    with SEED.open("a", encoding="utf-8") as f:
        for w, p in sorted(new.items()):
            f.write(f"{w}\t%<{p}%>\tsrc:wikt\n")

    # POS örtüşme kontrolü (ortak lemmalarda POS uyuşması — bağımsız doğrulama)
    common = [(w, p) for w, p in wikt.items() if w in have_lemma]
    agree = sum(1 for w, p in common if (w, p) in have)
    print(f"\nOrtak lemma (POS karşılaştırılabilir): {len(common)}")
    print(f"POS uyuşması: {agree} (%{100*agree/max(len(common),1):.1f})")
    print(f"\nEklendi: {len(new)} giriş (src:wikt). Yeni toplam ~{len(have)+len(new)}")


if __name__ == "__main__":
    main()
