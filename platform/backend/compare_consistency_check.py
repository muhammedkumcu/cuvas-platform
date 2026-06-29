#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#55 — Karşılaştır "Dizilim" tutarlılık + ek yazımı GOLD doğrulaması.

Karşılaştır sayfasının iki olası kaynağı vardı:
  - STATİK : aktif kelimenin küratörlü `cognates` verisi (cognates_deep.json) — etimolojik
             kognatlar (kavram-tabanlı). API-türevli (çekimli) kelimede `cognates` BOŞ → kırık görünüm.
  - DİNAMİK: canlı /crosslang (kaynak kelimeyi her dilde aynı morfolojiyle üretir) + per-dil /segment.

KARAR: DİNAMİK otoritedir (canlı FST). Bu betik dinamiğin ek YAZIMINI gold-doğrular:
  her dilde /segment morfemleri YÜZEYE birebir geri-birleşmeli (round-trip = morfem birleşimi == yüzey).
Round-trip %100 ise segmentasyon/ek yazımı tutarlı demektir (FST'nin kendi üretimiyle birebir).

UI tarafı (build.py): compare ekranına API kelimeyle gelince componentDidUpdate otomatik runCompare
çalıştırır → statik (kırık) yerine dinamik gösterilir. Curated varsayılan kelimenin statik kognat
showcase'i korunur (activeWordId!=='__api').

Çalıştırma: VM API açıkken  python platform/backend/compare_consistency_check.py
"""
import json, sys, urllib.request

API = "http://127.0.0.1:8000"
# Çekimli test sözcükleri (kaynak dil, kelime) — fiil + isim çekimleri, çoklu kol.
TESTS = [
    ("tur", "okuduk"),    # oku-<v><tv><ifi><p1><pl>  (we read, past)
    ("tur", "evlerde"),   # ev-<n><pl><loc>
    ("kaz", "кітаптар"),  # kitap-<n><pl>
    ("tur", "geldim"),    # gel-<v><iv><ifi><p1><sg>
    ("chv", "хӗре"),      # hĕr-<n><dat>
]


def _post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))


def check(src, word):
    cl = _post("/crosslang", {"lang": src, "word": word})
    results = cl.get("results") or []
    tags = cl.get("tags")
    out = {"src": src, "word": word, "tags": tags, "n_langs": len(results), "rows": [], "rt_ok": 0, "rt_total": 0}
    for r in results:
        lg, surf = r.get("lang"), r.get("surface")
        if not surf:
            continue
        seg = _post("/segment", {"lang": lg, "word": surf})
        ms = seg.get("morphemes") or []
        recon = "".join(m.get("surface", "") for m in ms)
        ok = (recon == surf) and bool(ms)
        out["rt_total"] += 1
        out["rt_ok"] += 1 if ok else 0
        out["rows"].append({"lang": lg, "surface": surf,
                            "seg": " + ".join("%s{%s}" % (m.get("surface"), m.get("feat")) for m in ms),
                            "round_trip": "OK" if ok else ("FARK:" + recon if ms else "BOŞ")})
    return out


def main():
    grand_ok = grand_total = 0
    report = []
    for src, w in TESTS:
        try:
            res = check(src, w)
        except Exception as e:
            print("HATA", src, w, e); continue
        grand_ok += res["rt_ok"]; grand_total += res["rt_total"]
        report.append(res)
    # ASCII-güvenli yaz (konsol cp1254 Kiril'de çöker) → dosyaya JSON
    out_path = "platform/backend/compare_consistency_report.json"
    json.dump({"summary": {"round_trip_ok": grand_ok, "round_trip_total": grand_total,
                           "pct": round(100 * grand_ok / grand_total, 1) if grand_total else None},
               "tests": report}, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("compare consistency: round-trip %d/%d (%.1f%%) -> %s" %
          (grand_ok, grand_total, 100 * grand_ok / grand_total if grand_total else 0, out_path))


if __name__ == "__main__":
    main()
