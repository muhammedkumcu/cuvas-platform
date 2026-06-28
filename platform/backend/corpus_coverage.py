#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KORPUS KAPSAMI — FLORES'te OLMAYAN diller için (HF/Leipzig açık korpuslarından recall).
FLORES eşit-boyut/sıfır-gürültü omurgaydı; bu diller için kaynak heterojen → her dil kaynağıyla
ETİKETLENİR (dürüst, eşit-boyut değil). VM'de FST doğrudan (hızlı). Veri dosyaları /root'a scp'lenir.
Kaynaklar: nog = HF ansarzeinulla/Nogai-Unified-Corpus-v1 (CC-BY-NC) · kjh = HF adeshkin/khakas-monolingual (CC-BY).
"""
import hfst, glob, os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.expanduser("~/.turkicnlp/models")
# /root/cov_<lang>.txt dosyalarını otomatik bul; kaynak etiketleri:
SRC = {"nog": "HF·Nogai-Unified", "kjh": "HF·khakas-mono", "chv": "HF·chuvash_mono",
       "kaa": "HF·karakalpak", "sah": "fineweb-2", "alt": "fineweb-2", "gag": "fineweb-2",
       "kum": "fineweb-2", "krc": "fineweb-2", "tyv": "fineweb-2"}
JOBS = {}
for _f in __import__("glob").glob("/root/cov_*.txt"):
    _l = os.path.basename(_f)[4:-4]
    JOBS[_l] = (_f, SRC.get(_l, "HF"))


def analyzer(lang):
    h = glob.glob(f"{BASE}/{lang}/**/{lang}.automorf.hfst", recursive=True)
    return hfst.HfstInputStream(h[0]).read() if h else None


def toks(line):
    return [t for t in re.split(r"[\s.,;:!?\"'`()\[\]«»…—–/]+", line.strip())
            if t and re.search(r"[^\W\d_]", t, re.UNICODE)]


def main():
    data = {}
    print(f"{'dil':4} {'kapsam%':8} {'token':12} {'farklı-lemma':12} kaynak")
    print("-" * 60)
    for lang, (path, src) in JOBS.items():
        fst = analyzer(lang)
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
                    cache[t] = fst.lookup(t) or fst.lookup(t.lower())
                r = cache[t]
                if r:
                    recog += 1
                    for a in r:
                        lemmas.add(re.split(r"[<+]", a[0], 1)[0])
        cov = round(100 * recog / total, 1) if total else 0
        data[lang] = {"kapsam": cov, "token": total, "lemma": len(lemmas), "src": src}
        print(f"{lang:4} {cov:7.1f}% {recog:6}/{total:<6} {len(lemmas):12} {src}")
    print("-" * 60)
    print("===JSON===")
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
