# -*- coding: utf-8 -*-
"""
corpus_coverage.py — Çuvaş Wikipedia'sından gerçek metin çekip morfolojik
analizörün TOKEN ve TÜR (type) kapsamını ölçer (Türkmence makalesindeki metodoloji).

Kapsam = analizörün en az bir geçerli çözüm verdiği token oranı.
Tanınmayan yüksek-frekanslı türleri (gap analysis) raporlar.
"""
from __future__ import annotations
import json, re, sys, time, urllib.parse, urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path("chuvash-fst")))
from chuvash_fst import Lexicon, Analyzer  # noqa: E402
from chuvash_fst.phonology import normalize  # noqa: E402

API = "https://cv.wikipedia.org/w/api.php"
SEED = "chuvash-fst/data/chuvash_lexicon_seed.txt"
TOKEN_RE = re.compile(r"[а-яёӑӗҫӳ]{2,}", re.IGNORECASE)  # >=2 harf (tek harf = gürültü)
TARGET_TOKENS = 25000
UA = "ChuvashFST/0.1 (https://github.com/muhammedkumcu/cuvas-platform; research)"


def fetch_random_text(target_tokens):
    text = []
    n = 0
    for _ in range(30):
        p = {"action": "query", "generator": "random", "grnnamespace": "0",
             "grnlimit": "10", "prop": "extracts", "explaintext": "1",
             "exintro": "1", "exlimit": "20", "format": "json"}  # exintro = temiz lead prose
        req = urllib.request.Request(API + "?" + urllib.parse.urlencode(p),
                                     headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
        except Exception as e:
            print("uyarı:", e); time.sleep(3); continue
        for pg in d.get("query", {}).get("pages", {}).values():
            ex = pg.get("extract", "")
            if ex and len(ex) > 80:  # gerçek prose (stub/boş değil)
                text.append(ex)
                n += len(TOKEN_RE.findall(ex))
        print(f"  …{n} token", end="\r")
        if n >= target_tokens:
            break
        time.sleep(2.0)  # rate-limit'e saygı
    print()
    return "\n".join(text)


CACHE = Path("sources/_wiki_raw.txt")  # tekrar çekmemek için (gitignored)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if CACHE.exists():
        print(f"Önbellekten okunuyor: {CACHE}")
        raw = CACHE.read_text(encoding="utf-8")
    else:
        print("Çuvaş Wikipedia'dan metin çekiliyor…")
        raw = fetch_random_text(TARGET_TOKENS)
        CACHE.parent.mkdir(exist_ok=True)
        CACHE.write_text(raw, encoding="utf-8")
    # KRİTİK: tüm metni ÖNCE NFC normalize et (ayrık ӑ/ӗ -> birleşik) + homoglyph + küçült
    raw = normalize(raw).lower()
    tokens = TOKEN_RE.findall(raw)
    freq = Counter(tokens)
    print(f"Toplam token: {len(tokens)} · benzersiz tür: {len(freq)}")

    az = Analyzer(Lexicon().load(SEED))

    # her türü bir kez analiz et (önbellek)
    recognized_types = {}
    for t in freq:
        recognized_types[t] = az.analyze(t).success

    rec_tokens = sum(c for t, c in freq.items() if recognized_types[t])
    rec_types = sum(1 for t in freq if recognized_types[t])
    tok_cov = 100 * rec_tokens / max(len(tokens), 1)
    typ_cov = 100 * rec_types / max(len(freq), 1)

    print("\n=== KAPSAM SONUÇLARI (Çuvaş Wikipedia) ===")
    print(f"Token kapsamı: {rec_tokens}/{len(tokens)}  =  %{tok_cov:.2f}")
    print(f"Tür  kapsamı : {rec_types}/{len(freq)}  =  %{typ_cov:.2f}")

    print("\n=== En sık TANINMAYAN türler (gap analysis) ===")
    unrec = [(t, c) for t, c in freq.most_common() if not recognized_types[t]]
    for t, c in unrec[:30]:
        print(f"  {c:5d}  {t}")

    # rapor kaydet
    out = Path("chuvash-fst/data/coverage_report.json")
    out.write_text(json.dumps({
        "corpus": "cv.wikipedia.org (random)", "tokens": len(tokens),
        "types": len(freq), "token_coverage": round(tok_cov, 2),
        "type_coverage": round(typ_cov, 2),
        "top_unrecognized": unrec[:50],
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRapor: {out}")


if __name__ == "__main__":
    main()
