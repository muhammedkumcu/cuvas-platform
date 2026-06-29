#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DURUM TABLOSU — her dil için morfoloji motorunun GERÇEK yapabildikleri (dürüst, FST-probe).
Kullanıcı sordu: fiil mi problemli, isim okey mi, segment kaç parça, hangi diller kopula-zamanı
üretemiyor. /analyze + /segment + /generate ile ölçer. Çıktı: capability_report.json + konsol tablo.
"""
import json, sys, urllib.request
from collections import Counter

API = "http://127.0.0.1:8000"
NSEED = {"tur": "ev", "aze": "ev", "kaz": "бала", "kir": "бала", "uzb": "uy", "uig": "كىتاب",
         "tat": "кул", "bak": "китап", "chv": "хӗр", "sah": "ат", "tuk": "kitap", "crh": "kitap",
         "gag": "kitap", "kaa": "kitap", "alt": "ат", "kjh": "ат", "krc": "ат", "kum": "ат",
         "nog": "ат", "tyv": "ат"}
VSEED = {"tur": "oku", "aze": "oxu", "kaz": "оқы", "kir": "оку", "uzb": "oʻqi", "uig": "ئوقۇ",
         "tat": "укы", "bak": "уҡы", "chv": "вула", "sah": "аах", "tuk": "oka", "crh": "oqu",
         "gag": "oku", "kaa": "oqı", "alt": "кычыр", "kjh": "хығыр", "krc": "оху", "kum": "оху",
         "nog": "окы", "tyv": "ном"}


def _post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))


def gen1(lang, q):
    try:
        fs = (_post("/generate", {"lang": lang, "query": q}) or {}).get("forms") or []
        return fs[0].get("surface") if fs else None
    except Exception:
        return None


def seg_parts(lang, word):
    try:
        ms = (_post("/segment", {"lang": lang, "word": word}) or {}).get("morphemes") or []
        return len(ms), [m.get("surface") for m in ms], [m.get("tag") for m in ms]
    except Exception:
        return 0, [], []


def main():
    rep = {}
    for lg in sorted(NSEED):
        ns, vs = NSEED[lg], VSEED[lg]
        # 1) İSİM: 2-ekli biçim üret (çoğul+bulunma) -> segment incelik
        noun_form = gen1(lg, ns + "<n><pl><loc>") or gen1(lg, ns + "<n><pl><loc><nom>")
        n_parts = seg_parts(lg, noun_form)[0] if noun_form else 0
        # 2) FİİL: görülen geçmiş çoğul (gel+di+ler tipi) -> segment incelik
        past_form = gen1(lg, vs + "<v><tv><ifi><p3><pl>") or gen1(lg, vs + "<v><tv><past><p3><pl>") or gen1(lg, vs + "<v><iv><ifi><p3><pl>")
        v_parts = seg_parts(lg, past_form)[0] if past_form else 0
        # 3) KOPULA-ZAMANI üretimi: şimdiki/geniş kişili üretiyor mu? (Oğuz açığı)
        prog_pers = gen1(lg, vs + "<v><tv><prog><cop><aor><p1><sg>") or gen1(lg, vs + "<v><iv><prog><cop><aor><p1><sg>") or gen1(lg, vs + "<v><tv><pres><p1><sg>") or gen1(lg, vs + "<v><iv><pres><p1><sg>")
        prog_bare = gen1(lg, vs + "<v><tv><prog>") or gen1(lg, vs + "<v><iv><prog>")
        rep[lg] = {
            "isim_uretim": bool(noun_form), "isim_ornek": noun_form, "isim_segment_parca": n_parts,
            "fiil_uretim": bool(past_form), "fiil_ornek": past_form, "fiil_segment_parca": v_parts,
            "kopula_kisili_uretim": bool(prog_pers), "kopula_ornek": prog_pers,
            "kopula_yalin_uretim": bool(prog_bare), "kopula_yalin_ornek": prog_bare,
        }
    json.dump(rep, open("platform/backend/capability_report.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    # özet sayımlar
    n_ok = sum(1 for r in rep.values() if r["isim_uretim"])
    v_ok = sum(1 for r in rep.values() if r["fiil_uretim"])
    cop_ok = sum(1 for r in rep.values() if r["kopula_kisili_uretim"])
    fine_v = sum(1 for r in rep.values() if r["fiil_segment_parca"] >= 3)
    print("DURUM: isim-uretim %d/20, fiil-uretim %d/20, kopula-kisili %d/20, fiil-segment>=3parca %d/20"
          % (n_ok, v_ok, cop_ok, fine_v))
    print("capability_report.json yazildi")


if __name__ == "__main__":
    main()
