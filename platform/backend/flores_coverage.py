#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KORPUS KAPSAMI (recall) — FLORES-200 (insan-çevirisi, sıfır-gürültü, eşit-boyut 1012 cümle).
Her FST'nin gerçek metindeki kelimeleri ne kadar TANIDIĞI (kapsam = tanınan token / toplam token).
Ayrıca tanınan FARKLI LEMMA sayısı (sözlük büyüklüğünün korpus-temelli alt-sınırı = T3'e bağlı).
VM'de FST'yi DOĞRUDAN çağırır (HTTP yok → hızlı). Veri: /root/flores (CC-BY-SA). Uydurma yok.
FLORES Türkçe-Türk dilleri: 10 dil; geri kalan 10 (chv/sah/gag/kaa/alt/kjh/krc/kum/nog/tyv) FLORES'te yok.
"""
import hfst, glob, os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.expanduser("~/.turkicnlp/models")
FL = "/root/flores/flores200_dataset/devtest"
MAP = {"tur": "tur_Latn", "aze": "azj_Latn", "kaz": "kaz_Cyrl", "kir": "kir_Cyrl",
       "uzb": "uzn_Latn", "uig": "uig_Arab", "tat": "tat_Cyrl", "bak": "bak_Cyrl",
       "crh": "crh_Latn", "tuk": "tuk_Latn"}


def analyzer(lang):
    hits = glob.glob(f"{BASE}/{lang}/**/{lang}.automorf.hfst", recursive=True)
    return hfst.HfstInputStream(hits[0]).read() if hits else None


def toks(line):
    out = []
    for t in re.split(r"[\s.,;:!?\"'`()\[\]«»…—–\-/]+", line.strip()):
        if t and re.search(r"[^\W\d_]", t, re.UNICODE):  # en az 1 harf (saf sayı/noktalama atılır)
            out.append(t)
    return out


def main():
    data = {}
    print(f"{'dil':4} {'kapsam%':8} {'token':12} {'farklı-lemma':12}")
    print("-" * 44)
    for lang, fl in MAP.items():
        fst = analyzer(lang)
        path = os.path.join(FL, fl + ".devtest")
        if not fst or not os.path.exists(path):
            print(f"{lang:4}  (FST/dosya yok)")
            continue
        total = recog = 0
        lemmas = set()
        cache = {}
        for line in open(path, encoding="utf-8"):
            for t in toks(line):
                total += 1
                if t not in cache:
                    res = fst.lookup(t) or fst.lookup(t.lower())
                    cache[t] = res
                res = cache[t]
                if res:
                    recog += 1
                    for a in res:
                        lemmas.add(re.split(r"[<+]", a[0], 1)[0])
        cov = round(100 * recog / total, 1) if total else 0
        data[lang] = {"kapsam": cov, "token": total, "recog": recog, "lemma": len(lemmas)}
        print(f"{lang:4} {cov:7.1f}% {recog:6}/{total:<6} {len(lemmas):12}")
    print("-" * 44)
    print("kapsam = tanınan token / toplam (FLORES devtest, 1012 cümle) · farklı-lemma = korpusta görülen kök")
    print("===JSON===")
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
