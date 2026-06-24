# Platform — Hedef Mimari ve Notlar (apertium-temelli, çok-dilli)

> Bu klasör **yeni yönün** (Apertium-temelli çok-dilli Türk dilleri morfoloji + karşılaştırma platformu) kodunu barındıracak. Şu an yalnız `apertium_probe.py` (kanıt) var; platform inşa edilecek.

## Motor (kanıtlandı — VM/Linux)
- `pip install hfst turkicnlp` (Linux'ta sorunsuz; Windows'ta hfst derlenmiyor → **dev'i VM/Linux'ta yap**).
- `turkicnlp.download("<dil>")` → apertium FST'lerini indirir: `~/.turkicnlp/models/<dil>/<script>/morph/apertium/`
  - `<dil>.automorf.hfst` = ANALİZ (yüzey→kök+etiket), `<dil>.autogen.hfst` = ÜRETİM (etiket→yüzey).
- hfst ile doğrudan: `hfst.HfstInputStream(path).read().lookup("...")`.
- Diller (apertium morph backend'i olanlar): chv, tur, aze, tuk, gag, crh, tat, bak, kaz, kir, kaa, krc, kum, nog, uzb, uig, alt, kjh, tyv, sah (+klj kısmi).
- **Üretim örneği (chv):** `кӗнеке<n><pl><dat>` → `кӗнекесене`; `вула<v><tv><pres><p1><sg>` → `вулатӑп`.

## Platform özellikleri (hedef)
- **Morfolojik analiz** ("bu kelimeyi açıkla") — apertium, 20 dil.
- **Üretim + paradigma tabloları** — apertium autogen (etiket setini paradigma şablonlarıyla gez → tablo).
- **ICALL alıştırma** — doğru form + FST-üretimli çeldirici (boşluk-doldurma); oyunlaştırma, SRS.
- **★ Karşılaştırma ağı** — kelime/kavram gir → kökü + diğer Türk dillerindeki kognatları + **ses denklikleri** (rotasizm z→r, lambdasizm ş→l…) + karşılaştırmalı paradigma. Veri temeli: `arastirma/3-turk-dilleri-karsilastirma` derlemesi (PDF geldiğinde).
- **Sanal klavye** (Kiril/Latin/Arap) + harf-çevrim + (sona saklanan) homoglyph normalizasyon.

## Teknik yığın (öneri)
- **Backend:** Python (FastAPI/Flask) — `turkicnlp`/`hfst` ile apertium FST'lerini çağırır, JSON döner. **Linux deploy** (Render/Docker; apertium burada çalışır).
- **Frontend:** hafif SPA (paradigma gezgini, karşılaştırma ağı görünümü, alıştırma). `arsiv/.../web/` UI fikirleri şablon.
- **Değerlendirme/altın standart:** UniMorph (Türk dilleri paradigmaları), Universal Dependencies treebank'leri, Wiktionary — analiz/üretim precision'ı için (ML değil).

## Apertium'a geri katkı (akademik + topluluk)
Platform kullanıldıkça hatalar yüzeye çıkar (Türkmence'de 8 fiil hatası bulmuştuk) → apertium repolarına düzeltme katkısı. Apertium GPL/açık, katkı teşvik edilir.
