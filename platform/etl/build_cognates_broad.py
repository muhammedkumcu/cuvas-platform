# -*- coding: utf-8 -*-
"""build_cognates_broad.py — Savelyev CLDF (cognates.json, 254 kavram) → cognates_broad.json

KÖKEN Kognat Ağı'nın "GENİŞ tarama" katmanı (ds18 derin 11'in yanına). 254 kavram × ≤32 dil,
kognat-seti (cogid) tabanlı boşluk tespiti, akademik karşılaştırmalı yazım (readable).
DÜRÜST: Savelyev verisinde yerel yazı/IPA/per-hücre ses kuralı YOK — bunlar yalnız derin sette.
Geniş katman = form + proto + boşluk + segment (akademik). Glosslar İngilizce → Türkçe eşlendi (254).
Kaynak: SavelyevTurkic CLDF (CC BY 4.0) — Savelyev & Robbeets 2020.
"""
import json
import io
import os
import re

# Savelyev dil adı → Türkçe görünen ad (32)
SAV_TR = {
    "Turkish": "Türkçe", "Azeri": "Azerbaycanca", "Turkmen": "Türkmence", "Gagauz": "Gagavuzca",
    "Kazakh": "Kazakça", "Kirghiz": "Kırgızca", "Tatar": "Tatarca", "Bashkir": "Başkurtça",
    "KaraKalpak": "Karakalpakça", "CrimeanTatar": "Kırım Tatarcası", "KarachayBalkar": "Karaçay-Balkarca",
    "Kumyk": "Kumukça", "Nogai": "Nogayca", "Karaim": "Karayca", "Baraba": "Baraba Tatarcası",
    "Uzbek": "Özbekçe", "Uighur": "Uygurca", "Chuvash": "Çuvaşça",
    "Yakut": "Yakutça", "Dolgan": "Dolganca", "Tuvan": "Tuvaca", "Tofa": "Tofaca",
    "Khakas": "Hakasça", "Shor": "Şorca", "SouthAltai": "Altayca", "NorthAltai": "Kuzey Altayca",
    "MiddleChulym": "Orta Çulımca", "SarygYugur": "Sarı Uygurca", "Salar": "Salarca",
    "Khalaj": "Halaçça", "OldUyghur": "Eski Uygurca", "CodexCumanicus": "Codex Cumanicus",
}

# Akademik karşılaştırmalı yazım (build.py COG_READABLE ile uyumlu)
READABLE = {"ḳ": "q", "χ": "h", "ɣ": "ğ", "γ": "ğ", "ŋ": "ñ", "ə": "ä", "ɘ": "ĕ", "ɵ": "ö",
            "ɯ": "ı", "ɨ": "ı", "ʒ": "j", "ɕ": "ś", "ʃ": "ş", "ʷ": "", "ụ": "u", "ỹ": "y", "ʁ": "ğ",
            "ø": "ö", "œ": "ö", "æ": "ä", "ɲ": "ny", "ʂ": "ş", "ʐ": "j", "ǰ": "c"}


def readable(s):
    return "".join(READABLE.get(ch, ch) for ch in str(s or ""))


