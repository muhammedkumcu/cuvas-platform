# DEEP RESEARCH PROMPT (DAR/ODAKLI) — Yüzey Morfem Bölümleme + Diller-Arası Eşdeğer Bulma (Türk dilleri)

> **Bağlam:** KÖKEN platformunda apertium FST'leri kullanıyoruz. apertium **lemma + morfolojik etiket** veriyor (ör. `evlerde → ev<n><pl><loc>`) ve ses değişimini bile doğru çözüyor (`kitabımızda → kitap<n><px1pl><loc>`). İKİ somut mühendislik açığımız var; bu araştırma SADECE bu ikisini derinlemesine çözsün. Geniş envanter ayrı promptta (`5-...nlp-envanteri`); burada **dar ve uygulanabilir** cevap istiyoruz: hangi açık aracı/yöntemi, hangi lisansla, nasıl entegre ederiz.

## SORU 1 — Yüzey morfem bölümleme (kök + ek_hecesi + ek_hecesi …)
apertium lemma+etiket veriyor ama **yüzeydeki ek hecelerinin sınırını** (kitab|ımız|da → "ımız", "da") doğrudan vermiyor. Biz şu an kümülatif üretim+fark ile çıkarıyoruz; ses değişiminde yaklaşık kalıyor. İstenen:
1. **Her Türk dili için**, yüzey morfem bölümlemesi (segmentation) DOĞRUDAN veren açık kaynak araç var mı? Özellikle:
   - **Zemberek (Türkçe):** `WordAnalysis` çıktısı yüzey morfemlerini (surface forms of morphemes) veriyor mu? Hangi API (`analyzeAndDisambiguate`, `MorphologicalAnalysis.getMorphemeDataList` / `surfaceForm`)? Lisans (Apache-2.0?), Java↔Python köprüsü (`zemberek-python`, JPype), olgunluk.
   - **apertium/HFST:** FST'lerin **segment-marker** (örn. `+`/`>` ile morfem sınırı) üreten derlemesi mümkün mü? `hfst-tokenize`, two-level kuralların ara temsili, `lexc/twol` kaynaklarından sınır çıkarma. Pratik mi?
   - **Giella / GiellaLT** Türk dilleri için (var mı, hangi diller), yüzey bölümleme veriyor mu.
   - **UniParser-morph, Apertium-`xxx`-segmenter, Morfessor / SentencePiece (denetimsiz)** — Türk dilleri için doğruluk/uygunluk.
2. **Genel yöntem:** lemma+etiket veren bir FST'den yüzey hece sınırına geçmenin **en sağlam açık yöntemi** nedir (kümülatif üretim+hizalama, FST inversion, çift-yönlü FST, allomorf tablosu)? Ses-değişimi (ünsüz yumuşaması, ünlü düşmesi, allomorfi) altında doğruluğu nasıl artırılır? Somut, uygulanabilir teknik öneri + varsa hazır kütüphane.
3. **Karar tablosu:** dil × {yüzey-bölümleme aracı var mı? / hangisi / lisans / Python'dan çağrılabilir mi}.

## SORU 2 — Diller-arası eşdeğer bulma ("diller arası" canlı karşılaştırma için)
KÖKEN'de bir kelime aratınca onu **tüm Türk dillerinde** göstermek istiyoruz (statik "okuduk" örneğindeki gibi: oku-du-k / oxu-du-q / uqı-dı-q…). apertium o yüzeyi sadece geçerli olduğu dilde tanır. Eşdeğeri bulmak için açık yollar:
1. **Kök/lemma çapraz-dil eşlemesi (tercih edilen yön):** bir lemma'yı (ör. `oku`) tüm Türk dillerindeki karşılığına (`oxu, uqı, oqı, oqı, oqu…`) eşleyen **açık** kaynak hangisi? Aday: **Apertium iki-dilli sözlükler** (`apertium-tur-aze` vb. `.dix`), **PanLex**, **Wiktionary/Wikidata lexemes**, **lexibank/CLDF (SavelyevTurkic) kognat setleri**, **PanLex/Concepticon**. Her birinin Türk dilleri kapsamı, lisansı, kök-düzeyi eşleme kalitesi.
2. **Yöntem:** "kaynak dilde çöz (lemma+etiket) → lemmayı hedef dile eşle → aynı etiketleri hedef dilde ÜRET" boru hattı pratik mi? Hangi diller arası tam zincir kurulabilir (apertium üretici + iki-dilli sözlük mevcudiyeti matrisi)?
3. **Alternatif — çeviri:** NLLB-200 / OPUS-MT / Apertium çiftleri ile kelime/biçim çevirisi; Türk dilleri arası (sadece X↔Türkçe değil) kapsam ve kalite; lisans.
4. **Karar:** KÖKEN için **en uygulanabilir + açık-lisanslı** diller-arası eşleme stratejisi; "hızlı kurulabilir" zincir(ler) hangileri.

## Çıktı
- Her iki soru için **net, uygulanabilir öneri** + **karar tablosu** + her araç/kaynağın **lisans + depo/URL + Python'dan kullanılabilirlik** notu.
- "Hemen yapılabilir" vs "araştırma gerektirir" ayrımı.
- Atıf zorunlu, uydurma yok, bulunamayan = "kaynak bulunamadı".
