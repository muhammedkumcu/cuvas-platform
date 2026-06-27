# -*- coding: utf-8 -*-
"""build_cognates_deep.py — ds18 (Genişletilmiş Kognat Veritabanı) → cognates_deep.json

Kaynak: arastirma/18Türk Dilleri Kognat Veritabanı.pdf (deepsearch 18) — faithful transcript.
Her hücre: yerel yazı (Cyrillic temiz; Arap-yazılı Uygurca romanize) · Latin transkripsiyon ·
IPA · morfem segmentasyonu · Kognat Set ID (boşluk tespiti) · uygulanan ses kuralı.
Atıf: Savelyev & Robbeets 2020 (Bayesian filodilbilim) + Cambridge Turkic + Wiktionary/Concepticon
(PDF'in 'Alıntılanan çalışmalar' bölümü). UYDURMA YOK — tabloda olmayan dil/kavram eklenmez.

18 dil (kol-gruplu sıra) — Kognat Ağı radyal grafiğinde renk-bitişik gösterilir.
11 kavram = ds18'de TAM matrisi verilen kavramlar (5 anlamsal kategori). Akrabalık kategorisinde
ds18 tam tablo vermediği için kavram eklenmemiştir (dürüst).
"""
import json
import io
import os

LANGS = [
    ("Türkçe", "tur", "Oğuz"), ("Azerbaycanca", "azj", "Oğuz"),
    ("Türkmence", "tuk", "Oğuz"), ("Gagavuzca", "gag", "Oğuz"),
    ("Kazakça", "kaz", "Kıpçak"), ("Kırgızca", "kir", "Kıpçak"),
    ("Tatarca", "tat", "Kıpçak"), ("Başkurtça", "bak", "Kıpçak"),
    ("Karakalpakça", "kaa", "Kıpçak"), ("Kırım Tatarcası", "crh", "Kıpçak"),
    ("Özbekçe", "uzn", "Karluk"), ("Uygurca", "uig", "Karluk"),
    ("Çuvaşça", "chv", "Ogur"),
    ("Yakutça", "sah", "Sibirya"), ("Tuvaca", "tyv", "Sibirya"),
    ("Hakasça", "kjh", "Sibirya"), ("Şorca", "cjs", "Sibirya"),
    ("Halaçça", "klj", "Argu"),
]

