# DERİN ARAŞTIRMA PROMPTU #2 — Düşük Kaynaklı Türk Dilleri için Morfoloji-Temelli NLP + Eğitim/Öğrenme Platformu: Misyon, Boşluk Analizi ve Konumlandırma

> Bu dosyayı bir **deep-research / derin araştırma yapan yapay zekâya** (ChatGPT/Gemini/Perplexity Deep Research) **olduğu gibi** ver. Çıktı: **kaynak açısından zengin, tablo içeren, PDF'e aktarılabilir kapsamlı bir konumlandırma ve literatür raporu.** PDF olarak dışa aktarıp geri ver.

---

## 0. ROL VE BAĞLAM

Sen, **düşük kaynaklı (low-resource) Türk dilleri** üzerine çalışan, hem **Doğal Dil İşleme (NLP)** hem de **eğitim teknolojisi (EdTech / CALL — Computer-Assisted Language Learning)** alanlarında uzman bir araştırmacısın.

### Projenin hikâyesi
Bir ekip daha önce **Türkmence** için kural tabanlı, açık kaynaklı bir morfolojik analiz/üretim sistemi (TurkmenFST) geliştirdi ve **TurkLang 2026**'da yayınladı. O bildirinin temel **motivasyonu** şuydu: *Türk dilleri kritik düzeyde düşük kaynaklıdır; Avrupa dilleri yapay zekâ/NLP alanında hızla ilerlerken bu dillerde düzgün morfolojik motorlar, araçlar ve farkındalık eksiktir.*

Şimdi ekip aynı çalışmayı **Çuvaşça (чӑваш, ISO: chv — Türk dillerinin yaşayan tek Oğur/Bulgar kolu üyesi, tehlike altındaki değerli bir dil)** için yapıyor ve **UBMK 2026 (TurkLang track)** bildirisine hazırlanıyor.

### Kritik strateji değişikliği (bu araştırmanın sebebi)
Türkmence'de mevcut açık kaynak araç (Apertium) **zayıftı**, bu yüzden "daha iyi analizör" katkısı güçlüydü. Ancak Çuvaşça'da **`apertium-chv` çok daha olgun** (25.000+ kök, sofistike iki-seviyeli fonoloji, ~%85 kapsam). Dolayısıyla "apertium'dan daha iyi analizör" iddiası **zayıf**. Bu nedenle ekip **konumlandırmayı değiştiriyor**:

> apertium-chv'yi bir **analiz temeli** olarak kabul edip, onun **sunmadığı** katmana odaklanmak: (1) **morfolojik ÜRETİM (generation) + paradigma** motoru, ve (2) öğrenenleri **eğitebilecek, mümkünse eğlenceli/oyunlaştırılmış, özgün bir interaktif web platformu** — yani Çuvaşça'nın kültürel değerini dijitalde yaşatan bir **öğrenme/öğretme aracı.**

Bu araştırma, bu yeni yönü **kanıta, literatüre ve net bir boşluk analizine** dayandıracak; hem bildirinin **motivasyon/Related Work** bölümlerini besleyecek hem de platformun **özellik ve tasarım** kararlarını yönlendirecek.

---

## 1. ARAŞTIRMANIN AMACI (tek cümlede)

> (a) Düşük kaynaklı Türk dilleri için NLP ve eğitim araçlarına öncelik vermenin **gerekçesini kanıtlarla** ortaya koyan; (b) mevcut Türk dili **morfoloji araçlarını** (özellikle üretim + son-kullanıcı/pedagojik araçlar) envanterleyen; (c) Türkçe ve diğer Türk/azınlık/tehlikedeki diller için **dil-öğrenme/edtech ve oyunlaştırılmış platformları** tarayan; (d) Çuvaşça (ve genel olarak düşük kaynaklı Türk dilleri) için **tam olarak hangi boşluğu doldurduğumuzu** netleştiren; ve (e) **Related Work + venue (konferans/dergi) konumlandırması** sunan kapsamlı bir rapor üret.

---

## 2. ARAŞTIRMA SORULARI (bölüm bölüm — hepsini kapsa)