# 254 İngilizce gloss → (Türkçe, kategori). Kategoriler (10): Vücut, Doğa, Hayvan & bitki,
# Eylem, Nitelik, Sayılar, Zaman, Kişi & akrabalık, Dilbilgisi & uzay, Nesne & soyut.
GL = {
    "HERE": ("burada", "Dilbilgisi & uzay"), "HIDE (CONCEAL)": ("saklamak", "Eylem"),
    "BEAT": ("dövmek", "Eylem"), "HOLE": ("delik", "Nesne & soyut"), "HORN (ANATOMY)": ("boynuz", "Vücut"),
    "HOT": ("sıcak", "Nitelik"), "HOUSE": ("ev", "Nesne & soyut"), "HOW": ("nasıl", "Dilbilgisi & uzay"),
    "HUNT": ("avlamak", "Eylem"), "ICE": ("buz", "Doğa"), "ASH": ("kül", "Doğa"),
    "IN": ("içinde", "Dilbilgisi & uzay"), "JUMP": ("sıçramak", "Eylem"), "KILL": ("öldürmek", "Eylem"),
    "KNEE": ("diz", "Vücut"), "KNOW (SOMETHING)": ("bilmek", "Eylem"), "LAKE": ("göl", "Doğa"),
    "LAUGH": ("gülmek", "Eylem"), "LEAF": ("yaprak", "Hayvan & bitki"), "LEFT": ("sol", "Dilbilgisi & uzay"),
    "FOOT OR LEG": ("ayak / bacak", "Vücut"), "ASK (REQUEST)": ("istemek", "Eylem"), "LICK": ("yalamak", "Eylem"),
    "LIE DOWN": ("yatmak", "Eylem"), "BE ALIVE": ("yaşamak", "Eylem"), "LIVER": ("karaciğer", "Vücut"),
    "LONG": ("uzun", "Nitelik"), "LOOK": ("bakmak", "Eylem"), "LOOK FOR": ("aramak", "Eylem"),
    "LOUSE": ("bit", "Hayvan & bitki"), "MAN": ("adam", "Kişi & akrabalık"), "MANY": ("çok", "Nitelik"),
    "AT": ("-de", "Dilbilgisi & uzay"), "MEAT": ("et", "Nesne & soyut"), "MONTH": ("ay (takvim)", "Zaman"),
    "MOON": ("ay (gök)", "Doğa"), "MOTHER": ("anne", "Kişi & akrabalık"), "MOUNTAIN OR HILL": ("dağ / tepe", "Doğa"),
    "MOUTH": ("ağız", "Vücut"), "NAME": ("ad", "Nesne & soyut"), "NARROW": ("dar", "Nitelik"),
    "NASAL MUCUS (SNOT)": ("sümük", "Vücut"), "NAVEL": ("göbek", "Vücut"), "BACK": ("sırt", "Vücut"),
    "NEAR": ("yakın", "Dilbilgisi & uzay"), "NECK": ("boyun", "Vücut"), "NEW": ("yeni", "Nitelik"),
    "NIGHT": ("gece", "Zaman"), "NOSE": ("burun", "Vücut"), "NOT": ("değil", "Dilbilgisi & uzay"),
    "OLD": ("eski", "Nitelik"), "ONE": ("bir", "Sayılar"), "OPEN": ("açmak", "Eylem"),
    "OTHER": ("başka", "Dilbilgisi & uzay"), "BAD": ("kötü", "Nitelik"), "PERSON": ("kişi", "Kişi & akrabalık"),
    "PLAY": ("oynamak", "Eylem"), "PULL": ("çekmek", "Eylem"), "PUS": ("irin", "Vücut"),
    "PUSH": ("itmek", "Eylem"), "PUT ON": ("giymek", "Eylem"), "RAIN (PRECIPITATION)": ("yağmur", "Doğa"),
    "RAW": ("çiğ", "Nitelik"), "RED": ("kırmızı", "Nitelik"), "REMAIN": ("kalmak", "Eylem"),
    "BARK": ("ağaç kabuğu", "Hayvan & bitki"), "RIGHT": ("sağ", "Dilbilgisi & uzay"), "RIPEN": ("olgunlaşmak", "Eylem"),
    "RISE (MOVE UPWARDS)": ("yükselmek", "Eylem"), "RIVER": ("nehir", "Doğa"), "ROOT": ("kök", "Hayvan & bitki"),
    "ROPE": ("ip", "Nesne & soyut"), "ROUND": ("yuvarlak", "Nitelik"), "RUN": ("koşmak", "Eylem"),
    "SALT": ("tuz", "Nesne & soyut"), "SAND": ("kum", "Doğa"), "BELLY": ("karın", "Vücut"),
    "SAY": ("demek", "Eylem"), "SCRATCH": ("kaşımak", "Eylem"), "SEA": ("deniz", "Doğa"),
    "SEE": ("görmek", "Eylem"), "SEED": ("tohum", "Hayvan & bitki"), "SEW": ("dikmek", "Eylem"),
    "SHADE": ("gölge", "Doğa"), "SHARP": ("keskin", "Nitelik"), "SHORT": ("kısa", "Nitelik"),
    "SHOULDER": ("omuz", "Vücut"), "BIG": ("büyük", "Nitelik"), "SING": ("şarkı söylemek", "Eylem"),
    "SIT": ("oturmak", "Eylem"), "SKIN": ("deri", "Vücut"), "SKY": ("gökyüzü", "Doğa"),
    "SLEEP": ("uyumak", "Eylem"), "SMALL": ("küçük", "Nitelik"), "SMELL": ("koklamak", "Eylem"),
    "SMOKE (EXHAUST)": ("duman", "Doğa"), "SMOOTH": ("pürüzsüz", "Nitelik"), "SNAKE": ("yılan", "Hayvan & bitki"),
    "BIRD": ("kuş", "Hayvan & bitki"), "SNOW": ("kar", "Doğa"), "SOFT": ("yumuşak", "Nitelik"),
    "EARTH (SOIL)": ("toprak", "Doğa"), "SOUR": ("ekşi", "Nitelik"), "SPIN": ("eğirmek", "Eylem"),
    "SPIT": ("tükürmek", "Eylem"), "STAND": ("durmak", "Eylem"), "STAR": ("yıldız", "Doğa"),
    "STICK": ("değnek", "Nesne & soyut"), "STONE": ("taş", "Doğa"), "BITE": ("ısırmak", "Eylem"),
    "FINGERNAIL": ("tırnak", "Vücut"), "STRAIGHT": ("düz", "Nitelik"), "SUCK": ("emmek", "Eylem"),
    "SUN": ("güneş", "Doğa"), "SWALLOW": ("yutmak", "Eylem"), "SWEET": ("tatlı", "Nitelik"),
    "SWELL": ("şişmek", "Eylem"), "SWIM": ("yüzmek", "Eylem"), "TAIL": ("kuyruk", "Vücut"),
    "TAKE": ("almak", "Eylem"), "TALL": ("uzun boylu", "Nitelik"), "BITTER": ("acı", "Nitelik"),
    "TEAR (SHRED)": ("yırtmak", "Eylem"), "THAT": ("şu / o", "Dilbilgisi & uzay"), "THERE": ("orada", "Dilbilgisi & uzay"),
    "THEY": ("onlar", "Dilbilgisi & uzay"), "THICK": ("kalın", "Nitelik"), "UPPER LEG (THIGH)": ("uyluk", "Vücut"),
    "THIN": ("ince", "Nitelik"), "THINK": ("düşünmek", "Eylem"), "THIS": ("bu", "Dilbilgisi & uzay"),
    "THREE": ("üç", "Sayılar"), "BLACK": ("siyah", "Nitelik"), "THROAT": ("boğaz", "Vücut"),
    "THROW": ("atmak", "Eylem"), "TIE": ("bağlamak", "Eylem"), "ROTTEN": ("çürük", "Nitelik"),
    "TOMORROW": ("yarın", "Zaman"), "TONGUE": ("dil", "Vücut"), "TOOTH": ("diş", "Vücut"),
    "TREE": ("ağaç", "Hayvan & bitki"), "TRUE": ("doğru", "Nitelik"), "TURN (SOMETHING)": ("döndürmek", "Eylem"),
    "BLOOD": ("kan", "Vücut"), "TWO": ("iki", "Sayılar"), "VOMIT": ("kusmak", "Eylem"),
    "WALK": ("yürümek", "Eylem"), "WARM": ("ılık", "Nitelik"), "WASH": ("yıkamak", "Eylem"),
    "WATER": ("su", "Doğa"), "WEAVE": ("dokumak", "Eylem"), "WET": ("ıslak", "Nitelik"),
    "WHAT": ("ne", "Dilbilgisi & uzay"), "WHEN": ("ne zaman", "Dilbilgisi & uzay"), "BLOW (OF WIND)": ("esmek", "Eylem"),
    "WHERE": ("nerede", "Dilbilgisi & uzay"), "WHICH": ("hangi", "Dilbilgisi & uzay"), "WHITE": ("beyaz", "Nitelik"),
    "WHO": ("kim", "Dilbilgisi & uzay"), "WIDE": ("geniş", "Nitelik"), "WIND": ("rüzgar", "Doğa"),
    "WING": ("kanat", "Hayvan & bitki"), "WITH": ("ile", "Dilbilgisi & uzay"), "WOMAN": ("kadın", "Kişi & akrabalık"),
    "WOOD": ("odun", "Nesne & soyut"), "BONE": ("kemik", "Vücut"), "FOREST": ("orman", "Doğa"),
    "WORM": ("kurt (solucan)", "Hayvan & bitki"), "YEAR": ("yıl", "Zaman"), "YELLOW": ("sarı", "Nitelik"),
    "YESTERDAY": ("dün", "Zaman"), "BOTTOM": ("alt", "Dilbilgisi & uzay"), "BRAIN": ("beyin", "Vücut"),
    "BRANCH": ("dal", "Hayvan & bitki"), "BREAK (CLEAVE)": ("kırmak", "Eylem"), "BREAST": ("göğüs", "Vücut"),
    "WE": ("biz", "Dilbilgisi & uzay"), "BREATHE": ("nefes almak", "Eylem"), "BURN": ("yanmak", "Eylem"),
    "CARRY": ("taşımak", "Eylem"), "CHEEK": ("yanak", "Vücut"), "CHEW": ("çiğnemek", "Eylem"),
    "CHILD (DESCENDANT)": ("çocuk", "Kişi & akrabalık"), "CHIN": ("çene", "Vücut"), "CLAW": ("pençe", "Vücut"),
    "CLOUD": ("bulut", "Doğa"), "COLD": ("soğuk", "Nitelik"), "I": ("ben", "Dilbilgisi & uzay"),
    "COME": ("gelmek", "Eylem"), "COUGH": ("öksürmek", "Eylem"), "COUNT": ("saymak", "Eylem"),
    "COVER": ("örtmek", "Eylem"), "GRIND": ("öğütmek", "Eylem"), "CRY": ("ağlamak", "Eylem"),
    "CUT": ("kesmek", "Eylem"), "DAY (NOT NIGHT)": ("gün", "Zaman"), "DEEP": ("derin", "Nitelik"),
    "DIE": ("ölmek", "Eylem"), "YOU": ("siz", "Dilbilgisi & uzay"), "DIG": ("kazmak", "Eylem"),
    "DIRTY": ("kirli", "Nitelik"), "DO OR MAKE": ("yapmak", "Eylem"), "DOG": ("köpek", "Hayvan & bitki"),
    "DRINK": ("içmek", "Eylem"), "DRY": ("kuru", "Nitelik"), "DUST": ("toz", "Doğa"),
    "EAR": ("kulak", "Vücut"), "EAT": ("yemek", "Eylem"), "EDGE": ("kenar", "Dilbilgisi & uzay"),
    "THOU": ("sen", "Dilbilgisi & uzay"), "EGG": ("yumurta", "Hayvan & bitki"), "EYE": ("göz", "Vücut"),
    "FALL": ("düşmek", "Eylem"), "FAR": ("uzak", "Dilbilgisi & uzay"), "FAT (ORGANIC SUBSTANCE)": ("yağ", "Vücut"),
    "FATHER": ("baba", "Kişi & akrabalık"), "FEAR (BE AFRAID)": ("korkmak", "Eylem"), "FEATHER": ("tüy", "Hayvan & bitki"),
    "FEMALE ANIMAL": ("dişi hayvan", "Hayvan & bitki"), "FIGHT": ("savaşmak", "Eylem"), "HE OR SHE OR IT": ("o", "Dilbilgisi & uzay"),
    "FIND": ("bulmak", "Eylem"), "FIRE": ("ateş", "Doğa"), "FIREWOOD": ("odun (yakacak)", "Nesne & soyut"),
    "FISH": ("balık", "Hayvan & bitki"), "FIVE": ("beş", "Sayılar"), "FLOW": ("akmak", "Eylem"),
    "FLOWER": ("çiçek", "Hayvan & bitki"), "FLY (INSECT)": ("sinek", "Hayvan & bitki"), "FLY (MOVE THROUGH AIR)": ("uçmak", "Eylem"),
    "FOAM": ("köpük", "Doğa"), "ABOVE": ("üst", "Dilbilgisi & uzay"), "FOG": ("sis", "Doğa"),
    "FOREHEAD": ("alın", "Vücut"), "FOUR": ("dört", "Sayılar"), "FREEZE": ("donmak", "Eylem"),
    "FRUIT": ("meyve", "Hayvan & bitki"), "FULL": ("dolu", "Nitelik"), "GIVE": ("vermek", "Eylem"),
    "GO": ("gitmek", "Eylem"), "GOOD": ("iyi", "Nitelik"), "GRASP": ("tutmak", "Eylem"),
    "ANT": ("karınca", "Hayvan & bitki"), "GRASS": ("ot", "Hayvan & bitki"), "GREEN": ("yeşil", "Nitelik"),
    "GROW": ("büyümek", "Eylem"), "GUTS": ("bağırsak", "Vücut"), "HAIR (HEAD)": ("saç", "Vücut"),
    "HARD": ("sert", "Nitelik"), "HEAD": ("baş", "Vücut"), "HEAR": ("işitmek", "Eylem"),
    "HEART": ("kalp", "Vücut"), "HEAVY": ("ağır", "Nitelik"), "ARM OR HAND": ("kol / el", "Vücut"),
}


