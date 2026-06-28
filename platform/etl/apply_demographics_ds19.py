# -*- coding: utf-8 -*-
"""R5b-2 — 47-dil KAYNAKLI demografi tablosu → languages.master.json

Kaynak: arastirma/19-Türk Dilleri Derin Profil Araştırması.pdf, Bölüm 3
(sayfa 17-21): "Türk Dilleri Küresel Canlılık ve Konuşur Demografisi Tablosu (47 Dil)".
Tablo Lewis & Simons (2010) EGIDS + Ethnologue + UNESCO Tehlikedeki Diller Atlası +
Glottolog çapraz-referansıyla derlenmiş (PDF içi atıf). Buradaki her satır o tablodan
BİREBİR aktarılmıştır (uydurma yok). Tabloda ISO'su olmayan alt-lehçeler (Horasan,
Dobruca Tatarcası, Soyot/Teleüt/Telengit/Tubalar/Çelkan) master anahtarlarıyla eşleşmez;
master'da karşılığı olanlar işlenir.

Tablo ISO -> master ISO eşlemesi: uzb->uzn, aze->azj, Horasan Türkçesi(ISO yok)->kmz,
alt->alt (master'daki "Altayca (Güney)"). Tabloda satırı OLMAYAN master dilleri
(azb Güney Azerbaycanca, uzs Güney Özbekçe, atv Altayca-Kuzey) DOKUNULMADAN bırakılır.

ÇUVAŞÇA istisnası: tablo Ethnologue 2019 = 1.2M (etnik/eski) verir; biz projede 2020
Rusya nüfus sayımı L1 = 740 bin (≈%30 düşüş) anlatısını kullanıyoruz (Dilin Kalbi sayfası).
Daha güncel + L1-spesifik olduğu için chv = 740 bin / 2020 / Rusya Nüfus Sayımı korunur.

Yazar alanlar (her dile): speakers (temiz, insan-okunur), speakers_year, speakers_source,
egids (kod), egids_label (İng., faithful), unesco (TR). vitality DEĞİŞMEZ (renk hattı).
"""
import json
import pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
MASTER = DATA / "languages.master.json"

# UNESCO İng. -> TR (faithful İng. master'da egids_label/unesco_en'de değil; TR gösterim)
UNESCO_TR = {
    "Normal": "Güvende", "Vulnerable": "Hassas", "Threatened": "Tehdit altında",
    "Definitely endangered": "Kesin tehlikede", "Severely endangered": "Ciddi tehlikede",
    "Critically endangered": "Çok kritik tehlikede", "Extinct": "Ölü",
}

