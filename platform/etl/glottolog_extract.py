#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Glottolog CLDF -> dil profilleri + canlılık (kaynaklı JSON).

Kaynak  : Glottolog 5.x CLDF (github.com/glottolog/glottolog-cldf)
Lisans  : CC BY 4.0
Erişim  : 2026-06-24 (yerel: sources/glottolog-cldf)

Üretir: platform/data/profiles.json
  - dil kimliği (glottocode/iso/koordinat/ülkeler) + kol + AES canlılık (açık, EGIDS/UNESCO eşlemeli)

AES = Agglomerated Endangerment Status (1-6) — Ethnologue/EGIDS'in AÇIK alternatifi.
İLKE: yalnız kaynakta olan; AES yoksa null (uydurma yok).
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GL = ROOT / "sources" / "glottolog-cldf" / "cldf"
OUT = ROOT / "platform" / "data"; OUT.mkdir(parents=True, exist_ok=True)

META = {"source": "Glottolog 5.x CLDF", "license": "CC BY 4.0",
        "url": "https://github.com/glottolog/glottolog-cldf", "accessed": "2026-06-24"}

# hedef diller (ISO 639-3) — MVP 10 + tehlikedeki odak + diğer kollar
TARGET = {"tur","azj","tuk","kaz","kir","tat","bak","uig","uzb","chv","sah",
          "tyv","kjh","cjs","klj","gag","crh","kaa","kum","krc","nog","dlg","alt"}
MVP = {"tur","azj","kaz","kir","uzb","uig","tat","bak","chv","sah"}
ISO_BRANCH = {
    "chv":"Ogur",
    "tur":"Oğuz","azj":"Oğuz","tuk":"Oğuz","gag":"Oğuz",
    "tat":"Kıpçak","bak":"Kıpçak","kaz":"Kıpçak","kir":"Kıpçak","crh":"Kıpçak",
    "kaa":"Kıpçak","kum":"Kıpçak","krc":"Kıpçak","nog":"Kıpçak",
    "uzb":"Karluk","uig":"Karluk",
    "sah":"Sibirya","tyv":"Sibirya","kjh":"Sibirya","cjs":"Sibirya","dlg":"Sibirya","alt":"Sibirya",
    "klj":"Argu",
}


def read(name, base=GL):
    with open(base / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    # AES kod -> etiket + crosswalk
    aes_code = {}
    for c in read("codes.csv"):
        if c["Parameter_ID"] == "aes":
            aes_code[c["ID"]] = {"label": c["Name"], "crosswalk": c["Description"], "level": int(c["numerical_value"])}
    # glottocode -> aes
    aes_of = {}
    for v in read("values.csv"):
        if v["Parameter_ID"] == "aes":
            aes_of[v["Language_ID"]] = {"code": v["Code_ID"], "comment": v["Comment"]}

    # diller: hedef iso'lar; iso başına AES'i olan satırı tercih et
    best = {}
    for L in read("languages.csv"):
        iso = L["ISO639P3code"]
        if iso not in TARGET:
            continue
        has_aes = L["Glottocode"] in aes_of
        cur = best.get(iso)
        if cur is None or (has_aes and not cur["_has_aes"]):
            best[iso] = {"_has_aes": has_aes, "row": L}

    profiles = []
    for iso, b in best.items():
        L = b["row"]; gc = L["Glottocode"]
        a = aes_of.get(gc)
        aes = None
        if a:
            cd = aes_code.get(a["code"], {})
            aes = {"level": cd.get("level"), "label": cd.get("label"),
                   "crosswalk": cd.get("crosswalk"), "comment": a["comment"], "source_glottolog": True}
        profiles.append({
            "iso": iso, "glottocode": gc, "name": L["Name"], "branch": ISO_BRANCH.get(iso),
            "macroarea": L["Macroarea"] or None, "countries": L["Countries"] or None,
            "lat": float(L["Latitude"]) if L["Latitude"] else None,
            "lon": float(L["Longitude"]) if L["Longitude"] else None,
            "level": L["Level"], "vitality_aes": aes, "mvp": iso in MVP,
        })
    profiles.sort(key=lambda p: (p["branch"] or "z", p["name"]))

    json.dump({"_meta": {**META, "module": "Dil Profilleri / Canlılık",
                         "note": "vitality_aes = Glottolog AES (açık); EGIDS/UNESCO/ElCat eşlemesi crosswalk'ta."},
               "profiles": profiles},
              open(OUT / "profiles.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"profiles.json : {len(profiles)} dil ({sum(1 for p in profiles if p['mvp'])} MVP)")
    for p in profiles:
        v = p["vitality_aes"]
        print(f"  {p['iso']:4s} {p['name']:22s} {str(p['branch']):8s} AES={v['level'] if v else '-'} {v['label'] if v else '(yok)'}")


if __name__ == "__main__":
    main()
