# YOL HARİTASI — Fazlı Plan (kullanıcı notları + deepsearch bulguları)

> Her madde: **ne / yapar mıyız (gerekçe) / nasıl / bağımlılık / ❓açık soru**. "Yatay ölçek + eğitim portalı" en sonda (`GELECEK-PLANLAR.md`). Bu dosya, fikirler netleştikçe güncellenir; karar verilenler ✅, beklemedekiler ⏳.

## ★ DEEPSEARCH İHTİYAÇ HARİTASI (hangi iş hangi deepsearch'i bekler)
Promptlar `arastirma/`'da; sonuçlar geldikçe locale çekip işleriz.
| İş | Deepsearch | Durum |
|---|---|---|
| **Faz 1.1 füzyonel ayrışma** | **GEREKMEZ** — `5c` (_morfoloji_plani) zaten yöntemi+örnekleri verdi | hazır, yapılabilir |
| Faz 1.3 harita/soy-ağacı UX | gerekmez (saf UI) | hazır |
| Faz 1.4 Hakkında/iletişim | gerekmez | hazır |
| Faz 2.1 TTS | `6` (TTS/ASR) | ✅✅ **YAPILDI** — profillere "Seslendirme (TTS/ASR)" bölümü (`profiles_tts.json`); gerçek motor = gelecek altyapı |
| Faz 2.2 LLM/HF ekosistem | `7` (LLM/NLP/HF) | ✅✅ **YAPILDI** — Araştırmacı Merkezi'ne "Dil × yetenek envanteri" matrisi + 8 org (`ecosystem.json`); nötr (olgunluk yargısı yok) |
| Faz 2.5 Kollar açıklayıcı | `8` (sınıflandırma çerçevesi) | ✅✅ **YAPILDI** — sonuç işlendi, Tarih & Köken'e "altı kol" kartı + Bayes soy ağacı |
| Faz 2.6 Derin dil profilleri | `9` (kol-bazlı batch A-E) | ✅✅ **YAPILDI** — 14 dil derin profil işlendi (`profiles_deep.json`) + Joshi çapraz-kontrol düzeltmeleri |
| **Kaynaklar büyük güncelleme** | TÜM deepsearch'ler (5,5b,5c,6,7,8,9) sonrası | bekliyor |
> **Özet:** Şimdi deepsearch beklemeden **Faz 1.1 / 1.3 / 1.4** yapılabilir. Faz 2+ ve içerik/kaynak işleri deepsearch sonuçlarını bekler.

---

## FAZ 1 — Yakın kalite (mevcut MVP'yi akademik-mükemmel yap) — ÖNCE BU
Çekirdek morfoloji + karşılaştırma zaten çalışıyor; bu faz onu "%100 doğru / paper-hazır" yapar.

### 1.1 🔶 Füzyonel ek ince-ayrışması — KISMİ (Çuvaş SIRA ✅ yapıldı; kanonik-allomorf füzyon-bölme ⏳ sırada)
- **✅ Yapıldı (Çuvaş morfotaktik sıra):** deepsearch 5c'nin dediği gibi chv sırası Kök+İyelik+Çoğul (px<pl) — apertium-chv yalnız `<px><pl>` üretir; `_segment_align`'a dile-duyarlı slot sırası eklendi → `хӗррӗмсем` artık `хӗр+рӗм+сем`. Basit çoğul/hâl bozulmadı. (`app.py: _segment_align(lang)`.)
- **⏳ Kalan (kanonik-allomorf füzyon-bölme) — DİKKATLİ:** chv `-не`/uig `lir`/sah oblik-gövde gibi kaynaşık ekleri ALT-morfeme bölme. Yöntem (5c): "lemma + KANONİK allomorf dizisi" vs yüzey TEK NW; dile-özgü 0-ceza (uig ä→i; chv epentetik н). **100% doğruluk için** kanonik allomorf tabloları (chv px3sg -ĕ/-i + dat -e/-a + epentez n; uig -lär/-im) gramer kaynağıyla doğrulanmalı → bu yüzden aceleye getirilmedi.
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

