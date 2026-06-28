# İnceleme Yöntemi — kullanıcı tarzının analizi + geliştirme önerisi

> R7 (28 Haz). Kullanıcının (Muhammed Kumcu) sayfa-sayfa inceleme tarzını çözümler ve
> ileriki turlar için sistematik bir **inceleme çerçevesi** önerir. Amaç: incelemenin
> "rastgele göze çarpan" yerine **kapsamlı + tekrarlanabilir** olması.

---

## 1) Kullanıcının inceleme tarzı — gözlenen kalıplar

Kullanıcı 27-28 Haziran'da uygulamayı **ekran ekran**, **ekran görüntüsü üzerinden** inceledi ve
~30 maddelik geri bildirim verdi. Çıkan kalıplar:

1. **Ekran-görüntüsü güdümlü, somut.** Soyut "şurası güzel değil" yerine ekran görüntüsündeki
   tam öğeyi işaret eder (ör. "sağ üstteki Karşılaştır butonu olmasın", "haritada İstanbul Boğazı
   kara gözüküyor"). → Geri bildirim **eyleme dönüştürülebilir**.
2. **Kaynak takıntısı (en güçlü ilke).** "deepsearch kaynak değil; o PDF'lerin içindeki gerçek
   kaynakları yaz." Her veri/iddia **adıyla anılan akademik bir kaynağa** bağlanmalı. Uydurma =
   kırmızı çizgi.
3. **Robotik dilden nefret.** "'ad ya da kola göre filtrele' — bunun başlıkta ne işi var?" Başlıklar
   **temiz isim tamlaması** olmalı, talimat değil. Metinler doğal, insan Türkçesi.
4. **Tek-ekran / tutarlılık.** Aynı işi yapan iki ekran ("o sayfa nasıl hâlâ yaşıyor?"), tutarsız
   bold/italik, farklı nokta boyutları → hepsi gürültü. **Bir iş = bir ekran, bir standart.**
5. **Açıklama beklentisi (meraklı öğrenen).** Her sayfa "bu nedir / neyi gösterir / neden önemli"
   demeli (R-AÇIKLAMA bu istekten doğdu). Hem çocuğa hem araştırmacıya hitap.
6. **Dürüstlük > doluluk.** Ölü/küçük dillerde bilgi yoksa **boş bırak** (uydurma); ama kaynak
   bulunabiliyorsa **araştır ve doldur** ("ölü diller neredeyse hiç bilgi yok → güçlü deepsearch yaz").
7. **Süreç disiplini.** "Sağlam todolist kur, adım adım ilerle, sık commit/push, sonunda tüm MD'leri
   güncelle + kısa resume promptu ver." İzlenebilirlik ve devamlılık önemli.
8. **Önce onay, sonra büyük iş.** Kapsamlı bir işten önce planı **dürüstçe** anlatmamı ve onay
   beklememi ister; küçük düzeltmeleri doğrudan yapmamı.

## 2) Bu tarzın güçlü yanları
- **Kullanıcı-empatisi yüksek:** gerçek bir ziyaretçi gibi gezer, jargon değil deneyim görür.
- **Akademik bütünlük:** kaynak ve dürüstlük ısrarı, projeyi "demo" olmaktan çıkarıp yayımlanabilir
  kılıyor (UBMK/TurkLang hedefi).
- **Somutluk:** her not tek bir commit'e çevrilebiliyor → düşük belirsizlik.

## 3) Kör noktalar (incelemenin atladıkları)
- **Bakılmayan sayfalar:** Morfoloji Analiz ve Paradigma Gezgini hiç incelenmedi (oysa ürünün
  teknik kalbi). → bkz `sayfa-sayfa-analiz.md`, bu iki sayfayı ben analiz ettim.
- **Erişilebilirlik:** renk-kontrastı, klavye navigasyonu, ekran okuyucu, `alt` metinleri hiç
  konuşulmadı. Çift-kitleli (çocuk dahil) bir üründe önemli.
- **Mobil/dar ekran:** tüm inceleme geniş masaüstünde yapıldı; responsive davranış test edilmedi.
- **Boş/hata durumları:** arama sonuç bulamayınca, API kapalıyken, kelime çözümlenemeyince ne
  oluyor — sistematik bakılmadı.
- **Performans:** 254-kavram Geniş kognat, 47-dil harita gibi ağır görünümlerin yük süresi/akıcılığı.
- **İçerik doğruluğunun denetimi:** metinler "akıcı mı" diye okundu; ama dilbilimsel iddiaların
  **bir uzmanca** doğrulanması (ör. refleks örnekleri) ayrı bir tur ister.

## 4) Önerilen inceleme çerçevesi (gelecek turlar için)

Her sayfa için 6 eksenli sabit kontrol listesi — "göze çarpan"ı sisteme bağlar:

| Eksen | Sorulacak soru |
|---|---|
| **İçerik & doğruluk** | Her iddia kaynaklı mı? Dilbilimsel örnek doğru mu? Uydurma var mı? |
| **Dil & ton** | Başlık temiz isim mi (talimat değil)? Metin doğal Türkçe mi? Robotik kalıp var mı? |
| **Tutarlılık** | Aynı öğe her yerde aynı mı görünüyor (renk/boyut/etiket)? Çift ekran var mı? |
| **Açıklama** | "Bu nedir / neyi gösterir / neden önemli" var mı? Hem çocuk hem araştırmacı anlar mı? |
| **Durumlar** | Boş/hata/yükleniyor/dar-ekran halleri makul mü? |
| **Erişim** | Kontrast, klavye, odak, alt-metin yeterli mi? |

**Süreç kuralı:** her tur → todolist → adım adım + ayrı commit/push → sonunda MD güncelle + resume.
**Karar kuralı:** büyük/geri-dönüşü zor iş → önce planı dürüstçe anlat, onay bekle; küçük düzeltme → doğrudan yap.

## 5) Sonuç
Kullanıcının tarzı **somut, kaynak-odaklı, kullanıcı-empatik** — projenin akademik ciddiyetinin
asıl kaynağı bu. Geliştirme yönü: aynı titizliği **atlanan eksenlere** (bakılmayan sayfalar,
erişilebilirlik, mobil, hata durumları, uzman doğrulaması) de sistematik biçimde taşımak. Yukarıdaki
6-eksenli çerçeve bunu "akılda tutmaya" değil, **kontrol listesine** bağlar.
