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
CASE_TR = {"nom": "Yalın", "gen": "İlgi", "dat": "Yönelme", "acc": "Belirtme",
           "loc": "Bulunma", "abl": "Ayrılma", "ins": "Araç"}

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


app = FastAPI(title="KÖKEN Morfoloji API", version="0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class AnalyzeReq(BaseModel):
    lang: str
    word: str


class GenerateReq(BaseModel):
    lang: str
    query: str          # ör. "хӗр<n><pl><dat>"


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


@app.post("/generate")
def generate(req: GenerateReq):
    if req.lang not in LANGS:
        raise HTTPException(400, f"desteklenmeyen dil: {req.lang}")
    fst = _fst(req.lang, "autogen")
    res = fst.lookup(req.query.strip())
    return {"lang": req.lang, "query": req.query,
            "forms": [{"surface": r[0], "weight": r[1]} for r in res], "_source": SOURCE}


@app.get("/paradigm/{lang}/{lemma}")
def paradigm(lang: str, lemma: str, pos: str = "n"):
    """İsim çekim paradigması: hâl × sayı (apertium autogen ile; üretilemeyenler atlanır)."""
    if lang not in LANGS:
        raise HTTPException(400, f"desteklenmeyen dil: {lang}")
    gen = _fst(lang, "autogen")
    rows = []
    for case in CASES:
        cell = {"case": case, "case_tr": CASE_TR.get(case, case)}
        for num in ("sg", "pl"):
            q = f"{lemma}<{pos}>" + ("<pl>" if num == "pl" else "") + f"<{case}>"
            res = gen.lookup(q)
            cell[num] = res[0][0] if res else None
            cell[num + "_query"] = q
        if cell.get("sg") or cell.get("pl"):
            rows.append(cell)
    return {"lang": lang, "lemma": lemma, "pos": pos, "rows": rows, "_source": SOURCE}
