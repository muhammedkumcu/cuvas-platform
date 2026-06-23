# DERİN ARAŞTIRMA PROMPTU — Çuvaşça Kural Tabanlı Morfolojik Analiz & Üretim Sistemi

> Bu dosyayı bir **deep-research / derin araştırma yapan yapay zekâya** (ChatGPT Deep Research, Gemini Deep Research, Perplexity Deep Research vb.) **olduğu gibi** ver. Çıktı olarak **kaynakça açısından zengin, tablo içeren, PDF'e aktarılabilir kapsamlı bir rapor** isteniyor. Raporu PDF olarak dışa aktarıp bana geri ver.

---

## 0. ROL VE BAĞLAM

Sen, Türk dilleri (Turkic languages) üzerine uzmanlaşmış bir **hesaplamalı dilbilim (computational linguistics) araştırmacısısın**. Görevin, **Çuvaşça (Chuvash / чӑваш чӗлхи; ISO 639-3: `chv`)** dili için **kural tabanlı (rule-based), açık kaynaklı bir morfolojik analiz ve üretim (analysis & generation) sistemi** kurmak ve bunu akademik bir bildiriye dönüştürmek isteyen bir ekip için **eksiksiz bir kaynak ve dilbilgisi araştırması** yapmaktır.

### Neden bu araştırma?
Bu ekip daha önce **Türkmence** için tam olarak böyle bir sistem geliştirdi ve **TurkLang 2026** konferansında yayınladı (TurkmenFST). O sistem şu beş çekirdek bileşenden oluşuyordu:

1. **Fonoloji motoru** (ünlü uyumu, ünsüz yumuşaması, ünlü düşmesi, yuvarlaklaşma — durumsuz/stateless fonksiyonlar)
2. **Sözlük yöneticisi** (kök + POS + morfolojik özellik etiketleri içeren ~32.700 girişlik sözlük; 5 bağımsız kaynaktan 9 aşamalı derleme hattıyla derlendi)
3. **Morfotaktik sonlu durum makinesi** (FST-ilhamlı; ek sırası kısıtları: İsim = KÖK+[ÇOĞUL]+[İYELİK]+[HAL], Fiil = KÖK+[OLUMSUZ]+ZAMAN+[ŞAHIS])
4. **Üretim motoru** (kök + özellikler → çekimli yüzey biçimi)
5. **Üret-ve-doğrula (generate-and-verify) analiz motoru** (çekimli biçim → kök + ekler)
6. Üstüne REST API + web arayüzü + Hunspell sözlük dışa aktarımı.

Türkmence sistem **658.881 token'lık** bir haber corpusunda **%96,37 token kapsamı** elde etti ve resmî bir dil portalına (enedilim.com) karşı çapraz doğrulandı.

**Şimdi aynı metodolojiyi Çuvaşça için tekrarlamak istiyoruz.** ANCAK Çuvaşça, Türk dillerinin geri kalanından **kökten farklıdır** (aşağıya bakınız) — bu yüzden Türkmence motorunu kopyala-yapıştır yapamayız; Çuvaşça'nın kendi fonolojisi, hal sistemi, fiil zamanları ve **Kiril yazısı** için baştan tasarım gerekiyor. Bu araştırmanın amacı, o yeniden tasarımı ve sözlük derlemesini **gerçeklere ve kaynaklara dayandırmaktır**.

### Çuvaşça'yı özel kılan ve dikkat gerektiren noktalar (araştırmanın bunları derinlemesine ele alması ZORUNLU):
- Çuvaşça, yaşayan tek **Oğur (Bulgar) kolu** üyesidir; Oğuz/Kıpçak Türkçesinden binlerce yıl önce ayrılmıştır. Standart Türk dili NLP araçları ve çapraz-dilli aktarım Çuvaşça'da büyük ölçüde **başarısız olur**.
- **Rotasizm** (ortak Türkçe `z` → Çuvaşça `r`) ve **Lambdasizm** (ortak Türkçe `ş` → Çuvaşça `l`) gibi düzenli ses denklikleri vardır. Bunlar köken/kök tanımada kritiktir.
- **Kiril alfabesi** kullanır (Latin değil!). Çuvaş alfabesinde Rus Kirilline ek olarak **dört özel harf** vardır: **Ӑ ӑ, Ӗ ӗ, Ҫ ҫ, Ӳ ӳ**. İndirgenmiş (reduced) ünlüler (ă, ĕ) fonoloji ve hece yapısı açısından merkezîdir.
- Ünlü uyumu Türkmence'den farklı işler (ağırlıklı **ön/art (palatal) uyum**; yuvarlaklık uyumunun durumu araştırılmalı).
- Hal sistemi, iyelik, çoğul (**-сем**), fiil zaman/kip sistemi ve olumsuzluk **Oğuz dillerinden belirgin biçimde farklıdır**.

