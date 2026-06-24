# YOLCULUK ve VAZGEÇİLENLER — Ne Yaptık, Neyden Vazgeçtik, NEDEN

> Bu belge, projede yapılıp sonra **terk edilen** işleri ve **neden** vazgeçtiğimizi kaydeder.
> Amaç: emek kaybolmasın, aynı yola tekrar girmeyelim, kararların gerekçesi belli olsun.

## Özet zaman çizgisi
1. **Başlangıç hedefi:** Türkmence'de yaptığımız (TurkLang 2026) kural-tabanlı kendi morfolojik motorunu **Çuvaşça için tekrarlamak.**
2. **Yaptık (kendi motor — `arsiv/cuvasca-kendi-motor/`):** apertium-chv + Hunspell + Wiktionary + corpus'tan **63.5K girişlik 4-kaynaklı sözlük**; Python fonoloji/morfotaktik/üretim/analiz motoru; web + REST API + ICALL alıştırma + sanal Kiril klavyesi; **%75 token kapsamı**; bağımsız doğrulama (Wiktionary %86); **karışık-yazı kirliliği bulgusu (%45.85)**. 62 test.
3. **Kırılma noktası:** Kullanıcı haklı olarak sordu — apertium-chv zaten olgun (~%85), stemmer+lemmatizer+üretim var; **biz neden kendi motorumuzu yapıyoruz?** Ben "Windows'ta apertium çalışmaz" demiştim — **yanlıştı.**
4. **Kanıt (VM'de):** Linux'ta `pip install hfst turkicnlp` sorunsuz; `turkicnlp.download("chv")` apertium FST'sini indiriyor; **analiz HEM üretim** çalışıyor (`automorf` + `autogen` FST'leri), ~20 Türk dili için. → "Windows engeli" sadece dev makineydi; **deploy Linux'ta apertium kusursuz.**
5. **Pivot (mevcut yön):** Tek dilli kendi-motor → **çok-dilli (~20 dil) Apertium-temelli morfoloji öğrenme + karşılaştırma platformu.** apertium ile yarışmıyoruz; onu **öğrenenlere erişilebilir** kılıyoruz + üstüne **karşılaştırma ağı** koyuyoruz.

## Neden vazgeçtik (kendi motor)
- **Apertium daha olgun:** ~%85 kapsam (bizim %75), tam tag seti, ~20 dil; bizim Python motoru bunu **daha düşük kapsamda yeniden icat ediyordu.**
- **Apertium kullanılabilir:** Linux deploy ortamında (Render/Docker) hfst+apertium çalışıyor → "kendi motor zorunlu" gerekçesi (Windows) çürüdü.
- **Akademik konumlandırma:** "apertium'dan iyi analizör" iddiası zayıftı; "apertium'u erişilebilir kılan + karşılaştıran platform" çok daha güçlü ve geniş.

## Saklanan / hâlâ değerli varlıklar (arsiv'den geri gelebilir)
- **Karışık-yazı kirliliği bulgusu (%45.85):** Çuvaş metninde Latin breve (ă/ĕ/ç) ↔ Kiril karışması; normalizasyon. **Sona saklandı (kullanıcı kararı)** — özgün NLP nüvesi, paper'a geç döneminde girer. Kod: `arsiv/.../chuvash_fst/phonology.py` (CHUVASH_LATIN_MAP) + ölçüm `arsiv/.../scripts/corpus_coverage.py`.
- **Çok-kaynaklı sözlük derleme metodolojisi** (apertium+Hunspell+Wiktionary+corpus-keşfi) + Hunspell'i Wayback'ten kurtarma — yeniden kullanılabilir teknik.
- **Çuvaşça morfoloji kural spesifikasyonu** (`arsiv/.../kurallar/KURALLAR_CUVASCA.md`) — Çuvaşça derin vaka için referans.
- **Web/ICALL prototipi** (`arsiv/.../chuvash-fst/web/`) — yeni platformun UI fikirleri için şablon (paradigma gezgini, sanal klavye, alıştırma).

## Dersler (tekrar düşmemek için)
- **"X kullanılamaz" deme — KANITLA.** "Windows'ta hfst derlenmiyor" ≠ "apertium kullanılamaz"; deploy ortamı (Linux) farklı. Empirik test her şeyi değiştirdi.
- **Olgun açık kaynak aracı yeniden icat etme.** Üstüne değer kat (erişilebilirlik, pedagoji, karşılaştırma).
- **Kullanıcının stratejik itirazlarını ciddiye al** — "gerçekten yeterli mi / neden kendi motor" soruları yönü düzeltti.
