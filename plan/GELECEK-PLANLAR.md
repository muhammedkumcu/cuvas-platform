# GELECEK PLANLARI — Yatay ölçek + cila + altyapı (DİKEY MVP sonrası sıralı plan)

> **Durum (25 Haz 2026):** Deepsearch-bağımsız **dikey MVP neredeyse tamamen bitti** (Faz 1 + 2.x + 3.1; bkz `YOL-HARITASI.md`). Sırada **yatay ölçek** (tüm Türk dilleri + lehçeleri) ve ona hazırlık UI cilası var. **Sıralama aşağıda.** Çocuk eğitim portalı **EN SON** iş (Bölüm D). Felsefe değişmez: **kaynak + test + doğruluk; UYDURMA YOK** (DEVAM §4.5).

---

## BÖLÜM A — YATAY ÖLÇEK ÖNCESİ UI / CİLA (kullanıcı notları, 25 Haz) — ✅ TAMAMLANDI (26 Haz)
> Bunların çoğu yatay ölçeğin ÖN ŞARTI: dil sayısı artınca bu sorunlar büyür. **A1–A6 hepsi yapıldı, Claude_Preview'da doğrulandı, ayrı commit+push'lu** (sonuç özeti aşağıda, her madde başında ✅).

- **A1 · Kognat kelime-seçme ekranı (★ ölçek ön-şartı):** Yatay ölçekte tüm kelimeleri ekleyeceğiz → seçim ekranı çok kalabalık olacak. **Kategorili/aranabilir** bir kelime-seçici lazım (vücut/doğa/sayı/akrabalık/eylem… — bkz deepsearch 18 kategorileri). Şimdiki düz liste ölçeklenemez.
- **A2 · Karşılaştır ekranı başlık hardcode'u:** Karşılaştır'a girince **"'okuduk' — diller arası"** başlığı TÜM sekmelerde (dizilim, ses denklikleri, soy ağacı, harita) kalıyor — mantıksız sekmelerden (soy ağacı, harita, ses denklikleri) **kaldır** (yalnız "dizilim"e ait). *(Hardcoded — kolay unutulur; bkz E maddesi.)*
- **A3 · Ana sayfa (landing) güncelliği:** İlk karşılayan ekran eskimiş — artık daha çok dilde analiz yapabiliyoruz, yatayda çok daha fazla olacak. Dil sayısı/kapsam dinamik yansımalı (hardcoded "N dil" varsa güncelle).
- **A4 · Harita arka planı + düğüm yoğunluğu:** Konumlar doğru (gerçek koordinat projeksiyonu) ama **arka plan haritası biraz saçma duruyor** — şekil/renkler beğenildi, bu tarzda ama **daha doğru** bir arka plan çiz. + Bazı düğümler çok yakın (Çuvaşça↔Tatarca; Tatarca arkada kalıyor); yeni diller eklenince daha zor olacak → **düğüm seçme/ayırma önlemi** (hover büyütme, zoom, ya da tıkla-listeden-seç). (Deepsearch 11 koordinatları + S.Sibirya kümesi.)
- **A5 · Uzaklık Gezgini ortadaki kutu:** Ortadaki gösterim kutusu **çok uzun** → taban-dil seçim kısmını kısıtlıyor. O UI yeniden dengelenmeli (kutu kompakt, taban-dil + eksenler ferah). Genel olarak iyi düşünülmeli.
- **A6 · Kaynaklar & Lisanslar büyümesi:** Yatayda çok kaynak olacak → kendi sayfasında **kategori** (veri/araç/model/literatür/deepsearch…) düşün. Her modülün KULLANIM eşlemesi güncel kalmalı. (Ne zaman: her yeni veri eklendiğinde + ölçek sonrası toplu.)

