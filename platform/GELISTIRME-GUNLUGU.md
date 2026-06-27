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

## EK-OTURUM (25 Haz, devam) — deepsearch 9 işlendi: DERİN PROFİLLER (Faz 2.6 ✅)
- **Kaynak okuma:** 9.1 (Oğuz), 9.2 (Kıpçak), 9.3 (Karluk), 9.4 (Sibirya), 9.5 (Oğur-Argu) tam okundu; 14 displayed dil için ORTAK ŞABLON çıkarıldı.
- **`platform/data/profiles_deep.json`** oluşturuldu: 14 dil × 4 bölüm (Tarih / Yapı & özgünlük / İlişkiler / Dijital güç), atıflı (Joshi sınıfı, apertium kök sayıları, ses kuralları, alfabe tarihleri, kilit isimler: Aşmarin, Feyzhanov, Böhtlingk, Doerfer, Mahtumkulu, Abay, Baytursunov…). build.py `DEEPPROF` enjeksiyonu + `profileSel.deep` birleşimi + profil kartında bölümlü markup. Claude_Preview'da doğrulandı (14 dil render, logicError null).
- **★ ÇAPRAZ-KONTROL = verimizi TEST etti, düzeltmeler yapıldı (kanıtla-iddia-etme ilkesi):** Joshi sınıfı eski değerleri (deepsearch 5 envanteri) deepsearch 9 dil-bazlı verisiyle çelişiyordu → düzeltildi: **az 1→2-3, kk 2-3→3, tt 2-3→1, ug 2-3→1, tyv 0→1, kjh 0→1**. Diğer veriler (Çuvaş morfotaktik sıra, 740K demografi, EGIDS, kol etiketleri) teyitli.
- **Kullanıcı geri bildirimi:** "Tarih & Köken" en altındaki "ırk/gen midir" kara kutusu kaldırıldı (gereksiz görüldü). Sayfa zaman çizelgesiyle temiz bitiyor.
- **Bekleyen:** Faz 2.1 TTS (`_tts_asr.txt`), Faz 2.2 LLM/HF ekosistem (`_llm_hf_ekosistem.txt`), Faz 2.7 KAYNAKLAR. Displayed-dışı diller (gag/crh/uzb/alt…) deepsearch 9 metinlerinde hazır → yatay ölçekte işlenecek.

## EK-OTURUM (25 Haz, devam-2) — deepsearch 6 işlendi: SESLENDİRME ekosistem haritası (Faz 2.1 ✅)
- **`platform/data/profiles_tts.json`** (deepsearch 6) → Dil Profilleri'ne **"Seslendirme (TTS/ASR)" 5. bölümü**: 14 dil × açık model + lisans + kalite + boşluk (Piper/MIT, Meta MMS-TTS/CC-BY-NC, ISSAI Spark-TTS/TatarTTS, eSpeak NG; Common Voice saatleri, WER). build.py'de `deep`'e 5. bölüm olarak merge edildi. Claude_Preview'da doğrulandı (logicError null).
- **Misyon vurgusu (dürüst boşluk haritası):** Çuvaşça'nın MMS'te bile TTS olmaması (yalnız eSpeak NG) ve ~%60 ASR WER'i açıkça gösterildi — "dijital uçurum" kapsayıcılık anlatısı.
- **KALAN = gerçek ses motoru entegrasyonu (ayrı altyapı fazı):** raporun Dinamik Hibrit Yönlendirme mimarisi (Piper ONNX sunucu / MMS HF API / eSpeak NG tarayıcı-WASM) ileride uygulanacak. "▷ Seslendir" hâlâ Web Speech.

