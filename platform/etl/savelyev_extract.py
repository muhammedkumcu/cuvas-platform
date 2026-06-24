#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SavelyevTurkic CLDF -> platform veri ürünleri (kaynaklı JSON).

Kaynak  : SavelyevTurkic CLDF  (github.com/lexibank/savelyevturkic)
Lisans  : CC BY 4.0
Atıf    : Savelyev & Robbeets (2020), Bayesian phylolinguistics... (J. of Language Evolution 5/1)
Erişim  : 2026-06-24 (yerel: sources/savelyevturkic)

Üretir (platform/data/):
  - languages.geo.json   : 32 dil + glottocode/iso/lat-lon/kol  -> Harita modülü
  - cognates.json        : kavram -> kognat setleri (üye diller + biçim/segment/kök) -> Kognat Ağı
  - distance.lexical.json : dil x dil leksikostatistik mesafe (paylaşılan kognat oranı) -> Uzaklık(leksikal)

İLKE: her çıktı bir `_meta` bloğu taşır (kaynak+lisans+yöntem). Uydurma yok; veriler doğrudan CLDF'ten.
"""
import csv, json, itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]           # repo kökü
CLDF = ROOT / "sources" / "savelyevturkic" / "cldf"
OUT  = ROOT / "platform" / "data"
OUT.mkdir(parents=True, exist_ok=True)

META = {
    "source": "SavelyevTurkic CLDF",
    "license": "CC BY 4.0",
    "url": "https://github.com/lexibank/savelyevturkic",
    "reference": "Savelyev & Robbeets (2020), J. of Language Evolution 5(1):39-53",
    "accessed": "2026-06-24",
}

# Language_ID -> kol (kollar #3/#4 derlemelerinden)
BRANCH = {
    "Chuvash": "Ogur",
    "Turkish": "Oğuz", "Azeri": "Oğuz", "Turkmen": "Oğuz", "Gagauz": "Oğuz", "Salar": "Oğuz",
    "Tatar": "Kıpçak", "Bashkir": "Kıpçak", "Kazakh": "Kıpçak", "KaraKalpak": "Kıpçak",
    "Nogai": "Kıpçak", "KarachayBalkar": "Kıpçak", "Kumyk": "Kıpçak", "Kirghiz": "Kıpçak",
    "CrimeanTatar": "Kıpçak", "Karaim": "Kıpçak", "CodexCumanicus": "Kıpçak", "Baraba": "Kıpçak",
    "Uzbek": "Karluk", "Uighur": "Karluk",
    "Yakut": "Sibirya", "Dolgan": "Sibirya", "Tuvan": "Sibirya", "Tofa": "Sibirya",
    "Khakas": "Sibirya", "Shor": "Sibirya", "NorthAltai": "Sibirya", "SouthAltai": "Sibirya",
    "MiddleChulym": "Sibirya", "SarygYugur": "Sibirya",
    "Khalaj": "Argu",
    "OldUyghur": "Eski Türkçe",
}
ISO_OVERRIDE = {"Turkish": "tur", "Tatar": "tat"}      # CLDF'te boş kalan ISO'lar
MVP = {"tur", "azj", "kaz", "kir", "uzb", "uig", "tat", "bak", "chv", "sah"}


def read_csv(name):
    with open(CLDF / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    langs = read_csv("languages.csv")
    params = read_csv("parameters.csv")
    forms = read_csv("forms.csv")
    cogs = read_csv("cognates.csv")

    # ---- diller + coğrafya ----
    lang_by_id = {}
    geo = []
    for L in langs:
        lid = L["ID"]
        iso = L["ISO639P3code"] or ISO_OVERRIDE.get(lid, "")
        rec = {
            "id": lid, "name": L["Name"], "glottocode": L["Glottocode"] or None,
            "iso": iso or None, "branch": BRANCH.get(lid),
            "lat": float(L["Latitude"]) if L["Latitude"] else None,
            "lon": float(L["Longitude"]) if L["Longitude"] else None,
            "mvp": iso in MVP,
        }
        lang_by_id[lid] = rec
        geo.append(rec)
    json.dump({"_meta": {**META, "module": "Harita / dil kimliği"}, "languages": geo},
              open(OUT / "languages.geo.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # ---- form_id -> cognateset/root ----
    cog_of = {}
    for c in cogs:
        cog_of[c["Form_ID"]] = {"cs": c["Cognateset_ID"], "root": c["Root"] or None}

    concept = {p["ID"]: {"name": p["Name"], "gloss": p["Concepticon_Gloss"]} for p in params}

    # ---- kavram -> cognateset -> üyeler ----
    by_concept = {}                          # pid -> {cs -> {root, members[]}}
    lang_concept_cs = {}                     # (lang, pid) -> set(cs)
    for fr in forms:
        fid, lid, pid = fr["ID"], fr["Language_ID"], fr["Parameter_ID"]
        cg = cog_of.get(fid)
        if not cg:
            continue
        cs = cg["cs"]
        member = {
            "lang": lid, "iso": lang_by_id.get(lid, {}).get("iso"),
            "branch": BRANCH.get(lid),
            "value": fr["Value"], "form": fr["Form"], "segments": fr["Segments"],
        }
        d = by_concept.setdefault(pid, {}).setdefault(cs, {"cognateset_id": cs, "root": cg["root"], "members": []})
        d["members"].append(member)
        lang_concept_cs.setdefault((lid, pid), set()).add(cs)

    cognates = []
    for pid, sets in by_concept.items():
        cognates.append({
            "concept_id": pid,
            "concept": concept.get(pid, {}).get("name"),
            "gloss": concept.get(pid, {}).get("gloss"),
            "sets": sorted(sets.values(), key=lambda s: -len(s["members"])),
        })
    cognates.sort(key=lambda c: c["concept_id"])
    json.dump({"_meta": {**META, "module": "Kognat Ağı",
                         "note": "Cognate_Detection_Method=expert (uzman yargısı)"},
               "concepts": cognates},
              open(OUT / "cognates.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # ---- leksikostatistik mesafe: paylaşılan kognat oranı ----
    all_pids = {pid for (_, pid) in lang_concept_cs}
    ids = [L["ID"] for L in langs]
    matrix = {}
    for a in ids:
        matrix[a] = {}
        for b in ids:
            if a == b:
                matrix[a][b] = {"similarity": 1.0, "distance": 0.0, "shared": None, "total": None}
                continue
            shared = total = 0
            for pid in all_pids:
                csa = lang_concept_cs.get((a, pid))
                csb = lang_concept_cs.get((b, pid))
                if csa and csb:
                    total += 1
                    if csa & csb:
                        shared += 1
            sim = (shared / total) if total else None
            matrix[a][b] = {
                "similarity": round(sim, 4) if sim is not None else None,
                "distance": round(1 - sim, 4) if sim is not None else None,
                "shared": shared, "total": total,
            }
    json.dump({"_meta": {**META, "module": "Uzaklık Gezgini (leksikal eksen)",
                         "method": "iki dilin ortak attığı kavramlarda aynı kognat setini paylaşma oranı; mesafe=1-benzerlik"},
               "matrix": matrix},
              open(OUT / "distance.lexical.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # ---- özet (sanity check) ----
    nset = sum(len(c["sets"]) for c in cognates)
    print(f"languages.geo.json   : {len(geo)} dil ({sum(1 for g in geo if g['mvp'])} MVP)")
    print(f"cognates.json        : {len(cognates)} kavram, {nset} kognat seti, {len(forms)} form")
    print(f"distance.lexical.json : {len(ids)}x{len(ids)} matris")
    print("--- sanity: Çuvaşça (Chuvash) leksikal mesafe (büyük = uzak) ---")
    row = matrix["Chuvash"]
    for b in ["Turkish", "Tatar", "Kazakh", "Uzbek", "Uighur", "Yakut", "Khalaj", "Azeri"]:
        d = row.get(b, {})
        print(f"  Chuvash–{b:9s}: mesafe={d.get('distance')}  (paylaşılan {d.get('shared')}/{d.get('total')})")


if __name__ == "__main__":
    main()
