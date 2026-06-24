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

## 1.5) ŞU AN — Vizyon & UI fazı (BENİM YAPILACAKLARIM)
- [x] **Platform vizyon/kavram dokümanı** → `plan/PLATFORM-VIZYON.md` (amaç/vizyon/misyon/kitleler/modüller/ekran haritası — UI geliştirmeyi beslemek için).
- [ ] **Kullanıcı:** geliştirdiği **UI dosyalarını** gösterecek → birlikte inceleyip ona göre çalışmaya başla.
- [ ] UI geldiğinde: UI'yı vizyon/modül haritasıyla eşle; eksik/uyumsuz noktaları çıkar; UI ↔ backend API sözleşmesini taslakla.
- [ ] **Mimari dokümanı** → `plan/MIMARI.md` (birleşik veri modeli #3+#3b+#4; modül haritası; API uçları; veri şeması core/extended + script katmanı; FST olgunluk → MVP).

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
