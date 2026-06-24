#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KÖKEN Morfoloji API — Apertium FST'lerini saran FastAPI backend.

Çalışma yeri: LİNUX VM (apertium/hfst Windows'ta derlenmez). Bkz. DEVAM.md §2.
Motor   : Apertium morfolojik FST'leri (analiz=automorf, üretim=autogen), turkicnlp ile indirilmiş.
Kaynak  : Apertium (GPL-3.0). Her yanıt `_source` ile künye taşır.
Diller  : MVP 10 — tur, aze, kaz, kir, uzb, uig, tat, bak, chv, sah.

Çalıştır (VM'de):
    /root/apv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
"""
import os, glob, re
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hfst

BASE = os.path.expanduser("~/.turkicnlp/models")
SOURCE = {"source": "Apertium FST", "license": "GPL-3.0", "via": "turkicnlp"}

LANG_INFO = {
    "tur": ("Türkçe", "Latn"), "aze": ("Azerbaycanca", "Latn"), "kaz": ("Kazakça", "Cyrl"),
    "kir": ("Kırgızca", "Cyrl"), "uzb": ("Özbekçe", "Latn"), "uig": ("Uygurca", "Arab"),
    "tat": ("Tatarca", "Cyrl"), "bak": ("Başkurtça", "Cyrl"), "chv": ("Çuvaşça", "Cyrl"),
    "sah": ("Sahaca (Yakut)", "Cyrl"),
}
LANGS = list(LANG_INFO)

# isim çekimi paradigması için ortak apertium etiket şablonu (üretip tutanlar gösterilir)
CASES = ["nom", "gen", "dat", "acc", "loc", "abl", "ins"]
CASE_SET = set(CASES)
CASE_TR = {"nom": "Yalın", "gen": "İlgi", "dat": "Yönelme", "acc": "Belirtme",
           "loc": "Bulunma", "abl": "Ayrılma", "ins": "Araç"}
# fiil çekimi: zaman × (kişi×sayı). Diller arası etiket farklı (Türkçe ifi, Çuvaşça pres/past/fut) →
# adaylar denenir, yalnız ÜRETİLEN hücreler tabloya girer (dinamik).
V_TENSES = [("pres", "Şimdiki/geniş"), ("past", "Geçmiş"), ("ifi", "Görülen geçmiş"),
            ("fut", "Gelecek"), ("aor", "Geniş zaman"), ("cond", "Şart")]
V_PERSONS = [("p1", "sg", "1. tekil"), ("p2", "sg", "2. tekil"), ("p3", "sg", "3. tekil"),
             ("p1", "pl", "1. çoğul"), ("p2", "pl", "2. çoğul"), ("p3", "pl", "3. çoğul")]
# apertium etiketi → okunur Türkçe (ek glossları için)
TAG_TR = {"pl": "çokluk", "nom": "yalın", "gen": "ilgi", "dat": "yönelme", "acc": "belirtme",
          "loc": "bulunma", "abl": "ayrılma", "ins": "araç", "cop": "ek-fiil", "ifi": "görülen geçmiş",
          "past": "geçmiş", "pres": "şimdiki/geniş", "fut": "gelecek", "aor": "geniş", "cond": "şart",
          "p1": "1. kişi", "p2": "2. kişi", "p3": "3. kişi", "sg": "tekil", "imp": "emir", "attr": "sıfat",
          "px1sg": "iyelik (benim)", "px2sg": "iyelik (senin)", "px3sp": "iyelik (onun)"}

_cache = {}


def _find(lang: str, kind: str) -> Optional[str]:
    hits = glob.glob(f"{BASE}/{lang}/**/{lang}.{kind}.hfst", recursive=True)
    return hits[0] if hits else None


def _fst(lang: str, kind: str):
    key = (lang, kind)
    if key not in _cache:
        path = _find(lang, kind)
        if not path:
            raise HTTPException(404, f"{lang} için {kind} FST yok")
        _cache[key] = hfst.HfstInputStream(path).read()
    return _cache[key]


def _parse(raw: str) -> dict:
    """'хӗр<n><pl><nom>' -> {lemma, tags[]}; bileşik (+) ham bırakılır."""
    lemma = re.split(r"[<+]", raw, 1)[0]
    tags = re.findall(r"<([^>]+)>", raw)
    return {"raw": raw, "lemma": lemma, "tags": tags}


def _gen1(gen, query: str):
    """autogen ile tek yüzey biçimi (yoksa None)."""
    res = gen.lookup(query)
    return res[0][0] if res else None


def _suffix(a: str, b: str) -> str:
    """b'nin a ile ortak ön ekinden sonrası (yüzey eki yaklaşık)."""
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    return b[i:]


def _segment_noun(gen, lemma, tags):
    """İsim: kök + (çokluk) + (iyelik) + (hâl) yüzey eklerini kümülatif üretim+farkla çıkarır."""
    has_pl = "pl" in tags
    px = next((t for t in tags if t.startswith("px")), None)
    case = next((t for t in tags if t in CASE_SET), "nom")
    pre = ("<pl>" if has_pl else "")
    root = _gen1(gen, f"{lemma}<n><nom>") or lemma
    morphs = [{"surface": root, "tag": "KÖK", "feat": "kök", "type": "kök"}]
    base = root
    if has_pl:
        sp = _gen1(gen, f"{lemma}<n><pl><nom>")
        if sp:
            morphs.append({"surface": _suffix(base, sp), "tag": "ÇĞL", "feat": "çokluk", "type": "çokluk"})
            base = sp
    if px:
        pf = _gen1(gen, f"{lemma}<n>{pre}<{px}>")
        if pf:
            morphs.append({"surface": _suffix(base, pf), "tag": px.upper(),
                           "feat": TAG_TR.get(px, px), "type": "iyelik"})
            base = pf
    if case != "nom":
        full = _gen1(gen, f"{lemma}<n>{pre}" + (f"<{px}>" if px else "") + f"<{case}>")
        if full:
            morphs.append({"surface": _suffix(base, full), "tag": case.upper(),
                           "feat": CASE_TR.get(case, case) + " hâli", "type": "hâl"})
    return morphs


def _reconstructs(morphs, word):
    return "".join(m["surface"] for m in morphs) == word


def _fallback_split(gen, lemma, tags, word, pos):
    """Allomorf/ses-değişimi yüzünden çok-parçalı bölünme tutmazsa: kök + kaynaşık kalan ek (dürüst)."""
    if pos == "v":
        root = lemma
        for tr in ("tv", "iv"):
            s = _gen1(gen, f"{lemma}<v><{tr}><imp><p2><sg>")
            if s:
                root = s
                break
        skip = ("v", "tv", "iv")
    else:
        root = _gen1(gen, f"{lemma}<n><nom>") or lemma
        skip = ("n", "nom", "attr")
    morphs = [{"surface": root, "tag": "KÖK", "feat": "kök" if pos == "n" else "fiil kökü", "type": "kök"}]
    rem = _suffix(root, word)
    if rem:
        feats = [t for t in tags if t not in skip]
        morphs.append({"surface": rem, "tag": "+".join(t.upper() for t in feats) or "EK",
                       "feat": " · ".join(TAG_TR.get(t, t) for t in feats) or "ek",
                       "type": "zaman" if pos == "v" else "hâl"})
    return morphs


def _segment_verb(gen, lemma, tags, word):
    """Fiil: kök (emir 2.tekil ~ yalın gövde) + kalan yüzey (zaman·kişi kaynaşık)."""
    stem = None
    for tr in ("tv", "iv"):
        stem = _gen1(gen, f"{lemma}<v><{tr}><imp><p2><sg>")
        if stem:
            break
    stem = stem or lemma
    morphs = [{"surface": stem, "tag": "KÖK", "feat": "fiil kökü", "type": "kök"}]
    rest = _suffix(stem, word)
    if rest:
        feats = [t for t in tags if t not in ("v", "tv", "iv")]
        morphs.append({"surface": rest, "tag": "+".join(t.upper() for t in feats),
                       "feat": " · ".join(TAG_TR.get(t, t) for t in feats), "type": "zaman"})
    return morphs


# --- Needleman-Wunsch hizalama ile yüzey bölümleme (deepsearch önerisi) ---
# Apertium lemma+etiket verir; kümülatif üretim + fonolojik-cezalı hizalama ile GERÇEK yüzey ekleri
# ve ses olayları (yumuşama/ünlü düşmesi) otomatik çıkar. El-allomorf tablosu GEREKMEZ; sadece
# fonolojik denklik (sesli~sesli, yumuşama çiftleri) puanlaması — Türk dilleri geneli.
TURKIC_VOWELS = set("aâeıiîoöuûüAÂEIİÎOÖUÛÜ"
                    "аәеёиоөуүұыэюяіАӘЕЁИОӨУҮҰЫЭЮЯІӑӗӳӐӖӲ")
_VOICE_PAIRS = [("p", "b"), ("ç", "c"), ("t", "d"), ("k", "g"), ("k", "ğ"), ("g", "ğ"), ("q", "ğ"),
                ("п", "б"), ("т", "д"), ("к", "г"), ("қ", "ғ"), ("ш", "ж"), ("с", "з"), ("х", "г")]
_VOICE = set()
for _a, _b in _VOICE_PAIRS:
    _VOICE.add((_a, _b)); _VOICE.add((_b, _a))


def _is_vowel(c):
    return c.lower() in TURKIC_VOWELS


def _nw_cols(a, b):
    """Needleman-Wunsch hizalama; fonolojik puanlama. Sütunlar: (a_harf|'', b_harf|'')."""
    GAP = -2

    def sc(x, y):
        if x == y:
            return 3
        if (x.lower(), y.lower()) in _VOICE:
            return 2
        if _is_vowel(x) and _is_vowel(y):
            return 1
        return -2
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        D[i][0] = i * GAP
    for j in range(1, m + 1):
        D[0][j] = j * GAP
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = max(D[i - 1][j - 1] + sc(a[i - 1], b[j - 1]), D[i - 1][j] + GAP, D[i][j - 1] + GAP)
    i, j, cols = n, m, []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + sc(a[i - 1], b[j - 1]):
            cols.append((a[i - 1], b[j - 1])); i -= 1; j -= 1
        elif i > 0 and D[i][j] == D[i - 1][j] + GAP:
            cols.append((a[i - 1], "")); i -= 1
        else:
            cols.append(("", b[j - 1])); j -= 1
    cols.reverse()
    return cols


def _nw_score(a, b):
    """Sadece NW hizalama skoru (geri-iz yok); O(n) bellek."""
    GAP = -2

    def sc(x, y):
        if x == y:
            return 3
        if (x.lower(), y.lower()) in _VOICE:
            return 2
        if _is_vowel(x) and _is_vowel(y):
            return 1
        return -2
    m = len(b)
    prevrow = [j * GAP for j in range(m + 1)]
    for i in range(1, len(a) + 1):
        ai = a[i - 1]
        cur = [i * GAP] + [0] * m
        for j in range(1, m + 1):
            cur[j] = max(prevrow[j - 1] + sc(ai, b[j - 1]), prevrow[j] + GAP, cur[j - 1] + GAP)
        prevrow = cur
    return prevrow[m]


def _trailing_affix(prev, cur):
    """cur = (ses-değişmiş prev gövdesi) + ek. Gövde ÖNDE olduğundan, prev'e en iyi oturan ön-ek
    sınırı k≈len(prev) civarında aranır → ek = cur[k:]. Tekrar-altdizi (балалар) ve ünlü düşmesine
    (burun→burnu) dayanıklıdır; saf sondan-soymanın kaydığı yerleri düzeltir."""
    if not prev:
        return cur
    lo = max(1, len(prev) - 3)
    hi = min(len(cur), len(prev) + 4)
    best_k = min(len(prev), len(cur))
    best = None
    for k in range(lo, hi + 1):
        s = _nw_score(prev, cur[:k])
        if best is None or s > best:
            best, best_k = s, k
    return cur[best_k:]


def _classify_change(frm, to):
    if to in ("", "∅"):
        return "ünlü düşmesi" if _is_vowel(frm) else "ünsüz düşmesi"
    if (frm.lower(), to.lower()) in _VOICE:
        return "ünsüz yumuşaması"
    if _is_vowel(frm) and _is_vowel(to):
        return "ünlü değişimi"
    return "ses değişimi"


def _sound_changes(lemma, root):
    """Sözlük kökü (lemma) vs yüzeydeki gövde (root) farkı → ses olayları listesi."""
    if lemma == root:
        return []
    out = []
    for ca, cb in _nw_cols(lemma, root):
        if ca and cb and ca != cb:
            out.append({"type": _classify_change(ca, cb), "from": ca, "to": cb})
        elif ca and not cb:
            out.append({"type": _classify_change(ca, "∅"), "from": ca, "to": "∅"})
        elif cb and not ca:
            out.append({"type": "ses türemesi", "from": "∅", "to": cb})
    return out


def _segment_align(gen, lemma, tags, word):
    """İSİM: kümülatif üretim (nom-sonlu ara biçimler) + NW hizalama → gerçek yüzey ekleri + ses olayları.
    Üretim eksik/yeniden üretmiyorsa None → çağıran fallback'e düşer."""
    if not tags or tags[0] != "n":
        return None
    has_pl = "pl" in tags
    px = next((t for t in tags if t.startswith("px")), None)
    case = next((t for t in tags if t in CASE_SET), "nom")
    pre = "<pl>" if has_pl else ""
    levels = [("kök", f"{lemma}<n><nom>")]
    if has_pl:
        levels.append(("pl", f"{lemma}<n><pl><nom>"))
    if px:
        levels.append((px, f"{lemma}<n>{pre}<{px}><nom>"))
    if case != "nom":
        levels.append((case, f"{lemma}<n>{pre}" + (f"<{px}>" if px else "") + f"<{case}>"))
    surfaces = []
    for _lab, q in levels:
        s = _gen1(gen, q)
        if s is None:
            return None
        surfaces.append(s)
    if surfaces[-1] != word:
        return None
    affixes = []
    for i in range(1, len(levels)):
        affixes.append((levels[i][0], _trailing_affix(surfaces[i - 1], surfaces[i])))
    total = sum(len(a) for _, a in affixes)
    root_surface = word[:len(word) - total] if 0 < total <= len(word) else surfaces[0]
    # Büyük kutuda SÖZLÜK kökü (lemma) gösterilir; yüzeydeki ses-değişmiş gövde (root_surface) yalnız
    # ses-olayı rozetinde işaretlenir (kitap → kitab). Linguistik olarak doğrusu kanonik köktür.
    morphs = [{"surface": lemma, "tag": "KÖK", "feat": "kök", "type": "kök"}]
    for tag, aff in affixes:
        if not aff:
            continue
        if tag == "pl":
            typ, feat = "çokluk", "çokluk"
        elif tag.startswith("px"):
            typ, feat = "iyelik", TAG_TR.get(tag, tag)
        elif tag in CASE_SET:
            typ, feat = "hâl", CASE_TR.get(tag, tag) + " hâli"
        else:
            typ, feat = "hâl", TAG_TR.get(tag, tag)
        morphs.append({"surface": aff, "tag": tag.upper(), "feat": feat, "type": typ})
    return morphs, _sound_changes(lemma, root_surface)


def _build_verb(gen, lemma):
    """Fiil çekim blokları: yalnız ÜRETİLEN zaman/kişi hücreleri (dile göre dinamik)."""
    blocks = []
    for ttag, ttr in V_TENSES:
        cells, any_c = [], False
        for ptag, num, ptr in V_PERSONS:
            surf = None
            for tr in ("tv", "iv"):
                surf = _gen1(gen, f"{lemma}<v><{tr}><{ttag}><{ptag}><{num}>")
                if surf:
                    break
            cells.append({"person": ptr, "surface": surf})
            any_c = any_c or bool(surf)
        if any_c:
            blocks.append({"tense": ttr, "tense_tag": ttag, "cells": cells})
    return blocks


app = FastAPI(title="KÖKEN Morfoloji API", version="0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class AnalyzeReq(BaseModel):
    lang: str
    word: str


class GenerateReq(BaseModel):
    lang: str
    query: str          # ör. "хӗр<n><pl><dat>"


class AnalyzeAllReq(BaseModel):
    word: str


@app.get("/health")
def health():
    return {"ok": True, "langs": LANGS, "models_base": BASE, "_source": SOURCE}


@app.get("/languages")
def languages():
    out = []
    for c in LANGS:
        name, script = LANG_INFO[c]
        out.append({"code": c, "name": name, "script": script,
                    "analyzer": bool(_find(c, "automorf")), "generator": bool(_find(c, "autogen"))})
    return {"languages": out, "_source": SOURCE}


@app.post("/analyze")
def analyze(req: AnalyzeReq):
    if req.lang not in LANGS:
        raise HTTPException(400, f"desteklenmeyen dil: {req.lang}")
    fst = _fst(req.lang, "automorf")
    res = fst.lookup(req.word.strip())
    analyses = [{**_parse(r[0]), "weight": r[1]} for r in res]
    return {"lang": req.lang, "word": req.word, "count": len(analyses),
            "analyses": analyses, "_source": SOURCE}


@app.post("/analyze_all")
def analyze_all(req: AnalyzeAllReq):
    """Kelimeyi TÜM MVP dillerinde dener; yalnız çözümlenen diller döner (multi-dil otomatik)."""
    word = req.word.strip()
    out = {}
    for lang in LANGS:
        try:
            res = _fst(lang, "automorf").lookup(word)
        except HTTPException:
            continue
        if res:
            out[lang] = [{**_parse(r[0]), "weight": r[1]} for r in res]
    return {"word": word, "count": len(out), "langs": out, "_source": SOURCE}


@app.post("/generate")
def generate(req: GenerateReq):
    if req.lang not in LANGS:
        raise HTTPException(400, f"desteklenmeyen dil: {req.lang}")
    fst = _fst(req.lang, "autogen")
    res = fst.lookup(req.query.strip())
    return {"lang": req.lang, "query": req.query,
            "forms": [{"surface": r[0], "weight": r[1]} for r in res], "_source": SOURCE}


@app.post("/segment")
def segment(req: AnalyzeReq):
    """Canlı analizi GERÇEK yüzey eklerine böler (apertium etiket değil): kök + ekler.
    İsim hâl/çokluk eklerini kümülatif üretim+farkla; fiilde kök + kaynaşık ek."""
    if req.lang not in LANGS:
        raise HTTPException(400, f"desteklenmeyen dil: {req.lang}")
    word = req.word.strip()
    res = _fst(req.lang, "automorf").lookup(word)
    if not res:
        return {"lang": req.lang, "word": word, "ok": False, "morphemes": [], "_source": SOURCE}
    raw = res[0][0]
    p = _parse(raw)
    lemma, tags = p["lemma"], p["tags"]
    pos = tags[0] if tags else ""
    gen = _fst(req.lang, "autogen")
    sound_changes = []
    method = "fallback"
    if pos == "n":
        aligned = _segment_align(gen, lemma, tags, word)
        if aligned:
            morphs, sound_changes = aligned
            method = "nw-align"
        else:
            morphs = _segment_noun(gen, lemma, tags)
            if not _reconstructs(morphs, word):
                morphs = _fallback_split(gen, lemma, tags, word, "n")
            else:
                method = "cumulative"
            sound_changes = _sound_changes(lemma, morphs[0]["surface"]) if morphs else []
    elif pos == "v":
        morphs = _segment_verb(gen, lemma, tags, word)
        if not _reconstructs(morphs, word):
            morphs = _fallback_split(gen, lemma, tags, word, "v")
        else:
            method = "verb"
    else:
        morphs = [{"surface": word, "tag": pos.upper() or "?", "feat": pos or "", "type": "kök"}]
    return {"lang": req.lang, "word": word, "raw": raw, "lemma": lemma, "tags": tags,
            "pos": pos, "ok": pos in ("n", "v"), "morphemes": morphs,
            "sound_changes": sound_changes, "method": method, "_source": SOURCE}


@app.get("/paradigm/{lang}/{lemma}")
def paradigm(lang: str, lemma: str, pos: str = "n"):
    """Çekim paradigması: İSİM (hâl × sayı) + FİİL (zaman × kişi) — üretilebilen hücreler.
    Lemma hem isim hem fiil olabilir; her ikisinin tablosu da döner (UI sekmelerle gösterir)."""
    if lang not in LANGS:
        raise HTTPException(400, f"desteklenmeyen dil: {lang}")
    gen = _fst(lang, "autogen")
    rows = []
    for case in CASES:
        cell = {"case": case, "case_tr": CASE_TR.get(case, case)}
        for num in ("sg", "pl"):
            q = f"{lemma}<n>" + ("<pl>" if num == "pl" else "") + f"<{case}>"
            res = gen.lookup(q)
            cell[num] = res[0][0] if res else None
            cell[num + "_query"] = q
        if cell.get("sg") or cell.get("pl"):
            rows.append(cell)
    verb_blocks = _build_verb(gen, lemma)
    return {"lang": lang, "lemma": lemma, "pos": pos, "rows": rows,
            "noun": {"rows": rows}, "verb": {"tenses": verb_blocks},
            "has_noun": bool(rows), "has_verb": bool(verb_blocks), "_source": SOURCE}
