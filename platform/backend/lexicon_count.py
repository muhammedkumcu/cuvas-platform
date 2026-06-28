#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SÖZLÜK ZENGİNLİĞİ — apertium tek-dilli sözlüklerindeki KÖK (stem) sayısı, TÜRÜNE GÖRE.
Neden: apertium morfoloji = sözlükten (kök + paradigma) derlenen FST; aynı FST hem analiz hem
üretim yapar → kök sayısı İKİSİNİ DE sınırlar = dilin dijital morfolojik zenginliği.

YÖNTEM (uniform — hem 'POS-adlı lexicon' hem 'Common+continuation' yapısı için):
Her stem girişi bir CONTINUATION sınıfına gider (N1/V-TV/A1/ADV/NUM...). Bu sınıfın adı POS'u
kodlar. Girişleri continuation sınıfının POS'una göre sayarız. Morfotaktik girişler (CASE/PLURAL/
CLIT → başka morfotaktik sınıf) POS-stem sınıfına gitmediği için sayılmaz. Eşlenmeyen sınıflar
ayrıca raporlanır → KESİNLİK (uydurma/tahmin yok). Kaynak: apertium-<lang> .lexc (GPL-3.0).
"""
import os, re, sys, glob, json
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.environ.get("APT_ROOT", "/tmp/apt3")
LANGS = os.environ.get("APT_LANGS", "tur aze kaz kir uzb uig tat bak chv sah tuk crh gag kaa alt kjh krc kum nog tyv").split()
DIAG = os.environ.get("APT_DIAG", "")  # boş değilse eşlenmeyen continuation sınıflarını bas


def pos_of_cont(c):
    """Continuation sınıf adı → POS (apertium-turkic konvansiyonu)."""
    u = c.upper().lstrip("%")
    # özel ad / sayı önce (N ile başlayabilir)
    if u.startswith(("NP", "PROP", "TOP", "ANTHR", "COG", "AL", "PATR")):
        return "özel"
    if u.startswith("NUM"):
        return "sayı"
    if u.startswith("ADV"):
        return "zarf"
    if u.startswith(("ADJ",)) or re.match(r"A[0-9]", u) or u == "A":
        return "sıfat"
    if re.match(r"N([0-9]|-|$|OM|UN|ABBR)", u) or u in ("N", "SUBST", "NOMINAL"):
        return "isim"
    if u.startswith("V") and not u.startswith(("VAUX-ONLY",)):
        return "fiil"
    if u.startswith(("PRON", "PRN", "PERS-PRON")):
        return "zamir"
    if u.startswith(("CNJ", "CONJ", "POST", "ADP", "INTERJ", "DET", "PCLE", "PRCL")):
        return "diğer"
    return None


def parse_lang(d):
    files = glob.glob(os.path.join(d, "**", "*.lexc"), recursive=True)
    if not files:
        return None, {}
    by_pos = {}
    unmapped = {}
    for f in files:
        try:
            lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
        except Exception:
            continue
        cur = None
        for ln in lines:
            m = re.match(r"\s*LEXICON\s+(\S+)", ln)
            if m:
                cur = m.group(1)
                continue
            s = ln.strip()
            if not s or s.startswith("!"):
                continue
            # inline yorum at: % ile escape edilmemiş ilk '!'
            body = re.split(r"(?<!%)!", s, 1)[0].strip()
            # continuation = ';'den önceki SON geçerli lexicon-adı (ağırlık/gloss "..."1.0 vb. atlanır)
            mm = re.search(r'([A-Za-z][A-Za-z0-9_\-]*)\s*(?:"[^"]*"|[0-9.]+|@[^@]*@|\s)*;\s*$', body)
            if not mm:
                continue
            cont = mm.group(1)
            p = pos_of_cont(cont)
            if p and p != "diğer":
                by_pos[p] = by_pos.get(p, 0) + 1
            elif p is None:
                unmapped[cont] = unmapped.get(cont, 0) + 1
    return by_pos, unmapped


def main():
    print("=" * 90)
    print(f"{'dil':4} {'isim':>7} {'fiil':>7} {'sıfat':>7} {'zarf':>6} {'özel':>7} {'sayı':>5} {'zamir':>6} {'İÇERİK':>8}")
    print("-" * 90)
    data = {}
    for lang in LANGS:
        d = os.path.join(ROOT, "apertium-" + lang)
        by_pos, unmapped = parse_lang(d)
        if by_pos is None:
            print(f"{lang:4}  (.lexc yok)")
            data[lang] = None
            continue
        g = lambda p: by_pos.get(p, 0)
        content = g("isim") + g("fiil") + g("sıfat") + g("zarf") + g("sayı") + g("zamir")
        data[lang] = {"isim": g("isim"), "fiil": g("fiil"), "sıfat": g("sıfat"), "zarf": g("zarf"),
                      "özel": g("özel"), "sayı": g("sayı"), "zamir": g("zamir"), "icerik": content}
        print(f"{lang:4} {g('isim'):7} {g('fiil'):7} {g('sıfat'):7} {g('zarf'):6} {g('özel'):7} "
              f"{g('sayı'):5} {g('zamir'):6} {content:8}")
        if DIAG and unmapped:
            top = sorted(unmapped.items(), key=lambda x: -x[1])[:8]
            print(f"     eşlenmeyen continuation (büyükler): {top}")
    print("-" * 90)
    print("===JSON===")
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
