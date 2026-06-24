# ÇUVAŞÇA ÖĞRENME PLATFORMU — SOMUT ÖZELLİK & İÇERİK SPESİFİKASYONU

> Pivot (bkz. PLAN_CUVASCA.md §PIVOT): apertium analiz temeli, biz **üretim + ICALL öğrenme** katmanı. Bu dosya "tam olarak ne ekleyeceğiz" sorusunun somut yanıtı. Öncelik etiketleri: **[MVP]** = paper için bu hafta · **[STRETCH]** = kabul sonrası / sonraki dalga.

## A. Motor-güçlü araçlar (çekirdek değer)
1. **[MVP] Paradigma Gezgini** — kullanıcı bir Çuvaşça isim/fiil girer → tam çekim tablosu (isim: 8 hal × tekil/çoğul + iyelik; fiil: şimdiki/geçmiş/gelecek/emir × 6 şahıs + olumsuz). Morfemler **renklendirilir** (kök / ek). *Durum: motor hazır (Gün 3-4).*
2. **[MVP] "Bu Kelimeyi Açıkla" (Analiz)** — yüzey kelime → kök + ek zinciri + etiketler + Rusça anlam. *Gün 5 analiz motoru.*
3. **[MVP] Yazım Denetimi** — girilen biçim geçerli mi (sözlük + morfoloji), değilse öneri. *Motor + lexicon.*
4. **[MVP] Sözlük Arama** — 25.034 kök + Rusça anlam (apertium'dan). Köke tıkla → paradigma. *Veri hazır.*

## B. ICALL — Akıllı öğrenme (yeniliğin kalbi)
5. **[MVP] Boşluk-Doldurma Egzersizi** — sistem doğru çekimli formu **üretir** + 3 **çeldirici (distractor)** üretir (yanlış ama yapısal olarak mantıklı: yanlış hal/şahıs/uyum). Çoktan seçmeli/yazmalı.
6. **[STRETCH] Aralıklı Tekrar (SRS)** — kelime + paradigma hücrelerinde Leitner/SM-2 tekrar zamanlaması.
7. **[STRETCH] Oyunlaştırma** — günlük seri (streak), puan, rozet (ör. "Hal Ustası"), seviye, liderlik.
8. **[STRETCH] Yapılandırılmış Dersler** — morfoloji giriş modülleri (haller, iyelik, zamanlar) interaktif örneklerle.

## C. UX / Çuvaşça'ya özgü
9. **[MVP] Sanal Kiril Klavyesi** — Ӑ Ӗ Ҫ Ӳ tek dokunuş; mobil uyumlu.
10. **[MVP] Homoglyph Düzeltici** — Latin a/c/e/o/p/x/y → Kiril otomatik (girişte görünmez). *Motor hazır (phonology.normalize).*
11. **[STRETCH] Harf Çevrimi** — Kiril ↔ Latin geçiş; arayüz dili TR/RU/EN.
12. **[STRETCH] Kültürel tasarım** — Çuvaş motifleri/renkleri (aidiyet hissi).

## D. Çok-dillilik (extensibility kanıtı)
13. **[MVP-light] Dil-soyutlamalı mimari** — motor `language` parametresiyle çalışır; Çuvaşça birinci sınıf.
14. **[STRETCH] İkinci dil: Türkmence** — elimizdeki TurkmenFST motorunu aynı platforma bağla → "yeniden kullanılabilir şablon" iddiasının canlı kanıtı. Pan-Türkik vizyonu = gelecek çalışma.

## E. Teknik mimari (araştırma #2, D3)
- **Backend:** Python REST API (Flask/FastAPI) → `chuvash_fst` motorunu çağırır, JSON döner.
- **Frontend:** hafif SPA (statik + fetch) — kırsal düşük bant için PWA, Vercel/Render.
- **Bu hafta MVP web:** tek sayfa — Paradigma Gezgini + Analiz + Yazım + sanal klavye. Oyunlaştırma/SRS sonra.

## F. Paper ile eşleme (akademik kanıt)
- Sistem yeniliği → A1-2, B5 (FST'nin ICALL'e yeniden kullanımı).
- Teknik katkı → C10 (homoglyph normalizasyon).
- Değerlendirme (Gün 6) → motor kapsamı + apertium karşılaştırması + round-trip; (stretch) küçük egzersiz/uzman değerlendirmesi.
- Metodoloji/şablon → D13-14 (Türkmence→Çuvaşça yeniden kullanım).

## Bu haftanın gerçekçi MVP'si (paper demosu)
Motor (✅ isim+fiil) + analiz (Gün 5) + REST API (Gün 5) + tek-sayfa web (Paradigma Gezgini + Analiz + Yazım + sanal klavye + homoglyph) + corpus değerlendirmesi (Gün 6). Oyunlaştırma/SRS/dersler/ses/Türkmence-2.dil = kabul sonrası dalga.
