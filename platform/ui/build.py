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
# Uzaklık Gezgini — Savelyev leksikal/filogenetik matrisi 32 dil; hepsi açılır (10→32 yatay ölçek).
# (ui_code, Savelyev adı, iso[None=master'da yok→geo eksik], TR ad-yedek, kol)
DIST_ROWS = [
    ("chv", "Chuvash", "chv", "Çuvaşça", "Ogur"), ("tt", "Tatar", "tat", "Tatarca", "Kıpçak"),
    ("bak", "Bashkir", "bak", "Başkurtça", "Kıpçak"), ("kk", "Kazakh", "kaz", "Kazakça", "Kıpçak"),
    ("kg", "Kirghiz", "kir", "Kırgızca", "Kıpçak"), ("tr", "Turkish", "tur", "Türkçe", "Oğuz"),
    ("az", "Azeri", "azj", "Azerbaycanca", "Oğuz"), ("tk", "Turkmen", "tuk", "Türkmence", "Oğuz"),
    ("ug", "Uighur", "uig", "Uygurca", "Karluk"), ("sah", "Yakut", "sah", "Yakutça", "Sibirya"),
    ("uzn", "Uzbek", "uzn", "Özbekçe", "Karluk"), ("gag", "Gagauz", "gag", "Gagavuzca", "Oğuz"),
    ("crh", "CrimeanTatar", "crh", "Kırım Tatarcası", "Oğuz"), ("kaa", "KaraKalpak", "kaa", "Karakalpakça", "Kıpçak"),
    ("krc", "KarachayBalkar", "krc", "Karaçay-Balkarca", "Kıpçak"), ("kum", "Kumyk", "kum", "Kumukça", "Kıpçak"),
    ("nog", "Nogai", "nog", "Nogayca", "Kıpçak"), ("kdr", "Karaim", "kdr", "Karayca", "Kıpçak"),
    ("klj", "Khalaj", "klj", "Halaçça", "Argu"), ("alt", "SouthAltai", "alt", "Altayca (Güney)", "Sibirya"),
    ("atv", "NorthAltai", "atv", "Altayca (Kuzey)", "Sibirya"), ("kjh", "Khakas", "kjh", "Hakasça", "Sibirya"),
    ("cjs", "Shor", "cjs", "Şorca", "Sibirya"), ("tyv", "Tuvan", "tyv", "Tuvaca", "Sibirya"),
    ("dlg", "Dolgan", "dlg", "Dolganca", "Sibirya"), ("kim", "Tofa", "kim", "Tofaca", "Sibirya"),
    ("culw", "MiddleChulym", "clw", "Çulımca", "Sibirya"), ("slr", "Salar", "slr", "Salarca", "Oğuz"),
    ("ybe", "SarygYugur", "ybe", "Sarı Uygurca", "Sibirya"), ("oui", "OldUyghur", "oui", "Eski Uygurca", "Karluk"),
    ("qwm", "CodexCumanicus", "qwm", "Codex Cumanicus", "Kıpçak"), ("baraba", "Baraba", None, "Baraba Tatarcası", "Kıpçak"),
]
DIST_LEX = {r[0]: r[1] for r in DIST_ROWS}
DIST_ISO = {r[0]: (r[2] or "") for r in DIST_ROWS}


def haversine(a, b):
    from math import radians, sin, cos, asin, sqrt
    la1, lo1, la2, lo2 = map(radians, [a[0], a[1], b[0], b[1]])
    h = sin((la2 - la1) / 2) ** 2 + cos(la1) * cos(la2) * sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * asin(sqrt(h))


def build_distance(mcoord, lex, typ, cog, intel):
    codes = list(DIST_LEX)
    coords = {c: mcoord[DIST_ISO[c]] for c in codes if DIST_ISO.get(c) and DIST_ISO[c] in mcoord}
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


def build_cognates_deep(cogdeep):
    """ds18 → COGNATES (Kognat Ağı). 11 kavram × 18 dil; her düğüm: latin biçim + kol + ses kuralı +
    yerel yazı + IPA + morfem + cogid. Boşluk (gap) = cogid baskın-cogid'den farklı (leksikal yenilik/alıntı).
    ruleIdx → Ses denklikleri sekmesine bağlantı (proto-fonem tabanlı: *ŕ=rotasizm, *ĺ=lambdasizm)."""
    from collections import Counter
    out, first = {}, None
    for c in cogdeep["concepts"]:
        cells = c["cells"]
        dom = Counter(cl["cogid"] for cl in cells).most_common(1)[0][0]
        nodes, gaps = [], []
        for cl in cells:
            shift = cl["cogid"] != dom
            nodes.append({"lang": cl["lang"], "word": cl["latin"], "branch": cl["branch"],
                          "shift": shift, "native": cl["native"], "rule": cl["rule"],
                          "ipa": cl["ipa"], "morph": cl["morph"], "cogid": cl["cogid"]})
            if shift:
                gaps.append(cl["lang"])
        proto = c["proto"]
        ridx = 0 if "ŕ" in proto else (1 if "ĺ" in proto else None)
        cid = c.get("concepticon")
        note = (f"Proto-Türkçe kök {proto}" + (f" · Concepticon {cid}." if cid else ".") + " " + c["note"]
                + (f" Boşluk (kognat seti farklı): {', '.join(gaps)}." if gaps else
                   " Tüm dillerde aynı kognat seti — boşluk yok."))
        out[c["key"]] = {"gloss": c["gloss"], "gloss_en": c.get("gloss_en", ""), "proto": proto,
                         "note": note, "nodes": nodes, "cat": c["cat"], "ruleIdx": ridx,
                         "concepticon": cid}
        if first is None:
            first = c["key"]
    return out, first


# ds17 — Türk dilleri kol-seviyesi ses izoglossları (faithful; Savelyev/Johanson/Tekin atıflı).
# 4 Çuvaş-merkezli kuraldan → 7 kol-izoglosuna (Çuvaş-ötesi, çok-kollu refleksler). İlk iki kart
# (rotasizm=0, lambdasizm=1) kognat goCompareSound bağlantısıyla uyumlu kalır.
def build_sound_laws(ev=None):
    # rot/lam/y kanıt sayıları Savelyev verisinden (sound_evidence) — veriden, hardcode değil; ds17'de de doğrulanır.
    rot_n = ev["rot"][0] if ev else 36
    lam_n = ev["lam"][0] if ev else 29
    y_n = ev["y"][0] if ev else 14
    return [
        {"key": "rot", "proto": "*ŕ", "name": "Rotasizm", "evid": f"Savelyev: {rot_n} kognat",
         "desc": "Oğur ↔ Şaz makro-ayrımı — Türk dili tarihindeki en birincil izogloss.",
         "reflexes": [
             {"branch": "Çuvaşça (Oğur)", "val": "r", "ex": "тăхăр · хӗр · ҫӗр"},
             {"branch": "Ortak Türkçe (Şaz)", "val": "z", "ex": "dokuz · kız · yüz"}]},
        {"key": "lam", "proto": "*ĺ", "name": "Lambdasizm", "evid": f"Savelyev: {lam_n} kognat",
         "desc": "Rotasizmle paralel ikinci makro-izogloss (palatalize yanal *ĺ).",
         "reflexes": [
             {"branch": "Çuvaşça (Oğur)", "val": "l", "ex": "хӗл · чул · кӗмӗл"},
             {"branch": "Ortak Türkçe", "val": "ş", "ex": "kış · taş · gümüş"},
             {"branch": "Kıpçak · Sibirya", "val": "s", "ex": "qıs · tas (alt-refleks)"}]},
        {"key": "h", "proto": "*h-", "name": "Söz başı *h- korunumu",
         "desc": "Argu (Halaçça) izolesini ayırır — Orhun'dan dahi eskicil katman (Doerfer).",
         "reflexes": [
             {"branch": "Halaçça (Argu)", "val": "h-", "ex": "hadaq · hirkäk · huzun"},
             {"branch": "Diğer tüm kollar", "val": "Ø", "ex": "ayak · erkek · uzun"}]},
        {"key": "d", "proto": "*-d-", "name": "Söz içi *-d- farklılaşması",
         "desc": "Genel Türkçe iç tasnifin turnusol kâğıdı (*adak 'ayak').",
         "reflexes": [
             {"branch": "Oğuz · Kıpçak · Karluk", "val": "y", "ex": "ayak / oyoq"},
             {"branch": "Tuva · Halaç", "val": "d", "ex": "adaq / hadaq"},
             {"branch": "Yakutça", "val": "t", "ex": "atax"},
             {"branch": "Hakas · Şor", "val": "z", "ex": "azaq"},
             {"branch": "Çuvaşça", "val": "r", "ex": "ura"}]},
        {"key": "g", "proto": "*-G", "name": "Son ses *-G",
         "desc": "Hece-sonu damak ünsüzü — hece yapısını belirleyen kol ayrımı (*tāg 'dağ').",
         "reflexes": [
             {"branch": "Oğuz", "val": "ː / ğ", "ex": "dağ /dɑː/"},
             {"branch": "Kıpçak", "val": "w", "ex": "taw · suw"},
             {"branch": "Karluk", "val": "g / ğ", "ex": "tog'"},
             {"branch": "Yakutça", "val": "Ø / diftong", "ex": "tıa · haya"}]},
        {"key": "y", "proto": "*y-", "name": "Söz başı *y-", "evid": f"Savelyev: {y_n} kognat (ś)",
         "desc": "y / c / j / ś / s — makro-grupları ayıran geniş ve kurallı yelpaze.",
         "reflexes": [
             {"branch": "Oğuz · Karluk", "val": "y", "ex": "yol · yıl"},
             {"branch": "Kıpçak", "val": "j / c", "ex": "jol · col"},
             {"branch": "Yakutça", "val": "s", "ex": "suol · sıl"},
             {"branch": "Çuvaşça (Oğur)", "val": "ś", "ex": "ҫул (śul)"}]},
        {"key": "voi", "proto": "*t- · *k-", "name": "Baş ses tonlulaşması",
         "desc": "Oğuz kolunu Kıpçak/Karluk/Sibirya'dan ayıran sistematik ötümlüleşme.",
         "reflexes": [
             {"branch": "Oğuz", "val": "d- / g-", "ex": "dağ · gök · gümüş"},
             {"branch": "Kıpçak · Karluk · Sibirya", "val": "t- / k-", "ex": "taw · kök · kümüş"}]},
    ]


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


def _spk_rank(label):
    """'~85 milyon' / '~740 bin' → sayısal sıralama anahtarı (önem)."""
    m = re.search(r"([\d,.]+)\s*(milyon|bin)?", label or "")
    if not m:
        return 0.0
    try:
        v = float(m.group(1).replace(".", "").replace(",", "."))
    except ValueError:
        return 0.0
    u = m.group(2)
    return v * 1e6 if u == "milyon" else (v * 1e3 if u == "bin" else v)


def build_map(master):
    # B3 — TÜM diller (master); B4/ATLAS-zoom — ZOOM-KADEMELİ etiket eşiği (lz): her zoom seviyesinde
    # açgözlü yerleşim (kutu/offset ~1/z, etiketler ekran-sabit). lz = etiketin göründüğü EN KÜÇÜK zoom.
    # Atlas yakınlaştıkça noktalar ayrılır → daha çok etiket çakışmadan açılır. era stili + boyut.
    langs = [L for L in master if L.get("lat") is not None and L.get("lon") is not None]
    langs.sort(key=lambda L: ({"living": 2}.get(L["era"], 1),
                              1e9 if L["iso"] == "chv" else _spk_rank(L.get("speakers", ""))), reverse=True)
    pos = {L["iso"]: project(L["lon"], L["lat"]) for L in langs}
    Z_LEVELS = [1.0, 1.5, 2.0, 2.6, 3.4]
    label_at = {L["iso"]: (0, 0) for L in langs}   # iso → (lz, ldir); lz=0 → en yüksek zoomda bile sığmadı
    for z in Z_LEVELS:
        placed = []
        for L in langs:
            iso = L["iso"]; x, y = pos[iso]
            # z=1'de SEYREK overview (büyük kutu → yalnız önemli diller), yakınlaştıkça (kutu ~1/z) açılır
            hw, hh = (0.9 + 0.52 * len(L["name"])) / z, 3.2 / z
            for cand, off in ((1, 3.0 / z), (2, -3.0 / z)):       # 1=alt, 2=üst
                cy = y + off
                if cy - hh < 1 or cy + hh > 99:
                    continue
                if all(not (abs(x - px) < (hw + phw) and abs(cy - py) < (hh + phh)) for px, py, phw, phh in placed):
                    placed.append((x, cy, hw, hh))
                    if label_at[iso][0] == 0:
                        label_at[iso] = (z, cand)
                    break
    rows = []
    for L in langs:
        iso = L["iso"]; x, y = pos[iso]
        lz, ldir = label_at[iso]
        rank = _spk_rank(L.get("speakers", ""))
        sz = 3 if (L["era"] == "living" and rank >= 1e6) else (2 if L["era"] == "living" else 1)
        parts = [f"name:{json.dumps(L['name'], ensure_ascii=False)}", f"code:{json.dumps(iso)}",
                 f"branch:{json.dumps(L['branch'], ensure_ascii=False)}", f"x:{x}", f"y:{y}",
                 f"speakers:{json.dumps(L.get('speakers',''), ensure_ascii=False)}",
                 f"note:{json.dumps(L.get('note',''), ensure_ascii=False)}",
                 f"vit:{json.dumps(L.get('vitality',''), ensure_ascii=False)}",
                 f"era:{json.dumps(L['era'])}", f"lz:{lz}", f"ldir:{ldir}", f"sz:{sz}"]
        if iso == "chv":
            parts.append("hi:true")
        rows.append("    {" + ", ".join(parts) + "},")
    return "MAP = [\n" + "\n".join(rows) + "\n  ];"


# B2 — GERÇEK çizim harita: dotlarla AYNI projeksiyonda (viewBox 0..100), gerçek lat/lon'dan
# çizilmiş tanınabilir Avrasya: su tabanı + kara poligonu (Akdeniz/Arabistan/Hindistan kıyıları +
# doğu Pasifik kıyısı) + iç denizler + Basra Körfezi + önemli dağ sıraları. "Çizim ama gerçek."
# Ölçek: 1° boylam ≈ 0.7517 x-birim, 1° enlem ≈ 1.6949 y-birim (project() ile birebir).
def _pj(lon, lat):
    return (round(0.7517 * lon - 14.71, 2), round(-1.6949 * lat + 118.58, 2))


