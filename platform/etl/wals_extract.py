#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WALS CLDF -> tipolojik mesafe + özellik matrisi (kaynaklı JSON).

Kaynak  : WALS Online CLDF (github.com/cldf-datasets/wals)
Lisans  : CC BY 4.0
Erişim  : 2026-06-24 (yerel: sources/wals)

Üretir (platform/data/):
  - distance.typological.json : dil x dil tipolojik mesafe (ortak özniteliklerde farklılık oranı) -> Uzaklık(tipolojik)
  - features.wals.json        : dil -> {özellik: değer} + özellik/değer sözlükleri -> Özellik Matrisi

İLKE: yalnız WALS'ta attested olan özellikler; bir dilde özellik yoksa atlanır (uydurma yok).
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
W = ROOT / "sources" / "wals" / "cldf"
OUT = ROOT / "platform" / "data"; OUT.mkdir(parents=True, exist_ok=True)
META = {"source": "WALS Online CLDF", "license": "CC BY 4.0",
        "url": "https://github.com/cldf-datasets/wals", "accessed": "2026-06-24"}

# our_iso -> tercih edilen WALS dil id'si (standart çeşit)
PICK = {"tur":"tur","azj":"aze","tuk":"tkm","kaz":"kaz","kir":"kgz","tat":"tvo","bak":"bsk",
        "uig":"uyg","uzb":"uzb","chv":"chv","sah":"ykt","tyv":"tuv","kjh":"khk","cjs":"shr",
        "klj":"khl","gag":"gag","crh":"cri","kaa":"kkp","kum":"kuq","krc":"krc","nog":"nog",
        "dlg":"dol","alt":"aso"}
MVP = {"tur","azj","kaz","kir","uzb","uig","tat","bak","chv","sah"}
BRANCH = {"chv":"Ogur","tur":"Oğuz","azj":"Oğuz","tuk":"Oğuz","gag":"Oğuz","tat":"Kıpçak","bak":"Kıpçak",
          "kaz":"Kıpçak","kir":"Kıpçak","crh":"Kıpçak","kaa":"Kıpçak","kum":"Kıpçak","krc":"Kıpçak",
          "nog":"Kıpçak","uzb":"Karluk","uig":"Karluk","sah":"Sibirya","tyv":"Sibirya","kjh":"Sibirya",
          "cjs":"Sibirya","dlg":"Sibirya","alt":"Sibirya","klj":"Argu"}


def read(name):
    with open(W / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    wals_ids = set(PICK.values())
    iso_of = {w: iso for iso, w in PICK.items()}
    params = {p["ID"]: p["Name"] for p in read("parameters.csv")}
    codes = {c["ID"]: c["Name"] for c in read("codes.csv")}

    # değer vektörleri (yalnız seçili dillerin satırları)
    vec = {iso: {} for iso in PICK}                # iso -> {param_id: code_id}
    with open(W / "values.csv", encoding="utf-8") as f:
        for v in csv.DictReader(f):
            lid = v["Language_ID"]
            if lid in wals_ids and v["Code_ID"]:
                vec[iso_of[lid]][v["Parameter_ID"]] = v["Code_ID"]

    isos = [i for i in PICK if vec[i]]             # veri olan diller

    # tipolojik mesafe: ortak attested özniteliklerde farklılık oranı
    matrix = {}
    for a in isos:
        matrix[a] = {}
        for b in isos:
            if a == b:
                matrix[a][b] = {"distance": 0.0, "shared": None, "diff": None}
                continue
            shared = [p for p in vec[a] if p in vec[b]]
            diff = sum(1 for p in shared if vec[a][p] != vec[b][p])
            n = len(shared)
            matrix[a][b] = {"distance": round(diff / n, 4) if n else None, "shared": n, "diff": diff}

    json.dump({"_meta": {**META, "module": "Uzaklık Gezgini (tipolojik eksen)",
                         "method": "ortak attested WALS özniteliğinde farklı değer oranı (normalize Hamming)"},
               "matrix": matrix},
              open(OUT / "distance.typological.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # özellik matrisi (değer etiketleriyle)
    feats = {}
    for iso in isos:
        feats[iso] = {"name": iso, "branch": BRANCH.get(iso), "mvp": iso in MVP,
                      "values": {p: {"code": c, "label": codes.get(c)} for p, c in vec[iso].items()}}
    json.dump({"_meta": {**META, "module": "Özellik Matrisi"},
               "parameters": params, "languages": feats},
              open(OUT / "features.wals.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"distance.typological.json : {len(isos)} dil; features.wals.json : {len(params)} özellik tanımı")
    print(f"diller (öznitelik sayısı): " + ", ".join(f"{i}({len(vec[i])})" for i in isos))
    print("--- sanity: Çuvaşça tipolojik mesafe ---")
    for b in ["tur","tat","kaz","uzb","uig","sah","klj","azj"]:
        d = matrix.get("chv", {}).get(b, {})
        print(f"  chv–{b}: mesafe={d.get('distance')} (ortak {d.get('shared')} özn., {d.get('diff')} farklı)")


if __name__ == "__main__":
    main()
