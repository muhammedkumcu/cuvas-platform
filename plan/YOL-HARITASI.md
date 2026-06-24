# YOL HARİTASI — Fazlı Plan (kullanıcı notları + deepsearch bulguları)

> Her madde: **ne / yapar mıyız (gerekçe) / nasıl / bağımlılık / ❓açık soru**. "Yatay ölçek + eğitim portalı" en sonda (`GELECEK-PLANLAR.md`). Bu dosya, fikirler netleştikçe güncellenir; karar verilenler ✅, beklemedekiler ⏳.

## ★ DEEPSEARCH İHTİYAÇ HARİTASI (hangi iş hangi deepsearch'i bekler)
Promptlar `arastirma/`'da; sonuçlar geldikçe locale çekip işleriz.
| İş | Deepsearch | Durum |
|---|---|---|
| **Faz 1.1 füzyonel ayrışma** | **GEREKMEZ** — `5c` (_morfoloji_plani) zaten yöntemi+örnekleri verdi | hazır, yapılabilir |
| Faz 1.3 harita/soy-ağacı UX | gerekmez (saf UI) | hazır |
| Faz 1.4 Hakkında/iletişim | gerekmez | hazır |
| Faz 2.1 TTS | `6` (TTS/ASR) | prompt hazır, sonuç bekleniyor |
| Faz 2.2 LLM/HF ekosistem | `7` (LLM/NLP/HF) | prompt hazır, sonuç bekleniyor |
| Faz 2.5 Kollar açıklayıcı | `8` (sınıflandırma çerçevesi) | prompt hazır |
| Faz 2.6 Derin dil profilleri | `9` (kol-bazlı batch A-E) | prompt hazır |
| **Kaynaklar büyük güncelleme** | TÜM deepsearch'ler (5,5b,5c,6,7,8,9) sonrası | bekliyor |
> **Özet:** Şimdi deepsearch beklemeden **Faz 1.1 / 1.3 / 1.4** yapılabilir. Faz 2+ ve içerik/kaynak işleri deepsearch sonuçlarını bekler.

---

## FAZ 1 — Yakın kalite (mevcut MVP'yi akademik-mükemmel yap) — ÖNCE BU
Çekirdek morfoloji + karşılaştırma zaten çalışıyor; bu faz onu "%100 doğru / paper-hazır" yapar.

### 1.1 ⏳ Füzyonel ek ince-ayrışması (NW kanonik-allomorf tek-hizalama) — ★ yüksek değer
- **Ne:** chv `-не`, uig `lir`, sah oblik-gövde gibi kaynaşık ekleri ŞU AN tek kaynaşık ek bırakıyoruz (yeniden-üretim %93 ama tam ayrışma değil). Deepsearch (5c) bunların **gerçek portmanteau OLMADIĞINI** kanıtladı: chv -не = +i(iyelik)+**n**(epentez)+e(hâl); uig lär+i (ä→i daralması); **bölünebilir.**
- **Yapar mıyız:** EVET — paper'ın morfoloji çekirdeğini güçlendirir, Çuvaşçayı derinleştirir.
- **Nasıl:** deepsearch'ün önerdiği yöntem — "lemma + KANONİK allomorf dizisi" vs yüzey TEK Needleman-Wunsch hizalaması; dile-özgü maliyet matrisi (uig ä→i = 0 ceza; chv epentetik н = 0 gap). Kanonik allomorf dizileri apertium `.twol` dosyalarından + dilbilgisinden. **chv morfotaktik sırası farklı: Kök+İyelik+Çoğul+Hâl** (ortak Türkçe Kök+Çoğul+İyelik+Hâl değil) — kümülatif seviyelerimizi chv için bu sıraya göre düzelt.
- **❓Soru:** bunu (a) deepsearch'teki örneklerle elle-kanonik-tablo kurarak mı, yoksa (b) önce ayrı bir "kanonik allomorf çıkarımı" deepsearch'i ile mi yapalım? (100% doğruluk kritik.)

