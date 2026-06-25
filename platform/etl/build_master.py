# -*- coding: utf-8 -*-
"""
KÖKEN — Master dil envanteri (yatay ölçek temeli).
Kaynak: deepsearch 11 (arastirma/_envanter11.json) + Glottolog CLDF (kanonik ad/koordinat çapraz-kontrol).
Çıktı: platform/data/languages.master.json  (47 dil/lehçe/tarihsel form; era etiketli).
İlke: koordinat/ad GLOTTOLOG'tan (otorite); kol/era/konuşur/Bayes-notu deepsearch 11'den; tutarsızlık RAPOR edilir.
Çalıştır: python platform/etl/build_master.py   (pdfminer/pdfplumber GEREKMEZ — _envanter11.json hazır.)
"""
import csv, json, re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "arastirma" / "_envanter11.json"
GLOT = ROOT / "sources" / "glottolog-cldf" / "cldf" / "languages.csv"
OUT = ROOT / "platform" / "data" / "languages.master.json"

# Temiz Türkçe adlar (standart, yerleşik dil adları — ISO 639-3 anahtarlı)
TR_NAME = {
    "tur": "Türkçe", "gag": "Gagavuzca", "bgx": "Balkan Gagavuzcası", "azj": "Azerbaycanca",
    "azb": "Güney Azerbaycanca", "tuk": "Türkmence", "kmz": "Horasan Türkçesi", "qxq": "Kaşkayca",
    "slr": "Salarca", "crh": "Kırım Tatarcası", "uum": "Urumca", "kaz": "Kazakça", "kir": "Kırgızca",
    "tat": "Tatarca", "bak": "Başkurtça", "kaa": "Karakalpakça", "krc": "Karaçay-Balkarca",
    "kum": "Kumukça", "nog": "Nogayca", "kdr": "Karayca", "jct": "Kırımçak", "sty": "Sibirya Tatarcası",
    "alt": "Altayca (Güney)", "xzm": "Harezm Türkçesi", "qwm": "Codex Cumanicus Kıpçakçası",
    "uzn": "Özbekçe", "uzs": "Güney Özbekçe", "uig": "Uygurca", "aib": "Eynuca", "ili": "İli Türki",
    "oui": "Eski Uygurca", "xqa": "Karahanlı Türkçesi", "chg": "Çağatayca", "sah": "Yakutça (Saha)",
    "dlg": "Dolganca", "tyv": "Tuvaca", "kim": "Tofaca", "kjh": "Hakasça", "cjs": "Şorca",
    "atv": "Altayca (Kuzey)", "clw": "Çulımca", "ybe": "Sarı Uygurca", "chv": "Çuvaşça",
    "xbo": "İdil Bulgarcası", "zkz": "Hazarca", "klj": "Halaçça", "otk": "Eski Türkçe (Orhun)",
}

# Mevcut 14 MVP dilinin SOURCED inline-kart notu (UI'dan taşındı) — iso anahtarlı
NOTE = {
    "tur": "Batı Oğuz; en çok konuşulan Türk dili.",
    "azj": "Merkez Oğuz; ayırt edici açık ə sesi.",
    "tuk": "Doğu Oğuz; Ana Türkçe uzun ünlülerini korur.",
    "chv": "Yaşayan TEK Oğur dili; rotasizm *z>r, lambdasizm *š>l.",
    "tat": "İdil-Ural Kıpçakçası; tarihsel ünlü kayması (söz→süz).",
    "bak": "Peltek /θ/(ҫ), /ð/(ҙ) ve söz başı /h/ sesleri.",
    "kaz": "Katı ünlü uyumu; 12 çoğul eki varyantı.",
    "kir": "Katı dudak uyumu; Manas destanı dili.",
    "uig": "Karluk; Arap yazısı tüm ünlüleri gösterir.",
    "sah": "Kuzey Sibirya; genitif/lokatif hâllerini yitirdi.",
    "tyv": "Gırtlaksı (kargyraa) ünlüler; höömey geleneği.",
    "kjh": "Islıklı sibilantlar (ş→s); 10 gramatik hâl.",
    "klj": "Argu kolu; söz başı *h-'yi korur — arkaik 'müze'.",
    "cjs": "Ciddi tehlikede; Yenisey (Mrassu/Kondoma) lehçeleri.",
}

# Glottocode düzeltmeleri (deepsearch 11 tablosunda hatalı/eksik çıkanlar — Glottolog'tan doğru):
GLOT_FIX = {"qxq": "qash1234", "oui": "oldu1239", "qwm": "cuma1241", "aib": "ayns1238"}


