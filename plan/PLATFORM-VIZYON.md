# PLATFORM VİZYON & KAVRAM DOKÜMANI
### Türk Dilleri Morfoloji + Karşılaştırma + Araştırma Platformu

> Bu belge platformun **ne olduğunu, kime/neye hizmet ettiğini, hangi modüllerden oluştuğunu ve hangi deneyimi vaat ettiğini** anlatır. Amaç: UI/tasarım geliştirilirken ortak bir "kuzey yıldızı" sağlamak. Tüm içerik, `arastirma/` altındaki 3 derin araştırma derlemesine (#3 eşzamanlı dilbilim, #3b ürün/mühendislik, #4 tarih/sosyokültür/ilişki) dayanır.
> Durum: **kavram/tasarım fazı** — 24 Haziran 2026.

---

## 1. TEK CÜMLEDE

**~20 Türk dilini tek bir çatı altında analiz eden, üreten, karşılaştıran ve tarihiyle birlikte anlatan; hem öğrenenlere hem araştırmacılara hizmet eden, açık kaynak bir dijital atlas ve laboratuvar.**

### Çalışma adı önerileri (UI/marka için — karar senin)
- **Kâşgar / Dîvân** — Kaşgarlı Mahmud'un *Dîvânu Lugâti't-Türk*'üne (ilk karşılaştırmalı Türk dilleri atlası, ~1075) saygı duruşu; tam da bizim yaptığımız işin tarihsel atası.
- **Lir–Şaz** — Türk dillerinin iki ana kolu (Oğur/Lir & Ortak/Şaz); dilbilimsel ama akılda kalıcı.
- **Türkik Atlas** / **Türk Dilleri Gözlemevi** / **Orhun** — daha düz/tanımlayıcı seçenekler.

---

## 2. VİZYON

> **Türk dil dünyasının tek noktadan keşfedildiği, öğrenildiği ve takip edildiği açık dijital merkez olmak.**

Bir kullanıcı — ister meraklı bir öğrenci, ister sahada çalışan bir Türkolog — bu siteye geldiğinde; bir Türk dilini **çözümleyebilmeli**, başka bir Türk diline **çevirebilmeden** ama **karşılaştırabilmeli**, bir kelimenin diğer dillerdeki **kökteşlerini ve neden öyle değiştiğini** görebilmeli, dillerin **tarihini, akrabalığını ve birbirine uzaklığını** farklı pencerelerden okuyabilmeli ve tüm bunları **kaynağıyla** alabilmelidir.

---

## 3. MİSYON (somut amaçlar)

1. **Dijital kapsayıcılık:** Düşük kaynaklı ve tehlikedeki Türk dillerine (Çuvaş, Saha, Tuva, Hakas, Altay, Şor, Halaç…) dijital yaşam alanı açmak. Birçoğu Joshi (2020) ölçeğinde **Sınıf 0–1** — "fiziksel ölümden önce dijital ölüm" riski altında. Platform bunları **görünür** kılar.
2. **Parçalılığı bitirmek:** Bugün her dilin verisi/aracı ayrı yerde (apertium, UniMorph, UD, WALS, Glottolog, sözlükler…). Platform bunları **tek arayüzde** birleştirir.
3. **Olgun aracı yeniden icat etmemek, erişilebilir kılmak:** Apertium FST'leri (analiz + üretim) zaten güçlü ama CLI/MT odaklı. Biz üstüne **pedagoji + karşılaştırma + araştırma** katmanı koyarız.
4. **Araştırmacının ilk uğrağı olmak:** Türk dilleri üzerine çalışan/araştırma yapan/test etmek isteyen birinin işini **gerçekten kolaylaştıran**, "literatür karşısındaymış gibi" hissettiren bir merkez.
5. **Akademik dürüstlük:** Her iddia **kaynaklı**, her veri **lisanslı**, tartışmalı konular **"tartışmalı" etiketli**. Uydurma yok.

---

## 4. PROBLEM / NEDEN GEREKLİ (literatürdeki boşluk)

- **Kaynak parçalılığı:** Veri/araçlar dağınık; diller-arası tek-noktadan karşılaştırmalı sorgu yok.
- **Yazı/transliterasyon kakofonisi:** Özbekçe `Oʻ/Gʻ` ters-apostrof kaosu, Uygurca RTL Arap (UEY), Başkurt `ҙ/ҫ`, Çuvaş `Ӑ/Ӗ/Ҫ/Ӳ` — veri setlerini kirletir, çapraz sorguyu engeller.
- **Düşük-kaynak körlüğü:** Sınıf 0 diller (Şor, Salar, Dolgan…) için neredeyse hiç yapılandırılmış veri yok.
- **Pedagojik araç yokluğu:** Türk dilleri morfolojisini **öğreten**, oyunlaştıran, karşılaştırmalı gösteren bir öğrenme platformu yok.
- **"Tek pencere" yanılgısı:** Akrabalık tek bir ağaç değildir; soy, coğrafya, tipoloji, anlaşılabilirlik ve genetik **farklı haritalar** üretir — bunu bir arada gösteren araç yok.

---

## 5. HEDEF KİTLELER

### 5.1 Öğrenenler (çocuklar, öğrenciler, meraklılar)
- **İhtiyaç:** sezgisel keşif, görsellik, oyunlaştırma, "bu kelime neden böyle?" cevabı, az teknik jargon.
- **Değer önerisi:** renkli morfem analizi, paradigma gezgini, kognat ağı, animasyonlu ses-denkliği açıklayıcısı, boşluk-doldurma alıştırmaları, sanal klavye. **"Öğrenen modu"** varsayılan.

### 5.2 Araştırmacılar / akademisyenler (KRİTİK kitle)
- **İhtiyaç:** birleşik arama, diller-arası karşılaştırmalı sorgu, toplu analiz/üretim, **dışa aktarım** (CSV/JSON/CoNLL-U), **açık API**, lisans şeffaflığı, alıntılanabilir kalıcı bağlantılar, tekrarlanabilirlik, "literatür/veri gözlemevi".
- **Değer önerisi:** "literatür karşısındaymış gibi" tek nokta; sahada en çok zorlandıkları işleri (parçalı veri, transliterasyon, düşük-kaynak diller) çözen araçlar. **"Uzman modu"** ile ham etiketler, kaynaklar, lisanslar, indirme.

### 5.3 Dil toplulukları & canlandırma (ikincil ama anlamlı)
- **İhtiyaç:** kendi dillerinin görünürlüğü, doğru temsil, öğretim materyali.
- **Değer önerisi:** tehlikedeki dillere eşit/öncelikli yer; kültür kartları; topluluk katkısına açıklık.

---

## 6. TEMEL İLKELER (tasarım & içerik bunlardan çıkar)
1. **Açık & kaynaklı** — her veri kaynağı + lisansıyla; "uydurma yok".
2. **Apertium = motor, rakip değil** — üstüne değer (pedagoji, karşılaştırma, erişim) katarız; bulunan hatalar upstream'e geri katkı.
3. **Tehlikedeki dile öncelik** — büyük diller kadar küçük diller de görünür; canlılık ön planda.
4. **Çift kitle, iki mod** — aynı veri, "öğrenen" ve "uzman" görünümleri.
5. **Çoklu yazı yerlidir** — "tek alfabe" varsayımı yok; her dilin kendi envanteri + ortak gösterim arasında çift yönlü eşleme.
6. **Düzenli farklılık** — diller "aynı" değil, **kurallı biçimde farklı**; platform bu düzeni öğretir.
7. **Genişleyebilirlik** — yeni dil = veri + FST eklemek; yeni modül = takılabilir.

---

## 7. PLATFORM DENEYİMİ — MODÜLLER

> Her modül: **ne yapar · kimin için · hangi veriyle**. (Veri: #3=eşzamanlı dilbilim, #3b=mühendislik, #4=tarih/ilişki, apertium=FST.)

### A. Morfolojik Analiz & Üretim *(MVP çekirdeği)*
- **Ne:** Bir kelime gir → kök + morfolojik etiketler (analiz). Kök + etiket seç → yüzey biçim (üretim). 20 dil (MVP'de 10).
- **Kim:** İkisi de. **Veri:** apertium `automorf`/`autogen` FST.

### B. Paradigma Gezgini
- **Ne:** Bir kök için tam çekim tablosu (hal × sayı × iyelik; fiil için zaman/kip × kişi). Renkli morfemler.
- **Kim:** Öğrenen + araştırmacı. **Veri:** apertium `autogen` + UniMorph hizalama.

### C. Kognat Ağı (Cognate Graph)
- **Ne:** Bir kavram/kök gir → diğer Türk dillerindeki kökteşleri **düğüm-grafik** olarak; kognat boşlukları (ödünçleme/farklı kök) işaretli.
- **Kim:** İkisi de. **Veri:** SavelyevTurkic CLDF (32 dil/254 kavram/905 set, CC BY 4.0) + NorthEuraLex (CC BY 4.0) + #3 kognat tabloları.

### D. Ses-Denkliği Açıklayıcısı (Sound Correspondence Engine)
- **Ne:** "Neden Türkçe *ayak*, Çuvaşça *ura*, Yakutça *atax*?" → Ana Türkçe biçimden her kola **animasyonlu** harf-dönüşüm rotası. Rotasizm (z→r), lambdasizm (ş→l), *d/t/y/z, *h-, *g/ğ/v/w.
- **Kim:** Öğrenen (görsel) + araştırmacı (makine-okunur kural). **Veri:** #3/#3b kural iskeletleri.

### E. Çok-Boyutlu Uzaklık Gezgini *(yıldız özellik)*
- **Ne:** İki/çok dil seç → aralarındaki uzaklığı **farklı eksenlerde** göster: filogenetik · leksikostatistik (Swadesh %) · karşılıklı anlaşılabilirlik (asimetrik) · tipolojik · coğrafi. **Radar grafik / ağ görünümü.** "Çuvaşça–Tatarca coğrafi komşu (0.02) ama leksikal yabancı (35)" gibi çelişkileri anlatır.
- **Kim:** İkisi de. **Veri:** #4 Bölüm J matrisleri (J.1–J.3) + #3 fonetik mesafe.

### F. Dil Profili Sayfaları
- **Ne:** Her dil için: adlandırma, coğrafya, tarih, ilk tanıklık, edebî gelenek, standart/diyalekt, konuşur sayısı, resmî statü, canlılık, yazı tarihi, **kültür kartı** (din + destan).
- **Kim:** İkisi de. **Veri:** #4 Bölüm C/D/E/H + 20-dil profil matrisi.

### G. Tarih Haritası + Zaman Çizelgesi
- **Ne:** İnteraktif harita + kronoloji: Göktürk→Uygur→Karahanlı→Altın Orda→Çağatay→Osmanlı→Sovyet alfabe reformları→1991→bugün; her olay **dilsel sonucuyla**.
- **Kim:** İkisi de (öğrenen için hikâye, araştırmacı için kaynak). **Veri:** #4 Bölüm B/D/K.

### H. Canlılık / Tehlike Isı-Haritası
- **Ne:** Haritada her dil EGIDS + Joshi sınıfına göre renklenir (kırmızı=tehlikede). Dil politikası bağlamı (2018 RF yasası vb.).
- **Kim:** İkisi de + topluluklar. **Veri:** #4 Bölüm E.

### I. Genetik-vs-Dil Mit Kırıcı
- **Ne:** "Dil ailesi = ırk mı?" sorusuna **bilimsel, şovenizmden arınmış** bilgi kutusu (Yunusbayev 2015: dil = elit baskınlığı/dil değiştirme, gen değil).
- **Kim:** İkisi de. **Veri:** #4 Bölüm I (dikkatli çerçeveleme, uyarı kutuları).

### J. ICALL — Oyunlaştırılmış Öğrenme
- **Ne:** Boşluk-doldurma + FST-üretimli çeldirici; doğru paradigmayı seçme; SRS (aralıklı tekrar); puan/rozet.
- **Kim:** Öğrenen. **Veri:** apertium üretim + paradigma.

### K. Araştırmacı Merkezi *(misyon kritik)*
- **Ne:** Birleşik sorgu (bir kök → eşzamanlı çekim + transliterasyon + kognat ağacı) · toplu analiz/üretim · **dışa aktarım** (CSV/JSON/CoNLL-U) · **açık REST API** + dokümantasyon · lisans şeffaflığı · alıntılanabilir bağlantılar.
- **Kim:** Araştırmacı. **Veri:** tüm katmanlar + API.

### L. Çoklu Yazı + Transliterasyon + Sanal Klavye *(çapraz-kesen)*
- **Ne:** Kiril/Latin/Arap arası tek-tık çevrim (Ortak Türk Alfabesi'ne normalize); RTL desteği; dile özgü sanal klavye; (sona saklanan) homoglyph/karışık-yazı normalizasyonu.
- **Kim:** İkisi de. **Veri:** turkicnlp transliterator + #3b script-katman notları.

---

## 8. İKİ MOD (aynı veri, iki görünüm)
- **Öğrenen Modu (varsayılan):** sade, görsel, az jargon; renkli morfemler, animasyon, oyun, ipuçları.
- **Uzman/Araştırmacı Modu:** ham morfolojik etiketler, kaynak künyeleri, lisanslar, indirme/dışa aktarım, API erişimi, çekirdek/genişletilmiş ayrımları (`core_cases`/`extended_cases`).
- Geçiş tek anahtarla; UI bunu baştan öngörmeli.

---

## 9. KAPSAM: MVP vs TAM VİZYON
- **MVP (ilk sürüm):** **10 dil** (tur, aze, kaz, kir, uzb, uig, tat, bak, chv, sah — 5 kolu da kapsar) + **morfoloji çekirdeği** (Modül A/B) çalışan backend. Diğer modüller veriyle kademeli eklenir.
- **Tam vizyon:** ~20+ dil (Gagavuz, Kırım Tatar, Karakalpak, Kumuk, Karaçay-Balkar, Nogay, Altay, Hakas, Tuva, Halaç, Şor, Salar, Dolgan, Karaim…) + tüm modüller + araştırmacı API + ICALL.

---

## 10. TEKNİK BAĞLAM (UI'nin bilmesi gerekenler)
- **Backend:** Python **FastAPI**, **Linux VM'de** çalışır (apertium Windows'ta derlenmez). UI ona **JSON REST API** ile konuşur.
- **Veri:** yapısal depo (MVP'de SQLite → sonra Postgres); her kayıt **kaynak + lisans** alanlı; `core_cases`/`extended_cases`; her dile **script + fonolojik normalizasyon katmanı**.
- **Dil kodları:** ISO (chv, tur, aze, tuk, gag, crh, tat, bak, kaz, kir, kaa, krc, kum, nog, uzb, uig, alt, kjh, tyv, sah, klj…).
- **Yazı:** UI çoklu-script + RTL (Arap/UEY) + özel Kiril karakterleri desteklemeli; transliterasyon backend'den gelir.
- **Açık API:** araştırmacıların programatik erişimi baştan tasarıma dahil.

---

## 11. UI İÇİN SOMUT EKRAN HARİTASI (tasarımına doğrudan girdi)
1. **Ana sayfa / keşif:** arama kutusu (kelime veya kavram) + dil seçimi + harita; "öğrenen/uzman" modu anahtarı.
2. **Analiz sonucu:** kelime → morfem dökümü (renkli) + lemma + etiketler; "uzman" görünümünde ham tag + kaynak.
3. **Paradigma sayfası:** kök + dil → tam çekim tablosu; dil değiştir/çoklu-dil karşılaştır.
4. **Karşılaştırma çalışma alanı:** birden çok dil yan yana — kognat ağı / ses-denkliği / paradigma sekmeleri.
5. **Uzaklık gezgini:** dil seç → radar/ağ; eksen anahtarları (filogenetik/leksikal/anlaşılabilirlik/coğrafi).
6. **Dil profili:** uzun-form sayfa + kültür kartı + canlılık rozeti + yazı-tarihi şeridi.
7. **Tarih haritası/zaman çizelgesi:** kaydırılabilir kronoloji + harita katmanı.
8. **Araştırmacı paneli:** birleşik sorgu + toplu işlem + dışa aktarım + API dokümanı.
9. **Çapraz öğeler:** sanal klavye, transliterasyon anahtarı, kaynak/lisans rozetleri, alıntı/paylaş bağlantısı.

---

## 12. GÖRSEL KİMLİK İPUÇLARI (öneri, bağlayıcı değil)
- **Motifler:** ağ/grafik (kognat & uzaklık), harita (coğrafya/yayılım), zaman şeridi (tarih), morfem-blokları (renkli ekler).
- **Renk:** dil kollarına renk paleti (Oğuz/Kıpçak/Karluk/Sibirya/Oğur/Argu); canlılık için ısı-skalası.
- **Ton:** hem bilimsel-güvenilir hem davetkâr-keşifsel; "atlas + laboratuvar".
- **Yazı:** çok-script font yığını (Latin + Kiril özel harfler + Arap); okunabilirlik öncelikli.

---

## 13. İÇERİK & AKADEMİK DÜRÜSTLÜK
- Her modülde **kaynak künyesi** ve **lisans** görünür/erişilebilir.
- Tartışmalı konular (Altay/Transavrasya makro-akrabalık, köken, genetik) **"tartışmalı"** etiketi + birden çok görüş.
- Genetik-vs-dil ve dil politikası içeriği **tarafsız, siyaset/ırk çıkarımından uzak**.
- Karışık-yazı (Latin breve ↔ Kiril) normalizasyon bulgusu **sona** saklanır (kullanıcı kararı) — özgün NLP nüvesi.

---

> **Sonuç:** Bu platform bir "sözlük" ya da tek bir "çevirici" değil; **soy-ağaç + ses-denkliği + kognat + morfotaktik + tarih + canlılık + çok-yazılı gösterim**in bir arada çalıştığı, çift kitleli bir **atlas ve laboratuvar**dır. UI bu vizyonu — özellikle "iki mod", "çoklu yazı" ve "karşılaştırma/uzaklık görselleştirmeleri"ni — baştan öngörmelidir.
