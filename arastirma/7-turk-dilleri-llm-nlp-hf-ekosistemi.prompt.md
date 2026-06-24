# DEEP RESEARCH PROMPT (ÇOK DETAYLI) — Türk Dilleri LLM / NLP / HuggingFace Ekosistemi Envanteri

> **Bağlam & amaç:** KÖKEN, araştırmacıların "ilk uğrağı" olmayı, Türk dillerine dair açık literatürü/araçları/modelleri tek elden gösterip eksik/gelişmişliği işaretlemeyi hedefliyor. Platforma bir **"Türk Dilleri NLP/LLM Ekosistemi"** bölümü ekleyeceğiz. Bu araştırma o bölümün VERİSİNİ üretsin: HuggingFace ve genel literatürde Türk dilleri için NE VARSA kapsamlı, güncel, atıflı, lisanslı bir envanter. Morfoloji araçları ayrı promptlarda (`5`, `5b`); BURADA odak: **LLM'ler, sinir-ağı modelleri, veri setleri, ASR/STT/TTS, benchmark/leaderboard, organizasyonlar, güncel çalışmalar.** Uydurma YOK; her kayıt URL+lisans+tarih; bulunamayan = "kaynak bulunamadı".

## Kapsanan diller
Türkçe + Azerice, Türkmence, Gagavuzca, Kırım Tatarcası, Tatarca, Başkurtça, Kazakça, Kırgızca, Karakalpakça, Karaçay-Balkarca, Kumukça, Nogayca, Özbekçe, Uygurca, Altayca, Hakasça, Tuvaca, Şorca, Saha (Yakut), **Çuvaşça**, Halaçça (+ varsa Salar, Dolganca). Düşük-kaynaklı + çekirdek Çuvaşçaya özel önem.

## İstenen başlıklar (her biri için: ad, org/yazar, URL/HF-repo, lisans, tarih, dil-kapsamı, kısa değerlendirme)
1. **Dil modelleri (encoder/LLM):** çok-dilli (mBERT, XLM-R, mT5, BLOOM, Aya, NLLB) Türk dili kapsamı; **Türkçe özel** (BERTurk, TURNA, Trendyol-LLM, Kanarya, VBART, Cosmos, Hamza/SambaLingo…); **diğer Türk dilleri için özel** modeller (Kazakh/Uzbek/Tatar/Uyghur/Azerbaijani BERT/GPT — HF'de org/model adlarıyla).
2. **Üretken LLM'ler & instruction-tuned:** Türk dillerini destekleyen açık LLM'ler (Llama/Qwen/Gemma türevleri, yerel fine-tune'lar), çok-dilli kapsama.
3. **Veri setleri:** tek-dilli korpuslar (OSCAR, CC-100, mC4, Wikipedia dump'ları — Türk dili boyutları), **paralel** (OPUS, NLLB, FLORES-200 hangi Türk dilleri), talimat/QA/benchmark setleri, NER/POS/duygu/özetleme setleri, **tarihsel** (Orhun, Eski Uygur).
4. **ASR/STT & TTS:** HF'deki Türk dili konuşma modelleri (Whisper türevleri, MMS, wav2vec2, Common Voice; **örnek: TurkmedSTT — Türkçe medikal STT org'u** gibi alana/dile özel çalışmalar), org bazında.
5. **Benchmark / leaderboard / değerlendirme:** Türkçe/Türk dilleri için açık leaderboard'lar (Türkçe MMLU, TruthfulQA-tr, Mukayese, açık değerlendirme suit'leri), çok-dilli benchmark'larda Türk dilleri.
6. **Anahtar organizasyonlar & topluluklar:** HF org'ları (boun-tabilab, ytu-ce-cosmos, ISSAI, Trendyol, KUIS-AI, Tilmash, sahatyla vb.), üniversite grupları, "awesome-turkish-nlp" tarzı dizinler, TurkLang/UBMK toplulukları.
7. **Güncel çalışmalar (son 1–2 yıl):** yeni model/dataset duyuruları, makaleler, dil başına "en son ne çıktı".

## Platforma yansıtma (ürün açısından — kısa öneri)
- Bu envanteri KÖKEN'de **nasıl göstermeliyiz?** Öneri: dil × yetenek (LLM / dataset / ASR / TTS / benchmark) matrisi + her hücrede "var/yok + en iyi açık kaynak + HF linki + lisans". Araştırmacıya "bu dilde ne var, ne yok" tek bakışta.
- **Güncellik:** bu liste nasıl GÜNCEL tutulur? (HF API ile org/model otomatik çekme mümkün mü; manuel periyodik mi.) "Haberler / yeni çıkanlar" akışı için kaynak önerisi.

## Çıktı
Dil × yetenek **matrisi** + her araç/model için künye (ad/URL/lisans/tarih/kapsam) + **boşluk haritası** (dil başına en kritik eksik) + "hemen platforma eklenebilir" kısa liste + güncel-tutma stratejisi.