### 2.1 ✅ Seslendirme (TTS/ASR) — ekosistem/boşluk haritası YAPILDI (deepsearch 6, 25 Haz)
- **Ne yapıldı (içerik katmanı):** Dil Profilleri'ne **"Seslendirme (TTS/ASR)" 5. bölümü** (`platform/data/profiles_tts.json`) — 14 dil × açık model + lisans + kalite + boşluk (Piper/MIT, Meta MMS-TTS/CC-BY-NC, ISSAI Spark/TatarTTS, eSpeak NG; Common Voice saatleri, WER). Çuvaşça TTS boşluğu ve yüksek ASR WER'leri dürüstçe gösterildi (dijital kapsayıcılık misyonu).
- **★ KALAN (gerçek motor entegrasyonu = gelecek ALTYAPI işi):** "▷ Seslendir" hâlâ tarayıcı Web Speech'e düşüyor. Raporun önerdiği mimari: **Dinamik Hibrit Yönlendirme** — tr/kaz → sunucu Piper(ONNX); uzb/uig/sah → HF Inference API (MMS-TTS, ön-işlem: Latin→Kiril, num2words); chv/bak → tarayıcı eSpeak NG (WASM, espeakng.js). ASR telaffuz kontrolü yalnız tr/kaz (Whisper); chv/sah WER yüksek → ertelendi. Bu altyapı ayrı bir mühendislik fazıdır.

### 2.2 ✅✅ Türk Dilleri NLP/LLM Ekosistemi — YAPILDI + YENİDEN TASARLANDI (deepsearch 7 + web, 25 Haz)
- **v1 (matris) kullanıcı tarafından yetersiz bulundu** (durağan tek isim, link yok, Zemberek/Apertium atlanmış) → **v2 YENİDEN:** ayrı **"Ekosistem" sayfası** (sol menü ARAŞTIR). **Kategori-önce → dil-içinde → DOĞRUDAN bağlantı launchpad'i.**
- **8 kategori, 101 bağlantı** (`platform/data/ecosystem.json`): Üretken LLM · Encoder/temsil · ASR · TTS · Veri setleri · Benchmark · **Araçlar (Apertium·Zemberek·TRmorph·Zeyrek·Stanza·TurkicNLP)** · Organizasyonlar. Her kategoride **hub** linkleri (HF arama+leaderboard+awesome-liste) + dil-bazlı 1-5 öne çıkan model/veri/araç linki (↗ yeni sekme, `target=_blank`).
- **Kaynak:** deepsearch 7 (gerçek HF repoları) + **kendi web araştırmam** (WebSearch: Zemberek/TRmorph/zeyrek/Starlang, agmmnn/turkish-nlp-resources, OpenLLM-TR & Türkçe-MMLU leaderboard doğrulandı). Uydurma link yok; nötr (olgunluk yargısı yok).
- build.py: matris Araştırmacı Merkezi'nden kaldırıldı (sade sorgu/API'ye döndü); yeni `eco` ekranı + nav + isEco + anchor-jump kategori navı; USAGE'a Ekosistem modülü. Claude_Preview ✅.
- **★ ZENGİNLEŞTİRME (opsiyonel, hazır):** `arastirma/10-ekosistem-derin-linkli.prompt.md` — kategori-yapılı, link+indirme-sayısı talepli, HF-dışı dahil maks-kapsam deepsearch promptu. + ileride HfApi CRON otomatik güncel-tutma (ayrı altyapı).
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

### 2.5 ✅✅ "Türk dilleri kolları NEDİR" açıklayıcı — YAPILDI (deepsearch 8 işlendi, 25 Haz)
- **Ne yapıldı:** "Tarih & Köken" ekranına **"Türk dillerinin altı kolu"** kartı (zaman çizelgesinin üstüne) — 6 Johanson kolu, her biri: pedagojik tanım + ayırt edici izogloss (rotasizm/lambdasizm, *h-, *-d-, *-G, *y-) + örnek kelime + bölge/tarih etiketi. Kart başlığında Johanson "altın standart" + Savelyev & Robbeets (2020) Bayes doğrulaması atfı.
- **+ Soy ağacı (Karşılaştır):** basit 5-satırlık ağaç → **Bayes Maximum Credibility Tree** topolojisine güncellendi (14 düğüm: Proto-Türkçe→Oğur/Genel Türkçe→Kuzey Sibirya, Çekirdek→Güney Sibirya, Makro GB-Doğu→Halaç-Salar, Merkezî→Oğuz/Makro-Kıpçak→Karluk/Kıpçak); mutlak tarihler ~MÖ 66 (Oğur) / ~MS 474 (Kuzey Sibirya).
- **Karar (uygulandı):** ayrı sol-menü değil → **mevcut "Tarih & Köken" ekranına** girdi (kullanıcı kararı). Kaynak: `_siniflandirma.txt` (deepsearch 8); 6-kol etiketimiz "altın standart Johanson modeli" olarak teyit edildi.
- **Deepsearch 8'in işlenmemiş düzeltme önerileri (ileride):** Salarca→Oğuz'da [Areal:Amdo] meta-etiket; Sarı Uygurca→Karluk değil G.Sibirya; Kırım Tatarcası→geçişken (Kıpçak ana+Oğuz temas); kognat motoruna izogloss RegEx kuralları.

