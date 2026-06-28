# DEVAM — Oturum Devir Notu (KÖKEN · Türk Dilleri Morfoloji Platformu)

> **Compact sonrası / yeni oturumda İLK BUNU OKU.** Bu §0 = güncel tek-bakış. Sonra: §2 (VM erişimi), §3 (apertium), §4.5 (FELSEFE), §4.6 (HATALAR+ÇÖZÜMLER), §7 (konvansiyonlar).
> **Güncelleme: 28 Haziran 2026.** Repo: github.com/muhammedkumcu/cuvas-platform (main, push'lu, temiz).

---

## 0) ŞU AN NEREDE KALDIK — TEK BAKIŞ

### ★★★ EN GÜNCEL (28 Haz) — KULLANICI İNCELEME NOTLARI + R-FAZLARI (compact-sonrası ÖNCE BUNU OKU)
**Bölüm B (yatay ölçek) içerik+UI bitti; kullanıcı AYRINTILI sayfa-sayfa inceleme yaptı → R1-R8 fazları.** Tümü Claude_Preview'da doğrulandı, ayrı commit'lerle push'lu, tree temiz. Felsefe §4.5 DEĞİŞMEZ. **Sıralı detay: `plan/GELECEK-PLANLAR.md` "★ İNCELEME NOTLARI" bölümü.**

**✅ YAPILDI (R1-R5b-1, 27-28 Haz):**
- **R1-R4 (UI cila):** net metin/başlık düzeltmeleri (footer, "Türk dilleri haritası", Dilin Kalbi sidebar, Kıpçak cümlesi, 1.binyıl, Ekosistem ★/↓ metrikleri kaldırıldı) · **ana sayfa HERO + akıllı arama** (dil→profil, kavram→kognat, kelime→analiz) · **konuşur-yılları kaldırıldı** (R5b-2'de kaynaklı geri gelecek) · profil listesi canlılık-rengine sıralı + temiz başlık.
- **Harita:** tek-boyut standardı (konuşur-kademe kalktı) · **ölü diller tek koyu gri çerçevesiz nokta** · bold/italik kakofonisi kalktı (yalnız ölü diller italik) · **mouse sürükle-pan** · "Büyük atlas" butonu kaldırıldı → **Karşılaştır harita SEKMESİ tamamen kaldırıldı** (3 tab) + atlas "←Karşılaştır"→Dizilim (eski önizleme öldürüldü) · Boğaz/Ege/Kızıldeniz su + Kıbrıs adası eklendi.
- **Kognat:** alfabetik sıra · **büyük graf (600px) + büyük merkez (104px) + ≤26 düğüm TEK halka** (deep 18 = 0 çakışma; broad 32 = 2 halka, çakışma 39→10) · proto responsive · tablo sütun başlıkları (DİL/BİÇİM/...) + turuncu-satır açıklaması · "**Bu sayfa ne anlatıyor?**" en altta + **okuma kılavuzu üstteki "nasıl çalışır?"da** (SES NOTU panelinden taşındı).
- **Karşılaştır:** gereksiz kaynak kaldırıldı · soy ağacı "nasıl okunur" açıklaması (FAMILY 14-düğüm Bayes). **Uzaklık:** taban/karşılaştırılan dil **yan yana, aynı format, ~10 görünür kaydırmalı**.
- **R5a ✅:** 2 deepsearch promptu (`arastirma/19,20*.prompt.md`). **SONUÇLAR GELDİ → `arastirma/19-Türk Dilleri Derin Profil Araştırması.pdf` + `20-Türk Dilleri Tarihi Araştırması.pdf` → çıkarıldı: `_prof19.txt` (28 sf) + `_tarih20.txt` (14 sf).**
- **R5b-1 ✅:** **ds19 → 17 derin profil** (`profiles_deep.json` 39→46; `platform/etl/build_profiles_ds19.py`): 7 YENİ yaşayan az-belgeli lehçe (bgx/qxq/uum/kdr/jct/sty/kim — derin profili YOKtu) + clw/ili + 8 tarihsel yenilendi. Faithful + **gerçek kaynaklı** (Erdal/Tekin/Dolatkhah/Csató/Schluessel/Ercilasun/Röhrborn/Grönbech/Harrison + Glottolog/Ethnologue/UNESCO). → "ölü diller bilgi yok" çözüldü.
- **R-AÇIKLAMA başladı:** Kognat'a "Bu sayfa ne anlatıyor?" bölümü = HER SAYFAYA gelecek açıklama deseninin ilk örneği.

**⏳ SIRADAKİ (R-fazları, sıralı) — POST-COMPACT BURADAN DEVAM:**
1. **R5b-2 · 47-dil KAYNAKLI konuşur/yıl/EGIDS** → `_prof19.txt` SAYFA 17-21'deki **47-dil tablosu** (Dil·ISO·Kol·Konuşur[yıl,kaynak]·EGIDS/UNESCO). Master'a uniform işle: konuşur sayısı + yıl + kaynak (kullanıcının "yıl+kaynak" isteği; biz yılları kaldırmıştık → şimdi kaynaklı geri ekle). build.py'de lang_extra "speakers" override'ını kaldır → master tek kaynak; profil KONUŞUR kutusuna küçük "yıl·kaynak" altyazısı. *(iso eşleme: master azj=Azerice/aze, uzn=Özbekçe/uzb; tablo "aze"/"uzb" kullanıyor.)*
2. **R5b-3 · ds20 (TARİH)** → `_tarih20.txt`: zengin zaman çizelgesi + 6 kol DETAYLI ses-yasası + Bayes filogeni açıklaması → Tarih & Köken sayfasını zenginleştir (kullanıcı: "çok özet, renkler karmaşık, daha detaylı"). FAMILY ağacı + timeline (dc.html) zaten var, ds20'den genişlet.
3. **R-AÇIKLAMA · kalan sayfalar** → Harita, Profiller, Tarih, Karşılaştır, Uzaklık, Ekosistem, Analiz, Paradigma, Dilin Kalbi'ne "bu nedir/neyi gösterir/neden önemli" kaynaklı bölüm (Kognat'taki desen).
4. **R6 · KAYNAKLAR overhaul** → ⚠ kullanıcı net dedi: **"deepsearch" kaynak DEĞİL; o PDF'lerin içindeki GERÇEK kaynakları yaz** (her ds PDF'inin 'Alıntılanan çalışmalar' bölümü). Uygulama içi `SOURCES` + Kaynaklar sayfasını katmanlı genişlet (en önemliler üstte, kalan altta — GitHub/paper/HF/URL).
5. **R7 · ANALİZ MD'leri** → `inceleme-yontemi.md` (kullanıcının inceleme tarzını analiz et + geliştir) + sayfa-sayfa analiz MD (Morfoloji & Paradigma DAHİL — kullanıcının bakmadıkları; ben kendim bakıp analiz/plan yapacağım).
6. **R8 · MD + resume** (bu adım kısmen yapıldı; her büyük adımda tekrar güncelle).
- **Bekleyen kararlar:** isim/domain (ertelendi; müsait .com: kokence/getkoken/kokenatlas/sazlir/lirturk). Kognat 254→tüm Savelyev (opsiyonel, Geniş modda zaten 254 var). Bölüm C (altyapı: ses motoru/üretim/HfApi-CRON) ve D (eğitim portalı) İNCELEME bitince.

