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
    # İlk 10 (MVP) + 10 yeni = 20 dil (turkicnlp catalog'da apertium morph backend'i olan TÜM Türk dilleri).
    "tur": ("Türkçe", "Latn"), "aze": ("Azerbaycanca", "Latn"), "kaz": ("Kazakça", "Cyrl"),
    "kir": ("Kırgızca", "Cyrl"), "uzb": ("Özbekçe", "Latn"), "uig": ("Uygurca", "Arab"),
    "tat": ("Tatarca", "Cyrl"), "bak": ("Başkurtça", "Cyrl"), "chv": ("Çuvaşça", "Cyrl"),
    "sah": ("Sahaca (Yakut)", "Cyrl"),
    "tuk": ("Türkmence", "Latn"), "crh": ("Kırım Tatarcası", "Latn"), "gag": ("Gagavuzca", "Latn"),
    "kaa": ("Karakalpakça", "Latn"), "alt": ("Altayca", "Cyrl"), "kjh": ("Hakasça", "Cyrl"),
    "krc": ("Karaçay-Balkarca", "Cyrl"), "kum": ("Kumukça", "Cyrl"), "nog": ("Nogayca", "Cyrl"),
    "tyv": ("Tuvaca", "Cyrl"),
}
LANGS = list(LANG_INFO)

# apertium FST olgunluk seviyesi (turkicnlp catalog.json'dan; dürüst kalite göstergesi — UI'da rozet).
QUALITY = {
    "tur": "production", "kaz": "production", "tat": "production",
    "aze": "stable", "kir": "stable", "uzb": "stable",
    "bak": "beta", "chv": "beta", "crh": "beta", "tuk": "beta", "uig": "beta",
    "alt": "prototype", "gag": "prototype", "kaa": "prototype", "kjh": "prototype",
    "krc": "prototype", "kum": "prototype", "nog": "prototype", "sah": "prototype", "tyv": "prototype",
}

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
          "px1sg": "iyelik (benim)", "px2sg": "iyelik (senin)", "px3sp": "iyelik (onun)",
          # genişletme (UI humanizer ile hizalı; segment feat'i hiçbir dilde ham kalmasın)
          "px1pl": "iyelik (bizim)", "px2pl": "iyelik (sizin)", "px3pl": "iyelik (onların)",
          "px3sg": "iyelik (onun)", "prog": "şimdiki/süren", "npst": "geniş/şimdiki", "opt": "istek",
          "qst": "soru eki", "neg": "olumsuzluk", "pass": "edilgen", "caus": "ettirgen", "refl": "dönüşlü",
          "recip": "işteş", "coop": "işteş", "equ": "eşitlik", "dist": "üleştirme", "n": "ad", "v": "fiil",
          "adj": "sıfat", "adv": "zarf", "num": "sayı", "ord": "sıra sayısı", "prn": "zamir",
          "dem": "işaret", "itg": "soru", "qnt": "nicelik", "np": "özel ad", "top": "yer adı",
          "ant": "kişi adı", "cog": "soyadı", "mod_ass": "kesinlik kipi", "cnjcoo": "bağlaç",
          "subst": "adlaşmış", "ger": "isim-fiil", "ger_past": "geçmiş isim-fiili", "ger_fut": "gelecek isim-fiili",
          "ger_aor": "geniş isim-fiili", "ger_impf": "süren isim-fiili", "ger_perf": "bitmiş isim-fiili",
          "ger_pabs": "geçmiş isim-fiili", "ger_ppot": "olasılık isim-fiili", "gpr": "ortaç",
          "gpr_past": "geçmiş ortaç", "gpr_fut": "gelecek ortaç", "gpr_aor": "geniş ortaç",
          "gpr_impf": "süren ortaç", "gpr_perf": "bitmiş ortaç", "gpr_pot": "olasılık ortacı",
          "gpr_ppot": "olasılık ortacı", "gpr_rsub": "ilgi ortacı", "prc_perf": "bitmiş sıfat-fiil",
          "prc_impf": "süren sıfat-fiil", "prc_past": "geçmiş sıfat-fiil", "prc_fut": "gelecek sıfat-fiil",
          "prc_aor": "geniş sıfat-fiil", "prc_cond": "şart ortacı", "prc_irre": "gerçeküstü sıfat-fiil",
          "gna_cond": "şart ulacı", "gna_impf": "süren ulaç", "err_orth": "yazım/standart-dışı",
          "par": "kısmî", "phrase": "öbek", "advl": "zarf", "inf": "mastar"}

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