# Her kavram: cells = LANGS sırasında 18 demet (native, latin, ipa, morph, cogid, rule).
# native: Uygurca Arap yazısı PDF'te bozuk çıktığından romanize (latin) tutuldu (dürüst).
CONCEPTS = [
    {
        "key": "goz", "gloss": "Göz", "gloss_en": "Eye", "cat": "Vücut",
        "concepticon": 1248, "proto": "*kȫŕ",
        "note": "Sibirya grubu dışında (karak 'göz bebeği'→'göz' anlam genişlemesi) çok yüksek korunum.",
        "cells": [
            ("göz", "göz", "ɟœz", "göz", 1, "*k>g, *ŕ>z, *ȫ>ö"),
            ("göz", "göz", "ɟœz", "göz", 1, "*k>g, *ŕ>z, *ȫ>ö"),
            ("göz", "göːz", "gœːz", "göːz", 1, "*k>g, *ŕ>z, *ȫ>öː (uzun ünlü)"),
            ("göz", "göz", "ɟœz", "göz", 1, "*k>g, *ŕ>z, *ȫ>ö"),
            ("көз", "köz", "kœz", "köz", 1, "*ŕ>z, *ȫ>ö"),
            ("көз", "köz", "kœz", "köz", 1, "*ŕ>z, *ȫ>ö"),
            ("күз", "küz", "kyz", "küz", 1, "*ŕ>z, *ȫ>ü"),
            ("күҙ", "küź", "kyð", "küź", 1, "*ŕ>z>ź (ð), *ȫ>ü"),
            ("ko'z", "köz", "kœz", "köz", 1, "*ŕ>z, *ȫ>ö"),
            ("köz", "köz", "kœz", "köz", 1, "*ŕ>z, *ȫ>ö"),
            ("ko'z", "ko'z", "kɒz", "ko'z", 1, "*ŕ>z, *ȫ>o' (yuvarlaklaşma)"),
            ("köz", "köz", "køz", "köz", 1, "*ŕ>z, *ȫ>ö"),
            ("куҫ", "kuś", "kuɕ", "kuś", 1, "*ŕ>r>ś, *ȫ>u (Çuvaş rotasizm istisnası)"),
            ("харах", "xarax", "xarax", "xara-x", 2, "Leksikal yenilik (boşluk; 'siyahlık' kökünden)"),
            ("карак", "karak", "qaraq", "kara-k", 2, "Leksikal yenilik (Sibirya izoglosu)"),
            ("харах", "xarax", "xarax", "xara-x", 2, "Leksikal yenilik"),
            ("қарак", "qaraq", "qaraq", "qara-q", 2, "Leksikal yenilik"),
            ("kőz", "kőz", "kœːz", "kőːz", 1, "*ŕ>z, *ȫ>öː (uzun ünlü)"),
        ],
    },
    {
        "key": "bas", "gloss": "Baş", "gloss_en": "Head", "cat": "Vücut",
        "concepticon": 1256, "proto": "*baĺč / *baš",
        "note": "Leksikal yeniliğin neredeyse hiç görülmediği en katı kognat setlerinden biri; Çuvaşça puś dahi düzenli lambdasizmle bağlanır.",
        "cells": [
            ("baş", "baş", "baʃ", "baş", 3, "*ĺ>ş"),
            ("baş", "baş", "bɑʃ", "baş", 3, "*ĺ>ş"),
            ("baş", "baːş", "baːʃ", "baːş", 3, "*ĺ>ş, *a>aː (uzun ünlü)"),
            ("baş", "baş", "bɑʃ", "baş", 3, "*ĺ>ş"),
            ("бас", "bas", "bɑs", "bas", 3, "*ĺ>ş>s (Kıpçak sızıcılaşması)"),
            ("баш", "baş", "bɑʃ", "baş", 3, "*ĺ>ş"),
            ("баш", "baş", "baʃ", "baş", 3, "*ĺ>ş"),
            ("баш", "baş", "bɑʃ", "baş", 3, "*ĺ>ş"),
            ("bas", "bas", "bɑs", "bas", 3, "*ĺ>ş>s"),
            ("baş", "baş", "baʃ", "baş", 3, "*ĺ>ş"),
            ("bosh", "bosh", "bɒʃ", "bosh", 3, "*ĺ>ş, *a>o"),
            ("bash", "bash", "bɑʃ", "bash", 3, "*ĺ>ş"),
            ("пуҫ", "puś", "puɕ", "puś", 3, "*b>p, *ĺ>l>ś (Oğur lambdasizm sızıcılaşması)"),
            ("бас", "bas", "bɑs", "bas", 3, "*ĺ>ş>s"),
            ("баж-", "bažı", "baʒi", "baž-ı", 3, "*ĺ>ş>ž (intervokalik ötümlüleşme)"),
            ("пас", "pas", "pas", "pas", 3, "*b>p, *ĺ>ş>s"),
            ("паш", "paş", "paʃ", "paş", 3, "*b>p, *ĺ>ş"),
            ("baş", "baˑş", "baˑʃ", "baˑş", 3, "Yarı-uzun ünlü"),
        ],
    },
    {
        "key": "kan", "gloss": "Kan", "gloss_en": "Blood", "cat": "Vücut",
        "concepticon": 1246, "proto": "*qān (*kiān)",
        "note": "Uzun ünlü korunumu Yakutça (xaan) ve Halaççada (qán) net. Çuvaşça yun bir fonetik uç nokta ama kognat.",
        "cells": [
            ("kan", "kan", "kan", "kan", 4, "*q>k, *ā>a"),
            ("qan", "qan", "qɑn", "qan", 4, "*ā>a"),
            ("gān", "ga:n", "gɑːn", "gaːn", 4, "*q>g, *ā>aː (uzun ünlü)"),
            ("kan", "kan", "kɑn", "kan", 4, "*q>k"),
            ("қан", "qan", "qɑn", "qan", 4, "*ā>a"),
            ("кан", "qan", "qɑn", "qan", 4, "*q>q, *ā>a"),
            ("кан", "qan", "qan", "qan", 4, "*q>q"),
            ("ҡан", "qan", "qɑn", "qan", 4, "*q>q"),
            ("qan", "qan", "qɑn", "qan", 4, "*q>q"),
            ("qan", "qan", "qan", "qan", 4, "*q>q"),
            ("qon", "qon", "qɒn", "qon", 4, "*ā>o"),
            ("qan", "qan", "qɑn", "qan", 4, "*q>q"),
            ("юн", "yun", "jun", "yun", 4, "*q>y, *ā>u (ağır fonetik evrim)"),
            ("хаан", "xaan", "xaan", "xaan", 4, "*q>x, *ā>aa (uzun ünlü)"),
            ("хан", "xan", "xan", "xan", 4, "*q>x"),
            ("хан", "xan", "xan", "xan", 4, "*q>x"),
            ("қан", "qan", "qan", "qan", 4, "*q>q"),
            ("qán", "qán", "qaːn", "qaːn", 4, "*ā>aː (uzun ünlü)"),
        ],
    },
    {
        "key": "ayak", "gloss": "Ayak", "gloss_en": "Foot / Leg", "cat": "Vücut",
        "concepticon": 2098, "proto": "*adak",
        "note": "İntervokalik *d evriminin turnusol kelimesi (y/d/t/z refleksleri). Çuvaşça ura leksikal yenilik (boşluk).",
        "cells": [
            ("ayak", "ayak", "aˈjak", "a-yak", 5, "*d>y (Oğuz lenisyonu)"),
            ("ayaq", "ayaq", "ɑˈjɑq", "a-yaq", 5, "*d>y, *k>q"),
            ("aýak", "aýak", "aˈjak", "a-ýak", 5, "*d>ý"),
            ("ayak", "ayak", "ɑˈjɑk", "a-yak", 5, "*d>y"),
            ("аяқ", "ayaq", "ɑˈjɑq", "a-yaq", 5, "*d>y"),
            ("аяк", "ayak", "ɑˈjɑq", "a-yak", 5, "*d>y"),
            ("аяк", "ayak", "aˈjak", "a-yak", 5, "*d>y"),
            ("аяҡ", "ayaq", "ɑˈjɑq", "a-yaq", 5, "*d>y"),
            ("ayaq", "ayaq", "ɑˈjɑq", "a-yaq", 5, "*d>y"),
            ("ayaq", "ayaq", "aˈjaq", "a-yaq", 5, "*d>y"),
            ("oyoq", "oyoq", "ɒˈjɒq", "o-yoq", 5, "*d>y, *a>o"),
            ("ayaq", "ayaq", "aˈjaq", "a-yaq", 5, "*d>y"),
            ("ура", "ura", "uˈra", "ura", 6, "Leksikal yenilik (boşluk; yeni kök gelişimi)"),
            ("атах", "atax", "aˈtax", "a-tax", 5, "*d>t (sertleşme), *k>x"),
            ("адак", "adak", "aˈdaq", "a-dak", 5, "*d korundu (Sibirya arkaizmi)"),
            ("азах", "azaq", "aˈzaq", "a-zaq", 5, "*d>z"),
            ("азақ", "azaq", "aˈzaq", "a-zaq", 5, "*d>z"),
            ("hadaq", "hadaq", "haˈdaq", "hadaq", 5, "*p->h- (türeme/korunma), *d korundu"),
        ],
    },
    {
        "key": "tas", "gloss": "Taş", "gloss_en": "Stone", "cat": "Doğa",
        "concepticon": 1335, "proto": "*tāĺ",
        "note": "Çuvaşça čul, t>č palatalizasyonu + lambdasizmle doğrudan PT köküne bağlı (Vovin).",
        "cells": [
            ("taş", "taş", "taʃ", "taş", 7, "*t>t, *ā>a, *ĺ>ş"),
            ("daş", "daş", "dɑʃ", "daş", 7, "*t>d (Oğuz ötümlüleşmesi), *ĺ>ş"),
            ("daş", "daːş", "dɑːʃ", "daːş", 7, "*t>d, *ā>aː (uzun ünlü), *ĺ>ş"),
            ("taş", "taş", "tɑʃ", "taş", 7, "*ĺ>ş"),
            ("тас", "tas", "tɑs", "tas", 7, "*ĺ>ş>s"),
            ("таш", "taş", "tɑʃ", "taş", 7, "*ĺ>ş"),
            ("таш", "taş", "taʃ", "taş", 7, "*ĺ>ş"),
            ("таш", "taş", "tɑʃ", "taş", 7, "*ĺ>ş"),
            ("tas", "tas", "tɑs", "tas", 7, "*ĺ>ş>s"),
            ("taş", "taş", "taʃ", "taş", 7, "*ĺ>ş"),
            ("tosh", "tosh", "tɒʃ", "tosh", 7, "*ĺ>ş, *ā>o"),
            ("tash", "tash", "tɑʃ", "tash", 7, "*ĺ>ş"),
            ("чул", "čul", "t͡ɕul", "čul", 7, "*t>č (palatalizasyon), *ā>u, *ĺ>l (lambdasizm)"),
            ("таас", "taas", "taːs", "taa-s", 7, "*ā>aa (uzun ünlü), *ĺ>ş>s"),
            ("даш", "daş", "daʃ", "daş", 7, "*t>d, *ĺ>ş"),
            ("тас", "tas", "tas", "tas", 7, "*ĺ>ş>s"),
            ("таш", "taş", "taʃ", "taş", 7, "*ĺ>ş"),
            ("tâaş", "tâaş", "taːʃ", "taːş", 7, "*ā>aː (uzun ünlü), *ĺ>ş"),
        ],
    },
    {
        "key": "su", "gloss": "Su", "gloss_en": "Water", "cat": "Doğa",
        "concepticon": 1222, "proto": "*sub / *suv",
        "note": "Sözcük sonu *-b lenisyonu (v/w/Ø) kol alt-ayrımlarını çizer; Sibirya'da -g/-ğ türemesi.",
        "cells": [
            ("su", "su", "su", "su", 8, "*b>v>Ø"),
            ("su", "su", "su", "su", 8, "*b>v>Ø"),
            ("suw", "suw", "suw", "suw", 8, "*b>w"),
            ("su", "su", "su", "su", 8, "*b>Ø"),
            ("су", "sw", "sʊw", "suw", 8, "*b>w"),
            ("суу", "suu", "suː", "suu", 8, "*b>w>u (uzama)"),
            ("су", "su", "su", "su", 8, "*b>Ø"),
            ("һыу", "hïw", "hɯw", "hïw", 8, "*s>h, *u>ï, *b>w"),
            ("suw", "suw", "sʊw", "suw", 8, "*b>w"),
            ("suv", "suv", "suv", "suv", 8, "*b>v"),
            ("suv", "suv", "suv", "suv", 8, "*b>v"),
            ("su", "su", "su", "su", 8, "*b>Ø"),
            ("шыв", "šyv", "ʂɯʋ", "šyv", 8, "*s>š, *u>y, *b>v"),
            ("уу", "uu", "uː", "uu", 8, "*s>Ø, *b>w>u (sözcük başı s düşmesi)"),
            ("суг", "sug", "suʁ", "su-g", 8, "*b>g (Sibirya -g türemesi)"),
            ("суғ", "suğ", "suʁ", "su-ğ", 8, "*b>ğ"),
            ("суғ", "suğ", "suʁ", "su-ğ", 8, "*b>ğ"),
            ("suw", "suw", "suw", "suw", 8, "*b>w"),
        ],
    },
    {
        "key": "bir", "gloss": "Bir", "gloss_en": "One", "cat": "Sayılar",
        "concepticon": None, "proto": "*bīr",
        "note": "Sıfır leksikal yenilik — sayı sistemi filogenetik olarak sarsılmaz kararlılıkta.",
        "cells": [
            ("bir", "bir", "bir", "bir", 9, "*ī>i"),
            ("bir", "bir", "bir", "bir", 9, "*ī>i"),
            ("bir", "bi:r", "biːr", "biːr", 9, "*ī>iː (uzun ünlü korunumu)"),
            ("bir", "bir", "bir", "bir", 9, "*ī>i"),
            ("бір", "bir", "bɪr", "bir", 9, "*ī>i"),
            ("бир", "bir", "bir", "bir", 9, "*ī>i"),
            ("бер", "ber", "ber", "ber", 9, "*ī>e"),
            ("бер", "ber", "ber", "ber", 9, "*ī>e"),
            ("bir", "bir", "bɪr", "bir", 9, "*ī>i"),
            ("bir", "bir", "bir", "bir", 9, "*ī>i"),
            ("bir", "bir", "bir", "bir", 9, "*ī>i"),
            ("bir", "bir", "bir", "bir", 9, "*ī>i"),
            ("пӗр", "pĕr", "pɘr", "pĕr", 9, "*b>p, *ī>ĕ"),
            ("биир", "biir", "biːr", "biir", 9, "*ī>ii (uzun ünlü)"),
            ("бир", "bir", "bir", "bir", 9, "*ī>i"),
            ("пір", "pir", "pir", "pir", 9, "*b>p"),
            ("пир", "pir", "pir", "pir", 9, "*b>p"),
            ("bi:r", "bi:r", "biːr", "biːr", 9, "*ī>iː (uzun ünlü)"),
        ],
    },
    {
        "key": "iki", "gloss": "İki", "gloss_en": "Two", "cat": "Sayılar",
        "concepticon": None, "proto": "*ẹkki",
        "note": "Sibirya'da intervokalik /k/ erimesi (iyi, iygi) dışında kök bütünüyle aynı; ikizleşme çoğunda korunur.",
        "cells": [
            ("iki", "iki", "ici", "iki", 10, "*ẹ>i, *kk>k"),
            ("iki", "iki", "ici", "iki", 10, "*ẹ>i, *kk>k"),
            ("iki", "iki", "ici", "iki", 10, "*ẹ>i, *kk>k"),
            ("iki", "iki", "ici", "iki", 10, "*ẹ>i, *kk>k"),
            ("екі", "eki", "jeci", "eki", 10, "*ẹ>e"),
            ("эки", "eki", "eci", "eki", 10, "*ẹ>e"),
            ("ике", "ike", "ice", "ike", 10, "*ẹ>i, *i>e"),
            ("ике", "ike", "ice", "ike", 10, "*ẹ>i, *i>e"),
            ("eki", "eki", "eci", "eki", 10, "*ẹ>e"),
            ("eki", "eki", "eci", "eki", 10, "*ẹ>e"),
            ("ikki", "ikki", "icci", "ikki", 10, "İkizleşme (gemination) korundu"),
            ("ikki", "ikki", "icci", "ikki", 10, "İkizleşme korundu"),
            ("иккӗ", "ikkĕ", "iccɘ", "ikkĕ", 10, "*ẹ>i, *i>ĕ, ikizleşme korundu"),
            ("икки", "ikki", "icci", "ikki", 10, "*ẹ>i, ikizleşme korundu"),
            ("ийи", "iyi", "iji", "iyi", 10, "*kk>y (lenisyon)"),
            ("ікі", "iki", "ici", "iki", 10, "*ẹ>i"),
            ("ийги", "iygi", "ijgi", "iygi", 10, "*kk>yg (Sibirya yumuşaması)"),
            ("äkki", "äkki", "æcci", "äkki", 10, "*ẹ>ä, ikizleşme korundu"),
        ],
    },
    {
        "key": "gel", "gloss": "Gel-", "gloss_en": "Come", "cat": "Eylem",
        "concepticon": None, "proto": "*kẹl-",
        "note": "Aglütinatif yapının çekirdeğindeki fiil kökü, tüm kollarda olağanüstü kararlı.",
        "cells": [
            ("gel-", "gel-", "ɟel", "gel-", 11, "*k>g, *ẹ>e"),
            ("gəl-", "gəl-", "ɟæl", "gəl-", 11, "*k>g, *ẹ>ə"),
            ("gel-", "gel-", "ɟel", "gel-", 11, "*k>g, *ẹ>e"),
            ("gel-", "gel-", "ɟel", "gel-", 11, "*k>g, *ẹ>e"),
            ("кел-", "kel-", "cel", "kel-", 11, "*ẹ>e"),
            ("кел-", "kel-", "cel", "kel-", 11, "*ẹ>e"),
            ("кил-", "kil-", "cil", "kil-", 11, "*ẹ>i"),
            ("кил-", "kil-", "cil", "kil-", 11, "*ẹ>i"),
            ("kel-", "kel-", "cel", "kel-", 11, "*ẹ>e"),
            ("kel-", "kel-", "cel", "kel-", 11, "*ẹ>e"),
            ("kel-", "kel-", "cel", "kel-", 11, "*ẹ>e"),
            ("kel-", "kel-", "cæl", "kel-", 11, "*ẹ>e (ä)"),
            ("кил-", "kil-", "cil", "kil-", 11, "*ẹ>i"),
            ("кэл-", "käl-", "cæl", "käl-", 11, "*ẹ>ä"),
            ("кел-", "kel-", "cel", "kel-", 11, "*ẹ>e"),
            ("кил-", "kil-", "cil", "kil-", 11, "*ẹ>i"),
            ("кел-", "kel-", "cel", "kel-", 11, "*ẹ>e"),
            ("käl-", "käl-", "cæl", "käl-", 11, "*ẹ>ä"),
        ],
    },
    {
        "key": "gumus", "gloss": "Gümüş", "gloss_en": "Silver", "cat": "Temel / Kültür",
        "concepticon": None, "proto": "*kümüĺ",
        "note": "Maden adı erken ticaret ağlarını gösterir; Tuvaca möngün Moğolca alıntı (boşluk).",
        "cells": [
            ("gümüş", "gümüş", "ɟyˈmyʃ", "gümüş", 12, "*k>g, *ĺ>ş"),
            ("gümüş", "gümüş", "ɟyˈmyʃ", "gümüş", 12, "*k>g, *ĺ>ş"),
            ("kümüş", "kümüş", "cyˈmyʃ", "kümüş", 12, "*k korundu, *ĺ>ş"),
            ("gümüş", "gümüş", "ɟyˈmyʃ", "gümüş", 12, "*k>g, *ĺ>ş"),
            ("күміс", "kümis", "kyˈmɪs", "kümis", 12, "*ĺ>ş>s, *ü>i"),
            ("күмүш", "kümüş", "kyˈmyʃ", "kümüş", 12, "*ĺ>ş"),
            ("көмеш", "kömeş", "køˈmeʃ", "kömeş", 12, "*ü>ö, *ĺ>ş"),
            ("көмөш", "kömöş", "køˈmøʃ", "kömöş", 12, "*ü>ö, *ĺ>ş"),
            ("gúmis", "gúmis", "gyˈmɪs", "gúmis", 12, "*k>g, *ĺ>s"),
            ("kümüş", "kümüş", "kyˈmyʃ", "kümüş", 12, "*ĺ>ş"),
            ("kumush", "kumush", "kuˈmuʃ", "kumush", 12, "*ü>u, *ĺ>ş"),
            ("kümüsh", "kümüsh", "kyˈmyʃ", "kümüsh", 12, "*ĺ>ş"),
            ("кӗмӗл", "kĕmĕl", "kɘˈmɘl", "kĕmĕl", 12, "*ü>ĕ, *ĺ>l (lambdasizm)"),
            ("көмүс", "kömüs", "køˈmys", "kömüs", 12, "*ü>ö, *ĺ>s"),
            ("мөңгүн", "möngün", "mœŋˈgyn", "möngün", 13, "Alıntı/boşluk (Moğolca möngü)"),
            ("кӱмӱс", "kümüs", "kyˈmys", "kümüs", 12, "*ĺ>s"),
            ("кӱмӱш", "kümüş", "kyˈmyʃ", "kümüş", 12, "*ĺ>ş"),
            ("kümüş", "kümüş", "kyˈmyʃ", "kümüş", 12, "*ĺ>ş"),
        ],
    },
    {
        "key": "ev", "gloss": "Ev", "gloss_en": "House", "cat": "Temel / Kültür",
        "concepticon": None, "proto": "*eb",
        "note": "Göçebe barınak kavramında yoğun çeşitlilik; Çuvaşça pürt ve Yakutça jiä ayrı köklerden (iki boşluk).",
        "cells": [
            ("ev", "ev", "ev", "ev", 14, "*b>v"),
            ("ev", "ev", "ev", "ev", 14, "*b>v"),
            ("öý", "öý", "œj", "öý", 14, "*e>ö, *b>ý"),
            ("ev", "ev", "ev", "ev", 14, "*b>v"),
            ("үй", "üy", "yj", "üy", 14, "*e>ü, *b>y"),
            ("үй", "üy", "yj", "üy", 14, "*e>ü, *b>y"),
            ("өй", "öy", "œj", "öy", 14, "*e>ö, *b>y"),
            ("өй", "öy", "œj", "öy", 14, "*e>ö, *b>y"),
            ("úy", "úy", "yj", "úy", 14, "*e>ü, *b>y"),
            ("ev", "ev", "ev", "ev", 14, "*b>v"),
            ("uy", "uy", "uj", "uy", 14, "*e>u, *b>y"),
            ("öy", "öy", "œj", "öy", 14, "*e>ö, *b>y"),
            ("пӳрт", "pürt", "pyrt", "pürt", 15, "Leksikal yenilik (ayrı PT kökü *bürk ile bağlantılı)"),
            ("дьиэ", "jiä", "d͡ʑiæ", "jiä", 16, "Leksikal yenilik / boşluk"),
            ("өг", "ög", "œʁ", "ög", 14, "*e>ö, *b>g (Sibirya / Moğolca etkisi tartışmalı)"),
            ("іб", "ib", "ib", "ib", 14, "*e>i, *b korundu"),
            ("эп", "ep", "ep", "ep", 14, "*b>p"),
            ("häv", "häv", "hæv", "häv", 14, "*e>ä, *b>v, *p->h- türemesi"),
        ],
    },
]


