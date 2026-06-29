#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#56 — HUMANIZER TAM KORPUS DENETİMİ (host-side, API üzerinden; VM /root/cov_*.txt silinmişti).
Her dilin morfolojisini /generate ile sistematik üretir (isim: hâl×sayı×iyelik; fiil: zaman×kişi×sayı),
üretilen yüzey biçimlerini /analyze ile çözer ve çıkan TÜM apertium etiketlerini toplar (analiz
belirsizliği türev etiketleri de yakalar: ger_*, gpr_*, prc_*, subst, prog, pot, evid…).
Sonra UI humanizer'ının (build.py TAGSHORT/TAGLONG) kapsamadığı etiketleri RAPORLAR — bunlar
kullanıcıya HAM (büyük harf) sızabilir. Bulgular humanizer'a eklenir → "her dil için doğru" garanti.

Çalıştırma: VM API açıkken  python platform/backend/humanizer_audit_api.py
"""
import json, re, sys, urllib.request
from collections import Counter

API = "http://127.0.0.1:8000"

# build.py TAGSHORT anahtarlarıyla AYNI tutulmalı (59 etiket). Denetim bunlara göre yapılır.
KNOWN = set("""abl acc adj adv advl ant aor attr caus cog cond coop cop dat dem dist equ fut gen
ger ger_past ger_perf gpr_past gpr_perf gpr_pot ifi imp ins itg loc n neg nom np num ord p1 p2 p3
pass past pl prc_cond prc_impf prc_perf pres prn px1pl px1sg px2pl px2sg px3pl px3sp qnt recip refl
sg top v
tv iv err_orth subst prog npst opt qst cnjcoo mod_ass px3sg plu gpr gpr_fut gpr_aor gpr_impf
gpr_ppot gpr_rsub ger_fut ger_aor ger_impf ger_pabs ger_ppot ger2 ger4 gna_cond gna_impf prc_fut
prc_past prc_aor prc_irre par phrase""".split())

# isim + fiil tohum lemmaları (feature_probe + tense_probe ile aynı havuz)
NSEED = {"tur": "ev", "aze": "ev", "kaz": "бала", "kir": "бала", "uzb": "uy", "uig": "كىتاب",
         "tat": "кул", "bak": "китап", "chv": "хӗр", "sah": "ат", "tuk": "kitap", "crh": "kitap",
         "gag": "kitap", "kaa": "kitap", "alt": "ат", "kjh": "ат", "krc": "ат", "kum": "ат",
         "nog": "ат", "tyv": "ат"}
VSEED = {"tur": "oku", "aze": "oxu", "kaz": "оқы", "kir": "оку", "uzb": "oʻqi", "uig": "ئوقۇ",
         "tat": "укы", "bak": "уҡы", "chv": "вула", "sah": "аах", "tuk": "oka", "crh": "oqu",
         "gag": "oku", "kaa": "oqı", "alt": "кычыр", "kjh": "хығыр", "krc": "оху", "kum": "оху",
         "nog": "окы", "tyv": "ном"}
CASES = ["nom", "gen", "dat", "acc", "loc", "abl", "ins"]
NUMS = ["", "pl"]
PXS = ["", "px1sg", "px3sp"]
TENSES = ["pres", "past", "ifi", "fut", "aor", "cond"]
PERS = ["p1", "p3"]


def _post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))


def gen(lang, q):
    try:
        return [f.get("surface") for f in (_post("/generate", {"lang": lang, "query": q}) or {}).get("forms", []) if f.get("surface")]
    except Exception:
        return []


def analyze_tags(lang, word):
    try:
        d = _post("/analyze", {"lang": lang, "word": word})
        return [t for a in (d.get("analyses") or []) for t in (a.get("tags") or [])]
    except Exception:
        return []


def main():
    per_lang = {}
    all_unc = Counter()
    for lg in sorted(NSEED):
        forms = set()
        ns = NSEED[lg]
        for nm in NUMS:
            for px in PXS:
                for cs in CASES:
                    q = ns + "<n>" + ("<pl>" if nm else "") + (("<" + px + ">") if px else "") + "<" + cs + ">"
                    forms.update(gen(lg, q))
        vs = VSEED[lg]
        for tn in TENSES:
            for pr in PERS:
                for vn in ["sg", "pl"]:
                    forms.update(gen(lg, "%s<v><tv><%s><%s><%s>" % (vs, tn, pr, vn)))
                    forms.update(gen(lg, "%s<v><iv><%s><%s><%s>" % (vs, tn, pr, vn)))
        # üretilen her yüzeyi çöz → etiket topla (belirsizlik türev etiketleri de yakalar)
        tags = Counter()
        for w in forms:
            for t in analyze_tags(lg, w):
                tags[t.lower()] += 1
        unc = {t: c for t, c in tags.items() if t not in KNOWN}
        for t, c in unc.items():
            all_unc[t] += c
        per_lang[lg] = {"n_forms": len(forms), "n_tags": len(tags), "uncovered": dict(sorted(unc.items(), key=lambda x: -x[1]))}
    rep = {"summary": {"known_count": len(KNOWN),
                       "uncovered_total": len(all_unc),
                       "uncovered_tags": dict(sorted(all_unc.items(), key=lambda x: -x[1]))},
           "per_lang": per_lang}
    json.dump(rep, open("platform/backend/humanizer_audit_report.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("HUMANIZER denetimi: KNOWN=%d, kapsanmayan ETIKET=%d -> humanizer_audit_report.json" %
          (len(KNOWN), len(all_unc)))
    print("Kapsanmayanlar (frekansa gore):", dict(sorted(all_unc.items(), key=lambda x: -x[1])))


if __name__ == "__main__":
    main()