---

## 1. ARAŞTIRMANIN AMACI (tek cümlede)

> Çuvaşça için **kural tabanlı bir morfolojik analiz + üretim sistemi** inşa etmemizi ve bunu **UBMK 2026 / TurkLang** bildirisine dönüştürmemizi sağlayacak; (a) **tam ve kaynaklı bir Çuvaş morfolojisi tarifi**, (b) **açık kaynaklı/serbestçe kullanılabilir sözlük & corpus kaynaklarının envanteri (lisans bilgisiyle)**, ve (c) **mevcut Çuvaşça hesaplamalı çalışmaların karşılaştırması** üreten bir araştırma raporu hazırla.

---

## 2. ARAŞTIRMA SORULARI (bölüm bölüm — hepsini kapsa)

### BÖLÜM A — Dil, soy ve yazı sistemi
A1. Çuvaşça'nın soyağacı: Oğur/Bulgar kolu, ortak Türkçeden ayrılışı, en yakın akrabaları (tarihî Bulgarca, Hazarca). Modern lehçeleri: **Viryal (Yukarı)** ve **Anatri (Aşağı)**; standart yazı dili hangisine dayanır?
A2. **Rotasizm ve lambdasizm**: en az 10 somut örnek çiftiyle (ortak Türkçe biçim ↔ Çuvaşça biçim, anlam). Bunların kök tanıma/karşılaştırma için sonuçları.
A3. **Yazı sistemi**: 37 harfli modern Çuvaş Kiril alfabesinin tam dökümü; dört özel harfin (Ӑ, Ӗ, Ҫ, Ӳ) ses değerleri. Yaygın **Latin harf çevrimi (romanization/transliteration) şemaları** (bilimsel transkripsiyon, ISO 9, Türkologların kullandığı sistem). Tarihî yazılar (Aşmarin öncesi, eski Kiril, 1873 Yakovlev alfabesi). **Unicode kod noktaları** ve metin işlemede dikkat edilecek noktalar (büyük/küçük harf, sıralama).
A4. **Ses envanteri**: ünlüler (tam ünlüler vs. indirgenmiş ünlüler **ă/ĕ**; ön-art ve yuvarlaklık boyutları), ünsüzler. Çuvaşça'da **ünsüz uzunluğu/ikizleşme (gemination)** ve **sesli/sessiz ünsüz** karşıtlığının fonemik durumu (yazıda gösterilmeyen ama kuralla belirlenen seslenme).

### BÖLÜM B — Fonoloji / morfofonoloji (fonoloji motorunun temeli)
B1. **Ünlü uyumu**: Çuvaşça'da ön/art uyum nasıl işler? İndirgenmiş ünlüler uyuma nasıl katılır? Yuvarlaklık uyumu var mı, varsa hangi koşullarda? Eklerin ünlü değişkenleri (allomorf) hangi kurala göre seçilir? Tablolarla göster.
B2. **Ünsüz değişimleri**: Ünlüler arasında ve ek sınırlarında seslenme/yumuşama (ör. tonsuz → tonlu), ikizleşme, düşme. Türkmence'deki "ünsüz yumuşaması" (k→g, p→b, t→d, ç→j) kuralının **Çuvaşça karşılığı nedir?** Hangi ünsüzler hangi ortamda değişir? Düzenli mi, sözlükte istisna mı tutulmalı?
B3. **İndirgenmiş ünlü düşmesi / epentez**: ă, ĕ ünlülerinin ek alırken düşmesi/eklenmesi. Kurallar ve örnekler.
B4. Ek başı ünlü/ünsüz uyum koşulları (bağlayıcı ünlü, koruyucu ünsüz vb.).
B5. **ÖZET TABLO**: Türkmence motorunun fonoloji kuralları (vowel harmony, consonant softening, vowel elision, labial rounding) ile Çuvaşça'da bunların **hangisinin geçerli, hangisinin farklı, hangisinin yeni** olduğunu karşılaştıran bir tablo.