## EK-OTURUM (25 Haz, devam-3) — UI tutarlılık + Faz 2.2 EKOSİSTEM (deepsearch 7) ✅
- **Dil Profilleri UI tutarlılık (kullanıcı geri bildirimi):** derin bölümler (Tarih'ten itibaren) sağ özet kartından çıkarılıp iki-sütun gridin ALTINA tam genişlikte (2 sütun) taşındı. Sağ özet kutusu yine kompakt — sol seçiciyle dengeli. Claude_Preview ✅.
- **Faz 2.2 (deepsearch 7) YAPILDI:** `platform/data/ecosystem.json` → **Araştırmacı Merkezi**'ne "Dil × yetenek envanteri" matrisi (13 dil × Üretken LLM/Encoder/Korpus/Konuşma/Benchmark) + zero-resource notu + 8 anahtar org kartı (HF linkli ↗). build.py'de statik üretildi (overflow-x scroll tablo + org grid). Claude_Preview ✅ (logicError null).
- **★ KULLANICI KARARI:** ekosistem matrisine **olgunluk/eksiklik yargısı KONMADI** — "—" yalnız "bu taramada kayıt yok"; caption açıkça "değerlendirme araştırmacıya aittir" der. Nötr envanter ilkesi.
- **Faz 2.7 (KAYNAKLAR) YAPILDI:** uygulama içi SOURCES+USAGE'a `bayes` (Savelyev & Robbeets 2020 + Johanson), `hf` (HuggingFace ekosistemi), `deepds` (KÖKEN derin araştırmalar) eklendi; USAGE eşlemesi güncellendi (Tarih & Köken'e bayes+cldf; Profiller/Araştırmacı'ya hf+deepds). KAYNAKLAR.md defterine 3 yeni veri dosyası + deepsearch satırları. Claude_Preview ✅ (KULLANIM doğru, demo yok).
- **DURUM: TÜM DEEPSEARCH (5,5b,5c,6,7,8,9.1-9.5) + Faz 2.x içerik (2.1/2.2/2.5/2.6/2.7) İŞLENDİ.** Sıradaki deepsearch-bağımsız: 1.1 füzyon-ayrışma (dikkatli), 1.3 harita/UX, 1.4 Hakkında, 3.1 Çuvaşça Dilin Kalbi.

## EK-OTURUM (25 Haz, devam-4) — EKOSİSTEM SAYFASI yeniden tasarımı (Faz 2.2 v2)
- **Kullanıcı geri bildirimi (2.2 v1 matris yetersiz):** durağan tek isim (ör. Türkçe yalnız "TurkmedSTT"), **link yok**, **Zemberek/Apertium atlanmış**, kategori ayrımı yok. İstek: kategori-önce → dil-içinde → **bol DOĞRUDAN link** (HF "güncel takip" arama + en çok indirilen/öne çıkan direkt linkleri); araştırmacıyı çalışmaya götüren launchpad.
- **Plan onaylandı** (plan-mode; placement=ayrı sayfa, ~8 kategori, dil başına hub+4-5 link; kendi web araştırması + uydurma yok).
- **YAPILDI — ayrı "Ekosistem" sayfası** (sol menü ARAŞTIR): `ecosystem.json` kategori-önce yeniden yazıldı; **8 kategori, 101 bağlantı** (LLM/Encoder/ASR/TTS/Veri/Benchmark/Araçlar/Org). Her kategoride hub linkleri + dil-bazlı öne çıkanlar (↗ `target=_blank`). **Eksik araçlar eklendi:** Zemberek (github.com/ahmetaa/zemberek-nlp), TRmorph, Zeyrek, Apertium (per-lang), Stanza, TurkicNLP. build.py: matris Araştırmacı Merkezi'nden kaldırıldı (sade sorgu/API'ye döndü); yeni `eco` ekranı + NAVGROUPS öğesi + `isEco` + sticky anchor-jump kategori navı; USAGE'a Ekosistem. Claude_Preview ✅ (8 kategori, gerçek linkler, anchor-jump, logicError null).
- **Kaynak/doğrulama:** deepsearch 7 (gerçek HF repoları) + **kendi WebSearch'üm** (Zemberek/TRmorph/zeyrek/Starlang, agmmnn/turkish-nlp-resources, OpenLLM-TR & alibayram Türkçe-MMLU leaderboard doğrulandı). Nötr (olgunluk yargısı yok — kullanıcı kararı).
- **Zenginleştirme promptu hazır:** `arastirma/10-ekosistem-derin-linkli.prompt.md` (kategori-yapılı, link+indirme talepli, HF-dışı dahil — sonraki dalga).

