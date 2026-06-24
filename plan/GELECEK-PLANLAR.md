# GELECEK PLANLARI (MVP + yatay ölçek SONRASI)

> MVP'yi ve tüm Türk dillerine yatay ölçeği bitirdikten sonra ele alınacak fikirler. Şimdi YAPILMAZ; burada saklanır ki kaybolmasın.

## 1) Çocuk / öğrenci eğitim portalı (★ kullanıcı fikri, onaylı)
**Fikir:** "Öğrenen modu"nu gerçek bir **eğitim portalına** dönüştürmek — siteyi çocuklar/öğrenciler için belirgin biçimde farklılaştıran bir bölüm.
- **Öğrenen modu** (varsayılan, çocuk-dostu): sadeleştirilmiş arayüz, az jargon, **oyunlaştırma** (ICALL alıştırmaları, rozet/seri/SRS — UI'da iskelet zaten var), renkli görsel anlatım, **sanal Kiril/Latin klavye**, sesli okuma, adım adım dersler.
- **Uzman modu** (araştırmacı): ham morfolojik etiketler, kaynak/lisans künyeleri, dışa aktarım (CSV/JSON/CoNLL-U), açık API. *(Şu an öğrenen/uzman anahtarı yalnız Analiz'de ham FST detayını gösterip gizliyor — bu fikir onu anlamlı kılar.)*
- **Neden mantıklı:** vizyonumuzun "çift kitle" ayağının (öğrenen + araştırmacı) öğrenen tarafını gerçekten somutlaştırır; platformu salt referans olmaktan çıkarıp **öğretici** yapar; özellikle tehlikedeki diller için canlandırma değeri.
- **Bağımlılık:** önce MVP morfoloji+karşılaştırma sağlamlaşmalı, sonra yatay ölçek (tüm diller). Ardından bu portal.

## ★ YATAY ÖLÇEK NOTLARI — kaynaktaki tam veriyi açmak (dikey bitince)
> Şu an DİKEY (MVP'yi sağlam+kaliteli) yapıyoruz; aşağıdakiler kaynaklarımızda DAHA FAZLA olan ama bilinçli olarak **bir alt kümesini gösterdiğimiz** yerler. Yatay ölçekte (tüm Türk dilleri + tam veri) açılacak. Buraya çıktıkça ekle.
- **Kognat ağı:** Savelyev'de **254 kavram / 905 kognat seti** var; biz şu an **14 kavram** gösteriyoruz → tümünü aç. (Not: "herhangi yazılan kelime → canlı kognat" APERTIUM'la mümkün değil; kognat tespiti ayrı bir araştırma işi.)
- **Diller:** Apertium'da ~20 Türk dili FST'si hedefimizde; MVP'de **10 dil** canlı. Yatay ölçek = kalan dilleri (tuk, gag, crh, kaa, krc, kum, nog, alt, kjh, tyv, klj…) ekle.
- **Dil profilleri / canlılık:** Glottolog AES **23 dil**, Wikipedia zengin metin **14 dil** → tüm dillere genişlet.
- **Uzaklık matrisleri:** Savelyev **32 dil**; biz **10 dil** gösteriyoruz → matrisleri tam set için aç.
- **Harita:** **14 dil** koordinatı yerleştirildi → tüm dilleri ekle.
- **Anlaşılabilirlik (Lindsay):** sınırlı çift kümesi → kaynak elverdikçe genişlet.
- **Genel ilke:** "kaynağımızda daha fazlası olup belirli bir kısmını gösterdiğimiz" her yer yatay-ölçek adayıdır; UI'da "şu an N gösteriliyor" notu + bu listeye kayıt.

## 2) (yer tutucu) Diğer gelecek fikirleri
- Kullanıcı katkısı / topluluk düzeltmeleri (kognat, çeviri, örnek cümle).
- Apertium'a geri hata-düzeltme katkısı (kullanım arttıkça yüzeye çıkan hatalar).
- Tarihsel metin/yazıt katmanı (Orhun, Dîvân) — derin tarih modülü.
- Mobil uyum / PWA.

> Ekleme: yeni gelecek fikri çıktıkça buraya kaydet.
