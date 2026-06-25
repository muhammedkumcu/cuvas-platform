#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KÖKEN UI build — kullanıcının export ettiği tasarıma GERÇEK, kaynaklı veriyi enjekte eder.

Girdi : platform/ui/Morfoloji Platformu.dc.html  (DesignCanvas export'u — TEK DOĞRULUK)
        platform/data/*.json                       (kaynaklı veri ürünleri)
Çıktı : platform/ui/dist/index.html  (+ support.js kopyası) — çalıştırılabilir, gerçek-veri sürümü

İLKE: kullanıcı tasarımı tekrar export edince bu betiği tekrar çalıştır → gerçek-veri sürümü yeniden üretilir.
Bu adım: LANGPROFILE canlılık alanlarını Glottolog AES (CC BY 4.0) ile değiştirir (Dil Profilleri + Canlılık),
profil modülünün "⚠ örnek" rozetini kaldırır, ve canlı API tabanını (KOKEN_API) ekler.
Sonraki adımlar: Analiz/Paradigma → canlı API; Kognat/Harita/Uzaklık → ilgili JSON.
"""
import json, re, shutil
from pathlib import Path

UI = Path(__file__).resolve().parent
SRC = UI / "Morfoloji Platformu.dc.html"
DATA = UI.parent / "data"
DIST = UI / "dist"; DIST.mkdir(exist_ok=True)

# UI kodu -> profiles.json iso
CODE2ISO = {"tr":"tur","az":"azj","tk":"tuk","kk":"kaz","kg":"kir","tt":"tat","bak":"bak",
            "ug":"uig","chv":"chv","sah":"sah","tyv":"tyv","kjh":"kjh","shor":"cjs","clw":"klj"}
# AES seviyesi -> UI vit (0-6 görsel canlılık çubuğu) + Türkçe etiket
AES_VIT = {1: 6, 2: 4, 3: 3, 4: 2, 5: 1, 6: 0}
AES_TR = {"not endangered": "güvende", "threatened": "tehdit altında", "shifting": "değişen",
          "moribund": "ölmekte", "nearly extinct": "kritik", "extinct": "ölü"}
API = "http://127.0.0.1:8000"

# Harita: Glottolog enlem/boylam -> UI şematik harita yüzdesi (Türkçe & Yakut çapalarıyla doğrusal fit)
MAP_ISOS = ["tur", "azj", "tuk", "chv", "tat", "bak", "kaz", "kir", "uig", "sah", "tyv", "kjh", "klj", "cjs"]
TR_NAME = {"tur": "Türkçe", "azj": "Azerbaycanca", "tuk": "Türkmence", "chv": "Çuvaşça", "tat": "Tatarca",
           "bak": "Başkurtça", "kaz": "Kazakça", "kir": "Kırgızca", "uig": "Uygurca", "sah": "Yakutça",
           "tyv": "Tuvaca", "kjh": "Hakasça", "klj": "Halaçça", "cjs": "Şorca"}
# iso → UI profil kodu (harita düğümünden profile gitmek için)
ISO_TO_PROFILE = {"tur": "tr", "azj": "az", "tuk": "tk", "chv": "chv", "tat": "tt", "bak": "bak", "kaz": "kk",
                  "kir": "kg", "uig": "ug", "sah": "sah", "tyv": "tyv", "kjh": "kjh", "klj": "clw", "cjs": "shor"}
# Harita düğümüne tıklanınca açılan inline kart için kısa bilgi (profil koduna göre): (konuşur, ayırt edici not)
MAP_CARD = {
    "tr": ("~85 milyon", "Batı Oğuz; en çok konuşulan Türk dili."),
    "az": ("~24 milyon", "Merkez Oğuz; ayırt edici açık ə sesi."),
    "tk": ("~7 milyon", "Doğu Oğuz; Ana Türkçe uzun ünlülerini korur."),
    "chv": ("~740 bin", "Yaşayan TEK Oğur dili; rotasizm *z>r, lambdasizm *š>l."),
    "tt": ("~5 milyon", "İdil-Ural Kıpçakçası; tarihsel ünlü kayması (söz→süz)."),
    "bak": ("~1,2 milyon", "Peltek /θ/(ҫ), /ð/(ҙ) ve söz başı /h/ sesleri."),
    "kk": ("~14 milyon", "Katı ünlü uyumu; 12 çoğul eki varyantı."),
    "kg": ("~5 milyon", "Katı dudak uyumu; Manas destanı dili."),
    "ug": ("~10 milyon", "Karluk; Arap yazısı tüm ünlüleri gösterir."),
    "sah": ("~450 bin", "Kuzey Sibirya; genitif/lokatif hâllerini yitirdi."),
    "tyv": ("~280 bin", "Gırtlaksı (kargyraa) ünlüler; höömey geleneği."),
    "kjh": ("~40 bin", "Islıklı sibilantlar (ş→s); 10 gramatik hâl."),
    "clw": ("~20 bin", "Argu kolu; söz başı *h-'yi korur — arkaik 'müze'."),
    "shor": ("~2,8 bin", "Ciddi tehlikede; Yenisey (Mrassu/Kondoma) lehçeleri."),
}


# Uzaklık Gezgini: UI dil kodu -> veri anahtarları
DIST_LEX = {"chv": "Chuvash", "tt": "Tatar", "bak": "Bashkir", "kk": "Kazakh", "kg": "Kirghiz",
            "tr": "Turkish", "az": "Azeri", "tk": "Turkmen", "ug": "Uighur", "sah": "Yakut"}
DIST_ISO = {"chv": "chv", "tt": "tat", "bak": "bak", "kk": "kaz", "kg": "kir",
            "tr": "tur", "az": "azj", "tk": "tuk", "ug": "uig", "sah": "sah"}


def haversine(a, b):
    from math import radians, sin, cos, asin, sqrt
    la1, lo1, la2, lo2 = map(radians, [a[0], a[1], b[0], b[1]])
    h = sin((la2 - la1) / 2) ** 2 + cos(la1) * cos(la2) * sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * asin(sqrt(h))


def build_distance(prof, lex, typ, cog, intel):
    codes = list(DIST_LEX)
    coords = {c: (prof[DIST_ISO[c]]["lat"], prof[DIST_ISO[c]]["lon"]) for c in codes
              if prof.get(DIST_ISO[c]) and prof[DIST_ISO[c]].get("lat") is not None}
    # coğrafi: haversine, en büyük çiftle normalize
    geo_km = {a: {} for a in coords}
    mx = 1.0
    for a in coords:
        for b in coords:
            d = haversine(coords[a], coords[b]); geo_km[a][b] = d; mx = max(mx, d)
    # filogenetik: Savelyev kognat-seti karakterleri üzerinden Jaccard (Bayes ağacının GİRDİSİ; yenilikleri cezalandırır)
    lang_sets = {}
    for c in cog["concepts"]:
        for s in c["sets"]:
            for m in s["members"]:
                lang_sets.setdefault(m["lang"], set()).add(s["cognateset_id"])
    leks, tipo, geo, filo, anla = {}, {}, {}, {}, {}
    for a in codes:
        leks[a], tipo[a], geo[a], filo[a], anla[a] = {}, {}, {}, {}, {}
        sa = lang_sets.get(DIST_LEX[a], set())
        for b in codes:
            lv = lex.get(DIST_LEX[a], {}).get(DIST_LEX[b], {})
            tv = typ.get(DIST_ISO[a], {}).get(DIST_ISO[b], {})
            if lv.get("distance") is not None: leks[a][b] = lv["distance"]
            if tv.get("distance") is not None: tipo[a][b] = tv["distance"]
            if a in geo_km and b in geo_km[a]: geo[a][b] = round(geo_km[a][b] / mx, 3)
            sb = lang_sets.get(DIST_LEX[b], set())
            if sa and sb:
                filo[a][b] = round(1 - len(sa & sb) / len(sa | sb), 4)
            if a == b:
                anla[a][b] = 0.0
            else:
                pct = intel.get(a, {}).get(b)
                if pct is None: pct = intel.get(b, {}).get(a)
                if pct is not None: anla[a][b] = round(1 - pct / 100, 3)
    return {"leks": leks, "tipo": tipo, "geo": geo, "filo": filo, "anla": anla}


# Kognat Ağı: gösterilecek diller (Savelyev ID, UI adı, kol) + kavramlar (Concepticon → Türkçe, anahtar)
COG_DISP = [("Chuvash", "Çuvaşça", "Ogur"), ("Turkish", "Türkçe", "Oğuz"), ("Azeri", "Azerbaycanca", "Oğuz"),
            ("Tatar", "Tatarca", "Kıpçak"), ("Kazakh", "Kazakça", "Kıpçak"), ("Uighur", "Uygurca", "Karluk"),
            ("Yakut", "Yakutça", "Sibirya")]
COG_CONC = {"EYE": ("göz", "goz"), "WATER": ("su", "su"), "YEAR": ("yıl", "yil"), "STONE": ("taş", "tas"),
            "FOREST": ("orman", "orman"), "FIVE": ("beş", "bes"), "NAME": ("ad", "ad"), "TONGUE": ("dil", "dil"),
            "HEAD": ("baş", "bas"), "BLOOD": ("kan", "kan"), "BONE": ("kemik", "kemik"), "TWO": ("iki", "iki"),
            "ARM OR HAND": ("el / kol", "el"), "DAY (NOT NIGHT)": ("gün", "gun")}

# A1 — Kognat kelime-seçici için anlamsal kategoriler (Leipzig-Jakarta/Swadesh alanları;
# yatay ölçekte deepsearch 18 kategorileriyle aynı taksonomi genişletilecek). Kavram→kategori.
COG_CAT = {"EYE": "Vücut", "TONGUE": "Vücut", "HEAD": "Vücut", "BLOOD": "Vücut",
           "BONE": "Vücut", "ARM OR HAND": "Vücut",
           "WATER": "Doğa", "STONE": "Doğa", "FOREST": "Doğa",
           "YEAR": "Zaman", "DAY (NOT NIGHT)": "Zaman",
           "FIVE": "Sayılar", "TWO": "Sayılar",
           "NAME": "Soyut"}


# C — kognat düğüm sözcükleri okunur karşılaştırmalı yazıma çevrilir (Savelyev IPA-vari → sade Latin).
# Bunlar YEREL ortografi DEĞİL; kaynak yerel-script vermiyor → dürüst etiket: "karşılaştırmalı biçim".
COG_READABLE = {"ḳ": "q", "χ": "h", "ɣ": "ğ", "γ": "ğ", "ŋ": "ñ", "ə": "ä", "ɘ": "ĕ",
                "ɯ": "ı", "ɨ": "ı", "ʒ": "j", "ɕ": "ś", "ʃ": "ş", "ʷ": "", "ụ": "u", "ỹ": "y"}


def readable(s):
    return "".join(COG_READABLE.get(ch, ch) for ch in str(s))


def build_cognates(cog):
    from collections import Counter
    disp_ids = {d[0] for d in COG_DISP}
    by_gloss = {c["gloss"]: c for c in cog["concepts"]}
    out, first = {}, None
    for gloss, (tr, key) in COG_CONC.items():
        c = by_gloss.get(gloss)
        if not c:
            continue
        langset = {}
        for s in c["sets"]:
            for m in s["members"]:
                if m["lang"] in disp_ids and m["lang"] not in langset:
                    langset[m["lang"]] = (s["cognateset_id"], s["root"], m["value"])
        if len(langset) < 3:
            continue
        dom = Counter(v[0] for v in langset.values()).most_common(1)[0][0]
        dom_root = next(v[1] for v in langset.values() if v[0] == dom)
        nodes = [{"lang": name, "word": readable(langset[sid][2]), "branch": branch, "shift": langset[sid][0] != dom}
                 for sid, name, branch in COG_DISP if sid in langset]
        gaps = [n["lang"] for n in nodes if n["shift"]]
        # (b) bu kognat hangi ses-denkliği kuralını örnekler? Proto-fonem + Çuvaşça çıktı doğrulaması (güvenli).
        # SOUND sırası: 0=rotasizm 1=lambdasizm 2=baş y->ś 3=ünlü indirgeme.
        chvw = next((n["word"] for n in nodes if n["lang"] == "Çuvaşça"), "")
        turw = next((n["word"] for n in nodes if n["lang"] == "Türkçe"), "")
        rule_idx = None
        if "ŕ" in (dom_root or "") and "r" in chvw:
            rule_idx = 0
        elif "ĺ" in (dom_root or "") and "l" in chvw:
            rule_idx = 1
        elif chvw and chvw[0] in "śşsҫ" and turw and turw[0] in "yj":
            rule_idx = 2
        note = f"Proto-Türkçe kök {dom_root}. Aynı renk = aynı kognat seti; farklı düğüm = kognat boşluğu" + \
               (f" ({', '.join(gaps)})." if gaps else ".") + " Biçimler okunur karşılaştırmalı yazımdadır."
        out[key] = {"gloss": tr, "proto": dom_root, "note": note, "nodes": nodes, "ruleIdx": rule_idx,
                    "cat": COG_CAT.get(gloss, "Diğer")}
        if first is None:
            first = key
    return out, first


# (b) Ses denklikleri KANIT-DESTEKLİ: yerleşik kurallar (Türkoloji olgusu) + Savelyev kognat verisinden
# PROTO-FONEM tabanlı kanıt sayısı. Proto *ŕ = rotasizm, *ĺ = lambdasizm (akademik-tanımlayıcı işaret).
def sound_evidence(cog):
    res = {"rot": [0, []], "lam": [0, []], "y": [0, []]}
    for c in cog["concepts"]:
        for s in c["sets"]:
            root = s.get("root") or ""
            forms = {m["lang"]: m["value"] for m in s["members"]}
            cv, tr = forms.get("Chuvash"), forms.get("Turkish")
            pair = (readable(cv), readable(tr)) if (cv and tr) else None
            if "ŕ" in root:
                res["rot"][0] += 1
                if pair and "r" in pair[0]:
                    res["rot"][1].append(pair)
            if "ĺ" in root:
                res["lam"][0] += 1
                if pair:
                    res["lam"][1].append(pair)
            if cv and tr and cv[0] in "śšsʂ" and tr[0] in "yj":
                res["y"][0] += 1
                res["y"][1].append((readable(cv), readable(tr)))
    return res


def project(lon, lat):
    x = max(4, min(95, round(0.7517 * lon - 14.71, 1)))
    y = max(6, min(91, round(-1.6949 * lat + 118.58, 1)))
    return x, y


def build_map(prof):
    rows = []
    for iso in MAP_ISOS:
        p = prof.get(iso)
        if not p or p.get("lat") is None or p.get("lon") is None:
            continue
        x, y = project(p["lon"], p["lat"])
        code = ISO_TO_PROFILE.get(iso, "")
        sp, note = MAP_CARD.get(code, ("", ""))
        parts = [f"name:'{TR_NAME.get(iso, p['name'])}'", f"code:'{code}'",
                 f"branch:'{p['branch']}'", f"x:{x}", f"y:{y}",
                 f"speakers:{json.dumps(sp, ensure_ascii=False)}", f"note:{json.dumps(note, ensure_ascii=False)}"]
        if iso == "chv":
            parts.append("hi:true")
        # A4b — düğüm yoğunluğu: çakışan komşuların etiketini YUKARI al (alternatif yön → üst üste binmez).
        # tat (Çuvaşça d=1.6) · cjs Şor + tyv Tuvaca (Hakasça'yla d=2.3–3.9 Sibirya üçlüsü).
        FORCE_ABOVE = {"tat", "cjs", "tyv"}
        if y > 50 or iso in FORCE_ABOVE:
            parts.append("below:true")
        rows.append("    {" + ", ".join(parts) + "},")
    return "MAP = [\n" + "\n".join(rows) + "\n  ];"


# A4a — harita arka planı DOTLARLA AYNI projeksiyonda (viewBox 0..100); iç denizler gerçek
# lat/lon'dan project() ile yerleştirilir → arka plan artık veriyle hizalı (eski SVG ayrı 1000×560
# koord sistemindeydi = "saçma"). Ölçek: 1° boylam ≈ 0.7517 x-birim, 1° enlem ≈ 1.6949 y-birim.
def build_map_bg():
    p = project
    # iç denizler/göller: (boylam_merkez, enlem_merkez, boylam_açıklık°, enlem_açıklık°)
    seas = [(34.5, 43.2, 13.0, 4.6),   # Karadeniz
            (50.5, 41.7, 7.0, 10.6),   # Hazar (dikey)
            (59.5, 45.0, 3.2, 2.8),    # Aral
            (76.0, 45.7, 6.6, 1.4),    # Balkaş
            (107.0, 53.6, 2.2, 4.4)]   # Baykal
    sea_svg = []
    for lon, lat, ws, hs in seas:
        cx, cy = p(lon, lat)
        rx, ry = round(ws / 2 * 0.7517, 2), round(hs / 2 * 1.6949, 2)
        sea_svg.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#mSea)" '
                       f'stroke="#a6bdbf" stroke-width="0.8" vector-effect="non-scaling-stroke"/>')
    grat = []
    for lon in (40, 60, 80, 100, 120):
        x, _ = p(lon, 45)
        grat.append(f'<line x1="{x}" y1="0" x2="{x}" y2="100"/>')
    for lat in (30, 40, 50, 60):
        _, y = p(70, lat)
        grat.append(f'<line x1="0" y1="{y}" x2="100" y2="{y}"/>')
    # Akdeniz/güneybatı yumuşak köşe (Anadolu'nun güneyi) — coğrafi olarak gerçek su kenarı
    med = ('<path d="M 0 57 Q 6 60 10 68 Q 8 84 4 100 L 0 100 Z" fill="url(#mSea)" opacity="0.92"/>')
    return ('<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">'
            '<defs>'
            '<linearGradient id="mLand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ece5d5"></stop><stop offset="1" stop-color="#e3dbc8"></stop></linearGradient>'
            '<linearGradient id="mSea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cdd9da"></stop><stop offset="1" stop-color="#bccbcc"></stop></linearGradient>'
            '</defs>'
            '<rect x="0" y="0" width="100" height="100" fill="url(#mLand)"></rect>'
            + med
            + '<g stroke="rgba(33,29,23,.08)" stroke-width="0.6" vector-effect="non-scaling-stroke">' + "".join(grat) + '</g>'
            + "".join(sea_svg)
            + '</svg>')


def main():
    html = SRC.read_text(encoding="utf-8")
    prof = {p["iso"]: p for p in json.load(open(DATA / "profiles.json", encoding="utf-8"))["profiles"]}
    lex = json.load(open(DATA / "distance.lexical.json", encoding="utf-8"))["matrix"]
    typ = json.load(open(DATA / "distance.typological.json", encoding="utf-8"))["matrix"]
    cog = json.load(open(DATA / "cognates.json", encoding="utf-8"))
    extra = json.load(open(DATA / "lang_extra.json", encoding="utf-8"))["languages"]
    intel = json.load(open(DATA / "intelligibility.json", encoding="utf-8"))["intel"]

    # A3 — landing/footer kapsam sayıları VERİDEN (hardcode değil; veri büyüdükçe rebuild ile güncellenir)
    LIVE_FST = ["chv", "tur", "aze", "kaz", "kir", "uzb", "uig", "tat", "bak", "sah"]  # canlı FST (LIVE_LN ile eş)
    n_live = len(LIVE_FST)                                    # 10 — canlı morfolojik analiz
    n_prof = len(prof)                                        # 23 — derin profil
    n_geo = len(lex)                                          # 32 — karşılaştırmalı atlas (Savelyev)
    n_branch = len({p.get("branch") for p in prof.values()})  # 6 — Türk dil kolu

    changed = []
    for code, iso in CODE2ISO.items():
        p = prof.get(iso)
        aes = p and p.get("vitality_aes")
        if not aes:
            continue
        vit = AES_VIT.get(aes["level"], 3)
        m = re.search(r"EGIDS:\s*([^;]+)", aes.get("crosswalk") or "")
        egids_code = (m.group(1).strip() if m else str(aes["level"]))
        egids = f"{egids_code} · {AES_TR.get(aes['label'], aes['label'])}"
        # ilgili LANGPROFILE satırında egids ve vit alanlarını değiştir (kaynak: Glottolog AES)
        html, n1 = re.subn(rf"(\{{code:'{code}',[^\n]*?egids:')[^']*'", rf"\g<1>{egids}'", html)
        html, n2 = re.subn(rf"(\{{code:'{code}',[^\n]*?vit:)\d+", rf"\g<1>{vit}", html)
        if n1 or n2:
            changed.append(f"{code}/{iso}: egids='{egids}' vit={vit}")

    # Dil profili serbest-metin zenginleştirmesi ← lang_extra.json (Wikipedia, çapraz-kontrollü)
    nenrich = 0
    for code, e in extra.items():
        for field in ("speakers", "script", "note"):
            if field in e:
                pat = re.compile(r"(\{code:'" + re.escape(code) + r"',[^\n]*?" + field + r":)'[^']*'")
                html, n = pat.subn(lambda m, v=e[field]: m.group(1) + json.dumps(v, ensure_ascii=False), html, count=1)
                nenrich += n
    # Derin dil profilleri (deepsearch 9.1–9.5) → DEEPPROF; profil ekranında bölümlü gösterilir
    deep = json.load(open(DATA / "profiles_deep.json", encoding="utf-8"))["deep"]
    # + Seslendirme (TTS/ASR) bölümü (deepsearch 6) — her dile 5. bölüm olarak eklenir
    tts = json.load(open(DATA / "profiles_tts.json", encoding="utf-8"))["tts"]
    for code, body in tts.items():
        if code in deep:
            deep[code].append({"label": "Seslendirme (TTS/ASR)", "body": body})
    html = html.replace("  LANGPROFILE = [",
                        "  DEEPPROF = " + json.dumps(deep, ensure_ascii=False) + ";\n  LANGPROFILE = [", 1)
    html = html.replace(
        "profileSel:{...sel, vc:this.vitColor(sel.vit), branchColor:this.BRANCHCOLOR[sel.branch]||'#5f574b'},",
        "profileSel:{...sel, deep:(this.DEEPPROF&&this.DEEPPROF[sel.code])||[], vc:this.vitColor(sel.vit), branchColor:this.BRANCHCOLOR[sel.branch]||'#5f574b'},", 1)
    # Derin bölümler ARTIK iki-sütun gridin ALTINDA, TAM GENİŞLİKTE (sağ özet kutusu küçük/dengeli kalsın).
    # 2 sütunlu kart ızgarası → "Tarih"ten itibaren genişçe okunur (kullanıcı UI tutarlılık notu).
    deep_markup = (
        '\n        <div style="margin-top:22px;display:grid;grid-template-columns:repeat(2,1fr);gap:16px;align-items:start">\n'
        '          <sc-for list="{{ profileSel.deep }}" as="d" hint-placeholder-count="5">\n'
        '            <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:14px;padding:18px 22px">\n'
        "              <div style=\"font-size:11px;font-family:'IBM Plex Mono',monospace;letter-spacing:.5px;color:#b86a2e\">{{ d.label }}</div>\n"
        '              <p style="font-size:14px;line-height:1.65;color:#3f3a32;margin:8px 0 0">{{ d.body }}</p>\n'
        '            </div>\n'
        '          </sc-for>\n'
        '        </div>')
    # özet kartının notu + sağ kart kapanışı + iki-sütun grid kapanışı → deep bloğunu grid'in HEMEN ALTINA koy
    note_block = ('<p style="font-size:15px;line-height:1.7;color:#3f3a32;margin:22px 0 0">{{ profileSel.note }}</p>\n'
                  '          </div>\n'
                  '        </div>')
    ndeep = 1 if note_block in html else 0
    html = html.replace(note_block, note_block + deep_markup, 1)
    print(f"  Derin profiller (ds9): {len(deep)} dil, tam-genislik markup={ndeep}")

    # Wikipedia kaynağını kütüğe ekle + profil modülünün kaynaklarını güncelle (demo çıktı, wiki girdi)
    html = html.replace(
        "glottolog:{label:'Glottolog', detail:'soy ağacı / sınıflandırma', lic:'CC BY 4.0', kind:'veri', url:'glottolog.org'},",
        "glottolog:{label:'Glottolog', detail:'soy ağacı / sınıflandırma / AES canlılık', lic:'CC BY 4.0', kind:'veri', url:'glottolog.org'},\n    wiki:{label:'Wikipedia', detail:'dil profili serbest-metni (çapraz-kontrollü)', lic:'CC BY-SA 4.0', kind:'veri', url:'wikipedia.org'},")
    html = html.replace("{mod:'Dil Profilleri', srcs:['ethnologue','joshi','glottolog','demo']}",
                        "{mod:'Dil Profilleri', srcs:['glottolog','wiki','joshi']}")
    # Uzaklık 5/5 eksen artık kaynaklı: Lindsay'i kütüğe ekle, demo'yu çıkar
    html = html.replace(
        "wals:   {label:'WALS', detail:'tipolojik özellikler (uzaklık ekseni)', lic:'CC BY 4.0', kind:'veri', url:'wals.info'},",
        "wals:   {label:'WALS', detail:'tipolojik özellikler (uzaklık ekseni)', lic:'CC BY 4.0', kind:'veri', url:'wals.info'},\n    lindsay:{label:'Lindsay — anlaşılabilirlik', detail:'deneysel/yaklaşık karşılıklı anlaşılabilirlik', lic:'akademik', kind:'literatür', url:'tehlikedekidiller.com'},")
    html = html.replace("{mod:'Uzaklık Gezgini', srcs:['cldf','wals','glottolog','demo']}",
                        "{mod:'Uzaklık Gezgini', srcs:['cldf','wals','glottolog','lindsay']}")

    # ── Faz 2.7 — KAYNAKLAR güncelleme: deepsearch-türevli kaynakları kütüğe ekle + modüllere bağla ──
    html = html.replace(
        "    joshi:  {label:'Joshi ve ark. 2020', detail:'dijital kaynak sınıfları (0–5)', lic:'akademik', kind:'literatür', url:'aclanthology.org'},",
        "    joshi:  {label:'Joshi ve ark. 2020', detail:'dijital kaynak sınıfları (0–5)', lic:'akademik', kind:'literatür', url:'aclanthology.org'},\n"
        "    bayes:  {label:'Savelyev & Robbeets 2020', detail:'Bayes filogenetik — soy ağacı & zaman derinliği; Johanson altı kol tasnifi', lic:'akademik', kind:'literatür', url:'academic.oup.com/jole'},\n"
        "    hf:     {label:'HuggingFace ekosistemi', detail:'açık model/veri kartları (LLM · encoder · ASR/TTS · benchmark)', lic:'model bazında', kind:'veri', url:'huggingface.co'},\n"
        "    deepds: {label:'KÖKEN derin araştırmalar', detail:'çapraz-kontrollü derleme (profiller · seslendirme · ekosistem · sınıflandırma)', lic:'derleme', kind:'sentez', url:'arastirma/'},")
    # USAGE: yeni içerik katmanlarını ilgili modüllere bağla
    html = html.replace("{mod:'Dil Profilleri', srcs:['glottolog','wiki','joshi']}",
                        "{mod:'Dil Profilleri', srcs:['glottolog','wiki','joshi','hf','deepds']}")
    html = html.replace("{mod:'Tarih & Köken', srcs:['kasgari','yunusbayev','glottolog']}",
                        "{mod:'Tarih & Köken', srcs:['kasgari','glottolog','bayes','cldf','yunusbayev']}")
    # NOT: hf/deepds → Ekosistem sayfasına bağlanır (USAGE 'Ekosistem' satırı eco bloğunda eklenir); Araştırmacı sade kalır.
    print("  Faz 2.7 KAYNAKLAR: +bayes +hf +deepds; USAGE Profiller/Tarih güncellendi")

    # canlı API tabanı + paylaşılan canlı-analiz yardımcıları (tek dil + tüm diller ortak)
    if "KOKEN_API" not in html:
        helper = (
            "class Component extends DCLogic {\n"
            "  KOKEN_API = '%s';\n"
            "  LIVE_LN = {chv:'Çuvaşça',tur:'Türkçe',aze:'Azerice',kaz:'Kazakça',kir:'Kırgızca',uzb:'Özbekçe',uig:'Uygurca',tat:'Tatarca',bak:'Başkurtça',sah:'Yakutça'};\n"
            "  apiWordFrom(lg, word, analyses){\n"
            "    const TT = {n:'kök',v:'kök',pl:'çokluk',nom:'hâl',gen:'hâl',dat:'hâl',acc:'hâl',loc:'hâl',abl:'hâl',ins:'hâl',px1sg:'iyelik',px2sg:'iyelik',px3sp:'iyelik',pres:'zaman',past:'zaman',fut:'zaman',p1:'kişi',p2:'kişi',p3:'kişi'};\n"
            "    const a = (analyses && analyses[0]) || null;\n"
            "    const ms = a ? [{text:a.lemma, tag:'KÖK', type:'kök', label:'kök (apertium FST)', gloss:a.lemma, gItem:a.lemma, note:'Apertium morfolojik çözümlemesi.'}]\n"
            "        .concat((a.tags||[]).map(t=>({text:t, tag:String(t).toUpperCase(), type:(TT[t]||'kök'), label:'etiket: '+t, gloss:t, gItem:t, note:'Apertium etiketi.'})))\n"
            "      : [{text:word, tag:'?', type:'kök', label:'çözümlenemedi', gloss:'?', gItem:word, note:'Apertium bu biçimi tanımadı.'}];\n"
            "    return {lang:'cv', langName:(this.LIVE_LN[lg]||lg)+' · canlı FST', surface:word, translit:'', gloss:(a?('apertium: '+a.raw):'çözümlenemedi'), morphemes:ms, cognates:[]};\n"
            "  }"
        ) % API
        html = html.replace("class Component extends DCLogic {", helper, 1)

    # Harita ← gerçek Glottolog koordinatları (şematik projeksiyon)
    new_map = build_map(prof)
    html, nmap = re.subn(r"MAP = \[.*?\n  \];", lambda m: new_map, html, flags=re.DOTALL)
    # Faz 1.3 — Harita düğümü TIKLANINCA INLINE bilgi (sayfadan çıkmaz; kullanıcı kararı), profile gitmez
    html = html.replace("        return { name:m.name, branch:m.branch, col,",
                        "        return { name:m.name, branch:m.branch, col, go:()=>this.setState({mapSel:m.code}),", 1)
    html = html.replace('<div style="{{ n.dotStyle }}">',
                        '<div onClick="{{ n.go }}" style="cursor:pointer;transition:transform .14s ease;{{ n.dotStyle }}" style-hover="z-index:40;transform:translate(-50%,-50%) scale(1.5)">', 1)
    # A4a — arka plan SVG'sini projeksiyon-hizalı yenisiyle değiştir (eski 1000×560 elle-çizim blob = saçma)
    na4 = 0
    html, na4a = re.subn(r'<svg viewBox="0 0 1000 560".*?</svg>', lambda m: build_map_bg(), html, flags=re.DOTALL)
    na4 += na4a
    # konteyner arka planı: deniz mavisi → kara tonu (yeni SVG kara-tabanlı; köşelerde mavi sızmasın)
    if 'aspect-ratio:1000/560;background:#cdd9da;' in html:
        html = html.replace('aspect-ratio:1000/560;background:#cdd9da;', 'aspect-ratio:1000/560;background:#ece5d5;', 1); na4 += 1
    # bölge etiketlerini projeksiyon-doğru konuma taşı (HTML span = SVG stretch'inden etkilenmez)
    for old_pos, new_pos in [("left:7%;top:60%", "left:3.5%;top:63%"), ("left:30%;top:14%", "left:16%;top:12%"),
                             ("left:42%;top:60%", "left:33%;top:62%"), ("left:72%;top:8%", "left:60%;top:6%")]:
        if old_pos in html:
            html = html.replace(old_pos, new_pos, 1); na4 += 1
    # Argu kolu rengini ekle (Halaçça düğümü + lejant)
    html = html.replace("    'Karluk':'oklch(0.5 0.13 295)', 'Sibirya':'oklch(0.52 0.13 235)',",
                        "    'Karluk':'oklch(0.5 0.13 295)', 'Sibirya':'oklch(0.52 0.13 235)', 'Argu':'#8a7a2e',", 1)
    # mapInfo (seçili düğümün inline kartı) — renderVals
    html = html.replace(
        "      mapLegend:Object.entries(this.BRANCHCOLOR).map(([k,v])=>({label:k, hue:v})),",
        "      mapLegend:Object.entries(this.BRANCHCOLOR).map(([k,v])=>({label:k, hue:v})),\n"
        "      mapInfo:(()=>{ const m=this.MAP.find(x=>x.code===S.mapSel); return m?{has:true,name:m.name,branch:m.branch,speakers:m.speakers,note:m.note,col:(this.BRANCHCOLOR[m.branch]||'#5f574b')}:{has:false,name:'',branch:'',speakers:'',note:'',col:'#5f574b'}; })(),", 1)
    # inline kart markup'ı (lejantın hemen altına)
    map_legend_block = (
        '          <div style="display:flex;gap:18px;flex-wrap:wrap;margin-top:14px;padding:0 4px">\n'
        '            <sc-for list="{{ mapLegend }}" as="l" hint-placeholder-count="5">\n'
        '              <span style="display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:#5f574b"><span style="width:11px;height:11px;border-radius:50%;background:{{ l.hue }}"></span>{{ l.label }} kolu</span>\n'
        '            </sc-for>\n'
        '          </div>')
    map_card = (
        '\n          <sc-if value="{{ mapInfo.has }}" hint-placeholder-val="{{ false }}">\n'
        '          <div style="margin-top:14px;background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-left:4px solid {{ mapInfo.col }};border-radius:12px;padding:14px 18px">\n'
        '            <div style="display:flex;align-items:baseline;gap:10px;flex-wrap:wrap">\n'
        "              <span style=\"font-family:'Spectral',serif;font-size:18px;font-weight:700;color:#211d17\">{{ mapInfo.name }}</span>\n"
        "              <span style=\"font-size:11px;color:#fff;background:{{ mapInfo.col }};border-radius:12px;padding:2px 10px;font-family:'IBM Plex Mono',monospace\">{{ mapInfo.branch }} kolu</span>\n"
        "              <span style=\"margin-left:auto;font-size:12px;color:#9a9082;font-family:'IBM Plex Mono',monospace\">{{ mapInfo.speakers }}</span>\n"
        '            </div>\n'
        '            <p style="font-size:13.5px;line-height:1.6;color:#5f574b;margin:8px 0 0">{{ mapInfo.note }}</p>\n'
        '          </div>\n'
        '          </sc-if>')
    nmapcard = 1 if map_legend_block in html else 0
    html = html.replace(map_legend_block, map_legend_block + map_card, 1)
    # intro ipucu
    html = html.replace(
        "Çuvaşça, İdil (Volga) boyunda, Ogur kolunun yaşayan tek temsilcisi olarak ayrı durur.",
        "Çuvaşça, İdil (Volga) boyunda, Ogur kolunun yaşayan tek temsilcisi olarak ayrı durur. Bir dile tıkla — bilgisi aşağıda açılır.", 1)
    print(f"  Harita inline kart (1.3): mapInfo+kart={nmapcard}")
    print(f"  A4a harita arka planı projeksiyon-hizalı (SVG+konteyner+4 bölge etiketi): {na4}/6 yama")

    # Uzaklık Gezgini ← gerçek matrisler: leksikal(Savelyev) + tipolojik(WALS) + coğrafi(koordinat)
    real_dist = build_distance(prof, lex, typ, cog, intel)
    if "REAL_DIST" not in html:
        html = html.replace("  KOKEN_API = '" + API + "';",
                            "  KOKEN_API = '" + API + "';\n  REAL_DIST = " + json.dumps(real_dist) + ";", 1)
    old_val = "    const val = (key)=> Math.abs(base[key]-t[key]);"
    new_val = ("    const RD = this.REAL_DIST || {};\n"
               "    const realv = (m)=>{ const r=(RD[m]||{})[S.distBase]; return (r && r[S.distTarget]!=null) ? r[S.distTarget] : null; };\n"
               "    const val = (key)=>{ const m = {leks:'leks', tipo:'tipo', cogr:'geo', filo:'filo', anla:'anla'}[key]; const rv = m ? realv(m) : null; return rv!=null ? rv : Math.abs(base[key]-t[key]); };")
    ndist = 1 if old_val in html else 0
    html = html.replace(old_val, new_val, 1)

    # Kognat Ağı ← gerçek kognat setleri (SavelyevTurkic)
    cog_obj, cog_default = build_cognates(cog)
    new_cog = "COGNATES = " + json.dumps(cog_obj, ensure_ascii=False) + ";"
    html, ncog = re.subn(r"COGNATES = \{.*?\n  \};", lambda m: new_cog, html, flags=re.DOTALL)
    if cog_default:
        html = html.replace("cognateKey: 'kiz',", f"cognateKey: '{cog_default}', cognateQ: '', cognateCat: 'all',", 1)

    # ---- A1: Kognat kelime-seçici = kategorili + aranabilir (yatay ölçek ön-şartı) ----
    na1 = 0
    # (1) cognateVals filtre + kategori mantığı: düz .map → kategori çipleri + filtrelenmiş .filter().map()
    a1_old = (
        "    const keys = Object.entries(this.COGNATES).map(([k,v])=>{\n"
        "      const sel = k===S.cognateKey;\n"
        "      return { key:k, label:v.gloss, sel, go:()=>this.setState({cognateKey:k}),\n"
        "        style:`cursor:pointer;border:1.5px solid ${sel?'#211d17':'rgba(33,29,23,.14)'};background:${sel?'#211d17':'#fff'};color:${sel?'#f4f1ea':'#211d17'};border-radius:18px;padding:7px 16px;font-size:14px;font-family:'Spectral',serif;font-weight:600` };\n"
        "    });\n")
    a1_new = (
        "    const _cq = (S.cognateQ||'').trim().toLocaleLowerCase('tr'), _ccat = S.cognateCat||'all';\n"
        "    const _norm = (s)=>String(s||'').toLocaleLowerCase('tr');\n"
        "    const _catCount = {}; Object.values(this.COGNATES).forEach(v=>{ const kk=v.cat||'Diğer'; _catCount[kk]=(_catCount[kk]||0)+1; });\n"
        "    const _catList = Object.keys(_catCount).sort((a,b)=>a.localeCompare(b,'tr'));\n"
        "    const _mkCat = (key,label,nn)=>{ const sel=_ccat===key; return { key, label: label+(nn!=null?' · '+nn:''), go:()=>this.setState({cognateCat:key}),\n"
        "      style:`cursor:pointer;border:1px solid ${sel?'#d98b4a':'rgba(33,29,23,.16)'};background:${sel?'#d98b4a':'#fff'};color:${sel?'#211d17':'#5f574b'};border-radius:14px;padding:5px 13px;font-size:12.5px;font-family:'IBM Plex Mono',monospace;font-weight:${sel?600:400}` }; };\n"
        "    const cognateCats = [_mkCat('all','Tümü',Object.keys(this.COGNATES).length)].concat(_catList.map(k=>_mkCat(k,k,_catCount[k])));\n"
        "    const keys = Object.entries(this.COGNATES).filter(([k,v])=>{\n"
        "      if (_ccat!=='all' && (v.cat||'Diğer')!==_ccat) return false;\n"
        "      if (_cq && _norm(v.gloss).indexOf(_cq)<0 && _norm(k).indexOf(_cq)<0) return false;\n"
        "      return true;\n"
        "    }).map(([k,v])=>{\n"
        "      const sel = k===S.cognateKey;\n"
        "      return { key:k, label:v.gloss, sel, go:()=>this.setState({cognateKey:k}),\n"
        "        style:`cursor:pointer;border:1.5px solid ${sel?'#211d17':'rgba(33,29,23,.14)'};background:${sel?'#211d17':'#fff'};color:${sel?'#f4f1ea':'#211d17'};border-radius:18px;padding:7px 16px;font-size:14px;font-family:'Spectral',serif;font-weight:600` };\n"
        "    });\n")
    if a1_old in html:
        html = html.replace(a1_old, a1_new, 1); na1 += 1
    # (2) return'e yeni alanlar: kategori çipleri, arama kutusu state+handler, boş-durum bayrağı
    a1_ret_old = "    return { cognateKeys:keys, cognateGloss:c.gloss, cognateProto:c.proto, cognateNote:c.note, cognateNodes:nodes };"
    a1_ret_new = ("    return { cognateKeys:keys, cognateCats, cognateEmpty:keys.length===0, cognateQ:S.cognateQ||'',\n"
                  "      onCognateInput:(e)=>this.setState({cognateQ:e.target.value}),\n"
                  "      cognateGloss:c.gloss, cognateProto:c.proto, cognateNote:c.note, cognateNodes:nodes };")
    if a1_ret_old in html:
        html = html.replace(a1_ret_old, a1_ret_new, 1); na1 += 1
    # (3) seçici markup: düz buton satırı → arama kutusu + kategori çipleri + filtrelenmiş kavramlar + boş-durum
    a1_mk_old = ('        <div style="display:flex;gap:8px;flex-wrap:wrap">\n'
                 '          <sc-for list="{{ cognateKeys }}" as="k" hint-placeholder-count="3"><button onClick="{{ k.go }}" style="{{ k.style }}">{{ k.label }}</button></sc-for>\n'
                 '        </div>')
    a1_mk_new = (
        '        <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:14px;padding:16px 18px">\n'
        '          <input value="{{ cognateQ }}" onInput="{{ onCognateInput }}" placeholder="Kavram ara — ör. göz, su, sayı…" style="width:100%;max-width:340px;padding:9px 13px;border:1.5px solid rgba(33,29,23,.18);border-radius:10px;background:#fff;font-size:14px;font-family:inherit;color:#211d17;outline:none">\n'
        '          <div style="display:flex;gap:6px;flex-wrap:wrap;margin:12px 0 10px">\n'
        '            <sc-for list="{{ cognateCats }}" as="c"><button onClick="{{ c.go }}" style="{{ c.style }}">{{ c.label }}</button></sc-for>\n'
        '          </div>\n'
        '          <div style="display:flex;gap:8px;flex-wrap:wrap">\n'
        '            <sc-for list="{{ cognateKeys }}" as="k" hint-placeholder-count="3"><button onClick="{{ k.go }}" style="{{ k.style }}">{{ k.label }}</button></sc-for>\n'
        '          </div>\n'
        '          <sc-if value="{{ cognateEmpty }}" hint-placeholder-val="{{ false }}"><div style="font-size:13px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace;padding:6px 2px">Eşleşen kavram yok — aramayı veya kategoriyi değiştir.</div></sc-if>\n'
        '        </div>')
    if a1_mk_old in html:
        html = html.replace(a1_mk_old, a1_mk_new, 1); na1 += 1
    # NOT: A2 (Karşılaştır başlık sekmeye-duyarlı) D-bloğunda compareHeadline tanımında yapılır (tek kaynak).

    # ---- A3: ana sayfa (landing) güncelliği — kapsam sayıları VERİDEN, footer düzelt ----
    na3 = 0
    # (1) kenar çubuğu footer: "5 KOL · 14 DİL" hem stale hem yanlış (gerçek: 6 kol, 32 dil atlas)
    a3_foot_old = "5 KOL · 14 DİL · ÇUVAŞ ÇEKİRDEK · v0.4"
    a3_foot_new = f"{n_branch} KOL · {n_geo} DİL · ÇUVAŞ ÇEKİRDEK · v0.4"
    if a3_foot_old in html:
        html = html.replace(a3_foot_old, a3_foot_new, 1); na3 += 1
    # (2) landing'e KATMANLI KAPSAM şeridi (dürüst: analiz 10 < profil 23 < atlas 32; yatay ölçek ipucu)
    a3_strip = (
        '        <div style="margin-top:30px;display:flex;gap:10px;flex-wrap:wrap">\n'
        + "".join(
            '          <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:12px;padding:11px 16px;display:flex;flex-direction:column;gap:2px">\n'
            f'            <span style="font-family:\'Spectral\',serif;font-size:24px;font-weight:700;color:{col};line-height:1">{num}</span>\n'
            f'            <span style="font-size:11.5px;color:#5f574b;font-family:\'IBM Plex Mono\',monospace;letter-spacing:.3px">{lab}</span>\n'
            '          </div>\n'
            for num, lab, col in [
                (n_live, "dil · canlı FST analizi", "#b8602e"),
                (n_prof, "dil · derin profil", "#2f6fb0"),
                (n_geo, "dil · karşılaştırmalı atlas", "#2f8a5b"),
                (n_branch, "kol · Türk dil ailesi", "#8a6d2e"),
            ])
        + '          <div style="align-self:center;font-size:11.5px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace;max-width:16ch;line-height:1.4">…yatay ölçekte tüm Türk dillerine açılıyor</div>\n'
        + '        </div>\n')
    a3_anchor = '        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:42px">'
    if a3_anchor in html:
        html = html.replace(a3_anchor, a3_strip + a3_anchor, 1); na3 += 1
    # (3) landing kartındaki "yedi dilde" stale-sayısı → ölçek-dayanıklı "diller arasında"
    a3_card_old = "desc:'Aynı anlamı yedi dilde yan yana diz; ç↔ş, z↔r ses denkliklerini ve soy ağacını gör.'"
    a3_card_new = "desc:'Aynı anlamı diller arasında yan yana diz; ç↔ş, z↔r ses denkliklerini ve soy ağacını gör.'"
    if a3_card_old in html:
        html = html.replace(a3_card_old, a3_card_new, 1); na3 += 1

    # ---- A5: Uzaklık Gezgini — ortadaki radar kutusu "çok uzun" (grid stretch). Kompakt + dengele ----
    na5 = 0
    # (1) dış grid: stretch'i kapat (align-items:start) → radar kutusu içerik-boyu; sol sütun ferah (230→248)
    a5_outer_old = '<div style="display:grid;grid-template-columns:230px 1fr;gap:24px;margin-top:26px">'
    a5_outer_new = '<div style="display:grid;grid-template-columns:248px 1fr;gap:30px;margin-top:26px;align-items:start">'
    if a5_outer_old in html:
        html = html.replace(a5_outer_old, a5_outer_new, 1); na5 += 1
    # (2) sağ sütunu flex-col yap (radar|eksen grid + OKUMA); iç grid align-start + gap ferah
    a5_inner_old = '          <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'
    a5_inner_new = ('          <div style="display:flex;flex-direction:column;gap:18px">\n'
                    '            <div style="display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start">')
    if a5_inner_old in html:
        html = html.replace(a5_inner_old, a5_inner_new, 1); na5 += 1
    # (3) OKUMA kutusunu sağ sütuna taşı (radar/eksen altına) → sağdaki boşluğu doldurur, denge kurar
    a5_okuma_old = (
        '          </div>\n'
        '        </div>\n'
        '        <div style="margin-top:20px;background:#211d17;color:#f4f1ea;border-radius:14px;padding:20px 24px;display:flex;gap:14px;align-items:flex-start">\n'
        '          <span style="font-size:20px">◎</span>\n'
        '          <div><div style="font-size:11px;font-family:\'IBM Plex Mono\',monospace;letter-spacing:1px;color:rgba(244,241,234,.5);margin-bottom:6px">OKUMA</div><div style="font-size:14.5px;line-height:1.6">{{ distNarr }}</div></div>\n'
        '        </div>')
    a5_okuma_new = (
        '          </div>\n'
        '          <div style="background:#211d17;color:#f4f1ea;border-radius:14px;padding:18px 22px;display:flex;gap:14px;align-items:flex-start">\n'
        '            <span style="font-size:20px">◎</span>\n'
        '            <div><div style="font-size:11px;font-family:\'IBM Plex Mono\',monospace;letter-spacing:1px;color:rgba(244,241,234,.5);margin-bottom:6px">OKUMA</div><div style="font-size:14.5px;line-height:1.6">{{ distNarr }}</div></div>\n'
        '          </div>\n'
        '          </div>\n'
        '        </div>')
    if a5_okuma_old in html:
        html = html.replace(a5_okuma_old, a5_okuma_new, 1); na5 += 1

    # kopya/metin düzeltmeleri — yalnız NET redundant/teknik ifadeler (tasarımı bozmadan, minimal)
    copy_fix = {
        "14 dil · soldan kenar rengi = canlılık": "Türk dilleri ve canlılık durumları",
        "Kaynak: SavelyevTurkic CLDF · NorthEuraLex — örnek/illüstratif değerler":
            "Kaynak: Savelyev (leksikal+filogenetik) · WALS (tipolojik) · koordinat (coğrafi) · Lindsay (anlaşılabilirlik)",
        "örn. okuduk, ormanda, kızlar": "seçili dilde canlı FST analizi",
    }
    nfix = 0
    for old, new in copy_fix.items():
        if old in html:
            html = html.replace(old, new); nfix += 1

    # --- CANLI API bağlama (Paradigma + Analiz) — VM kapalıysa illüstratife düşer ---
    nlive = 0
    live = []
    # 1) state alanları
    live.append(("    paradigmRoot: 'hĕr',", "    paradigmRoot: 'hĕr',\n    apiParadigm: {}, apiWord: null, searchLang: 'auto', paradigmFree: null, paradigmFreeQ: '', apiAllLangs: {}, apiMatchCodes: [], apiMatchLang: null, researchQ: '', researchApi: null, compareApi: null, compareQ: '', paradigmPos: 'noun', helpOpen: '',"))
    # küratörlü kök seçilince serbest çekimi temizle
    live.append(("        go:()=>this.setState({paradigmRoot:k}),", "        go:()=>this.setState({paradigmRoot:k, paradigmFree:null}),"))
    # paradigmVals return: serbest çekim (herhangi bir kök, seçili dil) + handler'lar
    live.append((
        "    return { paradigmRoots:roots, paradigmIsVerb:isVerb, paradigmIsNoun:!isVerb, paradigmRows:rows,\n"
        "      paradigmTitle:this.disp(p.root, p.rootLat), paradigmGloss:`“${p.gloss}”`,\n"
        "      paradigmSub: isVerb ? (p.label+' · şahıs çekimi') : 'Ad çekimi · hâl × sayı' };",
        "    const F = this.state.paradigmFree;\n"
        "    const cF = (s)=> s ? [{ text:this.disp(s), hue:this.hue('kök'), bg:this.hueBg('kök'), border:this.hueBorder('kök') }] : null;\n"
        "    const hasNounF = !!(F && Array.isArray(F.rows) && F.rows.length);\n"
        "    const hasVerbF = !!(F && Array.isArray(F.verb) && F.verb.length);\n"
        "    const isFree = hasNounF || hasVerbF;\n"
        "    let posF = this.state.paradigmPos || 'noun';\n"
        "    if (isFree){ if(posF==='noun' && !hasNounF && hasVerbF) posF='verb'; if(posF==='verb' && !hasVerbF) posF='noun'; }\n"
        "    const freeRows = (isFree && posF==='noun' && hasNounF) ? F.rows.map(r=>({ caseLabel:r.case_tr, tag:(r.case||'').toUpperCase(), sg:cF(r.sg), pl:cF(r.pl), trSg:'', trPl:'' })) : null;\n"
        "    const verbBlocks = (isFree && posF==='verb' && hasVerbF) ? F.verb.map(b=>({ tense:b.tense, cells:b.cells.map(c=>({ person:c.person, surface:c.surface?this.disp(c.surface):'—' })) })) : null;\n"
        "    const posTabs = isFree ? [['noun','İsim çekimi',hasNounF],['verb','Fiil çekimi',hasVerbF]].filter(t=>t[2]).map(t=>({ label:t[1], go:()=>this.setState({paradigmPos:t[0]}), style:`cursor:pointer;border:none;border-radius:8px;padding:8px 15px;font-size:13px;font-weight:600;font-family:inherit;background:${posF===t[0]?'#211d17':'transparent'};color:${posF===t[0]?'#f4f1ea':'#5f574b'}` })) : [];\n"
        "    const LNp = {chv:'Çuvaşça',tur:'Türkçe',aze:'Azerice',kaz:'Kazakça',kir:'Kırgızca',uzb:'Özbekçe',uig:'Uygurca',tat:'Tatarca',bak:'Başkurtça',sah:'Yakutça'};\n"
        "    return { paradigmRoots:roots, paradigmIsVerb:isVerb && !isFree, paradigmIsNoun: isFree ? (posF==='noun') : !isVerb, paradigmIsVerbView: isFree && posF==='verb', paradigmRows: freeRows||rows, paradigmVerbBlocks: verbBlocks||[], paradigmPosTabs: posTabs, paradigmHasPosTabs: posTabs.length>1,\n"
        "      paradigmTitle: isFree ? this.disp(F.lemma) : this.disp(p.root, p.rootLat),\n"
        "      paradigmGloss: isFree ? ('· '+F.langName) : `“${p.gloss}”`,\n"
        "      paradigmSub: isFree ? ('canlı apertium çekimi · '+F.langName) : (isVerb ? (p.label+' · şahıs çekimi') : 'Ad çekimi · hâl × sayı'),\n"
        "      paradigmFreeQ: this.state.paradigmFreeQ||'',\n"
        "      onParadigmFreeInput:(e)=>this.setState({paradigmFreeQ:e.target.value}),\n"
        "      onParadigmFreeKey:(e)=>{ if(e.key!=='Enter') return; const lemma=(this.state.paradigmFreeQ||'').trim(); if(!lemma) return; const lg=this.state.searchLang||'chv'; fetch(this.KOKEN_API+'/paradigm/'+lg+'/'+encodeURIComponent(lemma)).then(r=>r.json()).then(d=>this.setState({paradigmFree:{lemma, langName:(LNp[lg]||lg), rows:(d&&d.rows)||[]}})).catch(()=>{}); } };"))
    # paradigma: serbest kök girişi ÜSTTE (arama düşük kalmasın) + örnekler ÖRNEK olarak etiketli
    live.append((
        '        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:18px">\n          <sc-for list="{{ paradigmRoots }}"',
        '        <div style="display:flex;align-items:center;gap:10px;margin-top:18px;flex-wrap:wrap">\n'
        '          <input value="{{ paradigmFreeQ }}" onInput="{{ onParadigmFreeInput }}" onKeyDown="{{ onParadigmFreeKey }}" placeholder="Bir kök yaz + Enter — sağ üstteki dilde canlı çekim" style="flex:1;min-width:300px;max-width:520px;padding:12px 15px;border:1.5px solid rgba(33,29,23,.18);border-radius:10px;background:#fff;font-size:15px;font-family:inherit;color:#211d17;outline:none">\n'
        '        </div>\n'
        '        <div style="font-size:11px;letter-spacing:1px;color:#9a9082;margin-top:18px;font-family:monospace">ÖRNEK KÖKLER (farklı dillerden)</div>\n'
        '        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">\n          <sc-for list="{{ paradigmExamples }}"'))
    # 2) componentDidUpdate → ekrana girince paradigma çek
    live.append((
        "  componentDidUpdate(prevProps, prevState){\n"
        "    if (prevState && prevState.screen !== this.state.screen){\n"
        "      try { const el = document.getElementById('content-scroll'); if (el) el.scrollTop = 0; } catch(e){}\n"
        "    }\n"
        "  }",
        "  componentDidUpdate(prevProps, prevState){\n"
        "    if (prevState && prevState.screen !== this.state.screen){\n"
        "      try { const el = document.getElementById('content-scroll'); if (el) el.scrollTop = 0; } catch(e){}\n"
        "    }\n"
        "    if (this.state.screen==='paradigm'){\n"
        "      const p = this.PARADIGM[this.state.paradigmRoot]; const root = p && p.root;\n"
        "      if (root && this.state.apiParadigm[root]===undefined){\n"
        "        this.setState(s=>({apiParadigm:{...s.apiParadigm,[root]:null}}));\n"
        "        fetch(this.KOKEN_API+'/paradigm/chv/'+encodeURIComponent(root)).then(r=>r.json())\n"
        "          .then(d=>this.setState(s=>({apiParadigm:{...s.apiParadigm,[root]:(d&&d.rows)||[]}}))).catch(()=>{});\n"
        "      }\n"
        "    }\n"
        "  }"))
    # 3) paradigmVals: API satırları varsa onları kullan
    live.append((
        "    const isVerb = p.kind==='fiil';\n"
        "    const rows = p.rows.map(r=>({ caseLabel:r.case, tag:r.tag, sg:cell(r.sg), pl:r.pl?cell(r.pl):null, trSg:r.trSg, trPl:r.trPl,\n"
        "      fst: r.sg.map(([t,ty],i)=> i===0 ? this.cyr2lat(t) : '+'+r.tag).join('') }));",
        "    const isVerb = p.kind==='fiil';\n"
        "    const apiR = this.state.apiParadigm && this.state.apiParadigm[p.root];\n"
        "    const cellOne = (s)=> s ? [{ text:this.disp(s), hue:this.hue('kök'), bg:this.hueBg('kök'), border:this.hueBorder('kök') }] : null;\n"
        "    const rows = (Array.isArray(apiR) && apiR.length)\n"
        "      ? apiR.map(r=>({ caseLabel:r.case_tr, tag:(r.case||'').toUpperCase(), sg:cellOne(r.sg), pl:cellOne(r.pl), trSg:'', trPl:'', fst:r.sg||'' }))\n"
        "      : p.rows.map(r=>({ caseLabel:r.case, tag:r.tag, sg:cell(r.sg), pl:r.pl?cell(r.pl):null, trSg:r.trSg, trPl:r.trPl,\n"
        "        fst: r.sg.map(([t,ty],i)=> i===0 ? this.cyr2lat(t) : '+'+r.tag).join('') }));"))
    # 4) active(): canlı analiz kelimesi
    live.append((
        "  active(){ return this.WORDS[this.state.activeWordId]; }",
        "  active(){ return this.state.activeWordId==='__api' && this.state.apiWord ? this.state.apiWord : this.WORDS[this.state.activeWordId]; }"))
    # 5) runSearch(): eşleşme yoksa canlı /analyze; "auto" ise /analyze_all (multi-dil) — apiWordFrom ortak
    live.append((
        "  runSearch(){\n"
        "    const q = (this.state.query||'').trim().toLowerCase();\n"
        "    if (!q) return;\n"
        "    for (const id in this.WORDS){ const w = this.WORDS[id];\n"
        "      if ([w.gloss, w.surface, w.translit].some(s=>String(s).toLowerCase().includes(q))){\n"
        "        this.setState({ screen:'analiz', activeWordId:id, selMorphIdx:0, stripCount:0 }); return; } }\n"
        "  }",
        "  runSearch(){\n"
        "    const q = (this.state.query||'').trim().toLowerCase();\n"
        "    if (!q) return;\n"
        "    for (const id in this.WORDS){ const w = this.WORDS[id];\n"
        "      if ([w.gloss, w.surface, w.translit].some(s=>String(s).toLowerCase().includes(q))){\n"
        "        this.setState({ screen:'analiz', activeWordId:id, selMorphIdx:0, stripCount:0 }); return; } }\n"
        "    const word = (this.state.query||'').trim(); const lg = this.state.searchLang||'chv';\n"
        "    if (lg==='auto'){\n"
        "      fetch(this.KOKEN_API+'/analyze_all',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({word})}).then(r=>r.json()).then(d=>{\n"
        "        const langs=d.langs||{}; const codes=Object.keys(langs);\n"
        "        if (!codes.length){ this.setState({ apiWord:this.apiWordFrom('chv', word, null), activeWordId:'__api', apiAllLangs:{}, apiMatchCodes:[], apiMatchLang:null, screen:'analiz', selMorphIdx:0, stripCount:0 }); return; }\n"
        "        const first=codes[0];\n"
        "        this.setState({ apiAllLangs:langs, apiMatchCodes:codes, apiMatchLang:first, apiWord:this.apiWordFrom(first, word, langs[first]), activeWordId:'__api', screen:'analiz', selMorphIdx:0, stripCount:0 });\n"
        "      }).catch(()=>{});\n"
        "      return;\n"
        "    }\n"
        "    fetch(this.KOKEN_API+'/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:lg,word})}).then(r=>r.json()).then(d=>{\n"
        "      this.setState({ apiWord:this.apiWordFrom(lg, word, d.analyses), activeWordId:'__api', apiAllLangs:{}, apiMatchCodes:[], apiMatchLang:null, screen:'analiz', selMorphIdx:0, stripCount:0 });\n"
        "    }).catch(()=>{});\n"
        "  }"))
    # 6) USAGE: paradigma demo'dan çıktı (canlı FST)
    live.append(("    {mod:'Paradigma Gezgini', srcs:['fst','unimorph','demo']},",
                 "    {mod:'Paradigma Gezgini', srcs:['fst','unimorph']},"))
    for old, new in live:
        if old in html:
            html = html.replace(old, new, 1); nlive += 1
        else:
            print("  ! CANLI bağlama eşleşmedi:", old[:48])

    # ============================================================
    #  DİL MODELİ (kullanıcı kararı: Otomatik + manuel; HER EKRANDA giriş YANINDA — üst barda DEĞİL)
    #  Üst bardaki dil seçici kaldırıldı; "Otomatik" varsayılan (emoji yok). Çok-dillilik otomatik/görünmez.
    # ============================================================
    sel_langs = [("chv", "Çuvaşça"), ("tur", "Türkçe"), ("aze", "Azerice"), ("kaz", "Kazakça"),
                 ("kir", "Kırgızca"), ("uzb", "Özbekçe"), ("uig", "Uygurca"), ("tat", "Tatarca"),
                 ("bak", "Başkurtça"), ("sah", "Yakutça")]
    langopts = '<option value="auto">Otomatik (dil algıla)</option>' + \
               "".join(f'<option value="{c}">{n}</option>' for c, n in sel_langs)
    SELBOX = ('<select value="{{ searchLang }}" onInput="{{ onSearchLang }}" title="Çözümleme dili" '
              'style="background:#fff;border:1px solid rgba(33,29,23,.16);border-radius:9px;padding:9px 9px;'
              'font-size:12.5px;font-family:inherit;color:#211d17;cursor:pointer;max-width:170px;flex-shrink:0">'
              + langopts + '</select>')
    INP = ('padding:12px 15px;border:1.5px solid rgba(33,29,23,.18);border-radius:10px;background:#fff;'
           'font-size:15px;font-family:inherit;color:#211d17;outline:none')
    nsel = 0

    # render bağları: searchLang + compare girişi + ekran-duyarlı onSearchLang (dil değişince o ekranı yineler)
    rb_old = "      navGroups, wordChips, screenTag:tag, query:S.query,"
    rb_new = ("      navGroups, wordChips, screenTag:tag, query:S.query, searchLang:S.searchLang, compareQ:S.compareQ||'',\n"
              "      onCompareInput:(e)=>this.setState({compareQ:e.target.value}),\n"
              "      onCompareKey:(e)=>{ if(e.key!=='Enter') return; const w=(this.state.compareQ||'').trim(); if(w) this.runCompare(w, this.state.searchLang); },\n"
              "      onSearchLang:(e)=>{ const v=e.target.value; this.setState({searchLang:v}); const s=this.state.screen; setTimeout(()=>{\n"
              "        if(s==='analiz' && (this.state.query||'').trim()) this.runSearch();\n"
              "        else if(s==='research' && (this.state.researchQ||'').trim()) this.runResearch(v, this.state.researchQ.trim());\n"
              "        else if(s==='paradigm' && (this.state.paradigmFreeQ||'').trim()) this.runParadigm(this.state.paradigmFreeQ.trim());\n"
              "        else if(s==='compare' && (this.state.compareQ||'').trim()) this.runCompare(this.state.compareQ.trim(), this.state.searchLang);\n"
              "      },0); },")
    if rb_old in html:
        html = html.replace(rb_old, rb_new, 1); nsel += 1
    else:
        print("  ! dil render bağı eşleşmedi")

    # Analiz: kendi giriş kutusu + yanında dil seçici — BAŞLIĞIN ALTINDA (paradigma gibi), morfem kartının üstünde
    analiz_old = ('        <!-- morpheme blocks -->\n'
                  '        <div style="margin-top:30px;background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:16px;padding:34px 30px">')
    analiz_new = ('        <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:24px 0 0">\n'
                  '          <input value="{{ query }}" onInput="{{ onQuery }}" onKeyDown="{{ onSearchKey }}" placeholder="Kelime yaz + Enter — canlı morfolojik analiz" style="flex:1;min-width:260px;max-width:480px;' + INP + '">\n'
                  '          ' + SELBOX + '\n'
                  '        </div>\n' + analiz_old)
    if analiz_old in html:
        html = html.replace(analiz_old, analiz_new, 1); nsel += 1
    else:
        print("  ! analiz giriş eşleşmedi")

    # Karşılaştır: kendi giriş kutusu + dil seçici
    cmp_old = "<div style=\"font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:1.5px;color:#d98b4a\">KARŞILAŞTIR</div>"
    cmp_new = (cmp_old + '\n'
               '        <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:14px">\n'
               '          <input value="{{ compareQ }}" onInput="{{ onCompareInput }}" onKeyDown="{{ onCompareKey }}" placeholder="Kelime yaz + Enter — diller arası canlı çözümle" style="flex:1;min-width:260px;max-width:480px;' + INP + '">\n'
               '          ' + SELBOX + '\n'
               '        </div>')
    if cmp_old in html:
        html = html.replace(cmp_old, cmp_new, 1); nsel += 1
    else:
        print("  ! karşılaştır giriş eşleşmedi")

    # Paradigma: giriş kutusunun yanına dil seçici + placeholder (artık üst barda değil)
    par_inp = '<input value="{{ paradigmFreeQ }}" onInput="{{ onParadigmFreeInput }}" onKeyDown="{{ onParadigmFreeKey }}" placeholder="Bir kök yaz + Enter — sağ üstteki dilde canlı çekim" style="flex:1;min-width:300px;max-width:520px;padding:12px 15px;border:1.5px solid rgba(33,29,23,.18);border-radius:10px;background:#fff;font-size:15px;font-family:inherit;color:#211d17;outline:none">'
    par_new = ('<input value="{{ paradigmFreeQ }}" onInput="{{ onParadigmFreeInput }}" onKeyDown="{{ onParadigmFreeKey }}" placeholder="Bir kök yaz + Enter — canlı çekim" style="flex:1;min-width:260px;max-width:440px;' + INP + '">\n          ' + SELBOX)
    if par_inp in html:
        html = html.replace(par_inp, par_new, 1); nsel += 1
    else:
        print("  ! paradigma giriş eşleşmedi")

    # onParadigmFreeKey → runParadigm (auto destekli)
    opk_old = "onParadigmFreeKey:(e)=>{ if(e.key!=='Enter') return; const lemma=(this.state.paradigmFreeQ||'').trim(); if(!lemma) return; const lg=this.state.searchLang||'chv'; fetch(this.KOKEN_API+'/paradigm/'+lg+'/'+encodeURIComponent(lemma)).then(r=>r.json()).then(d=>this.setState({paradigmFree:{lemma, langName:(LNp[lg]||lg), rows:(d&&d.rows)||[]}})).catch(()=>{}); }"
    if opk_old in html:
        html = html.replace(opk_old, "onParadigmFreeKey:(e)=>{ if(e.key!=='Enter') return; const lemma=(this.state.paradigmFreeQ||'').trim(); if(lemma) this.runParadigm(lemma); }", 1); nsel += 1
    else:
        print("  ! onParadigmFreeKey eşleşmedi")

    # methods: runParadigm (auto) + runCompare — runSearch'ten ÖNCE
    m_anchor = "  runSearch(){\n    const q = (this.state.query||'').trim().toLowerCase();\n    if (!q) return;\n    for (const id in this.WORDS){ const w = this.WORDS[id];"
    m_new = (
        "  runParadigm(lemma){\n"
        "    const fp=(l)=>fetch(this.KOKEN_API+'/paradigm/'+l+'/'+encodeURIComponent(lemma)).then(r=>r.json()).then(d=>this.setState({paradigmFree:{lemma, lang:l, langName:(this.LIVE_LN[l]||l), rows:(d.noun&&d.noun.rows)||d.rows||[], verb:(d.verb&&d.verb.tenses)||[]}})).catch(()=>{});\n"
        "    const lg=this.state.searchLang;\n"
        "    if(lg && lg!=='auto'){ fp(lg); }\n"
        "    else { fetch(this.KOKEN_API+'/analyze_all',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({word:lemma})}).then(r=>r.json()).then(d=>{ const c=Object.keys(d.langs||{}); fp(c[0]||'chv'); }).catch(()=>{}); }\n"
        "  }\n"
        "  runCompare(word, srcLang){\n"
        "    const run=(src)=>{\n"
        "      fetch(this.KOKEN_API+'/crosslang',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:src,word})}).then(r=>r.json()).then(d=>{\n"
        "        const results=(d.results&&d.results.length)?d.results:[{lang:src,surface:word,self:true}];\n"
        "        Promise.all(results.map(rr=>fetch(this.KOKEN_API+'/segment',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:rr.lang,word:rr.surface})}).then(r=>r.json()).then(s=>[rr.lang,{surface:rr.surface,lemma:rr.lemma,self:!!rr.self,morphemes:(s&&s.morphemes)||null}]).catch(()=>[rr.lang,{surface:rr.surface,lemma:rr.lemma,self:!!rr.self,morphemes:null}]))).then(pairs=>{\n"
        "          const rows={}; pairs.forEach(p=>{rows[p[0]]=p[1];}); const sr=(rows[src]&&rows[src].morphemes)||[];\n"
        "          const selfM = sr.length ? sr.map((m,i)=>({text:m.surface, tag:m.tag, type:m.type||'kök', label:(i===0?'kök':'ek')+' · '+m.feat, gloss:m.feat, gItem:m.surface, note:''})) : [{text:word, tag:'KÖK', type:'kök', label:'kök', gloss:'', gItem:word, note:''}];\n"
        "          this.setState({ apiWord:{lang:'cv', langName:(this.LIVE_LN[src]||src)+' · canlı', surface:word, translit:'', gloss:'', morphemes:selfM, cognates:[]}, activeWordId:'__api', apiMatchLang:src, compareApi:{word, src, rows}, screen:'compare', compareTab:'rows', selMorphIdx:0, stripCount:0 });\n"
        "        });\n"
        "      }).catch(()=>{});\n"
        "    };\n"
        "    if(srcLang && srcLang!=='auto'){ run(srcLang); return; }\n"
        "    fetch(this.KOKEN_API+'/analyze_all',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({word})}).then(r=>r.json()).then(d=>{ const c=Object.keys(d.langs||{}); run(c[0]||'tur'); }).catch(()=>{});\n"
        "  }\n"
        + m_anchor)
    if m_anchor in html:
        html = html.replace(m_anchor, m_new, 1); nsel += 1
    else:
        print("  ! runParadigm/runCompare anchor eşleşmedi")

    print(f"  Dil modeli (per-ekran giriş+seçici): {nsel}/6 yama")

    # ============================================================
    #  ANALİZ — canlı sonuçta GERÇEK yüzey ekleri (/segment); apertium etiketi değil gerçek ek (ler, de)
    # ============================================================
    seg = []
    seg.append(("applySegment method",
        "  runParadigm(lemma){",
        "  applySegment(lg, word){\n"
        "    if(!lg || lg==='auto' || !word) return;\n"
        "    fetch(this.KOKEN_API+'/segment',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:lg,word})}).then(r=>r.json()).then(d=>{\n"
        "      if(!d || !d.morphemes || !d.morphemes.length) return;\n"
        "      const ms = d.morphemes.map((m,i)=>({ text:m.surface, tag:m.tag, type:m.type||'kök', label:(i===0?'kök':'ek')+' · '+m.feat, gloss:m.feat, gItem:m.surface, note:(i===0?'Apertium çözümlemesinin köküdür.':('Apertium üretiminden çıkarılan yüzey eki — işlevi: '+m.feat+'.')) }));\n"
        "      this.setState(s=>{ if(!s.apiWord || s.apiWord.surface!==word) return {}; return { apiWord: Object.assign({}, s.apiWord, {morphemes: ms, soundChanges: d.sound_changes||[], forms: d.forms||null}) }; });\n"
        "    }).catch(()=>{});\n"
        "  }\n"
        "  runParadigm(lemma){"))
    seg.append(("runSearch single segment",
        "    fetch(this.KOKEN_API+'/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:lg,word})}).then(r=>r.json()).then(d=>{\n"
        "      this.setState({ apiWord:this.apiWordFrom(lg, word, d.analyses), activeWordId:'__api', apiAllLangs:{}, apiMatchCodes:[], apiMatchLang:null, screen:'analiz', selMorphIdx:0, stripCount:0 });\n"
        "    }).catch(()=>{});",
        "    fetch(this.KOKEN_API+'/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:lg,word})}).then(r=>r.json()).then(d=>{\n"
        "      this.setState({ apiWord:this.apiWordFrom(lg, word, d.analyses), activeWordId:'__api', apiAllLangs:{}, apiMatchCodes:[], apiMatchLang:null, screen:'analiz', selMorphIdx:0, stripCount:0 });\n"
        "      this.applySegment(lg, word);\n"
        "    }).catch(()=>{});"))
    seg.append(("runSearch auto segment",
        "        this.setState({ apiAllLangs:langs, apiMatchCodes:codes, apiMatchLang:first, apiWord:this.apiWordFrom(first, word, langs[first]), activeWordId:'__api', screen:'analiz', selMorphIdx:0, stripCount:0 });",
        "        this.setState({ apiAllLangs:langs, apiMatchCodes:codes, apiMatchLang:first, apiWord:this.apiWordFrom(first, word, langs[first]), activeWordId:'__api', screen:'analiz', selMorphIdx:0, stripCount:0 });\n"
        "        this.applySegment(first, word);"))
    nseg = 0
    for label, old, new in seg:
        if old in html:
            html = html.replace(old, new, 1); nseg += 1
        else:
            print("  ! SEG eşleşmedi:", label)
    print(f"  Analiz segment (gerçek yüzey ekleri): {nseg}/{len(seg)}")

    # ses olayı (sound_changes) rozeti — analiz: "p → b · ünsüz yumuşaması" (öğrenci + araştırmacı)
    scfix = []
    scfix.append(("ses olayı render",
        "      active:{surface:w.surface, translit:w.translit, gloss:w.gloss, langName:w.langName, headword:this.disp(w.surface,w.translit), morphemes},",
        "      active:{surface:w.surface, translit:w.translit, gloss:w.gloss, langName:w.langName, headword:this.disp(w.surface,w.translit), morphemes},\n"
        "      soundChanges:((w&&w.soundChanges)||[]).map(c=>({disp:c.from+' → '+c.to, type:c.type})), hasSoundChanges:!!(w&&w.soundChanges&&w.soundChanges.length),"))
    scfix.append(("ses olayı markup",
        "{{ fstSource }} · {{ fstLicense }}</span>\n          </div>\n          </sc-if>",
        "{{ fstSource }} · {{ fstLicense }}</span>\n          </div>\n          </sc-if>\n"
        "          <sc-if value=\"{{ hasSoundChanges }}\" hint-placeholder-val=\"{{ false }}\">\n"
        "          <div style=\"margin-top:16px;padding-top:14px;border-top:1px dashed rgba(33,29,23,.12);display:flex;align-items:center;gap:8px;flex-wrap:wrap\">\n"
        "            <span style=\"font-family:'IBM Plex Mono',monospace;font-size:11px;color:#9a9082;letter-spacing:.5px\">SES OLAYI</span>\n"
        "            <sc-for list=\"{{ soundChanges }}\" as=\"c\" hint-placeholder-count=\"2\"><span style=\"display:inline-flex;align-items:center;gap:7px;font-size:12.5px;background:#f3efe6;border:1px solid rgba(217,139,74,.3);border-radius:14px;padding:4px 12px;color:#3f3a32\"><span style=\"font-family:'Spectral',serif;font-weight:600\">{{ c.disp }}</span><span style=\"color:#9a9082\">{{ c.type }}</span></span></sc-for>\n"
        "          </div>\n"
        "          </sc-if>"))
    nsc2 = 0
    for label, old, new in scfix:
        if old in html:
            html = html.replace(old, new, 1); nsc2 += 1
        else:
            print("  ! ses olayı eşleşmedi:", label)
    print(f"  Ses olayı rozeti: {nsc2}/{len(scfix)}")

    # ============================================================
    #  GÜNCELLEME (24 Haz) — temizlik & yeni davranışlar (kullanıcı notları)
    #  • "HAM ÇIKTI / ⬇ Dışa aktar" kara barları yersiz → kaldır; export tablolarda kopyalama olur.
    #  • Sol-alt "XP · x/y ünite" sayacı saçma → kaldır (eğitim portalı GELECEK işi).
    #  • Kullanılmayan 'demo' kaynağını kütükten çıkar (F).  • Font/renk paleti korunur.
    # ============================================================
    gfix = []  # (etiket, eski, yeni)

    # G7 — sol-alt XP sayacı kaldır
    gfix.append(("sidebar XP",
        '      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">\n'
        "        <span style=\"font-family:'Spectral',serif;font-size:18px;font-weight:700;color:#d98b4a\">{{ hubXp }}</span>\n"
        '        <span style="font-size:11px;color:rgba(244,241,234,.5)">XP · {{ hubDoneCount }}/{{ hubTotal }} ünite tamam</span>\n'
        '      </div>\n', ''))

    # G1 — Paradigma ekranındaki kara "HAM ÇIKTI / Dışa aktar" barı kaldır
    gfix.append(("paradigma export barı",
        '        <sc-if value="{{ isExpert }}" hint-placeholder-val="{{ false }}">\n'
        '        <div style="margin-top:14px;display:flex;align-items:center;gap:12px;background:#15120e;color:#f4f1ea;border-radius:11px;padding:11px 16px;flex-wrap:wrap">\n'
        "          <span style=\"font-size:11px;font-family:'IBM Plex Mono',monospace;letter-spacing:.5px;color:#9abf8f\">UZMAN MODU</span>\n"
        '          <span style="font-size:12.5px;color:rgba(244,241,234,.8)">Ham morfolojik etiketler ve kaynak künyeleri görünür.</span>\n'
        '          <button onClick="{{ goResearch }}" style="margin-left:auto;cursor:pointer;background:#2f6fb0;color:#fff;border:none;border-radius:8px;padding:7px 13px;font-size:12px;font-family:inherit">⬇ Dışa aktar</button>\n'
        '        </div>\n'
        '        </sc-if>\n', ''))

    # G1 — Kognat ekranındaki aynı kara barı kaldır
    gfix.append(("kognat export barı",
        '        <sc-if value="{{ isExpert }}" hint-placeholder-val="{{ false }}">\n'
        '        <div style="margin-bottom:14px;display:flex;align-items:center;gap:12px;background:#15120e;color:#f4f1ea;border-radius:11px;padding:11px 16px;flex-wrap:wrap">\n'
        "          <span style=\"font-size:11px;font-family:'IBM Plex Mono',monospace;letter-spacing:.5px;color:#9abf8f\">UZMAN MODU</span>\n"
        '          <span style="font-size:12.5px;color:rgba(244,241,234,.8)">Kognat seti makine-okunur biçimde alınabilir.</span>\n'
        '          <button onClick="{{ goResearch }}" style="margin-left:auto;cursor:pointer;background:#2f6fb0;color:#fff;border:none;border-radius:8px;padding:7px 13px;font-size:12px;font-family:inherit">⬇ Dışa aktar</button>\n'
        '        </div>\n'
        '        </sc-if>\n', ''))

    ngfix = 0
    for label, old, new in gfix:
        if old in html:
            html = html.replace(old, new); ngfix += 1
        else:
            print("  ! güncelleme eşleşmedi:", label)

    # G3 — Paradigma örnek kökleri DİL DENGELİ (her dilden birer örnek; Çuvaşça en önemli/ilk)
    html = html.replace(
        "      goParadigm:()=>this.setState({screen:'paradigm'}),",
        "      goParadigm:()=>this.setState({screen:'paradigm'}),\n"
        "      paradigmExamples: [{lang:'chv', lemma:'хӗр', gloss:'kız', name:'Çuvaşça'}, {lang:'tur', lemma:'ev', gloss:'ev', name:'Türkçe'}, {lang:'tat', lemma:'кул', gloss:'el', name:'Tatarca'}, {lang:'kaz', lemma:'бала', gloss:'çocuk', name:'Kazakça'}, {lang:'sah', lemma:'ат', gloss:'at', name:'Yakutça'}].map(e=>{ const sel = this.state.paradigmFree && this.state.paradigmFree.lemma===e.lemma && this.state.searchLang===e.lang; return { label:e.lemma, gloss:e.gloss, kind:e.name, go:()=>{ this.setState({searchLang:e.lang, paradigmFreeQ:e.lemma}); setTimeout(()=>this.runParadigm(e.lemma),0); }, style:`cursor:pointer;display:flex;flex-direction:column;align-items:flex-start;gap:2px;border:1.5px solid ${sel?'#211d17':'rgba(33,29,23,.14)'};background:${sel?'#211d17':'#fff'};color:${sel?'#f4f1ea':'#211d17'};border-radius:11px;padding:10px 15px;font-family:inherit`, glossStyle:`font-size:11px;color:${sel?'rgba(244,241,234,.6)':'#9a9082'}` }; }),", 1)

    # G1 — Paradigma tablosuna "Tabloyu kopyala" (export tablolarda kopyalama olur)
    html = html.replace(
        '        <div style="margin-top:22px;background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:16px;overflow:hidden">',
        '        <div style="margin-top:22px;display:flex;align-items:center;gap:10px">\n'
        "          <span style=\"font-size:11px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.5px\">ÇEKİM TABLOSU</span>\n"
        '          <button onClick="{{ copyParadigm }}" style="margin-left:auto;cursor:pointer;background:#fff;border:1px solid rgba(33,29,23,.16);border-radius:8px;padding:6px 12px;font-size:12px;font-family:inherit;color:#211d17">⧉ Tabloyu kopyala</button>\n'
        '        </div>\n'
        '        <div id="paradigm-table" style="margin-top:10px;background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:16px;overflow:hidden">', 1)
    # copyParadigm handler (DOM → pano; tablodan bağımsız, güvenli)
    html = html.replace(
        "      goResearch:()=>this.setState({screen:'research'}),",
        "      goResearch:()=>this.setState({screen:'research'}),\n"
        "      copyParadigm:()=>{ try{ const t=document.getElementById('paradigm-table'); if(t) navigator.clipboard.writeText(t.innerText); }catch(e){} },\n"
        "      apiMatches: (this.state.apiMatchCodes||[]).map(lc=>{ const sel=lc===this.state.apiMatchLang; return { label:(this.LIVE_LN[lc]||lc), go:()=>{ const wd=(this.state.apiWord&&this.state.apiWord.surface)||''; this.setState({apiMatchLang:lc, apiWord:this.apiWordFrom(lc, wd, (this.state.apiAllLangs||{})[lc]), selMorphIdx:0}); this.applySegment(lc, wd); }, style:`cursor:pointer;border:1.5px solid ${sel?'#211d17':'rgba(33,29,23,.16)'};background:${sel?'#211d17':'#fff'};color:${sel?'#f4f1ea':'#211d17'};border-radius:16px;padding:5px 13px;font-size:12.5px;font-family:inherit` }; }),\n"
        "      hasApiMatches: (this.state.apiMatchCodes||[]).length>1,", 1)

    # A — Analiz ekranına "bu kelime şu dillerde" çip satırı (otomatik/multi-dil sonucu)
    html = html.replace(
        '        <div style="display:grid;grid-template-columns:1.2fr .8fr;gap:20px;margin-top:20px">',
        '        <sc-if value="{{ hasApiMatches }}" hint-placeholder-val="{{ false }}">\n'
        '        <div style="margin-top:18px;display:flex;align-items:center;gap:9px;flex-wrap:wrap">\n'
        "          <span style=\"font-size:11px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.5px\">BU KELİME ŞU DİLLERDE</span>\n"
        '          <sc-for list="{{ apiMatches }}" as="m" hint-placeholder-count="3"><button onClick="{{ m.go }}" style="{{ m.style }}">{{ m.label }}</button></sc-for>\n'
        '        </div>\n'
        '        </sc-if>\n'
        '        <div style="display:grid;grid-template-columns:1.2fr .8fr;gap:20px;margin-top:20px">', 1)

    # F — kullanılmayan 'demo' kaynağını kütükten çıkar (tüm modüller artık kaynaklı)
    html = html.replace(
        "    demo:   {label:'Örnek veri (illüstratif)', detail:'gerçek backend bağlanınca değişecek', lic:'—', kind:'geçici', url:'—'},\n", "")

    print(f"  Güncelleme temizliği (XP/export barları): {ngfix}/3")

    # ============================================================
    #  B — ARAŞTIRMACI MERKEZİ CANLI (serbest sözcük + sağ-üst dil → /analyze → gerçek JSON/CoNLL-U/CSV + indir)
    # ============================================================
    # runResearch metodu (canlı analiz → researchApi); küratörlü kelime yerine sentetik WORD-şekilli nesne
    html = html.replace(
        "  researchVals(){",
        "  runResearch(lang, word){\n"
        "    if(lang==='auto'){\n"
        "      fetch(this.KOKEN_API+'/analyze_all',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({word})}).then(r=>r.json()).then(d=>{ const langs=d.langs||{}; const codes=Object.keys(langs); const l=codes[0]||'chv'; this.setState({ researchApi:{lang:l, word, analyses:(codes.length?langs[l]:[])} }); }).catch(()=>{});\n"
        "      return;\n"
        "    }\n"
        "    fetch(this.KOKEN_API+'/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang,word})}).then(r=>r.json()).then(d=>{\n"
        "      this.setState({ researchApi:{lang, word, analyses:d.analyses||[]} });\n"
        "    }).catch(()=>{});\n"
        "  }\n\n"
        "  researchVals(){", 1)

    bfix = []
    bfix.append(("research veri kaynağı",
        "    const S = this.state, w = this.WORDS[S.researchWord];\n    if (!w) return {};",
        "    const S = this.state;\n"
        "    let w = this.WORDS[S.researchWord];\n"
        "    if (S.researchApi){ const R=S.researchApi; const a=(R.analyses&&R.analyses[0])||null;\n"
        "      const ms = a ? [{text:a.lemma, gItem:a.lemma, gloss:'lemma', type:'kök'}].concat((a.tags||[]).map(t=>({text:'', gItem:'', gloss:t, type:(/^(pres|past|fut|aor)$/.test(t)?'zaman':/^p[123]/.test(t)?'kişi':'etiket')}))) : [{text:R.word, gItem:R.word, gloss:'?', type:'kök'}];\n"
        "      w = { lang:R.lang, langName:(this.LIVE_LN[R.lang]||R.lang), surface:R.word, translit:'', gloss:(a?('apertium: '+a.raw):'çözümlenemedi'), morphemes:ms };\n"
        "    }\n"
        "    if (!w) return {};"))
    bfix.append(("research çip sel",
        "      const sel = k===S.researchWord;\n      return { key:k, surface:v.surface, gloss:v.gloss, sel, go:()=>this.setState({researchWord:k}),",
        "      const sel = !S.researchApi && k===S.researchWord;\n      return { key:k, surface:v.surface, gloss:v.gloss, sel, go:()=>this.setState({researchWord:k, researchApi:null}),"))
    bfix.append(("research json lang", "lang:'chv', lemma, gloss:w.gloss,", "lang:(w.lang||'chv'), lemma, gloss:w.gloss,"))
    bfix.append(("research conllu lang", "# lang = chv", "# lang = ${w.lang||'chv'}"))
    bfix.append(("research return",
        "    return { researchWords:words, researchFmtTabs:fmtTabs, researchCode:fmts[S.researchFmt],\n"
        "      researchApiUrl:`GET /api/v1/analyze?lang=chv&form=${encodeURIComponent(w.surface)}`,\n"
        "      copyResearch:()=>{ try{ navigator.clipboard.writeText(fmts[S.researchFmt]); }catch(e){} } };",
        "    const cur = fmts[S.researchFmt]; const ext = {json:'json',conllu:'conllu',csv:'csv'}[S.researchFmt];\n"
        "    const lgR = (S.searchLang&&S.searchLang!=='auto')?S.searchLang:'chv';\n"
        "    return { researchWords:words, researchFmtTabs:fmtTabs, researchCode:cur,\n"
        "      researchQ: S.researchQ||'', researchLangName: (S.searchLang==='auto'?'Otomatik':(this.LIVE_LN[lgR]||'Çuvaşça')), researchLive: !!S.researchApi,\n"
        "      onResearchInput:(e)=>this.setState({researchQ:e.target.value}),\n"
        "      onResearchKey:(e)=>{ if(e.key!=='Enter') return; const word=(this.state.researchQ||'').trim(); if(!word) return; this.runResearch((this.state.searchLang||'auto'), word); },\n"
        "      researchApiUrl:`GET /api/v1/analyze?lang=${w.lang||'chv'}&form=${encodeURIComponent(w.surface)}`,\n"
        "      copyResearch:()=>{ try{ navigator.clipboard.writeText(cur); }catch(e){} },\n"
        "      downloadResearch:()=>{ try{ const b=new Blob([cur],{type:'text/plain;charset=utf-8'}); const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download='koken_'+(w.surface||'analiz')+'.'+ext; a.click(); }catch(e){} } };"))
    # markup: serbest giriş kutusu (örnek çiplerin üstünde) + indir butonu
    bfix.append(("research input markup",
        '        <div style="display:flex;gap:8px;flex-wrap:wrap">\n'
        "          <sc-for list=\"{{ researchWords }}\" as=\"w\" hint-placeholder-count=\"4\"><button onClick=\"{{ w.go }}\" style=\"{{ w.style }}\">{{ w.surface }} <span style=\"font-size:11px;opacity:.6;font-family:'IBM Plex Sans'\">{{ w.gloss }}</span></button></sc-for>\n"
        '        </div>',
        '        <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px">\n'
        '          <input value="{{ researchQ }}" onInput="{{ onResearchInput }}" onKeyDown="{{ onResearchKey }}" placeholder="Sözcük yaz + Enter — canlı çözümle &amp; dışa aktar" style="flex:1;min-width:260px;max-width:460px;' + INP + '">\n'
        '          ' + SELBOX + '\n'
        '        </div>\n'
        "        <div style=\"font-size:11px;letter-spacing:1px;color:#9a9082;margin-bottom:8px;font-family:'IBM Plex Mono',monospace\">ÖRNEK (Çuvaşça · hızlı doldur)</div>\n"
        '        <div style="display:flex;gap:8px;flex-wrap:wrap">\n'
        "          <sc-for list=\"{{ researchWords }}\" as=\"w\" hint-placeholder-count=\"4\"><button onClick=\"{{ w.go }}\" style=\"{{ w.style }}\">{{ w.surface }} <span style=\"font-size:11px;opacity:.6;font-family:'IBM Plex Sans'\">{{ w.gloss }}</span></button></sc-for>\n"
        '        </div>'))
    bfix.append(("research download btn",
        '              <button onClick="{{ copyResearch }}" style="margin-left:auto;cursor:pointer;background:rgba(244,241,234,.1);color:#f4f1ea;border:none;border-radius:7px;padding:7px 13px;font-size:12px;font-family:inherit">⧉ Kopyala</button>',
        '              <button onClick="{{ downloadResearch }}" style="margin-left:auto;cursor:pointer;background:rgba(244,241,234,.1);color:#f4f1ea;border:none;border-radius:7px;padding:7px 13px;font-size:12px;font-family:inherit">⬇ İndir</button>\n'
        '              <button onClick="{{ copyResearch }}" style="cursor:pointer;background:rgba(244,241,234,.1);color:#f4f1ea;border:none;border-radius:7px;padding:7px 13px;font-size:12px;font-family:inherit">⧉ Kopyala</button>'))
    nb = 0
    for label, old, new in bfix:
        if old in html:
            html = html.replace(old, new, 1); nb += 1
        else:
            print("  ! B eşleşmedi:", label)
    print(f"  Araştırmacı Merkezi canlı (B): {nb}/{len(bfix)}")

    # ============================================================
    #  PARADİGMA — İSİM/FİİL sekmeleri + fiil çekim tablosu (zaman × kişi); "at" gibi köklerde fiil de
    #  (G1'in ÇEKİM TABLOSU başlığından SONRA çalışmalı)
    # ============================================================
    cfix = []
    cfix.append(("paradigma pos tabs",
        '        <div style="margin-top:22px;display:flex;align-items:center;gap:10px">\n'
        "          <span style=\"font-size:11px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.5px\">ÇEKİM TABLOSU</span>",
        '        <sc-if value="{{ paradigmHasPosTabs }}" hint-placeholder-val="{{ false }}">\n'
        '        <div style="display:flex;gap:8px;background:#ece7dc;padding:5px;border-radius:11px;width:fit-content;margin-top:18px">\n'
        '          <sc-for list="{{ paradigmPosTabs }}" as="t" hint-placeholder-count="2"><button onClick="{{ t.go }}" style="{{ t.style }}">{{ t.label }}</button></sc-for>\n'
        '        </div>\n'
        '        </sc-if>\n'
        '        <div style="margin-top:18px;display:flex;align-items:center;gap:10px">\n'
        "          <span style=\"font-size:11px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.5px\">ÇEKİM TABLOSU</span>"))
    verbview = (
        '          <sc-if value="{{ paradigmIsVerbView }}" hint-placeholder-val="{{ false }}">\n'
        '          <sc-for list="{{ paradigmVerbBlocks }}" as="blk" hint-placeholder-count="3">\n'
        "            <div style=\"background:#211d17;color:#f4f1ea;font-size:11px;font-family:'IBM Plex Mono',monospace;letter-spacing:.5px;padding:9px 22px\">{{ blk.tense }}</div>\n"
        '            <div style="display:grid;grid-template-columns:repeat(3,1fr)">\n'
        '              <sc-for list="{{ blk.cells }}" as="c" hint-placeholder-count="6">\n'
        '                <div style="padding:11px 18px;border-bottom:1px solid rgba(33,29,23,.07);border-right:1px solid rgba(33,29,23,.05)">\n'
        "                  <div style=\"font-size:10.5px;color:#9a9082;font-family:'IBM Plex Mono',monospace\">{{ c.person }}</div>\n"
        "                  <div style=\"font-family:'Spectral',serif;font-size:18px;font-weight:600;color:#211d17;margin-top:2px\">{{ c.surface }}</div>\n"
        '                </div>\n'
        '              </sc-for>\n'
        '            </div>\n'
        '          </sc-for>\n'
        '          </sc-if>\n')
    cfix.append(("paradigma fiil tablosu",
        '        </div>\n        <div style="margin-top:14px;display:flex;gap:16px;flex-wrap:wrap"><sc-for list="{{ legend }}"',
        verbview + '        </div>\n        <div style="margin-top:14px;display:flex;gap:16px;flex-wrap:wrap"><sc-for list="{{ legend }}"'))
    ncfix = 0
    for label, old, new in cfix:
        if old in html:
            html = html.replace(old, new, 1); ncfix += 1
        else:
            print("  ! C(paradigma) eşleşmedi:", label)
    print(f"  Paradigma isim/fiil sekmeleri + fiil tablosu: {ncfix}/{len(cfix)}")

    # ============================================================
    #  AÇIK API dürüst etiket (planlanan genel API) + "nasıl çalışır?" aç-kapa ipuçları (çift kitle)
    # ============================================================
    def helpblk(scr, text):
        return ('        <button onClick="{{ toggleHelp_%s }}" style="cursor:pointer;background:none;border:1px solid rgba(33,29,23,.16);border-radius:8px;padding:6px 12px;font-size:12px;font-family:inherit;color:#5f574b;margin:0 0 14px">✷ nasıl çalışır?</button>\n'
                '        <sc-if value="{{ help_%s }}" hint-placeholder-val="{{ false }}">\n'
                '        <div style="background:#f3efe6;border:1px solid rgba(33,29,23,.1);border-radius:12px;padding:15px 18px;margin:0 0 18px;font-size:13.5px;line-height:1.7;color:#3f3a32;max-width:74ch">%s</div>\n'
                '        </sc-if>\n') % (scr, scr, text)
    dfix2 = []
    dfix2.append(("help render bağları",
        "      goResearch:()=>this.setState({screen:'research'}),",
        "      goResearch:()=>this.setState({screen:'research'}),\n"
        "      help_research:this.state.helpOpen==='research', toggleHelp_research:()=>this.setState(s=>({helpOpen:s.helpOpen==='research'?'':'research'})),\n"
        "      help_cognate:this.state.helpOpen==='cognate', toggleHelp_cognate:()=>this.setState(s=>({helpOpen:s.helpOpen==='cognate'?'':'cognate'})),\n"
        "      help_compare:this.state.helpOpen==='compare', toggleHelp_compare:()=>this.setState(s=>({helpOpen:s.helpOpen==='compare'?'':'compare'})),"))
    dfix2.append(("help research",
        '<p style="font-size:15px;line-height:1.6;color:#5f574b;max-width:66ch;margin:0 0 16px">Bir sözcük seç; çözümlemeyi makine-okunur biçimlerde al. Her kayıt kaynak + lisans alanlıdır; sonuç alıntılanabilir kalıcı bir bağlantı üretir.</p>',
        '<p style="font-size:15px;line-height:1.6;color:#5f574b;max-width:66ch;margin:0 0 16px">Bir sözcük seç; çözümlemeyi makine-okunur biçimlerde al. Her kayıt kaynak + lisans alanlıdır; sonuç alıntılanabilir kalıcı bir bağlantı üretir.</p>\n'
        + helpblk('research', 'Bir sözcük yazıp Enter’a basınca kelime, sunucuda çalışan <strong>Apertium FST motorumuza</strong> (bizim API) gönderilir; kök ve dilbilgisi etiketleri çıkarılıp <strong>JSON / CoNLL-U / CSV</strong> biçimlerinde, kaynak ve lisansıyla sunulur — “İndir”le dosya alınır. Sağdaki “AÇIK API” kutusu, ileride <strong>yayımlanacak genel REST ucunun taslağıdır</strong> (şu an yerel/geliştirme ortamında çalışıyor).')))
    dfix2.append(("help cognate",
        '<p style="font-size:15px;line-height:1.6;color:#5f574b;max-width:64ch;margin:0 0 12px">Ortak bir atadan gelen biçimler. Turuncu kesik çizgi, o dilde düzenli bir <strong>ses değişimi</strong> olduğunu gösterir — kök aynı, görünüş farklı.</p>',
        '<p style="font-size:15px;line-height:1.6;color:#5f574b;max-width:64ch;margin:0 0 12px">Ortak bir atadan gelen biçimler. Turuncu kesik çizgi, o dilde düzenli bir <strong>ses değişimi</strong> olduğunu gösterir — kök aynı, görünüş farklı.</p>\n'
        + helpblk('cognate', 'Buradaki köktaşlar <strong>canlı analiz değildir</strong>; <strong>SavelyevTurkic CLDF</strong> veri setinden (905 kognat seti, 254 kavram) seçilmiş hazır karşılaştırmalı veridir. Yazdığınız herhangi bir kelimenin kognatı otomatik üretilmez — kognat tespiti ayrı bir iştir. Şu an 14 kavram gösteriliyor; daha fazlası <strong>yatay ölçek</strong> aşamasında eklenecek.')))
    dfix2.append(("help compare",
        '<div style="display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-top:8px">',
        helpblk('compare', 'Yazdığınız kelime, tüm MVP dillerinde Apertium ile <strong>anlık çözümlenir</strong> (/analyze_all) ve kök+ek dizilimi diller arası yan yana getirilir. “Ses denklikleri” sekmesi ise Çuvaşça↔Ortak Türkçe <strong>düzenli ses değişimlerini</strong> (küratörlü) gösterir.')
        + '        <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-top:8px">'))
    dfix2.append(("açık api label",
        "<div style=\"font-size:11px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.5px\">AÇIK API</div>",
        "<div style=\"font-size:11px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.5px\">AÇIK API · planlanan</div>"))
    dfix2.append(("açık api desc",
        '<div style="font-size:12.5px;color:#5f574b;margin-top:10px;line-height:1.5">REST uç noktası; programatik erişim baştan tasarıma dahil.</div>',
        '<div style="font-size:12.5px;color:#5f574b;margin-top:10px;line-height:1.5">Genel REST ucu — programatik erişim baştan tasarıma dahil. <strong>Şu an yerel/geliştirme</strong>; yayımlanınca bu biçimde erişilecek.</div>'))
    nd2 = 0
    for label, old, new in dfix2:
        if old in html:
            html = html.replace(old, new, 1); nd2 += 1
        else:
            print("  ! D2 eşleşmedi:", label)
    print(f"  Açık API etiket + nasıl çalışır ipuçları: {nd2}/{len(dfix2)}")

    # ============================================================
    #  DAYANIKLILIK — hue() bilinmeyen morfem tipinde ÇÖKMESİN (segment fallback 'ek' vb. → kök rengine düş)
    #  (Kırmızı ekran "renderVals: reading 'hue'" bug'ının kök çözümü)
    # ============================================================
    hue_old = ("  hue(t){ return `oklch(0.52 0.13 ${this.TYPES[t].hue})`; }\n"
               "  hueLight(t){ return `oklch(0.74 0.13 ${this.TYPES[t].hue})`; }\n"
               "  hueBg(t){ return `oklch(0.94 0.045 ${this.TYPES[t].hue})`; }\n"
               "  hueBorder(t){ return `oklch(0.84 0.07 ${this.TYPES[t].hue})`; }")
    hue_new = ("  _hue(t){ return (this.TYPES[t]||this.TYPES['kök']).hue; }\n"
               "  hue(t){ return `oklch(0.52 0.13 ${this._hue(t)})`; }\n"
               "  hueLight(t){ return `oklch(0.74 0.13 ${this._hue(t)})`; }\n"
               "  hueBg(t){ return `oklch(0.94 0.045 ${this._hue(t)})`; }\n"
               "  hueBorder(t){ return `oklch(0.84 0.07 ${this._hue(t)})`; }")
    if hue_old in html:
        html = html.replace(hue_old, hue_new, 1); print("  hue() dayanıklı: 1")
    else:
        print("  ! hue() eşleşmedi")

    # ============================================================
    #  ÜST BAR KALDIRILDI (kullanıcı isteği) — her ekranda kendi girişi var; Кир/Lat sidebar'a taşındı
    # ============================================================
    html2, ntop = re.subn(r'<!-- context bar -->.*?<div id="content-scroll"', '<div id="content-scroll"', html, flags=re.DOTALL)
    if ntop:
        html = html2
    print(f"  Üst bar kaldırıldı: {ntop}")
    # scriptToggle (Кир/Lat) koyu sidebar'a uygun stil
    sc_old = ("    const scriptToggle = [['cyrillic','Кир'],['latin','Lat']].map(([id,label])=>({\n"
              "      label, go:()=>this.setState({script:id}), style:seg(S.script===id) }));")
    sc_new = ("    const segD = (active)=>`cursor:pointer;border:none;padding:5px 12px;font-size:12px;font-weight:600;font-family:inherit;border-radius:7px;background:${active?'#f4f1ea':'transparent'};color:${active?'#211d17':'rgba(244,241,234,.55)'}`;\n"
              "    const scriptToggle = [['cyrillic','Кир'],['latin','Lat']].map(([id,label])=>({\n"
              "      label, go:()=>this.setState({script:id}), style:segD(S.script===id) }));")
    nsc = 1 if sc_old in html else 0
    html = html.replace(sc_old, sc_new, 1)
    # Кир/Lat'ı sidebar alt kısmına ekle (versiyon satırının üstüne)
    side_old = '    <div style="padding:14px 20px 16px;border-top:1px solid rgba(244,241,234,.12)">\n'
    side_new = ('    <div style="padding:14px 20px 16px;border-top:1px solid rgba(244,241,234,.12)">\n'
                '      <div style="display:flex;align-items:center;gap:8px;margin-bottom:11px">\n'
                "        <span style=\"font-size:10px;font-family:'IBM Plex Mono',monospace;color:rgba(244,241,234,.4);letter-spacing:.5px\">YAZI</span>\n"
                '        <div style="display:flex;background:rgba(244,241,234,.08);border-radius:8px;padding:3px"><sc-for list="{{ scriptToggle }}" as="m" hint-placeholder-count="2"><button onClick="{{ m.go }}" style="{{ m.style }}">{{ m.label }}</button></sc-for></div>\n'
                '      </div>\n')
    nside = 1 if side_old in html else 0
    html = html.replace(side_old, side_new, 1)
    print(f"  script toggle sidebar'a: style={nsc} sidebar={nside}")

    # ============================================================
    #  D — KARŞILAŞTIR "dizilim" CANLI: aranan kelime tüm dillerde (/analyze_all) → satırlar
    #  (FST kök+etiket verir; yüzey-segmentasyon değil — küratörlü kognatlardaki renkli hizalama kadar
    #   ince değil ama gerçek/canlı. Küratörlü kelimeler eski zengin görünümünü korur.)
    # ============================================================
    dfix = []
    # canlı kelimede Karşılaştır'a geçerken kelimeyi tüm dillerde çöz
    dfix.append(("compare fetch",
        "      goCompareActive:()=>this.setState({screen:'compare', compareTab:'rows'}),",
        "      goCompareActive:()=>{ if(this.state.activeWordId==='__api' && this.state.apiWord){ this.runCompare(this.state.apiWord.surface, this.state.apiMatchLang || this.state.searchLang); } else { this.setState({screen:'compare', compareTab:'rows'}); } },"))
    # allLangs: canlı sonuç varsa dillerden GERÇEK ek dizilimi (segment); yoksa POS etiketlerini eleyerek tag
    dfix.append(("compare allLangs",
        "    const allLangs = [{lang:w.lang,langName:w.langName,branch:'Ogur',translit:w.translit,morphemes:w.morphemes.map(m=>[m.text,m.tag,m.type]),self:true}, ...w.cognates];",
        "    const cmpA = (S.activeWordId==='__api' && S.compareApi && S.compareApi.word===w.surface) ? S.compareApi : null;\n"
        "    const cmpRows = cmpA ? cmpA.rows : null;\n"
        "    const CBR = {tur:'Oğuz',aze:'Oğuz',tuk:'Oğuz',kaz:'Kıpçak',kir:'Kıpçak',tat:'Kıpçak',bak:'Kıpçak',uzb:'Karluk',uig:'Karluk',chv:'Ogur',sah:'Sibirya'};\n"
        "    const allLangs = cmpRows\n"
        "      ? Object.entries(cmpRows).map(([lc,info])=>{ const seg=info.morphemes; const ms = (seg && seg.length) ? seg.map(m=>[m.surface, (m.tag||'').toString(), (m.type||'kök')]) : [[info.surface,'KÖK','kök']]; return {lang:lc, langName:(this.LIVE_LN[lc]||lc), branch:(CBR[lc]||'—'), translit:info.surface, morphemes:ms, self:!!info.self}; })\n"
        "      : [{lang:w.lang,langName:w.langName,branch:'Ogur',translit:w.translit,morphemes:w.morphemes.map(m=>[m.text,m.tag,m.type]),self:true}, ...w.cognates];"))
    # başlık: A2 — sekmeye-duyarlı. Dizilim'de canlı kelimenin yüzey biçimi + "— diller arası";
    # mantıksız sekmelerde (ses denklikleri/soy ağacı/harita) kelime referansı YOK, sekme başlığı.
    dfix.append(("compare başlık binding (A2 sekmeye-duyarlı)",
        "      compareRows, legend, soundCards, familyRows, timeline,",
        "      compareRows, compareHeadline:(S.compareTab==='sound' ? 'Ses denklikleri' : S.compareTab==='tree' ? 'Soy ağacı & zaman çizelgesi' : S.compareTab==='map' ? 'Dil haritası' : ('\\u201C'+((S.activeWordId==='__api' && w && w.surface) ? w.surface : (w?w.gloss:''))+'\\u201D — diller arası')), legend, soundCards, familyRows, timeline,"))
    dfix.append(("compare başlık markup (A2 wrapper kaldır)",
        '<h2 style="font-family:\'Spectral\',serif;font-weight:600;font-size:38px;margin:0">“{{ active.gloss }}” — diller arası</h2>',
        '<h2 style="font-family:\'Spectral\',serif;font-weight:600;font-size:38px;margin:0">{{ compareHeadline }}</h2>'))
    nd = 0
    for label, old, new in dfix:
        if old in html:
            html = html.replace(old, new, 1); nd += 1
        else:
            print("  ! D eşleşmedi:", label)
    print(f"  Karşılaştır dizilim canlı (D): {nd}/{len(dfix)}")

    # ============================================================
    #  E — TARİH & KÖKEN: Çuvaş-merkezli, kaynaklı 2 olay (tehlikedeki dile derinlik)
    # ============================================================
    efix = []
    # İdil (Volga) Bulgar mezar yazıtları — Çuvaşçanın doğrudan tarihsel tanığı (Erdal, wolgabolgarische Inschriften)
    efix.append(("tarih: İdil Bulgar",
        "    {era:'13–16.yy', title:'Altın Orda · Çağatayca', desc:'Kıpçak ve Karluk yazı dilleri olgunlaşır; İdil Bulgarcası Çuvaşçaya evrilir.', kind:'dil'},",
        "    {era:'13–14.yy', title:'İdil Bulgar mezar yazıtları', desc:'Volga Bulgarcasının r/l-Türkçesi (Ogur) izlerini taşıyan Arap harfli taş yazıtlar — Çuvaşçanın doğrudan tarihsel tanığı (Erdal, wolgabolgarische Inschriften).', kind:'yazı'},\n"
        "    {era:'13–16.yy', title:'Altın Orda · Çağatayca', desc:'Kıpçak ve Karluk yazı dilleri olgunlaşır; İdil Bulgarcası Çuvaşçaya evrilir.', kind:'dil'},"))
    # Aşmarin'in 17 ciltlik Çuvaş sözlüğü — düşük-kaynaklı dil için olağanüstü betimleyici temel
    efix.append(("tarih: Aşmarin",
        "    {era:'1920–30’lar', title:'Sovyet alfabe reformları',",
        "    {era:'1898–1950', title:'Aşmarin · Çuvaş Sözlüğü (17 cilt)', desc:'N. İ. Aşmarin’in “Çăvaš sămahĕsen kĕneki” adlı 17 ciltlik sözlüğü — düşük-kaynaklı bir dil için olağanüstü betimleyici temel.', kind:'eser'},\n"
        "    {era:'1920–30’lar', title:'Sovyet alfabe reformları',"))
    ne = 0
    for label, old, new in efix:
        if old in html:
            html = html.replace(old, new, 1); ne += 1
        else:
            print("  ! E eşleşmedi:", label)
    print(f"  Tarih & Köken kaynaklı genişletme (E): {ne}/{len(efix)}")

    # ============================================================
    #  E2 — KOLLAR AÇIKLAYICI (deepsearch 8: Türk dilleri sınıflandırma çerçevesi)
    #  6 kol (Johanson; Savelyev & Robbeets 2020 Bayes filogenetiğiyle doğrulandı) — her kol
    #  pedagojik tanım + ayırt edici izogloss + örnek. + Soy ağacı = Bayes Max-Credibility Tree.
    # ============================================================
    KOLLAR = [
        ("Oğur (Bulgar)", "İdil-Ural · ilk ayrılan (~MÖ 66)", "#b8602e",
         "Aileden en erken kopan kol. Tek yaşayan dili Çuvaşça; Fin-Ugor ve Rusça ile iç içe geçtiği için diğer Türk dillerinden en uzağı.",
         [("Rotasizm *z &gt; r", "tokkuz → tăhăr “dokuz”"),
          ("Lambdasizm *š &gt; l", "kïš → hĕl “kış”")]),
        ("Argu (Halaç)", "İran · izole zaman kapsülü", "#8a7a2e",
         "Göktürkçe dönemi seslerini bir zaman kapsülü gibi koruyan izole dil. Tek üye Halaçça (İran, Markazi).",
         [("Söz başı *h- korunur", "*hadaq → hadaq “ayak”"),
          ("Söz içi *-d- korunur", "Orhun arkaik d’li biçimleri")]),
        ("Sibirya (Kuzeydoğu)", "Sibirya · Kuzey + Güney", "oklch(0.52 0.13 235)",
         "Moğol ve Tunguz komşulukla şekillenen kuzey dilleri. Kuzey (Yakut, Dolgan ~MS 474) ile Güney (Tuva, Hakas, Altay) ayrı dallardır.",
         [("*-d- ayrışır", "ayak → atah · adak · azax"),
          ("Söz başı *y- &gt; s", "yol → suol (Yakut)")]),
        ("Karluk (Güneydoğu)", "Orta Asya · İpek Yolu", "oklch(0.5 0.13 295)",
         "Semerkant–Buhara–Kaşgar şehir dilleri; Farsça-Arapça etkili, Çağataycanın mirasçısı. Özbekçe, Uygurca.",
         [("*-G korunur", "dağlık → tağlıq"),
          ("Ünlü uyumu zayıflar", "güzel → gözal (Özbek)")]),
        ("Kıpçak (Kuzeybatı)", "Bozkır · geniş yayılım", "oklch(0.5 0.13 150)",
         "Karadeniz kuzeyinden Orta Asya bozkırlarına uzanan göçebe kol. Kazak, Tatar, Kırgız, Başkurt, Karakalpak…",
         [("*-G &gt; -w", "dağlı → tawlı"),
          ("Söz başı *y- &gt; c/j", "yol → col / jol")]),
        ("Oğuz (Güneybatı)", "Anadolu–Kafkas–Balkan", "oklch(0.55 0.13 35)",
         "En çok konuşulan ve birbirini en rahat anlayan kol. Türkçe, Azerice, Türkmence, Gagavuzca.",
         [("Baş ses tonlulaşması *t&gt;d, *k&gt;g", "tağ → dağ, kök → gök"),
          ("Sonek *-G düşer", "kalgan → kalan")]),
    ]
    def _kol_card(name, region, color, desc, rules):
        rr = ""
        for rule, ex in rules:
            rr += (f"""                  <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap"><span style="font-family:'IBM Plex Mono',monospace;font-size:10px;background:#f3eee3;border-radius:5px;padding:2px 7px;color:#7a7164;white-space:nowrap">{rule}</span><span style="font-family:'Spectral',serif;font-size:13px;color:#211d17">{ex}</span></div>\n""")
        return (f"""                <div style="background:#fff;border:1px solid rgba(33,29,23,.1);border-left:4px solid {color};border-radius:12px;padding:15px 17px">\n"""
                f"""                  <div style="display:flex;align-items:baseline;gap:9px;flex-wrap:wrap"><span style="font-family:'Spectral',serif;font-size:17px;font-weight:700;color:{color}">{name}</span><span style="font-size:10.5px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.3px">{region}</span></div>\n"""
                f"""                  <p style="font-size:12px;line-height:1.55;color:#5f574b;margin:7px 0 11px">{desc}</p>\n"""
                f"""                  <div style="display:flex;flex-direction:column;gap:6px">\n{rr}                  </div>\n"""
                f"""                </div>\n""")
    kollar_cards = "".join(_kol_card(*k) for k in KOLLAR)
    # Kart, "Tarih & Köken" (isHistory) ekranına — kronolojik zaman çizelgesinin HEMEN ÜSTÜNE girer.
    kollar_card = (
        """        <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:16px;padding:24px 26px;margin:6px 0 30px">\n"""
        """          <div style="font-family:'Spectral',serif;font-weight:600;font-size:22px;margin-bottom:6px">Türk dillerinin altı kolu</div>\n"""
        """          <p style="font-size:13.5px;line-height:1.6;color:#5f574b;max-width:74ch;margin:0 0 18px">Lars Johanson'ın <b>altı kollu</b> modeli bugün Türkoloji'nin altın standardıdır; Savelyev &amp; Robbeets (2020) Bayes filogenetiğiyle de doğrulanmıştır. Her kolu, tarihsel bir ses yasası — <b>izogloss</b> — birbirinden ayırır.</p>\n"""
        """          <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:13px">\n"""
        + kollar_cards +
        """          </div>\n"""
        # Geçişken & sınır diller (deepsearch 8 nüansları) — kol etiketleri net olmayan diller
        """          <div style="margin-top:18px;padding-top:16px;border-top:1px dashed rgba(33,29,23,.16)">\n"""
        """            <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.5px;color:#9a9082;margin-bottom:9px">GEÇİŞKEN &amp; SINIR DİLLER</div>\n"""
        """            <div style="display:flex;flex-direction:column;gap:7px;font-size:12.5px;line-height:1.55;color:#5f574b;max-width:80ch">\n"""
        """              <div><b style="color:#211d17">Kırım Tatarcası</b> — köken olarak <b>Kıpçak</b>, ama yüzyıllarca Osmanlı temasıyla güçlü Oğuz tabakası edinmiş <b>geçişken</b> bir dil (Kıpçak gövde + Oğuz leksikon).</div>\n"""
        """              <div><b style="color:#211d17">Salarca</b> — genetik olarak <b>Oğuz</b>, ancak Çin'de <b>Amdo</b> (Tibet-Çin) dil birliği etkisiyle ünlü uyumunu yitirip analitikleşmiş <span style="font-family:'IBM Plex Mono',monospace;font-size:11px">[areal: Amdo]</span>.</div>\n"""
        """              <div><b style="color:#211d17">Sarı Uygurca</b> — adı yanıltıcıdır: Sincan'daki Karluk Uygurcasıyla akraba <b>değil</b>; arkaik bir <b>Güney Sibirya</b> (Yenisey) dilidir.</div>\n"""
        """            </div>\n"""
        """          </div>\n"""
        """        </div>\n""")
    hist_anchor = """        <h2 style="font-family:'Spectral',serif;font-weight:600;font-size:38px;margin:8px 0 18px">Proto-Türkçeden bugüne</h2>\n"""
    nkol = 1 if hist_anchor in html else 0
    html = html.replace(hist_anchor, hist_anchor + kollar_card, 1)

    old_family = (
        "  FAMILY = [\n"
        "    {name:'Proto-Türkçe', note:'ana dil', depth:0},\n"
        "    {name:'Ogur (Bulgar) kolu', note:'erken ayrılan dal', depth:1},\n"
        "    {name:'Çuvaşça', note:'tek yaşayan Ogur dili', depth:2, hi:true},\n"
        "    {name:'Ortak Türkçe', note:'diğer tüm diller', depth:1},\n"
        "    {name:'Oğuz · Kıpçak · Karluk · Sibirya', note:'Türkçe, Tatarca, Kazakça, Yakutça…', depth:2},\n"
        "  ];")
    new_family = (
        "  FAMILY = [\n"
        "    {name:'Proto-Türkçe', note:'ana dil · kök ~MÖ 66 (Bayes: Savelyev & Robbeets 2020)', depth:0},\n"
        "    {name:'Oğur (Bulgar) kolu', note:'ilk ayrılan dal — rotasizm *z>r, lambdasizm *š>l', depth:1},\n"
        "    {name:'Çuvaşça', note:'Oğur kolunun tek yaşayan dili', depth:2, hi:true},\n"
        "    {name:'Genel (Ortak) Türkçe', note:'diğer tüm kollar', depth:1},\n"
        "    {name:'Kuzey Sibirya', note:'~MS 474 — Yakutça (Saha), Dolganca', depth:2},\n"
        "    {name:'Çekirdek Genel Türkçe', note:'', depth:2},\n"
        "    {name:'Güney Sibirya', note:'Tuva, Hakas, Altay · ilk kopan: Sarı Uygurca', depth:3},\n"
        "    {name:'Makro Güneybatı–Doğu', note:'', depth:3},\n"
        "    {name:'Halaç–Salar', note:'Halaçça (Argu) · söz başı *h- korunur', depth:4},\n"
        "    {name:'Merkezî Türkçe', note:'*d>y tamamlanmış homojen blok', depth:4},\n"
        "    {name:'Oğuz kolu', note:'Türkçe, Azerice, Türkmence, Gagavuz', depth:5},\n"
        "    {name:'Makro-Kıpçak', note:'Kıpçak–Karluk kardeşliği', depth:5},\n"
        "    {name:'Karluk kolu', note:'Özbekçe, Uygurca', depth:6},\n"
        "    {name:'Kıpçak kolu', note:'Kazak, Tatar, Kırgız, Başkurt…', depth:6},\n"
        "  ];")
    nfam = 1 if old_family in html else 0
    html = html.replace(old_family, new_family, 1)
    # Kullanıcı geri bildirimi: "Tarih & Köken" en altındaki kara "ırk/gen" kutusu gereksiz → kaldır
    html, nbox = re.subn(
        r'\s*<div style="margin-top:14px;background:#211d17;color:#f4f1ea;border-radius:18px;padding:28px 32px">.*?</div>\s*(</section>)',
        r'\n      \1', html, flags=re.S, count=1)
    print(f"  Kollar aciklayici (ds8): kol_karti={nkol} soy_agaci={nfam} kol_sayisi={len(KOLLAR)} irk_kutu_kaldir={nbox}")

    # --- Katman ağacı / soyma: canlı kelimede GERÇEK yüzey kümülatif biçim (kitap→kitabımız→kitabımızda)
    #     morfem-metni birleştirmek yerine /segment'in döndürdüğü forms[] kullanılır (ses olayı dahil) ---
    html = html.replace(
        "      text: w.morphemes.slice(0,i+1).map(x=>x.text).join(''),",
        "      text: (w.forms && w.forms[i]!=null) ? w.forms[i] : w.morphemes.slice(0,i+1).map(x=>x.text).join(''),", 1)
    html = html.replace(
        "    const stripRoot = remaining.map(x=>x.text).join('') || w.morphemes[0].text;",
        "    const stripRoot = (w.forms && w.forms[w.morphemes.length-1-S.stripCount]!=null) ? w.forms[w.morphemes.length-1-S.stripCount] : (remaining.map(x=>x.text).join('') || w.morphemes[0].text);", 1)

    # ============================================================
    #  JOSHI KAYNAK SINIFI (0–5) — dil profillerine rozet (deepsearch envanter PDF'i; misyon: eksik/gelişmişlik)
    # ============================================================
    # Joshi sınıfı deepsearch 9 (kol-bazlı derin profiller) ile hizalandı (çapraz-kontrol düzeltmeleri):
    #   az 1→2–3, kk 2–3→3, tt 2–3→1, ug 2–3→1, tyv 0→1, kjh 0→1 (kaynak: _profil_*.txt)
    JOSHI = {"tr": "4 · yüksek", "az": "2–3 · orta", "tk": "1 · düşük", "kk": "3 · yükselen",
             "kg": "1 · düşük", "tt": "1 · düşük", "bak": "1 · düşük", "ug": "1 · düşük",
             "chv": "1 · düşük", "sah": "1–2 · gelişen", "tyv": "1 · düşük", "kjh": "1 · düşük",
             "shor": "0 · aşırı düşük", "clw": "0 · aşırı düşük"}
    njoshi = 0
    for code, val in JOSHI.items():
        html, n = re.subn(r"(\{code:'" + re.escape(code) + r"',)", r"\1joshi:'" + val + r"', ", html, count=1)
        njoshi += n
    # stat grid 3→2 sütun + NLP KAYNAK SINIFI kutusu
    html = html.replace(
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:24px">',
        '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:24px">', 1)
    kol_box = ("              <div style=\"background:#fff;border:1px solid rgba(33,29,23,.08);border-radius:11px;padding:14px 16px\">"
               "<div style=\"font-size:11px;color:#9a9082;letter-spacing:.5px\">KOL</div>"
               "<div style=\"font-family:'Spectral',serif;font-size:18px;font-weight:600;margin-top:3px\">{{ profileSel.branch }}</div></div>")
    joshi_box = ("\n              <div style=\"background:#fff;border:1px solid rgba(33,29,23,.08);border-radius:11px;padding:14px 16px\" "
                 "title=\"Joshi ve ark. 2020 — dijital/NLP kaynak zenginliği sınıfı (0=aşırı düşük … 5=yüksek)\">"
                 "<div style=\"font-size:11px;color:#9a9082;letter-spacing:.5px\">NLP KAYNAK SINIFI</div>"
                 "<div style=\"font-family:'Spectral',serif;font-size:18px;font-weight:600;margin-top:3px\">{{ profileSel.joshi }}</div></div>")
    njbox = 1 if kol_box in html else 0
    html = html.replace(kol_box, kol_box + joshi_box, 1)
    print(f"  Joshi kaynak sınıfı: {njoshi} dil, stat kutusu={njbox}")

    # ============================================================
    #  (b) SES DENKLİKLERİ KANIT-DESTEKLİ — yerleşik kurallar + Savelyev kognat verisinden kanıt sayısı
    # ============================================================
    ev = sound_evidence(cog)
    EVID = {
        "ROTASİZM": "SavelyevTurkic: %d kognat seti bu kuralı doğrular (proto *ŕ → Çuv. r / Ortak Türkçe z)" % ev["rot"][0],
        "LAMBDASİZM": "SavelyevTurkic: %d kognat seti (proto *ĺ → Çuv. l / Ortak Türkçe ş)" % ev["lam"][0],
        "BAŞ Y- > Ś": "SavelyevTurkic: %d Çuvaşça–Türkçe çiftinde (söz başı j-/y- → ś-)" % ev["y"][0],
        "ÜNLÜ İNDİRGEME": "Düzenli ses olayı: vurgusuz ünlüler Çuvaşçada ă / ĕ sesine iner",
    }
    nev = 0
    for name, txt in EVID.items():
        old = "name:'%s'," % name
        if old in html:
            html = html.replace(old, "name:'%s', evidence:'%s'," % (name, txt), 1); nev += 1
    # kanıt satırı markup'ı (kart içinde, isim/cv-ct satırının altında)
    html = html.replace(
        '                  <span style="margin-left:auto;font-family:\'IBM Plex Mono\',monospace;font-size:11px;color:#9a9082;letter-spacing:.5px;text-align:right">{{ s.name }}</span>\n'
        '                </div>',
        '                  <span style="margin-left:auto;font-family:\'IBM Plex Mono\',monospace;font-size:11px;color:#9a9082;letter-spacing:.5px;text-align:right">{{ s.name }}</span>\n'
        '                </div>\n'
        '                <div style="margin-top:9px;font-size:10.5px;font-family:\'IBM Plex Mono\',monospace;color:#8a8073;line-height:1.5;text-align:left">{{ s.evidence }}</div>', 1)
    print(f"  Ses denklikleri kanıt (Savelyev): rot={ev['rot'][0]} lam={ev['lam'][0]} y={ev['y'][0]}, enjekte={nev}/4")
    # (b) kognat→kural bağı: "ses denkliklerinde incele" seçili kognatın örneklediği kuralı VURGULAR
    html = html.replace(
        "      goCompareSound:()=>this.setState({screen:'compare', compareTab:'sound'}),",
        "      goCompareSound:()=>{ const cg=this.COGNATES[this.state.cognateKey]; this.setState({screen:'compare', compareTab:'sound', soundSel:(cg && cg.ruleIdx!=null)?cg.ruleIdx:this.state.soundSel}); },", 1)

    # --- DENETİM DÜZELTMELERİ (görünür taraftaki sabit/eskimiş/tutarsız öğeler) ---
    audit = [
        # paradigma başlığı artık dinamik (herhangi dilde çekim)
        ("PARADİGMA GEZGİNİ · Çuvaşça", "PARADİGMA GEZGİNİ · {{ paradigmLang }}"),
        ("paradigmFreeQ: this.state.paradigmFreeQ||'',",
         "paradigmLang: (this.state.paradigmFree && Array.isArray(this.state.paradigmFree.rows)) ? this.state.paradigmFree.langName : 'Çuvaşça', paradigmFreeQ: this.state.paradigmFreeQ||'',"),
        # öğrenen/uzman KALDIR: her şey görünür (isExpert hep true) + toggle'ı sil
        ("isExpert:S.mode==='expert'", "isExpert: true"),
        # stale konuşur sayısı (timeline) → güncel
        ("Ogur kolunun yaşayan tek temsilcisi; ~1 milyon konuşur, tehlike altında.",
         "Ogur kolunun yaşayan tek temsilcisi; ~740 bin konuşur, tehlike altında."),
    ]
    naudit = 0
    for old, new in audit:
        c = html.count(old)
        if c:
            html = html.replace(old, new); naudit += c
        else:
            print("  ! denetim eşleşmedi:", old[:46])
    print(f"  Denetim düzeltmeleri: {naudit}")

    # ============================================================
    #  Faz 2.2 (yeniden) — EKOSİSTEM SAYFASI (deepsearch 7 + web araştırması)
    #  Ayrı "Ekosistem" sayfası: kategori × dil × DOĞRUDAN bağlantı (launchpad). Nötr; olgunluk yargısı yok.
    # ============================================================
    eco = json.load(open(DATA / "ecosystem.json", encoding="utf-8"))
    def _chip(label, url, note=""):
        ns = f'<span style="color:#9a9082;font-weight:400"> · {note}</span>' if note else ''
        return (f'<a href="{url}" target="_blank" rel="noopener" '
                'style="display:inline-flex;align-items:baseline;gap:6px;text-decoration:none;background:#fbfaf6;'
                'border:1px solid rgba(33,29,23,.12);border-radius:9px;padding:7px 12px;font-size:12.5px;color:#211d17;'
                "font-family:'IBM Plex Sans',sans-serif;line-height:1.35\">"
                f'<span>{label}{ns}</span><span style="color:#b86a2e;font-size:11px;align-self:center">↗</span></a>')
    def _cat_inner(c):
        hubs = "".join(_chip(h["label"], h["url"]) for h in c.get("hubs", []))
        hubrow = (f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px">{hubs}</div>') if hubs else ''
        groups = ""
        for lg in c["langs"]:
            chips = "".join(_chip(l["label"], l["url"], l.get("note", "")) for l in lg["links"])
            groups += (f'<div style="margin-bottom:15px">'
                       f"<div style=\"font-family:'Spectral',serif;font-size:15px;font-weight:600;color:#211d17;margin-bottom:8px\">{lg['name']}</div>"
                       f'<div style="display:flex;flex-wrap:wrap;gap:8px">{chips}</div></div>')
        return (f"<div style=\"font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:1px;color:#d98b4a;margin-bottom:4px\">KATEGORİ</div>"
                f"<h3 style=\"font-family:'Spectral',serif;font-weight:600;font-size:24px;margin:0 0 4px\">{c['title']}</h3>"
                f'<p style="font-size:13px;line-height:1.55;color:#5f574b;max-width:80ch;margin:0 0 14px">{c["desc"]}</p>'
                f'{hubrow}{groups}')
    # SEKMELİ: kategoriye basınca yalnız o kategori açılır (sc-if). Varsayılan: Üretken LLM.
    cat_blocks = ""
    for c in eco["categories"]:
        cat_blocks += ('      <sc-if value="{{ eco_' + c["key"] + ' }}" hint-placeholder-val="{{ false }}">\n'
                       '        <div style="margin-top:16px">' + _cat_inner(c) + '</div>\n'
                       '      </sc-if>\n')
    ECO_SCREEN = (
        '      <sc-if value="{{ isEco }}" hint-placeholder-val="{{ false }}">\n'
        '      <section style="max-width:1080px;margin:0 auto;padding:34px 40px 70px">\n'
        "        <div style=\"font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:1.5px;color:#d98b4a\">EKOSİSTEM</div>\n"
        "        <h2 style=\"font-family:'Spectral',serif;font-weight:600;font-size:38px;margin:8px 0 8px\">Türk dilleri NLP/LLM kaynak merkezi</h2>\n"
        '        <p style="font-size:15px;line-height:1.7;color:#5f574b;max-width:82ch;margin:0 0 8px">' + eco["intro"] + '</p>\n'
        '        <p style="font-size:12px;line-height:1.6;color:#9a9082;max-width:82ch;margin:0 0 16px">' + eco["_meta"]["note"] + '</p>\n'
        '        <div style="position:sticky;top:0;z-index:5;background:#f4f1ea;padding:10px 0 12px;display:flex;flex-wrap:wrap;gap:7px;border-bottom:1px solid rgba(33,29,23,.1)">\n'
        '          <sc-for list="{{ ecoTabs }}" as="t" hint-placeholder-count="8"><button onClick="{{ t.go }}" style="{{ t.style }}">{{ t.title }}</button></sc-for>\n'
        '        </div>\n'
        + cat_blocks +
        '      </section>\n'
        '      </sc-if>\n')
    eco_screen_anchor = "      <!-- ===================== TARİH & KÖKEN ===================== -->"
    neco = 1 if eco_screen_anchor in html else 0
    html = html.replace(eco_screen_anchor, ECO_SCREEN + "\n" + eco_screen_anchor, 1)
    # ECOCATMETA: sekme listesi (component field)
    ecometa = json.dumps([{"key": c["key"], "title": c["title"]} for c in eco["categories"]], ensure_ascii=False)
    html = html.replace("  LANGPROFILE = [", "  ECOCATMETA = " + ecometa + ";\n  LANGPROFILE = [", 1)
    # nav öğesi (ARAŞTIR grubu)
    nnav = 0
    nav_old = ("    {group:'ARAŞTIR', items:[\n"
               "      {id:'research', label:'Araştırmacı Merkezi'},\n"
               "      {id:'sources', label:'Kaynaklar & Lisanslar'},\n"
               "    ]},")
    nav_new = ("    {group:'ARAŞTIR', items:[\n"
               "      {id:'research', label:'Araştırmacı Merkezi'},\n"
               "      {id:'eco', label:'Ekosistem'},\n"
               "      {id:'sources', label:'Kaynaklar & Lisanslar'},\n"
               "    ]},")
    if nav_old in html:
        html = html.replace(nav_old, nav_new, 1); nnav = 1
    # renderVals: isEco + ecoTabs (sekme butonları) + kategori bayrakları (varsayılan llm)
    TAB_ACT = "cursor:pointer;background:#211d17;color:#f4f1ea;border:1px solid #211d17;border-radius:8px;padding:6px 11px;font-size:11.5px;font-family:'IBM Plex Mono',monospace"
    TAB_INACT = "cursor:pointer;background:transparent;color:#5f574b;border:1px solid rgba(33,29,23,.2);border-radius:8px;padding:6px 11px;font-size:11.5px;font-family:'IBM Plex Mono',monospace"
    eco_vals = ("isEco:S.screen==='eco', "
                "ecoTabs:this.ECOCATMETA.map(c=>({title:c.title, go:()=>this.setState({ecoCat:c.key}), "
                "style:((S.ecoCat||'llm')===c.key?\"" + TAB_ACT + "\":\"" + TAB_INACT + "\")})), "
                "eco_llm:(S.ecoCat||'llm')==='llm', eco_encoder:S.ecoCat==='encoder', eco_asr:S.ecoCat==='asr', "
                "eco_tts:S.ecoCat==='tts', eco_data:S.ecoCat==='data', eco_bench:S.ecoCat==='bench', "
                "eco_tools:S.ecoCat==='tools', eco_orgs:S.ecoCat==='orgs',")
    html = html.replace("isResearch:S.screen==='research',", "isResearch:S.screen==='research', " + eco_vals, 1)
    html = html.replace("{mod:'Araştırmacı Merkezi', srcs:['fst','ud','cldf','unimorph']},",
                        "{mod:'Araştırmacı Merkezi', srcs:['fst','ud','cldf','unimorph']},\n    {mod:'Ekosistem', srcs:['hf','deepds','fst']},", 1)
    ncat = len(eco["categories"]); nlink = sum(len(l["links"]) for c in eco["categories"] for l in c["langs"]) + sum(len(c.get("hubs", [])) for c in eco["categories"])
    print(f"  Ekosistem SAYFASI (ds7+web): ekran={neco} nav={nnav} kategori={ncat} bağlantı={nlink}")

    # ============================================================
    #  Faz 1.4 — HAKKINDA & İLETİŞİM sayfası (kullanıcı notu)
    # ============================================================
    REPO = "https://github.com/muhammedkumcu/cuvas-platform"
    _src_items = [
        ("Apertium FST", "morfoloji motoru (analiz/üretim)", "GPL-3.0"),
        ("SavelyevTurkic CLDF", "kognat ağı, çok-boyutlu uzaklık", "CC BY 4.0"),
        ("Glottolog", "sınıflandırma + AES canlılık", "CC BY 4.0"),
        ("WALS", "tipolojik özellikler", "CC BY 4.0"),
        ("Savelyev & Robbeets 2020", "Bayes soy ağacı (Tarih & Köken)", "akademik"),
        ("HuggingFace + derin araştırma", "ekosistem + derin profiller", "derleme"),
    ]
    src_cards = "".join(
        '<div style="background:#fff;border:1px solid rgba(33,29,23,.1);border-radius:11px;padding:13px 15px">'
        f"<div style=\"font-family:'Spectral',serif;font-size:15px;font-weight:600;color:#211d17\">{a}</div>"
        f'<div style="font-size:12.5px;color:#5f574b;margin-top:3px;line-height:1.45">{b}</div>'
        f"<div style=\"font-size:11px;color:#9a9082;margin-top:6px;font-family:'IBM Plex Mono',monospace\">{c}</div></div>"
        for a, b, c in _src_items)
    misyon = "".join(f'<li style="margin-bottom:7px">{x}</li>' for x in [
        'Araştırmacının <b>ilk uğrağı</b>: Türk dil dünyasının açık literatür ve araçlarını tek yerde.',
        'Düşük-kaynaklı / tehlikedeki Türk dillerine <b>dijital kapsayıcılık</b> (çekirdek: Çuvaşça).',
        'Akademik dürüstlük: <b>her veri kaynağına bağlı</b>, uydurma yok; gerçek veriyle değişene kadar işaretli.',
        "Apertium'u yeniden icat etmeden üstüne <b>erişilebilirlik + pedagoji + karşılaştırma</b> katmanı; hatalar yüzeye çıktıkça motora geri katkı.",
    ])
    ABOUT = (
        '      <sc-if value="{{ isAbout }}" hint-placeholder-val="{{ false }}">\n'
        '      <section style="max-width:900px;margin:0 auto;padding:34px 40px 70px">\n'
        "        <div style=\"font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:1.5px;color:#d98b4a\">HAKKINDA & İLETİŞİM</div>\n"
        "        <h2 style=\"font-family:'Spectral',serif;font-weight:600;font-size:38px;margin:8px 0 16px\">KÖKEN nedir?</h2>\n"
        '        <p style="font-size:15.5px;line-height:1.75;color:#3f3a32;max-width:74ch;margin:0 0 14px">KÖKEN, ~20 Türk dili için açık kaynak bir <b>morfoloji + karşılaştırma + araştırma</b> platformudur. Olgun <b>Apertium</b> sonlu-durum dilbilgileri (FST) üzerine; analiz, üretim, paradigma, kognat ağı, ses denklikleri, çok-boyutlu uzaklık, dil profilleri, harita, tarih ve NLP/LLM ekosistemi katmanları ekler. İki kitleye birden hizmet eder: <b>öğrenenler</b> (öğrenci/çocuk) ve <b>araştırmacılar</b>.</p>\n'
        '        <p style="font-size:15.5px;line-height:1.75;color:#3f3a32;max-width:74ch;margin:0 0 24px">Çekirdeği <b>Çuvaşça</b>dır — yaşayan tek Oğur (Bulgar) Türk dili ve tehlikedeki düşük-kaynaklı bir dil. Platformun bir ayağı bu tür dilleri dijital dünyada görünür kılmaktır.</p>\n'
        '        <div style="background:#211d17;color:#f4f1ea;border-radius:18px;padding:26px 30px;margin-bottom:26px">\n'
        "          <h3 style=\"font-family:'Spectral',serif;font-size:22px;font-weight:600;margin:0 0 12px\">Misyon</h3>\n"
        '          <ul style="margin:0;padding-left:20px;font-size:14.5px;line-height:1.6;color:rgba(244,241,234,.9)">' + misyon + '</ul>\n'
        '        </div>\n'
        "        <h3 style=\"font-family:'Spectral',serif;font-size:22px;font-weight:600;margin:0 0 4px\">Veri & motor</h3>\n"
        '        <p style="font-size:13.5px;color:#5f574b;margin:0 0 14px">Her veri doğrudan bir kaynağa dayanır. Tam liste: <b>Kaynaklar &amp; Lisanslar</b> sayfası.</p>\n'
        '        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:26px">' + src_cards + '</div>\n'
        "        <h3 style=\"font-family:'Spectral',serif;font-size:22px;font-weight:600;margin:0 0 10px\">İletişim & katkı</h3>\n"
        '        <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:14px;padding:20px 24px;font-size:14.5px;line-height:1.8;color:#3f3a32">\n'
        '          <div>Geliştirici: <b>Muhammed Kumcu</b> — Marmara Üniversitesi.</div>\n'
        f'          <div>Kaynak kod / katkı (issue · PR): <a href="{REPO}" target="_blank" rel="noopener" style="color:#2f6fb0;text-decoration:none">github.com/muhammedkumcu/cuvas-platform ↗</a></div>\n'
        '          <div>E-posta: <a href="mailto:muhammedkumcu@marun.edu.tr" style="color:#2f6fb0;text-decoration:none">muhammedkumcu@marun.edu.tr</a></div>\n'
        '        </div>\n'
        '        <p style="font-size:12.5px;color:#9a9082;margin:14px 0 0;line-height:1.6">Açık kaynak. Akademik hedef: UBMK/TurkLang ve ötesi. Apertium GPL-3.0 motorunun üstünde, verisi kaynaklı bir erişim/araştırma katmanı.</p>\n'
        '      </section>\n'
        '      </sc-if>\n')
    about_anchor = "      <!-- ===================== KAYNAKLAR & LİSANSLAR ===================== -->"
    nabout = 1 if about_anchor in html else 0
    html = html.replace(about_anchor, ABOUT + "\n" + about_anchor, 1)
    # nav (KEŞFET grubuna Hakkında) + isAbout bayrağı
    html = html.replace(
        "      {id:'history', label:'Tarih & Köken'},\n    ]},\n    {group:'ANALİZ', items:[",
        "      {id:'history', label:'Tarih & Köken'},\n      {id:'about', label:'Hakkında'},\n    ]},\n    {group:'ANALİZ', items:[", 1)
    html = html.replace("isHistory:S.screen==='history',", "isHistory:S.screen==='history', isAbout:S.screen==='about',", 1)
    print(f"  Hakkında sayfası (1.4): ekran={nabout}, kaynak kart={len(_src_items)}")

    # ============================================================
    #  Faz 3.1 — ÇUVAŞÇA "DİLİN KALBİ" anlatı sayfası (çekirdek dil; kullanıcı onaylı ayrı sayfa)
    # ============================================================
    SES = [
        ("dokuz", "тăхăр · tăhăr", "rotasizm *z→r + *q→x"),
        ("kız", "хӗр · hĕr", "*z→r, *q→x"),
        ("kış", "хӗл · hĕl", "lambdasizm *š→l"),
        ("gümüş", "кӗмӗл · kĕmĕl", "*š→l"),
        ("yüz (100)", "ҫӗр · śĕr", "söz başı *y→ś, *z→r"),
        ("yol", "ҫул · śul", "*y→ś"),
        ("kara", "хура · hura", "*q→x"),
        ("öküz", "вăкăр · văkăr", "*z→r"),
    ]
    ses_rows = "".join(
        '<tr>'
        f"<td style=\"padding:8px 12px;border-top:1px solid rgba(33,29,23,.07);font-family:'Spectral',serif;font-size:15px;color:#5f574b\">{a}</td>"
        f"<td style=\"padding:8px 12px;border-top:1px solid rgba(33,29,23,.07);font-family:'Spectral',serif;font-size:16px;font-weight:600;color:#b86a2e\">{b}</td>"
        f"<td style=\"padding:8px 12px;border-top:1px solid rgba(33,29,23,.07);font-family:'IBM Plex Mono',monospace;font-size:11px;color:#9a9082\">{c}</td>"
        '</tr>' for a, b, c in SES)
    OZG = [
        ("Tersine morfotaktik", "Ekler Kök + <b>İyelik</b> + <b>Çoğul</b> + Hâl sırasıyla dizilir — diğer tüm Türk dilleri Kök+Çoğul+İyelik+Hâl kullanır. Örn. <i>хӗр-ӗм-сен-чен</i> 'kızlarımdan'."),
        ("-сем / -сам çoğulu", "Ana Türkçe -lAr yerine kökeni belirsiz, Ana Türkçe'ye dayandırılamayan <b>-сем/-сам</b> eki (Mari diliyle temas izi)."),
        ("Yönelme-Belirtme birleşmesi", "Türk dillerinde ayrı işaretlenen yönelme (dative) ve belirtme (accusative) Çuvaşçada <b>tek ekte</b> kaynaşır (-(н)А)."),
        ("İndirgenmiş ünlüler", "Kiril'e özel eklenen <b>ă (Ӑ)</b> ve <b>ĕ (Ӗ)</b> ultra-kısa ünlüleri + ünlü kalitesine göre yer değiştiren sıra dışı vurgu."),
    ]
    ozg_cards = "".join(
        '<div style="background:#fff;border:1px solid rgba(33,29,23,.1);border-left:4px solid #b8602e;border-radius:12px;padding:16px 18px">'
        f"<div style=\"font-family:'Spectral',serif;font-size:16px;font-weight:700;color:#211d17;margin-bottom:6px\">{t}</div>"
        f'<div style="font-size:13px;line-height:1.6;color:#5f574b">{b}</div></div>' for t, b in OZG)
    TARIH = [
        ("13–14. yy", "İdil Bulgar mezar yazıtları", "Volga Bulgarcasının r/l-Türkçesi (Oğur) izlerini taşıyan Arap harfli taş yazıtlar — Çuvaşçanın doğrudan tarihsel tanığı."),
        ("1863", "Feyzhanov · 'Çuvaş anahtarı'", "Hüseyin Feyzhanov, Bulgar kitabelerindeki tarih/sayıların Çuvaşça fonolojiyle (rotasizm/lambdasizm) yazıldığını gösterip İdil Bulgarcasının bir Oğur dili olduğunu kanıtladı."),
        ("1928–1950", "Aşmarin · 17 ciltlik Sözlük", "N. İ. Aşmarin'in 'Thesaurus Linguae Tschuvaschorum'u — şamanik dualar, halk şarkıları, arkaik sözcüklerle devasa kültürel ansiklopedi; düşük-kaynaklı bir dil için olağanüstü temel."),
    ]
    tarih_rows = "".join(
        '<div style="position:relative;padding-left:30px;padding-bottom:20px">'
        '<span style="position:absolute;left:4px;top:4px;width:12px;height:12px;border-radius:50%;background:#b8602e;border:2px solid #f4f1ea"></span>'
        f"<div style=\"font-family:'IBM Plex Mono',monospace;font-size:12px;color:#d98b4a\">{e}</div>"
        f"<div style=\"font-family:'Spectral',serif;font-size:17px;font-weight:600;margin:2px 0 3px\">{t}</div>"
        f'<div style="font-size:13.5px;line-height:1.55;color:#5f574b;max-width:64ch">{d}</div></div>' for e, t, d in TARIH)
    HEART = (
        '      <sc-if value="{{ isHeart }}" hint-placeholder-val="{{ false }}">\n'
        '      <section style="max-width:920px;margin:0 auto;padding:34px 40px 70px">\n'
        # hero
        '        <div style="background:#211d17;color:#f4f1ea;border-radius:22px;padding:34px 36px;margin-bottom:30px">\n'
        "          <div style=\"font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:2px;color:#e9a978\">ÇEKİRDEK DİL</div>\n"
        "          <h2 style=\"font-family:'Spectral',serif;font-weight:600;font-size:42px;margin:10px 0 6px\">Çuvaşça — Dilin Kalbi</h2>\n"
        '          <p style="font-size:16px;line-height:1.7;color:rgba(244,241,234,.85);max-width:64ch;margin:0">Yaşayan tek <b>Oğur (Bulgar)</b> Türk dili. Türk dil ailesinden binlerce yıl önce ilk ayrılan kolun son temsilcisi — ve bu yüzden Ana Türkçenin yeniden kurulduğu paha biçilmez bir laboratuvar.</p>\n'
        '          <div style="display:flex;gap:26px;flex-wrap:wrap;margin-top:20px">\n'
        "            <div><div style=\"font-family:'Spectral',serif;font-size:24px;font-weight:700\">~740 bin</div><div style=\"font-size:11px;color:rgba(244,241,234,.55);font-family:'IBM Plex Mono',monospace\">KONUŞUR (2020)</div></div>\n"
        "            <div><div style=\"font-family:'Spectral',serif;font-size:24px;font-weight:700\">Oğur</div><div style=\"font-size:11px;color:rgba(244,241,234,.55);font-family:'IBM Plex Mono',monospace\">KOL (tek üye)</div></div>\n"
        "            <div><div style=\"font-family:'Spectral',serif;font-size:24px;font-weight:700\">EGIDS 6b</div><div style=\"font-size:11px;color:rgba(244,241,234,.55);font-family:'IBM Plex Mono',monospace\">TEHLİKEDE</div></div>\n"
        '          </div>\n'
        '        </div>\n'
        # neden paha biçilmez
        "        <h3 style=\"font-family:'Spectral',serif;font-size:24px;font-weight:600;margin:0 0 10px\">Neden paha biçilmez?</h3>\n"
        '        <p style="font-size:15px;line-height:1.75;color:#3f3a32;max-width:74ch;margin:0 0 28px">Çuvaşça, Ortak (Şaz) Türkçeden çok erken ayrıldığı için karşılıklı anlaşılabilirliği sıfıra yakındır. Ama tam da bu uzaklık onu değerli kılar: düzenli ses denklikleri (rotasizm, lambdasizm), Ana Türkçe ve hatta Transavrasya rekonstrüksiyonlarında bir <b>anahtar dil</b> yapar. İdil-Ural havzasında Fin-Ugor (Mari) ve Rusça ile yüzyıllarca temas, ona benzersiz areal özellikler kazandırmıştır.</p>\n'
        # ses kanunları
        "        <h3 style=\"font-family:'Spectral',serif;font-size:24px;font-weight:600;margin:0 0 6px\">Ses kanunları</h3>\n"
        '        <p style="font-size:13.5px;line-height:1.6;color:#5f574b;max-width:74ch;margin:0 0 14px">Ortak Türkçedeki bir ses, Çuvaşçada düzenli olarak başka bir sese karşılık gelir. Bu kurallar Savelyev kognat verimizde kanıtlıdır: <b>36</b> rotasizm (*z→r), <b>29</b> lambdasizm (*š→l), <b>14</b> söz başı *y→ś çifti.</p>\n'
        '        <div style="border:1px solid rgba(33,29,23,.1);border-radius:14px;overflow:hidden;margin-bottom:30px">\n'
        '          <table style="border-collapse:collapse;width:100%">\n'
        "            <thead><tr style=\"background:#fbfaf6\"><th style=\"text-align:left;padding:9px 12px;font-size:11px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.5px\">ORTAK TÜRKÇE</th><th style=\"text-align:left;padding:9px 12px;font-size:11px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.5px\">ÇUVAŞÇA</th><th style=\"text-align:left;padding:9px 12px;font-size:11px;font-family:'IBM Plex Mono',monospace;color:#9a9082;letter-spacing:.5px\">KURAL</th></tr></thead>\n"
        '            <tbody>' + ses_rows + '</tbody>\n'
        '          </table>\n'
        '        </div>\n'
        # yapı özgünlüğü
        "        <h3 style=\"font-family:'Spectral',serif;font-size:24px;font-weight:600;margin:0 0 14px\">Yapının özgünlüğü</h3>\n"
        '        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-bottom:30px">' + ozg_cards + '</div>\n'
        # tarih
        "        <h3 style=\"font-family:'Spectral',serif;font-size:24px;font-weight:600;margin:0 0 16px\">Tarihsel tanıklar</h3>\n"
        '        <div style="position:relative;padding-left:6px;margin-bottom:30px"><div style="position:absolute;left:9px;top:6px;bottom:14px;width:2px;background:rgba(33,29,23,.12)"></div>' + tarih_rows + '</div>\n'
        # bugün
        '        <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:16px;padding:24px 28px;margin-bottom:28px">\n'
        "          <h3 style=\"font-family:'Spectral',serif;font-size:22px;font-weight:600;margin:0 0 10px\">Bugün — ve dijital uçurum</h3>\n"
        '          <p style="font-size:14.5px;line-height:1.7;color:#3f3a32;max-width:74ch;margin:0 0 8px">Konuşur sayısı on yılda ~1,04 milyondan <b>740 bine</b> düştü (≈%30 kayıp); kentlerde aktarım Rusçaya kayıyor. Dijital dünyada da geride: Joshi <b>Sınıf 1</b>; Meta\'nın 1.107 dilik dev TTS projesinde bile Çuvaşça <b>yok</b> (yalnız eSpeak NG), konuşma tanımada hata oranı ~%60.</p>\n'
        '          <p style="font-size:13.5px;line-height:1.65;color:#5f574b;max-width:74ch;margin:0">KÖKEN\'in çekirdeği Çuvaşça olması tesadüf değil: bu platformun bir amacı, böyle paha biçilmez ama tehlikedeki bir dili dijital dünyada görünür kılmaktır.</p>\n'
        '        </div>\n'
        # CTA
        "        <div style=\"font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:1px;color:#9a9082;margin-bottom:10px\">ÇUVAŞÇAYI KEŞFET</div>\n"
        '        <div style="display:flex;flex-wrap:wrap;gap:10px">\n'
        '          <button onClick="{{ heartLearn }}" style="cursor:pointer;background:#b8602e;color:#fff;border:none;border-radius:10px;padding:11px 18px;font-size:14px;font-family:\'Spectral\',serif;font-weight:600">Çuvaşça Atölyesi →</button>\n'
        '          <button onClick="{{ heartProfile }}" style="cursor:pointer;background:#fff;color:#211d17;border:1px solid rgba(33,29,23,.18);border-radius:10px;padding:11px 18px;font-size:14px;font-family:\'Spectral\',serif;font-weight:600">Dil profili →</button>\n'
        '          <button onClick="{{ heartCognate }}" style="cursor:pointer;background:#fff;color:#211d17;border:1px solid rgba(33,29,23,.18);border-radius:10px;padding:11px 18px;font-size:14px;font-family:\'Spectral\',serif;font-weight:600">Kognat ağı →</button>\n'
        '          <button onClick="{{ heartCompare }}" style="cursor:pointer;background:#fff;color:#211d17;border:1px solid rgba(33,29,23,.18);border-radius:10px;padding:11px 18px;font-size:14px;font-family:\'Spectral\',serif;font-weight:600">Ses denklikleri →</button>\n'
        '        </div>\n'
        '      </section>\n'
        '      </sc-if>\n')
    heart_anchor = "      <!-- ===================== KAYNAKLAR & LİSANSLAR ===================== -->"
    nheart = 1 if heart_anchor in html else 0
    html = html.replace(heart_anchor, HEART + "\n" + heart_anchor, 1)
    # nav (KEŞFET'e Çuvaşça Kalbi, Tarih & Köken'den sonra) + isHeart + CTA handler'ları
    html = html.replace(
        "      {id:'history', label:'Tarih & Köken'},\n      {id:'about', label:'Hakkında'},",
        "      {id:'history', label:'Tarih & Köken'},\n      {id:'heart', label:'Çuvaşça Kalbi'},\n      {id:'about', label:'Hakkında'},", 1)
    html = html.replace(
        "isAbout:S.screen==='about',",
        "isAbout:S.screen==='about', isHeart:S.screen==='heart', heartLearn:this.go('learn'), heartProfile:()=>this.setState({screen:'profile',profileSel:'chv'}), heartCognate:this.go('cognate'), heartCompare:this.go('compare'),", 1)
    print(f"  Çuvaşça Dilin Kalbi (3.1): ekran={nheart}, ses={len(SES)} özg={len(OZG)} tarih={len(TARIH)}")

    (DIST / "index.html").write_text(html, encoding="utf-8")
    shutil.copy(UI / "support.js", DIST / "support.js")

    print(f"dist/index.html yazıldı.")
    print(f"  LANGPROFILE canlılık (Glottolog AES): {len(changed)} dil")
    print(f"  MAP harita koordinatları (Glottolog): {nmap} blok, {new_map.count('{name')} dil")
    print(f"  Uzaklık matrisleri (Savelyev+WALS+coğrafi): val patch={ndist}, REAL_DIST enjekte")
    print(f"  Kognat Ağı (SavelyevTurkic): {ncog} blok, {len(cog_obj)} kavram (default '{cog_default}')")
    print(f"  A1 kognat kelime-seçici (kategorili+aranabilir): {na1}/3 yama")
    print(f"  A3 landing kapsam (veriden: {n_live}/{n_prof}/{n_geo} dil, {n_branch} kol) + footer + kart: {na3}/3 yama")
    print(f"  A5 Uzaklık radar kutusu kompakt + OKUMA sağ sütuna (denge): {na5}/3 yama")
    print(f"  Kopya düzeltmeleri: {nfix}")
    print(f"  Dil profili zenginleştirme (Wikipedia, çapraz-kontrollü): {nenrich} alan ({len(extra)} dil)")
    print(f"  Canlı API bağlama (Paradigma+Analiz): {nlive}/6 yama")


if __name__ == "__main__":
    main()