# --- DİLLER-ARASI: apertium iki-dilli sözlükler (.dix) → çapraz-dil kök grafiği (deepsearch kararı) ---
# Boru hattı: kaynak dilde analiz (lemma+etiket) → .dix ile kök eşle → hedefte AYNI etiketlerle ÜRET.
# Doğrudan çift yoksa diller-grafiğinde pivot (tur→tat→bak). chv/sah/uig pair yok → o hedefler atlanır.
DIX_DIR = os.path.expanduser("~/koken_api/dix")
DIX = {}        # (srcL, tgtL) -> {src_lemma: tgt_lemma}
DIX_ADJ = {}    # langL -> {komşu diller}


def _load_dix():
    if DIX:
        return
    for path in glob.glob(DIX_DIR + "/*.dix"):
        base = os.path.basename(path)[:-4]
        if "-" not in base:
            continue
        a, b = base.split("-", 1)
        try:
            text = open(path, encoding="utf-8").read()
        except Exception:
            continue
        fwd, bwd = {}, {}
        for m in re.finditer(r"<e\b[^>]*>(.*?)</e>", text, re.S):
            e = m.group(1)
            lm = re.search(r"<l\b[^>]*>(.*?)</l>", e, re.S)
            rm = re.search(r"<r\b[^>]*>(.*?)</r>", e, re.S)
            if not lm or not rm:
                continue
            ls = re.sub(r"<[^>]+>", "", lm.group(1)).strip()
            rs = re.sub(r"<[^>]+>", "", rm.group(1)).strip()
            if not ls or not rs or " " in ls or " " in rs:
                continue
            fwd.setdefault(ls, rs)
            bwd.setdefault(rs, ls)
        DIX[(a, b)] = fwd
        DIX[(b, a)] = bwd
        DIX_ADJ.setdefault(a, set()).add(b)
        DIX_ADJ.setdefault(b, set()).add(a)


# FİİL TAM etiket normalizasyonu (deepsearch 5c: apertium FST'leri arası TAM envanteri farklı).
# Hedef dile göre riskli zaman/kip etiketlerini o dilde sentetik üretimi GARANTİ ikameye düşürür.
# (chv/sah geçmiş=<past>; chv geniş=<pres>; kaz/kir şimdiki analitik → <aor> fallback; ulaç→part.)
TAG_NORM = {
    "chv": {"ifi": "past", "aor": "pres", "ger_past": "part_past", "ger_pres": "part_pres", "gpr_past": "part_past"},
    "sah": {"ifi": "past", "ger_past": "part_past", "ger_pres": "part_pres", "gpr_past": "part_past"},
    "kaz": {"pres": "aor"},
    "kir": {"pres": "aor"},
}


def _norm_tags(tags, tgt):
    m = TAG_NORM.get(tgt)
    return tags if not m else [m.get(t, t) for t in tags]


# crosslang: SONLU fiil okumasını ortaç/isimleştirmeye TERCİH ET. apertium analiz sırası ortacı
# önce verebilir (ör. "okuduk" -> [ger_past,nom] ... [ifi,p1,pl] en sonda); finite okuma seçilmezse
# diller-arası üretim yanlış biçim (вуланӑ ortaç) verir. Sonlu = kişi + zaman, ortaç/isim değil.
_FINITE_TENSE = {"ifi", "past", "pres", "fut", "aor", "cond", "imp"}
_NONFINITE = {"ger", "ger_past", "ger_perf", "ger_pres", "gpr_past", "gpr_pot", "gpr",
              "prc_perf", "prc_impf", "subst", "attr", "inf"}


def _verb_rank(tags):
    """0 = sonlu fiil (kişi+zaman, ortaç/kopula değil) → en çok yeğlenir; 2 = diğer (isim/ortaç)."""
    if not tags or tags[0] != "v":
        return 2
    person = any(t in ("p1", "p2", "p3") for t in tags)
    tense = any(t in _FINITE_TENSE for t in tags)
    nonfin = any(t in _NONFINITE for t in tags)
    cop = "cop" in tags
    if person and tense and not nonfin and not cop:
        return 0
    if tense and not nonfin and not cop:
        return 1
    return 2


