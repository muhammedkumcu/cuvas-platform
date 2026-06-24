# YOL HARİTASI & TODO — Türk Dilleri Morfoloji + Karşılaştırma Platformu

> Canlı görev listesi. İş ilerledikçe kutucukları işaretle, yeni madde ekle. **Tek doğruluk kaynağı sıralaması:** [`DEVAM.md`](../DEVAM.md) §0 → bu dosya → ilgili plan dosyaları.
> Güncelleme: **24 Haziran 2026.**

## 0) KARARLAR (kesin)
- **Hedef:** Platformun hakkını ver; **30 Haziran UBMK son tarihine sıkışma** (yetişirsek sunarız). Daha ileri/güçlü bir venue hedefle. "Tarih yokmuşçasına" sağlam çalış.
- **Çift kitle:** (1) **Öğrenenler** (çocuk/öğrenci/meraklı) + (2) **Araştırmacılar** (KRİTİK) — "literatür karşılarındaymış gibi", Türk dil dünyasının takip edildiği, ilk başvurulacak çözüm‑odaklı merkez.
- **Motor:** Apertium FST (analiz **ve** üretim), `turkicnlp`/`hfst`, **Linux/VM'de**. ~20 dil.
- **MVP dil kümesi (KESİN):** **5-kol 10 dil → tur, aze, kaz, kir, uzb, uig, tat, bak, chv, sah** (FST olgunluğuna göre, 3b önerisi). Sonra 20+'ya ölçekle.
- **İlk dikey dilim (KESİN):** **Morfoloji çekirdeği** (analiz + üretim + paradigma) — backend, VM'de.
- **Tech yığını (KESİN):** Backend **FastAPI** (VM/Linux, apertium sarıcı) · veri **SQLite→Postgres** · **açık REST API** · **UI'yı KULLANICI veriyor** (geliştiriyor; gösterecek).
- **Sıralama:** araştırma TAMAM → vizyon dokümanı (bu tur) → kullanıcı UI'yı gösterir → mimari (`MIMARI.md`) + morfoloji backend → modüller.
- **Commit'lerde yalnız kullanıcı görünür** (Co‑Authored‑By Claude YOK).

---

## 1) ARAŞTIRMA FAZI — TAMAM ✅
- [x] #3 (`3-turk-dilleri-karsilastirma.pdf`) + #3b (`3b-karsilastirma-agi-temeli.pdf`, mühendislik odaklı) + #4 (`4-turk-dilleri-tarih-sosyokultur-iliski.pdf`, 24 sf/68 kaynak) alındı, metne çevrildi, isimler düzenlendi.
- [x] Misfire (`4-KONUDISI-...pdf`) işaretlendi — içerik için kullanılmaz.
- [x] Üç derleme triyaj edildi; mimari için anahtar bulgular çıkarıldı (3-katman veri, FST olgunluk seviyeleri, veri setleri+lisans, uzaklık matrisleri).

## 1.5) Vizyon & UI fazı — TAMAM ✅
- [x] **Platform vizyon dokümanı** → `plan/PLATFORM-VIZYON.md`.
- [x] **UI geldi & entegre** → `platform/ui/` (KÖKEN, DesignCanvas prototipi). İncelendi: tam modül seti, 14 dil, öğrenen/uzman modu, yerleşik kaynak-kütüğü. `platform/ui/README.md` (veri sözleşmesi) yazıldı.