### 1.2 ✅ Ses denklikleri KANIT-DESTEKLİ + kognata bağlı (kullanıcının (b) isteği) — YAPILDI
- **Ne:** Karşılaştır'daki "ses denklikleri" şu an statik 4 Çuvaş kuralı (rotasizm r↔z…) + elle örnekler; seçilen kognatla bağlı değil.
- **Yapar mıyız:** EVET, ama **akademik kesinlikle.** Kurallar (rotasizm/lambdasizm) Türkoloji ders-kitabı OLGULARI (100% doğru) — bunları algoritma "icat etmemeli". Doğru yaklaşım: kuralları **kendi Savelyev kognat verimizden KANITLA** (her kurala N kognat çifti göster) + seçilen kognatı ilgili kurala BAĞLA + istatistik.
- **✅ Yapıldı:** Karşılaştır > Ses denklikleri'ndeki 4 kural artık **SavelyevTurkic kognat verisinden kanıtlı** (proto-fonem temelli: rotasizm 36 *ŕ, lambdasizm 29 *ĺ, baş y->ś 14 çift). Kognat ağında bir kelime seçip "ses denkliklerinde incele" → o kelimenin örneklediği kural OTOMATİK vurgulanır (güvenli tespit: proto-fonem + Çuvaşça yüzey çıktısı). `build.py: sound_evidence()` + `build_cognates ruleIdx`.
- **Açık (sonra):** vurgulanan kural için seçili kognatın verideki destek çiftlerini de listelemek; diğer kol-çifti denklikleri (Kıpçak↔Oğuz) — yatay.

### 1.3 ⏳ Soy ağacı + Harita UX iyileştirmesi (kullanıcı notu)
- **Ne:** Haritada **Türkiye boşlukta** duruyor gibi; dile tıklayınca **direkt sayfa değiştirmek yerine** o sayfada (yan panel/popover) bilgi açılması daha kaliteli.
- **Yapar mıyız:** EVET, küçük-orta UI işi, kalite artışı net.
- **Nasıl:** harita projeksiyonunu düzelt (Türkiye konumu/etiketi); düğüme tıkla → inline kart (profil özeti + "tam profile git" linki), navigasyon yerine. Soy ağacı interaktif (dal tıkla → vurgu).
- **❓Soru:** harita gerçek coğrafi projeksiyon mu kalsın yoksa şematik mi; inline panel mı popover mı?

### 1.4 ⏳ "Hakkında" + iletişim (kullanıcı notu)
- **Ne:** Platformun amacı/felsefesi/ekibi/kaynak-ilkesi + iletişim (e-posta/GitHub) — sol menüde "Hakkında".
- **Yapar mıyız:** EVET, küçük, akademik ciddiyet + iletişim için gerekli. Deepsearch gerekmez.
- **Nasıl:** tek sayfa: misyon (çift kitle, dijital kapsayıcılık), metodoloji (gerçek kaynak/atıf/uydurma-yok), açık kaynak/lisans, ekip + iletişim. İletişim bu sayfanın içinde.

---

## FAZ 2 — Yeni modüller (araştırmacı + içerik değeri; deepsearch SONRASI)

### 2.1 ⏳ Doğru seslendirme (TTS) — her dil için (kullanıcı notu)
- **Ne:** "▷ Seslendir" şu an tarayıcı Web Speech'e düşüyor → çoğu Türk dilini desteklemiyor/yanlış. Dil-başına doğru TTS lazım.
- **Yapar mıyız:** EVET (öğrenci + araştırmacı değeri). **Deepsearch hazırlandı: `arastirma/6-seslendirme-tts-asr...`** (MMS-TTS, Coqui, Piper, espeak; dürüst boşluk: Çuvaşça TTS var mı?).
- **Nasıl:** deepsearch sonucu → dil→model yönlendirme; sunucu yerel / HF API / tarayıcı-WASM kararı.
- **Bağımlılık:** deepsearch 6 sonucu.