def _map_lemma(src, tgt, lemma):
    """src dilindeki lemma'yı tgt diline .dix grafiğinde (BFS pivot) eşle; yoksa None."""
    if src == tgt:
        return lemma
    from collections import deque
    seen = {src}
    q = deque([(src, lemma)])
    while q:
        L, lem = q.popleft()
        for nb in DIX_ADJ.get(L, ()):
            tl = DIX.get((L, nb), {}).get(lem)
            if tl is None:
                continue
            if nb == tgt:
                return tl
            if nb not in seen:
                seen.add(nb)
                q.append((nb, tl))
    return None


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


def _noun_tag_feat(tglist):
    """Bir (gerekirse KAYNAŞIK) ek için tip + okunur işlev etiketi."""
    parts = []
    has_case = has_px = has_pl = False
    for t in tglist:
        if t == "pl":
            parts.append("çokluk"); has_pl = True
        elif t.startswith("px"):
            parts.append(TAG_TR.get(t, t)); has_px = True
        elif t in CASE_SET:
            parts.append(CASE_TR.get(t, t) + " hâli"); has_case = True
        else:
            parts.append(TAG_TR.get(t, t))
    typ = "hâl" if has_case else ("iyelik" if has_px else ("çokluk" if has_pl else "hâl"))
    return typ, " · ".join(parts)


# Faz 1.1 — TEMİZ SINIR füzyon-bölme için bilinen ÇOĞUL allomorfları (uzun→kısa eşleştir).
# Yalnız Çuvaşça: oblik çoğul (-сен/-сан) hâl ekinden ÖNCE gelir ve nom-çoğuldan (-сем/-сам) farklıdır;
# bu yüzden kümülatif zincir tutmaz → kaynaşık çıkar. Diğer dillerde pl+hâl zinciri zaten tutuyor (bölme gereksiz).
PLURAL_ALLO = {"chv": ("сен", "сан", "сем", "сам")}


def _plural_allomorph(aff, lang):
    """Yüzey ekinin başındaki bilinen çoğul allomorfunu döndürür (yoksa None)."""
    for a in PLURAL_ALLO.get(lang, ()):
        if aff.startswith(a) and len(a) < len(aff):
            return a
    return None