### ✅ SONUÇ ÖZETİ (26 Haz — yapıldı, Claude_Preview doğrulamalı, ayrı commit'ler)
- **A1 ✅** kategorili+aranabilir kognat seçici (çipler Vücut/Doğa/Zaman/Sayılar/Soyut sayaçlı + arama + boş-durum; `COG_CAT`, ds18 ile genişleyecek).
- **A2 ✅** `compareHeadline` sekmeye-duyarlı: "X — diller arası" yalnız dizilim; diğer sekmeler sekme-başlığı (çift-tanım çakışması giderildi).
- **A3 ✅** landing katmanlı kapsam şeridi (10/23/32 dil + 6 kol, hepsi VERİDEN) + footer "6 KOL·32 DİL" (eski "5·14" stale+yanlıştı) + "yedi dilde"→"diller arasında".
- **A4 ✅** harita arka planı projeksiyon-hizalı (`build_map_bg()`, iç denizler gerçek lat/lon: Hazar Azerice↔Türkmence kıyıları doğru) + hover-büyütme + etiket kademe (Tatarca/Şor/Tuvaca); tıkla→inline kart korundu.
- **A5 ✅** Uzaklık radar kutusu kompakt (`align-items:start`) + taban-dil/eksen ferah + OKUMA sağ sütuna (denge).
- **A6 ✅** Kaynaklar 4 kategori grubu (Araçlar & motorlar / Veri setleri / Akademik literatür / Derin araştırma & derlemeler) + sayaç; ölçekte yeni kaynaklar kategoriye düşer.
> **Ölçek bağı:** A1'in `COG_CAT` taksonomisi + kavram listesi deepsearch 18 işlenince genişletilecek; seçici altyapısı hazır.

---

## BÖLÜM B — YATAY ÖLÇEK (tüm Türk dilleri + lehçeleri) — 🔄 DEVAM EDİYOR
> Felsefe: önce dikey sağlam (✅), sonra yatay. **Deepsearch 11-18 çıktıları geldi (`arastirma/11..18*.pdf`).**

### ✅ YAPILDI (26 Haz)
- **B0 · Master envanteri `languages.master.json` (★ temel):** ds11 (pdfplumber tablo) + Glottolog çapraz-kontrol → **47 dil/lehçe/tarihsel** (39 canlı+7 tarihsel+1 proto). Koordinat: canlı→Glottolog, tarihsel→ds11. `platform/etl/build_master.py`.
- **Harita + ATLAS ✅ tüm 47 dile açıldı:** gerçek çizim harita (`build_map_bg()` v3: kıyılar/iç denizler/Basra/dağ sıraları/**nehirler**/ızgara) + açgözlü etiket-yerleştirme (çakışma çözüldü) + era stili + inline kart (vitalite+era). **ATLAS sayfası** (kullanıcı: "sığmıyor → önizleme + tıkla→büyük sayfa"): Karşılaştır'da küçük önizleme (dots-only) + "Büyük atlas" butonu/nav → ayrı büyük sayfa; zengin adlandırılmış coğrafya (İstanbul Boğazı, denizler, dağlar, nehirler, Turan/Sibirya bölgeleri). **Kullanıcı istekleri karşılandı.**

### B1 · Deepsearch promptları/çıktıları (11–18 ✅ TÜMÜ İŞLENDİ)
- `arastirma/11-tum-turk-dilleri-envanter.prompt.md` — TAM dil/lehçe listesi + ISO/Glottocode/kol/koordinat/canlılık (ölçek TEMELİ).
- `12-oguz` · `13-kipcak` · `14-karluk` · `15-sibirya` · `16-ogur-argu` **-derin-profiller.prompt.md** — kol-bazlı DERİN profiller + lehçeler (her dil: kimlik/canlılık/koordinat/tarih/yapı/izogloss/**15 kognat anahtar kelime**/dijital).
- `17-capraz-kol-ses-denklikleri.prompt.md` — tüm kol-çiftleri izogloss tabloları (ses denklikleri modülünü Çuvaş-ötesine taşı).
- `18-genisletilmis-kognat-leksikal.prompt.md` — Leipzig-Jakarta+Swadesh, **kategorize** (A1 kelime-seçiciyi besler).