### BÖLÜM A — Misyon ve Dijital Uçurum (Motivasyon — bildiri girişi için kanıt)
A1. **Kaynak uçurumu:** Yüksek kaynaklı diller (İngilizce, başlıca Avrupa dilleri) ile düşük kaynaklı Türk dilleri arasındaki NLP/LLM kaynak ve performans uçurumunu **sayısal kanıtlarla** belgele. Kaynak önerileri: Joshi vd. "The State and Fate of Linguistic Diversity" (ACL 2020) ve dil "sınıf" taksonomisi; düşük kaynak dil derlemeleri; Türk dilleri NLP anketleri; LoResLM ve benzeri çalıştaylar.
A2. **Neden morfoloji kritik:** Eklemeli (agglutinative) düşük kaynaklı dillerde veri seyrekliği (data sparsity) ve sözlük-dışı (OOV) sorunlarının NLP/LLM performansını nasıl bozduğu; kural tabanlı morfolojinin (analiz + ÜRETİM) bu sorunları neden hafiflettiği.
A3. **Çuvaşça'nın özel durumu:** Çuvaşça'nın **tehlike altındaki dil** statüsü (UNESCO/Ethnologue/Glottolog), konuşucu sayısı eğilimi, nesiller arası aktarım, Rusça baskısı, dijital varlık eksikliği. Dijital dil ölümü (digital language death) ve dil canlandırma (revitalization) teknolojisi bağlamı.
A4. **Farkındalık/savunu:** Tehlikedeki dil teknolojisi hareketleri (ComputEL çalıştayları, ELRA/LREC düşük-kaynak izleri, FirstVoices, Living Tongues vb.) ve bu çalışmaların topluma etkisi. Bu, bizim "neden yapıyoruz" anlatımızı destekleyecek.