---

### ★★ GÜNCEL DURUM (27 Haz) — (alttaki kronoloji; güncel için yukarıdaki ★★★'a bak)
**DİKEY MVP ✅ + BÖLÜM A (UI cilası) ✅ + BÖLÜM B (yatay ölçek) DEVAM EDİYOR.** Hepsi Claude_Preview'da doğrulandı, ayrı commit'lerle push'lu, tree temiz. **Felsefe: §4.5 (UYDURMA YOK) — DEĞİŞMEZ.** Sıralı plan detayı: `plan/GELECEK-PLANLAR.md`.

**DİKEY MVP ✅ (deepsearch-bağımsız, arka plan):** Faz 1 (füzyon ek-ayrışması chv %75.3→%93.2 · ses denklikleri kanıtlı · harita inline-kart · Hakkında) · Faz 2 (Seslendirme · **Ekosistem sayfası** · kollar+Bayes ağacı · derin profiller · KAYNAKLAR) · Faz 3.1 (Çuvaşça "Dilin Kalbi"). Deepsearch 5-10 işlendi.

**BÖLÜM A — yatay ölçek öncesi UI cilası ✅ (A1-A6, 26 Haz):** A1 kognat kelime-seçici kategorili+aranabilir · A2 Karşılaştır başlığı sekmeye-duyarlı · A3 landing kapsam şeridi VERİDEN + footer düzeltildi · A4 harita projeksiyon-hizalı arka plan + hover + etiket kademe · A5 Uzaklık radar kompakt + OKUMA sağa · A6 Kaynaklar 4 kategori. *(Detay: GELECEK-PLANLAR Bölüm A.)*

