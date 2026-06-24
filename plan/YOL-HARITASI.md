# YOL HARİTASI — Fazlı Plan (kullanıcı notları + deepsearch bulguları)

> Her madde: **ne / yapar mıyız (gerekçe) / nasıl / bağımlılık / ❓açık soru**. "Yatay ölçek + eğitim portalı" en sonda (`GELECEK-PLANLAR.md`). Bu dosya, fikirler netleştikçe güncellenir; karar verilenler ✅, beklemedekiler ⏳.

---

## FAZ 1 — Yakın kalite (mevcut MVP'yi akademik-mükemmel yap) — ÖNCE BU
Çekirdek morfoloji + karşılaştırma zaten çalışıyor; bu faz onu "%100 doğru / paper-hazır" yapar.

### 1.1 ⏳ Füzyonel ek ince-ayrışması (NW kanonik-allomorf tek-hizalama) — ★ yüksek değer
- **Ne:** chv `-не`, uig `lir`, sah oblik-gövde gibi kaynaşık ekleri ŞU AN tek kaynaşık ek bırakıyoruz (yeniden-üretim %93 ama tam ayrışma değil). Deepsearch (5c) bunların **gerçek portmanteau OLMADIĞINI** kanıtladı: chv -не = +i(iyelik)+**n**(epentez)+e(hâl); uig lär+i (ä→i daralması); **bölünebilir.**
- **Yapar mıyız:** EVET — paper'ın morfoloji çekirdeğini güçlendirir, Çuvaşçayı derinleştirir.
- **Nasıl:** deepsearch'ün önerdiği yöntem — "lemma + KANONİK allomorf dizisi" vs yüzey TEK Needleman-Wunsch hizalaması; dile-özgü maliyet matrisi (uig ä→i = 0 ceza; chv epentetik н = 0 gap). Kanonik allomorf dizileri apertium `.twol` dosyalarından + dilbilgisinden. **chv morfotaktik sırası farklı: Kök+İyelik+Çoğul+Hâl** (ortak Türkçe Kök+Çoğul+İyelik+Hâl değil) — kümülatif seviyelerimizi chv için bu sıraya göre düzelt.
- **❓Soru:** bunu (a) deepsearch'teki örneklerle elle-kanonik-tablo kurarak mı, yoksa (b) önce ayrı bir "kanonik allomorf çıkarımı" deepsearch'i ile mi yapalım? (100% doğruluk kritik.)

### 1.2 ⏳ Ses denklikleri DİNAMİK + kanıtlı (kullanıcının (b) isteği) — ★
- **Ne:** Karşılaştır'daki "ses denklikleri" şu an statik 4 Çuvaş kuralı (rotasizm r↔z…) + elle örnekler; seçilen kognatla bağlı değil.
- **Yapar mıyız:** EVET, ama **akademik kesinlikle.** Kurallar (rotasizm/lambdasizm) Türkoloji ders-kitabı OLGULARI (100% doğru) — bunları algoritma "icat etmemeli". Doğru yaklaşım: kuralları **kendi Savelyev kognat verimizden KANITLA** (her kurala N kognat çifti göster) + seçilen kognatı ilgili kurala BAĞLA + istatistik.
- **Nasıl:** Savelyev kognat setlerinde Çuvaşça biçim ↔ ortak-Türkçe biçim hizala; her bilinen kurala uyan çiftleri say/göster ("rotasizm: 40 kognat çiftinde doğrulandı"). LingPy / correspondence-pattern literatürü (deepsearch 5c ref [23]).
- **❓Soru (KRİTİK):** yaklaşım — **(A) kanıt-destekli yerleşik kurallar** (öneri, akademik-güvenli) / **(B) saf veri-çıkarımı** (daha "yeni" ama spürios risk) / **(C) melez** (yerleşik + dikkatli yeni kol-çifti çıkarımı)? Ve bunun için ayrı deepsearch ister misin?

### 1.3 ⏳ Soy ağacı + Harita UX iyileştirmesi (kullanıcı notu)
- **Ne:** Haritada **Türkiye boşlukta** duruyor gibi; dile tıklayınca **direkt sayfa değiştirmek yerine** o sayfada (yan panel/popover) bilgi açılması daha kaliteli.
- **Yapar mıyız:** EVET, küçük-orta UI işi, kalite artışı net.
- **Nasıl:** harita projeksiyonunu düzelt (Türkiye konumu/etiketi); düğüme tıkla → inline kart (profil özeti + "tam profile git" linki), navigasyon yerine. Soy ağacı interaktif (dal tıkla → vurgu).
- **❓Soru:** harita gerçek coğrafi projeksiyon mu kalsın yoksa şematik mi; inline panel mı popover mı?

---

## FAZ 2 — Yeni modüller (araştırmacı değeri; deepsearch SONRASI)

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

## Karar günlüğü (kullanıcı onayladıkça doldur)
- Faz 1.1 füzyonel ayrışma yöntemi: ❓
- Faz 1.2 ses denklikleri yaklaşımı (A/B/C): ❓
- Faz 2.2 ekosistem bölümü kapsam/yer: ❓
- Faz 3.1 Çuvaşça sayfası: ❓