def build_map_bg():
    # Doğu (Pasifik) kıyısı NE→SE, sonra güney kıyısı SE→W (Hindistan + Arabistan çıkıntıları)
    EAST = [(148, 60), (145, 54), (141, 50), (137, 47), (132, 44), (128, 41), (125, 38),
            (122, 34), (120, 30), (116, 25), (112, 21), (108, 17), (106, 14)]
    SOUTH = [(103, 13), (99, 14), (95, 17), (91, 21), (88, 22), (85, 18), (82, 14), (79, 9),
             (76, 9), (73, 15), (70, 20), (66, 24), (62, 25), (58, 25), (55, 26), (58, 23),
             (59, 21), (55, 16), (51, 13), (47, 13), (44, 14), (41, 18), (39, 23), (37, 28),
             (36, 32), (37, 36), (33, 36), (29, 36.5), (25, 37), (22, 38.5), (20, 41)]
    seg = lambda pts: "".join(f"L {_pj(lo,la)[0]} {_pj(lo,la)[1]} " for lo, la in pts)
    land = (f"M -5 -5 L 105 -5 L 105 {_pj(148,60)[1]} " + seg(EAST) + seg(SOUTH)
            + f"L -5 {_pj(20,41)[1]} L -5 -5 Z")
    # iç denizler/göller: (boylam, enlem, boylam_açıklık°, enlem_açıklık°)
    # +İstanbul Boğazı (su), +Ege/Akdeniz, +Kızıldeniz (güneydeki kanal/deniz) — kullanıcı isteği
    seas = [(34.5, 43.2, 13.0, 4.6), (50.5, 41.7, 7.0, 10.6), (59.5, 45.0, 3.2, 2.8),
            (76.0, 45.7, 6.6, 1.4), (107.0, 53.6, 2.2, 4.4), (51.0, 28.7, 6.5, 3.0),
            (28.9, 41.0, 1.8, 3.0), (25.0, 37.8, 5.6, 5.2), (36.5, 22.0, 2.6, 15.0)]
    sea_svg = []
    for lon, lat, ws, hs in seas:
        cx, cy = _pj(lon, lat)
        rx, ry = round(ws / 2 * 0.7517, 2), round(hs / 2 * 1.6949, 2)
        sea_svg.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#mSea)" '
                       f'stroke="#a6bdbf" stroke-width="0.7" vector-effect="non-scaling-stroke"/>')
    # adalar (kara, suyun üstüne çizilir): Kıbrıs
    islands = [(33.4, 35.0, 2.4, 1.3)]
    isl_svg = []
    for lon, lat, ws, hs in islands:
        cx, cy = _pj(lon, lat)
        rx, ry = round(ws / 2 * 0.7517, 2), round(hs / 2 * 1.6949, 2)
        isl_svg.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#mLand)" '
                       f'stroke="#c2b393" stroke-width="0.6" vector-effect="non-scaling-stroke"/>')
    # önemli dağ sıraları (gerçek konum): (boylam1,enlem1, boylam2,enlem2, tepe-sayısı)
    ranges = [(40, 43.5, 48, 42, 3), (59, 52, 60.5, 61, 4), (72, 42, 84, 42.5, 5),
              (85, 49, 92, 51, 3), (67, 37, 75, 38, 3), (80, 35.5, 94, 36, 4)]
    peaks = []
    for lo1, la1, lo2, la2, n in ranges:
        x1, y1 = _pj(lo1, la1); x2, y2 = _pj(lo2, la2)
        for i in range(n):
            t = (i + 0.5) / n
            cx = x1 + (x2 - x1) * t; cy = y1 + (y2 - y1) * t
            peaks.append(f"M {cx-0.9:.1f} {cy+0.4:.1f} L {cx:.1f} {cy-1.5:.1f} L {cx+0.9:.1f} {cy+0.4:.1f}")
    # büyük nehirler (yer şekilleri): İdil/Volga, Amu Derya, Sir Derya — ince mavi polilinler
    rivers = [[(57, 57), (53, 55.5), (49, 53), (47.5, 50), (47, 47)],   # İdil (Volga) → Hazar
              [(73, 38), (68, 38.5), (64, 40), (61, 42), (59.8, 43.5)],  # Amu Derya → Aral
              [(71, 41), (67, 43), (64, 44.5), (62, 45.5)]]              # Sir Derya → Aral
    riv_svg = []
    for pts in rivers:
        d = "M " + " L ".join(f"{_pj(lo,la)[0]} {_pj(lo,la)[1]}" for lo, la in pts)
        riv_svg.append(f'<path d="{d}" fill="none" stroke="#9fb9c2" stroke-width="0.7" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke" opacity="0.7"/>')
    grat = []
    for lon in (40, 60, 80, 100, 120):
        x, _ = _pj(lon, 45); grat.append(f'<line x1="{x}" y1="0" x2="{x}" y2="100"/>')
    for lat in (30, 40, 50, 60):
        _, y = _pj(70, lat); grat.append(f'<line x1="0" y1="{y}" x2="100" y2="{y}"/>')
    return ('<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">'
            '<defs>'
            '<linearGradient id="mLand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ece4d3"></stop><stop offset="1" stop-color="#e0d7c2"></stop></linearGradient>'
            '<linearGradient id="mSea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cbd8d9"></stop><stop offset="1" stop-color="#b9c9ca"></stop></linearGradient>'
            '</defs>'
            '<rect x="0" y="0" width="100" height="100" fill="url(#mSea)"></rect>'
            f'<path d="{land}" fill="url(#mLand)" stroke="#c2b393" stroke-width="0.6" vector-effect="non-scaling-stroke"></path>'
            + '<g stroke="rgba(33,29,23,.07)" stroke-width="0.5" vector-effect="non-scaling-stroke">' + "".join(grat) + '</g>'
            + "".join(riv_svg)
            + "".join(sea_svg)
            + "".join(isl_svg)
            + f'<path d="{" ".join(peaks)}" fill="none" stroke="#b7a378" stroke-width="0.7" stroke-linejoin="round" vector-effect="non-scaling-stroke" opacity="0.85"></path>'
            + '</svg>')


# Atlas (büyük harita) için zengin coğrafya etiketleri — HTML span'leri (projeksiyon %'sinde konum).
# Denizler/dağlar/nehirler/boğaz + bölgeler; "İstanbul Boğazı ve bilinen yer şekilleri" (kullanıcı).
def atlas_feature_labels():
    seas = [(34, 43, "Karadeniz"), (51.5, 39, "Hazar Denizi"), (59.5, 45.6, "Aral G."),
            (27, 33.5, "Akdeniz"), (74, 46.3, "Balkaş G."), (108, 53.5, "Baykal G."), (77, 42.6, "Issık G.")]
    mts = [(45.5, 43.3, "Kafkaslar"), (80, 41.5, "Tien Şan"), (89, 50, "Altay Dağları"),
           (60, 57.5, "Ural Dağları"), (72.5, 37.5, "Pamir")]
    rivers = [(50, 51.5, "İdil"), (63, 41, "Amu Derya")]
    marks = [(28.8, 41.2, "İstanbul Boğazı")]
    regions = [(33, 38.5, "ANADOLU"), (52, 56, "İDİL-URAL"), (69, 44.5, "TURAN"), (96, 60, "SİBİRYA")]
    out = []
    sty = ("position:absolute;transform:translate(-50%,-50%);pointer-events:none;white-space:nowrap;"
           "font-family:'Spectral',serif;letter-spacing:.2px")
    for lo, la, nm in seas:
        x, y = _pj(lo, la)
        out.append(f'<span style="{sty};left:{x}%;top:{y}%;font-style:italic;font-size:11px;color:#6f8e9b">{nm}</span>')
    for lo, la, nm in rivers:
        x, y = _pj(lo, la)
        out.append(f'<span style="{sty};left:{x}%;top:{y}%;font-style:italic;font-size:10px;color:#8aa6b0">{nm}</span>')
    for lo, la, nm in mts:
        x, y = _pj(lo, la)
        out.append(f'<span style="{sty};left:{x}%;top:{y}%;font-size:10.5px;color:#9a7d4e">▲ {nm}</span>')
    for lo, la, nm in marks:
        x, y = _pj(lo, la)
        out.append(f'<span style="{sty};left:{x}%;top:{y}%;font-size:10px;color:#b8602e;font-weight:600">◦ {nm}</span>')
    for lo, la, nm in regions:
        x, y = _pj(lo, la)
        out.append(f'<span style="{sty};left:{x}%;top:{y}%;font-family:\'IBM Plex Mono\',monospace;font-size:11px;letter-spacing:2px;color:rgba(122,110,90,.6)">{nm}</span>')
    return "\n            ".join(out)


