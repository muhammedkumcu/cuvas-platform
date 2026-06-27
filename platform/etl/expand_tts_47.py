# -*- coding: utf-8 -*-
"""expand_tts_47.py — profiles_tts.json'a 25 yeni dilin Seslendirme (TTS/ASR) durumunu ekler.

Kaynak: deepsearch 6 (`_tts_asr.txt`, Türk dilleri açık TTS/ASR ekosistemi). UYDURMA YOK:
- Gerçek model yalnız ds6'da ADI GEÇEN dillerde (uzn/azb/crh/nog = Meta MMS-TTS / eSpeak / wav2vec2).
- Özel modeli olmayan yaşayan diller → dürüst "açık model yok" + ds6'nın önerdiği yakın-dil ikamesi /
  eSpeak fonem enjeksiyonu yolu (ds6 'Dürüst Boşluk Haritası' bölümü).
- Tarihsel/ölü diller → canlı konuşur olmadığından "seslendirme uygulanamaz" (yazılı korpus dili).

İdempotent: yalnız EKSİK kodları ekler, mevcut 14'ü ezmez. Kodlar profiles_deep.json anahtarlarıyla eşleşir
(böylece build.py'deki `if code in deep` ile profilin 5. bölümü olarak görünür).
"""
import json
import io
import os