### 2.6 ✅✅ Derin dil profilleri — YAPILDI (deepsearch 9.1-9.5 işlendi, 25 Haz)
- **Ne yapıldı:** 14 displayed dil için **derin profil** (`platform/data/profiles_deep.json`) → Dil Profilleri ekranında 4 bölüm: **Tarih · Yapı & özgünlük · İlişkiler · Dijital güç**. Her bölüm atıflı (Glottolog/Ethnologue/UNESCO + Wikipedia/Grokipedia/ACL/apertium-wiki/HF), uydurma yok. build.py `DEEPPROF` enjeksiyonu + `profileSel.deep` birleşimi; not paragrafının altına bölümlü render.
- **★ Verimizi TEST etti (çapraz-kontrol düzeltmeleri uygulandı):** Joshi sınıfı deepsearch 9 ile hizalandı — **az 1→2-3, kk 2-3→3 (yükselen), tt 2-3→1, ug 2-3→1, tyv 0→1, kjh 0→1** (eski değerler deepsearch 5 envanterindendi; 9 daha ayrıntılı/dil-bazlı). Çuvaş morfotaktik sıra, demografi (740K), EGIDS 6b — hepsi teyitli, tutarsızlık yok.
- **İŞLENMEMİŞ kalan deepsearch 9 dilleri (displayed dışı, ileride yatay ölçek):** gag, crh, slr, kmz (Oğuz); kaa, krc, kum, nog (Kıpçak); uzb, aib(Eynu), ili (Karluk); alt, dlg, ybe, fuyu (Sibirya) — metinler `_profil_*.txt`'de hazır.
- **Kalan profil işleri:** deepsearch 8'in düzeltme önerileri (Sarı Uygurca→G.Sibirya kol etiketi, Kırım Tatarcası geçişken, Salarca areal) + her dile birincil ürün/avantaj-dezavantaj alanı (opsiyonel derinleştirme).

### 2.7 ✅ KAYNAKLAR güncelleme — YAPILDI (25 Haz)
- **Ne yapıldı:** Uygulama içi **"Kaynaklar & Lisanslar"** (SOURCES + USAGE) ekranına 3 yeni künye: **`bayes`** (Savelyev & Robbeets 2020 + Johanson tasnifi → Tarih & Köken), **`hf`** (HuggingFace ekosistemi → Dil Profilleri + Araştırmacı), **`deepds`** (KÖKEN derin araştırmalar 5–9 → Dil Profilleri + Araştırmacı). USAGE eşlemesi güncellendi (Tarih & Köken'e bayes+cldf; Profiller/Araştırmacı'ya hf+deepds). `demo` zaten kaldırılmıştı.
- **+ `KAYNAKLAR.md` defteri:** kaynak tablosuna bayes/hf/deepds satırları; veri-ürünleri tablosuna `profiles_deep.json` / `profiles_tts.json` / `ecosystem.json`; tarih 25 Haz.
- **Not (ileride):** UD ağaçbank-bazlı lisans ayrımı + her deepsearch'in tam kaynakça URL listesi (akademik ek) henüz işlenmedi — paper aşamasında genişletilebilir.

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
- **Faz 2.5 kollar açıklayıcı:** ✅ **deepsearch 8 sonrası, Tarih & Köken'i BAŞTAN kurarken orada** (ayrı menü değil).
- **Faz 1.3 harita:** ✅ **gerçek dünya haritası DEĞİL** — mevcut tatlı/akademik ŞEMATİK duruşu KORU, ama dil konumlarını + dünya şeklini **gerçeğe daha yakın** yap (kalite+tutarlılık). İnline kart (tıkla→sayfa değiştirme yerine).
- **ŞİMDİ:** ✅ Faz **1.1 füzyonel ayrışma** (kullanıcı seçti).
- **Faz 3.1 Çuvaşça "Dilin Kalbi":** ✅ AYRI anlatı sayfası (onaylı; Saha/Şor için de şablon).