### 2.2 ⏳ Türk Dilleri NLP/LLM Ekosistemi bölümü (kullanıcı notu — ★ büyük)
- **Ne:** HF + literatürde Türk dilleri için ne varsa (LLM, dataset, ASR/STT/TTS, benchmark, org'lar; örn. TurkmedSTT) gösteren, eksik/gelişmişliği işaretleyen **araştırmacı hub'ı**. Vizyonun "ilk uğrak" ayağıyla birebir.
- **Yapar mıyız:** EVET — bu, platformu salt morfolojiden "Türk dil dünyası araştırma merkezi"ne taşır. **Çok detaylı deepsearch hazırlandı: `arastirma/7-...llm-nlp-hf-ekosistemi`.**
- **Nasıl:** dil × yetenek (LLM/dataset/ASR/TTS/benchmark) matrisi + her hücre künye+HF linki+lisans + boşluk haritası. Joshi kaynak-sınıfıyla bütünleşir.
- **❓Soru:** ne kadar belirgin/kapsamlı — ayrı ana-menü modülü mü, Araştırmacı Merkezi içinde mi? Güncel tutma: HF API ile otomatik çekme mi, periyodik manuel mi?

### 2.3 ⏳ Güncellik / haberler katmanı (kullanıcı notu)
- **Ne:** "yeni ne çıktı" — yeni model/dataset/makale duyuruları, dil dünyası haberleri; platformun canlı/güncel hissi.
- **Yapar mıyız:** muhtemelen EVET ama **sürdürülebilirlik şüphesi** (kim/ne güncelleyecek?).
- **Nasıl (seçenekler):** (i) HF API'den org/model son-güncelleme çekme (otomatik, dar); (ii) seçili RSS/kaynak akışı; (iii) elle küratörlü "değişiklik günlüğü". 
- **❓Soru:** otomatik mi (dar ama sürdürülebilir) yoksa küratörlü mü (zengin ama emek)? Öncelik düşük mü?

### 2.4 ⏳ Apertium-üstü çalışmalar / güncel literatür taraması (kullanıcı notu)
- **Ne:** apertium üzerine inşa edilenler (apertium-extra vb.) + literatürde koyabileceğimiz en güncel işler.
- **Yapar mıyız:** araştırma kalemi — kısmen `5`/`5b`/`7` deepsearch'leriyle örtüşür.
- **Nasıl:** mevcut envanter deepsearch'lerine ekle; çıkanları ekosistem bölümüne (2.2) yerleştir.

### 2.5 ⏳ "Türk dilleri kolları NEDİR" açıklayıcı kategorisi (kullanıcı notu) — ★
- **Ne:** Oğuz/Kıpçak/Karluk/Sibirya/Oğur/Argu kollarını **herkesin anlayacağı dilde + diyagram/şablonla** anlatan, sol menüde ayrı bir açıklayıcı bölüm. ("Bunları anlatmak bu platformun görevidir.")
- **Yapar mıyız:** EVET — vizyonun pedagoji + "ilk uğrak" ayağıyla birebir; çocuk eğitim portalının da temeli.
- **Nasıl:** her kol için sade tanım + tanımlayıcı izogloss (örn. Ogur=rotasizm) + örnek kelime + interaktif soy ağacı diyagramı. **Deepsearch `8` (sınıflandırma çerçevesi)** verisiyle.
- **❓Soru:** ayrı sol-menü kategorisi mi, yoksa mevcut "Tarih & Köken" / "Dil Profilleri" içine mi? (Mevcut Tarih & Köken + Karşılaştır>Soy ağacı kısmen var.)

### 2.6 ⏳ Derin dil profillerini doldurma (kullanıcı notu — çok detaylı deepsearch)
- **Ne:** Her dilin tarihi, yapısı, ilişkileri, dijital gücü, apertium/NLP varlığı/ürün/avantaj/dezavantaj — kapsamlı, atıflı profiller; hem modülleri DOLDURUR hem verimizi TEST eder (doğruluk/eksik/tutarlılık).
- **Yapar mıyız:** EVET — akademik ciddiyet + kaynağa bağlılık için omurga.
- **Nasıl:** **Deepsearch `9` (kol-bazlı batch A-E; her batch ayrı çalıştır)** → çıktıları locale çek, çapraz-kontrol, profiller/tarih/ekosistem modüllerine işle. + **Deepsearch `8`** çerçevesi.

### 2.7 ⏳ KAYNAKLAR büyük güncelleme (kullanıcı notu) — ★ tüm deepsearch'ler sonrası
- **Ne:** Platformda her yerde geçen kaynak künyelerini + "Kaynaklar & Lisanslar" bölümünü **baştan, eksiksiz** güncelle (tüm deepsearch'lerin kaynakçaları + locale çekilen yeni veriler).
- **Yapar mıyız:** EVET — "hiçbir veri kaynaksız değildir" ilkesi; akademik dürüstlüğün vitrini.
- **Nasıl:** 5,5b,5c,6,7,8,9 sonuçları geldikçe her birinin kaynakçasını `KAYNAKLAR.md` + UI Kaynaklar bölümüne işle; her modülün kullandığı kaynağı doğrula/güncelle.
- **Bağımlılık:** TÜM deepsearch'ler.

---

## FAZ 3 — Çuvaşça derinlik ("dilin kalbi") — brainstorm

### 3.1 ⏳ Çuvaşça "Dilin Kalbi" sayfası (kullanıcı fikri)
- **Ne:** Çekirdek dilimiz Çuvaşçaya özel, derin bir sayfa — Ogur kolu hikâyesi, ses kanunları (kanıtlı, 1.2 ile), tarihçe (İdil Bulgar, Aşmarin), canlılık, örnek paradigmalar, kognat ağı, "neden bu dil paha biçilmez".
- **Yapar mıyız:** ❓ kullanıcı "üzerine düşünürüz" dedi. **Benim görüşüm:** EVET değerli — misyonun (tehlikedeki dile derinlik) somut vitrini + paper için güçlü vaka çalışması. Mevcut modülleri (profil+kognat+ses+tarih) Çuvaşça için tek "anlatı" sayfasında birleştirir.
- **❓Soru:** ayrı özel sayfa mı (anlatı/hikâye akışı) yoksa mevcut Çuvaşça içeriğini derinleştirmek mi yeterli? Diğer tehlikedeki diller (Saha, Şor) için de şablon olur mu?

---

## FAZ 4 — Yatay ölçek + Eğitim portalı
`GELECEK-PLANLAR.md`'ye bak (tüm ~20 dil + tam veri açma + çocuk/öğrenci eğitim portalı). Bu fazlar EN SON.

---

## Karar günlüğü (kullanıcı kararları)
- **Faz 1.2 ses denklikleri:** ✅ **(A) Kanıt-destekli yerleşik kurallar** — kurallar ground truth, Savelyev verisinden KANITLA + kognatı kurala bağla. (Saf çıkarım reddedildi: spürios riski.)
- **Faz 1.1 + 1.2 ayrı deepsearch:** ✅ HAYIR — eldeki 5c + Savelyev ile dikkatlice ilerle.
- **Faz 2.2 ekosistem yeri:** ⏳ deepsearch 7 sonucu gelince karar.
- **Faz 2.5 kollar açıklayıcı yeri:** ❓ ayrı sol-menü kategorisi mi / Tarih & Köken içine mi?
- **Faz 1.3 harita:** ❓ gerçek coğrafi mi / şematik mi; inline panel mı popover mı?
- **Faz 3.1 Çuvaşça "Dilin Kalbi":** ✅ AYRI anlatı sayfası (onaylı; Saha/Şor için de şablon).
