#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#54 — Üreteç dile-duyarlı ZAMAN envanteri (FEATTENSE). Apertium zaman/görünüş kodlaması DİLDEN DİLE
hem ETİKET ADI hem YAPI olarak farklıdır:
  - tur: görülen geçmiş = <ifi>, şart = <cond> DOĞRUDAN kişi alır; aorist/şimdiki/gelecek ise
    KOPULA ile kurulur (okur+um) ve /generate ile kişi-çekimli ÜRETİLEMEZ (analyze≠generate asimetrisi).
  - chv: pres/past/fut/cond hepsi DOĞRUDAN kişi (вулатӑп). <ifi>/<aor> YOK.
  - kaz/kir/uig/uzb/sah/crh: past/ifi/fut/aor üretir.
Bu yüzden bant-aid fallback (past<->ifi, pres<->aor) yetersiz: tur'da şimdiki/gelecek BOŞ kalıyor.
DOĞRU çözüm: her dilin FST'sinde HANGİ UI-zamanı kişi-çekimli ÜRETİYOR onu probe et → FEATTENSE;
Üreteç o dilde üretmeyen zamanı GRİLER (FEATCASE'in hâlleri grilemesi gibi).

Yöntem (SSH gerekmez, host'tan API): birkaç fiili crosslang ederek dil başına lemma topla;
her dil+lemma için UI-zaman -> [ham etiket adayları] (bant-aid) × [tv,iv] /generate dene.
Kişi-çekimli (<p1><sg>) üretirse o UI-zaman geçerli.

Çıktı: tense_probe_report.json (ham + UI) + feattense.js.txt (build.py'ye gömülecek tek satır).
"""
import json, sys, urllib.request

API = "http://127.0.0.1:8000"
PROBE_VERBS = ["okudum", "geldim", "bildim", "aldım", "gördüm", "yazdım"]  # crosslang lemma toplamak için
UI_TENSES = ["pres", "past", "ifi", "fut", "aor", "cond"]
# UI-zaman -> denenecek ham apertium etiketleri (bant-aid: aynı anlamın dile göre farklı etiketi)
TA = {"pres": ["pres", "prs", "aor"], "past": ["past", "ifi"], "ifi": ["ifi", "past"],
      "fut": ["fut", "fti"], "aor": ["aor", "pres"], "cond": ["cond", "cni"]}


def _post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))


def gen_ok(lang, query):
    try:
        return bool((_post("/generate", {"lang": lang, "query": query}) or {}).get("forms"))
    except Exception:
        return False


# crosslang'in ulaşamadığı diller için doğrudan fiil-tohumları (her dilde birden çok aday denenir).
DIRECT_SEEDS = {
    "aze": ["oxu", "gəl", "al"], "tuk": ["oka", "gel", "al", "git"], "gag": ["oku", "gel", "al"],
    "kaa": ["oqı", "oqu", "kel", "al"], "alt": ["кычыр", "кел", "ал", "бар"],
    "kjh": ["хығыр", "кил", "ал", "пар"], "krc": ["оху", "окъу", "кел", "ал"],
    "kum": ["оху", "гел", "ал", "бар"], "nog": ["окы", "кел", "ал", "бар"], "tyv": ["ном", "кел", "ал", "бар"],
}


def collect_lemmas():
    """Birden çok fiili crosslang -> {lang: {lemma}} (union) + ulaşılamayanlara doğrudan tohum."""
    lem = {}
    for vb in PROBE_VERBS:
        try:
            d = _post("/crosslang", {"lang": "tur", "word": vb})
        except Exception:
            continue
        for r in (d.get("results") or []):
            if r.get("lemma"):
                lem.setdefault(r["lang"], set()).add(r["lemma"])
    out = {lg: sorted(s) for lg, s in lem.items()}
    for lg, seeds in DIRECT_SEEDS.items():
        if lg not in out:
            out[lg] = seeds  # crosslang ulaşamadı → doğrudan tohum (probe yine /generate ile doğrular)
    return out


def main():
    lemmas = collect_lemmas()
    feat_ui, ex = {}, {}
    for lg, lms in sorted(lemmas.items()):
        valid, exl = [], {}
        for tn in UI_TENSES:
            hit = None
            for tag in TA[tn]:
                for kind in ("tv", "iv"):
                    for lm in lms:
                        q = "%s<v><%s><%s><p1><sg>" % (lm, kind, tag)
                        if gen_ok(lg, q):
                            d = _post("/generate", {"lang": lg, "query": q})
                            hit = (d.get("forms") or [{}])[0].get("surface")
                            break
                    if hit:
                        break
                if hit:
                    break
            if hit:
                valid.append(tn); exl[tn] = hit
        feat_ui[lg] = valid; ex[lg] = exl
    json.dump({"FEATTENSE_UI": feat_ui, "examples": ex, "ui_tenses": UI_TENSES,
               "note": "UI-zaman gecerli = o dilde kisi-cekimli (p1.sg) URETIYOR (bant-aid etiketleriyle). "
                       "Bos = FST o UI-zamani kisi-cekimli uretemiyor (or. tur kopula-zamanlari)."},
              open("platform/backend/tense_probe_report.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    js = "{" + ",".join("%s:[%s]" % (lg, ",".join("'%s'" % t for t in feat_ui[lg]))
                        for lg in sorted(feat_ui)) + "}"
    open("platform/backend/feattense.js.txt", "w", encoding="utf-8").write(js)
    print("FEATTENSE_UI: %d dil probe edildi -> tense_probe_report.json + feattense.js.txt" % len(feat_ui))


if __name__ == "__main__":
    main()