### BÖLÜM C — İsim (nominal) morfolojisi
C1. **Hal (case) sistemi**: Çuvaşça'nın tüm halleri (yalın, iyelik/genitif, datif, akkuzatif — datif-akkuzatif birleşik mi?, lokatif, ablatif, instrumental/araç, mahrumiyet/abessive, sebep-amaç vb.). HER hal için: ek biçimi (Kiril + Latin çevrim), ön/art allomorfları, ünsüzle/ünlüyle biten köklerdeki davranış. **Tam tablo** istiyorum.
C2. **Çoğul**: -сем eki ve allomorfları; iyelik+çoğul etkileşimi.
C3. **İyelik (possessive) ekleri**: 6 şahıs (tekil/çoğul 1./2./3.). Tam tablo + allomorflar.
C4. **Ek sıralaması (slot order)**: Çuvaşça isimde ekler hangi sırayla gelir? KÖK + [ÇOĞUL] + [İYELİK] + [HAL] sırası Çuvaşça için doğru mu, yoksa farklı mı (ör. iyelik-hal etkileşimi, pronominal n)? Sonlu durum makinesi için bu kritik.
C5. **Tam örnek paradigma**: yaygın bir isim (ör. "ҫын" = insan, ya da "кӗнеке" = kitap) için tekil/çoğul × tüm haller × iyelik tablosunun tamamı (Kiril + Latin + Türkçe anlam).
C6. Sıfatlar, zamirler (kişi/işaret/soru), sayılar (asıl + sıra sayı ekleri) ve bunların morfolojik özellikleri.

### BÖLÜM D — Fiil (verbal) morfolojisi
D1. **Zaman/kip sistemi**: Çuvaşça'nın tüm fiil zamanları ve kipleri. En azından: şimdiki/geniş, geçmiş (belirli `-рӗ` / kategorik, ve belirsiz/sonuç `-нӑ`), gelecek, koşul/şart, emir/buyruk, istek/optatif, gereklilik, vb. HER biri için ek biçimleri ve **6 şahıs çekimi**.
D2. **Şahıs ekleri**: zamana göre değişen şahıs/sayı işaretleyicileri.
D3. **Olumsuzluk (negation)**: Çuvaşça olumsuzluk nasıl yapılır (ör. `-ма/-ме`, `мар`, özel olumsuz fiil çekimleri)? Türkmence'de olumsuzluk üç stratejiyle (sentetik/kaynaşık/analitik) yapılıyordu — Çuvaşça'da kaç strateji var, hangileri?
D4. **Çekimsiz/yarı-çekimli biçimler (non-finite)**: mastar (`-ма/-ме`), sıfat-fiiller (participle: geçmiş/şimdi/gelecek), zarf-fiiller (converb/gerund) — tam liste, ekler, örnekler.
D5. **Çatı (voice)**: ettirgen (causative), edilgen (passive), işteş (reciprocal), dönüşlü (reflexive) ekleri ve üst üste binmesi (stacking).
D6. **Görünüş/yardımcı fiil yapıları** (aspect/auxiliary): Çuvaşça'da yaygın birleşik fiil/yardımcı fiil kalıpları.
D7. **Ek sıralaması**: Fiilde KÖK + [ÇATI] + [OLUMSUZ] + ZAMAN/KİP + [ŞAHIS] sırası doğru mu? Sonlu durum makinesi için netleştir.
D8. **Tam örnek paradigma**: yaygın bir fiil (ör. "кил-" = gelmek, "пар-" = vermek) için tüm zamanlar × 6 şahıs × olumlu/olumsuz tablosu (Kiril + Latin + Türkçe).

### BÖLÜM E — Türetim (derivational) morfolojisi
E1. Üretken türetme ekleri: isimden-isim, isimden-sıfat, isimden-fiil, fiilden-isim, fiilden-fiil, sıfat türetimi. En yaygın 15–25 türetme ekini örneklerle listele (Türkmence sistemde -lI, -lIk, -sIz, -çI, -dAş gibi eklerin Çuvaşça karşılıkları neler?).

### BÖLÜM F — Mevcut hesaplamalı kaynaklar & sözlük/corpus envanteri (EN KRİTİK BÖLÜM)
Bu bölüm, hem sözlük derlememizi besleyecek hem de bildirinin "Related Work" ve karşılaştırma tablosunu oluşturacak. **Her kaynak için: ad, URL, boyut (giriş/cümle sayısı), format, LİSANS, erişim yöntemi (API/scrape/indirme), güncellik ve kullanışlılık değerlendirmesi.**

