# DEEP RESEARCH PROMPT — Türk Dilleri NLP/LLM Ekosistemi: KATEGORİ × DİL × DOĞRUDAN BAĞLANTI (link-yoğun, güncel)

> **Amaç (KÖKEN "Ekosistem" sayfası için):** Mevcut sayfayı (kategori-önce → dil-içinde → doğrudan bağlantı launchpad'i) **maksimuma** çıkar. Tek isim/durağan envanter İSTEMİYORUZ — araştırmacıyı **doğrudan çalışmaya götüren BOL bağlantı** istiyoruz: HuggingFace model/veri kartları, GitHub repoları, leaderboard'lar, derli toplu listeler, makaleler, **HF dışı** kaynaklar (üniversite/lab sayfaları, korpus portalları, Common Voice, OSCAR, vb.).
>
> **Çıktı biçimi (ÖNEMLİ):** Aşağıdaki her **kategori** için, her **dil** altında **mümkün olduğunca çok** giriş ver. Her giriş: **`Ad — TAM URL — kısa not (mimari/lisans/boyut) — (varsa) indirme sayısı / yıldız / son güncelleme tarihi`**. Bağlantı **doğrulanmış/gerçek** olmalı (uydurma URL YOK); bulunamayan = "kayıt bulunamadı". Tartışmalı/eski olanı işaretle. **Olgunluk/yeterlilik yargısı KOYMA** (nötr; değerlendirme araştırmacıya ait) — yalnız ne VAR olduğunu, nerede olduğunu ve ne kadar kullanıldığını (indirme/yıldız) raporla.

## Kapsanacak diller
Türkçe, Azerice (kuzey/güney), Türkmence, Gagavuzca, Kırım Tatarcası, Kazakça, Kırgızca, Tatarca, Başkurtça, Karakalpakça, Karaçay-Balkarca, Kumukça, Nogayca, Özbekçe, Uygurca, Çuvaşça, Sahaca (Yakut), Tuvaca, Hakasça, Altayca, Şorca, Halaçça, Salarca, Sarı Uygurca, Dolganca. (Kaynağı olmayan diller için "kayıt bulunamadı" + en yakın çok-dilli platform.)

## Kategoriler (her biri için dil-bazlı BOL bağlantı + kategori-geneli "hub" bağlantıları)
1. **Üretken LLM** — chat/instruct/reasoning; tokenizer notu. Hub: ilgili HF arama, OpenLLM-TR ve diğer leaderboard'lar, awesome-listeler.
2. **Encoder / temsil** — BERT/ELECTRA/embedding/tokenizer; fill-mask/feature-extraction.
3. **Konuşma tanıma (ASR/STT)** — Whisper/MMS/wav2vec2 türevleri; WER/CER + saat. Hub: Common Voice indir sayfaları.
4. **Seslendirme (TTS)** — MMS/Piper/eSpeak/ISSAI/yerel; lisans (MIT/CC-BY-NC). Hub: HF TTS arama.
5. **Veri setleri / korpuslar** — tek-dilli, paralel, talimat; boyut. Hub: OSCAR, FLORES+/OLDI, ulusal korpuslar (TS Corpus, TNC vb.), HF datasets arama.
6. **Benchmark / değerlendirme** — yerel/kültürel setler + leaderboard'lar (Cetvel, TUMLU, kyrgyzMMLU, TurkBench, Türkçe-MMLU…).
7. **Araçlar / kütüphaneler** — FST/morfoloji/çeviri/işleme: **Apertium (per-dil), Zemberek, TRmorph, Zeyrek, Starlang, Nuve, TurkicNLP, Stanza, Trankit**, transliterasyon, OCR (Eski Türk/Uygur).
8. **Organizasyonlar & topluluklar** — laboratuvarlar/şirketler/topluluk indeksleri (ISSAI, YTÜ Cosmos, VNGRS, aLLMA, Tahrirchi/UzLM, Boğaziçi, TurkicNLP, kesimeg awesome, agmmnn liste, dergiler/konferanslar TurkLang/UBMK).

## Ek istekler
- **Güncellik:** 2025–2026'da çıkan/öne çıkanları özellikle vurgula; her girişe (varsa) **son güncelleme** ve **indirme** ekle.
- **HF dışını unutma:** GitHub, üniversite/lab siteleri, Common Voice, OSCAR, ELRA/LDC (açık olanlar), dergi/portal.
- **"En çok indirilen / en başarılı":** her dil-kategori için ilk 3-5'i indirme/leaderboard sırasına göre işaretle.
- **Otomatik güncel-tutma için:** her organizasyon/lab'ın HF `author=` ve dil `tags=` filtreli arama URL'lerini ver (KÖKEN'in HfApi CRON'u için).

## Çıktı
Kategori başlıkları altında dil alt-başlıkları + madde madde **Ad — URL — not — metrik**. Sonda: (i) kategori-geneli hub URL listesi, (ii) "kayıt bulunamadı" dilleri, (iii) kısa kaynak/atıf listesi.
