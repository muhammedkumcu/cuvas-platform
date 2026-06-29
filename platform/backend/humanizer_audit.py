#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HUMANIZER DENETİMİ (#kullanıcı: "humanizer her dil için doğru çalışıyor mu emin ol").
Her dilde GERÇEK korpus (/root/cov_*.txt) tokenlarını automorf ile çözer, çıkan TÜM apertium
etiketlerini toplar; UI humanizer'ının (TAGSHORT/TAGLONG) kapsamadığı etiketleri raporlar —
bunlar kullanıcıya HAM (büyük harf) sızar. Çıktı: dil başına kapsanmayan etiket + frekans.
FLORES dilleri (tur/kaz/tat...) için cov dosyası yok; en olası novel-etiket bölgesi olan
prototip/beta dilleri (cov'lu 10) burada denetlenir; bulgular humanizer'a eklenir.
"""
import hfst, glob, os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.expanduser("~/.turkicnlp/models")
# UI humanizer'ının bildiği etiketler (build.py TAGSHORT/TAGLONG ile AYNI tutulmalı)
KNOWN = {"n", "v", "adj", "attr", "adv", "cop", "pl", "sg", "nom", "gen", "dat", "acc", "loc",
         "abl", "ins", "px1sg", "px2sg", "px3sp", "px1pl", "px2pl", "px3pl", "past", "ifi",
         "pres", "fut", "aor", "cond", "imp", "p1", "p2", "p3", "ger", "ger_past", "ger_perf",
         "ger_pres", "gpr_past", "gpr_pot", "gpr", "prc_perf", "prc_impf", "subst", "inf"}


def analyzer(lang):
    h = glob.glob(f"{BASE}/{lang}/**/{lang}.automorf.hfst", recursive=True)
    return hfst.HfstInputStream(h[0]).read() if h else None


def toks(line):
    return [t for t in re.split(r"[\s.,;:!?\"'`()\[\]«»…—–/]+", line.strip())
            if t and re.search(r"[^\W\d_]", t, re.UNICODE)]


def main():
    out = {}
    for f in sorted(glob.glob("/root/cov_*.txt")):
        lang = os.path.basename(f)[4:-4]
        fst = analyzer(lang)
        if not fst:
            continue
        from collections import Counter
        unc = Counter()
        seen, n = set(), 0
        for line in open(f, encoding="utf-8"):
            for t in toks(line):
                if t in seen:
                    continue
                seen.add(t)
                n += 1
                if n > 8000:
                    break
                for a in (fst.lookup(t) or fst.lookup(t.lower()) or []):
                    for tag in re.findall(r"<([^>]+)>", a[0]):
                        if tag not in KNOWN:
                            unc[tag] += 1
            if n > 8000:
                break
        out[lang] = dict(unc.most_common(25))
        top = ", ".join(f"{k}({v})" for k, v in unc.most_common(15)) or "(hepsi kapsanıyor)"
        print(f"{lang:4} kapsanmayan: {top}")
    print("===JSON===")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