def _segment_align(gen, lemma, tags, word, lang=""):
    """İSİM: kümülatif üretim (nom-sonlu ara biçimler) + NW hizalama → gerçek yüzey ekleri + ses olayları.
    Üretim eksik/yeniden üretmiyorsa None → çağıran fallback'e düşer."""
    if not tags or tags[0] != "n":
        return None
    has_pl = "pl" in tags
    px = next((t for t in tags if t.startswith("px")), None)
    case = next((t for t in tags if t in CASE_SET), "nom")
    # MORFOTAKTİK SIRA (deepsearch 5c): Çuvaşça Kök+İYELİK+ÇOĞUL (px<pl); diğerleri Kök+ÇOĞUL+İYELİK (pl<px).
    # apertium-chv yalnız <px><pl> üretir; <pl><px> = boş → eski sıra chv'de hizalamayı bozuyordu.
    if lang == "chv":
        slots = ([(px, f"<{px}>")] if px else []) + ([("pl", "<pl>")] if has_pl else [])
    else:
        slots = ([("pl", "<pl>")] if has_pl else []) + ([(px, f"<{px}>")] if px else [])
    levels = [("kök", f"{lemma}<n><nom>")]
    acc = ""
    for label, tg in slots:
        acc += tg
        levels.append((label, f"{lemma}<n>{acc}<nom>"))
    if case != "nom":
        levels.append((case, f"{lemma}<n>{acc}<{case}>"))
    surfaces = []
    for _lab, q in levels:
        s = _gen1(gen, q)
        if s is None:
            return None
        surfaces.append(s)
    if surfaces[-1] != word:
        return None
    # her seviye için: (etiket listesi, kümülatif gerçek yüzey, eklenen yüzey eki) — ardışık NW hizalama
    steps = [([levels[i][0]], surfaces[i], _trailing_affix(surfaces[i - 1], surfaces[i]))
             for i in range(1, len(levels))]
    # ek zinciri kelimenin GERÇEK bir son-eki mi? Çuvaşça gibi KAYNAŞIK iyelik+hâl'de nom-ara-biçim
    # sahte olur (ҫурчӗ ≠ ҫуртне ön-eki) → zincir tutmaz. O zaman: kök + TEK kaynaşık ek (etiketler birleşik).
    joined = "".join(a for _, _, a in steps)
    if not (joined and word.endswith(joined)):
        all_tags = [lv[0] for lv in levels[1:]]
        aff = _trailing_affix(surfaces[0], word)
        # Faz 1.1b — vokal-sonu gövdede İYELİK eki son ünlüyü değiştirip yutulabilir (кӗнеке→кӗнеки,
        # iyelik -и). _trailing_affix bunu yakın-eşleşme sanıp BOŞ ek döndürür → iyelik kaybolur.
        # Ek YOK ama tüm etiketler iyelik(px) ise: sapma-kuyruğunu (_suffix) ek olarak geri al
        # (kök yüzeyde ünlü düşmesi rozetiyle gösterilir). YALNIZ saf-iyelik durumu (hâl/çoğul yok).
        if not aff and all_tags and all(str(t).startswith("px") for t in all_tags):
            aff = _suffix(surfaces[0], word)
        steps = [(all_tags, word, aff)] if aff else []
        # Faz 1.1 — TEMİZ SINIR füzyon-bölme: yalnız [pl, <tek hâl>] (px YOK) ve yüzey ek bilinen
        # çoğul allomorfuyla başlıyorsa çoğul|hâl sınırından böl (ör. chv сенче→сен+че, сене→сен+е).
        # px+hâl portmanteau'ya DOKUNMA (iyelikli hâl Çuvaşçada tek yüzeyde gerçek-kaynaşıktır).
        if aff and "pl" in all_tags and not any(str(t).startswith("px") for t in all_tags):
            cs = [t for t in all_tags if t in CASE_SET and t != "nom"]
            allo = _plural_allomorph(aff, lang)
            if len(cs) == 1 and allo:
                rsp = word[:len(word) - len(aff)]
                steps = [(["pl"], rsp + allo, allo), (cs, word, aff[len(allo):])]
    total = sum(len(a) for _, _, a in steps)
    root_surface = word[:len(word) - total] if 0 < total <= len(word) else surfaces[0]
    # Büyük kutuda SÖZLÜK kökü (lemma); yüzeydeki ses-değişmiş gövde yalnız SES OLAYI rozetinde.
    morphs = [{"surface": lemma, "tag": "KÖK", "feat": "kök", "type": "kök"}]
    forms = [surfaces[0]]  # katman ağacı için kümülatif GERÇEK yüzey
    for tglist, surf, aff in steps:
        if not aff:
            continue
        typ, feat = _noun_tag_feat(tglist)
        morphs.append({"surface": aff, "tag": "+".join(t.upper() for t in tglist), "feat": feat, "type": typ})
        forms.append(surf)
    return morphs, _sound_changes(lemma, root_surface), forms


V_TENSE_TAGS = {"pres", "past", "ifi", "fut", "aor", "cond", "imp", "prc_perf", "prc_impf",
                "ger", "ger_past", "ger_perf", "gpr_past", "gpr_pot"}


_VERB_PERS = {"cop", "p1", "p2", "p3"}  # bu etiketten İTİBAREN kişi/kopula bloğu başlar


