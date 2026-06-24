# DEEP RESEARCH PROMPT — Türk Dilleri Açık Kaynak NLP / Hesaplamalı Dilbilim Envanteri

> **Amaç (KÖKEN platformu için):** ~20 Türk dilinin her biri için **açık kaynak / açık erişimli** tüm hesaplamalı dilbilim araç ve kaynaklarını tek bir yerde, **olgunluk ve eksiklikleriyle** haritalamak. Çıktı; (a) platformun arkasına hangi motorları takacağımızı (örn. Türkçe için Zemberek, ötekiler için apertium ve dile özgü ne varsa) belirleyecek, (b) araştırmacılara "bu dilde ne var, ne yok, ne kadar olgun" diye gösterilecek envanterin temeli olacak. **Bu platform, Türk dillerine ait açık kaynak literatürü/araçları araştırmacılara tek elden gösteren, eksik/gelişmişliği işaretleyen, ilham veren bir laboratuvar olmayı hedefler — bu araştırma onun omurgasıdır.**

## Kapsanacak diller (en az)
Türkçe, Azerbaycanca (kuzey/güney), Türkmence, Gagavuzca, Kırım Tatarcası, Tatarca, Başkurtça, Kazakça, Kırgızca, Karakalpakça, Karaçay-Balkarca, Kumukça, Nogayca, Özbekçe, Uygurca, Altayca, Hakasça, Tuvaca, Şorca, Saha (Yakut), Çuvaşça, Halaçça. (Daha küçük/tehlikedeki üyeler de: Salar, Fu-yü Kırgızcası, Dolganca vb. — bulunursa ekle.)

## Her dil için istenen başlıklar (tablo + kısa değerlendirme)
1. **Morfolojik analizör / üretici** (FST veya kural/istatistik): apertium, HFST, Zemberek (TR), TRmorph (TR), Giella/GiellaLT, UniParser/uniparser-morph, Apertium-`xxx`, Helsinki FSTs, vb. → **kapsam (lemma/etiket/yüzey-bölümleme verebiliyor mu?), lisans, bakım durumu (son commit), depo linki, bilinen doğruluk/değerlendirme**.
2. **Stemmer / lemmatizer / POS etiketleyici / bağımlılık ayrıştırıcı (parser)**: Universal Dependencies ağaç bankaları (hangi diller, boyut, lisans), Stanza/UDPipe/spaCy modeli var mı.
3. **Sözlükler / sözvarlığı kaynakları**: Wiktionary kapsamı, UniMorph, lexibank/CLDF (SavelyevTurkic vb.), Apertium iki-dilli sözlükler, açık tarihsel/etimolojik sözlükler (Clauson, Räsänen, VEWT, EDAL — açık mı?), Çuvaş için Aşmarin (dijital mi?).
4. **Korpuslar**: tek-dilli (boyut, lisans, indirilebilir mi), **paralel** korpuslar (OPUS, hangi çiftler), tarihsel/yazıt korpusları (Orhun, Eski Uygur, TİTUS, VATEC), konuşma korpusları.
5. **Gömme / dil modelleri (LLM)**: fastText/word2vec (hangi diller), çok-dilli LLM kapsamı (mBERT, XLM-R, BLOOM, mT5 — Türk dilleri dahil mi), **Türkçe/Türk dilleri özel açık modeller** (BERTurk, TURNA, Trendyol, Kanarya, mukayese; diğer diller için kazakh/uzbek/tatar BERT'leri vb.), açık ASR/TTS (Whisper kapsamı, Common Voice hangi diller, Coqui/MMS).
6. **Çeviri (MT)**: Apertium dil çiftleri (hangi Türk dili çiftleri var, olgunluk), açık NMT (NLLB-200 Türk dilleri kapsamı, OPUS-MT), **Türk dilleri arası** (sadece X↔Türkçe değil) ne var.
7. **Kognat / etimoloji / karşılaştırmalı veri**: SavelyevTurkic dışında açık kognat setleri, ses-denkliği kuralı veri setleri, proto-Türkçe rekonstrüksiyon kaynakları.
8. **Dijital canlılık / kaynak sınıfı**: Joshi ve ark. (2020) sınıfı (0–5), Glottolog AES, dilin "düşük-kaynak" derecesi; **somut eksik listesi** (örn. "bu dilde UD ağaç bankası YOK", "morfolojik analizör sadece kısmi").
9. **Araştırma ekosistemi**: ana araştırma grupları/laboratuvarlar, TurkLang / UBMK / Turkic-NLP atölyeleri, anahtar makaleler (son 5 yıl), düzenli güncellenen "awesome-turkic-nlp" tarzı listeler.

## Özellikle netleştirilmesi gereken karşılaştırmalar
- **Türkçe morfoloji: Zemberek vs Apertium vs TRmorph** — hangisi **yüzey bölümleme** (kök + ek hece ek hece) verir, hangisi sadece lemma+etiket? Lisans (Zemberek = Apache-2.0?), Java bağımlılığı, Python sarmalayıcı (zemberek-python) var mı, performans.
- **Yüzey morfem bölümleme** genel problemi: apertium gibi lemma+etiket veren sistemlerden **yüzey hecelerine** geçmenin açık yöntemleri (kümülatif üretim, FST'lerin segment-marker üreten sürümleri, morfessor/sentencepiece gibi denetimsiz yöntemler) — Türk dilleri için en sağlamı?
- **Diller arası eşdeğer bulma (live "diller arası" karşılaştırma için):** bir kelimeyi/lemma'yı tüm Türk dillerinde eşleştirmek için açık yollar — Apertium çeviri çiftleri zinciri, kognat veritabanı eşlemesi, çok-dilli sözlük (PanLex, Wiktionary), NLLB ile çeviri. Hangisi pratik + lisans-uygun?

## Çıktı biçimi
- Dil × yetenek **matrisi** (satır: dil, sütun: morfo-analizör / UD / korpus / embedding / ASR / MT / sözlük), her hücrede **var/kısmi/yok + en iyi açık araç + lisans**.
- Her araç için: **ad, depo/URL, lisans, bakım durumu, kapsam, KÖKEN'e entegre edilebilirlik notu**.
- "**Hızlı kazanımlar**" bölümü: KÖKEN'in MVP'sine hemen entegre edebileceği, olgun + uygun-lisanslı 5–10 araç/kaynak.
- "**Boşluk haritası**": araştırmacıya gösterilecek, dil başına en kritik eksikler.
- **Atıf + lisans** her kaynakta zorunlu; uydurma YOK, bulunamayan = "kaynak bulunamadı" yaz.

## İlke (KÖKEN metodolojisi)
PDF/özet değil; **gerçek depoları/veri setlerini** işaret et (URL), lisansı doğrula, mümkünse son commit/sürüm tarihini ver. Spekülasyon ile doğrulanmış bilgiyi ayır.