### B2 · Sonuçlar gelince işlenecek modüller
- **Dil Profilleri:** **BASE 14 → 47 ✅** + **DERİN bölümler 14 → 39 ✅** (ds9/14/16 _profil_*.txt'ten faithful+atıflı 4 bölüm). Eklenen 25: Özbekçe/G.Özbekçe/Eynu/İli (Karluk) · 5 Kıpçak (Karakalpak/Karaçay-Balkar/Kumuk/Nogay/Kırım Tatar) · 4 Oğuz (Gagavuz/Salar/Horasan/G.Azerbaycan) · 4 Sibirya (alt/atv/Dolgan/Sarı Uygur) · **8 TARİHSEL** (İdil Bulgar/Hazar/Çağatay/Karahanlı/Harezm/Orhun/Eski Uygur/Codex Cumanicus). **Kalan derin = 8 küçük lehçe/kriptolekt** (Kaşkay/Balkan Gagavuz/Sibirya Tatar/Tofa/Urum/Karay/Kırımçak/Çulım) — **dedicated kaynak yok → dürüstçe ÖZET-only.** TTS 14→47 ayrı. *(Selektör 47'de uzun — A1-tarzı kategori/arama ileride.)*
- **Kognat Ağı:** ✅ 7 → **18 dil derin (ds18)** + **254 kavram geniş (Savelyev)**. **Derin/Geniş toggle:** Derin = `cognates_deep.json` (11 kavram × 18 dil; yerel yazı/IPA/morfem/kognat-ID/ses-kuralı). Geniş = `cognates_broad.json` (254 kavram × ≤32 dil; TR gloss + 10 kategori + cogid boşluk; akademik yazım, IPA/ses-kuralı YOK — dürüstçe notlandı). 937KB lazy-fetch (`ensureBroad`, dist'e kopya; index.html gömülmez). cogid boşluk tespiti + "Dil dil ses kuralı/biçim" dökümü her iki modda.
- **Ses denklikleri:** ✅ Çuvaş-merkezli 4 kural → **7 kol-izoglosu** (ds17). `build_sound_laws`: rotasizm/lambdasizm/*h-/*-d-/*-G/*y-/ötümlüleşme; çok-kollu refleks + kanıt rozeti (36/29/14 Savelyev'den). Kognat→kural bağı korundu. *(9 dil-çifti karşılaştırma tablosu ds17'de var — ileride ek sekme olabilir.)*
- **Uzaklık:** ✅ 10 → 32 dil (Savelyev tam leksikal/filogenetik matris; `DIST_ROWS`, koordinat master'dan, LANGVEC 32; tipolojik WALS 23). *(Anlaşılabilirlik/Lindsay kısmi — genişletilebilir.)*
- **Harita:** ✅ 14 → 47 dil + Atlas/zoom (master; gerçek çizim harita + açgözlü etiket declutter + era stili). *(Profiller ölçeklenince inline kart notları zenginleştirilebilir.)*
- **TTS profil bölümü:** ✅ 14 → **39 dil** (ds6). `profiles_tts.json` +25 (`expand_tts_47.py`); her derin profil "Seslendirme (TTS/ASR)" 5. bölümü taşır. Gerçek model uzn/azb/crh/nog; küçük yaşayan diller "yakın-dil ikamesi/eSpeak"; tarihsel diller "uygulanamaz". *(Tavan 39 = derin profil sayısı; 8 özet-only lehçenin TTS bölümü yok.)*
- **Ekosistem:** ✅ + yeni **"Dil dil keşif"** sekmesi (9. kategori) — 39 yaşayan dilin her biri için doğrudan HF arama hub'ı (model+veri; yeni/küçük diller dahil; dürüst "arama" çerçevesi). Küratörlü öne çıkanlar 8 kategoride.
- **Dil Profilleri selektör:** ✅ A1-tarzı arama kutusu + kol kategori çipleri (47 dil uzun listesi süzülür). *(8 küçük lehçe DERİN profili dedicated kaynak olmadığından bloke — uydurma yok; base+TTS "yok" var.)*

---

## ★ İNCELEME NOTLARI (kullanıcı, 28 Haz) — UI cila + içerik fazları
Kullanıcı ayrıntılı sayfa-sayfa inceleme yaptı. İşlenenler ve sıralı kalan:
- **R1-R4 ✅ (28 Haz):** net metin/UI düzeltmeleri · ana sayfa HERO + akıllı arama · konuşur-yılı kaldırma · **Harita** (tek boyut, ölü diller gri çerçevesiz nokta, sürükle-pan, Büyük-atlas butonu kaldırıldı, temiz başlık) · **Kognat** (alfabetik, büyük graf+merkez, ≤26 düğüm tek halka [deep 0 çakışma], broad 2-halka, proto-fit, tablo başlıkları, "Bu sayfa ne anlatıyor?" açıklaması) · **Karşılaştır** (gereksiz kaynak kaldırıldı, soy ağacı "nasıl okunur") · **Uzaklık** (taban/karşılaştırılan yan yana kaydırmalı).
- **★ R-AÇIKLAMA ✅ (28 Haz):** 9 sayfaya "Bu sayfa ne anlatıyor?" (nedir/nasıl okunur/neden önemli + kaynak) eklendi — Harita, Profiller, Tarih, Karşılaştır, Uzaklık, Ekosistem, Analiz, Paradigma, Dilin Kalbi. Kognat deseniyle birebir, tek `_help_block` + sc-if/section regex (9/9). Doğal Türkçe, kaynaklı, uydurmasız.
- **R5a ✅:** 2 deepsearch promptu (19 az-belgeli diller + 20 tarih). **Sonuçlar geldi** (`19/20*.pdf`).
- **R5b ✅ (28 Haz):** **R5b-1** ds19 → 17 derin profil (profiles_deep 39→46). **R5b-2** ds19 Bölüm 3 = 47-dil KAYNAKLI demografi (konuşur/yıl/kaynak/EGIDS/UNESCO) → master tek kaynak (SPKMETA; chv=740bin/2020 korundu; lang_extra speakers override kalktı). **R5b-3** ds20 → Tarih sayfası: Bayes açıklama bloğu (254 kavram/905 kognat/3 düğüm+%95 GA) + 6 kol detaylı izogloss + 15-satır kaynaklı timeline + kronolojik renk gradyanı.
- **⏳ R6:** Kaynaklar overhaul — "deepsearch" yerine **gerçek kaynaklar** (her ds PDF'inin içindeki atıflar); Kaynaklar sayfasını katmanlı genişlet.
- **⏳ R7:** analiz MD'leri — inceleme-yöntemi.md (kullanıcı tarzı) + sayfa-sayfa analiz (Morfoloji/Paradigma dahil, kullanıcının bakmadıkları).
- **⏳ R8 (en son):** tüm MD + DEVAM.md dikkatli güncelleme + compact-sonrası resume promptu.
- **Bekleyen kararlar:** isim/domain (ertelendi; müsait .com: kokence/getkoken/kokenatlas/sazlir/lirturk).

---

## BÖLÜM C — ALTYAPI (ayrı mühendislik fazları)
- **C1 · Gerçek ses motoru (TTS/ASR):** "▷ Seslendir" şu an tarayıcı Web Speech'e düşüyor. Deepsearch 6'nın önerdiği **Dinamik Hibrit Yönlendirme**: tr/kaz → sunucu Piper (ONNX); uzb/uig/sah → HF Inference API (MMS-TTS, ön-işlem Latin→Kiril/num2words); chv/bak → tarayıcı eSpeak NG (WASM). FastAPI router. ASR telaffuz kontrolü yalnız tr/kaz (Whisper).
- **C2 · Morfolojik ÜRETİM (kullanıcı notu):** Üretim ucu (`/generate`) var ama UI'da öne çıkmıyor; tam bir "kök + etiket → form üret" arayüzü gelecek planı.
- **C3 · Ekosistem HfApi-CRON otomatik güncel-tutma:** `huggingface_hub` ile periyodik `list_models/list_datasets` (author=issai/ytu-ce-cosmos…, tags=language:tr…) → "Yeni çıkanlar" akışı + indirme sayısı güncelleme (ecosystem.json elle güncelden kurtulur).

---

## BÖLÜM D — EN SON: ÇOCUK / ÖĞRENCİ EĞİTİM PORTALI (★ onaylı, en son iş)
**Fikir:** "Öğrenen modu"nu gerçek bir eğitim portalına dönüştürmek.
- **Öğrenen modu** (çocuk-dostu): sade arayüz, oyunlaştırma (ICALL, rozet/seri/SRS — iskelet var), sanal Kiril/Latin klavye, sesli okuma (C1'e bağlı), adım adım dersler.
- **Uzman modu** (araştırmacı): ham etiketler, künye, dışa aktarım, açık API.
- **Saha/Şor "Dilin Kalbi" şablonu:** Çuvaş "Dilin Kalbi" sayfasını (Faz 3.1) diğer tehlikedeki dillere (Saha, Tuva, Halaç…) şablonla. Eğitim portalının canlandırma ayağı.
- **Bağımlılık:** önce A+B+C bitmeli. **EN SON.**

---

## Diğer gelecek fikirleri (yer tutucu)
- Kullanıcı katkısı / topluluk düzeltmeleri (kognat, çeviri, örnek cümle). · Apertium'a geri hata-düzeltme katkısı. · Tarihsel metin/yazıt katmanı (Orhun, Dîvân). · Mobil/PWA. · Kognat motoruna izogloss RegEx; chv px+hâl portmanteau'yu ayrı etiketleme; harita S.Sibirya etiket nudge.

> Ekleme: yeni gelecek fikri/UI notu çıktıkça buraya kaydet.
