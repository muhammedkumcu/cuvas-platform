# DERİN ARAŞTIRMA PROMPTU #3 — Türk Dillerinin Karşılaştırmalı Dilbilimi: Benzerlikler, Farklılıklar, Akrabalık Ağı

> Bu dosyayı bir **deep-research / derin araştırma yapan yapay zekâya** (ChatGPT/Gemini/Perplexity Deep Research) **olduğu gibi** ver. Çıktı: **kaynak açısından zengin, tablolarla dolu, PDF'e aktarılabilir BÜYÜK bir derleme.** Bu derleme, ~20 Türk dilinin morfolojisini **karşılaştıran** bir öğrenme/keşif platformunun veri ve içerik temelini oluşturacak.

---

## 0. ROL VE BAĞLAM

Sen, **karşılaştırmalı Türkoloji (comparative Turkic linguistics)** ve **hesaplamalı dilbilim** kesişiminde uzman bir araştırmacısın. Bir ekip, **Apertium morfolojik FST'leriyle ~20 Türk dili için** (analiz + üretim) çalışan, **öğrenen-odaklı bir morfoloji platformu** kuruyor. Platformun **yıldız özelliği**: Türk dillerini **birbiriyle karşılaştıran** bir keşif ağı — bir kelime/kavram gir, onun **kökünü, morfolojik analizini ve diğer Türk dillerindeki karşılıklarını/kognatlarını**, aralarındaki **düzenli ses denkliklerini** (ör. Çuvaş rotasizmi z→r, lambdasizm ş→l) ve **morfolojik farkları** gör.

apertium üzerinden çalışılacak diller (kabaca): **Çuvaşça (chv), Türkçe (tur), Azerice (aze), Türkmence (tuk), Gagavuzca (gag), Kırım Tatarcası (crh), Tatarca (tat), Başkurtça (bak), Kazakça (kaz), Kırgızca (kir), Karakalpakça (kaa), Karaçay-Balkarca (krc), Kumukça (kum), Nogayca (nog), Özbekçe (uzb), Uygurca (uig), Altayca (alt), Hakasça (kjh), Tuvaca (tyv), Saha/Yakutça (sah), Halaçça (klj)**.

Bu rapor, bu **karşılaştırma ağının** dilbilimsel ve veri temelini eksiksiz kurmalı.

---

## 1. ARAŞTIRMANIN AMACI (tek cümlede)

> Türk dillerinin **akrabalık yapısını, düzenli ses denkliklerini, fonolojik ve morfolojik benzerlik/farklılıklarını, kognat (kökteş) sözcük setlerini ve bunları besleyecek mevcut veri kaynaklarını** kaynaklarıyla derleyen; bir **karşılaştırma platformunun** (kognat ağı + ses-denkliği açıklayıcısı + karşılaştırmalı paradigma tabloları + özellik matrisleri) doğrudan üzerine inşa edilebileceği kapsamlı bir referans üret.

---

## 2. ARAŞTIRMA SORULARI (bölüm bölüm — hepsini kapsa)

