# platform/ui — KÖKEN arayüzü (DesignCanvas prototipi)

> Kullanıcının tasarladığı **KÖKEN — "Türk dilleri atlası & laboratuvarı"** arayüzü. Yüksek kaliteli, çalışan bir **prototip**; verisi şimdilik **illüstratif (örnek)**, gerçek kaynak+backend bağlanınca değişecek.
> Güncelleme: 24 Haziran 2026.

## Dosyalar
- **`Morfoloji Platformu.dc.html`** — asıl arayüz (**GÜNCEL sürüm burada**). DesignCanvas formatı (`<x-dc>`, `sc-for`/`sc-if`, `{{ binding }}`). İçinde:
  - üst kısım: template (sidebar + tüm ekranlar, satıriçi stil),
  - alt kısım: `<script type="text/x-dc">` → `class Component extends DCLogic` = **state + veri + mantık (handlers)**.
- **`support.js`** — DesignCanvas **çalışma zamanı** (render motoru). Veri DEĞİL; `.dc.html`'i çalıştırır.
- **`screenshots/`** — ⚠ **ESKİ** (kullanıcı uyardı): güncel hâl koddadır, screenshot'lar değil.
- `thumbnail.png` — küçük önizleme.

## Mimari (nasıl çalışıyor)
DesignCanvas reaktif bileşeni: `state` değişince template yeniden render olur. `{{ x }}` ifadeleri `Component`'in alanlarına/getter'larına bağlanır; `onClick="{{ handler }}"` metodları tetikler. Tüm uygulama tek dosyada, harici framework yok (yalnız `support.js` runtime).

## Modüller (ekranlar) — `state.screen`
`home · analiz · paradigm · cognate · compare(rows/sound/tree/map) · distance · profile · history · learn(hub/lesson/flash/done) · research · sources`
Ek katmanlar: **mod** (`learner`/`expert` — uzman modda FST çözümlemesi + ham etiket + kaynak/lisans görünür), **script** (`cyrillic`/`latin` — yerleşik translit: `BASECYR`+`TRANSLIT`).

## VERİ SÖZLEŞMESİ — `.dc.html` içindeki sabitler (gerçek veriyle DEĞİŞTİRİLECEK)
| Sabit | İçerik | Gerçek kaynak (bkz. `platform/KAYNAKLAR.md`) |
|---|---|---|
| `WORDS` | analiz edilmiş kelimeler + morfemler + diller-arası kognatlar | **Apertium FST** (analiz) + SavelyevTurkic |
| `PARADIGM` | çekim tabloları (hâl×sayı, fiil) | **Apertium autogen** + UniMorph |
| `COGNATES` | kognat ağı düğümleri | **SavelyevTurkic CLDF** (cognates.csv) + NorthEuraLex |
| `SOUND` | ses denklikleri + örnekler | #3/#3b derlemeleri (kurallar) |
| `FAMILY`/`TIMELINE`/`HISTORY` | soy ağacı, zaman çizelgesi | Glottolog + #4 (Bölüm B/K) |
| `MAP` (x,y) | harita konumları | **SavelyevTurkic lat/long** → harita izdüşümü |
| `DISTAXES`/`LANGVEC` | 5-eksenli uzaklık (filo/leks/anla/tipo/coğr) | #4 (J.1-3) + SavelyevTurkic(leks) + WALS(tipo) + lat/long(coğr) |
| `LANGPROFILE` | 14 dil profili (EGIDS, konuşur, yazı, bölge) | Glottolog AES + #4 (Bölüm C/E) |
| `SOURCES`/`USAGE` | kaynak kütüğü + modül→kaynak | `platform/KAYNAKLAR.md` ile senkron |
| `FLASHCARDS`/`LESSONS`/`WORKSHOPS`/`BADGES` | ICALL içerik | apertium üretim + ders tasarımı |

## Build (gerçek veri enjeksiyonu) — `build.py`
> **Kaynak dosya (`Morfoloji Platformu.dc.html`) ASLA elle düzenlenmez** — o senin tasarım export'un, tek doğruluk. Gerçek veri ayrı bir **build adımında** enjekte edilir:
```
python platform/ui/build.py        # -> platform/ui/dist/index.html (+ support.js)
```
`build.py`, kaynağı + `platform/data/*.json`'u okuyup gerçek-veri sürümünü `dist/`'e üretir. **Sen tasarımı tekrar export edince → sadece `build.py`'yi tekrar çalıştır.** Şu an enjekte edilen: `LANGPROFILE` canlılık alanları ← **Glottolog AES** (Dil Profilleri + Canlılık gerçek; profil modülünün "⚠ örnek" rozeti kalktı) + canlı API tabanı (`KOKEN_API`).

**Önizleme:** `python -m http.server 8080` (repo kökünde) → `http://127.0.0.1:8080/platform/ui/dist/index.html`.

## Çalışma yöntemi (her modül için döngü)
1. **Kaynağı çek** (`sources/`) → `platform/KAYNAKLAR.md` güncelle.
2. **Çıkar** (`platform/etl/`): kaynaktan UI sabitine uygun **kaynaklı JSON** (`platform/data/`).
3. **Backend** (VM, FastAPI): canlı FST analiz/üretim/paradigma (`platform/backend/`).
4. **`build.py` ile enjekte et:** statik veriyi sabitlere bak; canlı uçları API'ye bağla; ilgili modülün **"⚠ örnek"** rozetini kaldır.
5. **Önizle & doğrula** (yukarıdaki server).

## Önemli notlar
- **MVP dilleri:** tur, aze, kaz, kir, uzb, uig, tat, bak, chv, sah (UI ayrıca tyv/kjh/şor/halaç profili taşır — tehlikedeki odak).
- Dosya adında boşluk var (`Morfoloji Platformu.dc.html`) — kullanıcı yeniden export edince üzerine binsin diye **özgün ad korundu**.
- Apertium **Windows'ta çalışmaz**; canlı analiz **VM'de** (bkz. `DEVAM.md` §2).
