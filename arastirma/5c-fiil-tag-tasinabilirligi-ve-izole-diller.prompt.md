# DEEP RESEARCH PROMPT (DAR/ODAKLI) — Türk Dilleri Arası Fiil Etiket Taşınabilirliği + İzole Diller + Füzyonel Ayrışma

> **Bağlam:** KÖKEN'de diller-arası motor (`/crosslang`) çalışıyor: kaynak dilde analiz → apertium `.dix` ile kök eşle → hedefte AYNI etiketlerle üret. İSİMLERDE güçlü (evlerde → 8 dil). Üç somut duvara tosladık; bu araştırma SADECE bunları çözsün. Genel envanter ayrı (`5-`, `5b-` promptları). Uygulanabilirlik + açık-lisans + atıf şart; uydurma yok.

## SORU 1 — Fiil TAM (zaman-görünüş-kip) etiketlerinin Türk dilleri ARASI karşılığı
İsim çekim etiketleri (`<pl>`, `<px1pl>`, `<loc>`…) apertium Türk FST'lerinde büyük oranda ORTAK → diller-arası üretim sorunsuz. Ama FİİL etiketleri tutmuyor: Türkçe "gidiyorum" `git<v><tv><pres><...>` ve "okuduk" `oku<v><tv><ger_past>` hedef dillerde üretmiyor (etiket envanteri farklı). İstenen:
1. **apertium-tur, -kaz, -tat, -bak, -kir, -aze, -uzb, -uig, -chv, -sah** morfolojik FST'lerinde FİİL **zaman/görünüş/kip + kişi** etiket envanterlerinin **karşılaştırmalı tablosu**: hangi etiket hangi dilde var, hangileri ORTAK, hangileri dile-özgü (ör. Türkçe `<pres>` şimdiki zaman ≈ diğer dillerde ne; `<ifi>` görülen geçmiş hangi dillerde; `<ger_past>` ulaç).
2. Bir kaynak-dil fiil çözümünü hedef-dilde geçerli çekime çevirmek için **etiket-haritalama (tag normalization) tablosu** önerisi: `tur:<pres> → kaz:?`, `tur:<ger_past> → ?`. Hangi TAM kategorileri tüm aileye güvenle taşınır, hangileri taşınamaz (dürüst sınır)?
3. Kaynak: apertium FST'lerinin `.lexc`/`.rlx`/`twol` dosyaları, apertium Türk dilleri wiki, ilgili tezler. Somut, uygulanabilir çıktı (JSON-vari harita).

## SORU 2 — İzole diller: Saha (Yakut) + Çuvaşça çapraz-dil kaynakları
`/crosslang` apertium `.dix` grafiğine dayanıyor. **Saha (sah) için HİÇBİR iki-dilli apertium pair YOK** → cross-lang dışı. Çuvaşça yalnız `chv-tat` ile bağlı (çekirdek dilimiz, daha fazlası lazım). İstenen:
1. **Saha (Yakut):** açık kaynak/erişimli **iki-dilli sözlük veya kök-eşleme** kaynağı var mı (apertium-sah-? denemeleri, GiellaLT-sah, Wiktionary sah, sahatyla.ru, PanLex sah kapsamı, Lexibank/Savelyev sah)? Saha'yı diğer Türk dillerine kök-düzeyinde bağlayacak EN uygulanabilir açık yol.
2. **Çuvaşça:** `chv-tat` dışında açık iki-dilli/kök-eşleme kaynağı (apertium-chv-?, Wiktionary chv, Aşmarin dijital, PanLex chv). Çuvaşçayı daha çok dile bağlamak için.
3. **Genel fallback:** SavelyevTurkic CLDF (254 kavram, bizde var) ile izole dilleri bağlamak pratik mi — kavram→hedef-dil kognat biçimi (çekimsiz gösterim)? Lisans/uygulanabilirlik.

## SORU 3 — Füzyonel (kaynaşık) iyelik+hâl ince ayrışması
Çuvaşça iyelik+hâl (ҫурт**не**) ve Uygurca çoğul+iyelik (köz**lىrى**m) **kaynaşık/allomorfik**; bizim "nom-ara-biçim + NW-hizalama" yöntemimiz bunları tek kaynaşık ek olarak bırakıyor (doğru ama kaba; yeniden-üretim %93 ama tam morfem ayrışması değil). İstenen:
1. Çuvaşça ve Yakutça (ve Uygurca çoğul+iyelik) için **iyelik+hâl yüzey allomorf tabloları** — açık kaynaklarda (dilbilgileri, apertium lexc, GiellaLT) bu eklerin yüzey biçimleri ve sınırları belgeli mi? Tek kaynaşık ek yerine ALT-morfemlere (iyelik | hâl) bölmek için referans tablo.
2. Bu dillerde iyelik+hâl gerçekten PORTMANTEAU mu (bölünemez) yoksa bölünebilir allomorf mu — linguistik kaynak.
3. (5b'deki) Needleman-Wunsch yöntemini "lemma + kanonik-allomorf-dizisi vs yüzey" tek-hizalamaya çevirmek bu füzyonu çözer mi; bu diller için kanonik allomorf dizileri.

## Çıktı
Her soru için **net, uygulanabilir öneri + tablo + lisans/URL**. "Hemen yapılabilir" vs "araştırma gerektirir" ayrımı. Bulunamayan = "kaynak bulunamadı".