## 1.6) ŞU AN — Kaynak çekme & veri çıkarımı (kullanıcı ilkesi: kaynaklı, locale çek, uydurma yok)
- [x] `platform/KAYNAKLAR.md` provenance defteri kuruldu (UI'daki SOURCES ile senkron).
- [x] **Kaynak hasadı:** SavelyevTurkic, **Glottolog-CLDF**, NorthEuraLex, WALS, UniMorph (×9 dil), UD (IMST/BOUN/Kazakh-KTB/Uyghur-UDT) çekildi. (unimorph/chv yok → apertium-chv'den.)
- [x] **Çıkarım — SavelyevTurkic** → `cognates.json` (905 set), `languages.geo.json`, `distance.lexical.json`. Betik: `etl/savelyev_extract.py`.
- [x] **Çıkarım — Glottolog** → `profiles.json` (23 dil + AES canlılık). Betik: `etl/glottolog_extract.py`.
- [x] **Çıkarım — WALS** → tipolojik mesafe + özellik matrisi (`distance.typological.json`, `features.wals.json`).
- [ ] **Çıkarım — kalan:** UniMorph → paradigma · NorthEuraLex → kognat(ikincil) · UD → analiz bağlamı. Joshi/Yunusbayev makaleleri.
- [x] **VM BACKEND CANLI:** apertium FST (10 dil) indirildi → `platform/backend/app.py` (FastAPI) host:8000'de analiz/üretim/paradigma servis ediyor. Test edildi. (`platform/backend/README.md`)
- [~] **UI'ya bağlama** (`platform/ui/build.py` → `dist/`; kaynak .dc.html elle düzenlenmez):
  - [x] **Dil Profilleri + Canlılık** ← `profiles.json` (Glottolog AES); önizlemede doğrulandı (Şorca `EGIDS 8a · ölmekte`), "⚠ örnek" rozeti kalktı.
  - [x] **Harita** ← Glottolog koordinatları (14 dil, gerçek projeksiyon); doğrulandı.
  - [x] **Uzaklık Gezgini** ← gerçek matrisler: 3/5 eksen (leksikal Savelyev + tipolojik WALS + coğrafi koordinat); filo/anla illüstratif kaldı (#4 J matrisleri gelince). Doğrulandı: chv→tt coğrafi 0.02 / leksikal 0.37 / tipolojik 0.26.
  - [x] **Dil Profilleri zenginleştirme** ← `lang_extra.json` (Wikipedia, Glottolog/Savelyev ile çapraz-kontrollü, atıflı): **14/14 dil** — güncel speakers/script/zengin not (kaynakta olmayan kültür notu boş bırakıldı). Layout değişmedi (mevcut slotlar).
  - [x] **Analiz + Paradigma → CANLI API, HERHANGİ KELİME/DİL** (host:8000, graceful fallback):
    - **Dil seçici** (bağlam çubuğu, 10 dil): Analiz seçili dilde herhangi bir kelimeyi çözer. Doğrulandı: Türkçe + 'evlerimizden' → ev+etiketler.
    - **Paradigma serbest kök girişi** + seçili dil: herhangi bir adın canlı çekimi. Doğrulandı: tur + 'ev' → evin/eve/evde/evden/evler (`/paradigm/tur/ev`).
    - Küratörlü Çuvaşça örnekler + Paradigma kökleri quick-pick olarak kalır.
  - [x] **Harita düğümü → profil bağı**: haritada bir dile tıklayınca o dilin profiline gider. Doğrulandı (Çuvaşça düğümü → profil).
  - [x] **Kopya taraması** (3 net düzeltme, konservatif): profil başlığı · kognat notu kaynak tekrarı · Uzaklık illüstratif caption.
  - [x] **Kognat Ağı** ← `cognates.json` (14 kavram, gerçek kognat setleri + boşluklar; Savelyev karşılaştırmalı transkripsiyon — yerel ortografi sonra apertium/translit ile güzelleştirilebilir). Doğrulandı: göz *görs vs Yakut χaraχ boşluğu.
  - [x] **filogenetik eksen** ← Savelyev kognat-karakteri Jaccard mesafesi (Bayes ağacının girdisi; yenilikleri yakalar). Doğrulandı: chv→tt 0.61 (>leksikal 0.37). → Uzaklık 4/5 gerçek.
  - [x] **anlaşılabilirlik eksen** ← Lindsay (deneysel/yaklaşık, `intelligibility.json`, atıflı). → **Uzaklık 5/5 eksen kaynaklı**, "örnek" rozeti + eski illüstratif caption kalktı. Doğrulandı: chv→tt anla 0.92 (Çuvaş izolasyonu).
- [x] **Denetim #1** (görünür taraf): Paradigma başlığı dinamik (sabit "Çuvaşça" bug'ı); öğrenen/uzman + mod-gizleme KALDIRILDI (her şey görünür); "UZMAN MODU"→"HAM ÇIKTI"; paradigma serbest girişi yukarı + örnekler etiketli; stale ~1milyon chv→740bin.

## 1.7) ✅ A→F PLANI + GÜNCELLEME NOTLARI — TAMAMLANDI (24 Haz, Claude_Preview doğrulandı; her adım ayrı commit)
> Detay: `DEVAM.md` §0. VM uvicorn temiz restart + `/analyze_all` doğrulandı (host'tan da). Tümü `build.py` enjeksiyonu.
- [x] **A) Multi-dil OTOMATİK analiz** — "⚡ Otomatik · tüm diller" → /analyze_all + "BU KELİME ŞU DİLLERDE" çipleri; dil değişince anında yeniden çözer (G4). `apiWordFrom`+`LIVE_LN`.
- [x] **B) Araştırmacı Merkezi CANLI** — serbest sözcük+dil → /analyze → gerçek JSON/CoNLL-U/CSV + İndir; API URL canlı. `runResearch`.
- [x] **C) Kognat okunur yazım** — `readable()` (ḳ→q, χ→h, ɣ→ğ, ə→ä, ŋ→ñ…); proto-kök akademik; dürüst "karşılaştırmalı biçim" etiketi.
- [x] **D) Karşılaştır "dizilim" canlı** — `goCompareActive` → /analyze_all → `compareApi`; başlık `compareHeadline` (yüzey).
- [x] **E) Tarih & Köken** — İdil Bulgar mezar yazıtları (Erdal) + Aşmarin 17 ciltlik Çuvaş sözlüğü.
- [x] **F) 'demo' temizliği** — `SOURCES.demo` çıkarıldı.
- [x] **G1)** "HAM ÇIKTI/Dışa aktar" barları kaldırıldı → tablolarda kopyalama. **G3)** paradigma örnekleri dil dengeli. **G7)** sol-alt XP sayacı kaldırıldı. Font/renk paleti korundu.