def slug(g):
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", g.lower())).strip("_")


def build():
    d = json.load(io.open(os.path.join(os.path.dirname(__file__), "..", "data", "cognates.json"), encoding="utf-8"))
    cats_seen, cognates = [], {}
    unmapped = []
    for c in d["concepts"]:
        g = c["gloss"]
        tr, cat = GL.get(g, (g.title(), "Diğer"))
        if g not in GL:
            unmapped.append(g)
        if cat not in cats_seen:
            cats_seen.append(cat)
        # dominant cognate set = en çok dile sahip cogid
        set_langs = {s["cognateset_id"]: len({m["lang"] for m in s["members"]}) for s in c["sets"]}
        dom = max(set_langs, key=set_langs.get)
        dom_root = next((s.get("root") for s in c["sets"] if s["cognateset_id"] == dom), "")
        proto = readable((dom_root or "").split(":")[0].strip())
        nodes, seen, gaps = [], set(), []
        for s in c["sets"]:
            cogid = s["cognateset_id"]
            for m in s["members"]:
                lg = m["lang"]
                if lg in seen:
                    continue
                seen.add(lg)
                form = m.get("form") or (m.get("value") or "").split(",")[0].strip()
                if not form:
                    continue
                shift = cogid != dom
                node = {"lang": SAV_TR.get(lg, lg), "word": readable(form),
                        "branch": m.get("branch", "?"), "shift": shift, "cogid": cogid,
                        "rule": readable(m.get("segments") or "")}
                nodes.append(node)
                if shift:
                    gaps.append(SAV_TR.get(lg, lg))
        if len(nodes) < 2:
            continue
        # kola göre sırala (renk-bitişik), Çuvaşça/derin diller önce gelsin diye stabil
        BORDER = {"Oğuz": 0, "Kıpçak": 1, "Karluk": 2, "Ogur": 3, "Sibirya": 4, "Argu": 5, "Eski Türkçe": 6}
        nodes.sort(key=lambda n: (BORDER.get(n["branch"], 9), n["lang"]))
        ridx = 0 if "ŕ" in (dom_root or "") else (1 if "ĺ" in (dom_root or "") else None)
        ngap = len(gaps)
        note = (f"Proto {proto or '—'} · {len(nodes)} dil · {len(c['sets'])} kognat seti. "
                + (f"Boşluk (farklı kök/alıntı): {ngap} dil." if ngap else "Tek kognat seti — boşluk yok.")
                + " Akademik karşılaştırmalı yazım (yerel yazı/IPA yalnız Derin sette).")
        cognates[slug(g)] = {"gloss": tr, "gloss_en": g, "cat": cat, "proto": proto,
                             "note": note, "nodes": nodes, "ruleIdx": ridx}
    order = ["Vücut", "Doğa", "Hayvan & bitki", "Nitelik", "Eylem", "Sayılar", "Zaman",
             "Kişi & akrabalık", "Nesne & soyut", "Dilbilgisi & uzay", "Diğer"]
    categories = [c for c in order if c in cats_seen] + [c for c in cats_seen if c not in order]
    return {
        "_meta": {
            "source": "SavelyevTurkic CLDF (cognates.json) — Savelyev & Robbeets 2020",
            "license": "CC BY 4.0",
            "method": "254 İngilizce gloss → Türkçe + 10 kategori eşleme; cogid majority → boşluk tespiti; "
                      "akademik karşılaştırmalı yazım (readable). DÜRÜST: yerel yazı/IPA/ses kuralı YOK (derin sette).",
            "concepts": len(cognates), "categories": categories,
        },
        "categories": categories,
        "cognates": cognates,
    }, unmapped


if __name__ == "__main__":
    data, unmapped = build()
    out = os.path.join(os.path.dirname(__file__), "..", "data", "cognates_broad.json")
    with io.open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("cognates_broad.json: %d kavram, %d kategori" % (data["_meta"]["concepts"], len(data["categories"])))
    print("  kategoriler:", ", ".join(data["categories"]))
    if unmapped:
        print("  ! TR gloss eslesmemis (%d):" % len(unmapped), ", ".join(unmapped[:20]))
    else:
        print("  TR gloss: 254/254 eslesti")