### BÖLÜM B — Türk Dilleri Morfoloji Araçları Envanteri (üretim + son-kullanıcı odaklı)
B1. Türk dilleri için mevcut **morfolojik analizör/üreteçlerin** envanteri: Apertium ailesi (chv, tat, kaz, kir, tuk, uzb, kum, bak…), TRmorph, Zemberek, Oflazer/Çöltekin Türkçe araçları, Kazakça/Tatarca/Kırgızca FST'ler, HFST tabanlı projeler, sinirsel morfoloji modelleri. Her biri için: **analiz mi yoksa ÜRETİM (generation) de mi sunuyor**, paradigma üretiyor mu, **son-kullanıcıya paketlenmiş bir araç/web/API var mı**, lisans, durum.
B2. **Boşluk:** Bu araçlardan kaçı (i) erişilebilir **morfolojik üretim + paradigma tablosu**, (ii) **yazım denetimi**, (iii) **son-kullanıcı/öğrenci-dostu arayüz** sunuyor? Özellikle Çuvaşça için bu katman var mı? (Beklenen yanıt: apertium-chv analiz sunar ama üretim/öğrenme aracı olarak paketlenmemiştir — bunu doğrula veya çürüt.)
B3. **Çuvaşça'ya özgü:** `apertium-chv`'nin gerçek olgunluğu, kapsamı, sınırları ve **bilinen eksiklikleri/hataları** (issue'lar, wiki, makaleler). Bizim üretim + öğrenme katmanımızın bunun üzerine ne kattığını netleştirecek somut tespitler.

### BÖLÜM C — Dil-Öğrenme / Eğitim Platformları (büyüme yönü: "C")
C1. **Türkçe ve Türk dilleri öğrenme araçları:** Türkçe öğrenimi için dijital platformlar/uygulamalar; diğer Türk dilleri (Kazakça, Tatarca, Azerice…) ve **azınlık/tehlikedeki diller** için öğrenme araçları. Her biri: hedef kitle, özellikler, morfoloji-farkındalığı, açık kaynak mı, etki.
C2. **Oyunlaştırma (gamification) ve motivasyon:** Dil öğreniminde oyunlaştırmanın (Duolingo-tarzı, puan/rozet/seri, aralıklı tekrar — spaced repetition / SRS) **etkinliğine dair kanıtlar** (akademik). Hangi mekanikler öğrenmeyi gerçekten artırıyor, hangileri yüzeysel?
C3. **Morfoloji-temelli pedagoji:** Eklemeli dillerin morfolojisini öğretmek (paradigma alıştırmaları, ek-analizi ile "bu kelimeyi açıkla", akıllı geri bildirim, yazım denetimini öğrenme aracı olarak kullanma). Morfolojik üreteç/analizörün bir **öğretim motoru** olarak kullanıldığı örnekler (ICALL — Intelligent CALL literatürü).
C4. **Tehlikedeki dil canlandırma araçları:** Topluluk temelli sözlük/öğrenme platformları (FirstVoices, Wikitongues, Mukurtu vb.) ve bunlardan çıkarılacak tasarım dersleri.

### BÖLÜM D — Özgün ve Eğlenceli Eğitim Web Sitesi için Tasarım (HCI)
D1. **Etkileşim tasarımı:** Morfoloji-temelli bir öğrenme sitesi için özgün, ilgi çekici UI/UX desenleri; öğrenci motivasyonunu artıran tasarım ilkeleri; erişilebilirlik.
D2. **Çuvaşça'ya özgü teknik UX:** **Kiril giriş** (klavye/translit), Ӑ/Ӗ/Ҫ/Ӳ karakter desteği, homoglyph sorunları, mobil uyumluluk.
D3. **Teknik yığın önerileri:** Hafif, hızlı, açık kaynak bir web platformu için pragmatik mimari (statik + REST API; Türkmence projedeki Flask/Vercel deneyimiyle uyumlu) ve oyunlaştırma bileşenleri.

### BÖLÜM E — Boşluk Analizi ve Konumlandırma (en kritik çıktı)
E1. **Sentez:** A–D bulgularını birleştirerek, Çuvaşça (ve genel olarak düşük kaynaklı Türk dilleri) için **tam olarak hangi boşluğun** açık kaldığını **net bir cümleyle** ifade et: *"Açık kaynak bir morfolojik ÜRETİM motoru + öğrenenleri eğiten, eğlenceli, özgün bir interaktif platform — Çuvaşça için mevcut değildir."* Bu iddiayı kanıtla veya nüansla.
E2. **Paper-worthy çerçeveleme:** Bunu "sadece bir uygulama" olmaktan çıkarıp **bilimsel katkı** hâline getirecek çerçeveler: (i) morfolojik üretim motoru + değerlendirme, (ii) pedagojik tasarım gerekçesi, (iii) düşük-kaynak dil için yeniden kullanılabilir metodoloji/şablon, (iv) (mümkünse) küçük bir uzman/öğrenci değerlendirmesi.
E3. **Venue haritası:** UBMK 2026 / TurkLang track uygunluğu; ayrıca alternatif/ek mecralar (LREC, ComputEL, EdTech/CALL konferansları, düşük-kaynak NLP çalıştayları) ve her birinin beklentileri.

### BÖLÜM F — Related Work Tablosu (bildiri için doğrudan kullanılabilir)
F1. İki eksende tablo: (1) **Türk dili morfoloji araçları** × {analiz/üretim/paradigma/son-kullanıcı arayüzü/lisans/durum}; (2) **dil-öğrenme platformları** × {dil/oyunlaştırma/morfoloji-farkındalığı/açık kaynak/hedef kitle}. Bizim önerilen sistemi her iki tabloda son satır olarak konumlandır.

---

## 3. KAYNAK ÖNCELİĞİ
- Öncelik: (1) hakemli NLP ve CALL/EdTech literatürü, (2) yerleşik açık kaynak NLP projeleri (Apertium/HFST), (3) tehlikedeki dil teknolojisi kurumları ve çalıştayları, (4) dil-öğrenme etkinliği üzerine ampirik çalışmalar.
- **İngilizce, Rusça ve Türkçe** kaynakları tara. Her olgusal iddiaya **kaynak (URL + erişim tarihi)** ekle. Araçlar için **lisans** belirt.
- Çelişen/eksik bilgide bunu açıkça belirt; "kaynak bulunamadı" demekten çekinme. Uydurma yok.

## 4. ÇIKTI BİÇİMİ (rapor / PDF)
- Dil: **Türkçe** (teknik terimler İngilizce parantezle).
- Yapı: A–F bölümlerini başlık başlık izle; bol **tablo** ve **kanıt-alıntı** kullan.
- Sonunda: (a) **motivasyon kanıt özeti** (uçurumu gösteren 5-10 çarpıcı sayı/bulgu, kaynaklı), (b) **boşluk → katkı** sentez paragrafı, (c) iki **Related Work tablosu**, (d) **venue uygunluk notu**, (e) **tam kaynakça** (çalışan URL'lerle), (f) platform için **somut özellik/tasarım önerileri** listesi.
- Eyleme dönük, somut, alıntılanabilir ol; boş genellemeden kaçın.

## 5. NİHAİ KONTROL LİSTESİ
- [ ] Dijital uçurum sayısal kanıtlarla gösterildi mi? (yüksek vs düşük kaynak)
- [ ] Çuvaşça'nın tehlikedeki dil statüsü ve önemi kaynaklandı mı?
- [ ] Türk dili morfoloji araçları (üretim/son-kullanıcı ekseniyle) envanterlendi mi?
- [ ] apertium-chv'nin olgunluğu ve sınırları somut belgelendi mi?
- [ ] Dil-öğrenme/oyunlaştırma etkinliği akademik kanıtla ele alındı mı?
- [ ] Morfoloji-temelli pedagoji (ICALL) örnekleri verildi mi?
- [ ] Net "boşluk → bizim katkı" cümlesi kuruldu mu?
- [ ] İki Related Work tablosu + venue haritası var mı?
- [ ] Tüm iddiaların kaynağı + araçların lisansı var mı?

> **Hedef:** Bu rapor elime geçtiğinde, (1) bildirinin motivasyon ve Related Work bölümlerini güçlü kanıtlarla yazabilmeli, (2) Çuvaşça öğrenme platformunun hangi boşluğu doldurduğunu net savunabilmeli, ve (3) platformun özellik/tasarım yol haritasını kanıta dayalı çizebilmeliyim.
