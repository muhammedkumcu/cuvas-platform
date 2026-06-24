# -*- coding: utf-8 -*-
"""
validate_wiktionary.py — Wiktionary Çuvaşça lemmalarını (apertium'dan BAĞIMSIZ)
çekip kendi sözlüğümüzle çapraz doğrular.

- Category:Chuvash lemmas üyelerini MediaWiki API ile sayfalayarak indirir.
- Kiril tek-kelime lemmaları süzer.
- Seed sözlüğümüzle örtüşme oranını raporlar (döngüsel olmayan doğrulama).
- Listeyi data/wiktionary_chv_lemmas.txt olarak kaydeder (sözlük zenginleştirme adayı).
"""
from __future__ import annotations
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://en.wiktionary.org/w/api.php"
SEED = Path("chuvash-fst/data/chuvash_lexicon_seed.txt")
OUT = Path("chuvash-fst/data/wiktionary_chv_lemmas.txt")
CYR = set("абвгдежзийклмнопрстуфхцчшщъыьэюяёӑӗҫӳ")


def fetch_category(cat: str):
    members, cont = [], None
    while True:
        params = {
            "action": "query", "list": "categorymembers",
            "cmtitle": f"Category:{cat}", "cmlimit": "500",
            "cmtype": "page", "format": "json",
        }
        if cont:
            params["cmcontinue"] = cont
        url = API + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "ChuvashFST-research/0.1"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        members += [m["title"] for m in data["query"]["categorymembers"]]
        cont = data.get("continue", {}).get("cmcontinue")
        if not cont:
            break
        time.sleep(0.3)
    return members


def is_cyr_word(t: str) -> bool:
    t = t.strip().lower()
    if not t or " " in t:
        return False
    return all(c in CYR or c == "-" for c in t)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("Wiktionary Category:Chuvash lemmas çekiliyor…")
    titles = fetch_category("Chuvash lemmas")
    lemmas = sorted({t.strip().lower() for t in titles if is_cyr_word(t)})
    print(f"Toplam üye: {len(titles)} · Kiril tek-kelime lemma: {len(lemmas)}")

    OUT.write_text("\n".join(lemmas) + "\n", encoding="utf-8")
    print(f"Kaydedildi: {OUT}")

    # seed sözlükle örtüşme (BAĞIMSIZ doğrulama)
    our = set()
    for line in SEED.open(encoding="utf-8"):
        if line.strip():
            our.add(line.split("\t")[0].strip().lower())
    overlap = [l for l in lemmas if l in our]
    missing = [l for l in lemmas if l not in our]
    print(f"\n--- BAĞIMSIZ ÇAPRAZ DOĞRULAMA (Wiktionary ⟂ apertium) ---")
    print(f"Wiktionary lemma: {len(lemmas)}")
    print(f"Sözlüğümüzde bulunan: {len(overlap)} (%{100*len(overlap)/max(len(lemmas),1):.1f})")
    print(f"Sözlüğümüzde olmayan (zenginleştirme adayı): {len(missing)}")
    print("Örnek eksikler:", ", ".join(missing[:25]))


if __name__ == "__main__":
    main()
