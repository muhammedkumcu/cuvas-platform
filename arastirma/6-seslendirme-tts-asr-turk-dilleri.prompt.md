# DEEP RESEARCH PROMPT — Türk Dilleri için Açık Seslendirme (TTS) + Konuşma Tanıma (ASR) Modelleri

> **Bağlam:** KÖKEN platformunda her dilde "▷ Seslendir" var ama şu an tarayıcı Web Speech API'sine düşüyor — çoğu Türk dilini DESTEKLEMİYOR / yanlış telaffuz. Her MVP dili (tur, aze, kaz, kir, uzb, uig, tat, bak, **chv**, sah) ve mümkünse tüm Türk dilleri için **doğru telaffuzlu, açık/açık-erişimli TTS** lazım. İkincil: ASR (öğrenci telaffuz alıştırması + araştırmacı için). Uygulanabilirlik + lisans + atıf şart; uydurma yok, bulunamayan = "kaynak bulunamadı".

## SORU 1 — Dil başına AÇIK TTS (metin → konuşma)
Her dil için (öncelik: chv, sah, kaz, uig gibi düşük-kaynak + çekirdek Çuvaşça):
1. **Hangi açık/açık-erişimli TTS modeli/sesi var?** Aday aileler: **Meta MMS-TTS** (1100+ dil, hangi Türk dilleri?), **Coqui TTS / XTTS**, **Piper** (rhasspy), **espeak-ng** (fonem tabanlı — hangi Türk dilleri, kalite), HuggingFace TTS modelleri (org/model adı), bölgesel projeler.
2. Her model: **kapsadığı diller, kalite (doğal/robotik), lisans (ticari uygun mu), boyut, çalıştırma (HF Inference API / yerel / ONNX), Python entegrasyonu.**
3. **Dürüst boşluk haritası:** hangi Türk dilleri için HİÇ açık TTS yok (örn. Çuvaşça, Şor, Halaç?). Bu diller için espeak-ng fonem-kuralı veya yakın-dil sesi ikamesi pratik mi?
4. **Entegrasyon önerisi:** KÖKEN (FastAPI + web) için en uygulanabilir mimari — sunucuda yerel model mi, HF API mi, tarayıcıda WASM (Piper/espeak) mı? Dil→model yönlendirme tablosu.

## SORU 2 — Açık ASR (konuşma → metin) [ikincil]
1. Türk dilleri için açık ASR: **Whisper** (hangi Türk dillerini ne kalitede), **Meta MMS-ASR**, **Mozilla Common Voice** (hangi Türk dilleri, saat), wav2vec2/HF modelleri, bölgesel (örn. ISSAI Kazakça).
2. Öğrenci "telaffuzunu söyle, kontrol et" alıştırması için hangi diller pratik; lisans/kapsam.

## SORU 3 — Karar tabloları
- **TTS:** dil × {en iyi açık model / kalite / lisans / çalıştırma şekli / Python}.
- **ASR:** dil × {model / kapsam / lisans}.
- "Hemen yapılabilir" (örn. MMS-TTS HF API) vs "araştırma/eğitim gerektirir" (örn. Çuvaşça TTS yoksa) ayrımı.
- KÖKEN'e **MVP'de hemen bağlanabilecek** 1 TTS hattı önerisi (tüm/çoğu MVP dilini kapsayan).
