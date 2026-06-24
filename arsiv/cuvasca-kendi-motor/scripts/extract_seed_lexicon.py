# -*- coding: utf-8 -*-
"""
extract_seed_lexicon.py — apertium-chv .lexc dosyasından kök (stem) sözlüğü çıkarır.

apertium-chv.chv.lexc yapısı:
  - Satır ~160-1219: morfotaktik continuation class'lar (atlanır)
  - Stem (kök) bölümleri (top-level LEXICON'lar):
      Miscellaneous, Postposition, Conjunction, Adjectives, Adverbs,
      Nouns, Verbs, Proper, Numerals, Pronouns, Determiners
  - Sonda: DIGITLEX, NP-UNK, GUESS-QUEUE, Guesser (atlanır)

Stem giriş formatı:
  lemma:morfofonemik_kök%{...%}   CONT_CLASS ;   ! "rusça gloss"
  (ör:  ҫын:ҫын%{ː%}   N ;   ! "человек")

Çıktı: chuvash-fst/data/chuvash_lexicon_seed.txt
  lemma<TAB>%<pos%>[<TAB>gloss_ru:...]
"""
from __future__ import annotations
import re, sys, io
from pathlib import Path
from collections import Counter, OrderedDict

LEXC = Path("sources/apertium-chv/apertium-chv.chv.lexc")
OUT  = Path("chuvash-fst/data/chuvash_lexicon_seed.txt")

# Hangi top-level LEXICON bölümü hangi POS'a karşılık geliyor
SECTION_POS = {
    "Nouns": "n",
    "Verbs": "v",
    "Adjectives": "adj",
    "Adverbs": "adv",
    "Proper": "np",
    "Numerals": "num",
    "Pronouns": "prn",
    "Determiners": "det",
    "Postposition": "post",
    "Conjunction": "cnj",
    "Miscellaneous": "misc",
}
# Bunlar stem bölümü DEĞİL (morfotaktik veya guesser) — atla
SKIP_SECTIONS = {"DIGITLEX", "NP-UNK", "GUESS-QUEUE", "Guesser", "Punctuation"}

TAG_RE   = re.compile(r"%<[^>]*%>")      # %<n%> gibi etiket emisyonları
ARCHI_RE = re.compile(r"%\{[^}]*%\}")    # %{ː%}, %{A%} gibi arşifonemler


def clean_lemma(entry: str) -> str:
    """Stem girişinin sol tarafından temiz yüzey lemmasını çıkar."""
    # ':' öncesi = yüzey lemma (sağ taraf morfofonemik gövde)
    lemma = entry.split(":", 1)[0]
    lemma = TAG_RE.sub("", lemma)
    lemma = ARCHI_RE.sub("", lemma)
    # lexc kaçışlarını çöz: %X -> X  (%+ %< vs.)
    lemma = re.sub(r"%(.)", r"\1", lemma)
    lemma = lemma.strip().lstrip("+").strip()
    return lemma


def main():
    if not LEXC.exists():
        sys.exit(f"BULUNAMADI: {LEXC.resolve()}")

    current_section = None
    in_stem_section = False
    pos = None
    # lemma -> (pos, gloss)  (ilk görülen korunur; tekrarları say)
    entries: "OrderedDict[tuple, str]" = OrderedDict()
    dup = 0
    per_pos = Counter()

    with LEXC.open(encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.strip()

            # LEXICON başlığı mı?
            m = re.match(r"^LEXICON\s+(\S+)", stripped)
            if m:
                current_section = m.group(1)
                if current_section in SECTION_POS:
                    in_stem_section = True
                    pos = SECTION_POS[current_section]
                else:
                    in_stem_section = False
                    pos = None
                continue

            if not in_stem_section:
                continue
            if not stripped or stripped.startswith("!"):
                continue

            # gloss'u ayır (yorum)
            gloss = ""
            if "!" in stripped:
                code, _, after = stripped.partition("!")
                gloss = after.strip().strip('"').strip()
            else:
                code = stripped

            code = code.strip()
            if not code or code.endswith("#") and ";" not in code:
                continue
            # 'entry  CONT ;' -> entry = ilk whitespace token
            # ';' ve sonrasını at
            code = code.split(";", 1)[0].strip()
            if not code:
                continue
            entry_tok = code.split()[0]
            lemma = clean_lemma(entry_tok)

            if not lemma:
                continue
            # tek karakterli noktalama / rakam vs. ele
            if all(not (c.isalpha()) for c in lemma):
                continue

            # Gemination: apertium morfofonemik gövdesinde %{ː%} işareti varsa
            # kök sonu ünsüz ek alırken ikizleşir (ҫын -> ҫынн-)
            rhs = entry_tok.split(":", 1)[1] if ":" in entry_tok else ""
            geminates = ("ː" in rhs) or ("%{ː%}" in entry_tok)

            key = (lemma, pos)
            if key in entries:
                dup += 1
                continue
            entries[key] = {"gloss": gloss, "gem": geminates}
            per_pos[pos] += 1

    # yaz
    OUT.parent.mkdir(parents=True, exist_ok=True)
    gem_count = 0
    with OUT.open("w", encoding="utf-8") as out:
        for (lemma, pos), info in entries.items():
            feats = []
            if info["gem"]:
                feats.append("gemination")
                gem_count += 1
            if info["gloss"]:
                feats.append("ru:" + info["gloss"])
            if feats:
                out.write(f"{lemma}\t%<{pos}%>\t{';'.join(feats)}\n")
            else:
                out.write(f"{lemma}\t%<{pos}%>\n")

    # rapor
    total = len(entries)
    print(f"Toplam benzersiz (lemma,pos): {total}")
    print(f"Atlanan tekrar: {dup}")
    print("POS dağılımı:")
    for p, c in per_pos.most_common():
        print(f"  {p:6s} {c:6d}  (%{100*c/total:.1f})")
    print(f"Gemination işaretli kök: {gem_count}")
    print(f"\nÇıktı: {OUT}")

    # benzersiz lemma (POS'tan bağımsız)
    uniq_lemmas = len({l for (l, _) in entries})
    print(f"Benzersiz lemma (POS'tan bağımsız): {uniq_lemmas}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
