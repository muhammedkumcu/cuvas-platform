#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIŞ-GOLD DOĞRULUK değerlendirmesi — UniMorph (insan-küratörlü) vs bizim /analyze.
Felsefe: round-trip İÇ tutarlılık ölçer; bu betik DIŞ doğruluk ölçer (döngüsel değil).
Metrik (tag-şeması eşlemesi GEREKTİRMEZ — dürüst, basit):
  - tanıma%   : UniMorph biçimine analizci HERHANGİ bir çözüm veriyor mu (kapsam/recall).
  - lemma%    : tanınanlar içinde bizim lemma == UniMorph lemma olanlar (lemmatizasyon doğruluğu).
İsimlerle sınırlı (N;...): fiil lemma'sı UniMorph'ta mastar (göndermek), apertium'da gövde (gönder) → adil değil.
Veri: sources/<lang>/<lang> (UniMorph; gitignored). API: localhost:8000 (VM port-forward).
NOT: bazı UniMorph dosyalarının yazısı FST'den farklı olabilir (ör. tat UniMorph Latin, FST Kiril) →
düşük tanıma = yazı uyuşmazlığı işareti, FST hatası DEĞİL; dürüstçe raporlanır.
"""
import json, urllib.request, sys, os, random
sys.stdout.reconfigure(encoding="utf-8")
API = "http://127.0.0.1:8000"
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "sources")
N = 1500         # dil başına örnek isim biçimi (yüksek örneklem — istatistiksel geçerlilik)
random.seed(42)  # tekrar-üretilebilir

# UniMorph'u sources/<lang>/<lang>'da olan + FST'si olan diller
LANGS = ["tur", "aze", "kaz", "kir", "uzb", "uig", "tat", "bak", "sah"]


def post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))


def load_nouns(lang):
    path = os.path.join(ROOT, lang, lang)
    if not os.path.exists(path):
        return None
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) != 3:
                continue
            lemma, form, feats = p
            if not feats.startswith("N"):       # yalnız isim
                continue
            if " " in form or " " in lemma:      # tek-sözcük
                continue
            rows.append((lemma.strip(), form.strip()))
    return rows


def main():
    print("=" * 72)
    print(f"{'dil':4} {'gold-isim':10} {'örnek':6} {'tanıma%':8} {'lemma%':8}  not")
    print("-" * 72)
    grand = {}
    for lang in LANGS:
        rows = load_nouns(lang)
        if not rows:
            print(f"{lang:4} {'(UniMorph yok / boş)':>10}")
            continue
        sample = random.sample(rows, min(N, len(rows)))
        seen = recog = lemma_ok = 0
        fails = []
        for lemma, form in sample:
            try:
                d = post("/analyze", {"lang": lang, "word": form})
            except Exception:
                continue
            seen += 1
            an = d.get("analyses", [])
            if an:
                recog += 1
                lemmas = {a.get("lemma", "").lower() for a in an}
                if lemma.lower() in lemmas:
                    lemma_ok += 1
                elif len(fails) < 3:
                    fails.append(f"{form}: gold={lemma} bizde={sorted(lemmas)[:2]}")
        if not seen:
            continue
        rp = 100 * recog / seen
        lp = 100 * lemma_ok / recog if recog else 0.0
        note = "" if rp > 40 else "DÜŞÜK tanıma → yazı uyuşmazlığı olabilir"
        grand[lang] = (len(rows), seen, rp, lp, fails)
        print(f"{lang:4} {len(rows):10} {seen:6} {rp:7.1f}% {lp:7.1f}%  {note}")
    print("-" * 72)
    print("tanıma% = UniMorph biçimini analizci tanıdı mı (kapsam) · lemma% = doğru lemmatizasyon (tanınanlarda)")
    for lang, (_, _, _, _, fails) in grand.items():
        if fails:
            print(f"\n[{lang}] örnek lemma-uyuşmazlığı:")
            for f in fails:
                print("   ", f)


if __name__ == "__main__":
    main()
