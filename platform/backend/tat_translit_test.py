#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tatarca UniMorph (Latin) -> Kiril harf-çevirisi DENEMESİ (FST Kiril; doğruluk ölçmek için).
DÜRÜSTLÜK testi: çeviri kötüyse tanıma düşük çıkar → o zaman 'güvenilir değil' deriz, sayı VERMEYİZ."""
import json, urllib.request, sys, os, random
sys.stdout.reconfigure(encoding="utf-8")
API = "http://127.0.0.1:8000"
random.seed(42)


def lat2cyr(s):
    s = s.lower()
    for a, b in [("ya", "я"), ("yä", "я"), ("yu", "ю"), ("yü", "ю"), ("yo", "йо"),
                 ("yı", "йы"), ("yi", "йи"), ("ye", "е")]:
        s = s.replace(a, b)
    m = {"a": "а", "ä": "ә", "b": "б", "c": "җ", "ç": "ч", "d": "д", "e": "е", "f": "ф",
         "g": "г", "ğ": "г", "h": "һ", "ı": "ы", "i": "и", "j": "ж", "k": "к", "q": "к",
         "l": "л", "m": "м", "n": "н", "ñ": "ң", "o": "о", "ö": "ө", "p": "п", "r": "р",
         "s": "с", "ş": "ш", "t": "т", "u": "у", "ü": "ү", "v": "в", "w": "в", "x": "х",
         "y": "й", "z": "з", "'": "", "’": ""}
    return "".join(m.get(c, c) for c in s)


def post(p, d):
    r = urllib.request.Request(API + p, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=20))


path = os.path.join(os.path.dirname(__file__), "..", "..", "sources", "tat", "tat")
rows = []
for line in open(path, encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) == 3 and p[2].startswith("N") and " " not in p[1]:
        rows.append((p[0], p[1]))
sample = random.sample(rows, min(1000, len(rows)))
seen = recog = lemma_ok = 0
ex = []
for lemma, form in sample:
    cform, clemma = lat2cyr(form), lat2cyr(lemma)
    d = post("/analyze", {"lang": "tat", "word": cform})
    seen += 1
    an = d.get("analyses", [])
    if an:
        recog += 1
        if clemma in {a.get("lemma", "").lower() for a in an}:
            lemma_ok += 1
        elif len(ex) < 4:
            ex.append(f"{form}->{cform}: gold={clemma} bizde={sorted({a['lemma'] for a in an})[:2]}")
print(f"tat (Latin->Kiril çeviri): örnek={seen} tanıma={100*recog/seen:.1f}% "
      f"lemma={100*lemma_ok/recog if recog else 0:.1f}%")
print("KARAR: tanıma >%60 ise çeviri güvenilir, tat'a sayı eklenebilir; düşükse 'dış gold yok' kalır.")
for e in ex:
    print("  ", e)
