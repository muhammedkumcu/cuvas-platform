#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""U1 — her dilin GEÇERLİ hâl envanteri (FST'den, autogen ile doğrudan). VM'de çalışır.
Üreteç bu envanterle dile-duyarlı olur: o dilde üretmeyen hâli işaretler/gizler."""
import hfst, glob, os, json, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.expanduser("~/.turkicnlp/models")
SEED = {"tur": "ev", "aze": "ev", "kaz": "бала", "kir": "бала", "uzb": "uy", "uig": "كىتاب",
        "tat": "кул", "bak": "китап", "chv": "хӗр", "sah": "ат", "tuk": "kitap", "crh": "kitap",
        "gag": "kitap", "kaa": "kitap", "alt": "ат", "kjh": "ат", "krc": "ат", "kum": "ат",
        "nog": "ат", "tyv": "ат"}
CASES = ["nom", "gen", "dat", "acc", "loc", "abl", "ins"]


def autogen(lang):
    h = glob.glob(f"{BASE}/{lang}/**/{lang}.autogen.hfst", recursive=True)
    return hfst.HfstInputStream(h[0]).read() if h else None


FEAT = {}
for lang, s in SEED.items():
    g = autogen(lang)
    if not g:
        continue
    ok = []
    for c in CASES:
        if g.lookup(s + f"<n><{c}>") or (c == "nom" and g.lookup(s + "<n>")):
            ok.append(c)
    FEAT[lang] = ok
print(json.dumps(FEAT, ensure_ascii=False))
