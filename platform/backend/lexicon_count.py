#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SÖZLÜK ZENGİNLİĞİ — apertium tek-dilli sözlüklerindeki KÖK (stem) sayısı, TÜRÜNE GÖRE.
Neden: apertium morfoloji = sözlükten (kök listesi + paradigmalar) derlenen FST; aynı FST hem
analiz hem üretim yapar → sözlükteki kök sayısı İKİSİNİ DE doğrudan sınırlar. Bu sayılar dilin
dijital morfolojik zenginliğini/yoksulluğunu gösterir (araştırmacı için kıymetli).
Yöntem: .lexc dosyalarında 'LEXICON Root' doğrudan POS-adlı stem lexicon'larına dallanır
(Nouns/Verbs/Adjectives/Adverbs/Proper/Numerals/Pronouns...). Her POS lexicon'undaki giriş = o
türde bir kök. Root'un REFERANS verdiği lexicon'lar sayılır (morfotaktik V-FIN/CASE vb. hariç).
Kaynak: apertium-<lang> repoları (GPL-3.0), /tmp/apt3'e klonlanmış. Uydurma yok; yapı farklıysa işaretli.
"""
import os, re, sys, glob, json
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.environ.get("APT_ROOT", "/tmp/apt3")
LANGS = ["tur", "aze", "kaz", "kir", "uzb", "uig", "tat", "bak", "chv", "sah",
         "tuk", "crh", "gag", "kaa", "alt", "kjh", "krc", "kum", "nog", "tyv"]

POS_TR = {"isim": "isim", "fiil": "fiil", "sıfat": "sıfat", "zarf": "zarf",
          "özel": "özel ad", "sayı": "sayı", "zamir": "zamir", "edat": "edat/bağlaç"}


def pos_of(name):
    n = name.lower()
    if n.startswith(("noun", "subst")) or n == "n":
        return "isim"
    if n.startswith("verb") or n == "v":
        return "fiil"
    if n.startswith(("adject", "adj")):
        return "sıfat"
    if n.startswith(("adverb", "adv")):
        return "zarf"
    if n.startswith(("proper", "propn", "np", "toponym")):
        return "özel"
    if n.startswith(("numeral", "num")):
        return "sayı"
    if n.startswith(("pronoun", "pron")):
        return "zamir"
    if n.startswith(("postp", "conj", "adposition")):
        return "edat"
    return None


def parse_lexc(files):
    """Tüm .lexc dosyalarını oku: lexicon -> giriş sayısı; ayrıca Root'un referansları."""
    counts = {}
    root_refs = set()
    for f in files:
        cur = None
        in_root = False
        try:
            lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
        except Exception:
            continue
        for ln in lines:
            m = re.match(r"\s*LEXICON\s+(\S+)", ln)
            if m:
                cur = m.group(1)
                in_root = (cur == "Root")
                counts.setdefault(cur, 0)
                continue
            s = ln.strip()
            if not s or s.startswith("!"):
                continue
            if in_root:
                # Root referansı: 'LexiconName ;' (giriş değil, dallanma)
                r = re.match(r"([A-Za-z0-9_\-]+)\s*;", s)
                if r:
                    root_refs.add(r.group(1))
            elif cur and cur != "Root":
                counts[cur] = counts.get(cur, 0) + 1
    return counts, root_refs


def main():
    print("=" * 84)
    print(f"{'dil':4} {'isim':>7} {'fiil':>7} {'sıfat':>7} {'zarf':>6} {'özel ad':>8} {'sayı':>5} {'zamir':>6} {'İÇERİK':>8}  not")
    print("-" * 84)
    data = {}
    for lang in LANGS:
        d = os.path.join(ROOT, "apertium-" + lang)
        files = glob.glob(os.path.join(d, "**", "*.lexc"), recursive=True)
        if not files:
            print(f"{lang:4} {'(.lexc bulunamadı / repo yok ya da farklı yapı)':>40}")
            data[lang] = None
            continue
        counts, root_refs = parse_lexc(files)
        # Root referansı varsa onları, yoksa POS-eşleşen tüm lexicon'ları kullan
        names = root_refs if root_refs else set(counts)
        by_pos = {}
        for nm in names:
            p = pos_of(nm)
            if p:
                by_pos[p] = by_pos.get(p, 0) + counts.get(nm, 0)
        get = lambda p: by_pos.get(p, 0)
        content = get("isim") + get("fiil") + get("sıfat") + get("zarf") + get("sayı") + get("zamir")
        note = "" if content > 0 else "POS lexicon eşleşmedi (yapı farklı)"
        data[lang] = {"isim": get("isim"), "fiil": get("fiil"), "sıfat": get("sıfat"),
                      "zarf": get("zarf"), "özel": get("özel"), "sayı": get("sayı"),
                      "zamir": get("zamir"), "icerik": content}
        print(f"{lang:4} {get('isim'):7} {get('fiil'):7} {get('sıfat'):7} {get('zarf'):6} "
              f"{get('özel'):8} {get('sayı'):5} {get('zamir'):6} {content:8}  {note}")
    print("-" * 84)
    print("İÇERİK = isim+fiil+sıfat+zarf+sayı+zamir (özel ad = yer/kişi adları ayrı). Kaynak: apertium .lexc (GPL-3.0).")
    print("===JSON===")
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
