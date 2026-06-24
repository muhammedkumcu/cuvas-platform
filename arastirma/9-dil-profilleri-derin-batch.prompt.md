# DEEP RESEARCH PROMPT — Türk Dilleri DERİN Profilleri (kol-bazlı BATCH; her batch ayrı çalıştır)

> **Amaç (KÖKEN için):** Her Türk dili için **çok detaylı, atıflı, akademik** profil — tarih, yapı, ilişkiler, dijital güç, apertium/NLP varlığı, ürünler, avantaj/dezavantaj. Bu profiller (i) platformun Dil Profilleri/Tarih/Ekosistem modüllerini DOLDURACAK, (ii) mevcut verimizi (canlılık, Joshi, uzaklık, branch) **çapraz-kontrol ederek doğruluğunu/eksiğini/tutarlılığını TEST EDECEK.** Akademik çalışma + (gelecekte) çocuk eğitim portalı için kaynağa sıkı bağlılık ŞART.
>
> **Nasıl kullan:** Aşağıdaki **ORTAK ŞABLON**u her dile uygula. **Tek seferde 20 dil yerine, aşağıdaki BATCH'leri AYRI AYRI deepsearch'te çalıştır** (daha derin sonuç). İstersen bir batch'i tek tek dillere de bölebilirsin. Her kayıt: **kaynak/URL + lisans + atıf**; uydurma YOK; bulunamayan = "kaynak bulunamadı"; tartışmalı = işaretle.

## ORTAK ŞABLON (her dil için)
1. **Kimlik:** ad (yerli/İngilizce/Türkçe), ISO 639-3, kol/alt-grup, konuşulduğu yer, yazı sistem(ler)i (tarihsel + güncel).
2. **Konuşur & canlılık:** konuşur sayısı (kaynak + tarih), Glottolog **AES** + Ethnologue **EGIDS** + UNESCO durumu, aktarım/tehlike. (Bizim verimizle karşılaştır.)
3. **Tarih:** kökeni, proto-Türkçeden ayrılışı, tarihsel dönemler, yazı geçmişi (alfabe değişimleri), kilit tarihsel metinler/sözlükler.
4. **Yapı (dilbilimsel özgünlük):** fonoloji (ünlü/ünsüz envanteri, ünlü uyumu tipi, özgün sesler), morfoloji (çekim özellikleri, bu dili ayıran morfotaktik — örn. Çuvaş Kök+İyelik+Çoğul+Hâl), sözdizimi, özgün/arkaik özellikler.
5. **İlişkiler:** en yakın akraba dil(ler), karşılıklı anlaşılabilirlik (kaynak), areal/temas etkileri (komşu dillerden).
6. **Dijital/NLP gücü:** **Joshi sınıfı (0-5)**, **apertium FST** olgunluğu (analyzer/generator/çeviri çiftleri, kapsam %), HuggingFace/açık modeller (LLM/BERT/ASR/TTS), korpus (tek-dilli/paralel), açık sözlük/UD ağaç bankası, bölgesel projeler. **Ürünler + avantaj + dezavantaj/eksik.**
7. **KÖKEN test notu:** bu dil için bizim gösterdiğimiz veriyle (varsa) çelişki/eksik var mı; eklememiz gereken kilit şey.
8. **Sade özet:** çocuk/öğrenci için 2-3 cümle + "bu dili özel/önemli kılan ne".

## BATCH'LER (her birini AYRI çalıştır)

### BATCH A — Oğuz (Güneybatı)
Türkiye Türkçesi (tur), Azerbaycanca (aze, kuzey/güney), Türkmence (tuk), Gagavuzca (gag), Kırım Tatarcası (crh — Kıpçak etkili Oğuz), Salar (slr), Horasan Türkçesi (varsa).

### BATCH B — Kıpçak (Kuzeybatı)
Kazakça (kaz), Kırgızca (kir), Tatarca (tat), Başkurtça (bak), Karakalpakça (kaa), Karaçay-Balkarca (krc), Kumukça (kum), Nogayca (nog), Kırım Tatarcası (crh — A ile çapraz).

### BATCH C — Karluk (Güneydoğu)
Özbekçe (uzb), Uygurca (uig), (varsa) Ay-Uygur/İli Türki varyantları.

### BATCH D — Sibirya (Kuzeydoğu)
Saha/Yakut (sah), Tuvaca (tyv), Hakasça (kjh), Altayca (alt), Şorca (cjs), Dolganca (dlg), Sarı Uygurca (ybe), Fu-yü Kırgızcası.

### BATCH E — Oğur + Argu + izole/tehlikedeki
**Çuvaşça (chv — ÇEKİRDEK, en derin)**, Halaçça (klj — Argu). Çuvaşçaya özel: Ogur kolu, rotasizm/lambdasizm, İdil Bulgar mirası, Aşmarin sözlüğü, neden "yaşayan tek Ogur dili", paha biçilmezliği.

## Çıktı (her batch)
Dil başına ORTAK ŞABLON doldurulmuş profil + **atıf listesi** + "KÖKEN için düzeltme/ekleme önerileri" + batch sonunda **diller-arası kısa karşılaştırma** (bu kol içi benzerlik/farklar).
