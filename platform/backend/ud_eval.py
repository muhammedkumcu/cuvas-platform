#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
İKİNCİ DIŞ-GOLD: Universal Dependencies (UD) treebank'leri — GERÇEK CÜMLE doğruluğu.
UniMorph izole paradigma tablosudur; UD insan-anotasyonlu çalışan metindir → tamamlayıcı, bağımsız.
★ Kritik: UD_Uyghur ARAP yazısında (bizim uig FST'siyle eşleşir) → UniMorph'un Latin↔Arap yazı
uyumsuzluğunu AŞAR. UD_Kazakh Kiril (kaz, UniMorph'ta minik), UD_Turkish gerçek metin.
Metrik (UniMorph ile aynı, kıyaslanabilir): tanıma% (recall) + lemma% (lemmatizasyon doğruluğu,
isim/fiil/sıfat/zarf tokenlerinde). Veri: sources/UD_* (CoNLL-U). API: localhost:8000.
"""
import json, urllib.request, sys, os, glob, random
sys.stdout.reconfigure(encoding="utf-8")
API = "http://127.0.0.1:8000"
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "sources")
N = 3000
random.seed(42)
CONTENT = {"NOUN", "VERB", "ADJ", "ADV", "PROPN", "NUM"}
# FST kodu -> UD treebank dizin desenleri
UD = {"tur": ["UD_Turkish-BOUN", "UD_Turkish-IMST"], "kaz": ["UD_Kazakh-KTB"], "uig": ["UD_Uyghur-UDT"]}


def post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))


def load_ud(dirs):
    rows = []
    for dn in dirs:
        for f in glob.glob(os.path.join(ROOT, dn, "*.conllu")):
            for line in open(f, encoding="utf-8"):
                if not line.strip() or line.startswith("#"):
                    continue
                c = line.rstrip("\n").split("\t")
                if len(c) < 4 or "-" in c[0] or "." in c[0]:
                    continue
                form, lemma, upos = c[1], c[2], c[3]
                if upos not in CONTENT or lemma == "_" or not form.strip():
                    continue
                if " " in form:
                    continue
                rows.append((form.strip(), lemma.strip(), upos))
    return rows


def main():
    print("=" * 74)
    print(f"{'dil':4} {'UD-token':9} {'örnek':6} {'tanıma%':8} {'lemma%':8}  not (yazı)")
    print("-" * 74)
    data = {}
    for lang, dirs in UD.items():
        rows = load_ud(dirs)
        if not rows:
            print(f"{lang:4} (UD bulunamadı)")
            continue
        sample = random.sample(rows, min(N, len(rows)))
        seen = recog = lemma_ok = 0
        for form, lemma, upos in sample:
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
        rp = 100 * recog / seen if seen else 0
        lp = 100 * lemma_ok / recog if recog else 0
        scr = {"tur": "Latin", "kaz": "Kiril", "uig": "Arap"}[lang]
        data[lang] = {"tokens": len(rows), "sample": seen, "recog": round(rp, 1), "lemma": round(lp, 1)}
        print(f"{lang:4} {len(rows):9} {seen:6} {rp:7.1f}% {lp:7.1f}%  {scr} (UD ↔ FST eşleşiyor)")
    print("-" * 74)
    print("UD = gerçek cümle gold'u (UniMorph paradigma tablosuna tamamlayıcı, bağımsız 2. gold).")
    print("===JSON===")
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