**BÖLÜM B — YATAY ÖLÇEK (★ ŞU AN BURADAYIZ).** Deepsearch 11-18 çıktıları `arastirma/11..18*.pdf` (kullanıcı çalıştırdı). **YAPILANLAR (✅):**
- **B0 · master envanteri** `platform/data/languages.master.json` (47 dil/lehçe/tarihsel; ds11 + Glottolog çapraz-kontrol; `platform/etl/build_master.py`). **★ Master = harita+profil+uzaklık'ın TEK kaynağı.**
- **Harita + ATLAS + ZOOM ✅** tüm 47 dile açıldı: gerçek çizim harita (`build_map_bg()` v3 — kıyı/deniz/dağ/nehir/Boğaz; `atlas_feature_labels()`). Karşılaştır'da küçük önizleme (dots-only) + "Büyük atlas" → ayrı **Atlas sayfası** (`isAtlas`). **Zoom/pan** (uç-dil sıkışma çözümü): zoom-kademeli etiket eşiği `lz` + counter-scale + 6 ODAK düğmesi + zoom +/−. `mapNodes` ekran-duyarlı.
- **Dil Profilleri ✅** BASE 14→47 (master'dan sourced özet) + **DERİN 14→39** (ds9/14/16'dan faithful+atıflı; tüm büyük canlı + **8 tarihsel** [Orhun/Çağatay/Karahanlı/Eski Uygur/İdil Bulgar/Hazar/Harezm/Codex Cumanicus]). Kalan 8 küçük lehçe/kriptolekt (Kaşkay/Balkan Gagavuz/Sibirya Tatar/Tofa/Urum/Karay/Kırımçak/Çulım) **dedicated kaynaksız → özet-only (dürüst)**.
- **Uzaklık Gezgini ✅** 10→32 dil (Savelyev tam leksikal/filogenetik matris; `DIST_ROWS`; koordinat master'dan; LANGVEC 32).
- **Kognat Ağı + Ses denklikleri ✅** (ds17/18, 27 Haz). **Kognat 7→18 dil:** yeni `platform/data/cognates_deep.json` (11 kavram × 18 dil; her hücre yerel yazı/Latin/IPA/morfem/**kognat-ID**/ses-kuralı; `platform/etl/build_cognates_deep.py`). `build_cognates_deep` → 18-dilli radyal graf (cogid-tabanlı **boşluk tespiti**) + graf-altı "**Dil dil ses kuralı**" dökümü (kol-renkli, boşluk turuncu); A1 seçici 5 kategori otomatik. **Ses denklikleri 4 Çuvaş-merkezli kural → 7 kol-izoglosu** (`build_sound_laws`: rotasizm/lambdasizm/*h-/*-d-/*-G/*y-/ötümlüleşme; çok-kollu refleks + kanıt rozeti 36/29/14 **Savelyev verisinden**). Kognat→kural bağı korundu. *(Detay: GELISTIRME-GUNLUGU devam-14.)* **NOT:** Savelyev `cognates.json` (254 kavram·32 dil) hâlâ repoda — Kognat Ağı'nı bu 254'e açma seçeneği `GELECEK-PLANLAR`'da; ds18'in 11'i "derin", Savelyev 254'ü "geniş tarama" katmanı.
- **TTS profil bölümü 14→39 ✅** (ds6, 27 Haz). `profiles_tts.json` +25 dil (`platform/etl/expand_tts_47.py`); tüm 39 derin profil "Seslendirme (TTS/ASR)" 5. bölümü taşır. **Uydurma yok:** gerçek açık model yalnız ds6'da adı geçenlerde (uzn/azb/crh/nog = MMS-TTS/eSpeak/wav2vec2); özel modeli olmayan yaşayan küçük diller → "açık model yok + yakın-dil ikamesi/eSpeak"; tarihsel/ölü diller → "seslendirme uygulanamaz". *(8 özet-only küçük lehçenin derin profili yok → TTS bölümü de yok; o yüzden tavan 39, 47 değil.)*
- **Ekosistem "Dil dil keşif" + Dil Profilleri A1 selektör ✅** (27 Haz, tek patch). Ekosistem'e 9. sekme **"Dil dil keşif"** — her yaşayan master dili (39) için doğrudan HF arama hub'ı (model+veri; `HF_CODE` eşlemesi; yeni-küçük diller dahil; dürüst "arama" çerçevesi, iddia değil). Dil Profilleri 47-dil selektörüne **arama kutusu + kol kategori çipleri** (Tümü/6 kol sayaçlı; liste ayrı kaydırılır; h2 stale "14 dil"→dinamik).
- **Kognat Ağı GENİŞ tarama — Savelyev 254 kavram ✅** (27 Haz). **Derin (ds18, 11) / Geniş (Savelyev, 254) toggle.** `platform/data/cognates_broad.json` + `platform/etl/build_cognates_broad.py`: 254 İngilizce gloss→TR (254/254) + 10 kategori; cogid-majority **boşluk tespiti**; akademik karşılaştırmalı yazım (yerel yazı/IPA YOK — dürüstçe notlandı). **937KB veri index.html'e GÖMÜLMEZ → `dist/cognates_broad.json`'a kopyalandı, "Geniş" moduna geçince `ensureBroad()` ile LAZY-FETCH** (index.html 540KB'da kaldı). cognateVals SRC-seçimli; tablo başlığı + geometri (n>24→32 düğüm) dinamik. *(Detay: GELISTIRME-GUNLUGU devam-17.)*

**⏳ SIRADAKİ:**
- **★★ BÖLÜM B BİTTİ.** Tek bloke iş: **8 küçük lehçe DERİN profili** (Kaşkay/Balkan Gagavuz/Sibirya Tatar/Tofa/Urum/Karay/Kırımçak/Çulım) — **dedicated deepsearch kaynağı YOK → bloke** (uydurma yok; kaynak gelirse eklenir). Base profil + harita + TTS "yok" zaten var.
- **★ SIRADAKİ = BÖLÜM C (altyapı / gerçek mühendislik):**
  1. **Gerçek ses motoru (C1):** "▷ Seslendir" şu an tarayıcı Web Speech'e düşüyor → ds6'nın **Dinamik Hibrit Router**'ı: tr/kaz Piper (ONNX, sunucu) · uzb/uig/sah MMS-TTS (HF API + Latin→Kiril/num2words ön-işlem) · chv/bak eSpeak NG (tarayıcı WASM). FastAPI Smart Router. *(VM gerekir.)*
  2. **Morfolojik ÜRETİM arayüzü (C2):** backend `/generate` var ama UI panel yok → kök + öznitelik seç → yüzey biçim üret (analizin tersi).
  3. **Ekosistem HfApi-CRON (C3):** metrik (indirme/yıldız) otomatik tazeleme.
- **Bölüm D — EN SON:** çocuk/öğrenci eğitim portalı + Saha/Şor "Dilin Kalbi" şablonu.
- Sonra **Bölüm C (altyapı):** gerçek ses motoru (Piper/MMS/eSpeak+FastAPI) · morfolojik üretim arayüzü · ekosistem HfApi-CRON.
- **Bölüm D — EN SON:** çocuk eğitim portalı + Saha/Şor "Dilin Kalbi" şablonu.

**⚠ TEKNİK:** pdfplumber/pdfminer tablo+metin çıkarımı = `arastirma` venv (`/c/Users/Tombulteke/Desktop/turkmence-guncelleme/.venv/Lib/site-packages` PYTHONPATH + `C:\Users\Tombulteke\AppData\Local\Programs\Python\Python311\python.exe`). Çıkarılan `_*.txt`/`_*.json` commit'li, PDF'ler gitignore. **Konsol cp1254 → print'te `→`/Kiril ÇÖKER**, `->` kullan ya da dosyaya yaz + Read. **Profil derin ekleme deseni:** ds9/14/16 `_profil_*.txt` oku → `profiles_deep.json["deep"][code]` = 4 bölüm (Tarih/Yapı & özgünlük/İlişkiler/Dijital güç, ~150-280 char, faithful+atıflı) → `python platform/ui/build.py` → Claude_Preview doğrula → commit.

**KRİTİK HATIRLATMALAR (her zaman):** ① **UYDURMA YOK** — kaynak + test + doğruluk her şeyin önünde (§4.5 FELSEFE; kanıtla-iddia-etme, test sonucu paylaş). ② **Commit + push SIK** (kolay unutuluyor; her adımda). ③ **HARDCODED kısımlar önemli ve unutulur** (ör. Karşılaştır başlığı, ana sayfa dil sayısı) — değişikliklerde tara. ④ **`.dc.html` ELLE DÜZENLENMEZ → build.py.** ⑤ Backend için VM açık + uvicorn (§4.6 tuzağı). ⑥ Commit'lerde yalnız Muhammed Kumcu (Co-Authored-By YOK).

---

### NE YAPIYORUZ — amaç
**KÖKEN** — "Türk dilleri atlası & laboratuvarı." ~20 Türk dili için Apertium FST'leriyle çalışan, **çift kitleli** açık kaynak **morfoloji + karşılaştırma + araştırma platformu**:
analiz · üretim · paradigma · kognat ağı · ses denkliği · çok-boyutlu uzaklık · dil profilleri · harita · tarih · ICALL.
- **İki kitle:** (1) **öğrenenler** (çocuk/öğrenci) + (2) **araştırmacılar (KRİTİK)** — "literatür karşısındaymış gibi", Türk dil dünyasının takip edildiği, araştırmacının **ilk uğrağı**, işini kolaylaştıran (birleşik sorgu, toplu analiz, dışa aktarım, açık API) merkez.
- Düşük-kaynaklı/**tehlikedeki** üyelere (Çuvaş, Saha, Tuva, Hakas, Şor, Halaç) özel önem (dijital kapsayıcılık misyonu).
- **Felsefe/ilkeler: §4.5 — MUTLAKA OKU.** Akademik hedef: çift-kitleli çok-dilli çok-boyutlu böyle bir platform YOK (apertium=CLI/MT, turkicnlp=dev-kütüphane). Venue: UBMK/TurkLang ya da daha güçlüsü (tarihe sıkışma).

### MİMARİ — 3 katman
1. **Backend (VM/Linux)** — `platform/backend/app.py` (FastAPI), apertium FST sarıcı. Uçlar: `/health /languages /analyze {lang,word} /analyze_all {word} /generate {lang,query} /segment {lang,word} /paradigm/{lang}/{lemma}`. **`/segment`** = canlı kelimeyi GERÇEK yüzey eklerine böler (kümülatif üretim+fark; tutmazsa kök+kalan'a düşer). **`/paradigm`** artık isim (hâl×sayı) + **fiil** (zaman×kişi, üretilen hücreler dinamik) döner (`noun`/`verb`/`has_noun`/`has_verb`). 10 MVP dil FST'si. Host'tan `http://127.0.0.1:8000` (VBox port-forward `koken`:8000 + guest firewalld 8000). **Başlat: VM'de `bash /root/koken_api/start.sh` (pkill+setsid+detach); ⚠ uvicorn tuzağı: §4.6 + `platform/backend/README.md`.**
2. **Veri (gerçek, locale çekilmiş, kaynaklı)** — `platform/data/*.json` (her dosya `_meta`+lisans):
   `cognates.json` · `languages.geo.json` · `distance.lexical.json` · `distance.typological.json` · `features.wals.json` · `profiles.json` (+AES canlılık) · `intelligibility.json` (Lindsay) · `lang_extra.json` (Wikipedia, 14 dil).
   Çıkarım betikleri: `platform/etl/` (savelyev/glottolog/wals). Ham kaynaklar: `sources/` (gitignored: savelyevturkic, glottolog-cldf, wals, northeuralex, unimorph×9, UD×4). **Provenance defteri: `platform/KAYNAKLAR.md`.**
3. **UI (KÖKEN)** — `platform/ui/`. ⚠⚠ **KURAL: kullanıcının tasarım export'u `Morfoloji Platformu.dc.html` (DesignCanvas; `support.js`=runtime) ELLE DÜZENLENMEZ.** Tüm değişiklikler **`platform/ui/build.py`** ile enjekte edilir → **`dist/index.html`** (çalıştırılabilir). Kullanıcı tasarımı tekrar export edince → `python platform/ui/build.py` tekrar çalıştır. Veri sözleşmesi + modül haritası: `platform/ui/README.md`.

### MODÜL DURUMU (hepsi build.py ile enjekte, Claude_Preview'da doğrulandı)
- ✅ **Dil Profilleri + Canlılık** — Glottolog AES + 14/14 dil Wikipedia zengin metin (çapraz-kontrollü, atıflı). Harita düğümü → profil.
- ✅ **Harita** — 14 dil Glottolog koordinat (şematik projeksiyon).
- ✅ **Uzaklık Gezgini** — **5/5 eksen kaynaklı**: leksikal+filogenetik (Savelyev), tipolojik (WALS), coğrafi (koordinat), anlaşılabilirlik (Lindsay).
- ✅ **Kognat Ağı** — 14 kavram, gerçek kognat setleri+boşluklar (Savelyev); formlar artık **okunur karşılaştırmalı yazım** (C ✅, `readable()`); proto-kök akademik.
- ✅ **Analiz CANLI + MULTI-DİL OTOMATİK** — seçicide "⚡ Otomatik" → `/analyze_all` (kelime hangi dil(ler)de varsa) + "BU KELİME ŞU DİLLERDE" çipleri; ya da tek dilde `/analyze`. Dil değişince anında yeniden çözer.
- ✅ **Paradigma CANLI** — serbest kök girişi → `/paradigm/<dil>/<kök>`; örnek kökler **dil dengeli** (G3); tabloya "⧉ Tabloyu kopyala".
- ✅ **Araştırmacı Merkezi CANLI** (B) — serbest sözcük + dil → `/analyze` → gerçek JSON/CoNLL-U/CSV + İndir.
- ✅ **Karşılaştır "dizilim" CANLI** (D) — aranan kelime `/analyze_all` ile diller-arası.
- ✅ **öğrenen/uzman + export barları KALDIRILDI**; sol-alt XP sayacı kaldırıldı (G7). **Кир/Lat** toggle çalışıyor. Paradigma/Karşılaştır başlıkları **dinamik**.

### ★ 2. TUR GÜNCELLEMELERİ (kullanıcı testi sonrası — TAMAMLANDI, Claude_Preview doğrulandı)
- **DİL MODELİ değişti:** üst bardaki dil seçici KALDIRILDI; **her ekranda (Analiz/Paradigma/Araştırmacı/Karşılaştır) kendi giriş kutusu + yanında kompakt dil seçici** ("Otomatik (dil algıla)" varsayılan, emoji yok). `searchLang` default `'auto'`. Dil değişince ekran-duyarlı yeniden çözümleme. Üst-bar global arama kutusu KALDI (auto). (Çok-dillilik artık görünmez/otomatik; manuel seçim de var.)
- **Analiz GERÇEK yüzey ekleri:** canlı sonuç artık `/segment` ile **ev·ler·de** gösterir (apertium etiketi pl/loc DEĞİL). `applySegment` metodu; dil çipiyle yeniden bölünür.
- **Paradigma FİİL:** "at" gibi köklerde **İsim/Fiil sekmeleri**; fiil tablosu zaman×kişi (attım/attın… , atsam…). Örnekler `runParadigm` (auto destekli).
- **Karşılaştır CANLI giriş:** "okuduk" sabitliği kaldırıldı; yazılan kelime `/analyze_all` ile diller arası (`runCompare`).
- **Araştırmacı:** "Otomatik" bug'ı düzeldi (auto→/analyze_all); **"AÇIK API · planlanan"** dürüst etiket (gerçek uç = VM `/analyze`); **"✷ nasıl çalışır?"** aç-kapa ipuçları (Araştırmacı/Kognat/Karşılaştır).
- **Kognat = küratörlü** (Savelyev statik, 14/254 kavram) — canlı değil; yatay-ölçek notu `plan/GELECEK-PLANLAR.md`'de.
- DETAY/commit'ler: git log (Backend /segment+fiil → UI dil modeli → segment → fiil paradigma → help/API).

### ★ 3. TUR — MORFOLOJİ KALİTESİ + DEEPSEARCH (TAMAMLANDI, test edildi)
- **Yüzey bölümleme yeniden yazıldı = Needleman-Wunsch hizalama** (deepsearch önerisi): kümülatif üretim + fonolojik-cezalı hizalama → gerçek yüzey ekleri + **ses olayları** (p→b ünsüz yumuşaması) OTOMATİK; el-allomorf tablosu yok. **Kök kutusu = SÖZLÜK biçimi** (kitap), ses olayı ayrı **SES OLAYI rozetinde**.
- **Analiz-seçimi düzeltmesi (kritik):** `/segment` tüm analizleri deneyip **align eden İSİM**'i seçer (analyses[0] çoğu yanlış fiil veriyordu). → 10-dil round-trip testi (`platform/backend/segment_eval.py`, 1700+ form): **tüm dillerde %100 align, ~%98 ek-sayı**; chv %92.6 (en zayıf, Çuvaş iyelik). uig Arap yazısı bekler.
- **Deepsearch PDF'leri** `arastirma/Türk Dilleri NLP *.pdf` (+ `_nlp_araclari.txt`/`_nlp_envanteri.txt` çıkarımları). **Tam değerlendirme + kararlar + sıradaki işler: `platform/MORFOLOJI-DEGERLENDIRME.md` ← OKU.**
- **Kararlar:** Türkçe Zemberek opsiyonel üst-kalite (NW zaten %98.8); **diller-arası = apertium `.dix` boru hattı** (★ sıradaki, en yüksek değer); Joshi kaynak sınıfı (0-5) profillere; NLLB red.
- **★ DİLLER-ARASI MOTOR YAPILDI + GENİŞLETİLDİ (10/10 dil):** `/crosslang` (apertium `.dix` grafiği + BFS pivot) — aranan kelime tüm Türk dillerinde CANLI üretilir (statik "okuduk" gibi); Karşılaştır "dizilim"e bağlı. Deepsearch 5c uygulandı: **chv-tur (31K) + kaz-sah** ile Çuvaşça+Saha bağlandı (хӗр→kız, göz→харах); **fiil TAM etiket normalizasyonu** (TAG_NORM: chv/sah ifi→past, kaz/kir pres→aor fallback). `.dix` VM'de `/root/koken_api/dix/` (`fetch_dix.sh`). Joshi kaynak-sınıfı (0-5) profillerde. Fiil bölümleme + chv kaynaşık-çöküş cilası yapıldı (yeniden-üretim %92-95).
- **✅ (b) SES DENKLİKLERİ KANIT-DESTEKLİ + kognata bağlı:** Karşılaştır>Ses denklikleri'ndeki 4 kural artık Savelyev kognat verisinden kanıtlı (rotasizm 36 *ŕ, lambdasizm 29 *ĺ, y->ś 14); kognat seçip "incele" → kuralı vurgular. (Kullanıcı kararı: yerleşik kurallar ground truth, veriden kanıtla.)
- **★ AŞAĞISI = KRONOLOJİK GEÇMİŞ (paper için log). GÜNCEL durum yukarıda "★★ GÜNCEL DURUM" + `plan/GELECEK-PLANLAR.md`'de. `plan/YOL-HARITASI.md` (FAZLI + DEEPSEARCH İHTİYAÇ HARİTASI):**
  - **ŞİMDİ yapılabilir (deepsearch BEKLEMEZ):** Faz **1.1** füzyonel ek ince-ayrışması (NW kanonik-allomorf; 5c yöntemi+örnekleri verdi: chv -не=+i+n+e bölünebilir, chv sırası Kök+İyelik+Çoğul+Hâl) · Faz **1.3** harita/soy-ağacı UX (Türkiye konumu + tıkla-inline) · Faz **1.4** Hakkında/iletişim.
  - **Deepsearch BEKLER:** Faz 2.1 TTS (`6`), 2.2 LLM/HF ekosistem (`7`), 2.5 kollar açıklayıcı (`8`), 2.6 derin dil profilleri (`9` kol-batch), 2.7 KAYNAKLAR büyük güncelleme (TÜM deepsearch'ler sonrası) · Faz 3 Çuvaşça "Dilin Kalbi" (✅ ayrı sayfa onaylı).
  - **Deepsearch promptları HAZIR:** `arastirma/5,5b,5c,6,7,8,9*.prompt.md`. Çıktılar geldikçe locale çek (pdfminer; PDF'ler gitignore, `_*.txt` commit'li), çapraz-kontrol, işle.
  - **GELMİŞ + İŞLENMİŞ deepsearch çıktıları:** `_nlp_araclari.txt`+`_nlp_envanteri.txt` (5/5b) ✅, `_morfoloji_plani.txt` (5c) ✅, **`_siniflandirma.txt` (8) ✅ → Faz 2.5 kollar açıklayıcı YAPILDI** (Tarih & Köken'e "altı kol" kartı + Bayes soy ağacı), **`_profil_*.txt` (9.1-9.5) ✅ → Faz 2.6 derin profiller YAPILDI** (`profiles_deep.json`, 14 dil × 4 bölüm; Joshi çapraz-kontrol düzeltmeleri). 25 Haz.
  - **`_tts_asr.txt` (6) ✅ → Faz 2.1 YAPILDI** (profillere "Seslendirme (TTS/ASR)" 5. bölümü, `profiles_tts.json`).
  - **`_llm_hf_ekosistem.txt` (7) ✅ → Faz 2.2 YAPILDI + YENİDEN** (v1 matris yetersiz bulundu → v2: ayrı **"Ekosistem" sayfası**, kategori-önce → dil-içinde → DOĞRUDAN bağlantı; 8 kategori, 101 link; Zemberek/TRmorph/Apertium dahil; hub linkleri + dil-bazlı öne çıkanlar; `ecosystem.json`). Deepsearch 7 + kendi web araştırmam; nötr. Zenginleştirme promptu hazır: `arastirma/10-ekosistem-derin-linkli.prompt.md`.
  - **`KAYNAKLAR` (2.7) ✅ → YAPILDI** (uygulama içi SOURCES+USAGE'a bayes/hf/deepds; KAYNAKLAR.md'ye 3 yeni veri dosyası + deepsearch satırları).
  - **★ TÜM DEEPSEARCH + 2.x İÇERİK İŞLENDİ (2.1/2.2/2.5/2.6/2.7 ✅).** Ekosistem (2.2) **yeniden tasarlandı**: ayrı "Ekosistem" SAYFASI, kategori SEKMELERİ (tıkla→tek kategori), 8 kategori × dil × link launchpad (Zemberek/Apertium dahil).
  - **★ FAZ 1 + 3.1 (deepsearch-bağımsız) YAPILDI:** **1.3 harita inline-kart ✅**, **1.4 Hakkında/iletişim ✅**, **1.1 güvenli füzyon-bölme ✅** (chv pl+hâl temiz sınırı böl; segment_eval: chv ek-sayı %75.3→%92.0, regresyon yok; VM'ye deploy edildi; px+hâl portmanteau korundu), **3.1 Çuvaşça "Dilin Kalbi" anlatı sayfası ✅**.
  - **★ A BLOĞU (deepsearch-bağımsız) TAMAMLANDI:** **1.1b** ✅ (vokal-sonu iyelik kurtarma: кӗнеки→kök+и; chv ek-sayı %92→%93.2, recon %93.2→%94.4, regresyonsuz; toplam 1.1: chv %75.3→%93.2). **Kol-düzeltmeleri** ✅ — veri çapraz-kontrolü: cognates.json kol etiketleri ZATEN doğru (CrimeanTatar→Kıpçak, Salar→Oğuz, SarygYugur→**Sibirya**, Khalaj→Argu); yanlış atama YOK → Tarih & Köken altı-kol kartına **"Geçişken & sınır diller"** nüans notu eklendi (Kırım Tatarcası geçişken, Salarca [areal:Amdo], Sarı Uygurca adı-yanıltıcı Güney Sibirya).
  - **Ekosistem zenginleştirme (deepsearch 10) ✅ YAPILDI** (`_ekosistem10.txt` → `ecosystem.json` metriklerle: Asure-12B, KazLLM, VNLP 287★, sayro-tts, mmBERT 340K↓…). → **Bununla DİKEY MVP bitti.**
  - **★ SIRADAKİ = YATAY ÖLÇEK** (güncel özet ve sıralı plan: §0 üstündeki "★★ GÜNCEL DURUM" + `plan/GELECEK-PLANLAR.md` A/B/C/D). Deepsearch **11-18 promptları yazıldı** (`arastirma/11..18`), kullanıcı çalıştıracak. UI cila notları GELECEK-PLANLAR Bölüm A'da.
  - **Açık sorular:** YOL-HARITASI karar günlüğü (kollar açıklayıcı yeri; harita projeksiyon tipi).

### ✅ A→F PLANI + GÜNCELLEME NOTLARI — TAMAMLANDI (24 Haz, Claude_Preview'da doğrulandı)
Tümü `build.py` enjeksiyonu, her adım ayrı commit+push. **Backend canlı doğrulandı** (uvicorn temiz restart, §4.6).
- **A) Multi-dil OTOMATİK analiz** ✅ — `/analyze_all` canlı; dil seçicide **"⚡ Otomatik · tüm diller"**; `runSearch` auto dalı → ilk eşleşen dil + Analiz'de **"BU KELİME ŞU DİLLERDE"** çip satırı (tıkla → o dile geç, state `apiMatchCodes/apiMatchLang/apiAllLangs`). **Dil seçici değişince anında yeniden çözer** (kullanıcının "çalışmıyor" algısı çözüldü). Paylaşılan `apiWordFrom(lg,word,analyses)` + `LIVE_LN`.
- **B) Araştırmacı Merkezi CANLI** ✅ — serbest sözcük girişi + sağ-üstteki dil → canlı `/analyze` → **gerçek JSON/CoNLL-U/CSV** + **İndir** (Blob) + Kopyala; API URL aranan kelimeye göre güncel. `runResearch(lang,word)` + sentetik WORD-şekilli nesne (metodun gerisi aynı kalır).
- **C) Kognat okunur yazım** ✅ — `readable()` (ḳ→q, χ→h, ɣ→ğ, ə→ä, ŋ→ñ, ɘ→ĕ …) düğüm sözcüklerine; proto-kök akademik korundu; "Biçimler okunur karşılaştırmalı yazımdadır" etiketi.
- **D) Karşılaştır "dizilim" canlı** ✅ — `goCompareActive` canlı kelimede `/analyze_all` → `compareApi` → diller-arası satır; başlık ham gloss yerine yüzey biçimi (`compareHeadline`). Küratörlü kelimeler eski zengin görünümü korur.
- **E) Tarih & Köken** ✅ — Çuvaş-merkezli 2 kaynaklı olay: İdil Bulgar mezar yazıtları (Erdal), Aşmarin 17 ciltlik sözlük.
- **F) 'demo' temizliği** ✅ — `SOURCES.demo` çıkarıldı; hiçbir modülde "⚠ örnek/illüstratif" kalmadı.

### ✅ KULLANICI GÜNCELLEME NOTLARI (24 Haz screenshot) — TAMAMLANDI
- **G1)** "HAM ÇIKTI / ⬇ Dışa aktar" kara barları (paradigma+kognat) KALDIRILDI → yerine **tablolarda kopyalama** (paradigma "⧉ Tabloyu kopyala"; araştırmacıda Kopyala+İndir).
- **G3)** Paradigma örnek kökleri **dil dengeli** (хӗр·Çuvaşça, ev·Türkçe, кул·Tatarca, бала·Kazakça, ат·Yakutça; tıkla → o dilde canlı çekim). Çuvaşça en önemli/varsayılan.
- **G4)** Sağ-üst **dil seçimi** (A'da anında geri bildirim) ve **Кир/Lat** toggle: ikisi de ÇALIŞIYOR (Çuvaşça вуларӑмӑр→vularămăr doğrulandı; Latin-script dillerde çevrilecek bir şey olmadığı için değişmez — beklenen).
- **G7)** Sol-alt **"XP · x/y ünite"** sayacı KALDIRILDI (eğitim portalı = gelecek işi, `plan/GELECEK-PLANLAR.md`; girişi sol menüdeki "Öğren").
- Font/renk paleti korundu; tüm 11 ekran render, `logicError:null`.

> İLERİDE benzer iş döngüsü: `build.py`'ye yama → `python platform/ui/build.py` → Claude_Preview'da doğrula → commit+push. **Preview: reload/click sonrası eval ASYNC — bir tık sonra tekrar oku.**

### OKUNMASI GEREKEN MD'LER (sırayla)
1. **Bu DEVAM.md** — özellikle §0, §2 (VM), §3 (apertium), §4.5 (felsefe), §4.6 (hatalar), §7.
2. `platform/ui/README.md` — UI veri sözleşmesi + **build.py workflow** (kritik: .dc.html elle düzenlenmez).
3. **`platform/GELISTIRME-GUNLUGU.md`** — KALICI kronolojik geliştirme günlüğü (paper için: kararlar+gerekçe+metrik gelişimi+hata analizi). Her oturumda güncellenir.
3b. **`platform/MORFOLOJI-DEGERLENDIRME.md`** — yüzey-bölümleme yöntemi (NW-hizalama) + 10-dil test sonuçları + deepsearch kararları + sıradaki işler.
4. `platform/KAYNAKLAR.md` — kaynak/lisans defteri (provenance).
4. `platform/backend/README.md` — API başlat/durdur/erişim.
5. **`plan/YOL-HARITASI.md`** — FAZLI yol haritası (kullanıcı notları + deepsearch bulguları; açık sorular/karar günlüğü). · `plan/TODO.md` · `plan/PLATFORM-VIZYON.md` · `plan/GELECEK-PLANLAR.md` (eğitim portalı + yatay ölçek, EN SON) · `plan/YOLCULUK-VE-VAZGECILENLER.md`.

### KRİTİK HATIRLATMALAR
- Commit'lerde **yalnız kullanıcı (Muhammed Kumcu)** görünür — **Co-Authored-By Claude YOK**.
- **`.dc.html` ELLE DÜZENLENMEZ** → her şey `build.py`. Siteyi BOZMA (güzel tasarım); değişiklikleri abartma, net olanları yap.
- **Kaynak ilkesi:** PDF doğrudan veri değil; işaret ettiği veri setini locale çek, çapraz-kontrol et (özellikle Wikipedia), atıf+lisans ver, **uydurma yok** (kaynak yoksa null/boş bırak).
- **Önce dikey (MVP sağlam+kaliteli), SONRA yatay (tüm Türk dillerine ölçek).** Yatay ölçek EN SON.
- Canlı API için **VM açık + uvicorn çalışır** olmalı.

---

## 1) PROJE (özet)
Açık kaynak, çift-kitleli (öğrenen+araştırmacı) **Türk dilleri morfoloji + karşılaştırma + araştırma platformu**. Diller (apertium morph backend): **chv tur aze tuk gag crh tat bak kaz kir kaa krc kum nog uzb uig alt kjh tyv sah** (+klj kısmi). MVP 10: tur, aze, kaz, kir, uzb, uig, tat, bak, chv, sah.

---

## 2) ORTAM — VM/APERTIUM ERİŞİMİ (KRİTİK)
- **Proje kökü (Windows/host):** `C:\Users\Tombulteke\Desktop\cuvas-guncelleme`
- **Windows'ta apertium ÇALIŞMAZ** (`pip install hfst` derlenmez). **Geliştirme/canlı API Linux VM'de.**
- **VM:** VirtualBox `RHEL9-Bootcamp` (RHEL 9.8, Python 3.9). Host'tan SSH:
  ```bash
  ssh -i ~/.ssh/cuvas_vm -p 2222 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1
  ```
  - NAT port-forward (host 2222→guest 22) + (host 8000→guest 8000, adı `koken`). VM kapanırsa tekrar gerekebilir:
    `VBoxManage controlvm "RHEL9-Bootcamp" natpf1 "ssh,tcp,127.0.0.1,2222,,22"` / `... "koken,tcp,127.0.0.1,8000,,8000"`.
  - venv: `/root/apv` (hfst+turkicnlp+fastapi+uvicorn). FST'ler `/root/.turkicnlp/models/`. API kodu: `/root/koken_api/app.py`.
  - guest firewalld'de 8000 açık (`firewall-cmd --add-port=8000/tcp --permanent`).
- `VBoxManage` host'ta: `/c/Program Files/Oracle/VirtualBox/VBoxManage.exe`. `gh` (host) `muhammedkumcu` authenticated.

---

## 3) APERTIUM / BACKEND — NASIL ÇALIŞIR (kanıtlanmış)
- FST yolları: `~/.turkicnlp/models/<dil>/<script>/morph/apertium/<dil>.{automorf|autogen}.hfst` (analiz | üretim).
- İndirme (yalnız morph, nöral modeller DEĞİL): `turkicnlp.download(lang, processors=['morph'], script=<Latn|Cyrl|Arab>)`.
- Düşük seviye: `hfst.HfstInputStream(path).read().lookup("кӗнеке<n><pl><dat>")` → `[('кӗнекесене',0.0)]`.
- **API başlat (VM'de) — TEMİZ restart (§4.6'daki tuzağa dikkat):**
  ```bash
  ssh ... 'pkill -9 -f "uvicorn app:app"; sleep 2; cd /root/koken_api && setsid /root/apv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 >uvicorn.log 2>&1 </dev/null & '
  # SONRA VM-İÇİ doğrula: ssh ... 'curl -s http://127.0.0.1:8000/health'  (host'tan önce!)
  ```

---

## 4) PİVOT GEÇMİŞİ (kısa)
- **Faz 1 (terk):** Türkmence kendi-motorunu Çuvaşça için tekrarladık → `arsiv/cuvasca-kendi-motor/` (Python motor, %75 kapsam, **karışık-yazı %45.85 bulgusu** — sona saklandı). Detay: `plan/YOLCULUK-VE-VAZGECILENLER.md`.
- **Kırılma:** apertium olgun + Linux'ta çalışıyor → kendi motor gereksizdi (kullanıcı haklıydı).
- **Pivot:** çok-dilli apertium platformu + karşılaştırma ağı (kullanıcı fikri).

## 4.5) FELSEFE & İLKELER (yön bunlardan çıkar)
- **Olgun açık kaynağı yeniden icat etme** → üstüne değer kat (erişilebilirlik, pedagoji, karşılaştırma).
- **Düşük-kaynak/tehlikedeki Türk dilleri için dijital kapsayıcılık.**
- **Apertium = motor (rakip değil); biz = erişilebilirlik + öğrenme + karşılaştırma + araştırma katmanı.** Hatalar yüzeye çıkınca apertium'a geri katkı.
- **Gerçek kaynak, locale çek, çapraz-kontrol, atıf+lisans, UYDURMA YOK.** PDF'ler pusula; veri PDF'in işaret ettiği setlerden. (Kullanıcı bunu DEFALARCA vurguladı — kaynaklara/doğruluğa aşırı önem; uydurma link/segmentasyon/iddia = KIRMIZI ÇİZGİ. Emin değilsen koyma, "kaynak bulunamadı" yaz.)
- **Kanıtla, iddia etme** (empirik test). **Test sonucunu kullanıcıya GÖSTER** (ör. backend morfoloji = `segment_eval` önce/sonra; regresyon kontrolü). Bozma riski varsa değişikliği yapma/geri al.
- **Commit + push SIK** (her adımda; kullanıcı sık unuttuğumu hatırlattı). Commit'lerde yalnız Muhammed Kumcu (Co-Authored-By YOK).
- **HARDCODED kısımlar önemli + unutulur** — UI değişikliklerinde sabit metin/sayıları (başlık, dil sayısı vb.) tara.
- **Önce dikey (MVP sağlam ✅), sonra yatay (ölçek).** Siteyi bozma; değişiklik abartma; tasarımı koru.

## 4.6) HATALAR & ÇÖZÜMLER (tekrar düşmemek için)
- **Apertium "kullanılamaz" YANLIŞTI** → Windows'ta hfst yok ≠ apertium yok; **Linux VM**. DERS: ortam-engelini genel imkânsızlık sanma.
- **⚠ uvicorn ESKİ kod tuzağı (YENİ):** Çok önceki bir turda `setsid uvicorn ... &` bir SSH komutunda başlatıldı ve harness o kanalı **uzun süre arka planda tuttu** (pid 6157/6159); app.py değişince **eski uvicorn ESKİ kodu servis etmeye devam etti** (404 /analyze_all). ÇÖZÜM: `pkill -9 -f "uvicorn app:app"; sleep 2; setsid ... uvicorn ... </dev/null &` → **VM-İÇİ `curl localhost:8000/health` ile doğrula, SONRA host'tan test et.** Host'tan "connection reset/10054" = uvicorn down. DERS: kanalı tutan uvicorn-start komutları sorun; her zaman temiz pkill+restart+VM-içi doğrula.
- **build.py string-yama yaklaşımı:** `.dc.html` elle düzenlenmez; build.py'de **birebir string** eşleşmesi gerekir. Apostrof: tasarımcı **kıvrık ' (U+2019)** kullanmış → ASCII ' ile eşleşmez. Apostrof içeren metni JS'e enjekte ederken **`json.dumps`** kullan (çift tırnak, güvenli). Eşleşme tutmazsa build.py uyarı basar.
- **Claude_Preview async:** `location.reload()`/`click()` sonrası eval HEMEN okursa boş döner (render async) → bir eval sonra tekrar oku. `<select>`/`<input>` simülasyonu: `el.value=...; el.dispatchEvent(new Event('input',{bubbles:true}))` (+ Enter için `KeyboardEvent('keydown',{key:'Enter',bubbles:true})`).
- **Windows konsol (cp1254) Türkçe ı/ş + Kiril'i bozar** → dosyaya UTF-8 yaz, `Read`/python (`sys.stdout.reconfigure(encoding='utf-8')`) ile doğrula; konsola güvenme.
- **Güvenlik classifier:** public repo / kalıcı-uzaktan-erişim engellenebilir → kullanıcı açık onayıyla yap, BYPASS etme.
- **Ölü host → Wayback Machine** (web.archive.org) dene. **Windows git CRLF uyarıları** zararsız.

---

## 5) ARAŞTIRMA TEMELİ (`arastirma/`) — HEPSİ ELDE
- **1-cuvasca-morfoloji**, **2-egitim-platform** (prompt+pdf) — eski faz/konumlandırma.
- **3-turk-dilleri-karsilastirma** (+pdf) — eşzamanlı dilbilim çekirdeği (ses denklikleri, paradigmalar, kognatlar, veri envanteri).
- **3b-karsilastirma-agi-temeli** (pdf) — ÜRÜN/MÜHENDİSLİK (3-katman veri mimarisi, **FST olgunluk seviyeleri**, MVP seti, veri setleri+lisans).
- **4-turk-dilleri-tarih-sosyokultur-iliski** (+pdf) — tarih/sosyokültür/ilişki (profiller, AES, **uzaklık matrisleri J.1-3**, areal, genetik-vs-dil, araştırmacı ekosistemi).
- **4-KONUDISI-...pdf** = misfire (metodoloji denemesi), içerik için KULLANILMAZ.
- Çıkarılmış metinler `_research*_text.txt` (gitignored).

## 6) KLASÖR HARİTASI
```
DEVAM.md · README.md
arastirma/   1..4 prompt.md + pdf'ler · _*.txt (gitignored)
plan/        TODO.md · PLATFORM-VIZYON.md · GELECEK-PLANLAR.md · YOLCULUK-VE-VAZGECILENLER.md · PLAN.md · PLATFORM-OZELLIKLERI.md
platform/
  backend/   app.py (FastAPI) · README.md · requirements.txt
  ui/        Morfoloji Platformu.dc.html (TASARIM, elle düzenleme!) · support.js (runtime) · build.py (ENJEKSİYON) · dist/index.html (çalışır) · README.md · screenshots/(eski)
  data/      *.json (çıkarılmış kaynaklı veri)
  etl/       savelyev_extract.py · glottolog_extract.py · wals_extract.py
  KAYNAKLAR.md · NOTLAR.md · apertium_probe.py
arsiv/cuvasca-kendi-motor/   (terk edilen Python motor)
sources/     (gitignored) savelyevturkic · glottolog-cldf · wals · northeuralex · unimorph* · UD_* · apertium-chv · hunspell_cv …
.claude/launch.json   (Claude_Preview "koken" :8090)
```

## 7) KONVANSİYONLAR / TUZAKLAR
- **Commit'lerde Claude GÖRÜNMEZ** (Co-Authored-By YOK). Yazar = Muhammed Kumcu. Her adımda commit+push.
- **`.dc.html` elle düzenlenmez** → build.py. Önizleme: `python -m http.server 8080` (repo kökü) → `http://127.0.0.1:8080/platform/ui/dist/index.html`.
- **gh** `muhammedkumcu` authenticated. Repo public. Deploy/uzaktan-erişim = classifier engelleyebilir → açık onay.
- Türkmence klasörü (`Desktop/turkmence-guncelleme`) = kullanıcının AYRI projesi; DOKUNMA (push yetkisi de yok, 403).
- md'leri güncel tut (iş ilerledikçe DEVAM.md + plan/TODO.md).

## 8) HEMEN BAŞLAMAK İÇİN (yeni oturum)
1. §0 (A→F planı) + §2 (VM) + §3 (API restart) + §4.5 (felsefe) + §4.6 (hatalar, özellikle uvicorn) oku.
2. **VM'i kontrol et + uvicorn temiz restart + `/analyze_all` doğrula** (A planının ön şartı).
3. A→F'yi sırayla uygula: her adım build.py → `python platform/ui/build.py` → Claude_Preview doğrula → commit+push.
4. Yatay ölçek YOK (MVP bitene kadar).

## 9) COMPACT SONRASI — KULLANICININ GÖNDERECEĞİ ÖRNEK PROMPT
```
cuvas-guncelleme projesindeyiz. Önce DEVAM.md'yi oku (§0 A→F planı + §2 VM + §3 API restart + §4.5 felsefe + §4.6 hatalar).
KÖKEN = ~20 Türk dili morfoloji+karşılaştırma+araştırma platformu; backend VM'de canlı (apertium), UI build.py ile
dist/index.html'e enjekte (.dc.html ELLE DÜZENLENMEZ). Şimdi: A→F planını TEK PATCHTE, aralarda commit+kontrol ile bitir.
Önce VM uvicorn'u temiz restart edip /analyze_all'ı doğrula, sonra A (multi-dil otomatik) UI'sini yap. Commit'lerde Claude görünmesin.
```