## EK-OTURUM (25 Haz, devam-5) — Ekosistem SEKMELERİ + FAZ 1 (1.3 ✅, 1.4 ✅, 1.1 araştırıldı)
- **Ekosistem sekmeleri (kullanıcı geri bildirimi):** kategoriler artık SEKME — basınca yalnız o kategori yerinde açılır (varsayılan Üretken LLM), hepsi tek sayfada değil, jump-scroll yok. Reaktif sc-if (eco_<key>) + ecoTabs/ecoCat. Claude_Preview ✅.
- **Faz 1.4 (Hakkında & İletişim) ✅:** KEŞFET'e sayfa — KÖKEN nedir + Misyon + Veri & motor (6 kaynak kartı) + iletişim (GitHub + e-posta).
- **Faz 1.3 (Harita UX) ✅:** düğüme tıkla → INLINE bilgi kartı (sayfadan çıkmaz; kullanıcı kararı); gerçek koordinat projeksiyonu (Türkçe Anadolu'da); Argu kolu rengi+lejant (Halaçça). 14 dil.
- **Faz 1.1 (füzyon ayrışma) — CANLI ARAŞTIRMA (değişiklik yapılmadı, bilinçli):** `/segment` (chv) gerçek davranış incelendi → **tek-tip bölme YANLIŞ.** Üç sınıf: zaten-doğru / gerçek-portmanteau (ҫуртне, BÖLME) / güvenle-bölünebilir (кӗнекесенче→сен+че). + olası bug (кӗнекине'de iyelik -и- sahte ses-değişimi). Bulgular + plan `MORFOLOJI-DEGERLENDIRME.md`'de. **Backend morfoloji + "%100 doğru" mandası + kullanıcı away → ayrı odaklı, `segment_eval`-doğrulamalı oturumda yapılacak; aceleye getirilip uydurma segmentasyon üretilmedi.**

## EK-OTURUM (25 Haz, devam-6) — Faz 1.1 GÜVENLİ-BÖLME (doğrulandı) + Faz 3.1 (Dilin Kalbi)
- **Faz 1.1 (güvenli füzyon-bölme) ✅ — segment_eval ile DOĞRULANDI:** `app.py`'ye TEMİZ-SINIR bölme (chv pl+hâl: сенче→сен+че; px+hâl portmanteau KORUNDU). VM'ye scp + start.sh ile temiz uvicorn restart (§4.6) + eval. **Sonuç: chv ek-sayı %75.3→%92.0 (+16.7), align %100 & yeniden-üretim %93.2 değişmedi, diğer 9 dil regresyonsuz.** Kalan ~%8 = bilinçli korunan px+hâl portmanteau + `кӗнеки` px3sp-и yutulma bug'ı (ayrı pas). Bulgular+sonuçlar `MORFOLOJI-DEGERLENDIRME.md`'de.
- **Faz 3.1 (Çuvaşça "Dilin Kalbi") ✅:** KEŞFET'e anlatı sayfası — hero + neden paha biçilmez + ses kanunları tablosu (8 kognat + kanıt) + yapı özgünlüğü (4 kart) + tarihsel tanıklar (Bulgar/Feyzhanov/Aşmarin) + dijital uçurum + CTA. Claude_Preview ✅ (CTA→chv profili).
- **Süreç notu:** 1.1 backend olduğundan VM workflow kullanıldı — scp app.py → start.sh (setsid+disown; tek-seferlik SSH `& disown` SIGHUP'a takıldı, start.sh düzeltti) → VM-içi health doğrula → eval. §4.6 uvicorn tuzağı yine geçerli.

## EK-OTURUM (25 Haz, devam-7) — A BLOĞU: 1.1b + kol-düzeltmeleri (tek patch)
- **Faz 1.1b (vokal-sonu iyelik kurtarma) ✅ doğrulandı:** `app.py`'de saf-iyelik + boş-ek durumunda `_suffix` ile sapma-kuyruğu kurtarma. `кӗнеки`→кӗнеке+**и** (ünlü düşmesi е→∅), `ачи`→ача+и. **segment_eval: chv ek-sayı %92.0→%93.2, yeniden-üretim %93.2→%94.4; ünsüz-sonu iyelik (хӗр→хӗрри) + diğer 9 dil regresyonsuz.** Toplam 1.1 (a+b): chv ek-sayı **%75.3→%93.2 (+17.9)**. Kalan ~%6.8 = bilinçli korunan px+hâl portmanteau (doğru çözüm). VM'ye deploy.
- **Kol-düzeltmeleri (deepsearch 8) ✅:** ÖNCE veri çapraz-kontrol — `cognates.json` kol etiketleri ZATEN doğru (CrimeanTatar→Kıpçak, Salar→Oğuz, **SarygYugur→Sibirya** [Karluk değil], Khalaj→Argu). **Yanlış atama yoktu** → uydurma "düzeltme" yapılmadı; bunun yerine Tarih & Köken altı-kol kartına **"Geçişken & sınır diller"** NÜANS notu eklendi (Kırım Tatarcası geçişken / Salarca [areal:Amdo] / Sarı Uygurca adı-yanıltıcı Güney Sibirya). Claude_Preview ✅.
- **Paper notu:** "verimizi test ettik, kol etiketleri deepsearch 8 ile bire bir tutuyor" — değerli bir doğrulama kaydı.

## EK-OTURUM (25 Haz, devam-8) — Deepsearch 10 + YATAY ÖLÇEK PLANI (DİKEY MVP BİTTİ)
- **Deepsearch 10 (ekosistem, linkli+metrik) işlendi:** `_ekosistem10.txt` (25 dil, 128 URL, indirme/yıldız metrikleri) → `ecosystem.json` zenginleştirildi (Trendyol-Asure-12B, Magibu, Turkcell, KazLLM-8B/70B/Qolda, Alloma/behbudiy, Atllama, mmBERT 340K↓, VBART, TY-ecomm-embed, VNLP 287★, Fitrat, sayro-tts, Kazakh_TTS/KSC2, uzbek-stt, whisper-crh/uyghur/tk, CulturaX…). Metrikler not alanında. Claude_Preview ✅. → **Bununla DİKEY MVP (deepsearch-bağımsız) TAMAMLANDI.**
- **Yatay ölçek deepsearch promptları yazıldı (11-18, AYRI dosyalar):** kullanıcı isteği — batch'leri tek dosyada toplama (deepsearch zorlaşıyor). 11 envanter · 12-16 kol-bazlı derin profiller+lehçeler · 17 çapraz-kol ses denklikleri · 18 genişletilmiş kognat (kategorize). Kullanıcı çalıştıracak.
- **Plan dosyaları compact için DİKKATLİCE güncellendi:** DEVAM §0'a "★★ GÜNCEL DURUM" tek-bakış bloğu (dikey MVP bitti + yatay ölçek A/B/C/D + kritik hatırlatmalar) + §4.5 felsefe güçlendirildi (uydurma-yok/test-göster/commit-push/hardcoded). `GELECEK-PLANLAR.md` yeniden yapılandırıldı (A yatay-öncesi UI cilası [kullanıcı notları] · B yatay ölçek · C altyapı · D en son eğitim portalı). YOL-HARITASI durum + Faz 4 güncel.
- **Kullanıcı UI notları (yatay ölçek öncesi, GELECEK-PLANLAR Bölüm A):** kognat kelime-seçici (kategorili), Karşılaştır başlık hardcode'u kaldır, ana sayfa dil-sayısı, harita arka planı+düğüm yoğunluğu, Uzaklık uzun-kutu, Kaynaklar kategorize. + morfolojik üretim & öğren/araştırmacı = gelecek.

## EK-OTURUM (26 Haz, devam-9) — BÖLÜM A: yatay ölçek öncesi UI cilası (A1–A6 ✅, hepsi Claude_Preview doğrulamalı, ayrı commit'ler)
Kullanıcı onayıyla "A baştan sona A1→A6" yapıldı. Hepsi `build.py` enjeksiyonu (.dc.html elle düzenlenmedi), her madde ayrı commit+push.
- **A1 · Kognat kelime-seçici (★ ölçek ön-şartı) ✅:** Düz buton satırı ölçeklenemez → **kategorili + aranabilir** seçici. `COG_CAT` taksonomisi (Leipzig-Jakarta: Vücut/Doğa/Zaman/Sayılar/Soyut; **ds18 ile genişleyecek**), `build_cognates` `cat` alanı, `cognateVals` filtre+kategori-çipleri (sayaçlı) + arama kutusu (`cognateQ`) + boş-durum. Test: kategori sayaçları doğru (Vücut→6 vücut parçası), arama 'gö'→göz, boş-durum çalışıyor. **Karar:** seçici ALTYAPISI şimdi kuruldu (14 kavramla), ölçekte yalnız veri+taksonomi büyür.
- **A2 · Karşılaştır başlık hardcode'u ✅:** "X — diller arası" başlığı TÜM sekmelerde kalıyordu (mantıksız). `compareHeadline` **sekmeye-duyarlı** yapıldı: kelime referansı yalnız dizilim'de; ses denklikleri/soy ağacı/harita'da sekme-başlığı. **Hata bulundu+çözüldü:** D-bloğunda zaten bir `compareHeadline` tanımı vardı → benim eklediğim çift-tanımla çakıştı (JS son-anahtar kazanıyor, hep "okuduk" gösteriyordu); tek-kaynağa indirgendi (D-bloğu tab-aware yapıldı, h2 wrapper içine alındı). 4 sekme doğrulandı.
- **A3 · Ana sayfa güncelliği + dil sayısı dinamik ✅:** Landing'e **katmanlı kapsam şeridi** — 10 dil canlı FST / 23 dil derin profil / 32 dil atlas / 6 kol — **hepsi veriden** (`n_live/n_prof=len(prof)/n_geo=len(lex)/n_branch`), hardcode literal yok. Footer "5 KOL·14 DİL" **stale+yanlış** (gerçek 6 kol — Argu/Karluk/Kıpçak/Ogur/Oğuz/Sibirya) → "6 KOL·32 DİL". Kart "yedi dilde" → "diller arasında" (ölçek-dayanıklı).
- **A4 · Harita arka planı + düğüm yoğunluğu ✅:** **(A4a)** Asıl "saçma" sebebi: arka plan SVG'si (viewBox 1000×560 elle-çizim blob, damlayan kenar) **dotlardan AYRI koordinat sistemindeydi** → coğrafya veriyle hizasız. `build_map_bg()` ile SVG dotlarla **AYNI** `project()` projeksiyonuna (viewBox 0..100) taşındı; iç denizler GERÇEK lat/lon'dan (1°lon≈0.7517x, 1°lat≈1.6949y): Karadeniz, **Hazar (dikey, Azerice batı↔Türkmence doğu kıyı — coğrafi doğru, projeksiyondan ÇIKIYOR)**, Aral, Balkaş, Baykal + meridyen/paralel ızgarası + Akdeniz köşesi. Bölge etiketleri projeksiyon-doğru. **(A4b)** Çakışan düğümler ölçüldü (Çuvaşça↔Tatarca d=1.6; Sibirya üçlüsü Şor/Hakasça/Tuvaca d=2.3–3.9) → hover-büyütme (`.scp2:hover` scale 1.5 + z-index 40 öne) + etiket kademe (FORCE_ABOVE: tat/cjs/tyv yukarı). **Tıkla→inline kart KORUNDU** (Çuvaşça tıklayınca kart doğrulandı).
- **A5 · Uzaklık radar kutusu "çok uzun" ✅:** Sebep grid stretch (radar kutusu sol seçici sütunu kadar uzayıp boş alan). Dış+iç grid `align-items:start` (kutu içerik-boyu=kompakt), sol sütun 230→248px (taban-dil çipleri ferah), iç gap ferah, **OKUMA kutusu sağ sütuna** taşındı (sağdaki boşluk doldu, denge). Div dengesi korundu.
- **A6 · Kaynaklar kategorize ✅:** Flat liste → **4 kategori grubu** (`kind` alanından, sıralı): Araçlar & motorlar (1) / Veri setleri (9) / Akademik literatür (5) / Derin araştırma & derlemeler (1). `sourceGroups` (boş kategori atlanır) + renkli başlık + sayaç; kart-içi tür rozeti kaldırıldı (başlık taşıyor). Intro güncel (F temizliğiyle "örnek/illüstratif" zaten yoktu → metin de güncellendi). **Ölçekte yeni kaynaklar ilgili kategoriye düşer.**
- **Paper notu:** Bölüm A = "yatay ölçeğin ön-şartı UI altyapısı"; özellikle A1 (kategorili kelime-seçici) ve A4a (projeksiyon-hizalı harita) ölçek için kritik. A3'teki katmanlı kapsam (10<23<32) dürüst bir kapsam-iletişimi (overstatement yok).

## EK-OTURUM (26 Haz, devam-10) — BÖLÜM B başladı: YATAY ÖLÇEK (master envanteri + HARİTA tüm dillere)
Kullanıcı onayı: "B'ye geçelim; harita önce; 47'sinin tümü era etiketli; harita GERÇEK çizim olsun (denizler/karalar/dağlar); etiket çakışmasına çözüm."
- **B1 · Master dil envanteri ✅ (`languages.master.json`, `platform/etl/build_master.py`):** deepsearch 11 PDF tablosu **pdfplumber** ile çıkarıldı (`_envanter11.json`; pdfminer tabloyu dikey karıştırdı → pdfplumber 10-sütun temiz). **47 dil/lehçe/tarihsel form** (39 canlı + 7 tarihsel + 1 proto), 7 kol. **Glottolog CLDF çapraz-kontrol** (`languages.csv` iso/glottocode→kanonik ad/lat-lon). **KARARLAR:** koordinat/ad → canlı dillerde **Glottolog otorite** (nokta-konum); **tarihsel/proto dillerde ds11** (Glottolog GÜVENİLMEZ: xzm Harezm→Letonya [yanlış glottocode "Khwarezmian" İrani dili], otk Orhun→İran; ds11 tarihsel-bölge doğru). `GLOT_FIX` ds11 glottocode hataları (qxq/oui/qwm/aib). Temiz TR adları + 14 MVP sourced not taşındı + temiz konuşur-etiketi (`~N milyon/bin`, tarihselde boş). Çapraz-kontrol raporu loglandı.
- **HARİTA tüm 47 dile açıldı ✅ (B2 arka plan + B3 dotlar + B4 declutter):**
  - **B2 — GERÇEK çizim harita (`build_map_bg()` v2):** dotlarla AYNI `_pj()` projeksiyonunda (viewBox 0..100) tanınabilir Avrasya: su tabanı + **kara poligonu gerçek kıyılarla** (Akdeniz + Arabistan + Hindistan çıkıntıları + doğu Pasifik kıyısı) + iç denizler (Karadeniz/Hazar [Azerice batı↔Türkmence doğu kıyı — projeksiyondan ÇIKIYOR]/Aral/Balkaş/Baykal) + **Basra Körfezi** + **önemli dağ sıraları** (Kafkasya/Ural/Tien Şan/Altay/Pamir/Kunlun gerçek konumda ^^^ glifleri) + ızgara + subtle deniz etiketleri.
  - **B3 — `build_map(master)`:** MAP_ISOS/MAP_CARD/prof yerine master; 14→47 dot. Dot boyutu konuşura göre (sz), era stili (tarihsel = içi boş halka + italik etiket).
  - **B4 — ETİKET ÇAKIŞMA ÇÖZÜMÜ (açgözlü yerleştirme):** önem-sırası (chv çekirdek en öncelikli → canlı>tarihsel → konuşur); her dile etiket-kutusu hesaplanır, **çakışmıyorsa** yerleştirilir (alt/üst), **çakışıyorsa etiket gizlenir** ama dot tıklanabilir + hover-büyür. Massif çakışma çözüldü. *(Deneme-yanılma: tüm dotları engel yapınca AŞIRI declutter [hiç etiket]; geri alındı → label-label çakışması + chv önceliği.)* İnline kart: vitalite + era rozeti.
  - **ATLAS sayfası (kullanıcı: "harita sığmıyor → önizleme + tıkla→büyük sayfa"):** Karşılaştır'daki harita = **küçük önizleme** (dots-only, dil etiketleri gizli = temiz) + **"⛶ Büyük atlas →"** butonu + KEŞFET nav "Harita". Tıklayınca **ayrı büyük Atlas sayfası** (`isAtlas`, max-w 1340, aspect 1.62). `mapNodes` **ekran-duyarlı** (TEK node seti). **Zengin coğrafya** (`build_map_bg` v3 + `atlas_feature_labels()`): nehirler (İdil/Volga, Amu/Sir Derya) + denizler (Karadeniz/Hazar/Aral/Balkaş/Baykal/Issık/Akdeniz adlı) + dağlar (Kafkaslar/Tien Şan/Altay/Ural/Pamir ▲) + İstanbul Boğazı + bölgeler (Anadolu/İdil-Ural/Turan/Sibirya). İnline kart vitalite+era.
  - **ATLAS ZOOM/PAN (kullanıcı: "uç diller [Yakutça/Dolganca] çekirdeği sıkıştırıyor, kalabalık göremiyoruz"):** kök sorun = düzgün-doğrusal projeksiyonda uç diller kutuyu esnetip yoğun çekirdeği sıkıştırıyor. **Çözüm (kullanıcı seçimi): yakınlaştırma + bölge düğmeleri.** `build_map` **ZOOM-KADEMELİ etiket eşiği** (`lz`): her zoom seviyesinde açgözlü yerleşim (kutu/offset ~1/z), lz=etiketin göründüğü en küçük zoom. **z=1 SEYREK overview** (~19 büyük dil), yakınlaştıkça çakışmadan açılır. **Counter-scale**: zoom-wrapper'a karşı nokta+etiket EKRAN-SABİT (büyümez, AYRILIR) → yoğun küme yayılır, okunur. 6 ODAK düğmesi (zoom+pan preset) + zoom +/− (1-4×) + % gösterge. Coğrafya TAM korunur, dot→kart her zoom'da. *(Bu, "isimler çakışmasın + kalabalık bölgeyi rahat gör" isteğini çözer.)*
- **Paper notu:** master envanteri = yatay ölçeğin tek-otoriteli temeli; çapraz-kontrol (canlı→Glottolog / tarihsel→ds11) kararı kaynak-güvenilirliği farkındalığını gösterir (uydurma yok). Açgözlü etiket-yerleştirme = ölçeklenebilir kartografik declutter; önizleme/atlas ayrımı = bilgi-yoğun veriyi iki kademede sunma deseni.

## EK-OTURUM (26 Haz, devam-11) — Dil Profilleri BASE 14 → 47
Önerilen sıra-1. **`build_map` mantığıyla aynı master-tabanlı yaklaşım:** 14'ün zengin pipeline'ına (AES/Wikipedia/DEEPPROF/TTS) DOKUNMADAN, master envanterinden **33 yeni dil LANGPROFILE'a eklendi** (ISO-kodlu; Çulımca `clw`→`culw` çakışma çözümü). Her yeni dil: ad/kol/konuşur (master) · **egids+vit vitaliteden TÜRETİLDİ** (EGIDS-orta-token → 0-6 vit + TR etiket; tarihsel→vit0 "tarihî·ölü dil") · **region KÜRATE** (factual homeland, 33 dil) · script de-space · **joshi muhafazakâr** (uzn=3 [Joshi 2020], diğer canlı="0–1 çok düşük", tarihsel="—" — uydurma sayı YOK, düşük-kaynak gerçeğini yansıtır) · note factual (kol+region; **derin bölümler ds12-16'dan sonra**). Yeni 33 dil DEEPPROF'suz → ÖZET-only (dürüst). Claude_Preview: 47 dil selektörde, Nogayca (Kıpçak·~87bin·EGIDS 4·Kiril·0–1) + Çağatayca (tarihî·ölü) doğru. **Paper notu:** vit/egids vitalite-stringinden türetme = sourced (Glottolog AES/EGIDS), kürate region = factual coğrafya; joshi'de sayı uydurmak yerine "0–1" aralığı + "—" dürüstlüğü.
> **Kalan (Dil Profilleri):** derin bölümler 14→47 (ds9 ~30 dil + ds12-16 kol-derin → DEEPPROF/tts). Selektör 47'de uzun → A1-tarzı kategori/arama ileride.

## EK-OTURUM (26 Haz, devam-12) — Dil Profilleri DERİN bölümler 14 → 29 (ds9'dan faithful)
"devam" → kol-kol batch. ds9 `_profil_{karluk,kipcak,oguz,sibirya}.txt` (zengin, atıflı akademik raporlar) okunup her yeni dil için **4 derin bölüm** (Tarih / Yapı & özgünlük / İlişkiler / Dijital güç) — mevcut 14'ün stiliyle (~150-280 char, yoğun, atıflı). **Faithful sentez, uydurma YOK** (kaynakta olmayan eklenmedi; dedicated kaynağı olmayan diller özet-only bırakıldı).
- **Karluk +2:** Özbekçe (uzn — **14'te YOKTU, 30-40M, en büyük eksiklik**: Çağatay varisi, ünlü uyumu KAYBI [Fars], Joshi Sınıf 3 ✓, apertium-uzb/UD), G.Özbekçe (uzs — Oğuz substratı, Afganistan).
- **Kıpçak +5:** Karakalpak (Kazak ikizi+Özbek alıntı, Aral krizi), Karaçay-Balkar (Kafkas uvular substratı), Kumuk (eski Kafkasya lingua francası→Sınıf 0), Nogay (en saf arkaik Kıpçak, /ş/→/s/), Kırım Tatar (Oğuz-Kıpçak HİBRİDİ 3 diyalekt, crh-tur trunk).
- **Oğuz +4:** Gagavuz (Ortodoks Hristiyan istisna, Balkan Sprachbund SOV→SVO), Salar (Çin'de ada, Tibet evidensiyallik), Horasan (Türkmence↔Azerice geçiş, /ɑ/→[ɒ]), G.Azerbaycan (azb, Arap-Fars, Fars etkisi).
- **Sibirya +4:** Altayca-Güney/Kuzey (Sibirya↔Kıpçak köprüsü), Dolganca (Yakut+Evenki melez, s→h), Sarı Uygurca (Eski Uygur GERÇEK mirasçısı, preaspirasyon).
- **`profiles_deep` 14→29.** Her batch ayrı commit, Claude_Preview doğrulamalı (Özbekçe/Kırım Tatar/Gagavuz/Dolganca 4 bölüm render).
- **DEVAMI (aynı oturum) → 14→39:** +Eynu/İli (ds9 Karluk: kriptolekt karma dil / Kıpçak-melez moribund). **8 TARİHSEL dil** (ds16 _profil16 çıkarıldı + ds14 _profil14 çıkarıldı + ds13 _profil13): İdil Bulgar (Feyzhanov 1863 mezar taşı, Çuvaş atası), Hazar (Pax Khazarica, tartışmalı), Çağatay (Nevâî/Muhâkemet, Özbek/Uygur atası), Karahanlı (DLT+Kutadgu Bilig, İslami ilk edebi dil), Harezm (geçiş), Orhun/Eski Türkçe (8.yy Göktürk yazıtları, Genel Türkçe kök), Eski Uygur (Turfan dini metin; gerçek mirasçısı Sarı Uygur≠Modern Uygur), Codex Cumanicus (~1303). **Kalan 8 = küçük lehçe/kriptolekt** (Kaşkay/Balkan Gagavuz/Sibirya Tatar/Tofa/Urum/Karay/Kırımçak/Çulım) — dedicated kaynak yok → **dürüstçe özet-only** (uydurma YOK). Claude_Preview: Çağatayca/Dolganca doğru. **Paper notu:** tarihsel diller için kaynak-temelli (DLT, Orhun yazıtları, Codex Cumanicus, Feyzhanov mezar taşları) faithful sentez; kaynaksız küçük lehçeler bilinçli özet-only.

## EK-OTURUM (27 Haz, devam-13) — Uzaklık Gezgini 10 → 32 dil (Savelyev tam matris)
"devam" → Bölüm B sıradaki. **`build_distance` 10→32:** `DIST_ROWS` (32 dil = 31 master-eşleşik + Baraba Tatarcası; ui_code/Savelyev-adı/iso/TR-ad/kol) → `DIST_LEX`/`DIST_ISO` türetildi. **Koordinat artık master'dan** (`mcoord`, prof yerine) → yeni dillerin coğrafi ekseni de çalışır. **LANGVEC 10→32** master ad/kol + chv-satırı gerçek değer yedeğiyle üretilip enjekte (REAL_DIST pairwise'i ezer). Eksen kapsamı: leksikal/filogenetik **32** (Savelyev), tipolojik **23** (WALS), coğrafi 47 (master koord), anlaşılabilirlik (Lindsay) kısmi. Claude_Preview: 32 çip, Nogayca↔Tatarca leksikal 0.08 (Kıpçak yakınlığı doğru), A5 kompakt düzeni 32'yi temiz taşıyor. **Paper notu:** mevcut Savelyev verisinin tamamının açılması = "elimizde daha fazlası vardı, alt kümesini gösteriyorduk" durumunun düzeltilmesi.

## EK-OTURUM (27 Haz, devam-14) — Kognat Ağı 7→18 dil (ds18) + Ses denklikleri 4→7 kol-izoglosu (ds17)
"DEVAM.md §0'ı oku, planı özetle, onayımla devam" → Bölüm B sıradaki-1 (Kognat+Ses). **ds17/18 PDF'leri pdfplumber ile çıkarıldı** (`_kognat18.txt` 26 sf, `_ses17.txt` 19 sf; faithful transcript, atıflı). **KOGNAT 7→18 DİL:** yeni `platform/data/cognates_deep.json` + `platform/etl/build_cognates_deep.py` (11 kavram × 18 dil = 198 hücre; her hücre yerel yazı/Latin/IPA/morfem/**kognat-ID**/ses-kuralı; Vücut/Doğa/Sayılar/Eylem/Temel-Kültür). `build_cognates_deep` → 18-dilli radyal graf (cogid majority → **boşluk tespiti**: göz 4 Sibirya karak/xarax, ayak Çuvaş ura, gümüş Tuva möngün, ev Çuvaş pürt + Yakut jiä = 8 boşluk) + graf-altı "**Dil dil ses kuralı**" dökümü (kol-renkli nokta, boşluk turuncu satır, yerel yazı + ses kuralı). A1 seçici 5 kategori otomatik beslenir; geometri 18 düğüm için ölçeklendi (yarıçap 37→41). Halaçça/Argu rengi mevcut (harita bölümünden). **SES DENKLİKLERİ 4 Çuvaş-merkezli kural → 7 kol-izoglosu:** `build_sound_laws(ev)` = rotasizm/lambdasizm/söz-başı-*h-/söz-içi-*-d-/son-ses-*-G/söz-başı-*y-/baş-ses-tonlulaşması; her kart **proto-fonem + çok-kollu refleks** (kol-renkli nokta + değer + örnek) + **kanıt rozeti** (rot/lam/y = 36/29/14, `sound_evidence(cog)` ile **Savelyev verisinden**, hardcode değil). Kart UI cv↔ct ikiliden çoklu-refleks gride; giriş metni kol-seviyesi çerçeveye; eski 4-kart EVID enjeksiyonu kaldırıldı. Kognat→kural bağı korundu (`goCompareSound`, ruleIdx proto-fonem tabanlı). **Claude_Preview:** Göz 18 düğüm + 4 boşluk satırı, Ev 2 boşluk (pürt/jiä), Baş 0 boşluk; 7 ses kartı + refleksler; Taş (*tāĺ)→Lambdasizm bağı doğrulandı. 2 ayrı commit+push. **Karar:** ds18 hand-curated 18-dil veri, Savelyev raw `cognates.json`'ın yerine Kognat Ağı'nı besler (çok daha zengin: yerel yazı+IPA+ses kuralı); `cognates.json` yalnız `sound_evidence` kanıt sayısı için kalır.

## EK-OTURUM (27 Haz, devam-15) — TTS profil bölümü 14 → 39 dil (ds6 boşluk haritası)
"o 250-kelimelik kognat kaynağını cevapla, sonra devam" → Savelyev `cognates.json` (254 kavram·32 dil) repoda doğrulandı + Kognat Ağı'na 254 açma seçeneği plana not düşüldü; ardından SIRADAKİ-1 = TTS. **ds6 `_tts_asr.txt` (931 satır) okundu** (Meta MMS-TTS 1.107 dil/VITS/CC-BY-NC, Piper MIT, eSpeak GPLv3, ISSAI, Whisper/wav2vec2). **`profiles_tts.json` 14→39:** `platform/etl/expand_tts_47.py` (idempotent) ile +25 dil; anahtarlar `profiles_deep.json` ile birebir → her derin profil 5. bölüm "Seslendirme (TTS/ASR)" taşır. **UYDURMA YOK politikası:** ① gerçek açık model yalnız ds6'da ADI GEÇEN dillerde — **uzn** (MMS uzb-script_cyrillic, Latin→Kiril ön-işlem + piyazon/qutadgu_bilik fine-tune + ASR Gearnode/qwen3-asr-uzbek Apache 2.0), **azb** (MMS azb), **crh** (MMS crh + robinhad/wav2vec2-xls-r-300m-crh), **nog** (MMS + eSpeak çift kapsam); ② özel modeli olmayan yaşayan küçük diller (uzs/gag/kaa/krc/kum/alt/atv/slr/ili/aib/dlg/ybe/kmz) → dürüst "açık model yok" + ds6'nın 'Dürüst Boşluk Haritası'ndaki yakın-dil ikamesi (XTTS sıfır-atış) / eSpeak fonem enjeksiyonu yolu; ③ tarihsel/ölü diller (oui/chg/xbo/xqa/xzm/otk/qwm/zkz) → "canlı konuşur yok → TTS/ASR uygulanamaz (yazılı korpus)". **Tavan 39 (47 değil):** 8 özet-only küçük lehçenin derin profili yok → TTS bölümü de yok. **Claude_Preview:** Özbekçe 5 bölüm + gerçek model (MMS+qwen3) render; Çağatayca "uygulanamaz" render. Commit+push.

## EK-OTURUM (27 Haz, devam-16) — Bölüm B kalanı TEK PATCH: Ekosistem keşif + Profil A1 selektör
"Bölüm C'ye kadar olan kısmı tek patchte tamamla" → iki kalan Bölüm B işi tek geçişte. **① Ekosistem "Dil dil keşif" (9. kategori/sekme):** `build.py`'de master'dan yaşayan 39 dil için sentetik kategori üretildi — her dil doğrudan HF arama hub'ı (`huggingface.co/models?language=<kod>&sort=trending` + datasets); `HF_CODE` eşlemesi (tur→tr, azj→az, … 639-1; diğerleri ISO 639-3). Yeni/küçük diller dahil (nog/klj/aib/uzs/slr…). **DÜRÜST çerçeve:** açıklamada "arama linki; sonuç sayısı dilin dijital varlığını yansıtır, bazıları boş olabilir — bu da dürüst sinyaldir" (iddia YOK). Bağlantı 101→187. Mevcut sekme mimarisine (ECOCATMETA + eco_* bayrak) doğal eklendi (eco_discover). **② Dil Profilleri A1 selektör:** 47-dil listesine arama kutusu + kol kategori çipleri (Tümü·47 / Oğuz·10 / Kıpçak·15 / Karluk·8 / Sibirya·9 / Ogur·3 / Argu·1); `profileVals`'a filtre mantığı (kognat A1 deseni), liste ayrı kaydırma kabında, boş-durum, stale h2 "14 dil"→`{{ profileTotal }}` dinamik. **Claude_Preview:** profil 47→Sibirya 9 (Yakut/Tuva/Hakas/Şor/Dolgan/Tofa/Altay/Çulım/Sarı Uygur)→arama "nog" 1; keşif sekmesi 39 dil + HF linkleri (klj/nog dahil); konsol temiz. Tek commit+push. **Karar:** 8 küçük lehçenin DERİN profili dedicated kaynak olmadığından eklenMEDİ (uydurma yok) — base+TTS "yok" zaten var.

## EK-OTURUM (27 Haz, devam-17) — Kognat Ağı GENİŞ tarama: Savelyev 254 kavram (Derin/Geniş toggle, lazy-fetch)
"Kognat 254 olayını kapsamlı düşün, planı dürüstçe sun, onay bekle" → kullanıcı **B seçeneğini** (Derin/Geniş toggle) onayladı. **Veri gerçeği incelendi (dürüst):** `cognates.json` = 254 kavram · ort. 29.9 dil/kavram · 32 dil · 7 kol; üyede `value/form/segments/branch/cogid` VAR ama **yerel yazı/IPA/per-hücre ses kuralı YOK** (bunlar yalnız ds18 derin sette elle eklenmişti). → İki katman: **Derin (11, zengin)** + **Geniş (254, akademik yazım)**. **`build_cognates_broad.py`:** 254 İngilizce gloss → Türkçe (254/254 eşleşti) + 10 kategori (Vücut/Doğa/Hayvan&bitki/Nitelik/Eylem/Sayılar/Zaman/Kişi&akrabalık/Nesne&soyut/Dilbilgisi&uzay); 32 Savelyev→TR dil adı; cogid-majority **boşluk tespiti**; `readable()` (ø→ö, χ→h, segmentler dahil). → `cognates_broad.json` (937KB). **Mimari karar:** 937KB index.html'e GÖMÜLMEZ (538→1.5MB olurdu) → `dist/cognates_broad.json`'a kopyalanır, **"Geniş" moduna geçince `ensureBroad()` LAZY-FETCH** (runtime zaten fetch destekliyor; canlı analiz gibi). index.html 540KB'da kaldı. **build.py:** Derin/Geniş toggle butonları + mod-notu; `cognateVals` SRC-seçimli (`this.COGNATES` vs `this.COGNATES_BROAD`), anahtar fallback (mod değişince ilk kavrama), yükleniyor durumu; tablo başlığı dinamik ("Dil dil ses kuralı"↔"biçim & segment"); geometri 3. kademe (n>24→32 düğüme kadar yarıçap 44/küçük düğüm). A1 selektör+kategoriler aktif kaynaktan beslenir. **Claude_Preview:** Geniş→254 kavram, 11 kategori (Eylem·78/Nitelik·40/Vücut·36/Dilbilgisi·28/Doğa·25…toplam 254); göz→32 düğüm + 7 Sibirya boşluğu (karak/qaraq/χaraχ); köz/göz okunur; arama "su" çalışır; Derin'e dönüş 11 kavram+ds18 notu; konsol temiz. Commit+push. **Felsefe:** her kavram notunda "yerel yazı/IPA yalnız Derin sette" açıkça yazılı (dürüstlük).

> **★★ BÖLÜM B BİTTİ:** Bölüm A ✅ · master 47 ✅ · harita/atlas/zoom ✅ · profiller base 47 + derin 39 ✅ · Uzaklık 32 ✅ · Kognat 18-dil + Ses denklikleri 7-izogloss ✅ · TTS 14→39 ✅ · Ekosistem keşif + Profil A1 ✅ · **Kognat GENİŞ 254 (Derin/Geniş) ✅**. **Tek kalan:** 8 küçük lehçe derin (kaynaksız→bloke). **★ SIRADAKİ = BÖLÜM C** (altyapı: ① ses motoru Piper/MMS/eSpeak+FastAPI router · ② morfolojik üretim arayüzü · ③ HfApi-CRON) **→ D (eğitim portalı, en son).** Felsefe korundu, her adım commit+push.

## Sıradaki / açık işler — bkz `plan/GELECEK-PLANLAR.md` (sıralı: A UI-öncesi · B yatay ölçek · C altyapı · D eğitim portalı)
1. **YATAY ÖLÇEK (★ SIRADAKİ):** UI cilası (Bölüm A) **✅ bitti** (26 Haz). Deepsearch 11-18 çıktıları geldi (`arastirma/11..18*.pdf`) → locale çek (pdfminer→`_*.txt`), çapraz-kontrol, tüm modülleri tüm dillere aç (A1 taksonomi+COG_CONC genişlet, profiller 14→tüm, harita/uzaklık/ses-denklikleri/ekosistem ölçekle).
2. (Opsiyonel) Türkçe Zemberek (JPype) üst-kalite — NW zaten %98.8, acil değil.
3. Sıfat/zarf yüzey bölümleme (POS başına kümülatif şablon).
4. **.dix kalıcılığı:** VM'de `/root/koken_api/dix/` (gitignored, GPL). VM sıfırlanırsa `bash platform/backend/fetch_dix.sh` (VM'de) ile yeniden indir.
