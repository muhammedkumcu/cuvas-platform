#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yüzey bölümleme ROUND-TRIP değerlendirmesi (10 MVP dili).
Mantık: bilinen etiketlerden form ÜRET (gold) → /segment ile çöz → beklenen ek sayısı +
yeniden-üretim tutuyor mu? Gold = üretilen formun etiket yapısı. VM'de (localhost:8000) çalışır.
Çıktı: dil başına nw-align oranı, ek-sayısı doğruluğu, örnek başarısızlıklar.
"""
import json, urllib.request, sys
sys.stdout.reconfigure(encoding="utf-8")
API = "http://127.0.0.1:8000"

# aday isim kökleri (geçersizler otomatik elenir: gen(lemma<n><nom>) boşsa atılır)
SEEDS = {
    "tur": ["ev", "kitap", "göz", "ağaç", "çocuk", "yol", "kuş", "renk", "el", "su", "kanat", "burun"],
    "aze": ["ev", "kitab", "göz", "ağac", "yol", "əl", "su", "daş", "qız", "dağ"],
    "kaz": ["үй", "кітап", "көз", "бала", "жол", "қала", "ат", "ел", "су", "кітеп"],
    "kir": ["үй", "китеп", "көз", "бала", "жол", "тоо", "ат", "эл", "суу", "кыз"],
    "uzb": ["uy", "kitob", "koʻz", "bola", "yoʻl", "ish", "ot", "el", "suv", "qiz"],
    "uig": ["كىتاب", "ئۆي", "كۆز", "بالا", "يول", "ئىش", "ئات", "قىز", "سۇ"],  # Arap yazısı (FST böyle bekler)
    "tat": ["йорт", "китап", "күз", "бала", "юл", "авыл", "кул", "ат", "ел", "кыз"],
    "bak": ["өй", "китап", "күҙ", "бала", "юл", "ат", "ел", "һыу", "ҡыҙ"],
    "chv": ["ҫурт", "кӗнеке", "куҫ", "ача", "ҫул", "хӗр", "ял", "ал", "вӑрман"],
    "sah": ["дьиэ", "кинигэ", "харах", "оҕо", "суол", "ат", "ыал", "уу", "кыыс"],
    # --- E5: 10 yeni dil (geniş aday havuzu; geçersizler gen(<n><nom>) ile otomatik elenir) ---
    "tuk": ["kitap", "at", "öý", "göz", "suw", "ýol", "gün", "el", "baş", "daş", "gyz", "ene"],
    "crh": ["kitap", "at", "ev", "köz", "suv", "yol", "kün", "el", "qol", "baş", "taş", "qız"],
    "gag": ["kitap", "ev", "göz", "su", "yol", "gün", "el", "kol", "baş", "taş", "dil", "ana"],
    "kaa": ["kitap", "at", "úy", "kóz", "suw", "jol", "kún", "el", "qol", "bas", "tas", "qız"],
    "alt": ["ат", "айыл", "кӧс", "суу", "јол", "кӱн", "эл", "кол", "баш", "таш", "бичик", "эне"],
    "kjh": ["ат", "иб", "харах", "суг", "чол", "кӱн", "чир", "хол", "пас", "тас", "ном", "ине"],
    "krc": ["ат", "юй", "кёз", "суу", "джол", "кюн", "эл", "къол", "баш", "таш", "китап", "ана"],
    "kum": ["ат", "уьй", "гёз", "сув", "ёл", "гюн", "эл", "къол", "баш", "таш", "китап", "ана"],
    "nog": ["ат", "уьй", "коьз", "сув", "йол", "кун", "эл", "кол", "бас", "тас", "китап", "ана"],
    "tyv": ["ат", "ӧг", "карак", "суг", "орук", "хүн", "чер", "хол", "баш", "даш", "ном", "ие"],
}
CASES = ["nom", "gen", "dat", "acc", "loc", "abl"]
PXS = ["px1sg", "px1pl", "px3sp"]


def post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))


def get(path):
    return json.load(urllib.request.urlopen(API + path, timeout=20))


def gen(lang, query):
    d = post("/generate", {"lang": lang, "query": query})
    fs = d.get("forms", [])
    if not fs and query.endswith("<nom>"):   # Türkmen vb. yalın hâl İŞARETSİZ → <nom>'suz tekrar dene
        d = post("/generate", {"lang": lang, "query": query[:-5]})
        fs = d.get("forms", [])
    return fs[0]["surface"] if fs else None


def combos():
    out = []
    for c in CASES:
        out.append((["pl"] if False else []) + [c])  # tekil hâl
    for c in ["nom", "loc", "abl", "dat"]:
        out.append(["pl", c])
    for px in PXS:
        for c in ["nom", "loc", "dat"]:
            out.append([px, c])
    out.append(["pl", "px1pl", "loc"])
    out.append(["pl", "px1sg", "abl"])
    return out


def expected_affixes(tags):
    # nom dışı çekim eki sayısı: pl + px + (case!=nom)
    n = 0
    for t in tags:
        if t == "pl" or t.startswith("px") or (t in CASES and t != "nom"):
            n += 1
    return n


def main():
    grand = {}
    for lang, seeds in SEEDS.items():
        valid = [s for s in seeds if gen(lang, f"{s}<n><nom>")]
        total = ok_align = ok_count = recon = 0
        methods = {}
        fails = []
        for lemma in valid:
            for tags in combos():
                q = f"{lemma}<n>" + "".join(f"<{t}>" for t in tags)
                form = gen(lang, q)
                if not form:
                    continue
                total += 1
                d = post("/segment", {"lang": lang, "word": form})
                m = d.get("method", "?")
                methods[m] = methods.get(m, 0) + 1
                if m == "nw-align":
                    ok_align += 1
                exp = expected_affixes(tags)
                got = len(d.get("morphemes", [])) - 1
                cnt_ok = (got == exp)
                if cnt_ok:
                    ok_count += 1
                # yüzey yeniden-üretim: ekleri (lemma kökü hariç) form'un sonuna ekleyince eşleşmeli
                affixes = "".join(x["surface"] for x in d.get("morphemes", [])[1:])
                if affixes and form.endswith(affixes):
                    recon += 1
                if not cnt_ok and len(fails) < 4:
                    seg = "+".join(x["surface"] for x in d.get("morphemes", []))
                    fails.append(f"{form} [{'+'.join(tags)}] beklenen ek={exp} -> {seg} ({m})")
        grand[lang] = (len(valid), total, ok_align, ok_count, recon, methods, fails)

    print("=" * 78)
    print(f"{'dil':4} {'kök':4} {'form':5} {'align%':7} {'ekSay%':7} {'yenidn%':8}  yöntemler")
    print("-" * 78)
    for lang, (nv, tot, al, oc, rc, meth, fails) in grand.items():
        if tot == 0:
            print(f"{lang:4} {nv:4} {tot:5}  (üretim yok / FST kapsamı eksik)")
            continue
        print(f"{lang:4} {nv:4} {tot:5} {100*al/tot:6.1f}% {100*oc/tot:6.1f}% {100*rc/tot:7.1f}%  {meth}")
    print("-" * 78)
    for lang, (nv, tot, al, oc, rc, meth, fails) in grand.items():
        if fails:
            print(f"\n[{lang}] örnek ek-sayısı tutmayanlar:")
            for f in fails:
                print("   ", f)


if __name__ == "__main__":
    main()