F1. **Apertium `apertium-chv`**: var mı, lexicon/stem sayısı, kapsamı, lexc/twolc formatı, lisansı, GitHub yolu, bilinen kapsama oranı. (Türkmence makalesinde Apertium-tuk bir karşılaştırma temeliydi — Çuvaşça için eşdeğeri bul.)
F2. **Wiktionary Çuvaşça lemmaları**: `en.wiktionary.org/wiki/Category:Chuvash_lemmas` (ve `ru.wiktionary`, `cv.wiktionary`) kaç lemma içeriyor, POS dağılımı, nasıl çekilir (MediaWiki API), lisans (CC BY-SA).
F3. **Hunspell / yazım denetimi sözlüğü**: Çuvaşça için bir Hunspell (.dic/.aff) veya benzeri yazım sözlüğü var mı (LibreOffice/Mozilla)? Boyut, format, lisans.
F4. **Corpus kaynakları (değerlendirme corpusu için)**:
   - **Çuvaş Ulusal Korpusu** (corpus.chv / "Чӑваш чӗлхин корпусӗ") — boyut, erişim, lisans.
   - HuggingFace üzerindeki Çuvaşça veri kümeleri (ör. ~3,9M cümlelik tek dilli korpus; Çuvaşça-Rusça ~1,4M paralel; Çuvaşça-İngilizce ~200K). Tam adlar, linkler, lisanslar.
   - Çuvaşça **Wikipedia** dökümü (boyut, indirme).
   - Çuvaşça haber siteleri / resmî yayınlar (Türkmence'deki metbugat.gov.tm muadili — değerlendirme corpusu kaynağı olabilecek, taranabilir Çuvaşça haber/metin siteleri).
F5. **Sözlükler (kök kaynağı + altın standart doğrulama referansı)**:
   - **Aşmarin'in 17 ciltlik Çuvaşça Sözlüğü (Ашмарин, Thesaurus Linguae Tschuvaschorum)** — dijital sürümü var mı?
   - Skvortsov Çuvaşça-Rusça sözlüğü; Çuvaşça-Rusça/İngilizce çevrimiçi sözlükler (**samah.chv**, **chuvash.org**, **en.chuvash.org**, Glosbe).
   - Türkmence projedeki **enedilim.com**'un Çuvaşça muadili olabilecek **otoriter, resmî/akademik bir çevrimiçi sözlük portalı** (altın standart doğrulama için) — hangisi en güvenilir ve makineyle sorgulanabilir?
F6. **Krylov morfolojik sözlüğü / morfoloji veritabanı**: N. Krylov ve "Чувашский корпус" ekibinin morfolojik etiketli kaynakları; samah.org/corpus üzerindeki morfolojik analizörler.
F7. **Universal Dependencies**: Çuvaşça için bir **UD treebank** var mı? (UD_Chuvash). Boyut, etiket seti, morfolojik açıklama — hem değerlendirme hem karşılaştırma için.

### BÖLÜM G — Önceki akademik/hesaplamalı çalışmalar (Related Work)
G1. Çuvaşça morfolojisi üzerine **kural tabanlı / FST / HFST çalışmaları**, tezler, makaleler. Her biri için: yazar, yıl, yöntem (XFST/HFST/lexc-twolc/neural), lexicon boyutu, raporlanan kapsam/başarı, durum (aktif/pasif).
G2. Çuvaşça'yı kapsayan **çok-dilli Türk dili NLP araçları** (ör. TurkicNLP, Apertium Turkic, çok-dilli morfoloji modelleri) ve bunların Çuvaşça performansı/sınırları.
G3. **KARŞILAŞTIRMA TABLOSU** (bildirideki Tablo için doğrudan kullanılabilir): mevcut Çuvaşça morfolojik analiz sistemleri × {teknoloji, lexicon boyutu, çekim kodu sayısı, corpus kapsamı, türetim desteği, kapsam, durum}.

### BÖLÜM H — Türkmence ↔ Çuvaşça farkları (yeniden tasarım rehberi)
H1. Türkmence morfolojik motorunun her bileşeni (fonoloji kuralları, isim hal sistemi, iyelik, çoğul, fiil zaman/kip seti, olumsuzluk stratejileri, çatı, türetim) için, **Çuvaşça'da neyin aynı kalabileceğini, neyin değiştirilmesi gerektiğini, neyin tamamen yeni olduğunu** maddeleyen net bir geçiş haritası. Bu, mühendislik eforunu planlamamız için en değerli çıktı.
H2. **Kiril yazısının** mühendislik sonuçları: tokenizasyon, normalizasyon, harf çevrimi katmanı gerekir mi, sözlük hangi yazıda tutulmalı (Kiril mi, Latin çevrim mi, ikisi birden mi)?

### BÖLÜM I — Risk, kapsam ve uygulanabilirlik
I1. Çuvaşça'da morfolojik analizi **özellikle zorlaştıran** olgular (yoğun morfofonoloji, çok işlevli ekler, eş biçimlilik/homonimi, alıntı katmanları — Rusça etkisi). Bunları öngör.
I2. Bir haftalık yoğun, **yalnızca açık kaynak/serbest kaynaklarla** çalışmaya uygun, gerçekçi bir **asgari uygulanabilir kapsam** önerisi: hangi morfolojik olgular önce modellenmeli (en yüksek corpus getirisi), hangileri ertelenebilir?

---

## 3. KAYNAK ÖNCELİĞİ VE GÜVENİLİRLİK
- Önceliğin: (1) hakemli akademik kaynaklar ve dilbilgisi gramerleri, (2) Apertium/HFST gibi yerleşik açık kaynak NLP projeleri, (3) resmî/akademik Çuvaş dil kurumları ve sözlükleri, (4) Wikimedia (Wiktionary/Wikipedia) ve kürasyonlu veri kümeleri.
- **Rusça ve İngilizce** kaynakları mutlaka tara (Çuvaş dilbilimi literatürünün çoğu Rusçadır). Gerektiğinde Çuvaşça kaynakları da kullan.
- Her olgusal iddianın yanına **kaynak (URL + erişim tarihi)** koy. Lisans bilgisi **olmazsa olmaz** — sözlük kaynaklarını kullanabilmemiz lisansa bağlı.
- Çelişen bilgi varsa (ör. hal sayısı kaynaklara göre değişir) bunu **açıkça belirt** ve baskın görüşü işaretle.

## 4. ÇIKTI BİÇİMİ (rapor / PDF)
- Dil: **Türkçe** (teknik terimler İngilizce parantezle). Ama dilbilgisi örneklerini **mutlaka** üç sütunlu ver: **Çuvaşça (Kiril) · Latin harf çevrimi · Türkçe anlam/gloss**.
- Yapı: yukarıdaki A–I bölümlerini başlık başlık izle. Bol **tablo** kullan (özellikle hal, iyelik, fiil paradigmaları ve kaynak envanteri tabloları).
- Sonunda: (a) **kaynak envanteri özet tablosu** (kaynak · tür · boyut · lisans · URL · kullanım rolü), (b) **tam kaynakça** (çalışan URL'lerle), (c) **"Türkmence→Çuvaşça yeniden tasarım haritası"** özet tablosu, (d) **bir haftalık asgari uygulanabilir kapsam** önerisi.
- Uzunluk hedefi: kapsamlı (kısa tutma); her bölüm somut örnekler ve kaynaklarla dolu olsun. Boş genellemelerden kaçın; **eyleme dönük, somut, alıntılanabilir** bilgi ver.
- **Doğrulanamayan iddiaları uydurma.** Bir bilgi bulunamıyorsa "kaynak bulunamadı" de.

---

## 5. NİHAİ KONTROL LİSTESİ (raporu teslim etmeden önce kendine sor)
- [ ] Çuvaş hal sisteminin tamamı, ek allomorfları ve örnek paradigmalarıyla verildi mi?
- [ ] Fiil zaman/kip sisteminin tamamı 6 şahıs çekimiyle ve olumsuzluğuyla verildi mi?
- [ ] Rotasizm/lambdasizm ve Kiril yazısı (4 özel harf) net açıklandı mı?
- [ ] Fonoloji kuralları (ünlü uyumu, ünsüz değişimi, indirgenmiş ünlü düşmesi) örneklerle verildi mi?
- [ ] Apertium-chv, Wiktionary, Hunspell, Çuvaş Ulusal Korpusu, HuggingFace veri kümeleri, UD treebank ve otoriter sözlük portalı — hepsi lisans + URL + boyutla envantere alındı mı?
- [ ] Önceki Çuvaşça morfoloji çalışmaları için bir karşılaştırma tablosu çıktı mı?
- [ ] "Türkmence → Çuvaşça yeniden tasarım haritası" tablosu verildi mi?
- [ ] Tüm dilbilgisi örnekleri Kiril + Latin + anlam üçlüsüyle mi?
- [ ] Her olgusal iddianın kaynağı var mı?

> **Hedef:** Bu rapor elime geçtiğinde, hiçbir ek araştırmaya gerek kalmadan Çuvaşça morfolojik motorunu tasarlamaya, sözlüğü derlemeye ve UBMK 2026 bildirisini yazmaya başlayabilmeliyim.