# 25 yeni dil — faithful, atıflı (ds6). Anahtarlar profiles_deep.json ile birebir.
NEW_TTS = {
    # ---- Gerçek açık model (ds6'da adı geçen) ----
    "uzn": "TTS: Meta MMS-TTS (uzb-script_cyrillic) — yalnız Kiril eğitildi, Latin girdi önce Kiril'e "
           "çevrilmeli (TurkicNLP); CC-BY-NC 4.0, HF Inference API. piyazon/qutadgu_bilik fine-tune'u "
           "noktalama/sayı hatalarını giderir. ASR: Gearnode/qwen3-asr-uzbek (Apache 2.0) Whisper "
           "halüsinasyonlarını çözer (~104K örnek).",
    "azb": "TTS: Meta MMS-TTS Güney lehçesi için ayrı kontrol noktası sunar (azb); Kuzey (azj) ile iki "
           "ayrı MMS modeli mevcut. CC-BY-NC 4.0, HF Inference API. Dedicated yüksek-kalite model yok; "
           "Türkçe/Azerice fonetik yakınlığından XTTS ile sıfır-atışlı ses klonlama bir alternatif.",
    "crh": "TTS: Meta MMS-TTS (crh) kontrol noktası var; CC-BY-NC 4.0. ASR: robinhad/wav2vec2-xls-r-300m-crh "
           "açık modeli mevcut (Apache 2.0). Oğuz-Kıpçak hibrit fonolojisi yakın-dil ikamesini "
           "(Türkçe/Tatarca) kolaylaştırır.",
    "nog": "TTS: hem Meta MMS-TTS (nog) hem eSpeak NG (nog) destekler — küçük Kıpçak dilleri içinde nadir "
           "çift kapsam. MMS CC-BY-NC 4.0 (bulut), eSpeak GPLv3 (tarayıcı WASM). Dedicated ASR yok; "
           "yakın-dil (Kazakça/Karakalpakça) transferi gerekir.",
    # ---- Açık model yok → yakın-dil ikamesi / eSpeak fonem (ds6 'Dürüst Boşluk Haritası') ----
    "uzs": "Dedicated açık TTS/ASR yok. Özbekçe (uzn) MMS-TTS modeli diyalekt sürekliliği nedeniyle "
           "yakın-dil ikamesi olarak kullanılabilir; eSpeak NG Özbekçe (uz) fonem seti taban alınabilir.",
    "gag": "Dedicated açık TTS/ASR yok. Oğuz fonolojisi sayesinde Türkçe Piper (tr_TR) / MMS-TTS yakın-dil "
           "ikamesi yüksek anlaşılırlıkla çalışır; XTTS sıfır-atışlı klonlama bir yol. Latin alfabe entegre eder.",
    "kaa": "Dedicated açık TTS/ASR yok. Kazakça (ISSAI/MMS) + Özbekçe modelleri yakın-dil ikamesi sağlar "
           "(Kıpçak çekirdek + Özbek alıntıları). eSpeak fonem enjeksiyonu MVP altyapısı için uygundur.",
    "krc": "Dedicated açık TTS/ASR yok. Kıpçak fonolojisi için yakın-dil ikamesi (Kumukça/Kazakça) + "
           "Kafkas uvular seslerine (/q x ɣ/) eSpeak fonem kuralı eklenmesi gerekir.",
    "kum": "Dedicated açık TTS/ASR yok. Eski Kafkasya lingua francası olsa da dijital kaynağı zayıf; "
           "yakın-dil ikamesi (Nogayca/Azerice) + eSpeak fonem enjeksiyonu pratik yol.",
    "alt": "Dedicated açık TTS/ASR yok. Güney Sibirya fonolojisi için yakın-dil ikamesi (Kırgızca/Hakasça) "
           "veya XTTS sıfır-atışlı klonlama; eSpeak fonem kuralı eklenebilir.",
    "atv": "Dedicated açık TTS/ASR yok. Kuzey Altay (Yenisey) grubu için Güney Sibirya yakın-dil ikamesi + "
           "eSpeak fonem kuralı tek pratik yol.",
    "slr": "Dedicated açık TTS/ASR yok. Çin'de izole; ünlü uyumu kaybı + Tibet/Çin teması özel fonem "
           "gerektirir. Yakın-dil ikamesi sınırlı (Türkmence kökü); eSpeak fonem enjeksiyonu en uygulanabilir.",
    "ili": "Dedicated açık TTS/ASR yok. Karluk yakın-dili (Uygurca MMS / Özbekçe) ikamesi gerekir; "
           "kontak özellikleri için eSpeak fonem kuralı eklenebilir.",
    "aib": "Dedicated açık TTS/ASR yok (Uygurca tabanlı Farsça-sözcüklü kriptolekt). Uygurca MMS-TTS "
           "yapısal taban sağlar; özel gizli sözcük dağarcığı sentezi sınırlar.",
    "dlg": "Dedicated açık TTS/ASR yok — ds6 boşluk haritasında açıkça anılır. Yakutça (sah) MMS-TTS "
           "yakın-dil ikamesi (Yakut+Evenki melezi); eSpeak fonem enjeksiyonu MVP için uygundur.",
    "ybe": "Dedicated açık TTS/ASR yok. Preaspirasyon (oHtis) gibi özel sesler yakın-dil ikamesini "
           "zorlaştırır; eSpeak fonem kuralı yazımı tek pratik yol.",
    "kmz": "Dedicated açık TTS/ASR yok. Türkmence↔Azerice geçiş dili; Türkmence (tuk MMS-TTS) veya Azerice "
           "yakın-dil ikamesi yüksek anlaşılırlık verir.",
    # ---- Tarihsel / ölü diller → seslendirme uygulanamaz (yazılı korpus) ----
    "oui": "Tarihsel/ölü dil (8.–14. yy Eski Uygur külliyatı). Canlı konuşur olmadığından TTS/ASR "
           "uygulanamaz; rekonstrüktif sesletim yalnız akademik amaçlıdır.",
    "chg": "Tarihsel yazı dili (15.–20. yy Çağatayca). Canlı konuşuru yok → TTS/ASR uygulanamaz; metinler "
           "ardılı Özbekçe/Uygurca sesletimiyle yaklaşık okunabilir.",
    "xbo": "Tarihsel/ölü Oğur dili (İdil Bulgar mezar yazıtları). Seslendirme uygulanamaz; Çuvaşça "
           "fonolojisi yalnız rekonstrüksiyon için referans.",
    "xqa": "Tarihsel yazı dili (11.–13. yy Karahanlı; Dîvân, Kutadgu Bilig). Canlı konuşuru yok → TTS/ASR "
           "uygulanamaz; rekonstrüktif okuma akademik.",
    "xzm": "Tarihsel geçiş yazı dili (13.–14. yy Harezm Türkçesi). Seslendirme uygulanamaz (yalnız yazılı "
           "korpus).",
    "otk": "Tarihsel/ölü dil (8. yy Orhun yazıtları, Eski Türkçe). Seslendirme uygulanamaz; rekonstrüktif "
           "sesletim yalnız akademik.",
    "qwm": "Tarihsel kaynak dili (14. yy Codex Cumanicus, Kıpçakça). Canlı konuşuru yok → TTS/ASR "
           "uygulanamaz; ardılı Kıpçak dilleri referans.",
    "zkz": "Tarihsel/ölü dil (Hazarca, yetersiz belgeleme). Seslendirme uygulanamaz; sınıflandırması dahi "
           "tartışmalı.",
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "data", "profiles_tts.json")
    d = json.load(io.open(path, encoding="utf-8"))
    tts = d["tts"]
    added, skipped = [], []
    for code, body in NEW_TTS.items():
        if code in tts:
            skipped.append(code)
        else:
            tts[code] = body
            added.append(code)
    d["_meta"]["source"] = (d["_meta"].get("source", "")
                            + " | +25 dil (deepsearch 6 boşluk haritası): gerçek model uzn/azb/crh/nog, "
                              "yakın-dil ikamesi/eSpeak yaşayan küçük diller, tarihsel diller uygulanamaz.")
    d["_meta"]["lang_count"] = len(tts)
    d["_meta"]["accessed"] = "2026-06-27"
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("profiles_tts.json: +%d dil eklendi (toplam %d). Atlanan (mevcut): %s"
          % (len(added), len(tts), ",".join(skipped) or "yok"))
    print("  eklenen:", ",".join(sorted(added)))


if __name__ == "__main__":
    main()
