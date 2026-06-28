# DEEP RESEARCH — Türk Dilleri METİN KORPUSU Kaynak Haritası (kapsam ölçümü + açık veri katkısı)

> **Amaç (KÖKEN için):** Platformda morfolojik analiz/üretim/paradigma **20 Türk dilinde** canlı çalışıyor (apertium FST'leri). Şimdi her dil için **kapsam (coverage/recall)** ölçeceğiz: gerçek metindeki sözcüklerin yüzde kaçını analizci tanıyor. Bunun için **dil başına temiz, mümkünse eşit-boyutlu metin korpusu** lazım. Bu prompt, **20 dilin her biri için hangi korpusun var olduğunu** (kaynak/boyut/lisans/URL) haritalar. **Akademik, atıflı, UYDURMA YOK** — korpus bulunamayan dil için açıkça "bulunamadı / çok kısıtlı" yaz. **Wikipedia birincil kaynak DEĞİL** (en fazla Leipzig gibi derlemelerin bileşeninde dolaylı geçerse not düş).

## Diller (tam 20 — apertium morph FST'si olanlar)
**Büyük/orta:** Türkçe (tur), Azerbaycanca (aze), Kazakça (kaz), Kırgızca (kir), Özbekçe (uzb), Uygurca (uig), Tatarca (tat), Başkurtça (bak), Çuvaşça (chv), Sahaca/Yakutça (sah), Türkmence (tuk), Kırım Tatarcası (crh), Gagavuzca (gag), Karakalpakça (kaa).
**★ DÜŞÜK-KAYNAKLI 6 (en kritik — burada özellikle derine in):** Altayca (alt), Hakasça (kjh), Karaçay-Balkarca (krc), Kumukça (kum), Nogayca (nog), Tuvaca (tyv).
> Not: Bu dillerin hepsinin apertium FST'si + sözlüğü VAR; dolayısıyla FST'nin kurulduğu **kaynak metin** de bir yerde olmalı (apertium veri depoları, İncil/dini çeviriler, ulusal/bölgesel haber, sosyal medya, OSCAR/CC100/mC4 dilimleri, üniversite projeleri). Bu dillerde "hiç yok" cevabını kolay kabul etme — **iyi kötü** bir kaynak bul.

## İstenen: dil başına korpus tablosu — her satır bir korpus kaynağı
Her dil için bulabildiğin TÜM kayda değer metin korpuslarını şu sütunlarla listele:

1. **Dil** (kod)
2. **Korpus adı / sağlayıcı** (ör. Leipzig Corpora, Common Voice, ulusal korpus, apertium-<lang> veri, OSCAR, …)
3. **Tür**: haber / web-tarama / edebî / dinî (İncil/Kur'an çevirisi) / konuşma-transkripti / ansiklopedik / parlamento / sosyal medya
4. **Boyut** (token ve/veya cümle sayısı; tahminse "≈" + dayanak)
5. **Yazı sistemi** (Latin/Kiril/Arap — bizim FST script'iyle uyumlu mu)
6. **Lisans** + **yeniden dağıtılabilir mi?** (CC0/CC-BY = evet; CC-BY-NC/telifli = yalnız ölç+atıf, dağıtma)
7. **Erişim URL'i** (doğrudan indirme ya da sayfa; erişilebilirlik doğrulanmış)
8. **Standart-boyut katmanı var mı** (ör. Leipzig 10K/30K/100K cümle — eşit-boyut karşılaştırma için)
9. **Kalite notu** (editlü/temiz mi, gürültü, kod-karışımı, OCR hatası vb.)

## Özellikle araştır (öncelik sırası)
1. **Leipzig Corpora Collection** (wortschatz.uni-leipzig.de) — hangi 20 dilde var, hangi sabit-boyut katmanları (10K/30K/100K/300K/1M cümle), kompozisyon (haber/web/wiki oranı), lisans. *(Eşit-boyut karşılaştırmanın omurgası.)*
2. **Mozilla Common Voice** — hangi Türk dillerinde var, transkript token sayısı, **CC0** doğrula (açık-veri katkımız bu olur).
3. **Resmi/ulusal kaynaklar:** ulusal dil korpusları (Tatar Milli Korpusu, Bashkir, Kazakh Language Corpus, Sakha, Uzbek vb.) + **devlet haber ajansları** (her dilin resmî haber sitesi — temiz, editlü; TurkmenFST'de kullanılan yöntem). Lisans/erişim.
4. **★ 6 düşük-kaynaklı dil için derin tarama:** apertium-<lang> GitHub depolarındaki kaynak/test korpusları; **No Language Left Behind (NLLB)** & **FLORES-200** kapsamı; **OSCAR / CC100 / mC4 / Glot500 / MADLAD-400** bu dilleri içeriyor mu (boyut!); İncil çevirisi (eBible.org / PNG corpus); RusyaFederasyonu cumhuriyet dilleri dijital arşivleri (Hakas/Tuva/Altay/Nogay/Kumuk/Karaçay-Balkar bölgesel gazete/portal); üniversite/akademik proje korpusları.
5. **Türkçe NLP toplulukları & HuggingFace datasets** — Türk dilleri için açık metin veri setleri (token sayısı + lisans).

## Çıktı formatı
- Dil başına tablo (yukarıdaki 9 sütun) + en sonda **özet matris**: 20 dil × (en iyi standart korpus / boyut / lisans / yeniden-dağıtılabilir mi).
- **Öneri bölümü:** eşit-boyut kapsam karşılaştırması için EN İYİ tek-kaynak hangisi (muhtemelen Leipzig — doğrula), açık-veri katkısı için hangileri (CC0), ve 6 düşük-kaynaklı dil için pratik plan.
- **Dürüstlük:** her boyut/lisans iddiası kaynaklı; doğrulanamayan link "erişilemedi"; korpussuz dil açıkça işaretli. Sonda **atıf listesi** (Leipzig Goldhahn vd. 2012, Common Voice Ardila vd. 2020, OSCAR, NLLB vb. gerçek künyeler).

## KÖKEN bağlamı
Bu veri, sitedeki **"Kalite & Kapsam"** sayfasını besleyecek: 20 dil × (kalite tier · lexicon büyüklüğü · round-trip tutarlılık · UniMorph doğruluk · **korpus kapsamı**). Kapsam metriği yalnızca temiz, kaynaklı korpusla anlamlı; o yüzden bu haritalama kritik. Eşit-boyut + açık-lisans + düşük-kaynaklı dillerde "iyi kötü bir şey" üçlüsü hedef.