def main():
    html = SRC.read_text(encoding="utf-8")
    master = json.load(open(DATA / "languages.master.json", encoding="utf-8"))["languages"]  # B1 — yatay ölçek temeli
    prof = {p["iso"]: p for p in json.load(open(DATA / "profiles.json", encoding="utf-8"))["profiles"]}
    lex = json.load(open(DATA / "distance.lexical.json", encoding="utf-8"))["matrix"]
    typ = json.load(open(DATA / "distance.typological.json", encoding="utf-8"))["matrix"]
    cog = json.load(open(DATA / "cognates.json", encoding="utf-8"))
    cogdeep = json.load(open(DATA / "cognates_deep.json", encoding="utf-8"))  # ds18 — 11 kavram × 18 dil (yatay ölçek)
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
    # Konuşur sayısındaki (YYYY) sayım yılları KALDIRILIR — master'daki 33 dilde yıl yok; tutarlılık için
    # tümünden çıkarılır (rakamlar zaten "~" tahmin). Kaynaklı+yıllı zenginleştirme sonraki deepsearch'le gelir.
    nenrich = 0
    for code, e in extra.items():
        for field in ("speakers", "script", "note"):
            if field in e:
                val = re.sub(r"\s*\([^)]*\d{4}[^)]*\)", "", e[field]).strip() if field == "speakers" else e[field]
                pat = re.compile(r"(\{code:'" + re.escape(code) + r"',[^\n]*?" + field + r":)'[^']*'")
                html, n = pat.subn(lambda m, v=val: m.group(1) + json.dumps(v, ensure_ascii=False), html, count=1)
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

    # ── Dil Profilleri 14 → 47: master'dan 33 YENİ dili EKLE (14'ün zengin pipeline'ına dokunma) ──
    PROF14_ISO = {"tur", "azj", "tuk", "kaz", "kir", "uig", "sah", "tyv", "kjh", "tat", "bak", "chv", "cjs", "klj"}
    REGION_TR = {
        "gag": "Moldova (Gagavuzya)", "bgx": "Balkanlar (Bulgaristan/Yunanistan)", "azb": "İran (Güney Azerbaycan)",
        "kmz": "İran (Horasan)", "qxq": "İran (Fars)", "slr": "Çinghay/Gansu (ÇHC)", "crh": "Kırım; Orta Asya sürgün",
        "uum": "Ukrayna (Azak); Gürcistan", "kaa": "Karakalpakistan (Özbekistan)", "krc": "Karaçay-Çerkes/Kabardey (RF)",
        "kum": "Dağıstan (RF)", "nog": "Dağıstan/Stavropol (RF)", "kdr": "Litvanya, Kırım (Karaim)",
        "jct": "Kırım (Kırımçak)", "sty": "Batı Sibirya (Tümen, RF)", "alt": "Altay Cumhuriyeti (RF)",
        "xzm": "Harezm (tarihî bölge)", "qwm": "Karadeniz kuzeyi (tarihî)", "uzn": "Özbekistan",
        "uzs": "Afganistan (Güney Özbek)", "aib": "Sincan (ÇHC) — Eynu", "ili": "Sincan/Kazakistan (İli vadisi)",
        "oui": "Turfan/Tarım (tarihî)", "xqa": "Kaşgar/Balasagun (tarihî)", "chg": "Maveraünnehir (tarihî)",
        "dlg": "Taymır (RF) — Dolgan", "kim": "İrkutsk/Buryatya (RF) — Tofa", "atv": "Altay (RF, kuzey)",
        "clw": "Tomsk (RF) — Çulım", "ybe": "Çinghay/Gansu (ÇHC) — Sarı Uygur", "xbo": "İdil-Bulgar (tarihî)",
        "zkz": "Hazar Kağanlığı (tarihî)", "otk": "Orhun vadisi (tarihî, Moğolistan)"}
    JOSHI33 = {"uzn": "3 · orta"}   # Joshi 2020 Özbekçe=3; diğer canlılar düşük-kaynak, tarihseller —
    EG_VIT = {"0": 6, "1": 6, "2": 6, "3": 5, "4": 4, "5": 4, "6a": 3, "6b": 2, "7": 1, "8a": 0, "8b": 0, "9": 0, "10": 0}
    EG_TR = {"0": "uluslararası", "1": "ulusal", "2": "bölgesel", "3": "bölgesel", "4": "eğitimsel", "5": "gelişen",
             "6a": "güçlü", "6b": "tehlikede", "7": "değişen", "8a": "ölmekte", "8b": "ölmekte", "9": "uykuda", "10": "ölü"}
    AES_V = {"Safe": 6, "Vulnerable": 4, "Threatened": 3, "Definitelyendangered": 2,
             "Severelyendangered": 1, "Criticallyendangered": 0, "Extinct": 0}

    def _vit_egids(L):
        if L["era"] != "living":
            return 0, "tarihî · ölü dil"
        parts = [re.sub(r"\s+", "", p) for p in (L.get("vitality") or "").split("/")]
        eg = parts[1] if len(parts) > 1 else ""
        vit = EG_VIT.get(eg)
        if vit is None:
            vit = AES_V.get(parts[0] if parts else "", 3)
        lab = EG_TR.get(eg, (parts[0].lower() if parts else ""))
        return vit, (f"{eg} · {lab}" if eg else (lab or "—"))

    new_rows = []
    for L in master:
        iso = L["iso"]
        if iso in PROF14_ISO or L.get("lat") is None:
            continue
        vit, egids = _vit_egids(L)
        region = REGION_TR.get(iso, "—")
        joshi = JOSHI33.get(iso, "—" if L["era"] != "living" else "0–1 · çok düşük")
        if L.get("note"):
            note = L["note"]
        elif L["era"] != "living":
            note = f"Tarihsel/ölü {L['branch']} dili; {region}."
        else:
            note = f"{L['branch']} kolu; {region}."
        entry = {"code": ("culw" if iso == "clw" else iso), "name": L["name"], "branch": L["branch"],
                 "speakers": (L.get("speakers") or "—"), "egids": egids, "vit": vit,
                 "script": (re.sub(r"\s+", "", (L.get("script") or "").split("(")[0]) or "—"),
                 "region": region, "note": note, "joshi": joshi}
        new_rows.append("    " + json.dumps(entry, ensure_ascii=False) + ",")
    prof_anchor = "  ];\n\n  // ---- HISTORY timeline ----"
    nprof33 = 0
    if prof_anchor in html:
        html = html.replace(prof_anchor, "\n".join(new_rows) + "\n" + prof_anchor, 1); nprof33 = len(new_rows)
    print(f"  Dil Profilleri 14->{14 + nprof33} (master'dan +{nprof33} yeni dil)")
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
    new_map = build_map(master)
    html, nmap = re.subn(r"MAP = \[.*?\n  \];", lambda m: new_map, html, flags=re.DOTALL)
    # Faz 1.3 — Harita düğümü TIKLANINCA INLINE bilgi (sayfadan çıkmaz; kullanıcı kararı), profile gitmez
    html = html.replace("        return { name:m.name, branch:m.branch, col,",
                        "        return { name:m.name, branch:m.branch, col, go:()=>this.setState({mapSel:m.code}),", 1)
    html = html.replace('<div style="{{ n.dotStyle }}">',
                        '<div onClick="{{ n.go }}" style="cursor:pointer;transition:transform .14s ease;{{ n.dotStyle }}" style-hover="z-index:40;transform:translate(-50%,-50%) scale(1.5)">', 1)
    # B3/B4 — mapNodes render: çap (sz), etiket-görünürlüğü (lbl: 0 gizli / 1 alt / 2 üst), era stili (tarihsel içi boş+italik)
    nb34 = 0
    b34 = [
        ("        const col = this.BRANCHCOLOR[m.branch];",
         "        const col = this.BRANCHCOLOR[m.branch] || '#9a9082';\n"
         "        const _hist = m.era && m.era!=='living', _big = this.state.screen==='atlas', _z = (this.state.atlasZoom||1);\n"
         "        const _cs = _big ? (1/_z) : 1;\n"   # zoom-wrapper'a karşı ekran-sabit (nokta+etiket büyümez, AYRILIR)
         "        const _d = m.hi?10:9, _show = _big && m.lz>0 && _z>=m.lz;"),   # TEK boyut (konuşur-bazlı kademe kaldırıldı); yalnız Çuvaşça bir tık büyük
        ("transform:translate(-50%,-50%);display:flex;flex-direction:${m.below?'column-reverse':'column'};align-items:center;gap:4px;z-index:${m.hi?3:2}",
         "transform:translate(-50%,-50%) scale(${_cs});display:flex;flex-direction:${m.ldir===2?'column-reverse':'column'};align-items:center;gap:2px;z-index:${m.hi?6:(_show?4:2)}"),
        ("ball:`width:${m.hi?18:13}px;height:${m.hi?18:13}px;border-radius:50%;background:${col};border:2px solid #fbfaf6;box-shadow:0 0 0 ${m.hi?'4px':'1px'} ${m.hi?'rgba(184,96,46,.25)':'rgba(33,29,23,.12)'}`,",
         "ball:`width:${_d}px;height:${_d}px;border-radius:50%;background:${_hist?'#6f665a':col};border:2px solid #fbfaf6;box-shadow:0 0 0 ${m.hi?'3px':'1px'} ${m.hi?'rgba(184,96,46,.30)':'rgba(33,29,23,.14)'}`,"),   # ölü/tarihsel diller: tek koyu gri dolu nokta (kol rengi/çerçeve yok)
        ("label:`font-size:${m.hi?'13px':'12px'};font-weight:${m.hi?'700':'500'};font-family:'Spectral',serif;color:#211d17;white-space:nowrap;background:rgba(251,250,246,.85);padding:1px 6px;border-radius:5px` };",
         "label:`${_show?'':'display:none;'}font-size:11px;font-weight:${m.hi?'600':'500'};font-family:'Spectral',serif;color:${_hist?'#6f665a':'#211d17'};${_hist?'font-style:italic;':''}white-space:nowrap;background:rgba(251,250,246,.94);padding:0 5px;border-radius:5px;box-shadow:0 1px 3px rgba(33,29,23,.08)` };"),
    ]
    for old, new in b34:
        if old in html:
            html = html.replace(old, new, 1); nb34 += 1
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
    # B2 — deniz etiketleri (suyun içinde, dot yok → clutter yok; "denizler önemli olsun"). pointer-events:none
    _sea_lbl = lambda lf, tp, name: (f'<span style="position:absolute;left:{lf}%;top:{tp}%;font-family:\'Spectral\',serif;'
                                     f'font-style:italic;font-size:9.5px;color:#7f9aa6;letter-spacing:.3px;pointer-events:none;white-space:nowrap">{name}</span>\n            ')
    sea_labels = (_sea_lbl(5.5, 42, "Karadeniz") + _sea_lbl(18.5, 56, "Hazar Denizi")
                  + _sea_lbl(26, 37.5, "Aral") + _sea_lbl(3.5, 74, "Akdeniz"))
    if "            <!-- language dots -->" in html:
        html = html.replace("            <!-- language dots -->", sea_labels + "<!-- language dots -->", 1); na4 += 1
    # Argu kolu rengini ekle (Halaçça düğümü + lejant)
    html = html.replace("    'Karluk':'oklch(0.5 0.13 295)', 'Sibirya':'oklch(0.52 0.13 235)',",
                        "    'Karluk':'oklch(0.5 0.13 295)', 'Sibirya':'oklch(0.52 0.13 235)', 'Argu':'#8a7a2e',", 1)
    # mapInfo (seçili düğümün inline kartı) — renderVals
    html = html.replace(
        "      mapLegend:Object.entries(this.BRANCHCOLOR).map(([k,v])=>({label:k, hue:v})),",
        "      mapLegend:Object.entries(this.BRANCHCOLOR).map(([k,v])=>({label:k, hue:v})),\n"
        "      mapInfo:(()=>{ const m=this.MAP.find(x=>x.code===S.mapSel); const eL={living:'',historical:'tarihsel · ölü dil',proto:'ata dil (kök)'}; return m?{has:true,name:m.name,branch:m.branch,speakers:m.speakers,note:m.note||'',vit:m.vit||'',era:(eL[m.era]||''),col:(this.BRANCHCOLOR[m.branch]||'#9a9082')}:{has:false,name:'',branch:'',speakers:'',note:'',vit:'',era:'',col:'#9a9082'}; })(),", 1)
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
        "            <div style=\"display:flex;gap:8px;flex-wrap:wrap;margin-top:7px\"><sc-if value=\"{{ mapInfo.era }}\" hint-placeholder-val=\"{{ false }}\"><span style=\"font-size:10.5px;color:#b8602e;background:#f4ece2;border:1px solid #e4d3c2;border-radius:10px;padding:1px 9px;font-family:'IBM Plex Mono',monospace\">{{ mapInfo.era }}</span></sc-if><sc-if value=\"{{ mapInfo.vit }}\" hint-placeholder-val=\"{{ false }}\"><span style=\"font-size:10.5px;color:#5f574b;background:#efece4;border-radius:10px;padding:1px 9px;font-family:'IBM Plex Mono',monospace\">canlılık: {{ mapInfo.vit }}</span></sc-if></div>\n"
        '            <sc-if value="{{ mapInfo.note }}" hint-placeholder-val="{{ false }}"><p style="font-size:13.5px;line-height:1.6;color:#5f574b;margin:8px 0 0">{{ mapInfo.note }}</p></sc-if>\n'
        '          </div>\n'
        '          </sc-if>')
    nmapcard = 1 if map_legend_block in html else 0
    html = html.replace(map_legend_block, map_legend_block + map_card, 1)
    # intro ipucu
    html = html.replace(
        "Çuvaşça, İdil (Volga) boyunda, Ogur kolunun yaşayan tek temsilcisi olarak ayrı durur.",
        "Çuvaşça, İdil (Volga) boyunda, Ogur kolunun yaşayan tek temsilcisi olarak ayrı durur. Aşağıdaki haritaya tıklayarak tüm Türk dillerini etkileşimli atlasta keşfedebilirsin.", 1)

    # ── ATLAS (büyük harita SAYFASI) — Karşılaştır'daki önizleme tıklanınca açılır ──
    natlas = 0
    atlas_dots = (
        '            <sc-for list="{{ mapNodes }}" as="n" hint-placeholder-count="8">\n'
        '              <div onClick="{{ n.go }}" style="cursor:pointer;transition:transform .14s ease;{{ n.dotStyle }}" style-hover="z-index:40">\n'
        '                <span style="{{ n.ball }}"></span>\n'
        '                <span style="{{ n.label }}">{{ n.name }}</span>\n'
        '              </div>\n'
        '            </sc-for>')
    atlas_legend = (
        '        <div style="display:flex;gap:15px;flex-wrap:wrap;margin-top:14px;padding:0 2px;align-items:center">\n'
        '          <sc-for list="{{ mapLegend }}" as="l"><span style="display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:#5f574b"><span style="width:11px;height:11px;border-radius:50%;background:{{ l.hue }}"></span>{{ l.label }} kolu</span></sc-for>\n'
        '          <span style="display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:#5f574b"><span style="width:11px;height:11px;border-radius:50%;background:#6f665a"></span>tarihsel · ölü dil</span>\n'
        '        </div>')
    # bölge odak düğmeleri (zoom + pan preset) + zoom +/− kontrolleri
    region_row = (
        '        <div style="display:flex;gap:7px;flex-wrap:wrap;margin:10px 0 0;align-items:center">\n'
        '          <span style="font-size:11px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace;letter-spacing:.5px;margin-right:2px">ODAK:</span>\n'
        '          <sc-for list="{{ atlasRegions }}" as="r"><button onClick="{{ r.go }}" style="{{ r.style }}">{{ r.label }}</button></sc-for>\n'
        '        </div>')
    zoom_ctrl = (
        '          <div style="position:absolute;right:12px;bottom:12px;z-index:20;display:flex;flex-direction:column;gap:5px">\n'
        '            <button onClick="{{ atlasZoomIn }}" style="cursor:pointer;width:34px;height:34px;border-radius:9px;border:1px solid rgba(33,29,23,.18);background:#fff;font-size:19px;font-weight:600;color:#211d17;box-shadow:0 2px 8px rgba(33,29,23,.16);line-height:1">+</button>\n'
        '            <button onClick="{{ atlasZoomOut }}" style="cursor:pointer;width:34px;height:34px;border-radius:9px;border:1px solid rgba(33,29,23,.18);background:#fff;font-size:21px;font-weight:600;color:#211d17;box-shadow:0 2px 8px rgba(33,29,23,.16);line-height:1">−</button>\n'
        '          </div>\n'
        '          <div style="position:absolute;left:12px;bottom:12px;z-index:20;font-size:11px;color:#5f574b;background:rgba(251,250,246,.9);border-radius:8px;padding:3px 9px;font-family:\'IBM Plex Mono\',monospace">{{ atlasZoomPct }}</div>')
    ATLAS = (
        '      <!-- ===================== ATLAS (büyük harita) ===================== -->\n'
        '      <sc-if value="{{ isAtlas }}" hint-placeholder-val="{{ false }}">\n'
        '      <section style="max-width:1340px;margin:0 auto;padding:26px 34px 70px">\n'
        '        <div style="font-family:\'IBM Plex Mono\',monospace;font-size:12px;letter-spacing:1.5px;color:#d98b4a">TÜRK DÜNYASI DİL ATLASI</div>\n'
        '        <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:18px;flex-wrap:wrap;margin:6px 0 2px">\n'
        '          <h2 style="font-family:\'Spectral\',serif;font-weight:600;font-size:36px;margin:0">Türk dilleri haritası</h2>\n'
        '          <button onClick="{{ goCompareMap }}" style="cursor:pointer;background:#fff;border:1px solid rgba(33,29,23,.18);border-radius:9px;padding:8px 14px;font-size:13px;font-family:inherit;color:#211d17">← Karşılaştır</button>\n'
        '        </div>\n'
        '        <p style="font-size:14.5px;line-height:1.6;color:#5f574b;max-width:82ch;margin:0 0 4px">Türk dillerinin coğrafi dağılımı; denizler, dağlar ve nehirlerle birlikte. Üstten bir bölge seçin ya da +/− ile yakınlaştırıp haritayı sürükleyerek gezin. Ölü ve tarihsel diller içi boş halkayla, eğik yazıyla gösterilir.</p>\n'
        + region_row + '\n'
        '        <div onMouseDown="{{ atlasDown }}" onMouseMove="{{ atlasMove }}" onMouseUp="{{ atlasUp }}" onMouseLeave="{{ atlasUp }}" style="position:relative;width:100%;aspect-ratio:1.62;background:#ece5d5;border:1px solid rgba(33,29,23,.12);border-radius:18px;overflow:hidden;margin-top:10px;cursor:{{ atlasCursor }};user-select:none">\n'
        '          <div style="{{ atlasWrapStyle }}">\n'
        '            ' + build_map_bg() + '\n'
        '            ' + atlas_feature_labels() + '\n'
        + atlas_dots + '\n'
        '          </div>\n'
        + zoom_ctrl + '\n'
        '        </div>\n'
        + atlas_legend + '\n'
        + map_card + '\n'
        '      </section>\n'
        '      </sc-if>\n')
    ogren_anchor = "      <!-- ===================== OGREN ===================== -->"
    if ogren_anchor in html:
        html = html.replace(ogren_anchor, ATLAS + ogren_anchor, 1); natlas += 1
    # mouse sürükle-pan: atlas yakınlaştırıldığında haritayı gezmek için (atlasCx/atlasCy güncellenir)
    if "  active(){ return this.WORDS[this.state.activeWordId]; }" in html:
        html = html.replace("  active(){ return this.WORDS[this.state.activeWordId]; }",
            "  atlasPanStart(e){ const z=(this.state.atlasZoom||1); if(z<=1.01)return; const t=e.currentTarget; this._pan={x:e.clientX,y:e.clientY,cx:(this.state.atlasCx||50),cy:(this.state.atlasCy||45),w:(t&&t.clientWidth)||800,h:(t&&t.clientHeight)||500}; }\n"
            "  atlasPanMove(e){ if(!this._pan)return; const z=(this.state.atlasZoom||1); const dx=e.clientX-this._pan.x, dy=e.clientY-this._pan.y; const cx=Math.max(8,Math.min(92,this._pan.cx - dx*100/(this._pan.w*z))); const cy=Math.max(8,Math.min(92,this._pan.cy - dy*100/(this._pan.h*z))); this.setState({atlasCx:cx,atlasCy:cy}); }\n"
            "  atlasPanEnd(){ this._pan=null; }\n"
            "  active(){ return this.WORDS[this.state.activeWordId]; }", 1); natlas += 1
    # renderVals: isAtlas + go handler'ları (goCognate komşuluğuna)
    html = html.replace(
        "      goCognate:()=>this.setState({screen:'cognate'}),",
        "      goCognate:()=>this.setState({screen:'cognate'}),\n"
        "      isAtlas:S.screen==='atlas', goAtlas:()=>this.setState({screen:'atlas'}), goCompareMap:()=>this.setState({screen:'compare', compareTab:'map'}),\n"
        "      atlasDown:(e)=>this.atlasPanStart(e), atlasMove:(e)=>this.atlasPanMove(e), atlasUp:()=>this.atlasPanEnd(), atlasCursor:((S.atlasZoom||1)>1.01?'grab':'default'),\n"
        "      atlasWrapStyle:(()=>{ const z=S.atlasZoom||1, cx=S.atlasCx||50, cy=S.atlasCy||45; return `position:absolute;inset:0;transform-origin:0 0;transition:transform .3s ease;transform:scale(${z}) translate(${(50/z-cx).toFixed(2)}%, ${(50/z-cy).toFixed(2)}%)`; })(),\n"
        "      atlasZoomPct:'%'+Math.round((S.atlasZoom||1)*100),\n"
        "      atlasZoomIn:()=>this.setState(s=>({atlasZoom:Math.min(4,Math.round((((s.atlasZoom||1))+0.5)*10)/10)})),\n"
        "      atlasZoomOut:()=>this.setState(s=>({atlasZoom:Math.max(1,Math.round((((s.atlasZoom||1))-0.5)*10)/10)})),\n"
        "      atlasRegions:[['Tüm dünya',1,50,45],['Anadolu–Kafkas',2.7,15,49],['İdil-Ural',2.7,23,26],['Orta Asya',2.4,37,45],['Batı Sibirya',2.3,53,28],['Doğu (Saha)',2.0,72,13]].map(rr=>{ const sel=Math.abs((S.atlasZoom||1)-rr[1])<0.05 && Math.abs((S.atlasCx||50)-rr[2])<0.6; return { label:rr[0], go:()=>this.setState({atlasZoom:rr[1],atlasCx:rr[2],atlasCy:rr[3]}), style:`cursor:pointer;border:1px solid ${sel?'#211d17':'rgba(33,29,23,.16)'};background:${sel?'#211d17':'#fff'};color:${sel?'#f4f1ea':'#5f574b'};border-radius:14px;padding:5px 12px;font-size:12px;font-family:'IBM Plex Sans',sans-serif;font-weight:${sel?600:500}` }; }),", 1)
    # atlas state alanları
    html = html.replace("    compareTab: 'rows',", "    compareTab: 'rows', atlasZoom:1, atlasCx:50, atlasCy:45,", 1)
    natlas += 1 if "isAtlas:S.screen==='atlas'" in html else 0
    # nav: KEŞFET'e "Harita" (Dil Profilleri'nden sonra)
    if "{id:'profile', label:'Dil Profilleri'}," in html:
        html = html.replace("{id:'profile', label:'Dil Profilleri'},",
                            "{id:'profile', label:'Dil Profilleri'},\n      {id:'atlas', label:'Harita'},", 1); natlas += 1
    # Karşılaştır harita önizlemesi: tüm önizlemeyi tıklanabilir yap (Büyük atlas butonu kaldırıldı —
    # kullanıcı: "büyük atlas yazısı gereksiz, doğrudan etkileşimli karşılasın"). Tam etkileşim Harita sayfasında.
    cmp_map_div = '<div style="position:relative;width:100%;aspect-ratio:1000/560;background:#ece5d5;border:1px solid rgba(33,29,23,.12);border-radius:18px;overflow:hidden">'
    cmp_map_new = '<div onClick="{{ goAtlas }}" style="position:relative;width:100%;aspect-ratio:1000/560;background:#ece5d5;border:1px solid rgba(33,29,23,.12);border-radius:18px;overflow:hidden;cursor:pointer">'
    if cmp_map_div in html:
        html = html.replace(cmp_map_div, cmp_map_new, 1); natlas += 1
    # breadcrumb etiketi (üst bar)
    html = html.replace("research:'/ araştırmacı', cognate:'/ kognat', sources:'/ kaynaklar' }",
                        "research:'/ araştırmacı', cognate:'/ kognat', sources:'/ kaynaklar', atlas:'/ harita' }", 1)
    print(f"  ATLAS büyük harita sayfası (ekran+handler+nav+önizleme CTA): {natlas}/4")
    print(f"  Harita inline kart (1.3): mapInfo+kart={nmapcard}")
    print(f"  A4a/B2 harita arka planı (SVG+konteyner+4 bölge+deniz etiketleri): {na4}/7 yama")
    print(f"  B3/B4 harita TÜM diller ({len(master)}) + açgözlü etiket + era stili: mapNodes={nb34}/4 yama")

    # Uzaklık Gezgini ← gerçek matrisler: leksikal(Savelyev) + tipolojik(WALS) + coğrafi(koordinat)
    # B yatay ölçek: 10 → 32 dil (Savelyev leksikal matrisinin tamamı). Koordinat master'dan.
    mcoord = {L["iso"]: (L["lat"], L["lon"]) for L in master if L.get("lat") is not None and L.get("lon") is not None}
    real_dist = build_distance(mcoord, lex, typ, cog, intel)
    if "REAL_DIST" not in html:
        html = html.replace("  KOKEN_API = '" + API + "';",
                            "  KOKEN_API = '" + API + "';\n  REAL_DIST = " + json.dumps(real_dist) + ";", 1)
    old_val = "    const val = (key)=> Math.abs(base[key]-t[key]);"
    new_val = ("    const RD = this.REAL_DIST || {};\n"
               "    const realv = (m)=>{ const r=(RD[m]||{})[S.distBase]; return (r && r[S.distTarget]!=null) ? r[S.distTarget] : null; };\n"
               "    const val = (key)=>{ const m = {leks:'leks', tipo:'tipo', cogr:'geo', filo:'filo', anla:'anla'}[key]; const rv = m ? realv(m) : null; return rv!=null ? rv : Math.abs(base[key]-t[key]); };")
    ndist = 1 if old_val in html else 0
    html = html.replace(old_val, new_val, 1)
    # LANGVEC 10 → 32 (master adı/kol + chv-satırı gerçek değerlerle yedek). REAL_DIST pairwise'i ezer.
    chv_row = lambda key: real_dist.get(key, {}).get("chv", {})
    lv_rows = []
    for code, sav, iso, nm, branch in DIST_ROWS:
        f = lambda key, d=0.5: round(chv_row(key).get(code, d), 3)
        lv_rows.append("    %s: {name:%s, branch:%s, filo:%s, leks:%s, anla:%s, tipo:%s, cogr:%s}," % (
            code, json.dumps(nm, ensure_ascii=False), json.dumps(branch, ensure_ascii=False),
            f("filo"), f("leks"), f("anla"), f("tipo"), f("geo")))
    new_langvec = "LANGVEC = {\n" + "\n".join(lv_rows) + "\n  };"
    html, nlv = re.subn(r"LANGVEC = \{.*?\n  \};", lambda m: new_langvec, html, flags=re.DOTALL)
    print(f"  Uzaklik 10->{len(DIST_ROWS)} dil (Savelyev tam matris): LANGVEC={nlv}, REAL_DIST mcoord")

    # Kognat Ağı ← ds18 genişletilmiş kognat veritabanı (11 kavram × 18 dil, faithful+atıflı)
    cog_obj, cog_default = build_cognates_deep(cogdeep)
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
                  "      cognateGloss:c.gloss, cognateProto:c.proto, cognateNote:c.note, cognateNodes:nodes,\n"
                  "      cognateProtoStyle:(\"font-family:'Spectral',serif;font-weight:700;line-height:1.05;text-align:center;color:#211d17;font-size:\"+((c.proto||'').length>11?'11px':(c.proto||'').length>6?'15px':'18px')),\n"
                  "      cognateCol3:(S.cognateMode==='broad'?'Segment':'Ses kuralı'),\n"
                  "      cognateCells:cells, cognateGap:gaps, cognateCatName:(c.cat||''),\n"
                  "      cognateConcepticon:(c.concepticon!=null?('Concepticon '+c.concepticon):'') };")
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
    # ---- ds18: Kognat Ağı 7→18 dil + ses-kuralı dökümü (yatay ölçek) ----
    # NOT: BRANCHCOLOR['Argu'] (Halaçça) ZATEN harita bölümünde eklendi (#8a7a2e) → burada tekrar eklenmez.
    ndeep = 0
    # (1) cognateVals düğüm geometrisi: 18 düğüm için yarıçap/boyut ölçekle + ses-kuralı tablo satırları (cells/gaps)
    deep_geo_old = (
        "    const n = c.nodes.length;\n"
        "    const nodes = c.nodes.map((nd,i)=>{\n"
        "      const a = (-90 + i*(360/n))*Math.PI/180;\n"
        "      const xp = 50 + 37*Math.cos(a), yp = 50 + 37*Math.sin(a);\n"
        "      const col = this.BRANCHCOLOR[nd.branch] || '#5f574b';\n"
        "      return { lang:nd.lang, word:this.disp(nd.word, null, nd.lang==='Çuvaşça'?'chv':'gen'), branch:nd.branch, shift:!!nd.shift,\n"
        "        xp:xp.toFixed(2), yp:yp.toFixed(2),\n"
        "        edgeStroke: nd.shift ? '#d98b4a' : 'rgba(33,29,23,.22)',\n"
        "        edgeWidth: nd.shift ? '2' : '1.3', edgeDash: nd.shift ? '5,4' : '0',\n"
        "        nodeStyle:`position:absolute;left:${xp.toFixed(2)}%;top:${yp.toFixed(2)}%;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:3px;background:${nd.shift?'#211d17':'#fff'};border:2px solid ${col};border-radius:12px;padding:8px 13px;min-width:62px;box-shadow:0 3px 10px rgba(33,29,23,.1);z-index:2`,\n"
        "        wordStyle:`font-family:'Spectral',serif;font-size:20px;font-weight:700;color:${nd.shift?'#f4f1ea':'#211d17'}`,\n"
        "        langStyle:`font-size:10px;font-family:'IBM Plex Mono',monospace;color:${nd.shift?'rgba(244,241,234,.6)':'#9a9082'}` };\n"
        "    });")
    deep_geo_new = (
        "    const _ns = [...c.nodes].sort((a,b)=>String(a.lang).localeCompare(String(b.lang),'tr'));\n"
        "    const n = _ns.length;\n"
        "    const _r0 = n>26 ? 42 : n>12 ? 42 : 38, _alt = n>26 ? 7 : 0, _rm = n>26 ? 2 : 1;\n"   # graf büyütüldü → ≤26 düğüm TEK halka (derin 18 dahil); 32 düğümde 2 halka
        "    const _mw = n>24 ? 24 : n>12 ? 44 : 60, _pad = n>24 ? '3px 6px' : n>12 ? '4px 7px' : '8px 13px', _wf = n>24 ? 12 : n>12 ? 15 : 20;\n"
        "    const nodes = _ns.map((nd,i)=>{\n"
        "      const a = (-90 + i*(360/n))*Math.PI/180;\n"
        "      const _r = _r0 + (i%_rm)*_alt;\n"
        "      const xp = 50 + _r*Math.cos(a), yp = 50 + _r*Math.sin(a);\n"
        "      const col = this.BRANCHCOLOR[nd.branch] || '#7d6a55';\n"
        "      return { lang:nd.lang, word:this.disp(nd.word, null, nd.lang==='Çuvaşça'?'chv':'gen'), branch:nd.branch, shift:!!nd.shift,\n"
        "        xp:xp.toFixed(2), yp:yp.toFixed(2),\n"
        "        edgeStroke: nd.shift ? '#d98b4a' : 'rgba(33,29,23,.22)',\n"
        "        edgeWidth: nd.shift ? '2' : '1.3', edgeDash: nd.shift ? '5,4' : '0',\n"
        "        nodeStyle:`position:absolute;left:${xp.toFixed(2)}%;top:${yp.toFixed(2)}%;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:2px;background:${nd.shift?'#211d17':'#fff'};border:2px solid ${col};border-radius:11px;padding:${_pad};min-width:${_mw}px;box-shadow:0 3px 10px rgba(33,29,23,.1);z-index:2`,\n"
        "        wordStyle:`font-family:'Spectral',serif;font-size:${_wf}px;font-weight:700;color:${nd.shift?'#f4f1ea':'#211d17'}`,\n"
        "        langStyle:`font-size:${n>24?'7px':'9px'};font-family:'IBM Plex Mono',monospace;color:${nd.shift?'rgba(244,241,234,.6)':'#9a9082'};white-space:nowrap` };\n"
        "    });\n"
        "    const gaps = _ns.filter(nd=>nd.shift).map(nd=>nd.lang);\n"
        "    const cells = _ns.map(nd=>{ const col=this.BRANCHCOLOR[nd.branch]||'#7d6a55';\n"
        "      const fd = (nd.native && nd.native!==nd.word) ? (nd.native+' · '+nd.word) : nd.word;\n"
        "      return { lang:nd.lang, branch:nd.branch, form:fd, rule:(nd.rule||''), shift:!!nd.shift, dotColor:col,\n"
        "        rowStyle:`display:grid;grid-template-columns:132px minmax(96px,1fr) 1.4fr;gap:10px;align-items:baseline;padding:7px 12px;border-radius:9px;background:${nd.shift?'rgba(217,139,74,.10)':'#fbfaf6'};border:1px solid ${nd.shift?'rgba(217,139,74,.35)':'rgba(33,29,23,.07)'}`,\n"
        "        langStyle:'font-family:\\'Spectral\\',serif;font-size:14.5px;font-weight:600;color:#211d17;display:flex;align-items:center;gap:7px',\n"
        "        formStyle:'font-family:\\'Spectral\\',serif;font-size:15px;color:#211d17',\n"
        "        ruleStyle:`font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:${nd.shift?'#b8602e':'#6b6358'}` };\n"
        "    });")
    if deep_geo_old in html:
        html = html.replace(deep_geo_old, deep_geo_new, 1); ndeep += 1
    # (2) markup: graf altına dil-dil ses-kuralı dökümü + kaynak satırını ds18'e güncelle
    deep_mk_old = (
        '            <div style="margin-top:14px;font-size:11px;color:rgba(244,241,234,.4);font-family:\'IBM Plex Mono\',monospace">Kaynak: SavelyevTurkic CLDF · CC BY 4.0</div>\n'
        '          </div>\n'
        '        </div>\n'
        '      </section>')
    deep_mk_new = (
        '            <div style="margin-top:14px;font-size:11px;color:rgba(244,241,234,.4);font-family:\'IBM Plex Mono\',monospace">Kaynak: KÖKEN derin araştırma (ds18) · Savelyev 2020 + Cambridge Turkic + Wiktionary</div>\n'
        '          </div>\n'
        '        </div>\n'
        '        <div style="margin-top:32px">\n'
        '          <div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:12px">\n'
        '            <span style="font-family:\'Spectral\',serif;font-weight:600;font-size:21px;color:#211d17">Dil dil ses kuralı</span>\n'
        '            <span style="font-size:12.5px;color:#9a9082">{{ cognateConcepticon }} · Proto {{ cognateProto }} · {{ cognateCatName }}</span>\n'
        '          </div>\n'
        '          <div style="display:grid;grid-template-columns:132px minmax(96px,1fr) 1.4fr;gap:10px;padding:0 12px 7px;font-family:\'IBM Plex Mono\',monospace;font-size:10.5px;letter-spacing:.8px;color:#9a9082;border-bottom:1px solid rgba(33,29,23,.08);margin-bottom:6px">\n'
        '            <span>DİL</span><span>BİÇİM</span><span>{{ cognateCol3 }}</span>\n'
        '          </div>\n'
        '          <div style="display:flex;flex-direction:column;gap:5px">\n'
        '            <sc-for list="{{ cognateCells }}" as="c" hint-placeholder-count="6">\n'
        '              <div style="{{ c.rowStyle }}">\n'
        '                <span style="{{ c.langStyle }}"><span style="width:8px;height:8px;border-radius:3px;background:{{ c.dotColor }};flex:none"></span>{{ c.lang }}</span>\n'
        '                <span style="{{ c.formStyle }}">{{ c.form }}</span>\n'
        '                <span style="{{ c.ruleStyle }}">{{ c.rule }}</span>\n'
        '              </div>\n'
        '            </sc-for>\n'
        '          </div>\n'
        '          <div style="margin-top:10px;font-size:12px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace"><b style="color:#b8602e">Turuncu satır</b> = kognat boşluğu: o dil bu kavramı farklı bir kökten (ya da alıntıdan) karşılar — yani ortak atadan gelmez.</div>\n'
        '        </div>\n'
        '        <div style="margin-top:34px;background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:16px;padding:24px 28px;max-width:840px">\n'
        '          <div style="font-family:\'Spectral\',serif;font-weight:600;font-size:20px;margin-bottom:12px">Bu sayfa ne anlatıyor?</div>\n'
        '          <div style="font-size:14px;line-height:1.7;color:#3f3a32;display:flex;flex-direction:column;gap:11px">\n'
        '            <p style="margin:0"><b>Kökteş (kognat) nedir?</b> Farklı dillerde, ortak bir atadan — aynı eski kelimeden — türeyen sözcüklerdir. Türkçe <i>göz</i>, Kazakça <i>köz</i>, Çuvaşça <i>kuś</i>: üçü de Ana Türkçe <i>*kȫŕ</i> kökünden gelir.</p>\n'
        '            <p style="margin:0"><b>Dairede ne var?</b> Ortada dilbilimcilerin yeniden kurduğu <b>Ana Türkçe kök</b>, çevresinde bu kökün bugünkü dillerdeki karşılıkları. Düz çizgi doğrudan kökteşi; <b style="color:#b8602e">turuncu kesik çizgi</b> o dilin kavramı <b>farklı bir kökten</b> (ya da alıntıyla) karşıladığını, yani kognat boşluğunu gösterir.</p>\n'
        '            <p style="margin:0"><b>Neden önemli?</b> Düzenli ses denklikleri (ör. Çuvaşça <i>r</i> ↔ Ortak Türkçe <i>z</i>) ve kökteşler, dillerin akrabalığını ortaya koyan ve ortak atayı yeniden kurmayı sağlayan <b>karşılaştırmalı yöntemin</b> temelidir. Boşluklar ise her dilin kendi tarihini — göç, temas, yenilik — ele verir.</p>\n'
        '          </div>\n'
        '          <div style="margin-top:15px;font-size:11.5px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace">Karşılaştırmalı yöntem (tarihsel dilbilim) · Savelyev &amp; Robbeets 2020 · Cambridge, The Turkic Languages (2021)</div>\n'
        '        </div>\n'
        '      </section>')
    if deep_mk_old in html:
        html = html.replace(deep_mk_old, deep_mk_new, 1); ndeep += 1
    # proto-fonem bubble: uzun protolar (ör. *baĺč / *baš, *kümüĺ) daireye sığsın diye responsive font
    if '<span style="font-family:\'Spectral\',serif;font-size:19px;font-weight:700">{{ cognateProto }}</span>' in html:
        html = html.replace('<span style="font-family:\'Spectral\',serif;font-size:19px;font-weight:700">{{ cognateProto }}</span>',
                            '<span style="{{ cognateProtoStyle }}">{{ cognateProto }}</span>', 1); ndeep += 1
    # GRAF BÜYÜTÜLDÜ: kutular tek halkaya sığsın (kullanıcı önerisi) — konteyner 460→600, merkez bubble 88→104
    if 'position:relative;width:100%;max-width:460px;aspect-ratio:1/1;margin:0 auto' in html:
        html = html.replace('position:relative;width:100%;max-width:460px;aspect-ratio:1/1;margin:0 auto',
                            'position:relative;width:100%;max-width:600px;aspect-ratio:1/1;margin:0 auto', 1); ndeep += 1
    if 'transform:translate(-50%,-50%);background:#d98b4a;color:#211d17;border-radius:50%;width:88px;height:88px;' in html:
        html = html.replace('transform:translate(-50%,-50%);background:#d98b4a;color:#211d17;border-radius:50%;width:88px;height:88px;',
                            'transform:translate(-50%,-50%);background:#d98b4a;color:#211d17;border-radius:50%;width:104px;height:104px;', 1); ndeep += 1
    # SES NOTU paneli doğal yükseklikte (align-items:start) — NASIL OKUNUR açıklaması panelden ÇIKARILDI,
    # kullanıcı isteğiyle üstteki "nasıl çalışır?" yardımına taşındı (aşağıda helpblk'e eklendi).
    html = html.replace('grid-template-columns:1fr 290px;gap:24px;margin-top:22px;align-items:center',
                        'grid-template-columns:1fr 300px;gap:24px;margin-top:22px;align-items:start', 1)
    # Karşılaştır harita SEKMESİ KALDIRILDI + atlas "← Karşılaştır" → Dizilim sekmesi (eski harita önizlemesi öldürüldü).
    html = html.replace("    const compareTabs = [['rows','Dizilim'],['sound','Ses denklikleri'],['tree','Soy ağacı'],['map','Harita']]",
                        "    const compareTabs = [['rows','Dizilim'],['sound','Ses denklikleri'],['tree','Soy ağacı']]", 1)
    html = html.replace("goCompareMap:()=>this.setState({screen:'compare', compareTab:'map'}),",
                        "goCompareMap:()=>this.setState({screen:'compare', compareTab:'rows'}),", 1)
    print(f"  ds18 Kognat: dokum + proto-fit + tablo baslik + GRAF buyutme + SES NOTU dolu + Harita-sekme->atlas: {ndeep}/5")

    # ---- ds17: Ses denklikleri 4 Çuvaş-merkezli kural → 7 kol-izoglosu (Çuvaş-ötesi) ----
    nsl = 0
    # (1) SOUND dizisini ds17 kol-izoglosslarıyla değiştir (rot/lam/y kanıt sayıları Savelyev verisinden)
    sl = build_sound_laws(sound_evidence(cog))
    new_sound = "  SOUND = " + json.dumps(sl, ensure_ascii=False) + ";"
    html, c_sl = re.subn(r"  SOUND = \[.*?\n  \];", lambda m: new_sound, html, flags=re.DOTALL)
    nsl += c_sl
    # (2) soundCards builder: çok-kollu refleks + kol-renkli nokta + kanıt rozeti
    sl_b_old = (
        "    const soundCards = this.SOUND.map((s,i)=>({\n"
        "      ...s,\n"
        "      select:()=>this.setState({soundSel:i}),\n"
        "      cardStyle:`cursor:pointer;text-align:left;background:${i===S.soundSel?'#fff':'#fbfaf6'};border:2px solid ${i===S.soundSel?'#d98b4a':'rgba(33,29,23,.1)'};border-radius:14px;padding:20px 22px;font-family:inherit;box-shadow:${i===S.soundSel?'0 8px 20px rgba(33,29,23,.08)':'none'};transition:all .15s`,\n"
        "    }));")
    sl_b_new = (
        "    const _scol = (b)=>{ const bc=this.BRANCHCOLOR; if(/Oğur|Çuvaş/.test(b))return bc['Ogur']; if(/Argu|Halaç/.test(b))return bc['Argu']||'#8a7a2e'; if(/Yakut|Sibirya|Hakas|Şor|Tuva/.test(b))return bc['Sibirya']; if(/Kıpçak/.test(b))return bc['Kıpçak']; if(/Karluk/.test(b))return bc['Karluk']; if(/Oğuz/.test(b))return bc['Oğuz']; return '#9a9082'; };\n"
        "    const soundCards = this.SOUND.map((s,i)=>({\n"
        "      proto:s.proto, name:s.name, desc:s.desc, evid:(s.evid||''),\n"
        "      evidStyle: s.evid ? \"font-size:10.5px;font-family:'IBM Plex Mono',monospace;letter-spacing:.3px;color:#2f8a5b;background:rgba(47,138,91,.1);border-radius:6px;padding:2px 8px;margin-left:auto\" : 'display:none',\n"
        "      reflexes: s.reflexes.map(r=>({ branch:r.branch, val:r.val, ex:r.ex, dotColor:_scol(r.branch) })),\n"
        "      select:()=>this.setState({soundSel:i}),\n"
        "      cardStyle:`cursor:pointer;text-align:left;background:${i===S.soundSel?'#fff':'#fbfaf6'};border:2px solid ${i===S.soundSel?'#d98b4a':'rgba(33,29,23,.1)'};border-radius:14px;padding:20px 22px;font-family:inherit;box-shadow:${i===S.soundSel?'0 8px 20px rgba(33,29,23,.08)':'none'};transition:all .15s`,\n"
        "    }));")
    if sl_b_old in html:
        html = html.replace(sl_b_old, sl_b_new, 1); nsl += 1
    # (3) kart markup: cv↔ct ikili → proto + ad + kanıt + kol-refleks satırları
    sl_mk_old = (
        '              <button onClick="{{ s.select }}" style="{{ s.cardStyle }}">\n'
        '                <div style="display:flex;align-items:center;gap:14px">\n'
        '                  <span style="font-family:\'Spectral\',serif;font-size:30px;font-weight:700;color:#2f6fb0">{{ s.cv }}</span>\n'
        '                  <span style="font-size:20px;color:#9a9082">↔</span>\n'
        '                  <span style="font-family:\'Spectral\',serif;font-size:30px;font-weight:700;color:#b86a2e">{{ s.ct }}</span>\n'
        '                  <span style="margin-left:auto;font-family:\'IBM Plex Mono\',monospace;font-size:11px;color:#9a9082;letter-spacing:.5px;text-align:right">{{ s.name }}</span>\n'
        '                </div>\n'
        '                <div style="margin-top:14px;display:flex;flex-direction:column;gap:8px">\n'
        '                  <sc-for list="{{ s.examples }}" as="e" hint-placeholder-count="2">\n'
        '                    <div style="display:flex;align-items:center;gap:10px;font-family:\'Spectral\',serif">\n'
        '                      <span style="font-size:17px;font-weight:600;color:#2f6fb0">{{ e.cv }}</span>\n'
        '                      <span style="font-size:13px;color:#9a9082;font-family:\'IBM Plex Sans\'">Çuv.</span>\n'
        '                      <span style="margin-left:auto;font-size:17px;font-weight:600;color:#b86a2e">{{ e.tr }}</span>\n'
        '                      <span style="font-size:13px;color:#9a9082;font-family:\'IBM Plex Sans\';width:54px;text-align:right">Tür.</span>\n'
        '                    </div>\n'
        '                  </sc-for>\n'
        '                </div>\n'
        '              </button>')
    sl_mk_new = (
        '              <button onClick="{{ s.select }}" style="{{ s.cardStyle }}">\n'
        '                <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">\n'
        '                  <span style="font-family:\'Spectral\',serif;font-size:30px;font-weight:700;color:#2f6fb0">{{ s.proto }}</span>\n'
        '                  <span style="font-family:\'Spectral\',serif;font-size:18px;font-weight:600;color:#211d17">{{ s.name }}</span>\n'
        '                  <span style="{{ s.evidStyle }}">{{ s.evid }}</span>\n'
        '                </div>\n'
        '                <div style="font-size:13px;color:#5f574b;margin-top:7px;line-height:1.5">{{ s.desc }}</div>\n'
        '                <div style="margin-top:13px;display:flex;flex-direction:column;gap:7px">\n'
        '                  <sc-for list="{{ s.reflexes }}" as="r" hint-placeholder-count="2">\n'
        '                    <div style="display:grid;grid-template-columns:148px 74px 1fr;gap:9px;align-items:baseline">\n'
        '                      <span style="display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-family:\'IBM Plex Mono\',monospace;color:#5f574b"><span style="width:8px;height:8px;border-radius:3px;background:{{ r.dotColor }};flex:none"></span>{{ r.branch }}</span>\n'
        '                      <span style="font-family:\'Spectral\',serif;font-size:19px;font-weight:700;color:#b86a2e">{{ r.val }}</span>\n'
        '                      <span style="font-family:\'Spectral\',serif;font-size:14px;color:#5f574b">{{ r.ex }}</span>\n'
        '                    </div>\n'
        '                  </sc-for>\n'
        '                </div>\n'
        '              </button>')
    if sl_mk_old in html:
        html = html.replace(sl_mk_old, sl_mk_new, 1); nsl += 1
    # (4) giriş metni: Çuvaş-merkezli → kol-seviyesi izogloss çerçevesi
    sl_intro_old = ('<p style="font-size:15px;line-height:1.6;color:#5f574b;max-width:70ch;margin:0 0 14px">Çuvaşça, '
                    'Türk dil ailesinin en erken ayrılan kolu (Ogur/Bulgar). Bu yüzden düzenli ses denklikleri '
                    'taşır: bir Çuvaşça sesi, ortak Türkçedeki başka bir sese karşılık gelir. Bir kartı seç, '
                    'harfler eşleşsin.</p>')
    sl_intro_new = ('<p style="font-size:15px;line-height:1.6;color:#5f574b;max-width:74ch;margin:0 0 14px">Türk '
                    'dilleri ailesini kollara ayıran <strong>düzenli ses yasaları</strong> (izoglosslar). Her kart '
                    'bir Proto-Türkçe fonemin farklı kollardaki refleksini ve örneklerini gösterir — Çuvaşça (Oğur) '
                    'ile başlayıp tüm kol-çiftlerine açılır.</p>')
    if sl_intro_old in html:
        html = html.replace(sl_intro_old, sl_intro_new, 1); nsl += 1
    print(f"  ds17 Ses denklikleri 4->7 kol-izoglosu: {nsl}/4 yama (SOUND, builder, kart, giris)")

    # ---- Bölüm B: Dil Profilleri selektörü A1-tarzı (47 dil → ara + kola göre süz) ----
    npf = 0
    # (1) state: profileQ + profileCat
    if "profileSel: 'chv'," in html:
        html = html.replace("profileSel: 'chv',", "profileSel: 'chv', profileQ:'', profileCat:'all',", 1); npf += 1
    # (2) profileVals: filtre mantığı (arama + kol kategorisi) + kategori çipleri
    pf_old = "    const cards = this.LANGPROFILE.map(l=>{\n      const sel = l.code===S.profileSel, vc = this.vitColor(l.vit);"
    pf_new = (
        "    const _pq=(S.profileQ||'').trim().toLocaleLowerCase('tr'), _pcat=S.profileCat||'all', _pn=(s)=>String(s||'').toLocaleLowerCase('tr');\n"
        "    const _pbc={}; this.LANGPROFILE.forEach(l=>{ const b=l.branch||'?'; _pbc[b]=(_pbc[b]||0)+1; });\n"
        "    const _pbl=Object.keys(_pbc).sort((a,b)=>a.localeCompare(b,'tr'));\n"
        "    const _pmk=(key,label,nn)=>{ const s=_pcat===key; return {key,label:label+(nn!=null?' \\u00b7 '+nn:''),go:()=>this.setState({profileCat:key}),style:`cursor:pointer;border:1px solid ${s?'#d98b4a':'rgba(33,29,23,.16)'};background:${s?'#d98b4a':'#fff'};color:${s?'#211d17':'#5f574b'};border-radius:13px;padding:4px 11px;font-size:11.5px;font-family:'IBM Plex Mono',monospace;font-weight:${s?600:400}`}; };\n"
        "    const profileCats=[_pmk('all','Tümü',this.LANGPROFILE.length)].concat(_pbl.map(b=>_pmk(b,b,_pbc[b])));\n"
        "    const _pfilt=this.LANGPROFILE.filter(l=>{ if(_pcat!=='all'&&(l.branch||'?')!==_pcat) return false; if(_pq && _pn(l.name).indexOf(_pq)<0) return false; return true; }).sort((a,b)=>((b.vit||0)-(a.vit||0))||a.name.localeCompare(b.name,'tr'));\n"
        "    const cards = _pfilt.map(l=>{\n      const sel = l.code===S.profileSel, vc = this.vitColor(l.vit);")
    if pf_old in html:
        html = html.replace(pf_old, pf_new, 1); npf += 1
    # (3) return'e yeni alanlar
    pf_ret_old = "    return { profileCards:cards,"
    pf_ret_new = ("    return { profileCards:cards, profileCats, profileTotal:this.LANGPROFILE.length,\n"
                  "      profileEmpty:cards.length===0, profileQ:S.profileQ||'', onProfileInput:(e)=>this.setState({profileQ:e.target.value}),")
    if pf_ret_old in html:
        html = html.replace(pf_ret_old, pf_ret_new, 1); npf += 1
    # (4) h2 stale "14 dil" → dinamik sayı + süzme ipucu
    pf_h2_old = '>14 dil · soldan kenar rengi = canlılık</h2>'
    pf_h2_new = '>Türk dilleri ve canlılık durumları</h2>'
    if pf_h2_old in html:
        html = html.replace(pf_h2_old, pf_h2_new, 1); npf += 1
    # (5) markup: liste üstüne arama kutusu + kol çipleri (sabit), liste ayrı kaydırılır
    pf_mk_old = ('          <div style="display:flex;flex-direction:column;gap:8px;max-height:600px;overflow:auto;padding-right:4px">\n'
                 '            <sc-for list="{{ profileCards }}" as="c" hint-placeholder-count="6">')
    pf_mk_new = ('          <div style="display:flex;flex-direction:column;gap:11px">\n'
                 '            <div style="display:flex;flex-direction:column;gap:9px">\n'
                 '              <input value="{{ profileQ }}" onInput="{{ onProfileInput }}" placeholder="Dil ara — ör. Nogay, Saha…" style="width:100%;padding:8px 12px;border:1.5px solid rgba(33,29,23,.18);border-radius:10px;background:#fff;font-size:13.5px;font-family:inherit;color:#211d17;outline:none">\n'
                 '              <div style="display:flex;gap:6px;flex-wrap:wrap">\n'
                 '                <sc-for list="{{ profileCats }}" as="pc"><button onClick="{{ pc.go }}" style="{{ pc.style }}">{{ pc.label }}</button></sc-for>\n'
                 '              </div>\n'
                 '            </div>\n'
                 '            <div style="display:flex;flex-direction:column;gap:8px;max-height:520px;overflow:auto;padding-right:4px">\n'
                 '            <sc-for list="{{ profileCards }}" as="c" hint-placeholder-count="6">')
    if pf_mk_old in html:
        html = html.replace(pf_mk_old, pf_mk_new, 1); npf += 1
    # (6) markup kapanış: ekstra wrapper div'i kapat + boş-durum
    pf_close_old = ('            </sc-for>\n'
                    '          </div>\n'
                    '          <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:18px;padding:30px 32px">')
    pf_close_new = ('            </sc-for>\n'
                    '            <sc-if value="{{ profileEmpty }}" hint-placeholder-val="{{ false }}"><div style="font-size:12.5px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace;padding:8px 2px">Eşleşen dil yok — aramayı/kolu değiştir.</div></sc-if>\n'
                    '            </div>\n'
                    '          </div>\n'
                    '          <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:18px;padding:30px 32px">')
    if pf_close_old in html:
        html = html.replace(pf_close_old, pf_close_new, 1); npf += 1
    print(f"  Dil Profilleri selektör A1 (ara + kol süzme): {npf}/6 yama")

    # ---- Kognat GENİŞ tarama (Savelyev 254) — Derin/Geniş toggle + lazy-fetch ----
    # 937KB'lık broad veri index.html'e GÖMÜLMEZ → dist'e kopyalanır, "Geniş" moduna geçince fetch'lenir.
    import shutil
    shutil.copyfile(DATA / "cognates_broad.json", UI / "dist" / "cognates_broad.json")
    nbr = 0
    # (1) state: cognateMode + broadReady (cog_default enjeksiyonu boşluklu: "cognateQ: ''")
    if "cognateKey: 'goz', cognateQ: '', cognateCat: 'all'," in html:
        html = html.replace("cognateKey: 'goz', cognateQ: '', cognateCat: 'all',",
                            "cognateKey: 'goz', cognateQ: '', cognateCat: 'all', cognateMode:'deep', broadReady:false,", 1); nbr += 1
    # (2) ensureBroad metodu (lazy fetch) — cognateVals'tan hemen önce
    if "  cognateVals(){" in html:
        html = html.replace("  cognateVals(){",
            "  ensureBroad(){ if(this._bl||this.COGNATES_BROAD) return; this._bl=true; "
            "fetch('cognates_broad.json').then(r=>r.json()).then(d=>{ this.COGNATES_BROAD=d.cognates; this.BROAD_CATS=d.categories; this._bl=false; this.setState({broadReady:true}); })"
            ".catch(()=>{ this._bl=false; this.setState({broadErr:true}); }); }\n\n  cognateVals(){", 1); nbr += 1
    # (3) cognateVals açılışı: SRC seçimi + mod toggle vals + anahtar fallback + yükleniyor erken-çıkış
    br_open_old = "    const S = this.state, c = this.COGNATES[S.cognateKey];\n    if (!c) return {};"
    br_open_new = (
        "    const S = this.state;\n"
        "    const _broad = S.cognateMode==='broad';\n"
        "    const SRC = _broad ? (this.COGNATES_BROAD||{}) : this.COGNATES;\n"
        "    const _modeVals = { cognateBroad:_broad,\n"
        "      goCogDeep:()=>this.setState({cognateMode:'deep',cognateCat:'all',cognateQ:'',cognateKey:'goz'}),\n"
        "      goCogBroad:()=>{ this.ensureBroad(); this.setState({cognateMode:'broad',cognateCat:'all',cognateQ:''}); },\n"
        "      cognateLoading:(_broad && !this.COGNATES_BROAD),\n"
        "      cognateModeNote:(_broad ? 'Savelyev · akademik yazım · 254 kavram × ≤32 dil' : 'ds18 · yerel yazı + IPA + ses kuralı · 11 kavram × 18 dil'),\n"
        "      cognateTableTitle:(_broad ? 'Dil dil biçim & segment' : 'Dil dil ses kuralı'),\n"
        "      deepBtnStyle:'cursor:pointer;border-radius:9px;padding:6px 15px;font-size:12.5px;font-family:inherit;border:1.5px solid '+(!_broad?'#211d17':'rgba(33,29,23,.18)')+';background:'+(!_broad?'#211d17':'#fff')+';color:'+(!_broad?'#f4f1ea':'#5f574b'),\n"
        "      broadBtnStyle:'cursor:pointer;border-radius:9px;padding:6px 15px;font-size:12.5px;font-family:inherit;border:1.5px solid '+(_broad?'#211d17':'rgba(33,29,23,.18)')+';background:'+(_broad?'#211d17':'#fff')+';color:'+(_broad?'#f4f1ea':'#5f574b') };\n"
        "    let _ck = S.cognateKey; let c = SRC[_ck]; if(!c){ _ck = Object.keys(SRC)[0]; c = SRC[_ck]; }\n"
        "    if (!c) return _modeVals;")
    if br_open_old in html:
        html = html.replace(br_open_old, br_open_new, 1); nbr += 1
    # (4) A1 filtre/sayaç this.COGNATES → SRC (aktif kaynak), seçili anahtar _ck
    for a, b in [("Object.entries(this.COGNATES).filter(([k,v])=>{", "Object.entries(SRC).filter(([k,v])=>{"),
                 ("Object.values(this.COGNATES).forEach(v=>{", "Object.values(SRC).forEach(v=>{"),
                 ("[_mkCat('all','Tümü',Object.keys(this.COGNATES).length)]", "[_mkCat('all','Tümü',Object.keys(SRC).length)]"),
                 ("      const sel = k===S.cognateKey;\n      return { key:k, label:v.gloss, sel,", "      const sel = k===_ck;\n      return { key:k, label:v.gloss, sel,")]:
        if a in html:
            html = html.replace(a, b, 1); nbr += 1
    # (5) return'e mod vals'ı kat
    if "    return { cognateKeys:keys, cognateCats," in html:
        html = html.replace("    return { cognateKeys:keys, cognateCats,",
                            "    return { ..._modeVals, cognateKeys:keys, cognateCats,", 1); nbr += 1
    # (6) markup: A1 kutusunun üstüne Derin/Geniş toggle + yükleniyor; tablo başlığı dinamik
    br_tog_anchor = '        <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:14px;padding:16px 18px">\n          <input value="{{ cognateQ }}"'
    br_tog_new = (
        '        <div style="display:flex;align-items:center;gap:9px;margin-bottom:13px;flex-wrap:wrap">\n'
        '          <button onClick="{{ goCogDeep }}" style="{{ deepBtnStyle }}">Derin · 11</button>\n'
        '          <button onClick="{{ goCogBroad }}" style="{{ broadBtnStyle }}">Geniş · 254</button>\n'
        '          <span style="font-size:11.5px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace">{{ cognateModeNote }}</span>\n'
        '        </div>\n'
        '        <sc-if value="{{ cognateLoading }}" hint-placeholder-val="{{ false }}"><div style="font-size:13px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace;padding:14px 2px">Geniş kognat verisi (254 kavram) yükleniyor…</div></sc-if>\n'
        + br_tog_anchor)
    if br_tog_anchor in html:
        html = html.replace(br_tog_anchor, br_tog_new, 1); nbr += 1
    # tablo başlığı: sabit "Dil dil ses kuralı" → dinamik
    if '>Dil dil ses kuralı</span>' in html:
        html = html.replace('>Dil dil ses kuralı</span>', '>{{ cognateTableTitle }}</span>', 1); nbr += 1
    # NOT: geometri kademeleri (n>24/n>12) + alternatif yarıçap artık deep_geo_new'de (R4) — ayrı geo3 yaması yok.
    print(f"  Kognat GENİŞ (Savelyev 254) lazy-fetch + Derin/Geniş toggle: {nbr}/11 yama")

    # ---- Ana sayfa hero: akıllı arama (dil→profil, kavram→kognat, kelime→analiz) + hızlı eylemler ----
    nhome = 0
    # (1) runSearch'i akıllı yönlendiriciye çevir (eskiden yalnız 5 küratörlü kelimeyi buluyordu)
    rs_old = ("  runSearch(){\n"
              "    const q = (this.state.query||'').trim().toLowerCase();\n"
              "    if (!q) return;\n"
              "    for (const id in this.WORDS){ const w = this.WORDS[id];\n"
              "      if ([w.gloss, w.surface, w.translit].some(s=>String(s).toLowerCase().includes(q))){\n"
              "        this.setState({ screen:'analiz', activeWordId:id, selMorphIdx:0, stripCount:0 }); return; } }\n"
              "  }")
    rs_new = ("  runSearch(){\n"
              "    const raw=(this.state.query||'').trim(); if(!raw) return; const n=s=>String(s||'').toLocaleLowerCase('tr'); const q=n(raw);\n"
              "    const lp=(this.LANGPROFILE||[]); const lm=lp.find(l=>n(l.name)===q)||(q.length>=3&&lp.find(l=>n(l.name).startsWith(q)));\n"
              "    if(lm){ this.setState({screen:'profile', profileSel:lm.code, profileQ:'', profileCat:'all'}); return; }\n"
              "    const ce=Object.entries(this.COGNATES||{}); const cm=ce.find(([k,v])=>n(v.gloss)===q)||(q.length>=3&&ce.find(([k,v])=>n(v.gloss).startsWith(q)));\n"
              "    if(cm){ this.setState({screen:'cognate', cognateMode:'deep', cognateKey:cm[0], cognateCat:'all', cognateQ:''}); return; }\n"
              "    for(const id in this.WORDS){ const w=this.WORDS[id]; if([w.gloss,w.surface,w.translit].some(s=>n(s).includes(q))){ this.setState({screen:'analiz', activeWordId:id, selMorphIdx:0, stripCount:0}); return; } }\n"
              "    this.setState({screen:'analiz'});\n"
              "  }")
    if rs_old in html:
        html = html.replace(rs_old, rs_new, 1); nhome += 1
    # (2) bağlam çubuğu arama placeholder'ı: kapsamı yansıt
    if 'placeholder="Kelime ara, Enter’a bas — örn. okuduk, ormanda, kızlar…"' in html:
        html = html.replace('placeholder="Kelime ara, Enter’a bas — örn. okuduk, ormanda, kızlar…"',
                            'placeholder="Dil, kavram ya da kelime ara — Çuvaşça · göz · okuduk"', 1); nhome += 1
    # (3) ana sayfaya belirgin hero arama + hızlı-eylem çipleri (giriş metninden sonra)
    chip = ("cursor:pointer;background:#fff;border:1px solid rgba(33,29,23,.16);border-radius:20px;"
            "padding:8px 15px;font-size:13.5px;font-family:inherit;color:#211d17")
    hero_anchor = ('        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:42px">\n'
                   '          <sc-for list="{{ homeCards }}" as="c" hint-placeholder-count="3">')
    hero_block = (
        '        <div style="margin-top:32px;max-width:580px">\n'
        '          <div style="position:relative">\n'
        '            <input value="{{ query }}" onInput="{{ onQuery }}" onKeyDown="{{ onSearchKey }}" placeholder="Dil, kavram ya da kelime ara — Çuvaşça · göz · okuduk" style="width:100%;padding:15px 16px 15px 48px;border:1.5px solid rgba(33,29,23,.18);border-radius:14px;background:#fff;font-size:16px;font-family:inherit;color:#211d17;outline:none;box-shadow:0 2px 12px rgba(33,29,23,.05)">\n'
        '            <span style="position:absolute;left:18px;top:50%;transform:translateY(-50%);color:#9a9082;font-size:18px">⌕</span>\n'
        '          </div>\n'
        '          <div style="margin-top:13px;display:flex;gap:8px;flex-wrap:wrap">\n'
        f'            <button onClick="{{{{ goHomeAnaliz }}}}" style="{chip}">Kelime çözümle</button>\n'
        f'            <button onClick="{{{{ goHomeCompare }}}}" style="{chip}">Dilleri karşılaştır</button>\n'
        f'            <button onClick="{{{{ goHomeProfile }}}}" style="{chip}">Dil profilleri</button>\n'
        f'            <button onClick="{{{{ goHomeAtlas }}}}" style="{chip}">Harita</button>\n'
        '          </div>\n'
        '        </div>\n\n'
        + hero_anchor)
    if hero_anchor in html:
        html = html.replace(hero_anchor, hero_block, 1); nhome += 1
    # (4) "ÖRNEK SÖZCÜK" bloğunu kaldır → yerine sade öne-çıkan yönlendirme (Dilin Kalbi)
    ornek_old = (
        '        <div style="margin-top:46px;display:flex;gap:14px;align-items:center;flex-wrap:wrap">\n'
        '          <span style="font-size:12.5px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace">ÖRNEK SÖZCÜK:</span>\n'
        '          <sc-for list="{{ wordChips }}" as="w" hint-placeholder-count="3">\n'
        '            <button onClick="{{ w.goAnaliz }}" style="cursor:pointer;background:#fff;border:1px solid rgba(33,29,23,.14);border-radius:20px;padding:8px 16px;font-size:14px;font-family:\'Spectral\',serif;font-weight:500;color:#211d17">{{ w.surface }} <span style="color:#9a9082;font-family:\'IBM Plex Sans\';font-size:12px">· {{ w.gloss }}</span></button>\n'
        '          </sc-for>\n'
        '        </div>')
    ornek_new = (
        '        <button onClick="{{ goHomeHeart }}" style="margin-top:42px;cursor:pointer;display:flex;align-items:center;gap:14px;background:#211d17;border:none;border-radius:14px;padding:18px 22px;text-align:left;width:100%;max-width:580px">\n'
        '          <span style="font-size:26px">❧</span>\n'
        '          <span style="display:flex;flex-direction:column;gap:3px">\n'
        '            <span style="font-family:\'Spectral\',serif;font-size:17px;font-weight:600;color:#f4f1ea">Nereden başlamalı? Çuvaşça — Dilin Kalbi</span>\n'
        '            <span style="font-size:13px;color:rgba(244,241,234,.6)">Türk dil ailesinin en erken ayrılan kolu; Ana Türkçeyi okumanın anahtarı.</span>\n'
        '          </span>\n'
        '          <span style="margin-left:auto;color:#d98b4a;font-size:15px">→</span>\n'
        '        </button>')
    if ornek_old in html:
        html = html.replace(ornek_old, ornek_new, 1); nhome += 1
    # (5) hızlı-eylem + öne-çıkan handler'ları renderVals'a kat
    if "      homeCards,\n" in html:
        html = html.replace("      homeCards,\n",
                            "      homeCards, goHomeAnaliz:this.go('analiz'), goHomeCompare:this.go('compare'), "
                            "goHomeProfile:this.go('profile'), goHomeAtlas:this.go('atlas'), goHomeHeart:this.go('heart'),\n", 1); nhome += 1
    print(f"  Ana sayfa hero (akıllı arama + hızlı eylem + öne-çıkan): {nhome}/5 yama")
    # küçük metin: "~MÖ 1.binyıl" → boşluklu ("1. binyıl" doğru kullanım = birinci binyıl)
    html = html.replace("~MÖ 1.binyıl", "~MÖ 1. binyıl")

    # NOT: A2 (Karşılaştır başlık sekmeye-duyarlı) D-bloğunda compareHeadline tanımında yapılır (tek kaynak).

    # ---- A3: ana sayfa (landing) güncelliği — kapsam sayıları VERİDEN, footer düzelt ----
    na3 = 0
    # (1) kenar çubuğu footer: kullanıcı isteği — "KOL · DİL · ÇUVAŞ ÇEKİRDEK" kaldırıldı, yalnız sürüm
    a3_foot_old = "5 KOL · 14 DİL · ÇUVAŞ ÇEKİRDEK · v0.4"
    a3_foot_new = "KÖKEN · v0.4"
    if a3_foot_old in html:
        html = html.replace(a3_foot_old, a3_foot_new, 1); na3 += 1
    # (2) ana sayfa kapsam şeridi KALDIRILDI (kullanıcı isteği — gereksiz bulundu).
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

    # ---- A6: Kaynaklar sayfası KATEGORİZE (yatay ölçekte çok kaynak gelecek → araç/veri/literatür/sentez) ----
    na6 = 0
    # (1) kindHue: 'sentez' rengi ekle (deepds), kullanılmayan 'geçici'yi nötrle
    a6_hue_old = "const kindHue = {veri:'#2f6fb0', 'araç':'#2f8a5b', 'literatür':'#8a5cc0', 'geçici':'#b86a2e'};"
    a6_hue_new = "const kindHue = {veri:'#2f6fb0', 'araç':'#2f8a5b', 'literatür':'#8a5cc0', 'sentez':'#b86a2e', 'geçici':'#9a9082'};"
    if a6_hue_old in html:
        html = html.replace(a6_hue_old, a6_hue_new, 1); na6 += 1
    # (2) sourceVals'e kategori grupları (sıralı: araç→veri→literatür→sentez; boş kategori atlanır)
    a6_grp_old = "    return { showSrcStrip:!!usage, pageSources,"
    a6_grp_new = ("    const CAT_ORDER=['araç','veri','literatür','sentez'];\n"
                  "    const CAT_LABEL={'araç':'Araçlar & motorlar','veri':'Veri setleri','literatür':'Akademik literatür','sentez':'Derin araştırma & derlemeler'};\n"
                  "    const sourceGroups = CAT_ORDER.map(cat=>{ const rows=sourceRows.filter(r=>r.kind===cat); return {cat, catLabel:CAT_LABEL[cat]||cat, hue:(kindHue[cat]||'#9a9082'), rows, count:rows.length}; }).filter(g=>g.count>0);\n"
                  "    return { showSrcStrip:!!usage, pageSources,")
    if a6_grp_old in html:
        html = html.replace(a6_grp_old, a6_grp_new, 1); na6 += 1
    a6_ret_old = "isSources:S.screen==='sources', sourceRows };"
    a6_ret_new = "isSources:S.screen==='sources', sourceRows, sourceGroups };"
    if a6_ret_old in html:
        html = html.replace(a6_ret_old, a6_ret_new, 1); na6 += 1
    # (3) markup: flat liste → kategori başlıklı gruplu liste (kart-içi tür rozeti kaldırıldı, başlık taşıyor)
    a6_mk_old = (
        '        <div style="display:flex;flex-direction:column;gap:10px">\n'
        '          <sc-for list="{{ sourceRows }}" as="s" hint-placeholder-count="6">\n'
        '            <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:13px;padding:16px 20px">\n'
        '              <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">\n'
        '                <span style="font-family:\'Spectral\',serif;font-size:17px;font-weight:600;color:#211d17">{{ s.label }}</span>\n'
        '                <span style="{{ s.kindStyle }}">{{ s.kind }}</span>\n'
        '                <span style="font-family:\'IBM Plex Mono\',monospace;font-size:11px;color:#9a9082;margin-left:auto">{{ s.lic }}</span>\n'
        '              </div>\n'
        '              <div style="font-size:13px;color:#5f574b;margin-top:5px">{{ s.detail }}</div>\n'
        '              <div style="font-size:12px;color:#9a9082;margin-top:8px;font-family:\'IBM Plex Mono\',monospace">KULLANIM: {{ s.used }}</div>\n'
        '            </div>\n'
        '          </sc-for>\n'
        '        </div>')
    a6_mk_new = (
        '        <div style="display:flex;flex-direction:column;gap:28px">\n'
        '          <sc-for list="{{ sourceGroups }}" as="g" hint-placeholder-count="4">\n'
        '            <div>\n'
        '              <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;border-bottom:1px solid rgba(33,29,23,.08);padding-bottom:8px">\n'
        '                <span style="width:9px;height:9px;border-radius:3px;background:{{ g.hue }}"></span>\n'
        '                <span style="font-family:\'Spectral\',serif;font-size:21px;font-weight:600;color:#211d17">{{ g.catLabel }}</span>\n'
        '                <span style="font-family:\'IBM Plex Mono\',monospace;font-size:12px;color:#9a9082">{{ g.count }} kaynak</span>\n'
        '              </div>\n'
        '              <div style="display:flex;flex-direction:column;gap:10px">\n'
        '                <sc-for list="{{ g.rows }}" as="s" hint-placeholder-count="3">\n'
        '                  <div style="background:#fbfaf6;border:1px solid rgba(33,29,23,.1);border-radius:13px;padding:16px 20px">\n'
        '                    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">\n'
        '                      <span style="font-family:\'Spectral\',serif;font-size:17px;font-weight:600;color:#211d17">{{ s.label }}</span>\n'
        '                      <span style="font-family:\'IBM Plex Mono\',monospace;font-size:11px;color:#9a9082;margin-left:auto">{{ s.lic }}</span>\n'
        '                    </div>\n'
        '                    <div style="font-size:13px;color:#5f574b;margin-top:5px">{{ s.detail }}</div>\n'
        '                    <div style="font-size:12px;color:#9a9082;margin-top:8px;font-family:\'IBM Plex Mono\',monospace">KULLANIM: {{ s.used }}</div>\n'
        '                  </div>\n'
        '                </sc-for>\n'
        '              </div>\n'
        '            </div>\n'
        '          </sc-for>\n'
        '        </div>')
    if a6_mk_old in html:
        html = html.replace(a6_mk_old, a6_mk_new, 1); na6 += 1
    # (4) intro metni: 'örnek/illüstratif' artık yok (F temizliği) → kategori + ölçek vurgulu güncel metin
    a6_intro_old = 'Akademik dürüstlük ilkesi: hiçbir veri kaynaksız değildir. Aşağıda her kaynak, lisansı ve <strong>hangi modüllerde kullanıldığı</strong> listelenir. “Örnek/illüstratif” işaretli alanlar, gerçek backend (Apertium + CLDF) bağlandığında değişecektir.'
    a6_intro_new = 'Akademik dürüstlük ilkesi: hiçbir veri kaynaksız değildir. Kaynaklar <strong>kategoriye göre</strong> düzenlenir; her biri lisansı ve <strong>hangi modüllerde kullanıldığıyla</strong> listelenir. Yatay ölçekte bu kütük büyüdükçe yeni kaynaklar ilgili kategoriye eklenir.'
    if a6_intro_old in html:
        html = html.replace(a6_intro_old, a6_intro_new, 1); na6 += 1

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
        + helpblk('cognate', '<strong>Nasıl okunur:</strong> Ortadaki daire, dilbilimcilerin yeniden kurduğu <strong>Ana Türkçe kök</strong>; çevresinde bu kökün bugünkü dillerdeki karşılıkları. Düz çizgi doğrudan kökteşi, <strong style="color:#b8602e">turuncu kesik çizgi</strong> ise o dilin kavramı farklı bir kökten — yani <strong>kognat boşluğundan</strong> — karşıladığını gösterir. <strong>Derin</strong> sekmesi 11 kavramı yerel yazı/IPA/ses kuralıyla, <strong>Geniş</strong> sekmesi Savelyev’in 254 kavramını gösterir. Bunlar küratörlü karşılaştırmalı veridir (canlı analiz değil); yazdığınız kelimenin kognatı otomatik üretilmez.')))
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
         "Karadeniz kuzeyinden Orta Asya bozkırlarına uzanan göçebe kol. Kazak, Tatar, Kırgız, Başkurt, Karakalpak, Nogay, Kumuk gibi geniş bir grup.",
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
    # Soy ağacına "nasıl okunur" alt-başlığı (kullanıcı: ne neye bağlı anlaşılmıyor)
    html = html.replace(
        '<div style="font-family:\'Spectral\',serif;font-weight:600;font-size:20px;margin-bottom:18px">Soy ağacı</div>',
        '<div style="font-family:\'Spectral\',serif;font-weight:600;font-size:20px;margin-bottom:4px">Soy ağacı</div>\n'
        '            <div style="font-size:12.5px;color:#5f574b;margin-bottom:16px;line-height:1.5;max-width:60ch">Soldan sağa okunur: en solda ortak ata, sağa gidildikçe daha geç ayrılan kollar. Girinti bir dalın hangi koldan türediğini gösterir. <span style="color:#9a9082">(Savelyev &amp; Robbeets 2020 Bayes ağacı)</span></div>', 1)

    # ---- R4 Uzaklık seçici: TABAN + KARŞILAŞTIRILAN dili YAN YANA kaydırmalı liste (tek format) ----
    nud = 0
    # (1) distLangOptions (taban) → distLangs ile aynı liste-buton formatı (nokta + ad)
    dlo_old = ("    const distLangOptions = Object.entries(this.LANGVEC).map(([code,d])=>{\n"
               "      const sel = code===S.distBase;\n"
               "      return { code, name:d.name, go:()=>pickBase(code),\n"
               "        style:`cursor:pointer;border:1.5px solid ${sel?'#211d17':'rgba(33,29,23,.14)'};background:${sel?'#211d17':'#fff'};color:${sel?'#f4f1ea':'#211d17'};border-radius:16px;padding:6px 12px;font-size:12.5px;font-family:inherit` };\n"
               "    });")
    dlo_new = ("    const distLangOptions = Object.entries(this.LANGVEC).map(([code,d])=>{\n"
               "      const sel = code===S.distBase; const col = this.BRANCHCOLOR[d.branch] || '#5f574b';\n"
               "      return { code, name:d.name, branch:d.branch, go:()=>pickBase(code),\n"
               "        style:`cursor:pointer;display:flex;align-items:center;gap:9px;text-align:left;border:1.5px solid ${sel?'#211d17':'rgba(33,29,23,.12)'};background:${sel?'#211d17':'#fff'};color:${sel?'#f4f1ea':'#211d17'};border-radius:10px;padding:8px 12px;font-size:13px;font-family:inherit`,\n"
               "        dot:`width:9px;height:9px;border-radius:50%;background:${col};flex-shrink:0` };\n"
               "    });")
    if dlo_old in html:
        html = html.replace(dlo_old, dlo_new, 1); nud += 1
    # (2) dış grid genişliği: 248px → 380px (iki liste yan yana sığsın)
    if 'grid-template-columns:248px 1fr;gap:30px;margin-top:26px;align-items:start' in html:
        html = html.replace('grid-template-columns:248px 1fr;gap:30px;margin-top:26px;align-items:start',
                            'grid-template-columns:380px 1fr;gap:26px;margin-top:26px;align-items:start', 1); nud += 1
    # (3) sol sütun: dikey yığın → iki YAN YANA kaydırmalı liste (aynı format, ~10 dil görünür)
    dsel_old = ('          <div style="display:flex;flex-direction:column;gap:7px">\n'
                '            <div style="font-size:11px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace;letter-spacing:.5px;margin-bottom:3px">TABAN DİL</div>\n'
                '            <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px">\n'
                '              <sc-for list="{{ distLangOptions }}" as="o" hint-placeholder-count="9"><button onClick="{{ o.go }}" style="{{ o.style }}">{{ o.name }}</button></sc-for>\n'
                '            </div>\n'
                '            <div style="font-size:11px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace;letter-spacing:.5px;margin-bottom:3px">KARŞILAŞTIRILAN DİL</div>\n'
                '            <sc-for list="{{ distLangs }}" as="l" hint-placeholder-count="5">\n'
                '              <button onClick="{{ l.go }}" style="{{ l.style }}"><span style="{{ l.dot }}"></span>{{ l.name }}<span style="{{ l.branchStyle }}">{{ l.branch }}</span></button>\n'
                '            </sc-for>\n'
                '          </div>')
    dsel_new = ('          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">\n'
                '            <div>\n'
                '              <div style="font-size:11px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace;letter-spacing:.5px;margin-bottom:7px">TABAN DİL</div>\n'
                '              <div style="display:flex;flex-direction:column;gap:5px;max-height:404px;overflow-y:auto;padding-right:4px">\n'
                '                <sc-for list="{{ distLangOptions }}" as="o" hint-placeholder-count="9"><button onClick="{{ o.go }}" style="{{ o.style }}"><span style="{{ o.dot }}"></span>{{ o.name }}</button></sc-for>\n'
                '              </div>\n'
                '            </div>\n'
                '            <div>\n'
                '              <div style="font-size:11px;color:#9a9082;font-family:\'IBM Plex Mono\',monospace;letter-spacing:.5px;margin-bottom:7px">KARŞILAŞTIRILAN DİL</div>\n'
                '              <div style="display:flex;flex-direction:column;gap:5px;max-height:404px;overflow-y:auto;padding-right:4px">\n'
                '                <sc-for list="{{ distLangs }}" as="l" hint-placeholder-count="5"><button onClick="{{ l.go }}" style="{{ l.style }}"><span style="{{ l.dot }}"></span>{{ l.name }}</button></sc-for>\n'
                '              </div>\n'
                '            </div>\n'
                '          </div>')
    if dsel_old in html:
        html = html.replace(dsel_old, dsel_new, 1); nud += 1
    print(f"  R4 Uzaklık seçici yan yana kaydırmalı: {nud}/3 yama")
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
    # NOT: Ses denklikleri kanıt sayıları (rot/lam/y) artık ds17 SOUND kartlarına build_sound_laws(ev) ile
    # gömülü (yukarıda). Eski 4-kart EVID enjeksiyonu kaldırıldı (yeni 7 kol-izoglosu kartı kullanılıyor).
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
    # ── Bölüm B: "Dil dil keşif" kategorisi — HER yaşayan master dili için doğrudan HF arama hub'ı ──
    # (yeni/küçük diller dahil). DÜRÜST: bunlar ARAMA linki — sonuç sayısı dilin dijital varlığını yansıtır,
    # iddia değil. HF kod eşlemesi: 639-1 olanlar kısa, diğerleri ISO 639-3 (HF facet'i çoğunu tanır).
    HF_CODE = {"tur": "tr", "azj": "az", "aze": "az", "tuk": "tk", "kaz": "kk", "kir": "ky",
               "uzn": "uz", "uzb": "uz", "uig": "ug", "tat": "tt", "bak": "ba", "chv": "cv"}
    disc_langs = []
    for L in sorted([m for m in master if m.get("era") == "living"], key=lambda m: (m["branch"], m["name"])):
        hc = HF_CODE.get(L["iso"], L["iso"])
        disc_langs.append({"name": f'{L["name"]} · {L["branch"]}', "links": [
            {"label": "HF modeller", "url": f"https://huggingface.co/models?language={hc}&sort=trending", "note": hc},
            {"label": "HF veri", "url": f"https://huggingface.co/datasets?language={hc}"},
        ]})
    eco["categories"].append({
        "key": "discover", "title": "Dil dil keşif",
        "desc": "Her yaşayan Türk dili için doğrudan HuggingFace arama girişi (model + veri). Sonuç sayısı "
                "dilin dijital varlığını yansıtır — bazı küçük dillerde boş çıkabilir; bu da dürüst bir sinyaldir. "
                "Küratörlü öne çıkanlar için diğer kategorilere bakın.",
        "hubs": [{"label": "HF · tüm modeller (trend)", "url": "https://huggingface.co/models?sort=trending"},
                 {"label": "HF · tüm veri setleri", "url": "https://huggingface.co/datasets"},
                 {"label": "Mozilla Common Voice", "url": "https://commonvoice.mozilla.org/datasets"}],
        "langs": disc_langs,
    })
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
                "eco_tools:S.ecoCat==='tools', eco_orgs:S.ecoCat==='orgs', eco_discover:S.ecoCat==='discover',")
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
        '          <p style="font-size:16px;line-height:1.7;color:rgba(244,241,234,.85);max-width:64ch;margin:0">Yaşayan tek <b>Oğur (Bulgar)</b> Türk dili. Türk dil ailesinden binlerce yıl önce ilk ayrılan kolun son temsilcisi — bu yüzden Ana Türkçeyi yeniden kurmada eşsiz bir anahtardır.</p>\n'
        '          <div style="display:flex;gap:26px;flex-wrap:wrap;margin-top:20px">\n'
        "            <div><div style=\"font-family:'Spectral',serif;font-size:24px;font-weight:700\">~740 bin</div><div style=\"font-size:11px;color:rgba(244,241,234,.55);font-family:'IBM Plex Mono',monospace\">KONUŞUR (2020)</div></div>\n"
        "            <div><div style=\"font-family:'Spectral',serif;font-size:24px;font-weight:700\">Oğur</div><div style=\"font-size:11px;color:rgba(244,241,234,.55);font-family:'IBM Plex Mono',monospace\">KOL</div></div>\n"
        "            <div><div style=\"font-family:'Spectral',serif;font-size:24px;font-weight:700\">EGIDS 6b</div><div style=\"font-size:11px;color:rgba(244,241,234,.55);font-family:'IBM Plex Mono',monospace\">TEHLİKEDE</div></div>\n"
        '          </div>\n'
        '        </div>\n'
        # neden paha biçilmez
        "        <h3 style=\"font-family:'Spectral',serif;font-size:24px;font-weight:600;margin:0 0 10px\">Neden paha biçilmez?</h3>\n"
        '        <p style="font-size:15px;line-height:1.75;color:#3f3a32;max-width:74ch;margin:0 0 28px">Çuvaşça, Ortak (Şaz) Türkçeden çok erken ayrıldığı için karşılıklı anlaşılabilirliği sıfıra yakındır. Ama tam da bu uzaklık onu değerli kılar: düzenli ses denklikleri (rotasizm, lambdasizm), Ana Türkçe ve hatta Transavrasya rekonstrüksiyonlarında bir <b>anahtar dil</b> yapar. İdil-Ural havzasında Fin-Ugor (Mari) ve Rusça ile yüzyıllarca temas, ona benzersiz areal özellikler kazandırmıştır.</p>\n'
        # ses kanunları
        "        <h3 style=\"font-family:'Spectral',serif;font-size:24px;font-weight:600;margin:0 0 6px\">Ses kanunları</h3>\n"
        '        <p style="font-size:13.5px;line-height:1.6;color:#5f574b;max-width:74ch;margin:0 0 14px">Ortak Türkçedeki bir ses, Çuvaşçada düzenli olarak başka bir sese karşılık gelir. Savelyev’in karşılaştırmalı kognat veri tabanında bu kuralların görüldüğü kökteş çifti sayısı: <b>36</b> rotasizm (*z↔r), <b>29</b> lambdasizm (*š↔l), <b>14</b> söz başı *y↔ś.</p>\n'
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
        "      {id:'history', label:'Tarih & Köken'},\n      {id:'heart', label:'Dilin Kalbi'},\n      {id:'about', label:'Hakkında'},", 1)
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
    print(f"  A3 landing footer + kart (kapsam şeridi kaldırıldı): {na3}/2 yama")
    print(f"  A5 Uzaklık radar kutusu kompakt + OKUMA sağ sütuna (denge): {na5}/3 yama")
    print(f"  A6 Kaynaklar sayfası kategorize (araç/veri/literatür/sentez): {na6}/5 yama")
    print(f"  Kopya düzeltmeleri: {nfix}")
    print(f"  Dil profili zenginleştirme (Wikipedia, çapraz-kontrollü): {nenrich} alan ({len(extra)} dil)")
    print(f"  Canlı API bağlama (Paradigma+Analiz): {nlive}/6 yama")


if __name__ == "__main__":
    main()