def load_glottolog():
    by_iso, by_glot = {}, {}
    with open(GLOT, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rec = {"name": r["Name"], "lat": r["Latitude"], "lon": r["Longitude"],
                   "glot": r["Glottocode"], "iso": r["ISO639P3code"], "level": r["Level"]}
            if r["ISO639P3code"]:
                by_iso[r["ISO639P3code"]] = rec
            by_glot[r["Glottocode"]] = rec
    return by_iso, by_glot


def num(x):
    try:
        return round(float(x), 2)
    except (TypeError, ValueError):
        return None


# Mevcut 14 MVP dilinin küratörlü konuşur-etiketi (UI'dan); diğerleri ds11 sayısından hesaplanır.
SPK_CURATED = {"tur": "~85 milyon", "azj": "~24 milyon", "tuk": "~7 milyon", "chv": "~740 bin",
               "tat": "~5 milyon", "bak": "~1,2 milyon", "kaz": "~14 milyon", "kir": "~5 milyon",
               "uig": "~10 milyon", "sah": "~450 bin", "tyv": "~280 bin", "kjh": "~40 bin",
               "klj": "~20 bin", "cjs": "~2,8 bin"}


def spk_label(iso, raw, era):
    """ds11 konuşur metnindeki sayıyı (sarma-boşluklu) temiz '~N milyon/bin' etiketine çevir."""
    if iso in SPK_CURATED:
        return SPK_CURATED[iso]
    if era != "living":
        return "tarihsel (ölü dil)"
    m = re.match(r"~?\s*([\d.\s]+)", raw or "")
    if not m:
        return ""
    digits = re.sub(r"[.\s]", "", m.group(1))
    if not digits.isdigit():
        return ""
    n = int(digits)
    if n >= 1_000_000:
        v = n / 1_000_000
        return f"~{int(v)} milyon" if v == int(v) else f"~{v:.1f}".replace(".", ",") + " milyon"
    if n >= 1000:
        return f"~{n // 1000} bin"
    return f"~{n}"


def main():
    inv = json.load(open(INV, encoding="utf-8"))
    by_iso, by_glot = load_glottolog()
    out, report = [], []
    for e in inv:
        iso = e["iso"]
        glot = GLOT_FIX.get(iso, e["glot"])
        g = by_iso.get(iso) or by_glot.get(glot)
        # era düzeltme: Tarihi/Ölü tür → historical (proto yalnız Ortak kök)
        era = e["era"]
        if e["maj"] == "Ortak":
            era = "proto"
        elif "Tarihi" in e["type"] or "Ölü" in e["type"]:
            era = "historical"
        else:
            era = "living"
        # koordinat: CANLI dillerde Glottolog otorite (nokta-konum); TARİHSEL/PROTO dillerde Glottolog
        # güvenilmez (yanlış glottocode/rekonstrüksiyon — ör. xzm→Letonya, otk→İran) → ds11 tarihsel bölge.
        lat_g, lon_g = (num(g["lat"]), num(g["lon"])) if g else (None, None)
        lat_i, lon_i = num(e["lat_inv"]), num(e["lon_inv"])
        if era == "living":
            lat = lat_g if lat_g is not None else lat_i
            lon = lon_g if lon_g is not None else lon_i
            coord_src = "glottolog" if lat_g is not None else ("deepsearch11" if lat_i is not None else "YOK")
        else:
            lat = lat_i if lat_i is not None else lat_g
            lon = lon_i if lon_i is not None else lon_g
            coord_src = "deepsearch11(tarihsel)" if lat_i is not None else ("glottolog" if lat_g is not None else "YOK")
        # tutarsızlık raporu (>3° fark — yalnız canlı dillerde anlamlı)
        if era == "living" and lat_g is not None and lat_i is not None and (abs(lat_g - lat_i) > 3 or abs((lon_g or 0) - (lon_i or 0)) > 3):
            report.append(f"  ~ koord farkı {iso} ({TR_NAME.get(iso,'?')}): glottolog({lat_g},{lon_g}) [kullanılan] vs ds11({lat_i},{lon_i})")
        if not g:
            report.append(f"  ! Glottolog'ta bulunamadı {iso}/{glot} ({TR_NAME.get(iso,'?')}) — koordinat ds11'den")
        out.append({
            "iso": iso, "glottocode": glot, "name": TR_NAME.get(iso, e["name_inv"]),
            "name_en": (g["name"] if g else ""), "branch": e["maj"], "branch_detail": e["branch_detail"],
            "lat": lat, "lon": lon, "coord_src": coord_src, "era": era, "type": e["type"],
            "speakers": spk_label(iso, e["speakers"], era), "speakers_raw": e["speakers"],
            "vitality": e["vit"], "script": e["script"],
            "note": NOTE.get(iso, ""), "bayes": e["bayes"],
        })
    meta = {
        "_meta": {
            "title": "KÖKEN master dil envanteri (yatay ölçek temeli)",
            "source": "deepsearch 11 (envanter: kol/era/konuşur/Bayes) + Glottolog CLDF v5 (kanonik ad/koordinat, çapraz-kontrol)",
            "license": "Glottolog CC BY 4.0; deepsearch derleme (atıflı)",
            "count": len(out), "living": sum(1 for x in out if x["era"] == "living"),
            "historical": sum(1 for x in out if x["era"] == "historical"),
            "proto": sum(1 for x in out if x["era"] == "proto"),
            "note": "Koordinat/ad GLOTTOLOG otoritesinden; kol/era/konuşur/Bayes deepsearch 11'den. GLOT_FIX: ds11 glottocode hataları düzeltildi.",
        },
        "languages": out,
    }
    json.dump(meta, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"languages.master.json yazıldı: {len(out)} dil "
          f"(canlı {meta['_meta']['living']}, tarihsel {meta['_meta']['historical']}, proto {meta['_meta']['proto']})")
    print("ÇAPRAZ-KONTROL RAPORU:" if report else "Çapraz-kontrol: tutarsızlık yok.")
    print("\n".join(report))


if __name__ == "__main__":
    main()
