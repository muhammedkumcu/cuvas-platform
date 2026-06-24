# YOL HARİTASI & TODO — Türk Dilleri Morfoloji + Karşılaştırma Platformu

> Canlı görev listesi. İş ilerledikçe kutucukları işaretle, yeni madde ekle. **Tek doğruluk kaynağı sıralaması:** [`DEVAM.md`](../DEVAM.md) §0 → bu dosya → ilgili plan dosyaları.
> Güncelleme: **24 Haziran 2026.**

## 0) KARARLAR (kesin)
- **Hedef:** Platformun hakkını ver; **30 Haziran UBMK son tarihine sıkışma** (yetişirsek sunarız). Daha ileri/güçlü bir venue hedefle. "Tarih yokmuşçasına" sağlam çalış.
- **Çift kitle:** (1) **Öğrenenler** (çocuk/öğrenci/meraklı) + (2) **Araştırmacılar** (KRİTİK) — "literatür karşılarındaymış gibi", Türk dil dünyasının takip edildiği, ilk başvurulacak çözüm‑odaklı merkez.
- **Motor:** Apertium FST (analiz **ve** üretim), `turkicnlp`/`hfst`, **Linux/VM'de**. ~20 dil.
- **MVP dil kümesi:** temsilci alt küme → **tur, kaz, uzb, chv, sah, tyv, kjh** (~7; her koldan + tehlikedeki odak). Sonra 20'ye ölçekle.
- **Sıralama:** Önce **#4 PDF'ini bekle** → mimariyi **birlikte** baştan (genişleyebilir) planla → adım adım geliştir.
- **Commit'lerde yalnız kullanıcı görünür** (Co‑Authored‑By Claude YOK).

---

## 1) ŞU AN — Araştırma fazı (BEKLEME + HAZIRLIK)
- [x] #3 karşılaştırma PDF'i alındı, metin çıkarıldı, isimlendirme düzene sokuldu (`arastirma/3-...pdf`).
- [x] #4 prompt'u yazıldı (`arastirma/4-turk-dilleri-tarih-sosyokultur-iliski.prompt.md`) — tarih/sosyokültür/ilişki + araştırmacı‑merkezi.
- [ ] **Kullanıcı:** #4 prompt'unu deepsearch'e ver → **büyük (40‑50 sayfa) tarih/ilişki PDF'ini** getir.
- [ ] (Opsiyonel, paralel) #3'ten yapısal veriyi (ses denklikleri, kognat setleri, paradigma şablonları, uzaklık yüzdeleri) **taslak JSON şemasına** dönüştürme notları çıkar — kodlamadan, sadece tasarım.

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
