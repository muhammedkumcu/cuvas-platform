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
        nodes = [{"lang": name, "word": langset[sid][2], "branch": branch, "shift": langset[sid][0] != dom}
                 for sid, name, branch in COG_DISP if sid in langset]
        gaps = [n["lang"] for n in nodes if n["shift"]]
        note = f"Proto-Türkçe kök {dom_root}. Aynı renk = aynı kognat seti; farklı düğüm = kognat boşluğu" + \
               (f" ({', '.join(gaps)})." if gaps else ".")
        out[key] = {"gloss": tr, "proto": dom_root, "note": note, "nodes": nodes}
        if first is None:
            first = key
    return out, first


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
        parts = [f"name:'{TR_NAME.get(iso, p['name'])}'", f"code:'{ISO_TO_PROFILE.get(iso, '')}'",
                 f"branch:'{p['branch']}'", f"x:{x}", f"y:{y}"]
        if iso == "chv":
            parts.append("hi:true")
        if y > 50:
            parts.append("below:true")
        rows.append("    {" + ", ".join(parts) + "},")
    return "MAP = [\n" + "\n".join(rows) + "\n  ];"


def main():
    html = SRC.read_text(encoding="utf-8")
    prof = {p["iso"]: p for p in json.load(open(DATA / "profiles.json", encoding="utf-8"))["profiles"]}
    lex = json.load(open(DATA / "distance.lexical.json", encoding="utf-8"))["matrix"]
    typ = json.load(open(DATA / "distance.typological.json", encoding="utf-8"))["matrix"]
    cog = json.load(open(DATA / "cognates.json", encoding="utf-8"))
    extra = json.load(open(DATA / "lang_extra.json", encoding="utf-8"))["languages"]
    intel = json.load(open(DATA / "intelligibility.json", encoding="utf-8"))["intel"]

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

    # canlı API tabanı (sonraki adımda Analiz/Paradigma bağlanacak)
    if "KOKEN_API" not in html:
        html = html.replace("class Component extends DCLogic {",
                            f"class Component extends DCLogic {{\n  KOKEN_API = '{API}';", 1)

    # Harita ← gerçek Glottolog koordinatları (şematik projeksiyon)
    new_map = build_map(prof)
    html, nmap = re.subn(r"MAP = \[.*?\n  \];", lambda m: new_map, html, flags=re.DOTALL)
    # Harita düğümü → o dilin profiline git (mapNodes'a go + düğümü tıklanabilir yap)
    html = html.replace("        return { name:m.name, branch:m.branch, col,",
                        "        return { name:m.name, branch:m.branch, col, go:()=>this.setState({screen:'profile', profileSel:m.code}),", 1)
    html = html.replace('<div style="{{ n.dotStyle }}">',
                        '<div onClick="{{ n.go }}" style="cursor:pointer;{{ n.dotStyle }}">', 1)

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
        html = html.replace("cognateKey: 'kiz',", f"cognateKey: '{cog_default}',", 1)

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
    live.append(("    paradigmRoot: 'hĕr',", "    paradigmRoot: 'hĕr',\n    apiParadigm: {}, apiWord: null, searchLang: 'chv', paradigmFree: null, paradigmFreeQ: '',"))
    # küratörlü kök seçilince serbest çekimi temizle
    live.append(("        go:()=>this.setState({paradigmRoot:k}),", "        go:()=>this.setState({paradigmRoot:k, paradigmFree:null}),"))
    # paradigmVals return: serbest çekim (herhangi bir kök, seçili dil) + handler'lar
    live.append((
        "    return { paradigmRoots:roots, paradigmIsVerb:isVerb, paradigmIsNoun:!isVerb, paradigmRows:rows,\n"
        "      paradigmTitle:this.disp(p.root, p.rootLat), paradigmGloss:`“${p.gloss}”`,\n"
        "      paradigmSub: isVerb ? (p.label+' · şahıs çekimi') : 'Ad çekimi · hâl × sayı' };",
        "    const F = this.state.paradigmFree;\n"
        "    const cF = (s)=> s ? [{ text:this.disp(s), hue:this.hue('kök'), bg:this.hueBg('kök'), border:this.hueBorder('kök') }] : null;\n"
        "    const freeRows = (F && Array.isArray(F.rows)) ? F.rows.map(r=>({ caseLabel:r.case_tr, tag:(r.case||'').toUpperCase(), sg:cF(r.sg), pl:cF(r.pl), trSg:'', trPl:'' })) : null;\n"
        "    const LNp = {chv:'Çuvaşça',tur:'Türkçe',aze:'Azerice',kaz:'Kazakça',kir:'Kırgızca',uzb:'Özbekçe',uig:'Uygurca',tat:'Tatarca',bak:'Başkurtça',sah:'Yakutça'};\n"
        "    return { paradigmRoots:roots, paradigmIsVerb:isVerb && !freeRows, paradigmIsNoun:(!isVerb)||!!freeRows, paradigmRows: freeRows||rows,\n"
        "      paradigmTitle: freeRows ? this.disp(F.lemma) : this.disp(p.root, p.rootLat),\n"
        "      paradigmGloss: freeRows ? ('· '+F.langName) : `“${p.gloss}”`,\n"
        "      paradigmSub: freeRows ? ('canlı apertium çekimi · '+F.langName) : (isVerb ? (p.label+' · şahıs çekimi') : 'Ad çekimi · hâl × sayı'),\n"
        "      paradigmFreeQ: this.state.paradigmFreeQ||'',\n"
        "      onParadigmFreeInput:(e)=>this.setState({paradigmFreeQ:e.target.value}),\n"
        "      onParadigmFreeKey:(e)=>{ if(e.key!=='Enter') return; const lemma=(this.state.paradigmFreeQ||'').trim(); if(!lemma) return; const lg=this.state.searchLang||'chv'; fetch(this.KOKEN_API+'/paradigm/'+lg+'/'+encodeURIComponent(lemma)).then(r=>r.json()).then(d=>this.setState({paradigmFree:{lemma, langName:(LNp[lg]||lg), rows:(d&&d.rows)||[]}})).catch(()=>{}); } };"))
    # paradigma: serbest kök girişi ÜSTTE (arama düşük kalmasın) + örnekler ÖRNEK olarak etiketli
    live.append((
        '        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:18px">\n          <sc-for list="{{ paradigmRoots }}"',
        '        <div style="display:flex;align-items:center;gap:10px;margin-top:18px;flex-wrap:wrap">\n'
        '          <input value="{{ paradigmFreeQ }}" onInput="{{ onParadigmFreeInput }}" onKeyDown="{{ onParadigmFreeKey }}" placeholder="Bir kök yaz + Enter — sağ üstteki dilde canlı çekim" style="flex:1;min-width:300px;max-width:520px;padding:12px 15px;border:1.5px solid rgba(33,29,23,.18);border-radius:10px;background:#fff;font-size:15px;font-family:inherit;color:#211d17;outline:none">\n'
        '        </div>\n'
        '        <div style="font-size:11px;letter-spacing:1px;color:#9a9082;margin-top:18px;font-family:monospace">ÖRNEK KÖKLER (Çuvaşça)</div>\n'
        '        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">\n          <sc-for list="{{ paradigmRoots }}"'))
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
    # 5) runSearch(): eşleşme yoksa canlı /analyze
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
        "    const word = (this.state.query||'').trim();\n"
        "    const LN = {chv:'Çuvaşça',tur:'Türkçe',aze:'Azerice',kaz:'Kazakça',kir:'Kırgızca',uzb:'Özbekçe',uig:'Uygurca',tat:'Tatarca',bak:'Başkurtça',sah:'Yakutça'}; const lg = this.state.searchLang||'chv';\n"
        "    const TT = {n:'kök',v:'kök',pl:'çokluk',nom:'hâl',gen:'hâl',dat:'hâl',acc:'hâl',loc:'hâl',abl:'hâl',ins:'hâl',px1sg:'iyelik',px2sg:'iyelik',px3sp:'iyelik',pres:'zaman',past:'zaman',fut:'zaman',p1:'kişi',p2:'kişi',p3:'kişi'};\n"
        "    fetch(this.KOKEN_API+'/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:lg,word})}).then(r=>r.json()).then(d=>{\n"
        "      const a = (d.analyses&&d.analyses[0])||null;\n"
        "      const ms = a ? [{text:a.lemma, tag:'KÖK', type:'kök', label:'kök (apertium FST)', gloss:a.lemma, gItem:a.lemma, note:'Apertium morfolojik çözümlemesi.'}]\n"
        "        .concat((a.tags||[]).map(t=>({text:t, tag:String(t).toUpperCase(), type:(TT[t]||'kök'), label:'etiket: '+t, gloss:t, gItem:t, note:'Apertium etiketi.'})))\n"
        "        : [{text:word, tag:'?', type:'kök', label:'çözümlenemedi', gloss:'?', gItem:word, note:'Apertium bu biçimi tanımadı.'}];\n"
        "      const apiWord = {lang:'cv', langName:(LN[lg]||lg)+' · canlı FST', surface:word, translit:'', gloss:(a?('apertium: '+a.raw):'çözümlenemedi'), morphemes:ms, cognates:[]};\n"
        "      this.setState({ apiWord, activeWordId:'__api', screen:'analiz', selMorphIdx:0, stripCount:0 });\n"
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

    # --- Analiz DİL SEÇİCİ: bağlam çubuğuna select; Analiz seçili dilde herhangi bir kelimeyi çözer ---
    sel_langs = [("chv", "Çuvaşça"), ("tur", "Türkçe"), ("aze", "Azerice"), ("kaz", "Kazakça"),
                 ("kir", "Kırgızca"), ("uzb", "Özbekçe"), ("uig", "Uygurca"), ("tat", "Tatarca"),
                 ("bak", "Başkurtça"), ("sah", "Yakutça")]
    opts = "".join(f'<option value="{c}">{n}</option>' for c, n in sel_langs)
    sel = ('<select value="{{ searchLang }}" onInput="{{ onSearchLang }}" title="Analiz dili" '
           'style="background:#fff;border:1px solid rgba(33,29,23,.16);border-radius:9px;padding:10px 8px;'
           'font-size:13px;font-family:inherit;color:#211d17;cursor:pointer">' + opts + '</select>')
    nsel = 0
    if '<div style="margin-left:auto;display:flex;align-items:center;gap:10px">' in html:
        html = html.replace('<div style="margin-left:auto;display:flex;align-items:center;gap:10px">',
                            sel + '\n      <div style="margin-left:auto;display:flex;align-items:center;gap:10px">', 1)
        html = html.replace("      navGroups, wordChips, screenTag:tag, query:S.query,",
                            "      navGroups, wordChips, screenTag:tag, query:S.query, searchLang:S.searchLang, onSearchLang:(e)=>this.setState({searchLang:e.target.value}),", 1)
        nsel = 1
    print(f"  Analiz dil seçici: {nsel}")

    # --- DENETİM DÜZELTMELERİ (görünür taraftaki sabit/eskimiş/tutarsız öğeler) ---
    audit = [
        # paradigma başlığı artık dinamik (herhangi dilde çekim)
        ("PARADİGMA GEZGİNİ · Çuvaşça", "PARADİGMA GEZGİNİ · {{ paradigmLang }}"),
        ("paradigmFreeQ: this.state.paradigmFreeQ||'',",
         "paradigmLang: (this.state.paradigmFree && Array.isArray(this.state.paradigmFree.rows)) ? this.state.paradigmFree.langName : 'Çuvaşça', paradigmFreeQ: this.state.paradigmFreeQ||'',"),
        # öğrenen/uzman KALDIR: her şey görünür (isExpert hep true) + toggle'ı sil
        ("isExpert:S.mode==='expert'", "isExpert: true"),
        ('        <div style="display:flex;background:#ece7dc;border-radius:9px;padding:3px">\n'
         '          <sc-for list="{{ modeToggle }}" as="m" hint-placeholder-count="2"><button onClick="{{ m.go }}" style="{{ m.style }}">{{ m.label }}</button></sc-for>\n'
         '        </div>\n', ''),
        # 'UZMAN MODU' etiketi mod kalkınca anlamsız → nötr
        ("UZMAN MODU", "HAM ÇIKTI"),
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

    (DIST / "index.html").write_text(html, encoding="utf-8")
    shutil.copy(UI / "support.js", DIST / "support.js")

    print(f"dist/index.html yazıldı.")
    print(f"  LANGPROFILE canlılık (Glottolog AES): {len(changed)} dil")
    print(f"  MAP harita koordinatları (Glottolog): {nmap} blok, {new_map.count('{name')} dil")
    print(f"  Uzaklık matrisleri (Savelyev+WALS+coğrafi): val patch={ndist}, REAL_DIST enjekte")
    print(f"  Kognat Ağı (SavelyevTurkic): {ncog} blok, {len(cog_obj)} kavram (default '{cog_default}')")
    print(f"  Kopya düzeltmeleri: {nfix}")
    print(f"  Dil profili zenginleştirme (Wikipedia, çapraz-kontrollü): {nenrich} alan ({len(extra)} dil)")
    print(f"  Canlı API bağlama (Paradigma+Analiz): {nlive}/6 yama")


if __name__ == "__main__":
    main()
