# DEEP RESEARCH — Türk Dilleri & Lehçeleri TAM ENVANTERİ + Sınıflandırma (yatay ölçek temeli)

> **Amaç (KÖKEN için):** Platformu MVP-14'ten **tüm Türk dilleri ve başlıca lehçelerine** genişletiyoruz. Bu prompt, ölçeğin **temel listesini** üretir: harita, dil profilleri, uzaklık ve kognat modüllerinin hepsi bu listeden beslenecek. **Akademik, atıflı, uydurma YOK** — bulunamayan alan "kaynak bulunamadı".

## İstenen: tek bir KAPSAMLI tablo — her satır bir dil/lehçe
Aşağıdaki sütunlarla **mümkün olan tüm Türk dil ve lehçelerini** listele (en az ~35 dil + başlıca lehçeler; standart diller + tehlikedeki/izole + tarihi diller ayrı işaretli):

1. **Ad** (Türkçe / yerli / İngilizce)
2. **ISO 639-3** kodu (yoksa "—")
3. **Glottocode** (Glottolog)
4. **Kol** (Johanson: Oğuz / Kıpçak / Karluk / Sibirya / Oğur / Argu) + **alt-grup** (ör. Kıpçak-Nogay, Sayan, Yenisey, Kuzey/Güney)
5. **Koordinat** (yaklaşık merkez enlem, boylam — harita için)
6. **Konuşur sayısı** (kaynak + tarih)
7. **Canlılık**: Glottolog AES + Ethnologue EGIDS + UNESCO (üçü de)
8. **Yazı sistem(ler)i** (güncel + tarihsel)
9. **Tür**: standart dil / lehçe / tehlikedeki / izole / tarihi-ölü
10. **Bayes ayrılma notu** (varsa, Savelyev & Robbeets 2020 zaman derinliği)

## Kapsanacaklar (eksiksiz olsun)
- **Oğuz:** Türkiye Tü., Azerbaycanca (kuzey/güney), Türkmence, Gagavuzca, Kırım Tatarcası (Oğuz-etkili), Salarca, Horasan Tü., Kaşkayca, Afşarca, Sungur, Urum (varsa).
- **Kıpçak:** Kazakça, Kırgızca, Tatarca, Başkurtça, Karakalpakça, Karaçay-Balkarca, Kumukça, Nogayca, Kırım Tatarcası, Karayca (Karaim), Kırımçak, Baraba.
- **Karluk:** Özbekçe (kuzey/güney), Uygurca (+ Lopnor), Eynu (Ainu), İli Türki, Çağatayca (tarihi).
- **Sibirya:** Saha/Yakut, Dolganca, Tuvaca, Tofaca, Hakasça, Şorca, Altayca (kuzey/güney), Çulımca, Sarı Uygurca (Batı Yugur), Fu-yü Kırgızcası.
- **Oğur:** Çuvaşça (+ İdil Bulgarcası, Hazarca — tarihi).
- **Argu:** Halaçça.
- **Tarihi/ölü:** Eski Türkçe (Orhun), Eski Uygurca, Karahanlı, Harezm, Kıpçak (Codex Cumanicus), Kuman.

## Çıktı
Tek tablo + her hücre kaynaklı; sonda **kısa atıf listesi**. Tartışmalı sınıflandırmaları (Salar, Sarı Uygur, Kırım Tatar geçişken, Fu-yü) işaretle. **KÖKEN notu:** mevcut 14-dil verimizle (chv·tur·aze·tuk·kaz·kir·tat·bak·uig·sah·tyv·kjh·shor·klj) çelişki/eksik var mı.