# master_iso: (speakers, year, source, egids_code, egids_label_en, unesco_en)
# — hepsi ds19 Bölüm 3 tablosundan birebir.
DEMO = {
    "tur": ("83 milyon", "2019", "Ethnologue", "1", "National", "Normal"),
    "uzn": ("32 milyon", "2019", "Ethnologue", "1", "National", "Normal"),
    "azj": ("30 milyon", "2019", "Ethnologue", "1", "National", "Normal"),
    "kaz": ("19 milyon", "2019", "Ethnologue", "1", "National", "Normal"),
    "uig": ("13 milyon", "2019", "Ethnologue", "2", "Provincial", "Normal"),
    "tuk": ("7 milyon", "2019", "Ethnologue", "1", "National", "Normal"),
    "tat": ("5,5 milyon", "2019", "Ethnologue", "2", "Provincial", "Normal"),
    "kir": ("5 milyon", "2019", "Ethnologue", "1", "National", "Normal"),
    "bak": ("1,5 milyon", "2019", "Ethnologue", "2", "Provincial", "Vulnerable"),
    # chv: tablo 1.2M (2019 Ethnologue) yerine 2020 Rusya sayımı L1 740 bin (proje anlatısı)
    "chv": ("740 bin", "2020", "Rusya Nüfus Sayımı", "2", "Provincial", "Vulnerable"),
    "qxq": ("1 milyon", "2021", "Ethnologue", "6a", "Vigorous", "Normal"),
    "kmz": ("1 milyon", "2019", "Ethnologue", "6b", "Threatened", "Vulnerable"),
    "kaa": ("650 bin", "2019", "Ethnologue", "2", "Provincial", "Normal"),
    "crh": ("600 bin", "2019", "Ethnologue", "6b", "Threatened", "Severely endangered"),
    "kum": ("450 bin", "2019", "Ethnologue", "5", "Developing", "Vulnerable"),
    "krc": ("400 bin", "2019", "Ethnologue", "5", "Developing", "Vulnerable"),
    "sah": ("400 bin", "2019", "Ethnologue", "2", "Provincial", "Vulnerable"),
    "bgx": ("331 bin", "2022", "Campbell vd.", "7", "Shifting", "Threatened"),
    "tyv": ("300 bin", "2019", "Ethnologue", "2", "Provincial", "Vulnerable"),
    "uum": ("190 bin", "2000", "Ethnologue (etnik nüfus)", "8a–8b", "Moribund / Nearly extinct", "Definitely endangered"),
    "gag": ("150 bin", "2019", "Ethnologue", "3", "Trade", "Critically endangered"),
    "sty": ("100 bin", "2019", "Ethnologue", "6b", "Threatened", "Definitely endangered"),
    "nog": ("100 bin", "2019", "Ethnologue", "5", "Developing", "Definitely endangered"),
    "slr": ("70 bin", "2019", "Ethnologue", "6b", "Threatened", "Vulnerable"),
    "alt": ("60 bin", "2019", "Ethnologue", "2", "Provincial", "Severely endangered"),
    "kjh": ("50 bin", "2019", "Ethnologue", "2", "Provincial", "Definitely endangered"),
    "klj": ("20 bin", "2019", "Ethnologue", "6b", "Threatened", "Vulnerable"),
    "aib": ("6 bin", "2019", "Ethnologue", "6b", "Threatened", "Critically endangered"),
    "ybe": ("5 bin", "2019", "Ethnologue", "8a", "Moribund", "Severely endangered"),
    "cjs": ("3 bin", "2019", "Ethnologue", "6b", "Threatened", "Severely endangered"),
    "dlg": ("1.000", "2019", "Ethnologue", "6b", "Threatened", "Definitely endangered"),
    "jct": ("200", "2007", "Ethnologue", "8b", "Nearly extinct", "Critically endangered"),
    "ili": ("~120", "1982", "Hahn & Salminen", "8a", "Moribund", "Severely endangered"),
    "kim": ("~40", "2007", "ELP / Ethnologue", "8b", "Nearly extinct", "Critically endangered"),
    "kdr": ("~50", "2006", "Kocaoğlu / Ethnologue", "8b", "Nearly extinct", "Critically endangered"),
    "clw": ("44", "2010", "Rus Nüfus Sayımı", "8b", "Nearly extinct", "Critically endangered"),
    # Tarihsel / ölü diller (tablo: "Kaynak Yok (Ölü dil)", EGIDS 10 Extinct)
    "otk": ("", "", "", "10", "Extinct", "Extinct"),
    "oui": ("", "", "", "10", "Extinct", "Extinct"),
    "xqa": ("", "", "", "10", "Extinct", "Extinct"),
    "xzm": ("", "", "", "10", "Extinct", "Extinct"),
    "qwm": ("", "", "", "10", "Extinct", "Extinct"),
    "xbo": ("", "", "", "10", "Extinct", "Extinct"),
    "zkz": ("", "", "", "10", "Extinct", "Extinct"),
    "chg": ("", "", "", "10", "Extinct", "Extinct"),
}

# tabloda satırı olmayan master dilleri (dokunulmaz, ama not düşülür)
NOT_IN_TABLE = {"azb", "uzs", "atv"}


def main():
    doc = json.load(open(MASTER, encoding="utf-8"))
    applied, skipped, missing = [], [], []
    seen = set()
    for L in doc["languages"]:
        iso = L["iso"]
        if iso in DEMO:
            sp, yr, src, eg, eg_lab, un_en = DEMO[iso]
            L["speakers"] = sp if sp else (L.get("speakers") or "")
            L["speakers_year"] = yr
            L["speakers_source"] = src
            L["egids"] = eg
            L["egids_label"] = eg_lab
            L["unesco"] = UNESCO_TR.get(un_en, un_en)
            L["unesco_en"] = un_en
            L.pop("speakers_raw", None)  # bozuk PDF-çıkarım alanını temizle
            applied.append(iso)
            seen.add(iso)
        elif iso in NOT_IN_TABLE:
            # tabloda yok: mevcut speakers korunur, demografi alanları boş bırakılır (dürüst)
            L.setdefault("speakers_year", "")
            L.setdefault("speakers_source", "")
            L.pop("speakers_raw", None)
            skipped.append(iso)
        else:
            missing.append(iso)

    # tabloda olup master'da bulunmayanları raporla (olmamalı)
    not_found = [k for k in DEMO if k not in seen]

    json.dump(doc, open(MASTER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    out = []
    out.append("R5b-2 demografi uygulandi -> languages.master.json")
    out.append(f"  uygulanan (tablodan): {len(applied)} dil")
    out.append(f"  tabloda yok (dokunulmadi): {skipped}")
    if missing:
        out.append(f"  ESLEsMEYEN master ISO (DEMO'da yok): {missing}")
    if not_found:
        out.append(f"  UYARI - DEMO'da olup master'da bulunamadi: {not_found}")
    rep = pathlib.Path(__file__).resolve().parent / "_apply_demographics_ds19.out.txt"
    rep.write_text("\n".join(out), encoding="utf-8")
    print("OK -> " + str(rep))


if __name__ == "__main__":
    main()
