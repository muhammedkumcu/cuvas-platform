# KÖKEN — Geliştirme Günlüğü (paper için kalıcı kayıt)

> Kronolojik mühendislik günlüğü: **ne yaptık, hangi kararı NEDEN aldık, neyi nasıl test ettik, metrikler nasıl değişti, nelere dikkat ettik.** Amaç: paper yazımında her şey elde olsun. Tamamlayıcı belgeler: `MORFOLOJI-DEGERLENDIRME.md` (yöntem+test detayı), `KAYNAKLAR.md` (veri provenance), `plan/YOLCULUK-VE-VAZGECILENLER.md` (terk edilenler), `DEVAM.md` (anlık durum). Bu günlüğe **her oturumda yeni giriş eklenir.**

---

## FAZ 0 — Kendi morfoloji motoru (TERK; detay: YOLCULUK-VE-VAZGECILENLER.md)
- Türkmence (TurkmenFST) kural-tabanlı motorunu Çuvaşça için tekrarladık: 63.5K girişlik 4-kaynaklı sözlük, Python fonoloji/morfotaktik motoru, %75 token kapsamı, **karışık-yazı kirliliği bulgusu %45.85**.
- **Karar / gerekçe:** apertium-chv zaten olgun (~%85, analiz+üretim). "Windows'ta apertium çalışmaz" gerekçesi YANLIŞ çıktı (Linux VM'de hfst+turkicnlp sorunsuz). → kendi motoru terk; **olgun aracı yeniden icat etme, üstüne değer kat.**
- **Ders:** "X kullanılamaz" deme, KANITLA (ortam-engelini genel imkânsızlık sanma).

## FAZ 1 — Pivot: çok-dilli Apertium platformu (KÖKEN)
- Tek-dilli kendi-motor → **~20 Türk dili için Apertium-temelli morfoloji + karşılaştırma + araştırma platformu.** Çift kitle: öğrenen + araştırmacı (kritik). Düşük-kaynaklı/tehlikedeki dillere (Çuvaş çekirdek) özel önem.
- **3-katman mimari:** (1) Backend = FastAPI, apertium FST sarıcı (Linux VM; `automorf`=analiz, `autogen`=üretim). (2) Veri = locale çekilmiş kaynaklı JSON. (3) UI = DesignCanvas tasarımı, **`build.py` ile enjeksiyon** (.dc.html elle düzenlenmez).
- MVP 10 dil: tur, aze, kaz, kir, uzb, uig, tat, bak, chv, sah.

## FAZ 2 — Veri katmanı (gerçek, kaynaklı, çapraz-kontrollü)
- **İlke:** PDF doğrudan veri değil; işaret ettiği seti locale çek, çapraz-kontrol et, atıf+lisans ver, **uydurma yok** (kaynak yoksa null). Detay: `KAYNAKLAR.md`.
- Çekilen+çıkarılan: SavelyevTurkic CLDF (kognat, 905 set/254 kavram, CC-BY-4.0), Glottolog (sınıflandırma+AES canlılık), WALS (tipoloji), Lindsay (anlaşılabilirlik), Wikipedia (profil metni, çapraz-kontrollü). 5/5 uzaklık ekseni kaynaklı.

## FAZ 3 — UI entegrasyonu + canlı API
- `build.py` string-enjeksiyon: tasarım export'una gerçek veri + canlı API çağrıları enjekte → `dist/index.html`. (Apostrof/encoding tuzakları: `json.dumps`; cp1254 konsol → UTF-8 dosya + Read ile doğrula.)
- Modüller canlıya bağlandı: Analiz, Paradigma (+fiil), Kognat, Karşılaştır, Uzaklık, Profiller, Harita, Araştırmacı Merkezi (CSV/JSON/CoNLL-U export).
- **Kullanıcı geri bildirimiyle düzeltmeler:** üst-bar dil seçici kaldırıldı (her ekranda kendi girişi + kompakt "Otomatik" seçici); export barları kaldırıldı (tablolarda kopyala); sidebar XP kaldırıldı; örnek kökler dil-dengeli; "nasıl çalışır?" ipuçları; Açık API dürüst etiketlendi.

## FAZ 4 — Morfoloji kalitesi: YÜZEY BÖLÜMLEME (bu projenin NLP nüvesi)

### 4.1 Problem
Apertium **lemma + morfolojik etiket** verir ve ses olayında bile DOĞRUDUR: `kitabımızda → kitap<n><px1pl><loc>` (lemma=kitap, kitab değil). Ama **yüzeydeki hece sınırını** (kitab|ımız|da) vermez. Öğrenen+araştırmacı için gerçek ekleri (ler, de) göstermek istiyoruz.

### 4.2 İlk yaklaşım — kümülatif üretim + string farkı (yetersiz)
`gen(lemma<n><nom>)`, `gen(<pl><nom>)`… üretip ardışık farkını al. **Sorun:** ses olayında (kitap→kitab) gövde-ek sınırı kayıyor; ortak-önek farkı yanlış sonuç veriyor (kitap+bımızda). Ayrıca yüzey gövdesini (kitab) izole edemiyor.

### 4.3 Deepsearch (iki prompt: `arastirma/5*.prompt.md`; çıktı: `_nlp_araclari.txt`, `_nlp_envanteri.txt`)
- **Türkçe:** Zemberek doğrudan yüzey morfem verir (Apache-2.0, JPype; zemberek-python overflow bug'lı) — opsiyonel üst-kalite.
- **Tüm diller (FST'ye dokunmadan):** **Needleman-Wunsch karakter hizalaması + fonolojik ceza matrisi** (p~b, k~ğ, I~ı/i/u/ü = sıfır ceza). Evrensel, saf Python. Morfessor/BPE = uygunsuz (gramer sınırına saygısız).
- **Diller-arası:** apertium `.dix` iki-dilli sözlükler (deterministik); NLLB red (CC-BY-NC + morfoloji kaybı).

### 4.4 Uygulama — NW-hizalama (deepsearch + kullanıcının allomorf fikrinin birleşimi)
`backend/app.py`: kümülatif üretim (nom-sonlu ara biçimler) → ardışık biçimleri NW ile hizala (skor: aynı+3, yumuşama+2, sesli~sesli+1, boşluk−2) → ek = **önden-çapalı** (k≈len(prev)) en iyi bölme (tekrar-altdizi + ünlü düşmesine dayanıklı). **El-allomorf tablosu GEREKMEZ** (tek dil-özel şey fonolojik denklik; Latin+Kiril+Arap geneli).
- **Ses olayı çıktısı:** lemma vs yüzey-gövde NW farkı → `sound_changes` (p→b "ünsüz yumuşaması" vb.) — hem öğrenci hem araştırmacı için ayırt edici özellik.

### 4.5 ★ Kritik bulgu — ANALİZ SEÇİMİ
İlk test: align %73 (kaz), %88 (tat/bak). **Kök neden:** `/segment` `analyses[0]`'ı kullanıyordu; FST birden çok analiz döner ve **ilki çoğu zaman yanlış POS (isim yerine fiil)**: `kanat→kana+t(fiil)`, `жолдың/оҕо` fiil okunuyor → align tutmuyor.
- **Düzeltme:** tüm analizleri dene, **align EDEN İSİM** analizini seç.
- **Etki:** kaz %73→**100**, tat/bak %88→**100**, tüm dillerde %100 align. (Tek satırlık fikir, en büyük kazanım — paper'da vurgulanmalı.)

### 4.6 Test metodolojisi — round-trip (gold = üretim)
`backend/segment_eval.py`: bilinen etiketlerden form ÜRET (gold yapı) → `/segment` ile çöz → beklenen ek sayısı + yeniden-üretim tutuyor mu. Dil başına aday isim kökleri (geçersiz olanlar `gen(lemma<n><nom>)` boşsa otomatik elenir), hâl×çokluk×iyelik kombinasyonları. **10 MVP dili, 1700+ form.**

### 4.7 Sonuçlar (analiz-seçimi düzeltmesi sonrası)
| dil | form | align% | ek-sayı% | yeniden% |
|----|----:|----:|----:|----:|
| aze, kaz, kir, uzb, tat, bak | 105–210 | 100 | **100** | ~95 |
| uig | 189 | 100 | 98.9 | 85.7 |
| sah | 108 | 100 | 99.1 | 75.9 |
| tur | 252 | 100 | 98.8 | 94.8 |
| chv | 162 | 100 | 92.6 | 72.2 |

### 4.8 Hangi dilde NİYE zorlandık (paper için hata analizi)
- **uig:** apertium-uig **Arap yazısı** bekler; ilk testte Latin seed → "0 form". Arapça seed ile sorunsuz (`كىتاب+لار+دا`). → test artefaktıydı, gerçek boşluk değil.
- **chv (en zayıf, %92.6):** Çuvaşça **iyelik (px3sp)** ve bazı hâl ekleri farklı morfotaktik; nom-sonlu kümülatif ara biçimler her zaman temiz hizalanmıyor (`кӗнеки`, `ҫуртне`). Çekirdek dilimiz → öncelikli ince ayar.
- **tur (~%1):** **ünlü düşmesi + iyelik** etkileşimi (burun→burn, `burnunda` 2 yerine 1 ek).
- **sah (~%1):** birkaç kök kenar durumu (`оҕо`).

### 4.9 Görüntüleme kararları (linguistik doğruluk + tutarlılık)
- **Kök kutusu = SÖZLÜK biçimi (lemma: kitap)**, yüzeydeki ses-değişmiş gövde (kitab) DEĞİL; ses olayı ayrı **SES OLAYI rozetinde**. Gerekçe: kanonik kök linguistik olarak doğru; öğrenci sözlükte "kitap" arar.
- **Katman ağacı = GERÇEK kümülatif yüzey** (`/segment` `forms`: kitap→kitabımız→kitabımızda, ses olayı dahil) — morfem-metni birleştirmek "kitapımız" üretiyordu (yanlış); düzeltildi.

### 4.10 Kapsam sınırları (dürüst — paper'da belirtilecek)
- **İsim:** tam (NW-align; yeniden-üretim %92–95). **Fiil:** ✅ NW-align (`_segment_verb_align`) — kök + kaynaşık zaman·kişi eki + ses olayı (zaman+kişi portmanteau olduğu için 2-katman). **Sıfat/zarf:** sınırlı (isim okuması varsa isim gibi; türemiş sıfat/zarf ekleri henüz bölünmüyor). Genişletme = gelecek (sıfat/zarf için kümülatif şablon).
- `/segment` bağlı yerler: **Analiz** (applySegment) + **Karşılaştır** (runCompare/crosslang). Araştırmacı Merkezi ham etiket (FST çıktısı) gösterir — araştırmacı için uygun.

### 4.11 Cila (bu oturum)
- **Kaynaşık çöküş (chain-check):** ek dizisi kelimenin gerçek son-eki değilse (Çuvaşça iyelik+hâl не, Uygurca çoğul+iyelik allomorfisi) → kök + TEK kaynaşık ek. **Yeniden-üretim doğruluğu yükseldi** (chv 72→93, sah 76→93, uig 86→94); ek-sayısı proxy'si düştü (füzyonun dürüst yansıması). Basit çoğul/hâl tam ayrışır.
- **Fiil bölümleme** eklendi (yukarıda).
- **Joshi kaynak sınıfı (0–5)** dil profillerine rozet (envanter PDF'i).

## FAZ 5 — Diller-arası eşdeğer (✅ YAPILDI, isimlerde güçlü)
- Hedef: aranan kelimeyi TÜM Türk dillerinde canlı göster (statik "okuduk" gibi). Yöntem (deepsearch kararı): **apertium `.dix` boru hattı** — kaynak dilde analiz → `.dix` ile kök eşle → hedefte AYNI etiketlerle üret.
- **Uygulama:** `.dix` dosyaları GitHub'dan VM'e indirildi (`/root/koken_api/dix/`: tur-aze, tur-kir, tur-tat, tur-uzb, kaz-tat, kaz-kir, tat-bak; GPL-3.0). Backend `_load_dix()` regex ile lemma→lemma grafiği kurar; `_map_lemma()` BFS pivot (doğrudan çift yoksa tur→tat→bak). `/crosslang {lang,word}` ucu: en eşlenebilir analizi seç → her hedefe kök eşle → hedef autogen ile AYNI etiketlerle üret → üretebilen hedefler döner.
- **Sonuç (test):** `evlerde` → 7 dil (aze:evlerde, kaz:үйлерде, kir:үйлөрдө, uzb:uylarda, tat:өйләрдә, bak:өйҙәрҙә); `kitabımızda` → 6 dil (iyelik dahil: kaz:кітабымызда…); `kaz баласы` → tur:çocuğu + 5 dil. **Deterministik, morfolojik sadık.**
- **UI:** Karşılaştır "dizilim" `/crosslang` + her dilin `/segment`'i → renkli morfem kutuları (statik okuduk deneyimi, CANLI). Kaynak dil: ekran seçicisi ya da otomatik algıla.
- **Kapsam sınırı (dürüst):** `.dix` grafiği tur/aze/kaz/kir/uzb/tat/bak'ı kapsar. **chv/sah/uig için iki-dilli pair YOK** → o hedefler dönmez. Fiil `<ger_past>` gibi dile-özgü etiketler hedefte üretmeyebilir (atlanır). Sözlükte olmayan kök eşlenmez. Genişletme: daha çok `.dix` + Savelyev CLDF (254 kavram) fallback.

## OTURUM GİRİŞİ (bu oturum) — özet
1. **Kök kutusu = lemma** (kitap), ses olayı ayrı rozet; **katman ağacı = gerçek yüzey** (`forms`: kitap→kitabımız→kitabımızda) — morfem-metni birleştirme bug'ı (kitapımız) giderildi.
2. **NW-hizalama yüzey bölümleme** + **analiz-seçimi düzeltmesi** (align eden isim) → 10 dil round-trip testi (`segment_eval.py`, 1700+ form): %100 align, ~%98 ek-sayı (chv %92.6).
3. **Ses olayı rozetleri** her dilde doğrulandı (Latin+Kiril voicing).
4. **★ Diller-arası `/crosslang` motoru** (apertium `.dix`) — aranan kelime tüm Türk dillerinde canlı; Karşılaştır'a bağlandı.
5. Kalıcı **GELISTIRME-GUNLUGU.md** oluşturuldu (paper için).

---

## SES OLAYI doğrulaması (diller arası, bu oturum)
Voicing çiftleri Latin+Kiril kapsıyor; rozetler her dilde çalışıyor: tur p→b/ç→c/k→g, kaz/tat п→б, aze p→b — DOĞRU. Bazı dillerde "yok" çünkü FST'nin sözlük biçimi zaten sesli (uzb *kitob*, bak *китаб*) → doğru davranış.

---

## YAPILANLAR (bu ek-oturum) ✅
- **A) Joshi kaynak sınıfı (0–5)** dil profillerine rozet (envanter PDF'i). • **B) Fiil yüzey bölümleme** (NW-align). • **C) chv kaynaşık-çöküş cilası** (yeniden-üretim ↑). • **D) Diller-arası genişletme:** chv-tat + kaz-uig `.dix` → Çuvaşça+Uygurca grafiğe bağlandı; `/crosslang` çoklu-analiz → fiil cross-lang (attım→7 dil). `fetch_dix.sh` (reproducibility).

## EK-OTURUM (deepsearch 5c uygulandı + (b) + planlama)
- **Deepsearch 5c sonucu (`_morfoloji_plani.txt`) uygulandı:** chv-tur (31K) + kaz-sah `.dix` → 10/10 dil cross-lang'a bağlandı (хӗр→kız, göz→харах); **fiil TAM normalizasyonu** (TAG_NORM) → fiil cross-lang (attım→8 dil). Deepsearch ayrıca **füzyonel ayrışmanın bölünebilir** olduğunu kanıtladı (chv -не=+i+n+e; chv sırası Kök+İyelik+Çoğul+Hâl) → Faz 1.1.
- **✅ (b) ses denklikleri kanıt-destekli + kognata bağlı** (kullanıcı kararı): 4 kural Savelyev verisinden kanıtlı (rotasizm 36, lambdasizm 29, y->ś 14, proto-fonem temelli); kognat→kural vurgusu. `build.py: sound_evidence + build_cognates ruleIdx`.
- **Planlama:** `plan/YOL-HARITASI.md` fazlı + DEEPSEARCH İHTİYAÇ HARİTASI; yeni notlar yerleşti (kollar açıklayıcı, derin profiller, kaynaklar güncelleme, Hakkında). Deepsearch promptları hazır: `6` TTS, `7` LLM/HF, `8` sınıflandırma çerçevesi, `9` kol-bazlı derin profiller.

## EK-OTURUM (25 Haz) — deepsearch 8 işlendi: KOLLAR AÇIKLAYICI (Faz 2.5 ✅)
- **Tüm deepsearch sonuçları geldi** (6 TTS, 7 LLM/HF, 8 sınıflandırma, 9.1-9.5 derin profiller A-E) → locale çıkarıldı (`_siniflandirma.txt`, `_profil_*.txt`; pdfminer, PDF gitignore, `_*.txt` commit'li).
- **Veri çapraz-kontrolü (uydurma denetimi):** deepsearch 9.5 (Çuvaş+Argu) yetkili sayıları `profiles.json` ile örtüştü — chv 740K/2020 EGIDS 6b, Joshi chv=1/klj=0, **Çuvaş morfotaktik sıra Kök+İyelik+Çoğul+Hâl (xĕr-ĕm-sen-čen) bizim uyguladığımızı doğruladı**. Tutarsızlık yok.
- **Faz 2.5 YAPILDI (kullanıcının deepsearch 8 sonrası kararıydı):**
  1. **"Tarih & Köken" ekranına "Türk dillerinin altı kolu" kartı** — 6 Johanson kolu (Oğur/Argu/Sibirya/Karluk/Kıpçak/Oğuz), her biri pedagojik tanım + ayırt edici izogloss + örnek kelime + bölge/tarih. Johanson "altın standart" + Savelyev & Robbeets 2020 Bayes doğrulaması atfı.
  2. **Karşılaştır>Soy ağacı = Bayes Maximum Credibility Tree** (basit 5 satır → 14 düğüm gerçek topoloji + mutlak tarihler ~MÖ 66 Oğur / ~MS 474 Kuzey Sibirya).
  - **Karar:** ayrı sol-menü değil, mevcut Tarih & Köken ekranı (kullanıcı). build.py enjeksiyonu (E2 bölümü), Claude_Preview'da doğrulandı (6 kol + 14 düğüm render, logicError null).
- **Sıradaki içerik işleri (deepsearch sonucu ELDE, işlenecek):** Faz 2.6 derin profiller (9.1-9.4 → Dil Profilleri zenginleştirme + çapraz-kontrol), Faz 2.1 TTS (`6`), Faz 2.2 LLM/HF ekosistem (`7`), Faz 2.7 KAYNAKLAR. Deepsearch 8'in işlenmemiş düzeltme önerileri: Sarı Uygurca→G.Sibirya, Kırım Tatarcası geçişken, Salarca areal etiketi.

## Sıradaki / açık işler — bkz `plan/YOL-HARITASI.md` (özet)
1. **ŞİMDİ (deepsearch beklemez):** Faz 1.1 füzyonel ayrışma (NW kanonik-allomorf) · 1.3 harita/UX · 1.4 Hakkında.
2. (Opsiyonel) Türkçe Zemberek (JPype) üst-kalite — NW zaten %98.8, acil değil.
3. Sıfat/zarf yüzey bölümleme (POS başına kümülatif şablon).
4. **.dix kalıcılığı:** VM'de `/root/koken_api/dix/` (gitignored, GPL). VM sıfırlanırsa `bash platform/backend/fetch_dix.sh` (VM'de) ile yeniden indir.
