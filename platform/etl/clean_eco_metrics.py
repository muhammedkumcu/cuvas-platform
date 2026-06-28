# -*- coding: utf-8 -*-
"""clean_eco_metrics.py — ecosystem.json'dan yıldız (★) / indirme (↓) metriklerini kaldırır.
Kullanıcı isteği: bu sayılar zamanla eskir ve nötr launchpad mantığına gölge düşürür. Notlardaki
nitel açıklama (mimari, lisans, dil) korunur; yalnız '· 41★', '340K↓' gibi metrik parçaları + ilgili
açıklama cümleleri çıkar."""
import json
import io
import os
import re

P = os.path.join(os.path.dirname(__file__), "..", "data", "ecosystem.json")
d = json.load(io.open(P, encoding="utf-8"))


def strip(note):
    if not note:
        return note
    s = note
    # "· 41★", "· 3.38K↓", "· 340K↓", "· 1.2M★" gibi ayraçlı metrikler
    s = re.sub(r"\s*·\s*[\d.,]+\s*[KMB]?\s*[★↓]", "", s)
    # baştaki/yalın metrik: "6★", "340K↓ · "
    s = re.sub(r"^[\d.,]+\s*[KMB]?\s*[★↓]\s*·?\s*", "", s)
    s = re.sub(r"[\d.,]+\s*[KMB]?\s*[★↓]", "", s)
    # kalan çift/baş/son ayraçları temizle
    s = re.sub(r"\s*·\s*·\s*", " · ", s)
    s = re.sub(r"^\s*·\s*|\s*·\s*$", "", s)
    return s.strip()


n = 0
for c in d.get("categories", []):
    for h in c.get("hubs", []):
        nv = strip(h.get("note", ""))
        if nv != h.get("note", ""):
            h["note"] = nv; n += 1
    for lg in c.get("langs", []):
        for link in lg.get("links", []):
            if "note" in link:
                nv = strip(link["note"])
                if nv != link["note"]:
                    n += 1
                    if nv:
                        link["note"] = nv
                    else:
                        del link["note"]

# intro / _meta metin güncellemeleri (metrik ibarelerini kaldır)
d["intro"] = d["intro"].replace(" — mümkün olduğunda indirme/yıldız metrikleriyle", "")
m = d["_meta"]
m["note"] = (m["note"].replace(" + indirme/yıldız metrikleri", "")
             .replace(" ★=yıldız, ↓=indirme.", "").strip())
m["source"] = re.sub(r"\s*Metrikler \(indirme/yıldız/tarih\)[^.]*\.", "", m["source"]).strip()

with io.open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("ecosystem.json: %d not metrikten temizlendi; intro/_meta güncellendi" % n)