## 2) #4 GELİNCE — Mimari tasarımı (BİRLİKTE kesinleştirilecek)
- [ ] #4 PDF metnini çıkar + #3 ile birlikte **birleşik veri modeli** tasarla (dil profili, ses‑denkliği kuralı, kognat seti, paradigma, çok‑boyutlu uzaklık matrisi, zaman çizelgesi olayı, kaynak/lisans).
- [ ] **Modül haritası** netleştir (aşağıdaki §4) + **MVP kapsamı** (hangi modüller v1'de).
- [ ] **Teknik yığın** kararı: backend (FastAPI öneri) · veri katmanı (JSON/SQLite/Postgres?) · frontend (hafif SPA) · deploy (Linux/Docker/Render) · API tasarımı (araştırmacılar için açık API).
- [ ] **Genişleyebilirlik ilkeleri:** yeni dil eklemek = veri dosyası eklemek; yeni eksen/modül takılabilir olmalı.
- [ ] Mimari kararları `plan/MIMARI.md`'ye yaz; `DEVAM.md` güncelle.

## 3) BACKEND (VM'de — apertium çekirdeği)
- [ ] VM'de `/root/apv` ortamını doğrula; MVP dilleri için apertium FST'lerini indir (`turkicnlp.download(...)`).
- [ ] **Analiz API'si** (yüzey → kök+etiket), MVP dilleri.
- [ ] **Üretim API'si** (etiket → yüzey) + **paradigma tablosu** üreteci (tag şablonları).
- [ ] **Karşılaştırmalı paradigma** uç noktası (aynı kavram N dilde).
- [ ] **Transliterasyon** katmanı (Kiril/Latin/Arap ↔ Ortak Türk Alfabesi).
- [ ] **Araştırmacı uçları:** toplu analiz/üretim, dışa aktarım (CSV/JSON/CoNLL‑U), kalıcı alıntı bağlantıları, açık API + dokümantasyon.

## 4) KARŞILAŞTIRMA & İÇERİK KATMANI (veriden)
- [ ] **Ses‑denkliği açıklayıcısı** (#3 B bölümü → makine‑okunur kurallar: rotasizm/lambdasizm/*d‑t‑y‑z/*h‑/*g‑v‑w).
- [ ] **Kognat ağı** (#3 E + #4 J → düğüm‑grafik; kognat boşlukları işaretli).
- [ ] **Çok‑boyutlu uzaklık gezgini** (#4 J → filogenetik/leksikostatistik/tipolojik/anlaşılabilirlik/coğrafi matrisler).
- [ ] **Dil profili sayfaları** (#4 C/D/E/H).
- [ ] **İnteraktif harita + zaman çizelgesi** (#4 B/K).
- [ ] **Makro‑akrabalık & temas görünümü** (#4 F/G) — tartışmalılar "tartışmalı" etiketiyle.
- [ ] **Canlılık/tehlike katmanı** (#4 E) + **genetik‑vs‑dil açıklayıcısı** (#4 I, dikkatli).

## 5) FRONTEND & ÖĞRENEN DENEYİMİ
- [ ] Paradigma gezgini (renkli morfemler) + sanal klavye (Kiril/Latin/Arap) — `arsiv/.../web/` UI fikirleri şablon.
- [ ] ICALL alıştırmaları (boşluk‑doldurma + FST‑üretimli çeldirici) + oyunlaştırma/SRS.
- [ ] Çocuk/öğrenci dostu keşif arayüzü; araştırmacı dostu "uzman modu".

## 6) DEĞERLENDİRME & YAYIN
- [ ] Analiz/üretim precision/recall: **UniMorph + UD + Wiktionary** altın standart (ML değil).
- [ ] (Sona) karışık‑yazı %45.85 bulgusu + Çuvaşça derin vaka.
- [ ] Paper (İngilizce; UBMK/TurkLang veya daha güçlü venue). Katkı: çift‑kitleli, çok‑dilli, çok‑boyutlu Türk dilleri morfoloji+karşılaştırma+araştırma merkezi.

---

## NOTLAR
- Her adımda **commit + push** (Claude attribution YOK).
- Apertium'da bulunan hatalar → upstream'e geri katkı (akademik + topluluk değeri).
- İçeriği #3 ve #4 derlemelerine **kaynaklı** dayandır; "uydurma yok" ilkesi platform metinleri için de geçerli.
