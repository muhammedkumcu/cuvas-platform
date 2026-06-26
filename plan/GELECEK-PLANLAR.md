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

### B1 · Deepsearch promptları/çıktıları (11 ✅ işlendi; 12-18 elde, çıkarım sırada)
- `arastirma/11-tum-turk-dilleri-envanter.prompt.md` — TAM dil/lehçe listesi + ISO/Glottocode/kol/koordinat/canlılık (ölçek TEMELİ).
- `12-oguz` · `13-kipcak` · `14-karluk` · `15-sibirya` · `16-ogur-argu` **-derin-profiller.prompt.md** — kol-bazlı DERİN profiller + lehçeler (her dil: kimlik/canlılık/koordinat/tarih/yapı/izogloss/**15 kognat anahtar kelime**/dijital).
- `17-capraz-kol-ses-denklikleri.prompt.md` — tüm kol-çiftleri izogloss tabloları (ses denklikleri modülünü Çuvaş-ötesine taşı).
- `18-genisletilmis-kognat-leksikal.prompt.md` — Leipzig-Jakarta+Swadesh, **kategorize** (A1 kelime-seçiciyi besler).

### B2 · Sonuçlar gelince işlenecek modüller
- **Dil Profilleri:** 🔄 **BASE 14 → 47 ✅** (master'dan; ad/kol/konuşur/egids/vit/script/region/joshi/note — sourced özet; yeni 33 dil gezilebilir, ÖZET-only). **Kalan:** derin bölümler (Tarih/Yapı/İlişkiler/Dijital/TTS) 14 → 47 (deepsearch 9 ~30 dil + 12-16 kol-derin → DEEPPROF/tts genişlet). *(Not: profil selektörü 47'de uzun liste — A1-tarzı kategori/arama ileride.)*
- **Kognat Ağı:** 14 kavram × 7 dil → çok kavram × tüm diller (Savelyev 254 kavram + deepsearch 18). A1 kelime-seçici şart.
- **Ses denklikleri:** Çuvaş-merkezli → tüm kol-çiftleri (deepsearch 17).
- **Uzaklık:** Savelyev 32 dil matrisini tam aç (şu an 10).
- **Harita:** ✅ 14 → 47 dil (master envanteri; gerçek çizim harita + açgözlü etiket declutter + era stili). *(Profiller ölçeklenince inline kart notları ds12-16'dan zenginleştirilebilir.)*
- **Ekosistem:** deepsearch 7+10 ~25 dil işlendi; yeni dillerde HF arama hub'ı + bulunanlar.

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