def _segment_verb_align(gen, lemma, tags, word):
    """FİİL: kök + ZAMAN eki + KİŞİ/kopula eki (kümülatif, 3 katman). geldiler→gel+di+ler,
    geliyorum→gel+iyor+um. Türk dilleri eklemelidir: zaman ile kişi AYRILABİLİR → dürüst incelik.
    Yöntem: yalın gövde (s0) + ZAMAN gövdesi (s1=lemma<v><tr><tense>[<p3><sg>]) üret; kelimeyi
    s0|s1 sınırlarından böl → zaman eki = s1-s0, kişi eki = kelime-s1. Kopula-zamanlarında da
    çalışır çünkü s1 (geliyor) ÜRETİLİR ve kalan (um) kelimeden kesilir (üretim gerektirmez).
    3-katman tutmazsa kök + kaynaşık ek (2 katman) FALLBACK (portmanteau dürüstlüğü). Üretim
    yoksa None → çağıran genel fallback'e düşer."""
    if not tags or tags[0] != "v":
        return None
    trans = "tv" if "tv" in tags else ("iv" if "iv" in tags else "")
    if not trans:
        return None
    base = f"{lemma}<v><{trans}>"
    stem = _gen1(gen, f"{base}<imp><p2><sg>") or lemma  # yalın gövde (gel)
    if _nw_score(stem, word[:len(stem) + 2]) < len(stem):
        return None
    feats = [t for t in tags if t not in ("v", "tv", "iv")]

    # ── 3-KATMAN deneme: feats'i ZAMAN | KİŞİ olarak böl (ilk {cop,p1,p2,p3} öncesi = zaman) ──
    ci = next((i for i, t in enumerate(feats) if t in _VERB_PERS), len(feats))
    tense_tags, pers_tags = feats[:ci], feats[ci:]
    if tense_tags and pers_tags:
        tq = "".join(f"<{t}>" for t in tense_tags)
        tform = None
        for suff in ("", "<p3><sg>", "<p3><pl>"):  # zaman gövdesi (kişisiz/asgari kişi)
            tform = _gen1(gen, base + tq + suff)
            if tform:
                break
        if tform and len(tform) > len(stem):
            t_aff = _trailing_affix(stem, tform)       # di / iyor
            p_aff = _trailing_affix(tform, word)       # ler / um
            if t_aff and p_aff and word.endswith(p_aff) and word[:len(word) - len(p_aff)].endswith(t_aff):
                feat_t = " · ".join(TAG_TR.get(t, t) for t in tense_tags) or "zaman"
                feat_p = " · ".join(TAG_TR.get(t, t) for t in pers_tags) or "kişi"
                morphs = [
                    {"surface": lemma, "tag": "KÖK", "feat": "fiil kökü", "type": "kök"},
                    {"surface": t_aff, "tag": "+".join(t.upper() for t in tense_tags), "feat": feat_t, "type": "zaman"},
                    {"surface": p_aff, "tag": "+".join(t.upper() for t in pers_tags) or "KİŞİ", "feat": feat_p, "type": "kişi"},
                ]
                surface_stem = word[:len(word) - len(t_aff) - len(p_aff)]
                forms = [stem, word[:len(word) - len(p_aff)], word]
                return morphs, _sound_changes(lemma, surface_stem), forms

    # ── FALLBACK: kök + TEK kaynaşık ek (zaman+kişi portmanteau ya da 3-katman tutmadı) ──
    aff = _trailing_affix(stem, word)
    if not aff or not word.endswith(aff):
        return None
    morphs = [{"surface": lemma, "tag": "KÖK", "feat": "fiil kökü", "type": "kök"},
              {"surface": aff, "tag": "+".join(t.upper() for t in feats) or "EK",
               "feat": " · ".join(TAG_TR.get(t, t) for t in feats) or "çekim", "type": "zaman"}]
    surface_stem = word[:len(word) - len(aff)]  # ses olayı: gövdenin kelimedeki yüzey hâli (git→gid)
    forms = [stem, word]
    return morphs, _sound_changes(lemma, surface_stem), forms


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
        out.append({"code": c, "name": name, "script": script, "quality": QUALITY.get(c, "?"),
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


@app.post("/crosslang")
def crosslang(req: AnalyzeReq):
    """Aranan kelimeyi diğer Türk dillerinde CANLI üretir (statik 'okuduk' gibi): kaynakta analiz →
    .dix ile kök eşle → hedefte AYNI etiketlerle üret. İsimlerde güçlü; etiketi tutmayan hedef atlanır.
    chv/sah/uig için .dix yok → o hedefler dönmez (dürüst kapsam)."""
    if req.lang not in LANGS:
        raise HTTPException(400, f"desteklenmeyen dil: {req.lang}")
    _load_dix()
    word = req.word.strip()
    res = _fst(req.lang, "automorf").lookup(word)
    if not res:
        return {"lang": req.lang, "word": word, "results": [], "_source": SOURCE}
    # eşlenebilir kök tercih et: ilk analizi al, ama .dix'te kökü olan bir analiz varsa onu yeğle
    # tüm analiz adayları (lemma, etiketler) — her hedef için EN İYİ üreteni dene (fiil/dayanıklılık)
    cands = [(p["lemma"], p["tags"]) for p in (_parse(r[0]) for r in res)]
    cands.sort(key=lambda c: _verb_rank(c[1]))  # sonlu fiil okumasını öne al (kararlı; isimler korunur)
    disp = next((c for c in cands
                 if any(c[0] in DIX.get((req.lang, nb), {}) for nb in DIX_ADJ.get(req.lang, ()))), cands[0])
    results = [{"lang": req.lang, "lemma": disp[0], "surface": word, "self": True}]
    for tgt in LANGS:
        if tgt == req.lang:
            continue
        surf = used = None
        for lemma, tags in cands:
            # .dix eşlemesi; yoksa KÖK-FALLBACK: kökü hedefte AYNEN dene (aynı/kognat kök, çoğu
            # zaman aynı yazı sistemindeki diller — hedef FST üretirse kök doğrulanmış olur, uydurma yok).
            tl = _map_lemma(req.lang, tgt, lemma) or lemma
            # önce ham etiket, tutmazsa TAM-normalize edilmiş etiketle dene (fiil taşınabilirliği)
            g = _gen1(_fst(tgt, "autogen"), tl + "".join(f"<{t}>" for t in tags))
            if not g:
                nt = _norm_tags(tags, tgt)
                if nt != tags:
                    g = _gen1(_fst(tgt, "autogen"), tl + "".join(f"<{t}>" for t in nt))
            if g:
                surf, used = g, tl
                break
        if surf:
            results.append({"lang": tgt, "lemma": used, "surface": surf})
    return {"lang": req.lang, "word": word, "lemma": disp[0], "tags": disp[1],
            "results": results, "count": len(results), "_source": SOURCE}


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
    gen = _fst(req.lang, "autogen")
    # TÜM analizleri dene; ALIGN EDEN İSİM analizini tercih et — analyses[0] çoğu zaman yanlış POS
    # (isim yerine fiil) verir; bu seçim kanat/жолдың/оҕо gibi yanlış fiil okumalarını eler.
    chosen = None
    for r in res:
        rp = _parse(r[0])
        if rp["tags"] and rp["tags"][0] == "n":
            aligned = _segment_align(gen, rp["lemma"], rp["tags"], word, req.lang)
            if aligned:
                morphs, sc, forms = aligned
                chosen = (r[0], rp["lemma"], rp["tags"], morphs, sc, "nw-align", forms)
                break
    if chosen is None:
        # align eden isim yoksa: align eden FİİL (kök + kaynaşık çekim eki, NW-align + ses olayı).
        # SONLU fiil okumasını ortaç/isimleştirmeye tercih et (okuduk -> ifi,p1,pl; ger_past değil).
        for r in sorted(res, key=lambda x: _verb_rank(_parse(x[0])["tags"])):
            rp = _parse(r[0])
            if rp["tags"] and rp["tags"][0] == "v":
                va = _segment_verb_align(gen, rp["lemma"], rp["tags"], word)
                if va:
                    morphs, sc, forms = va
                    chosen = (r[0], rp["lemma"], rp["tags"], morphs, sc, "verb-align", forms)
                    break
    if chosen is None:
        # align eden isim/fiil yok → ilk analiz + mevcut mantık (cumulative / fiil / fallback)
        p = _parse(res[0][0])
        lemma, tags = p["lemma"], p["tags"]
        pos = tags[0] if tags else ""
        sc, method = [], "fallback"
        if pos == "n":
            morphs = _segment_noun(gen, lemma, tags)
            if not _reconstructs(morphs, word):
                morphs = _fallback_split(gen, lemma, tags, word, "n")
            else:
                method = "cumulative"
            sc = _sound_changes(lemma, morphs[0]["surface"]) if morphs else []
        elif pos == "v":
            morphs = _segment_verb(gen, lemma, tags, word)
            if not _reconstructs(morphs, word):
                morphs = _fallback_split(gen, lemma, tags, word, "v")
            else:
                method = "verb"
        else:
            morphs = [{"surface": word, "tag": pos.upper() or "?", "feat": pos or "", "type": "kök"}]
        chosen = (res[0][0], lemma, tags, morphs, sc, method, None)
    raw, lemma, tags, morphs, sound_changes, method, forms = chosen
    pos = tags[0] if tags else ""
    return {"lang": req.lang, "word": word, "raw": raw, "lemma": lemma, "tags": tags,
            "pos": pos, "ok": pos in ("n", "v"), "morphemes": morphs, "forms": forms,
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