### BÖLÜM A — Sınıflandırma ve Soyağacı
A1. Türk dillerinin kolları: **Oğuz, Kıpçak, Karluk, Oğur (Bulgar), Sibirya (Sayan/Yenisey/Kuzey), Argu (Halaç)**. Her kolun ayırıcı özellikleri.
A2. Yukarıdaki ~20 dilin **hangi kola** ait olduğu (tablo: dil ↔ kol ↔ alt-kol). Çuvaşça'nın yalnız Oğur kolu üyesi olarak özel konumu.
A3. **Soyağacı + zaman derinlikleri** (Ana Türkçe'den ayrışma tahminleri; Oğur kolunun erken kopuşu). Glottolog/literatür temelli.

### BÖLÜM B — Düzenli Ses Denklikleri (RAPORUN KALBİ)
B1. Türk dilleri arası **düzenli ses denklikleri** — kollar arası sistematik karşılıklar. En azından:
   - **Rotasizm/Zetasizm:** Ana Türkçe *z ↔ Çuvaşça r (ör. *boz → пӑр / buz).
   - **Lambdasizm/Sigmatizm:** *ş ↔ Çuvaşça l (ör. *kış → хӗл / kış).
   - **d/t/y/z/j denkliği:** *ayak/adak/azak/atax/azmax (Ana Türkçe *ḏ refleksleri).
   - **g/ğ/v/w/null:** söz içi/sonu damaksıllar.
   - **Söz başı h-/null/y-** (ör. Halaçça h- koruması), **söz başı b-/m-, t-/d-**.
   - Ünlü denklikleri (ör. Çuvaş indirgenmiş ünlüleri, Yakut uzun ünlüleri).
B2. Her denklik için: **Ana Türkçe biçim → her kolun/dilin yansıması** tablosu + örnek sözcükler (yazı + Latin çevrim + anlam). Bu tablolar platformun "ses-denkliği açıklayıcısı"nı besleyecek — **makine-okunur kural seti** olarak da düşün.

### BÖLÜM C — Fonoloji Karşılaştırması
C1. Diller arası **ünlü envanterleri** (8'li, 9'lu sistemler; Çuvaş ă/ĕ; Yakut uzun ünlü+diftong).
C2. **Ünlü uyumu tipleri:** damak (ön/art) uyumu her dilde var mı; **dudak (yuvarlaklık) uyumu** hangi dillerde güçlü/zayıf/kayıp (ör. Özbekçe'de uyumun çözülmesi, Çuvaşça'da yuvarlaklık uyumu yokluğu).
C3. **Ünsüz sistemleri** ve dile özgü değişimler (Yakut, Çuvaş, Sibirya dilleri).

### BÖLÜM D — Morfoloji Karşılaştırması (platform paradigma tabloları için)
D1. **Hal sistemleri** karşılaştırması: temel haller (yalın, ilgi, yönelme, belirtme, bulunma, ayrılma, vasıta…) ve **ek biçimleri** diller arası tablo. Çuvaşça'nın datif-akkuzatif birleşmesi, ek sayısı farkları.
D2. **Çoğul** (-lar/-ler ve varyantları; Çuvaş -сем) ve **iyelik** ekleri karşılaştırması.
D3. **Fiil sistemi:** zaman/görünüş/kip ve **şahıs ekleri**; olumsuzluk; diller arası benzer/farklı yapılar. Aynı kavramın (ör. "geliyorum") 5-6 dildeki karşılaştırmalı çekimi.
D4. **Ek dizilişi (morfotaktik)** farkları (ör. Çuvaşça KÖK+İYELİK+ÇOĞUL+HAL ↔ Oğuz KÖK+ÇOĞUL+İYELİK+HAL).
D5. **Karşılaştırmalı paradigma örnekleri:** bir-iki ortak kök (ör. "ev", "gel-") için 6-8 dilde tam çekim tablosu (yazı + Latin + anlam).

### BÖLÜM E — Sözvarlığı ve Kognatlar (kognat-ağı için)
E1. **Çekirdek kognat setleri:** Swadesh listesi temelinde (sayılar, akrabalık, beden, doğa, temel fiiller) Türk dilleri arası kökteş sözcükler tablosu. Düzenli ses denkliklerini örnekleyen setler.
E2. **Alıntı katmanları:** Arapça/Farsça (Oğuz-Karluk), Rusça (Sovyet etkisi), Moğolca (Sibirya), Fin-Ugor (Çuvaş-İdil) — diller arası dağılım.
E3. **Mevcut kognat/etimoloji veri kaynakları** (platform verisi için, lisansıyla): Sevortyan *ESTYa*, Clauson *EDT*, Starostin *EDAL/Starling* (Tower of Babel), VanderWal Anand kognat setleri, *Turkic Lexicon*, NorthEuraLex, IELex-benzeri Türk veri setleri, Wiktionary etimolojileri.

### BÖLÜM F — Yazı Sistemleri
F1. Her dilin kullandığı yazı(lar): **Kiril / Latin / Arap** (ve geçiş durumları: Kazak/Özbek Latin'e geçiş, Azeri Latin, vb.). Platformun çoklu-yazı + harf-çevrim katmanı için tablo.

### BÖLÜM G — Karşılıklı Anlaşılabilirlik & Benzerlik Ölçümleri
G1. Diller/kollar arası **sözlüksel benzerlik / karşılıklı anlaşılabilirlik** üzerine nicel çalışmalar (varsa yüzdeler, mesafe matrisleri). Çuvaşça'nın diğerlerinden uzaklığı.

### BÖLÜM H — Mevcut Karşılaştırmalı Kaynaklar & Veri Setleri (platform için)
H1. **Standart referanslar:** Johanson & Csató, *The Turkic Languages* (Routledge); Tekin *Türk Dillerinin Sınıflandırılması*; Menges; Róna-Tas. 
H2. **Hesaplamalı veri:** UniMorph (Türk dilleri paradigmaları), Universal Dependencies (Türk treebank'leri), WALS (Türk dilleri özellik kodları), Glottolog (soyağacı), Apertium ailesi, UraloAltaic/NorthEuraLex. Her biri: kapsam, format, **lisans**, URL, platformda kullanım rolü.

### BÖLÜM I — Platforma Dönük Çıktı (eyleme dönük)
I1. Her bulgu kümesinin platformda **hangi özelliği** besleyeceğini netleştir:
   - **Kognat ağı görünümü** ← E1 kognat setleri + B ses denklikleri.
   - **Ses-denkliği açıklayıcısı** ← B tabloları (makine-okunur kurallar).
   - **Karşılaştırmalı paradigma tabloları** ← D + apertium üretimi.
   - **Özellik matrisi** (dil × özellik: uyum tipi, hal sayısı, yazı, kol) ← A, C, D, F.
I2. **Veri haritası:** hangi açık veri seti (UniMorph/UD/WALS/Glottolog/kognat DB) hangi özelliği doğrudan besler; lisans uyumu.

---

## 3. KAYNAK ÖNCELİĞİ
- (1) Hakemli karşılaştırmalı Türkoloji ve tarihsel dilbilim; (2) standart referans gramerler (Johanson & Csató, Clauson, Tekin, Sevortyan); (3) açık veri (UniMorph, UD, WALS, Glottolog); (4) Wiktionary etimoloji/kognat.
- **İngilizce, Rusça, Türkçe** tara. Her iddiaya kaynak (URL + erişim tarihi). Veri setlerine **lisans**.
- Çelişen sınıflandırma/etimolojilerde bunu belirt, baskın görüşü işaretle. **Uydurma yok.**

## 4. ÇIKTI BİÇİMİ (rapor / PDF)
- Dil: **Türkçe** (teknik terim İngilizce parantezle).
- **Bol tablo:** ses-denkliği tabloları (Ana Türkçe → diller), kognat setleri (kavram × dil), karşılaştırmalı paradigmalar (çekim × dil), özellik matrisi (dil × özellik).
- Tüm örnekler: **yazı (Kiril/Latin/Arap) · Latin çevrim · Türkçe anlam**.
- Sonunda: (a) **özellik matrisi** (20 dil × {kol, yazı, ünlü-uyumu, hal sayısı, ayırıcı ses olayları}), (b) **ana ses-denkliği özet tablosu**, (c) **veri-kaynağı envanteri** (kaynak · kapsam · lisans · URL · platform rolü), (d) tam kaynakça.
- Kapsamlı tut; eyleme dönük, alıntılanabilir ol.

## 5. NİHAİ KONTROL LİSTESİ
- [ ] 20 dilin kol/soyağacı sınıflandırması tabloyla verildi mi?
- [ ] Rotasizm/lambdasizm + d/t/y/z/j + diğer ana ses denklikleri Ana-Türkçe→diller tablosuyla mı?
- [ ] Ünlü uyumu tipleri (dudak uyumu kaybı dahil) diller arası karşılaştırıldı mı?
- [ ] Hal/iyelik/çoğul/fiil ekleri ve morfotaktik diziliş karşılaştırma tablosu var mı?
- [ ] Çekirdek kognat setleri (Swadesh) diller arası tablo halinde mi?
- [ ] Kognat/etimoloji + UniMorph/UD/WALS/Glottolog veri kaynakları lisans+URL ile envanterlendi mi?
- [ ] Yazı sistemleri tablosu var mı?
- [ ] "Platform veri haritası" (hangi veri → hangi özellik) verildi mi?
- [ ] Tüm örnekler yazı+çevrim+anlam üçlüsüyle mi? Her iddianın kaynağı var mı?

> **Hedef:** Bu derleme elime geçtiğinde, Türk dillerinin tüm benzerlik/farklılıklarını **bir arada** sunan; kognat ağı, ses-denkliği açıklayıcısı, karşılaştırmalı paradigma ve özellik matrisi içeren bir platformu **doğrudan** inşa edebilmeli ve literatürden yeni tespitler geldikçe ekleyebilmeliyim.
