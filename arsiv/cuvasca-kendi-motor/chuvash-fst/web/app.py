# -*- coding: utf-8 -*-
"""
ChuvashFST — Web/REST API (Flask)

Motoru (chuvash_fst) JSON API olarak sunar ve tek-sayfa öğrenme arayüzünü servis eder.
Çalıştırma:  python web/app.py   ->  http://localhost:5000
"""
import os
import sys
import random

# paketi import edilebilir kıl
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from flask import Flask, request, jsonify, render_template  # noqa: E402

from chuvash_fst import (  # noqa: E402
    Lexicon, NounGenerator, VerbGenerator, Analyzer, normalize,
)
from chuvash_fst import morphotactics as M  # noqa: E402

DATA = os.path.join(os.path.dirname(_HERE), "data", "chuvash_lexicon_seed.txt")

app = Flask(__name__)
LEX = Lexicon().load(DATA)
NG = NounGenerator(LEX)
VG = VerbGenerator(LEX)
AZ = Analyzer(LEX)


# ---- sayfa ----
@app.route("/")
def index():
    return render_template("index.html", lexicon_count=LEX.count)


# ---- API ----
@app.route("/api/health")
def health():
    return jsonify(status="ok", lexicon_count=LEX.count)


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    word = (request.json or {}).get("word", "")
    res = AZ.analyze(word)
    return jsonify(
        word=res.word,
        success=res.success,
        parses=[dict(stem=p.stem, pos=p.pos, analysis=p.analysis,
                     breakdown=p.breakdown, gloss=p.gloss_ru) for p in res.parses],
    )


@app.route("/api/generate/noun", methods=["POST"])
def api_gen_noun():
    d = request.json or {}
    r = NG.generate(normalize(d.get("stem", "")),
                    possessive=d.get("possessive"),
                    plural=bool(d.get("plural", False)),
                    case=d.get("case", "nom"))
    return jsonify(word=r.word, breakdown=r.breakdown, analysis=r.analysis, valid=r.valid)


@app.route("/api/generate/verb", methods=["POST"])
def api_gen_verb():
    d = request.json or {}
    r = VG.generate(normalize(d.get("stem", "")),
                    tense=d.get("tense", "pres"),
                    person=d.get("person"),
                    neg=bool(d.get("neg", False)))
    return jsonify(word=r.word, breakdown=r.breakdown, analysis=r.analysis, valid=r.valid)


@app.route("/api/paradigm/noun")
def api_paradigm_noun():
    stem = normalize(request.args.get("stem", ""))
    return jsonify(stem=stem, table=NG.full_table(stem))


@app.route("/api/paradigm/verb")
def api_paradigm_verb():
    stem = normalize(request.args.get("stem", ""))
    return jsonify(stem=stem, table=VG.conjugation_table(stem))


@app.route("/api/spellcheck", methods=["POST"])
def api_spellcheck():
    word = normalize((request.json or {}).get("word", ""))
    return jsonify(word=word, correct=AZ.is_valid(word))


@app.route("/api/lexicon/<word>")
def api_lexicon(word):
    entries = LEX.lookup(word)
    return jsonify(word=normalize(word), found=bool(entries),
                   entries=[dict(lemma=e.lemma, pos=e.pos, gloss=e.gloss_ru,
                                 flags=list(e.flags)) for e in entries])


@app.route("/api/exercise")
def api_exercise():
    """ICALL boşluk-doldurma: doğru form + 3 FST-üretimli çeldirici (distractor)."""
    nouns = [e for e in LEX.nouns() if 2 <= len(e.lemma) <= 9 and "ё" not in e.lemma]
    e = random.choice(nouns)
    target = random.choice([c for c in M.CASES if c != "nom"])
    correct = NG.generate(e.lemma, case=target).word
    # çeldiriciler: farklı hallerden yanlış ama yapısal formlar
    distractors = set()
    for c in M.CASES:
        if c == target:
            continue
        w = NG.generate(e.lemma, case=c).word
        if w and w != correct:
            distractors.add(w)
    opts = [correct] + random.sample(sorted(distractors), min(3, len(distractors)))
    random.shuffle(opts)
    return jsonify(
        prompt=f"'{e.lemma}' kelimesinin {M.CASE_NAMES_TR[target]} hâli?",
        stem=e.lemma, gloss=e.gloss_ru, case=target,
        answer=correct, options=opts,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