def build():
    cats = []
    out_concepts = []
    for c in CONCEPTS:
        assert len(c["cells"]) == len(LANGS), f'{c["key"]}: {len(c["cells"])} hücre, {len(LANGS)} dil bekleniyor'
        if c["cat"] not in cats:
            cats.append(c["cat"])
        cells = []
        for (name, iso, branch), cell in zip(LANGS, c["cells"]):
            native, latin, ipa, morph, cogid, rule = cell
            cells.append({"lang": name, "iso": iso, "branch": branch, "native": native,
                          "latin": latin, "ipa": ipa, "morph": morph, "cogid": cogid, "rule": rule})
        out_concepts.append({"key": c["key"], "gloss": c["gloss"], "gloss_en": c["gloss_en"],
                             "cat": c["cat"], "concepticon": c["concepticon"], "proto": c["proto"],
                             "note": c["note"], "cells": cells})
    return {
        "_meta": {
            "source": "deepsearch 18 — Genişletilmiş Kognat ve Leksikal Veri Matrisi (KÖKEN derin araştırma)",
            "method": "faithful transcript (pdfplumber); Savelyev & Robbeets 2020 Bayesian filodilbilim + "
                      "Cambridge Turkic + Wiktionary/Concepticon çapraz-atıf (PDF 'Alıntılanan çalışmalar')",
            "license": "derleme (her hücre kaynağına atıflı); uydurma yok",
            "langs": len(LANGS), "concepts": len(out_concepts), "categories": cats,
            "fields": "native (yerel yazı; Uygurca Arap-yazı romanize), latin, ipa, morph (morfem seg.), "
                      "cogid (kognat set ID — boşluk tespiti), rule (uygulanan ses kuralı)",
            "note": "11 kavram = ds18'de TAM 18-dil matrisi verilenler. Akrabalık kategorisinde tam tablo "
                    "olmadığından kavram eklenmedi (dürüst). cogid farkı = leksikal yenilik/alıntı (gap).",
        },
        "categories": cats,
        "concepts": out_concepts,
    }


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "..", "data", "cognates_deep.json")
    data = build()
    with io.open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    ng = sum(1 for c in data["concepts"] for cell in c["cells"] if cell["cogid"] != c["cells"][0]["cogid"])
    print("cognates_deep.json yazildi: %d kavram x %d dil, kategoriler=%s"
          % (data["_meta"]["concepts"], data["_meta"]["langs"], ",".join(data["categories"])))
    print("  toplam hucre=%d, bosluk(gap) hucre=%d (cogid != baskin)"
          % (len(data["concepts"]) * len(LANGS), ng))
